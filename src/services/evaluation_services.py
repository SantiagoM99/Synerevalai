# src/services/evaluation_service.py

import openai
from bert_score import score
from prometheus_eval.vllm import VLLM
from prometheus_eval import PrometheusEval
from prometheus_eval.prompts import ABSOLUTE_PROMPT, SCORE_RUBRIC_TEMPLATE
from prometheus_eval.litellm import LiteLLM, AsyncLiteLLM

# ---------------------------------------------------------------------------------
# EJEMPLO: Podrías tener un logger, settings, etc. que vivan en src/config/settings.py
# from src.config.settings import settings
# openai.api_key = settings.OPENAI_API_KEY
# ---------------------------------------------------------------------------------

# ---------- Función 1: Evaluación con modelo de OpenAI ----------
def evaluate_with_openai(model_response: str, reference: str) -> float:
    """
    Evalúa una respuesta generada frente a una referencia usando un prompt con OpenAI.
    Retorna una puntuación numérica.
    """
    prompt = (
        f"Evalúa la siguiente respuesta del modelo comparada con la respuesta de referencia. "
        f"Proporciona una calificación del 1 al 10 considerando coherencia, precisión y completitud.\n\n"
        f"Respuesta del modelo: {model_response}\n"
        f"Respuesta de referencia: {reference}\n\n"
        f"Calificación:"
    )

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=10,
            temperature=0.0,
        )
        score_text = response.choices[0].text.strip()
        score_value = float(score_text)
    except Exception as e:
        print(f"Error en evaluate_with_openai: {e}")
        score_value = 0.0

    return score_value


# ---------- Función 2: Evaluación utilizando BERTScore ----------
def evaluate_with_bertscore(model_responses: list, reference_responses: list) -> dict:
    """
    Evalúa en batch usando BERTScore y retorna los promedios de Precision, Recall y F1.
    """
    try:
        P, R, F1 = score(model_responses, reference_responses, lang="es", verbose=True)
        bert_results = {
            "precision": P.mean().item(),
            "recall": R.mean().item(),
            "f1": F1.mean().item()
        }
    except Exception as e:
        print(f"Error en evaluate_with_bertscore: {e}")
        bert_results = {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    
    return bert_results


# ---------- Componente 3: Evaluación con Prometheus-Eval ----------
def init_prometheus_judge() -> PrometheusEval:
    """
    Inicializa y retorna una instancia del evaluador Prometheus-Eval usando el modelo local.
    """
    # Ajusta el nombre del modelo local a tu conveniencia
    model = LiteLLM("ollama/llama3.2:3b")
    return PrometheusEval(model=model, absolute_grade_template=ABSOLUTE_PROMPT)

# Instancia global de PrometheusEval (para no recargar el modelo en cada petición)
prometheus_judge = init_prometheus_judge()

def evaluate_prometheus(instruction: str, model_response: str, reference: str, rubric: dict) -> tuple:
    """
    Utiliza Prometheus-Eval para realizar una evaluación de calificación absoluta (1 a 5)
    sobre la respuesta del modelo, basado en una rúbrica específica.
    
    Retorna (feedback, score).
    """
    score_rubric = SCORE_RUBRIC_TEMPLATE.format(**rubric)
    
    try:
        feedback, score = prometheus_judge.single_absolute_grade(
            instruction=instruction,
            response=model_response,
            rubric=score_rubric,
            reference_answer=reference
        )
    except Exception as e:
        print(f"Error in evaluate_prometheus: {e}")
        feedback, score = "Error en evaluación Prometheus", 0.0
    
    return feedback, score


# ---------- Función general para evaluar todo ----------
def evaluate_all(
    instruction: str,
    model_responses: list,
    reference_responses: list,
    rubric: dict
) -> dict:
    """
    Evalúa un conjunto de respuestas del modelo utilizando:
      - OpenAI (opcionalmente, si está configurado)
      - BERTScore (batch)
      - Prometheus-Eval (individualmente)
    
    Retorna un dict con resultados.
    """
    # En caso de querer usar evaluate_with_openai, descomenta lo necesario
    openai_scores = []
    prometheus_scores = []

    for model_resp, ref_resp in zip(model_responses, reference_responses):
        # Ejemplo: si quieres usar OpenAI, descomenta
        # openai_score = evaluate_with_openai(model_resp, ref_resp)
        # openai_scores.append(openai_score)

        feedback, score = evaluate_prometheus(instruction, model_resp, ref_resp, rubric)
        prometheus_scores.append((feedback, score))
    
    bert_results = evaluate_with_bertscore(model_responses, reference_responses)
    
    # Promedio de OpenAI (si lo usaste)
    avg_openai = sum(openai_scores) / len(openai_scores) if openai_scores else 0.0

    return {
        "openai_score": avg_openai,
        "bertscore": bert_results,
        "prometheus_score": prometheus_scores
    }

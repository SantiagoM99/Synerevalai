import openai
from bert_score import score
from prometheus_eval.vllm import VLLM
from prometheus_eval import PrometheusEval
from prometheus_eval.prompts import ABSOLUTE_PROMPT, SCORE_RUBRIC_TEMPLATE
from prometheus_eval.litellm import LiteLLM, AsyncLiteLLM
from openai import OpenAI
from ..config.settings import settings
from ..schemas.openai_schemas import EvaluationOutput
import os


def evaluate_with_openai(
    instruction: str, model_response: str, reference: str
) -> EvaluationOutput:
    """
    Evalúa la respuesta generada por el modelo frente a una respuesta de referencia utilizando la instrucción original.

    Esta función calcula una serie de criterios de evaluación (de 1 a 10) junto con una breve explicación para cada uno.
    Los criterios evaluados son:
      - Robustez
      - Exactitud
      - Completitud
      - Legibilidad
      - Coherencia con la instrucción

    Parameters
    ----------
    instruction : str
        La instrucción original utilizada para generar la respuesta del modelo.
    model_response : str
        La respuesta generada por el modelo.
    reference : str
        La respuesta de referencia contra la cual se evalúa la respuesta del modelo.

    Returns
    -------
    EvaluationOutput
        Un objeto JSON estructurado de la siguiente forma:

        {
          "evaluations": {
              "Robustez": {"score": int, "explanation": str},
              "Exactitud": {"score": int, "explanation": str},
              "Completitud": {"score": int, "explanation": str},
              "Legibilidad": {"score": int, "explanation": str},
              "Coherencia": {"score": int, "explanation": str}
          },
          "final_score": int
        }
    """
    prompt = (
        f"Instrucción original: {instruction}\n\n"
        f"Respuesta del modelo: {model_response}\n"
        f"Respuesta de referencia: {reference}\n\n"
        "Evalúa la siguiente respuesta generada por el modelo comparándola con la respuesta de referencia.\n\n"
        "Para cada uno de los siguientes criterios, asigna una puntuación del 1 al 10 y proporciona una breve explicación:\n"
        "  - Robustez\n"
        "  - Exactitud\n"
        "  - Completitud\n"
        "  - Legibilidad\n"
        "  - Coherencia ante la instrucción\n\n"
        "Finalmente, indica una calificación final (sin explicación) que represente la evaluación global.\n\n"
    )

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer",
                    "content": [
                        {"type": "text", "text": "You are a helpful assistant."}
                    ],
                },
                {"role": "user", "content": [{"type": "text", "text": prompt}]},
            ],
            response_format=EvaluationOutput,
        )
        structured_output = completion.choices[0].message.parsed
        return structured_output
    except Exception as e:
        print(f"Error en evaluate_with_openai: {e}")
        return None


def evaluate_with_bertscore(model_responses: list, reference_responses: list) -> dict:
    """
    Evalúa en batch usando BERTScore y retorna los promedios de Precision, Recall y F1.
    """
    try:
        P, R, F1 = score(model_responses, reference_responses, lang="es", verbose=True)
        bert_results = {
            "precision": P.mean().item(),
            "recall": R.mean().item(),
            "f1": F1.mean().item(),
        }
    except Exception as e:
        print(f"Error en evaluate_with_bertscore: {e}")
        bert_results = {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    return bert_results


def init_prometheus_judge() -> PrometheusEval:
    """
    Inicializa y retorna una instancia del evaluador Prometheus-Eval usando el modelo local.

    Esta función crea una instancia del evaluador Prometheus-Eval utilizando un modelo local.
    Se emplea la clase LiteLLM con el identificador del modelo "ollama/llama3.2:3b", el cual se puede ajustar según sea necesario.

    Returns
    -------
    PrometheusEval
        Instancia inicializada de PrometheusEval con el modelo local y la plantilla de calificación absoluta definida.
    """

    model = LiteLLM("ollama/llama3.2:3b")
    return PrometheusEval(model=model, absolute_grade_template=ABSOLUTE_PROMPT)


prometheus_judge = init_prometheus_judge()


def evaluate_prometheus(
    instruction: str, model_response: str, reference: str, rubric: dict
) -> tuple:
    """
    Utiliza Prometheus-Eval para realizar una evaluación de calificación absoluta (1 a 5)
    sobre la respuesta del modelo, basada en una rúbrica específica.

    La evaluación se realiza comparando la respuesta del modelo contra una respuesta de referencia,
    utilizando la instrucción original y formateando la rúbrica de evaluación.

    Parameters
    ----------
    instruction : str
        La instrucción original utilizada para generar la respuesta del modelo.
    model_response : str
        La respuesta generada por el modelo.
    reference : str
        La respuesta de referencia para comparar.
    rubric : dict
        Diccionario que contiene los criterios y lineamientos de la rúbrica de calificación.

    Returns
    -------
    tuple
        Tuple que contiene:
            - feedback (str): Retroalimentación proporcionada por el evaluador.
            - score (float): Calificación absoluta entre 1 y 5.

    Notes
    -----
    Si ocurre algún error durante la evaluación, se imprime un mensaje de error y se retornan valores por defecto.
    """
    score_rubric = SCORE_RUBRIC_TEMPLATE.format(**rubric)

    try:
        feedback, score = prometheus_judge.single_absolute_grade(
            instruction=instruction,
            response=model_response,
            rubric=score_rubric,
            reference_answer=reference,
        )
    except Exception as e:
        print(f"Error in evaluate_prometheus: {e}")
        feedback, score = "Error en evaluación Prometheus", 0.0

    return feedback, score


def evaluate_all(
    instruction: str, model_responses: list, reference_responses: list, rubric: dict
) -> dict:
    """
    Evalúa un conjunto de respuestas del modelo utilizando múltiples métodos de evaluación,
    organizando los resultados por documento. Para cada documento se evalúan:

      - OpenAI: usando `evaluate_with_openai`
      - BERTScore: calculado de forma individual para cada par de respuesta del modelo y respuesta de referencia.
      - Prometheus-Eval: usando `evaluate_prometheus`

    Además, se incluye la respuesta del modelo en cada objeto de evaluación para identificar cada documento.

    Parameters
    ----------
    instruction : str
        La instrucción original usada para generar las respuestas del modelo.
    model_responses : list of str
        Lista de respuestas generadas por el modelo.
    reference_responses : list of str
        Lista de respuestas de referencia para comparar con las respuestas del modelo.
    rubric : dict
        Diccionario con la rúbrica de calificación para la evaluación con Prometheus-Eval.

    Returns
    -------
    dict
        Diccionario con la evaluación por documento con la siguiente estructura:

        {
            "documents": [
                {
                    "model_response": str,
                    "openai_score": EvaluationOutput,
                    "bertscore": {"precision": float, "recall": float, "f1": float},
                    "prometheus_score": {"feedback": str, "score": int}
                },
                ...
            ]
        }
    """
    documents = []

    for model_resp, ref_resp in zip(model_responses, reference_responses):
        openai_score = evaluate_with_openai(instruction, model_resp, ref_resp)

        feedback, prometheus_score = evaluate_prometheus(
            instruction, model_resp, ref_resp, rubric
        )
        bertscore = evaluate_with_bertscore([model_resp], [ref_resp])

        document_result = {
            "model_response": model_resp,
            "openai_score": openai_score,
            "bertscore": bertscore,
            "prometheus_score": {"feedback": feedback, "score": prometheus_score},
        }
        documents.append(document_result)

    return documents

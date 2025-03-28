import pandas as pd
from io import BytesIO
from fastapi import HTTPException
from ..schemas.teacher_evaluation_schemas import TeacherEvaluationRequest
from .evaluation_services import (
    evaluate_with_openai,
    evaluate_with_bertscore,
    evaluate_prometheus
)

def process_teacher_evaluation(file_stream, eval_req: TeacherEvaluationRequest) -> BytesIO:
    """
    Procesa el Excel con las respuestas de los estudiantes y aplica las evaluaciones para cada pregunta.
    
    Se asume que el archivo Excel tiene la siguiente estructura:
      - Primera columna: 'student_name'
      - Luego, cada columna corresponde a una pregunta (en el mismo orden que en reference_responses e instructions)
    
    Retorna un objeto BytesIO que contiene el Excel de salida con, para cada estudiante,
    la evaluación por pregunta (calificación y retroalimentación) y una nota final.
    """
    try:
        df = pd.read_excel(file_stream)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al leer el archivo Excel: {e}")

    # Verificamos que exista la columna del nombre del estudiante
    if "student_name" not in df.columns:
        raise HTTPException(status_code=400, detail="El archivo debe contener una columna 'student_name'.")

    num_questions = len(eval_req.reference_responses)
    # Se asume que las columnas siguientes a 'student_name' corresponden a las respuestas de cada pregunta
    # y que hay exactamente num_questions columnas de respuestas
    student_answers = df.iloc[:, 1:1+num_questions]
    if student_answers.shape[1] != num_questions:
        raise HTTPException(status_code=400, detail=f"Se esperaban {num_questions} preguntas, pero se encontraron {student_answers.shape[1]} columnas de respuestas.")

    # Listas para resultados por estudiante
    results = []

    # Iteramos por cada fila (estudiante)
    for index, row in df.iterrows():
        student_name = row["student_name"]
        question_evaluations = []
        final_scores = []

        # Iteramos por cada pregunta (columna)
        for q in range(num_questions):
            student_answer = row.iloc[q+1]  # asumiendo que las respuestas están en orden
            reference = eval_req.reference_responses[q]
            instruction = eval_req.instructions[q]
            # Prometheus y BERTScore
            prometheus_feedback, prometheus_score = evaluate_prometheus(instruction, student_answer, reference, eval_req.rubric)
            bertscore = evaluate_with_bertscore([student_answer], [reference])

            q_score = prometheus_score

            final_scores.append(q_score)

            question_evaluations.append({
                "question": f"Q{q+1}",
                "student_answer": student_answer,
                "bertscore": bertscore,
                "prometheus_feedback": prometheus_feedback,
                "prometheus_score": prometheus_score,
                "final_question_score": q_score
            })

        # Calificación final del estudiante: promedio de las calificaciones de las preguntas
        final_grade = sum(final_scores) / len(final_scores) if final_scores else 0

        results.append({
            "student_name": student_name,
            "questions": question_evaluations,
            "final_grade": final_grade
        })

    # Convertir los resultados a un DataFrame para exportar a Excel
    # Para simplificar, aplanamos la estructura: una fila por estudiante con columnas para cada pregunta y la nota final.
    output_rows = []
    for res in results:
        row = {"student_name": res["student_name"], "final_grade": res["final_grade"]}
        for q_eval in res["questions"]:
            q = q_eval["question"]
            row[f"{q} final_score"] = q_eval["final_question_score"]
            row[f"{q} prometheus_feedback"] = q_eval["prometheus_feedback"]
            # Puedes incluir más columnas si lo deseas, por ejemplo openai_evaluation, bertscore, cost, etc.
        output_rows.append(row)

    output_df = pd.DataFrame(output_rows)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        output_df.to_excel(writer, index=False)
    output.seek(0)
    return output

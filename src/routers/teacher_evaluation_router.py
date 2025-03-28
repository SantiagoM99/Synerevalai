from fastapi import APIRouter, File, UploadFile, Form, Depends
from fastapi.responses import StreamingResponse
import json
from typing import List
from ..schemas.teacher_evaluation_schemas import TeacherEvaluationRequest
from ..services.teacher_evaluation_services import process_teacher_evaluation

router = APIRouter()

@router.post("/teacher/evaluate")
def teacher_evaluate(eval_req: str, file: UploadFile = File(...)):
    """
    Endpoint para que el profesor suba un Excel con las respuestas de los estudiantes y 
    los parámetros de evaluación (rúbrica, respuestas de referencia, instrucciones, modelos evaluados y tokens usados).

    Se espera que los parámetros se envíen en el body en formato JSON.
    'file' es el Excel con la columna 'student_name' y una columna por cada pregunta.
    
    Retorna un Excel con la evaluación de cada estudiante.
    """
    try:
        eval_req_jsn = TeacherEvaluationRequest(**json.loads(eval_req))
        output_excel = process_teacher_evaluation(file.file, eval_req_jsn)
    except Exception as e:
        return {"error": f"Error al procesar la evaluación: {e}"}

    return StreamingResponse(
        output_excel,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=teacher_evaluation.xlsx"},
    )

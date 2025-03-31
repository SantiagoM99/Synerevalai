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
    Endpoint for the teacher to upload an Excel file with student responses and
    evaluation parameters (rubric, reference answers, instructions, evaluated models, and tokens used).

    Parameters
    ----------
    eval_req : str
        JSON string containing the evaluation parameters.
    file : UploadFile
        Excel file with a 'student_name' column and one column per question.

    Returns
    -------
    StreamingResponse
        An Excel file with the evaluation results for each student.
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

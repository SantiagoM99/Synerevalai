# src/routers/evaluator_router.py

from fastapi import APIRouter
from src.schemas.evaluation_schemas import EvaluationRequest, EvaluationResponse
from src.services.evaluation_services import evaluate_all
from typing import List

router = APIRouter()


@router.post("/evaluate", response_model=List[EvaluationResponse])
def evaluate_endpoint(request: EvaluationRequest):
    """
    Endpoint para evaluar las respuestas de un modelo (POST).
    """
    print("Evaluating model responses...")
    results = evaluate_all(
        instruction=request.instruction,
        model_responses=request.model_responses,
        reference_responses=request.reference_responses,
        rubric=request.rubric,
    )

    return results

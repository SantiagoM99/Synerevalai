# src/routers/evaluator_router.py

from fastapi import APIRouter
from src.schemas.evaluation_schemas import (
    EvaluationRequest, 
    EvaluationResponse
)
from src.services.evaluation_service import evaluate_all

router = APIRouter()

@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate_endpoint(request: EvaluationRequest):
    """
    Endpoint para evaluar las respuestas de un modelo (POST).
    """
    results = evaluate_all(
        instruction=request.instruction,
        model_responses=request.model_responses,
        reference_responses=request.reference_responses,
        rubric=request.rubric
    )
    
    return {
        "openai_score": results["openai_score"],
        "bertscore": results["bertscore"],
        "prometheus_score": results["prometheus_score"]
    }

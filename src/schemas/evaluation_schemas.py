# src/schemas/evaluation_schemas.py

from pydantic import BaseModel
from typing import List, Dict

class EvaluationRequest(BaseModel):
    instruction: str
    model_responses: List[str]
    reference_responses: List[str]
    rubric: Dict[str, str]


class BERTScore(BaseModel):
    precision: float
    recall: float
    f1: float

class EvaluationResponse(BaseModel):
    openai_score: float
    bertscore: BERTScore
    # La respuesta de prometheus es una lista de tuplas (feedback, score).
    # Para simplificar, podríamos representarla como una lista de dicts o algo similar.
    # Aquí haremos una aproximación sencilla.
    prometheus_score: list
from pydantic import BaseModel, Field
from typing import List, Dict


class CriterionEvaluation(BaseModel):
    score: int
    explanation: str


class Evaluations(BaseModel):
    Robustez: CriterionEvaluation
    Exactitud: CriterionEvaluation
    Completitud: CriterionEvaluation
    Legibilidad: CriterionEvaluation
    Coherencia: CriterionEvaluation


class EvaluationOutput(BaseModel):
    evaluations: Evaluations
    final_score: int

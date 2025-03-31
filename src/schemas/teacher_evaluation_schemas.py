from pydantic import BaseModel, Field
from typing import List, Dict


class TeacherEvaluationRequest(BaseModel):
    rubric: Dict[str, str] = Field(
        ...,
        example={
            "criteria": "Describe the expected quality for each answer.",
            "score1_description": "La respuesta no cumple con lo mínimo requerido.",
            "score2_description": "La respuesta es parcialmente correcta pero le falta profundidad.",
            "score3_description": "La respuesta es aceptable, pero puede mejorarse.",
            "score4_description": "La respuesta es buena y cumple la mayoría de las expectativas.",
            "score5_description": "La respuesta es excelente y excede las expectativas.",
        },
    )
    reference_responses: List[str] = Field(
        ...,
        example=[
            "En una recesión, la economía se contrae, se reducen el empleo, la inversión y el consumo, lo que conduce a un descenso en el crecimiento económico y a mayores niveles de incertidumbre.",
            "La globalización aumenta la competencia internacional, fomenta la innovación y la transferencia tecnológica, pero también puede generar desigualdades y presiones sobre los mercados locales.",
            "Las medidas fiscales como la reducción de impuestos y el aumento del gasto público, junto con políticas monetarias expansivas, pueden incentivar el consumo y la inversión, estimulando el crecimiento económico durante una crisis.",
        ],
    )
    instructions: List[str] = Field(
        ...,
        example=[
            "Evalúa la pregunta 1 considerando claridad, precisión y profundidad en la respuesta.",
            "Evalúa la pregunta 2 analizando la argumentación y la capacidad de vincular conceptos económicos.",
            "Evalúa la pregunta 3 considerando la relevancia de las medidas propuestas y la coherencia en la respuesta.",
        ],
    )

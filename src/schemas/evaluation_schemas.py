from pydantic import BaseModel, Field
from typing import List, Dict
from .openai_schemas import EvaluationOutput


class EvaluationRequest(BaseModel):
    instruction: str = Field(
        ...,
        example="Struggling with a recent break-up, a person opens up about the intense feelings of loneliness and sadness. They ask for advice on how to cope with the heartbreak and move forward in life.",
    )
    model_responses: List[str] = Field(
        ...,
        example=[
            "No sé, simplemente supéralo, ya pasa.",
            "Entiendo que estés triste, pero intenta mantenerte ocupado y no pensar demasiado en ello.",
            "Lamento mucho que estés pasando por este doloroso momento. Es natural sentir un vacío y tristeza tras la pérdida de una relación significativa. Permítete sentir el dolor, llora si lo necesitas, y no te presiones para sanar rápidamente. Considera buscar el apoyo de amigos, familiares o incluso un profesional, ya que compartir tus sentimientos puede ser un gran alivio. Recuerda que cada persona tiene su propio ritmo de recuperación, y está bien tomarse el tiempo que necesites para volver a encontrar tu equilibrio.",
        ],
    )
    reference_responses: List[str] = Field(
        ...,
        example=[
            "Es importante reconocer el dolor, permitirse sentir las emociones y buscar apoyo en amigos o profesionales. El proceso de sanación toma tiempo.",
            "Es normal sentir tristeza y dolor tras una ruptura. Además de mantener la mente ocupada, es fundamental permitirse sentir y buscar apoyo de personas de confianza o profesionales para procesar la situación.",
            "Es fundamental reconocer y aceptar el dolor que sientes tras la ruptura. Permítete experimentar tus emociones sin juzgarte, y busca el apoyo de personas cercanas o profesionales para ayudarte a procesar lo vivido. Toma acciones de autocuidado, como descansar, practicar actividades que te hagan sentir bien y darte el espacio necesario para sanar a tu propio ritmo. Recuerda que el proceso de recuperación es gradual y cada paso cuenta.",
        ],
    )
    rubric: Dict[str, str] = Field(
        ...,
        example={
            "criteria": "Is the model proficient in applying empathy and emotional intelligence to its responses when the user conveys emotions or faces challenging circumstances?",
            "score1_description": "The model neglects to identify or react to the emotional tone of user inputs, giving responses that are unfitting or emotionally insensitive.",
            "score2_description": "The model intermittently acknowledges emotional context but often responds without sufficient empathy or emotional understanding.",
            "score3_description": "The model typically identifies emotional context and attempts to answer with empathy, yet the responses might sometimes miss the point or lack emotional profundity.",
            "score4_description": "The model consistently identifies and reacts suitably to emotional context, providing empathetic responses. Nonetheless, there may still be sporadic oversights or deficiencies in emotional depth.",
            "score5_description": "The model excels in identifying emotional context and persistently offers empathetic, emotionally aware responses that demonstrate a profound comprehension of the user's emotions or situation.",
        },
    )


class BERTScore(BaseModel):
    precision: float
    recall: float
    f1: float


class EvaluationResponse(BaseModel):
    model_response: str
    openai_score: EvaluationOutput
    bertscore: BERTScore
    prometheus_score: dict

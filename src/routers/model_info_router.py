# src/routers/model_info_router.py

from fastapi import APIRouter

router = APIRouter()


@router.get("/info")
def get_model_info():
    """
    Endpoint para extraer información del modelo (GET).
    Ajusta según la información que quieras devolver.
    """
    # Aquí podrías, por ejemplo, devolver la configuración actual del modelo,
    # el nombre del modelo, versión, etc.
    return {
        "model_name": "ollama/llama3.2:3b",
        "description": "Modelo local para evaluaciones con PrometheusEval.",
    }

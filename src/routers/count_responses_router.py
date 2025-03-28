from fastapi import APIRouter, File, UploadFile
from ..services.count_responses_services import count_generative_responses_from_yaml

router = APIRouter()


@router.post("/count-responses", response_model=dict)
async def count_responses(file: UploadFile = File(...)):
    """
    Cuenta las respuestas generativas a partir de un archivo YAML subido.

    Este endpoint permite subir un archivo YAML a través de Swagger y devuelve un resumen que
    incluye la cantidad de respuestas generativas encontradas en el flujo principal, las condiciones
    y el total de respuestas generativas.

    Parameters
    ----------
    file : UploadFile
        Archivo YAML subido mediante el widget de subida de archivos de Swagger.

    Returns
    -------
    dict
        Diccionario con la siguiente estructura:
        {
            "main_flow": int,
            "conditions": dict,
            "total_count": int
        }
    """
    content = await file.read()
    result = count_generative_responses_from_yaml(content)
    return result

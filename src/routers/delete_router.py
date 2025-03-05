# src/routers/delete_router.py

from fastapi import APIRouter

router = APIRouter()

@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    Endpoint para eliminar un elemento (DELETE).
    Ajusta la lógica real de eliminación.
    """
    # Lógica de eliminación. Ejemplo: delete from DB
    # ...
    return {"message": f"Item {item_id} eliminado exitosamente."}

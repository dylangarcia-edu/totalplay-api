from fastapi import APIRouter

from app import db
from app.schemas import PaqueteEnum, PaqueteUpdate

router = APIRouter(prefix="/v1/api/paquetes", tags=["Paquetes"])


@router.get("")
def obtener_paquetes():
    return {"success": True, "total": len(db.paquetes), "data": db.paquetes}


@router.put("/{nombre_paquete}")
def actualizar_costo(nombre_paquete: PaqueteEnum, datos: PaqueteUpdate):
    db.paquetes[nombre_paquete.value] = datos.costo
    return {
        "success": True,
        "message": "Costo actualizado",
        "data": {"paquete": nombre_paquete.value, "costo": datos.costo},
    }
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app import db
from app.schemas import ServicioCreate, ServicioUpdate

router = APIRouter(prefix="/v1/api/servicios", tags=["Servicios"])


def _sin_zona(fecha):
    """Quita la zona horaria (la 'Z' de Swagger) para poder comparar fechas sin error."""
    if fecha is not None and fecha.tzinfo is not None:
        return fecha.replace(tzinfo=None)
    return fecha


def _armar_registro(servicio, cliente):
    """Une el servicio con los datos del cliente y el costo actual del paquete."""
    return {
        "id_servicio": servicio["id_servicio"],
        "id_cliente": cliente["id_cliente"],
        "nombre_cliente": cliente["nombre_cliente"],
        "direccion": cliente["direccion"],
        "paquete": servicio["paquete"],
        "costo_paquete": db.paquetes[servicio["paquete"]],  # se lee al momento: respeta costos actualizados
        "fecha_registro": servicio["fecha_registro"],
    }


@router.get("")
def consultar_servicios(
    fecha_desde: Optional[datetime] = Query(None, description="Incluye servicios desde esta fecha/hora"),
    fecha_hasta: Optional[datetime] = Query(None, description="Incluye servicios hasta esta fecha/hora"),
):
    """Consulta/reporte de servicios: solo clientes activos, con filtro opcional por fecha."""
    fecha_desde = _sin_zona(fecha_desde)
    fecha_hasta = _sin_zona(fecha_hasta)

    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        raise HTTPException(status_code=400, detail="fecha_desde no puede ser mayor que fecha_hasta")

    data = []
    for servicio in db.servicios:
        cliente = db.buscar_cliente(servicio["id_cliente"])
        if cliente is None or not cliente["active"]:
            continue  # solo clientes activos
        fecha_servicio = _sin_zona(servicio["fecha_registro"])
        if fecha_desde and fecha_servicio < fecha_desde:
            continue
        if fecha_hasta and fecha_servicio > fecha_hasta:
            continue
        data.append(_armar_registro(servicio, cliente))

    return {
        "success": True,
        "total": len(data),
        "total_costo": sum(r["costo_paquete"] for r in data),
        "data": data,
    }


@router.post("", status_code=201)
def registrar_servicio(datos: ServicioCreate):
    cliente = db.buscar_cliente(datos.id_cliente)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if not cliente["active"]:
        raise HTTPException(
            status_code=400,
            detail="No se puede registrar un servicio a un cliente inactivo",
        )

    nuevo = {
        "id_servicio": db.siguiente_id(db.servicios, "id_servicio"),
        "id_cliente": datos.id_cliente,
        "paquete": datos.paquete.value,
        "fecha_registro": _sin_zona(datos.fecha_registro) or datetime.now(),
    }
    db.servicios.append(nuevo)
    return {"success": True, "message": "Servicio registrado", "data": _armar_registro(nuevo, cliente)}


@router.put("/{id_servicio}")
def actualizar_servicio(id_servicio: int, datos: ServicioUpdate):
    servicio = db.buscar_servicio(id_servicio)
    if servicio is None:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    cliente = db.buscar_cliente(servicio["id_cliente"])
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if not cliente["active"]:
        raise HTTPException(
            status_code=400,
            detail="No se puede actualizar el servicio de un cliente inactivo",
        )

    if datos.paquete is not None:
        servicio["paquete"] = datos.paquete.value
    if datos.fecha_registro is not None:
        servicio["fecha_registro"] = _sin_zona(datos.fecha_registro)

    return {"success": True, "message": "Servicio actualizado", "data": _armar_registro(servicio, cliente)}

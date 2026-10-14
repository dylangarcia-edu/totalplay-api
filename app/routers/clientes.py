from fastapi import APIRouter, HTTPException
from app import db
from app.schemas import ClienteCreate, ClienteUpdate

router = APIRouter(prefix="/v1/api/clientes", tags=["Clientes"])

# ---------- Ver ----------
@router.get("")
def obtener_clientes():
    return {
        "success": True,
        "total": len(db.clientes),
        "data": db.clientes,
    }

# ---------- Registrar ----------
@router.post("", status_code=201)
def registrar_cliente(datos: ClienteCreate):
    nuevo = {
        "id_cliente": db.siguiente_id(db.clientes, "id_cliente"),
        "nombre_cliente": datos.nombre_cliente,
        "direccion": datos.direccion,
        "active": True,
    }
    db.clientes.append(nuevo)
    return {"success": True, "message": "Cliente registrado", "data": nuevo}

# ---------- Actualizar ----------
@router.put("/{id_cliente}")
def actualizar_cliente(id_cliente: int, datos: ClienteUpdate):
    cliente = db.buscar_cliente(id_cliente)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if not cliente["active"]:
        raise HTTPException(status_code=400, detail="No se puede actualizar un cliente inactivo")

    if datos.nombre_cliente is not None:
        cliente["nombre_cliente"] = datos.nombre_cliente
    if datos.direccion is not None:
        cliente["direccion"] = datos.direccion

    return {"success": True, "message": "Cliente actualizado", "data": cliente}

# ---------- Desactivar ----------
@router.delete("/{id_cliente}")
def desactivar_cliente(id_cliente: int):
    cliente = db.buscar_cliente(id_cliente)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if not cliente["active"]:
        raise HTTPException(status_code=400, detail="El cliente ya está inactivo")

    cliente["active"] = False
    return {"success": True, "message": "Cliente desactivado", "data": cliente}
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# ---------- Paquetes ----------

class PaqueteEnum(str, Enum):
    """Paquetes válidos, cualquier otro valor es rechazado debido a Pydantic"""
    basico = "basico"
    intermedio = "intermedio"
    premium = "premium"

class PaqueteUpdate(BaseModel):
    costo: float = Field(..., ge=0)  # Costo debe ser mayor o igual a 0


# ---------- Clientes ----------

class ClienteCreate(BaseModel):
    nombre_cliente: str = Field(..., min_length=1)
    direccion: str = Field(..., min_length=1)


class ClienteUpdate(BaseModel):
    nombre_cliente: Optional[str] = Field(None, min_length=1)
    direccion: Optional[str] = Field(None, min_length=1)


# ---------- Servicios ----------

class ServicioCreate(BaseModel):
    id_cliente: int
    paquete: PaqueteEnum
    fecha_registro: Optional[datetime] = None


class ServicioUpdate(BaseModel):
    paquete: Optional[PaqueteEnum] = None
    fecha_registro: Optional[datetime] = None
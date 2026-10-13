from datetime import datetime

# Costos de los paquetes. Es un diccionario: nombre -> precio
paquetes = {
    "basico": 400.00,
    "intermedio": 500.00,
    "premium": 600.00,
}

# Clientes de prueba (para no empezar con la API vacía)
clientes = [
    {"id_cliente": 1, "nombre_cliente": "Ana López", "direccion": "Av. Reforma 123, CDMX", "active": True},
    {"id_cliente": 2, "nombre_cliente": "Luis Pérez", "direccion": "Calle 5 de Mayo 45, Puebla", "active": True},
    {"id_cliente": 3, "nombre_cliente": "María Ruiz", "direccion": "Blvd. Juárez 890, Monterrey", "active": False},
]

# Servicios de prueba
servicios = [
    {"id_servicio": 1, "id_cliente": 1, "paquete": "basico", "fecha_registro": datetime(2026, 10, 1, 10, 0)},
    {"id_servicio": 2, "id_cliente": 2, "paquete": "premium", "fecha_registro": datetime(2026, 10, 5, 15, 30)},
    {"id_servicio": 3, "id_cliente": 3, "paquete": "intermedio", "fecha_registro": datetime(2026, 9, 20, 9, 0)},
]

def siguiente_id(lista, campo):
    """Regresa el siguiente id disponible: el más alto + 1."""
    if not lista:
        return 1
    return max(item[campo] for item in lista) + 1

def buscar_cliente(id_cliente):
    """Regresa el cliente con ese id, o None si no existe."""
    for cliente in clientes:
        if cliente["id_cliente"] == id_cliente:
            return cliente
    return None


def buscar_servicio(id_servicio):
    """Regresa el servicio con ese id, o None si no existe."""
    for servicio in servicios:
        if servicio["id_servicio"] == id_servicio:
            return servicio
    return None
from fastapi import FastAPI
from app.routers import clientes, paquetes, servicios

app = FastAPI(
    title="API TotalPlay",
    description="Gestión de clientes, servicios y paquetes de internet",
    version="1.0.0",
)

app.include_router(clientes.router)
app.include_router(servicios.router)
app.include_router(paquetes.router)


@app.get("/")
def inicio():
    return {"mensaje": "API TotalPlay funcionando correctamente."}
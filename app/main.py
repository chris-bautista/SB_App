"""
Auto Servicio Bautista — aplicación web.

Punto de entrada. Arranca con:

    uvicorn app.main:app --reload
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import config
from app.routers import publico

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=config.app_nombre,
    docs_url="/api/docs" if config.debug else None,
    redoc_url=None,
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

plantillas = Jinja2Templates(directory=BASE_DIR / "templates")


def pesos(valor) -> str:
    """
    Formatea un número como precio mexicano: 11800 -> $11,800

    Se muestran centavos solo cuando existen, porque la mayoría de los
    importes del taller son cerrados y '$2,600.00' agrega ruido visual.
    """
    if valor is None:
        return ""
    valor = float(valor)
    if valor == int(valor):
        return f"${int(valor):,}"
    return f"${valor:,.2f}"


plantillas.env.filters["pesos"] = pesos

# El router necesita el motor de plantillas ya configurado con los filtros.
publico.plantillas = plantillas
app.include_router(publico.router)

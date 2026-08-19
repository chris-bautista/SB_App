"""
Auto Servicio Bautista — aplicación web.

Punto de entrada. Arranca con:

    uvicorn app.main:app --reload
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app import models  # noqa: F401 — registra Nota/Concepto en Base.metadata
from app.config import config
from app.db import Base, engine
from app.routers import admin, publico
from app.security import NoAutenticado

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=config.app_nombre,
    docs_url="/api/docs" if config.debug else None,
    redoc_url=None,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=config.secret_key,
    session_cookie="autosb_admin_session",
    max_age=60 * 60 * 8,  # 8 horas
    # En desarrollo (.env DEBUG=true) el sitio corre en http; con https_only=True
    # ahí, el navegador descartaría la cookie de sesión sin ningún error visible
    # y el login "no pegaría". En producción (DEBUG=false) sí debe ir en True.
    https_only=not config.debug,
)

# Sin Alembic en este alcance: create_all() es barato e idempotente, y no hay
# lifespan hook en este proyecto, así que se ejecuta una vez al importar main.
Base.metadata.create_all(bind=engine)

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

# Los routers necesitan el motor de plantillas ya configurado con los filtros.
publico.plantillas = plantillas
app.include_router(publico.router)

admin.plantillas = plantillas
app.include_router(admin.router)


@app.exception_handler(NoAutenticado)
async def redirigir_a_login(request: Request, exc: NoAutenticado):
    return RedirectResponse(url="/admin/login", status_code=303)

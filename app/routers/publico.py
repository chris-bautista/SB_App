"""
Rutas del sitio público (sin login).
"""

from datetime import date

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import contenido

router = APIRouter()
plantillas: Jinja2Templates | None = None   # lo inyecta main.py al arrancar


def contexto_base(request: Request) -> dict:
    """
    Datos que necesita cualquier página pública: la barra de navegación y el
    pie usan estos valores en todas las vistas.
    """
    return {
        "request": request,
        "negocio": contenido.NEGOCIO,
        "horario": contenido.HORARIO,
        "servicios": contenido.SERVICIOS,
        "whatsapp_mensaje": contenido.WHATSAPP_MENSAJE.replace(" ", "%20"),
        "anio": date.today().year,
    }


@router.get("/", response_class=HTMLResponse, name="inicio")
async def inicio(request: Request):
    contexto = contexto_base(request)
    contexto.update({
        "cifras": contenido.CIFRAS,
        "servicios_adicionales": contenido.SERVICIOS_ADICIONALES,
        "nota": contenido.NOTA_EJEMPLO,
        "proceso": contenido.PROCESO,
        "nosotros": contenido.NOSOTROS,
    })
    return plantillas.TemplateResponse(request, "publico/index.html", contexto)

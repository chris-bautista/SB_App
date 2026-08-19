"""
Rutas del panel de administración (requieren sesión iniciada, salvo login).

Los handlers son "def" normales, no "async def": la verificación de
contraseña con bcrypt es CPU-bound y lenta a propósito (~100-300ms), y las
consultas a SQLAlchemy aquí son bloqueantes. Un "async def" correría eso
directo en el event loop y bloquearía todas las peticiones concurrentes
mientras tanto. FastAPI despacha los "def" normales a un threadpool aparte,
que es justo lo que se necesita aquí.
"""

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import exportadores
from app.config import config
from app.db import get_db
from app.models import Concepto, Nota
from app.security import admin_requerido, verificar_password

router = APIRouter()
plantillas: Jinja2Templates | None = None   # lo inyecta main.py al arrancar


# ---------------------------------------------------------------------------
# Login / logout
# ---------------------------------------------------------------------------

@router.get("/admin/login", response_class=HTMLResponse, name="admin_login")
def login_formulario(request: Request):
    if request.session.get("admin"):
        return RedirectResponse(url=request.url_for("admin_dashboard"), status_code=303)
    return plantillas.TemplateResponse(request, "admin/login.html", {"request": request, "error": None})


@router.post("/admin/login", name="admin_login_post")
def login_enviar(request: Request, usuario: str = Form(...), password: str = Form(...)):
    if usuario == config.admin_usuario and verificar_password(password, config.admin_password_hash):
        request.session["admin"] = usuario
        return RedirectResponse(url=request.url_for("admin_dashboard"), status_code=303)
    return plantillas.TemplateResponse(
        request, "admin/login.html",
        {"request": request, "error": "Usuario o contraseña incorrectos."},
        status_code=401,
    )


@router.post("/admin/logout", name="admin_logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=request.url_for("admin_login"), status_code=303)


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@router.get(
    "/admin", response_class=HTMLResponse, name="admin_dashboard",
    dependencies=[Depends(admin_requerido)],
)
def dashboard(request: Request, db: Session = Depends(get_db)):
    total = db.scalar(select(func.count(Nota.id))) or 0
    recientes = db.scalars(select(Nota).order_by(Nota.creado_en.desc()).limit(5)).all()
    return plantillas.TemplateResponse(
        request, "admin/dashboard.html", {"request": request, "total": total, "recientes": recientes},
    )


# ---------------------------------------------------------------------------
# Notas: listado y creación
# ---------------------------------------------------------------------------

@router.get(
    "/admin/notas", response_class=HTMLResponse, name="admin_notas_lista",
    dependencies=[Depends(admin_requerido)],
)
def notas_lista(request: Request, db: Session = Depends(get_db)):
    notas = db.scalars(select(Nota).order_by(Nota.creado_en.desc())).all()
    return plantillas.TemplateResponse(request, "admin/notas_lista.html", {"request": request, "notas": notas})


@router.get(
    "/admin/notas/nueva", response_class=HTMLResponse, name="admin_nota_nueva",
    dependencies=[Depends(admin_requerido)],
)
def nota_nueva_formulario(request: Request):
    return plantillas.TemplateResponse(request, "admin/nota_form.html", {"request": request, "error": None})


@router.post(
    "/admin/notas/nueva", name="admin_nota_nueva_post",
    dependencies=[Depends(admin_requerido)],
)
def nota_nueva_guardar(
    request: Request,
    db: Session = Depends(get_db),
    cliente_nombre: str = Form(...),
    cliente_telefono: str = Form(""),
    vehiculo_marca: str = Form(...),
    vehiculo_modelo: str = Form(...),
    vehiculo_anio: int | None = Form(None),
    vehiculo_placas: str = Form(""),
    trabajo: str = Form(...),
    aviso: str = Form(""),
    tipo: list[str] = Form(default=[]),
    descripcion: list[str] = Form(default=[]),
    posicion: list[str] = Form(default=[]),
    lado: list[str] = Form(default=[]),
    cantidad: list[int] = Form(default=[]),
    importe: list[float] = Form(default=[]),
):
    conceptos = [
        Concepto(tipo=t, descripcion=d, posicion=p or None, lado=lado_ or None, cantidad=c, importe=i)
        for t, d, p, lado_, c, i in zip(tipo, descripcion, posicion, lado, cantidad, importe)
        if d.strip()
    ]
    if not conceptos:
        return plantillas.TemplateResponse(
            request, "admin/nota_form.html",
            {"request": request, "error": "Agrega al menos un concepto."},
            status_code=400,
        )

    nota = Nota(
        cliente_nombre=cliente_nombre,
        cliente_telefono=cliente_telefono or None,
        vehiculo_marca=vehiculo_marca,
        vehiculo_modelo=vehiculo_modelo,
        vehiculo_anio=vehiculo_anio,
        vehiculo_placas=vehiculo_placas or None,
        trabajo=trabajo,
        aviso=aviso or None,
        conceptos=conceptos,
    )
    db.add(nota)
    db.commit()
    db.refresh(nota)
    return RedirectResponse(url=request.url_for("admin_nota_detalle", nota_id=nota.id), status_code=303)


# ---------------------------------------------------------------------------
# Exportaciones del historial — DEBEN declararse antes de /admin/notas/{nota_id}
# (si no, FastAPI intenta convertir "exportar" a int y responde 422).
# ---------------------------------------------------------------------------

@router.get(
    "/admin/notas/exportar/excel", name="admin_notas_exportar_excel",
    dependencies=[Depends(admin_requerido)],
)
def notas_exportar_excel(db: Session = Depends(get_db)):
    notas = db.scalars(select(Nota).order_by(Nota.creado_en.desc())).all()
    return exportadores.notas_a_excel(notas)


@router.get(
    "/admin/notas/exportar/sql", name="admin_notas_exportar_sql",
    dependencies=[Depends(admin_requerido)],
)
def notas_exportar_sql(db: Session = Depends(get_db)):
    notas = db.scalars(select(Nota).order_by(Nota.creado_en.desc())).all()
    return exportadores.notas_a_sql(notas)


# ---------------------------------------------------------------------------
# Notas: detalle y exportación individual
# ---------------------------------------------------------------------------

@router.get(
    "/admin/notas/{nota_id}", response_class=HTMLResponse, name="admin_nota_detalle",
    dependencies=[Depends(admin_requerido)],
)
def nota_detalle(request: Request, nota_id: int, db: Session = Depends(get_db)):
    nota = db.get(Nota, nota_id)
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return plantillas.TemplateResponse(request, "admin/nota_detalle.html", {"request": request, "nota": nota})


@router.get(
    "/admin/notas/{nota_id}/excel", name="admin_nota_excel",
    dependencies=[Depends(admin_requerido)],
)
def nota_excel(nota_id: int, db: Session = Depends(get_db)):
    nota = db.get(Nota, nota_id)
    if nota is None:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return exportadores.nota_a_excel(nota)

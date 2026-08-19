"""
Autenticación del panel de administración: hash de contraseña y sesión.
"""

from fastapi import Request
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password_plano: str) -> str:
    return pwd_context.hash(password_plano)


def verificar_password(password_plano: str, password_hash: str) -> bool:
    if not password_hash:
        return False
    return pwd_context.verify(password_plano, password_hash)


class NoAutenticado(Exception):
    """Se lanza cuando una ruta protegida se visita sin sesión iniciada."""


def admin_requerido(request: Request) -> None:
    if not request.session.get("admin"):
        raise NoAutenticado()

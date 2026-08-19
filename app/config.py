"""
Configuración de la aplicación.

Todo lo que cambia entre tu computadora y el servidor vive aquí y se lee del
archivo .env, nunca del código. Copia .env.example a .env para empezar.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Configuracion(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Nombre visible de la app (aparece en la documentación de FastAPI).
    app_nombre: str = "Auto Servicio Bautista"

    # True solo en desarrollo: recarga plantillas sin reiniciar el servidor.
    debug: bool = False

    # Cadena de conexión a la base de datos.
    #
    # SQLite queda perfecto en local. En producción hay que apuntar esto a un
    # Postgres: el plan gratuito de Render borra el disco en cada reinicio y
    # una base SQLite ahí se pierde. Como usamos SQLAlchemy, cambiar de motor
    # es cambiar esta línea, nada más.
    database_url: str = f"sqlite:///{BASE_DIR.parent / 'data' / 'autosb.db'}"

    # Llave para firmar la cookie de sesión del panel de administración.
    # Genera una con:  python -c "import secrets; print(secrets.token_hex(32))"
    secret_key: str = "cambiar-esta-llave-antes-de-publicar"

    # Credenciales del panel de administración. admin_password_hash es un
    # hash bcrypt, nunca la contraseña en texto plano. Generarlo con:
    #   python -c "from app.security import hash_password; print(hash_password('tu-contraseña'))"
    admin_usuario: str = "admin"
    admin_password_hash: str = ""


config = Configuracion()

"""
Motor y sesión de SQLAlchemy.

SQLite es el motor local (ver app/config.py). check_same_thread=False es
obligatorio: uvicorn puede atender peticiones en hilos distintos del
threadpool y, sin esa bandera, sqlite3 rechaza usar una misma conexión
desde un hilo distinto al que la abrió.

Esto es seguro aquí porque get_db() abre una conexión NUEVA por petición
(nunca se comparte una Session entre peticiones concurrentes) y la cierra
al terminar. Nunca crear una Session a nivel de módulo y reutilizarla.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import config

connect_args = {"check_same_thread": False} if config.database_url.startswith("sqlite") else {}

engine = create_engine(config.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

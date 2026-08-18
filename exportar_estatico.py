"""
Exporta el sitio público a HTML estático, listo para GitHub Pages.

Uso:

    python exportar_estatico.py

Genera la carpeta docs/ con index.html y los archivos estáticos. Esa carpeta
es la que GitHub Pages publica.

Por qué existe: GitHub Pages no ejecuta Python. Como la página pública no
tiene nada dinámico (no hay formularios ni consultas a base de datos), se
puede renderizar una sola vez y servir el HTML resultante.

Cuando llegue el panel de administración, ese sí necesita servidor y va
aparte, en Render. El sitio público se queda aquí.
"""

import re
import shutil
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

RAIZ = Path(__file__).resolve().parent
DESTINO = RAIZ / "docs"
ESTATICOS = RAIZ / "app" / "static"


def rutas_relativas(html: str) -> str:
    """
    Convierte las rutas absolutas de los archivos estáticos en relativas.

    Hace falta porque en GitHub Pages el sitio no vive en la raíz del dominio
    sino en usuario.github.io/repositorio/. Una ruta como /static/css/output.css
    apuntaría fuera del proyecto y la página saldría sin estilos.
    """
    html = html.replace("http://testserver/static/", "static/")
    html = re.sub(r'(href|src)="/static/', r'\1="static/', html)
    return html


def exportar() -> None:
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    DESTINO.mkdir()

    cliente = TestClient(app)
    respuesta = cliente.get("/")
    respuesta.raise_for_status()

    (DESTINO / "index.html").write_text(rutas_relativas(respuesta.text), encoding="utf-8")

    shutil.copytree(ESTATICOS, DESTINO / "static")

    # Sin este archivo, GitHub ignora las carpetas que empiezan con guion bajo
    # y procesa el sitio con Jekyll, que no necesitamos.
    (DESTINO / ".nojekyll").touch()

    peso = sum(f.stat().st_size for f in DESTINO.rglob("*") if f.is_file())
    print(f"Listo: {DESTINO}  ({peso / 1024:.0f} KB)")
    print("Súbelo a GitHub y activa Pages apuntando a la carpeta docs/")


if __name__ == "__main__":
    exportar()

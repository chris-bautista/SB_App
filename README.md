# Auto Servicio Bautista

Sitio web y sistema de gestión del taller. Etapa actual: **sitio público terminado**.

FastAPI + Jinja2 + Tailwind CSS v4. Sin base de datos todavía.

## Arrancar

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
uvicorn app.main:app --reload
```

Abre http://127.0.0.1:8000

El CSS ya viene compilado en `app/static/css/output.css`, así que el sitio se ve
bien sin instalar Node. Solo necesitas Node si vas a **modificar** estilos:

```bash
npm install
npm run css      # recompila mientras editas
npm run build    # versión minificada para publicar
```

## Qué editar

Todo el contenido del sitio está en **`app/contenido.py`**. Las plantillas no
tienen ni un texto escrito a mano: cambias ese archivo y cambia la página.

Los colores y tipografías están en **`app/static/css/input.css`**, en el bloque
`@theme`. Son ocho valores; cambiarlos cambia la identidad completa del sitio.

### Pendientes antes de publicar

En `app/contenido.py`, busca los comentarios `← COMPLETAR`:

- `whatsapp` — número en formato internacional sin signos, ej. `5213312345678`
- `telefono` y `telefono_visible`
- `direccion` y `ciudad_cp`
- `url` — el dominio final
- `maps_embed` — el `src` del iframe de Google Maps (si lo dejas vacío, en su
  lugar aparece un bloque con la dirección; no se rompe nada)
- Confirmar el `HORARIO`

También falta una imagen `app/static/img/og.jpg` (1200×630 px) para que el
enlace se vea bien al compartirlo por WhatsApp.

## Publicar en GitHub Pages

La página pública no tiene nada dinámico, así que se puede exportar a HTML
estático y publicarla gratis en GitHub Pages. GitHub Pages **no ejecuta
Python**: sin este paso, el repositorio no se ve como sitio.

```bash
python exportar_estatico.py    # genera la carpeta docs/
git add . && git commit -m "Actualizar sitio" && git push
```

Después, una sola vez: en GitHub, **Settings → Pages → Source: Deploy from a
branch → Branch: main, carpeta /docs → Save.** En un par de minutos el sitio
queda en `https://TU-USUARIO.github.io/autosb/`.

Cada vez que cambies algo en `contenido.py` o en las plantillas, hay que
volver a correr `exportar_estatico.py` antes de hacer push. El servidor
FastAPI es para desarrollar y para el panel de administración que viene
después; lo que ve el cliente es la carpeta `docs/`.

## Estructura

```
app/
├─ main.py            Arranque, montaje de estáticos, filtro de precios
├─ config.py          Variables de entorno
├─ contenido.py       ← Todo el contenido del sitio
├─ routers/
│  └─ publico.py      Rutas sin login
├─ templates/
│  ├─ base.html       Head, SEO, Open Graph, datos estructurados, scripts
│  ├─ partials/       Barra de navegación y pie
│  └─ publico/
│     └─ index.html   Página de inicio
└─ static/css/
   ├─ input.css       Tokens de diseño (editar aquí)
   └─ output.css      Compilado (no editar a mano)
```

## Decisiones

**HTML renderizado en el servidor, no SPA.** Para un sitio de una página y un
CRUD interno, Jinja carga más rápido, indexa mejor en Google y se mantiene con
menos piezas móviles que React.

**El contenido vive en Python, no en el HTML.** Cambiar un precio o un teléfono
no debería obligar a tocar plantillas. También deja el camino listo para cuando
los servicios salgan de la base de datos en vez de una constante.

**Los servicios están ordenados por volumen real de trabajo**, tomado de las 62
notas registradas. Suspensión y dirección aparecen primero y marcadas como
especialidad porque son el 60% de lo que hace el taller.

**La nota de servicio del hero es real** (folio N-006). Es el argumento central
del sitio: el cliente ve cómo se le va a cotizar antes de escribir. El nombre
del cliente no aparece; si prefieres no mostrar precios reales, cambia
`NOTA_EJEMPLO` en `contenido.py`.

## Siguientes etapas

1. Modelo de datos y base SQLite + importador del Excel
2. Login del administrador
3. CRUD de clientes, vehículos y notas de servicio
4. Exportación a `.xlsx` y `.sql`
5. Despliegue

**Nota sobre el despliegue:** el plan gratuito de Render borra el disco en cada
reinicio y no permite discos persistentes, así que una base SQLite ahí se
pierde. Como todo pasa por SQLAlchemy, en producción basta apuntar
`DATABASE_URL` a un Postgres externo con capa gratuita permanente. El código no
cambia.

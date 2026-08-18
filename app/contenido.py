"""
Contenido del sitio público.

Este es el ÚNICO archivo que hay que editar para cambiar textos, datos de
contacto o servicios. Las plantillas no tienen contenido escrito a mano.

Los campos marcados con  # ← COMPLETAR  son datos reales del taller que
todavía no tengo. El sitio funciona sin ellos, pero hay que llenarlos antes
de publicar.
"""

# ---------------------------------------------------------------------------
# Datos del negocio
# ---------------------------------------------------------------------------

NEGOCIO = {
    "nombre": "Auto Servicio Bautista",
    "nombre_corto": "Bautista",
    "descripcion": (
        "Taller mecánico en el centro de Guadalajara especializado en suspensión "
        "y dirección."
    ),
    "ciudad": "Guadalajara, Jalisco",
    # Formato internacional sin signos, para el enlace de WhatsApp.
    "whatsapp": "5213339548635",
    # Formato para marcar desde el celular.
    "telefono": "3339548635",             # ← COMPLETAR
    "telefono_visible": "3339548635",   # ← COMPLETAR
    "direccion": "C. Humboldt #547, Colonia Centro Barranquitas",
    "ciudad_cp": "Guadalajara, Jal. C.P. 44200",
    # URL del sitio ya publicado (se usa en las etiquetas Open Graph).
    "url": "https://autoserviciobautista.com",    # ← COMPLETAR
    # Pega aquí el atributo src del iframe de Google Maps.
    # Si lo dejas vacío, en lugar del mapa se muestra un bloque con la
    # dirección y un botón, que se ve bien y no queda roto.
    "maps_embed": "",                     # ← COMPLETAR
    "maps_link": "https://maps.google.com/?q=C.+Humboldt+547+Colonia+Centro+Barranquitas+Guadalajara+44200",
}

HORARIO = [
    {"dias": "Lunes a viernes", "horas": "9:00 a 19:00"},
    {"dias": "Sábado", "horas": "9:00 a 14:00"},
    {"dias": "Domingo", "horas": "Cerrado"},
]

# Mensaje con el que se abre WhatsApp al dar clic en el botón principal.
WHATSAPP_MENSAJE = (
    "Hola, vengo del sitio web. Quiero cotizar un servicio para mi auto."
)

# ---------------------------------------------------------------------------
# Cifras
#
# Son afirmaciones sobre cómo trabaja el taller, no datos de operación.
# Cuántos clientes hay o cuántas notas se registraron es información interna
# y vive detrás del login, nunca en la página pública.
# ---------------------------------------------------------------------------

CIFRAS = [
    {"dato": "60%", "etiqueta": "suspensión y dirección"},
    {"dato": "16", "etiqueta": "marcas atendidas"},
    {"dato": "2", "etiqueta": "generaciones en el taller"},
    {"dato": "100%", "etiqueta": "cotizado antes de empezar"},
]

# ---------------------------------------------------------------------------
# Servicios
#
# Ordenados por volumen real de trabajo, no alfabéticamente ni al azar.
# "servicios" es el número de notas de servicio en las que aparece cada
# categoría. Suspensión y dirección son casi el 60% del trabajo del taller:
# eso es lo que el sitio comunica primero.
# ---------------------------------------------------------------------------

SERVICIOS = [
    {
        "nombre": "Suspensión",
        "especialidad": True,
        "resumen": "Lo que más hacemos y lo que mejor hacemos.",
        "trabajos": [
            "Amortiguadores y bases",
            "Horquillas y bujes",
            "Rótulas y baleros",
            "Rectificado de eje trasero",
            "Hules de barra estabilizadora",
        ],
    },
    {
        "nombre": "Dirección",
        "especialidad": True,
        "resumen": "Cremallera completa, de la reparación al ajuste fino.",
        "trabajos": [
            "Reparación de cremallera",
            "Terminales y bieletas",
            "Mangueras y cubrepolvos",
            "Rectificado de mango",
            "Columna y sensor de dirección",
        ],
    },
    {
        "nombre": "Motor",
        "especialidad": False,
        "resumen": "Mantenimiento preventivo y sistema de enfriamiento.",
        "trabajos": [
            "Afinación mayor y menor",
            "Lavado de inyectores",
            "Radiador y bomba de agua",
            "Bandas y mangueras",
        ],
    },
    {
        "nombre": "Llantas y rines",
        "especialidad": False,
        "resumen": "Montaje y alineación en el mismo taller.",
        "trabajos": [
            "Venta y montaje de llantas",
            "Alineación",
            "Rines delanteros",
        ],
    },
    {
        "nombre": "Chasis",
        "especialidad": False,
        "resumen": "Enderezado estructural con soldadura.",
        "trabajos": [
            "Enderezado de chasis",
            "Cierre y estirado de puente",
            "Soldadura y refuerzos",
            "Hules de carrocería",
        ],
    },
    {
        "nombre": "Transmisión",
        "especialidad": False,
        "resumen": "Clutch, flechas y transmisiones automáticas.",
        "trabajos": [
            "Clutch completo",
            "Bomba y cilindro esclavo",
            "Juntas homocinéticas y crucetas",
            "Afinación de transmisión CVT",
        ],
    },
    {
        "nombre": "Frenos",
        "especialidad": False,
        "resumen": "Del cambio de balatas a la fuga que nadie encuentra.",
        "trabajos": [
            "Balatas y discos",
            "Rectificado de disco",
            "Cálipers y mangueras",
            "Purgado y reparación de fugas",
        ],
    },
]

# Categorías con poco volumen: se mencionan en una línea, sin inflar la lista.
SERVICIOS_ADICIONALES = "sistema eléctrico, escape, pensión y trabajos generales"

# ---------------------------------------------------------------------------
# Nota de servicio de ejemplo
#
# Es el elemento central del sitio: muestra el FORMATO en que cotiza el
# taller, pieza por pieza y con posición y lado. Eso es lo que ningún
# competidor de la zona enseña.
#
# Deliberadamente NO es una nota real. Publicar folios y precios exactos
# expone tus tarifas a la competencia y te quita margen de negociación.
# Si algún día decides publicar precios reales, este es el único bloque
# que hay que cambiar.
# ---------------------------------------------------------------------------

NOTA_EJEMPLO = {
    "titulo": "Así cotizamos",
    "trabajo": "Suspensión delantera completa",
    "vehiculo": "Nissan Versa 2019",
    "conceptos": [
        {"tipo": "Producto", "descripcion": "Amortiguador",
         "posicion": "Anterior", "lado": "Izquierdo", "cantidad": 1, "importe": 2500},
        {"tipo": "Producto", "descripcion": "Amortiguador",
         "posicion": "Anterior", "lado": "Derecho", "cantidad": 1, "importe": 2500},
        {"tipo": "Producto", "descripcion": "Horquilla superior",
         "posicion": "Anterior", "lado": "Izquierdo", "cantidad": 1, "importe": 2500},
        {"tipo": "Producto", "descripcion": "Base de amortiguador",
         "posicion": "Anterior", "lado": "Izquierdo", "cantidad": 1, "importe": 900},
        {"tipo": "Producto", "descripcion": "Base de amortiguador",
         "posicion": "Anterior", "lado": "Derecho", "cantidad": 1, "importe": 900},
        {"tipo": "Servicio", "descripcion": "Mano de obra",
         "posicion": "", "lado": "", "cantidad": 1, "importe": 2200},
    ],
    "total": 11500,
    "aviso": (
        "Así se ve una nota de Auto Servicio Bautista: pieza por pieza, con "
        "posición y lado. La tuya depende de tu vehículo y de lo que "
        "realmente necesite."
    ),
}

# ---------------------------------------------------------------------------
# Cómo trabajamos
#
# Va numerado porque es una secuencia real: el orden importa y el cliente
# necesita saber que la cotización llega ANTES de que se toque el carro.
# ---------------------------------------------------------------------------

PROCESO = [
    {
        "titulo": "Revisamos el carro",
        "texto": (
            "Lo escuchamos, lo manejamos y lo subimos a la rampa. Si hace falta, "
            "escáner. Nunca cambiamos una pieza por descarte."
        ),
    },
    {
        "titulo": "Te pasamos la nota",
        "texto": (
            "Pieza por pieza, con posición y lado, mano de obra por separado y "
            "el total abajo. Tú decides qué se hace ahora y qué puede esperar."
        ),
    },
    {
        "titulo": "Reparamos y te entregamos",
        "texto": (
            "Te avisamos si aparece algo que no estaba en la nota, antes de "
            "hacerlo. Te devolvemos las piezas que se cambiaron."
        ),
    },
]

# ---------------------------------------------------------------------------
# Quiénes somos
# ---------------------------------------------------------------------------

NOSOTROS = {
    "titulo": "Un taller de dos",
    "parrafos": [
        (
            "Auto Servicio Bautista lo llevamos padre e hijo. No hay recepción, "
            "ni asesor de servicio, ni comisión por venderte piezas que no "
            "necesitas. El que revisa tu carro es el mismo que te lo explica y "
            "el mismo que lo repara."
        ),
        (
            "Trabajamos sobre todo suspensión y dirección, que es donde tenemos "
            "más oficio: rectificar un eje trasero o reparar una cremallera "
            "completa son trabajos que muchos talleres prefieren no tomar."
        ),
        (
            "Llevamos registro de cada servicio que sale del taller. Si tu carro "
            "ya pasó por aquí, sabemos exactamente qué se le hizo y cuándo."
        ),
    ],
    "valores": [
        {
            "titulo": "Cotización antes del trabajo",
            "texto": "Nunca vas a recibir una cuenta más alta que la nota que autorizaste.",
        },
        {
            "titulo": "Te devolvemos las piezas",
            "texto": "Todo lo que se cambia se entrega. No hay que pedirlo.",
        },
        {
            "titulo": "Historial de tu vehículo",
            "texto": "Guardamos qué se hizo, cuándo y con qué piezas. Sin cobrar por consultarlo.",
        },
    ],
}

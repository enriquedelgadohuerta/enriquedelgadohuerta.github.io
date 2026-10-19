#!/usr/bin/env python3
"""Genera las páginas locales /perito-informatico-<lugar>/ , el índice /zonas/
y el sitemap a partir de _tools/zonas.json.

Uso (desde la raíz del repositorio):
    python3 _tools/generar_zonas.py

Es idempotente: vuelve a escribir todas las páginas y el sitemap cada vez.
La carpeta _tools/ no se publica (GitHub Pages/Jekyll ignora las carpetas que empiezan por "_").
"""
import hashlib
import html
import json
import math
import os
import re
import unicodedata
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://informeperitoinformatico.es"
TEL = "+34649716627"
TEL_H = "649 716 627"
WA = "34649716627"
EMAIL = "info@informeperitoinformatico.es"
HOY = date.today().isoformat()

with open(os.path.join(ROOT, "_tools", "zonas.json"), encoding="utf-8") as f:
    DATA = json.load(f)

ORIG = DATA["origen"]
PARTIDOS_CAM = DATA["partidos_cam"]
COMPOSICION = DATA["composicion_partidos"]


# ───────────────────────── utilidades ─────────────────────────
def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s


def esc(s):
    return html.escape(s, quote=True)


def km(a, b):
    r = 6371.0
    p1, p2 = math.radians(a["lat"]), math.radians(b["lat"])
    dp = p2 - p1
    dl = math.radians(b["lon"] - a["lon"])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def pick(lugar, opciones, salt=""):
    """Elige una variante de forma estable según el lugar (misma página → mismo texto)."""
    h = int(hashlib.sha1((lugar["slug"] + salt).encode()).hexdigest(), 16)
    return opciones[h % len(opciones)]


def de(nombre):
    """'de' + nombre, contrayendo 'de El' → 'de El' (se deja) y 'de Los' etc."""
    return "de " + nombre


def en(nombre):
    return "en " + nombre


def redondea(d):
    if d < 15:
        return max(1, int(round(d)))
    if d < 100:
        return int(round(d / 5.0) * 5)
    return int(round(d / 10.0) * 10)


# ───────────────────────── modelo ─────────────────────────
LUGARES = DATA["lugares"]
for l in LUGARES:
    l["slug"] = slugify(l["nombre"])
    l["url"] = f"/perito-informatico-{l['slug']}/"
    l["dist"] = km(ORIG, l)
    if l.get("base"):
        l["modo"] = "base"
    elif l["tipo"] in ("corredor", "partido"):
        l["modo"] = "local"
    elif l["dist"] <= 200 and not l.get("isla"):
        l["modo"] = "cercana"
    else:
        l["modo"] = "remota"
    # órganos judiciales
    if l["ccaa"] == "Comunidad de Madrid":
        l["audiencia_txt"] = "la Audiencia Provincial de Madrid"
        l["tsj_txt"] = "Tribunal Superior de Justicia de Madrid"
    elif l["provincia"] == "Guadalajara":
        l["audiencia_txt"] = "la Audiencia Provincial de Guadalajara"
        l["tsj_txt"] = "Tribunal Superior de Justicia de Castilla-La Mancha (Albacete)"
    else:
        l["audiencia_txt"] = l.get("audiencia") or f"la Audiencia Provincial de {l['provincia']}"
        l["tsj_txt"] = l["tsj"]
    if l["tipo"] == "capital":
        l["partido"] = l["nombre"]

POR_NOMBRE = {l["nombre"]: l for l in LUGARES}
assert len(POR_NOMBRE) == len(LUGARES), "nombres duplicados en zonas.json"
assert len({l["slug"] for l in LUGARES}) == len(LUGARES), "slugs duplicados"


def enlace_lugar(nombre):
    l = POR_NOMBRE.get(nombre)
    if l:
        return f'<a href="{l["url"]}">{esc(nombre)}</a>'
    return esc(nombre)


def lista_natural(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " y " + items[-1]


def cercanos(l, n=6):
    otros = [o for o in LUGARES if o is not l]
    if l["modo"] in ("base", "local"):
        cand = [o for o in otros if o["modo"] in ("base", "local")]
    else:
        cand = [o for o in otros if o["tipo"] == "capital"]
    cand.sort(key=lambda o: km(l, o))
    res = cand[:n]
    base = POR_NOMBRE["Alcalá de Henares"]
    if l is not base and base not in res:
        res = res[: n - 1] + [base]
    return res


# ───────────────────────── bloques de texto ─────────────────────────
ICON_CHECK = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>'
ICON_PIN = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>'
def _svg_wa():
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        m = re.search(r'<a class="btn btn-wa"[^>]*>\s*(<svg.*?</svg>)', f.read(), re.S)
    return m.group(1)


ICON_WA = _svg_wa()
ICON_TEL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.13.96.36 1.9.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0122 16.92z"/></svg>'


def wa_link(l):
    from urllib.parse import quote
    if l is None:
        txt = "Hola Enrique, quería hacerte una consulta."
    else:
        txt = f"Hola Enrique, te escribo desde {l['nombre']}. Quería hacerte una consulta."
    return f"https://wa.me/{WA}?text={quote(txt)}"


def lead(l):
    n = l["nombre"]
    if l["modo"] == "base":
        return (f"Trabajo desde {n}. Si tienes mensajes, correos o fotos que pueden ser importantes en un juicio "
                f"—o sospechas que los que te enseñan son falsos— te ayudo a saber qué valor tienen y a presentarlos "
                f"con todas las garantías, sin tecnicismos.")
    if l["modo"] == "local":
        return pick(l, [
            f"Atiendo en persona en {n}: puedo recoger la prueba o analizar el teléfono sin que tengas que desplazarte. "
            f"Te explico qué valor tienen tus WhatsApp, correos o capturas antes de que gastes un euro.",
            f"Si vives o trabajas en {n} y tienes mensajes, correos o fotos que pueden decidir un juicio, "
            f"los analizo con método forense y te lo cuento sin jerga. Me desplazo a {n} cuando hace falta.",
            f"Perito informático para particulares y abogados de {n}. Convierto chats, correos y capturas en una prueba "
            f"que se sostiene en el juzgado, y voy a {n} cuando la prueba hay que tomarla en persona.",
        ])
    if l["modo"] == "cercana":
        return pick(l, [
            f"Trabajo para clientes de {n} a distancia y, cuando la prueba lo exige, me desplazo. "
            f"Analizo WhatsApp, correos, capturas y móviles y te lo explico sin tecnicismos.",
            f"¿Necesitas un perito informático en {n}? La mayoría de los análisis se hacen a distancia con garantías; "
            f"para extraer datos de un móvil o ratificar en juicio, voy a {n}.",
        ])
    return pick(l, [
        f"Atiendo casos de {n} a distancia: la mayor parte de las pruebas digitales se pueden recibir y analizar "
        f"con cadena de custodia sin que nos veamos en persona. Te lo explico todo sin tecnicismos.",
        f"Perito informático para particulares y abogados de {n}. Trabajo a distancia con método forense "
        f"documentado y, si el caso lo requiere, organizo el desplazamiento.",
    ])


def bloque_modalidad(l):
    n = l["nombre"]
    d = redondea(l["dist"])
    if l["modo"] == "base":
        pasos = [
            ("Nos vemos en Alcalá", "Si lo prefieres, quedamos en persona para que me cuentes el caso y vea la prueba."),
            ("Extracción en el momento", "Cuando hay que analizar un teléfono, la adquisición se hace delante de ti y se documenta con huellas SHA-256."),
            ("Juzgados de Alcalá", "Ratifico el informe en los juzgados de Alcalá de Henares, donde se ven los asuntos de Alcalá, Meco, Camarma, Villalbilla y el resto de su partido judicial."),
        ]
        intro = "Alcalá de Henares es mi base. Todo lo que necesites se puede hacer en persona y sin desplazamientos largos."
    elif l["modo"] == "local":
        intro = pick(l, [
            f"{n} está a unos {d} km de Alcalá de Henares, donde trabajo. Eso significa que puedo hacer en persona todo lo que lo requiera.",
            f"Desde Alcalá de Henares hasta {n} hay unos {d} km, así que el trabajo presencial no supone retrasos para ti.",
            f"Estoy a unos {d} km de {n}. Lo que se pueda hacer a distancia lo hacemos a distancia; lo que no, en persona.",
        ], "intro")
        pasos = [
            ("Primera consulta a distancia", "Me cuentas el caso por WhatsApp, teléfono o correo y te digo si un informe tiene sentido. Gratis."),
            (f"Recogida en {n}", f"Si hay que extraer datos de un teléfono o documentar una entrega, voy a {n} o quedamos donde te venga mejor."),
            ("Ratificación en juicio", f"Defiendo el informe en persona en los juzgados del partido judicial de {l['partido']}."),
        ]
    elif l["modo"] == "cercana":
        intro = f"{n} está a unos {d} km en línea recta de Alcalá de Henares. Combino trabajo a distancia y desplazamientos puntuales."
        pasos = [
            ("Consulta y presupuesto a distancia", "Por WhatsApp, teléfono o videollamada. Te digo si merece la pena y cuánto cuesta, por escrito."),
            ("Prueba a distancia o en persona", f"Correos y copias de conversaciones se reciben con garantías a distancia. Para un móvil, voy a {n} o lo recibo con cadena de custodia documentada."),
            ("Ratificación", f"Acudo a los juzgados de {n} cuando hay que ratificar. Si el juzgado lo admite, también puede hacerse por videoconferencia."),
        ]
    else:
        if l.get("isla"):
            intro = f"Trabajo desde Alcalá de Henares y llegar a {n} exige avión o barco. Por eso la mayor parte del trabajo se organiza a distancia, sin perder garantías."
        else:
            intro = f"Trabajo desde Alcalá de Henares, a unos {d} km en línea recta de {n}. Por eso la mayor parte del trabajo se organiza a distancia, sin perder garantías."
        pasos = [
            ("Consulta y presupuesto a distancia", "Por WhatsApp, teléfono o videollamada. Te digo con franqueza si un informe te ayuda y te paso el presupuesto por escrito."),
            ("Recepción segura de la prueba", "Correos, archivos y copias de conversaciones se reciben con huella SHA-256 desde el primer momento. Si hay que analizar un teléfono, se valora el envío con cadena de custodia o el desplazamiento."),
            ("Ratificación", f"Si el juzgado de {n} lo admite, la ratificación puede hacerse por videoconferencia; si no, me desplazo y el viaje figura en el presupuesto."),
        ]
    li = "\n".join(
        f'      <li class="step"><h3>{esc(t)}</h3><p>{esc(p)}</p></li>' for t, p in pasos
    )
    titulo = "Cómo trabajo en Alcalá de Henares" if l["modo"] == "base" else f"Cómo trabajo con clientes de {esc(n)}"
    return f"""<section class="band" id="como-trabajo" aria-labelledby="h2-modo">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{ICON_PIN} {esc(n)}</span>
      <h2 id="h2-modo">{titulo}</h2>
      <p class="lead">{esc(intro)}</p>
    </div>
    <ol class="steps steps-3">
{li}
    </ol>
  </div>
</section>"""


def bloque_juzgado(l):
    n = l["nombre"]
    filas = []
    if l["ccaa"] == "Comunidad de Madrid":
        num = PARTIDOS_CAM[l["partido"]]
        if l["partido"] == n:
            filas.append(("Partido judicial", f"{esc(n)} es cabeza del partido judicial nº {num} de la Comunidad de Madrid."))
        else:
            filas.append(("Partido judicial", f"{esc(n)} pertenece al partido judicial de {enlace_lugar(l['partido'])} (nº {num} de la Comunidad de Madrid): los asuntos de primera instancia e instrucción se ven en sus juzgados."))
    elif l["provincia"] == "Guadalajara":
        if n == "Guadalajara":
            filas.append(("Partido judicial", "Guadalajara es cabeza de su partido judicial, que incluye los municipios del Corredor del Henares en la provincia."))
        else:
            filas.append(("Partido judicial", f"{esc(n)} pertenece al partido judicial de {enlace_lugar('Guadalajara')}: los asuntos se ven en los juzgados de la capital."))
    else:
        filas.append(("Juzgados", f"Los asuntos de {esc(n)} se tramitan en los juzgados de su partido judicial, con sede en la propia ciudad."))
    filas.append(("Recursos", f"Las apelaciones en materia civil y penal van a {esc(l['audiencia_txt'])}."))
    filas.append(("Ámbito autonómico", esc(l["tsj_txt"]) + "."))
    comp = COMPOSICION.get(l["partido"])
    if comp:
        otros = [m for m in comp if m != n]
        filas.append(("Mismo partido", "También atiendo " + lista_natural([enlace_lugar(m) for m in otros]) + "."))
    dl = "\n".join(f"      <div><dt>{t}</dt><dd>{d}</dd></div>" for t, d in filas)
    nota = pick(l, [
        "Saber dónde se va a ver tu asunto ayuda a planificar plazos y la ratificación del informe.",
        "El informe pericial se aporta con la demanda o la denuncia, o en el momento procesal que indique tu abogado.",
        "Me coordino con tu abogado para que el informe llegue a tiempo al juzgado que corresponda.",
    ], "juz")
    return f"""<section id="juzgados" aria-labelledby="h2-juz">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Dónde se presenta tu informe</span>
      <h2 id="h2-juz">Juzgados que corresponden a {esc(n)}</h2>
      <p class="lead">{esc(nota)}</p>
    </div>
    <dl class="facts">
{dl}
    </dl>
    <p class="disclaimer">Información orientativa sobre la organización judicial. Tu abogado confirmará el órgano competente en tu caso concreto.</p>
  </div>
</section>"""


SERVICIOS = [
    ("WhatsApp y mensajería", "Autenticar conversaciones de WhatsApp o Telegram, cotejar capturas con el original y fijar la prueba con hash.", "Acoso o amenazas por mensajes"),
    ("Correo electrónico", "Origen real de un correo, cabeceras, SPF, DKIM y DMARC. Facturas con otra cuenta bancaria y suplantaciones.", "Correo falso o estafa"),
    ("Capturas e imágenes", "¿Es auténtica esta captura o esta foto? Metadatos, coherencia de formato y huellas de edición.", "Autenticidad de capturas o imágenes"),
    ("Móviles Android e iOS", "Extracción forense de mensajes, fotos, llamadas y ubicaciones de tu teléfono con cadena de custodia.", "Análisis de un móvil"),
    ("Datos borrados", "Qué se puede recuperar de un teléfono o sus copias de seguridad, con expectativas realistas desde el principio.", "Recuperar datos borrados"),
    ("Informe y contrapericial", "Informe conforme a UNE 197010 y revisión técnica del informe de la otra parte. Ratificación en juicio.", "Informe pericial para un procedimiento"),
]


def bloque_servicios(l):
    n = l["nombre"]
    orden = SERVICIOS[:]
    # Variación estable del orden para que las páginas no sean idénticas
    h = int(hashlib.sha1(l["slug"].encode()).hexdigest(), 16)
    rot = h % 3
    orden = orden[rot:] + orden[:rot]
    cards = "\n".join(
        f"""      <article class="problem">
        <h3>{esc(t)}</h3>
        <p>{esc(d)}</p>
        <a class="problem-link" href="/#servicios">Ver el detalle técnico →</a>
      </article>""" for t, d, _ in orden
    )
    titulo = pick(l, [
        f"En qué puedo ayudarte en {n}",
        f"Peritajes informáticos que hago en {n}",
        f"Qué analizo para clientes de {n}",
    ], "serv")
    return f"""<section class="band" id="servicios" aria-labelledby="h2-serv">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Servicios</span>
      <h2 id="h2-serv">{esc(titulo)}</h2>
      <p class="lead">Para particulares y para despachos de abogados. Si tu caso no encaja en ninguno, cuéntamelo igualmente.</p>
    </div>
    <div class="problems">
{cards}
    </div>
    <p class="note-out">No hago intrusiones en cuentas o dispositivos ajenos ni “espío” móviles: solo analizo pruebas a las que tienes derecho legítimo de acceso.</p>
  </div>
</section>"""


def faqs(l):
    n = l["nombre"]
    d = redondea(l["dist"])
    out = []
    if l["modo"] == "base":
        out.append((f"¿Dónde nos vemos en Alcalá de Henares?",
                    "Quedamos donde te resulte más cómodo dentro de Alcalá. Muchas consultas se resuelven además por WhatsApp o teléfono sin necesidad de vernos."))
    elif l["modo"] == "local":
        out.append((f"¿Tengo que ir a Alcalá de Henares si vivo en {n}?",
                    f"No. Estoy a unos {d} km de {n}: cuando hay que ver un teléfono o recoger una prueba, voy yo. La primera consulta se hace por WhatsApp, teléfono o correo."))
    else:
        out.append((f"¿Puedes hacer un peritaje para {n} sin venir?",
                    f"Sí, en la mayoría de los casos. Correos, archivos y copias de conversaciones se reciben a distancia con huella SHA-256 y cadena de custodia. Cuando hay que analizar un teléfono, valoramos juntos el envío o el desplazamiento a {n}."))
    juz = f"los juzgados del partido judicial de {l['partido']}"
    if l["modo"] in ("base", "local"):
        out.append((f"¿Ratificas el informe en {juz}?",
                    f"Sí. Si el juzgado cita al perito para ratificar el informe, acudo en persona a {juz} y respondo a las preguntas del juez y de las partes."))
    else:
        out.append((f"¿Y si hay que ratificar el informe en {n}?",
                    f"Si el juzgado de {n} acepta la videoconferencia, la ratificación se puede hacer a distancia. Si exige presencia, me desplazo y el coste del viaje aparece en el presupuesto desde el principio, sin sorpresas."))
    out.append((pick(l, [f"¿Cuánto cuesta un perito informático en {n}?", f"¿Qué precio tiene un informe pericial informático en {n}?"], "faqp"),
                "Depende del tipo de prueba, del volumen de información y de si hay que acudir a juicio. La primera consulta es gratuita y, si seguimos, recibes un presupuesto cerrado por escrito antes de empezar."))
    out.append(("¿Necesito abogado para contratarte?",
                "No. Muchas personas me consultan antes de tener abogado para saber si su prueba se sostiene. Si después hay procedimiento, me coordino con tu abogado."))
    return out


def bloque_faq(l, preguntas):
    items = "\n".join(
        f'      <details class="qa"><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>'
        for q, a in preguntas
    )
    return f"""<section id="preguntas" aria-labelledby="h2-faq">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">Dudas habituales</span>
      <h2 id="h2-faq">Preguntas desde {esc(l['nombre'])}</h2>
    </div>
    <div class="faq">
{items}
    </div>
  </div>
</section>"""


def bloque_cercanos(l):
    links = "\n".join(
        f'      <li><a href="{o["url"]}">Perito informático en {esc(o["nombre"])}</a></li>' for o in cercanos(l)
    )
    titulo = "Zonas cercanas" if l["modo"] in ("base", "local") else "Otras ciudades donde trabajo"
    return f"""<section class="band" id="zonas" aria-labelledby="h2-zonas">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">También atiendo</span>
      <h2 id="h2-zonas">{titulo}</h2>
    </div>
    <ul class="zone-links">
{links}
    </ul>
    <p class="zone-all"><a href="/zonas/">Ver todas las zonas →</a></p>
  </div>
</section>"""


def bloque_contacto(l):
    return f"""<section id="contacto" aria-labelledby="h2-contacto">
  <div class="wrap">
    <div class="cta-local">
      <div>
        <span class="eyebrow">Primera consulta gratuita</span>
        <h2 id="h2-contacto">Cuéntame qué ha pasado</h2>
        <p class="lead">Con dos o tres frases me basta para orientarte. Te respondo en menos de 24 horas.</p>
      </div>
      <div class="hero-ctas">
        <a class="btn btn-wa" href="{wa_link(l)}" target="_blank" rel="noopener">{ICON_WA} Escríbeme por WhatsApp</a>
        <a class="btn btn-ghost" href="tel:{TEL}">{ICON_TEL} {TEL_H}</a>
        <a class="btn btn-ghost" href="/#contacto">Formulario de contacto</a>
      </div>
    </div>
  </div>
</section>"""


# ───────────────────────── esqueleto ─────────────────────────
HEAD_BRAND = """<a class="brand" href="/" aria-label="informeperitoinformatico.es — inicio">
      <svg class="brand-mark" width="38" height="42" viewBox="0 0 36 40" aria-hidden="true">
        <polygon points="18,2 34,11 34,29 18,38 2,29 2,11" fill="#0f6e67"/>
        <circle cx="16" cy="18" r="6.5" fill="none" stroke="#fbf7f1" stroke-width="2.2"/>
        <line x1="20.8" y1="22.8" x2="26" y2="28" stroke="#fbf7f1" stroke-width="2.6" stroke-linecap="round"/>
        <path d="M12.6 18.3l2.3 2.2 4-4.3" fill="none" stroke="#e9a23b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <span class="brand-text">
        <span class="brand-name">Enrique Delgado</span>
        <span class="brand-sub">Perito informático · Alcalá de Henares</span>
      </span>
    </a>"""


def header():
    return f"""<header class="site-head">
  <div class="wrap head-inner">
    {HEAD_BRAND}
    <nav aria-label="Principal">
      <ul class="nav">
        <li><a href="/#te-ayudo">¿Qué te ha pasado?</a></li>
        <li><a href="/#como-trabajo">Cómo trabajo</a></li>
        <li><a href="/#precio">Precio</a></li>
        <li><a href="/zonas/">Zonas</a></li>
        <li><a class="btn btn-primary btn-sm" href="#contacto">Consulta gratis</a></li>
      </ul>
    </nav>
    <button class="menu-btn" id="menu-btn" aria-expanded="false" aria-controls="mobile-nav">
      <span class="bars" aria-hidden="true"><span></span><span></span><span></span></span>
      <span class="label">Menú</span>
    </button>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="Menú móvil">
    <a href="/">Inicio</a>
    <a href="/#te-ayudo">¿Qué te ha pasado?</a>
    <a href="/#servicios">Servicios</a>
    <a href="/#precio">Precio</a>
    <a href="/#preguntas">Preguntas frecuentes</a>
    <a href="/zonas/">Zonas donde trabajo</a>
    <a href="#contacto">Contacto</a>
  </nav>
</header>"""


def footer():
    return f"""<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>Enrique Delgado · Perito informático</h4>
        <p>Informes periciales de WhatsApp, correo electrónico, capturas de pantalla, imágenes y dispositivos móviles para particulares y abogados. Alcalá de Henares, Comunidad de Madrid y toda España.</p>
      </div>
      <div>
        <h4>Zonas</h4>
        <ul>
          <li><a href="/perito-informatico-alcala-de-henares/">Alcalá de Henares</a></li>
          <li><a href="/perito-informatico-madrid/">Madrid</a></li>
          <li><a href="/perito-informatico-guadalajara/">Guadalajara</a></li>
          <li><a href="/zonas/">Todas las zonas</a></li>
        </ul>
      </div>
      <div>
        <h4>Legal</h4>
        <ul>
          <li><a href="/aviso_legal.html">Aviso legal</a></li>
          <li><a href="/privacidad.html">Política de privacidad</a></li>
          <li><a href="/cookies.html">Política de cookies</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© 2026 informeperitoinformatico.es</span>
      <span>Esta web no usa cookies ni rastreadores.</span>
    </div>
  </div>
</footer>"""


def quickbar(l=None):
    wa = wa_link(l) if l else f"https://wa.me/{WA}"
    return f"""<div class="quickbar" aria-label="Contacto rápido">
  <a class="btn btn-ghost" href="tel:{TEL}">Llamar</a>
  <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
</div>"""


def documento(title, desc, canonical, jsonld, cuerpo, og_title=None):
    ld = "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(j, ensure_ascii=False, indent=2)}\n</script>' for j in jsonld
    )
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Enrique Delgado — Perito Informático">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="theme-color" content="#fbf7f1">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{esc(og_title or title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="informeperitoinformatico.es">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preload" href="/assets/fonts/fraunces-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/atkinson-hyperlegible-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
{ld}
</head>
<body class="has-quickbar">
<a class="skip" href="#main">Saltar al contenido</a>
{header()}
<main id="main">
{cuerpo}
</main>
{footer()}
{quickbar()}
<script src="/main.js" defer></script>
</body>
</html>
"""


# ───────────────────────── página local ─────────────────────────
def pagina(l):
    n = l["nombre"]
    canonical = SITE + l["url"]
    title = f"Perito Informático en {n} | WhatsApp, Correos y Capturas"
    if len(title) > 65:
        title = f"Perito Informático en {n} | WhatsApp y Correos"
    if len(title) > 65:
        title = f"Perito Informático en {n}"
    desc_opts = [
        f"Perito informático en {n} para particulares y abogados. Peritaje de WhatsApp, correos, capturas y móviles con informe UNE 197010. Primera consulta gratuita.",
        f"¿Necesitas un perito informático en {n}? Analizo WhatsApp, correos electrónicos, capturas y teléfonos y te lo explico sin tecnicismos. Consulta gratis.",
        f"Informes periciales informáticos en {n}: autenticidad de WhatsApp, correos falsos, capturas e imágenes y móviles. Respuesta en 24 h y primera consulta gratuita.",
    ]
    desc = pick(l, desc_opts, "desc")
    preguntas = faqs(l)

    place = {"@type": "City", "name": n,
             "containedInPlace": {"@type": "AdministrativeArea", "name": l["provincia"] if l["provincia"] != l["ccaa"] else l["ccaa"]}}
    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "@id": canonical + "#servicio",
            "name": f"Perito informático en {n}",
            "serviceType": "Peritaje informático",
            "url": canonical,
            "description": desc,
            "provider": {"@id": SITE + "/#organization"},
            "areaServed": place,
            "availableChannel": {
                "@type": "ServiceChannel",
                "servicePhone": {"@type": "ContactPoint", "telephone": TEL, "contactType": "customer service", "availableLanguage": "es"},
                "serviceUrl": canonical,
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Zonas", "item": SITE + "/zonas/"},
                {"@type": "ListItem", "position": 3, "name": f"Perito informático en {n}", "item": canonical},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preguntas
            ],
        },
    ]

    if l["modo"] in ("base", "local"):
        eyebrow = f"{ICON_PIN} {esc(n)} · atención presencial"
    else:
        eyebrow = f"{ICON_PIN} {esc(n)} · a distancia y en persona cuando hace falta"

    hero = f"""<section class="hero hero-local" id="inicio" aria-labelledby="h1">
  <div class="wrap">
    <nav class="crumbs" aria-label="Migas de pan"><a href="/">Inicio</a><span aria-hidden="true">›</span><a href="/zonas/">Zonas</a><span aria-hidden="true">›</span><span aria-current="page">{esc(n)}</span></nav>
    <span class="eyebrow">{eyebrow}</span>
    <h1 id="h1">Perito informático en <em>{esc(n)}</em></h1>
    <p class="lead">{esc(lead(l))}</p>
    <div class="hero-ctas">
      <a class="btn btn-wa" href="{wa_link(l)}" target="_blank" rel="noopener">{ICON_WA} Escríbeme por WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{TEL}">{ICON_TEL} {TEL_H}</a>
    </div>
    <ul class="reassure">
      <li>{ICON_CHECK}Primera consulta gratuita</li>
      <li>{ICON_CHECK}Presupuesto cerrado por escrito</li>
      <li>{ICON_CHECK}Informes conforme a UNE 197010</li>
    </ul>
  </div>
</section>"""

    cuerpo = "\n\n".join([
        hero,
        bloque_servicios(l),
        bloque_modalidad(l),
        bloque_juzgado(l),
        bloque_faq(l, preguntas),
        bloque_cercanos(l),
        bloque_contacto(l),
    ])
    html_doc = documento(title, desc, canonical, jsonld, cuerpo, og_title=f"Perito informático en {n}")
    # el quickbar lleva el texto de WhatsApp con la ciudad
    html_doc = html_doc.replace(quickbar(), quickbar(l))
    return html_doc


# ───────────────────────── índice de zonas ─────────────────────────
def pagina_zonas():
    grupos = [
        ("Corredor del Henares", "Atención presencial desde Alcalá de Henares, en la parte madrileña y en la de Guadalajara.",
         [l for l in LUGARES if l["tipo"] == "corredor"]),
        ("Comunidad de Madrid · partidos judiciales", "Cabezas de partido judicial de la Comunidad de Madrid. Me desplazo para extracciones y ratificaciones.",
         [l for l in LUGARES if l["tipo"] == "partido"] + [POR_NOMBRE[p] for p in ("Alcalá de Henares", "Torrejón de Ardoz", "Coslada")]),
        ("Capitales de provincia", "Trabajo a distancia con cadena de custodia y me desplazo cuando el caso lo requiere.",
         [l for l in LUGARES if l["tipo"] == "capital" or l.get("capital")]),
    ]
    secciones = []
    for i, (t, d, ls) in enumerate(grupos):
        vistos, uniq = set(), []
        for l in ls:
            if l["slug"] not in vistos:
                vistos.add(l["slug"])
                uniq.append(l)
        uniq.sort(key=lambda x: slugify(x["nombre"]))
        li = "\n".join(f'      <li><a href="{l["url"]}">{esc(l["nombre"])}</a></li>' for l in uniq)
        band = ' class="band"' if i % 2 == 0 else ""
        secciones.append(f"""<section{band} aria-labelledby="h2-z{i}">
  <div class="wrap">
    <div class="section-head">
      <h2 id="h2-z{i}">{esc(t)}</h2>
      <p class="lead">{esc(d)}</p>
    </div>
    <ul class="zone-links">
{li}
    </ul>
  </div>
</section>""")
    canonical = SITE + "/zonas/"
    hero = f"""<section class="hero hero-local" aria-labelledby="h1">
  <div class="wrap">
    <nav class="crumbs" aria-label="Migas de pan"><a href="/">Inicio</a><span aria-hidden="true">›</span><span aria-current="page">Zonas</span></nav>
    <span class="eyebrow">{ICON_PIN} Alcalá de Henares, Madrid y toda España</span>
    <h1 id="h1">Zonas donde trabajo como <em>perito informático</em></h1>
    <p class="lead">Trabajo desde Alcalá de Henares. En el Corredor del Henares y la Comunidad de Madrid atiendo en persona; en el resto de España, a distancia y con desplazamiento cuando el caso lo pide.</p>
  </div>
</section>"""
    jsonld = [{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Zonas", "item": canonical},
        ],
    }]
    cuerpo = hero + "\n\n" + "\n\n".join(secciones) + "\n\n" + bloque_contacto(None)
    return documento(
        "Zonas de servicio | Perito Informático Enrique Delgado",
        "Perito informático en Alcalá de Henares, el Corredor del Henares, los partidos judiciales de la Comunidad de Madrid y las capitales de provincia de España.",
        canonical, jsonld, cuerpo)


# ───────────────────────── sitemap ─────────────────────────
def sitemap():
    urls = [(SITE + "/", "monthly", "1.0"), (SITE + "/zonas/", "monthly", "0.7")]
    orden = sorted(LUGARES, key=lambda l: ({"base": 0, "local": 1, "cercana": 2, "remota": 3}[l["modo"]], l["dist"]))
    for l in orden:
        pr = {"base": "0.9", "local": "0.8", "cercana": "0.6", "remota": "0.5"}[l["modo"]]
        urls.append((SITE + l["url"], "monthly", pr))
    body = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{HOY}</lastmod>\n    <changefreq>{c}</changefreq>\n    <priority>{p}</priority>\n  </url>"
        for u, c, p in urls
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'


def main():
    # limpia páginas locales anteriores para no dejar huérfanas
    for d in os.listdir(ROOT):
        p = os.path.join(ROOT, d)
        if d.startswith("perito-informatico-") and os.path.isdir(p):
            idx = os.path.join(p, "index.html")
            if os.path.exists(idx):
                os.remove(idx)
            if not os.listdir(p):
                os.rmdir(p)
    for l in LUGARES:
        d = os.path.join(ROOT, l["url"].strip("/"))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina(l))
    os.makedirs(os.path.join(ROOT, "zonas"), exist_ok=True)
    with open(os.path.join(ROOT, "zonas", "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina_zonas())
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap())
    modos = {}
    for l in LUGARES:
        modos[l["modo"]] = modos.get(l["modo"], 0) + 1
    print(f"{len(LUGARES)} páginas locales + /zonas/ + sitemap.xml  ·  {modos}")


if __name__ == "__main__":
    main()

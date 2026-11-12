#!/usr/bin/env python3
"""Genera las páginas de servicio (/peritaje-<servicio>/).

Uso (desde la raíz del repositorio):
    python3 _tools/generar_servicios.py && python3 _tools/generar_zonas.py

El segundo comando regenera el sitemap incluyendo estas páginas.
Reutiliza cabecera, pie y plantilla de generar_zonas.py. Las preguntas del
FAQPage (JSON-LD) salen de la misma lista que las visibles, así coinciden siempre.
"""
import os
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar_zonas as gz  # noqa: E402

SITE = gz.SITE
esc = gz.esc

# Al añadir una página aquí (GENERADORES, al final), añadirla también a
# PAGINAS_SERVICIO y SERVICIO_URL en generar_zonas.py (sitemap y enlaces).


def wa(texto):
    return f"https://wa.me/{gz.WA}?text={quote(texto)}"


def tarjetas(items):
    return "\n".join(
        f"""      <article class="problem">
        <h3>{esc(t)}</h3>
        <p>{esc(d)}</p>
      </article>""" for t, d in items
    )


def bloque_faq(titulo, preguntas):
    items = "\n".join(
        f'      <details class="qa"><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>'
        for q, a in preguntas
    )
    return f"""<section id="preguntas" aria-labelledby="h2-faq">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">Dudas habituales</span>
      <h2 id="h2-faq">{esc(titulo)}</h2>
    </div>
    <div class="faq">
{items}
    </div>
  </div>
</section>"""


# ───────────────────────── Peritaje de WhatsApp ─────────────────────────
WA_CASOS = [
    ("Acoso o amenazas", "Mensajes que demuestran lo que está pasando y que necesitas presentar sin que puedan decir que los has inventado."),
    ("Deudas, alquileres y acuerdos", "Un préstamo, una señal, un acuerdo de pago o una orden de trabajo que solo quedó por escrito en WhatsApp."),
    ("Conflictos laborales", "Instrucciones, cambios de horario, avisos de despido o conversaciones con la empresa que hay que acreditar."),
    ("Familia y custodia", "Comunicaciones sobre los hijos, el régimen de visitas o la pensión que forman parte del procedimiento."),
    ("Te acusan con capturas", "La otra parte aporta pantallazos que crees falsos o sacados de contexto y necesitas una contrapericial."),
    ("Mensajes borrados o editados", "Se eliminó un mensaje clave o se editó después. Vemos si quedan rastros técnicos que lo acrediten."),
]

WA_ANALISIS = [
    ("Origen y autoría", "Qué número envió cada mensaje, en qué conversación y desde qué dispositivo, a partir de la base de datos de la aplicación y no de una imagen."),
    ("Integridad con hash", "Calculo huellas SHA-256 de todo lo adquirido. Cualquier cambio posterior, por pequeño que sea, se detectaría."),
    ("Cotejo de capturas", "Comparo cada pantallazo con el registro original: texto, fecha, hora, remitente y orden de los mensajes."),
    ("Eliminados y editados", "Rastros de mensajes borrados «para todos» o editados, cuando el dispositivo y el tiempo transcurrido lo permiten."),
    ("Audios, fotos y documentos", "Archivos adjuntos con su fecha, su vínculo con el mensaje en que se enviaron y sus metadatos."),
    ("Telegram, Signal e Instagram", "El mismo método para otras aplicaciones de mensajería y redes sociales, adaptado a cómo guarda los datos cada una."),
]

WA_FAQ = [
    ("¿Tengo que dejarte el móvil?",
     "Solo el tiempo de la adquisición, que se hace con el teléfono delante y suele resolverse en una sesión. En el Corredor del Henares y la Comunidad de Madrid voy yo; en el resto de España valoramos juntos la mejor opción."),
    ("¿Puedo exportar el chat yo mismo y enviártelo?",
     "La opción «Exportar chat» de WhatsApp genera un texto que cualquiera puede editar, así que no acredita nada por sí sola. Sirve para que me hagas una idea del caso, pero el informe se hace sobre el teléfono o su copia de seguridad."),
    ("¿Se pueden recuperar mensajes de WhatsApp borrados?",
     "A veces sí. Depende del modelo de teléfono, del tiempo transcurrido y de si existen copias de seguridad. Antes de empezar te digo con franqueza qué es razonable esperar."),
    ("¿Y si la conversación está en el móvil de la otra persona?",
     "Si participaste en ella, normalmente también está en tu teléfono y se analiza ahí. El dispositivo de otra persona solo se puede analizar con su consentimiento o por orden judicial, que tu abogado puede solicitar."),
    ("¿No basta con un acta notarial?",
     "El notario da fe de lo que ve en la pantalla, pero no comprueba si la conversación ha sido manipulada ni quién la escribió. Si la otra parte impugna los mensajes, lo que resuelve la duda es el análisis técnico de un perito."),
    ("¿Trabajas fuera de Madrid, por ejemplo en Sevilla, Málaga o Valencia?",
     "Sí, atiendo casos de toda España. Muchas veces la adquisición puede hacerse a distancia con cadena de custodia y huellas SHA-256; si hace falta, me desplazo. La ratificación puede hacerse por videoconferencia cuando el juzgado lo admite."),
    ("¿Cuánto cuesta un peritaje de WhatsApp?",
     "Depende del número de conversaciones y mensajes, de cómo haya que extraerlos, de la urgencia y de si hay que ratificar el informe en juicio. La primera consulta es gratuita y, si seguimos, recibes un presupuesto cerrado por escrito antes de empezar."),
]


def pagina_whatsapp():
    slug = "peritaje-whatsapp"
    url = f"{SITE}/{slug}/"
    title = "Perito Informático de WhatsApp | Informe pericial para juicio"
    desc = ("Peritaje de WhatsApp para juicio: analizo la conversación en el teléfono original, cotejo "
            "capturas y busco mensajes borrados. Toda España. Consulta gratis.")
    wa_txt = "Hola Enrique, quería consultarte un caso de mensajes de WhatsApp."

    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "@id": url + "#servicio",
            "name": "Peritaje informático de WhatsApp",
            "alternateName": ["Perito de WhatsApp", "Informe pericial de WhatsApp"],
            "serviceType": "Peritaje informático de mensajería",
            "url": url,
            "description": desc,
            "provider": {"@id": SITE + "/#organization"},
            "areaServed": {"@type": "Country", "name": "España"},
            "availableChannel": {
                "@type": "ServiceChannel",
                "servicePhone": {"@type": "ContactPoint", "telephone": gz.TEL, "contactType": "customer service", "availableLanguage": "es"},
                "serviceUrl": url,
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Servicios", "item": SITE + "/#servicios"},
                {"@type": "ListItem", "position": 3, "name": "Peritaje de WhatsApp", "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in WA_FAQ
            ],
        },
    ]

    hero = f"""<section class="hero hero-local" id="inicio" aria-labelledby="h1">
  <div class="wrap">
    <nav class="crumbs" aria-label="Migas de pan"><a href="/">Inicio</a><span aria-hidden="true">›</span><a href="/#servicios">Servicios</a><span aria-hidden="true">›</span><span aria-current="page">WhatsApp</span></nav>
    <span class="eyebrow">Peritaje de WhatsApp y mensajería</span>
    <h1 id="h1">Perito informático de <em>WhatsApp</em></h1>
    <p class="lead">Analizo la conversación original en tu teléfono, la fijo con huellas digitales y la presento en un informe pericial que el juez puede valorar con garantías. Para particulares y abogados, en Madrid y en toda España.</p>
    <div class="hero-ctas">
      <a class="btn btn-wa" href="{wa(wa_txt)}" target="_blank" rel="noopener">{gz.ICON_WA} Escríbeme por WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{gz.TEL}">{gz.ICON_TEL} {gz.TEL_H}</a>
    </div>
    <ul class="reassure">
      <li>{gz.ICON_CHECK}Primera consulta gratuita</li>
      <li>{gz.ICON_CHECK}Presupuesto cerrado por escrito</li>
      <li>{gz.ICON_CHECK}Informes conforme a UNE 197010</li>
    </ul>
  </div>
</section>"""

    casos = f"""<section class="band" id="casos" aria-labelledby="h2-casos">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Cuándo lo necesitas</span>
      <h2 id="h2-casos">Casos en los que un peritaje de WhatsApp marca la diferencia</h2>
      <p class="lead">Si tu caso no está aquí, cuéntamelo igualmente: te digo si un informe tiene sentido antes de que gastes nada.</p>
    </div>
    <div class="problems">
{tarjetas(WA_CASOS)}
    </div>
  </div>
</section>"""

    pantallazo = """<section id="pantallazos" aria-labelledby="h2-pantallazos">
  <div class="wrap first-aid">
    <div>
      <span class="eyebrow">La pregunta más habitual</span>
      <h2 id="h2-pantallazos">¿No basta con un <em>pantallazo</em>?</h2>
      <p class="lead">A veces sí, pero no te fíes. Desde la sentencia del Tribunal Supremo 300/2015, si la otra parte impugna una conversación con argumentos, hay que demostrar su origen, su autoría y su integridad. Y hoy fabricar un chat falso con apariencia real está al alcance de cualquiera.</p>
      <p><a class="problem-link" href="/articulos/pantallazos-whatsapp-prueba-juicio/">Lee qué dice el Supremo sobre los pantallazos →</a></p>
    </div>
    <ol>
      <li><strong>Una captura es una imagen</strong><span>Se puede recortar, editar o generar desde cero. No dice nada de quién escribió el mensaje ni de si es completo.</span></li>
      <li><strong>El chat exportado es texto editable</strong><span>«Exportar chat» genera un archivo que cualquiera puede modificar con un editor.</span></li>
      <li><strong>Lo que da solidez es el original</strong><span>La base de datos de la aplicación en el teléfono, adquirida con cadena de custodia y explicada en un informe.</span></li>
    </ol>
  </div>
</section>"""

    analisis = f"""<section class="band" id="que-analizo" aria-labelledby="h2-analizo">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">El detalle técnico</span>
      <h2 id="h2-analizo">Qué analizo exactamente</h2>
      <p class="lead">Trabajo sobre la base de datos de la aplicación (msgstore.db en Android, ChatStorage.sqlite en iPhone) o sobre la copia de seguridad, nunca sobre la imagen.</p>
    </div>
    <div class="problems">
{tarjetas(WA_ANALISIS)}
    </div>
    <div class="standards" aria-label="Normas de referencia">
      Trabajo conforme a: <span class="pill">UNE 197010</span><span class="pill">UNE 71505-3</span><span class="pill">ISO/IEC 27037</span><span class="pill">LEC arts. 335–352</span>
    </div>
    <p class="note-out">No accedo a teléfonos ni cuentas ajenos ni «espío» un WhatsApp: solo analizo conversaciones a las que tienes derecho legítimo de acceso.</p>
  </div>
</section>"""

    pasos = """<section id="como-trabajo" aria-labelledby="h2-proceso">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">Sin sorpresas</span>
      <h2 id="h2-proceso">Cómo es un peritaje de WhatsApp, paso a paso</h2>
    </div>
    <ol class="steps">
      <li class="step">
        <h3>Me cuentas el caso</h3>
        <p>Por WhatsApp, teléfono o correo. Te digo con franqueza si un informe te ayuda y qué conversaciones conviene analizar.</p>
        <span class="tag">Gratis</span>
      </li>
      <li class="step">
        <h3>Presupuesto</h3>
        <p>Recibes por escrito qué incluye, el plazo y el precio cerrado. Tú decides sin compromiso.</p>
        <span class="tag">Por escrito</span>
      </li>
      <li class="step">
        <h3>Adquisición</h3>
        <p>Con el teléfono delante, extraigo la conversación sin alterarla y documento cada paso de la cadena de custodia.</p>
        <span class="tag">Hash SHA-256</span>
      </li>
      <li class="step">
        <h3>Informe y juicio</h3>
        <p>Te entrego el informe y te lo explico. Si hay que ratificarlo ante el juez, allí estaré para defenderlo.</p>
        <span class="tag">UNE 197010</span>
      </li>
    </ol>
  </div>
</section>"""

    precio = """<section class="band" id="precio" aria-labelledby="h2-precio">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Hablemos claro</span>
      <h2 id="h2-precio">¿Cuánto cuesta un peritaje de WhatsApp?</h2>
      <p class="lead">No te voy a dar una tarifa genérica que luego no se cumple. Lo que sí te garantizo:</p>
    </div>
    <div class="price">
      <div class="price-card highlight">
        <p class="big">0 €</p>
        <h3>La primera consulta</h3>
        <p>Me cuentas tu caso y te digo, sin compromiso, si un informe pericial te va a ayudar. Si no lo necesitas, te lo digo.</p>
      </div>
      <div class="price-card">
        <h3>Presupuesto cerrado, antes de empezar</h3>
        <p>El precio depende sobre todo de:</p>
        <ul>
          <li>Cuántas conversaciones y qué periodo hay que analizar</li>
          <li>Si se trabaja con el teléfono o con una copia de seguridad</li>
          <li>Si hay que buscar mensajes eliminados o cotejar capturas de la otra parte</li>
          <li>La urgencia y los plazos del procedimiento</li>
          <li>Si hace falta ratificar el informe en juicio</li>
        </ul>
      </div>
    </div>
  </div>
</section>"""

    relacionados = """<section id="leer-mas" aria-labelledby="h2-leer">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Para leer con calma</span>
      <h2 id="h2-leer">Artículos relacionados</h2>
    </div>
    <ul class="zone-links">
      <li><a href="/articulos/pantallazos-whatsapp-prueba-juicio/">¿Basta un pantallazo de WhatsApp como prueba?</a></li>
      <li><a href="/articulos/primeras-horas-conservar-prueba-digital/">Qué hacer en las primeras horas para no perder la prueba</a></li>
      <li><a href="/articulos/pruebas-falsas-inteligencia-artificial/">Pruebas falsas hechas con IA en los juicios</a></li>
      <li><a href="/articulos/como-elegir-perito-informatico/">Cómo elegir un perito informático</a></li>
    </ul>
    <p class="zone-all"><a href="/zonas/">Ver las zonas donde trabajo →</a></p>
  </div>
</section>"""

    contacto = f"""<section class="band" id="contacto" aria-labelledby="h2-contacto">
  <div class="wrap">
    <div class="cta-local">
      <div>
        <span class="eyebrow">Primera consulta gratuita</span>
        <h2 id="h2-contacto">Cuéntame qué mensajes necesitas acreditar</h2>
        <p class="lead">Con dos o tres frases me basta para orientarte. Mientras tanto, no borres el chat ni reinstales WhatsApp. Te respondo en menos de 24 horas.</p>
      </div>
      <div class="hero-ctas">
        <a class="btn btn-wa" href="{wa(wa_txt)}" target="_blank" rel="noopener">{gz.ICON_WA} Escríbeme por WhatsApp</a>
        <a class="btn btn-ghost" href="tel:{gz.TEL}">{gz.ICON_TEL} {gz.TEL_H}</a>
        <a class="btn btn-ghost" href="/#contacto">Formulario de contacto</a>
      </div>
    </div>
  </div>
</section>"""

    cuerpo = "\n\n".join([hero, casos, pantallazo, analisis, pasos, precio,
                          bloque_faq("Preguntas sobre el peritaje de WhatsApp", WA_FAQ), relacionados, contacto])
    doc = gz.documento(title, desc, url, jsonld, cuerpo, og_title="Perito informático de WhatsApp")
    return doc.replace(gz.quickbar(), gz.quickbar().replace(f"https://wa.me/{gz.WA}", wa(wa_txt)))


GENERADORES = {
    "peritaje-whatsapp": pagina_whatsapp,
}


def main():
    for slug, fn in GENERADORES.items():
        d = os.path.join(gz.ROOT, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(fn())
    print(f"{len(GENERADORES)} páginas de servicio: " + ", ".join(f"/{s}/" for s in GENERADORES))


if __name__ == "__main__":
    main()

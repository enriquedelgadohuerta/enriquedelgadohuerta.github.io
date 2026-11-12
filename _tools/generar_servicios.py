#!/usr/bin/env python3
"""Genera las páginas de servicio (/peritaje-<servicio>/) a partir de la lista SERVICIOS.

Uso (desde la raíz del repositorio):
    python3 _tools/generar_servicios.py && python3 _tools/generar_zonas.py

El segundo comando regenera el sitemap incluyendo estas páginas.
Reutiliza cabecera, pie y plantilla de generar_zonas.py. Las preguntas del
FAQPage (JSON-LD) salen de la misma lista que las visibles, así coinciden siempre.

Al añadir un servicio aquí, añadirlo también a PAGINAS_SERVICIO y SERVICIO_URL
en generar_zonas.py (sitemap, enlaces de las páginas locales).
"""
import os
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar_zonas as gz  # noqa: E402

SITE = gz.SITE
esc = gz.esc

NORMAS = """    <div class="standards" aria-label="Normas de referencia">
      Trabajo conforme a: <span class="pill">UNE 197010</span><span class="pill">UNE 71505-3</span><span class="pill">ISO/IEC 27037</span><span class="pill">LEC arts. 335–352</span>
    </div>"""


# ───────────────────────── contenidos ─────────────────────────
WHATSAPP = {
    "slug": "peritaje-whatsapp",
    "title": "Perito Informático de WhatsApp | Informe pericial para juicio",
    "desc": ("Peritaje de WhatsApp para juicio: analizo la conversación en el teléfono original, cotejo "
             "capturas y busco mensajes borrados. Toda España. Consulta gratis."),
    "og_title": "Perito informático de WhatsApp",
    "nombre": "Peritaje informático de WhatsApp",
    "alternos": ["Perito de WhatsApp", "Informe pericial de WhatsApp"],
    "tipo": "Peritaje informático de mensajería",
    "miga": "WhatsApp",
    "corto": "Peritaje de WhatsApp",
    "wa_txt": "Hola Enrique, quería consultarte un caso de mensajes de WhatsApp.",
    "eyebrow": "Peritaje de WhatsApp y mensajería",
    "h1": "Perito informático de <em>WhatsApp</em>",
    "lead": "Analizo la conversación original en tu teléfono, la fijo con huellas digitales y la presento en un informe pericial que el juez puede valorar con garantías. Para particulares y abogados, en Madrid y en toda España.",
    "casos_h2": "Casos en los que un peritaje de WhatsApp marca la diferencia",
    "casos": [
        ("Acoso o amenazas", "Mensajes que demuestran lo que está pasando y que necesitas presentar sin que puedan decir que los has inventado."),
        ("Deudas, alquileres y acuerdos", "Un préstamo, una señal, un acuerdo de pago o una orden de trabajo que solo quedó por escrito en WhatsApp."),
        ("Conflictos laborales", "Instrucciones, cambios de horario, avisos de despido o conversaciones con la empresa que hay que acreditar."),
        ("Familia y custodia", "Comunicaciones sobre los hijos, el régimen de visitas o la pensión que forman parte del procedimiento."),
        ("Te acusan con capturas", "La otra parte aporta pantallazos que crees falsos o sacados de contexto y necesitas una contrapericial."),
        ("Mensajes borrados o editados", "Se eliminó un mensaje clave o se editó después. Vemos si quedan rastros técnicos que lo acrediten."),
    ],
    "duda_id": "pantallazos",
    "duda_eyebrow": "La pregunta más habitual",
    "duda_h2": "¿No basta con un <em>pantallazo</em>?",
    "duda_lead": "A veces sí, pero no te fíes. Desde la sentencia del Tribunal Supremo 300/2015, si la otra parte impugna una conversación con argumentos, hay que demostrar su origen, su autoría y su integridad. Y hoy fabricar un chat falso con apariencia real está al alcance de cualquiera.",
    "duda_link": ("/articulos/pantallazos-whatsapp-prueba-juicio/", "Lee qué dice el Supremo sobre los pantallazos →"),
    "duda_puntos": [
        ("Una captura es una imagen", "Se puede recortar, editar o generar desde cero. No dice nada de quién escribió el mensaje ni de si es completo."),
        ("El chat exportado es texto editable", "«Exportar chat» genera un archivo que cualquiera puede modificar con un editor."),
        ("Lo que da solidez es el original", "La base de datos de la aplicación en el teléfono, adquirida con cadena de custodia y explicada en un informe."),
    ],
    "analisis_lead": "Trabajo sobre la base de datos de la aplicación (msgstore.db en Android, ChatStorage.sqlite en iPhone) o sobre la copia de seguridad, nunca sobre la imagen.",
    "analisis": [
        ("Origen y autoría", "Qué número envió cada mensaje, en qué conversación y desde qué dispositivo, a partir de la base de datos de la aplicación y no de una imagen."),
        ("Integridad con hash", "Calculo huellas SHA-256 de todo lo adquirido. Cualquier cambio posterior, por pequeño que sea, se detectaría."),
        ("Cotejo de capturas", "Comparo cada pantallazo con el registro original: texto, fecha, hora, remitente y orden de los mensajes."),
        ("Eliminados y editados", "Rastros de mensajes borrados «para todos» o editados, cuando el dispositivo y el tiempo transcurrido lo permiten."),
        ("Audios, fotos y documentos", "Archivos adjuntos con su fecha, su vínculo con el mensaje en que se enviaron y sus metadatos."),
        ("Telegram, Signal e Instagram", "El mismo método para otras aplicaciones de mensajería y redes sociales, adaptado a cómo guarda los datos cada una."),
    ],
    "nota_legal": "No accedo a teléfonos ni cuentas ajenos ni «espío» un WhatsApp: solo analizo conversaciones a las que tienes derecho legítimo de acceso.",
    "pasos_h2": "Cómo es un peritaje de WhatsApp, paso a paso",
    "pasos": [
        ("Me cuentas el caso", "Por WhatsApp, teléfono o correo. Te digo con franqueza si un informe te ayuda y qué conversaciones conviene analizar.", "Gratis"),
        ("Presupuesto", "Recibes por escrito qué incluye, el plazo y el precio cerrado. Tú decides sin compromiso.", "Por escrito"),
        ("Adquisición", "Con el teléfono delante, extraigo la conversación sin alterarla y documento cada paso de la cadena de custodia.", "Hash SHA-256"),
        ("Informe y juicio", "Te entrego el informe y te lo explico. Si hay que ratificarlo ante el juez, allí estaré para defenderlo.", "UNE 197010"),
    ],
    "precio_h2": "¿Cuánto cuesta un peritaje de WhatsApp?",
    "precio_factores": [
        "Cuántas conversaciones y qué periodo hay que analizar",
        "Si se trabaja con el teléfono o con una copia de seguridad",
        "Si hay que buscar mensajes eliminados o cotejar capturas de la otra parte",
        "La urgencia y los plazos del procedimiento",
        "Si hace falta ratificar el informe en juicio",
    ],
    "faq_h2": "Preguntas sobre el peritaje de WhatsApp",
    "faq": [
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
    ],
    "relacionados": [
        ("/articulos/pantallazos-whatsapp-prueba-juicio/", "¿Basta un pantallazo de WhatsApp como prueba?"),
        ("/articulos/primeras-horas-conservar-prueba-digital/", "Qué hacer en las primeras horas para no perder la prueba"),
        ("/articulos/pruebas-falsas-inteligencia-artificial/", "Pruebas falsas hechas con IA en los juicios"),
        ("/articulos/como-elegir-perito-informatico/", "Cómo elegir un perito informático"),
    ],
    "contacto_h2": "Cuéntame qué mensajes necesitas acreditar",
    "contacto_lead": "Con dos o tres frases me basta para orientarte. Mientras tanto, no borres el chat ni reinstales WhatsApp. Te respondo en menos de 24 horas.",
}

CORREO = {
    "slug": "peritaje-correo-electronico",
    "title": "Perito Informático de Correo Electrónico | Peritaje de emails",
    "desc": ("Peritaje de correo electrónico: origen real del email, cabeceras, SPF, DKIM y DMARC, "
             "facturas con otra cuenta y suplantaciones. Toda España. Consulta gratis."),
    "og_title": "Perito informático de correo electrónico",
    "nombre": "Peritaje informático de correo electrónico",
    "alternos": ["Perito de correo electrónico", "Peritaje de email", "Informe pericial de correo electrónico"],
    "tipo": "Peritaje informático de correo electrónico",
    "miga": "Correo electrónico",
    "corto": "Peritaje de correo electrónico",
    "wa_txt": "Hola Enrique, quería consultarte un caso de un correo electrónico.",
    "eyebrow": "Peritaje de correo electrónico",
    "h1": "Perito informático de <em>correo electrónico</em>",
    "lead": "Averiguo desde dónde se envió de verdad un correo, si es auténtico y si alguien ha suplantado a tu empresa o a tu proveedor, y lo presento en un informe pericial que sirve para la denuncia, la reclamación o el juicio. Para particulares, empresas y abogados, en toda España.",
    "casos_h2": "Casos en los que un peritaje de correo electrónico marca la diferencia",
    "casos": [
        ("Factura con otra cuenta bancaria", "Pagaste a un proveedor y el dinero acabó en otra cuenta. Hay que saber si el correo era suyo, si su buzón estaba comprometido o si era un dominio falso."),
        ("Suplantación de tu empresa", "Alguien envía correos en tu nombre o con un dominio casi idéntico al tuyo a tus clientes o a tu banco."),
        ("Correo que niegan haber enviado", "La otra parte dice que nunca mandó ese mensaje, o que el que aportas no es el que se envió."),
        ("Comunicaciones laborales", "Un despido, una sanción, una orden o un aviso por correo cuya fecha, envío o contenido hay que acreditar."),
        ("Phishing y reclamación al banco", "Picaste en un correo falso de tu banco y necesitas documentar cómo ocurrió para reclamar o denunciar."),
        ("Adjuntos manipulados", "Un PDF de factura, un contrato o un presupuesto que alguien ha modificado antes o después de enviarlo."),
    ],
    "duda_id": "impreso",
    "duda_eyebrow": "La pregunta más habitual",
    "duda_h2": "¿No basta con <em>imprimir</em> el correo?",
    "duda_lead": "No. Lo que ves en pantalla (el nombre del remitente, la dirección, la fecha) se puede falsificar con facilidad y no dice por dónde ha pasado el mensaje. Las pruebas técnicas están en las cabeceras, que no aparecen al imprimir ni en una captura.",
    "duda_link": ("/articulos/fraude-factura-cambio-cuenta-bancaria/", "Lee cómo funciona el fraude de la factura →"),
    "duda_puntos": [
        ("El remitente visible se puede falsificar", "El nombre y la dirección que muestra tu programa de correo los elige quien envía el mensaje."),
        ("Reenviar el correo lo altera", "Al reenviarlo se pierden o cambian las cabeceras originales que hay que analizar."),
        ("Lo que da solidez es el original", "El mensaje completo tal como está en el buzón (archivo .eml o .msg), adquirido con huella SHA-256 y explicado en un informe."),
    ],
    "analisis_lead": "Trabajo sobre el mensaje original exportado del buzón, con todas sus cabeceras, y, cuando hace falta, sobre los registros de la cuenta de correo.",
    "analisis": [
        ("Cabeceras completas", "Received, Message-ID, Return-Path y fechas: la ruta real del mensaje servidor a servidor y desde dónde salió."),
        ("SPF, DKIM y DMARC", "Si el servidor que lo envió estaba autorizado por el dominio y si la firma DKIM confirma que el mensaje no se ha alterado."),
        ("Dominios parecidos", "Detección de dominios casi idénticos al legítimo, con su fecha de registro y sus servidores de correo."),
        ("Adjuntos y metadatos", "Autor, programa y fechas de creación y modificación de PDF y documentos de Office, y cambios como un número de cuenta."),
        ("Buzón comprometido", "En Microsoft 365 o Google Workspace, inicios de sesión sospechosos y reglas de reenvío creadas por un intruso."),
        ("Envío y recepción", "Si un correo llegó a su destino y cuándo, a partir de las cabeceras y de los registros disponibles."),
    ],
    "nota_legal": "No accedo a cuentas de correo ajenas: solo analizo buzones y mensajes a los que tienes derecho legítimo de acceso.",
    "pasos_h2": "Cómo es un peritaje de correo electrónico, paso a paso",
    "pasos": [
        ("Me cuentas el caso", "Por WhatsApp, teléfono o correo. Te digo con franqueza si un informe te ayuda y qué mensajes conviene analizar.", "Gratis"),
        ("Presupuesto", "Recibes por escrito qué incluye, el plazo y el precio cerrado. Tú decides sin compromiso.", "Por escrito"),
        ("Adquisición", "Exporto los mensajes originales directamente del buzón, sin reenviarlos, y documento cada paso de la cadena de custodia.", "Hash SHA-256"),
        ("Informe y juicio", "Te entrego el informe y te lo explico. Si hay que ratificarlo ante el juez, allí estaré para defenderlo.", "UNE 197010"),
    ],
    "precio_h2": "¿Cuánto cuesta un peritaje de correo electrónico?",
    "precio_factores": [
        "Cuántos correos y qué periodo hay que analizar",
        "Si hay que revisar los registros de la cuenta (Microsoft 365, Google Workspace…)",
        "Si hay que analizar adjuntos o dominios sospechosos",
        "La urgencia y los plazos del procedimiento",
        "Si hace falta ratificar el informe en juicio",
    ],
    "faq_h2": "Preguntas sobre el peritaje de correo electrónico",
    "faq": [
        ("¿Me sirve el correo impreso o una captura?",
         "Como apoyo, sí; como prueba técnica, no. Ni la impresión ni la captura muestran las cabeceras, que son las que dicen desde dónde y por qué servidores se envió el mensaje."),
        ("¿Puedo reenviarte el correo para que lo analices?",
         "Mejor no: al reenviarlo se pierden datos. Te explico cómo descargar el mensaje original como archivo .eml o .msg, o lo exporto yo directamente del buzón con cadena de custodia."),
        ("Ya he pagado una factura falsa, ¿qué hago?",
         "Llama a tu banco cuanto antes para intentar retener la transferencia y presenta denuncia. No borres ni reenvíes los correos. El informe pericial documenta cómo se produjo el engaño y sirve para la denuncia y para reclamar a quien corresponda."),
        ("¿Se puede saber quién envió el correo?",
         "Normalmente se puede determinar desde qué servidor y en muchos casos desde qué dirección IP salió, y si el dominio era el legítimo. Identificar a la persona concreta suele requerir que el juzgado pida datos al proveedor, y el informe es la base para solicitarlo."),
        ("¿Puedes demostrar que un correo se envió o se recibió?",
         "En muchos casos sí, a partir de las cabeceras del mensaje en el buzón del destinatario o del remitente y de los registros de la cuenta. Antes de empezar te digo qué se puede acreditar con lo que hay."),
        ("¿Trabajas fuera de Madrid, por ejemplo en Málaga, Barcelona o Córdoba?",
         "Sí. El peritaje de correo se hace casi siempre a distancia: los mensajes se exportan del buzón con huellas SHA-256 y cadena de custodia, sin necesidad de desplazarse. La ratificación puede hacerse por videoconferencia cuando el juzgado lo admite."),
        ("¿Cuánto cuesta un peritaje de correo electrónico?",
         "Depende del número de mensajes, de si hay que revisar los registros de la cuenta o analizar adjuntos, de la urgencia y de si hay que ratificar el informe en juicio. La primera consulta es gratuita y, si seguimos, recibes un presupuesto cerrado por escrito antes de empezar."),
    ],
    "relacionados": [
        ("/articulos/fraude-factura-cambio-cuenta-bancaria/", "La factura con otra cuenta bancaria: el fraude BEC"),
        ("/articulos/victima-phishing-smishing-que-hacer/", "He pinchado en un correo falso de mi banco: qué hacer"),
        ("/articulos/primeras-horas-conservar-prueba-digital/", "Qué hacer en las primeras horas para no perder la prueba"),
        ("/articulos/como-elegir-perito-informatico/", "Cómo elegir un perito informático"),
    ],
    "contacto_h2": "Cuéntame qué correo necesitas analizar",
    "contacto_lead": "Con dos o tres frases me basta para orientarte. Mientras tanto, no borres ni reenvíes los mensajes. Te respondo en menos de 24 horas.",
}

SERVICIOS = [WHATSAPP, CORREO]


# ───────────────────────── plantilla ─────────────────────────
def wa(texto):
    return f"https://wa.me/{gz.WA}?text={quote(texto)}"


def tarjetas(items):
    return "\n".join(
        f"""      <article class="problem">
        <h3>{esc(t)}</h3>
        <p>{esc(d)}</p>
      </article>""" for t, d in items
    )


def pagina(s):
    url = f"{SITE}/{s['slug']}/"
    wa_url = wa(s["wa_txt"])
    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "@id": url + "#servicio",
            "name": s["nombre"],
            "alternateName": s["alternos"],
            "serviceType": s["tipo"],
            "url": url,
            "description": s["desc"],
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
                {"@type": "ListItem", "position": 3, "name": s["corto"], "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]
            ],
        },
    ]

    hero = f"""<section class="hero hero-local" id="inicio" aria-labelledby="h1">
  <div class="wrap">
    <nav class="crumbs" aria-label="Migas de pan"><a href="/">Inicio</a><span aria-hidden="true">›</span><a href="/#servicios">Servicios</a><span aria-hidden="true">›</span><span aria-current="page">{esc(s['miga'])}</span></nav>
    <span class="eyebrow">{esc(s['eyebrow'])}</span>
    <h1 id="h1">{s['h1']}</h1>
    <p class="lead">{esc(s['lead'])}</p>
    <div class="hero-ctas">
      <a class="btn btn-wa" href="{wa_url}" target="_blank" rel="noopener">{gz.ICON_WA} Escríbeme por WhatsApp</a>
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
      <h2 id="h2-casos">{esc(s['casos_h2'])}</h2>
      <p class="lead">Si tu caso no está aquí, cuéntamelo igualmente: te digo si un informe tiene sentido antes de que gastes nada.</p>
    </div>
    <div class="problems">
{tarjetas(s['casos'])}
    </div>
  </div>
</section>"""

    puntos = "\n".join(f"      <li><strong>{esc(t)}</strong><span>{esc(d)}</span></li>" for t, d in s["duda_puntos"])
    duda = f"""<section id="{s['duda_id']}" aria-labelledby="h2-{s['duda_id']}">
  <div class="wrap first-aid">
    <div>
      <span class="eyebrow">{esc(s['duda_eyebrow'])}</span>
      <h2 id="h2-{s['duda_id']}">{s['duda_h2']}</h2>
      <p class="lead">{esc(s['duda_lead'])}</p>
      <p><a class="problem-link" href="{s['duda_link'][0]}">{esc(s['duda_link'][1])}</a></p>
    </div>
    <ol>
{puntos}
    </ol>
  </div>
</section>"""

    analisis = f"""<section class="band" id="que-analizo" aria-labelledby="h2-analizo">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">El detalle técnico</span>
      <h2 id="h2-analizo">Qué analizo exactamente</h2>
      <p class="lead">{esc(s['analisis_lead'])}</p>
    </div>
    <div class="problems">
{tarjetas(s['analisis'])}
    </div>
{NORMAS}
    <p class="note-out">{esc(s['nota_legal'])}</p>
  </div>
</section>"""

    pasos_li = "\n".join(f"""      <li class="step">
        <h3>{esc(t)}</h3>
        <p>{esc(d)}</p>
        <span class="tag">{esc(tag)}</span>
      </li>""" for t, d, tag in s["pasos"])
    pasos = f"""<section id="como-trabajo" aria-labelledby="h2-proceso">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">Sin sorpresas</span>
      <h2 id="h2-proceso">{esc(s['pasos_h2'])}</h2>
    </div>
    <ol class="steps">
{pasos_li}
    </ol>
  </div>
</section>"""

    factores = "\n".join(f"          <li>{esc(f)}</li>" for f in s["precio_factores"])
    precio = f"""<section class="band" id="precio" aria-labelledby="h2-precio">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Hablemos claro</span>
      <h2 id="h2-precio">{esc(s['precio_h2'])}</h2>
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
{factores}
        </ul>
      </div>
    </div>
  </div>
</section>"""

    faq_items = "\n".join(
        f'      <details class="qa"><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>'
        for q, a in s["faq"]
    )
    faq = f"""<section id="preguntas" aria-labelledby="h2-faq">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">Dudas habituales</span>
      <h2 id="h2-faq">{esc(s['faq_h2'])}</h2>
    </div>
    <div class="faq">
{faq_items}
    </div>
  </div>
</section>"""

    otros = [o for o in SERVICIOS if o is not s]
    rel = [(u, t) for u, t in s["relacionados"]] + [(f"/{o['slug']}/", o["corto"]) for o in otros]
    rel_li = "\n".join(f'      <li><a href="{u}">{esc(t)}</a></li>' for u, t in rel)
    relacionados = f"""<section id="leer-mas" aria-labelledby="h2-leer">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Para leer con calma</span>
      <h2 id="h2-leer">Artículos y servicios relacionados</h2>
    </div>
    <ul class="zone-links">
{rel_li}
    </ul>
    <p class="zone-all"><a href="/zonas/">Ver las zonas donde trabajo →</a></p>
  </div>
</section>"""

    contacto = f"""<section class="band" id="contacto" aria-labelledby="h2-contacto">
  <div class="wrap">
    <div class="cta-local">
      <div>
        <span class="eyebrow">Primera consulta gratuita</span>
        <h2 id="h2-contacto">{esc(s['contacto_h2'])}</h2>
        <p class="lead">{esc(s['contacto_lead'])}</p>
      </div>
      <div class="hero-ctas">
        <a class="btn btn-wa" href="{wa_url}" target="_blank" rel="noopener">{gz.ICON_WA} Escríbeme por WhatsApp</a>
        <a class="btn btn-ghost" href="tel:{gz.TEL}">{gz.ICON_TEL} {gz.TEL_H}</a>
        <a class="btn btn-ghost" href="/#contacto">Formulario de contacto</a>
      </div>
    </div>
  </div>
</section>"""

    cuerpo = "\n\n".join([hero, casos, duda, analisis, pasos, precio, faq, relacionados, contacto])
    doc = gz.documento(s["title"], s["desc"], url, jsonld, cuerpo, og_title=s["og_title"])
    return doc.replace(gz.quickbar(), gz.quickbar().replace(f"https://wa.me/{gz.WA}", wa_url))


def main():
    for s in SERVICIOS:
        d = os.path.join(gz.ROOT, s["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina(s))
    print(f"{len(SERVICIOS)} páginas de servicio: " + ", ".join(f"/{s['slug']}/" for s in SERVICIOS))


if __name__ == "__main__":
    main()

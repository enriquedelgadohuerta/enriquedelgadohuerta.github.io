#!/usr/bin/env python3
"""Genera /articulos/ (índice) y /articulos/<slug>/ a partir de la lista ARTICULOS.

Uso (desde la raíz del repositorio):
    python3 _tools/generar_articulos.py && python3 _tools/generar_zonas.py

El segundo comando regenera el sitemap incluyendo los artículos.
Para añadir un artículo: añadir un dict a ARTICULOS (el cuerpo es HTML sencillo:
<p>, <h2>, <ul>/<ol>, <strong>).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar_zonas as gz  # noqa: E402  (reutiliza cabecera, pie y plantilla)

SITE = gz.SITE
LINKEDIN = "https://www.linkedin.com/in/perito-informatico-enrique-delgado/"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]

ARTICULOS = [
    {
        "slug": "pantallazos-whatsapp-prueba-juicio",
        "tag": "WhatsApp",
        "fecha": "2026-10-23",
        "titulo": "¿Basta un pantallazo de WhatsApp como prueba en un juicio?",
        "desc": "Qué dice el Tribunal Supremo sobre las capturas de WhatsApp, cuándo hace falta un informe pericial y qué hacer para que tu prueba no se caiga si la impugnan.",
        "resumen": "A veces sí, pero no te fíes: lo que da solidez a la prueba es el original en el teléfono.",
        "cuerpo": """
<p>«Tengo los pantallazos, ¿con eso vale?» Es la pregunta que más me hacen. Y la respuesta corta es: <strong>a veces sí, pero no te fíes</strong>.</p>

<h2>Lo que ha cambiado en los tribunales</h2>
<p>Durante años, la referencia fue la sentencia del Tribunal Supremo 300/2015: si la otra parte impugnaba una conversación aportada en captura, hacía falta una prueba pericial que acreditara su origen, su autoría y su integridad.</p>
<p>En 2025 el Supremo suavizó ese criterio (por ejemplo, en la STS 629/2025): una captura de WhatsApp puede valorarse como prueba sin informe pericial, salvo que existan indicios razonables de manipulación.</p>

<h2>El problema: basta con que la impugnen con argumentos</h2>
<p>Que una captura <em>pueda</em> valer no significa que vaya a valer en tu caso. Si la otra parte la impugna aportando motivos —incoherencias de fechas, mensajes que no encajan, una conversación que no aparece en su teléfono—, vuelve a ser necesario demostrar que es auténtica. Y hoy generar una conversación falsa con apariencia real está al alcance de cualquiera.</p>

<h2>Qué da solidez a la prueba</h2>
<p>No es la imagen, sino el original:</p>
<ul>
<li><strong>La conversación en el propio teléfono</strong>, sin borrar ni reinstalar nada.</li>
<li><strong>Una adquisición documentada</strong>, con huellas digitales (hash SHA-256) que demuestran que nada ha cambiado después.</li>
<li><strong>Un informe pericial</strong> que explique al juez qué se ha analizado, cómo y con qué grado de certeza.</li>
</ul>

<h2>Mi consejo</h2>
<p>Guarda los pantallazos, pero sobre todo <strong>conserva el teléfono tal como está</strong>. Si el asunto llega a juicio y alguien pone en duda tus mensajes, lo agradecerás.</p>
""",
    },
    {
        "slug": "fraude-factura-cambio-cuenta-bancaria",
        "tag": "Correo",
        "fecha": "2026-10-23",
        "titulo": "La factura con otra cuenta bancaria: cómo funciona el fraude y qué hacer",
        "desc": "El fraude del cambio de cuenta (BEC) explicado: cómo se produce, qué revelan las cabeceras del correo (SPF, DKIM, DMARC) y qué hacer si ya has pagado.",
        "resumen": "El remitente se puede falsificar; el rastro técnico del correo, mucho menos.",
        "cuerpo": """
<p>Te llega un correo de tu proveedor de siempre. Misma firma, mismo tono, sin faltas de ortografía. Solo cambia una cosa: «hemos cambiado de banco, a partir de ahora paga en esta cuenta». Pagas. Y el dinero nunca llega a tu proveedor.</p>

<h2>Qué es el fraude del cambio de cuenta</h2>
<p>Es una variante del llamado <strong>BEC</strong> (<em>Business Email Compromise</em>), uno de los fraudes más habituales en pymes y autónomos. INCIBE lo documenta como un caso real y frecuente: los delincuentes suplantan al proveedor, o acceden a su buzón, y aprovechan una conversación legítima para cambiar el número de cuenta.</p>
<p>Suele hacerse de una de estas formas:</p>
<ul>
<li>Con un <strong>dominio casi idéntico</strong> al del proveedor (una letra cambiada, otra terminación).</li>
<li>Con un <strong>remitente falsificado</strong> que muestra la dirección correcta.</li>
<li>Desde el <strong>buzón real del proveedor</strong>, si sus credenciales han sido robadas.</li>
</ul>

<h2>Lo que el correo no puede esconder</h2>
<p>Cada correo lleva unas <strong>cabeceras técnicas</strong> que registran por qué servidores pasó, cuándo y desde dónde se envió, y el resultado de los controles <strong>SPF</strong>, <strong>DKIM</strong> y <strong>DMARC</strong> del dominio. Analizándolas se puede determinar si el mensaje vino de verdad del proveedor, de un dominio parecido o de un buzón comprometido. Esa información es clave para la denuncia y para reclamar al banco.</p>

<h2>Tres consejos</h2>
<ol>
<li><strong>Confirma cualquier cambio de cuenta por teléfono</strong>, a un número que ya tuvieras, nunca al que venga en el propio correo.</li>
<li><strong>No reenvíes ni borres el correo sospechoso</strong>: reenviarlo altera los datos técnicos que hay que analizar.</li>
<li><strong>Si ya has pagado, denuncia cuanto antes</strong> ante la Policía Nacional o la Guardia Civil, avisa a tu banco y conserva el mensaje original.</li>
</ol>
""",
    },
    {
        "slug": "primeras-horas-conservar-prueba-digital",
        "tag": "Evidencia",
        "fecha": "2026-10-23",
        "titulo": "Qué hacer en las primeras horas para no perder una prueba digital",
        "desc": "Cinco cosas que conviene hacer (y no hacer) desde el primer minuto ante un caso de acoso, amenazas o estafa para que la prueba digital siga siendo válida.",
        "resumen": "Lo que haces en las primeras horas decide si la prueba se sostiene después.",
        "cuerpo": """
<p>Cuando alguien me llama por un caso de acoso, amenazas o una estafa, muchas veces la prueba ya está en peligro. No por mala fe, sino por hacer lo que parece lógico: borrar el chat para no verlo, reenviar el correo a alguien de confianza o llevar el móvil a reparar.</p>

<p class="note"><strong>Si estás en peligro, llama al 112.</strong> Puedes denunciar ya: el informe pericial se puede aportar después.</p>

<h2>Cinco cosas desde el primer minuto</h2>
<ol>
<li><strong>No borres nada.</strong> Ni el chat, ni la aplicación, ni el correo. Tampoco vacíes la papelera ni «limpies» el teléfono.</li>
<li><strong>No reenvíes ni restaures copias de seguridad.</strong> Reenviar un correo o restaurar una copia puede cambiar los datos técnicos que hay que analizar.</li>
<li><strong>Haz capturas, pero no te quedes solo con ellas.</strong> Sirven de apoyo, pero se pueden impugnar. Lo que cuenta es el original en el dispositivo o la cuenta.</li>
<li><strong>Guarda el dispositivo tal como está.</strong> No lo formatees ni lo lleves a reparar sin consultarlo antes.</li>
<li><strong>Apunta qué pasó y cuándo.</strong> Una nota con fechas y quién es quién ahorra tiempo de análisis, y por tanto dinero.</li>
</ol>

<h2>¿Y después?</h2>
<p>Con la prueba conservada, un perito puede adquirirla de forma documentada, fijarla con huellas digitales y explicar en un informe qué muestra y qué no. Si tienes dudas sobre tu caso, la primera consulta es gratuita.</p>
""",
    },
]


def fecha_larga(iso):
    a, m, d = iso.split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {a}"


def pagina_articulo(a):
    url = f"{SITE}/articulos/{a['slug']}/"
    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "@id": url + "#articulo",
            "headline": a["titulo"],
            "description": a["desc"],
            "inLanguage": "es-ES",
            "datePublished": a["fecha"],
            "dateModified": a["fecha"],
            "mainEntityOfPage": url,
            "image": f"{SITE}/og-image.jpg",
            "author": {"@type": "Person", "@id": SITE + "/#person", "name": "Enrique Delgado", "url": SITE + "/", "sameAs": [LINKEDIN]},
            "publisher": {"@id": SITE + "/#organization"},
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Artículos", "item": SITE + "/articulos/"},
                {"@type": "ListItem", "position": 3, "name": a["titulo"], "item": url},
            ],
        },
    ]
    otros = "\n".join(
        f'      <li><a href="/articulos/{o["slug"]}/">{gz.esc(o["titulo"])}</a></li>'
        for o in ARTICULOS if o is not a
    )
    cuerpo = f"""<article class="legal article">
  <nav class="crumbs" aria-label="Migas de pan"><a href="/">Inicio</a><span aria-hidden="true">›</span><a href="/articulos/">Artículos</a><span aria-hidden="true">›</span><span aria-current="page">{gz.esc(a['tag'])}</span></nav>
  <span class="eyebrow">{gz.esc(a['tag'])}</span>
  <h1>{gz.esc(a['titulo'])}</h1>
  <p class="meta">Por <a href="{LINKEDIN}" rel="author me noopener" target="_blank">Enrique Delgado</a>, perito informático · {fecha_larga(a['fecha'])}</p>
  <div class="article-body">
{a['cuerpo'].strip()}
  </div>
  <aside class="article-cta" id="contacto">
    <h2>¿Tienes un caso parecido?</h2>
    <p>Cuéntamelo sin compromiso: te digo si un informe pericial te ayuda y cuánto costaría, por escrito.</p>
    <div class="hero-ctas">
      <a class="btn btn-wa" href="https://wa.me/{gz.WA}?text=Hola%20Enrique%2C%20he%20le%C3%ADdo%20tu%20art%C3%ADculo%20y%20quer%C3%ADa%20hacerte%20una%20consulta." target="_blank" rel="noopener">{gz.ICON_WA} Escríbeme por WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{gz.TEL}">{gz.ICON_TEL} {gz.TEL_H}</a>
    </div>
  </aside>
  <section class="article-more" aria-labelledby="h2-mas">
    <h2 id="h2-mas">Sigue leyendo</h2>
    <ul class="zone-links">
{otros}
    </ul>
    <p class="zone-all"><a href="{LINKEDIN}" target="_blank" rel="me noopener">Sígueme en LinkedIn para nuevos artículos →</a></p>
  </section>
</article>"""
    return gz.documento(a["titulo"] + " | Enrique Delgado, perito informático", a["desc"], url, jsonld, cuerpo,
                        og_title=a["titulo"]).replace('<meta property="og:type" content="website">',
                                                       '<meta property="og:type" content="article">')


def pagina_indice():
    url = SITE + "/articulos/"
    cards = "\n".join(f"""      <a class="article-card" href="/articulos/{a['slug']}/">
        <span class="g-tag">{gz.esc(a['tag'])}</span>
        <h2>{gz.esc(a['titulo'])}</h2>
        <p>{gz.esc(a['resumen'])}</p>
        <span class="more">Leer →</span>
      </a>""" for a in sorted(ARTICULOS, key=lambda x: x["fecha"], reverse=True))
    cuerpo = f"""<section class="hero hero-local" aria-labelledby="h1">
  <div class="wrap">
    <nav class="crumbs" aria-label="Migas de pan"><a href="/">Inicio</a><span aria-hidden="true">›</span><span aria-current="page">Artículos</span></nav>
    <span class="eyebrow">Para leer con calma</span>
    <h1 id="h1">Artículos sobre <em>prueba digital</em></h1>
    <p class="lead">Explicaciones breves y sin tecnicismos sobre WhatsApp, correos, capturas y móviles como prueba. También los publico en <a href="{LINKEDIN}" target="_blank" rel="me noopener">LinkedIn</a>.</p>
  </div>
</section>
<section class="band" aria-label="Lista de artículos">
  <div class="wrap">
    <div class="article-grid">
{cards}
    </div>
  </div>
</section>
""" + gz.bloque_contacto(None)
    jsonld = [{
        "@context": "https://schema.org",
        "@type": "Blog",
        "@id": url + "#blog",
        "name": "Artículos sobre prueba digital",
        "url": url,
        "inLanguage": "es-ES",
        "author": {"@id": SITE + "/#person"},
        "publisher": {"@id": SITE + "/#organization"},
        "blogPost": [{"@type": "BlogPosting", "headline": a["titulo"], "url": f"{SITE}/articulos/{a['slug']}/",
                      "datePublished": a["fecha"]} for a in ARTICULOS],
    }]
    return gz.documento("Artículos sobre prueba digital | Enrique Delgado, perito informático",
                        "Artículos sobre WhatsApp, correos electrónicos, capturas y móviles como prueba en un juicio, escritos por un perito informático.",
                        url, jsonld, cuerpo)


def main():
    base = os.path.join(gz.ROOT, "articulos")
    os.makedirs(base, exist_ok=True)
    for a in ARTICULOS:
        d = os.path.join(base, a["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina_articulo(a))
    with open(os.path.join(base, "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina_indice())
    print(f"{len(ARTICULOS)} artículos + /articulos/")


if __name__ == "__main__":
    main()

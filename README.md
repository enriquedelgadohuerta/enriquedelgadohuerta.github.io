# informeperitoinformatico.es

Web profesional de Enrique Delgado, perito informático. Sitio estático publicado con GitHub Pages (dominio en `CNAME`).

## Estructura

```
index.html              Página principal (una sola página con anclas)
styles.css              Estilos compartidos por todas las páginas
main.js                 Menú móvil, animaciones y formulario (sin servidor)
aviso_legal.html        Aviso legal
privacidad.html         Política de privacidad
cookies.html            Política de cookies (la web no usa cookies)
assets/fonts/           Fraunces y Atkinson Hyperlegible (SIL OFL 1.1), autoalojadas
favicon.svg, og-image.jpg, perito-informatico-enrique-delgado-*.jpg
sitemap.xml, robots.txt, CNAME
perito-informatico-*/   Páginas locales (generadas, no editar a mano)
zonas/                  Índice de zonas (generado)
_tools/                 Generador y datos de las páginas locales (no se publica)
```

## Notas

- **Formulario de contacto**: no envía datos a ningún servidor. Compone el mensaje y lo abre en WhatsApp o en el correo del visitante.
- **Sin cookies ni terceros**: no hay Google Fonts, analítica ni avatares externos. Si se añade algo así, actualizar `cookies.html` y `privacidad.html`.
- **Datos estructurados**: `ProfessionalService`, `Person` y `FAQPage` en `index.html`. Las preguntas del JSON-LD deben coincidir con las visibles en la sección `#preguntas`.
- **Casos tipo**: la sección `#casos` contiene ejemplos ilustrativos, no testimonios. No marcar reseñas con Schema.org salvo que sean reales y verificables.

## Páginas locales (SEO local)

Las páginas `/perito-informatico-<lugar>/`, `/zonas/` y `sitemap.xml` se generan con:

```
python3 _tools/generar_zonas.py
```

- Datos en `_tools/zonas.json`: Corredor del Henares (Madrid y Guadalajara), las 21 cabezas de partido judicial de la Comunidad de Madrid y las 52 capitales de provincia.
- Para añadir un municipio, se añade una entrada a `lugares` y se vuelve a ejecutar el script. Para cambiar textos, editar las funciones del script, no el HTML generado.
- Cada página incluye datos estructurados `Service` (proveedor: la organización de la home), `BreadcrumbList` y `FAQPage` coherente con las preguntas visibles.
- El script reescribe `sitemap.xml` entero.

## Buscadores con IA (ChatGPT, Gemini, Copilot, Claude, Perplexity)

- `robots.txt` permite expresamente los rastreadores de búsqueda y de IA (OAI-SearchBot, Google-Extended, Bingbot, Claude-SearchBot, PerplexityBot…).
- `llms.txt`: resumen del sitio para asistentes de IA. Mantenerlo coherente con la home.
- IndexNow: la clave es el fichero `<32 hex>.txt` de la raíz (no borrarlo). Tras publicar, `python3 _tools/indexnow.py` avisa a Bing de todas las URLs del sitemap.

## Artículos

`/articulos/` y cada artículo se generan con `python3 _tools/generar_articulos.py` (lista `ARTICULOS` dentro del script). Después ejecutar `python3 _tools/generar_zonas.py` para regenerar el sitemap con los artículos. Son los mismos contenidos que se publican en LinkedIn.

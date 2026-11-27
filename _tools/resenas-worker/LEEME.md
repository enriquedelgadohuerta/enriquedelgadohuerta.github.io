# Opiniones de Google en la web

La sección **Opiniones en Google** de la portada (`#resenas`) muestra en vivo la valoración media y las reseñas de tu Perfil de Empresa en Google. Esta carpeta no se publica (Jekyll ignora las carpetas que empiezan por `_`).

```
Navegador ──GET /api/resenas──▶ Worker resenas-perito ──▶ Places API (New) · Place Details
   ▲                                  (clave en secreto)        (tu ficha de Google)
   └──────────── JSON con valoración, nº de opiniones y hasta 5 reseñas ◀──┘
```

- **Sincronización:** no hay copia. Cada vez que alguien llega a la sección, el Worker consulta Google; una reseña nueva aparece en cuanto Google la publica. Las condiciones de Google Maps Platform prohíben guardar o cachear reseñas, por eso no hay KV ni JSON en el repositorio.
- **Límite de Google:** Places API devuelve **como máximo 5 reseñas**, las que Google considera más relevantes (no las elige uno). El botón «Ver todas en Google» lleva a la ficha completa.
- **Mientras no esté configurado** (`data-api=""` en `index.html`), la sección permanece oculta. Si Google o el Worker fallan, la sección tampoco aparece.
- **Sin datos estructurados:** no se añade `aggregateRating`/`Review` en JSON‑LD con estas reseñas. Google no admite marcado de reseñas sobre el propio negocio («self‑serving») ni reseñas copiadas de otra plataforma.

## Puesta en marcha (una vez, unos 20 minutos)

### 1. Perfil de Empresa verificado

La ficha debe existir, estar **verificada y visible** en Google Maps. Como empresa de servicios sin local, configúrala como *empresa de servicios a domicilio* con zona de servicio (Alcalá de Henares, Corredor del Henares, Comunidad de Madrid) y la dirección oculta.

### 2. Obtener el Place ID

En <https://developers.google.com/maps/documentation/places/web-service/place-id> busca el nombre de tu ficha y copia el identificador (empieza por `ChIJ…`). Pégalo en `PLACE_ID` de `wrangler.toml`.

### 3. Clave de Places API

1. <https://console.cloud.google.com> → crea el proyecto `web-perito`.
2. *Facturación*: vincula una cuenta de facturación (Google la exige aunque el uso quede dentro de la cuota gratuita mensual) y crea **una alerta de presupuesto de 1 €**.
3. *APIs y servicios → Biblioteca →* habilita **Places API (New)**.
4. *Credenciales → Crear credenciales → Clave de API*. En la clave:
   - **Restricciones de API:** solo *Places API (New)*.
   - Restricciones de aplicación: ninguna (la usa el Worker desde servidor; la protección es que nunca sale de Cloudflare).
5. *Cuotas* de Places API (New): limita *Place Details* a, por ejemplo, **30 solicitudes al día**. Así es imposible pasar de la cuota gratuita aunque alguien recargue la página en bucle: si se alcanza el tope, la sección simplemente no aparece ese día.

### 4. Desplegar el Worker

En tu Mac, dentro de esta carpeta (con `wrangler` ya instalado del Worker de subidas):

```bash
npx wrangler login                    # si no tienes sesión
npx wrangler secret put PLACES_API_KEY  # pega la clave del paso 3
npx wrangler deploy
```

Comprueba: `curl -s https://resenas-perito.<tu-subdominio>.workers.dev/api/resenas | head -c 400`

### 5. Activar la sección

En `index.html`, en `<section id="resenas" … data-api="">`, pon la URL completa:

```html
data-api="https://resenas-perito.subida-perito.workers.dev/api/resenas"
```

Commit y push. La sección aparece sola.

## Pedir reseñas a clientes

Enlace directo para escribir una opinión (útil al cerrar un expediente, por correo o WhatsApp):

```
https://search.google.com/local/writereview?placeid=<PLACE_ID>
```

Pídela a todos los clientes por igual y sin ofrecer nada a cambio: las políticas de Google prohíben incentivarlas o pedirlas solo a clientes satisfechos («review gating»). Y por deber de confidencialidad, no respondas en público confirmando que alguien ha sido cliente ni con datos del caso.

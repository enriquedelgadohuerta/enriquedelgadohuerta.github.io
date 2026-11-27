/*
 * Worker de reseñas — informeperitoinformatico.es
 *
 * Devuelve a la web, en tiempo real, la valoración media y las reseñas de tu
 * Perfil de Empresa de Google, consultando Places API (New) → Place Details.
 *
 * Por qué un Worker y no una llamada desde el navegador: la clave de la API
 * queda guardada como secreto en Cloudflare y no se expone en el HTML.
 *
 * Por qué no se guarda nada: las condiciones de Google Maps Platform prohíben
 * almacenar o cachear el contenido de Places (salvo el place ID). Cada visita
 * que llega a la sección hace una consulta en vivo; no hay KV ni caché.
 *
 * Variables (wrangler.toml): PLACE_ID, ALLOWED_ORIGIN, LANG
 * Secreto:                   PLACES_API_KEY  (wrangler secret put PLACES_API_KEY)
 */

const FIELDS = [
  "displayName",
  "rating",
  "userRatingCount",
  "googleMapsUri",
  "reviews",
  "attributions",
].join(",");

export default {
  async fetch(req, env) {
    const cors = corsHeaders(req, env);
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (req.method !== "GET") return json({ error: "Método no permitido" }, 405, cors);

    const origin = req.headers.get("Origin");
    if (origin && cors["Access-Control-Allow-Origin"] !== origin) {
      return json({ error: "Origen no permitido" }, 403, cors);
    }
    const url = new URL(req.url);
    if (url.pathname !== "/api/resenas") return json({ error: "No encontrado" }, 404, cors);

    try {
      return json(await resenas(env), 200, cors);
    } catch (err) {
      console.error(err.stack || String(err));
      return json({ error: "No disponible" }, 502, cors);
    }
  },
};

async function resenas(env) {
  if (!env.PLACE_ID || !env.PLACES_API_KEY) throw new Error("Falta PLACE_ID o PLACES_API_KEY");
  const lang = env.LANG || "es";
  const r = await fetch(
    `https://places.googleapis.com/v1/places/${encodeURIComponent(env.PLACE_ID)}?languageCode=${lang}&regionCode=ES`,
    {
      headers: {
        "X-Goog-Api-Key": env.PLACES_API_KEY,
        "X-Goog-FieldMask": FIELDS,
      },
      cf: { cacheTtl: 0, cacheEverything: false },
    },
  );
  if (!r.ok) throw new Error(`Places ${r.status}: ${await r.text()}`);
  const p = await r.json();

  return {
    nombre: p.displayName?.text || "",
    valoracion: typeof p.rating === "number" ? p.rating : null,
    total: p.userRatingCount || 0,
    urlFicha: p.googleMapsUri || "",
    urlEscribir: `https://search.google.com/local/writereview?placeid=${encodeURIComponent(env.PLACE_ID)}`,
    atribuciones: (p.attributions || []).map((a) => ({ proveedor: a.provider || "", url: a.providerUri || "" })),
    resenas: (p.reviews || []).map((v) => ({
      autor: v.authorAttribution?.displayName || "Usuario de Google",
      autorUrl: v.authorAttribution?.uri || "",
      autorFoto: v.authorAttribution?.photoUri || "",
      estrellas: v.rating || 0,
      texto: v.text?.text || v.originalText?.text || "",
      cuando: v.relativePublishTimeDescription || "",
      fecha: v.publishTime || "",
      urlResena: v.googleMapsUri || "",
    })),
  };
}

function corsHeaders(req, env) {
  const allowed = (env.ALLOWED_ORIGIN || "").split(",").map((s) => s.trim()).filter(Boolean);
  const origin = req.headers.get("Origin") || "";
  return {
    "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0] || "",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { ...headers, "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" },
  });
}

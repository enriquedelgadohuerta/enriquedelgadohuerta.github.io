/*
 * Worker de subidas — informeperitoinformatico.es
 *
 * Recibe peticiones de /enviar-archivos/ y deja los archivos en tu OneDrive
 * mediante Microsoft Graph. El navegador sube los bytes directamente a la
 * sesión de subida de OneDrive; este Worker solo autoriza, abre la sesión y
 * guarda el manifiesto. Si el navegador no puede hablar con OneDrive (CORS),
 * /api/chunk reenvía los trozos.
 *
 * Variables (wrangler.toml): CLIENT_ID, BASE_FOLDER, ALLOWED_ORIGIN
 * Secreto:                   LINK_SECRET  (wrangler secret put LINK_SECRET)
 * KV:                        TOKENS, clave "refresh_token"
 */

const GRAPH = "https://graph.microsoft.com/v1.0";
const TOKEN_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token";
const SCOPE = "Files.ReadWrite offline_access";
const MAX_FILE = 20 * 1024 * 1024 * 1024;
const UPLOAD_HOSTS = [/\.1drv\.com$/i, /^api\.onedrive\.com$/i, /\.sharepoint\.com$/i, /\.microsoft\.com$/i];

export default {
  async fetch(req, env) {
    const cors = corsHeaders(req, env);
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (req.method !== "POST") return json({ error: "Método no permitido" }, 405, cors);
    if (cors["Access-Control-Allow-Origin"] !== req.headers.get("Origin")) {
      return json({ error: "Origen no permitido" }, 403, cors);
    }
    const url = new URL(req.url);
    try {
      if (url.pathname === "/api/session") return await session(req, env, cors);
      if (url.pathname === "/api/chunk") return await chunk(req, env, cors);
      if (url.pathname === "/api/manifest") return await manifest(req, env, cors);
      return json({ error: "No encontrado" }, 404, cors);
    } catch (err) {
      const status = err.status || 500;
      if (status >= 500) console.error(err.stack || String(err));
      return json({ error: status >= 500 ? "Error interno, inténtalo de nuevo en unos minutos" : err.message }, status, cors);
    }
  },
};

// ---------- Rutas ----------

async function session(req, env, cors) {
  const b = await req.json();
  await checkLink(env, b.e, b.x, b.c);
  checkBatch(b.batch);
  const size = Number(b.size);
  if (!Number.isSafeInteger(size) || size <= 0 || size > MAX_FILE) throw httpError(400, "Tamaño de archivo no válido");
  const name = safeName(b.name);
  const path = `${env.BASE_FOLDER}/${b.e}/${b.batch}/${name}`;
  const token = await accessToken(env);
  const r = await fetch(`${GRAPH}/me/drive/root:/${encodePath(path)}:/createUploadSession`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ item: { "@microsoft.graph.conflictBehavior": "rename" } }),
  });
  if (!r.ok) throw new Error(`createUploadSession ${r.status}: ${await r.text()}`);
  const j = await r.json();
  return json({ uploadUrl: j.uploadUrl, path }, 200, cors);
}

async function chunk(req, env, cors) {
  const h = req.headers;
  await checkLink(env, h.get("X-Exp"), h.get("X-Cad"), h.get("X-Cod"));
  const uploadUrl = h.get("X-Upload-Url") || "";
  const range = h.get("X-Content-Range") || "";
  let u;
  try { u = new URL(uploadUrl); } catch { throw httpError(400, "URL de subida no válida"); }
  if (u.protocol !== "https:" || !UPLOAD_HOSTS.some((re) => re.test(u.hostname))) throw httpError(400, "Destino no permitido");
  if (!/^bytes \d+-\d+\/\d+$/.test(range)) throw httpError(400, "Rango no válido");
  const body = await req.arrayBuffer();
  const r = await fetch(uploadUrl, { method: "PUT", headers: { "Content-Range": range }, body });
  return new Response(await r.text(), { status: r.status, headers: { ...cors, "Content-Type": "application/json" } });
}

async function manifest(req, env, cors) {
  const raw = await req.text();
  if (raw.length > 512 * 1024) throw httpError(413, "Manifiesto demasiado grande");
  const b = JSON.parse(raw);
  await checkLink(env, b.e, b.x, b.c);
  checkBatch(b.batch);
  const recibido = new Date().toISOString();
  const record = {
    servidor: {
      recibido_utc: recibido,
      ip_remitente: req.headers.get("CF-Connecting-IP"),
      pais: req.cf && req.cf.country,
      user_agent: req.headers.get("User-Agent"),
      enlace: { expediente: b.e, caducidad: b.x },
    },
    cliente: b.manifest,
  };
  const text = JSON.stringify(record, null, 2) + "\n";
  const sha = await sha256Hex(text);
  const path = `${env.BASE_FOLDER}/${b.e}/${b.batch}/_manifiesto_${b.batch}.json`;
  const token = await accessToken(env);
  const r = await fetch(`${GRAPH}/me/drive/root:/${encodePath(path)}:/content?@microsoft.graph.conflictBehavior=rename`, {
    method: "PUT",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: text,
  });
  if (!r.ok) throw new Error(`manifest ${r.status}: ${await r.text()}`);
  return json({ recibido, manifiesto_sha256: sha }, 200, cors);
}

// ---------- Autorización del enlace ----------

async function checkLink(env, e, x, c) {
  if (!/^[A-Za-z0-9-]{3,40}$/.test(e || "") || !/^\d{8}$/.test(x || "") || !/^[0-9a-f]{12}$/.test(c || "")) {
    throw httpError(403, "Enlace no válido");
  }
  const today = new Date().toISOString().slice(0, 10).replace(/-/g, "");
  if (x < today) throw httpError(403, "El enlace ha caducado");
  const expected = (await hmacHex(env.LINK_SECRET, `${e}|${x}`)).slice(0, 12);
  if (!timingSafeEqual(expected, c)) throw httpError(403, "Enlace no válido");
}

function checkBatch(batch) {
  if (!/^\d{8}T\d{6}Z$/.test(batch || "")) throw httpError(400, "Lote no válido");
}

// ---------- OneDrive: token ----------

async function accessToken(env) {
  const cached = await env.TOKENS.get("access_token", "json");
  if (cached && cached.exp > Date.now() + 60_000) return cached.token;

  const refresh = await env.TOKENS.get("refresh_token");
  if (!refresh) throw new Error("Falta refresh_token en KV");
  const r = await fetch(TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ client_id: env.CLIENT_ID, grant_type: "refresh_token", refresh_token: refresh, scope: SCOPE }),
  });
  const j = await r.json();
  if (!r.ok) throw new Error(`token ${r.status}: ${JSON.stringify(j)}`);
  // Microsoft rota el refresh token: se guarda siempre el último
  if (j.refresh_token && j.refresh_token !== refresh) await env.TOKENS.put("refresh_token", j.refresh_token);
  await env.TOKENS.put("access_token", JSON.stringify({ token: j.access_token, exp: Date.now() + j.expires_in * 1000 }), {
    expirationTtl: Math.max(60, j.expires_in - 120),
  });
  return j.access_token;
}

// ---------- Utilidades ----------

function corsHeaders(req, env) {
  const origin = req.headers.get("Origin") || "";
  const allowed = env.ALLOWED_ORIGIN.split(",").map((s) => s.trim());
  return {
    "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, X-Upload-Url, X-Content-Range, X-Exp, X-Cad, X-Cod",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function json(obj, status, headers) {
  return new Response(JSON.stringify(obj), { status, headers: { ...headers, "Content-Type": "application/json" } });
}

function httpError(status, message) {
  const e = new Error(message);
  e.status = status;
  return e;
}

function safeName(name) {
  let n = String(name || "").normalize("NFC").replace(/[\\/:*?"<>|#%\u0000-\u001f]/g, "_").trim();
  n = n.replace(/^\.+/, "_").slice(0, 180);
  return n || "archivo";
}

function encodePath(p) {
  return p.split("/").map(encodeURIComponent).join("/");
}

async function hmacHex(secret, msg) {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return hex(await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(msg)));
}

async function sha256Hex(text) {
  return hex(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text)));
}

function hex(buf) {
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

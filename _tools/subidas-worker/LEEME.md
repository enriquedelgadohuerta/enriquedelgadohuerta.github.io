# Subidas de archivos a OneDrive

La página `/enviar-archivos/` recibe archivos de clientes y los deja en tu OneDrive. Esta carpeta no se publica en la web, porque Jekyll ignora las carpetas que empiezan por `_`.

```
Navegador del cliente ──(1) pide sesión──▶ Worker Cloudflare ──▶ Microsoft Graph (tu OneDrive)
        │                                        ▲
        └──(2) sube los trozos directamente a OneDrive (o a través del Worker si falla CORS)
        └──(3) envía el manifiesto con las huellas SHA-256 ──┘  → _manifiesto_<lote>.json
```

Los archivos quedan en `OneDrive/Peritajes/Recepciones/<expediente>/<lote>/`, junto con `_manifiesto_<lote>.json`. El manifiesto incluye la hora del servidor, la IP y el navegador del remitente, y la huella SHA‑256 que el navegador calculó de cada archivo.

## Puesta en marcha (una sola vez, unos 20 minutos)

### 1. Registrar la aplicación en Microsoft

1. Entra en <https://entra.microsoft.com> con la cuenta Microsoft de tu OneDrive. Si te pide crear un directorio o una suscripción gratuita de Azure, créala: no tiene coste.
2. *Aplicaciones → Registros de aplicaciones → Nuevo registro*.
   - Nombre: `Subidas perito`
   - Tipos de cuenta: **Solo cuentas personales de Microsoft**
   - URI de redirección: plataforma **Cliente público/nativo (móvil y escritorio)**, valor `http://localhost:8400`
3. Copia el **Id. de aplicación (cliente)**: es el `CLIENT_ID`.
4. *Autenticación →* activa **Permitir flujos de clientes públicos**.
5. *Permisos de API → Agregar → Microsoft Graph → Permisos delegados →* `Files.ReadWrite` y `offline_access`.

### 2. Obtener el token de tu OneDrive

En tu Mac, dentro de esta carpeta:

```bash
python3 onedrive_token.py <CLIENT_ID>
```

Inicia sesión y acepta los permisos. Se crea `refresh_token.txt`, que **no debes subir al repositorio**: bórralo cuando termines el paso 3.

### 3. Desplegar el Worker en Cloudflare

Necesitas una cuenta gratuita en <https://dash.cloudflare.com> y Node.js.

```bash
npm install -g wrangler
wrangler login

wrangler kv namespace create TOKENS        # copia el id que devuelve
# Edita wrangler.toml: pega CLIENT_ID y el id del KV

wrangler kv key put --binding TOKENS refresh_token "$(cat refresh_token.txt)" --remote
openssl rand -hex 32                       # genera el secreto de los enlaces y guárdalo en tu gestor de contraseñas
wrangler secret put LINK_SECRET            # pega ese secreto
wrangler deploy                            # devuelve https://subidas-perito.<tu-subdominio>.workers.dev

rm refresh_token.txt
```

### 4. Conectar la página

En `enviar-archivos/subida.js`, cambia la constante `API` por la URL que te ha dado `wrangler deploy`, y publica la web.

## Uso diario: generar el enlace de un cliente

```bash
export SUBIDAS_SECRET='<el secreto de LINK_SECRET>'
python3 _tools/subidas-worker/enlace_subida.py EXP-2026-014            # válido 15 días
python3 _tools/subidas-worker/enlace_subida.py EXP-2026-014 --dias 30
```

Envía al cliente el enlace que imprime. Funciona solo para ese expediente y deja de funcionar al caducar. Sin el secreto nadie puede fabricar un enlace válido.

Al recibir los archivos, comprueba en tu equipo que la huella de cada uno coincide con la del manifiesto y la del justificante del cliente, y regístralo en la cadena de custodia:

```bash
shasum -a 256 ~/OneDrive/Peritajes/Recepciones/EXP-2026-014/<lote>/*
```

## Mantenimiento y límites

- **Token caducado.** Si la página da "Error interno" y en *Cloudflare → Workers → subidas-perito → Logs* aparece `invalid_grant`, repite los pasos 2 y 3 (solo la línea `kv key put`). El token se renueva solo mientras haya uso; si pasan unos 90 días sin ninguna subida, caduca.
- **Tamaño.** Hasta 20 GB por archivo. Se sube en trozos de 5 MB y cada trozo se reintenta si falla.
- **Plan gratuito de Workers.** 100.000 peticiones al día, que sobran: cada archivo son 2 peticiones, más 1 por cada 5 MB si se usa el modo de reenvío.
- **OneDrive de trabajo (Microsoft 365 Empresa).** Si algún día lo usas, cambia `consumers` por `common` en `worker.js` y en `onedrive_token.py`, y elige "cuentas de cualquier organización y personales" al registrar la aplicación.

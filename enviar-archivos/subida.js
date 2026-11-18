/*
 * Envío seguro de archivos — informeperitoinformatico.es
 *
 * Enlace: /enviar-archivos/#e=<expediente>&x=<AAAAMMDD caducidad>&c=<código>
 * Los parámetros van tras "#": no llegan a GitHub Pages ni a sus registros.
 *
 * Por cada archivo: se pide al Worker una sesión de subida de OneDrive, se lee
 * el archivo por trozos, se actualiza la huella SHA-256 con cada trozo y se
 * sube el trozo. Al final se envía al Worker el manifiesto con las huellas,
 * que lo guarda junto a los archivos y devuelve la hora del servidor.
 */
(function () {
  "use strict";

  // URL del Worker de Cloudflare (ver _tools/subidas-worker/LEEME.md)
  var API = "https://subidas-perito.subida-perito.workers.dev";

  var CHUNK = 320 * 1024 * 16; // 5 MiB, múltiplo de 320 KiB como exige OneDrive
  var MAX_FILE = 20 * 1024 * 1024 * 1024; // 20 GB

  // ---------- SHA-256 incremental (FIPS 180-4) ----------
  var K = new Uint32Array([
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
  ]);

  function Sha256() {
    this.h = new Uint32Array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
      0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]);
    this.buf = new Uint8Array(64);
    this.bl = 0;
    this.len = 0;
    this.w = new Uint32Array(64);
  }
  Sha256.prototype._block = function (p, o) {
    var w = this.w, H = this.h, t;
    for (t = 0; t < 16; t++) {
      w[t] = (p[o + 4 * t] << 24) | (p[o + 4 * t + 1] << 16) | (p[o + 4 * t + 2] << 8) | p[o + 4 * t + 3];
    }
    for (t = 16; t < 64; t++) {
      var x = w[t - 15], y = w[t - 2];
      var s0 = ((x >>> 7) | (x << 25)) ^ ((x >>> 18) | (x << 14)) ^ (x >>> 3);
      var s1 = ((y >>> 17) | (y << 15)) ^ ((y >>> 19) | (y << 13)) ^ (y >>> 10);
      w[t] = (w[t - 16] + s0 + w[t - 7] + s1) | 0;
    }
    var a = H[0] | 0, b = H[1] | 0, c = H[2] | 0, d = H[3] | 0,
        e = H[4] | 0, f = H[5] | 0, g = H[6] | 0, h = H[7] | 0;
    for (t = 0; t < 64; t++) {
      var S1 = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
      var ch = (e & f) ^ (~e & g);
      var t1 = (h + S1 + ch + K[t] + w[t]) | 0;
      var S0 = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
      var mj = (a & b) ^ (a & c) ^ (b & c);
      var t2 = (S0 + mj) | 0;
      h = g; g = f; f = e; e = (d + t1) | 0; d = c; c = b; b = a; a = (t1 + t2) | 0;
    }
    H[0] += a; H[1] += b; H[2] += c; H[3] += d; H[4] += e; H[5] += f; H[6] += g; H[7] += h;
  };
  Sha256.prototype.update = function (d) {
    var i = 0, n = d.length;
    this.len += n;
    if (this.bl) {
      var take = Math.min(64 - this.bl, n);
      this.buf.set(d.subarray(0, take), this.bl);
      this.bl += take; i = take;
      if (this.bl === 64) { this._block(this.buf, 0); this.bl = 0; }
    }
    for (; i + 64 <= n; i += 64) this._block(d, i);
    if (i < n) { this.buf.set(d.subarray(i), 0); this.bl = n - i; }
  };
  Sha256.prototype.hex = function () {
    var hi = Math.floor(this.len / 0x20000000), lo = (this.len % 0x20000000) * 8;
    var pad = new Uint8Array(((this.bl < 56) ? 56 : 120) - this.bl + 8);
    pad[0] = 0x80;
    var L = pad.length;
    pad[L - 8] = hi >>> 24; pad[L - 7] = hi >>> 16; pad[L - 6] = hi >>> 8; pad[L - 5] = hi;
    pad[L - 4] = lo >>> 24; pad[L - 3] = lo >>> 16; pad[L - 2] = lo >>> 8; pad[L - 1] = lo;
    var saved = this.len;
    this.update(pad);
    this.len = saved;
    var out = "";
    for (var k = 0; k < 8; k++) out += ("00000000" + this.h[k].toString(16)).slice(-8);
    return out;
  };
  // Exportado para pruebas
  window.__Sha256 = Sha256;

  // ---------- Utilidades ----------
  function $(id) { return document.getElementById(id); }
  function fmtSize(n) {
    if (n < 1024) return n + " B";
    var u = ["KB", "MB", "GB", "TB"], i = -1;
    do { n /= 1024; i++; } while (n >= 1024 && i < u.length - 1);
    return n.toFixed(n < 10 ? 1 : 0).replace(".", ",") + " " + u[i];
  }
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function nowIso() { return new Date().toISOString(); }

  function parseLink() {
    var p = new URLSearchParams(location.hash.slice(1));
    var e = p.get("e") || "", x = p.get("x") || "", c = p.get("c") || "";
    if (!/^[A-Za-z0-9-]{3,40}$/.test(e) || !/^\d{8}$/.test(x) || !/^[0-9a-f]{12}$/.test(c)) return null;
    var today = new Date().toISOString().slice(0, 10).replace(/-/g, "");
    if (x < today) return null;
    return { e: e, x: x, c: c };
  }

  async function api(path, body, extraHeaders) {
    var headers = Object.assign({ "Content-Type": "application/json" }, extraHeaders || {});
    var r = await fetch(API + path, { method: "POST", headers: headers, body: JSON.stringify(body) });
    var j = null;
    try { j = await r.json(); } catch (_) { /* sin cuerpo */ }
    if (!r.ok) throw new Error((j && j.error) || ("Error del servidor (" + r.status + ")"));
    return j;
  }

  // ---------- Estado ----------
  var link = parseLink();
  var form = $("up-form");
  var list = $("files");
  var queue = [];
  var sending = false;
  var proxyMode = false;

  if (!link) { $("no-link").hidden = false; return; }
  form.hidden = false;
  $("ref-exp").textContent = link.e;
  $("ref-cad").textContent = "· enlace válido hasta el " + link.x.slice(6, 8) + "/" + link.x.slice(4, 6) + "/" + link.x.slice(0, 4);

  function render() {
    list.innerHTML = "";
    queue.forEach(function (it, idx) {
      var li = document.createElement("li");
      li.className = "file";
      li.innerHTML =
        '<div class="file-top"><span class="file-name"></span><span><span class="file-size"></span> ' +
        (sending || it.done ? "" : '<button type="button" class="file-rm" aria-label="Quitar">×</button>') +
        '</span></div><div class="bar"><span></span></div><div class="file-st"></div><span class="hash"></span>';
      li.querySelector(".file-name").textContent = it.file.name;
      li.querySelector(".file-size").textContent = fmtSize(it.file.size);
      var rm = li.querySelector(".file-rm");
      if (rm) rm.onclick = function () { queue.splice(idx, 1); render(); };
      it.el = li;
      paint(it);
      list.appendChild(li);
    });
  }
  function paint(it) {
    if (!it.el) return;
    it.el.querySelector(".bar span").style.width = (it.progress * 100).toFixed(1) + "%";
    var st = it.el.querySelector(".file-st");
    st.textContent = it.status || "Pendiente";
    st.className = "file-st" + (it.done ? " ok" : it.error ? " err" : "");
    it.el.querySelector(".hash").textContent = it.sha256 ? "SHA-256: " + it.sha256 : "";
  }

  function addFiles(files) {
    if (sending) return;
    for (var i = 0; i < files.length; i++) {
      var f = files[i];
      if (f.size > MAX_FILE) { showErr("«" + f.name + "» supera el máximo de 20 GB. Escríbeme y buscamos otra forma."); continue; }
      if (f.size === 0) continue;
      queue.push({ file: f, progress: 0, status: "", done: false, error: false, sha256: "" });
    }
    render();
  }

  var drop = $("drop");
  $("u-files").addEventListener("change", function (ev) { addFiles(ev.target.files); ev.target.value = ""; });
  ["dragenter", "dragover"].forEach(function (t) {
    drop.addEventListener(t, function (ev) { ev.preventDefault(); drop.classList.add("over"); });
  });
  ["dragleave", "drop"].forEach(function (t) {
    drop.addEventListener(t, function (ev) { ev.preventDefault(); drop.classList.remove("over"); });
  });
  drop.addEventListener("drop", function (ev) { addFiles(ev.dataTransfer.files); });

  function showErr(msg) { var e = $("u-err"); e.textContent = msg; e.classList.toggle("show", !!msg); }

  // ---------- Subida ----------
  // El cuerpo son los mismos bytes que se han usado para la huella
  async function putChunk(uploadUrl, blob, start, end, total) {
    var range = "bytes " + start + "-" + (end - 1) + "/" + total;
    if (!proxyMode) {
      try {
        var r = await fetch(uploadUrl, { method: "PUT", headers: { "Content-Range": range }, body: blob });
        if (r.ok || r.status === 202) return r;
        if (r.status >= 400 && r.status < 500 && r.status !== 416) throw new Error("OneDrive rechazó el trozo (" + r.status + ")");
        throw new Error("retry");
      } catch (err) {
        // Un TypeError es un fallo de red o de CORS: se pasa a enviar a través del Worker
        if (err instanceof TypeError) { proxyMode = true; } else { throw err; }
      }
    }
    var r2 = await fetch(API + "/api/chunk", {
      method: "POST",
      headers: {
        "Content-Type": "application/octet-stream",
        "X-Upload-Url": uploadUrl,
        "X-Content-Range": range,
        "X-Exp": link.e, "X-Cad": link.x, "X-Cod": link.c
      },
      body: blob
    });
    if (!r2.ok && r2.status !== 202) throw new Error("retry");
    return r2;
  }

  async function uploadOne(it, batch) {
    var f = it.file;
    it.status = "Preparando…"; paint(it);
    var s = await api("/api/session", {
      e: link.e, x: link.x, c: link.c, batch: batch,
      name: f.name, size: f.size
    });
    var hasher = new Sha256();
    var started = nowIso();
    for (var start = 0; start < f.size; start += CHUNK) {
      var end = Math.min(start + CHUNK, f.size);
      var bytes = new Uint8Array(await f.slice(start, end).arrayBuffer());
      hasher.update(bytes);
      var tries = 0;
      for (;;) {
        try { await putChunk(s.uploadUrl, bytes, start, end, f.size); break; }
        catch (err) {
          if (err.message !== "retry" || ++tries > 4) throw err.message === "retry" ? new Error("Se ha cortado la conexión") : err;
          it.status = "Reintentando…"; paint(it);
          await sleep(1500 * tries);
        }
      }
      it.progress = end / f.size;
      it.status = "Enviando… " + Math.floor(it.progress * 100) + " %";
      paint(it);
    }
    it.sha256 = hasher.hex();
    it.path = s.path;
    it.started = started;
    it.finished = nowIso();
    it.batch = batch;
    it.done = true;
    it.status = "Enviado";
    paint(it);
  }

  function receiptText(m, server) {
    var L = [];
    L.push("JUSTIFICANTE DE ENVÍO DE ARCHIVOS");
    L.push("Perito: Enrique Delgado · informeperitoinformatico.es");
    L.push("");
    L.push("Expediente:        " + m.expediente);
    L.push("Remitente:         " + m.remitente);
    L.push("Lote:              " + m.lote);
    L.push("Hora del servidor: " + (server.recibido || "—") + " (UTC)");
    L.push("Hora del equipo:   " + m.fin_envio + " (UTC)");
    if (m.nota) L.push("Nota:              " + m.nota);
    L.push("");
    L.push("Archivos (huella SHA-256 calculada en el dispositivo del remitente antes del envío):");
    m.archivos.forEach(function (a, i) {
      L.push("");
      L.push((i + 1) + ". " + a.nombre);
      L.push("   Tamaño:  " + a.bytes + " bytes");
      L.push("   SHA-256: " + a.sha256);
    });
    L.push("");
    L.push("Huella SHA-256 de este manifiesto: " + (server.manifiesto_sha256 || "—"));
    return L.join("\n");
  }

  form.addEventListener("submit", async function (ev) {
    ev.preventDefault();
    if (sending) return;
    var nombre = $("u-nombre").value.trim();
    if (nombre.length < 3) { showErr("Escribe tu nombre y apellidos."); $("u-nombre").focus(); return; }
    var pending = queue.filter(function (q) { return !q.done; });
    if (!pending.length) { showErr("Añade al menos un archivo."); return; }
    if (!$("u-ok").checked) { showErr("Marca la casilla de autorización para continuar."); return; }
    showErr("");

    sending = true;
    $("u-send").disabled = true;
    $("u-send").textContent = "Enviando…";
    render();
    window.onbeforeunload = function () { return "El envío no ha terminado."; };

    var batch = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");
    var failed = 0;
    for (var i = 0; i < queue.length; i++) {
      var it = queue[i];
      if (it.done) continue;
      it.error = false;
      try { await uploadOne(it, batch); }
      catch (err) { it.error = true; it.status = "Error: " + err.message; failed++; paint(it); }
    }

    var done = queue.filter(function (q) { return q.done && q.batch === batch; });
    var manifest = {
      expediente: link.e,
      remitente: nombre,
      nota: $("u-nota").value.trim(),
      lote: batch,
      fin_envio: nowIso(),
      navegador: navigator.userAgent,
      archivos: done.map(function (q) {
        return {
          nombre: q.file.name, bytes: q.file.size,
          modificado: q.file.lastModified ? new Date(q.file.lastModified).toISOString() : null,
          tipo: q.file.type || null, sha256: q.sha256,
          inicio_envio: q.started, fin_envio: q.finished, ruta_destino: q.path
        };
      })
    };

    var server = {};
    if (done.length) {
      try { server = await api("/api/manifest", { e: link.e, x: link.x, c: link.c, batch: batch, manifest: manifest }); }
      catch (err) { failed++; showErr("Los archivos se han enviado, pero no se ha podido registrar el justificante: " + err.message); }
    }

    window.onbeforeunload = null;
    sending = false;
    $("u-send").disabled = false;
    $("u-send").textContent = failed ? "Reintentar los que han fallado" : "Enviar más archivos";
    render();

    if (failed && !server.recibido) {
      if (!$("u-err").classList.contains("show")) showErr("Algunos archivos no se han podido enviar. Pulsa el botón para reintentarlo o escríbeme.");
    }
    if (done.length) {
      var txt = receiptText(manifest, server);
      $("receipt-txt").textContent = txt;
      $("receipt").hidden = false;
      $("receipt-dl").onclick = function () {
        var a = document.createElement("a");
        a.href = URL.createObjectURL(new Blob([txt + "\n"], { type: "text/plain;charset=utf-8" }));
        a.download = "justificante_" + link.e + "_" + batch + ".txt";
        document.body.appendChild(a); a.click(); a.remove();
      };
      $("receipt").scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
})();

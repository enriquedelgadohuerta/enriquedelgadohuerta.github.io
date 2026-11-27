/*
 * Sección "Opiniones en Google" de la portada.
 * Pide al Worker resenas-perito la valoración y las reseñas del Perfil de
 * Empresa en vivo (sin guardar nada), solo cuando el visitante se acerca a la
 * sección. Si el Worker no está configurado o falla, la sección no aparece.
 */
(function () {
  "use strict";
  var sec = document.getElementById("resenas");
  if (!sec) return;
  var API = sec.getAttribute("data-api");
  if (!API) return; // aún sin configurar: la sección sigue oculta

  var started = false;
  function start() {
    if (started) return;
    started = true;
    fetch(API, { headers: { Accept: "application/json" }, credentials: "omit" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(render)
      .catch(function () { /* sin reseñas, sin sección */ });
  }

  var anchor = document.getElementById("casos") || sec;
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      if (es.some(function (e) { return e.isIntersecting; })) { io.disconnect(); start(); }
    }, { rootMargin: "600px 0px" });
    io.observe(anchor);
  } else {
    start();
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function link(href, text, cls) {
    var a = el("a", cls, text);
    a.href = href;
    a.target = "_blank";
    a.rel = "noopener nofollow";
    return a;
  }
  function stars(n, big) {
    var s = el("span", "stars" + (big ? " stars-lg" : ""));
    var r = Math.round(n * 2) / 2;
    s.setAttribute("role", "img");
    s.setAttribute("aria-label", String(n).replace(".", ",") + " de 5 estrellas");
    for (var i = 1; i <= 5; i++) {
      var st = el("span", i <= r ? "on" : (i - 0.5 === r ? "half" : "off"), "★");
      st.setAttribute("aria-hidden", "true");
      s.appendChild(st);
    }
    return s;
  }
  function safeUrl(u) { return /^https:\/\//i.test(u || "") ? u : ""; }

  function render(d) {
    var list = sec.querySelector(".reviews");
    var summary = sec.querySelector(".reviews-summary");
    var write = sec.querySelector("[data-escribir]");
    var all = sec.querySelector("[data-ficha]");

    if (safeUrl(d.urlEscribir)) write.href = d.urlEscribir;
    if (safeUrl(d.urlFicha)) all.href = d.urlFicha; else all.remove();

    if (d.total > 0 && d.valoracion != null) {
      summary.appendChild(el("span", "score", String(d.valoracion.toFixed(1)).replace(".", ",")));
      summary.appendChild(stars(d.valoracion, true));
      summary.appendChild(el("span", "count", d.total + (d.total === 1 ? " opinión" : " opiniones") + " en Google"));
    } else {
      summary.appendChild(el("span", "count", "Todavía no hay opiniones publicadas. ¿Has trabajado conmigo? La tuya puede ser la primera."));
    }

    (d.resenas || []).forEach(function (v) {
      if (!v.texto) return;
      var card = el("article", "review");
      var head = el("header", "review-head");
      var foto = safeUrl(v.autorFoto);
      if (foto) {
        var img = el("img", "avatar");
        img.src = foto; img.alt = ""; img.width = 40; img.height = 40;
        img.loading = "lazy"; img.referrerPolicy = "no-referrer";
        head.appendChild(img);
      } else {
        head.appendChild(el("span", "avatar avatar-txt", (v.autor || "?").charAt(0).toUpperCase()));
      }
      var who = el("div", "who");
      var autorUrl = safeUrl(v.autorUrl);
      who.appendChild(autorUrl ? link(autorUrl, v.autor, "author") : el("span", "author", v.autor));
      var meta = el("div", "meta");
      meta.appendChild(stars(v.estrellas));
      if (v.cuando) {
        var t = el("time", null, v.cuando);
        if (v.fecha) t.dateTime = v.fecha;
        meta.appendChild(t);
      }
      who.appendChild(meta);
      head.appendChild(who);
      card.appendChild(head);

      var texto = v.texto.length > 420 ? v.texto.slice(0, 400).replace(/\s+\S*$/, "") + "…" : v.texto;
      card.appendChild(el("p", "review-text", texto));
      var src = el("p", "review-src");
      var u = safeUrl(v.urlResena);
      if (u) src.appendChild(link(u, texto !== v.texto ? "Leer completa en Google" : "Ver en Google"));
      else src.textContent = "Publicada en Google";
      card.appendChild(src);
      list.appendChild(card);
    });

    var attr = sec.querySelector(".reviews-attr");
    (d.atribuciones || []).forEach(function (a) {
      if (!a.proveedor) return;
      attr.appendChild(document.createTextNode(" · "));
      attr.appendChild(safeUrl(a.url) ? link(a.url, a.proveedor) : el("span", null, a.proveedor));
    });

    sec.hidden = false;
    var nav = document.querySelector('[data-nav-resenas]');
    if (nav) nav.hidden = false;
  }
})();

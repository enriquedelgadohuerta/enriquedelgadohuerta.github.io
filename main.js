/* informeperitoinformatico.es — interacción mínima, sin dependencias ni cookies */
(function () {
  'use strict';

  // Cabecera con borde al hacer scroll
  var head = document.querySelector('.site-head');
  if (head) {
    var onScroll = function () { head.classList.toggle('scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Menú móvil
  var menuBtn = document.getElementById('menu-btn');
  var mobileNav = document.getElementById('mobile-nav');
  function closeMenu() {
    if (!menuBtn) return;
    mobileNav.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false');
  }
  if (menuBtn && mobileNav) {
    menuBtn.addEventListener('click', function () {
      var open = mobileNav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', String(open));
    });
    mobileNav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeMenu); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  }

  // Aparición suave de secciones
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('visible'); obs.unobserve(en.target); }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(function (el) { obs.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('visible'); });
  }

  // Formulario: no envía nada a ningún servidor.
  // Compone el mensaje y lo abre en WhatsApp o en el programa de correo del visitante.
  var form = document.getElementById('consulta');
  if (!form) return;
  var topic = document.getElementById('f-tema');
  var err = document.getElementById('f-error');

  // Los enlaces "Cuéntame tu caso" de cada problema preseleccionan el tema
  document.querySelectorAll('[data-tema]').forEach(function (a) {
    a.addEventListener('click', function () {
      var val = a.getAttribute('data-tema');
      for (var i = 0; i < topic.options.length; i++) {
        if (topic.options[i].value === val) { topic.selectedIndex = i; break; }
      }
    });
  });

  function buildMessage() {
    var nombre = form.nombre.value.trim();
    var tema = topic.value;
    var texto = form.mensaje.value.trim();
    var lines = ['Hola Enrique, quería hacerte una consulta.'];
    if (nombre) lines.push('Me llamo ' + nombre + '.');
    if (tema) lines.push('Tema: ' + tema + '.');
    if (texto) lines.push('', texto);
    return { nombre: nombre, tema: tema, body: lines.join('\n') };
  }

  function valid() {
    var ok = form.mensaje.value.trim().length >= 10;
    err.classList.toggle('show', !ok);
    if (!ok) form.mensaje.focus();
    return ok;
  }

  document.getElementById('send-wa').addEventListener('click', function () {
    if (!valid()) return;
    var m = buildMessage();
    window.open('https://wa.me/34649716627?text=' + encodeURIComponent(m.body), '_blank', 'noopener');
  });

  document.getElementById('send-mail').addEventListener('click', function () {
    if (!valid()) return;
    var m = buildMessage();
    var subject = 'Consulta pericial' + (m.tema ? ' — ' + m.tema : '');
    window.location.href = 'mailto:info@informeperitoinformatico.es?subject=' +
      encodeURIComponent(subject) + '&body=' + encodeURIComponent(m.body);
  });
})();

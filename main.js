/* ============================================================
   PERITO INFORMÁTICO — main.js
   ============================================================ */

// ── Navbar scroll effect ──────────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
}, { passive: true });

// ── Mobile hamburger ──────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks  = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('active');
  navLinks.classList.toggle('open');
});

// Close menu when a link is clicked
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navLinks.classList.remove('open');
  });
});

// ── Active nav link on scroll ─────────────────────────────
const sections = document.querySelectorAll('section[id]');
const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navAnchors.forEach(a => {
        a.classList.toggle(
          'active',
          a.getAttribute('href') === `#${entry.target.id}`
        );
      });
    }
  });
}, { rootMargin: '-40% 0px -55% 0px' });

sections.forEach(s => observer.observe(s));

// ── Smooth scroll for anchor links ───────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ── Scroll reveal animations ──────────────────────────────
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll(
  '.service-card, .step, .case-item, .credential, .info-block'
).forEach((el, i) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = `opacity 0.5s ease ${i * 0.07}s, transform 0.5s ease ${i * 0.07}s`;
  revealObserver.observe(el);
});

document.addEventListener('animationend', () => {}, { once: true });

// Inject the .revealed class via JS (avoids CSS flash)
const style = document.createElement('style');
style.textContent = `.revealed { opacity: 1 !important; transform: none !important; }`;
document.head.appendChild(style);

// ── Contact form ──────────────────────────────────────────
const form    = document.getElementById('contact-form');
const message = document.getElementById('form-message');

form.addEventListener('submit', function (e) {
  e.preventDefault();
  message.className = 'form-message';
  message.style.display = 'none';

  // Basic validation
  const nombre  = form.nombre.value.trim();
  const email   = form.email.value.trim();
  const tipo    = form.tipo.value;
  const msg     = form.mensaje.value.trim();
  const lopd    = form.lopd.checked;

  if (!nombre || !email || !tipo || !msg || !lopd) {
    showMessage('error', '⚠ Por favor, complete todos los campos obligatorios y acepte la política de privacidad.');
    return;
  }

  if (!isValidEmail(email)) {
    showMessage('error', '⚠ El formato del email no es válido.');
    return;
  }

  // Simulate submission (replace with fetch to your backend/formspree/etc.)
  const btn = form.querySelector('.btn-submit');
  btn.disabled = true;
  btn.querySelector('span').textContent = 'Enviando...';

  setTimeout(() => {
    showMessage('success', '✓ Consulta recibida. Le responderemos en menos de 24 horas. Gracias.');
    form.reset();
    btn.disabled = false;
    btn.querySelector('span').textContent = 'Enviar consulta';
  }, 1500);
});

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showMessage(type, text) {
  message.textContent = text;
  message.className = `form-message ${type}`;
}

// ── Structured data (Schema.org) ──────────────────────────
const schema = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Perito Informático Judicial",
  "description": "Peritaje informático judicial especializado en correo electrónico, redes sociales, WhatsApp y Telegram.",
  "url": window.location.origin,
  "telephone": "+34600000000",
  "email": "perito@tudominio.es",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Madrid",
    "addressCountry": "ES"
  },
  "serviceType": [
    "Peritaje de correo electrónico",
    "Peritaje de redes sociales",
    "Peritaje de WhatsApp",
    "Peritaje de Telegram"
  ]
};

const ldJson = document.createElement('script');
ldJson.type = 'application/ld+json';
ldJson.textContent = JSON.stringify(schema);
document.head.appendChild(ldJson);

// ── Fix layout: wrap about & methodology sections ─────────
// About section
const aboutSection = document.querySelector('.about');
if (aboutSection) {
  const aboutContent = aboutSection.querySelector('.about-content');
  const aboutVisual  = aboutSection.querySelector('.about-visual');
  if (aboutContent && aboutVisual) {
    const wrapper = document.createElement('div');
    wrapper.className = 'about-inner-grid';
    aboutContent.parentNode.insertBefore(wrapper, aboutContent);
    wrapper.appendChild(aboutContent);
    wrapper.appendChild(aboutVisual);
  }
}

// Methodology section
const methodSection = document.querySelector('.methodology');
if (methodSection) {
  const mc = methodSection.querySelector('.method-content');
  const mv = methodSection.querySelector('.method-visual');
  if (mc && mv) {
    const wrapper = document.createElement('div');
    wrapper.className = 'method-inner-grid';
    mc.parentNode.insertBefore(wrapper, mc);
    wrapper.appendChild(mc);
    wrapper.appendChild(mv);
  }
}

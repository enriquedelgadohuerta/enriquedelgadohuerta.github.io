# Portfolio Peritaje Informático

Sitio web profesional para perito informático judicial. Estático, sin dependencias de servidor (excepto para el formulario de contacto).

## Estructura de ficheros

```
portfolio-peritaje/
├── index.html              ← Página principal (portfolio)
├── styles.css              ← Estilos completos
├── main.js                 ← Interactividad (navbar, formulario, animaciones)
├── aviso-legal.html        ← Aviso legal (LSSI)
├── politica-privacidad.html← Política de privacidad (RGPD)
├── politica-cookies.html   ← Política de cookies
└── README.md               ← Este fichero
```

## Qué necesitas personalizar

Busca y reemplaza en todos los ficheros:

| Marcador               | Reemplazar por                              |
|------------------------|---------------------------------------------|
| `Nombre Apellidos`     | Tu nombre completo                          |
| `XXXXX`               | Tu número de colegiado                      |
| `enriquedelgadohuerta@gmail.com`  | Tu email profesional                        |
| `+34 600 000 000`      | Tu teléfono real                            |
| `[Dirección]`          | Tu dirección profesional                    |
| `[CP]`                 | Tu código postal                            |
| `informeperitoinformatico.es`     | Tu dominio real                             |
| `X-XXXXXXXX`           | Tu NIF/CIF                                  |
| `Col. Nº XXXXX COIIE`  | Tu colegio y número real                    |
| `Madrid`               | Tu ciudad si es distinta                    |

## Formulario de contacto

El formulario incluye validación frontend. Para hacerlo funcional en producción, elige una opción:

### Opción A — Formspree (gratis, fácil)
1. Regístrate en https://formspree.io
2. Crea un nuevo formulario
3. En `main.js`, reemplaza el bloque `setTimeout` por:
```javascript
const res = await fetch('https://formspree.io/f/TU_ID', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    nombre: form.nombre.value,
    email: form.email.value,
    telefono: form.telefono.value,
    tipo: form.tipo.value,
    mensaje: form.mensaje.value
  })
});
if (res.ok) showMessage('success', '✓ Consulta recibida...');
else showMessage('error', '⚠ Error al enviar. Inténtelo de nuevo.');
```

### Opción B — EmailJS (sin servidor)
1. Regístrate en https://www.emailjs.com
2. Conecta tu cuenta de email
3. Añade su SDK y configura el envío

### Opción C — PHP (hosting propio)
Crea un fichero `send.php` y usa `fetch('/send.php', { method: 'POST', body: formData })`.

## Opciones de publicación

### GitHub Pages (gratis)
1. Crea repositorio en GitHub
2. Sube los ficheros
3. Ve a Settings → Pages → Source: main branch

### Netlify (gratis, recomendado)
1. Arrastra la carpeta a https://app.netlify.com/drop
2. Configura dominio personalizado en Settings

### Hosting tradicional (FTP)
Sube los ficheros a la carpeta `public_html` o `www` de tu hosting.

## SEO — Recomendaciones

- Añade tu foto real en `.profile-avatar` (reemplaza el placeholder SVG)
- Actualiza las estadísticas reales (+200 informes, etc.)
- Añade el atributo `lang` correcto ya está en `es`
- Configura Google Search Console con tu dominio
- Considera añadir un sitemap.xml (generadores gratuitos online)

## RGPD — Checklist legal

- [ ] Sustituir todos los datos ficticios por los reales
- [ ] Configurar el banner de cookies (recomendado: Cookiebot o Iubenda)
- [ ] Registrar el tratamiento de datos en el RAAD (si aplica)
- [ ] Revisar la política de privacidad con tu abogado
- [ ] Añadir tu número de colegiado real

## Tecnologías

- HTML5 semántico
- CSS3 con variables (sin framework)
- JavaScript vanilla (sin dependencias)
- Google Fonts: DM Serif Display + IBM Plex Mono + Outfit
- Schema.org estructurado (LocalBusiness) generado dinámicamente

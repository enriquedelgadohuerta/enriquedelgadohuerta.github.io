#!/usr/bin/env python3
"""Genera las páginas de servicio (/peritaje-<servicio>/) a partir de la lista SERVICIOS.

Uso (desde la raíz del repositorio):
    python3 _tools/generar_servicios.py && python3 _tools/generar_zonas.py

El segundo comando regenera el sitemap incluyendo estas páginas.
Reutiliza cabecera, pie y plantilla de generar_zonas.py. Las preguntas del
FAQPage (JSON-LD) salen de la misma lista que las visibles, así coinciden siempre.

Al añadir un servicio aquí, añadirlo también a PAGINAS_SERVICIO y SERVICIO_URL
en generar_zonas.py (sitemap, enlaces de las páginas locales).
"""
import os
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar_zonas as gz  # noqa: E402

SITE = gz.SITE
esc = gz.esc

NORMAS = """    <div class="standards" aria-label="Normas de referencia">
      Trabajo conforme a: <span class="pill">UNE 197010</span><span class="pill">UNE 71505-3</span><span class="pill">ISO/IEC 27037</span><span class="pill">LEC arts. 335–352</span>
    </div>"""


# ───────────────────────── contenidos ─────────────────────────
WHATSAPP = {
    "slug": "peritaje-whatsapp",
    "title": "Perito Informático de WhatsApp en Madrid | Informe para juicio",
    "desc": ("Peritaje de WhatsApp para juicio: analizo la conversación en el teléfono original, cotejo "
             "capturas y busco mensajes borrados. Toda España. Consulta gratis."),
    "og_title": "Perito informático de WhatsApp",
    "nombre": "Peritaje informático de WhatsApp",
    "alternos": ["Perito de WhatsApp", "Informe pericial de WhatsApp"],
    "tipo": "Peritaje informático de mensajería",
    "miga": "WhatsApp",
    "corto": "Peritaje de WhatsApp",
    "wa_txt": "Hola Enrique, quería consultarte un caso de mensajes de WhatsApp.",
    "eyebrow": "Peritaje de WhatsApp y mensajería",
    "h1": "Perito informático de <em>WhatsApp</em>",
    "lead": "Analizo la conversación original en tu teléfono, la fijo con huellas digitales y la presento en un informe pericial que el juez puede valorar con garantías. Para particulares y abogados, en Madrid y en toda España.",
    "casos_h2": "Casos en los que un peritaje de WhatsApp marca la diferencia",
    "casos": [
        ("Acoso o amenazas", "Mensajes que demuestran lo que está pasando y que necesitas presentar sin que puedan decir que los has inventado."),
        ("Deudas, alquileres y acuerdos", "Un préstamo, una señal, un acuerdo de pago o una orden de trabajo que solo quedó por escrito en WhatsApp."),
        ("Conflictos laborales", "Instrucciones, cambios de horario, avisos de despido o conversaciones con la empresa que hay que acreditar."),
        ("Familia y custodia", "Comunicaciones sobre los hijos, el régimen de visitas o la pensión que forman parte del procedimiento."),
        ("Te acusan con capturas", "La otra parte aporta pantallazos que crees falsos o sacados de contexto y necesitas una contrapericial."),
        ("Mensajes borrados o editados", "Se eliminó un mensaje clave o se editó después. Vemos si quedan rastros técnicos que lo acrediten."),
    ],
    "duda_id": "pantallazos",
    "duda_eyebrow": "La pregunta más habitual",
    "duda_h2": "¿No basta con un <em>pantallazo</em>?",
    "duda_lead": "A veces sí, pero no te fíes. Desde la sentencia del Tribunal Supremo 300/2015, si la otra parte impugna una conversación con argumentos, hay que demostrar su origen, su autoría y su integridad. Y hoy fabricar un chat falso con apariencia real está al alcance de cualquiera.",
    "duda_link": ("/articulos/pantallazos-whatsapp-prueba-juicio/", "Lee qué dice el Supremo sobre los pantallazos →"),
    "duda_puntos": [
        ("Una captura es una imagen", "Se puede recortar, editar o generar desde cero. No dice nada de quién escribió el mensaje ni de si es completo."),
        ("El chat exportado es texto editable", "«Exportar chat» genera un archivo que cualquiera puede modificar con un editor."),
        ("Lo que da solidez es el original", "La base de datos de la aplicación en el teléfono, adquirida con cadena de custodia y explicada en un informe."),
    ],
    "analisis_lead": "Trabajo sobre la base de datos de la aplicación (msgstore.db en Android, ChatStorage.sqlite en iPhone) o sobre la copia de seguridad, nunca sobre la imagen.",
    "analisis": [
        ("Origen y autoría", "Qué número envió cada mensaje, en qué conversación y desde qué dispositivo, a partir de la base de datos de la aplicación y no de una imagen."),
        ("Integridad con hash", "Calculo huellas SHA-256 de todo lo adquirido. Cualquier cambio posterior, por pequeño que sea, se detectaría."),
        ("Cotejo de capturas", "Comparo cada pantallazo con el registro original: texto, fecha, hora, remitente y orden de los mensajes."),
        ("Eliminados y editados", "Rastros de mensajes borrados «para todos» o editados, cuando el dispositivo y el tiempo transcurrido lo permiten."),
        ("Audios, fotos y documentos", "Archivos adjuntos con su fecha, su vínculo con el mensaje en que se enviaron y sus metadatos."),
        ("Telegram, Signal e Instagram", "El mismo método para otras aplicaciones de mensajería y redes sociales, adaptado a cómo guarda los datos cada una."),
    ],
    "nota_legal": "No accedo a teléfonos ni cuentas ajenos ni «espío» un WhatsApp: solo analizo conversaciones a las que tienes derecho legítimo de acceso.",
    "pasos_h2": "Cómo es un peritaje de WhatsApp, paso a paso",
    "pasos": [
        ("Me cuentas el caso", "Por WhatsApp, teléfono o correo. Te digo con franqueza si un informe te ayuda y qué conversaciones conviene analizar.", "Gratis"),
        ("Presupuesto", "Recibes por escrito qué incluye, el plazo y el precio cerrado. Tú decides sin compromiso.", "Por escrito"),
        ("Adquisición", "Con el teléfono delante, extraigo la conversación sin alterarla y documento cada paso de la cadena de custodia.", "Hash SHA-256"),
        ("Informe y juicio", "Te entrego el informe y te lo explico. Si hay que ratificarlo ante el juez, allí estaré para defenderlo.", "UNE 197010"),
    ],
    "precio_h2": "¿Cuánto cuesta un peritaje de WhatsApp?",
    "precio_factores": [
        "Cuántas conversaciones y qué periodo hay que analizar",
        "Si se trabaja con el teléfono o con una copia de seguridad",
        "Si hay que buscar mensajes eliminados o cotejar capturas de la otra parte",
        "La urgencia y los plazos del procedimiento",
        "Si hace falta ratificar el informe en juicio",
    ],
    "faq_h2": "Preguntas sobre el peritaje de WhatsApp",
    "faq": [
        ("¿Tengo que dejarte el móvil?",
         "Solo el tiempo de la adquisición, que se hace con el teléfono delante y suele resolverse en una sesión. En el Corredor del Henares y la Comunidad de Madrid voy yo; en el resto de España valoramos juntos la mejor opción."),
        ("¿Puedo exportar el chat yo mismo y enviártelo?",
         "La opción «Exportar chat» de WhatsApp genera un texto que cualquiera puede editar, así que no acredita nada por sí sola. Sirve para que me hagas una idea del caso, pero el informe se hace sobre el teléfono o su copia de seguridad."),
        ("¿Se pueden recuperar mensajes de WhatsApp borrados?",
         "A veces sí. Depende del modelo de teléfono, del tiempo transcurrido y de si existen copias de seguridad. Antes de empezar te digo con franqueza qué es razonable esperar."),
        ("¿Y si la conversación está en el móvil de la otra persona?",
         "Si participaste en ella, normalmente también está en tu teléfono y se analiza ahí. El dispositivo de otra persona solo se puede analizar con su consentimiento o por orden judicial, que tu abogado puede solicitar."),
        ("¿No basta con un acta notarial?",
         "El notario da fe de lo que ve en la pantalla, pero no comprueba si la conversación ha sido manipulada ni quién la escribió. Si la otra parte impugna los mensajes, lo que resuelve la duda es el análisis técnico de un perito."),
        ("¿Trabajas fuera de Madrid, por ejemplo en Sevilla, Málaga o Valencia?",
         "Sí, atiendo casos de toda España. Muchas veces la adquisición puede hacerse a distancia con cadena de custodia y huellas SHA-256; si hace falta, me desplazo. La ratificación puede hacerse por videoconferencia cuando el juzgado lo admite."),
        ("¿Cuánto cuesta un peritaje de WhatsApp?",
         "Depende del número de conversaciones y mensajes, de cómo haya que extraerlos, de la urgencia y de si hay que ratificar el informe en juicio. La primera consulta es gratuita y, si seguimos, recibes un presupuesto cerrado por escrito antes de empezar."),
    ],
    "relacionados": [
        ("/articulos/pantallazos-whatsapp-prueba-juicio/", "Pantallazos de WhatsApp como prueba: cuándo valen"),
        ("/articulos/primeras-horas-conservar-prueba-digital/", "Qué hacer en las primeras horas para no perder la prueba"),
        ("/articulos/pruebas-falsas-inteligencia-artificial/", "Pruebas falsas hechas con IA en los juicios"),
        ("/articulos/como-elegir-perito-informatico/", "Cómo elegir un perito informático"),
    ],
    "contacto_h2": "Cuéntame qué mensajes necesitas acreditar",
    "contacto_lead": "Con dos o tres frases me basta para orientarte. Mientras tanto, no borres el chat ni reinstales WhatsApp. Te respondo en menos de 24 horas.",
}

CORREO = {
    "slug": "peritaje-correo-electronico",
    "title": "Perito Informático de Correo Electrónico | Peritaje de emails",
    "desc": ("Peritaje de correo electrónico: origen real del email, cabeceras, SPF, DKIM y DMARC, "
             "facturas con otra cuenta y suplantaciones. Toda España. Consulta gratis."),
    "og_title": "Perito informático de correo electrónico",
    "nombre": "Peritaje informático de correo electrónico",
    "alternos": ["Perito de correo electrónico", "Peritaje de email", "Informe pericial de correo electrónico"],
    "tipo": "Peritaje informático de correo electrónico",
    "miga": "Correo electrónico",
    "corto": "Peritaje de correo electrónico",
    "wa_txt": "Hola Enrique, quería consultarte un caso de un correo electrónico.",
    "eyebrow": "Peritaje de correo electrónico",
    "h1": "Perito informático de <em>correo electrónico</em>",
    "lead": "Averiguo desde dónde se envió de verdad un correo, si es auténtico y si alguien ha suplantado a tu empresa o a tu proveedor, y lo presento en un informe pericial que sirve para la denuncia, la reclamación o el juicio. Para particulares, empresas y abogados, en toda España.",
    "casos_h2": "Casos en los que un peritaje de correo electrónico marca la diferencia",
    "casos": [
        ("Factura con otra cuenta bancaria", "Pagaste a un proveedor y el dinero acabó en otra cuenta. Hay que saber si el correo era suyo, si su buzón estaba comprometido o si era un dominio falso."),
        ("Suplantación de tu empresa", "Alguien envía correos en tu nombre o con un dominio casi idéntico al tuyo a tus clientes o a tu banco."),
        ("Correo que niegan haber enviado", "La otra parte dice que nunca mandó ese mensaje, o que el que aportas no es el que se envió."),
        ("Comunicaciones laborales", "Un despido, una sanción, una orden o un aviso por correo cuya fecha, envío o contenido hay que acreditar."),
        ("Phishing y reclamación al banco", "Picaste en un correo falso de tu banco y necesitas documentar cómo ocurrió para reclamar o denunciar."),
        ("Adjuntos manipulados", "Un PDF de factura, un contrato o un presupuesto que alguien ha modificado antes o después de enviarlo."),
    ],
    "duda_id": "impreso",
    "duda_eyebrow": "La pregunta más habitual",
    "duda_h2": "¿No basta con <em>imprimir</em> el correo?",
    "duda_lead": "No. Lo que ves en pantalla (el nombre del remitente, la dirección, la fecha) se puede falsificar con facilidad y no dice por dónde ha pasado el mensaje. Las pruebas técnicas están en las cabeceras, que no aparecen al imprimir ni en una captura.",
    "duda_link": ("/articulos/fraude-factura-cambio-cuenta-bancaria/", "Lee cómo funciona el fraude de la factura →"),
    "duda_puntos": [
        ("El remitente visible se puede falsificar", "El nombre y la dirección que muestra tu programa de correo los elige quien envía el mensaje."),
        ("Reenviar el correo lo altera", "Al reenviarlo se pierden o cambian las cabeceras originales que hay que analizar."),
        ("Lo que da solidez es el original", "El mensaje completo tal como está en el buzón (archivo .eml o .msg), adquirido con huella SHA-256 y explicado en un informe."),
    ],
    "analisis_lead": "Trabajo sobre el mensaje original exportado del buzón, con todas sus cabeceras, y, cuando hace falta, sobre los registros de la cuenta de correo.",
    "analisis": [
        ("Cabeceras completas", "Received, Message-ID, Return-Path y fechas: la ruta real del mensaje servidor a servidor y desde dónde salió."),
        ("SPF, DKIM y DMARC", "Si el servidor que lo envió estaba autorizado por el dominio y si la firma DKIM confirma que el mensaje no se ha alterado."),
        ("Dominios parecidos", "Detección de dominios casi idénticos al legítimo, con su fecha de registro y sus servidores de correo."),
        ("Adjuntos y metadatos", "Autor, programa y fechas de creación y modificación de PDF y documentos de Office, y cambios como un número de cuenta."),
        ("Buzón comprometido", "En Microsoft 365 o Google Workspace, inicios de sesión sospechosos y reglas de reenvío creadas por un intruso."),
        ("Envío y recepción", "Si un correo llegó a su destino y cuándo, a partir de las cabeceras y de los registros disponibles."),
    ],
    "nota_legal": "No accedo a cuentas de correo ajenas: solo analizo buzones y mensajes a los que tienes derecho legítimo de acceso.",
    "pasos_h2": "Cómo es un peritaje de correo electrónico, paso a paso",
    "pasos": [
        ("Me cuentas el caso", "Por WhatsApp, teléfono o correo. Te digo con franqueza si un informe te ayuda y qué mensajes conviene analizar.", "Gratis"),
        ("Presupuesto", "Recibes por escrito qué incluye, el plazo y el precio cerrado. Tú decides sin compromiso.", "Por escrito"),
        ("Adquisición", "Exporto los mensajes originales directamente del buzón, sin reenviarlos, y documento cada paso de la cadena de custodia.", "Hash SHA-256"),
        ("Informe y juicio", "Te entrego el informe y te lo explico. Si hay que ratificarlo ante el juez, allí estaré para defenderlo.", "UNE 197010"),
    ],
    "precio_h2": "¿Cuánto cuesta un peritaje de correo electrónico?",
    "precio_factores": [
        "Cuántos correos y qué periodo hay que analizar",
        "Si hay que revisar los registros de la cuenta (Microsoft 365, Google Workspace…)",
        "Si hay que analizar adjuntos o dominios sospechosos",
        "La urgencia y los plazos del procedimiento",
        "Si hace falta ratificar el informe en juicio",
    ],
    "faq_h2": "Preguntas sobre el peritaje de correo electrónico",
    "faq": [
        ("¿Me sirve el correo impreso o una captura?",
         "Como apoyo, sí; como prueba técnica, no. Ni la impresión ni la captura muestran las cabeceras, que son las que dicen desde dónde y por qué servidores se envió el mensaje."),
        ("¿Puedo reenviarte el correo para que lo analices?",
         "Mejor no: al reenviarlo se pierden datos. Te explico cómo descargar el mensaje original como archivo .eml o .msg, o lo exporto yo directamente del buzón con cadena de custodia."),
        ("Ya he pagado una factura falsa, ¿qué hago?",
         "Llama a tu banco cuanto antes para intentar retener la transferencia y presenta denuncia. No borres ni reenvíes los correos. El informe pericial documenta cómo se produjo el engaño y sirve para la denuncia y para reclamar a quien corresponda."),
        ("¿Se puede saber quién envió el correo?",
         "Normalmente se puede determinar desde qué servidor y en muchos casos desde qué dirección IP salió, y si el dominio era el legítimo. Identificar a la persona concreta suele requerir que el juzgado pida datos al proveedor, y el informe es la base para solicitarlo."),
        ("¿Puedes demostrar que un correo se envió o se recibió?",
         "En muchos casos sí, a partir de las cabeceras del mensaje en el buzón del destinatario o del remitente y de los registros de la cuenta. Antes de empezar te digo qué se puede acreditar con lo que hay."),
        ("¿Trabajas fuera de Madrid, por ejemplo en Málaga, Barcelona o Córdoba?",
         "Sí. El peritaje de correo se hace casi siempre a distancia: los mensajes se exportan del buzón con huellas SHA-256 y cadena de custodia, sin necesidad de desplazarse. La ratificación puede hacerse por videoconferencia cuando el juzgado lo admite."),
        ("¿Cuánto cuesta un peritaje de correo electrónico?",
         "Depende del número de mensajes, de si hay que revisar los registros de la cuenta o analizar adjuntos, de la urgencia y de si hay que ratificar el informe en juicio. La primera consulta es gratuita y, si seguimos, recibes un presupuesto cerrado por escrito antes de empezar."),
    ],
    "relacionados": [
        ("/articulos/fraude-factura-cambio-cuenta-bancaria/", "La factura con otra cuenta bancaria: el fraude BEC"),
        ("/articulos/victima-phishing-smishing-que-hacer/", "He pinchado en un correo falso de mi banco: qué hacer"),
        ("/articulos/primeras-horas-conservar-prueba-digital/", "Qué hacer en las primeras horas para no perder la prueba"),
        ("/articulos/como-elegir-perito-informatico/", "Cómo elegir un perito informático"),
    ],
    "contacto_h2": "Cuéntame qué correo necesitas analizar",
    "contacto_lead": "Con dos o tres frases me basta para orientarte. Mientras tanto, no borres ni reenvíes los mensajes. Te respondo en menos de 24 horas.",
}

CAPTURAS = {
    "slug": "peritaje-capturas-imagenes",
    "title": "Perito de Capturas de Pantalla e Imágenes | ¿Es auténtica?",
    "desc": ("Peritaje de capturas de pantalla y fotos: metadatos EXIF, huellas de edición, montajes e "
             "imágenes generadas con IA. Informe para juicio. Consulta gratis."),
    "og_title": "Perito informático de capturas de pantalla e imágenes",
    "nombre": "Peritaje informático de capturas de pantalla e imágenes",
    "alternos": ["Perito de capturas de pantalla", "Peritaje de fotografías", "Análisis forense de imágenes"],
    "tipo": "Análisis forense de imágenes",
    "miga": "Capturas e imágenes",
    "corto": "Peritaje de capturas e imágenes",
    "wa_txt": "Hola Enrique, quería consultarte un caso sobre una captura de pantalla o una foto.",
    "eyebrow": "Peritaje de capturas e imágenes",
    "h1": "¿Es auténtica esta <em>captura</em> o esta <em>foto</em>?",
    "lead": "Analizo capturas de pantalla y fotografías para saber si son originales, si se han retocado o si son un montaje, y lo presento en un informe pericial que puedes aportar al juicio o usar para impugnar la prueba de la otra parte. Para particulares y abogados, en toda España.",
    "casos_h2": "Casos en los que un peritaje de imágenes marca la diferencia",
    "casos": [
        ("Te acusan con un pantallazo", "La otra parte aporta una captura de WhatsApp, de un correo o de una red social que crees falsa, recortada o sacada de contexto."),
        ("Fotos como prueba de un hecho", "Daños en una vivienda o un vehículo, el estado de un local o una lesión: hay que acreditar cuándo y con qué dispositivo se tomó la foto."),
        ("Documentos fotografiados o escaneados", "Un justificante de pago, un contrato o un recibo cuya imagen pudo modificarse antes de presentarla."),
        ("Publicaciones en redes sociales", "Un comentario, un perfil o una historia de Instagram que ya no existe y del que solo queda una captura."),
        ("Imágenes generadas con IA", "Fotos o capturas que pueden haberse creado o alterado con herramientas de inteligencia artificial."),
        ("Acoso y difusión de imágenes", "Imágenes difundidas sin consentimiento cuyo origen, fecha o dispositivo hay que documentar para la denuncia."),
    ],
    "duda_id": "imagen-prueba",
    "duda_eyebrow": "Lo que conviene saber",
    "duda_h2": "Una imagen <em>no se defiende</em> sola",
    "duda_lead": "Hacer un pantallazo falso de WhatsApp o retocar una foto está hoy al alcance de cualquiera, y la inteligencia artificial lo ha hecho todavía más fácil. Si la otra parte impugna la imagen, hay que demostrar de dónde viene y que no se ha alterado.",
    "duda_link": ("/articulos/pruebas-falsas-inteligencia-artificial/", "Lee cómo se detectan las pruebas falsas hechas con IA →"),
    "duda_puntos": [
        ("Cuenta mucho el archivo original", "Una imagen reenviada por WhatsApp o descargada de una red social pierde casi todos sus metadatos. Siempre que se pueda, se analiza el archivo tal como lo guardó el dispositivo."),
        ("Una captura se coteja con su origen", "Si la conversación o la publicación todavía existe, se compara la captura con el original en el teléfono o en la cuenta."),
        ("No todo se puede afirmar", "A veces el análisis no permite concluir si hubo manipulación. Te digo antes de empezar qué es razonable esperar con lo que tienes."),
    ],
    "analisis_lead": "Trabajo sobre el archivo de imagen original y, si existe, sobre el dispositivo o la cuenta de los que procede, no solo sobre una copia impresa.",
    "analisis": [
        ("Metadatos EXIF y XMP", "Fecha y hora de captura, modelo de cámara o teléfono, software utilizado y, si existe, la ubicación GPS."),
        ("Huellas de edición", "Análisis de niveles de error (ELA), tablas de cuantización JPEG, doble compresión y zonas clonadas o pegadas."),
        ("Coherencia de la captura", "Si una captura de WhatsApp, correo o red social coincide con el formato real de la aplicación: tipografías, iconos, barra de estado, horas y orden de los mensajes."),
        ("Cotejo con el original", "Comparación de la captura con la conversación o publicación que se conserva en el dispositivo o en la cuenta."),
        ("Origen del archivo", "Indicios del dispositivo o programa que generó la imagen y de si ha pasado por aplicaciones que la recomprimen."),
        ("Contenido generado con IA", "Indicios técnicos y visuales de imágenes creadas o modificadas con inteligencia artificial, con sus limitaciones explicadas en el informe."),
    ],
    "nota_legal": "Analizo imágenes y capturas que tienes derecho a usar. No identifico a personas en fotos ni busco imágenes de terceros en Internet.",
    "pasos_h2": "Cómo es un peritaje de capturas e imágenes, paso a paso",
    "pasos": [
        ("Me cuentas el caso", "Por WhatsApp, teléfono o correo. Te digo con franqueza si un informe te ayuda y qué archivos conviene analizar.", "Gratis"),
        ("Presupuesto", "Recibes por escrito qué incluye, el plazo y el precio cerrado. Tú decides sin compromiso.", "Por escrito"),
        ("Adquisición", "Obtengo los archivos originales del dispositivo, de la cuenta o del expediente, calculo su huella SHA-256 y documento la cadena de custodia.", "Hash SHA-256"),
        ("Informe y juicio", "Te entrego el informe y te lo explico. Si hay que ratificarlo ante el juez, allí estaré para defenderlo.", "UNE 197010"),
    ],
    "precio_h2": "¿Cuánto cuesta un peritaje de capturas o imágenes?",
    "precio_factores": [
        "Cuántas imágenes o capturas hay que analizar",
        "Si se dispone del archivo original o solo de una copia",
        "Si hay que cotejar las capturas con el teléfono o la cuenta de origen",
        "La urgencia y los plazos del procedimiento",
        "Si hace falta ratificar el informe en juicio",
    ],
    "faq_h2": "Preguntas sobre el peritaje de capturas e imágenes",
    "faq": [
        ("¿Se puede saber si una captura de WhatsApp es falsa?",
         "Muchas veces sí. Se compara con la conversación original en el teléfono y se revisa si su formato coincide con el de la aplicación en esa versión. Si la conversación ya no existe, el análisis de la propia imagen aporta indicios, pero las conclusiones son más limitadas."),
        ("¿Qué pasa si la foto me la enviaron por WhatsApp?",
         "WhatsApp recomprime las imágenes y elimina la mayoría de los metadatos, así que se pierde información. Si es posible, conviene conseguir el archivo original del teléfono que hizo la foto."),
        ("¿Puedes saber cuándo y dónde se hizo una foto?",
         "Si el archivo original conserva sus metadatos EXIF, normalmente sí: fecha, hora, dispositivo y, si estaba activada, la ubicación GPS. Además compruebo si esos datos son coherentes entre sí, porque también se pueden modificar."),
        ("¿Se detectan las imágenes hechas con inteligencia artificial?",
         "Hay indicios técnicos y visuales que ayudan a detectarlas, pero ninguna herramienta es infalible. En el informe explico qué se ha encontrado y con qué grado de certeza, sin exagerar las conclusiones."),
        ("La otra parte ha presentado capturas, ¿qué puedo hacer?",
         "Tu abogado puede impugnarlas y pedir que se aporte el original. Con un informe pericial se señalan las incoherencias técnicas de las capturas y se justifica por qué no deben darse por buenas."),
        ("¿Trabajas fuera de Madrid?",
         "Sí. El análisis de imágenes se hace casi siempre a distancia: los archivos se entregan con su huella SHA-256 y cadena de custodia. Si hay que revisar un teléfono, en la Comunidad de Madrid voy yo y en el resto de España valoramos la mejor opción."),
        ("¿Cuánto cuesta un peritaje de capturas o imágenes?",
         "Depende del número de imágenes, de si se dispone del original y de si hay que cotejarlas con un teléfono o una cuenta. La primera consulta es gratuita y, si seguimos, recibes un presupuesto cerrado por escrito antes de empezar."),
    ],
    "relacionados": [
        ("/articulos/pruebas-falsas-inteligencia-artificial/", "Pruebas falsas hechas con IA en los juicios"),
        ("/articulos/pantallazos-whatsapp-prueba-juicio/", "Pantallazos de WhatsApp como prueba: cuándo valen"),
        ("/articulos/como-elegir-perito-informatico/", "Cómo elegir un perito informático"),
    ],
    "contacto_h2": "Cuéntame qué imagen necesitas analizar",
    "contacto_lead": "Con dos o tres frases me basta para orientarte. Mientras tanto, guarda los archivos originales y no los reenvíes ni los edites. Te respondo en menos de 24 horas.",
}

MOVIL = {
    "slug": "peritaje-movil",
    "title": "Perito Forense de Móviles Android e iPhone | Informe pericial",
    "desc": ("Análisis forense de móviles Android e iPhone: mensajes, llamadas, fotos y ubicaciones con "
             "cadena de custodia. Revisión de volcados policiales. Consulta gratis."),
    "og_title": "Perito forense de teléfonos móviles",
    "nombre": "Análisis forense de dispositivos móviles",
    "alternos": ["Perito informático de móviles", "Peritaje de teléfono móvil", "Forense de iPhone y Android"],
    "tipo": "Análisis forense de dispositivos móviles",
    "miga": "Teléfonos móviles",
    "corto": "Forense de móviles",
    "wa_txt": "Hola Enrique, quería consultarte un caso sobre el análisis de un teléfono móvil.",
    "eyebrow": "Forense de móviles Android e iOS",
    "h1": "Perito forense de <em>teléfonos móviles</em>",
    "lead": "Extraigo y analizo la información de teléfonos Android y iPhone (mensajes, llamadas, fotos, ubicaciones y aplicaciones) con cadena de custodia, y lo presento en un informe pericial para el juzgado. También reviso los volcados y los informes de móviles que aportan la policía o la otra parte.",
    "casos_h2": "Casos en los que el análisis de un móvil marca la diferencia",
    "casos": [
        ("Procedimientos penales", "Acreditar o descartar comunicaciones, llamadas o contactos entre personas investigadas a partir del contenido real del teléfono."),
        ("Revisión del volcado policial", "La policía ha extraído el teléfono y hay que comprobar qué contiene de verdad el volcado, cómo se hizo y si las conclusiones se sostienen."),
        ("Llamadas y comunicaciones", "Registro de llamadas, SMS y mensajes de varias aplicaciones para reconstruir quién habló con quién y cuándo."),
        ("Ubicaciones y desplazamientos", "Dónde estaba un teléfono en un momento concreto según la información que guardan el sistema, las fotos y las aplicaciones."),
        ("Ámbito laboral", "Teléfonos de empresa entregados por un empleado: qué contienen, qué se borró y cuándo, respetando la intimidad del trabajador."),
        ("Familia y custodia", "Mensajes, fotos y registros del propio teléfono que acreditan hechos relevantes en el procedimiento."),
    ],
    "duda_id": "deposito",
    "duda_eyebrow": "Muy habitual en penal",
    "duda_h2": "¿Y si el móvil está en el <em>juzgado</em>?",
    "duda_lead": "Cuando el teléfono está intervenido o depositado en el juzgado, el perito de parte no puede llevárselo sin más. Tu abogado debe pedir al juzgado que autorice el acceso o la entrega para la pericial, y el análisis se hace con las garantías que fije la resolución.",
    "duda_link": ("/articulos/primeras-horas-conservar-prueba-digital/", "Lee cómo conservar la prueba digital desde el principio →"),
    "duda_puntos": [
        ("Autorización judicial", "El abogado solicita la pericial y el acceso al dispositivo. El juzgado decide si se entrega, se analiza en sede judicial o se facilita una copia del volcado."),
        ("Trabajar sobre una copia", "Siempre que se pueda, el análisis se hace sobre una copia verificada con hash, para no alterar el original."),
        ("Contrastar el volcado oficial", "Si ya existe una extracción policial, compruebo su integridad y si permite sostener las conclusiones del atestado."),
    ],
    "analisis_lead": "Trabajo con extracciones lógicas del dispositivo y con sus copias de seguridad (iTunes/Finder, Google, iCloud cuando hay acceso legítimo), o con el volcado que facilite el juzgado.",
    "analisis": [
        ("Mensajería", "WhatsApp, Telegram, SMS y otras aplicaciones: conversaciones, participantes, fechas, adjuntos y mensajes eliminados cuando queden rastros."),
        ("Llamadas y contactos", "Registro de llamadas entrantes, salientes y perdidas, duración, contactos guardados y su historial."),
        ("Fotos, vídeos y audios", "Archivos multimedia con sus metadatos y su relación con las conversaciones en que se enviaron o recibieron."),
        ("Ubicaciones", "Datos de localización que guardan el sistema, las fotos y las aplicaciones, con sus limitaciones de precisión explicadas."),
        ("Línea temporal", "Reconstrucción cronológica de la actividad del teléfono en el periodo que interesa al procedimiento."),
        ("Revisión de informes ajenos", "Análisis crítico de volcados e informes de extracción (por ejemplo, de UFED/Cellebrite) aportados por la policía o la otra parte."),
    ],
    "nota_legal": "Solo analizo teléfonos a los que tienes derecho legítimo de acceso, con el consentimiento de su titular o con autorización judicial. No desbloqueo móviles ajenos ni accedo a cuentas de terceros.",
    "pasos_h2": "Cómo es el análisis forense de un móvil, paso a paso",
    "pasos": [
        ("Me cuentas el caso", "Por WhatsApp, teléfono o correo, tú o tu abogado. Te digo con franqueza si un informe te ayuda y qué hay que buscar.", "Gratis"),
        ("Presupuesto", "Recibes por escrito qué incluye, el plazo y el precio cerrado, incluidos los desplazamientos si los hay.", "Por escrito"),
        ("Adquisición", "Extraigo la información del teléfono o del volcado facilitado, calculo las huellas SHA-256 y documento la cadena de custodia.", "Hash SHA-256"),
        ("Informe y juicio", "Te entrego el informe y te lo explico. Si hay que ratificarlo ante el juez o el tribunal, allí estaré para defenderlo.", "UNE 197010"),
    ],
    "precio_h2": "¿Cuánto cuesta el análisis forense de un móvil?",
    "precio_factores": [
        "Qué hay que buscar y en qué periodo",
        "Si se trabaja con el teléfono, con una copia de seguridad o con un volcado ya realizado",
        "Si el móvil está depositado en un juzgado y hay que desplazarse",
        "La urgencia y los plazos del procedimiento",
        "Si hace falta ratificar el informe en juicio",
    ],
    "faq_h2": "Preguntas sobre el análisis forense de móviles",
    "faq": [
        ("¿Puedes analizar un móvil que está en el juzgado?",
         "Sí, siempre que el juzgado lo autorice. Tu abogado solicita la pericial y el acceso al teléfono o a una copia del volcado. Antes de pedirlo te ayudo a concretar qué hay que analizar, para que la solicitud sea precisa."),
        ("¿Se puede demostrar que dos personas no se comunicaron?",
         "Se puede acreditar qué registros existen en el teléfono y cuáles no, y si hay indicios de que se borró algo. Probar una ausencia tiene límites técnicos que explico en el informe con claridad, porque es justo lo que el tribunal va a preguntar."),
        ("¿Desbloqueas móviles sin el código?",
         "No. Trabajo con teléfonos cuyo titular facilita el acceso o con el volcado que proporciona el juzgado. No fuerzo el bloqueo de dispositivos ajenos."),
        ("¿Se pueden recuperar mensajes y fotos borrados?",
         "A veces. Depende del modelo, de la versión del sistema, del tiempo transcurrido y de las copias de seguridad. Antes de empezar te digo qué es razonable esperar, sin prometer lo que no se puede conseguir."),
        ("¿Revisas el informe de extracción de la policía?",
         "Sí. Compruebo cómo se hizo la extracción, si la cadena de custodia es correcta y si los datos sostienen las conclusiones del atestado. Es una de las contrapericiales más útiles en procedimientos penales."),
        ("¿Trabajas fuera de Madrid?",
         "Sí, en toda España. En la Comunidad de Madrid y el Corredor del Henares me desplazo con facilidad; en otras provincias valoramos el desplazamiento o el trabajo sobre un volcado. La ratificación puede hacerse por videoconferencia cuando el tribunal lo admite."),
        ("¿Cuánto cuesta analizar un móvil?",
         "Depende de qué haya que buscar, de cómo se acceda al teléfono, de los desplazamientos y de si hay que ratificar el informe. La primera consulta es gratuita y, si seguimos, recibes un presupuesto cerrado por escrito antes de empezar."),
    ],
    "relacionados": [
        ("/articulos/primeras-horas-conservar-prueba-digital/", "Qué hacer en las primeras horas para no perder la prueba"),
        ("/articulos/sim-swapping-movil-sin-cobertura/", "Móvil sin cobertura de repente: el SIM swapping"),
        ("/articulos/como-elegir-perito-informatico/", "Cómo elegir un perito informático"),
    ],
    "contacto_h2": "Cuéntame qué necesitas saber del teléfono",
    "contacto_lead": "Con dos o tres frases me basta para orientarte. Mientras tanto, no restaures el teléfono ni desinstales aplicaciones. Te respondo en menos de 24 horas.",
}

BORRADOS = {
    "slug": "recuperacion-datos-borrados",
    "title": "Recuperar Datos Borrados con Validez Pericial | Perito informático",
    "desc": ("Recuperación de mensajes, fotos y archivos borrados de móviles y copias de seguridad, con "
             "cadena de custodia y expectativas realistas. Consulta gratis."),
    "og_title": "Recuperación de datos borrados con validez pericial",
    "nombre": "Recuperación pericial de datos borrados",
    "alternos": ["Recuperar mensajes borrados", "Recuperación forense de datos", "Perito de datos borrados"],
    "tipo": "Recuperación forense de datos",
    "miga": "Datos borrados",
    "corto": "Recuperación de datos borrados",
    "wa_txt": "Hola Enrique, quería consultarte si se pueden recuperar unos datos borrados.",
    "eyebrow": "Datos borrados",
    "h1": "Recuperar datos <em>borrados</em> con validez pericial",
    "lead": "Busco mensajes, fotos y archivos eliminados en teléfonos, ordenadores y copias de seguridad, y documento lo que encuentro (y lo que no) en un informe pericial con cadena de custodia. Sin promesas imposibles: te digo antes de empezar qué es razonable esperar.",
    "casos_h2": "Casos en los que merece la pena buscar lo borrado",
    "casos": [
        ("Mensajes eliminados", "Una conversación de WhatsApp o un SMS clave que se borró por error o a propósito."),
        ("Fotos y vídeos", "Imágenes eliminadas del carrete que son importantes para acreditar un hecho."),
        ("Borrado por la otra parte", "Sospechas que alguien eliminó información de un dispositivo de empresa o compartido para ocultar algo."),
        ("Empleado que se marcha", "Un ordenador o un móvil de empresa devuelto «limpio»: qué se borró, cuándo y si se copió antes información."),
        ("Copias de seguridad antiguas", "La información ya no está en el teléfono, pero puede quedar en una copia de iCloud, Google o del ordenador."),
        ("Acreditar que hubo borrado", "A veces lo importante no es recuperar el contenido, sino demostrar que existió y que alguien lo eliminó."),
    ],
    "duda_id": "expectativas",
    "duda_eyebrow": "Hablemos claro",
    "duda_h2": "¿Se puede recuperar <em>todo</em>?",
    "duda_lead": "No, y desconfía de quien te lo asegure. Los teléfonos actuales cifran el almacenamiento y reutilizan rápido el espacio liberado, así que lo borrado hace tiempo suele perderse. Aun así, a menudo quedan rastros en bases de datos, copias de seguridad u otros dispositivos.",
    "duda_link": ("/articulos/primeras-horas-conservar-prueba-digital/", "Lee qué hacer en las primeras horas para no perder la prueba →"),
    "duda_puntos": [
        ("El tiempo juega en contra", "Cuanto más se usa el dispositivo después del borrado, menos probable es recuperar algo. Deja de usarlo si puedes."),
        ("Las copias de seguridad cuentan", "iCloud, Google Drive, copias en el ordenador o en otro teléfono pueden conservar lo que ya no está en el original."),
        ("Restaurar o reiniciar lo empeora", "No restaures el teléfono, no reinstales aplicaciones y no uses programas de recuperación que prometen milagros."),
    ],
    "analisis_lead": "Trabajo siempre sobre una copia verificada con hash, nunca directamente sobre el original, para no destruir lo que pueda quedar.",
    "analisis": [
        ("Bases de datos de aplicaciones", "Registros eliminados que permanecen en las bases SQLite de WhatsApp, SMS, llamadas o el carrete hasta que se sobrescriben."),
        ("Copias de seguridad", "Análisis de copias locales y en la nube a las que tienes acceso legítimo, comparadas con el estado actual del dispositivo."),
        ("Ordenadores y memorias", "Recuperación de archivos en discos, memorias USB y tarjetas SD mediante análisis del sistema de archivos y búsqueda por firmas."),
        ("Huellas del borrado", "Registros del sistema, miniaturas y referencias en otras aplicaciones que demuestran que un archivo o mensaje existió."),
        ("Línea temporal", "Cuándo se creó, se modificó y se eliminó la información, cuando el dispositivo lo registra."),
        ("Resultado documentado", "Qué se ha recuperado, de dónde procede y con qué certeza, y qué no ha sido posible recuperar."),
    ],
    "nota_legal": "Solo trabajo con dispositivos y cuentas a los que tienes derecho legítimo de acceso. No recupero información de dispositivos ajenos sin consentimiento de su titular o autorización judicial.",
    "pasos_h2": "Cómo es una recuperación de datos pericial, paso a paso",
    "pasos": [
        ("Me cuentas el caso", "Qué se borró, cuándo y en qué dispositivo. Te digo con franqueza si hay posibilidades reales antes de que gastes nada.", "Gratis"),
        ("Presupuesto", "Recibes por escrito qué incluye, el plazo y el precio cerrado. Tú decides sin compromiso.", "Por escrito"),
        ("Copia y análisis", "Hago una copia del dispositivo o de la copia de seguridad, calculo su huella SHA-256 y trabajo siempre sobre ella.", "Hash SHA-256"),
        ("Informe y juicio", "Te entrego el informe con lo recuperado y su procedencia. Si hay que ratificarlo ante el juez, allí estaré.", "UNE 197010"),
    ],
    "precio_h2": "¿Cuánto cuesta recuperar datos borrados?",
    "precio_factores": [
        "El tipo de dispositivo y de almacenamiento",
        "Qué información hay que buscar y de qué periodo",
        "Si existen copias de seguridad que analizar",
        "La urgencia y los plazos del procedimiento",
        "Si hace falta ratificar el informe en juicio",
    ],
    "faq_h2": "Preguntas sobre la recuperación de datos borrados",
    "faq": [
        ("¿Se pueden recuperar mensajes de WhatsApp borrados?",
         "A veces. Depende del teléfono, del tiempo transcurrido y de si hay copias de seguridad de WhatsApp en Google Drive o iCloud anteriores al borrado. Antes de empezar te digo qué es razonable esperar."),
        ("¿Y si borré el chat hace meses?",
         "Las posibilidades bajan mucho en el propio teléfono, pero puede quedar algo en copias de seguridad antiguas, en el ordenador o en el teléfono de la otra persona que participó en la conversación."),
        ("¿Sirve un programa de recuperación de los que se venden en Internet?",
         "No lo uses: puede sobrescribir justo lo que buscas y, además, el resultado no tendría cadena de custodia. Para que valga como prueba, el proceso tiene que estar documentado desde el principio."),
        ("Si no se recupera nada, ¿pago igual?",
         "El trabajo de análisis se presupuesta aunque el resultado sea negativo, porque se realiza igualmente. Por eso te digo antes de empezar si hay posibilidades reales; si no las veo, te lo digo y no seguimos."),
        ("¿Puedes demostrar que alguien borró información?",
         "A menudo sí: quedan huellas en el sistema, en otras aplicaciones o en copias de seguridad aunque el contenido no se pueda recuperar. Acreditar el borrado puede ser tan útil como recuperar el dato."),
        ("¿Trabajas fuera de Madrid?",
         "Sí, en toda España. Según el caso, me desplazo o se trabaja sobre una copia del dispositivo o de la copia de seguridad enviada con cadena de custodia."),
        ("¿Cuánto cuesta recuperar datos borrados?",
         "Depende del dispositivo, de lo que haya que buscar y de si hay copias de seguridad. La primera consulta es gratuita y, si seguimos, recibes un presupuesto cerrado por escrito antes de empezar."),
    ],
    "relacionados": [
        ("/articulos/primeras-horas-conservar-prueba-digital/", "Qué hacer en las primeras horas para no perder la prueba"),
        ("/articulos/pantallazos-whatsapp-prueba-juicio/", "Pantallazos de WhatsApp como prueba: cuándo valen"),
        ("/articulos/como-elegir-perito-informatico/", "Cómo elegir un perito informático"),
    ],
    "contacto_h2": "Cuéntame qué se borró y cuándo",
    "contacto_lead": "Con dos o tres frases me basta para decirte si hay posibilidades. Mientras tanto, usa el dispositivo lo menos posible y no lo restaures. Te respondo en menos de 24 horas.",
}

INFORME = {
    "slug": "informe-pericial-informatico",
    "title": "Informe Pericial Informático y Contrapericial | Ratificación en juicio",
    "desc": ("Informe pericial informático conforme a UNE 197010, contrapericial del informe contrario y "
             "ratificación en juicio. Civil, penal y laboral. Consulta gratis."),
    "og_title": "Informe pericial informático y contrapericial",
    "nombre": "Informe pericial informático",
    "alternos": ["Dictamen pericial informático", "Contrapericial informática", "Perito informático judicial"],
    "tipo": "Informe pericial informático",
    "miga": "Informe pericial",
    "corto": "Informe pericial y contrapericial",
    "wa_txt": "Hola Enrique, quería consultarte un informe pericial informático para un procedimiento.",
    "eyebrow": "Informe pericial y contrapericial",
    "h1": "Informe pericial informático y <em>contrapericial</em>",
    "lead": "Redacto informes periciales informáticos para procedimientos civiles, penales, laborales y contencioso-administrativos, reviso técnicamente el informe de la parte contraria y defiendo mis conclusiones en la ratificación. En coordinación con tu abogado, en toda España.",
    "casos_h2": "Cuándo necesitas un informe pericial informático",
    "casos": [
        ("Aportar una prueba digital", "Mensajes, correos, imágenes o datos de un dispositivo que tienen que entrar en el procedimiento con garantías de autenticidad."),
        ("Rebatir el informe contrario", "La otra parte ha presentado un informe pericial y necesitas una revisión técnica independiente de su método y sus conclusiones."),
        ("Revisar un atestado o volcado", "En penal, comprobar cómo se obtuvo la prueba digital de la acusación y si sostiene lo que se le atribuye."),
        ("Impugnar una prueba", "Capturas, correos o documentos de la otra parte que no tienen origen acreditado o presentan incoherencias técnicas."),
        ("Pericial judicial", "Designación por el juzgado a petición de parte para un informe técnico imparcial."),
        ("Antes de demandar", "Valorar con tu abogado si la prueba digital disponible sostiene la reclamación antes de iniciar el procedimiento."),
    ],
    "duda_id": "contrapericial",
    "duda_eyebrow": "La pregunta de los abogados",
    "duda_h2": "¿Qué aporta una <em>contrapericial</em>?",
    "duda_lead": "Un informe pericial no es verdad por haber sido presentado. La contrapericial revisa si el perito contrario adquirió bien la prueba, si respetó la cadena de custodia y si sus conclusiones se apoyan de verdad en los datos, y lo explica de forma que el tribunal pueda valorarlo.",
    "duda_link": ("/articulos/como-elegir-perito-informatico/", "Lee cómo elegir un perito informático →"),
    "duda_puntos": [
        ("Método y cadena de custodia", "Si la evidencia se obtuvo de forma verificable, con huellas hash y documentación de cada paso."),
        ("Herramientas y límites", "Si las herramientas usadas permiten afirmar lo que el informe afirma y qué limitaciones se omitieron."),
        ("Conclusiones frente a datos", "Si cada conclusión se apoya en un hecho técnico comprobable o es una interpretación sin respaldo."),
    ],
    "analisis_lead": "Cada informe sigue la estructura de la norma UNE 197010 y un tratamiento de la evidencia conforme a UNE 71505-3 e ISO/IEC 27037.",
    "analisis": [
        ("Objeto y alcance", "Qué se pide al perito, delimitado con el abogado, para que el informe responda exactamente a lo que interesa al procedimiento."),
        ("Adquisición documentada", "Cadena de custodia completa, con huellas SHA-256 de cada evidencia y registro de cada paso."),
        ("Metodología explicada", "Qué herramientas y técnicas se han usado y por qué, para que otro perito pueda reproducir el análisis."),
        ("Conclusiones claras", "Redactadas en lenguaje comprensible para jueces y letrados, separando lo que se afirma de lo que no se puede afirmar."),
        ("Revisión del informe contrario", "Análisis punto por punto del método, la cadena de custodia y las conclusiones del perito de la otra parte."),
        ("Ratificación", "Defensa del informe en juicio o vista y respuesta a las preguntas de las partes y del tribunal, presencial o por videoconferencia."),
    ],
    "nota_legal": "Actúo como perito de parte o judicial con independencia técnica: si el análisis no respalda tu posición, te lo diré antes de que el informe se presente.",
    "pasos_h2": "Cómo se elabora el informe pericial, paso a paso",
    "pasos": [
        ("Primera consulta", "Tú o tu abogado me contáis el caso y los plazos. Te digo con franqueza si la pericial tiene recorrido.", "Gratis"),
        ("Presupuesto y encargo", "Recibes por escrito qué incluye, el plazo y el precio cerrado. Concretamos el objeto de la pericial con el abogado.", "Por escrito"),
        ("Análisis", "Adquiero y analizo la evidencia, o reviso el informe contrario, documentando cada paso y la cadena de custodia.", "Hash SHA-256"),
        ("Informe y ratificación", "Entrego el informe en plazo, lo explico al abogado y lo defiendo ante el tribunal.", "UNE 197010"),
    ],
    "precio_h2": "¿Cuánto cuesta un informe pericial informático?",
    "precio_factores": [
        "Qué evidencias hay que analizar y su volumen",
        "Si es un informe propio o la revisión de un informe contrario",
        "Si hay que desplazarse para la adquisición o la ratificación",
        "Los plazos del procedimiento",
        "Si hace falta ratificar el informe en juicio",
    ],
    "faq_h2": "Preguntas sobre el informe pericial informático",
    "faq": [
        ("¿En qué procedimientos puedes actuar?",
         "En procedimientos civiles, penales, laborales y contencioso-administrativos, como perito de parte o designado por el juzgado. El informe se adapta a las exigencias de cada jurisdicción."),
        ("¿Cuánto tarda un informe pericial?",
         "Depende del volumen de evidencias y de la complejidad, pero siempre se fija un plazo por escrito en el presupuesto, ajustado a los plazos del procedimiento. Si hay urgencia, dímelo desde el primer mensaje."),
        ("¿Qué es la ratificación?",
         "Es la comparecencia del perito en el juicio o vista para confirmar su informe y responder a las preguntas de las partes y del tribunal. Preparo la ratificación con el abogado y explico las conclusiones con lenguaje claro."),
        ("¿Puedes revisar el informe del perito contrario?",
         "Sí. Analizo su método, la cadena de custodia, las herramientas y si sus conclusiones se sostienen. Puede plasmarse en un informe contrapericial o en notas técnicas para que tu abogado prepare el interrogatorio."),
        ("¿El informe me va a dar la razón?",
         "El informe dice lo que muestran los datos. Si el análisis no respalda tu posición, te lo comunico antes de presentarlo para que tu abogado decida, en lugar de aportar un informe que se volvería en tu contra."),
        ("¿Trabajas fuera de Madrid?",
         "Sí, en toda España. Gran parte del trabajo se hace a distancia con cadena de custodia, y la ratificación puede hacerse por videoconferencia cuando el tribunal lo admite. Si hay que desplazarse, se incluye en el presupuesto."),
        ("¿Cuánto cuesta un informe pericial informático?",
         "Depende del volumen de evidencias, de si es un informe propio o una contrapericial, de los desplazamientos y de la ratificación. La primera consulta es gratuita y, si seguimos, recibes un presupuesto cerrado por escrito antes de empezar."),
    ],
    "relacionados": [
        ("/articulos/como-elegir-perito-informatico/", "Cómo elegir un perito informático"),
        ("/articulos/pantallazos-whatsapp-prueba-juicio/", "Pantallazos de WhatsApp como prueba: cuándo valen"),
        ("/articulos/pruebas-falsas-inteligencia-artificial/", "Pruebas falsas hechas con IA en los juicios"),
    ],
    "contacto_h2": "Cuéntame el procedimiento y los plazos",
    "contacto_lead": "Con dos o tres frases me basta para orientarte. Si eres abogado, indícame la jurisdicción y la fecha límite. Te respondo en menos de 24 horas.",
}

ABOGADOS = {
    "slug": "peritaje-informatico-abogados",
    "title": "Perito Informático para Abogados y Despachos | Madrid y España",
    "desc": ("Perito informático para despachos: valoración previa de la prueba digital en 24 h, informe "
             "UNE 197010, contrapericial y ratificación. Civil, penal y laboral."),
    "og_title": "Perito informático para abogados y despachos",
    "nombre": "Perito informático para abogados",
    "alternos": ["Perito informático para despachos", "Colaboración pericial con abogados"],
    "tipo": "Peritaje informático para procedimientos judiciales",
    "miga": "Para abogados",
    "corto": "Para abogados y despachos",
    "wa_txt": "Hola Enrique, soy abogado y quería consultarte una pericial informática.",
    "eyebrow": "Para abogados y despachos",
    "h1": "Perito informático para <em>abogados</em> y despachos",
    "lead": "Trabajo con letrados en procedimientos civiles, penales, laborales y de familia en los que la prueba es digital: WhatsApp, correos, capturas, móviles. Te digo pronto y por escrito si la prueba se sostiene, y entrego el informe en el plazo que marca el procedimiento.",
    "casos_h2": "En qué te ayudo como perito de parte",
    "casos": [
        ("Valoración previa", "Antes de presentar la demanda o la denuncia, reviso la prueba digital de tu cliente y te digo si se sostiene y qué riesgos tiene si la impugnan."),
        ("Informe con la demanda", "Dictamen conforme a UNE 197010 para aportarlo con la demanda o la contestación, o en el momento procesal que corresponda."),
        ("Impugnar la prueba contraria", "Capturas, correos o documentos digitales de la otra parte sin origen acreditado: análisis técnico que fundamenta la impugnación."),
        ("Contrapericial", "Revisión del informe del perito contrario: método, cadena de custodia, herramientas y si las conclusiones se apoyan en los datos."),
        ("Penal: volcados y atestados", "Revisión de extracciones de móviles y de informes policiales, y análisis de dispositivos depositados con autorización judicial."),
        ("Preparar el interrogatorio", "Notas técnicas para la vista: qué preguntar al perito contrario y qué puntos débiles tiene su informe."),
    ],
    "duda_id": "plazos",
    "duda_eyebrow": "Lo que más preocupa a un despacho",
    "duda_h2": "Plazos, <em>honorarios</em> y criterio",
    "duda_lead": "Sé que el informe tiene que llegar a tiempo y que no puedes presentar una pericial que se caiga en la vista. Por eso trabajo con un plazo y un precio fijados por escrito desde el principio, y te aviso antes de redactar si el análisis no respalda la tesis de tu cliente.",
    "duda_link": ("/informe-pericial-informatico/", "Ver cómo es el informe pericial y la contrapericial →"),
    "duda_puntos": [
        ("Respuesta en 24 horas", "Primera valoración del caso sin coste, por teléfono, WhatsApp o correo, con indicación clara de si la pericial tiene recorrido."),
        ("Presupuesto cerrado", "Honorarios por escrito antes de empezar, incluidos los desplazamientos y la ratificación si se prevé."),
        ("Independencia técnica", "Si los datos no sostienen lo que necesitas, te lo digo antes de que el informe se presente."),
    ],
    "analisis_lead": "Informes con la estructura de la norma UNE 197010 y tratamiento de la evidencia según UNE 71505-3 e ISO/IEC 27037, pensados para que el juez los entienda.",
    "analisis": [
        ("Objeto pericial acotado", "Delimito contigo las preguntas que debe responder el informe, para que sea útil al procedimiento y no un análisis genérico."),
        ("Cadena de custodia", "Adquisición documentada con huellas SHA-256 desde el primer momento, para que la integridad de la prueba no sea un punto de ataque."),
        ("Lenguaje claro", "Conclusiones redactadas para jueces y letrados, separando lo que se afirma con certeza de lo que no puede afirmarse."),
        ("Mensajería y correo", "WhatsApp, Telegram, correo electrónico (cabeceras, SPF, DKIM, DMARC) y suplantaciones de identidad."),
        ("Imágenes y móviles", "Autenticidad de capturas y fotografías, análisis forense de teléfonos y recuperación de datos borrados cuando es posible."),
        ("Ratificación", "Comparecencia en juicio o vista, presencial en Madrid y Guadalajara y por videoconferencia en el resto de España cuando el tribunal lo admite."),
    ],
    "nota_legal": "Actúo como perito de parte o por designación judicial. Solo analizo dispositivos y cuentas con derecho legítimo de acceso, consentimiento del titular o autorización judicial.",
    "pasos_h2": "Cómo trabajamos juntos",
    "pasos": [
        ("Me cuentas el caso", "Jurisdicción, fase del procedimiento, plazos y qué prueba digital hay. Con eso te doy una primera valoración.", "24 h"),
        ("Presupuesto y encargo", "Honorarios y plazo de entrega por escrito. Concretamos juntos el objeto de la pericial.", "Por escrito"),
        ("Análisis e informe", "Adquiero la evidencia con cadena de custodia, la analizo y te explico las conclusiones antes de entregar el informe.", "UNE 197010"),
        ("Vista", "Preparamos la ratificación y defiendo el informe ante el tribunal.", "Ratificación"),
    ],
    "precio_h2": "¿Cómo se presupuesta una pericial informática?",
    "precio_factores": [
        "El tipo y el volumen de la prueba digital",
        "Si es un informe propio o una contrapericial",
        "Si hay que desplazarse para la adquisición o la vista",
        "Los plazos del procedimiento",
        "Si se prevé ratificación en juicio",
    ],
    "faq_h2": "Preguntas frecuentes de abogados",
    "faq": [
        ("¿Con cuánto tiempo necesitas el encargo?",
         "Cuanto antes, mejor, sobre todo si hay que adquirir la prueba de un teléfono. En cuanto me cuentes el caso te digo el plazo realista de entrega, y si el procedimiento aprieta lo indicamos en el presupuesto."),
        ("¿Puedo consultarte antes de que el cliente decida encargar la pericial?",
         "Sí. La primera valoración es gratuita y sirve precisamente para decidir si merece la pena. Si la prueba no se sostiene o no hace falta perito, te lo digo."),
        ("¿Trabajas en procedimientos penales?",
         "Sí, como perito de parte de la defensa o de la acusación particular: revisión de volcados y atestados, análisis de dispositivos depositados con autorización judicial y contrapericial del informe policial o del perito contrario."),
        ("¿Puedes ratificar fuera de Madrid?",
         "Sí. En Madrid y Guadalajara acudo en persona. En el resto de España, si el tribunal admite la videoconferencia la ratificación se hace a distancia; si exige presencia, me desplazo y el viaje figura en el presupuesto."),
        ("¿El informe va firmado por un ingeniero?",
         "Sí. Soy ingeniero técnico industrial con más de veinte años en consultoría tecnológica y de datos, y firmo personalmente cada informe y su ratificación."),
    ],
    "relacionados": [
        ("/articulos/pantallazos-whatsapp-prueba-juicio/", "Pantallazos de WhatsApp como prueba: cuándo valen"),
        ("/articulos/como-elegir-perito-informatico/", "Cómo elegir y contratar un perito informático"),
        ("/articulos/pruebas-falsas-inteligencia-artificial/", "Pruebas falsas hechas con IA en los juicios"),
    ],
    "contacto_h2": "Cuéntame el procedimiento y el plazo",
    "contacto_lead": "Jurisdicción, fase y fecha límite: con eso te doy una primera valoración en menos de 24 horas.",
}

SERVICIOS = [WHATSAPP, CORREO, CAPTURAS, MOVIL, BORRADOS, INFORME, ABOGADOS]


# ───────────────────────── plantilla ─────────────────────────
def wa(texto):
    return f"https://wa.me/{gz.WA}?text={quote(texto)}"


def tarjetas(items):
    return "\n".join(
        f"""      <article class="problem">
        <h3>{esc(t)}</h3>
        <p>{esc(d)}</p>
      </article>""" for t, d in items
    )


def pagina(s):
    url = f"{SITE}/{s['slug']}/"
    wa_url = wa(s["wa_txt"])
    jsonld = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "@id": url + "#servicio",
            "name": s["nombre"],
            "alternateName": s["alternos"],
            "serviceType": s["tipo"],
            "url": url,
            "description": s["desc"],
            "provider": {"@id": SITE + "/#organization"},
            "areaServed": {"@type": "Country", "name": "España"},
            "availableChannel": {
                "@type": "ServiceChannel",
                "servicePhone": {"@type": "ContactPoint", "telephone": gz.TEL, "contactType": "customer service", "availableLanguage": "es"},
                "serviceUrl": url,
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Servicios", "item": SITE + "/#servicios"},
                {"@type": "ListItem", "position": 3, "name": s["corto"], "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]
            ],
        },
    ]

    hero = f"""<section class="hero hero-local" id="inicio" aria-labelledby="h1">
  <div class="wrap">
    <nav class="crumbs" aria-label="Migas de pan"><a href="/">Inicio</a><span aria-hidden="true">›</span><a href="/#servicios">Servicios</a><span aria-hidden="true">›</span><span aria-current="page">{esc(s['miga'])}</span></nav>
    <span class="eyebrow">{esc(s['eyebrow'])}</span>
    <h1 id="h1">{s['h1']}</h1>
    <p class="lead">{esc(s['lead'])}</p>
    <div class="hero-ctas">
      <a class="btn btn-wa" href="{wa_url}" target="_blank" rel="noopener">{gz.ICON_WA} Escríbeme por WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{gz.TEL}">{gz.ICON_TEL} {gz.TEL_H}</a>
    </div>
    <ul class="reassure">
      <li>{gz.ICON_CHECK}Primera consulta gratuita</li>
      <li>{gz.ICON_CHECK}Presupuesto cerrado por escrito</li>
      <li>{gz.ICON_CHECK}Informes conforme a UNE 197010</li>
    </ul>
  </div>
</section>"""

    casos = f"""<section class="band" id="casos" aria-labelledby="h2-casos">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Cuándo lo necesitas</span>
      <h2 id="h2-casos">{esc(s['casos_h2'])}</h2>
      <p class="lead">Si tu caso no está aquí, cuéntamelo igualmente: te digo si un informe tiene sentido antes de que gastes nada.</p>
    </div>
    <div class="problems">
{tarjetas(s['casos'])}
    </div>
  </div>
</section>"""

    puntos = "\n".join(f"      <li><strong>{esc(t)}</strong><span>{esc(d)}</span></li>" for t, d in s["duda_puntos"])
    duda = f"""<section id="{s['duda_id']}" aria-labelledby="h2-{s['duda_id']}">
  <div class="wrap first-aid">
    <div>
      <span class="eyebrow">{esc(s['duda_eyebrow'])}</span>
      <h2 id="h2-{s['duda_id']}">{s['duda_h2']}</h2>
      <p class="lead">{esc(s['duda_lead'])}</p>
      <p><a class="problem-link" href="{s['duda_link'][0]}">{esc(s['duda_link'][1])}</a></p>
    </div>
    <ol>
{puntos}
    </ol>
  </div>
</section>"""

    analisis = f"""<section class="band" id="que-analizo" aria-labelledby="h2-analizo">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">El detalle técnico</span>
      <h2 id="h2-analizo">Qué analizo exactamente</h2>
      <p class="lead">{esc(s['analisis_lead'])}</p>
    </div>
    <div class="problems">
{tarjetas(s['analisis'])}
    </div>
{NORMAS}
    <p class="note-out">{esc(s['nota_legal'])}</p>
  </div>
</section>"""

    pasos_li = "\n".join(f"""      <li class="step">
        <h3>{esc(t)}</h3>
        <p>{esc(d)}</p>
        <span class="tag">{esc(tag)}</span>
      </li>""" for t, d, tag in s["pasos"])
    pasos = f"""<section id="como-trabajo" aria-labelledby="h2-proceso">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">Sin sorpresas</span>
      <h2 id="h2-proceso">{esc(s['pasos_h2'])}</h2>
    </div>
    <ol class="steps">
{pasos_li}
    </ol>
  </div>
</section>"""

    factores = "\n".join(f"          <li>{esc(f)}</li>" for f in s["precio_factores"])
    precio = f"""<section class="band" id="precio" aria-labelledby="h2-precio">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Hablemos claro</span>
      <h2 id="h2-precio">{esc(s['precio_h2'])}</h2>
      <p class="lead">No te voy a dar una tarifa genérica que luego no se cumple. Lo que sí te garantizo:</p>
    </div>
    <div class="price">
      <div class="price-card highlight">
        <p class="big">0 €</p>
        <h3>La primera consulta</h3>
        <p>Me cuentas tu caso y te digo, sin compromiso, si un informe pericial te va a ayudar. Si no lo necesitas, te lo digo.</p>
      </div>
      <div class="price-card">
        <h3>Presupuesto cerrado, antes de empezar</h3>
        <p>El precio depende sobre todo de:</p>
        <ul>
{factores}
        </ul>
      </div>
    </div>
  </div>
</section>"""

    faq_items = "\n".join(
        f'      <details class="qa"><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>'
        for q, a in s["faq"]
    )
    faq = f"""<section id="preguntas" aria-labelledby="h2-faq">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow">Dudas habituales</span>
      <h2 id="h2-faq">{esc(s['faq_h2'])}</h2>
    </div>
    <div class="faq">
{faq_items}
    </div>
  </div>
</section>"""

    otros = [o for o in SERVICIOS if o is not s]
    rel = [(u, t) for u, t in s["relacionados"]] + [(f"/{o['slug']}/", o["corto"]) for o in otros]
    rel_li = "\n".join(f'      <li><a href="{u}">{esc(t)}</a></li>' for u, t in rel)
    relacionados = f"""<section id="leer-mas" aria-labelledby="h2-leer">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Para leer con calma</span>
      <h2 id="h2-leer">Artículos y servicios relacionados</h2>
    </div>
    <ul class="zone-links">
{rel_li}
    </ul>
    <p class="zone-all"><a href="/zonas/">Ver las zonas donde trabajo →</a></p>
  </div>
</section>"""

    contacto = f"""<section class="band" id="contacto" aria-labelledby="h2-contacto">
  <div class="wrap">
    <div class="cta-local">
      <div>
        <span class="eyebrow">Primera consulta gratuita</span>
        <h2 id="h2-contacto">{esc(s['contacto_h2'])}</h2>
        <p class="lead">{esc(s['contacto_lead'])}</p>
      </div>
      <div class="hero-ctas">
        <a class="btn btn-wa" href="{wa_url}" target="_blank" rel="noopener">{gz.ICON_WA} Escríbeme por WhatsApp</a>
        <a class="btn btn-ghost" href="tel:{gz.TEL}">{gz.ICON_TEL} {gz.TEL_H}</a>
        <a class="btn btn-ghost" href="/#contacto">Formulario de contacto</a>
      </div>
    </div>
  </div>
</section>"""

    cuerpo = "\n\n".join([hero, casos, duda, analisis, pasos, precio, faq, relacionados, contacto])
    doc = gz.documento(s["title"], s["desc"], url, jsonld, cuerpo, og_title=s["og_title"])
    return doc.replace(gz.quickbar(), gz.quickbar().replace(f"https://wa.me/{gz.WA}", wa_url))


def main():
    for s in SERVICIOS:
        d = os.path.join(gz.ROOT, s["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina(s))
    print(f"{len(SERVICIOS)} páginas de servicio: " + ", ".join(f"/{s['slug']}/" for s in SERVICIOS))


if __name__ == "__main__":
    main()

"""Contenido propio de las páginas de capitales de provincia (y Ceuta y Melilla).

Solo hechos comprobables y útiles para quien tiene una prueba digital:
- municipios principales de la provincia (para que la página sirva a toda la provincia),
- secciones de la Audiencia Provincial fuera de la capital y sedes del TSJ,
- policía autonómica con competencias en ciberdelitos,
- lengua cooficial (mensajes y correos en catalán, valenciano, gallego o euskera),
- huso horario distinto (Canarias) y fronteras (Portugal, Marruecos, Francia),
- tren de alta velocidad con Madrid o desplazamiento en avión/barco.

generar_zonas.py llama a construir(lugar) y lo mezcla con LOCAL_EXTRA.
Nada de oficinas, domicilios ni casos inventados.
"""

# slug -> datos
D = {
    "a-coruna": dict(pueblos=["Santiago de Compostela", "Ferrol", "Arteixo", "Oleiros", "Carballo"], lengua="gallego", ave=True),
    "albacete": dict(pueblos=["Hellín", "Villarrobledo", "Almansa", "La Roda"], ave=True),
    "alicante": dict(pueblos=["Elche", "Torrevieja", "Orihuela", "Benidorm", "Alcoy", "Elda"], lengua="valenciano", ave=True,
                     secciones=["Elche"]),
    "almeria": dict(pueblos=["Roquetas de Mar", "El Ejido", "Vícar", "Níjar", "Huércal-Overa"], andalucia=True),
    "avila": dict(pueblos=["Arévalo", "Arenas de San Pedro", "Piedrahíta"], cyl=True),
    "badajoz": dict(pueblos=["Mérida", "Don Benito", "Almendralejo", "Villanueva de la Serena", "Zafra"], frontera="Portugal",
                    secciones=["Mérida"]),
    "barcelona": dict(pueblos=["L'Hospitalet de Llobregat", "Badalona", "Terrassa", "Sabadell", "Mataró"], lengua="catalán",
                      policia="los Mossos d'Esquadra", ave=True),
    "bilbao": dict(pueblos=["Barakaldo", "Getxo", "Portugalete", "Santurtzi", "Durango"], lengua="euskera", policia="la Ertzaintza"),
    "burgos": dict(pueblos=["Miranda de Ebro", "Aranda de Duero", "Briviesca"], ave=True, cyl=True),
    "caceres": dict(pueblos=["Plasencia", "Navalmoral de la Mata", "Coria", "Trujillo"], frontera="Portugal"),
    "cadiz": dict(pueblos=["Jerez de la Frontera", "Algeciras", "San Fernando", "El Puerto de Santa María", "Chiclana de la Frontera"],
                  secciones=["Jerez de la Frontera", "Algeciras", "Ceuta"], andalucia=True),
    "castellon-de-la-plana": dict(pueblos=["Vila-real", "Burriana", "la Vall d'Uixó", "Vinaròs", "Benicarló"], lengua="valenciano", ave=True),
    "ciudad-real": dict(pueblos=["Puertollano", "Tomelloso", "Alcázar de San Juan", "Valdepeñas", "Manzanares"], ave=True),
    "cordoba": dict(pueblos=["Lucena", "Puente Genil", "Montilla", "Priego de Córdoba", "Cabra"], ave=True, andalucia=True),
    "cuenca": dict(pueblos=["Tarancón", "San Clemente", "Motilla del Palancar"], ave=True),
    "girona": dict(pueblos=["Figueres", "Blanes", "Lloret de Mar", "Olot", "Salt"], lengua="catalán", policia="los Mossos d'Esquadra",
                   frontera="Francia", ave=True),
    "granada": dict(pueblos=["Motril", "Baza", "Guadix", "Loja", "Almuñécar"], ave=True, andalucia=True),
    "huelva": dict(pueblos=["Ayamonte", "Moguer", "Lepe", "Almonte", "Isla Cristina"], frontera="Portugal", andalucia=True),
    "huesca": dict(pueblos=["Monzón", "Barbastro", "Fraga", "Jaca", "Sabiñánigo"], frontera="Francia", ave=True),
    "jaen": dict(pueblos=["Linares", "Andújar", "Úbeda", "Martos", "Alcalá la Real"], andalucia=True),
    "las-palmas-de-gran-canaria": dict(pueblos=["Telde", "Santa Lucía de Tirajana", "Arrecife (Lanzarote)", "Puerto del Rosario (Fuerteventura)"],
                                       canarias=True, isla=True),
    "leon": dict(pueblos=["Ponferrada", "San Andrés del Rabanedo", "Astorga", "La Bañeza"], ave=True, cyl=True),
    "lleida": dict(pueblos=["Balaguer", "Tàrrega", "Mollerussa", "la Seu d'Urgell"], lengua="catalán", policia="los Mossos d'Esquadra",
                   frontera="Francia y Andorra", ave=True),
    "logrono": dict(pueblos=["Calahorra", "Arnedo", "Haro"]),
    "lugo": dict(pueblos=["Monforte de Lemos", "Viveiro", "Vilalba", "Sarria"], lengua="gallego"),
    "malaga": dict(pueblos=["Marbella", "Vélez-Málaga", "Fuengirola", "Torremolinos", "Estepona", "Antequera"], ave=True,
                   secciones=["Melilla"], andalucia=True),
    "murcia": dict(pueblos=["Cartagena", "Lorca", "Molina de Segura", "Yecla"], ave=True, secciones=["Cartagena"]),
    "ourense": dict(pueblos=["Verín", "O Barco de Valdeorras", "O Carballiño", "Xinzo de Limia"], lengua="gallego", frontera="Portugal", ave=True),
    "oviedo": dict(pueblos=["Gijón", "Avilés", "Mieres", "Langreo", "Siero"], ave=True, secciones=["Gijón"]),
    "palencia": dict(pueblos=["Carrión de los Condes", "Aguilar de Campoo", "Guardo", "Venta de Baños"], ave=True, cyl=True),
    "palma": dict(pueblos=["Manacor", "Inca", "Calvià", "Ibiza", "Maó (Menorca)"], lengua="catalán", isla=True),
    "pamplona": dict(pueblos=["Tudela", "Estella-Lizarra", "Tafalla", "Aoiz"], lengua="euskera (en parte de Navarra)",
                     policia="la Policía Foral de Navarra", frontera="Francia"),
    "pontevedra": dict(pueblos=["Vigo", "Vilagarcía de Arousa", "Redondela", "Cangas", "Lalín"], lengua="gallego", frontera="Portugal",
                       ave=True, secciones=["Vigo"]),
    "salamanca": dict(pueblos=["Béjar", "Ciudad Rodrigo", "Peñaranda de Bracamonte", "Vitigudino"], frontera="Portugal", cyl=True),
    "san-sebastian": dict(pueblos=["Irun", "Errenteria", "Eibar", "Zarautz", "Tolosa", "Bergara"], lengua="euskera",
                          policia="la Ertzaintza", frontera="Francia"),
    "santa-cruz-de-tenerife": dict(pueblos=["San Cristóbal de La Laguna", "Arona", "Adeje", "Puerto de la Cruz", "Santa Cruz de La Palma"],
                                   canarias=True, isla=True),
    "santander": dict(pueblos=["Torrelavega", "Castro Urdiales", "Laredo", "Reinosa"]),
    "segovia": dict(pueblos=["Cuéllar", "Sepúlveda", "Santa María la Real de Nieva"], ave=True, cyl=True),
    "sevilla": dict(pueblos=["Dos Hermanas", "Alcalá de Guadaíra", "Utrera", "Écija", "Lebrija", "Carmona"], ave=True, andalucia=True),
    "soria": dict(pueblos=["Almazán", "El Burgo de Osma"], cyl=True),
    "tarragona": dict(pueblos=["Reus", "Tortosa", "El Vendrell", "Valls", "Amposta", "Cambrils"], lengua="catalán",
                      policia="los Mossos d'Esquadra", ave=True),
    "teruel": dict(pueblos=["Alcañiz", "Calamocha"]),
    "toledo": dict(pueblos=["Talavera de la Reina", "Illescas", "Seseña", "Torrijos", "Ocaña", "Quintanar de la Orden"], ave=True),
    "valencia": dict(pueblos=["Torrent", "Gandia", "Paterna", "Sagunt", "Alzira", "Xàtiva"], lengua="valenciano", ave=True),
    "valladolid": dict(pueblos=["Medina del Campo", "Laguna de Duero", "Tordesillas"], ave=True, cyl=True),
    "vitoria-gasteiz": dict(pueblos=["Amurrio", "Laudio/Llodio"], lengua="euskera", policia="la Ertzaintza"),
    "zamora": dict(pueblos=["Benavente", "Toro", "Puebla de Sanabria", "Villalpando"], frontera="Portugal", ave=True, cyl=True),
    "zaragoza": dict(pueblos=["Calatayud", "Ejea de los Caballeros", "Utebo", "Tarazona", "Caspe"], ave=True),
    "ceuta": dict(pueblos=[], frontera="Marruecos", isla=True, andalucia=True),
    "melilla": dict(pueblos=[], frontera="Marruecos", isla=True, andalucia=True),
}


def _lista(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " y " + items[-1]


def construir(l, enlace_lugar):
    """Devuelve el dict de LOCAL_EXTRA para la capital l, o None si no hay datos."""
    x = D.get(l["slug"])
    if x is None:
        return None
    n, prov = l["nombre"], l["provincia"]
    pueblos = x.get("pueblos", [])
    pueblos_html = _lista(enlace_lugar(p) if p == "Puertollano" else p for p in pueblos)

    # ── lead ──
    if pueblos:
        ambito = f"Atiendo a particulares, empresas y despachos de {n} y del resto de la provincia de {prov}: {_lista(pueblos)}."
    else:
        ambito = f"Atiendo a particulares, empresas y despachos de {n}."
    if x.get("isla") and x.get("frontera") == "Marruecos":
        viaje = f"Para llegar a {n} hace falta barco o avión, así que casi todo se organiza a distancia y el desplazamiento se reserva para lo imprescindible."
    elif x.get("isla"):
        viaje = f"Desde Madrid se llega a {n} en avión: casi todo se organiza a distancia y el viaje se reserva para lo que de verdad lo exige."
    elif x.get("ave"):
        viaje = f"{n} tiene tren de alta velocidad con Madrid, así que cuando hay que ver un teléfono o ratificar puedo ir y volver con facilidad."
    else:
        viaje = f"Lo que se puede hacer a distancia se hace a distancia; para un teléfono o una ratificación presencial, me desplazo a {n}."
    lead = f"{ambito} {viaje}"

    # ── filas de juzgados ──
    juz = []
    secc = [s for s in x.get("secciones", []) if s not in ("Ceuta", "Melilla")]
    if secc:
        juz.append(("Secciones desplazadas",
                    f"La Audiencia Provincial de {prov} tiene también sección en {_lista(secc)}, que conoce de los recursos de su zona."))
    if x.get("andalucia") and l["slug"] not in ("granada",):
        juz.append(("Salas del TSJ", "El Tribunal Superior de Justicia de Andalucía, Ceuta y Melilla tiene su sede en Granada y salas también en Sevilla y Málaga."))
    if x.get("cyl") and l["slug"] not in ("burgos", "valladolid"):
        juz.append(("Salas del TSJ", "El Tribunal Superior de Justicia de Castilla y León tiene su sede en Burgos y salas también en Valladolid."))
    if x.get("canarias"):
        juz.append(("Dos sedes", "El Tribunal Superior de Justicia de Canarias tiene sede en Las Palmas de Gran Canaria y en Santa Cruz de Tenerife."))
    if x.get("policia"):
        juz.append(("Denuncias", f"Las denuncias por estafas, acoso o amenazas en línea se pueden presentar ante {x['policia']}, además de en el juzgado."))

    # ── casos ──
    casos = []
    lengua = x.get("lengua")
    if lengua:
        lg = lengua.split(" (")[0]
        casos.append((f"Mensajes en {lg}",
                      f"Chats y correos escritos en {lg}: el análisis técnico (metadatos, hashes, cabeceras) no depende del idioma. "
                      f"En el informe se identifican los mensajes relevantes y, si el procedimiento lo pide, se acompaña traducción al castellano."))
    if x.get("canarias"):
        casos.append(("Horas que no cuadran",
                      "Canarias va una hora por detrás de la península. Si una captura se hizo con un teléfono en otro huso, las horas "
                      "no coinciden con el original y la otra parte puede usarlo para impugnarla. En el informe se explica y se cuadra."))
    fr = x.get("frontera")
    if fr == "Portugal":
        casos.append(("Teléfonos cerca de la raya",
                      "Cerca de la frontera el móvil puede engancharse a una red portuguesa. Portugal va una hora por detrás, y eso "
                      "puede cambiar la hora de algunos registros. Hay que tenerlo en cuenta antes de afirmar cuándo se envió un mensaje."))
    elif fr == "Marruecos":
        casos.append(("Redes marroquíes y horarios",
                      "Muchos teléfonos se conectan a redes de Marruecos, que no sigue el mismo horario que España durante buena parte "
                      "del año. Antes de fechar un mensaje hay que comprobar con qué red y en qué hora estaba el dispositivo."))
    if x.get("policia"):
        casos.append((f"Denuncia ante {x['policia'].replace('los ', '').replace('la ', '')}",
                      f"Si vas a denunciar ante {x['policia']}, conviene llevar la conversación fijada con su huella SHA-256 para que "
                      f"no se pierda ni se pueda negar después."))
    if x.get("isla") and not fr:
        casos.append(("Prueba sin viajar",
                      "Correos, archivos y copias de conversaciones se reciben a distancia con huella SHA-256 desde el primer momento. "
                      "Para un teléfono, se valora el envío con cadena de custodia antes que el viaje."))
    p1 = pueblos[0] if pueblos else n
    genericos = [
        ("Familia y custodia", f"Mensajes entre exparejas sobre los hijos, la pensión o las visitas que se discuten en los juzgados de {n} o de {p1}."),
        ("Estafas y facturas falsas", "Facturas con la cuenta bancaria cambiada, SMS que suplantan al banco y compraventas entre particulares que acaban en denuncia."),
        ("Amenazas y acoso", "Conversaciones de WhatsApp, Instagram o Telegram que hay que fijar antes de denunciar para que no se pierdan ni se puedan negar."),
        ("Trabajo y empresa", "Despidos y reclamaciones con mensajes del encargado, correos internos o registros que una de las partes niega."),
    ]
    for g in genericos:
        if len(casos) >= 4:
            break
        casos.append(g)

    # ── preguntas frecuentes propias ──
    faqs = []
    if pueblos:
        faqs.append((f"¿Atiendes también {_lista(pueblos[:3])}?",
                     f"Sí. Trabajo con clientes de toda la provincia de {prov}, no solo de la capital. La forma de trabajar es la misma: "
                     f"consulta gratuita a distancia, recepción de la prueba con cadena de custodia y desplazamiento cuando hace falta."))
    if lengua:
        lg = lengua.split(" (")[0]
        faqs.append((f"¿Puedes analizar conversaciones en {lg}?",
                     f"Sí. La autenticidad de un chat o de un correo se demuestra con su estructura técnica, que es igual en cualquier idioma. "
                     f"El informe se redacta en castellano y, si hay que citar mensajes en {lg}, se indica el idioma y se valora con tu abogado "
                     f"si el procedimiento requiere traducción."))
    if x.get("canarias"):
        faqs.append(("¿La diferencia horaria de Canarias afecta a la prueba?",
                     "Puede afectar. WhatsApp muestra las horas según la zona horaria del teléfono que las enseña, así que un mismo mensaje "
                     "puede aparecer con una hora en Canarias y otra en la península. En el informe se indica la zona horaria de cada registro."))
    if fr in ("Portugal", "Francia", "Francia y Andorra", "Marruecos"):
        if fr == "Marruecos":
            resp = ("Los datos que guarda un operador marroquí solo se pueden pedir a través del juzgado, por vía de cooperación "
                    "internacional, y suele tardar. Por eso conviene asegurar antes todo lo que esté en tu propio teléfono.")
        else:
            resp = ("Los datos que guarda un operador extranjero solo se pueden pedir a través del juzgado, mediante cooperación "
                    "judicial internacional (dentro de la UE, por ejemplo, con una orden europea de investigación en lo penal). "
                    "Por eso conviene asegurar antes todo lo que esté en tu propio teléfono.")
        faqs.append((f"¿Y si la otra parte usa una línea de {fr.split(' y ')[0]}?", resp))
    if x.get("ave"):
        faqs.append((f"¿Cuánto tardas en venir a {n}?",
                     f"Con el tren de alta velocidad desde Madrid puedo estar en {n} en el día. La fecha se fija contigo y, si hay juicio, "
                     f"con la citación; el coste del viaje va en el presupuesto desde el principio."))

    # ── artículo relacionado ──
    if fr or x.get("canarias"):
        enlace = ("/articulos/primeras-horas-conservar-prueba-digital/", "Qué hacer en las primeras horas para no perder una prueba digital →")
    elif lengua:
        enlace = ("/articulos/pantallazos-whatsapp-prueba-juicio/", "Cuándo valen los pantallazos de WhatsApp como prueba →")
    else:
        enlace = ("/articulos/fraude-factura-cambio-cuenta-bancaria/", "Qué hacer si te llega una factura con otra cuenta bancaria →")

    titulo = f"Peritaje informático en {n} y su provincia" if pueblos else f"Peritaje informático en {n}"
    eyebrow = f"{n} y provincia" if pueblos else n
    return {
        "juzgado": juz,
        "faqs": faqs,
        "eyebrow": eyebrow,
        "titulo": titulo,
        "lead": lead,
        "lead_html": f"{ambito.replace(_lista(pueblos), pueblos_html) if pueblos else ambito} {viaje}",
        "casos": casos,
        "enlace": enlace,
    }

"""
Fuentes con las que arranca la Cablera la primera vez.
Después se editan desde la app (pestaña Fuentes): no hace falta tocar este archivo.

Campos de cada fuente:
  id         identificador corto, sin espacios
  nombre     cómo se muestra
  categoria  grupo en la pestaña Fuentes
  deporte    deporte por defecto de sus comunicados
  metodo     rss | river | web | pausada
               rss    feed RSS o Atom (url = dirección del feed)
               river  API JSON del sitio de River
               web    página de listado + lectura de cada nota (scraping)
               pausada  no se lee
  url        dirección del feed o del listado
  patron     (web) expresión regular que tienen que cumplir los links de las notas
  filtro     (opcional) expresión regular: solo entran notas cuyo título o texto la cumplan
  idioma     es | en | it | fr | pt (si no es "es", la IA traduce al redactar)
  detalle    nota para los editores
"""

# Argentinos en el exterior y Selección: para filtrar las fuentes de ligas de afuera
FILTRO_ARGENTINOS = (r"argentin|messi|scaloni|lautaro|juli[aá]n [aá]lvarez|enzo fern[aá]ndez|mac allister|"
                     r"de paul|garnacho|lisandro|cuti romero|dibu|emiliano mart[ií]nez|paredes|nico gonz[aá]lez|"
                     r"dybala|di mar[ií]a|simeone|mastantuono|echeverri|nico paz|thiago almada|soul[eé]|"
                     r"carboni|balerdi|senesi|montiel|molina|otamendi|lo celso|pochettino|inter miami")

FILTRO_TENIS = (r"argentin|cer[uú]ndolo|etcheverry|b[aá]ez|navone|comesa[ñn]a|tirante|d[ií]az acosta|burruchaga|"
                r"ugo carabelli|schwartzman|del potro|zeballos|podoroska|solana sierra|riera|carl[eé]|ger[ae]ld|coria")
FILTRO_RUGBY = r"argentin|pumas|pumitas|leoncitas|contepomi|montoya|kremer|matera|carreras|mallia"

FUENTES_BASE = [
    # ── Fútbol argentino
    dict(id="afa-noticias", nombre="AFA · Noticias", categoria="Fútbol argentino", deporte="Fútbol",
         metodo="web", url="https://www.afa.com.ar/es/posts", patron=r"/es/posts/(?!categories)[a-z0-9-]+/?$",
         detalle="Listado + nota completa. La fecha sale de la nota (dd/mm/aaaa). Verificada el 23/10."),
    dict(id="afa-selecciones", nombre="AFA · Selecciones", categoria="Fútbol argentino", deporte="Fútbol",
         metodo="web", url="https://www.afa.com.ar/es/posts/categories/selecciones", patron=r"/es/posts/(?!categories)[a-z0-9-]+/?$",
         detalle="Mayor, juveniles, femenino y argentinos en el exterior."),
    dict(id="afa-torneos", nombre="AFA · Torneos (ascenso)", categoria="Fútbol argentino", deporte="Fútbol",
         metodo="web", url="https://www.afa.com.ar/es/posts/categories/torneo", patron=r"/es/posts/(?!categories)[a-z0-9-]+/?$",
         detalle="Programación, resultados y comunicados del ascenso."),
    dict(id="afa-tribunal", nombre="AFA · Tribunal de Disciplina", categoria="Fútbol argentino", deporte="Fútbol",
         metodo="web", url="https://www.afa.com.ar/es/boletins/tribunal-de-disciplina?s=10", patron=r"assets1\.afa\.com\.ar/.*boletin.*\.pdf",
         detalle="Boletines en PDF (sanciones). Se extrae el texto del PDF; revisar siempre. Verificada el 23/10."),
    dict(id="lpf", nombre="Liga Profesional (LPF)", categoria="Fútbol argentino", deporte="Fútbol",
         metodo="rss", url="https://www.ligaprofesional.ar/feed/",
         detalle="Feed con texto completo: programación, árbitros, conferencias, juveniles."),
    # ── Clubes
    dict(id="boca", nombre="Boca Juniors", categoria="Clubes", deporte="Fútbol",
         metodo="web", url="https://www.bocajuniors.com.ar/noticias", patron=r"/noticias/[a-z0-9-]+/?$",
         detalle="La fecha sale del listado (en inglés: October 23, 2026). Verificada el 23/10."),
    dict(id="river", nombre="River Plate", categoria="Clubes", deporte="Fútbol",
         metodo="river", url="https://www.riverplate.com/api/v1/news/published?context=general&limit=15",
         detalle="API del sitio: título, fecha y texto. El link es el corto oficial (riverplate.com/n/…). Verificada el 23/10."),
    dict(id="racing", nombre="Racing Club", categoria="Clubes", deporte="Fútbol",
         metodo="rss", url="https://www.racingclub.com.ar/rss/",
         detalle="Feed oficial: prensa, primer equipo e institucional."),
    dict(id="independiente", nombre="Independiente", categoria="Clubes", deporte="Fútbol",
         metodo="web", url="https://www.clubaindependiente.com.ar/", patron=r"/noticias/\d{10}_",
         detalle="La fecha va en la dirección de cada nota y en sus metadatos. Verificada el 23/10."),
    dict(id="sanlorenzo", nombre="San Lorenzo", categoria="Clubes", deporte="Fútbol",
         metodo="web", url="https://www.sanlorenzo.com.ar/", patron=r"/noticias/\d{10}_",
         detalle="Muchas novedades solo en video (conferencias), que no se capturan. Verificada el 23/10."),
    # ── Fútbol internacional
    dict(id="conmebol", nombre="CONMEBOL", categoria="Fútbol internacional", deporte="Fútbol",
         metodo="rss", url="https://www.conmebol.com/feed/",
         detalle="Feed sin texto completo: se lee cada nota. Verificada el 23/10."),
    dict(id="uefa", nombre="UEFA", categoria="Fútbol internacional", deporte="Fútbol", idioma="en",
         metodo="web", url="https://www.uefa.com/news-media/", patron=r"/news/[0-9a-f]{4}-",
         filtro=FILTRO_ARGENTINOS, detalle="En inglés. Solo notas con argentinos. Verificada el 23/10."),
    dict(id="fifa", nombre="FIFA", categoria="Fútbol internacional", deporte="Fútbol",
         metodo="pausada", url="https://inside.fifa.com/es/news",
         detalle="Carga el contenido con JavaScript: no se puede leer sin navegador."),
    # ── Ligas del exterior
    dict(id="premier", nombre="Premier League", categoria="Ligas del exterior", deporte="Fútbol", idioma="en",
         metodo="premier", url="https://api.premierleague.com/content/premierleague/text/en?pageSize=40&detail=DETAILED",
         filtro=FILTRO_ARGENTINOS, detalle="API de la Premier: comunicados de los clubes (link al sitio de cada club). Solo notas con argentinos. Verificada el 23/10."),
    dict(id="laliga", nombre="LaLiga", categoria="Ligas del exterior", deporte="Fútbol",
         metodo="web", url="https://www.laliga.com/noticias", patron=r"/noticias/[a-z0-9-]{12,}/?$",
         filtro=FILTRO_ARGENTINOS, detalle="Mucho institucional: solo notas con argentinos. Verificada el 23/10."),
    dict(id="seriea", nombre="Serie A", categoria="Ligas del exterior", deporte="Fútbol", idioma="it",
         metodo="web", url="https://www.legaseriea.it/it", patron=r"/serie-a/news/[a-z0-9-]{8,}",
         filtro=FILTRO_ARGENTINOS, detalle="En italiano. Solo notas con argentinos. Verificada el 23/10."),
    dict(id="mls", nombre="MLS", categoria="Ligas del exterior", deporte="Fútbol", idioma="en",
         metodo="web", url="https://www.mlssoccer.com/news/", patron=r"/news/[a-z0-9-]{12,}",
         filtro=FILTRO_ARGENTINOS, detalle="En inglés. Messi, Inter Miami y argentinos. Verificada el 23/10."),
    dict(id="bundesliga", nombre="Bundesliga", categoria="Ligas del exterior", deporte="Fútbol",
         metodo="pausada", url="https://www.bundesliga.com/es/bundesliga/noticias",
         detalle="La sección en español muestra notas de archivo."),
    dict(id="ligue1", nombre="Ligue 1", categoria="Ligas del exterior", deporte="Fútbol",
         metodo="pausada", url="https://ligue1.com/fr/news",
         detalle="Carga el contenido con JavaScript: no se puede leer sin navegador."),
    # ── Tenis
    dict(id="atp", nombre="ATP Tour", categoria="Tenis", deporte="Tenis", idioma="en",
         metodo="web", url="https://www.atptour.com/en/news", patron=r"/en/news/[a-z0-9-]{10,}",
         filtro=FILTRO_TENIS, detalle="En inglés. Solo notas con argentinos. Su feed RSS está bloqueado; puede bloquear servidores: si queda Limitada, pausala."),
    dict(id="wta", nombre="WTA", categoria="Tenis", deporte="Tenis", idioma="en",
         metodo="web", url="https://www.wtatennis.com/news", patron=r"/news/\d+/",
         filtro=FILTRO_TENIS, detalle="En inglés. Solo notas con argentinas. Verificada el 23/10."),
    dict(id="daviscup", nombre="Copa Davis", categoria="Tenis", deporte="Tenis", idioma="en",
         metodo="web", url="https://www.daviscup.com/en/news", patron=r"/en/news/(?!category)[a-z0-9-]{12,}",
         filtro=r"argentin", detalle="En inglés. El sitio arma el texto con JavaScript: se toma solo el resumen. Abrí el original."),
    dict(id="aat", nombre="Asociación Argentina de Tenis", categoria="Tenis", deporte="Tenis",
         metodo="pausada", url="https://www.aat.com.ar",
         detalle="Las noticias se cargan con JavaScript desde una API con token: no se puede leer sin navegador."),
    # ── Motor
    dict(id="f1", nombre="Fórmula 1", categoria="Motor", deporte="Automovilismo", idioma="en",
         metodo="rss", url="https://www.formula1.com/en/latest/all.xml", filtro=r"colapinto|alpine",
         detalle="Solo notas sobre Colapinto o Alpine."),
    dict(id="fia", nombre="FIA", categoria="Motor", deporte="Automovilismo", idioma="en",
         metodo="rss", url="https://www.fia.com/rss/news", filtro=r"colapinto|alpine|argentin",
         detalle="Feed oficial (comunicados, conferencias de F1). Solo Colapinto, Alpine o argentinos. Verificada el 23/10."),
    dict(id="actc", nombre="ACTC · Turismo Carretera", categoria="Motor", deporte="Automovilismo",
         metodo="web", url="https://actc.org.ar/tc/noticias", patron=r"/noticias/[a-z0-9-]{8,}",
         detalle="La fecha sale del listado (dd/mm/aaaa). Verificada el 23/10."),
    # ── Rugby
    dict(id="uar", nombre="UAR", categoria="Rugby", deporte="Rugby",
         metodo="rss", url="https://uar.com.ar/feed/", detalle="Feed con texto completo."),
    dict(id="worldrugby", nombre="World Rugby", categoria="Rugby", deporte="Rugby",
         metodo="web", url="https://www.world.rugby/news", patron=r"/news/\d{6,}/",
         filtro=FILTRO_RUGBY, detalle="Responde en español. Solo notas con Pumas o argentinos. La fecha es la de última actualización. Verificada el 23/10."),
    dict(id="sra", nombre="Super Rugby Americas", categoria="Rugby", deporte="Rugby",
         metodo="pausada", url="https://www.superrugbyamericas.com/noticias-10",
         detalle="Las noticias se cargan con JavaScript: no se puede leer sin navegador."),
    # ── Básquet, vóley, hockey y olímpicos
    dict(id="liganacional", nombre="Liga Nacional de Básquet", categoria="Básquet", deporte="Básquet",
         metodo="web", url="https://www.laliganacional.com.ar/laliga/", patron=r"/noticia/\d+/",
         detalle="Liga Nacional, Liga Argentina y Liga Femenina. Verificada el 23/10."),
    dict(id="fiba", nombre="FIBA", categoria="Básquet", deporte="Básquet",
         metodo="web", url="https://www.fiba.basketball/es/news", patron=r"/news/[a-z0-9-]{10,}",
         filtro=r"argentin", detalle="En español. Solo notas con Argentina. Verificada el 23/10."),
    dict(id="cabb", nombre="CABB", categoria="Básquet", deporte="Básquet",
         metodo="web", url="https://www.cabb.com.ar/", patron="",
         detalle="Caído el 21/10 y el 23/10 (error 526 de certificado)."),
    dict(id="feva", nombre="FeVA · Vóley", categoria="Vóley y hockey", deporte="Vóley",
         metodo="rss", url="https://feva.org.ar/feed", detalle="Feed oficial (WordPress). Verificada el 23/10."),
    dict(id="cah", nombre="CAH · Hockey", categoria="Vóley y hockey", deporte="Hockey",
         metodo="web", url="https://www.cahockey.org.ar/", patron=r"/noticia/[^/]+/\d+",
         detalle="Leonas, Leones y torneos. La fecha sale del listado. Verificada el 23/10."),
    dict(id="coa", nombre="Comité Olímpico Argentino", categoria="Olímpicos", deporte="Polideportivo",
         metodo="web", url="https://www.coarg.org.ar/", patron=r"/item/\d+-",
         detalle="Todos los deportes olímpicos. Verificada el 23/10."),
]

for i, f in enumerate(FUENTES_BASE):
    f.setdefault("patron", "")
    f.setdefault("filtro", "")
    f.setdefault("idioma", "es")
    f.setdefault("orden", (i + 1) * 10)

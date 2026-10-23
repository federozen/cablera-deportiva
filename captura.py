"""
Captura de comunicados oficiales: RSS, la API de River y scraping de sitios web.
No usa IA: trae título, fecha, texto y link, y ordena por prioridad con reglas.
"""
import hashlib
import io
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from urllib.parse import urljoin, urlparse, urlunparse

import feedparser
import requests
from bs4 import BeautifulSoup

ART = timezone(timedelta(hours=-3))
MAX_HORAS = 72            # solo entran comunicados publicados en las últimas 72 horas
MAX_POR_FUENTE = 25       # notas nuevas que se leen por fuente y por corrida
SIN_FECHA_PRIMERA_VEZ = 6 # la primera vez que se lee una fuente, cuántas notas sin fecha entran
TIMEOUT = 20
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/rss+xml,*/*;q=0.8",
    "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
}


def ahora() -> datetime:
    return datetime.now(ART)


def iso(dt) -> str:
    return dt.astimezone(ART).isoformat(timespec="seconds") if dt else ""


# ─────────────────────────── fechas ───────────────────────────
MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
         "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
         "january": 1, "february": 2, "march": 3, "april": 4, "june": 6, "july": 7, "august": 8,
         "september": 9, "october": 10, "november": 11, "december": 12,
         "gennaio": 1, "febbraio": 2, "aprile": 4, "maggio": 5, "giugno": 6, "luglio": 7,
         "settembre": 9, "ottobre": 10, "dicembre": 12}
# Abreviaturas ("22 oct 2026", "Oct 23, 2026")
MESES.update({"ene": 1, "jan": 1, "feb": 2, "mar": 3, "abr": 4, "apr": 4, "jun": 6, "jul": 7, "ago": 8, "aug": 8,
              "sep": 9, "sept": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12, "dec": 12})
_MES_RE = "|".join(sorted(MESES, key=len, reverse=True))
RE_ISO = re.compile(r"(20\d\d)-(\d\d)-(\d\d)[T ](\d\d):(\d\d)(?::(\d\d))?(?:\.\d+)?(Z|[+-]\d\d:?\d\d)?")
RE_ES = re.compile(rf"\b(\d{{1,2}})\s+(?:de\s+)?({_MES_RE})(?![a-z])\.?,?\s+(?:de\s+|del\s+)?(20\d\d)\b", re.I)
RE_EN = re.compile(rf"\b({_MES_RE})(?![a-z])\.?\s+(\d{{1,2}}),?\s+(20\d\d)\b", re.I)
RE_DMY = re.compile(r"\b(\d{1,2})[/.](\d{1,2})[/.](20\d\d)\b")
RE_EPOCH = re.compile(r"/(1[6-9]\d{8})_")


def parse_fecha(t):
    """Primera fecha completa (con año) que aparezca en el texto. Devuelve datetime con zona o None."""
    if not t:
        return None
    t = str(t)
    m = RE_ISO.search(t)
    if m:
        y, mo, d, h, mi, s, tz = m.groups()
        try:
            dt = datetime(int(y), int(mo), int(d), int(h), int(mi), int(s or 0))
        except ValueError:
            return None
        if tz in (None, ""):
            return dt.replace(tzinfo=ART)
        if tz == "Z":
            return dt.replace(tzinfo=timezone.utc)
        tz = tz.replace(":", "")
        off = timedelta(hours=int(tz[1:3]), minutes=int(tz[3:5])) * (1 if tz[0] == "+" else -1)
        return dt.replace(tzinfo=timezone(off))
    try:   # RFC 822 de los RSS: "Fri, 23 Oct 2026 19:56:43 +0000"
        if re.search(r"\d{1,2} \w{3} 20\d\d \d\d:\d\d", t):
            dt = parsedate_to_datetime(t.strip())
            return dt if dt.tzinfo else dt.replace(tzinfo=ART)
    except (TypeError, ValueError):
        pass
    cands = []
    for rx, orden in ((RE_ES, "dmy"), (RE_EN, "mdy"), (RE_DMY, "dmy_num")):
        m = rx.search(t)
        if m:
            cands.append((m.start(), m, orden))
    if not cands:
        return None
    _, m, orden = min(cands, key=lambda x: x[0])
    try:
        if orden == "dmy":
            d, mo, y = int(m.group(1)), MESES[m.group(2).lower()], int(m.group(3))
        elif orden == "mdy":
            mo, d, y = MESES[m.group(1).lower()], int(m.group(2)), int(m.group(3))
        else:
            d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return datetime(y, mo, d, 12, 0, tzinfo=ART)   # sin hora: se toma el mediodía
    except (ValueError, KeyError):
        return None


_ABR = "ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|SET|OCT|NOV|DIC|JAN|APR|AUG|DEC"
# "23OCT" (en mayúsculas, puede venir pegado al título) o "22 oct" / "22 oct." (separado)
RE_CORTA = [re.compile(rf"(?<!\d)(\d{{1,2}})\s?({_ABR})(?![a-z])"),
            re.compile(rf"(?<!\d)(\d{{1,2}})\s+({_ABR.lower()})\.?(?![a-záéíóúñ])")]


def fecha_corta(t):
    """Fechas sin año de los listados ("23OCT", "22 oct"): se asume el año actual (o el anterior si quedaría en el futuro)."""
    m = RE_CORTA[0].search(t or "") or RE_CORTA[1].search(t or "")
    if not m:
        return None
    hoy = ahora()
    try:
        f = datetime(hoy.year, MESES[m.group(2).lower()], int(m.group(1)), 12, 0, tzinfo=ART)
    except (ValueError, KeyError):
        return None
    if f > hoy + timedelta(days=2):
        f = f.replace(year=hoy.year - 1)
    return f


def fecha_de_url(url):
    m = RE_EPOCH.search(url or "")
    if m:
        return datetime.fromtimestamp(int(m.group(1)), tz=timezone.utc)
    return None


# ─────────────────────────── red ───────────────────────────
def obtener(url, timeout=TIMEOUT):
    r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    r.raise_for_status()
    ct = r.headers.get("content-type", "").lower()
    if "charset=" not in ct and ("html" in ct or "xml" in ct or not ct):
        r.encoding = r.apparent_encoding or "utf-8"
    return r


def normalizar_url(u):
    p = urlparse(u)
    q = "&".join(x for x in p.query.split("&") if x and not x.startswith(("utm_", "fbclid", "gclid")))
    return urlunparse((p.scheme, p.netloc.lower().replace("www.", ""), p.path.rstrip("/") or "/", "", q, ""))


def id_de_url(fuente_id, url):
    return f"{fuente_id}-{hashlib.sha1(normalizar_url(url).encode()).hexdigest()[:8]}"


# ─────────────────────────── texto de una página ───────────────────────────
_BASURA = ["script", "style", "nav", "header", "footer", "aside", "form", "noscript", "iframe", "button", "svg", "figure"]


def limpiar(t):
    t = unescape(t or "").replace("\xa0", " ")
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def html_a_texto(html):
    """Texto de un fragmento HTML, con un párrafo por bloque."""
    if not html:
        return ""
    s = BeautifulSoup(html, "lxml")
    for x in s(_BASURA):
        x.decompose()
    partes = []
    for el in s.find_all(["p", "h2", "h3", "h4", "li", "blockquote"]):
        if el.find_parent(["p", "li", "blockquote"]):
            continue
        tx = limpiar(el.get_text("\n"))
        if tx:
            partes.append(("**" + tx + "**") if el.name in ("h2", "h3", "h4") and len(tx) < 120 else tx)
    if not partes:
        return limpiar(s.get_text("\n"))
    return "\n\n".join(partes)


def cuerpo_principal(soup):
    """El contenedor con más texto en párrafos directos (sirve para casi cualquier sitio)."""
    mejor, puntos = None, 0
    for el in soup.find_all(["article", "main", "section", "div"]):
        hijos = el.find_all(["p", "h2", "h3", "li", "blockquote"], recursive=False)
        tot = sum(len(h.get_text(" ", strip=True)) for h in hijos if h.name == "p")
        if tot > puntos:
            mejor, puntos = el, tot
    ps = [p for p in soup.find_all("p") if len(p.get_text(" ", strip=True)) > 40]
    total = sum(len(p.get_text(" ", strip=True)) for p in ps)
    if not mejor or puntos < 150 or puntos < total * 0.5:
        # El texto está repartido en varios bloques (MLS, ACTC): se toman todos los párrafos largos
        return "\n\n".join(limpiar(p.get_text("\n")) for p in ps)
    partes = []
    for h in mejor.find_all(["p", "h2", "h3", "li", "blockquote"], recursive=False):
        tx = limpiar(h.get_text("\n"))
        if not tx:
            continue
        partes.append(("**" + tx + "**") if h.name in ("h2", "h3") and len(tx) < 120 else tx)
    return "\n\n".join(partes)


def _meta(soup, *nombres):
    for n in nombres:
        el = soup.find("meta", attrs={"property": n}) or soup.find("meta", attrs={"name": n}) or soup.find("meta", attrs={"itemprop": n})
        if el and el.get("content"):
            return el["content"].strip()
    return ""


def _fecha_jsonld(soup):
    for s in soup.find_all("script", type="application/ld+json"):
        m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', s.string or s.get_text() or "")
        if m:
            f = parse_fecha(m.group(1))
            if f:
                return f
    return None


def limpiar_titulo(t, nombre_sitio=""):
    t = limpiar(t).replace("\n", " ")
    if " | " in t:
        t = max(t.split(" | "), key=len).strip()
    return t[:220]


def leer_articulo(url):
    """Lee una nota: título, fecha y texto. Si es un PDF, extrae el texto del PDF."""
    r = obtener(url)
    ct = r.headers.get("content-type", "").lower()
    if url.lower().split("?")[0].endswith(".pdf") or "pdf" in ct:
        return leer_pdf(r.content)
    soup = BeautifulSoup(r.text, "lxml")
    fecha = (parse_fecha(_meta(soup, "article:published_time", "datePublished", "og:published_time",
                               "publish-date", "pubdate", "date", "dc.date"))
             or _fecha_jsonld(soup))
    if not fecha:
        t = soup.find("time", attrs={"datetime": True})
        fecha = parse_fecha(t["datetime"]) if t else None
    h1 = soup.find("h1")
    titulo, fuerte = "", True
    if h1 and len(h1.get_text(strip=True)) > 10:
        titulo = h1.get_text(" ", strip=True)
    else:
        titulo = _meta(soup, "og:title", "twitter:title")
    if not titulo:   # solo el <title> de la página: suele ser el nombre del sitio
        titulo, fuerte = (soup.title.string if soup.title and soup.title.string else ""), False
    descripcion = _meta(soup, "og:description", "description", "twitter:description")
    for x in soup(_BASURA):
        x.decompose()
    texto = cuerpo_principal(soup)
    if len(texto) < 150 and len(descripcion) > len(texto):
        texto = limpiar(descripcion)   # sitios que arman la nota con JavaScript: queda al menos el resumen
    if not fecha:
        # Último recurso: la primera fecha completa (con año) de la página, cerca del título
        zona = soup.find("article") or soup.body or soup
        fecha_txt = parse_fecha(zona.get_text(" ", strip=True)[:4000])
        if fecha_txt and fecha_txt < ahora() - timedelta(days=30):
            fecha_txt = None   # una fecha vieja en el texto suele ser de otra cosa (pie de página, historia): mejor sin fecha
        return {"titulo": limpiar_titulo(titulo), "titulo_fuerte": fuerte, "fecha": fecha_txt, "fecha_debil": bool(fecha_txt), "texto": texto[:15000]}
    return {"titulo": limpiar_titulo(titulo), "titulo_fuerte": fuerte, "fecha": fecha, "fecha_debil": False, "texto": texto[:15000]}


def leer_pdf(contenido):
    try:
        from pypdf import PdfReader
        rd = PdfReader(io.BytesIO(contenido))
        texto = "\n\n".join((p.extract_text() or "") for p in rd.pages[:6])
    except Exception as e:  # PDF escaneado o roto
        return {"titulo": "", "fecha": None, "fecha_debil": False, "texto": "", "error": f"PDF ilegible ({str(e)[:60]})"}
    texto = limpiar(texto)
    return {"titulo": "", "fecha": parse_fecha(texto[:3000]), "fecha_debil": True, "texto": texto[:15000]}


# ─────────────────────────── lectores por método ───────────────────────────
def leer_rss(fuente):
    r = obtener(fuente["url"])
    feed = feedparser.parse(r.content)
    if not feed.entries:
        raise RuntimeError("el feed no trajo notas")
    out = []
    for e in feed.entries[:30]:
        link = e.get("link") or ""
        if not link:
            continue
        html = ""
        if e.get("content"):
            html = e["content"][0].get("value", "")
        texto = html_a_texto(html) if html else ""
        fecha = None
        for k in ("published", "updated", "dc_date"):
            if e.get(k):
                fecha = parse_fecha(e[k])
                if fecha:
                    break
        out.append({"url": link, "titulo": limpiar(e.get("title", "")), "fecha": fecha,
                    "texto": texto, "resumen": html_a_texto(e.get("summary", ""))[:600]})
    return out


def _texto_river(content_json):
    try:
        nodos = json.loads(content_json) if isinstance(content_json, str) else (content_json or {})
    except json.JSONDecodeError:
        return ""
    partes, vistos = [], set()

    def rec(nid):
        if nid in vistos or nid not in nodos:
            return
        vistos.add(nid)
        n = nodos[nid]
        txt = (n.get("props") or {}).get("text")
        if isinstance(txt, str) and txt.strip():
            partes.append(html_a_texto(txt) if "<" in txt else limpiar(txt))
        for h in n.get("nodes", []) or []:
            rec(h)
        for h in (n.get("linkedNodes") or {}).values():
            rec(h)
    rec("ROOT")
    return "\n\n".join(p for p in partes if p)


def leer_river(fuente):
    base = "https://www.riverplate.com"
    j = obtener(fuente["url"]).json()
    out = []
    for n in (j.get("data") or [])[:20]:
        slug = n.get("slug")
        if not slug:
            continue
        link = ((n.get("shortUrls") or {}).get("default")) or f"{base}/noticias/{slug}"
        out.append({"url": link, "titulo": limpiar(n.get("title", "")),
                    "fecha": parse_fecha(n.get("publicationDate")), "texto": "", "slug": slug,
                    "resumen": limpiar(n.get("summary", ""))})
    return out


def detalle_river(slug):
    j = obtener(f"https://www.riverplate.com/api/v1/news/{slug}").json()
    d = j.get("data") or {}
    texto = _texto_river(d.get("contentJson"))
    if not texto and d.get("summary"):
        texto = limpiar(d["summary"])
    return {"titulo": limpiar(d.get("title", "")), "fecha": parse_fecha(d.get("publicationDate")), "texto": texto[:15000]}


def leer_premier(fuente):
    """API de contenidos de la Premier League: reúne los comunicados de los clubes (con link al sitio del club)."""
    j = obtener(fuente["url"]).json()
    out = []
    for c in (j.get("content") or [])[:60]:
        link = c.get("hotlinkUrl") or (f"https://www.premierleague.com/en/news/{c.get('id')}/{c.get('titleUrlSegment', '')}" if c.get("id") else "")
        if not link:
            continue
        ms = c.get("publishFrom") or c.get("date")
        fecha = datetime.fromtimestamp(ms / 1000, tz=timezone.utc) if isinstance(ms, (int, float)) else parse_fecha(ms)
        resumen = limpiar(c.get("summary") or c.get("description") or "")
        out.append({"url": link, "titulo": limpiar(c.get("title", "")), "fecha": fecha,
                    "texto": html_a_texto(c.get("body") or ""), "resumen": resumen})
    return out


def leer_wp(fuente):
    """API de WordPress (/wp-json/wp/v2/posts): sitios que arman la página con JavaScript pero publican en WordPress.
    Si la fuente tiene "enlace" (ej. https://cahuracan.com/noticias/{slug}), se usa para el link público."""
    j = obtener(fuente["url"]).json()
    out = []
    for p in j[:30] if isinstance(j, list) else []:
        link = p.get("link") or ""
        if fuente.get("enlace") and p.get("slug"):
            link = fuente["enlace"].replace("{slug}", p["slug"])
        titulo = limpiar(BeautifulSoup((p.get("title") or {}).get("rendered", ""), "lxml").get_text(" "))
        cont = (p.get("content") or {}).get("rendered", "") or (p.get("excerpt") or {}).get("rendered", "")
        out.append({"url": link, "titulo": titulo, "fecha": parse_fecha(p.get("date")),
                    "texto": html_a_texto(cont)})
    return out


def _titulo_pdf(href, texto_a, fuente):
    if len(texto_a) >= 15 and not re.search(r"descarg|download", texto_a, re.I):
        return texto_a
    nombre = urlparse(href).path.rsplit("/", 1)[-1]
    nombre = re.sub(r"\.(docx?|pdf)", "", nombre, flags=re.I)
    nombre = re.sub(r"\(\d+\)", "", nombre)
    nombre = re.sub(r"[-_]+", " ", nombre).strip()
    return f"{fuente.get('nombre', '')}: {nombre}"


def leer_web(fuente):
    """Página de listado: links a notas (según el patrón) con el título y la fecha que muestre el listado."""
    url = fuente["url"]
    r = obtener(url)
    soup = BeautifulSoup(r.text, "lxml")
    patron = (fuente.get("patron") or "").strip()
    host = urlparse(r.url).netloc.replace("www.", "")
    if not patron:
        # Sin patrón: si el sitio tiene feed RSS, se usa el feed
        alt = soup.find("link", attrs={"type": re.compile("rss|atom")})
        if alt and alt.get("href"):
            return leer_rss({**fuente, "url": urljoin(r.url, alt["href"])})
    rx = re.compile(patron, re.I) if patron else None
    out, vistos = [], {}
    for a in soup.find_all("a", href=True):
        href = urljoin(r.url, a["href"].strip())
        if href.startswith(("mailto:", "javascript:")):
            continue
        if urlparse(href).netloc.replace("www.", "") != host and not href.lower().endswith(".pdf"):
            continue
        texto_a = limpiar(a.get_text(" ")).replace("\n", " ")
        if rx:
            if not rx.search(href):
                continue
        elif len(texto_a) < 25 or urlparse(href).path.count("/") < 2:
            continue
        clave = normalizar_url(href)
        if clave == normalizar_url(r.url):
            continue
        if clave in vistos:
            # El mismo link aparece varias veces (foto, título, "Leer más"): se queda el texto más largo
            previo = vistos[clave]
            t2 = re.sub(r"(leer m[aá]s|ver m[aá]s|read more)\s*$", "", texto_a, flags=re.I).strip()
            if len(t2) > len(previo["titulo"]) and not href.lower().split("?")[0].endswith(".pdf"):
                previo["titulo"] = t2
            if not previo["fecha"]:
                previo["fecha"] = parse_fecha(texto_a) or fecha_corta(texto_a)
            continue
        # Fecha visible en el listado: en el link o en su tarjeta
        fecha = parse_fecha(texto_a)
        if not fecha and a.parent is not None:
            t = a.parent.get_text(" ", strip=True)
            if len(t) < 400:
                fecha = parse_fecha(t)
        fecha = fecha_de_url(href) or fecha or fecha_corta(texto_a)
        titulo = re.sub(r"(leer m[aá]s|ver m[aá]s|read more)\s*$", "", texto_a, flags=re.I).strip()
        if href.lower().split("?")[0].endswith(".pdf"):
            titulo = _titulo_pdf(href, titulo, fuente)
        item = {"url": href, "titulo": titulo, "fecha": fecha, "texto": ""}
        vistos[clave] = item
        out.append(item)
        if len(out) >= 40:
            break
    if not out:
        raise RuntimeError("no se encontraron links a notas (¿cambió el sitio o el patrón?)")
    return out


LECTORES = {"rss": leer_rss, "river": leer_river, "web": leer_web, "premier": leer_premier, "wp": leer_wp}


# ─────────────────────────── clasificación (sin IA) ───────────────────────────
# Si el TÍTULO tiene alguna de estas, va con prioridad alta
ALTA = [r"selecci[oó]n (argentina|mayor)|la selecci[oó]n|\bscaloni", r"\bmessi\b", r"\bboca\b", r"\briver\b",
        r"\bracing\b", r"\bindependiente\b", r"san lorenzo", r"\bpumas\b|\bleonas\b|\bleones\b|\bpanteras\b", r"renunci", r"sanci[oó]n|sancionad|suspendid|suspensi[oó]n|tribunal de disciplina",
        r"lesi[oó]n|desgarro|rotura|ligamento|parte m[eé]dico|operad", r"\bfinal(es)?\b", r"convocad", r"colapinto",
        r"nuevo (dt|entrenador|t[eé]cnico)"]
# Si el texto tiene alguna de estas, va con prioridad media
MEDIA = ALTA + [r"tribunal", r"\bdt\b|entrenador|t[eé]cnico", r"argentin", r"programaci[oó]n|fixture", r"[aá]rbitro"]
DESCARTE = [(r"venta de entradas|entradas (para|ante|disponibles)|sac[aá] tu entrada|abono|ticket", "venta de entradas"),
            (r"asociate|hacete socio|cuota social|beneficio|descuento|sorteo", "socios y beneficios"),
            (r"sponsor|patrocin|alianza estrat[eé]gica|renuevan su alianza|nuevo acuerdo comercial|partner", "sponsors"),
            (r"merchandising|tienda oficial|indumentaria|nueva camiseta|camiseta alternativa", "merchandising"),
            (r"efem[eé]ride|un d[ií]a como hoy|cumplea[ñn]os|aniversario", "efemérides"),
            (r"\bvisitas guiadas|museo|colonia de vacaciones", "institucional menor")]
DEPORTES = [("Básquet", r"b[aá]squet|basket|\bnba\b|liga nacional"), ("Rugby", r"rugby|pumas|\buar\b"),
            ("Hockey", r"hockey|leonas"), ("Tenis", r"tenis|atp|wta"), ("Futsal", r"futsal|f[uú]tbol de sal[oó]n"),
            ("Vóley", r"v[oó]ley"), ("Handball", r"handball|balonmano"), ("Atletismo", r"atletismo"),
            ("Natación", r"nataci[oó]n"), ("Automovilismo", r"f[oó]rmula 1|\bf1\b|colapinto|turismo carretera|\btc\b")]


def clasificar(it, fuente):
    base = f"{it.get('titulo', '')} {it.get('texto', '')[:1500]}".lower()
    titulo = (it.get("titulo") or "").lower()
    for rx, motivo in DESCARTE:
        if re.search(rx, titulo):
            return "baja", f"Descarte automático: {motivo}", True
    if any(re.search(rx, titulo) for rx in ALTA):
        prio = "alta"
    elif any(re.search(rx, base) for rx in MEDIA):
        prio = "media"
    else:
        prio = "baja"
    return prio, "", False


def deporte_de(it, fuente):
    base = f"{it.get('titulo', '')} {it.get('texto', '')[:800]}".lower()
    dep = fuente.get("deporte") or "Fútbol"
    if fuente.get("categoria") in ("Clubes",):   # los clubes publican de muchos deportes
        for nombre, rx in DEPORTES:
            if re.search(rx, base[:300]):
                return nombre
    return dep


# ─────────────────────────── una fuente ───────────────────────────
def capturar_fuente(fuente, vistos: dict, prueba=False, limite=MAX_POR_FUENTE):
    """Lee una fuente y devuelve (items_nuevos, urls_vistas_nuevas, resumen).
    vistos: {url_normalizada: {...}} de corridas anteriores.
    prueba=True: no filtra por vistos ni por fecha (para el botón Probar)."""
    t0 = time.time()
    met = fuente.get("metodo")
    if met not in LECTORES:
        return [], {}, {"ok": True, "salteada": True, "mensaje": "pausada"}
    candidatos = LECTORES[met](fuente)
    ya_leida = any(v.get("f") == fuente["id"] for v in vistos.values())
    filtro = re.compile(fuente["filtro"], re.I) if fuente.get("filtro") else None
    if filtro and not prueba:
        limite = max(limite, 35)   # con filtro se descartan muchas: se leen más por corrida
    limite_tiempo = ahora() - timedelta(hours=MAX_HORAS)

    nuevos_vistos, pendientes = {}, []
    for c in candidatos:
        k = normalizar_url(c["url"])
        if not prueba and k in vistos:
            continue
        if not prueba and c.get("fecha") and c["fecha"] < limite_tiempo:
            nuevos_vistos[k] = {"f": fuente["id"], "t": iso(ahora()), "x": "vieja"}
            continue
        pendientes.append(c)
        if len(pendientes) >= limite:
            break

    def completar(c):
        try:
            if met == "river":
                d = detalle_river(c["slug"])
            elif len(c.get("texto") or "") >= 400:
                return c
            else:
                d = leer_articulo(c["url"])
            if d.get("error"):
                c["error"] = d["error"]
            c["texto"] = d.get("texto") or c.get("texto") or c.get("resumen", "")
            es_pdf = c["url"].lower().split("?")[0].endswith(".pdf")
            if d.get("titulo") and not es_pdf and (len(c.get("titulo") or "") < 12 or (met == "web" and d.get("titulo_fuerte", True))):
                c["titulo"] = d["titulo"]
            if not c.get("fecha") and d.get("fecha"):
                c["fecha"], c["fecha_debil"] = d["fecha"], d.get("fecha_debil", False)
        except Exception as e:
            c["texto"] = c.get("texto") or c.get("resumen", "")
            if len(c["texto"]) < 150:   # si el feed ya trajo el texto, no hace falta avisar
                c["error"] = f"no se pudo leer la nota ({str(e)[:80]})"
        return c

    with ThreadPoolExecutor(max_workers=6) as ex:
        completos = list(ex.map(completar, pendientes))

    items, sin_fecha, errores = [], 0, 0
    for c in completos:
        k = normalizar_url(c["url"])
        if c.get("error") and not c.get("texto"):
            errores += 1
            continue  # no se marca como vista: se reintenta en la próxima corrida
        nuevos_vistos[k] = {"f": fuente["id"], "t": iso(ahora())}
        if not c.get("titulo"):
            continue
        if filtro and not filtro.search(f"{c['titulo']} {c.get('texto', '')}"):
            nuevos_vistos[k]["x"] = "filtro"
            continue
        if not prueba and c.get("fecha") and c["fecha"] < limite_tiempo:
            nuevos_vistos[k]["x"] = "vieja"
            continue
        alertas = []
        if not c.get("fecha"):
            sin_fecha += 1
            if not prueba and not ya_leida and sin_fecha > SIN_FECHA_PRIMERA_VEZ:
                continue
            alertas.append("La fuente no muestra fecha de publicación: chequeá que sea nuevo.")
        elif c.get("fecha_debil"):
            alertas.append("Fecha tomada del texto de la página: confirmala.")
        if c.get("error"):
            alertas.append(c["error"])
        if len(c.get("texto") or "") < 200:
            alertas.append("Se pudo leer poco texto: abrí el original.")
        prio, motivo, descartar = clasificar(c, fuente)
        items.append({
            "id": id_de_url(fuente["id"], c["url"]),
            "fuente_id": fuente["id"], "fuente": fuente["nombre"], "categoria": fuente.get("categoria", ""),
            "url": c["url"], "titulo_original": c["titulo"], "texto": c.get("texto", ""),
            "publicado": iso(c.get("fecha")), "capturado": iso(ahora()),
            "deporte": deporte_de(c, fuente), "idioma": fuente.get("idioma", "es"),
            "prioridad": prio, "estado": "descartada" if descartar else "nueva",
            "motivo": motivo, "aviso": " ".join(alertas), "origen": met, "nota": None,
        })
    resumen = {"ok": True, "encontradas": len(candidatos), "nuevas": len(items), "errores": errores,
               "segundos": round(time.time() - t0, 1)}
    return items, nuevos_vistos, resumen

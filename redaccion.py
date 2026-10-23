"""
Redacción con IA, solo cuando el editor la pide (botón ✦ Redactar nota).
Usa ia_motores: los gratuitos primero y Claude de respaldo.
"""
import json
import re

import ia_motores

IDIOMAS = {"en": "inglés", "it": "italiano", "fr": "francés", "pt": "portugués", "de": "alemán"}

SISTEMA = """Sos redactor de la sección deportes de Olé (Argentina). Recibís material de sitios oficiales (clubes, federaciones, ligas) y escribís una NOTA NUEVA PARA OLÉ. Tu trabajo no es copiar, resumir ni corregir el texto original: es contarlo de nuevo, como periodista de Olé, con tus palabras.

PASO 1 · Clasificá el material:
- "comunicado": la institución anuncia o informa algo propio (decisión, sanción, parte médico, convocatoria, designación de árbitros, programación, venta de entradas, elecciones, acuerdo, repudio, comunicado oficial, declaración institucional). Suele estar escrito en primera persona de la institución ("el Club informa", "nuestro equipo", "comunicamos").
- "nota": el sitio oficial ya publicó una nota periodística (crónica de un partido, previa, entrevista, nota de color, historia).

PASO 2 · Escribí según el tipo:
- Si es "comunicado": nota periodística en tercera persona y en forma INDIRECTA, atribuyendo siempre a la fuente: "Boca informó a través de un comunicado que…", "según comunicó la AFA…", "en el parte médico difundido por el club…", "la Liga Profesional dio a conocer…". Nunca en primera persona de la institución ni con su tono celebratorio. Las frases textuales del comunicado que valga la pena conservar van entre comillas y atribuidas ("…", señaló el club en el texto).
- Si es "nota": reescribila completa para Olé: título nuevo con pegada, otro arranque, lo más noticioso primero, otro orden y otras palabras. Cuando un dato o una frase salga de la fuente, atribuilo ("según publicó el sitio oficial del Pincha").

ESTILO OLÉ: titulares con pegada (pueden tener juego de palabras, nunca a costa de la precisión); lenguaje futbolero rioplatense; oraciones cortas y ritmo ágil; apodos de clubes y selecciones cuando correspondan (Xeneize, Millonario, Academia, Rojo, Ciclón, Pincha, Lobo, Granate, Taladro, Bicho, Globo, Lepra, Canalla, la Selección, Pumas, Leonas, Leones); primer párrafo con qué, quién y cuándo; sin opinión ni adjetivos de hincha.

PROHIBIDO COPIAR: no repitas oraciones del original. Fuera de las citas entre comillas, nombres propios, cifras y fechas, no uses más de seis palabras seguidas iguales a las del original. El título y la bajada tienen que ser distintos a los del original.

DATOS: usá SOLO datos del material. No agregues resultados, fechas, cifras, nombres de pila, cargos ni contexto que no figuren. Lo que falte o sea dudoso va a "alerta".
FORMATO: listas largas (convocados, fixture, ternas, programación) al final, con una etiqueta en negrita tipo **Los convocados:** y un ítem por línea. Horarios con punto (17.10) y en hora argentina si la fuente la da. Si el material está en otro idioma, escribí en español rioplatense y aclaralo en "alerta".
Respondé SOLO con un objeto JSON válido, sin texto antes ni después."""

FORMATO = """Devolvé este JSON:
{"tipo": "comunicado" o "nota",
 "titulo": string (máx. 110 caracteres, distinto del original),
 "titulos_alternativos": [string, string],
 "bajada": string (1-2 oraciones),
 "cuerpo": string (3 a 6 párrafos separados por una línea en blanco),
 "competencia": string,
 "etiquetas": [string] (equipos, personas, torneos; máx. 8),
 "alerta": string (qué tiene que chequear el editor; "" si no hay nada)}"""

MODOS = {
    "auto": "",
    "comunicado": "El editor indica que es un COMUNICADO: escribí la nota en forma indirecta, citando a la fuente.",
    "nota": "El editor indica que es una NOTA del sitio: reescribila completa para Olé, con otro enfoque y otras palabras.",
}


def _palabras(t):
    t = re.sub(r"[\"“”«»][^\"“”«»]{0,400}[\"“”«»]", " ", t or "")   # las citas no cuentan
    return re.findall(r"[a-záéíóúüñ0-9]+", t.lower())


def copiado(original: str, nuevo: str, n: int = 7) -> float:
    """Qué parte de las secuencias de n palabras del texto nuevo aparecen tal cual en el original (0 a 1)."""
    a, b = _palabras(original), _palabras(nuevo)
    if len(b) < n:
        return 0.0
    orig = {tuple(a[i:i + n]) for i in range(len(a) - n + 1)}
    nuevas = [tuple(b[i:i + n]) for i in range(len(b) - n + 1)]
    return sum(1 for x in nuevas if x in orig) / len(nuevas)


def _extraer_json(t):
    t = t.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        pass
    i, j = t.find("{"), t.rfind("}")
    if i >= 0 and j > i:
        try:
            return json.loads(t[i:j + 1])
        except json.JSONDecodeError:
            pass
    raise ValueError("La IA no devolvió el formato esperado. Probá de nuevo o con otro motor.")


def traducir_titulos(titulos: list) -> list:
    """Traduce al español una lista de títulos en un solo pedido barato (modelo rápido, gratuitos primero).
    Devuelve la lista traducida en el mismo orden; si algo falla, levanta una excepción."""
    if not titulos:
        return []
    numerados = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(titulos))
    prompt = ("Traducí al español rioplatense estos títulos de noticias deportivas. Mantené nombres propios, "
              "clubes y torneos como se usan en Argentina (Champions League, Premier League, Grand Prix → Gran Premio). "
              "No agregues nada. Respondé SOLO con un array JSON de strings, en el mismo orden y con la misma cantidad.\n\n"
              + numerados)
    salida = ia_motores.generar(prompt, max_tokens=80 * len(titulos) + 200, nivel="rapido", motor="auto")
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", salida.strip())
    i, j = t.find("["), t.rfind("]")
    lista = json.loads(t[i:j + 1]) if i >= 0 and j > i else []
    if len(lista) != len(titulos):
        raise ValueError("La traducción no devolvió la misma cantidad de títulos.")
    return [str(x).strip() or o for x, o in zip(lista, titulos)]


def _pedir(prompt, motor):
    salida = ia_motores.generar(prompt, max_tokens=3000, nivel="modelo", motor=motor or "auto", system=SISTEMA)
    return _extraer_json(salida)


def redactar(item: dict, motor: str = "auto", indicaciones: str = "", modo: str = "auto") -> dict:
    texto = (item.get("texto") or "").strip()
    if len(texto) < 80:
        raise ValueError("El comunicado tiene muy poco texto para redactar una nota. Abrí el original.")
    idioma = IDIOMAS.get(item.get("idioma") or "es")
    partes = [
        f"Fuente: {item.get('fuente', '')} (sitio oficial)",
        f"Publicado: {item.get('publicado') or 'sin fecha en la fuente'}",
        f"Deporte: {item.get('deporte', '')}",
    ]
    if idioma:
        partes.append(f"Idioma del material: {idioma} (escribí en español).")
    if MODOS.get(modo):
        partes.append(MODOS[modo])
    if indicaciones:
        partes.append(f"Indicaciones del editor: {indicaciones.strip()[:500]}")
    titulo_orig = item.get("titulo_fuente") or item.get("titulo_original", "")
    base = "\n".join(partes) + f"\n\nTÍTULO ORIGINAL: {titulo_orig}\n\nMATERIAL ORIGINAL:\n\"\"\"\n{texto[:12000]}\n\"\"\"\n\n{FORMATO}"

    d = _pedir(base, motor)
    cuerpo = str(d.get("cuerpo") or "").strip()
    titulo = str(d.get("titulo") or "").strip()
    pct = copiado(texto, cuerpo)
    mismo_titulo = titulo.strip(" .").lower() == titulo_orig.strip(" .").lower()
    reintento = False
    if cuerpo and (pct > 0.25 or mismo_titulo):
        # Quedó demasiado parecida al original: se pide una segunda versión, más transformada
        aviso = (f"ATENCIÓN: tu versión anterior copió {round(pct * 100)}% de las frases del original"
                 + (" y repitió el título" if mismo_titulo else "") + ". Escribila de nuevo desde cero: "
                 "otro arranque, otro orden, otras palabras y forma indirecta citando a la fuente. Mismos datos.")
        try:
            d2 = _pedir(base + "\n\n" + aviso, motor)
            c2 = str(d2.get("cuerpo") or "").strip()
            if c2 and copiado(texto, c2) < pct:
                d, cuerpo, titulo, pct = d2, c2, str(d2.get("titulo") or "").strip(), copiado(texto, c2)
            reintento = True
        except (ValueError, RuntimeError):
            pass
    if not titulo or not cuerpo:
        raise ValueError("La IA devolvió una nota vacía. Probá de nuevo.")
    alerta = str(d.get("alerta") or "").strip()
    if pct > 0.25:
        alerta = (alerta + " " if alerta else "") + f"La nota todavía repite {round(pct * 100)}% de frases del original: reescribila o pedí otra versión con otro motor."
    alts = [str(x).strip() for x in (d.get("titulos_alternativos") or []) if str(x).strip()][:3]
    tipo = str(d.get("tipo") or "").strip().lower()
    return {
        "titulo": titulo[:160], "titulos_alternativos": alts, "bajada": str(d.get("bajada") or "").strip(),
        "cuerpo": cuerpo, "competencia": str(d.get("competencia") or "").strip(),
        "etiquetas": [str(x).strip() for x in (d.get("etiquetas") or []) if str(x).strip()][:10],
        "alerta": alerta, "tipo": tipo if tipo in ("comunicado", "nota") else "",
        "copiado": round(pct, 2), "reintento": reintento,
        "motor": ia_motores.ULTIMO.get("nombre", ""), "modelo": ia_motores.ULTIMO.get("modelo", ""),
    }

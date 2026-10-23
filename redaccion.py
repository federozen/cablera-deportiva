"""
Redacción con IA, solo cuando el editor la pide (botón ✦ Redactar nota).
Usa ia_motores: los gratuitos primero y Claude de respaldo.
"""
import json
import re

import ia_motores

IDIOMAS = {"en": "inglés", "it": "italiano", "fr": "francés", "pt": "portugués", "de": "alemán"}

SISTEMA = """Sos redactor de la sección deportes de Olé (Argentina). Convertís comunicados oficiales de federaciones, ligas y clubes en notas casi listas para publicar.
Estilo: titulares con pegada, lenguaje futbolero rioplatense, ritmo ágil, tercera persona, sin opinar ni exagerar.
Reglas estrictas:
- Usá SOLO datos que estén en el comunicado. No agregues resultados, fechas, cifras, nombres de pila, cargos ni contexto que no figuren. Si algo falta, no lo inventes: anotalo en "alerta".
- Lo nuevo primero; contexto después; listas largas (convocados, fixture, ternas, programación) al final, con una etiqueta en negrita tipo **Los convocados:** y un ítem por línea.
- Horarios con punto (17.10) y en hora argentina si el comunicado la da.
- Citas textuales entre comillas y atribuidas. Si el comunicado está en otro idioma, traducí todo al español rioplatense y aclaralo en "alerta".
- Fechas: usá las del comunicado. Si un evento ya pasó o las fechas no cierran, decilo en "alerta".
- En "alerta" anotá lo que el editor tiene que chequear (nombres dudosos, fechas inconsistentes, datos que faltan, citas traducidas). Si no hay nada, "".
Respondé SOLO con un objeto JSON válido, sin texto antes ni después."""

FORMATO = """Devolvé este JSON:
{"titulo": string (máx. 110 caracteres),
 "titulos_alternativos": [string, string],
 "bajada": string (1-2 oraciones),
 "cuerpo": string (3 a 6 párrafos separados por una línea en blanco),
 "competencia": string,
 "etiquetas": [string] (equipos, personas, torneos; máx. 8),
 "alerta": string}"""


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


def redactar(item: dict, motor: str = "auto", indicaciones: str = "") -> dict:
    texto = (item.get("texto") or "").strip()
    if len(texto) < 80:
        raise ValueError("El comunicado tiene muy poco texto para redactar una nota. Abrí el original.")
    idioma = IDIOMAS.get(item.get("idioma") or "es")
    partes = [
        f"Fuente: {item.get('fuente', '')}",
        f"Publicado: {item.get('publicado') or 'sin fecha en la fuente'}",
        f"Deporte: {item.get('deporte', '')}",
    ]
    if idioma:
        partes.append(f"Idioma del comunicado: {idioma} (traducilo).")
    if indicaciones:
        partes.append(f"Indicaciones del editor: {indicaciones.strip()[:500]}")
    prompt = "\n".join(partes) + f"\n\nTÍTULO ORIGINAL: {item.get('titulo_original', '')}\n\nCOMUNICADO:\n\"\"\"\n{texto[:12000]}\n\"\"\"\n\n{FORMATO}"
    salida = ia_motores.generar(prompt, max_tokens=2500, nivel="modelo", motor=motor or "auto", system=SISTEMA)
    d = _extraer_json(salida)
    titulo = str(d.get("titulo") or "").strip()
    cuerpo = str(d.get("cuerpo") or "").strip()
    if not titulo or not cuerpo:
        raise ValueError("La IA devolvió una nota vacía. Probá de nuevo.")
    alts = [str(x).strip() for x in (d.get("titulos_alternativos") or []) if str(x).strip()][:3]
    return {
        "titulo": titulo[:160], "titulos_alternativos": alts, "bajada": str(d.get("bajada") or "").strip(),
        "cuerpo": cuerpo, "competencia": str(d.get("competencia") or "").strip(),
        "etiquetas": [str(x).strip() for x in (d.get("etiquetas") or []) if str(x).strip()][:10],
        "alerta": str(d.get("alerta") or "").strip(),
        "motor": ia_motores.ULTIMO.get("nombre", ""), "modelo": ia_motores.ULTIMO.get("modelo", ""),
    }

"""
Cablera Deportiva · comunicados oficiales convertidos en notas estilo Olé.
Backend FastAPI para Vercel (mismo esquema que Panorama Deportes).

- La captura (scraping de RSS, la API de River y sitios oficiales) NO usa IA.
- La IA redacta solo cuando un editor toca "✦ Redactar nota".
- Todo pedido a /api (salvo health y config) necesita la clave personal CABLERA_CLAVE
  en el encabezado X-Cablera-Clave.
"""
import hmac
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import timedelta

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel

import almacen as db
import captura
import ia_motores
import redaccion
from fuentes_base import FUENTES_BASE, FUENTES_SIN_FILTRO
from ui import INDEX_HTML

VERSION = "1.4"
PRESUPUESTO_CAPTURA = int(os.environ.get("CABLERA_PRESUPUESTO_SEG", "200"))
DIAS_BANDEJA = 14            # la bandeja muestra lo capturado en los últimos 10 días
DIAS_VISTOS = 20             # se recuerda qué links ya se vieron durante 20 días

app = FastAPI(title="Cablera Deportiva")


# ─────────────────────────── seguridad ───────────────────────────
def _clave_config():
    return os.environ.get("CABLERA_CLAVE", "").strip()


def autorizar(clave):
    c = _clave_config()
    if not c:
        raise HTTPException(503, "Falta configurar CABLERA_CLAVE en Vercel (Settings → Environment Variables).")
    if not clave or not hmac.compare_digest(clave.strip().encode(), c.encode()):
        raise HTTPException(401, "Clave incorrecta.")


@app.exception_handler(db.ErrorAlmacen)
async def _error_almacen(_req: Request, e: db.ErrorAlmacen):
    return JSONResponse({"detail": str(e)}, status_code=503)


# ─────────────────────────── fuentes ───────────────────────────
def _quitar_filtros(fs):
    """Una sola vez: UEFA, Premier, LaLiga y Serie A traían solo notas con argentinos. Ahora traen todo."""
    if db.hget(db.K_META, "sin_filtro_intl") == "1":
        return
    base = {f["id"]: f for f in FUENTES_BASE}
    cambios = {}
    for fid in FUENTES_SIN_FILTRO:
        f = fs.get(fid)
        if f and f.get("filtro"):
            f = {**f, "filtro": "", "detalle": base.get(fid, {}).get("detalle", f.get("detalle", ""))}
            cambios[fid] = f
            fs[fid] = f
    if cambios:
        db.hset_muchos(db.K_FUENTES, cambios)
    db.hset(db.K_META, "sin_filtro_intl", "1")


def fuentes() -> dict:
    """Fuentes guardadas. Las fuentes nuevas de fuentes_base.py se suman solas (salvo las que un editor borró)."""
    fs = db.hgetall(db.K_FUENTES)
    borradas = fs.pop("_borradas", None) or []
    _quitar_filtros(fs)
    faltan = {f["id"]: {**f, "estado": "pausada" if f["metodo"] == "pausada" else "sin probar"}
              for f in FUENTES_BASE if f["id"] not in fs and f["id"] not in borradas}
    if faltan:
        db.hset_muchos(db.K_FUENTES, faltan)
        fs.update(faltan)
    return fs


def _estado_tras(f, ok, mensaje, resumen=None):
    f = dict(f)
    f["ultimo"] = {"fecha": captura.iso(captura.ahora()), "ok": ok, "mensaje": mensaje[:300], **(resumen or {})}
    if f.get("metodo") == "pausada":
        f["estado"] = "pausada"
    elif ok:
        f["estado"], f["fallas"] = "ok", 0
    else:
        f["fallas"] = int(f.get("fallas") or 0) + 1
        f["estado"] = "caida" if f["fallas"] >= 3 else "limitada"
    return f


# ─────────────────────────── items ───────────────────────────
ABREV = {"Fútbol": "FUT", "Básquet": "BAS", "Rugby": "RUG", "Automovilismo": "AUT", "Tenis": "TEN",
         "Hockey": "HOC", "Futsal": "FSA", "Vóley": "VOL", "Polideportivo": "POL",
         "Handball": "HAN", "Atletismo": "ATL", "Natación": "NAT", "Golf": "GOL", "Polo": "POL"}


def _codigos(nuevos, existentes):
    usados = {}
    for it in existentes.values():
        c = it.get("codigo") or ""
        m = re.match(r"^([A-Z]{3}-\d{4})-(\d+)$", c)
        if m:
            usados[m.group(1)] = max(usados.get(m.group(1), 0), int(m.group(2)))
    for it in nuevos:
        f = it.get("publicado") or it.get("capturado") or ""
        ddmm = (f[8:10] + f[5:7]) if len(f) >= 10 else "0000"
        dep = ABREV.get(it.get("deporte"), (it.get("deporte") or "GEN")[:3].upper())
        pref = f"{dep}-{ddmm}"
        usados[pref] = usados.get(pref, 0) + 1
        it["codigo"] = f"{pref}-{usados[pref]:02d}"


def _liviano(it):
    """Lo que necesita la bandeja (sin el texto completo)."""
    nota = it.get("nota") or None
    return {k: it.get(k) for k in ("id", "codigo", "fuente", "fuente_id", "categoria", "url", "titulo_original",
                                   "publicado", "capturado", "deporte", "prioridad", "estado", "motivo", "aviso",
                                   "origen", "idioma", "titulo_fuente")} | {
        "resumen": (it.get("texto") or "")[:260],
        "nota": {k: nota.get(k) for k in ("titulo", "bajada", "alerta", "motor", "tipo")} if nota else None,
    }


def guardar_items(nuevos):
    if not nuevos:
        return
    existentes = db.hgetall(db.K_ITEMS)
    nuevos = [n for n in nuevos if n["id"] not in existentes]
    _codigos(nuevos, existentes)
    db.hset_muchos(db.K_ITEMS, {n["id"]: n for n in nuevos})
    return nuevos


# ─────────────────────────── saneamiento (una sola vez por versión) ───────────────────────────
def sanear():
    """Hasta la v1.3 se colaban notas de archivo sin fecha (CAH, AFA, Copa Argentina) y quedaban como recientes.
    Se pasan a Descartadas las nuevas sin nota que no tienen fecha o que se publicaron más de 72 h antes de capturarlas."""
    if db.hget(db.K_META, "saneado") == VERSION:
        return 0
    items = db.hgetall(db.K_ITEMS)
    cambios = {}
    for iid, it in items.items():
        if it.get("estado") != "nueva" or it.get("nota") or it.get("origen") in ("manual", "migrada"):
            continue
        pub, cap = it.get("publicado") or "", it.get("capturado") or ""
        motivo = ""
        if not pub:
            motivo = "Revisión automática: sin fecha en la fuente, probable nota de archivo"
        else:
            try:
                from datetime import datetime as _dt
                if _dt.fromisoformat(pub) < _dt.fromisoformat(cap) - timedelta(hours=captura.MAX_HORAS):
                    motivo = f"Revisión automática: nota vieja (publicada el {pub[8:10]}/{pub[5:7]}/{pub[:4]})"
            except ValueError:
                pass
        if motivo:
            cambios[iid] = {**it, "estado": "descartada", "motivo": motivo}
    db.hset_muchos(db.K_ITEMS, cambios)
    db.hset(db.K_META, "saneado", VERSION)
    return len(cambios)


# ─────────────────────────── títulos en español ───────────────────────────
TRADUCIR_TITULOS = os.environ.get("CABLERA_TRADUCIR_TITULOS", "si").strip().lower() not in ("no", "0", "false")


def traducir(items):
    """Los títulos de fuentes en otro idioma se traducen al español al capturarlos (un solo pedido corto a la IA
    por corrida, con los motores gratuitos primero). El título original queda guardado en titulo_fuente."""
    pend = [i for i in items if (i.get("idioma") or "es") != "es" and i.get("estado") != "descartada" and not i.get("titulo_fuente")]
    if not pend or not TRADUCIR_TITULOS or not ia_motores.disponibles():
        return 0
    hechos = 0
    for k in range(0, len(pend), 25):
        lote = pend[k:k + 25]
        try:
            tr = redaccion.traducir_titulos([i["titulo_original"] for i in lote])
        except Exception:
            continue   # si falla, quedan en el idioma original: no frena la captura
        for it, t in zip(lote, tr):
            if t and t != it["titulo_original"]:
                it["titulo_fuente"], it["titulo_original"] = it["titulo_original"], t
                hechos += 1
    return hechos


# ─────────────────────────── captura ───────────────────────────
def _vistos():
    v = db.hgetall(db.K_VISTOS)
    corte = captura.iso(captura.ahora() - timedelta(days=DIAS_VISTOS))
    viejos = [k for k, x in v.items() if isinstance(x, dict) and (x.get("t") or "") < corte]
    if viejos:
        db.hdel(db.K_VISTOS, *viejos)
        for k in viejos:
            v.pop(k, None)
    return v


def capturar(ids=None, origen="manual"):
    t0 = time.time()
    fs = fuentes()
    # Primero las fuentes que hace más tiempo no se leen: si el tiempo no alcanza, las que quedan afuera
    # pasan primeras en la próxima corrida.
    elegidas = [f for f in sorted(fs.values(), key=lambda x: ((x.get("ultimo") or {}).get("fecha", ""), x.get("orden", 999)))
                if f.get("metodo") != "pausada" and (not ids or f["id"] in ids)]
    vistos = _vistos()
    resultados = {}

    def una(f):
        try:
            items, nv, res = captura.capturar_fuente(f, vistos)
            return f["id"], items, nv, res, None
        except Exception as e:
            return f["id"], [], {}, None, str(e)[:200] or e.__class__.__name__

    ex = ThreadPoolExecutor(max_workers=8)
    futuros = [ex.submit(una, f) for f in elegidas]
    hechos, pendientes = wait(futuros, timeout=PRESUPUESTO_CAPTURA)
    ex.shutdown(wait=False, cancel_futures=True)

    todos, todos_vistos, cambios_fuentes, errores = [], {}, {}, []
    for fu in hechos:
        fid, items, nv, res, err = fu.result()
        f = fs[fid]
        if err:
            cambios_fuentes[fid] = _estado_tras(f, False, err)
            errores.append({"fuente": f["nombre"], "mensaje": err})
        else:
            cambios_fuentes[fid] = _estado_tras(f, True, f"{res['nuevas']} nuevas de {res['encontradas']} encontradas", res)
        todos += items
        todos_vistos.update(nv)
        resultados[fid] = {"nuevas": len(items), "error": err}
    sin_tiempo = [f["nombre"] for f, fu in zip(elegidas, futuros) if fu in pendientes]

    traducir(todos)
    guardados = guardar_items(todos) or []
    db.hset_muchos(db.K_VISTOS, todos_vistos)
    db.hset_muchos(db.K_FUENTES, cambios_fuentes)
    corrida = {"fecha": captura.iso(captura.ahora()), "origen": origen, "fuentes": len(hechos),
               "nuevas": len([x for x in guardados if x["estado"] == "nueva"]),
               "descartadas": len([x for x in guardados if x["estado"] == "descartada"]),
               "errores": errores, "sin_tiempo": sin_tiempo, "segundos": round(time.time() - t0, 1),
               "titulos": [x.get("titulo_original", "")[:120] for x in guardados if x["estado"] == "nueva"][:20]}
    db.lpush_recortar(db.K_CORRIDAS, corrida)
    return corrida


# ─────────────────────────── modelos de pedido ───────────────────────────
class Estado(BaseModel):
    estado: str


class PedidoRedactar(BaseModel):
    motor: str = "auto"
    indicaciones: str = ""
    modo: str = "auto"


class Pegado(BaseModel):
    texto: str
    fuente: str = "Comunicado"
    url: str = ""
    deporte: str = ""
    redactar: bool = True
    motor: str = "auto"
    modo: str = "auto"


class Fuente(BaseModel):
    id: str = ""
    nombre: str
    categoria: str = "Otras"
    deporte: str = "Fútbol"
    metodo: str = "web"
    url: str
    patron: str = ""
    filtro: str = ""
    idioma: str = "es"
    enlace: str = ""
    detalle: str = ""
    orden: int = 500


# ─────────────────────────── rutas ───────────────────────────
@app.get("/api/health")
def health():
    return {"ok": True, "app": "Cablera Deportiva", "version": VERSION}


@app.get("/api/config")
def config():
    disp = ia_motores.disponibles()
    return {"version": VERSION, "clave_configurada": bool(_clave_config()), "almacen": db.descripcion(),
            "almacen_persistente": db.usa_redis(), "ia": bool(disp),
            "motores": [{"id": m, "nombre": ia_motores.NOMBRES[m]} for m in disp],
            "cadena": ia_motores.descripcion_cadena()}


@app.post("/api/login")
def login(x_cablera_clave: str = Header(default="")):
    autorizar(x_cablera_clave)
    return {"ok": True}


@app.get("/api/items")
def listar(x_cablera_clave: str = Header(default=""), dias: int = DIAS_BANDEJA):
    autorizar(x_cablera_clave)
    sanear()
    items = db.hgetall(db.K_ITEMS)
    corte = captura.iso(captura.ahora() - timedelta(days=max(1, min(dias, 60))))
    vis = [_liviano(i) for i in items.values() if (i.get("capturado") or "") >= corte or i.get("estado") in ("nueva", "revision")]
    ultima = db.lrange(db.K_CORRIDAS, 1)
    return {"items": vis, "total": len(items), "ultima_corrida": ultima[0] if ultima else None}


@app.get("/api/items/{iid}")
def detalle(iid: str, x_cablera_clave: str = Header(default="")):
    autorizar(x_cablera_clave)
    it = db.hget(db.K_ITEMS, iid)
    if not it:
        raise HTTPException(404, "No existe ese comunicado.")
    return it


@app.post("/api/items/{iid}/estado")
def cambiar_estado(iid: str, body: Estado, x_cablera_clave: str = Header(default="")):
    autorizar(x_cablera_clave)
    if body.estado not in ("nueva", "revision", "copiada", "descartada"):
        raise HTTPException(400, "Estado inválido.")
    it = db.hget(db.K_ITEMS, iid)
    if not it:
        raise HTTPException(404, "No existe ese comunicado.")
    it["estado"] = body.estado
    if body.estado == "copiada":
        it["copiada_en"] = captura.iso(captura.ahora())
    db.hset(db.K_ITEMS, iid, it)
    return {"ok": True, "estado": it["estado"]}


@app.post("/api/items/{iid}/redactar")
def redactar_item(iid: str, body: PedidoRedactar, x_cablera_clave: str = Header(default="")):
    autorizar(x_cablera_clave)
    it = db.hget(db.K_ITEMS, iid)
    if not it:
        raise HTTPException(404, "No existe ese comunicado.")
    if not ia_motores.disponibles():
        raise HTTPException(503, "No hay ningún motor de IA configurado en Vercel.")
    try:
        nota = redaccion.redactar(it, motor=body.motor, indicaciones=body.indicaciones, modo=body.modo if body.modo in redaccion.MODOS else "auto")
    except (ValueError, RuntimeError) as e:
        raise HTTPException(502, str(e))
    nota["generada"] = captura.iso(captura.ahora())
    if it.get("nota"):
        it["versiones_previas"] = ([it["nota"]] + (it.get("versiones_previas") or []))[:3]
    it["nota"] = nota
    db.hset(db.K_ITEMS, iid, it)
    return it


@app.post("/api/pegar")
def pegar(body: Pegado, x_cablera_clave: str = Header(default="")):
    autorizar(x_cablera_clave)
    texto = captura.limpiar(body.texto)
    if len(texto) < 80:
        raise HTTPException(400, "Pegá el comunicado completo (al menos un párrafo).")
    ahora = captura.iso(captura.ahora())
    primera = texto.split("\n")[0][:160]
    it = {"id": "manual-" + str(int(time.time() * 1000)), "fuente_id": "manual", "fuente": body.fuente.strip() or "Comunicado",
          "categoria": "Pegados a mano", "url": body.url.strip() if body.url.strip().startswith("http") else "",
          "titulo_original": primera, "texto": texto[:15000], "publicado": ahora, "capturado": ahora,
          "deporte": body.deporte.strip() or "Fútbol", "idioma": "es", "prioridad": "media", "estado": "nueva",
          "motivo": "", "aviso": "", "origen": "manual", "nota": None}
    it["prioridad"] = captura.clasificar(it, {})[0]
    if body.redactar and ia_motores.disponibles():
        try:
            it["nota"] = redaccion.redactar(it, motor=body.motor, modo=body.modo if body.modo in redaccion.MODOS else "auto") | {"generada": ahora}
        except (ValueError, RuntimeError) as e:
            it["aviso"] = f"No se pudo redactar: {e}"
    guardar_items([it])
    return db.hget(db.K_ITEMS, it["id"])


@app.post("/api/capturar")
def capturar_ruta(x_cablera_clave: str = Header(default=""), fuente: str = "", origen: str = "manual"):
    autorizar(x_cablera_clave)
    ids = [x for x in fuente.split(",") if x] or None
    return capturar(ids, origen=origen if origen in ("manual", "auto") else "manual")


@app.get("/api/corridas")
def corridas(x_cablera_clave: str = Header(default="")):
    autorizar(x_cablera_clave)
    return db.lrange(db.K_CORRIDAS, 30)


@app.get("/api/fuentes")
def listar_fuentes(x_cablera_clave: str = Header(default="")):
    autorizar(x_cablera_clave)
    return sorted(fuentes().values(), key=lambda f: f.get("orden", 999))


@app.post("/api/fuentes")
def guardar_fuente(body: Fuente, x_cablera_clave: str = Header(default="")):
    autorizar(x_cablera_clave)
    if body.metodo not in ("rss", "river", "web", "premier", "wp", "pausada"):
        raise HTTPException(400, "Método inválido.")
    for campo in ("patron", "filtro"):
        try:
            re.compile(getattr(body, campo) or "")
        except re.error as e:
            raise HTTPException(400, f"El {campo} no es una expresión regular válida: {e}")
    fs = fuentes()
    fid = body.id.strip() or re.sub(r"[^a-z0-9]+", "-", body.nombre.lower()).strip("-")[:40] or "fuente"
    previa = fs.get(fid, {})
    f = {**previa, **body.model_dump(), "id": fid}
    if body.metodo == "pausada":
        f["estado"] = "pausada"
    elif previa.get("estado") in (None, "pausada"):
        f["estado"] = "sin probar"
    db.hset(db.K_FUENTES, fid, f)
    return f


@app.delete("/api/fuentes/{fid}")
def borrar_fuente(fid: str, x_cablera_clave: str = Header(default="")):
    autorizar(x_cablera_clave)
    fuentes()
    borradas = db.hget(db.K_FUENTES, "_borradas") or []
    db.hset(db.K_FUENTES, "_borradas", sorted(set(borradas) | {fid}))
    db.hdel(db.K_FUENTES, fid)
    return {"ok": True}


@app.post("/api/fuentes/{fid}/probar")
def probar_fuente(fid: str, x_cablera_clave: str = Header(default="")):
    """Lee la fuente sin guardar nada y muestra qué encontró."""
    autorizar(x_cablera_clave)
    f = fuentes().get(fid)
    if not f:
        raise HTTPException(404, "No existe esa fuente.")
    if f.get("metodo") == "pausada":
        return {"ok": False, "mensaje": "La fuente está pausada: cambiá el método para probarla.", "items": []}
    t0 = time.time()
    try:
        items, _, res = captura.capturar_fuente(f, {}, prueba=True, limite=5)
    except Exception as e:
        db.hset(db.K_FUENTES, fid, _estado_tras(f, False, str(e)))
        return {"ok": False, "mensaje": str(e)[:300], "items": []}
    traducir(items)
    db.hset(db.K_FUENTES, fid, _estado_tras(f, True, f"Prueba: {res['encontradas']} links, {len(items)} notas leídas", res))
    return {"ok": True, "segundos": round(time.time() - t0, 1), "encontradas": res["encontradas"],
            "items": [{"titulo": i["titulo_original"], "publicado": i["publicado"], "url": i["url"],
                       "largo": len(i.get("texto") or ""), "inicio": (i.get("texto") or "")[:240],
                       "aviso": i.get("aviso", ""), "estado": i["estado"], "motivo": i["motivo"]} for i in items]}


@app.post("/api/importar")
def importar(x_cablera_clave: str = Header(default="")):
    """Carga una sola vez las notas de la Cablera anterior (archivo migracion_notas.json)."""
    autorizar(x_cablera_clave)
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migracion_notas.json")
    try:
        with open(ruta, encoding="utf-8") as fh:
            notas = json.load(fh)
    except FileNotFoundError:
        raise HTTPException(404, "No está el archivo migracion_notas.json en el repositorio.")
    existentes = db.hgetall(db.K_ITEMS)
    nuevos = {n["id"]: n for n in notas if n["id"] not in existentes}
    db.hset_muchos(db.K_ITEMS, nuevos)
    return {"importadas": len(nuevos), "ya_estaban": len(notas) - len(nuevos)}


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def index():
    return HTMLResponse(INDEX_HTML.replace("{{VERSION}}", VERSION), headers={"Cache-Control": "no-store"})


_FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#1F4FD1"/>'
            '<path d="M14 20h36M14 32h36M14 44h24" stroke="#fff" stroke-width="6" stroke-linecap="round"/></svg>')


@app.get("/favicon.svg", include_in_schema=False)
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(_FAVICON, media_type="image/svg+xml", headers={"Cache-Control": "public, max-age=86400"})

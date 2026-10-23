"""
Memoria de la Cablera: Upstash Redis (se crea con un clic en Vercel → Storage) o,
si no está configurado, un archivo JSON local (para probar en la compu).

Variables que carga Vercel solo al conectar la base:
  KV_REST_API_URL / KV_REST_API_TOKEN          (nombre que usa Vercel)
  UPSTASH_REDIS_REST_URL / UPSTASH_REDIS_REST_TOKEN   (nombre que usa Upstash)

Claves usadas en Redis (todas con el prefijo "cab:"):
  cab:items     hash  id -> comunicado/nota (JSON)
  cab:fuentes   hash  id -> fuente (JSON)
  cab:vistos    hash  url -> fecha en que se vio por primera vez (para no repetir)
  cab:corridas  lista de las últimas corridas de captura (JSON)
"""
import json
import os
import threading

import requests

PREFIJO = os.environ.get("CABLERA_PREFIJO", "cab").strip() or "cab"
K_ITEMS, K_FUENTES, K_VISTOS, K_CORRIDAS = (f"{PREFIJO}:items", f"{PREFIJO}:fuentes",
                                            f"{PREFIJO}:vistos", f"{PREFIJO}:corridas")


def _cfg():
    url = (os.environ.get("KV_REST_API_URL") or os.environ.get("UPSTASH_REDIS_REST_URL") or "").strip().rstrip("/")
    tok = (os.environ.get("KV_REST_API_TOKEN") or os.environ.get("UPSTASH_REDIS_REST_TOKEN") or "").strip()
    return url, tok


def usa_redis() -> bool:
    url, tok = _cfg()
    return bool(url and tok)


class ErrorAlmacen(Exception):
    pass


# ─────────────────────────── Redis (REST de Upstash) ───────────────────────────
def _pipeline(cmds):
    url, tok = _cfg()
    try:
        r = requests.post(f"{url}/pipeline", json=cmds, timeout=20,
                          headers={"Authorization": f"Bearer {tok}"})
    except requests.RequestException as e:
        raise ErrorAlmacen(f"No se pudo conectar con la base ({str(e)[:80]})")
    if r.status_code != 200:
        raise ErrorAlmacen(f"La base respondió {r.status_code}: {r.text[:150]}")
    out = []
    for x in r.json():
        if isinstance(x, dict) and x.get("error"):
            raise ErrorAlmacen(f"Error de la base: {x['error']}")
        out.append(x.get("result") if isinstance(x, dict) else x)
    return out


def _cmd(*args):
    return _pipeline([list(args)])[0]


# ─────────────────────────── JSON local ───────────────────────────
_LOCK = threading.Lock()
# En Vercel el disco es de solo lectura salvo /tmp (y /tmp se borra): sin Redis, nada queda guardado
_DIR = "/tmp" if os.environ.get("VERCEL") else os.path.dirname(os.path.abspath(__file__))
_ARCHIVO = os.environ.get("CABLERA_ARCHIVO", os.path.join(_DIR, "datos_locales.json"))


def _leer_local():
    try:
        with open(_ARCHIVO, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _guardar_local(d):
    tmp = _ARCHIVO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)
    os.replace(tmp, _ARCHIVO)


# ─────────────────────────── API común ───────────────────────────
def hgetall(key) -> dict:
    """Devuelve {campo: objeto} con los valores ya decodificados."""
    if usa_redis():
        flat = _cmd("HGETALL", key) or []
        pares = dict(zip(flat[0::2], flat[1::2]))
    else:
        with _LOCK:
            pares = dict(_leer_local().get(key, {}))
    out = {}
    for k, v in pares.items():
        try:
            out[k] = json.loads(v) if isinstance(v, str) else v
        except json.JSONDecodeError:
            out[k] = v
    return out


def hget(key, campo):
    if usa_redis():
        v = _cmd("HGET", key, campo)
    else:
        with _LOCK:
            v = _leer_local().get(key, {}).get(campo)
    if v is None:
        return None
    try:
        return json.loads(v) if isinstance(v, str) else v
    except json.JSONDecodeError:
        return v


def hset_muchos(key, valores: dict):
    """valores: {campo: objeto}. Se guardan como JSON."""
    if not valores:
        return
    if usa_redis():
        items = list(valores.items())
        for i in range(0, len(items), 100):
            args = ["HSET", key]
            for k, v in items[i:i + 100]:
                args += [k, json.dumps(v, ensure_ascii=False)]
            _cmd(*args)
    else:
        with _LOCK:
            d = _leer_local()
            h = d.setdefault(key, {})
            for k, v in valores.items():
                h[k] = json.dumps(v, ensure_ascii=False)
            _guardar_local(d)


def hset(key, campo, valor):
    hset_muchos(key, {campo: valor})


def hdel(key, *campos):
    if not campos:
        return
    if usa_redis():
        for i in range(0, len(campos), 200):
            _cmd("HDEL", key, *campos[i:i + 200])
    else:
        with _LOCK:
            d = _leer_local()
            h = d.setdefault(key, {})
            for c in campos:
                h.pop(c, None)
            _guardar_local(d)


def lpush_recortar(key, valor, maximo=60):
    v = json.dumps(valor, ensure_ascii=False)
    if usa_redis():
        _pipeline([["LPUSH", key, v], ["LTRIM", key, "0", str(maximo - 1)]])
    else:
        with _LOCK:
            d = _leer_local()
            lst = d.setdefault(key, [])
            lst.insert(0, v)
            del lst[maximo:]
            _guardar_local(d)


def lrange(key, n=30):
    if usa_redis():
        lst = _cmd("LRANGE", key, "0", str(n - 1)) or []
    else:
        with _LOCK:
            lst = list(_leer_local().get(key, []))[:n]
    out = []
    for v in lst:
        try:
            out.append(json.loads(v))
        except (json.JSONDecodeError, TypeError):
            pass
    return out


def descripcion() -> str:
    return "Upstash Redis" if usa_redis() else "archivo local (solo para pruebas)"

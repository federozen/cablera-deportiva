# Publicar la Cablera Deportiva en Vercel (sin consola)

Son 6 pasos, todos desde el navegador. Tiempo: 20 minutos.

## 1. Subir a GitHub

1. Entrá a https://github.com/new y creá un repositorio nuevo, por ejemplo `cablera-deportiva`. Puede ser **privado**.
2. En la página del repositorio vacío, tocá **uploading an existing file**.
3. Abrí la carpeta `cablera-deportiva` del zip y arrastrá **todo lo de adentro** (no la carpeta), incluidos los que empiezan con punto: `.github`, `.gitignore`, `.python-version`. Si no los ves: en Mac `Cmd + Shift + .` en el Finder; en Windows, Vista → Elementos ocultos.
4. Tocá **Commit changes**.

Tiene que quedar así en la raíz del repositorio:

```
app.py  captura.py  almacen.py  redaccion.py  ia_motores.py  fuentes_base.py  ui.py
migracion_notas.json  requirements.txt  .python-version  .gitignore
.github/workflows/captura.yml
```

Si `.github/workflows/captura.yml` no se subió: **Add file → Create new file**, escribí `.github/workflows/captura.yml` como nombre (GitHub crea las carpetas solo) y pegá el contenido del archivo.

## 2. Crear el proyecto en Vercel

1. https://vercel.com/new → elegí el repositorio `cablera-deportiva` → **Import**.
2. Vercel detecta que es FastAPI (Python). No cambies nada: **Deploy**.
3. Te da una dirección tipo `https://cablera-deportiva-xxxx.vercel.app`. Anotala.

## 3. Crear la base de datos (un clic)

1. En el proyecto de Vercel → pestaña **Storage** → **Create Database**.
2. Elegí **Upstash** → **Upstash for Redis** → plan **Free** → región São Paulo o Washington → **Create**.
3. Cuando pregunte, **conectala al proyecto** `cablera-deportiva` (Production, Preview y Development).

Vercel carga solas las variables `KV_REST_API_URL` y `KV_REST_API_TOKEN`. No hay que copiar nada.

## 4. Cargar la clave y la IA

Proyecto → **Settings → Environment Variables**. Agregá:

| Nombre | Valor |
|---|---|
| `CABLERA_CLAVE` | una clave personal larga que elijas, por ejemplo `cable-tribuna-2026-lluvia`. Es la que se pide para entrar. |
| `GEMINI_API_KEY` | (gratis) la misma que usás en Panorama Deportes |
| `MISTRAL_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY` | (gratis, opcionales) las mismas de Panorama |
| `ANTHROPIC_API_KEY` | (pago, respaldo) tu API key de Claude |

Con una sola clave de IA alcanza. Las podés copiar del proyecto de Panorama Deportes (Settings → Environment Variables → los tres puntitos → Copy).

Después: **Deployments** → tres puntitos del último → **Redeploy**.

## 5. Comprobar

- `https://TU-DIRECCION.vercel.app/api/health` → tiene que decir `{"ok":true,"app":"Cablera Deportiva",...}`.
- Abrí la dirección principal, ingresá tu `CABLERA_CLAVE`.
- Pestaña **Actividad**: tiene que decir *Base de datos: Upstash Redis*. Ahí tocá **Importar notas de la Cablera anterior** (una sola vez: trae las 52 notas de la versión anterior).
- Tocá **↻ Capturar ahora**. En uno o dos minutos aparecen los comunicados nuevos.
- Pestaña **Fuentes**: tocá **Probar** en cada fuente para ver qué encuentra (no guarda nada).

## 6. Captura automática cada 2 horas (GitHub Actions)

GitHub "toca el timbre" de la app cada 2 horas, de 7.33 a 21.33. No necesita claves de IA: solo la dirección y tu clave.

1. En GitHub: repositorio → **Settings → Secrets and variables → Actions → New repository secret**:
   - `CABLERA_URL` → la dirección de Vercel, por ejemplo `https://cablera-deportiva-xxxx.vercel.app`
   - `CABLERA_CLAVE` → la misma clave del paso 4
2. Pestaña **Actions** → si pide habilitarlas, tocá **I understand… enable**.
3. **Captura de la Cablera → Run workflow** para probar a mano. En el registro tiene que verse `Respuesta HTTP: 200` y el resumen.

Para cambiar el horario, editá la línea `cron` de `.github/workflows/captura.yml` (está en hora UTC = Argentina + 3).

## Actualizar a una versión nueva

GitHub → repositorio → **Add file → Upload files** → arrastrá todos los archivos de adentro de la carpeta nueva → **Commit changes**. Vercel publica solo en uno o dos minutos. La versión se ve al lado del logo.

## Si algo no anda

- **"Falta configurar CABLERA_CLAVE"**: cargala (paso 4) y hacé Redeploy.
- **Aviso amarillo "no hay base de datos conectada"**: falta el paso 3, o no hiciste Redeploy después.
- **Una fuente queda "Limitada" o "Caída"**: abrí Fuentes → **Probar** para ver el error. Si el sitio cambió, **Editar** y ajustá la dirección o el patrón. Si el sitio bloquea a Vercel (algunos bloquean servidores), pasala a *Pausada* y usá **+ Pegar comunicado** para sus notas.
- **"No respondió ningún motor de IA"**: revisá las claves de IA en Vercel y que tengan cupo.
- **El Action falla con 401**: `CABLERA_CLAVE` de GitHub no es igual a la de Vercel.
- **El Action falla por tiempo**: la captura tiene un tope de 200 segundos; las fuentes que no llegan quedan para la próxima. Si pasa siempre, pausá las fuentes más lentas.

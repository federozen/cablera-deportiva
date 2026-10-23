# Cablera Deportiva · v1.2

Comunicados oficiales de federaciones, ligas y clubes, capturados solos y listos para convertirse en notas estilo Olé.

## Cómo funciona

1. **Captura (sin IA, sin costo).** Cada 2 horas (GitHub Actions) o con **↻ Capturar ahora**, la app lee las fuentes oficiales: feeds RSS, la API de River y las webs (scraping). Trae título, fecha, texto completo y link de cada comunicado nuevo de las últimas 36 horas, y nunca repite uno ya visto.
2. **Orden por reglas.** Prioridad alta si el título habla de Selección, Messi, Boca, River, Racing, Independiente, San Lorenzo, renuncias, sanciones, lesiones, finales, convocatorias o Colapinto. Venta de entradas, socios, sponsors, merchandising y efemérides van solos a **Descartadas** (se pueden recuperar).
3. **Títulos en español.** Los títulos de fuentes en inglés o italiano (UEFA, Premier, Serie A, MLS, ATP, WTA, F1, FIA…) se traducen solos al capturarlos, todos juntos en un único pedido corto a la IA por corrida (motores gratuitos primero; con Claude Haiku cuesta una fracción de centavo). El título original queda visible en la nota. Si la IA no responde, quedan en el idioma original y se traducen al redactar.
4. **IA a demanda.** En la bandeja ves los títulos originales. Cuando uno te sirve, **✦ Redactar nota**: la IA escribe título, dos alternativos, bajada, cuerpo, etiquetas y lo que hay que chequear. Usa los motores gratuitos primero (Gemini, Mistral, Groq, OpenRouter) y Claude de respaldo. La nota queda guardada: no se paga dos veces. **↻ Otra versión** pide una nueva.
5. **Al CMS.** **Copiar nota completa** (con formato) la marca como *Copiada*. Estados: Nuevas, En revisión, Copiadas, Descartadas.

También: **+ Pegar comunicado** (lo que llega por mail o WhatsApp), filtros por deporte y fuente, búsqueda, y la pestaña **Fuentes** para agregar, editar, pausar y **Probar** fuentes sin tocar código.

## Fuentes y métodos

| Método | Para qué | Qué completar |
|---|---|---|
| RSS | sitios con feed (LPF, Racing, UAR, CONMEBOL, F1) | la dirección del feed |
| Web | sitios sin feed (AFA, Boca, Independiente, San Lorenzo, Liga Nacional…) | la página de listado y el **patrón**: un pedazo de la dirección que tienen todas las notas (ej. `/noticias/`) |
| API River | riverplate.com | nada |
| API Premier | premierleague.com (reúne los comunicados de los clubes) | nada |
| Pausada | sitios que necesitan navegador (FIFA, Ligue 1, AAT, Super Rugby Americas) | — |

**35 fuentes de arranque**, revisadas una por una el 23/10/2026 con un navegador: fútbol argentino (AFA, Tribunal de Disciplina en PDF, LPF), clubes (Boca, River, Racing, Independiente, San Lorenzo), CONMEBOL y UEFA, ligas del exterior (Premier, LaLiga, Serie A, MLS) filtradas por argentinos, tenis (ATP, WTA, Copa Davis), motor (F1, FIA, ACTC), rugby (UAR, World Rugby), básquet (Liga Nacional, FIBA, CABB), vóley (FeVA), hockey (CAH) y el Comité Olímpico Argentino. Las que no se pueden leer sin navegador quedan pausadas, con el motivo en la pestaña Fuentes. Si en el futuro se suman fuentes nuevas a `fuentes_base.py`, aparecen solas al actualizar (salvo las que hayas borrado).

El **filtro** deja pasar solo notas que mencionen ciertas palabras (separadas por `|`). Las ligas de afuera vienen filtradas por argentinos.

La fecha de cada nota sale, en este orden, de los metadatos de la página, de la dirección (Independiente y San Lorenzo la llevan), del listado (Boca) o del texto (AFA). Si no hay fecha, la nota entra con el aviso *Verificar*.

## Costos

- Vercel (plan gratis): la captura gasta poca CPU (sin IA). Las 4 horas de CPU por mes se comparten con Panorama y el Radar.
- Upstash Redis (plan gratis): sobra para la Cablera.
- IA: la traducción de títulos de fuentes extranjeras (un pedido corto por captura) y la redacción cuando tocás **Redactar**. Con los motores gratuitos, cero; con Claude Haiku 5.5, menos de medio centavo de dólar por nota.

## Archivos

| Archivo | Qué es |
|---|---|
| `app.py` | Servidor (FastAPI): bandeja, fuentes, captura y redacción |
| `captura.py` | Lectores RSS, API de River y scraping web; fechas y prioridades |
| `fuentes_base.py` | Fuentes con las que arranca (después se editan desde la app) |
| `redaccion.py` | El pedido a la IA con el estilo Olé |
| `ia_motores.py` | Motores de IA: gratuitos primero, Claude de respaldo (el mismo del Monitor) |
| `almacen.py` | Base de datos: Upstash Redis, o un archivo local para probar |
| `ui.py` | La interfaz |
| `migracion_notas.json` | Las 52 notas de la Cablera anterior, para importar una vez |
| `.github/workflows/captura.yml` | La captura automática cada 2 horas |

Publicación paso a paso: `DEPLOY_VERCEL.md`.

## Variables de entorno (Vercel)

| Variable | Obligatoria | Para qué |
|---|---|---|
| `CABLERA_CLAVE` | sí | clave personal para entrar |
| `KV_REST_API_URL`, `KV_REST_API_TOKEN` | sí (las carga Vercel) | base Upstash Redis |
| `GEMINI_API_KEY`, `MISTRAL_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY` | al menos una de IA | motores gratuitos |
| `ANTHROPIC_API_KEY` | opcional | Claude de respaldo |
| `IA_ORDEN`, `IA_RESPALDO_CLAUDE`, `CLAUDE_MODELO`, `GEMINI_MODELO`… | opcional | igual que en el Monitor |
| `CABLERA_PRESUPUESTO_SEG` | opcional | tope de segundos de cada captura (200) |
| `CABLERA_TRADUCIR_TITULOS` | opcional | `no` para no traducir los títulos al capturar |

## Probar en tu computadora (opcional)

```bash
pip install -r requirements.txt
CABLERA_CLAVE=prueba uvicorn app:app --reload
```

Sin Upstash configurado guarda todo en `datos_locales.json`.

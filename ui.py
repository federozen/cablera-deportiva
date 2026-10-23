INDEX_HTML = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Cablera Deportiva</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>
:root{
  --paper:#F3F5F8; --surface:#FFFFFF; --ink:#141820; --muted:#5A6372; --line:#DCE1E8;
  --accent:#1F4FD1; --accent-soft:rgba(31,79,209,.09); --on-accent:#FFFFFF;
  --alta:#C8372A; --media:#B97C06; --baja:#8A93A2; --ok:#1C8556; --warn-bg:#FFF6E0; --warn-ink:#6B4A00;
  --ia:#7A3FD1; --ia-soft:rgba(122,63,209,.10);
  --f-display:"Barlow Condensed","Arial Narrow",Impact,sans-serif;
  --f-body:"Source Serif 4",Georgia,"Times New Roman",serif;
  --f-ui:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --f-mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#0E1116; --surface:#161A21; --ink:#E7EAF0; --muted:#98A1B0; --line:#29303B;
  --accent:#86A2FF; --accent-soft:rgba(134,162,255,.12); --on-accent:#0E1116;
  --alta:#FF6F61; --media:#F0B23C; --baja:#7F8898; --ok:#4CC38A; --warn-bg:#2B2410; --warn-ink:#F3D58C;
  --ia:#B897FF; --ia-soft:rgba(184,151,255,.13); color-scheme:dark}}
*{box-sizing:border-box}
html,body{min-height:100%}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--f-ui);font-size:14px;line-height:1.45;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
button,input,textarea,select{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
[hidden]{display:none!important}
.wrap{max-width:1280px;margin:0 auto;display:flex;flex-direction:column;gap:14px;padding-block:18px 32px}

header.top{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px;border-bottom:3px solid var(--ink);padding-bottom:10px}
.brand h1{font-family:var(--f-display);font-weight:700;font-size:34px;line-height:1;letter-spacing:.01em;text-transform:uppercase;margin:0}
.brand h1 small{font-family:var(--f-mono);font-size:11px;font-weight:400;color:var(--muted);letter-spacing:0;margin-left:8px;vertical-align:4px}
.brand p{margin:4px 0 0;color:var(--muted);font-size:13px}
.ticker{font-family:var(--f-mono);font-size:12px;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.ticker b{color:var(--ink);font-weight:500}
.live{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--ok);margin-right:6px;vertical-align:1px}

.views{display:flex;gap:18px;border-bottom:1px solid var(--line);flex-wrap:wrap}
.views button{border:0;background:none;padding:6px 0 8px;margin-bottom:-1px;cursor:pointer;font-family:var(--f-display);font-size:20px;font-weight:600;letter-spacing:.02em;text-transform:uppercase;color:var(--muted);border-bottom:3px solid transparent}
.views button[aria-pressed="true"]{color:var(--ink);border-bottom-color:var(--accent)}
.views .n{font-family:var(--f-mono);font-size:12px;font-weight:400;margin-left:6px}

.toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}
.tabs{display:flex;gap:2px;flex-wrap:wrap;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:3px}
.tabs button{border:0;background:none;padding:6px 10px;border-radius:6px;cursor:pointer;color:var(--muted);font-weight:500}
.tabs button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}
.tabs .n{font-family:var(--f-mono);font-size:11px;margin-left:5px;opacity:.75}
.filters{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.filters select,.filters input[type=search]{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:6px 9px;min-width:0}
.filters input[type=search]{width:190px;max-width:100%}
.chk{display:flex;gap:6px;align-items:center;font-size:13px;color:var(--muted);cursor:pointer}
.btn{border:1px solid var(--line);background:var(--surface);border-radius:6px;padding:7px 12px;cursor:pointer;font-weight:500;white-space:nowrap;text-decoration:none;display:inline-flex;align-items:center;gap:6px}
.btn:hover{border-color:var(--muted)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}
.btn.ia{background:var(--ia);border-color:var(--ia);color:#fff}
.btn.sm{padding:4px 9px;font-size:12px}
.btn[disabled]{opacity:.5;cursor:default}

.desk{display:grid;grid-template-columns:minmax(300px,400px) minmax(0,1fr);gap:16px;align-items:start}
.list{display:flex;flex-direction:column;gap:8px;min-width:0}
.item{position:relative;display:block;width:100%;text-align:left;background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:10px 12px 11px 16px;cursor:pointer}
.item::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;border-radius:8px 0 0 8px;background:var(--baja)}
.item[data-p="alta"]::before{background:var(--alta)}
.item[data-p="media"]::before{background:var(--media)}
.item:hover{border-color:var(--muted)}
.item[aria-current="true"]{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent) inset}
.item[data-estado="copiada"],.item[data-estado="descartada"]{opacity:.62}
.meta{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:center;font-family:var(--f-mono);font-size:11px;color:var(--muted)}
.pill{font-family:var(--f-ui);font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;padding:1px 7px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}
.pill.ia{background:var(--ia-soft);color:var(--ia)}
.state{font-family:var(--f-ui);font-size:11px;font-weight:600;padding:1px 7px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}
.state[data-s="copiada"]{color:var(--ok);border-color:var(--ok)}
.state[data-s="revision"]{color:var(--media);border-color:var(--media)}
.item h3{font-family:var(--f-display);font-weight:600;font-size:20px;line-height:1.08;margin:6px 0 4px;text-wrap:balance}
.item .src{font-size:12px;color:var(--muted)}
.flag{color:var(--warn-ink);background:var(--warn-bg);font-family:var(--f-ui);font-size:11px;font-weight:600;padding:1px 6px;border-radius:4px}
.more{margin:4px auto 0}

.empty{background:var(--surface);border:1px dashed var(--line);border-radius:8px;padding:22px;color:var(--muted)}
.empty strong{color:var(--ink);display:block;font-family:var(--f-display);font-size:22px;font-weight:600;margin-bottom:4px}

article.note{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:22px clamp(16px,3vw,36px) 28px;min-width:0;position:sticky;top:12px;max-height:calc(100vh - 24px);overflow:auto}
.note .back{display:none}
.note .kicker{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;font-family:var(--f-mono);font-size:12px;color:var(--muted)}
.note .kicker a{color:var(--accent)}
.alert{margin:14px 0 0;background:var(--warn-bg);color:var(--warn-ink);border-radius:6px;padding:9px 12px;font-size:13px}
.alert b{font-weight:600}
.note h2{font-family:var(--f-display);font-weight:700;font-size:clamp(28px,3.6vw,40px);line-height:1.02;margin:16px 0 10px;text-wrap:balance;max-width:24ch}
.note .label{font-family:var(--f-ui);font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-top:16px}
.note .alts{display:flex;flex-direction:column;gap:4px;margin:0 0 14px}
.note .alts button{border:1px dashed var(--line);background:none;border-radius:6px;padding:5px 9px;text-align:left;cursor:pointer;font-family:var(--f-display);font-size:18px;font-weight:600;color:var(--muted)}
.note .alts button:hover{color:var(--ink);border-color:var(--muted)}
.note .bajada{font-family:var(--f-body);font-size:18px;line-height:1.45;color:var(--muted);margin:0 0 18px;max-width:62ch}
.note .cuerpo{font-family:var(--f-body);font-size:17px;line-height:1.62;max-width:65ch}
.note .cuerpo p{margin:0 0 14px}
.note .cuerpo strong{font-weight:600}
.note .orig{font-size:15px;color:var(--ink)}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin:18px 0 0}
.tags span{font-size:12px;border:1px solid var(--line);border-radius:4px;padding:2px 7px;color:var(--muted)}
.actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:14px 0 0;margin-top:20px;border-top:1px solid var(--line)}
.actions .sp{flex:1}
.toast{font-size:13px;color:var(--ok);font-weight:600}
.err{color:var(--alta);font-size:13px}
.iabox{margin:18px 0;padding:14px;border:1px solid var(--ia);background:var(--ia-soft);border-radius:8px;display:flex;flex-direction:column;gap:10px}
.iabox p{margin:0;font-size:13px;color:var(--muted)}
.iabox .row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.iabox input{flex:1;min-width:180px;background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:7px 9px}
.iabox select,.actions select{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:6px 8px}
.firma{font-family:var(--f-mono);font-size:11px;color:var(--muted);margin-top:8px}
details.orig-box{margin-top:22px;border-top:1px solid var(--line);padding-top:12px}
details.orig-box summary{cursor:pointer;font-weight:600;color:var(--muted)}
.spin{display:inline-block;width:12px;height:12px;border:2px solid currentColor;border-right-color:transparent;border-radius:50%;animation:sp .8s linear infinite;vertical-align:-1px}
@keyframes sp{to{transform:rotate(360deg)}}

.panel{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px;display:flex;flex-direction:column;gap:10px}
.panel h2{font-family:var(--f-display);font-size:24px;font-weight:600;margin:0}
.panel p{margin:0;color:var(--muted)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.panel label{display:flex;flex-direction:column;gap:4px;font-size:12px;font-weight:600;color:var(--muted);min-width:0}
.panel textarea,.panel input,.panel select{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:8px 10px;font-weight:400;color:var(--ink);min-width:0}
.panel textarea{min-height:170px;resize:vertical;font-family:var(--f-body);font-size:15px}
.panel .foot{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.hint{font-weight:400;font-size:12px;color:var(--muted)}

.sources{display:flex;flex-direction:column;gap:18px}
.sum{display:flex;flex-wrap:wrap;gap:8px 16px;color:var(--muted);font-size:13px;align-items:center}
.sum b{color:var(--ink);font-family:var(--f-mono);font-weight:500}
.sgroup h3{font-family:var(--f-display);font-size:18px;font-weight:600;text-transform:uppercase;letter-spacing:.03em;margin:0 0 6px}
.stable{background:var(--surface);border:1px solid var(--line);border-radius:8px;overflow-x:auto}
.stable table{width:100%;border-collapse:collapse;min-width:720px}
.stable th,.stable td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
.stable tr:last-child td{border-bottom:0}
.stable th{font-size:11px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.stable td.name a{color:var(--ink);font-weight:600;text-decoration:none}
.stable td.name a:hover{color:var(--accent);text-decoration:underline}
.stable td.det{color:var(--muted);font-size:13px;max-width:420px}
.stable td.acc{white-space:nowrap}
.method{font-family:var(--f-mono);font-size:11px;border:1px solid var(--line);border-radius:4px;padding:1px 6px;white-space:nowrap}
.st{font-size:11px;font-weight:600;padding:2px 8px;border-radius:999px;white-space:nowrap;border:1px solid currentColor}
.st[data-s="ok"]{color:var(--ok)}
.st[data-s="limitada"]{color:var(--media)}
.st[data-s="caida"]{color:var(--alta)}
.st[data-s="pausada"],.st[data-s="sin probar"]{color:var(--baja)}
.probe{background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin-top:8px;font-size:13px}
.probe ol{margin:6px 0 0;padding-left:18px}
.probe li{margin-bottom:6px}
.probe .mini{font-family:var(--f-mono);font-size:11px;color:var(--muted)}

.runs{display:flex;flex-direction:column;gap:8px}
.run{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:10px 12px}
.run .meta{margin-bottom:4px}
.run ul{margin:4px 0 0;padding-left:18px;color:var(--muted);font-size:13px}

.login{max-width:420px;margin:12vh auto 0}
@media (max-width:820px){
  .desk{grid-template-columns:minmax(0,1fr)}
  article.note{position:static;max-height:none}
  .desk.reading .list{display:none}
  .desk:not(.reading) article.note{display:none}
  .note .back{display:inline-flex;margin-bottom:10px}
  .grid2{grid-template-columns:1fr}
  .filters{width:100%}
  .filters input[type=search]{flex:1 1 100%;width:auto}
  .filters select{flex:1 1 40%}
  .views{gap:14px}
  .views button{font-size:17px}
  .brand h1{font-size:28px}
}
</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="brand">
      <h1>Cablera Deportiva<small>v{{VERSION}}</small></h1>
      <p>Comunicados oficiales capturados solos · la IA redacta solo cuando la pedís · estilo Olé</p>
    </div>
    <div class="ticker" id="ticker"></div>
  </header>

  <section class="panel login" id="login" hidden>
    <h2>Entrar</h2>
    <p id="login-msg">Ingresá la clave personal de la Cablera (la que está en CABLERA_CLAVE, en Vercel). Queda guardada en este dispositivo.</p>
    <label>Clave<input id="login-clave" type="password" autocomplete="current-password"></label>
    <div class="foot"><button class="btn primary" id="login-go" type="button">Entrar</button><span id="login-err" class="err"></span></div>
  </section>

  <main id="app" hidden>
    <nav class="views" aria-label="Secciones" id="views">
      <button type="button" data-view="bandeja" aria-pressed="true">Bandeja<span class="n" id="vn-bandeja"></span></button>
      <button type="button" data-view="fuentes" aria-pressed="false">Fuentes<span class="n" id="vn-fuentes"></span></button>
      <button type="button" data-view="actividad" aria-pressed="false">Actividad</button>
    </nav>

    <!-- BANDEJA -->
    <section id="v-bandeja" style="display:flex;flex-direction:column;gap:14px;margin-top:14px">
      <div class="toolbar">
        <div class="tabs" role="group" aria-label="Estado" id="tabs"></div>
        <div class="filters">
          <select id="f-deporte" aria-label="Deporte"><option value="">Todos los deportes</option></select>
          <select id="f-fuente" aria-label="Fuente"><option value="">Todas las fuentes</option></select>
          <label class="chk"><input type="checkbox" id="f-red"> Solo redactadas</label>
          <input id="f-q" type="search" placeholder="Buscar" aria-label="Buscar">
          <button class="btn" id="btn-pegar" type="button">+ Pegar comunicado</button>
        </div>
      </div>

      <section class="panel" id="pegar" hidden>
        <h2>Redactar desde un comunicado</h2>
        <p>Pegá un comunicado que llegó por mail o WhatsApp. Se suma a la bandeja y, si querés, la IA lo redacta en el momento.</p>
        <label>Texto del comunicado<textarea id="p-texto" placeholder="Pegá acá el texto completo"></textarea></label>
        <div class="grid2">
          <label>Fuente<input id="p-fuente" type="text" placeholder="Ej.: Prensa CABB"></label>
          <label>Link al original (opcional)<input id="p-url" type="url" placeholder="https://"></label>
        </div>
        <div class="foot">
          <label class="chk"><input type="checkbox" id="p-ia" checked> Redactar con IA ahora</label>
          <button class="btn primary" id="p-go" type="button">Sumar a la bandeja</button>
          <button class="btn" id="p-cancel" type="button">Cancelar</button>
          <span id="p-status" class="toast"></span>
        </div>
      </section>

      <div class="desk" id="desk">
        <div class="list" id="list" aria-label="Bandeja"><div class="empty"><strong>Cargando la bandeja</strong>Un momento…</div></div>
        <article class="note" id="note" aria-live="polite"><div class="empty"><strong>Elegí un comunicado</strong>Vas a ver el texto original y el botón para que la IA lo redacte como nota.</div></article>
      </div>
    </section>

    <!-- FUENTES -->
    <section id="v-fuentes" class="sources" hidden style="margin-top:14px"></section>

    <!-- ACTIVIDAD -->
    <section id="v-actividad" hidden style="display:flex;flex-direction:column;gap:14px;margin-top:14px"></section>
  </main>
</div>

<script>
(() => {
  const ESTADOS = [{k:"nueva",label:"Nuevas"},{k:"revision",label:"En revisión"},{k:"copiada",label:"Copiadas"},{k:"descartada",label:"Descartadas"},{k:"todas",label:"Todas"}];
  const ESTADO_TXT = {nueva:"Nueva", revision:"En revisión", copiada:"Copiada", descartada:"Descartada"};
  const ST_TXT = {ok:"Funciona", limitada:"Limitada", caida:"Caída", pausada:"Pausada", "sin probar":"Sin probar"};
  const MET_TXT = {rss:"RSS", river:"API River", premier:"API Premier", web:"Web", pausada:"Pausada"};
  const PRIO = {alta:0, media:1, baja:2};
  const IDIOMA = {en:"inglés", it:"italiano", fr:"francés", pt:"portugués", de:"alemán"};
  const MESES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
  const LS = "cablera_clave";
  const S = {clave:"", cfg:null, items:[], ultima:null, fuentes:[], view:"bandeja", estado:"nueva", deporte:"", fuente:"", red:false, q:"",
             sel:null, cache:{}, busy:{}, probes:{}, editando:null, capturando:false, mostrar:80};
  const $ = id => document.getElementById(id);
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const inline = s => esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  const paras = t => String(t || "").split(/\n{2,}/).map(p => p.trim()).filter(Boolean);
  const plain = s => String(s || "").replace(/\*\*(.+?)\*\*/g, "$1");
  try{ S.clave = localStorage.getItem(LS) || ""; }catch(e){}

  function fecha(v){
    if(!v) return "";
    const m = String(v).match(/^(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}):(\d{2}))?/);
    if(!m) return String(v);
    const d = `${Number(m[3])} ${MESES[Number(m[2])-1]}`;
    return m[4] ? `${d} · ${m[4]}.${m[5]}` : d;
  }
  const ts = n => Date.parse(n.publicado || n.capturado || 0) || 0;

  async function api(path, opts={}){
    const r = await fetch(path, {...opts, headers:{"Content-Type":"application/json","X-Cablera-Clave":S.clave, ...(opts.headers||{})}});
    let data = null; try{ data = await r.json(); }catch(e){}
    if(r.status === 401){ mostrarLogin("La clave no es correcta o cambió. Ingresala de nuevo."); throw new Error("Clave incorrecta"); }
    if(!r.ok) throw new Error((data && data.detail) || `Error ${r.status}`);
    return data;
  }

  // ───────── login
  function mostrarLogin(msg){
    $("app").hidden = true; $("login").hidden = false;
    if(msg) $("login-msg").textContent = msg;
    $("login-clave").focus();
  }
  async function entrar(){
    S.clave = $("login-clave").value.trim();
    $("login-err").textContent = "";
    try{
      await api("/api/login", {method:"POST"});
      try{ localStorage.setItem(LS, S.clave); }catch(e){}
      $("login").hidden = true; arrancar();
    }catch(e){ $("login-err").textContent = e.message; }
  }
  $("login-go").onclick = entrar;
  $("login-clave").addEventListener("keydown", e => { if(e.key === "Enter") entrar(); });

  // ───────── carga
  async function cargarItems(){
    const d = await api("/api/items");
    S.items = d.items; S.ultima = d.ultima_corrida;
    renderDeportes(); renderBandeja(); renderTicker();
  }
  async function cargarFuentes(){ S.fuentes = await api("/api/fuentes"); $("vn-fuentes").textContent = S.fuentes.length || ""; if(S.view==="fuentes") renderFuentes(); renderFuenteSelect(); }
  async function arrancar(){
    $("app").hidden = false;
    try{
      await Promise.all([cargarItems(), cargarFuentes()]);
    }catch(e){ if(e.message !== "Clave incorrecta") $("list").innerHTML = `<div class="empty"><strong>No se pudo cargar</strong>${esc(e.message)}</div>`; }
    setInterval(() => { if(!document.hidden) cargarItems().catch(()=>{}); }, 120000);
  }

  // ───────── bandeja
  function visibles(){
    const q = S.q.trim().toLowerCase();
    return S.items
      .filter(n => S.estado === "todas" || (n.estado || "nueva") === S.estado)
      .filter(n => !S.deporte || n.deporte === S.deporte)
      .filter(n => !S.fuente || n.fuente === S.fuente)
      .filter(n => !S.red || n.nota)
      .filter(n => !q || [n.titulo_original, n.nota && n.nota.titulo, n.fuente, n.resumen, n.codigo].join(" ").toLowerCase().includes(q))
      .sort((a,b) => (PRIO[a.prioridad] ?? 3) - (PRIO[b.prioridad] ?? 3) || ts(b) - ts(a));
  }
  function renderDeportes(){
    const sel = $("f-deporte"), ds = [...new Set(S.items.map(n => n.deporte).filter(Boolean))].sort();
    sel.innerHTML = `<option value="">Todos los deportes</option>` + ds.map(d => `<option ${d===S.deporte?"selected":""}>${esc(d)}</option>`).join("");
    renderFuenteSelect();
  }
  function renderFuenteSelect(){
    const sel = $("f-fuente"), fs = [...new Set(S.items.map(n => n.fuente).filter(Boolean))].sort();
    sel.innerHTML = `<option value="">Todas las fuentes</option>` + fs.map(d => `<option ${d===S.fuente?"selected":""}>${esc(d)}</option>`).join("");
  }
  function renderTabs(){
    const cnt = k => k === "todas" ? S.items.length : S.items.filter(n => (n.estado||"nueva") === k).length;
    $("tabs").innerHTML = ESTADOS.map(e => `<button type="button" data-k="${e.k}" aria-pressed="${S.estado===e.k}">${e.label}<span class="n">${cnt(e.k)}</span></button>`).join("");
    $("vn-bandeja").textContent = cnt("nueva") || "";
  }
  function renderTicker(){
    const u = S.ultima, nuevas = S.items.filter(n => (n.estado||"nueva")==="nueva").length;
    const red = S.items.filter(n => n.nota).length;
    $("ticker").innerHTML = `<span><span class="live"></span>Última captura <b>${u ? esc(fecha(u.fecha)) : "—"}</b></span><span><b>${nuevas}</b> nuevas</span><span><b>${red}</b> redactadas</span>` +
      `<button class="btn sm" id="btn-capturar" type="button" ${S.capturando?"disabled":""}>${S.capturando?'<span class="spin"></span> Capturando…':"↻ Capturar ahora"}</button>`;
  }
  function renderList(){
    const list = $("list"), vs = visibles();
    if(!S.items.length){
      list.innerHTML = `<div class="empty"><strong>La bandeja está vacía</strong>Tocá “↻ Capturar ahora” para leer las fuentes, o pegá un comunicado.</div>`; return;
    }
    if(!vs.length){ list.innerHTML = `<div class="empty"><strong>Nada por acá</strong>No hay comunicados con estos filtros. Probá con “Todas”.</div>`; return; }
    list.innerHTML = vs.slice(0, S.mostrar).map(n => `
      <button type="button" class="item" data-id="${esc(n.id)}" data-p="${esc(n.prioridad)}" data-estado="${esc(n.estado||"nueva")}" aria-current="${S.sel===n.id}">
        <div class="meta"><span class="pill">${esc(n.deporte)}</span>${n.nota?`<span class="pill ia">✦ Redactada</span>`:""}<span>${esc(n.codigo||"")}</span><span>${esc(fecha(n.publicado)) || "sin fecha"}</span>${(n.estado&&n.estado!=="nueva")?`<span class="state" data-s="${esc(n.estado)}">${ESTADO_TXT[n.estado]||""}</span>`:""}${(n.aviso||(n.nota&&n.nota.alerta))?`<span class="flag">Verificar</span>`:""}</div>
        <h3>${esc(n.nota ? n.nota.titulo : n.titulo_original)}</h3>
        <div class="src">${esc(n.fuente)}${n.titulo_fuente?` · traducido del ${IDIOMA[n.idioma]||"original"}`:""}${n.motivo?` · ${esc(n.motivo)}`:""}</div>
      </button>`).join("") + (vs.length > S.mostrar ? `<button class="btn more" id="b-more" type="button">Ver ${vs.length - S.mostrar} más</button>` : "");
  }

  function opcionesMotor(){
    const ms = (S.cfg && S.cfg.motores) || [];
    return `<option value="auto">Automático · gratis primero</option>` + ms.map(m => `<option value="${esc(m.id)}">${esc(m.nombre)}${m.id==="claude"?" (pago)":""}</option>`).join("");
  }

  function renderNote(){
    const el = $("note"), n = S.cache[S.sel], lite = S.items.find(x => x.id === S.sel);
    $("desk").classList.toggle("reading", !!S.sel);
    if(!S.sel || !lite){ el.innerHTML = `<div class="empty"><strong>Elegí un comunicado</strong>Vas a ver el texto original y el botón para que la IA lo redacte como nota.</div>`; return; }
    if(!n){ el.innerHTML = `<button type="button" class="btn back" id="b-back">← Volver</button><div class="empty"><strong><span class="spin"></span> Abriendo</strong></div>`; return; }
    const est = n.estado || "nueva", nota = n.nota, busy = S.busy[n.id];
    const kicker = `<div class="kicker"><span class="pill">${esc(n.deporte)}</span><span>${esc(n.codigo||"")}</span>
        <span>Fuente: ${n.url?`<a href="${esc(n.url)}" target="_blank" rel="noopener">${esc(n.fuente)} ↗</a>`:esc(n.fuente)}</span>
        <span>Publicado ${esc(fecha(n.publicado)) || "sin fecha"}</span><span class="state" data-s="${esc(est)}">${ESTADO_TXT[est]}</span></div>`;
    const avisos = [n.aviso, nota && nota.alerta].filter(Boolean);
    const alert = avisos.length ? `<div class="alert"><b>Verificar antes de publicar:</b> ${avisos.map(inline).join(" · ")}</div>` : "";
    const estadoBtns = `
        ${est!=="revision" && est!=="copiada" ? `<button type="button" class="btn" data-set="revision">Tomar para revisar</button>`:""}
        ${est!=="descartada" ? `<button type="button" class="btn" data-set="descartada">Descartar</button>`:""}
        ${est!=="nueva" ? `<button type="button" class="btn" data-set="nueva">Volver a Nuevas</button>`:""}`;
    const original = `<div class="cuerpo orig">${paras(n.texto).map(p => `<p>${inline(p).replace(/\n/g,"<br>")}</p>`).join("") || "<p><em>No se pudo leer el texto. Abrí el original.</em></p>"}</div>`;
    const iaOff = !(S.cfg && S.cfg.ia);
    const iabox = (titulo, boton) => `
      <div class="iabox">
        <p>${titulo}</p>
        <div class="row"><input id="ia-ind" type="text" placeholder="Indicaciones opcionales (ej.: enfocá en la lesión de X)" ${iaOff?"disabled":""}></div>
        <div class="row">
          <button type="button" class="btn ia" id="b-red" ${busy||iaOff?"disabled":""}>${busy?'<span class="spin"></span> Redactando…':boton}</button>
          <select id="ia-motor" aria-label="Motor de IA" ${iaOff?"disabled":""}>${opcionesMotor()}</select>
          <span id="ia-err" class="err">${iaOff?"La IA no está configurada en Vercel (falta al menos una clave de motor).":""}</span>
        </div>
      </div>`;
    if(!nota){
      el.innerHTML = `<button type="button" class="btn back" id="b-back">← Volver a la bandeja</button>${kicker}${alert}
        <div class="label">Comunicado original${n.titulo_fuente?` · título traducido del ${IDIOMA[n.idioma]||"original"}`:""}</div>
        <h2>${esc(n.titulo_original)}</h2>
        ${n.titulo_fuente?`<div class="firma" style="margin-top:-4px">Título en la fuente: ${esc(n.titulo_fuente)}</div>`:""}
        ${iabox("Todavía no se gastó IA en este comunicado. Si te sirve, pedí la nota estilo Olé: título, alternativas, bajada y cuerpo.", "✦ Redactar nota")}
        ${original}
        <div class="actions">
          <button type="button" class="btn" id="b-copy-o">Copiar texto original</button>
          <span class="toast" id="b-toast" role="status"></span><span class="sp"></span>${estadoBtns}
        </div>
        <textarea id="copy-fallback" readonly hidden style="width:100%;min-height:160px;margin-top:12px;font-family:var(--f-mono);font-size:12px"></textarea>`;
      return;
    }
    el.innerHTML = `<button type="button" class="btn back" id="b-back">← Volver a la bandeja</button>${kicker}${alert}
      <h2>${esc(nota.titulo)}</h2>
      ${(nota.titulos_alternativos||[]).length?`<div class="alts" aria-label="Títulos alternativos">${nota.titulos_alternativos.map(t=>`<button type="button" data-alt="${esc(t)}" title="Copiar este título">${esc(t)}</button>`).join("")}</div>`:""}
      <p class="bajada">${esc(nota.bajada)}</p>
      <div class="cuerpo">${paras(nota.cuerpo).map(p => `<p>${inline(p).replace(/\n/g,"<br>")}</p>`).join("")}</div>
      ${(nota.etiquetas||[]).length?`<div class="tags">${nota.etiquetas.map(t=>`<span>${esc(t)}</span>`).join("")}</div>`:""}
      <div class="firma">${nota.motor?`Hecho con IA · ${esc(nota.motor)}`:"Redactada en la Cablera anterior"}${nota.generada?` · ${esc(fecha(nota.generada))}`:""}</div>
      <div class="actions">
        <button type="button" class="btn primary" id="b-copy">Copiar nota completa</button>
        <button type="button" class="btn" id="b-copy-t">Copiar título</button>
        <span class="toast" id="b-toast" role="status"></span><span class="sp"></span>${estadoBtns}
      </div>
      <textarea id="copy-fallback" readonly hidden style="width:100%;min-height:160px;margin-top:12px;font-family:var(--f-mono);font-size:12px"></textarea>
      ${n.texto ? `<details class="orig-box"><summary>Comunicado original y otra versión</summary>
        ${iabox("¿No te convence? Pedí otra versión (se vuelve a usar IA).", "↻ Otra versión")}
        <h3 style="font-family:var(--f-display);font-size:22px;margin:8px 0">${esc(n.titulo_original)}</h3>${original}</details>` : ""}`;
  }
  function renderBandeja(){ renderTabs(); renderList(); renderNote(); renderTicker(); }

  async function abrir(id){
    S.sel = id; renderList(); renderNote();
    if(matchMedia("(max-width:820px)").matches) window.scrollTo({top:0});
    if(!S.cache[id]){
      try{ S.cache[id] = await api(`/api/items/${encodeURIComponent(id)}`); }
      catch(e){ $("note").innerHTML = `<div class="empty"><strong>No se pudo abrir</strong>${esc(e.message)}</div>`; return; }
      if(S.sel === id) renderNote();
    }
  }
  function actualizarLite(full){
    const i = S.items.findIndex(x => x.id === full.id);
    const lite = {...(S.items[i]||{}), ...full, resumen:(full.texto||"").slice(0,260),
      nota: full.nota ? {titulo:full.nota.titulo, bajada:full.nota.bajada, alerta:full.nota.alerta, motor:full.nota.motor} : null};
    delete lite.texto;
    if(i >= 0) S.items[i] = lite; else S.items.unshift(lite);
    S.cache[full.id] = full;
  }
  async function redactar(){
    const id = S.sel; if(!id || S.busy[id]) return;
    const motor = ($("ia-motor")||{}).value || "auto", ind = ($("ia-ind")||{}).value || "";
    S.busy[id] = true; renderNote();
    try{
      const full = await api(`/api/items/${encodeURIComponent(id)}/redactar`, {method:"POST", body:JSON.stringify({motor, indicaciones:ind})});
      actualizarLite(full); delete S.busy[id]; renderBandeja();
    }catch(e){ delete S.busy[id]; renderNote(); const er = $("ia-err"); if(er) er.textContent = e.message; }
  }
  async function setEstado(estado){
    const id = S.sel, n = S.cache[id]; if(!n) return;
    try{
      await api(`/api/items/${encodeURIComponent(id)}/estado`, {method:"POST", body:JSON.stringify({estado})});
      n.estado = estado; const l = S.items.find(x => x.id === id); if(l) l.estado = estado; renderBandeja();
    }catch(e){ const t = $("b-toast"); if(t){ t.className = "err"; t.textContent = e.message; } }
  }

  function textoPlano(n){
    const no = n.nota;
    return [no.titulo, "", no.bajada, "", ...paras(no.cuerpo).flatMap(p => [plain(p), ""]),
      `Fuente: ${n.fuente}${n.url?` (${n.url})`:""}`, (no.etiquetas||[]).length ? `Etiquetas: ${no.etiquetas.join(", ")}` : ""].join("\n").trim();
  }
  function textoHtml(n){
    const no = n.nota;
    return `<h1>${esc(no.titulo)}</h1><h2>${esc(no.bajada)}</h2>` + paras(no.cuerpo).map(p => `<p>${inline(p).replace(/\n/g,"<br>")}</p>`).join("") +
      `<p><em>Fuente: ${n.url?`<a href="${esc(n.url)}">${esc(n.fuente)}</a>`:esc(n.fuente)}</em></p>`;
  }
  async function copiar(txt, html){
    try{
      if(html && window.ClipboardItem){ await navigator.clipboard.write([new ClipboardItem({"text/plain":new Blob([txt],{type:"text/plain"}),"text/html":new Blob([html],{type:"text/html"})})]); }
      else await navigator.clipboard.writeText(txt);
      return true;
    }catch(e){ try{ await navigator.clipboard.writeText(txt); return true; }catch(e2){ return false; } }
  }
  function fallback(txt){
    const ta = $("copy-fallback"); if(!ta) return;
    ta.hidden = false; ta.value = txt; ta.focus(); ta.select();
    $("b-toast").textContent = "Seleccioné el texto: copialo con Ctrl+C / Cmd+C";
  }

  async function capturarAhora(){
    if(S.capturando) return;
    S.capturando = true; renderTicker();
    let c = null;
    try{
      c = await api("/api/capturar", {method:"POST"});
      S.ultima = c; await cargarItems(); await cargarFuentes();
    }catch(e){ alert("No se pudo capturar: " + e.message); }
    S.capturando = false; renderTicker();
    if(c) alertaCorrida(c);
    if(S.view === "actividad") renderActividad();
  }
  function alertaCorrida(c){
    const t = $("ticker"); const s = document.createElement("span"); s.className = c.errores && c.errores.length ? "err" : "toast";
    s.textContent = `${c.nuevas} nuevas${c.descartadas?`, ${c.descartadas} descartadas solas`:""}${c.errores&&c.errores.length?`, ${c.errores.length} fuentes con error`:""}`;
    t.appendChild(s); setTimeout(() => s.remove(), 9000);
  }

  // ───────── pegar
  async function pegar(){
    const st = $("p-status"), go = $("p-go");
    const body = {texto:$("p-texto").value, fuente:$("p-fuente").value || "Comunicado", url:$("p-url").value, redactar:$("p-ia").checked};
    if(body.texto.trim().length < 80){ st.className = "err"; st.textContent = "Pegá el comunicado completo (al menos un párrafo)."; return; }
    go.disabled = true; st.className = "toast"; st.innerHTML = body.redactar ? '<span class="spin"></span> Redactando…' : "Guardando…";
    try{
      const full = await api("/api/pegar", {method:"POST", body:JSON.stringify(body)});
      actualizarLite(full); $("p-texto").value = ""; $("p-url").value = ""; st.textContent = "Listo: está en Nuevas.";
      S.estado = "nueva"; renderDeportes(); abrir(full.id); renderBandeja();
    }catch(e){ st.className = "err"; st.textContent = e.message; }
    finally{ go.disabled = false; }
  }

  // ───────── fuentes
  function renderFuentes(){
    const el = $("v-fuentes"), fs = S.fuentes;
    const cnt = s => fs.filter(f => f.estado === s).length;
    const cats = [...new Set(fs.map(f => f.categoria || "Otras"))];
    const ult = f => f.ultimo ? `${f.ultimo.ok?"":"⚠ "}${esc(f.ultimo.mensaje||"")} <span class="mini">(${esc(fecha(f.ultimo.fecha))})</span>` : "";
    el.innerHTML = `<div class="sum"><span><b>${fs.length}</b> fuentes</span><span><b>${cnt("ok")}</b> funcionan</span><span><b>${cnt("limitada")}</b> limitadas</span><span><b>${cnt("caida")}</b> caídas</span><span><b>${cnt("pausada")}</b> pausadas</span><span class="sp" style="flex:1"></span><button class="btn primary" type="button" data-fedit="__nueva">+ Agregar fuente</button></div>
      <div id="f-form-slot"></div>` +
      cats.map(c => `<div class="sgroup"><h3>${esc(c)}</h3><div class="stable"><table><thead><tr><th>Fuente</th><th>Método</th><th>Estado</th><th>Última lectura y detalle</th><th></th></tr></thead><tbody>${
        fs.filter(f => (f.categoria || "Otras") === c).map(f => `<tr><td class="name"><a href="${esc(f.url)}" target="_blank" rel="noopener">${esc(f.nombre)}</a>${f.filtro?`<div class="mini" style="font-size:11px;color:var(--muted)">con filtro</div>`:""}</td>
          <td><span class="method">${esc(MET_TXT[f.metodo]||f.metodo)}</span></td>
          <td><span class="st" data-s="${esc(f.estado)}">${ST_TXT[f.estado]||esc(f.estado)}</span></td>
          <td class="det">${ult(f)}${f.ultimo?"<br>":""}${esc(f.detalle)}${S.probes[f.id]?renderProbe(S.probes[f.id]):""}</td>
          <td class="acc"><button class="btn sm" type="button" data-fprobar="${esc(f.id)}" ${f.metodo==="pausada"?"disabled":""}>Probar</button> <button class="btn sm" type="button" data-fedit="${esc(f.id)}">Editar</button></td></tr>`).join("")
      }</tbody></table></div></div>`).join("");
    if(S.editando) renderForm();
  }
  function renderProbe(p){
    if(p.cargando) return `<div class="probe"><span class="spin"></span> Leyendo la fuente…</div>`;
    if(!p.ok) return `<div class="probe err">✕ ${esc(p.mensaje)}</div>`;
    return `<div class="probe"><b>${p.encontradas} links encontrados</b> · primeras ${p.items.length} notas leídas en ${p.segundos} s (no se guardó nada)<ol>${
      p.items.map(i => `<li><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.titulo)}</a><div class="mini">${esc(fecha(i.publicado))||"sin fecha"} · ${i.largo} caracteres${i.estado==="descartada"?` · ${esc(i.motivo)}`:""}${i.aviso?` · ${esc(i.aviso)}`:""}</div><div class="mini">${esc(i.inicio)}…</div></li>`).join("") || "<li>No encontró notas: revisá el patrón o el filtro.</li>"
    }</ol></div>`;
  }
  async function probar(id){
    S.probes[id] = {cargando:true}; renderFuentes();
    try{ S.probes[id] = await api(`/api/fuentes/${encodeURIComponent(id)}/probar`, {method:"POST"}); }
    catch(e){ S.probes[id] = {ok:false, mensaje:e.message}; }
    await cargarFuentes();
  }
  function renderForm(){
    const slot = $("f-form-slot"); if(!slot) return;
    const f = S.editando === "__nueva" ? {id:"",nombre:"",categoria:"Clubes",deporte:"Fútbol",metodo:"web",url:"",patron:"",filtro:"",idioma:"es",detalle:"",orden:500} : S.fuentes.find(x => x.id === S.editando);
    if(!f){ slot.innerHTML = ""; return; }
    const opt = (v, arr) => arr.map(([k,l]) => `<option value="${k}" ${k===v?"selected":""}>${l}</option>`).join("");
    slot.innerHTML = `<section class="panel" id="f-form">
      <h2>${f.id ? "Editar " + esc(f.nombre) : "Nueva fuente"}</h2>
      <div class="grid2">
        <label>Nombre<input id="ff-nombre" value="${esc(f.nombre)}"></label>
        <label>Categoría<input id="ff-categoria" value="${esc(f.categoria)}" list="ff-cats"></label>
        <label>Método<select id="ff-metodo">${opt(f.metodo,[["web","Web (scraping)"],["rss","RSS"],["river","API de River"],["premier","API de la Premier"],["pausada","Pausada (no se lee)"]])}</select></label>
        <label>Deporte por defecto<input id="ff-deporte" value="${esc(f.deporte)}"></label>
      </div>
      <label>Dirección (del listado de noticias o del feed RSS)<input id="ff-url" value="${esc(f.url)}" placeholder="https://"></label>
      <div class="grid2">
        <label>Patrón de los links de notas <span class="hint">Solo Web. Parte de la dirección que tienen todas las notas, ej. <code>/noticias/</code>. Vacío: busca un RSS o links con títulos largos.</span><input id="ff-patron" value="${esc(f.patron)}"></label>
        <label>Filtro (opcional) <span class="hint">Solo entran notas que mencionen alguna de estas palabras, separadas por <code>|</code>. Ej.: <code>colapinto|alpine</code></span><input id="ff-filtro" value="${esc(f.filtro)}"></label>
        <label>Idioma<select id="ff-idioma">${opt(f.idioma||"es",[["es","Español"],["en","Inglés"],["it","Italiano"],["fr","Francés"],["pt","Portugués"]])}</select></label>
        <label>Orden<input id="ff-orden" type="number" value="${esc(f.orden)}"></label>
      </div>
      <label>Detalle para los editores<input id="ff-detalle" value="${esc(f.detalle)}"></label>
      <datalist id="ff-cats">${[...new Set(S.fuentes.map(x=>x.categoria))].map(c=>`<option value="${esc(c)}">`).join("")}</datalist>
      <div class="foot"><button class="btn primary" type="button" id="ff-save">Guardar</button><button class="btn" type="button" id="ff-cancel">Cancelar</button>
        ${f.id?`<span class="sp" style="flex:1"></span><button class="btn" type="button" id="ff-del">Borrar fuente</button>`:""}<span id="ff-err" class="err"></span></div>
    </section>`;
    slot.scrollIntoView({behavior:"smooth", block:"start"});
  }
  async function guardarFuente(){
    const f = S.editando === "__nueva" ? {} : S.fuentes.find(x => x.id === S.editando) || {};
    const body = {id:f.id||"", nombre:$("ff-nombre").value.trim(), categoria:$("ff-categoria").value.trim()||"Otras", metodo:$("ff-metodo").value,
      deporte:$("ff-deporte").value.trim()||"Fútbol", url:$("ff-url").value.trim(), patron:$("ff-patron").value.trim(), filtro:$("ff-filtro").value.trim(),
      idioma:$("ff-idioma").value, orden:Number($("ff-orden").value)||500, detalle:$("ff-detalle").value.trim()};
    if(!body.nombre || !/^https?:\/\//.test(body.url)){ $("ff-err").textContent = "Completá el nombre y una dirección que empiece con https://"; return; }
    try{ const g = await api("/api/fuentes", {method:"POST", body:JSON.stringify(body)}); S.editando = null; await cargarFuentes(); probar(g.id); }
    catch(e){ $("ff-err").textContent = e.message; }
  }
  async function borrarFuente(){
    const f = S.fuentes.find(x => x.id === S.editando); if(!f) return;
    if(!confirm(`¿Borrar la fuente ${f.nombre}? Los comunicados ya capturados quedan.`)) return;
    try{ await api(`/api/fuentes/${encodeURIComponent(f.id)}`, {method:"DELETE"}); S.editando = null; await cargarFuentes(); }
    catch(e){ $("ff-err").textContent = e.message; }
  }

  // ───────── actividad
  async function renderActividad(){
    const el = $("v-actividad");
    el.innerHTML = `<div class="empty"><strong><span class="spin"></span> Cargando</strong></div>`;
    let runs = [];
    try{ runs = await api("/api/corridas"); }catch(e){}
    const c = S.cfg || {};
    el.innerHTML = `
      ${c.almacen_persistente ? "" : `<div class="alert"><b>Atención:</b> no hay base de datos conectada (${esc(c.almacen||"")}). Lo que se capture se pierde. En Vercel: Storage → Create → Upstash Redis → conectar al proyecto → Redeploy.</div>`}
      <section class="panel">
        <h2>Configuración</h2>
        <p>Base de datos: <b>${esc(c.almacen||"")}</b> · IA: <b>${esc(c.cadena||"sin configurar")}</b> · versión ${esc(c.version||"")}</p>
        <p>La captura automática corre cada 2 horas desde GitHub Actions y no usa IA. La IA solo se usa cuando tocás “✦ Redactar nota”.</p>
        <div class="foot"><button class="btn" id="b-importar" type="button">Importar notas de la Cablera anterior</button><span id="imp-st" class="toast"></span>
        <span class="sp" style="flex:1"></span><button class="btn" id="b-salir" type="button">Olvidar clave en este dispositivo</button></div>
      </section>
      <h3 style="font-family:var(--f-display);font-size:22px;margin:4px 0 0;text-transform:uppercase">Últimas capturas</h3>
      <div class="runs">${runs.length ? runs.map(r => `<div class="run">
        <div class="meta"><span class="pill">${r.origen==="auto"?"Automática":"Manual"}</span><span>${esc(fecha(r.fecha))}</span><span>${r.fuentes} fuentes · ${r.segundos} s</span></div>
        <b>${r.nuevas} nuevas</b>${r.descartadas?` · ${r.descartadas} descartadas solas`:""}${(r.errores||[]).length?` · <span class="err">${r.errores.length} con error</span>`:""}${(r.sin_tiempo||[]).length?` · sin tiempo: ${esc(r.sin_tiempo.join(", "))}`:""}
        ${(r.titulos||[]).length||(r.errores||[]).length?`<ul>${(r.titulos||[]).map(t=>`<li>${esc(t)}</li>`).join("")}${(r.errores||[]).map(e=>`<li class="err">${esc(e.fuente)}: ${esc(e.mensaje)}</li>`).join("")}</ul>`:""}
      </div>`).join("") : `<div class="empty"><strong>Todavía no hubo capturas</strong>Tocá “↻ Capturar ahora”.</div>`}</div>`;
  }

  // ───────── vistas y eventos
  function setView(v){
    S.view = v;
    document.querySelectorAll("#views button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.view === v)));
    $("v-bandeja").hidden = v !== "bandeja"; $("v-fuentes").hidden = v !== "fuentes"; $("v-actividad").hidden = v !== "actividad";
    $("v-bandeja").style.display = v === "bandeja" ? "flex" : "none";
    $("v-actividad").style.display = v === "actividad" ? "flex" : "none";
    if(v === "fuentes") renderFuentes();
    if(v === "actividad") renderActividad();
  }

  document.addEventListener("click", async ev => {
    const t = ev.target.closest("button"); if(!t) return;
    if(t.closest("#views")){ setView(t.dataset.view); return; }
    if(t.closest("#tabs")){ S.estado = t.dataset.k; S.sel = null; S.mostrar = 80; renderBandeja(); return; }
    if(t.classList.contains("item")){ abrir(t.dataset.id); return; }
    if(t.id === "b-more"){ S.mostrar += 80; renderList(); return; }
    if(t.id === "btn-capturar"){ capturarAhora(); return; }
    if(t.id === "b-back"){ S.sel = null; renderList(); renderNote(); return; }
    if(t.id === "b-red"){ redactar(); return; }
    const n = S.cache[S.sel];
    if(t.id === "b-copy" && n){
      const ok = await copiar(textoPlano(n), textoHtml(n));
      if(ok){ $("b-toast").textContent = "Nota copiada. Pegala en el CMS."; if((n.estado||"nueva") !== "copiada") setEstado("copiada"); }
      else fallback(textoPlano(n));
      return;
    }
    if(t.id === "b-copy-t" && n){ const ok = await copiar(n.nota.titulo); if(ok) $("b-toast").textContent = "Título copiado"; else fallback(n.nota.titulo); return; }
    if(t.dataset.alt){ const ok = await copiar(t.dataset.alt); const to = $("b-toast"); if(to) to.textContent = ok ? "Título alternativo copiado" : ""; return; }
    if(t.id === "b-copy-o" && n){ const txt = n.titulo_original + "\n\n" + plain(n.texto); const ok = await copiar(txt); if(ok) $("b-toast").textContent = "Texto original copiado"; else fallback(txt); return; }
    if(t.dataset.set && n){ setEstado(t.dataset.set); return; }
    if(t.id === "btn-pegar"){ $("pegar").hidden = false; $("p-texto").focus(); return; }
    if(t.id === "p-cancel"){ $("pegar").hidden = true; $("p-status").textContent = ""; return; }
    if(t.id === "p-go"){ pegar(); return; }
    if(t.dataset.fprobar){ probar(t.dataset.fprobar); return; }
    if(t.dataset.fedit){ S.editando = t.dataset.fedit; renderForm(); return; }
    if(t.id === "ff-cancel"){ S.editando = null; renderForm(); return; }
    if(t.id === "ff-save"){ guardarFuente(); return; }
    if(t.id === "ff-del"){ borrarFuente(); return; }
    if(t.id === "b-importar"){
      const st = $("imp-st"); st.textContent = "Importando…";
      try{ const r = await api("/api/importar", {method:"POST"}); st.textContent = `${r.importadas} notas importadas${r.ya_estaban?` (${r.ya_estaban} ya estaban)`:""}.`; await cargarItems(); }
      catch(e){ st.className = "err"; st.textContent = e.message; }
      return;
    }
    if(t.id === "b-salir"){ try{ localStorage.removeItem(LS); }catch(e){} S.clave = ""; mostrarLogin("Clave olvidada en este dispositivo."); return; }
  });
  $("f-deporte").addEventListener("change", e => { S.deporte = e.target.value; renderList(); });
  $("f-fuente").addEventListener("change", e => { S.fuente = e.target.value; renderList(); });
  $("f-red").addEventListener("change", e => { S.red = e.target.checked; renderList(); });
  $("f-q").addEventListener("input", e => { S.q = e.target.value; renderList(); });

  (async () => {
    try{ S.cfg = await (await fetch("/api/config")).json(); }catch(e){ S.cfg = {}; }
    if(S.cfg && S.cfg.clave_configurada === false){
      $("login").hidden = false; $("login-msg").textContent = "Falta configurar CABLERA_CLAVE en Vercel (Settings → Environment Variables) y hacer Redeploy.";
      $("login-go").disabled = true; return;
    }
    if(!S.clave){ mostrarLogin(); return; }
    arrancar();
  })();
})();
</script>
</body>
</html>
"""

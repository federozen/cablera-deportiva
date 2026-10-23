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
/* navegación principal */
.nav{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) auto;gap:8px;align-items:stretch}
.nav .tab{display:flex;flex-direction:column;align-items:flex-start;gap:2px;text-align:left;border:1px solid var(--line);background:var(--surface);border-radius:10px;padding:10px 14px;cursor:pointer;min-width:0}
.nav .tab b{font-family:var(--f-display);font-size:21px;font-weight:600;letter-spacing:.02em;text-transform:uppercase;line-height:1.05;display:flex;gap:8px;align-items:baseline}
.nav .tab b .n{font-family:var(--f-mono);font-size:12px;font-weight:500;background:var(--accent);color:var(--on-accent);border-radius:999px;padding:0 7px;letter-spacing:0}
.nav .tab b .n:empty{display:none}
.nav .tab small{color:var(--muted);font-size:12px;line-height:1.3}
.nav .tab[aria-pressed="true"]{border-color:var(--ink);box-shadow:inset 0 -3px 0 var(--accent)}
.nav .help{border:1px solid var(--line);background:var(--surface);border-radius:10px;padding:0 14px;cursor:pointer;font-weight:600;color:var(--muted)}
.ayuda{background:var(--surface);border:1px solid var(--accent);border-radius:10px;padding:14px 18px;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px 20px}
.ayuda h3{grid-column:1/-1;margin:0;font-family:var(--f-display);font-size:22px;text-transform:uppercase}
.ayuda div{font-size:13px;color:var(--muted)}
.ayuda div b{display:block;color:var(--ink);font-size:14px;margin-bottom:2px}
.ayuda .x{grid-column:1/-1;justify-self:start}
/* barra de la bandeja */
.bar{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px 12px;display:flex;flex-direction:column;gap:10px}
.bar .row{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:flex-end}
.fld{display:flex;flex-direction:column;gap:3px;font-size:11px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);min-width:0}
.fld select{width:200px;max-width:100%}
.fld select,.fld input[type=search]{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:6px 9px;font-size:14px;font-weight:400;letter-spacing:0;text-transform:none;color:var(--ink);min-width:0}
.fld input[type=search]{width:220px}
.bar .sp{flex:1}
.bar .toggle{display:none}
.linkbtn{border:0;background:none;color:var(--accent);cursor:pointer;padding:6px 0;font-size:13px;font-weight:500}
.leyenda{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:12px;color:var(--muted);align-items:center}
.leyenda i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
.resumen-filtro{font-size:13px;color:var(--muted)}
.resumen-filtro b{color:var(--ink)}
/* grupos */
details.grupo{display:flex;flex-direction:column;gap:8px}
details.grupo>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:8px;padding:6px 2px;font-family:var(--f-display);font-size:19px;font-weight:600;text-transform:uppercase;letter-spacing:.02em;border-bottom:2px solid var(--ink)}
details.grupo>summary::-webkit-details-marker{display:none}
details.grupo>summary::before{content:"▾";font-size:14px;color:var(--muted);transition:transform .15s}
details.grupo:not([open])>summary::before{transform:rotate(-90deg)}
details.grupo>summary .n{font-family:var(--f-mono);font-size:12px;font-weight:400;color:var(--muted)}
details.grupo>summary .alta{font-family:var(--f-ui);font-size:11px;font-weight:600;color:var(--alta);text-transform:none;letter-spacing:0}
details.grupo .items{display:flex;flex-direction:column;gap:8px;margin-top:8px}
.tema{font-family:var(--f-ui);font-size:11px;font-weight:600;color:var(--ink);border:1px solid var(--line);border-radius:4px;padding:0 6px}
@media (max-width:820px){
  .nav{grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
  .nav .tab{padding:8px 10px}
  .nav .tab small{display:none}
  .nav .tab b{font-size:15px;flex-wrap:wrap;gap:4px}
  .bar .toggle{display:inline-flex}
  .bar:not(.abierta) .row.mas{display:none}
  .fld select{width:100%}
  .nav .help{grid-column:1/-1;padding:8px}
  .fld{flex:1 1 45%}
  .fld input[type=search]{width:100%}
  .fld.q{flex:1 1 100%}
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
    <nav class="nav" aria-label="Secciones" id="views">
      <button type="button" class="tab" data-view="bandeja" aria-pressed="true"><b>Bandeja <span class="n" id="vn-bandeja"></span></b><small>Los comunicados capturados. Elegí uno y pedí la nota.</small></button>
      <button type="button" class="tab" data-view="fuentes" aria-pressed="false"><b>Fuentes <span class="n" id="vn-fuentes" style="background:var(--line);color:var(--ink)"></span></b><small>De dónde se capturan, si funcionan y cómo agregar más.</small></button>
      <button type="button" class="tab" data-view="actividad" aria-pressed="false"><b>Actividad</b><small>Cada captura, errores, notas viejas y ajustes.</small></button>
      <button type="button" class="help" id="b-ayuda" aria-expanded="false">? Cómo se usa</button>
    </nav>
    <section class="ayuda" id="ayuda" hidden>
      <h3>Cómo se usa la Cablera</h3>
      <div><b>1 · Llegan solos</b>Cada 2 horas se leen las fuentes oficiales y los comunicados nuevos caen en <i>Nuevas</i>. También podés tocar <i>↻ Capturar ahora</i>.</div>
      <div><b>2 · Elegís</b>Ordená por <i>Más recientes</i> o <i>Más importantes</i>, agrupá por tema (Boca, River, Selección, Tenis…) y filtrá por período, deporte o fuente.</div>
      <div><b>3 · Pedís la nota</b>Abrí un comunicado y tocá <i>✦ Redactar nota</i>: la IA arma título, bajada y cuerpo estilo Olé. Solo ahí se usa IA.</div>
      <div><b>4 · Al CMS</b><i>Copiar nota completa</i> la pasa al portapapeles con formato y la marca como <i>Copiada</i>. Lo que no sirve, <i>Descartar</i>.</div>
      <div><b>Colores</b>La barrita de la izquierda: <span style="color:var(--alta)">roja</span> = prioridad alta (Selección, grandes, lesiones, sanciones, finales), <span style="color:var(--media)">amarilla</span> = media, gris = baja.</div>
      <div><b>Verificar</b>La etiqueta amarilla avisa que hay algo para chequear: sin fecha en la fuente, poco texto, una cita traducida…</div>
      <button class="btn sm x" type="button" id="b-ayuda-x">Entendido</button>
    </section>

    <!-- BANDEJA -->
    <section id="v-bandeja" style="display:flex;flex-direction:column;gap:14px;margin-top:14px">
      <div class="bar">
        <div class="row">
          <div class="tabs" role="group" aria-label="Estado" id="tabs"></div>
          <span class="sp"></span>
          <button class="btn" id="btn-pegar" type="button">+ Pegar comunicado</button>
        </div>
        <button class="btn sm toggle" type="button" id="b-filtros" aria-expanded="false">Ordenar y filtrar ▾</button>
        <div class="row mas">
          <label class="fld">Ordenar<select id="f-orden">
            <option value="recientes">Más recientes primero</option>
            <option value="prioridad">Más importantes primero</option>
            <option value="viejas">Más viejas primero</option></select></label>
          <label class="fld">Agrupar<select id="f-grupo">
            <option value="">Sin agrupar</option>
            <option value="tema">Por tema (club, Selección, deporte)</option>
            <option value="deporte">Por deporte</option>
            <option value="fuente">Por fuente</option>
            <option value="dia">Por día</option></select></label>
          <label class="fld">Período<select id="f-periodo">
            <option value="6">Últimas 6 horas</option>
            <option value="24">Últimas 24 horas</option>
            <option value="72">Últimos 3 días</option>
            <option value="168">Últimos 7 días</option>
            <option value="0">Todo</option></select></label>
          <label class="fld">Tema<select id="f-tema"><option value="">Todos</option></select></label>
          <label class="fld">Deporte<select id="f-deporte"><option value="">Todos</option></select></label>
          <label class="fld">Fuente<select id="f-fuente"><option value="">Todas</option></select></label>
          <label class="fld q">Buscar<input id="f-q" type="search" placeholder="Palabra, club, jugador…"></label>
        </div>
        <div class="row mas">
          <label class="chk"><input type="checkbox" id="f-red"> Solo las que ya tienen nota</label>
          <span class="resumen-filtro" id="f-resumen"></span>
          <button class="linkbtn" id="f-limpiar" type="button">Limpiar filtros</button>
          <span class="sp"></span>
          <span class="leyenda"><span><i style="background:var(--alta)"></i>Alta</span><span><i style="background:var(--media)"></i>Media</span><span><i style="background:var(--baja)"></i>Baja</span><span class="pill ia" style="font-size:10px">✦ Redactada</span><span class="flag">Verificar</span></span>
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
  const ESTADOS = [{k:"nueva",label:"Nuevas",tip:"Llegaron y nadie las tocó todavía"},{k:"revision",label:"En revisión",tip:"Alguien las tomó para trabajar"},
    {k:"copiada",label:"Copiadas al CMS",tip:"Ya se copiaron para publicar"},{k:"descartada",label:"Descartadas",tip:"No sirven (algunas se descartan solas: entradas, sponsors, socios)"},{k:"todas",label:"Todas",tip:"Todo junto"}];
  const ESTADO_TXT = {nueva:"Nueva", revision:"En revisión", copiada:"Copiada", descartada:"Descartada"};
  const ST_TXT = {ok:"Funciona", limitada:"Limitada", caida:"Caída", pausada:"Pausada", "sin probar":"Sin probar"};
  const MET_TXT = {rss:"RSS", river:"API River", premier:"API Premier", wp:"API WordPress", web:"Web", pausada:"Pausada"};
  const PRIO = {alta:0, media:1, baja:2};
  const IDIOMA = {en:"inglés", it:"italiano", fr:"francés", pt:"portugués", de:"alemán"};
  const MESES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
  const LS = "cablera_clave";
  const PREFS = "cablera_prefs";
  const S = {clave:"", cfg:null, items:[], ultima:null, fuentes:[], view:"bandeja", estado:"nueva", deporte:"", fuente:"", red:false, q:"",
             orden:"recientes", grupo:"", periodo:"72", tema:"", cerrados:{},
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
    cargarPrefs();
    try{ if(!localStorage.getItem("cablera_ayuda_vista")) $("ayuda").hidden = false; }catch(e){}
    try{
      await Promise.all([cargarItems(), cargarFuentes()]);
    }catch(e){ if(e.message !== "Clave incorrecta") $("list").innerHTML = `<div class="empty"><strong>No se pudo cargar</strong>${esc(e.message)}</div>`; }
    setInterval(() => { if(!document.hidden) cargarItems().catch(()=>{}); }, 120000);
  }

  // ───────── bandeja
  // ───────── temas: club, Selección, competencia o deporte
  const CLUB_FUENTE = {boca:"Boca", river:"River", racing:"Racing", independiente:"Independiente", sanlorenzo:"San Lorenzo",
    estudiantes:"Estudiantes", gimnasia:"Gimnasia", lanus:"Lanús", banfield:"Banfield", argentinos:"Argentinos Juniors",
    huracan:"Huracán", newells:"Newell's", velez:"Vélez", talleres:"Talleres", copaargentina:"Copa Argentina"};
  const TEMAS_TITULO = [
    ["Selección", /selecci[oó]n argentina|la selecci[oó]n|scaloni|albiceleste|\bsub[ -]?(15|17|20|23)\b|seleccion(es)? juvenil/i],
    ["Boca", /\bboca\b|xeneize/i], ["River", /\briver\b|millonario/i], ["Racing", /\bracing\b/i],
    ["Independiente", /independiente/i], ["San Lorenzo", /san lorenzo|cuervo/i], ["Estudiantes", /estudiantes/i],
    ["Copa Argentina", /copa argentina/i], ["Libertadores y Sudamericana", /libertadores|sudamericana|conmebol/i],
    ["Messi e Inter Miami", /\bmessi\b|inter miami/i], ["Colapinto y F1", /colapinto|f[oó]rmula 1|\bf1\b|alpine/i],
    ["Pumas", /\bpumas\b|pumitas/i], ["Leonas y Leones", /\bleonas\b|\bleones\b/i]];
  const TEMA_CATEGORIA = {"Ligas del exterior":"Argentinos en el exterior", "Fútbol internacional":"Copas y fútbol internacional",
    "Fútbol argentino":"Fútbol argentino"};
  function temaDe(n){
    if(n._tema) return n._tema;
    const t = (n.nota && n.nota.titulo) || n.titulo_original || "";
    let tema = null;
    for(const [nombre, rx] of TEMAS_TITULO.slice(0,1)) if(rx.test(t)) tema = nombre;
    if(!tema && CLUB_FUENTE[n.fuente_id]) tema = CLUB_FUENTE[n.fuente_id];
    if(!tema){
      let mejor = Infinity;
      for(const [nombre, rx] of TEMAS_TITULO.slice(1)){ const m = t.search(rx); if(m >= 0 && m < mejor){ mejor = m; tema = nombre; } }
    }
    if(!tema && n.deporte && n.deporte !== "Fútbol") tema = n.deporte;
    if(!tema) tema = TEMA_CATEGORIA[n.categoria] || (n.categoria === "Clubes" ? "Clubes" : "Otros");
    n._tema = tema; return tema;
  }
  function fechaRef(n){ return ts(n) || Date.parse(n.capturado || 0) || 0; }
  function hace(v){
    const t = Date.parse(v || ""); if(!t) return "";
    const m = Math.round((Date.now() - t) / 60000);
    if(m < 1) return "recién"; if(m < 60) return `hace ${m} min`;
    const h = Math.round(m / 60); if(h < 24) return `hace ${h} h`;
    const d = Math.round(h / 24); return d === 1 ? "ayer" : `hace ${d} días`;
  }
  function filtrados(sinPeriodo){
    const q = S.q.trim().toLowerCase(), lim = Number(S.periodo) ? Date.now() - Number(S.periodo) * 3600e3 : 0;
    return S.items
      .filter(n => S.estado === "todas" || (n.estado || "nueva") === S.estado)
      .filter(n => sinPeriodo || !lim || fechaRef(n) >= lim || !n.publicado && Date.parse(n.capturado || 0) >= lim)
      .filter(n => !S.deporte || n.deporte === S.deporte)
      .filter(n => !S.fuente || n.fuente === S.fuente)
      .filter(n => !S.tema || temaDe(n) === S.tema)
      .filter(n => !S.red || n.nota)
      .filter(n => !q || [n.titulo_original, n.titulo_fuente, n.nota && n.nota.titulo, n.fuente, n.resumen, n.codigo, temaDe(n)].join(" ").toLowerCase().includes(q));
  }
  function ordenar(arr){
    const f = {
      recientes: (a,b) => fechaRef(b) - fechaRef(a),
      viejas: (a,b) => fechaRef(a) - fechaRef(b),
      prioridad: (a,b) => (PRIO[a.prioridad] ?? 3) - (PRIO[b.prioridad] ?? 3) || fechaRef(b) - fechaRef(a)}[S.orden] || ((a,b) => fechaRef(b) - fechaRef(a));
    return arr.sort(f);
  }
  function visibles(){ return ordenar(filtrados()); }
  function clavesGrupo(n){
    if(S.grupo === "tema") return temaDe(n);
    if(S.grupo === "deporte") return n.deporte || "Sin deporte";
    if(S.grupo === "fuente") return n.fuente || "Sin fuente";
    if(S.grupo === "dia"){
      const t = fechaRef(n); if(!t) return "Sin fecha";
      const d = new Date(t), hoy = new Date(); const dd = Math.round((new Date(hoy.toDateString()) - new Date(d.toDateString())) / 864e5);
      return dd === 0 ? "Hoy" : dd === 1 ? "Ayer" : d.toLocaleDateString("es-AR", {weekday:"long", day:"numeric", month:"long"});
    }
    return "";
  }
  function guardarPrefs(){
    try{ localStorage.setItem(PREFS, JSON.stringify({orden:S.orden, grupo:S.grupo, periodo:S.periodo, cerrados:S.cerrados})); }catch(e){}
  }
  function cargarPrefs(){
    try{ const p = JSON.parse(localStorage.getItem(PREFS) || "{}"); Object.assign(S, {orden:p.orden || S.orden, grupo:p.grupo ?? S.grupo, periodo:p.periodo || S.periodo, cerrados:p.cerrados || {}}); }catch(e){}
    $("f-orden").value = S.orden; $("f-grupo").value = S.grupo; $("f-periodo").value = S.periodo;
  }
  function opciones(sel, valores, actual, todos){
    const cnt = {}; valores.forEach(v => cnt[v] = (cnt[v] || 0) + 1);
    const ks = Object.keys(cnt).sort((a,b) => a.localeCompare(b, "es"));
    sel.innerHTML = `<option value="">${todos}</option>` + ks.map(k => `<option value="${esc(k)}" ${k===actual?"selected":""}>${esc(k)} (${cnt[k]})</option>`).join("");
  }
  function renderDeportes(){
    const base = S.items.filter(n => S.estado === "todas" || (n.estado || "nueva") === S.estado);
    opciones($("f-deporte"), base.map(n => n.deporte).filter(Boolean), S.deporte, "Todos");
    opciones($("f-tema"), base.map(temaDe), S.tema, "Todos");
    renderFuenteSelect();
  }
  function renderFuenteSelect(){
    const base = S.items.filter(n => S.estado === "todas" || (n.estado || "nueva") === S.estado);
    opciones($("f-fuente"), base.map(n => n.fuente).filter(Boolean), S.fuente, "Todas");
  }
  function renderTabs(){
    const cnt = k => k === "todas" ? S.items.length : S.items.filter(n => (n.estado||"nueva") === k).length;
    $("tabs").innerHTML = ESTADOS.map(e => `<button type="button" data-k="${e.k}" title="${e.tip}" aria-pressed="${S.estado===e.k}">${e.label}<span class="n">${cnt(e.k)}</span></button>`).join("");
    $("vn-bandeja").textContent = cnt("nueva") || "";
  }
  function renderTicker(){
    const u = S.ultima, nuevas = S.items.filter(n => (n.estado||"nueva")==="nueva").length;
    const red = S.items.filter(n => n.nota).length;
    $("ticker").innerHTML = `<span><span class="live"></span>Última captura <b>${u ? esc(fecha(u.fecha)) : "—"}</b></span><span><b>${nuevas}</b> nuevas</span><span><b>${red}</b> redactadas</span>` +
      `<button class="btn sm" id="btn-capturar" type="button" ${S.capturando?"disabled":""}>${S.capturando?'<span class="spin"></span> Capturando…':"↻ Capturar ahora"}</button>`;
  }
  function itemHtml(n){
    const cuando = n.publicado ? `${esc(fecha(n.publicado))} · ${esc(hace(n.publicado))}` : `sin fecha · capturado ${esc(hace(n.capturado))}`;
    return `
      <button type="button" class="item" data-id="${esc(n.id)}" data-p="${esc(n.prioridad)}" data-estado="${esc(n.estado||"nueva")}" aria-current="${S.sel===n.id}">
        <div class="meta"><span class="pill">${esc(n.deporte)}</span>${S.grupo!=="tema"?`<span class="tema">${esc(temaDe(n))}</span>`:""}${n.nota?`<span class="pill ia">✦ Redactada</span>`:""}<span>${cuando}</span>${(n.estado&&n.estado!=="nueva"&&S.estado==="todas")?`<span class="state" data-s="${esc(n.estado)}">${ESTADO_TXT[n.estado]||""}</span>`:""}${(n.aviso||(n.nota&&n.nota.alerta))?`<span class="flag">Verificar</span>`:""}</div>
        <h3>${esc(n.nota ? n.nota.titulo : n.titulo_original)}</h3>
        <div class="src">${esc(n.fuente)}${n.titulo_fuente?` · traducido del ${IDIOMA[n.idioma]||"original"}`:""}${n.motivo?` · ${esc(n.motivo)}`:""}</div>
      </button>`;
  }
  function renderList(){
    const list = $("list"), vs = visibles();
    const total = filtrados(true).length;
    $("f-resumen").innerHTML = vs.length ? `Mostrando <b>${vs.length}</b>${total > vs.length ? ` de ${total} (el resto queda fuera del período)` : ""}` : "";
    if(!S.items.length){
      list.innerHTML = `<div class="empty"><strong>La bandeja está vacía</strong>Tocá “↻ Capturar ahora” arriba a la derecha para leer las fuentes, o pegá un comunicado.</div>`; return;
    }
    if(!vs.length){
      list.innerHTML = `<div class="empty"><strong>Nada por acá</strong>${total ? `Hay ${total} con estos filtros pero son más viejos: cambiá el <b>Período</b> a “Todo”.` : `No hay comunicados con estos filtros. Probá <b>Limpiar filtros</b> o el estado “Todas”.`}</div>`; return;
    }
    if(!S.grupo){
      list.innerHTML = vs.slice(0, S.mostrar).map(itemHtml).join("") + (vs.length > S.mostrar ? `<button class="btn more" id="b-more" type="button">Ver ${vs.length - S.mostrar} más</button>` : "");
      return;
    }
    const grupos = new Map();
    vs.forEach(n => { const k = clavesGrupo(n); if(!grupos.has(k)) grupos.set(k, []); grupos.get(k).push(n); });
    let orden = [...grupos.keys()];
    if(S.grupo !== "dia") orden.sort((a,b) => grupos.get(b).length - grupos.get(a).length || a.localeCompare(b, "es"));
    list.innerHTML = orden.map(k => {
      const ns = grupos.get(k), altas = ns.filter(n => n.prioridad === "alta").length, id = S.grupo + ":" + k;
      return `<details class="grupo" data-g="${esc(id)}" ${S.cerrados[id] ? "" : "open"}><summary>${esc(k)} <span class="n">${ns.length}</span>${altas?`<span class="alta">${altas} alta${altas>1?"s":""}</span>`:""}</summary><div class="items">${ns.slice(0, 40).map(itemHtml).join("")}${ns.length > 40 ? `<div class="resumen-filtro">…y ${ns.length - 40} más: filtrá por este grupo para verlas todas.</div>` : ""}</div></details>`;
    }).join("");
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
        <label>Método<select id="ff-metodo">${opt(f.metodo,[["web","Web (scraping)"],["rss","RSS"],["river","API de River"],["premier","API de la Premier"],["wp","API de WordPress"],["pausada","Pausada (no se lee)"]])}</select></label>
        <label>Deporte por defecto<input id="ff-deporte" value="${esc(f.deporte)}"></label>
      </div>
      <label>Dirección (del listado de noticias o del feed RSS)<input id="ff-url" value="${esc(f.url)}" placeholder="https://"></label>
      <div class="grid2">
        <label>Patrón de los links de notas <span class="hint">Solo Web. Parte de la dirección que tienen todas las notas, ej. <code>/noticias/</code>. Vacío: busca un RSS o links con títulos largos.</span><input id="ff-patron" value="${esc(f.patron)}"></label>
        <label>Filtro (opcional) <span class="hint">Solo entran notas que mencionen alguna de estas palabras, separadas por <code>|</code>. Ej.: <code>colapinto|alpine</code></span><input id="ff-filtro" value="${esc(f.filtro)}"></label>
        <label>Idioma<select id="ff-idioma">${opt(f.idioma||"es",[["es","Español"],["en","Inglés"],["it","Italiano"],["fr","Francés"],["pt","Portugués"]])}</select></label>
        <label>Orden<input id="ff-orden" type="number" value="${esc(f.orden)}"></label>
      </div>
      <label>Link público (solo API de WordPress, opcional) <span class="hint">Ej.: <code>https://cahuracan.com/noticias/{slug}</code></span><input id="ff-enlace" value="${esc(f.enlace||"")}"></label>
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
      idioma:$("ff-idioma").value, orden:Number($("ff-orden").value)||500, detalle:$("ff-detalle").value.trim(), enlace:$("ff-enlace").value.trim()};
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
    document.querySelectorAll("#views .tab").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.view === v)));
    $("v-bandeja").hidden = v !== "bandeja"; $("v-fuentes").hidden = v !== "fuentes"; $("v-actividad").hidden = v !== "actividad";
    $("v-bandeja").style.display = v === "bandeja" ? "flex" : "none";
    $("v-actividad").style.display = v === "actividad" ? "flex" : "none";
    if(v === "fuentes") renderFuentes();
    if(v === "actividad") renderActividad();
  }

  document.addEventListener("click", async ev => {
    const t = ev.target.closest("button"); if(!t) return;
    if(t.id === "b-ayuda" || t.id === "b-ayuda-x"){
      const a = $("ayuda"); a.hidden = t.id === "b-ayuda-x" ? true : !a.hidden; $("b-ayuda").setAttribute("aria-expanded", String(!a.hidden));
      try{ localStorage.setItem("cablera_ayuda_vista", "1"); }catch(e){}
      return;
    }
    if(t.closest("#views") && t.dataset.view){ setView(t.dataset.view); return; }
    if(t.id === "b-filtros"){ const b = t.closest(".bar"); b.classList.toggle("abierta"); t.setAttribute("aria-expanded", String(b.classList.contains("abierta"))); t.textContent = b.classList.contains("abierta") ? "Ocultar filtros ▴" : "Ordenar y filtrar ▾"; return; }
    if(t.id === "f-limpiar"){
      Object.assign(S, {deporte:"", fuente:"", tema:"", q:"", red:false, periodo:"0", mostrar:80});
      $("f-q").value = ""; $("f-red").checked = false; $("f-periodo").value = "0"; guardarPrefs(); renderDeportes(); renderList(); return;
    }
    if(t.closest("#tabs")){ S.estado = t.dataset.k; S.sel = null; S.mostrar = 80; renderDeportes(); renderBandeja(); return; }
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
  $("f-tema").addEventListener("change", e => { S.tema = e.target.value; renderList(); });
  $("f-orden").addEventListener("change", e => { S.orden = e.target.value; guardarPrefs(); renderList(); });
  $("f-grupo").addEventListener("change", e => { S.grupo = e.target.value; guardarPrefs(); renderList(); });
  $("f-periodo").addEventListener("change", e => { S.periodo = e.target.value; S.mostrar = 80; guardarPrefs(); renderList(); });
  $("list").addEventListener("toggle", e => {
    const d = e.target; if(!d.matches || !d.matches("details.grupo")) return;
    if(d.open) delete S.cerrados[d.dataset.g]; else S.cerrados[d.dataset.g] = 1; guardarPrefs();
  }, true);
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

import model as M, model2 as M2, hier as HI, json
V=[dict(id=v["id"],t=v["title"],tahap=v["tahap"],kel=v["kel"],var=v["var"],res=v["res"],el=[list(e) for e in v["elc"]],cat=v["cat"],frek=v["frek"],g=v["gid"],a=1 if v.get("auto") else 0,
        also=[[p,c,o] for (p,c),o in v["also"].items()],
        sup=[[x["key"],1 if x["coded"] else 0,1 if x["star"] else 0,x["body"],x["lists"],x["src"]] for x in v.get("sup",[])],
        ind=v.get("ind"),per=v.get("per"),anak=v.get("anak",[]),syn=1 if v.get("syn") else 0) for v in M.ALL]
def pk(E):
    if E["coded"]: body=[[o["s"],o["c"],o["d"],o["k"],o["ids"]] for o in E["opts"].values()]
    else: body=[[x["v"],x["k"],x["ids"]] for x in E["vals"].values()]
    return [E["key"],1 if E["coded"] else 0,1 if E["star"] else 0,E["ids"],body,[[l,i] for l,i in E["lists"].items()]]
G=[dict(id=g["id"],label=g["label"],status=g["status"],note=g["note"],m=[x["id"] for x in g["members"]],rel=g["related"],
        els=[pk(E) for E in g["els"]],ex=[[x["el"],x["kind"],x["parts"]] for x in g["expl"]]) for g in M.G]
DS={k:[1 if d["src"]=="playbook" else 0,d["t"],d["ctx"]] for k,d in M2.DESC.items()}
import markdown
DOC=markdown.markdown(open('/home/claude/doc/DOKUMENTASI.md').read(),extensions=['tables'])
REF=[dict(t=r["title"],tahap=r["tahap"],isi=r.get("isi",""),note=r["note"],kutipan=r.get("kutipan",""),
     tg=[[x["code"],x["judul"],x["url"]] for x in r["targets"]]) for r in M.REFS]
HH=[dict(id=h["id"],label=h["label"],m=h["m"],titles=h["titles"],nchild=h["nchild"],
     rows=[dict(label=r["label"],gid=r["gid"],by=r["by"]) for r in h["rows"]]) for h in HI.H]
D=json.dumps(dict(DOC=DOC,REF=REF,H=HH,HSTAT=HI.STAT,V=V,G=G,L=M.LISTS,T=[list(t) for t in M.TITLES],S=M.SRC,C=M.CODEVARS,RS=M2.RSOUT,DS=DS,SNAP='SATUSEHAT snapshot 18 Sep 2026',
   STD='Dokumen Lampiran Standar Terminologi SATUSEHAT v10.3 (30 Jun 2026)',
   GH='https://github.com/silviaavn/fhir-mapping-repository-id'),ensure_ascii=False,separators=(",",":"))
html=r'''<title>Crosscheck Playbook SATUSEHAT</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Fraunces:opsz,wght@9..144,600&display=swap">
<style>
:root{--bg:#FBF8F9;--surface:#FFFFFF;--ink:#221A1E;--muted:#6E6168;--line:#E7DEE2;--accent:#7A2E4D;--accent-soft:#F4E8ED;--code:#3B2D5C;--chip:#EFE7EB;--shadow:0 12px 32px rgba(34,26,30,.18);
--ok:#2F6B3A;--ok-bg:#E3F1E5;--warn:#8A5A00;--warn-bg:#FCF0D2;--bad:#9B2C2C;--bad-bg:#F9E0E0;--uni:#5E5A5C;--uni-bg:#EEEBEC;
--sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"IBM Plex Mono",ui-monospace,Consolas,monospace;--disp:"Fraunces",Georgia,serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#171214;--surface:#211A1D;--ink:#F1E9EC;--muted:#AE9FA6;--line:#3A2F34;--accent:#E7A3BE;--accent-soft:#3A2330;--code:#C9BCF2;--chip:#2E2428;--shadow:0 12px 32px rgba(0,0,0,.5);--ok:#9BD5A4;--ok-bg:#1F3324;--warn:#F2C66D;--warn-bg:#3A2E14;--bad:#F2A3A3;--bad-bg:#3D1F22;--uni:#C9C0C4;--uni-bg:#2C2629}}
:root[data-theme="dark"]{--bg:#171214;--surface:#211A1D;--ink:#F1E9EC;--muted:#AE9FA6;--line:#3A2F34;--accent:#E7A3BE;--accent-soft:#3A2330;--code:#C9BCF2;--chip:#2E2428;--shadow:0 12px 32px rgba(0,0,0,.5);--ok:#9BD5A4;--ok-bg:#1F3324;--warn:#F2C66D;--warn-bg:#3A2E14;--bad:#F2A3A3;--bad-bg:#3D1F22;--uni:#C9C0C4;--uni-bg:#2C2629}
[hidden]{display:none!important}
body{background:var(--bg);color:var(--ink);font:14px/1.5 var(--sans)}
.wrap{max-width:1380px;margin:0 auto;padding-inline:20px;padding-block:22px 60px}
h1{font-family:var(--disp);font-weight:600;font-size:clamp(21px,2.6vw,28px);line-height:1.2;margin:0 0 6px;text-wrap:balance}
header p{margin:0 0 6px;color:var(--muted);max-width:95ch;font-size:13px}
header details{font-size:12px;color:var(--muted)} header details li{margin:2px 0}
header code{font-family:var(--mono);font-size:12px;color:var(--code)}
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;position:sticky;top:env(safe-area-inset-top,0px);background:var(--bg);padding-block:10px;z-index:3;border-bottom:1px solid var(--line);margin-top:12px}
.tools input,.tools select,.tools button{font:13px var(--sans);padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--ink)}
.tools input{flex:1 1 200px}.tools select{max-width:320px}
#tsel{font-weight:600;border-color:var(--accent);color:var(--accent)}
.tools button{cursor:pointer}.tools button:hover{border-color:var(--accent)}
.tools input:focus,.tools select:focus,button:focus-visible,a:focus-visible{outline:2px solid var(--accent);outline-offset:1px}
.count{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.stats{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
.stats button{font:12px var(--sans);border:1px solid var(--line);background:var(--surface);color:var(--ink);padding:4px 10px;border-radius:999px;cursor:pointer}
.stats button[aria-pressed="true"]{outline:2px solid var(--accent)}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--surface)}
table{border-collapse:collapse;width:100%}
table.main{min-width:1080px;table-layout:fixed}
th,td{text-align:left;vertical-align:top;padding:5px 9px}
thead th{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600;background:var(--surface);position:sticky;top:0;border-bottom:1px solid var(--line)}
tr.step td{background:var(--accent-soft);color:var(--accent);font-weight:600;font-size:13px;padding:9px 10px}
tr.first td{border-top:1px solid var(--line)}
td.var{border-right:1px solid var(--line);padding:9px 10px!important}
.id{font-family:var(--mono);font-size:11px;color:var(--muted)}
td.var .kel{display:block;font-size:11px;color:var(--muted)}
td.var .nm{display:block;font-weight:600;margin:1px 0 4px}
.pill{display:inline-block;font-size:11px;padding:1px 7px;border-radius:10px;background:var(--chip);color:var(--ink);overflow-wrap:anywhere;margin:0 4px 3px 0}
.st{display:inline-block;font:600 11px var(--sans);padding:1px 8px;border-radius:10px;margin:0 4px 3px 0;border:0}
button.st{cursor:pointer;text-decoration:underline dotted;text-underline-offset:2px}
button.st::after{content:" ⓘ";font-weight:400}
.st-ok{background:var(--ok-bg);color:var(--ok)}.st-warn{background:var(--warn-bg);color:var(--warn)}.st-bad{background:var(--bad-bg);color:var(--bad)}.st-uni{background:var(--uni-bg);color:var(--uni)}
.muncul{margin-top:6px;font-size:11.5px}
.muncul b{display:block;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600;margin-top:4px}
a.lk{color:var(--accent);text-decoration:none;border-bottom:1px dotted var(--accent);font-size:11.5px}
a.lk:hover{border-bottom-style:solid}
.lkl{display:block;margin:1px 0}
.note{display:block;font-size:11.5px;color:var(--muted);margin-top:6px}
.freq{display:block;font-size:11px;color:var(--accent);margin-top:3px}
td.path{font-family:var(--mono);font-size:11.5px;color:var(--code);overflow-wrap:anywhere}
td.path.rep{color:var(--muted)} td.path.mand{font-weight:500}
td.val{font-size:12.5px;overflow-wrap:anywhere;font-weight:500}
td.ket{font-size:12.5px} td.also{font-size:11.5px}
.inl{padding-block:2px 10px!important}
.inlist{max-height:198px;overflow:auto;border:1px solid var(--line);border-radius:8px;margin-bottom:3px}
.inlist table{min-width:620px}
.inlist th{position:sticky;top:0;background:var(--accent-soft);color:var(--accent);font-size:10.5px}
.inlist td{padding:4px 8px;font-size:12px;border-bottom:1px solid var(--line);overflow-wrap:anywhere}
.inlist td.c{font-family:var(--mono);font-size:11.5px;color:var(--code)}
.lmeta{font-size:11px;color:var(--muted)}
/* consolidation list */
.klist{border:1px solid var(--line);border-radius:10px;background:var(--surface)}
.krow{border-bottom:1px solid var(--line)}
.krow:last-child{border-bottom:0}
.khead{display:grid;grid-template-columns:22px 70px minmax(180px,1.4fr) auto minmax(160px,1.2fr) 70px;gap:10px;align-items:center;padding:8px 12px;cursor:pointer}
.khead:hover{background:var(--accent-soft)}
.khead .car{color:var(--muted);transition:transform .15s}
.krow.open .car{transform:rotate(90deg)}
.khead .lb{font-weight:600}
.khead .tt{display:flex;flex-wrap:wrap;gap:3px}
.khead .n{font-size:11.5px;color:var(--muted);text-align:right;font-variant-numeric:tabular-nums}
.kbody{padding:4px 12px 14px 44px}
.kbody .tbl{margin-top:8px}
@media (prefers-reduced-motion:reduce){.khead .car{transition:none}}
.dim{color:var(--muted)}
.hl{animation:hl 2s ease-out}@keyframes hl{from{background:var(--warn-bg)}to{background:transparent}}
@media (prefers-reduced-motion:reduce){.hl{animation:none}}
/* popover */
#pop{position:fixed;z-index:20;width:min(560px,calc(100vw - 32px));max-height:min(70vh,560px);overflow:auto;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);padding:14px 16px}
#pop h3{margin:0 24px 4px 0;font:600 15px var(--sans)}
#pop .x{position:absolute;top:8px;right:10px;border:0;background:none;font-size:18px;cursor:pointer;color:var(--muted)}
#pop .pair{margin-top:10px;padding-top:8px;border-top:1px solid var(--line)}
#pop .pair h4{margin:0 0 4px;font:600 12px var(--sans);color:var(--accent)}
#pop ul{margin:0;padding-left:18px;font-size:12.5px}#pop li{margin:3px 0;overflow-wrap:anywhere}
#pop .dk,#drawer .dk{font:600 11px var(--sans);color:var(--bad);margin-top:4px}#pop .dl,#drawer .dl{font:600 11px var(--sans);color:var(--ok);margin-top:4px}
#drawer .pair{margin-top:8px}#drawer .pair h4{margin:0 0 3px;font:600 12px var(--sans);color:var(--accent)}#drawer ul{margin:0;padding-left:18px;font-size:12px}#drawer code{font-family:var(--mono);font-size:11px;color:var(--code)}
.cmp{width:100%;border-collapse:collapse;font-size:12px;margin-top:6px}.cmp td,.cmp th{border-bottom:1px solid var(--line);padding:3px 6px;vertical-align:top;overflow-wrap:anywhere}.cmp th{font-size:10.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}.cmp tr.acu td{background:var(--ok-bg)}
#pop code{font-family:var(--mono);font-size:11.5px;color:var(--code)}
mark{background:#FFE58A;color:#221A1E;border-radius:2px;padding:0 1px}
.descb{border:0;background:none;color:var(--accent);cursor:pointer;font-size:13px;padding:0 2px;vertical-align:1px}
.els{display:grid;gap:6px;margin-top:10px}
.el{border:1px solid var(--line);border-radius:8px;padding:6px 10px;background:var(--surface)}
.el.d-beda{border-left:4px solid var(--bad)}.el.d-sebagian{border-left:4px solid var(--warn)}
.eh{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline;font-size:12px}
.eh code{font-family:var(--mono);font-size:12px;color:var(--code)} .eh code.mand{font-weight:600}
.ev{font-size:12.5px;margin-top:3px;overflow-wrap:anywhere}
.tag{display:inline-block;font:600 10.5px var(--sans);padding:0 6px;border-radius:6px}
.tag.beda{background:var(--bad-bg);color:var(--bad)}.tag.sebagian{background:var(--warn-bg);color:var(--warn)}.tag.std{background:var(--accent-soft);color:var(--accent)}
.tag.rev{background:#E6E0F8;color:#4B3A8F}
.tag.sup{background:#DDEBF6;color:#1F4E6B}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .tag.sup{background:#1E3446;color:#AFD3EA}}
:root[data-theme="dark"] .tag.sup{background:#1E3446;color:#AFD3EA}
tr.ref td{background:var(--accent-soft);font-size:12.5px;padding:8px 12px}
tr.ref .rj{font-weight:600;color:var(--accent)}
tr.sup td{background:color-mix(in srgb,var(--chip) 45%,transparent)}
tr.ph td{background:color-mix(in srgb,var(--accent-soft) 70%,transparent);padding:6px 12px;font-size:12.5px}
tr.ph b{font-size:13px}
tr.hide{display:none}
.tgb{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:6px;font:11px var(--sans);padding:0 6px;cursor:pointer;margin-right:6px}
.ind{display:inline-block}
.tag.item{background:#E4EEDF;color:#2F5B2A}.tag.komponen{background:#F6E5D6;color:#7A431A}.tag.section{background:#E3E1F6;color:#3D357F}.tag.kelompok{background:var(--chip);color:var(--muted)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .tag.item{background:#24361F;color:#BFDDB5}:root:not([data-theme="light"]) .tag.komponen{background:#3A2718;color:#EBC49B}:root:not([data-theme="light"]) .tag.section{background:#272248;color:#C3BDF0}}
tr.sup td.path{opacity:.85}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .tag.rev{background:#332A55;color:#C9BCF2}}
:root[data-theme="dark"] .tag.rev{background:#332A55;color:#C9BCF2}
.tag.Inti{background:var(--ok-bg);color:var(--ok)}.tag.Umum{background:var(--warn-bg);color:var(--warn)}.tag.Kadang,.tag.Jarang{background:var(--uni-bg);color:var(--uni)}
#pop ul.parts{padding-left:14px;margin:2px 0 6px}
.rcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin-top:10px}
.rcard{text-align:left;border:1px solid var(--line);border-radius:10px;background:var(--surface);padding:10px 12px;cursor:pointer;font:13px var(--sans);color:var(--ink)}
.rcard:hover{border-color:var(--accent)} .rcard b{display:block;font-size:14px;color:var(--accent)} .rcard span{display:block;font-size:11.5px;color:var(--muted)}
.bar{display:inline-block;width:70px;height:7px;border-radius:4px;background:var(--chip);vertical-align:middle;overflow:hidden}.bar i{display:block;height:100%;background:var(--accent)}
details.rel{border:1px solid var(--line);border-radius:8px;background:var(--surface);margin-bottom:6px}
details.rel>summary{cursor:pointer;padding:7px 10px;display:flex;flex-wrap:wrap;gap:4px 12px;align-items:center;font-size:12.5px}
details.rel>summary code{font-family:var(--mono);font-size:12.5px;color:var(--code);font-weight:600;min-width:150px}
details.rel .rb{padding:2px 12px 10px 22px}
.rp{margin-top:8px}.rp .inlist{max-height:260px}
.inlist tr.std td{background:var(--accent-soft)}
.mx{border-collapse:collapse;font-size:12px;min-width:0}.mx th,.mx td{border:1px solid var(--line);padding:3px 6px;text-align:center;font-variant-numeric:tabular-nums}
.mx th{font:500 10.5px var(--mono);text-transform:none;letter-spacing:0;position:static}.mx td:first-child,.mx th:first-child{text-align:left}
.sec h3{font:600 14px var(--sans);margin:18px 0 6px}
.chips{display:flex;flex-wrap:wrap;gap:4px}
.back{font:13px var(--sans);border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:8px;padding:5px 10px;cursor:pointer}
.doc{max-width:980px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:8px 22px 18px;font-size:13.5px}
.doc h1{font-size:22px;margin-top:14px}.doc h2{font:600 16px var(--sans);margin:20px 0 6px;color:var(--accent)}
.doc table{border-collapse:collapse;margin:6px 0;width:100%}.doc td,.doc th{border:1px solid var(--line);padding:4px 8px;font-size:12.5px}.doc th{background:var(--accent-soft);position:static}
.doc li{margin:4px 0}
footer{margin-top:30px;font-size:12px;color:var(--muted)}
.revbtn{font:500 11px var(--sans);border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:10px;padding:1px 8px;cursor:pointer;margin:0 4px 3px 0}
.revbtn.has{border-color:var(--accent);color:var(--accent)}
.revok{display:inline-block;font:600 11px var(--sans);padding:1px 8px;border-radius:10px;background:var(--ok-bg);color:var(--ok);margin:0 4px 3px 0}
#drawer{position:fixed;top:0;right:0;bottom:0;width:min(460px,100vw);background:var(--surface);border-left:1px solid var(--line);box-shadow:var(--shadow);z-index:30;display:flex;flex-direction:column}
#drawer header{padding:14px 16px 8px;border-bottom:1px solid var(--line)}
#drawer h3{margin:0 28px 2px 0;font:600 15px var(--sans)}
#drawer .x{position:absolute;top:10px;right:12px;border:0;background:none;font-size:20px;cursor:pointer;color:var(--muted)}
#drawer .body{overflow:auto;padding:12px 16px;flex:1}
.rev{border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin-bottom:10px;font-size:12.5px}
.rev .meta{font-size:11px;color:var(--muted);margin-bottom:4px}
.rev .kind{font-weight:600}
.rev .src{display:inline-block;font:600 10px var(--sans);letter-spacing:.06em;text-transform:uppercase;padding:1px 6px;border-radius:6px;background:var(--accent-soft);color:var(--accent)}
.rev .src.base{background:var(--uni-bg);color:var(--uni)}
.rev .acts{margin-top:6px;display:flex;gap:6px}
.rev .acts button{font:12px var(--sans);border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:6px;padding:2px 8px;cursor:pointer}
form.revf{display:grid;gap:8px;border-top:1px solid var(--line);padding-top:12px;margin-top:6px;font-size:12.5px}
form.revf label{display:grid;gap:3px;font-weight:500}
form.revf input,form.revf select,form.revf textarea{font:13px var(--sans);padding:7px 9px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}
form.revf textarea{min-height:64px;resize:vertical}
form.revf button{font:600 13px var(--sans);padding:8px 12px;border-radius:8px;border:0;background:var(--accent);color:var(--surface);cursor:pointer;justify-self:start}
.revmsg{font-size:12px;color:var(--muted)}
.revbtns{display:flex;flex-wrap:wrap;gap:6px}
.revbtns button{font:600 12.5px var(--sans);padding:7px 10px;border-radius:8px;border:1px solid var(--accent);background:var(--surface);color:var(--accent);cursor:pointer}
.revbtns button[type=submit]{background:var(--accent);color:var(--surface);border-color:var(--accent)}
@media (max-width:760px){table.main{min-width:0} table.main thead{display:none} table.main tr{display:block;padding:6px 10px} table.main td{display:block;padding:2px 0} table.main td.var{border-right:0} table.main td[data-l]:not(:empty)::before{content:attr(data-l);display:block;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
 .khead{grid-template-columns:18px 1fr auto;} .khead .id,.khead .tt,.khead .n{display:none}}
</style>
<div class="wrap">
<header>
<h1>Variabel, elemen FHIR, dan crosscheck antar use case SATUSEHAT</h1>
<p>Pilih use case untuk melihat variabel per tahap alur beserta elemen FHIR dan nilainya (tanda * = wajib). Pilihan jawaban ditampilkan sebagai daftar system–code–display–keterangan. “Konsolidasi” menggabungkan variabel yang sama dari semua use case dan merangkum nilainya per elemen. “Ringkasan Resource” menunjukkan elemen apa yang biasanya ada di setiap resource lintas playbook, lengkap dengan kode dari Lampiran Standar Terminologi. Klik ⓘ di samping nama variabel untuk deskripsinya.</p>
<details><summary>Sumber dokumen</summary><ul id="src"></ul></details>
</header>
<div class="tools">
<select id="tsel" aria-label="Pilih use case"></select>
<input id="q" type="search" placeholder="Cari variabel, elemen, kode, atau display" aria-label="Cari">
<select id="vsel" aria-label="Filter nama variabel"></select>
<select id="ssel" aria-label="Filter status crosscheck"></select>
<button type="button" id="openall" hidden>Buka semua</button><button type="button" id="closeall" hidden>Tutup semua</button>
<span class="count" id="count"></span>
</div>
<div id="stats" class="stats"></div>
<div id="out"></div>
<footer>Sumber data dasar: <b id="snap"></b>. Revisi yang ditambahkan lewat tombol “Revisi” ditandai sebagai <b>Revisi kontributor</b> (nama & institusi pengusul), terpisah dari data SATUSEHAT. Kontributor tanpa akses tulis di halaman ini dapat mengirim usulan sebagai <b>GitHub Issue</b> (akun GitHub gratis) langsung dari form revisi. Status: <b>Identik</b> = elemen & nilai sama · Tahap yang di playbook hanya merujuk ke modul lain ditampilkan sebagai judul + tautan (baris “Mengikuti modul lain”), bukan disalin · <b>Saling melengkapi</b> = hanya ada elemen/pilihan tambahan, tanpa nilai yang bertentangan · <b>Kode sama, isi beda</b> dan <b>Maksud sama, kode/struktur beda</b> = ada konflik nilai; semua label ⓘ dapat diklik untuk melihat penjelasan perbedaan · <b>Unik</b> = hanya di satu variabel. Elemen generik (subject, encounter, performer, author, source, effectiveDateTime) tidak dipakai untuk mencocokkan.</footer>
</div>
<div id="pop" role="dialog" aria-modal="false" hidden></div>
<aside id="drawer" role="dialog" aria-label="Revisi kontributor" hidden><button class="x" type="button" aria-label="Tutup">×</button><header><h3 id="dtitle"></h3><div class="revmsg" id="dsub"></div></header><div class="body" id="dbody"></div></aside>
<script>
const D=__DATA__;
const esc=s=>(s==null?"":String(s)).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const VB={};D.V.forEach(v=>VB[v.id]=v); const GB={};D.G.forEach(g=>GB[g.id]=g);
const TN={};D.T.forEach(([k,n])=>TN[k]=n);
const ltxt=k=>{const L=D.L[k];return L?(L.title+" "+L.rows.map(r=>r.join(" ")).join(" ")):""};
D.V.forEach(v=>{v._s=(JSON.stringify([v.id,v.t,v.tahap,v.kel,v.var,v.res,v.el,v.cat,v.frek,(D.DS[v.id]||[])[1]])+" "+v.el.filter(e=>e[3]).map(e=>ltxt(e[3])).join(" ")).toLowerCase()});
D.G.forEach(g=>{g._s=(g.id+" "+g.label+" "+g.status+" "+g.note+" "+JSON.stringify(g.ex)+" "+g.m.map(i=>VB[i]._s).join(" ")).toLowerCase()});
const RSS={};Object.keys(D.RS).forEach(r=>RSS[r]=(r+" "+JSON.stringify(D.RS[r])).toLowerCase());
let REV=[],CSVREV=[];const RB={};function revFor(id){return RB[id]||[]}
function rebuildRB(){for(const k in RB)delete RB[k];[...REV,...CSVREV].forEach(r=>{(RB[r.target]=RB[r.target]||[]).push(r)});}
/* ---- revisi kontributor dari berkas CSV di folder revisi/ (tanpa akun Claude) ---- */
function splitCSV(line,d){const out=[];let cur="",q=false;for(let i=0;i<line.length;i++){const c=line[i];
 if(q){if(c==='"'){if(line[i+1]==='"'){cur+='"';i++}else q=false}else cur+=c}
 else if(c==='"')q=true;else if(c===d){out.push(cur);cur=""}else cur+=c}
 out.push(cur);return out}
function parseRevCSV(txt,file){
 txt=txt.replace(/^\uFEFF/,"").replace(/\r\n?/g,"\n");
 const rows=[];let cur="",q=false;
 for(let i=0;i<txt.length;i++){const c=txt[i];if(c==='"'){q=!q;cur+=c}else if(c==="\n"&&!q){rows.push(cur);cur=""}else cur+=c}
 if(cur.trim())rows.push(cur);
 const body=rows.filter(r=>r.trim());if(body.length<2)return[];
 const d=(body[0].split(";").length>body[0].split(",").length)?";":",";
 const hdr=splitCSV(body[0],d).map(x=>x.trim().toLowerCase().replace(/^"|"$/g,""));
 const find=(...alts)=>hdr.findIndex(h=>alts.some(a=>h===a||h.indexOf(a)===0));
 const ix={target:find("target","id"),element:find("elemen","element"),kind:find("jenis","kind"),proposed:find("usulan","proposed"),
  reason:find("alasan","reason","rujukan"),author:find("kontributor","nama","author","pengusul"),institution:find("institusi","instansi"),
  date:find("tanggal","date"),status:find("status"),aksi:find("aksi","action"),path:find("path"),
  oldv:find("nilai_lama","nilai lama"),newv:find("nilai_baru","nilai baru"),tujuan:find("tujuan","target_baru")};
 if(ix.target<0)return[];
 const out=[];
 body.slice(1).forEach((line,n)=>{const c=splitCSV(line,d).map(x=>x.trim().replace(/^"|"$/g,""));
  const g=i=>i>=0&&c[i]!=null?c[i]:"";const t=g(ix.target).trim().toUpperCase();
  if(!t||!(VB[t]||GB[t]))return;
  out.push({_id:file+"#"+(n+2),target:t,element:g(ix.element),kind:g(ix.kind).toLowerCase()||"usulan",proposed:g(ix.proposed),reason:g(ix.reason),
   authorName:g(ix.author),institution:g(ix.institution),createdAt:g(ix.date),status:(g(ix.status)||"terbuka").toLowerCase(),src:"csv",file:file,
   aksi:g(ix.aksi).toLowerCase().trim(),path:g(ix.path),nilai_lama:g(ix.oldv),nilai_baru:g(ix.newv),tujuan:g(ix.tujuan).trim(),line:n+2});});
 return out}
/* ---------- menerapkan revisi berstatus "diterima" ---------- */
const NP=p=>String(p||"").replace(/\*/g,"").replace(/\[(i|\d+)\]/g,"").replace(/ /g,"");
const PLACE=/(Code|Kode|Description|Deskripsi|ECL|\(|Lihat|\/\{|\{)/;
const concrete=x=>!!x&&!PLACE.test(x)&&x.length<=20&&!/\s/.test(String(x).trim());
const nval=x=>concrete(x)?x:"~";
const SKIPEL=/\.(subject|patient|encounter|context|performer|performer\.actor|effectiveDateTime|recorder|author|source|authored)$/;
const ANCSYS=["http://fhir.org/guides/who/anc-cds/CodeSystem/anc-custom-codes","http://terminology.kemkes.go.id/CodeSystem/anc-custom-codes"];
const STDSYS=["http://loinc.org","http://snomed.info/sct","http://hl7.org/fhir/sid/icd-10","http://terminology.kemkes.go.id","http://sys-ids.kemkes.go.id/kfa"];
const ORIG={v:{},g:{}};
function rebuildTree(){D.V.forEach(v=>v.anak=[]);D.V.forEach(v=>{if(v.ind&&VB[v.ind]&&v.ind!==v.id)VB[v.ind].anak.push(v.id)});for(const k in BLOCKS)delete BLOCKS[k];}
function snapshot(){D.V.forEach(v=>ORIG.v[v.id]={el:JSON.parse(JSON.stringify(v.el)),g:v.g,ind:v.ind,per:v.per});
 D.G.forEach(g=>ORIG.g[g.id]={m:g.m.slice(),status:g.status,els:g.els,ex:g.ex});}
function restore(){D.V.forEach(v=>{const o=ORIG.v[v.id];v.el=JSON.parse(JSON.stringify(o.el));v.g=o.g;v.ind=o.ind;v.per=o.per;delete v.rev;});rebuildTree();
 D.G.forEach(g=>{const o=ORIG.g[g.id];g.m=o.m.slice();g.status=o.status;g.els=o.els;g.ex=o.ex;delete g.applied;delete g.empty;delete g.forced;});}
function velements(v){const out=[],idx={},sys={};
 const push=(k,coded)=>{if(!idx[k]){idx[k]={key:k,coded:!!coded,star:false,opts:[],vals:[],lists:[]};out.push(idx[k])}return idx[k]};
 v.el.forEach(e=>{const raw=e[0],np=NP(raw),star=String(raw).startsWith("*"),lid=e[3];
  if(lid&&D.L[lid]){const L=D.L[lid],coded=(L.cols||[]).indexOf("system")>=0;const E=push(np,coded);E.star=E.star||star;E.lists.push(lid);
   if(coded)L.rows.forEach(r=>E.opts.push([r[0]||"",r[1]||"",r[2]||"",r[3]||""]));
   else L.rows.forEach(r=>E.vals.push([String(r[0]||""),r[1]||""]));return;}
  if(/\.(system|code|display)$/.test(np)){const pre=np.replace(/\.(system|code|display)$/,"");const E=push(pre,true);E.star=E.star||star;
   if(np.endsWith(".system"))sys[pre]=e[1];
   else if(np.endsWith(".code"))E.opts.push([sys[pre]||"",e[1],"",e[2]||""]);
   else{const last=E.opts[E.opts.length-1];if(last&&!last[2])last[2]=e[1];}return;}
  const E=push(np,false);E.star=E.star||star;E.vals.push([e[1],e[2]||""]);});
 return out}
function mainCodes(v){const out=[];velements(v).forEach(e=>{if(!/\.(code|type|vaccineCode|medicationCodeableConcept)(\.coding)?$/.test(e.key))return;
 e.opts.forEach(o=>{if(concrete(o[1])&&STDSYS.some(x=>String(o[0]).indexOf(x)===0))out.push(o[1])})});return out}
function groupEls(g){const order=[],E={},N=g.m.length;
 g.m.forEach(id=>{velements(VB[id]).forEach(x=>{
  if(!E[x.key]){E[x.key]={key:x.key,coded:x.coded,star:false,ids:[],opts:{},vals:{},lists:{}};order.push(x.key)}
  const e=E[x.key];e.coded=e.coded||x.coded;e.star=e.star||x.star;if(!e.ids.includes(id))e.ids.push(id);
  x.opts.forEach(o=>{const k=String(o[0]).replace(/\/$/,"")+"|"+o[1];const t=e.opts[k]||(e.opts[k]={s:o[0],c:o[1],d:o[2],k:o[3],ids:[]});e.opts[k]=t;
   if(!t.d&&o[2])t.d=o[2];if(!t.k&&o[3])t.k=o[3];if(!t.ids.includes(id))t.ids.push(id)});
  x.vals.forEach(o=>{const k=nval(o[0]);const t=e.vals[k]||(e.vals[k]={v:o[0],k:o[1],ids:[]});e.vals[k]=t;if(!t.ids.includes(id))t.ids.push(id)});
  x.lists.forEach(l=>{(e.lists[l]=e.lists[l]||[]).push(id)});})});
 const els=order.map(k=>{const e=E[k];
  const body=e.coded?Object.keys(e.opts).map(x=>{const o=e.opts[x];return [o.s,o.c,o.d,o.k,o.ids]}):Object.keys(e.vals).map(x=>{const o=e.vals[x];return [o.v,o.k,o.ids]});
  return [e.key,e.coded?1:0,e.star?1:0,e.ids,body,Object.keys(e.lists).map(l=>[l,[...new Set(e.lists[l])]])]});
 const ex=[];
 if(N>1){const res={};g.m.forEach(i=>{(res[VB[i].res]=res[VB[i].res]||[]).push(i)});
  if(Object.keys(res).length>1)ex.push(["Resource","beda",Object.keys(res).map(r=>[r,res[r]])]);
  els.forEach(a=>{const key=a[0],coded=a[1],eids=a[3],body=a[4];
   if(SKIPEL.test(key))return;
   const missing=g.m.filter(i=>!eids.includes(i));const sig={};
   eids.forEach(i=>{const parts=coded?body.filter(o=>o[4].includes(i)&&!ANCSYS.includes(o[0])).map(o=>String(o[1]+" "+(o[2]||"")).trim())
     :body.filter(o=>o[2].includes(i)&&nval(o[0])!=="~").map(o=>String(o[0]).slice(0,60));
    sig[i]=parts.sort().join("; ")});
   const distinct=new Set(Object.keys(sig).map(i=>sig[i]).filter(x=>x));
   if(!missing.length&&distinct.size<=1)return;
   const by={};Object.keys(sig).forEach(i=>{(by[sig[i]]=by[sig[i]]||[]).push(i)});
   const parts=Object.keys(by).map(x=>[x||"(ada, nilai tidak dirinci)",by[x]]);
   if(missing.length)parts.push(["(elemen tidak dipakai)",missing]);
   ex.push([key,distinct.size>1?"beda":"sebagian",parts]);});}
 return {els:els,ex:ex}}
function recalcGroup(g){const r=groupEls(g);g.els=r.els;g.ex=r.ex;
 if(!g.m.length){g.empty=true;g.status="Kosong (dipindahkan)";return}
 if(g.m.length===1){g.status="Unik";return}
 const beda=g.ex.filter(x=>x[1]==="beda"&&x[0]!=="Resource").length,sebagian=g.ex.filter(x=>x[1]==="sebagian").length,resbeda=g.ex.some(x=>x[0]==="Resource");
 const codes=g.m.map(i=>new Set(mainCodes(VB[i])));
 const shared=codes.length&&codes.every(c=>c.size)&&[...codes[0]].some(c=>codes.every(s=>s.has(c)));
 if(!beda&&!sebagian&&!resbeda)g.status="Identik";
 else if(!beda&&!resbeda)g.status="Saling melengkapi";
 else if(shared)g.status="Kode sama, isi beda";
 else g.status="Maksud sama, kode/struktur beda";}
function applyRow(r,touched){const a=(r.aksi||"").replace(/\s+/g,"-");
 if(!a||a==="catatan")return "";
 const t=r.target,v=VB[t],g=GB[t]||(v?GB[v.g]:null);const path=String(r.path||r.element||"").trim();
 const note=x=>{const gg=g||(v?GB[v.g]:null);if(gg){(gg.applied=gg.applied||[]).push(x);touched.add(gg.id)}if(v)v.rev=true;return x};
 if(a==="ganti-nilai"){if(!v||!path||!r.nilai_baru)return "";let n=0;
  v.el.forEach(e=>{if(NP(e[0])!==NP(path))return;if(r.nilai_lama&&String(e[1]).trim()!==String(r.nilai_lama).trim())return;
   if(e[1]===r.nilai_baru)return;if(e.length<4)e[3]=null;e[4]="rev";e[5]=e[5]||e[1];e[1]=r.nilai_baru;n++;});
  if(!n)return "";return note(`${t} · ${path}: “${r.nilai_lama||"semua nilai"}” → “${r.nilai_baru}”`)}
 if(a==="pindah-konsep"){const mv=v||VB[String(r.nilai_lama||"").trim().toUpperCase()]||VB[String(r.path||"").trim().toUpperCase()];
  if(!mv||!r.tujuan)return "";const t2=mv.id;const vv=mv;
  const tj=String(r.tujuan).trim().toUpperCase();const dst=GB[tj]?tj:(VB[tj]?VB[tj].g:"");if(!dst||dst===vv.g)return "";
  const old=GB[vv.g];old.m=old.m.filter(x=>x!==t2);GB[dst].m.push(t2);vv.g=dst;vv.rev=true;
  touched.add(old.id);touched.add(dst);(GB[dst].applied=GB[dst].applied||[]).push(`${t2} dipindahkan ke sini dari ${old.id}`);
  (old.applied=old.applied||[]).push(`${t2} dipindahkan ke ${dst}`);
  return `${t2} dipindahkan dari ${old.id} ke ${dst}`}
 if(a==="jadikan-anak"){const c=VB[t],pid=String(r.tujuan||"").trim().toUpperCase(),pv=VB[pid];
  if(!c||!pv||pid===t)return "";c.ind=pid;c.per=(String(r.path||"").trim()||"manual");c.rev=true;rebuildTree();
  touched.add(c.g);if(GB[c.g])(GB[c.g].applied=GB[c.g].applied||[]).push(`${t} dijadikan anak dari ${pid}`);
  return `${t} dijadikan anak dari ${pid} (${esc?"":""}${pv.var})`}
 if(a==="lepas-anak"){const c=VB[t];if(!c||!c.ind)return "";const old=c.ind;c.ind=null;c.per=null;c.rev=true;rebuildTree();
  touched.add(c.g);if(GB[c.g])(GB[c.g].applied=GB[c.g].applied||[]).push(`${t} dilepas dari induk ${old}`);
  return `${t} dilepas dari induk ${old}`}
 if(a==="tandai-status"){if(!g)return "";const st=(r.tujuan||r.nilai_baru||"Sudah diputuskan").trim();
  g.forced=st;touched.add(g.id);(g.applied=g.applied||[]).push(`status ditandai “${st}”`);return `${g.id} status → ${st}`}
 if(a==="tambah-pilihan"){if(!v||!path||!r.nilai_baru)return "";
  const p=String(r.nilai_baru).split("|").map(x=>x.trim());
  v.el.push([path+".system",p[0]||"",""," ",false],[path+".code",p[1]||"",r.usulan||"",null,"rev"],[path+".display",p[2]||"",""," ",false]);
  v.rev=true;return note(`${t} · ${path}: tambah pilihan ${p.join(" | ")}`)}
 if(a==="tambah-elemen"){if(!v||!path)return "";
  v.el.push([path,r.nilai_baru||r.usulan||"",r.alasan||"",null,"rev"]);v.rev=true;
  return note(`${t}: tambah elemen ${path} = ${r.nilai_baru||r.usulan||""}`)}
 return ""}
let APPLIED=[];
function applyRevisions(){restore();APPLIED=[];
 const rows=[...REV,...CSVREV].filter(r=>(r.status||"").toLowerCase()==="diterima"&&r.aksi&&r.aksi!=="catatan")
  .sort((a,b)=>String(a.createdAt||"").localeCompare(String(b.createdAt||""))||String(a.file||"").localeCompare(String(b.file||""))||(a.line||0)-(b.line||0));
 const touched=new Set();
 rows.forEach(r=>{const msg=applyRow(r,touched);if(msg){r.applied=true;APPLIED.push({r:r,msg:msg})}else r.applied=false;});
 touched.forEach(gid=>{const g=GB[gid];if(g)recalcGroup(g)});
 touched.forEach(gid=>{const g=GB[gid];if(g&&g.forced)g.status=g.forced});
 D.V.forEach(v=>{v._s=(JSON.stringify([v.id,v.t,v.tahap,v.kel,v.var,v.res,v.el,v.cat,v.frek,(D.DS[v.id]||[])[1]])).toLowerCase()});
 D.G.forEach(g=>{g._s=(g.id+" "+g.label+" "+g.status+" "+g.note+" "+JSON.stringify(g.ex)+" "+g.m.map(i=>VB[i]._s).join(" ")).toLowerCase()});}
async function loadCSVRev(){
 let names=[];const api=(D.GH||"").replace("https://github.com/","https://api.github.com/repos/");
 if(api){try{const r=await fetch(api+"/contents/docs/revisi?ref=main",{cache:"no-store"});
  if(r.ok){const j=await r.json();if(Array.isArray(j))names=j.filter(f=>f.type==="file"&&/\.(csv|tsv|txt)$/i.test(f.name)&&!/^template/i.test(f.name)).map(f=>f.name)}}catch(e){}}
 if(!names.length){try{const r=await fetch("revisi/daftar.json?t="+Date.now(),{cache:"no-store"});if(r.ok){const j=await r.json();if(Array.isArray(j))names=j}}catch(e){}}
 if(!names.length)names=["revisi.csv"];
 const out=[];
 for(const n of names){try{const r=await fetch("revisi/"+encodeURIComponent(n)+"?t="+Date.now(),{cache:"no-store"});
  if(!r.ok)continue;out.push(...parseRevCSV(await r.text(),n));}catch(e){}}
 CSVREV=out;rebuildRB();applyRevisions();
 if(out.length){const y=window.scrollY;render();window.scrollTo(0,y);if(drawerId)renderDrawer();}}
function stMatch(g,ss,ids){if(!ss)return true;if(ss==="__rev")return ids.some(i=>revFor(i).length);if(ss==="__open")return ids.some(i=>revFor(i).some(r=>r.status==="terbuka"));return g.status===ss}
const ST={"Saling melengkapi":"st-ok","Unik":"st-uni","Identik":"st-ok","Kode sama, isi beda":"st-warn","Maksud sama, kode/struktur beda":"st-bad","Nama sama, kode beda":"st-bad"};
const EXPL0={"Saling melengkapi":"Perbedaannya hanya berupa elemen atau pilihan tambahan di salah satu use case — tidak ada nilai yang bertentangan, sehingga gabungannya bisa dianggap versi yang lebih lengkap.","Kode sama, isi beda":"Kode konsep utamanya sama, tetapi ada nilai yang bertentangan pada elemen yang sama (mis. unit, category, kode pilihan). Coding tambahan anc-custom-codes tidak dihitung.","Maksud sama, kode/struktur beda":"Konsepnya setara, tetapi kode, category, atau resource yang dipakai berbeda — potensi inkonsistensi dokumentasi."};
const EXPL=Object.assign({},EXPL0,{"Identik":"Semua elemen & nilai sama di lebih dari satu playbook."});
document.getElementById("src").innerHTML=D.T.map(([k,n])=>`<li><b>${esc(n)}</b> — ${esc(D.S[k]||"")}</li>`).join("");
const tsel=document.getElementById("tsel"),vsel=document.getElementById("vsel"),ssel=document.getElementById("ssel"),q=document.getElementById("q");
tsel.innerHTML=D.T.map(([k,n])=>`<option value="${k}">${esc(k)} — ${esc(n)} (${D.V.filter(v=>v.t===k).length})</option>`).join("")+`<option value="K">Konsolidasi — semua use case (${D.G.length} konsep)</option><option value="H">Struktur induk–anak (${(D.H||[]).length} konsep lintas playbook)</option><option value="R">Ringkasan Resource (${Object.keys(D.RS).length} resource)</option><option value="DOC">Dokumentasi & progres pekerjaan</option><option value="REV">Revisi kontributor</option>`;
ssel.innerHTML='<option value="">Semua status</option>'+[...new Set(D.G.map(g=>g.status))].map(s=>`<option>${esc(s)}</option>`).join("")+'<option value="__rev">Ada revisi kontributor</option><option value="__open">Revisi masih terbuka</option>';
document.getElementById("snap").textContent=D.SNAP;
let view="K", focus=null, rsel=null; const open=new Set();
function qre(){const qq=q.value.trim();return qq.length<2?null:new RegExp(qq.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"),"gi")}
function mark(root){const re=qre();if(!re||!root)return;const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:n=>{if(!n.data.trim()||n.parentNode.closest("script,style,mark,select,option,textarea"))return 2;re.lastIndex=0;return re.test(n.data)?1:2}});
 const ns=[];while(w.nextNode()&&ns.length<5000)ns.push(w.currentNode);
 ns.forEach(n=>{const f=document.createDocumentFragment();let last=0;re.lastIndex=0;n.data.replace(re,(m,i)=>{f.append(n.data.slice(last,i));const k=document.createElement("mark");k.textContent=m;f.append(k);last=i+m.length;return m});f.append(n.data.slice(last));n.replaceWith(f);});}
function who(ids,all){if(all&&ids.length===all)return '<span class="dim">semua</span>';const by={};ids.forEach(i=>{const t=VB[i].t;(by[t]=by[t]||[]).push(i)});
 return Object.entries(by).map(([t,is])=>`<a class="lk" href="#${is[0]}" data-go="${t}" data-id="${is[0]}" title="${esc(is.map(i=>i+" "+VB[i].var).join("\n"))}">${esc(t)}${is.length>1?` ×${is.length}`:""}</a>`).join(", ")}
const cut=(t,n)=>t.length>n?t.slice(0,n)+"…":t;
function appliedHTML(g){return g.applied&&g.applied.length?`<div class="pair"><h4>Revisi kontributor yang sudah diterapkan (${g.applied.length})</h4><ul>${g.applied.map(x=>`<li>${esc(x)}</li>`).join("")}</ul><div class="dim" style="font-size:11.5px">Status dan perbandingan di bawah sudah dihitung ulang dengan revisi ini. Ringkasan Resource, Excel, dan JSON masih versi bangunan terakhir.</div></div>`:""}
function exHTML(g){if(!g.ex.length)return '<p class="dim" style="font-size:12.5px">Tidak ada perbedaan elemen yang terdeteksi otomatis.</p>';
 const B=g.ex.filter(x=>x[1]==="beda"),S=g.ex.filter(x=>x[1]==="sebagian");
 const li=x=>`<li><code>${esc(x[0])}</code><ul class="parts">${x[2].map(([t,ids])=>`<li><b>${who(ids)}</b>: ${esc(cut(t,420))}</li>`).join("")}</ul></li>`;
 return (B.length?`<div class="dk">Nilai berbeda antar use case (${B.length} elemen)</div><ul>${B.map(li).join("")}</ul>`:"")+(S.length?`<div class="dl">Elemen hanya dipakai sebagian use case (${S.length} elemen) — biasanya melengkapi</div><ul>${S.map(li).join("")}</ul>`:"");}
function descBtn(id){return `<button type="button" class="descb" data-desc="${id}" aria-label="Deskripsi variabel" title="Deskripsi variabel">ⓘ</button>`}
function badge(g){const c=ST[g.status]||"st-uni"; return (EXPL0[g.status]||(g.ex&&g.ex.length))?`<button type="button" class="st ${c}" data-pop="${g.id}" title="Lihat perbedaan">${esc(g.status)}</button>`:`<span class="st ${c}">${esc(g.status)}</span>`}
function vlink(id){const v=VB[id];return `<a class="lk lkl" href="#${id}" data-go="${v.t}" data-id="${id}">${esc(v.t)} · ${esc(v.var)} <span class="dim">${id}</span></a>`}
function glink(gid){return `<a class="lk lkl" href="#${gid}" data-go="K" data-id="${gid}">${esc(gid)} ${esc(GB[gid].label)}</a>`}
function limited(arr,fn,n=5){return arr.slice(0,n).map(fn).join("")+(arr.length>n?`<span class="dim" style="font-size:11px">+${arr.length-n} lagi (lihat konsolidasi)</span>`:"")}
function listTable(k,self){const L=D.L[k];if(!L)return"";
 const isCode=L.cols[1]==="code";
 const head=L.cols.map(c=>`<th>${esc(c)}</th>`).join("")+(isCode?"<th>Kode juga dipakai di</th>":"");
 const body=L.rows.map(r=>{let also="";if(isCode){const o=(D.C[r[1]]||[]).filter(x=>x!==self&&!(L.users||[]).includes(x));also=`<td>${o.slice(0,3).map(i=>`<a class="lk" href="#${i}" data-go="${VB[i].t}" data-id="${i}">${i}</a>`).join(" ")}${o.length>3?` +${o.length-3}`:""}</td>`}
  return `<tr>${r.map((x,i)=>`<td class="${i===1&&isCode?"c":""}">${esc(x)}</td>`).join("")}${also}</tr>`}).join("");
 const users=(L.users||[]).filter(x=>x!==self);
 return `<div class="inlist" tabindex="0" aria-label="${esc(L.title)}"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div><div class="lmeta">${esc(k)} · ${esc(L.title)} · ${L.rows.length} baris${L.rows.length>6?", gulir untuk melihat semua":""}${users.length?` · daftar yang sama dipakai juga oleh: ${users.slice(0,6).map(i=>`<a class="lk" href="#${i}" data-go="${VB[i].t}" data-id="${i}">${i}</a>`).join(" ")}${users.length>6?` +${users.length-6}`:""}`:""}</div>`}
function fillVsel(){const cur=vsel.value;
 vsel.innerHTML=view==="K"?'<option value="">Semua konsep</option>'+D.G.map(g=>`<option value="${g.id}">${g.id} · ${esc(g.label)}</option>`).join(""):'<option value="">Semua variabel</option>'+D.V.filter(v=>v.t===view&&!v.syn).map(v=>`<option value="${v.id}">${v.id} · ${esc(v.var)}</option>`).join("");
 vsel.value=[...vsel.options].some(o=>o.value===cur)?cur:"";}
function stats(){const pool=view==="K"?D.G:D.V.filter(v=>v.t===view&&!v.syn).map(v=>GB[v.g]);const c={};pool.forEach(g=>c[g.status]=(c[g.status]||0)+1);
 document.getElementById("stats").innerHTML=Object.entries(c).map(([s,n])=>`<button type="button" data-s="${esc(s)}" aria-pressed="${ssel.value===s}"><span class="st ${ST[s]}">${esc(s)}</span> ${n}</button>`).join("");}
function elRows(v){
 const alsoMap={};v.also.forEach(([p,c,o])=>alsoMap[p+"|"+c]=o);const rows=[];
 v.el.forEach((e,j)=>{const np=e[0].replace(/\*/g,"").replace(/\[(i|\d)\]/g,"").replace(/ /g,"");const rep=j>0&&v.el[j-1][0]===e[0];
  const al=alsoMap[np+"|"+e[1]]||[];
  rows.push(`<td class="path${rep?" rep":""}${e[0].startsWith("*")?" mand":""}" data-l="Elemen">${esc(e[0])}</td><td class="val" data-l="Nilai">${esc(e[1])}${e[4]==="rev"?` <span class="tag rev" title="${e[5]?"Nilai dasar SATUSEHAT: "+esc(e[5]):"Ditambahkan lewat revisi kontributor"}">revisi</span>`:""}</td><td class="ket" data-l="Keterangan">${esc(e[2])}</td><td class="also" data-l="Kode juga di">${limited(al,vlink,3)}</td>`);
  if(e[3]) rows.push(`<td colspan="4" class="inl">${listTable(e[3],v.id)}</td>`);});
 return rows;}
const BLOCKS={};
function stepNo(t){const m=/^(\d{1,2})[.]/.exec(t||"");return m?+m[1]:999}
function blocks(t){if(BLOCKS[t])return BLOCKS[t];
 const out=[],ix={};
 D.V.filter(v=>v.t===t).forEach(v=>{if(!(v.tahap in ix)){ix[v.tahap]={tahap:v.tahap,vars:[],ref:null};out.push(ix[v.tahap])}ix[v.tahap].vars.push(v)});
 (D.REF||[]).filter(r=>r.t===t).forEach(r=>{
  if(ix[r.tahap]){ix[r.tahap].ref=r;return}
  const b={tahap:r.tahap,vars:[],ref:r},n=stepNo(r.tahap);
  let at=out.findIndex(x=>stepNo(x.tahap)>n);if(at<0)at=out.length;
  out.splice(at,0,b);ix[r.tahap]=b;});
 BLOCKS[t]=out;return out}
function refRow(r,cols){const links=r.tg.map(([c,j,u])=>`<a class="lk" href="${esc(u)}" target="_blank" rel="noopener">Buka playbook ${esc(j)} ↗</a>`+(TN[c]?` · <a class="lk" href="#" data-go="${c}" data-id="">lihat ${esc(c)} di dokumentasi ini</a>`:"")).join("<br>");
 return `<tr class="ref"><td colspan="${cols}"><span class="rj">⤷ Mengikuti modul lain</span> — ${esc(r.note)}${r.kutipan?`<div class="dim" style="font-size:11.5px;margin-top:2px">“${esc(r.kutipan)}”</div>`:""}${r.isi?`<div class="dim" style="font-size:11.5px;margin-top:2px">Bagian yang dirujuk: ${esc(r.isi)}</div>`:""}<div style="margin-top:4px">${links}</div></td></tr>`}
function supRows(v){if(!v.sup||!v.sup.length)return [];
 return v.sup.map(x=>{const key=x[0],coded=x[1],star=x[2],body=x[3],lists=x[4],src=x[5];
  const who=src.map(i=>`<a class="lk" href="#${i}" data-go="${VB[i].t}" data-id="${i}">${esc(VB[i].t)} · ${i}</a>`).join(", ");
  let val="";
  if(coded)val=body.slice(0,3).map(o=>`<code>${esc(o[1])}</code> ${esc(o[2]||"")}`).join("<br>")+(body.length>3?`<div class="dim">+${body.length-3} pilihan lagi</div>`:"");
  else val=body.slice(0,3).map(o=>esc(o[0])).join("<br>")+(body.length>3?`<div class="dim">+${body.length-3} nilai lagi</div>`:"");
  if(!val)val=lists.length?'<span class="dim">(pilih dari daftar di bawah)</span>':'<span class="dim">(nilai tidak dirinci)</span>';
  const lst=lists.length?lists.map(l=>listTable(l,v.id)).join(""):"";
  return `<td class="path" data-l="Elemen">${star?"*":""}${esc(key)} <span class="tag sup">pelengkap</span></td><td class="val" data-l="Nilai">${val}</td><td class="ket" data-l="Keterangan">Dilengkapi dari playbook lain: ${who}${lst}</td><td class="also"></td>`});}
const PER={item:"item kuesioner",komponen:"komponen",section:"bagian dokumen",kelompok:"kelompok"};
function ancOf(v){const out=[];let x=v,g=0;while(x&&x.ind&&VB[x.ind]&&g++<8){out.push(x.ind);x=VB[x.ind]}return out}
function treeOrder(vs){const inB=new Set(vs.map(v=>v.id)),seen=new Set(),out=[];
 function emit(v,d){if(seen.has(v.id))return;seen.add(v.id);out.push([v,d]);
  (v.anak||[]).forEach(cid=>{const c=VB[cid];if(c&&inB.has(cid))emit(c,d+1)})}
 vs.forEach(v=>{if(!v.ind||!inB.has(v.ind))emit(v,0)});
 vs.forEach(v=>emit(v,0));
 return out}
function phRow(v,d,cols){const n=(v.anak||[]).length;
 return `<tr class="ph" data-anc="${ancOf(v).join(" ")}" id="${v.id}"><td colspan="${cols}"><span style="display:inline-block;width:${d*16}px"></span><button type="button" class="tgb" data-tg="${v.id}">▾</button><b>${esc(v.var)}</b> <span class="tag kelompok">kelompok</span> <span class="dim">${n} variabel · ${esc(v.id)}</span>${descBtn(v.id)}</td></tr>`}
function renderTitle(){
 const qq=q.value.toLowerCase().trim(),sv=vsel.value,ss=ssel.value;
 let h='<div class="tbl"><table class="main"><colgroup><col style="width:22%"><col style="width:27%"><col style="width:21%"><col style="width:17%"><col style="width:13%"></colgroup><thead><tr><th>Variabel & muncul di</th><th>Elemen / path FHIR</th><th>Nilai</th><th>Keterangan</th><th>Kode juga dipakai di</th></tr></thead><tbody>';
 let n=0;
 blocks(view).forEach(B=>{
  let vs=B.vars.filter(v=>{const g=GB[v.g];return v.syn?(!sv&&!ss&&(!qq||v._s.includes(qq))):(!(sv&&v.id!==sv)&&stMatch(g,ss,[v.id,g.id])&&!(qq&&!v._s.includes(qq)))});
  if(vs.length){const keep=new Set(vs.map(v=>v.id));vs.forEach(v=>ancOf(v).forEach(a=>keep.add(a)));
   vs=B.vars.filter(v=>keep.has(v.id));}
  const refOK=B.ref&&!sv&&!ss&&(!qq||(B.tahap+" "+B.ref.note+" "+B.ref.kutipan+" "+B.ref.isi).toLowerCase().includes(qq));
  if(!vs.length&&!refOK)return;
  h+=`<tr class="step"><td colspan="5">${esc(B.tahap)}</td></tr>`;
  if(refOK)h+=refRow(B.ref,5);
  treeOrder(vs).forEach(([v,dep])=>{
  if(v.syn){h+=phRow(v,dep,5);return}
  const g=GB[v.g];
  n++;const others=g.m.filter(x=>x!==v.id);
  let mu=`<div class="muncul"><b>Konsolidasi</b>${glink(g.id)}`;
  if(others.length)mu+=`<b>Juga muncul di</b>`+limited(others,vlink);
  if(g.rel.length)mu+=`<b>Terkait</b>`+limited(g.rel.map(r=>r[0]),glink,4);
  mu+="</div>";
  const rows=elRows(v),sup=supRows(v);const all=rows.concat(sup);
  const anc=ancOf(v).join(" ");
  all.forEach((c,j)=>{h+=`<tr class="${j>=rows.length?"sub sup":(j?"sub":"first")}" data-anc="${anc}">`+(j?"":`<td class="var" rowspan="${all.length}" id="${v.id}" data-l="Variabel" style="padding-left:${10+dep*16}px!important"><span class="id">${v.id}</span>${dep?'<span class="dim"> └</span>':""}${v.per&&v.ind?`<span class="tag ${v.per}">${esc(PER[v.per]||v.per)}</span>`:""}${(v.anak||[]).length?`<button type="button" class="tgb" data-tg="${v.id}" title="Sembunyikan/tampilkan ${v.anak.length} sub-variabel">${v.anak.length} sub ▾</button>`:""}<span class="kel">${esc(v.kel)}</span><span class="nm">${esc(v.var)} ${descBtn(v.id)}</span><span class="pill">${esc(v.res)}</span>${v.a?'<span class="pill" style="background:var(--warn-bg);color:var(--warn)" title="Diekstraksi otomatis dari halaman/PDF SATUSEHAT, belum dicek manual">otomatis</span>':""}${v.rev?'<span class="tag rev" title="Ada revisi kontributor yang sudah diterapkan pada variabel ini">direvisi</span>':""}${badge(g)}${revBtn(v.id)}${v.frek?`<span class="freq">${esc(v.frek)}</span>`:""}${mu}${v.cat?`<span class="note">${esc(v.cat)}</span>`:""}${v.sup&&v.sup.length?`<span class="note">${v.sup.length} elemen pelengkap dari playbook lain ditampilkan di bawah baris variabel ini.</span>`:""}</td>`)+c+"</tr>"});
 });});
 document.getElementById("out").innerHTML=h+(n?"":'<tr><td colspan="5" class="dim">Tidak ada variabel yang cocok dengan filter.</td></tr>')+"</tbody></table></div>";
 document.getElementById("count").textContent=n+" variabel";}
function optTable(rows,all,std){
 return `<div class="inlist" tabindex="0"><table><thead><tr><th>system</th><th>code</th><th>display</th><th>keterangan</th><th>dipakai di</th></tr></thead><tbody>${rows.map(o=>`<tr><td class="c">${esc(o[0])}</td><td class="c">${esc(o[1])}</td><td>${esc(o[2])}</td><td>${esc(o[3])}</td><td>${who(o[4],all)}</td></tr>`).join("")}</tbody></table></div>`}
function kbody(g){
 let h=`<div class="muncul" style="display:flex;flex-wrap:wrap;gap:2px 22px"><div><b>Variabel</b>${g.m.map(i=>`<div>${vlink(i).replace('lkl"','lkl" style="display:inline"')} ${descBtn(i)}</div>`).join("")}</div>${g.rel.length?`<div><b>Terkait</b>${g.rel.map(([rid,nt])=>glink(rid)+(nt?`<span class="dim" style="font-size:11px;display:block;max-width:60ch">${esc(nt)}</span>`:"")).join("")}</div>`:""}</div>${g.note?`<span class="note">${esc(g.note)}</span>`:""}`;
 const kind={};g.ex.forEach(x=>kind[x[0]]=x[1]);const N=g.m.length;
 h+=`<div class="els">`+g.els.map(([key,coded,star,ids,body,lists])=>{
  const k=kind[key];const all=ids.length===N;
  let hd=`<div class="eh"><code class="${star?"mand":""}">${star?"*":""}${esc(key)}</code><span>${N>1?(all?`<span class="dim">semua ${N} variabel</span>`:"dipakai di: "+who(ids)):""}</span>${k?`<span class="tag ${k}">${k==="beda"?"nilai berbeda":"hanya sebagian"}</span>`:""}</div>`;
  let bd="";
  if(coded){const same=body.length&&body.every(o=>o[4].length===ids.length);
   if(body.length===1)bd=`<div class="ev"><code>${esc(body[0][0])}</code> · <b>${esc(body[0][1])}</b> ${esc(body[0][2])}${body[0][3]?` <span class="dim">— ${esc(body[0][3])}</span>`:""}</div>`;
   else if(body.length)bd=optTable(body,same?body[0][4].length:N);}
  else{const vs=body.filter(x=>!(x[0]||"").startsWith("(wajib — nilai"));
   if(vs.length===1&&vs[0][2].length===ids.length)bd=`<div class="ev">${esc(vs[0][0])}${vs[0][1]?` <span class="dim">— ${esc(vs[0][1])}</span>`:""}</div>`;
   else if(vs.length)bd=`<div class="ev">${vs.map(x=>`<div>${esc(x[0])}${x[1]?` <span class="dim">— ${esc(x[1])}</span>`:""} <span style="font-size:11px">[${who(x[2],N)}]</span></div>`).join("")}</div>`;
   else if(body.length)bd=`<div class="ev dim">wajib — nilai tidak dirinci di playbook</div>`;}
  bd+=lists.map(([l,li])=>`<div class="ev">Daftar <b>${esc(l)}</b> dipakai oleh ${who(li,N)}${listTable(l,null)}</div>`).join("");
  return `<div class="el${k?" d-"+k:""}">${hd}${bd}</div>`}).join("")+`</div>`;
 return h;}
let AUTO_OPEN=new Set();
function renderK(){
 const qq=q.value.toLowerCase().trim(),sv=vsel.value,ss=ssel.value;let h='<div class="klist">',n=0;
 AUTO_OPEN=new Set();if(qq){const hits=D.G.filter(g=>(!sv||g.id===sv)&&stMatch(g,ss,[g.id,...g.m])&&g._s.includes(qq));if(hits.length<=25)hits.forEach(g=>AUTO_OPEN.add(g.id));}
 D.G.forEach(g=>{if(sv&&g.id!==sv)return;if(!stMatch(g,ss,[g.id,...g.m]))return;
  if(qq&&!g._s.includes(qq))return;n++;
  const titles=D.T.map(t=>t[0]).filter(t=>g.m.some(i=>VB[i].t===t));const isO=open.has(g.id)||(qq&&AUTO_OPEN.has(g.id));
  h+=`<div class="krow${isO?" open":""}" id="${g.id}"><div class="khead" data-k="${g.id}" role="button" tabindex="0" aria-expanded="${isO}"><span class="car">▶</span><span class="id">${g.id}</span><span class="lb">${esc(g.label)}${g.applied?'<span class="tag rev" title="Ada revisi kontributor yang sudah diterapkan">direvisi</span>':""}</span><span>${badge(g)}${revBtn(g.id,true)}</span><span class="tt">${titles.map(t=>`<span class="pill">${esc(t)}</span>`).join("")}</span><span class="n">${g.m.length} var</span></div>${isO?`<div class="kbody">${kbody(g)}</div>`:""}</div>`;});
 document.getElementById("out").innerHTML=h+(n?"":'<div class="dim" style="padding:12px">Tidak ada konsep yang cocok dengan filter.</div>')+"</div>";
 document.getElementById("count").textContent=n+" konsep · "+open.size+" terbuka";}
function toggleK(id){const wasO=open.has(id)||AUTO_OPEN.has(id);AUTO_OPEN.delete(id);wasO?open.delete(id):open.add(id);const row=document.getElementById(id);if(!row)return;const isO=open.has(id);row.classList.toggle("open",isO);row.querySelector(".khead").setAttribute("aria-expanded",isO);
 const b=row.querySelector(".kbody");if(isO&&!b){row.insertAdjacentHTML("beforeend",`<div class="kbody">${kbody(GB[id])}</div>`);mark(row.querySelector(".kbody"));}if(!isO&&b)b.remove();document.getElementById("count").textContent=document.querySelectorAll(".krow").length+" konsep · "+open.size+" terbuka";}
const LVL="Inti = dipakai ≥80% variabel yang memakai resource ini · Umum = 40–79% · Kadang = 10–39% · Jarang = <10%";
function pct(x){return Math.round(x*100)+"%"}
function whoN(ids){const by={};ids.forEach(i=>{const t=VB[i].t;(by[t]=by[t]||[]).push(i)});return Object.entries(by).map(([t,is])=>`<a class="lk" href="#${is[0]}" data-go="${t}" data-id="${is[0]}" title="${esc(is.slice(0,30).map(i=>i+" "+VB[i].var).join("\n"))}">${esc(t)}${is.length>1?` ×${is.length}`:""}</a>`).join(", ")}
function pathHTML(p,nv){
 let h=`<div class="rp"><div class="eh"><code>${esc(p.p)}</code><span class="dim">${p.n} variabel</span></div>`;
 const st=p.std;
 if(p.coded){const rows=p.vals.slice().sort((a,b)=>b[3].length-a[3].length);
  const ex=st?st.extra:[];
  h+=`<div class="inlist" tabindex="0"><table><thead><tr><th>system</th><th>code</th><th>display</th><th>dipakai di</th></tr></thead><tbody>${rows.map(o=>`<tr><td class="c">${esc(o[0])}</td><td class="c">${esc(o[1])}</td><td>${esc(o[2])}</td><td>${whoN(o[3])}</td></tr>`).join("")}${ex.map(o=>`<tr class="std"><td class="c">${esc(o[0])}</td><td class="c">${esc(o[1])}</td><td>${esc(o[2]||o[3])}</td><td><span class="tag std">Lampiran Std. Terminologi</span></td></tr>`).join("")}</tbody></table></div>`;}
 else if(p.vals.length){const rows=p.vals.slice().sort((a,b)=>b[1].length-a[1].length);
  h+=`<div class="inlist" tabindex="0"><table><thead><tr><th>nilai</th><th>dipakai di</th></tr></thead><tbody>${rows.map(o=>`<tr><td>${esc(o[0])}</td><td>${whoN(o[1])}</td></tr>`).join("")}</tbody></table></div>`;}
 Object.entries(p.lists||{}).forEach(([l,ids])=>{h+=`<div class="ev">Daftar <b>${esc(l)}</b> (${D.L[l]?D.L[l].rows.length:0} baris) dipakai di ${whoN(ids)}${listTable(l,null)}</div>`});
 if(st)h+=`<div class="lmeta"><span class="tag std">Lampiran Standar Terminologi</span> ${esc(st.sec.join("; "))} — ${st.n} kode di lampiran${p.coded?`, ${st.extra.length} belum muncul di playbook mana pun (baris berwarna)`:""}.${st.note.length&&!st.n?" "+esc(cut(st.note.join(" "),400)):""}</div>`;
 return h+"</div>";}
function relBody(e,R){let h="";
 const ch=Object.entries(e.choices||{});
 if(ch.length)h+=`<div class="ev"><b>Tipe data ${esc(e.el)} — pilih salah satu, tidak perlu semuanya:</b> ${ch.map(([c,n])=>`<code>${esc(c)}</code> ${n} var`).join(" · ")}</div>`;
 if(e.star.length)h+=`<div class="ev">Ditandai wajib (*) di: ${e.star.map(esc).join(", ")}</div>`;
 h+=`<div class="ev dim">Dipakai di: ${R.titles.filter(t=>e.cov[t]).map(t=>`${esc(t)} ${e.cov[t]}/${R.tv[t]}`).join(" · ")}</div>`;
 return h+e.paths.map(p=>pathHTML(p,R.nv)).join("");}
function renderR(){const qq=q.value.toLowerCase().trim();let h="";const out=document.getElementById("out");
 if(!rsel||!D.RS[rsel]){rsel=null;
  const rts=Object.keys(D.RS).filter(r=>!qq||RSS[r].includes(qq)).sort((a,b)=>D.RS[b].nv-D.RS[a].nv);
  h=`<p class="dim" style="font-size:12.5px;margin:6px 0">Pilih resource untuk melihat elemen apa saja yang dipakai lintas playbook, seberapa sering (${LVL}), nilai/kode yang dipakai, dan kode tambahan dari ${esc(D.STD)}.</p><div class="rcards">`+rts.map(r=>{const R=D.RS[r];const u=R.els.length;return `<button type="button" class="rcard" data-rs="${r}"><b>${esc(r)}</b><span>${R.nv} variabel · ${R.titles.length} use case</span><span>${u} elemen dipakai${R.canon?` · ${R.unused.length} elemen baku belum pernah dipakai`:""}</span><span>Inti: ${R.core.map(esc).join(", ")||"—"}</span>${R.miss.length?`<span style="color:var(--warn)">${R.miss.length} variabel tanpa elemen inti</span>`:""}</button>`}).join("")+"</div>";
  out.innerHTML=h;document.getElementById("count").textContent=rts.length+" resource";mark(out);return;}
 const R=D.RS[rsel];
 h=`<button type="button" class="back" data-rs="">← Semua resource</button><h2 style="font:600 20px var(--disp);margin:10px 0 2px">Ringkasan elemen ${esc(rsel)}</h2><p class="dim" style="font-size:12.5px;margin:0 0 8px">${R.nv} variabel (${R.npar} induk/variabel tunggal setelah sub-variabel dikelompokkan) dari ${R.titles.length} use case memakai ${esc(rsel)}. ${LVL}. Elemen bertipe pilihan ([x], mis. value[x]) dihitung sekali — cukup salah satu tipe datanya yang diisi.</p>`;
 const mc=R.els.filter(e=>e.pct>=0.4).slice(0,14);
 if(mc.length)h+=`<div class="sec"><h3>Kelengkapan per use case</h3><p class="dim" style="font-size:12px;margin:0 0 6px">Persentase variabel ${esc(rsel)} di tiap use case yang memuat elemen inti/umum. Sel kosong = elemen tidak pernah dipakai di use case itu.</p><div class="tbl"><table class="mx"><thead><tr><th>Use case (variabel)</th>${mc.map(e=>`<th>${esc(e.el)}</th>`).join("")}</tr></thead><tbody>${R.titles.map(t=>`<tr><td>${esc(t)} (${R.tv[t]})</td>${mc.map(e=>{const x=(e.cov[t]||0)/R.tv[t];return `<td style="background:color-mix(in srgb,var(--ok-bg) ${Math.round(x*100)}%,transparent)">${x?pct(x):""}</td>`}).join("")}</tr>`).join("")}</tbody></table></div></div>`;
 h+=`<div class="sec"><h3>Elemen yang dipakai (${R.els.length})</h3>`+R.els.map((e,i)=>{const op=qq&&JSON.stringify(e).toLowerCase().includes(qq);
  return `<details class="rel" data-ri="${i}"${op?" open":""}><summary><code>${esc(e.el)}</code><span class="tag ${e.lvl}">${e.lvl}</span><span class="bar"><i style="width:${pct(e.pct)}"></i></span><span>${e.n}/${R.nv} variabel (${pct(e.pct)})</span><span class="dim">${e.np||0}/${R.npar||0} induk</span><span class="dim">${e.titles.length}/${R.titles.length} use case</span>${e.star.length?`<span class="dim">wajib di ${e.star.length} use case</span>`:""}${!e.canon&&R.canon?'<span class="tag sebagian" title="Tidak ada di daftar elemen baku FHIR R4 untuk resource ini — bisa extension, salah ketik di playbook, atau salah baca saat ekstraksi otomatis">bukan elemen baku — cek</span>':""}${Object.keys(e.choices||{}).length?`<span class="dim">tipe: ${Object.keys(e.choices).map(esc).join(" | ")}</span>`:""}</summary><div class="rb">${op?relBody(e,R):""}</div></details>`}).join("")+"</div>";
 if(R.unused.length)h+=`<div class="sec"><h3>Elemen baku FHIR yang belum pernah dipakai (${R.unused.length})</h3><div class="chips">${R.unused.map(u=>`<span class="pill">${esc(u)}</span>`).join("")}</div></div>`;
 if(R.stdonly.length)h+=`<div class="sec"><h3>Hanya ada di Lampiran Standar Terminologi (${R.stdonly.length} path)</h3><p class="dim" style="font-size:12px;margin:0 0 6px">Path ${esc(rsel)} yang punya ketentuan terminologi di ${esc(D.STD)} tetapi tidak muncul di playbook mana pun.</p>`+R.stdonly.map(x=>`<details class="rel"><summary><code>${esc(x.path)}</code><span class="tag std">Lampiran Std. Terminologi</span><span class="dim">${esc(x.sec)} · ${x.rows.length} kode</span></summary><div class="rb">${x.note?`<div class="ev dim">${esc(cut(x.note,500))}</div>`:""}${x.rows.length?`<div class="inlist"><table><thead><tr><th>system</th><th>code</th><th>display</th><th>keterangan</th></tr></thead><tbody>${x.rows.map(r=>`<tr><td class="c">${esc(r[0])}</td><td class="c">${esc(r[1])}</td><td>${esc(r[2])}</td><td>${esc(r[3])}</td></tr>`).join("")}</tbody></table></div>`:""}</div></details>`).join("")+"</div>";
 if(R.miss.length)h+=`<div class="sec"><h3>Variabel tanpa elemen inti (${R.miss.length})</h3><p class="dim" style="font-size:12px;margin:0 0 6px">Variabel ${esc(rsel)} yang tidak memuat elemen yang biasanya ada (Inti). Bisa berarti playbook memang tidak merinci, atau ada yang terlewat.</p><details class="rel"><summary>Tampilkan daftar</summary><div class="rb">${R.miss.map(([i,m])=>`<div class="ev">${vlink(i).replace('lkl"','lkl" style="display:inline"')} — tidak ada: ${m.map(x=>`<code>${esc(x)}</code>`).join(", ")}</div>`).join("")}</div></details></div>`;
 out.innerHTML=h;document.getElementById("count").textContent=R.els.length+" elemen";mark(out);}
document.addEventListener("toggle",e=>{const d=e.target;if(!(d.matches&&d.matches("details.rel[data-ri]"))||!d.open)return;const b=d.querySelector(".rb");if(b.innerHTML)return;const R=D.RS[rsel];b.innerHTML=relBody(R.els[+d.dataset.ri],R);mark(b);},true);
function renderREV(){const all=[...REV,...CSVREV],out=document.getElementById("out"),qq=q.value.toLowerCase().trim();
 const rows=all.filter(r=>!qq||JSON.stringify(r).toLowerCase().includes(qq));
 const nm=r=>esc(r.authorName||PROF[r.author]||"Kontributor");
 let h=`<p class="dim" style="font-size:12.5px;margin:6px 0">Usulan revisi dari kontributor, terpisah dari data dasar SATUSEHAT. Kontributor mengisi form lewat tombol <b>Revisi</b> di variabel/konsep mana pun, lalu klik <b>Unduh usulan (.csv)</b> dan mengirim berkasnya ke pengelola. Pengelola cukup mengunggah berkas itu ke folder <code>docs/revisi/</code> di GitHub — halaman ini langsung memuatnya, tanpa perlu membangun ulang apa pun.<br>Baris yang mengisi kolom <code>aksi</code> (<code>ganti-nilai</code>, <code>pindah-konsep</code>, <code>tandai-status</code>, <code>tambah-pilihan</code>, <code>tambah-elemen</code>, <code>jadikan-anak</code>, <code>lepas-anak</code>) <b>diterapkan ke isi halaman</b> begitu kolom <code>status</code> diubah menjadi <code>diterima</code>; status konsep dan perbandingan antar use case ikut dihitung ulang. Ringkasan Resource, Excel, dan JSON tetap versi bangunan terakhir sampai dibangun ulang.</p>`;
 if(!all.length)h+=`<div class="dim" style="padding:12px">Belum ada revisi kontributor yang dimuat. <a class="lk" href="${esc(D.GH)}/tree/main/docs/revisi" target="_blank" rel="noopener">Lihat folder revisi di GitHub</a></div>`;
 else h+=`<div class="tbl"><table class="main" style="min-width:1000px"><thead><tr><th>Target</th><th>Elemen</th><th>Jenis</th><th>Usulan</th><th>Alasan</th><th>Pengusul</th><th>Tanggal</th><th>Status</th><th>Aksi otomatis</th><th>Sumber</th></tr></thead><tbody>${rows.map(r=>{
  const t=VB[r.target]?`${esc(VB[r.target].t)} · ${esc(VB[r.target].var)}`:(GB[r.target]?esc(GB[r.target].label):esc(r.target));
  return `<tr><td><a class="lk" href="#${r.target}" data-go="${GB[r.target]?"K":(VB[r.target]?VB[r.target].t:"K")}" data-id="${r.target}">${esc(r.target)}</a><div class="dim" style="font-size:11px">${t}</div></td><td class="path">${esc(r.element||"")}</td><td>${esc(KIND[r.kind]||r.kind||"")}</td><td class="ket">${esc(r.proposed||"")}</td><td class="ket">${esc(r.reason||"")}</td><td>${nm(r)}${r.institution?`<div class="dim" style="font-size:11px">${esc(r.institution)}</div>`:""}</td><td class="dim">${esc((r.createdAt||"").slice(0,10))}</td><td>${esc(r.status||"")}</td><td style="font-size:11.5px">${r.aksi?`<code>${esc(r.aksi)}</code>${r.applied?' <span class="tag rev">diterapkan</span>':(r.status==="diterima"?' <span class="tag sebagian">gagal / tidak cocok</span>':' <span class="dim">menunggu status “diterima”</span>')}`:'<span class="dim">catatan saja</span>'}</td><td class="dim" style="font-size:11px">${r.src==="csv"?esc(r.file):"halaman Claude"}</td></tr>`}).join("")}</tbody></table></div>`;
 out.innerHTML=h;document.getElementById("count").textContent=rows.length+" revisi";mark(out);}
function renderH(){const qq=q.value.toLowerCase().trim(),out=document.getElementById("out");
 const hs=(D.H||[]).filter(h=>!qq||JSON.stringify(h).toLowerCase().includes(qq));
 let h=`<p class="dim" style="font-size:12.5px;margin:6px 0">Variabel yang sebenarnya satu kesatuan — item kuesioner bertingkat (<code>linkId</code>), komponen satu pengukuran, bagian dokumen (<code>Composition.section</code>), dan kelompok bawaan playbook — ditampilkan sebagai induk beserta anaknya. Di sini induk yang muncul di lebih dari satu playbook dibandingkan: baris = sub-variabel, kolom = use case, sehingga terlihat modul mana yang tidak memuat item tertentu. Hierarki per playbook bisa dilihat langsung di tampilan use case masing-masing.</p>`;
 h+=hs.map(x=>{const cols=x.titles;
  return `<div class="el" id="${x.id}" style="padding:10px 12px"><div class="eh"><span class="id">${x.id}</span><b style="font-size:14px">${esc(x.label)}</b><span class="dim">${x.m.length} induk · ${x.nchild} sub-variabel</span>${cols.map(t=>`<span class="pill">${esc(t)}</span>`).join("")}</div>
  <div class="dim" style="font-size:11.5px;margin:2px 0 6px">Induk: ${x.m.map(i=>`<a class="lk" href="#${i}" data-go="${VB[i].t}" data-id="${i}">${esc(VB[i].t)} · ${esc(VB[i].var)} (${i})</a>`).join(" · ")}</div>
  <div class="tbl"><table class="mx"><thead><tr><th>Sub-variabel</th>${cols.map(t=>`<th>${esc(t)}</th>`).join("")}</tr></thead><tbody>${x.rows.map(r=>`<tr><td>${esc(r.label)}${r.gid?` <a class="lk" href="#${r.gid}" data-go="K" data-id="${r.gid}">${r.gid}</a>`:""}</td>${cols.map(t=>{const ids=r.by[t]||[];return `<td>${ids.length?ids.map(i=>`<a class="lk" href="#${i}" data-go="${t}" data-id="${i}" title="${esc(VB[i].var)}">✓</a>`).join(" "):'<span class="dim">—</span>'}</td>`}).join("")}</tr>`).join("")}</tbody></table></div></div>`}).join("");
 out.innerHTML=h||'<div class="dim" style="padding:12px">Tidak ada yang cocok.</div>';document.getElementById("count").textContent=hs.length+" konsep induk";mark(out);}
function render(){if(view==="H"){vsel.hidden=ssel.hidden=true;document.getElementById("stats").hidden=true;document.getElementById("openall").hidden=document.getElementById("closeall").hidden=true;tsel.value=view;renderH();return;}
 if(view==="REV"){vsel.hidden=ssel.hidden=true;document.getElementById("stats").hidden=true;document.getElementById("openall").hidden=document.getElementById("closeall").hidden=true;tsel.value=view;renderREV();return;}
 if(view==="DOC"){vsel.hidden=ssel.hidden=true;document.getElementById("stats").hidden=true;document.getElementById("openall").hidden=document.getElementById("closeall").hidden=true;tsel.value=view;const o=document.getElementById("out");o.innerHTML=`<article class="doc">${D.DOC}</article>`;document.getElementById("count").textContent="";mark(o);return;}
 const r=view==="R";vsel.hidden=r;ssel.hidden=r;document.getElementById("stats").hidden=r;if(!r){fillVsel();stats();}const k=view==="K";document.getElementById("openall").hidden=!k;document.getElementById("closeall").hidden=!k;
 r?renderR():(k?renderK():renderTitle());tsel.value=view;if(!r)mark(document.getElementById("out"));
 if(focus){const el=document.getElementById(focus);if(el){el.scrollIntoView({block:"start"});window.scrollBy(0,-70);(el.closest("tr")||el).classList.add("hl");}focus=null;}}
function go(v,id){if(v!==view){view=v;rsel=null;vsel.value="";ssel.value="";q.value="";}if(id&&v==="K")open.add(id);focus=id;if(id&&!document.getElementById(id)){vsel.value="";ssel.value="";q.value="";}render();}
function showPop(gid,anchor){const g=GB[gid],p=document.getElementById("pop");
 p.innerHTML=`<button class="x" type="button" aria-label="Tutup">×</button><h3>${esc(g.id)} · ${esc(g.label)}</h3><span class="st ${ST[g.status]}">${esc(g.status)}</span> <span class="dim" style="font-size:12px">${g.m.length} variabel: ${who(g.m)}</span><p style="font-size:12.5px;margin:6px 0">${esc(EXPL[g.status]||"")}</p>${g.note?`<p style="font-size:12.5px;margin:6px 0"><b>Catatan:</b> ${esc(g.note)}</p>`:""}${appliedHTML(g)}${exHTML(g)}`;
 placePop(p,anchor);}
function showDesc(id,anchor){const v=VB[id],d=D.DS[id]||[0,"",""],p=document.getElementById("pop");
 p.innerHTML=`<button class="x" type="button" aria-label="Tutup">×</button><h3>${esc(v.var)}</h3><span class="id">${id} · ${esc(TN[v.t]||v.t)} · ${esc(v.tahap)}</span><div style="margin:6px 0">${d[0]?'<span class="st st-ok">Dari playbook</span>':'<span class="st st-warn">Dibuat Claude — belum diverifikasi</span>'}</div><p style="font-size:13px;margin:6px 0">${esc(d[1])}</p>${d[0]?"":'<p class="dim" style="font-size:11.5px;margin:4px 0">Playbook tidak memuat deskripsi khusus untuk variabel ini; teks di atas disusun otomatis dari nama variabel, resource, kode utama, dan tipe nilainya.</p>'}${d[2]?`<details><summary style="cursor:pointer;font-size:12px">Konteks tahap dari playbook</summary><p style="font-size:12px;margin:4px 0">${esc(d[2])}</p></details>`:""}`;
 placePop(p,anchor);mark(p);}
function placePop(p,anchor){p.hidden=false;const r=anchor.getBoundingClientRect(),w=p.offsetWidth,hh=p.offsetHeight;
 let x=Math.min(r.left,window.innerWidth-w-16),y=r.bottom+6;if(y+hh>window.innerHeight-8)y=Math.max(8,r.top-hh-6);p.style.left=Math.max(16,x)+"px";p.style.top=y+"px";p.querySelector(".x").focus();}
document.addEventListener("click",e=>{
 const pb=e.target.closest("[data-pop]");if(pb){e.preventDefault();e.stopPropagation();showPop(pb.dataset.pop,pb);mark(document.getElementById("pop"));return;}
 const db=e.target.closest("[data-desc]");if(db){e.preventDefault();e.stopPropagation();showDesc(db.dataset.desc,db);return;}
 const rc=e.target.closest("[data-rs]");if(rc){rsel=rc.dataset.rs||null;window.scrollTo(0,0);render();return;}
 const pop=document.getElementById("pop");if(!pop.hidden&&(e.target.closest(".x")||!e.target.closest("#pop"))){pop.hidden=true;}
 const a=e.target.closest("a[data-go]");if(a){e.preventDefault();go(a.dataset.go,a.dataset.id);return;}
 const tg=e.target.closest("[data-tg]");if(tg){const id=tg.dataset.tg;const on=tg.textContent.indexOf("▾")>=0;
  document.querySelectorAll('tr[data-anc~="'+id+'"]').forEach(r=>r.classList.toggle("hide",on));
  tg.textContent=tg.textContent.replace(on?"▾":"▸",on?"▸":"▾");return;}
 const kh=e.target.closest(".khead");if(kh)toggleK(kh.dataset.k);
 const sb=e.target.closest(".stats button");if(sb){ssel.value=ssel.value===sb.dataset.s?"":sb.dataset.s;render();}});
document.addEventListener("keydown",e=>{if(e.key==="Escape")document.getElementById("pop").hidden=true;const kh=e.target.closest&&e.target.closest(".khead");if(kh&&(e.key==="Enter"||e.key===" ")){e.preventDefault();toggleK(kh.dataset.k);}});
document.getElementById("openall").onclick=()=>{document.querySelectorAll(".krow").forEach(r=>open.add(r.id));renderK();};
document.getElementById("closeall").onclick=()=>{open.clear();renderK();};
tsel.addEventListener("change",()=>go(tsel.value,null));
[q,vsel,ssel].forEach(x=>x.addEventListener("input",render));
function revBtn(id,grp){const ids=grp?[id,...GB[id].m]:[id];const rs=ids.flatMap(revFor);const ok=rs.some(r=>r.kind==="resolve"&&r.status==="diterima");
 return (ok?'<span class="revok">✔ Diselesaikan</span>':"")+`<button type="button" class="revbtn${rs.length?" has":""}" data-rev="${id}" title="Revisi kontributor">Revisi${rs.length?` (${rs.length})`:""}</button>`}
let DB=null,USER=null,ME=null,CANEDIT=false,drawerId=null,PROF={};
const KIND={resolve:"Resolve perbedaan",usulan:"Usulan revisi nilai",tambahpilihan:"Tambah pilihan jawaban",tambahelemen:"Tambah elemen baru",catatan:"Catatan"};
const inst0=(()=>{try{return localStorage.getItem("ss_inst")||""}catch(e){return ""}})();
const REVHDR=["target","elemen","jenis","usulan","alasan","kontributor","institusi","tanggal","status","aksi","path","nilai_lama","nilai_baru","tujuan"];const MYROWS=[];
function MYNAME(){let n="";try{n=localStorage.getItem("ss_nama")||""}catch(e){}
 if(!n){n=(prompt("Nama Anda (untuk dicatat sebagai pengusul):")||"").trim();try{localStorage.setItem("ss_nama",n)}catch(e){}}
 return n}
async function names(ids){if(!USER)return;const need=ids.filter(i=>i&&!(i in PROF));if(!need.length)return;try{const ps=await USER.profiles(need);for(const i of need)PROF[i]=(ps[i]&&ps[i].name)||""}catch(e){}}
function openDrawer(id){drawerId=id;document.getElementById("drawer").hidden=false;renderDrawer();}
async function renderDrawer(){if(!drawerId)return;const isG=drawerId.startsWith("K-");const g=isG?GB[drawerId]:GB[VB[drawerId].g];
 const ids=isG?[drawerId,...g.m]:[drawerId];const rs=ids.flatMap(revFor).sort((a,b)=>(b.createdAt||"").localeCompare(a.createdAt||""));
 await names(rs.map(r=>r.author));
 document.getElementById("dtitle").textContent=isG?`${g.id} · ${g.label}`:`${drawerId} · ${VB[drawerId].var}`;
 document.getElementById("dsub").innerHTML=`${esc(g.status)} · data dasar: ${esc(D.SNAP)}`;
 let h=`<div class="rev"><span class="src base">SATUSEHAT</span> <b>${esc(g.status)}</b><div class="meta">Data dasar dari dokumen resmi (${esc(D.SNAP)})</div>${g.note?`<div>${esc(g.note)}</div>`:""}${appliedHTML(g)}${g.ex.length?`<div style="margin-top:6px"><b>Yang perlu dicek / direvisi:</b></div>${exHTML(g)}`:'<div class="meta">Tidak ada perbedaan otomatis.</div>'}</div>`;
 h+=`<div class="rev"><b>Bandingkan nilai per elemen</b><div class="meta">Pilih elemen di form di bawah untuk melihat nilainya di setiap variabel. Baris hijau = versi acuan yang dipilih.</div><div id="cmpbox"></div></div>`;
 h+=rs.map(r=>`<div class="rev"><span class="src">Revisi kontributor</span> <span class="kind">${esc(KIND[r.kind]||r.kind)}</span> · <b>${esc(r.status)}</b>
  <div class="meta">${esc(r.authorName||PROF[r.author]||"Kontributor")}${r.institution?" · "+esc(r.institution):""} · ${esc((r.createdAt||"").slice(0,16).replace("T"," "))} · ${esc(r.target)}${r.element?" · "+esc(r.element):""}${r.acuan?" · acuan: "+esc(r.acuan):""}${r.file?' · berkas '+esc(r.file):""}</div>
  ${r.newItem?`<div><b>${r.kind==="tambahpilihan"?"Pilihan baru":"Elemen baru"}:</b> <code>${esc(Object.entries(r.newItem).filter(([k,v])=>v!==""&&v!==false).map(([k,v])=>k+"="+v).join(" · "))}</code></div>`:""}
  ${r.proposed?`<div><b>Usulan:</b> ${esc(r.proposed)}</div>`:""}${r.reason?`<div><b>Alasan:</b> ${esc(r.reason)}</div>`:""}<div class="meta">terhadap ${esc(r.baseline||"")}</div>
  ${CANEDIT&&!r.src?`<div class="acts">${["terbuka","diterima","ditolak"].filter(s=>s!==r.status).map(s=>`<button type="button" data-setst="${r._id}" data-st="${s}">Tandai ${s}</button>`).join("")}</div>`:""}</div>`).join("");
 const tgts=isG?[[g.id,"Konsep "+g.id],...g.m.map(i=>[i,i+" · "+VB[i].var])]:[[drawerId,drawerId]];
 const mem=isG?g.m:[drawerId];
 const els=[...new Set(mem.flatMap(i=>VB[i].el.map(e=>e[0])))];
 const lists=[...new Set(mem.flatMap(i=>VB[i].el.filter(e=>e[3]).map(e=>e[3]+"|"+e[0])))];
 h+=`<form class="revf" id="revf"><b>Tambah revisi</b>
  <label>Jenis<select id="rf-kind"><option value="resolve">Resolve perbedaan</option><option value="usulan">Usulan revisi nilai</option><option value="tambahpilihan">Tambah pilihan jawaban</option><option value="tambahelemen">Tambah elemen baru</option><option value="catatan">Catatan</option></select></label>
  <label>Target<select id="rf-target">${tgts.map(([v,l])=>`<option value="${v}">${esc(l)}</option>`).join("")}</select></label>
  <label data-k="resolve usulan catatan">Elemen (opsional)<select id="rf-el"><option value="">— seluruh variabel/konsep —</option>${els.map(e=>`<option>${esc(e)}</option>`).join("")}</select></label>
  ${isG?`<label data-k="resolve usulan">Versi acuan<select id="rf-acuan"><option value="">—</option>${g.m.map(i=>`<option value="${i}">${esc(VB[i].t)} · ${esc(VB[i].var)} (${i})</option>`).join("")}<option value="baru">Nilai baru (isi di usulan)</option></select></label>`:""}
  <label data-k="tambahpilihan">Daftar pilihan yang ditambah<select id="rf-list">${lists.map(x=>{const[k,p]=x.split("|");return `<option value="${k}">${esc(k)} · ${esc(p)}</option>`}).join("")}<option value="baru">Daftar baru (sebutkan elemen di Alasan)</option></select></label>
  <div data-k="tambahpilihan" style="display:grid;grid-template-columns:1fr 1fr;gap:6px"><input id="rf-sys" placeholder="system (mis. http://snomed.info/sct)"><input id="rf-code" placeholder="code"><input id="rf-disp" placeholder="display"><input id="rf-ket" placeholder="keterangan / label"></div>
  <div data-k="tambahelemen" style="display:grid;gap:6px"><input id="rf-path" placeholder="path FHIR (mis. Observation.method.coding.code)"><input id="rf-val" placeholder="nilai / terminologi"><input id="rf-eket" placeholder="keterangan"><label style="display:flex;gap:6px;align-items:center;font-weight:400"><input type="checkbox" id="rf-mand"> elemen wajib (*)</label></div>
  <label data-k="resolve usulan catatan">Usulan nilai / keputusan<textarea id="rf-prop" maxlength="2000"></textarea></label>
  <label>Alasan / rujukan<textarea id="rf-reason" maxlength="2000"></textarea></label>
  <label>Institusi<input id="rf-inst" maxlength="120" value="${esc(inst0)}" placeholder="mis. Dinkes Kota X / DTO Kemenkes"></label>
  <details><summary style="cursor:pointer;font-size:12px">Aksi otomatis (opsional — untuk pengelola)</summary>
   <div style="display:grid;gap:6px;margin-top:6px">
    <select id="rf-aksi"><option value="">— tidak ada, catatan/usulan saja —</option><option value="ganti-nilai">ganti-nilai (ubah nilai/kode elemen)</option><option value="pindah-konsep">pindah-konsep (pindahkan variabel ke konsep lain)</option><option value="tandai-status">tandai-status (tetapkan status konsep)</option><option value="tambah-pilihan">tambah-pilihan (system|code|display)</option><option value="tambah-elemen">tambah-elemen</option><option value="jadikan-anak">jadikan-anak (tujuan = ID induk)</option><option value="lepas-anak">lepas-anak</option></select>
    <input id="rf-apath" placeholder="path FHIR (mis. Observation.code.coding)"><input id="rf-aold" placeholder="nilai lama (opsional)"><input id="rf-anew" placeholder="nilai baru / system|code|display"><input id="rf-atuj" placeholder="tujuan (konsep K-xxx, ID variabel, atau status baru)">
    <span class="revmsg">Aksi baru dijalankan halaman setelah pengelola mengubah kolom <code>status</code> menjadi <code>diterima</code> di berkas CSV.</span></div></details>
  <div class="revbtns">${DB?'<button type="submit">Simpan revisi di halaman ini</button>':''}<button type="button" id="rf-csv">Unduh usulan (.csv)</button><button type="button" id="rf-gh">Kirim lewat GitHub Issue</button><button type="button" id="rf-copy">Salin teks usulan</button></div>
  <span class="revmsg">Cara termudah tanpa akun apa pun: klik <b>Unduh usulan (.csv)</b>, lalu kirim berkasnya ke pengelola — pengelola tinggal mengunggahnya ke folder <code>docs/revisi/</code> dan halaman ini langsung menampilkannya. ${DB?'“Simpan revisi di halaman ini” hanya untuk kontributor yang diberi akses tulis di halaman Claude. ':''}Punya akun GitHub gratis? Bisa juga lewat GitHub Issue.</span><span class="revmsg" id="rf-msg"></span></form>`;
 document.getElementById("dbody").innerHTML=h;formKind();cmp();}
function formKind(){const k=(document.getElementById("rf-kind")||{}).value;document.querySelectorAll("#revf [data-k]").forEach(el=>el.hidden=!el.dataset.k.split(" ").includes(k));}
function cmp(){const box=document.getElementById("cmpbox");if(!box)return;const isG=drawerId.startsWith("K-");const mem=isG?GB[drawerId].m:[drawerId];
 const el=(document.getElementById("rf-el")||{}).value;const ac=(document.getElementById("rf-acuan")||{}).value;
 if(!el){box.innerHTML='<div class="meta">Belum ada elemen dipilih.</div>';return;}
 box.innerHTML=`<table class="cmp"><tr><th>Variabel</th><th>Nilai</th><th>Keterangan</th></tr>${mem.map(i=>{const es=VB[i].el.filter(e=>e[0].replace("*","")===el.replace("*",""));
  return `<tr class="${ac===i?"acu":""}"><td>${esc(VB[i].t)} · ${i}</td><td>${es.length?es.map(e=>esc(e[1])+(e[3]?` <span class="id">(${e[3]}: ${D.L[e[3]].rows.map(r=>r[1]).join(", ").slice(0,160)})</span>`:"")).join("<br>"):'<span class="dim">— tidak ada —</span>'}</td><td>${es.map(e=>esc(e[2])).join("<br>")}</td></tr>`}).join("")}</table>`;}
document.addEventListener("change",e=>{if(e.target.id==="rf-kind")formKind();if(e.target.id==="rf-el"||e.target.id==="rf-acuan")cmp();});
function collectRev(){const V_=id=>(document.getElementById(id)||{}).value||"";
 const d={target:V_("rf-target"),element:V_("rf-el"),kind:V_("rf-kind"),acuan:V_("rf-acuan"),proposed:document.getElementById("rf-prop").value.trim(),
  reason:document.getElementById("rf-reason").value.trim(),institution:document.getElementById("rf-inst").value.trim()};
 if(d.kind==="tambahpilihan"){d.newItem={list:V_("rf-list"),system:V_("rf-sys").trim(),code:V_("rf-code").trim(),display:V_("rf-disp").trim(),keterangan:V_("rf-ket").trim()};d.element="";d.proposed="";}
 if(d.kind==="tambahelemen"){d.newItem={path:V_("rf-path").trim(),nilai:V_("rf-val").trim(),keterangan:V_("rf-eket").trim(),wajib:!!(document.getElementById("rf-mand")||{}).checked};d.element="";d.proposed="";}
 return d;}
function revText(d){const isG=d.target.startsWith("K-");const g=isG?GB[d.target]:GB[VB[d.target].g];const mem=isG?g.m:[d.target];
 const nm=isG?`${g.id} · ${g.label}`:`${d.target} · ${VB[d.target].var} (${TN[VB[d.target].t]||VB[d.target].t})`;
 let cur="";
 if(d.element){cur=mem.map(i=>{const es=VB[i].el.filter(e=>e[0].replace("*","")===d.element.replace("*",""));
  return `- ${VB[i].t} (${i}): ${es.length?es.map(e=>e[1]+(e[2]?" — "+e[2]:"")+(e[3]?` [daftar ${e[3]}]`:"")).join(" / "):"— tidak ada —"}`}).join("\n");}
 const item=d.newItem?Object.entries(d.newItem).filter(([k,v])=>v!==""&&v!==false).map(([k,v])=>`${k}: ${v}`).join("; "):"";
 return [`## Usulan revisi\n`,`**Jenis:** ${KIND[d.kind]||d.kind}`,`**Target:** ${nm}`,
  d.element?`**Elemen / path FHIR:** \`${d.element}\``:null,d.acuan?`**Versi acuan:** ${d.acuan}`:null,
  cur?`\n**Kondisi sekarang di dokumentasi:**\n${cur}`:null,
  item?`\n**${d.kind==="tambahpilihan"?"Pilihan baru":"Elemen baru"}:** ${item}`:null,
  d.proposed?`\n**Usulan:**\n${d.proposed}`:null,d.reason?`\n**Alasan / rujukan:**\n${d.reason}`:null,
  d.institution?`\n**Institusi pengusul:** ${d.institution}`:null,
  `\n---`,`Dikirim dari halaman crosscheck · data dasar ${D.SNAP}`].filter(x=>x!==null).join("\n");}
function revValid(d,msg){if(d.kind==="tambahpilihan"&&!(d.newItem&&d.newItem.code)){msg.textContent="Isi minimal kode pilihan baru.";return false;}
 if(d.kind==="tambahelemen"&&!(d.newItem&&d.newItem.path)){msg.textContent="Isi path elemen baru.";return false;}
 if(!d.newItem&&!d.proposed&&!d.reason){msg.textContent="Isi usulan atau alasan terlebih dahulu.";return false;}
 try{localStorage.setItem("ss_inst",d.institution)}catch(_){}
 return true;}
document.addEventListener("click",e=>{const msg=document.getElementById("rf-msg");
 if(e.target.id==="rf-csv"){const d=collectRev();if(!revValid(d,msg))return;
  const q=x=>'"'+String(x==null?"":x).replace(/"/g,'""')+'"';
  const item=d.newItem?Object.entries(d.newItem).filter(([k,v])=>v!==""&&v!==false).map(([k,v])=>k+": "+v).join("; "):"";
  const AV=id=>(document.getElementById(id)||{}).value||"";
  const row=[d.target,d.element,d.kind,[d.proposed,item,d.acuan?"acuan: "+d.acuan:""].filter(Boolean).join(" | "),d.reason,MYNAME(),d.institution,new Date().toISOString().slice(0,10),"terbuka",
   AV("rf-aksi"),AV("rf-apath"),AV("rf-aold"),AV("rf-anew"),AV("rf-atuj")];
  MYROWS.push(row);
  const csv="\uFEFF"+[REVHDR.map(q).join(","),...MYROWS.map(r=>r.map(q).join(","))].join("\r\n");
  const nm="revisi-"+((d.institution||"kontributor").toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"").slice(0,30))+"-"+new Date().toISOString().slice(0,10)+".csv";
  const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"}));a.download=nm;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),4000);
  msg.textContent=MYROWS.length+" usulan dalam berkas "+nm+" — kirim berkas ini ke pengelola.";
  if(window.claude){ // di halaman Claude unduhan diblokir: tampilkan teksnya agar bisa disalin
   msg.textContent=MYROWS.length+" usulan. Unduhan tidak tersedia di halaman Claude — salin teks di bawah, simpan sebagai "+nm+", lalu unggah ke docs/revisi/ di GitHub.";
   let ta=document.getElementById("rf-ta");if(!ta){ta=document.createElement("textarea");ta.id="rf-ta";ta.style.width="100%";ta.style.minHeight="120px";msg.after(ta);}
   ta.value=csv;ta.select();}}
 if(e.target.id==="rf-gh"){const d=collectRev();if(!revValid(d,msg))return;
  const title=`[Usulan] ${d.target}${d.element?" · "+d.element:""} — ${KIND[d.kind]||d.kind}`;
  const url=D.GH+"/issues/new?labels=usulan-revisi&title="+encodeURIComponent(title.slice(0,120))+"&body="+encodeURIComponent(revText(d).slice(0,6000));
  window.open(url,"_blank","noopener");msg.textContent="Tab GitHub dibuka — periksa isinya lalu klik “Create”.";}
 if(e.target.id==="rf-copy"){const d=collectRev();if(!revValid(d,msg))return;
  const t=revText(d);(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>msg.textContent="Teks usulan disalin.",()=>{msg.textContent="Salin manual dari kotak di bawah.";
   const ta=document.createElement("textarea");ta.value=t;ta.style.width="100%";ta.style.minHeight="140px";msg.after(ta);ta.select();});}});
document.addEventListener("submit",async e=>{if(e.target.id!=="revf")return;e.preventDefault();const msg=document.getElementById("rf-msg");
 const doc={target:document.getElementById("rf-target").value,element:document.getElementById("rf-el").value,kind:document.getElementById("rf-kind").value,acuan:(document.getElementById("rf-acuan")||{}).value||"",
  proposed:document.getElementById("rf-prop").value.trim(),reason:document.getElementById("rf-reason").value.trim(),institution:document.getElementById("rf-inst").value.trim(),
  author:ME,createdAt:new Date().toISOString(),status:"terbuka",baseline:D.SNAP,source:"kontributor"};
 const V_=id=>(document.getElementById(id)||{}).value||"";
 if(doc.kind==="tambahpilihan"){doc.newItem={list:V_("rf-list"),system:V_("rf-sys").trim(),code:V_("rf-code").trim(),display:V_("rf-disp").trim(),keterangan:V_("rf-ket").trim()};doc.element="";doc.proposed="";if(!doc.newItem.code){msg.textContent="Isi minimal kode pilihan baru.";return;}}
 if(doc.kind==="tambahelemen"){doc.newItem={path:V_("rf-path").trim(),nilai:V_("rf-val").trim(),keterangan:V_("rf-eket").trim(),wajib:!!(document.getElementById("rf-mand")||{}).checked};doc.element="";doc.proposed="";if(!doc.newItem.path){msg.textContent="Isi path elemen baru.";return;}}
 if(!doc.newItem&&!doc.proposed&&!doc.reason){msg.textContent="Isi usulan atau alasan terlebih dahulu.";return;}
 try{localStorage.setItem("ss_inst",doc.institution)}catch(_){}
 msg.textContent="Menyimpan…";try{await DB.collection("revisions").add(doc);msg.textContent="Tersimpan.";}catch(err){msg.textContent=err&&err.code==="invalid_argument"?"Anda tidak punya akses menulis di halaman ini.":"Gagal menyimpan, coba lagi.";}});
document.addEventListener("click",async e=>{const b=e.target.closest("[data-rev]");if(b){e.stopPropagation();openDrawer(b.dataset.rev);return;}
 if(e.target.closest("#drawer .x")){document.getElementById("drawer").hidden=true;drawerId=null;return;}
 const s=e.target.closest("[data-setst]");if(s&&DB){try{await DB.doc("revisions/"+s.dataset.setst).update({status:s.dataset.st,decidedBy:ME,decidedAt:new Date().toISOString()})}catch(_){}}},true);
(async()=>{const c=window.claude;if(!c||!c.use)return;try{[DB,USER]=await Promise.all([c.use("db"),c.use("user")]);}catch(_){}
 if(USER){try{ME=await USER.id();CANEDIT=await USER.canEdit();}catch(_){}}
 if(!DB)return;
 DB.collection("revisions").orderBy("createdAt","desc").limit(500).onSnapshot(snap=>{REV=snap.docs.map(d=>({_id:d.id,...d.data()}));rebuildRB();applyRevisions();
  const y=window.scrollY;render();window.scrollTo(0,y);renderDrawer();},()=>{});})();
snapshot();render();loadCSVRev();
</script>'''
open("crosscheck.html","w").write(html.replace("__DATA__",D))
import os;print(os.path.getsize("crosscheck.html"))

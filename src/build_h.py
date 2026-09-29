import model as M, model2 as M2, json
V=[dict(id=v["id"],t=v["title"],tahap=v["tahap"],kel=v["kel"],var=v["var"],res=v["res"],el=[list(e) for e in v["elc"]],cat=v["cat"],frek=v["frek"],g=v["gid"],a=1 if v.get("auto") else 0,
        also=[[p,c,o] for (p,c),o in v["also"].items()]) for v in M.ALL]
def pk(E):
    if E["coded"]: body=[[o["s"],o["c"],o["d"],o["k"],o["ids"]] for o in E["opts"].values()]
    else: body=[[x["v"],x["k"],x["ids"]] for x in E["vals"].values()]
    return [E["key"],1 if E["coded"] else 0,1 if E["star"] else 0,E["ids"],body,[[l,i] for l,i in E["lists"].items()]]
G=[dict(id=g["id"],label=g["label"],status=g["status"],note=g["note"],m=[x["id"] for x in g["members"]],rel=g["related"],
        els=[pk(E) for E in g["els"]],ex=[[x["el"],x["kind"],x["parts"]] for x in g["expl"]]) for g in M.G]
DS={k:[1 if d["src"]=="playbook" else 0,d["t"],d["ctx"]] for k,d in M2.DESC.items()}
import markdown
import os
_ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC=markdown.markdown(open(os.path.join(_ROOT,"docs","DOKUMENTASI.md")).read(),extensions=['tables'])
D=json.dumps(dict(DOC=DOC,V=V,G=G,L=M.LISTS,T=[list(t) for t in M.TITLES],S=M.SRC,C=M.CODEVARS,RS=M2.RSOUT,DS=DS,SNAP='SATUSEHAT snapshot 18 Sep 2026',
   STD='Dokumen Lampiran Standar Terminologi SATUSEHAT v10.3 (30 Jun 2026)'),ensure_ascii=False,separators=(",",":"))
html=r'''<title>SATUSEHAT Crosscheck ANC–RJ</title>
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
<footer>Sumber data dasar: <b id="snap"></b>. Revisi yang ditambahkan lewat tombol “Revisi” ditandai sebagai <b>Revisi kontributor</b> (nama & institusi pengusul), terpisah dari data SATUSEHAT. Status: <b>Identik</b> = elemen & nilai sama · <b>Identik (disalin)</b> = tahap yang di playbook merujuk ke modul Rawat Jalan, detailnya disalin dari RJ · <b>Saling melengkapi</b> = hanya ada elemen/pilihan tambahan, tanpa nilai yang bertentangan · <b>Kode sama, isi beda</b> dan <b>Maksud sama, kode/struktur beda</b> = ada konflik nilai; semua label ⓘ dapat diklik untuk melihat penjelasan perbedaan · <b>Unik</b> = hanya di satu variabel. Elemen generik (subject, encounter, performer, author, source, effectiveDateTime) tidak dipakai untuk mencocokkan.</footer>
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
let REV=[];const RB={};function revFor(id){return RB[id]||[]}
function stMatch(g,ss,ids){if(!ss)return true;if(ss==="__rev")return ids.some(i=>revFor(i).length);if(ss==="__open")return ids.some(i=>revFor(i).some(r=>r.status==="terbuka"));return g.status===ss}
const ST={"Saling melengkapi":"st-ok","Unik":"st-uni","Identik":"st-ok","Identik (disalin)":"st-ok","Kode sama, isi beda":"st-warn","Maksud sama, kode/struktur beda":"st-bad","Nama sama, kode beda":"st-bad"};
const EXPL0={"Saling melengkapi":"Perbedaannya hanya berupa elemen atau pilihan tambahan di salah satu use case — tidak ada nilai yang bertentangan, sehingga gabungannya bisa dianggap versi yang lebih lengkap.","Kode sama, isi beda":"Kode konsep utamanya sama, tetapi ada nilai yang bertentangan pada elemen yang sama (mis. unit, category, kode pilihan). Coding tambahan anc-custom-codes tidak dihitung.","Maksud sama, kode/struktur beda":"Konsepnya setara, tetapi kode, category, atau resource yang dipakai berbeda — potensi inkonsistensi dokumentasi."};
const EXPL=Object.assign({},EXPL0,{"Identik":"Semua elemen & nilai sama.","Identik (disalin)":"Detail disalin dari modul Rawat Jalan karena playbook merujuk ke sana."});
document.getElementById("src").innerHTML=D.T.map(([k,n])=>`<li><b>${esc(n)}</b> — ${esc(D.S[k]||"")}</li>`).join("");
const tsel=document.getElementById("tsel"),vsel=document.getElementById("vsel"),ssel=document.getElementById("ssel"),q=document.getElementById("q");
tsel.innerHTML=D.T.map(([k,n])=>`<option value="${k}">${esc(k)} — ${esc(n)} (${D.V.filter(v=>v.t===k).length})</option>`).join("")+`<option value="K">Konsolidasi — semua use case (${D.G.length} konsep)</option><option value="R">Ringkasan Resource (${Object.keys(D.RS).length} resource)</option><option value="DOC">Dokumentasi & progres pekerjaan</option>`;
ssel.innerHTML='<option value="">Semua status</option>'+[...new Set(D.G.map(g=>g.status))].map(s=>`<option>${esc(s)}</option>`).join("")+'<option value="__rev">Ada revisi kontributor</option><option value="__open">Revisi masih terbuka</option>';
document.getElementById("snap").textContent=D.SNAP;
let view=D.T[0][0], focus=null, rsel=null; const open=new Set();
function qre(){const qq=q.value.trim();return qq.length<2?null:new RegExp(qq.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"),"gi")}
function mark(root){const re=qre();if(!re||!root)return;const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:n=>{if(!n.data.trim()||n.parentNode.closest("script,style,mark,select,option,textarea"))return 2;re.lastIndex=0;return re.test(n.data)?1:2}});
 const ns=[];while(w.nextNode()&&ns.length<5000)ns.push(w.currentNode);
 ns.forEach(n=>{const f=document.createDocumentFragment();let last=0;re.lastIndex=0;n.data.replace(re,(m,i)=>{f.append(n.data.slice(last,i));const k=document.createElement("mark");k.textContent=m;f.append(k);last=i+m.length;return m});f.append(n.data.slice(last));n.replaceWith(f);});}
function who(ids,all){if(all&&ids.length===all)return '<span class="dim">semua</span>';const by={};ids.forEach(i=>{const t=VB[i].t;(by[t]=by[t]||[]).push(i)});
 return Object.entries(by).map(([t,is])=>`<a class="lk" href="#${is[0]}" data-go="${t}" data-id="${is[0]}" title="${esc(is.map(i=>i+" "+VB[i].var).join("\n"))}">${esc(t)}${is.length>1?` ×${is.length}`:""}</a>`).join(", ")}
const cut=(t,n)=>t.length>n?t.slice(0,n)+"…":t;
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
 vsel.innerHTML=view==="K"?'<option value="">Semua konsep</option>'+D.G.map(g=>`<option value="${g.id}">${g.id} · ${esc(g.label)}</option>`).join(""):'<option value="">Semua variabel</option>'+D.V.filter(v=>v.t===view).map(v=>`<option value="${v.id}">${v.id} · ${esc(v.var)}</option>`).join("");
 vsel.value=[...vsel.options].some(o=>o.value===cur)?cur:"";}
function stats(){const pool=view==="K"?D.G:D.V.filter(v=>v.t===view).map(v=>GB[v.g]);const c={};pool.forEach(g=>c[g.status]=(c[g.status]||0)+1);
 document.getElementById("stats").innerHTML=Object.entries(c).map(([s,n])=>`<button type="button" data-s="${esc(s)}" aria-pressed="${ssel.value===s}"><span class="st ${ST[s]}">${esc(s)}</span> ${n}</button>`).join("");}
function elRows(v){
 const alsoMap={};v.also.forEach(([p,c,o])=>alsoMap[p+"|"+c]=o);const rows=[];
 v.el.forEach((e,j)=>{const np=e[0].replace(/\*/g,"").replace(/\[(i|\d)\]/g,"").replace(/ /g,"");const rep=j>0&&v.el[j-1][0]===e[0];
  const al=alsoMap[np+"|"+e[1]]||[];
  rows.push(`<td class="path${rep?" rep":""}${e[0].startsWith("*")?" mand":""}" data-l="Elemen">${esc(e[0])}</td><td class="val" data-l="Nilai">${esc(e[1])}</td><td class="ket" data-l="Keterangan">${esc(e[2])}</td><td class="also" data-l="Kode juga di">${limited(al,vlink,3)}</td>`);
  if(e[3]) rows.push(`<td colspan="4" class="inl">${listTable(e[3],v.id)}</td>`);});
 return rows;}
function renderTitle(){
 const qq=q.value.toLowerCase().trim(),sv=vsel.value,ss=ssel.value;
 let h='<div class="tbl"><table class="main"><colgroup><col style="width:22%"><col style="width:27%"><col style="width:21%"><col style="width:17%"><col style="width:13%"></colgroup><thead><tr><th>Variabel & muncul di</th><th>Elemen / path FHIR</th><th>Nilai</th><th>Keterangan</th><th>Kode juga dipakai di</th></tr></thead><tbody>';
 let n=0,prev=null;
 D.V.filter(v=>v.t===view).forEach(v=>{const g=GB[v.g];
  if(sv&&v.id!==sv)return;if(!stMatch(g,ss,[v.id,g.id]))return;if(qq&&!v._s.includes(qq))return;
  if(v.tahap!==prev){h+=`<tr class="step"><td colspan="5">${esc(v.tahap)}</td></tr>`;prev=v.tahap}
  n++;const others=g.m.filter(x=>x!==v.id);
  let mu=`<div class="muncul"><b>Konsolidasi</b>${glink(g.id)}`;
  if(others.length)mu+=`<b>Juga muncul di</b>`+limited(others,vlink);
  if(g.rel.length)mu+=`<b>Terkait</b>`+limited(g.rel.map(r=>r[0]),glink,4);
  mu+="</div>";
  const rows=elRows(v);
  rows.forEach((c,j)=>{h+=`<tr class="${j?"sub":"first"}">`+(j?"":`<td class="var" rowspan="${rows.length}" id="${v.id}" data-l="Variabel"><span class="id">${v.id}</span><span class="kel">${esc(v.kel)}</span><span class="nm">${esc(v.var)} ${descBtn(v.id)}</span><span class="pill">${esc(v.res)}</span>${v.a?'<span class="pill" style="background:var(--warn-bg);color:var(--warn)" title="Diekstraksi otomatis dari halaman/PDF SATUSEHAT, belum dicek manual">otomatis</span>':""}${badge(g)}${revBtn(v.id)}${v.frek?`<span class="freq">${esc(v.frek)}</span>`:""}${mu}${v.cat?`<span class="note">${esc(v.cat)}</span>`:""}</td>`)+c+"</tr>"});
 });
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
  h+=`<div class="krow${isO?" open":""}" id="${g.id}"><div class="khead" data-k="${g.id}" role="button" tabindex="0" aria-expanded="${isO}"><span class="car">▶</span><span class="id">${g.id}</span><span class="lb">${esc(g.label)}</span><span>${badge(g)}${revBtn(g.id,true)}</span><span class="tt">${titles.map(t=>`<span class="pill">${esc(t)}</span>`).join("")}</span><span class="n">${g.m.length} var</span></div>${isO?`<div class="kbody">${kbody(g)}</div>`:""}</div>`;});
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
 h=`<button type="button" class="back" data-rs="">← Semua resource</button><h2 style="font:600 20px var(--disp);margin:10px 0 2px">Ringkasan elemen ${esc(rsel)}</h2><p class="dim" style="font-size:12.5px;margin:0 0 8px">${R.nv} variabel dari ${R.titles.length} use case memakai ${esc(rsel)}. ${LVL}. Elemen bertipe pilihan ([x], mis. value[x]) dihitung sekali — cukup salah satu tipe datanya yang diisi.</p>`;
 const mc=R.els.filter(e=>e.pct>=0.4).slice(0,14);
 if(mc.length)h+=`<div class="sec"><h3>Kelengkapan per use case</h3><p class="dim" style="font-size:12px;margin:0 0 6px">Persentase variabel ${esc(rsel)} di tiap use case yang memuat elemen inti/umum. Sel kosong = elemen tidak pernah dipakai di use case itu.</p><div class="tbl"><table class="mx"><thead><tr><th>Use case (variabel)</th>${mc.map(e=>`<th>${esc(e.el)}</th>`).join("")}</tr></thead><tbody>${R.titles.map(t=>`<tr><td>${esc(t)} (${R.tv[t]})</td>${mc.map(e=>{const x=(e.cov[t]||0)/R.tv[t];return `<td style="background:color-mix(in srgb,var(--ok-bg) ${Math.round(x*100)}%,transparent)">${x?pct(x):""}</td>`}).join("")}</tr>`).join("")}</tbody></table></div></div>`;
 h+=`<div class="sec"><h3>Elemen yang dipakai (${R.els.length})</h3>`+R.els.map((e,i)=>{const op=qq&&JSON.stringify(e).toLowerCase().includes(qq);
  return `<details class="rel" data-ri="${i}"${op?" open":""}><summary><code>${esc(e.el)}</code><span class="tag ${e.lvl}">${e.lvl}</span><span class="bar"><i style="width:${pct(e.pct)}"></i></span><span>${e.n}/${R.nv} variabel (${pct(e.pct)})</span><span class="dim">${e.titles.length}/${R.titles.length} use case</span>${e.star.length?`<span class="dim">wajib di ${e.star.length} use case</span>`:""}${!e.canon&&R.canon?'<span class="tag sebagian" title="Tidak ada di daftar elemen baku FHIR R4 untuk resource ini — bisa extension, salah ketik di playbook, atau salah baca saat ekstraksi otomatis">bukan elemen baku — cek</span>':""}${Object.keys(e.choices||{}).length?`<span class="dim">tipe: ${Object.keys(e.choices).map(esc).join(" | ")}</span>`:""}</summary><div class="rb">${op?relBody(e,R):""}</div></details>`}).join("")+"</div>";
 if(R.unused.length)h+=`<div class="sec"><h3>Elemen baku FHIR yang belum pernah dipakai (${R.unused.length})</h3><div class="chips">${R.unused.map(u=>`<span class="pill">${esc(u)}</span>`).join("")}</div></div>`;
 if(R.stdonly.length)h+=`<div class="sec"><h3>Hanya ada di Lampiran Standar Terminologi (${R.stdonly.length} path)</h3><p class="dim" style="font-size:12px;margin:0 0 6px">Path ${esc(rsel)} yang punya ketentuan terminologi di ${esc(D.STD)} tetapi tidak muncul di playbook mana pun.</p>`+R.stdonly.map(x=>`<details class="rel"><summary><code>${esc(x.path)}</code><span class="tag std">Lampiran Std. Terminologi</span><span class="dim">${esc(x.sec)} · ${x.rows.length} kode</span></summary><div class="rb">${x.note?`<div class="ev dim">${esc(cut(x.note,500))}</div>`:""}${x.rows.length?`<div class="inlist"><table><thead><tr><th>system</th><th>code</th><th>display</th><th>keterangan</th></tr></thead><tbody>${x.rows.map(r=>`<tr><td class="c">${esc(r[0])}</td><td class="c">${esc(r[1])}</td><td>${esc(r[2])}</td><td>${esc(r[3])}</td></tr>`).join("")}</tbody></table></div>`:""}</div></details>`).join("")+"</div>";
 if(R.miss.length)h+=`<div class="sec"><h3>Variabel tanpa elemen inti (${R.miss.length})</h3><p class="dim" style="font-size:12px;margin:0 0 6px">Variabel ${esc(rsel)} yang tidak memuat elemen yang biasanya ada (Inti). Bisa berarti playbook memang tidak merinci, atau ada yang terlewat.</p><details class="rel"><summary>Tampilkan daftar</summary><div class="rb">${R.miss.map(([i,m])=>`<div class="ev">${vlink(i).replace('lkl"','lkl" style="display:inline"')} — tidak ada: ${m.map(x=>`<code>${esc(x)}</code>`).join(", ")}</div>`).join("")}</div></details></div>`;
 out.innerHTML=h;document.getElementById("count").textContent=R.els.length+" elemen";mark(out);}
document.addEventListener("toggle",e=>{const d=e.target;if(!(d.matches&&d.matches("details.rel[data-ri]"))||!d.open)return;const b=d.querySelector(".rb");if(b.innerHTML)return;const R=D.RS[rsel];b.innerHTML=relBody(R.els[+d.dataset.ri],R);mark(b);},true);
function render(){if(view==="DOC"){vsel.hidden=ssel.hidden=true;document.getElementById("stats").hidden=true;document.getElementById("openall").hidden=document.getElementById("closeall").hidden=true;tsel.value=view;const o=document.getElementById("out");o.innerHTML=`<article class="doc">${D.DOC}</article>`;document.getElementById("count").textContent="";mark(o);return;}
 const r=view==="R";vsel.hidden=r;ssel.hidden=r;document.getElementById("stats").hidden=r;if(!r){fillVsel();stats();}const k=view==="K";document.getElementById("openall").hidden=!k;document.getElementById("closeall").hidden=!k;
 r?renderR():(k?renderK():renderTitle());tsel.value=view;if(!r)mark(document.getElementById("out"));
 if(focus){const el=document.getElementById(focus);if(el){el.scrollIntoView({block:"start"});window.scrollBy(0,-70);(el.closest("tr")||el).classList.add("hl");}focus=null;}}
function go(v,id){if(v!==view){view=v;rsel=null;vsel.value="";ssel.value="";q.value="";}if(id&&v==="K")open.add(id);focus=id;if(id&&!document.getElementById(id)){vsel.value="";ssel.value="";q.value="";}render();}
function showPop(gid,anchor){const g=GB[gid],p=document.getElementById("pop");
 p.innerHTML=`<button class="x" type="button" aria-label="Tutup">×</button><h3>${esc(g.id)} · ${esc(g.label)}</h3><span class="st ${ST[g.status]}">${esc(g.status)}</span> <span class="dim" style="font-size:12px">${g.m.length} variabel: ${who(g.m)}</span><p style="font-size:12.5px;margin:6px 0">${esc(EXPL[g.status]||"")}</p>${g.note?`<p style="font-size:12.5px;margin:6px 0"><b>Catatan:</b> ${esc(g.note)}</p>`:""}${exHTML(g)}`;
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
async function names(ids){if(!USER)return;const need=ids.filter(i=>i&&!(i in PROF));if(!need.length)return;try{const ps=await USER.profiles(need);for(const i of need)PROF[i]=(ps[i]&&ps[i].name)||""}catch(e){}}
function openDrawer(id){drawerId=id;document.getElementById("drawer").hidden=false;renderDrawer();}
async function renderDrawer(){if(!drawerId)return;const isG=drawerId.startsWith("K-");const g=isG?GB[drawerId]:GB[VB[drawerId].g];
 const ids=isG?[drawerId,...g.m]:[drawerId];const rs=ids.flatMap(revFor).sort((a,b)=>(b.createdAt||"").localeCompare(a.createdAt||""));
 await names(rs.map(r=>r.author));
 document.getElementById("dtitle").textContent=isG?`${g.id} · ${g.label}`:`${drawerId} · ${VB[drawerId].var}`;
 document.getElementById("dsub").innerHTML=`${esc(g.status)} · data dasar: ${esc(D.SNAP)}`;
 let h=`<div class="rev"><span class="src base">SATUSEHAT</span> <b>${esc(g.status)}</b><div class="meta">Data dasar dari dokumen resmi (${esc(D.SNAP)})</div>${g.note?`<div>${esc(g.note)}</div>`:""}${g.ex.length?`<div style="margin-top:6px"><b>Yang perlu dicek / direvisi:</b></div>${exHTML(g)}`:'<div class="meta">Tidak ada perbedaan otomatis.</div>'}</div>`;
 h+=`<div class="rev"><b>Bandingkan nilai per elemen</b><div class="meta">Pilih elemen di form di bawah untuk melihat nilainya di setiap variabel. Baris hijau = versi acuan yang dipilih.</div><div id="cmpbox"></div></div>`;
 h+=rs.map(r=>`<div class="rev"><span class="src">Revisi kontributor</span> <span class="kind">${esc(KIND[r.kind]||r.kind)}</span> · <b>${esc(r.status)}</b>
  <div class="meta">${esc(PROF[r.author]||"Kontributor")}${r.institution?" · "+esc(r.institution):""} · ${esc((r.createdAt||"").slice(0,16).replace("T"," "))} · ${esc(r.target)}${r.element?" · "+esc(r.element):""}${r.acuan?" · acuan: "+esc(r.acuan):""}</div>
  ${r.newItem?`<div><b>${r.kind==="tambahpilihan"?"Pilihan baru":"Elemen baru"}:</b> <code>${esc(Object.entries(r.newItem).filter(([k,v])=>v!==""&&v!==false).map(([k,v])=>k+"="+v).join(" · "))}</code></div>`:""}
  ${r.proposed?`<div><b>Usulan:</b> ${esc(r.proposed)}</div>`:""}${r.reason?`<div><b>Alasan:</b> ${esc(r.reason)}</div>`:""}<div class="meta">terhadap ${esc(r.baseline||"")}</div>
  ${CANEDIT?`<div class="acts">${["terbuka","diterima","ditolak"].filter(s=>s!==r.status).map(s=>`<button type="button" data-setst="${r._id}" data-st="${s}">Tandai ${s}</button>`).join("")}</div>`:""}</div>`).join("");
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
  ${DB?'<button type="submit">Simpan revisi</button>':'<span class="revmsg">Penyimpanan revisi aktif saat halaman dibuka di claude.ai.</span>'}<span class="revmsg" id="rf-msg"></span></form>`;
 document.getElementById("dbody").innerHTML=h;formKind();cmp();}
function formKind(){const k=(document.getElementById("rf-kind")||{}).value;document.querySelectorAll("#revf [data-k]").forEach(el=>el.hidden=!el.dataset.k.split(" ").includes(k));}
function cmp(){const box=document.getElementById("cmpbox");if(!box)return;const isG=drawerId.startsWith("K-");const mem=isG?GB[drawerId].m:[drawerId];
 const el=(document.getElementById("rf-el")||{}).value;const ac=(document.getElementById("rf-acuan")||{}).value;
 if(!el){box.innerHTML='<div class="meta">Belum ada elemen dipilih.</div>';return;}
 box.innerHTML=`<table class="cmp"><tr><th>Variabel</th><th>Nilai</th><th>Keterangan</th></tr>${mem.map(i=>{const es=VB[i].el.filter(e=>e[0].replace("*","")===el.replace("*",""));
  return `<tr class="${ac===i?"acu":""}"><td>${esc(VB[i].t)} · ${i}</td><td>${es.length?es.map(e=>esc(e[1])+(e[3]?` <span class="id">(${e[3]}: ${D.L[e[3]].rows.map(r=>r[1]).join(", ").slice(0,160)})</span>`:"")).join("<br>"):'<span class="dim">— tidak ada —</span>'}</td><td>${es.map(e=>esc(e[2])).join("<br>")}</td></tr>`}).join("")}</table>`;}
document.addEventListener("change",e=>{if(e.target.id==="rf-kind")formKind();if(e.target.id==="rf-el"||e.target.id==="rf-acuan")cmp();});
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
 DB.collection("revisions").orderBy("createdAt","desc").limit(500).onSnapshot(snap=>{REV=snap.docs.map(d=>({_id:d.id,...d.data()}));for(const k in RB)delete RB[k];REV.forEach(r=>{(RB[r.target]=RB[r.target]||[]).push(r)});
  const y=window.scrollY;render();window.scrollTo(0,y);renderDrawer();},()=>{});})();
render();
</script>'''
open(os.path.join(_ROOT,"docs","index.html"),"w").write(html.replace("__DATA__",D))
import os;print(os.path.getsize("crosscheck.html"))

# Export dataset terstruktur (JSON) — mencerminkan data yang dipakai halaman crosscheck
import sys, json, datetime
import os
_ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_D=lambda f: os.path.join(_ROOT,"data",f)
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import model as M, model2 as M2, hier as HI

STAMP=datetime.date.today().isoformat()
SNAP='SATUSEHAT snapshot 18 Sep 2026; MCU & TTE 7 Okt 2026'

def el(v): return [list(e) for e in v["elc"]]
VARS=[]
for v in M.ALL:
    d=M2.DESC.get(v["id"])
    VARS.append(dict(id=v["id"],use_case=v["title"],tahap=v["tahap"],kelompok=v["kel"],variabel=v["var"],
        resource=v["res"],elemen=el(v),
        pelengkap=[dict(key=x["key"],coded=x["coded"],star=x["star"],body=x["body"],lists=x["lists"],src=x["src"]) for x in v.get("sup",[])],
        catatan=v["cat"],frekuensi=v["frek"],otomatis=bool(v.get("auto")),konsep=v.get("gid"),
        induk=v.get("ind"),peran=v.get("per"),anak=v.get("anak",[]),kelompok_sintetis=bool(v.get("syn")),
        deskripsi=(dict(src=d["src"],t=d["t"],ctx=d["ctx"]) if d else {})))

KON=[dict(id=g["id"],label=g["label"],status=g["status"],catatan=g["note"],
          variabel=[x["id"] for x in g["members"]],
          perbedaan=[dict(el=x["el"],kind=x["kind"],parts=x["parts"],star=x.get("star",False)) for x in g["expl"]]) for g in M.G]

RUJ=[dict(title=r["title"],tahap=r["tahap"],code=r["code"],judul=r["judul"],url=r["url"],isi=r.get("isi",""),
          targets=r["targets"],note=r["note"],kutipan=r.get("kutipan","")) for r in M.REFS]

HIER=dict(statistik=HI.STAT,
          konsep_induk=[dict(id=h["id"],label=h["label"],induk=h["m"],use_case=h["titles"],
             sub=[dict(label=r["label"],konsep=r["gid"],per_use_case=r["by"]) for r in h["rows"]]) for h in HI.H])

OUT=dict(snapshot=STAMP,sumber_data=SNAP,titles=[list(t) for t in M.TITLES],sources=M.SRC,
         rujukan=RUJ,hierarki=HIER,variables=VARS,konsep=KON,daftar=M.LISTS,ringkasan_resource=M2.RSOUT)
p=_D(f'satusehat_structured_all_{STAMP.replace("-","")}.json')
json.dump(OUT,open(p,'w'),ensure_ascii=False)
print(p)
print({k:(len(v) if hasattr(v,"__len__") else v) for k,v in OUT.items() if k not in ("sources",)})

# Hierarki induk-anak variabel: item kuesioner, komponen, section Composition, kelompok playbook
import re, copy
import model as M
from model import ALL, BYID, npath

def _vals(v, suf):
    return [e[1] for e in v["el"] if npath(e[0].lstrip("*")).endswith(suf)]
LID=re.compile(r"^\d+(\.\d+)*$")
NUM=re.compile(r"^\((\d+)\)")
TOT=re.compile(r"total|jumlah skor|skor total|total skor", re.I)

for v in ALL: v["ind"]=None; v["per"]=None
SYN=[]        # node sintetis (kelompok)
GENERIC=re.compile(r"^(pemetaan variabel( dan terminologi spesifik)?|pemetaan nilai|terminologi spesifik|penting|catatan)\b",re.I)
def clean_kel(kel, ref):
    k=re.sub(r"^\s*\d+[.)]\s*","",str(kel or "").strip())
    k=re.sub(r"^Pemetaan Variabel( dan Terminologi Spesifik)?\s*","",k,flags=re.I).strip()
    k=re.sub(r"^(Data|Pengiriman Data)\s+","",k).strip()
    return k or re.sub(r"^\d+\.\s*","",ref["tahap"])
def syn_node(title, kel, ref):
    i=len([x for x in SYN if x["title"]==title])+1
    n=dict(id=f"{title}-K{i:02d}", title=title, tahap=ref["tahap"], kel="", var=clean_kel(kel,ref), res="", el=[], cat="", frek="",
           syn=True, ind=None, per="kelompok", auto=ref.get("auto"), gid=None, elc=[], also={}, sup=[])
    SYN.append(n); return n

# ---- 1. item kuesioner (QuestionnaireResponse.item.linkId) ----
QK={}
for v in ALL:
    if "QuestionnaireResponse" not in v["res"]: continue
    ids=[str(x).strip() for x in _vals(v,".linkId") if LID.match(str(x).strip())]
    if not ids: continue
    v["_lid"]=min(ids, key=lambda s:(len(s.split(".")), s))
    q=_vals(v,".questionnaire")
    key=(v["title"], re.sub(r"\s+","",str(q[0])) if q else "tahap:"+v["tahap"])
    QK.setdefault(key,{}).setdefault(v["_lid"], v["id"])
for v in ALL:
    if "_lid" not in v: continue
    q=_vals(v,".questionnaire")
    key=(v["title"], re.sub(r"\s+","",str(q[0])) if q else "tahap:"+v["tahap"])
    parts=v["_lid"].split(".")
    for k in range(len(parts)-1,0,-1):
        pid=QK[key].get(".".join(parts[:k]))
        if pid and pid!=v["id"]:
            v["ind"]=pid; v["per"]="item"; break

# ---- 2. section Composition ----
for t,_ in M.TITLES:
    doc=None
    for v in [x for x in ALL if x["title"]==t]:
        if "Composition" not in v["res"]: continue
        has_sec=any(".section" in npath(e[0]) for e in v["el"])
        has_type=any(npath(e[0]).startswith("Composition.type") for e in v["el"])
        if has_type and not has_sec: doc=v; continue
        if has_sec and doc and not v["ind"]:
            v["ind"]=doc["id"]; v["per"]="section"

# ---- 3. komponen bernomor "(n)" dalam satu kelompok ----
BYKEL={}
for v in ALL: BYKEL.setdefault((v["title"],v["kel"]),[]).append(v)
for (t,kel),vs in BYKEL.items():
    num=[v for v in vs if NUM.match(v["var"].strip())]
    if len(num)<2: continue
    tot=[v for v in vs if TOT.search(v["var"])]
    par=tot[0] if tot else None
    for v in num:
        if v["ind"] or (par and v["id"]==par["id"]): continue
        if par: v["ind"]=par["id"]; v["per"]="komponen"

# ---- 4. kelompok playbook sebagai induk sintetis ----
for (t,kel),vs in sorted(BYKEL.items(), key=lambda kv:(kv[0][0], min(ALL.index(x) for x in kv[1]))):
    if not kel or len(vs)<3: continue
    roots=[v for v in vs if not v["ind"]]
    if len(roots)<2: continue
    n=syn_node(t, kel, roots[0])
    for v in roots: v["ind"]=n["id"]; v["per"]=v["per"] or "kelompok"
ALL.extend(SYN)
BYID.update({n["id"]:n for n in SYN})

# ---- turunan: anak, kedalaman, urutan tampil ----
for v in ALL: v["anak"]=[]
for v in ALL:
    if v.get("ind") and v["ind"] in BYID and BYID[v["ind"]] is not v: BYID[v["ind"]]["anak"].append(v["id"])
def depth(v, seen=None):
    d=0; seen=set(); x=v
    while x.get("ind") and x["ind"] in BYID and x["ind"] not in seen and d<8:
        seen.add(x["ind"]); x=BYID[x["ind"]]; d+=1
    return d
for v in ALL: v["lvl"]=depth(v)
def root_of(v):
    seen=set(); x=v
    while x.get("ind") and x["ind"] in BYID and x["ind"] not in seen:
        seen.add(x["ind"]); x=BYID[x["ind"]]
    return x
ROOT={v["id"]:root_of(v)["id"] for v in ALL}

# ---- konsep induk (H): induk yang berpadanan antar playbook ----
def nlabel(s): return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9 ]"," ",str(s).lower())).strip()
PAR=[v for v in ALL if v["anak"]]
H=[]; byname={}
for v in PAR: byname.setdefault(nlabel(v["var"]),[]).append(v)
for name,vs in sorted(byname.items(), key=lambda kv: -len(kv[1])):
    if len({v["title"] for v in vs})<2: continue
    if GENERIC.match(vs[0]["var"] or ""): continue
    H.append(dict(id="", label=vs[0]["var"], m=[v["id"] for v in vs], titles=sorted({v["title"] for v in vs})))
H=[h for h in H if len(h["m"])>0]
H.sort(key=lambda h:(-len(h["titles"]), h["label"].lower()))
for i,h in enumerate(H,1): h["id"]=f"H-{i:03d}"
# matriks anak x use case: anak dikelompokkan lewat konsep (gid) atau nama
for h in H:
    rows={}; order=[]
    for pid in h["m"]:
        p=BYID[pid]
        for cid in p["anak"]:
            c=BYID[cid]
            key=c.get("gid") or ("n:"+nlabel(c["var"]))
            if key not in rows: rows[key]=dict(key=key, label=c["var"], gid=c.get("gid"), by={}); order.append(key)
            rows[key]["by"].setdefault(p["title"],[]).append(cid)
    h["rows"]=[rows[k] for k in order]
    h["nchild"]=sum(len(BYID[p]["anak"]) for p in h["m"])
STAT=dict(parents=len(PAR), syn=len(SYN),
          child=sum(1 for v in ALL if v.get("ind")),
          per={k:sum(1 for v in ALL if v.get("per")==k) for k in ("item","komponen","section","kelompok")},
          H=len(H), Hmulti=sum(1 for h in H if len(h["titles"])>1))
if __name__=="__main__":
    print(STAT)
    for h in H[:6]: print(h["id"],h["label"],h["titles"],"anak:",h["nchild"],"baris:",len(h["rows"]))

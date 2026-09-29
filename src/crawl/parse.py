import json, re, os
_ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_D=lambda f: os.path.join(_ROOT,"data",f)
RAW=json.load(open(_D('satusehat_playbook_raw_20260918.json')))
PDFJ=json.load(open(_D('satusehat_playbook_pdf_20260918.json')))['modules']
SHORT={"igd":"IGD","rawat-inap-new":"RANAP","kefarmasian":"FARMASI","data-kelahiran":"KELAHIRAN","inc":"INC","pnc":"PNC","rawat-jalan-gigi":"GIGI","gizi":"GIZI",
 "imunisasi-new":"IMUN","imunisasi-covid":"IMUNCOVID","mpdn":"MPDN","mtbs-prio":"MTBS","neonatus":"NEONATUS","pkpr-luar-gedung":"PKPR","klaim":"KLAIM","registrasi-jantung":"JANTUNG",
 "kanker":"KANKER","mata":"MATA","stroke":"STROKE","uronefro":"URONEFRO","rujukan-spesimen":"RUJSPES","shk":"SHK","skrining-ptm":"PTM","tuberkulosis":"TB","tumbuh-kembang-new":"TUMBANG","ubm":"UBM","zoonosis-rabies":"RABIES"}
LAMPMAP={"rawat-inap-new":"rawat-inap-fase-2","neonatus":"neonatus-prio","stroke":"registrasi-stroke"}
PATH=re.compile(r"^\*?(Patient|Encounter|Observation|Condition|Procedure|ServiceRequest|Specimen|DiagnosticReport|MedicationRequest|MedicationDispense|MedicationStatement|MedicationAdministration|Medication|Immunization|ImmunizationRecommendation|QuestionnaireResponse|EpisodeOfCare|CarePlan|Composition|ClinicalImpression|AllergyIntolerance|FamilyMemberHistory|RiskAssessment|Goal|NutritionOrder|ImagingStudy|Substance|Location|Organization|Practitioner|RelatedPerson|Coverage|Claim|ClaimResponse|Account|ChargeItem|Invoice|DocumentReference|Consent|Device|Appointment|Task|ServiceRequest|CareTeam|Questionnaire|Group|Flag|DetectedIssue|AdverseEvent|Media|Binary|Bundle|PractitionerRole|HealthcareService|EpisodeofCare|RiskAssesment|Specimen)\s*\.",re.I)
def clean(c): return re.sub(r"\{(cs|rs)\d+\}","",c or "").strip()
def fixpath(c):
    c=clean(c)
    return re.sub(r"\s+","",c) if PATH.match(c.replace(" ","")) else c
def is_path(c): return bool(PATH.match(c.replace(" ",""))) and len(c)<200
LBL=re.compile(r"^(pilihan jawaban|keterangan)",re.I)
def stripnum(s): return re.sub(r"^\s*(\d+(\.\d+)*\.?|[a-z]\.|[a-z]\))\s+","",s).strip()
SKIPH=re.compile(r"^(Pemetaan Variabel|Elemen/Path|Elemen / Path|Resource |Pemetaan variabel|Nama Variabel:)",re.I)

class Builder:
    def __init__(s,code):
        s.code=code; s.V=[]; s.cur=None; s.tahap=""; s.kel=""; s.pendhdr=None
    def new_var(s,name,kel=None):
        s.cur=dict(tahap=s.tahap or "—",kel=kel if kel is not None else s.kel,var=name[:140],res="",el=[],cat="",frek="",auto=True,_multi=[])
        s.V.append(s.cur)
    def ensure(s):
        if s.cur is None: s.new_var(s.kel or s.tahap or "Variabel")
    def add(s,path,vals,cs_single=False):
        s.ensure()
        vals=[v for v in vals if v!=""]
        if not vals: vals=[""]
        s.cur["_multi"].append([fixpath(path),vals,[]])
    def labels(s,vals):
        if s.cur and s.cur["_multi"]:
            # attach to trailing rows that have same count of values
            n=len([v for v in vals if v])
            for row in reversed(s.cur["_multi"]):
                if len(row[1])==n and n>1: row[2]=[v for v in vals if v]; return
            if n==1: s.cur["cat"]=(s.cur["cat"]+" " if s.cur["cat"] else "")+vals[0][:300]
    def finalize(s):
        for v in s.V:
            el=[]; M=v.pop("_multi")
            i=0
            # expand multi-valued coding triples into interleaved option rows
            while i<len(M):
                p,vals,lab=M[i]
                base=p.lstrip("*").rsplit(".",1)[0] if re.search(r"\.(system|code|display)$",p) else None
                if base and len(vals)>1 or (base and i+1<len(M) and len(M[i+1][1])>1 and M[i+1][0].lstrip("*").rsplit(".",1)[0]==base):
                    grp=[]; j=i
                    while j<len(M) and re.search(r"\.(system|code|display)$",M[j][0]) and M[j][0].lstrip("*").rsplit(".",1)[0]==base: grp.append(M[j]); j+=1
                    k=max(len(g[1]) for g in grp); labs=next((g[2] for g in grp if g[2]),[])
                    sysr=[g for g in grp if g[0].endswith(".system")]; cod=[g for g in grp if g[0].endswith(".code")]; dis=[g for g in grp if g[0].endswith(".display")]
                    for o in range(k):
                        if sysr: sv=sysr[0][1][o] if len(sysr[0][1])==k else sysr[0][1][0]; el.append((sysr[0][0],sv,""))
                        if cod: el.append((cod[0][0],cod[0][1][o] if o<len(cod[0][1]) else cod[0][1][-1],labs[o] if o<len(labs) else ""))
                        if dis: el.append((dis[0][0],dis[0][1][o] if o<len(dis[0][1]) else dis[0][1][-1],""))
                    i=j; continue
                if len(vals)>1:
                    for o,val in enumerate(vals): el.append((p,val,lab[o] if o<len(lab) else ""))
                else:
                    el.append((p,vals[0],lab[0] if lab else ""))
                i+=1
            v["el"]=el
            roots=[]
            for e in el:
                r=e[0].lstrip("*").split(".")[0]
                if r not in roots: roots.append(r)
            v["res"]=" + ".join(roots[:4])
        s.V=[v for v in s.V if v["el"]]
    def table(s,rows):
        if not rows: return
        flat=[[fixpath(c) for c in r] for r in rows]
        hdr=flat[0]
        if any(re.search(r"^variabel$",c,re.I) for c in hdr) and any("Resource" in c for c in hdr): return  # overview table
        # column-oriented option table: header cells are paths
        pcols=[i for i,c in enumerate(hdr) if is_path(c)]
        if len(pcols)>=2 and len(hdr)>=3:
            s.ensure()
            for r in flat[1:]:
                vals=[c for c in r]
                if not any(vals): continue
                ket=" ".join(vals[i] for i in range(len(vals)) if i not in pcols and i<len(hdr) and vals[i])
                for i in pcols:
                    if i<len(vals) and vals[i] not in ("","-"): s.cur["_multi"].append([hdr[i],[vals[i]],[ket] if hdr[i].endswith(".code") else []])
            return
        colhdr=None
        for r in flat:
            ne=[c for c in r if c]
            if not ne: continue
            first=r[0]
            pc=[i for i,c in enumerate(r) if is_path(c)]
            if len(pc)>=2 and len(r)>=3:
                colhdr=(r,pc); s.ensure(); continue
            if colhdr and not is_path(first) and len(ne)>=2:
                h,pcs=colhdr; vals=list(r)
                ket=" ".join(vals[i] for i in range(len(vals)) if i not in pcs and i<len(h) and vals[i])
                for i in pcs:
                    if i<len(vals) and vals[i] not in ("","-"): s.cur["_multi"].append([h[i],[vals[i]],[ket] if h[i].endswith(".code") else []])
                continue
            if is_path(first) or len(ne)==1: colhdr=None
            if len(r)>=4 and not is_path(first) and any(is_path(c) for c in r[2:5]): continue   # overview (No|Variabel|Resource|Path) row
            if len(r)>=4 and first=="" and r[1]=="" and not any(is_path(c) for c in r): continue
            if is_path(first):
                s.pendhdr=None; s.add(first,r[1:]); continue
            if len(ne)==1 and len(ne[0])<24 and re.fullmatch(r"[a-z][A-Za-z\[\]\.]*",ne[0]) and s.cur and s.cur["_multi"]:
                s.cur["_multi"][-1][0]+=ne[0]; continue   # path split across PDF page break
            if LBL.match(first):
                s.labels(r[1:]); continue
            if len(ne)==1 and not first=="" :
                t=ne[0]
                if SKIPH.match(t) or len(t)>160: 
                    if len(t)>160 and s.cur: s.cur["cat"]=(s.cur["cat"]+" " if s.cur["cat"] else "")+t[:300]
                    continue
                if s.pendhdr is not None and s.cur is not None and not s.cur["_multi"]:
                    # previous header had no rows -> it was a group title
                    s.V.pop(); s.kel=s.pendhdr
                s.new_var(stripnum(t)); s.pendhdr=stripnum(t); continue
            if first=="" : continue
            if first.lower().startswith(("elemen","resource","no")): continue
def lamp_lists(page,prefix):
    """returns {n: (title, cols, rows)} from lampiran page blocks"""
    L={}; head=""; n=0; cap=None
    for b in page["blocks"]:
        if b["t"]=="h": head=b["x"]
        elif b["t"]=="p":
            m=re.search(r"Lampiran\s+(\d+)",b["x"])
            if m and len(b["x"])<120: cap=int(m.group(1))
        elif b["t"]=="table":
            rows=[[clean(c) for c in r] for r in b["rows"]]
            if len(rows)<2: continue
            n+=1; num=cap or n; cap=None
            hdr=rows[0]
            cols=["system","code","display","Keterangan"] if any(h.endswith(".system") for h in hdr) else hdr[:6]
            body=[r[:len(cols)] for r in rows[1:] if any(r)]
            L[num]=(f"{prefix} Lampiran {num} — {head}"[:160],cols,body)
    return L

MODS={}
for url,page in RAW["pages"].items():
    slug=url.rstrip("/").split("/")[-1]
    if slug not in SHORT: continue
    code=SHORT[slug]; B=Builder(code); mand={}
    last_h=""
    if slug in PDFJ:  # PDF-based module
        pj=PDFJ[slug]; inlamp=False; lists={}; ln=0; curlist=None
        for pg in pj["pages"]:
            for line in pg["text"].split("\n"):
                l=line.strip()
                if (re.match(r"^[A-E]\.\s+LAMPIRAN\s*$",l) or re.match(r"^LAMPIRAN$",l)) and pg["page"]>8: inlamp=True
                if re.match(r"^\d{1,2}\.\s+(Pengiriman|Pendaftaran|Memulai|Pembaharuan|Menutup|Penutupan|Pencatatan|Registrasi)\b",l): B.tahap=l[:120]; B.kel=""; B.cur=None
                elif re.match(r"^\d{1,2}\.\d{1,2}(\.\d{1,2})*\.?\s+[A-Z]",l) and len(l)<110 and not inlamp: B.kel=stripnum(l)
                m=re.match(r"^\d{1,2}\.\s+Lampiran\s+(\d+)",l)
                if m and pg["page"]>8 and not re.search(r"\s\d+\s*$",l): inlamp=True; ln=int(m.group(1)); curlist=None
            for t in pg["tables"]:
                if not t: continue
                if str(t[0][0] or "").strip().startswith(("{","\"","[")): continue
                if inlamp:
                    rows=[[clean(c) for c in r] for r in t]
                    hdr=rows[0]
                    if any(".system" in h.replace(" ","") for h in hdr) or curlist is None:
                        key=ln or (len(lists)+1)
                        if key in lists and curlist==key: pass
                        cols=["system","code","display","Keterangan"] if any(".system" in h.replace(" ","") for h in hdr) else hdr[:6]
                        body=rows[1:] if any(".system" in h.replace(" ","") for h in hdr) else rows[1:]
                        lists.setdefault(key,[f"{code} Lampiran {key}",cols,[]])[2].extend([r[:len(cols)] for r in body if any(r)]); curlist=key
                    else:
                        lists[curlist][2].extend([r[:len(lists[curlist][1])] for r in rows if any(r)])
                else:
                    B.table(t)
        lamp={k:tuple(v) for k,v in lists.items()}
        src="PDF Google Drive: "+pj["file"]
    else:
        for b in page["blocks"]:
            if b["t"]=="h":
                if b["l"]==2: B.tahap=b["x"][:120]; B.kel=""; B.cur=None; B.pendhdr=None
                elif b["l"]>=3 and not re.match(r"^(Pemetaan|Ketentuan|Skema)",b["x"]): B.kel=b["x"][:120]; B.cur=None; B.pendhdr=None
                last_h=b["x"]
            elif b["t"]=="li" and b["x"].startswith("*") and is_path(b["x"][1:]):
                p=re.sub(r"\[i\]|<\?>|<x>","",b["x"][1:].replace(" ","")); mand.setdefault(p.split(".")[0],set()).add(p)
            elif b["t"]=="table": B.table(b["rows"])
        ls=LAMPMAP.get(slug,slug); lp=[v for k,v in RAW["lampiran"].items() if k.rstrip("/").split("/")[-1]==ls]
        lamp=lamp_lists(lp[0],code) if lp else {}
        src=url
    B.finalize()
    MODS[code]=dict(slug=slug,title=page.get("title") or code,url=url,src=src,V=B.V,mand={k:sorted(v) for k,v in mand.items()},lamp={str(k):v for k,v in lamp.items()})
json.dump(MODS,open(_D('satusehat_playbook_auto_extract.json'),'w'),ensure_ascii=False)
for c,m in MODS.items(): print(c,len(m["V"]),sum(len(v["el"]) for v in m["V"]),"lamp",len(m["lamp"]),"mand",len(m["mand"]))

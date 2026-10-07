# Element-level summaries: per concept group, per resource (Ringkasan Resource), std terminology, descriptions
import re, json
import os
_ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_D=lambda f: os.path.join(_ROOT,"data",f)
import model as M
import hier as HI
from model import ALL, G, LISTS, npath, BYID

TT=dict(M.TITLES)
CODED_SUFFIX=(".system",".code",".display")
EXCL=M.EXCL
def P(e): return e[0].lstrip("*")
def isstar(e): return e[0].startswith("*")

def codings(v):
    """-> ordered dict key(np coding prefix) -> {'rows':[[sys,code,disp,ket]], 'star':bool}; plus plain dict np->[(val,ket,lst)]"""
    el=v["el"]; nps=[npath(P(e)) for e in el]
    cnt={}
    for n in nps:
        if n.endswith(".code"): cnt[n[:-5]]=cnt.get(n[:-5],0)+1
    cod={}; plain={}; order=[]
    cursys={}
    for e,n in zip(el,nps):
        pre=n.rsplit(".",1)[0] if n.endswith(CODED_SUFFIX) else None
        if pre and pre in cnt:
            d=cod.setdefault(pre,{"rows":[],"star":False,"lists":[]})
            if pre not in order: order.append(pre)
            d["star"]=d["star"] or isstar(e)
            if n.endswith(".system"): cursys[pre]=e[1]
            elif n.endswith(".code"): d["rows"].append([cursys.get(pre,""),e[1],"",e[2]])
            elif d["rows"] and not d["rows"][-1][2]:
                d["rows"][-1][2]=e[1]
                if e[2] and not d["rows"][-1][3]: d["rows"][-1][3]=e[2]
            if len(e)>3 and e[3] not in d["lists"]: d["lists"].append(e[3])
        else:
            if n not in order: order.append(n)
            d=plain.setdefault(n,{"vals":[],"star":False,"lists":[]})
            d["star"]=d["star"] or isstar(e)
            if len(e)>3:
                if e[3] not in d["lists"]: d["lists"].append(e[3])
            else: d["vals"].append((e[1],e[2]))
    return order,cod,plain

def vnorm(x): return M.nval(x)
PLACEHOLDER=re.compile(r"^\(wajib — nilai tidak dirinci\)$")

def short_code(r):
    c=r[1]; d=r[2]
    if len(c)>40: c=c[:40]+"…"
    return (c+(" "+d if d and d not in ("SNOMED CT Description",) else "")).strip()

# ---------------- per-group element summary ----------------
def group_elements(g):
    ms=g["members"]; els={}; order=[]
    for m in ms:
        o,cod,plain=codings(m)
        for k in o:
            if k not in els: els[k]={"key":k,"coded":k in cod,"ids":[],"star":False,"opts":{},"vals":{},"lists":{}}; order.append(k)
            E=els[k]
            if m["id"] not in E["ids"]: E["ids"].append(m["id"])
            if k in cod:
                d=cod[k]; E["star"]|=d["star"]
                for r in d["rows"]:
                    ok=(r[0].rstrip("/"),r[1])
                    x=E["opts"].setdefault(ok,{"s":r[0],"c":r[1],"d":r[2],"k":r[3],"ids":[]})
                    if not x["d"] and r[2]: x["d"]=r[2]
                    if not x["k"] and r[3]: x["k"]=r[3]
                    if m["id"] not in x["ids"]: x["ids"].append(m["id"])
                for l in d["lists"]: E["lists"].setdefault(l,[]).append(m["id"])
            else:
                d=plain[k]; E["star"]|=d["star"]
                for val,ket in d["vals"]:
                    nk=vnorm(val) if not PLACEHOLDER.match(val) else "~"
                    x=E["vals"].setdefault(nk,{"v":val,"k":ket,"ids":[]})
                    if PLACEHOLDER.match(x["v"]) and not PLACEHOLDER.match(val): x["v"]=val
                    if m["id"] not in x["ids"]: x["ids"].append(m["id"])
                for l in d["lists"]: E["lists"].setdefault(l,[]).append(m["id"])
    return [els[k] for k in order]

def _skip_key(k):
    return bool(EXCL.search(k)) or k.endswith(".subject") or k.endswith(".patient")

def title_of(i): return BYID[i]["title"]
def label_of(i): return f"{BYID[i]['title']}"

def explain(g,els):
    """per-element, all-member explanation"""
    ms=g["members"]; ids=[m["id"] for m in ms]; out=[]
    if len(ms)<2: return out
    res={m["id"]:m["res"] for m in ms}
    if len(set(res.values()))>1:
        by={}
        for i,r in res.items(): by.setdefault(r,[]).append(i)
        out.append({"el":"Resource","kind":"beda","parts":[[r,v] for r,v in by.items()]})
    for E in els:
        k=E["key"]
        if _skip_key(k): continue
        missing=[i for i in ids if i not in E["ids"]]
        # value signature per member
        sig={}
        for i in E["ids"]:
            if E["coded"]:
                s=tuple(sorted(short_code([o["s"],o["c"],o["d"]]) for o in E["opts"].values() if i in o["ids"] and not any(sy in o["s"] for sy in M.ANCSYS)))
            else:
                s=tuple(sorted(x["v"][:60] for nk,x in E["vals"].items() if i in x["ids"] and nk!="~"))
            s=s+tuple("Daftar "+l for l,li in E["lists"].items() if i in li)
            sig[i]=s
        distinct=set(v for v in sig.values() if v)
        if not missing and len(distinct)<=1: continue
        by={}
        for i,s in sig.items(): by.setdefault(s,[]).append(i)
        parts=[[("; ".join(s) if s else "(ada, nilai tidak dirinci)"),v] for s,v in by.items()]
        if missing: parts.append(["(elemen tidak dipakai)",missing])
        kind="beda" if len(distinct)>1 else "sebagian"
        out.append({"el":k,"kind":kind,"parts":parts,"star":E["star"]})
    return out

for g in G:
    g["els"]=group_elements(g)
    g["expl"]=explain(g,g["els"])

# ---------------- Pelengkap: elemen dari playbook lain (grup "Saling melengkapi") ----------------
for v in ALL: v["sup"]=[]

for g in G:
    if g["status"]!="Saling melengkapi": continue
    ids=[m["id"] for m in g["members"]]
    for E in g["els"]:
        if _skip_key(E["key"]): continue
        miss=[i for i in ids if i not in E["ids"]]
        if not miss: continue
        if E["coded"]:
            body=[[o["s"],o["c"],o["d"],o["k"]] for o in E["opts"].values()]
        else:
            body=[[x["v"],x["k"]] for nk,x in E["vals"].items() if not PLACEHOLDER.match(x["v"])]
        lists=list(E["lists"].keys())
        if not body and not lists: continue
        src=sorted(E["ids"])
        for i in miss:
            BYID[i]["sup"].append(dict(key=E["key"],coded=E["coded"],star=E["star"],body=body[:40],lists=lists,src=src))
NSUP=sum(len(v["sup"]) for v in ALL); NSUPVAR=sum(1 for v in ALL if v["sup"])

# ---------------- Ringkasan Resource ----------------
CHOICE=re.compile(r"^(value|effective|onset|abatement|performed|occurrence|medication|deceased|multipleBirth|asNeeded|collected|fastingStatus|reported|allowed|born|serviced|timing|product|item|statusReason|dose|rate|scheduled|defaultValue|answer)(Quantity|CodeableConcept|String|Boolean|Integer|Range|Ratio|SampledData|Time|DateTime|Period|Timing|Instant|Age|Reference|Coding|Date|Decimal|Attachment|Uri|Url|Canonical|Code|Id|Markdown|PositiveInt|UnsignedInt|Identifier|Duration|SimpleQuantity)$")
def elem_of(rt,np_):
    segs=np_.split(".")[1:]
    if not segs: return ("(resource)",None)
    s0=re.sub(r":.*","",segs[0])
    if s0.endswith("[x]"): return (s0,None)
    if s0 in ("value","effective","onset","abatement","performed","occurrence","medication","deceased","multipleBirth","asNeeded","collected","born","reported"): return (s0+"[x]",s0+" (tipe tidak disebut)")
    m=CHOICE.match(s0)
    if m and m.group(1) not in ("item","product","dose","rate","timing","statusReason") or (m and rt in ("MedicationDispense",) and m.group(1)=="statusReason"):
        return (m.group(1)+"[x]",s0)
    if s0=="component" and len(segs)>1:
        s1=segs[1]; m=CHOICE.match(s1)
        if m and m.group(1)=="value": return ("component.value[x]",s1)
        return ("component."+s1,None)
    return (s0,None)

CANON={  # FHIR R4 top-level elements (choice types dikelompokkan sebagai [x])
 "Observation":"identifier basedOn partOf status category code subject focus encounter effective[x] issued performer value[x] dataAbsentReason interpretation note bodySite method specimen device referenceRange hasMember derivedFrom component.code component.value[x] component.dataAbsentReason component.interpretation component.referenceRange",
 "Encounter":"identifier status statusHistory class classHistory type serviceType priority subject episodeOfCare basedOn participant appointment period length reasonCode reasonReference diagnosis account hospitalization location serviceProvider partOf",
 "Condition":"identifier clinicalStatus verificationStatus category severity code bodySite subject encounter onset[x] abatement[x] recordedDate recorder asserter stage evidence note",
 "Procedure":"identifier instantiatesCanonical instantiatesUri basedOn partOf status statusReason category code subject encounter performed[x] recorder asserter performer location reasonCode reasonReference bodySite outcome report complication complicationDetail followUp note focalDevice usedReference usedCode",
 "CarePlan":"identifier instantiatesCanonical instantiatesUri basedOn replaces partOf status intent category title description subject encounter period created author contributor careTeam addresses supportingInfo goal activity note",
 "AllergyIntolerance":"identifier clinicalStatus verificationStatus type category criticality code patient encounter onset[x] recordedDate recorder asserter lastOccurrence note reaction",
 "ServiceRequest":"identifier instantiatesCanonical instantiatesUri basedOn replaces requisition status intent category priority doNotPerform code orderDetail quantity[x] subject encounter occurrence[x] asNeeded[x] authoredOn requester performerType performer locationCode locationReference reasonCode reasonReference insurance supportingInfo specimen bodySite note patientInstruction relevantHistory",
 "DiagnosticReport":"identifier basedOn status category code subject encounter effective[x] issued performer resultsInterpreter specimen result imagingStudy media conclusion conclusionCode presentedForm",
 "Medication":"identifier code status manufacturer form amount ingredient batch extension",
 "MedicationRequest":"identifier status statusReason intent category priority doNotPerform reported[x] medication[x] subject encounter supportingInformation authoredOn requester performer performerType recorder reasonCode reasonReference instantiatesCanonical instantiatesUri basedOn groupIdentifier courseOfTherapyType insurance note dosageInstruction dispenseRequest substitution priorPrescription detectedIssue eventHistory",
 "MedicationDispense":"identifier partOf status statusReason[x] category medication[x] subject context supportingInformation performer location authorizingPrescription type quantity daysSupply whenPrepared whenHandedOver destination receiver note dosageInstruction substitution detectedIssue eventHistory",
 "MedicationStatement":"identifier basedOn partOf status statusReason category medication[x] subject context effective[x] dateAsserted informationSource derivedFrom reasonCode reasonReference note dosage",
 "QuestionnaireResponse":"identifier basedOn partOf questionnaire status subject encounter authored author source item",
 "ClinicalImpression":"identifier status statusReason code description subject encounter effective[x] date assessor previous problem investigation protocol summary finding prognosisCodeableConcept prognosisReference supportingInfo note",
 "Specimen":"identifier accessionIdentifier status type subject receivedTime parent request collection processing container condition note extension",
 "Immunization":"identifier status statusReason vaccineCode patient encounter occurrence[x] recorded primarySource reportOrigin location manufacturer lotNumber expirationDate site route doseQuantity performer note reasonCode reasonReference isSubpotent subpotentReason education programEligibility fundingSource reaction protocolApplied",
 "EpisodeOfCare":"identifier status statusHistory type diagnosis patient managingOrganization period referralRequest careManager team account",
 "Composition":"identifier status type category subject encounter date author title confidentiality attester custodian relatesTo event section",
 "FamilyMemberHistory":"identifier instantiatesCanonical instantiatesUri status dataAbsentReason patient date name relationship sex born[x] age[x] estimatedAge deceased[x] reasonCode reasonReference note condition",
 "ImagingStudy":"identifier status modality subject encounter started basedOn referrer interpreter endpoint numberOfSeries numberOfInstances procedureReference procedureCode location reasonCode reasonReference note description series",
 "Goal":"identifier lifecycleStatus achievementStatus category priority description subject start[x] target statusDate statusReason expressedBy addresses note outcomeCode outcomeReference",
 "RelatedPerson":"identifier active patient relationship name telecom gender birthDate address photo period communication",
 "NutritionOrder":"identifier instantiatesCanonical instantiatesUri instantiates status intent patient encounter dateTime orderer allergyIntolerance foodPreferenceModifier excludeFoodModifier oralDiet supplement enteralFormula note",
 "Patient":"identifier active name telecom gender birthDate deceased[x] address maritalStatus multipleBirth[x] photo contact communication generalPractitioner managingOrganization link extension",
}
CANON={k:v.split() for k,v in CANON.items()}

RS={}
for v in ALL:
    if v.get("syn"): continue
    seen=set()
    for e in v["el"]:
        p=P(e); np_=npath(p)
        rt=np_.split(".")[0]
        if not re.match(r"^[A-Z][A-Za-z]+$",rt): continue
        R=RS.setdefault(rt,{"vars":set(),"titles":set(),"els":{}})
        R["vars"].add(v["id"]); R["titles"].add(v["title"])
        el,choice=elem_of(rt,np_)
        E=R["els"].setdefault(el,{"vars":set(),"titles":set(),"star":set(),"choices":{},"paths":{}})
        E["vars"].add(v["id"]); E["titles"].add(v["title"])
        if isstar(e): E["star"].add(v["title"])
        if choice: E["choices"].setdefault(choice,set()).add(v["id"])
# coded / plain values per path, via codings()
for v in ALL:
    if v.get("syn"): continue
    o,cod,plain=codings(v)
    for k in o:
        rt=k.split(".")[0]
        if rt not in RS: continue
        el,choice=elem_of(rt,k)
        E=RS[rt]["els"].get(el)
        if E is None: continue
        Pp=E["paths"].setdefault(k,{"coded":k in cod,"vals":{},"lists":{},"vars":set()})
        Pp["vars"].add(v["id"])
        if k in cod:
            Pp["coded"]=True
            for r in cod[k]["rows"]:
                ok=(r[0].rstrip("/"),r[1])
                x=Pp["vals"].setdefault(ok,{"s":r[0],"c":r[1],"d":r[2],"ids":set()})
                if not x["d"] and r[2]: x["d"]=r[2]
                x["ids"].add(v["id"])
            for l in cod[k]["lists"]: Pp["lists"].setdefault(l,set()).add(v["id"])
        else:
            for val,ket in plain[k]["vals"]:
                nk=vnorm(val) if not PLACEHOLDER.match(val) else "~"
                x=Pp["vals"].setdefault(nk,{"v":val,"ids":set()})
                if PLACEHOLDER.match(x["v"]) and not PLACEHOLDER.match(val): x["v"]=val
                x["ids"].add(v["id"])
            for l in plain[k]["lists"]: Pp["lists"].setdefault(l,set()).add(v["id"])

# ---------------- Lampiran Standar Terminologi ----------------
STD=json.load(open(_D('satusehat_standar_terminologi_v10.3.json')))
def nk(p):
    p=re.sub(r"\[[^\]]*\]","",p).replace("extension:","extension.")
    p=re.sub(r"\.coding\b","",p)
    p=re.sub(r"\.(code|system|display|CodeableConcept)$","",p)
    return p.lower().replace(" ","")
STDBY={}
for s in STD:
    if not s["path"].split(".")[0] in RS and s["res"] not in RS: continue
    STDBY.setdefault(nk(s["path"]),[]).append(s)
# attach
matched=set()
for rt,R in RS.items():
    for el,E in R["els"].items():
        for k,Pp in E["paths"].items():
            ss=STDBY.get(nk(k))
            if not ss: continue
            usedc={x.get("c",x.get("v")) for x in Pp["vals"].values()}
            extra=[]; notes=[]
            for s in ss:
                matched.add(s["no"]+s["path"])
                for r in s["rows"]:
                    if r["code"] in usedc: continue
                    extra.append([r["system"],r["code"],r["display"] or "",r["ket"] or ""])
                if s["note"]: notes.append(s["note"][:400])
            Pp["std"]={"sec":[f'{s["no"]} {s["path"]} (hlm. {s["page"]})' for s in ss],"extra":extra,"note":notes,"n":sum(len(s["rows"]) for s in ss)}
# std sections for elements/paths not used in any playbook
for s in STD:
    rt=s["path"].split(".")[0]
    if rt not in RS or (s["no"]+s["path"]) in matched: continue
    np_=re.sub(r"\[[^\]]*\]","",s["path"]).replace("extension:","extension.")
    el,_=elem_of(rt,np_)
    R=RS[rt]
    E=R["els"].get(el)
    lst=R.setdefault("stdonly",[])
    lst.append({"path":s["path"],"el":el,"sec":f'{s["no"]} {s["path"]} (hlm. {s["page"]})',"rows":[[r["system"],r["code"],r["display"] or "",r["ket"] or ""] for r in s["rows"]],"note":s["note"][:400],"elused":E is not None})

def level(p):
    return "Inti" if p>=0.8 else ("Umum" if p>=0.4 else ("Kadang" if p>=0.1 else "Jarang"))

RSOUT={}
for rt,R in sorted(RS.items()):
    nv=len(R["vars"]); titles=sorted(R["titles"],key=lambda t:[x for x,_ in M.TITLES].index(t))
    els=[]
    canon=CANON.get(rt,[])
    for el,E in R["els"].items():
        pct=len(E["vars"])/nv
        paths=[]
        for k,Pp in sorted(E["paths"].items()):
            if Pp["coded"]:
                vals=[[x.get("s",""),x.get("c",x.get("v")),x.get("d",""),sorted(x["ids"])] for x in Pp["vals"].values()]
            else:
                vals=[[x["v"],sorted(x["ids"])] for x in Pp["vals"].values()]
            paths.append({"p":k,"coded":Pp["coded"],"vals":vals,"lists":{l:sorted(i) for l,i in Pp["lists"].items()},"n":len(Pp["vars"]),"std":Pp.get("std")})
        # per-title coverage
        cov={t:0 for t in titles}
        for i in E["vars"]: cov[BYID[i]["title"]]+=1
        els.append({"el":el,"n":len(E["vars"]),"np":len({HI.ROOT.get(i,i) for i in E["vars"]}),"pct":round(pct,3),"lvl":level(pct),"titles":sorted(E["titles"]),"star":sorted(E["star"]),
                    "choices":{c:len(i) for c,i in sorted(E["choices"].items(),key=lambda x:-len(x[1]))},"paths":paths,"canon":el in canon,"cov":cov})
    els.sort(key=lambda x:(-x["pct"],x["el"]))
    tv={t:0 for t in titles}
    for i in R["vars"]: tv[BYID[i]["title"]]+=1
    used={e["el"] for e in els}
    # variables missing core elements
    core=[e["el"] for e in els if e["pct"]>=0.8]
    miss=[]
    for i in sorted(R["vars"]):
        have={el for el,E in R["els"].items() if i in E["vars"]}
        m=[c for c in core if c not in have]
        if m: miss.append([i,m])
    RSOUT[rt]={"nv":nv,"npar":len({HI.ROOT.get(i,i) for i in R["vars"]}),"titles":titles,"tv":tv,"els":els,"unused":[c for c in canon if c not in used],"core":core,"miss":miss,"stdonly":R.get("stdonly",[]),"canon":bool(canon)}

# ---------------- Deskripsi variabel ----------------
RAW=json.load(open(_D('satusehat_playbook_raw_20261007.json')))
PDFJ=json.load(open(_D('satusehat_playbook_pdf_20261007.json')))["modules"]
AUTO=json.load(open(_D('satusehat_playbook_auto_extract.json')))
URL={"ANC":"https://satusehat.kemkes.go.id/platform/docs/id/interoperability/anc/","RJ":"https://satusehat.kemkes.go.id/platform/docs/id/interoperability/rme-rawat-jalan/"}
for c,m in AUTO.items(): URL[c]=m["url"]
BOIL=re.compile(r"(Berikut( ini)? (adalah )?pemetaan|Penjelasan tipe mandatoris|Postman|Pemetaan Nilai|dapat dilihat (pada|di) (tabel|gambar)|Silakan klik|Terminologi spesifik yang digunakan|Setiap terdapat simbol)",re.I)
def sentences(t): return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])",t) if s.strip()]
MODTXT={}; STEPTXT={}
for code,url in URL.items():
    pg=RAW["pages"].get(url)
    if not pg: continue
    paras=[]; step=None; st={}
    for b in pg["blocks"]:
        if b["t"]=="h":
            m=re.match(r"^(\d{1,2})\.\s+(.*)",b["x"] or "")
            if m: step=m.group(1)
        elif b["t"] in ("p","li") and b.get("x"):
            x=b["x"]
            if BOIL.search(x) and len(x)<400: continue
            paras.append(x)
            if step and b["t"]=="p" and len(st.get(step,""))<700: st[step]=(st.get(step,"")+" "+x).strip()
    MODTXT[code]=paras; STEPTXT[code]=st
slug2code={m["slug"]:c for c,m in AUTO.items()}
for slug,pj in PDFJ.items():
    code="HIV" if slug=="hiv" else slug2code.get(slug)
    if not code: continue
    txt=" ".join(re.sub(r"(BUKU PANDUAN PUBLIK|SATUSEHAT versi[^\n]*|Halaman\s*\n?\s*\d+ dari \d+)","",p["text"]).replace("\n"," ") for p in pj["pages"])
    MODTXT[code]=[txt]
def stepnum(t):
    m=re.match(r"^(\d{1,2})\.",t or ""); return m.group(1) if m else None
def find_sentence(v):
    name=v["var"]; nm=re.sub(r"\s*\(.*?\)","",name).strip()
    if len(nm)<5: return None
    pat=re.compile(r"\b"+re.escape(nm)+r"\b",re.I)
    best=None
    for para in MODTXT.get(v["title"],[]):
        if not pat.search(para): continue
        for s in sentences(para):
            if pat.search(s) and 30<=len(s)<=420 and not BOIL.search(s) and "http" not in s and "{" not in s and not s.rstrip().endswith(":"):
                if re.search(r"\b(adalah|merupakan|yaitu|digunakan|untuk|berisi|mencatat|menunjukkan|didefinisikan|meliputi)\b",s,re.I):
                    return s
                best=best or s
    return best

RESDESC={"Observation":"hasil pemeriksaan/observasi","Condition":"kondisi/diagnosis pasien","Procedure":"tindakan/prosedur yang dilakukan","QuestionnaireResponse":"jawaban kuesioner/formulir",
 "Encounter":"data kunjungan","EpisodeOfCare":"episode perawatan","ServiceRequest":"permintaan layanan/pemeriksaan","Specimen":"spesimen","DiagnosticReport":"laporan hasil pemeriksaan penunjang",
 "MedicationRequest":"peresepan obat","MedicationDispense":"pengeluaran/pemberian obat","Medication":"data obat","Immunization":"pemberian imunisasi","AllergyIntolerance":"riwayat alergi",
 "CarePlan":"rencana asuhan/tindak lanjut","ClinicalImpression":"penilaian klinis/prognosis","Composition":"dokumen ringkasan (resume)","FamilyMemberHistory":"riwayat penyakit keluarga",
 "ImagingStudy":"citra hasil pemeriksaan radiologi","Patient":"identitas pasien","RelatedPerson":"data keluarga/penanggung jawab pasien","Goal":"target/tujuan asuhan","NutritionOrder":"instruksi diet/gizi",
 "MedicationStatement":"riwayat penggunaan obat","Claim":"data klaim","Coverage":"data penjaminan","Location":"data lokasi","Organization":"data organisasi"}
VALDESC=[("valueQuantity","angka (dengan satuan)"),("valueCodeableConcept","pilihan kode"),("valueString","teks bebas"),("valueBoolean","ya/tidak"),("valueInteger","bilangan bulat"),("valueDateTime","tanggal/waktu"),("valueRange","rentang nilai"),("valueRatio","rasio"),("valueTime","jam")]
def main_display(v):
    for e in v["el"]:
        n=npath(P(e))
        if re.search(r"\.(code|vaccineCode|medicationCodeableConcept|type)(\.coding)?\.display$",n) and e[1] and not e[1].startswith("(") and "Description" not in e[1] and len(e[1])<90:
            sysrow=[x for x in v["el"] if npath(P(x))==n[:-8]+".code"]
            return e[1]
    return None
def gen_desc(v):
    rs=[x.strip() for x in re.split(r"[+,]",v["res"]) if x.strip()]
    r0=rs[0] if rs else ""
    what=RESDESC.get(r0,"data "+r0)
    md=main_display(v)
    tah=re.sub(r'^\d+\.\s*','',v['tahap'])
    s=f"{v['var']} — {what}" + (f" dengan kode utama “{md}”" if md else "") + f", dicatat pada tahap “{tah}”"
    s+=f" dan dikirim menggunakan resource {' + '.join(rs)}."
    o,cod,plain=codings(v)
    vt=[d for k,d in VALDESC if any(npath(P(e)).endswith("."+k) or ("."+k+".") in npath(P(e)) for e in v["el"])]
    nopt=0
    for k,d in cod.items():
        if re.search(r"value|answer|code$",k) and len(d["rows"])>=2 and not k.endswith("category"): nopt=max(nopt,len(d["rows"]))
    if nopt>=2: s+=f" Nilai dipilih dari {nopt} pilihan jawaban yang tersedia."
    elif vt: s+=f" Nilai diisi sebagai {vt[0]}."
    if any(len(e)>3 for e in v["el"]): s+=" Daftar pilihan lengkap mengacu ke lampiran."
    return s
DESC={}
nplay=0
for v in ALL:
    if v.get("syn"):
        DESC[v["id"]]={"src":"claude","t":f"{v['var']} — kelompok variabel dari playbook {v['title']}: judul kelompok pada tabel pemetaan nilai yang menaungi {len(v['anak'])} variabel di bawahnya. Kelompok ini penanda struktur dokumen, bukan elemen FHIR.","ctx":""}
        continue
    step=stepnum(v["tahap"]); ctx=STEPTXT.get(v["title"],{}).get(step) if step else None
    base=v
    if v.get("copy"):
        src=[x for x in ALL if x["title"]=="RJ" and x["var"]==v["var"]]
        if src: base=src[0]
    s=find_sentence(base)
    if s: nplay+=1; DESC[v["id"]]={"src":"playbook","t":s,"ctx":(ctx or "")[:600]}
    else: DESC[v["id"]]={"src":"claude","t":gen_desc(v),"ctx":(ctx or "")[:600]}
if __name__=="__main__":
    import collections
    print("groups",len(G)); print("resources",len(RSOUT))
    for rt in ["Observation","Procedure","Condition"]:
        R=RSOUT[rt]; print(rt,R["nv"],len(R["els"]),R["core"],len(R["miss"]),len(R["stdonly"]),R["unused"][:8])
    print("desc playbook",nplay,"of",len(ALL))
    g=[g for g in G if g["label"]=="Edukasi"][0]
    for x in g["expl"]: print(x["el"],x["kind"]); [print("    ",p[0][:150],p[1]) for p in x["parts"]]
    import random
    for v in random.sample(ALL,6): print(v["id"],v["var"],DESC[v["id"]])

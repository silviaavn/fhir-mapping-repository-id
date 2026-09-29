import re, copy, json, os
import data3, rj, hiv
_ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_D=lambda f: os.path.join(_ROOT,"data",f)
TITLES=[("ANC","Antenatal Care (ANC)"),("RJ","Resume Medis Rawat Jalan"),("HIV","HIV (Fase 1)")]
SRC={"HIV":"Playbook Modul HIV v1.0 (PDF, header versi 1.3 / 15 Agu 2024; halaman web disunting 8 Des 2024)","ANC":"Playbook ANC (2 Okt 2025) + Lampiran Terminologi ANC (1 Nov 2024)","RJ":"Playbook Resume Medis Rawat Jalan + Lampiran Terminologi RME Rawat Jalan (7 Okt 2024)"}

# ---------- RJ: lampiran notes & lists ----------
LAMP={"Prognosis":"Lampiran: v1.2 memakai Kemkes clinical-term PR000001–PR000004, v2.0 diganti SNOMED.",
 "Kondisi saat meninggalkan RS (Condition)":"Lampiran: v1.2 memakai Kemkes clinical-term MN000001–MN000003, v2.0 diganti SNOMED.",
 "Tingkat kesadaran":"Lampiran: v1.2 memakai Kemkes clinical-term TK000001–TK000006, v2.0 diganti SNOMED. Display 450847001 di lampiran 'Response to pain', di playbook 'Responds to pain'.",
 "Rencana tindak lanjut":"Lampiran: rawat inap v1.2 = Kemkes TL000001, v2.0 = SNOMED 737481003.",
 "Edukasi":"Lampiran: v1.2 memakai Kemkes clinical-term ED000001–ED000007, v2.0 diganti SNOMED."}
for v in rj.V:
    if v["var"] in LAMP: v["cat"]=(v["cat"]+" " if v["cat"] else "")+LAMP[v["var"]]
    if v["var"] in ("Peresepan obat","Pengeluaran obat"):
        v["el"]=[(e[0],e[1],e[2],"kfa") if e[0]=="Medication.code.coding.code" else e for e in v["el"]]
    if v["var"]=="Peresepan obat":
        v["el"]=[(e[0],e[1],e[2],"resep") if e[0].startswith("Medication.ingredient.itemCodeableConcept") else e for e in v["el"]]

# ---------- ANC: replace 'rujuk modul' steps with RJ copies ----------
RJBY={v["var"]:v for v in rj.V}
RJSEC={v["var"]:v["tahap"] for v in rj.V}
REPL={"7.":["Permintaan pemeriksaan laboratorium","Status puasa pasien","Spesimen laboratorium","Hasil pemeriksaan laboratorium","Laporan pemeriksaan laboratorium","Permintaan pemeriksaan radiologi","Status alergi bahan kontras","Status kehamilan","Status puasa (radiologi)","Citra DICOM","Hasil (bacaan) radiologi","Laporan / kesimpulan radiologi"],
 "8.":["Diagnosis"],"9.":["Permintaan tindakan","Pelaksanaan tindakan"],"11.":["Peresepan obat","Pengkajian resep","Pengeluaran obat"],
 "12.":["Rencana tindak lanjut"],"13.":["Instruksi tindak lanjut & sarana transportasi rujuk"],"14.":["Kondisi saat meninggalkan RS (Condition)","Kondisi saat meninggalkan RS (Encounter)"],"15.":["Cara keluar dari RS"]}
ANC=[]; done=set()
for v in data3.V:
    k=v["tahap"].split(" ")[0]
    if k in REPL:
        if v["var"]=="Waktu kematian (bila meninggal)": pass
        else:
            if k not in done:
                for name in REPL[k]:
                    c=copy.deepcopy(RJBY[name]); c["tahap"]=v["tahap"]; c["copy"]="RJ"
                    c["cat"]=f"Disalin dari Rawat Jalan § {RJSEC[name]} (playbook ANC merujuk ke modul Rawat Jalan). "+c["cat"]
                    ANC.append(c)
                done.add(k)
            continue
    ANC.append(v)
# the Waktu kematian row sits after the step-14 copies (already the case by order)
HIVL=[]
for v in hiv.V:
    if v["tahap"].startswith("10.") and not any(x["tahap"].startswith("6.") for x in HIVL):
        for tah,names in hiv.COPY.items():
            for name in names:
                c=copy.deepcopy(RJBY[name]); c["tahap"]=tah; c["copy"]="RJ"
                c["cat"]=f"Disalin dari Rawat Jalan § {RJSEC[name]} (playbook HIV merujuk ke modul Rawat Jalan). "+c["cat"]
                HIVL.append(c)
    HIVL.append(v)
for v in ANC: v["title"]="ANC"
for v in rj.V: v["title"]="RJ"
for v in HIVL: v["title"]="HIV"
ALL=ANC+rj.V+HIVL
# ---------- auto-extracted modules ----------
AUTO=json.load(open(_D("satusehat_playbook_auto_extract.json")))
AUTOLISTS={}
for code,md in AUTO.items():
    TITLES.append((code,md["title"]))
    SRC[code]=("Ekstraksi otomatis dari "+md["src"]+" (18 Sep 2026) — belum dicek manual")
    mand={}
    for p in [x for ps in md["mand"].values() for x in ps]:
        mand.setdefault(p.split(".")[0],set()).add(re.sub(r"\[(i|\d)\]","",p))
    for k,(t,cols,rows) in md["lamp"].items():
        AUTOLISTS[f"{code}-L{k}"]=dict(title=t,cols=cols,rows=[[str(c) for c in r] for r in rows])
    for v in md["V"]:
        el=[]
        for e in v["el"]:
            p,val,ket=e[0],e[1],e[2]
            base=re.sub(r"\[(i|\d)\]","",p.lstrip("*")).replace(" ","")
            root=base.split(".")[0]
            if not p.startswith("*") and any(base==mp or base.startswith(mp+".") for mp in mand.get(root,())): p="*"+p
            mm=re.search(r"Lampiran\s+(\d+)",val)
            if mm and f"{code}-L{mm.group(1)}" in AUTOLISTS: el.append((p,"(pilih dari daftar)",f"Lampiran {mm.group(1)}",f"{code}-L{mm.group(1)}"))
            else: el.append((p,val,ket))
        roots={e[0].lstrip("*").split(".")[0] for e in el}
        have={re.sub(r"\[(i|\d)\]","",e[0].lstrip("*")).replace(" ","") for e in el}
        for r in roots:
            for mp in sorted(mand.get(r,())):
                if not any(h==mp or h.startswith(mp+".") for h in have): el.append(("*"+mp,"(wajib — nilai tidak dirinci)","Dari daftar elemen wajib (pemetaan nilai)"))
        v2=dict(v); v2["el"]=el; v2["title"]=code
        v2["cat"]=("Ekstraksi otomatis — belum dicek manual. "+(v.get("cat") or "")).strip()
        ALL.append(v2)
cnt={t:0 for t,_ in TITLES}
for v in ALL:
    cnt[v["title"]]+=1; v["id"]=f'{v["title"]}-{cnt[v["title"]]:03d}'
    v["el"]=[tuple(e) for e in v["el"]]

# ---------- normalisation ----------
GENERIC_PATH=re.compile(r"\.(subject|patient|encounter|context|performer(\[i\])?(\.actor)?|effectiveDateTime|recorder|author(\[i\])?|source|authored)$")
def npath(p): return re.sub(r"\[(i|\d)\]","",p.replace("*","")).replace(" ","")
PLACE=re.compile(r"(Code|Kode|Description|Deskripsi|ECL|\(|Lihat|/\{|\{)")
def concrete(val): return bool(val) and not PLACE.search(val) and len(val)<=20 and " " not in val.strip()
MAINCODE=re.compile(r"^(\w+)\.(code|type|vaccineCode|medicationCodeableConcept)(\.coding)?\.code$|^\w+\.bodySite\.coding\.code$|^Procedure\.code\.coding\.code$")
STDSYS=("http://loinc.org","http://snomed.info/sct","http://hl7.org/fhir/sid/icd-10","http://terminology.kemkes.go.id/CodeSystem/clinical-term","http://terminology.kemkes.go.id","http://sys-ids.kemkes.go.id/kfa","http://terminology.kemkes.go.id/CodeSystem/kptl")
def codes_with_system(v):
    out=[]; sysv=None
    for e in v["el"]:
        p=npath(e[0])
        if p.endswith(".system"): sysv=e[1]
        if p.endswith(".code") and "category" not in p and "Quantity" not in p and "quantity" not in p and sysv!="http://unitsofmeasure.org" and concrete(e[1]):
            out.append((p,sysv,e[1]))
    return out
def key_codes(v):
    ks=set()
    for p,s,c in codes_with_system(v):
        if MAINCODE.match(p) and s in STDSYS: ks.add(c)
    # value-set options are not identity; keep only main code identity (exclude option codes on value paths)
    return frozenset(ks)
def nname(s): return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9() ]","",s.lower())).strip()

# ---------- manual concept relations ----------
def find(title,name):
    r=[v for v in ALL if v["title"]==title and v["var"]==name]
    assert r, (title,name); return r[0]
SAME0=[  # (ANC var, RJ var, label, note)
 ("Identitas pasien (22 butir)","Nomor SATUSEHAT (IHS) pasien","Identitas pasien / nomor IHS","ANC merinci 22 butir identitas Patient; RJ hanya merujuk ke MPI."),
 ("Kunjungan ANC","Kunjungan rawat jalan","Pendaftaran kunjungan (Encounter)","Daftar elemen wajib berbeda: RJ mewajibkan classHistory & hospitalization.dischargeDisposition dan merinci class AMB + kelas layanan; ANC mewajibkan diagnosis.use/rank & menautkan episodeOfCare."),
 ("Kunjungan selesai + status kunjungan ANC","Kunjungan selesai","Pembaruan kunjungan saat selesai","ANC menambah Encounter.identifier status K1A–K6 dan episodeOfCare; RJ menambah Encounter.length."),
 ("Gigi dan mulut","Gigi geligi","Pemeriksaan fisik gigi & mulut","Maksud sama, kode beda: ANC SNOMED 423066003 'Finding of mouth region' + interpretation N/A; RJ LOINC 85910-8 + narasi."),
 ("Riwayat penyakit menular","Riwayat penyakit pribadi","Riwayat penyakit pribadi / menular","Kode (ECL) sama, tetapi category beda: ANC problem-list-item (HL7 condition-category), RJ previous-condition (Kemkes). RJ juga memakai clinicalStatus."),
 ("Riwayat penyakit keluarga","Riwayat penyakit keluarga","Riwayat penyakit keluarga","Resource beda: ANC memakai Condition, RJ memakai FamilyMemberHistory (relationship FAMMEMB) — ECL SNOMED sama."),
 ("Tema edukasi yang diberikan","Edukasi","Edukasi","ANC memakai kode Kemkes clinical-term ED000008–ED000012 (+ SNOMED 61310001) tanpa category; RJ v2.0 mewajibkan 2 coding (KPTL 10913 + SNOMED) dan category 409073007, serta telah mengganti kode Kemkes ED000001–7 ke SNOMED."),
]

SAME=[([("ANC",a),("RJ",b)],lab,note) for a,b,lab,note in SAME0]
_ed=[x for x in SAME if x[1]=="Edukasi"][0]
for _v in ALL:   # semua variabel Procedure edukasi = satu konsep (satu daftar pilihan jawaban)
    if _v["var"].lower().startswith("edukasi") and "Procedure" in _v["res"] and (_v["title"],_v["var"]) not in _ed[0] and not _v.get("copy"): _ed[0].append((_v["title"],_v["var"]))
SAME[1][0].append(("HIV","Kunjungan HIV (asal rujukan & alasan kunjungan)"))
SAME[1]=(SAME[1][0],SAME[1][1],SAME[1][2]+" HIV menambah asal rujukan (admitSource) & alasan kunjungan (reasonCode) dengan kode Kemkes/SNOMED.")
SAME+=[([("ANC","Skrining PPIA HIV"),("HIV","Rapid HIV 1+2 Ab (single)")],"Skrining / rapid HIV","Maksud sama, kode beda: ANC LOINC 68961-2 dengan nilai SNOMED 11214006/131194007 (Reactive/Non-Reactive); HIV memakai LOINC 7918-6/31201-7/80387-4 dengan nilai LOINC LA18332-9/LA15256-3 dan interpretation RR/NR."),
 ([("ANC","Skrining PPIA Sifilis (RPR)"),("ANC","Skrining PPIA Sifilis (VDRL)"),("HIV","RPR / VDRL")],"Skrining sifilis RPR / VDRL","Kode beda: ANC RPR 20508-8 [Units/volume] & VDRL 14904-7 [in Specimen] dengan nilai SNOMED; HIV RPR 20507-0 & VDRL 5292-8 [Presence] dengan nilai LOINC LA15255-5/LA15256-3."),
 ([("RJ","Permintaan pemeriksaan laboratorium"),("HIV","Permintaan pemeriksaan laboratorium HIV/IMS")],"Permintaan pemeriksaan laboratorium","HIV menambah reasonCode (Lampiran 8) dan memakai kode examination Kemkes (X099419/X099420) selain LOINC; RJ memakai LOINC + KPTL."),
 ([("RJ","Spesimen laboratorium"),("HIV","Spesimen HIV/IMS")],"Spesimen laboratorium","HIV memakai daftar tertutup jenis spesimen (Lampiran 10) & kondisi spesimen via status + condition (Lampiran 11); RJ memakai ECL SNOMED dan condition.text.")]
RELATED0=[  # (ANC var, RJ var, note)
 ("THT","Telinga","ANC 1 variabel THT (SNOMED 297268004); RJ memecah menjadi telinga/hidung/tenggorokan (LOINC)."),
 ("THT","Hidung",""),("THT","Tenggorokan",""),
 ("Dada (jantung)","Dada","ANC memecah dada menjadi jantung (LOINC 10200-4) & paru (SNOMED 301230006); RJ satu variabel LOINC 11391-0."),("Dada (paru)","Dada",""),
 ("Tungkai","Tungkai atas","ANC SNOMED 116312005 'Finding of lower limb'; RJ memecah tungkai atas (11414-0) & bawah (11389-4)."),("Tungkai","Tungkai bawah",""),
 ("Tidak diberikan konseling","Edukasi","Kode 409073007 'Education' dipakai ANC sebagai Procedure.code (status not-done), sedangkan RJ memakainya sebagai Procedure.category."),
 ("Tindakan USG kehamilan","Pelaksanaan tindakan","USG di ANC dicatat sebagai Procedure tanpa kode spesifik; ikuti struktur Pelaksanaan tindakan RJ (ICD-9-CM + SNOMED)."),
 ("Komplikasi / penyulit kehamilan","Diagnosis","Sama-sama ICD-10 di Condition; ANC category problem-list-item, RJ encounter-diagnosis — pastikan tidak dikirim ganda."),
 ("Waktu kematian (bila meninggal)","Kondisi saat meninggalkan RS (Encounter)","ANC mencatat waktu kematian (Observation 81956-5); RJ mencatat meninggal <48/>48 jam via dischargeDisposition."),
 ("Episode kehamilan","Status kehamilan","ANC menandai kehamilan via EpisodeOfCare type ANC; RJ (radiologi) via Observation LOINC 82810-3."),
]
for a in ["Hemoglobin","Skrining PPIA HIV","Skrining PPIA Sifilis (RPR)","Skrining PPIA Sifilis (VDRL)","Skrining PPIA Hepatitis B","Gula darah sewaktu","Protein urin","Golongan darah","Rhesus"]:
    RELATED0.append((a,"Hasil pemeriksaan laboratorium","ANC memberi kode LOINC spesifik + kode WHO; RJ memberi aturan umum hasil lab (LOINC, Specimen, DiagnosticReport)." if a=="Hemoglobin" else ""))
for a in ["Gestational sac (GS) diameter","Crown rump length (CRL)","DJJ (USG)","Usia kehamilan (USG)","HPL (USG)","Letak janin (USG)","Biparietal diameter (BPD)","Head circumference (HC)","Abdominal circumference (AC)","Femur length (FL)","Berat janin (USG)"]:
    RELATED0.append((a,"Hasil (bacaan) radiologi","ANC memakai Observation category imaging dengan kode LOINC spesifik & nilai kuantitatif; RJ: bacaan radiologi umum (valueString, derivedFrom ImagingStudy)." if a.startswith("Gestational") else ""))

RELATED=[("ANC",a,"RJ",b,n) for a,b,n in RELATED0]
RELATED+=[("ANC","Episode kehamilan","HIV","Episode perawatan HIV","Pola EpisodeOfCare sama; ANC status active & type 'ANC', HIV status waitlist & type HIV (system http://terminology.kemkes.go.id)."),
 ("RJ","Keluhan penyerta","HIV","Keluhan","RJ: ECL < 404684003 (bebas); HIV: daftar tertutup Lampiran 3; category sama problem-list-item."),("RJ","Keluhan utama","HIV","Keluhan","RJ memakai category chief-complaint (Kemkes); HIV problem-list-item."),
 ("ANC","Riwayat penyakit menular","HIV","Penyakit terkait pasien","ANC: ECL riwayat (SNOMED situation); HIV: daftar tertutup penyakit (Lampiran 5)."),("RJ","Riwayat penyakit pribadi","HIV","Penyakit terkait pasien",""),
 ("ANC","Skrining PPIA HIV","HIV","Rapid HIV 1 dan 2 Ab (identifier)",""),("ANC","Skrining PPIA HIV","HIV","Rapid HIV 1 Ab / HIV 2 Ab",""),("ANC","Skrining PPIA HIV","HIV","Rapid Duo/Combo (HIV + sifilis)",""),
 ("ANC","Skrining PPIA Sifilis (RPR)","HIV","Titer RPR",""),("ANC","Skrining PPIA Sifilis (RPR)","HIV","Rapid sifilis / TPHA",""),("RJ","Laporan pemeriksaan laboratorium","HIV","Laporan rapid serologis HIV single (R1–R3)","Struktur laporan HIV mengikuti RJ; HIV menambah conclusionCode.")]
for n in ["Rapid HIV 1+2 Ab (single)","Rapid HIV 1 dan 2 Ab (identifier)","Rapid HIV 1 Ab / HIV 2 Ab","Rapid Duo/Combo (HIV + sifilis)","PCR DNA/EID HIV kualitatif","PCR DNA/EID HIV kuantitatif (viral load)","PCR RNA HIV kuantitatif — [#/volume]","PCR RNA HIV kuantitatif — [Log #/volume]","PCR RNA HIV kuantitatif — [Units/volume]","Rapid sifilis / TPHA","Titer RPR","RPR / VDRL"]:
    RELATED.append(("RJ","Hasil pemeriksaan laboratorium","HIV",n,"HIV merinci kode LOINC & nilai hasil; RJ memberi aturan umum hasil lab." if n.startswith("Rapid HIV 1+2") else ""))
for n in ["Laporan rapid serologis HIV combo (R1–R3)","Laporan rapid serologis HIV (R1 saja)","Laporan PCR DNA/EID HIV kualitatif","Laporan PCR DNA/RNA HIV kuantitatif","Laporan rapid sifilis / TPHA","Laporan titer RPR","Laporan RPR / VDRL"]:
    RELATED.append(("RJ","Laporan pemeriksaan laboratorium","HIV",n,""))
# ---------- union-find grouping ----------
par={v["id"]:v["id"] for v in ALL}
def f(x):
    while par[x]!=x: par[x]=par[par[x]]; x=par[x]
    return x
def u(a,b): par[f(a)]=f(b)
BYID={v["id"]:v for v in ALL}
reason={}
# copies ↔ source
for v in ANC+HIVL:
    if v.get("copy"):
        src=[r for r in rj.V if r["var"]==v["var"]][0]; u(v["id"],src["id"]); reason.setdefault(v["id"],"copy")
# identical main-code key across different variables
bykey={}
for v in ALL:
    k=key_codes(v)
    if k: bykey.setdefault(k,[]).append(v)
def _s(v): return {(npath(e[0]),e[1]) for e in v["el"]}
for k,vs in bykey.items():
    for i in range(len(vs)):
        for j in range(i+1,len(vs)):
            if vs[i]["title"]!=vs[j]["title"] or _s(vs[i])==_s(vs[j]): u(vs[i]["id"],vs[j]["id"])
# same normalized name across titles
byname={}
for v in ALL: byname.setdefault((nname(v["var"])),[]).append(v)
for n,vs in byname.items():
    for i in range(len(vs)):
        for j in range(i+1,len(vs)):
            a,b=vs[i],vs[j]
            if a["title"]==b["title"]: continue
            ka,kb=key_codes(a),key_codes(b)
            if ka and kb and not (ka&kb): continue   # same name but different concrete codes -> not merged (related instead)
            if not ({x.strip() for x in re.split(r"[+,]",a["res"])} & {x.strip() for x in re.split(r"[+,]",b["res"])}): continue   # disjoint resources -> different concept
            u(a["id"],b["id"])
GLABEL={}; GNOTE={}
for mem,lab,note in SAME:
    vs=[find(t,n) for t,n in mem]
    for x in vs[1:]: u(vs[0]["id"],x["id"])
    GLABEL[vs[0]["id"]]=lab; GNOTE[vs[0]["id"]]=note
groups={}
for v in ALL: groups.setdefault(f(v["id"]),[]).append(v)
G=[]; GID={}
order=sorted(groups.values(),key=lambda vs:min(ALL.index(x) for x in vs))
for i,vs in enumerate(order,1):
    gid=f"K-{i:03d}"
    for x in vs: GID[x["id"]]=gid; x["gid"]=gid
    lab=next((GLABEL[x["id"]] for x in vs if x["id"] in GLABEL),None) or vs[0]["var"]
    note=" ".join(GNOTE[x["id"]] for x in vs if x["id"] in GNOTE)
    G.append(dict(id=gid,label=lab,members=vs,note=note,related=[]))
GBY={g["id"]:g for g in G}
# related links (manual + auto shared code across groups)
def addrel(va,vb,note):
    ga,gb=GBY[va["gid"]],GBY[vb["gid"]]
    if ga is gb: return
    if not any(r[0]==gb["id"] for r in ga["related"]): ga["related"].append((gb["id"],note))
    if not any(r[0]==ga["id"] for r in gb["related"]): gb["related"].append((ga["id"],note))
for t1,a,t2,b,note in RELATED: addrel(find(t1,a),find(t2,b),note)
for n,vs in byname.items():
    for i in range(len(vs)):
        for j in range(i+1,len(vs)):
            if vs[i]["gid"]!=vs[j]["gid"] and vs[i]["title"]!=vs[j]["title"]:
                addrel(vs[i],vs[j],f"Nama variabel sama ('{vs[i]['var']}') tetapi kode konsep berbeda")
codeocc={}
for v in ALL:
    for p,s,c in codes_with_system(v):
        if s and not s.startswith("http://terminology.hl7.org") and c not in ("final","completed"):
            codeocc.setdefault(c,[]).append((v["id"],p))
for c,occ in codeocc.items():
    ids=list(dict.fromkeys(o[0] for o in occ))
    for i in range(len(ids)):
        for j in range(i+1,len(ids)):
            va,vb=BYID[ids[i]],BYID[ids[j]]
            if MAINCODE.match(dict(occ)[va["id"]]) and MAINCODE.match(dict(occ)[vb["id"]]):
                addrel(va,vb,f"Kode {c} dipakai di keduanya")

# ---------- signatures, status & diff ----------
EXCL=re.compile(r"\.(subject|patient|encounter|context|performer|performer\.actor|effectiveDateTime|recorder|author|source|authored)$")
def nval(x):
    if concrete(x) or x.startswith("ECL") or x.startswith("http"): return x
    return "~"
ANCSYS={"http://fhir.org/guides/who/anc-cds/CodeSystem/anc-custom-codes","http://terminology.kemkes.go.id/CodeSystem/anc-custom-codes"}
def _skip_prefixes(v):
    return {e[0].lstrip("*").rsplit(".",1)[0] for e in v["el"] if e[0].endswith(".system") and e[1] in ANCSYS}
def _keep(v):
    sk=_skip_prefixes(v)
    return [e for e in v["el"] if not EXCL.search(npath(e[0])) and e[0].lstrip("*").rsplit(".",1)[0] not in sk]
def sig(v):
    return {(npath(e[0]),nval(e[1])) for e in _keep(v)}
def paths(v): return {npath(e[0]) for e in _keep(v)}
def _res(v): return {x.strip() for x in re.split(r"[+,]",v["res"])}
def diff(a,b):
    """returns (conflicts, complements)"""
    sa,sb=sig(a),sig(b); con=[]; com=[]
    ra,rb=_res(a),_res(b)
    if ra!=rb:
        (com if (ra<=rb or rb<=ra) else con).append(f"Resource: {a['title']} {a['res']} ≠ {b['title']} {b['res']}")
    pa,pb=paths(a),paths(b)
    for p in sorted(pa&pb):
        va={x[1] for x in sa if x[0]==p}; vb={x[1] for x in sb if x[0]==p}
        if va!=vb:
            oa_,ob_=sorted(va-vb-{"~"}),sorted(vb-va-{"~"}); parts=[]
            if not oa_ and not ob_: continue
            if oa_: parts.append(f"hanya {a['title']} ({a['id']}): "+" | ".join(oa_)[:160])
            if ob_: parts.append(f"hanya {b['title']} ({b['id']}): "+" | ".join(ob_)[:160])
            # value-set where one side only adds options (superset) = complement, else conflict
            (com if (not oa_ or not ob_) and len(va|vb)>2 else con).append(f"{p} — "+"; ".join(parts))
    oa=sorted(pa-pb); ob=sorted(pb-pa)
    if oa: com.append(f"Elemen hanya di {a['title']} ({a['id']}): "+", ".join(oa[:8])+(" …" if len(oa)>8 else ""))
    if ob: com.append(f"Elemen hanya di {b['title']} ({b['id']}): "+", ".join(ob[:8])+(" …" if len(ob)>8 else ""))
    return con,com
for g in G:
    ms=g["members"]; titles=[m["title"] for m in ms]
    if len(ms)==1: g["status"]="Unik"; g["diff"]=[]; continue
    base=next((x for x in ms if not x.get("copy")),ms[0]); diffs=[]
    for m in [x for x in ms if x is not base]:
        con,com=diff(base,m)
        if con or com: diffs.append((base["id"],m["id"],[("K",x) for x in con]+[("L",x) for x in com]))
    g["diff"]=diffs
    anycopy=any(m.get("copy") for m in ms)
    shared=set.intersection(*[set(key_codes(m)) for m in ms]) if all(key_codes(m) for m in ms) else set()
    anycon=any(t=="K" for _,_,d in diffs for t,_ in d)
    manual=any(m["id"] in GLABEL for m in ms)
    if not diffs: g["status"]="Identik (disalin)" if anycopy else "Identik"
    elif shared and not anycon: g["status"]="Saling melengkapi"
    elif shared: g["status"]="Kode sama, isi beda"
    elif not anycon and not manual: g["status"]="Saling melengkapi"
    else: g["status"]="Maksud sama, kode/struktur beda"
    if len(set(titles))==1 and g["status"]!="Unik": g["note"]=(g["note"]+" " if g["note"] else "")+"Beberapa variabel dalam satu judul memakai kode utama yang sama."
# per-element code occurrence: other variables using the same concrete code
def also(v):
    res={}
    for p,s,c in codes_with_system(v):
        if s and s.startswith("http://terminology.hl7.org"): continue
        oth=[o for o in dict.fromkeys(x[0] for x in codeocc.get(c,[])) if o!=v["id"]]
        if oth: res[(p,c)]=oth
    return res
for v in ALL: v["also"]=also(v)

# consolidated dedup rows
for g in G:
    rows={}
    for m in g["members"]:
        for e in m["el"]:
            k=(npath(e[0]),e[1])
            if k not in rows: rows[k]=dict(path=e[0].replace("[i]","[i]"),val=e[1],ket=e[2],lst=e[3] if len(e)>3 else None,ids=[])
            if m["id"] not in rows[k]["ids"]: rows[k]["ids"].append(m["id"])
            if not rows[k]["ket"] and e[2]: rows[k]["ket"]=e[2]
    g["rows"]=list(rows.values())

import json as _j
HL_=_j.load(open(_D("hiv_lists.json")))
LISTS={"icd":dict(title="Kode ICD-10 komplikasi/penyulit kehamilan (Lampiran 2 ANC)",cols=["code","display","Deskripsi","Trimester"],rows=[list(r) for r in data3.ICD]),
 "kfa":dict(title="Struktur kamus KFA (Lampiran RME Rawat Jalan + playbook)",cols=["Tag","Deskripsi","Format kode","Tata cara penamaan","Contoh"],rows=[
   ["BZA","Bahan Zat Aktif","91xxxxxx","Nama molekul kimia","Paracetamol"],["POV","Produk Obat Virtual","92xxxxxx","Zat aktif + kekuatan + satuan + bentuk sediaan","Paracetamol 500 mg Tablet"],
   ["POA","Produk Obat Aktual","93xxxxxx","Zat aktif + kekuatan + satuan + sediaan + (merek dagang)","Paracetamol 500 mg Tablet (Panadol)"],["POAK","Produk Obat Aktual dalam Kemasan","94xxxxxx","Produk aktual per kemasan (dari playbook)","—"]]),
 "resep":dict(title="Matriks skenario peresepan & pengeluaran obat (Lampiran RME Rawat Jalan)",cols=["Use case","Medication.code MR","Medication.ingredient MR","Medication.code MD","Medication.ingredient MD","Valid?"],rows=[
   ["Obat pakem tunggal (NC)","93xxx","-","93xxx","-","Valid"],["Obat pakem tunggal (NC)","92xxx","-","93xxx","-","Valid (93 sebaiknya turunan dari 92 di resep)"],["Obat pakem tunggal (NC)","91xxx","-","93xxx","-","Invalid"],
   ["Racikan non-d.t.d","-","93xxx / 92xxx; numerator 10 tab, denominator 30 kap","-","93xxx; numerator 10 tab, denominator 30 kap","Valid"],
   ["Racikan d.t.d (tanpa sisa)","-","91xxx; 125 mg / 1 kap","-","93xxx; 5 tab / 20 kap","Valid"],
   ["Narkotika (racikan)","-","91xxx; 3 mg / 1 tab","-","93xxx; 7,5 tab / 25 kapsul","Valid (tanpa pembulatan)"],
   ["Non-narkotika (racikan)","-","91xxx; 125 mg / 1 tab","-","93xxx; 8 tab / 30 kapsul","Valid (dibulatkan ke atas, dipakai 7,5)"],
   ["Obat minum (NC)","93xxx / 92xxx","91xxx; 120 mg / 5 mL","93xxx","91xxx; 120 mg / 5 mL","Valid (bila bersisa perlu catatan dokter)"],
   ["Obat suntik (NC)","93xxx / 92xxx","91xxx; 100 [U] / 1 mL","93xxx","91xxx; cartridge / mL","Valid (bila bersisa perlu catatan dokter)"]])}
for k,v in HL_.items(): LISTS[k]=v
for k,v in AUTOLISTS.items(): LISTS[k]=v
LISTS["icd"]["title"]="Kode ICD-10 komplikasi/penyulit kehamilan (Lampiran 2 ANC)"

# ---------- collapse answer options into lists ("sistem lampiran") ----------
LREG={}   # tuple(rows) -> list id
LUSERS={}
def _reglist(rows,title,plain=False):
    key=tuple(tuple(r) for r in rows)
    if key not in LREG:
        lid=f"P-{len(LREG)+1:03d}"; LREG[key]=lid
        LISTS[lid]=dict(title=title,cols=["system","nilai" if plain else "code","display","Keterangan / pilihan yang divisualisasikan"],rows=[list(r) for r in rows])
    return LREG[key]
def collapse(v):
    el=v["el"]; P=[e[0].lstrip("*") for e in el]
    cnt={}
    for p in P:
        if p.endswith(".code"): cnt[p[:-5]]=cnt.get(p[:-5],0)+1
    groups={k for k,n in cnt.items() if n>=2}
    plain={}
    for e,p in zip(el,P):
        if not p.endswith((".system",".code",".display")) and len(e)<4: plain.setdefault(p,[]).append(e)
    plain={p for p,es in plain.items() if len(es)>=2 and all(concrete(x[1]) or x[1].isdigit() for x in es) and len({x[1] for x in es})>=2}
    out=[]; done=set(); i=0
    while i<len(el):
        e,p=el[i],P[i]
        pre=p.rsplit(".",1)[0] if p.endswith((".system",".code",".display")) else None
        if pre in groups:
            if pre in done: i+=1; continue
            rows=[]; sysv=""; star=False
            for e2,p2 in zip(el,P):
                if p2.rsplit(".",1)[0]!=pre or not p2.endswith((".system",".code",".display")): continue
                star=star or e2[0].startswith("*")
                if p2.endswith(".system"): sysv=e2[1]
                elif p2.endswith(".code"): rows.append([sysv,e2[1],"",e2[2]])
                elif rows:
                    rows[-1][2]=e2[1]
                    if e2[2]: rows[-1][3]=(rows[-1][3]+"; " if rows[-1][3] else "")+e2[2]
            lid=_reglist(rows,f"{pre} — {v['var']}")
            LUSERS.setdefault(lid,[]).append(v["id"])
            out.append((("*" if star else "")+pre,"(pilih dari daftar)",f"{len(rows)} pilihan",lid)); done.add(pre)
        elif p in plain:
            if p in done: i+=1; continue
            es=[x for x,pp in zip(el,P) if pp==p]
            rows=[["-",x[1],"",x[2]] for x in es]
            lid=_reglist(rows,f"{p} — {v['var']}",True); LUSERS.setdefault(lid,[]).append(v["id"])
            out.append((es[0][0],"(pilih dari daftar)",f"{len(rows)} pilihan",lid)); done.add(p)
        else:
            out.append(e)
            if len(e)>3: LUSERS.setdefault(e[3],[]).append(v["id"])
        i+=1
    return out
for v in ALL: v["elc"]=collapse(v)
for k in LISTS: LISTS[k]["users"]=list(dict.fromkeys(LUSERS.get(k,[])))
# consolidated rows from collapsed elements
for g in G:
    rows={}
    for m in g["members"]:
        for e in m["elc"]:
            k=(npath(e[0]),e[1] if len(e)<4 else "LIST:"+e[3])
            if k not in rows: rows[k]=dict(path=e[0],val=e[1],ket=e[2],lst=e[3] if len(e)>3 else None,ids=[])
            if m["id"] not in rows[k]["ids"]: rows[k]["ids"].append(m["id"])
    g["rows"]=list(rows.values())
# code -> vars (for list tables)
CODEVARS={c:list(dict.fromkeys(o[0] for o in occ)) for c,occ in codeocc.items()}

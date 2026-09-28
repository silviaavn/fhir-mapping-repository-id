# HIV (Fase 1) — Playbook Modul HIV (PDF di Google Drive, header "versi 1.3, 15 Agustus 2024")
import json
from rj import co, opts, LN, SN, UC, HL, OC, KM, PAT, ENC, PR
LISTS=json.load(open('/home/claude/hiv/lists.json'))
V=[]
def add(tahap,kel,var,res,el,cat="",frek=""): V.append(dict(tahap=tahap,kel=kel,var=var,res=res,el=el,cat=cat,frek=frek))
V3=HL+"v3-ObservationInterpretation"; CT=KM+"/CodeSystem/clinical-term"; EX=KM+"/CodeSystem/examination"; Q23="https://fhir.kemkes.go.id/Questionnaire/Q0023"
OBSM=[("*Observation.subject",PAT,""),("*Observation.encounter",ENC,""),("Observation.effectiveDateTime","(DateTime)",""),("*Observation.performer[i]",PR,"")]
def obs(tahap,kel,var,cat,codes,value,extra=(),note="",frek="",res="Observation",status="final"):
    el=[("*Observation.status",status,"")]+co("Observation.category.coding",OC,cat,{"survey":"Survey","exam":"Exam","laboratory":"Laboratory","social-history":"Social History"}[cat])
    for i,(s,c,d) in enumerate(codes): el+=[("*"+p,v,k) for p,v,k in co(f"Observation.code.coding[{i}]" if len(codes)>1 else "Observation.code.coding",s,c,d)]
    el+=OBSM+list(value)+list(extra)
    add(tahap,kel,var,res,el,note,frek)
def L(path,listkey,label): return [(path,"(pilih dari daftar)",label,listkey)]
def qr(linkid,text,ans):
    return [("*QuestionnaireResponse.item.item.linkId",linkid,text),("QuestionnaireResponse.item.item.text",text,""),("*QuestionnaireResponse.item.item.answer."+ans[0],ans[1],ans[2] if len(ans)>2 else "")]

T="1. Pendaftaran pasien"
add(T,"Identitas pasien","Nomor SATUSEHAT (IHS) pasien","Patient",[("Patient.identifier[i]","Nomor IHS pasien","GET ke Master Patient Index (MPI)"),
 ("Patient.identifier[i]","NIK ibu kandung","Khusus bayi baru lahir"),("Patient.contact.name","Nama ibu kandung","Khusus bayi baru lahir")],"Detail pencarian pasien di Juknis SATSET.","Sekali per pasien")
T="2. Pendaftaran kunjungan"; K="Kunjungan"
ADM=[(CT,"EHA000002","Datang sendiri","Datang sendiri"),(KM,"TK000031","From outpatient department","Rujukan poli"),(CT,"EHA000001","Kader/ Komunitas","Kader kesehatan"),(KM,"TK000033","LSM","LSM"),(SN,"257622000","Healthcare facility","UPK lain")]
el=[]
for s,c,d,k in ADM: el+=[("Encounter.hospitalization.admitSource.coding.system",s,""),("Encounter.hospitalization.admitSource.coding.code",c,k),("Encounter.hospitalization.admitSource.coding.display",d,"")]
el+=[("Encounter.reasonCode.coding.system",SN,"Alasan kunjungan"),("Encounter.reasonCode.coding.code","24081000087105","Tes HIV"),("Encounter.reasonCode.coding.display","Human immunodeficiency virus nurse practitioner service",""),
     ("Encounter.reasonCode.coding.system",KM,""),("Encounter.reasonCode.coding.code","TK000033","Tes IMS"),("Encounter.reasonCode.coding.display","Tes IMS","")]
add(T,K,"Kunjungan HIV (asal rujukan & alasan kunjungan)","Encounter",[("*Encounter.status","Status kunjungan",""),("*Encounter.class","Kelas kunjungan",""),("*Encounter.subject",PAT,""),("*Encounter.participant[i].type / individual",PR,""),("*Encounter.period","Mulai–selesai kunjungan",""),("*Encounter.location[i]","Location/{ID}",""),("*Encounter.serviceProvider","Organization/{ID faskes}",""),("Encounter.episodeOfCare[i]","EpisodeOfCare/{ID episode HIV}","")]+el,
 "Elemen dasar Encounter mengikuti modul Rawat Jalan. Inkonsistensi di sumber: kode Kemkes TK000033 dipakai untuk dua arti berbeda ('LSM' pada asal rujukan dan 'Tes IMS' pada alasan kunjungan). Judul tabel menyebut 'Alasan Rujukan', padahal variabelnya Asal Rujukan.","Setiap kunjungan")
obs(T,K,"Pendidikan","social-history",[(LN,"82589-3","Highest level of education")],L("Observation.valueCodeableConcept.coding","pendidikan","Lampiran 1"),note="Pendidikan terakhir saat tes HIV.")
obs(T,K,"Pekerjaan","social-history",[(LN,"85658-3","Occupation [Type]")],L("Observation.valueCodeableConcept.coding","pekerjaan","Lampiran 2"),note="Pekerjaan terakhir saat tes HIV.")
T="3. Memulai episode perawatan HIV"
add(T,"Episode HIV","Episode perawatan HIV","EpisodeOfCare",[("EpisodeOfCare.identifier.system","http://sys-ids.kemkes.go.id/episode-of-care/{orgID}","ID terduga HIV"),("EpisodeOfCare.identifier.value","(String)","Kode ID kasus terduga HIV"),
 ("*EpisodeOfCare.status","waitlist","Saat pasien dinyatakan terduga HIV"),("EpisodeOfCare.statusHistory[i].status / period","Riwayat status",""),
 ("*EpisodeOfCare.type.coding.system",KM,""),("*EpisodeOfCare.type.coding.code","HIV",""),("*EpisodeOfCare.type.coding.display","Human Immunodeficiency Virus",""),
 ("*EpisodeOfCare.patient",PAT,""),("*EpisodeOfCare.managingOrganization","Organization/{ID faskes}",""),("*EpisodeOfCare.period.start","(Date)","")],
 "POST sekali saat hasil serologis HIV positif (terduga HIV), status 'waitlist'; balikan berisi ID episode dan nomor surveilans (suspect-id). Kunjungan berikutnya: GET dengan patient + type + status waitlist. Sumber menulis 'terduga TB' (salin dari modul TB).","Sekali per episode")
T="4. Anamnesis & pemeriksaan fisik"; K="Anamnesis"
add(T,K,"Keluhan","Condition",co("Condition.category.coding",HL+"condition-category","problem-list-item","Problem List Item")+[("*Condition.code.coding","(pilih dari daftar)","Lampiran 3","keluhan"),("*Condition.subject",PAT,""),("*Condition.encounter",ENC,"")],"Label di tabel 4.1 'Keluhan Utama'.")
obs(T,K,"Status kehamilan","survey",[(LN,"82810-3","Pregnancy status")],opts("Observation.valueCodeableConcept.coding",SN,[("77386006","Pregnancy","Ya"),("60001007","Not pregnant","Tidak")]))
obs(T,K,"Usia kehamilan","survey",[(LN,"32418-6","Obstetric trimester Stated"),(KM+"/CodeSystem/anc-custom-codes","ANC.SS.DE13","Trimester ke")],[("Observation.valueInteger","1","Trimester 1"),("Observation.valueInteger","2","Trimester 2"),("Observation.valueInteger","3","Trimester 3")],
 note="Label variabel 'Usia kehamilan', tapi kode & nilainya adalah trimester (sama dengan ANC 'Trimester ke-').")
K="Kajian tingkat risiko"
add(T,K,"Kajian tingkat risiko (kuesioner)","QuestionnaireResponse",[("*QuestionnaireResponse.status","completed",""),("QuestionnaireResponse.questionnaire",Q23,""),("QuestionnaireResponse.item.linkId","1","Kajian Tingkat Risiko (grup)"),
 ("*QuestionnaireResponse.subject",PAT,""),("*QuestionnaireResponse.encounter",ENC,""),("*QuestionnaireResponse.author",PR,""),("*QuestionnaireResponse.source",PAT,"")],
 "Setiap butir risiko dikirim sebagai Observation/Condition, lalu direferensikan dari item kuesioner (answer.valueReference).")
obs(T,K,"Kelompok populasi","survey",[(KM,"TK000034","Kelompok Populasi")],[("Observation.component.code.coding","(pilih dari daftar)","Lampiran 4","populasi"),("Observation.component.valueBoolean","true / false","")],
 extra=qr("1.1","Kelompok Populasi",("valueReference","Observation/{ID}","")),note="Sumber menukar system & code (system 'TK000034', code 'http://terminology.kemkes.go.id'); di sini sudah dibalik. Lampiran 4 juga menukar kolom code/display untuk kode Kemkes TK000035–TK000039.",res="Observation + QuestionnaireResponse")
for lid,v,s,c,d,nt in [("1.2","Hubungan seks vaginal berisiko",KM,"TK000053","Hubungan Seks Vaginal Beresiko",""),("1.3","Anal seks berisiko",KM,"TK000054","Anal Seks Beresiko",""),
 ("1.4","Bergantian peralatan suntik",SN,"228395002","Shares drug injecting equipment",""),("1.5","Transfusi darah",SN,"161664006","History of blood transfusion",""),
 ("1.6","Transmisi ibu ke anak",SN,"1290740005","Vertical transmission",""),("1.7","Periode jendela",SN,"1290194006","Seroconversion","Di sumber, answer.valueReference 1.7 tertulis 'variabel Kelompok Populasi' (salin-tempel).")]:
    obs(T,K,v,"survey",[(s,c,d)],[("Observation.valueBoolean","true / false","Ya / Tidak")],extra=qr(lid,v,("valueReference","Observation/{ID}","")),note=nt,res="Observation + QuestionnaireResponse")
add(T,K,"Penyakit terkait pasien","Condition + QuestionnaireResponse",co("Condition.category.coding",HL+"condition-category","problem-list-item","Problem List Item")+[("*Condition.code.coding","(pilih dari daftar)","Lampiran 5","penyakit"),("*Condition.subject",PAT,""),("*Condition.encounter",ENC,"")]+qr("1.8","Penyakit Terkait Pasien",("valueReference","Condition/{ID}","")),
 "Sumber menulis category.system observation-category untuk Condition; di sini dinormalisasi ke condition-category.")
add(T,K,"Risiko lainnya","QuestionnaireResponse",qr("1.9","Lainnya",("valueBoolean","true / false","Ada risiko lain?"))+[("QuestionnaireResponse.item.item.answer.item.linkId","1.9.1","Risiko Lainnya"),("QuestionnaireResponse.item.item.answer.item.answer.valueString","(String)","Dikirim jika 1.9 = true")])
K="Tanda klinis & pemeriksaan fisik"
add(T,K,"Tanda klinis IMS","QuestionnaireResponse + Condition",[("QuestionnaireResponse.item.linkId","2","Tanda Klinis IMS dan Pemeriksaan Fisik (grup)")]+qr("2.1","Tanda Klinis IMS",("valueBoolean","true / false","Ya / Tidak"))+
 co("Condition.category.coding",HL+"condition-category","problem-list-item","Problem List Item")+[("*Condition.code.coding","(pilih dari daftar)","Lampiran 6","tandaklinis"),("*Condition.subject",PAT,""),("*Condition.encounter",ENC,""),
 ("QuestionnaireResponse.item.item.answer.item.linkId","2.1.1","Jika ya, Tanda Klinis IMS"),("QuestionnaireResponse.item.item.answer.item.answer.valueReference","Condition/{ID}","")],"Sumber menulis category.system observation-category untuk Condition; dinormalisasi.")
obs(T,K,"Pemeriksaan fisik IMS","exam",[(LN,"29544-4","Physical findings")],L("Observation.valueCodeableConcept.coding","fisik","Lampiran 7"),extra=qr("2.2","Pemeriksaan Fisik",("valueReference","Observation/{ID}","")),res="Observation + QuestionnaireResponse")

T="5. Pemeriksaan penunjang"; K="Permintaan & spesimen"
add(T,K,"Permintaan pemeriksaan laboratorium HIV/IMS","ServiceRequest",[("*ServiceRequest.status","(status)",""),("*ServiceRequest.intent","(intent)",""),
 ("ServiceRequest.reasonCode.coding","(pilih dari daftar)","Lampiran 8 — alasan pemeriksaan","alasanperiksa"),("ServiceRequest.reasonCode.text","(String)",""),
 ("ServiceRequest.category.coding.system",SN,""),("ServiceRequest.category.coding.code","108252007",""),("ServiceRequest.category.coding.display","Laboratory procedure",""),
 ("*ServiceRequest.code.coding","(pilih dari daftar)","Lampiran 9 — jenis pemeriksaan","jenisperiksa"),("*ServiceRequest.subject",PAT,""),("*ServiceRequest.encounter",ENC,""),("*ServiceRequest.requester",PR,""),("*ServiceRequest.performer","Organization/{ID lab}","")],
 "Hasil pemeriksaan lanjutan dapat dibuat ServiceRequest baru dengan reasonReference ke hasil sebelumnya.")
add(T,K,"Spesimen HIV/IMS","Specimen",[("*Specimen.status","(pilih dari daftar)","Lampiran 11","kondisispesimen"),("*Specimen.type.coding","(pilih dari daftar)","Lampiran 10","spesimen"),("*Specimen.subject",PAT,""),
 ("Specimen.collection.collectedDateTime","(DateTime)","Tanggal & jam pengambilan"),("Specimen.condition.coding","(lihat Lampiran 11)","Kondisi spesimen saat diterima"),("Specimen.processing.timeDateTime","(DateTime)","Tanggal & jam pemeriksaan lab")],
 "Tabel ringkasan menulis 'Specimen.collectedDateTime' (seharusnya collection.collectedDateTime).")
K="Hasil pemeriksaan"
DAR=[("Observation.dataAbsentReason.coding.system",LN,""),("Observation.dataAbsentReason.coding.code","LA15841-2",""),("Observation.dataAbsentReason.coding.display","Invalid",""),
     ("Observation.dataAbsentReason.coding.system",HL+"data-absent-reason",""),("Observation.dataAbsentReason.coding.code","error","Hanya pemeriksaan mesin (mis. PCR)"),("Observation.dataAbsentReason.coding.display","Error",""),
     ("Observation.dataAbsentReason.coding.system",KM+"/CodeSystem/data-absent-reason",""),("Observation.dataAbsentReason.coding.code","OD000001","Hanya pemeriksaan mesin"),("Observation.dataAbsentReason.coding.display","Tidak ada hasil",""),
     ("Observation.issued","(DateTime)","Tanggal & jam hasil keluar"),("*Observation.performer","Practitioner/{ID}","Pemeriksa & dokter PJ lab")]
DARNOTE="Jika dataAbsentReason dipakai (Invalid/Error/Tidak ada hasil), Observation.status = cancelled."
def obsopt(var,codes,value,interp,note=""):
    el=[("*Observation.status","final / cancelled","")]+co("Observation.category.coding",OC,"laboratory","Laboratory")+[("*Observation.code.coding.system",LN,"")]
    for c,d in codes: el+=[("*Observation.code.coding.code",c,"Pilihan kode pemeriksaan"),("*Observation.code.coding.display",d,"")]
    el+=[("*Observation.subject",PAT,""),("*Observation.encounter",ENC,""),("Observation.specimen","Specimen/{ID}","")]+value
    if interp: el+=opts("Observation.interpretation.coding",V3,interp)
    add(T,K,var,"Observation",el+DAR,(note+" " if note else "")+DARNOTE)
RRNR=[("RR","Reactive"),("NR","Nonreactive")]; PN=[("POS","Positive"),("NEG","Negative")]
obsopt("Rapid HIV 1+2 Ab (single)",[("7918-6","HIV 1+2 Ab [Presence] in Serum"),("31201-7","HIV 1+2 Ab [Presence] in Serum or Plasma by Immunoassay"),("80387-4","HIV 1+2 Ab [Presence] in Serum, Plasma or Blood by Rapid immunoassay")],
 opts("Observation.valueCodeableConcept.coding",LN,[("LA18332-9","HIV Reactive (Undifferentiated)"),("LA15256-3","Nonreactive")]),RRNR,"R1/R2/R3 dikirim sebagai Observation terpisah; kesimpulan mengikuti algoritma di laporan (DiagnosticReport).")
obsopt("Rapid HIV 1 dan 2 Ab (identifier)",[("95524-5","HIV 1 and 2 Ab [Identifier] in Serum or Plasma by Immunoassay"),("69668-2","HIV 1 and 2 Ab [Identifier] in Serum or Plasma by Rapid immunoassay")],
 opts("Observation.valueCodeableConcept.coding",LN,[("LA18332-9","HIV Reactive (Undifferentiated)"),("LA18330-3","HIV-1 reactive"),("LA18331-1","HIV-2 reactive"),("LA15256-3","Nonreactive")]),RRNR)
obsopt("Rapid HIV 1 Ab / HIV 2 Ab",[("7917-8","HIV 1 Ab [Presence] in Serum"),("7919-4","HIV 2 Ab [Presence] in Serum")],opts("Observation.valueCodeableConcept.coding",LN,[("LA15255-5","Reactive"),("LA15256-3","Nonreactive")]),RRNR)
add(T,K,"Rapid Duo/Combo (HIV + sifilis)","Observation",[("*Observation.status","final / cancelled","")]+co("Observation.category.coding",OC,"laboratory","Laboratory")+
 [("*Observation.component.code","Kode pemeriksaan HIV & sifilis","Mengikuti tabel rapid HIV dan rapid sifilis"),("Observation.component.valueCodeableConcept","Hasil per komponen",""),("Observation.component.interpretation","Interpretasi per komponen",""),
  ("*Observation.subject",PAT,""),("*Observation.encounter",ENC,"")]+DAR,"1 payload dengan array Observation.component (HIV + sifilis). Biasanya untuk ibu hamil & triple eliminasi. "+DARNOTE)
obsopt("PCR DNA/EID HIV kualitatif",[("44871-2","HIV 1 proviral DNA [Presence] in Blood by NAA with probe detection"),("25841-8","HIV 2 proviral DNA [Presence] in Blood by NAA with probe detection")],
 opts("Observation.valueCodeableConcept.coding",LN,[("LA11882-0","Detected"),("LA11883-8","Not detected")]),PN,"Tabel ringkasan menyebut Observation.component.valueCodeableConcept, tabel terminologi memakai valueCodeableConcept.")
Q=lambda u:[("Observation.valueQuantity.value","(Decimal)",""),("Observation.valueQuantity.unit",u,""),("Observation.valueQuantity.system",UC,""),("Observation.valueQuantity.code",u,"")]
obsopt("PCR DNA/EID HIV kuantitatif (viral load)",[("74854-1","HIV 1 proviral DNA [#/volume] (viral load) in Blood by NAA with probe detection"),("25841-8","HIV 2 proviral DNA [Presence] in Blood by NAA with probe detection")],Q("{copies}/mL"),PN,
 "Kode kedua (25841-8) adalah pemeriksaan kualitatif ([Presence]) tetapi dipakai di tabel kuantitatif — kemungkinan salah tempel.")
obsopt("PCR RNA HIV kuantitatif — [#/volume]",[("59419-2","HIV 1 RNA [#/volume] (viral load) in Plasma by Probe with signal amplification"),("86548-5","HIV 2 RNA [#/volume] (viral load) in Plasma by NAA with probe detection")],Q("{copies}/mL"),PN)
obsopt("PCR RNA HIV kuantitatif — [Log #/volume]",[("29539-4","HIV 1 RNA [Log #/volume] (viral load) in Plasma by Probe with signal amplification")],Q("{Log_copies}/mL"),PN)
obsopt("PCR RNA HIV kuantitatif — [Units/volume]",[("62469-2","HIV 1 RNA [Units/volume] (viral load) in Serum or Plasma by NAA with probe detection"),("69354-9","HIV 2 RNA [Units/volume] (viral load) in Serum or Plasma by NAA with probe detection")],Q("[IU]/mL"),PN)
obsopt("Rapid sifilis / TPHA",[("8041-6","Treponema pallidum Ab [Presence] in Serum by Hemagglutination"),("22587-0","Treponema pallidum Ab [Presence] in Serum"),("5393-4","Treponema pallidum Ab [Presence] in Serum by Immunofluorescence")],
 [("Observation.valueCodeableConcept.coding.system",LN,""),("Observation.valueCodeableConcept.coding.code","LA15255-5","Reaktif"),("Observation.valueCodeableConcept.coding.display","Reactive",""),("Observation.valueCodeableConcept.coding.code","LA15256-3","Non reaktif"),("Observation.valueCodeableConcept.coding.display","Non-Reactive","")],None)
R=lambda s:[(f"Observation.valueRatio.{s}.value","(Decimal)",""),(f"Observation.valueRatio.{s}.unit","{titer}",""),(f"Observation.valueRatio.{s}.system",UC,""),(f"Observation.valueRatio.{s}.code","{titer}","")]
obsopt("Titer RPR",[("31147-2","Reagin Ab [Titer] in Serum by RPR")],R("numerator")+R("denominator"),PN,"Dikirim jika rapid sifilis/TPHA reaktif.")
obsopt("RPR / VDRL",[("20507-0","Reagin Ab [Presence] in Serum by RPR"),("5292-8","Reagin Ab [Presence] in Serum by VDRL")],
 [("Observation.valueCodeableConcept.coding.system",LN,""),("Observation.valueCodeableConcept.coding.code","LA15255-5","Reaktif"),("Observation.valueCodeableConcept.coding.display","Reactive",""),("Observation.valueCodeableConcept.coding.code","LA15256-3","Non reaktif"),("Observation.valueCodeableConcept.coding.display","Non-Reactive","")],None)
K="Laporan pemeriksaan"
DRC=co("DiagnosticReport.category.coding",HL+"v2-0074","LAB","Laboratory")
DRM=[("*DiagnosticReport.status","(status)",""),("*DiagnosticReport.subject",PAT,""),("*DiagnosticReport.encounter",ENC,""),("*DiagnosticReport.performer","Practitioner / Organization",""),("*DiagnosticReport.basedOn","ServiceRequest/{ID}",""),("*DiagnosticReport.result","Observation/{ID}","")]
NPI=opts("DiagnosticReport.conclusionCode.coding",LN,[("LA6577-6","Negative","Negatif"),("LA6576-8","Positive","Positif"),("LA9663-1","Inconclusive","Inkonklusif")])
def dr(var,code,concl,note=""): add(T,K,var,"DiagnosticReport",DRM[:1]+DRC+code+concl+DRM[1:],note)
dr("Laporan rapid serologis HIV single (R1–R3)",co("*DiagnosticReport.code.coding",EX,"X099419","Pemeriksaan HIV Diagnostik"),NPI+[("DiagnosticReport.conclusion","(algoritma R1–R3)","Lihat tabel algoritma","algoritma")])
dr("Laporan rapid serologis HIV combo (R1–R3)",co("*DiagnosticReport.code.coding",EX,"X099420","Pemeriksaan HIV + Sifilis"),[("DiagnosticReport.conclusionCode.text","Hasil Pemeriksaan HIV","")]+NPI+[("DiagnosticReport.conclusionCode.text","Hasil Pemeriksaan Sifilis","")]+
   opts("DiagnosticReport.conclusionCode.coding",LN,[("LA15255-5","Reactive","Reaktif"),("LA15256-3","Nonreactive","Nonreaktif")]))
dr("Laporan rapid serologis HIV (R1 saja)",[("*DiagnosticReport.code.coding","Sama dengan kode Observation rapid HIV","")],opts("DiagnosticReport.conclusionCode.coding",LN,[("LA6577-6","Negative","Negatif")]),"Dipakai bila R1 non-reaktif sehingga tidak ada pemeriksaan ulang.")
dr("Laporan PCR DNA/EID HIV kualitatif",[("*DiagnosticReport.code.coding.system",LN,""),("*DiagnosticReport.code.coding.code","44871-2",""),("*DiagnosticReport.code.coding.display","HIV 1 proviral DNA [Presence] in Blood by NAA with probe detection",""),("*DiagnosticReport.code.coding.code","25841-8",""),("*DiagnosticReport.code.coding.display","HIV 2 proviral DNA [Presence] in Blood by NAA with probe detection","")],
   opts("DiagnosticReport.conclusionCode.coding",LN,[("LA11882-0","Detected","DETECTED"),("LA11883-8","Not detected","NOT DETECTED")]))
dr("Laporan PCR DNA/RNA HIV kuantitatif",[("*DiagnosticReport.code.coding","Kode PCR kuantitatif / viral load","Sumber merujuk 'lampiran 12' yang tidak ada di dokumen (lihat Lampiran 9)")],opts("DiagnosticReport.conclusionCode.coding",V3,[("POS","Positive"),("NEG","Negative")]))
dr("Laporan rapid sifilis / TPHA",[("*DiagnosticReport.code.coding.system",LN,"")]+[x for c,d in [("8041-6","Treponema pallidum Ab [Presence] in Serum by Hemagglutination"),("22587-0","Treponema pallidum Ab [Presence] in Serum"),("5393-4","Treponema pallidum Ab [Presence] in Serum by Immunofluorescence")] for x in [("*DiagnosticReport.code.coding.code",c,""),("*DiagnosticReport.code.coding.display",d,"")]],
   opts("DiagnosticReport.conclusionCode.coding",LN,[("LA15255-5","Reactive","Reaktif"),("LA15256-3","Non-Reactive","Non reaktif")]))
dr("Laporan titer RPR",co("*DiagnosticReport.code.coding",LN,"31147-2","Reagin Ab [Titer] in Serum by RPR"),opts("DiagnosticReport.conclusionCode.coding",V3,[("POS","Positive"),("NEG","Negative")]))
dr("Laporan RPR / VDRL",[("*DiagnosticReport.code.coding.system",LN,""),("*DiagnosticReport.code.coding.code","20507-0",""),("*DiagnosticReport.code.coding.display","Reagin Ab [Presence] in Serum by RPR",""),("*DiagnosticReport.code.coding.code","5292-8",""),("*DiagnosticReport.code.coding.display","Reagin Ab [Presence] in Serum by VDRL","")],
   opts("DiagnosticReport.conclusionCode.coding",LN,[("LA15255-5","Reactive","Reaktif"),("LA15256-3","Non-Reactive","Non reaktif")]))
# placeholders for steps copied from RJ (filled in model)
COPY={"6. Diagnosis":["Diagnosis"],"7. Rencana tindak lanjut":["Rencana tindak lanjut"],"8. Kondisi saat meninggalkan faskes":["Kondisi saat meninggalkan RS (Condition)","Kondisi saat meninggalkan RS (Encounter)"],"9. Cara keluar dari faskes":["Cara keluar dari RS"]}
T="10. Pembaruan data kunjungan"
add(T,"Update Encounter","Kunjungan selesai","Encounter",[("*Encounter.status","finished",""),("*Encounter.period.end","(DateTime)",""),("*Encounter.diagnosis[i].condition","Condition/{ID}",""),("*Encounter.hospitalization.dischargeDisposition","Kondisi/cara keluar & RTL",""),("Encounter.episodeOfCare","EpisodeOfCare/{ID episode HIV}","")],"PUT dengan Encounter.id dari POST awal.","Setiap kunjungan")

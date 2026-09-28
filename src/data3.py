from data import ICD
LN="http://loinc.org"; SN="http://snomed.info/sct"; WHO="http://fhir.org/guides/who/anc-cds/CodeSystem/anc-custom-codes"
KA="http://terminology.kemkes.go.id/CodeSystem/anc-custom-codes"; KC="http://terminology.kemkes.go.id/CodeSystem/clinical-term"
UC="http://unitsofmeasure.org"; V3="http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation"
OC="http://terminology.hl7.org/CodeSystem/observation-category"; KFA="http://sys-ids.kemkes.go.id/kfa"
IMR="http://terminology.kemkes.go.id/CodeSystem/immunization-reason"; IMO="http://terminology.hl7.org/CodeSystem/immunization-origin"
Q2="https://fhir.kemkes.go.id/Questionnaire/Q0002"
CATD={"survey":"Survey","exam":"Exam","vital-signs":"Vital Signs","laboratory":"Laboratory","imaging":"Imaging","social-history":"Social History"}
V=[]  # each: dict(tahap,kel,var,res,cat,frek, el=[(path,nilai,ket)])
def add(tahap,kel,var,res,el,cat="",frek=""): V.append(dict(tahap=tahap,kel=kel,var=var,res=res,el=el,cat=cat,frek=frek))
def opts(prefix,system,items):
    e=[(prefix+".system",system,"")]
    for it in items:
        code,disp=it[0],it[1]; ket=it[2] if len(it)>2 else ""
        e.append((prefix+".code",code,disp+(" — "+ket if ket else "")))
    return e
def obs(tahap,kel,var,cat,c0,c1,value,extra=(),note="",frek=""):
    el=[("*Observation.status","final","Status hasil pemeriksaan"),
        ("Observation.category[0].coding[0].system",OC,""),("Observation.category[0].coding[0].code",cat,CATD[cat])]
    el.append(("*Observation.code.coding[0].system",c0[0],"")); el.append(("*Observation.code.coding[0].code",c0[1],c0[2]))
    if c1:
        el.append(("*Observation.code.coding[1].system",c1[0],"")); el.append(("*Observation.code.coding[1].code",c1[1],c1[2]))
    el+=[("*Observation.subject","Patient/{IHS pasien}",""),("*Observation.encounter","Encounter/{ID kunjungan}",""),
         ("Observation.effectiveDateTime","(DateTime)","Waktu pemeriksaan"),("*Observation.performer[i]","Practitioner/{IHS nakes}","Nakes pemeriksa")]
    el+=value; el+=list(extra)
    add(tahap,kel,var,"Observation",el,note,frek)
def qty(unit,code=None): return [("Observation.valueQuantity.value","(Decimal)","Nilai hasil"),("Observation.valueQuantity.unit",unit,""),("Observation.valueQuantity.system",UC,""),("Observation.valueQuantity.code",code or unit,"")]
INT=[("Observation.valueInteger","(Integer)","")]; DT=[("Observation.valueDateTime","(DateTime)","")]
def cc(system,items): return opts("Observation.valueCodeableConcept.coding[0]",system,items)
NA=opts("Observation.interpretation.coding[0]",V3,[("N","Normal","tampil: Normal"),("A","Abnormal","tampil: Tidak Normal")])
RX=[("11214006","Reactive"),("131194007","Non-Reactive")]
REF="Rujuk modul Rawat Jalan / IGD / Rawat Inap SATUSEHAT"

# 1 Pasien
T="1. Pendaftaran pasien"
idp=[("Patient.identifier[i].use / system / value","Nomor SATUSEHAT (IHS) pasien","Didapat via GET ke Master Patient Index (MPI)"),
 ("Patient.name[i].text","Nama lengkap",""),("Patient.identifier[i].use / system / value","Nomor rekam medis",""),
 ("Patient.identifier[i].use / system / value","NIK",""),("Patient.identifier[i].use / system / value","Nomor paspor / KITAS","Khusus WNA"),
 ("Patient.contact.name","Nama ibu kandung",""),("Patient.extension:birthPlace","Tempat lahir",""),("Patient.birthDate","Tanggal lahir",""),
 ("Patient.gender","Jenis kelamin",""),("Patient.communication.language","Bahasa yang dikuasai",""),
 ("Patient.address.line","Alamat lengkap, RT, RW",""),("Patient.address.extension:administrativeCode.extension:village","Kelurahan / desa","Kode wilayah"),
 ("Patient.address.extension:administrativeCode.extension:district","Kecamatan","Kode wilayah"),("Patient.address.extension:administrativeCode.extension:city","Kota / kabupaten","Kode wilayah"),
 ("Patient.address.extension:administrativeCode.extension:province","Provinsi","Kode wilayah"),("Patient.address.postalCode","Kode pos",""),
 ("Patient.address.country","Negara",""),("Patient.telecom","No. telepon rumah & seluler",""),("Patient.maritalStatus","Status pernikahan","")]
add(T,"Identitas pasien","Identitas pasien (22 butir)","Patient",idp,"Cukup cari IHS pasien di MPI lalu simpan di sistem; data diri tidak perlu dikirim ulang tiap transaksi.","Sekali per pasien")
# 2 Encounter
T="2. Pendaftaran kunjungan"
add(T,"Kunjungan","Kunjungan ANC","Encounter",[
 ("*Encounter.identifier[i]","No. registrasi kunjungan",""),("*Encounter.status","Status kunjungan",""),("*Encounter.statusHistory[i].status / period","Riwayat status + waktu",""),
 ("*Encounter.class","Kelas kunjungan",""),("*Encounter.subject","Patient/{IHS pasien}",""),
 ("Encounter.episodeOfCare[i]","EpisodeOfCare/{UUID episode kehamilan}","Dari tahap 3"),
 ("*Encounter.participant[i].type / individual","Practitioner/{IHS nakes}",""),("*Encounter.period","Mulai–selesai kunjungan",""),
 ("*Encounter.location[i]","Location/{ID poli KIA}",""),("*Encounter.serviceProvider","Organization/{ID faskes}",""),
 ("*Encounter.diagnosis[i].condition / use / rank","Diagnosis kunjungan","Diisi saat kunjungan selesai (tahap 16)")],
 "* = wajib. Satu rangkaian pelayanan = 1 Encounter.","Setiap kunjungan")
# 3 EoC
T="3. Memulai episode kehamilan"
add(T,"Episode kehamilan","Episode kehamilan","EpisodeOfCare",[
 ("*EpisodeOfCare.status","active",""),("EpisodeOfCare.statusHistory[i].status / period.start","active / tanggal mulai",""),
 ("*EpisodeOfCare.type[i]","ANC","Tipe episode Antenatal Care"),("*EpisodeOfCare.patient","Patient/{IHS pasien}",""),
 ("*EpisodeOfCare.managingOrganization","Organization/{ID faskes}",""),("*EpisodeOfCare.period.start","Tanggal HPHT (jika tersedia)","")],
 "POST sekali saja pada kunjungan ANC pertama; UUID balikan ditaruh di Encounter.episodeOfCare. Kunjungan berikutnya: GET EpisodeOfCare dengan patient + type ANC + status active (opsional + organization) untuk mengambil UUID-nya.","Sekali per kehamilan")
# 4 Obstetri
T="4. Kondisi pasien / status obstetri"; K="Status obstetri"
obs(T,K,"Gravida","survey",(LN,"11996-6","[#] Pregnancies"),(WHO,"ANC.B6.DE24","Number of pregnancies (gravida)"),INT,frek="Kunjungan pertama")
obs(T,K,"Partus","survey",(LN,"11977-6","[#] Parity"),(WHO,"ANC.B6.DE32","Parity"),INT)
obs(T,K,"Abortus","survey",(LN,"69043-8","Other pregnancy outcomes #"),(WHO,"ANC.B6.DE25","Number of miscarriages and/or abortions"),INT)
obs(T,K,"Tanggal HPHT","survey",(LN,"8665-2","Last menstrual period start date"),(WHO,"ANC.B6.DE14","Last menstrual period (LMP) date"),DT,note="Juga dipakai untuk EpisodeOfCare.period.start.")
obs(T,K,"Hari Perkiraan Lahir (HPL)","survey",(LN,"11778-8","Delivery date Estimated"),(WHO,"ANC.B6.DE22","Expected date of delivery (EDD)"),DT)
obs(T,K,"Berat badan sebelum hamil","survey",(LN,"56077-1","Body weight --pre current pregnancy"),(WHO,"ANC.B8.DE2","Pre-gestational weight"),qty("kg"))
obs(T,K,"Tinggi badan","vital-signs",(LN,"8302-2","Body height"),(WHO,"ANC.B8.DE1","Height"),qty("cm"))
obs(T,K,"IMT sebelum hamil","exam",(KC,"OC000010","Indeks Massa Tubuh Sebelum Hamil"),(KA,"ANC.SS.DE58","IMT Sebelum Hamil"),qty("kg/m2"),
 opts("Observation.interpretation.coding[0]",SN,[("248342006","Underweight","Kurus: ≤18,4 kg/m2"),("43664005","Normal weight","Normal: 18,5–24,9"),("238131007","Overweight","Gemuk: 25–29,9"),("414915002","Obese","Obesitas: ≥30")])
 +[("Observation.referenceRange.low / high / text","Batas rentang per kategori (lihat baris interpretation)","Lampiran 1")],
 note="Interpretation dari Lampiran 1. Versi 1.0 memakai kode Kemkes 'BMI-Normal' dst., v1.1 diganti SNOMED (Lampiran 3).")
obs(T,K,"Target kenaikan berat badan","exam",(KC,"OC000011","Target Kenaikan Berat Badan"),(WHO,"ANC.B8.DE10","Expected weight gain"),
 cc(KC,[("OV000008","5–9 kg","untuk IMT ≥30 (Obesitas)"),("OV000009","7–11.5 kg","untuk IMT 25,0–29,9 (Gemuk)"),("OV000010","11.5–16 kg","untuk IMT 18,5–24,9 (Normal)"),("OV000011","12.5–18 kg","untuk IMT <18,5 (Kurus)")]))
obs(T,K,"Jarak kehamilan saat ini dengan sebelumnya","survey",(KC,"OC000001","Jarak kehamilan"),(KA,"ANC.SS.DE53","Jarak kehamilan"),qty("mo"),note="Satuan bulan.")
K="Imunisasi tetanus"
TT=[("Immunization.protocolApplied[0].doseNumberPositiveInt",str(i),f"T{i}") for i in range(1,6)]
add(T,K,"Riwayat status imunisasi TT (T1–T5)","Immunization",[
 ("Immunization.status","completed / not-done",""),("Immunization.vaccineCode.coding[0].system",KFA,""),("Immunization.vaccineCode.coding[0].code","VG139","Td"),
 ("Immunization.occurrenceDateTime","(DateTime)","Tanggal pemberian dulu"),("Immunization.recorded","(DateTime)",""),("Immunization.primarySource","false","Data riwayat, bukan diberikan di sini"),
 ("Immunization.reportOrigin.coding[0].system",IMO,""),("Immunization.reportOrigin.coding[0].code","recall","Parent/Guardian/Patient Recall"),("Immunization.reportOrigin.coding[0].code","record","Written Record"),
 ("Immunization.reasonCode.coding[0].system",IMR,""),("Immunization.reasonCode.coding[0].code","IM-WUS","Imunisasi Program Rutin Lanjutan Wanita Usia Subur")]+TT,frek="Kunjungan pertama")
add(T,K,"Riwayat status imunisasi TT (T0 / belum pernah)","Immunization",[
 ("Immunization.status","not-done",""),("Immunization.vaccineCode.coding[0].system",KFA,""),("Immunization.vaccineCode.coding[0].code","VG139","Td"),
 ("Immunization.occurrenceString","(String)","Bukan DateTime"),("Immunization.primarySource","false",""),
 ("Immunization.reportOrigin.coding[0].system",IMO,""),("Immunization.reportOrigin.coding[0].code","recall","Parent/Guardian/Patient Recall"),
 ("Immunization.reasonCode.coding[0].system",IMR,""),("Immunization.reasonCode.coding[0].code","IM-WUS","Imunisasi Program Rutin Lanjutan Wanita Usia Subur")],"Tanpa doseNumber.")
add(T,K,"Pemberian imunisasi TT saat kunjungan (T1–T5)","Immunization",[
 ("Immunization.status","completed",""),("Immunization.vaccineCode","(Lihat Lampiran 4 terminologi imunisasi)","Kode vaksin KFA yang diberikan"),
 ("Immunization.occurrenceDateTime","(DateTime)",""),("Immunization.recorded","(DateTime)",""),("Immunization.primarySource","true","Diberikan di faskes ini"),
 ("Immunization.reasonCode.coding[0].system",IMR,""),("Immunization.reasonCode.coding[0].code","IM-WUS","Imunisasi Program Rutin Lanjutan Wanita Usia Subur")]+TT)
# 5
T="5. Data kunjungan kehamilan"; K="Usia kehamilan"
obs(T,K,"Usia kehamilan","survey",(LN,"18185-9","Gestational age"),(WHO,"ANC.B6.DE17","Gestational age"),qty("wk"),note="Satuan minggu.",frek="Setiap kunjungan")
obs(T,K,"Trimester ke-","survey",(LN,"32418-6","Obstetric trimester Stated"),(KA,"ANC.SS.DE13","Trimester ke"),[("Observation.valueInteger","(Integer)","1 / 2 / 3")],frek="Setiap kunjungan")
# 6
T="6. Pelayanan kehamilan"; K="6a. Pemeriksaan ibu"; F="Setiap kunjungan"
obs(T,K,"Berat badan","vital-signs",(LN,"29463-7","Body weight"),(WHO,"ANC.B8.DE3","Current weight"),qty("kg"),frek=F)
obs(T,K,"Lingkar lengan atas (LiLA)","exam",(SN,"284473002","Mid upper arm circumference"),(KA,"ANC.SS.DE3","Lingkar Lengan Atas (LILA)"),qty("cm"),
 [("Observation.interpretation.coding[0].system",KC,"untuk KEK & Risiko KEK"),("Observation.interpretation.coding[0].code","OI000018","Kurang Energi Kronis (KEK) — LiLA <23 cm"),("Observation.interpretation.coding[0].code","OI000035","Risiko Kurang Energi Kronis (KEK) — LiLA 23–<23,5 cm"),
  ("Observation.interpretation.coding[0].system",V3,"untuk Normal"),("Observation.interpretation.coding[0].code","N","Normal — LiLA ≥23,5 cm")],frek=F)
obs(T,K,"Tinggi fundus uteri","exam",(LN,"11881-0","Uterus Fundal height Tape measure"),(WHO,"ANC.B8.DE105","Symphysis-fundal height (SFH)"),qty("cm"),frek=F)
obs(T,K,"Tekanan darah sistolik","vital-signs",(LN,"8480-6","Systolic blood pressure"),(WHO,"ANC.B8.DE17","Systolic blood pressure"),qty("mm[Hg]"),frek=F)
obs(T,K,"Tekanan darah diastolik","vital-signs",(LN,"8462-4","Diastolic blood pressure"),(WHO,"ANC.B8.DE19","Diastolic blood pressure"),qty("mm[Hg]"),frek=F)
obs(T,K,"Nadi","vital-signs",(LN,"8867-4","Heart rate"),(WHO,"ANC.B8.DE36","Pulse rate"),qty("beats/minute","/min"),frek=F)
obs(T,K,"Suhu","vital-signs",(LN,"8310-5","Body temperature"),(WHO,"ANC.B8.DE34","Body temperature"),qty("C","Cel"),frek=F)
obs(T,K,"Pernapasan","vital-signs",(LN,"9279-1","Respiratory rate"),(KA,"ANC.SS.DE2","Pernapasan"),qty("breaths/min","/min"),frek=F)
obs(T,K,"Golongan darah","laboratory",(LN,"883-9","ABO group [Type] in Blood"),(WHO,"ANC.B9.DE24","Blood type"),cc(LN,[("LA19710-5","Group A"),("LA19709-7","Group B"),("LA19708-9","Group O"),("LA28449-9","Group AB")]))
obs(T,K,"Rhesus","laboratory",(LN,"10331-7","Rh [Type] in Blood"),(WHO,"ANC.B9.DE29","Rh factor"),cc(LN,[("LA6576-8","Positive"),("LA6577-6","Negative")]))
add(T,K,"Makanan Tambahan (MT) ibu hamil","QuestionnaireResponse",[
 ("QuestionnaireResponse.questionnaire",Q2,""),("QuestionnaireResponse.item.linkId","1","Makanan Tambahan Ibu Hamil (grup)"),
 ("QuestionnaireResponse.item.item.linkId","1.1","Jika LILA <23,5, Apakah mendapatkan MT"),("QuestionnaireResponse.item.item.answer.valueBoolean","true / false","Ya / Tidak"),
 ("QuestionnaireResponse.item.item.linkId","1.2","Jenis MT"),("QuestionnaireResponse.item.item.answer.valueCoding.system",KC,""),
 ("QuestionnaireResponse.item.item.answer.valueCoding.code","FO000001","MT Lokal"),("QuestionnaireResponse.item.item.answer.valueCoding.code","FO000002","MT Pabrikan")],
 "Tabel 2 menulis path 1.1 sebagai item.answer, Tabel 9 sebagai item.item.answer; di sini mengikuti Tabel 9 (item bersarang).")
K="6b. Pemeriksaan fisik ibu"
for v,c0,anc,ad,bs in [("Konjungtiva",(LN,"10197-2","Physical findings of Eye Narrative"),"ANC.SS.DE26","Pemeriksaan Fisik Konjungtiva",("29445007","Conjunctival structure")),
 ("Sklera",(LN,"10197-2","Physical findings of Eye Narrative"),"ANC.SS.DE27","Pemeriksaan Fisik Sklera",("18619003","Scleral structure")),
 ("Leher",(LN,"11411-6","Physical findings of Neck Narrative"),"ANC.SS.DE28","Pemeriksaan Fisik Leher",None),
 ("Gigi dan mulut",(SN,"423066003","Finding of mouth region"),"ANC.SS.DE29","Pemeriksaan Fisik Area Mulut",None),
 ("THT",(SN,"297268004","Ear, nose and throat finding"),"ANC.SS.DE30","Pemeriksaan Fisik Telinga Hidung dan Tenggorokan (THT)",None),
 ("Dada (jantung)",(LN,"10200-4","Physical findings of Heart Narrative"),"ANC.SS.DE31","Pemeriksaan Fisik Dada (Auskultasi Jantung)",None),
 ("Dada (paru)",(SN,"301230006","Lung finding"),"ANC.SS.DE32","Pemeriksaan Fisik Dada (Auskultasi Paru)",None),
 ("Perut",(LN,"10191-5","Physical findings of Abdomen Narrative"),"ANC.SS.DE33","Pemeriksaan Fisik Perut",None),
 ("Tungkai",(SN,"116312005","Finding of lower limb"),"ANC.SS.DE34","Pemeriksaan Fisik Tungkai",None)]:
    ex=([("Observation.bodySite.coding[0].system",SN,""),("Observation.bodySite.coding[0].code",bs[0],bs[1])] if bs else [])
    obs(T,K,v,"exam",c0,(KA,anc,ad),[],ex+NA)
K="6c. Pemeriksaan janin"
obs(T,K,"Denyut jantung janin (DJJ)","exam",(LN,"55283-6","Fetal Heart rate"),(WHO,"ANC.B8.DE107","Fetal heart rate"),qty("{beats}/min"),frek=F)
obs(T,K,"Kepala terhadap PAP","exam",(SN,"249111004","Engagement of head"),(KA,"ANC.SS.DE46","Kepala Terhadap PAP"),cc(SN,[("249112006","Head engaged","Masuk panggul"),("62098001","Head not engaged","Belum masuk panggul")]),note="v1.0 memakai kode Kemkes OC000002 / OV000001 / OV000002, v1.1 diganti SNOMED (Lampiran 3).")
obs(T,K,"Taksiran berat janin (TBJ)","exam",(LN,"89087-1","Fetal Body weight Estimated"),(KA,"ANC.SS.DE1","Taksiran Berat Janin (TBJ)"),qty("g"))
obs(T,K,"Presentasi janin","exam",(LN,"72155-5","Position in womb Fetus [RHEA]"),(WHO,"ANC.B8.DE111","Fetal presentation"),cc(SN,[("1209182005","Cephalic fetal presentation","Presentasi kepala"),("6096002","Breech presentation","Presentasi bokong"),("288203005","Transverse/oblique lie","Letak lintang")]),note="v1.0: OV000003 / OV000004 / OV000005, v1.1 diganti SNOMED.")
obs(T,K,"Jumlah janin","exam",(SN,"246435002","Number of fetuses"),(WHO,"ANC.B8.DE109","Number of fetuses"),INT,note="v1.0: Kemkes OC000003, v1.1 diganti SNOMED.")
K="6d. Pemeriksaan USG"
for v,c0,anc,val in [("Gestational sac (GS) diameter",("11850-5","Gestational sac Mean diameter US"),(KA,"ANC.SS.DE36","Gestational sac (GS) USG"),qty("cm")),
 ("Crown rump length (CRL)",("11957-8","Fetal Crown Rump length US"),(KA,"ANC.SS.DE37","Fetal Crown Rump Length (CRL) USG"),qty("cm")),
 ("DJJ (USG)",("11948-7","Fetal Heart rate US"),(KA,"ANC.SS.DE38","Denyut Jantung Janin (DJJ) USG"),qty("{beats}/min")),
 ("Usia kehamilan (USG)",("11888-5","Gestational age US composite estimate"),(WHO,"ANC.B6.DE20","Ultrasound"),qty("wk")),
 ("HPL (USG)",("11781-2","Delivery date US composite estimate"),(KA,"ANC.SS.DE40","Hari Perkiraan Lahir (HPL) USG"),DT),
 ("Biparietal diameter (BPD)",("11820-8","Fetal Head Diameter.biparietal US"),(KA,"ANC.SS.DE59","Biparietal Diameter (BPD) USG"),qty("cm")),
 ("Head circumference (HC)",("11984-2","Fetal Head Circumference US"),(KA,"ANC.SS.DE42","Head Circumference (HC) USG"),qty("cm")),
 ("Abdominal circumference (AC)",("11979-2","Fetal Abdomen Circumference US"),(KA,"ANC.SS.DE43","Abdominal Circumference (AC) USG"),qty("cm")),
 ("Femur length (FL)",("11963-6","Fetal Femur diaphysis [Length] US"),(KA,"ANC.SS.DE44","Femur Length (FL) USG"),qty("cm")),
 ("Berat janin (USG)",("11727-5","Fetal Body weight estimated by US"),(KA,"ANC.SS.DE45","Berat janin USG"),qty("g"))]:
    obs(T,K,v,"imaging",(LN,)+c0,anc,val)
obs(T,K,"Letak janin (USG)","imaging",(SN,"271692001","Presentation of fetus"),(KA,"ANC.SS.DE41","Letak Janin USG"),cc(SN,[("398236008","Intrauterine","Intrauteri"),("298109001","Ectopic","Ekstrauteri")]),note="v1.0: OC000004 / OV000006 / OV000007, v1.1 diganti SNOMED.")
add(T,K,"Tindakan USG kehamilan","Procedure",[("Procedure.status","completed",""),("Procedure.category.coding","Kategori prosedur",""),("Procedure.code.coding","Kode tindakan USG",""),("Procedure.performedPeriod","Waktu tindakan","")],"Kode tidak dirinci di playbook ANC. Citra DICOM via ImagingStudy mengikuti modul radiologi.")
K="6e. Pemeriksaan 10T (lab)"
TYP="Typo di sumber: baris code & display ditulis ulang sebagai '.system'."
obs(T,K,"Hemoglobin","laboratory",(LN,"718-7","Hemoglobin [Mass/volume] in Blood"),(WHO,"ANC.B9.DE175","Blood hemoglobin test conducted"),qty("g/dL"),note="Tes dasar")
obs(T,K,"Skrining PPIA HIV","laboratory",(LN,"68961-2","HIV 1 Ab [Presence] in Serum, Plasma or Blood by Rapid immunoassay"),(WHO,"ANC.B9.DE32","HIV test"),cc(SN,RX),note="Tes dasar. "+TYP)
obs(T,K,"Skrining PPIA Sifilis (RPR)","laboratory",(LN,"20508-8","Reagin Ab [Units/volume] in Serum or Plasma by RPR"),(WHO,"ANC.B9.DE96","Syphilis test conducted"),cc(SN,RX),note="Tes dasar. "+TYP)
obs(T,K,"Skrining PPIA Sifilis (VDRL)","laboratory",(LN,"14904-7","Reagin Ab [Presence] in Specimen by VDRL"),(WHO,"ANC.B9.DE96","Syphilis test conducted"),cc(SN,RX),note="Tes dasar. "+TYP)
obs(T,K,"Skrining PPIA Hepatitis B","laboratory",(LN,"75410-1","Hepatitis B virus surface Ag [Presence] in Serum, Plasma or Blood by Rapid immunoassay"),(WHO,"ANC.B9.DE60","Hepatitis B test conducted"),cc(SN,RX),note="Tes dasar. "+TYP)
obs(T,K,"Gula darah sewaktu","laboratory",(LN,"74774-1","Glucose [Mass/volume] in Serum, Plasma or Blood"),(WHO,"ANC.B9.DE159","Blood glucose test conducted"),qty("mg/dL"),note="Tes lain")
obs(T,K,"Protein urin","laboratory",(LN,"5804-0","Protein [mass/volume] in urine by test strip"),(WHO,"ANC.B9.DE114","Urine test conducted"),qty("mg/dL"),note="Tes lain")
K="6f. Pemantauan & pendampingan (4 Terlalu)"
el=[("QuestionnaireResponse.questionnaire",Q2,""),("QuestionnaireResponse.item.linkId","2","Pemantauan & Pendampingan (grup)")]
for lid,t in [("2.1","Terlalu muda usia melahirkan di bawah 21 tahun"),("2.2","Terlalu rapat jarak kelahiran (<2 tahun)"),("2.3","Terlalu tua (kehamilan di atas 35 tahun)"),("2.4","Terlalu sering melahirkan (anak >3)")]:
    el+=[("QuestionnaireResponse.item.item.linkId",lid,t),("QuestionnaireResponse.item.item.answer.valueBoolean","true / false","Ya / Tidak")]
add(T,K,"Pemantauan & pendampingan (4T)","QuestionnaireResponse",el,"Inkonsistensi di sumber: teks item 2.1 di Tabel 14 tertulis 'di bawah 20 tahun'.")
K="6g. Riwayat penyakit & risiko"
add(T,K,"Komplikasi / penyulit kehamilan","Condition",[("Condition.category.coding.system","http://terminology.hl7.org/CodeSystem/condition-category","Sumber (Tabel 15) tertulis .../condition-clinical; tabel lain memakai condition-category"),("Condition.category.coding.code","problem-list-item","Problem List Item"),("Condition.code.coding.system","http://hl7.org/fhir/sid/icd-10",""),("Condition.code.coding.code","Kode ICD-10","»LIST:icd"),("Condition.code.coding.display","ICD-10 Description","Pasangan display dari kode yang dipilih")])
add(T,K,"Riwayat penyakit menular","Condition",[("Condition.category.coding.system","http://terminology.hl7.org/CodeSystem/condition-category",""),("Condition.category.coding.code","problem-list-item","Problem List Item"),("Condition.code.coding.system",SN,""),("Condition.code.coding.code","ECL: < 417662000 OR < 443508001","»Konsep induk: History of clinical finding in subject / No history of clinical finding in subject"),("Condition.code.coding.display","SNOMED CT Description","»Pasangan display dari kode yang dipilih")],"Kode lengkap di Lampiran Standar Terminologi SATUSEHAT (umum).")
add(T,K,"Riwayat penyakit keluarga","Condition",[("Condition.category.coding.system","http://terminology.hl7.org/CodeSystem/condition-category",""),("Condition.category.coding.code","problem-list-item","Problem List Item"),("Condition.code.coding.system",SN,""),("Condition.code.coding.code","ECL: < 416471007 OR < 160266009","»Konsep induk: Family history of clinical finding / No family history of clinical finding"),("Condition.code.coding.display","SNOMED CT Description","»Pasangan display dari kode yang dipilih")],"Kode lengkap di Lampiran Standar Terminologi SATUSEHAT (umum).")
obs(T,K,"Merokok","social-history",(LN,"72166-2","Tobacco smoking status"),None,cc(SN,[("77176002","Smoker","Ya"),("43381005","Passive smoker","Pasif"),("8392000","Non-smoker","Tidak")]))
obs(T,K,"Konsumsi alkohol","social-history",(LN,"11331-6","History of Alcohol use"),None,cc(SN,[("219006","Current drinker","Ya"),("105542008","Non - drinker","Tidak")]))
K="6h. Kondisi lainnya"
add(T,K,"Disabilitas & kelas ibu hamil","QuestionnaireResponse",[("QuestionnaireResponse.questionnaire",Q2,""),("QuestionnaireResponse.item.linkId","3","Lainnya (grup)"),
 ("QuestionnaireResponse.item.item.linkId","3.1","Apakah disabilitas?"),("QuestionnaireResponse.item.item.answer.valueBoolean","true / false","Ya / Tidak"),
 ("QuestionnaireResponse.item.item.linkId","3.2","Apakah mengikuti kelas ibu hamil?"),("QuestionnaireResponse.item.item.answer.valueBoolean","true / false","Ya / Tidak")])
# 7
T="7. Pemeriksaan penunjang"
add(T,"Laboratorium","Permintaan & hasil laboratorium","ServiceRequest, Specimen, Observation",[
 ("ServiceRequest.code.coding","Nama pemeriksaan",""),("ServiceRequest.identifier","Nomor pemeriksaan",""),("ServiceRequest.authoredOn","Tanggal & jam permintaan",""),
 ("ServiceRequest.occurrenceDateTime","Tanggal & jam pemeriksaan",""),("ServiceRequest.requester","Dokter pengirim (+ no. telepon)",""),("ServiceRequest.encounter","Faskes & unit pengirim",""),
 ("ServiceRequest.priority","CITO / Non CITO",""),("ServiceRequest.reasonReference","Diagnosis / masalah",""),("ServiceRequest.note","Catatan permintaan",""),
 ("Specimen.collection.fastingStatusCodeableConcept.coding","Status puasa pasien",""),("Specimen.type.coding / type.text","Asal sumber spesimen",""),
 ("Specimen.collection.bodySite.coding","Lokasi pengambilan spesimen",""),("Specimen.collection.quantity","Jumlah / volume spesimen",""),
 ("Specimen.collection.method.coding / text","Cara / metode pengambilan",""),("Specimen.collection.collectedDateTime","Tanggal & jam pengambilan",""),
 ("Specimen.condition.text","Kondisi spesimen saat diambil",""),("Specimen.receivedTime","Tanggal & jam fiksasi",""),
 ("Specimen.container.additiveCodeableConcept.coding","Cairan fiksasi",""),("Specimen.container.capacity","Volume cairan fiksasi",""),
 ("Specimen.collection.collector","Petugas pengambil spesimen",""),("Specimen.extension.transportedPerson","Petugas pengantar spesimen",""),
 ("Specimen.extension.receivedPerson","Petugas penerima spesimen",""),("Specimen.processing.timeDateTime","Tanggal & jam pemeriksaan/pengolahan",""),
 ("Observation.code.coding / category.coding","Nilai hasil pemeriksaan (kode tes)",""),("Observation.valueCodeableConcept.coding","Normal / tidak normal",""),
 ("Observation.referenceRange","Nilai rujukan & nilai kritis",""),("Observation.interpretation.coding","Interpretasi hasil",""),
 ("Observation.performer (Practitioner)","Petugas analis, dokter validator, dokter penginterpretasi",""),("Observation.performer (Organization)","Faskes yang melakukan pemeriksaan",""),
 ("Observation.effectiveDateTime","Tanggal & jam hasil keluar dari lab",""),("Observation.issued","Tanggal & jam hasil diterima unit pengirim","")],REF+" (terminologi & payload detail).")
add(T,"Radiologi","Permintaan & hasil radiologi","ServiceRequest, AllergyIntolerance, Observation, ImagingStudy",[
 ("ServiceRequest.code.coding","Nama pemeriksaan radiologi",""),("ServiceRequest.identifier","Nomor permintaan",""),("ServiceRequest.authoredOn","Tanggal & jam permintaan",""),
 ("ServiceRequest.requester","Dokter pengirim (+ no. telepon)",""),("ServiceRequest.encounter","Faskes & unit pengirim",""),("ServiceRequest.priority","CITO / Non CITO",""),
 ("ServiceRequest.reasonReference","Diagnosis kerja / masalah",""),("ServiceRequest.note","Catatan permintaan",""),
 ("ServiceRequest.supportingInfo → AllergyIntolerance.code / category","Status alergi bahan kontras",""),("ServiceRequest.supportingInfo → Observation.code / valueCodeableConcept","Status kehamilan",""),
 ("ServiceRequest.occurrenceDateTime","Tanggal & jam pemeriksaan",""),("ServiceRequest.orderDetail.coding","Jenis bahan kontras",""),("ServiceRequest.contained","Identitas pasien",""),
 ("ImagingStudy.series.uid","Foto hasil (DICOM)",""),("ImagingStudy.interpreter","Dokter penginterpretasi",""),
 ("Observation.code / category / derivedFrom / valueString","Interpretasi radiologi","")],REF+".")
# 8-15
add("8. Diagnosis","Diagnosis","Diagnosis awal & akhir (primer / sekunder)","Encounter + Condition",[("Encounter.diagnosis.condition","Condition/{ID}",""),("Encounter.diagnosis.use","Jenis diagnosis (awal/akhir)",""),("Encounter.diagnosis.rank","1 = primer, 2+ = sekunder",""),("Condition.code.coding","Kode ICD-10",""),("Condition.category.coding","Kategori diagnosis","")],REF+".")
add("9. Tindakan / prosedur medis","Tindakan","Tindakan / prosedur medis","Procedure",[("Procedure.code.coding","Kode ICD-9-CM",""),("Procedure.category.coding","Kategori prosedur","")],REF+".")
T="10. Konseling / temu wicara / edukasi"
add(T,"Edukasi","Tema edukasi yang diberikan","Procedure",[("Procedure.code.coding[0].system",SN,"untuk edukasi gizi"),("Procedure.code.coding[0].code","61310001","Nutrition education"),
 ("Procedure.code.coding[0].system",KC,"untuk edukasi lain"),("Procedure.code.coding[0].code","ED000008","Edukasi Tanda Bahaya Kehamilan, Bersalin dan Nifas"),
 ("Procedure.code.coding[0].code","ED000009","Edukasi IMD dan ASI Eksklusif"),("Procedure.code.coding[0].code","ED000010","Edukasi PHBS"),
 ("Procedure.code.coding[0].code","ED000011","Edukasi KB pasca salin"),("Procedure.code.coding[0].code","ED000012","Edukasi lainnya")],
 "1 payload Procedure per topik (2 edukasi = 2 Procedure). Elemen lain mengikuti Pengiriman Data Edukasi di modul Rawat Jalan/IGD/Ranap.")
add(T,"Edukasi","Tidak diberikan konseling","Procedure",[("Procedure.status","not-done",""),("Procedure.code.coding[0].system",SN,""),("Procedure.code.coding[0].code","409073007","Education")])
T="11. Farmasi"
add(T,"Farmasi","Peresepan obat","Medication + MedicationRequest",[("Medication.code.coding","Nama obat (KFA)",""),("Medication.form.coding","Bentuk / sediaan",""),("MedicationRequest.medicationReference","Medication/{ID}",""),
 ("MedicationRequest.dispenseRequest.quantity","Jumlah obat",""),("MedicationRequest.dosageInstruction.route","Rute pemberian",""),("MedicationRequest.dosageInstruction.doseAndRate.doseQuantity.value / unit","Dosis & unit",""),
 ("MedicationRequest.dosageInstruction.timing","Frekuensi / interval",""),("MedicationRequest.dosageInstruction.additionalInstruction","Aturan tambahan & catatan resep",""),
 ("MedicationRequest.requester","Dokter penulis resep (+ no. HP)",""),("MedicationRequest.authoredOn","Tanggal & jam penulisan resep",""),("MedicationRequest.status","Status resep","")],REF+". Pengkajian resep (administrasi, farmasetik, klinis) via QuestionnaireResponse, lihat modul Pelayanan Kefarmasian.")
add(T,"Farmasi","Pengeluaran obat / obat dibawa pulang","Medication + MedicationDispense",[("Medication.code.coding","Nama obat (KFA)",""),("Medication.form.coding","Bentuk / sediaan",""),("MedicationDispense.medicationReference","Medication/{ID}",""),
 ("MedicationDispense.quantity","Jumlah obat",""),("MedicationDispense.dosageInstruction.route","Rute pemberian",""),("MedicationDispense.dosageInstruction.doseAndRate.doseQuantity.value / unit","Dosis & unit",""),
 ("MedicationDispense.dosageInstruction.timing","Frekuensi / interval",""),("MedicationDispense.dosageInstruction.additionalInstruction","Aturan tambahan","")],REF+".")
add("12. Rencana tindak lanjut & transportasi rujuk","RTL","Rencana tindak lanjut & sarana transportasi rujuk","Encounter + ServiceRequest",[("Encounter.hospitalization.dischargeDisposition","Rencana tindak lanjut",""),("ServiceRequest.code.coding","Jenis tindak lanjut",""),("ServiceRequest.locationCode","Sarana transportasi untuk rujuk","")],REF+".")
add("13. Instruksi tindak lanjut","RTL","Instruksi untuk tindak lanjut","ServiceRequest",[("ServiceRequest.status / intent","Status & intent permintaan",""),("ServiceRequest.code","Instruksi",""),("ServiceRequest.subject / encounter","Pasien & kunjungan",""),("ServiceRequest.occurrenceDateTime","Waktu tindak lanjut",""),("ServiceRequest.performer","Pelaksana","")],REF+".")
T="14. Kondisi saat meninggalkan faskes"
add(T,"Pulang","Kondisi saat meninggalkan RS / faskes","Condition + Encounter",[("Condition.code.coding","Kondisi pasien saat pulang",""),("Encounter.hospitalization.dischargeDisposition","Disposisi pulang","")],REF+".")
obs(T,"Pulang","Waktu kematian (bila meninggal)","exam",(LN,"81956-5","Date and time of death [TimeStamp]"),(KA,"ANC.SS.DE56","Waktu Kematian"),DT)
add("15. Cara keluar dari faskes","Pulang","Cara keluar dari RS / faskes","Encounter",[("Encounter.hospitalization.dischargeDisposition","Cara keluar","")],REF+".")
T="16. Pembaruan data kunjungan"
add(T,"Update Encounter","Kunjungan selesai + status kunjungan ANC","Encounter",[
 ("Encounter.statusHistory[i].status / period","in-progress (saat dilayani) → finished","Dianjurkan catat mulai & selesai tiap status"),
 ("Encounter.status","finished",""),("Encounter.period.end","Waktu kunjungan selesai",""),("*Encounter.diagnosis[i].condition","Condition/{ID diagnosis}",""),
 ("Encounter.hospitalization.dischargeDisposition","Kondisi / cara keluar & RTL",""),("Encounter.episodeOfCare","EpisodeOfCare/{UUID}",""),
 ("Encounter.identifier[0].system","http://terminology.kemkes.go.id/CodeSystem/episodeofcare/ANC","Status kunjungan ANC"),
 ("Encounter.identifier[0].value","K1A","Kunjungan K1 akses"),("Encounter.identifier[0].value","K1M","Kunjungan K1 murni"),("Encounter.identifier[0].value","K2","Kunjungan K2"),
 ("Encounter.identifier[0].value","K3","Kunjungan K3"),("Encounter.identifier[0].value","K4","Kunjungan K4"),("Encounter.identifier[0].value","K5","Kunjungan K5"),("Encounter.identifier[0].value","K6","Kunjungan K6")],
 "Metode PUT; Encounter.id = UUID dari POST kunjungan awal. Status K dikirim di setiap kunjungan ANC.","Setiap kunjungan")
T="17. Menutup episode kehamilan"
add(T,"Episode kehamilan","Tutup episode kehamilan","EpisodeOfCare",[("EpisodeOfCare.status","finished",""),("EpisodeOfCare.statusHistory[i].status","finished",""),
 ("EpisodeOfCare.period.end","Waktu berakhirnya kehamilan","Waktu persalinan / waktu keguguran atau kuret / hilang kontak: HPHT + 44 minggu (308 hari)"),
 ("EpisodeOfCare.statusHistory[i].period.end","Sama dengan period.end","")],"Metode PATCH (sejak v2.5; sebelumnya PUT).","Sekali per kehamilan")



PAT=("Patient/{IHS pasien}",""); ENC=("Encounter/{ID kunjungan}","")
EXTRA={
 "Permintaan & hasil laboratorium":[("*ServiceRequest.status","Status permintaan",""),("*ServiceRequest.intent","Intent permintaan",""),("*ServiceRequest.subject",)+PAT,("*ServiceRequest.encounter",)+ENC,("*ServiceRequest.performer","Practitioner / Organization pelaksana",""),
   ("*Specimen.status","Status spesimen",""),("*Specimen.subject",)+PAT,
   ("*DiagnosticReport.basedOn","ServiceRequest/{ID}","Laporan hasil lab"),("*DiagnosticReport.status","Status laporan",""),("*DiagnosticReport.code","Kode pemeriksaan",""),("*DiagnosticReport.subject",)+PAT,("*DiagnosticReport.encounter",)+ENC,("*DiagnosticReport.performer","Practitioner / Organization",""),("*DiagnosticReport.specimen","Specimen/{ID}",""),("*DiagnosticReport.result","Observation/{ID hasil}",""),
   ("*Observation.status","Status hasil",""),("*Observation.subject",)+PAT,("*Observation.encounter",)+ENC,("*Observation.value[x]","Nilai hasil","")],
 "Permintaan & hasil radiologi":[("*ServiceRequest.status","Status permintaan",""),("*ServiceRequest.intent","Intent permintaan",""),("*ServiceRequest.category","Kategori (radiologi)",""),("*ServiceRequest.subject",)+PAT,("*ServiceRequest.encounter",)+ENC,("*ServiceRequest.performer","Practitioner / Organization pelaksana",""),
   ("*ImagingStudy.identifier[i]","Accession number",""),("*ImagingStudy.status","Status studi",""),("*ImagingStudy.modality","Modalitas (mis. US)",""),("*ImagingStudy.subject",)+PAT,("*ImagingStudy.started","(DateTime)",""),("*ImagingStudy.basedOn","ServiceRequest/{ID}",""),("*ImagingStudy.endpoint","Endpoint NIDR",""),("*ImagingStudy.series.modality","Modalitas seri",""),
   ("*Observation.status","Status bacaan",""),("*Observation.subject",)+PAT,("*Observation.encounter",)+ENC,("*Observation.issued","(Instant)",""),("*Observation.performer","Practitioner/{IHS dokter radiologi}",""),
   ("*DiagnosticReport.basedOn / status / code / subject / encounter / performer / result / imagingStudy / conclusion","Laporan & kesimpulan radiologi","Semua wajib; rujuk modul")],
 "Diagnosis awal & akhir (primer / sekunder)":[("*Condition.subject",)+PAT,("*Condition.encounter",)+ENC],
 "Tindakan / prosedur medis":[("*Procedure.status","Status tindakan",""),("*Procedure.subject",)+PAT,("*Procedure.encounter",)+ENC,("*Procedure.performer[i].actor","Practitioner/{IHS nakes}","")],
 "Peresepan obat":[("*Medication.identifier[i]","ID obat internal",""),("*Medication.extension:medicationType","Jenis obat (non-racikan / racikan)",""),("*MedicationRequest.identifier[i]","No. resep",""),("*MedicationRequest.status","Status resep",""),("*MedicationRequest.intent","Intent resep",""),("*MedicationRequest.subject",)+PAT,("*MedicationRequest.substitution.allowed[x]","Boleh diganti / tidak","")],
 "Pengeluaran obat / obat dibawa pulang":[("*Medication.identifier[i]","ID obat internal",""),("*Medication.extension:medicationType","Jenis obat",""),("*MedicationDispense.identifier[i]","No. pengeluaran",""),("*MedicationDispense.status","Status pengeluaran",""),("*MedicationDispense.subject",)+PAT,("*MedicationDispense.context",)+ENC],
 "Rencana tindak lanjut & sarana transportasi rujuk":[("*ServiceRequest.status","Status",""),("*ServiceRequest.intent","Intent",""),("*ServiceRequest.subject",)+PAT,("*ServiceRequest.encounter",)+ENC],
 "Instruksi untuk tindak lanjut":[],
 "Kondisi saat meninggalkan RS / faskes":[("*Condition.subject",)+PAT,("*Condition.encounter",)+ENC],
}
for x in V:
    x["el"]=list(x["el"])+EXTRA.get(x["var"],[])

# ---------- post-processing: mandatory elements, stars, display split ----------
import re
REFS={"subject":"Patient/{IHS pasien}","patient":"Patient/{IHS pasien}","encounter":"Encounter/{ID kunjungan}","context":"Encounter/{ID kunjungan}"}
MAND={
 "Immunization":[("*Immunization.patient","Patient/{IHS pasien}",""),("*Immunization.encounter","Encounter/{ID kunjungan}",""),("*Immunization.expirationDate","(Date)","Tanggal kedaluwarsa vaksin"),("*Immunization.performer[i].function","Fungsi pelaksana","»Kode fungsi (mis. Administering Provider)"),("*Immunization.performer[i].actor","Practitioner/{IHS nakes}","")],
 "QuestionnaireResponse":[("*QuestionnaireResponse.status","completed",""),("*QuestionnaireResponse.subject","Patient/{IHS pasien}",""),("*QuestionnaireResponse.encounter","Encounter/{ID kunjungan}",""),("*QuestionnaireResponse.author","Practitioner/{IHS nakes}","Pengisi kuesioner"),("*QuestionnaireResponse.source","Patient/{IHS pasien}","Sumber jawaban"),("QuestionnaireResponse.authored","(DateTime)","Waktu pengisian")],
 "Condition":[("*Condition.subject","Patient/{IHS pasien}",""),("*Condition.encounter","Encounter/{ID kunjungan}","")],
 "Procedure":[("*Procedure.subject","Patient/{IHS pasien}",""),("*Procedure.encounter","Encounter/{ID kunjungan}",""),("*Procedure.performer[i].actor","Practitioner/{IHS nakes}","")],
}
STAR={"Immunization":["status","vaccineCode","occurrenceDateTime","primarySource","protocolApplied[0].doseNumber"],"QuestionnaireResponse":["item.item"],
 "Condition":["code"],"Procedure":["status","code"],"EpisodeOfCare":["status","type","patient","managingOrganization","period"],
 "ServiceRequest":["status","intent","code","subject","encounter","requester","performer"],"Specimen":["status","type","subject"],
 "MedicationRequest":["status","intent","medicationReference","subject","dosageInstruction.timing","dosageInstruction.route"],
 "MedicationDispense":["status","medicationReference","subject","context"],"Medication":["identifier"],
 "ImagingStudy":["series.uid","status","modality","subject"],"Encounter":["diagnosis","hospitalization.dischargeDisposition" if False else "status","period","identifier"]}
def starred(p):
    if p.startswith("*"): return p
    m=re.match(r"([A-Za-z]+)\.(.*)",p)
    if not m: return p
    r,rest=m.group(1),re.sub(r"\[i\]","",m.group(2))
    for k in STAR.get(r,[]):
        if rest==k or rest.startswith(k+".") or rest.startswith(k+"[") or rest.startswith(k+" "): return "*"+p
    return p
def split(p,v,k):
    if k.startswith("»"): return [(p,v,k[1:] if not k.startswith("»LIST") else "",) + (("icd",) if k=="»LIST:icd" else ())]
    if re.search(r"[cC]oding(\[\d\])?\.code$",p) and k:
        d,_,ket=k.partition(" — ")
        return [(p,v,""),(p[:-4]+"display",d,ket)]
    return [(p,v,k)]
for x in V:
    el=list(x["el"])
    for res,rows in MAND.items():
        if res in x["res"].split(" ")[0] or x["res"].startswith(res):
            have={re.sub(r"^\*","",e[0]) for e in el}
            add_front=[r for r in rows if r[0].endswith(".status") and r[0][1:] not in have and ("*"+r[0][1:]) not in have]
            add_back=[r for r in rows if not r[0].endswith(".status") and r[0].lstrip("*") not in have]
            if res=="Procedure" and not any(e[0].lstrip("*").startswith("Procedure.status") for e in el): add_front=[("*Procedure.status","completed","")]+add_front
            el=add_front+el+add_back
    out=[]
    for p,v,k in el: out+=split(starred(p),v,k)
    x["el"]=out

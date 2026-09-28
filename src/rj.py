# Resume Medis Rawat Jalan (SATUSEHAT) — dibangun dari playbook + lampiran rme-rawat-jalan1
LN="http://loinc.org"; SN="http://snomed.info/sct"; UC="http://unitsofmeasure.org"; HL="http://terminology.hl7.org/CodeSystem/"
OC=HL+"observation-category"; KFA="http://sys-ids.kemkes.go.id/kfa"; KM="http://terminology.kemkes.go.id"
CATD={"survey":"Survey","exam":"Exam","vital-signs":"Vital Signs","laboratory":"Laboratory","imaging":"Imaging","social-history":"Social History","therapy":"Therapy"}
V=[]
def add(tahap,kel,var,res,el,cat="",frek=""): V.append(dict(tahap=tahap,kel=kel,var=var,res=res,el=el,cat=cat,frek=frek))
def co(prefix,system,code,disp,ket=""):  # coding triple
    return [(prefix+".system",system,""),(prefix+".code",code,ket),(prefix+".display",disp,"")]
def opts(prefix,system,items):
    e=[(prefix+".system",system,"")]
    for it in items:
        e+=[(prefix+".code",it[0],it[2] if len(it)>2 else ""),(prefix+".display",it[1],"")]
    return e
OBSM=[("*Observation.subject","Patient/{IHS pasien}",""),("*Observation.encounter","Encounter/{ID kunjungan}",""),("Observation.effectiveDateTime","(DateTime)","Waktu pemeriksaan"),("*Observation.performer[i]","Practitioner/{IHS nakes}","")]
def obs(tahap,kel,var,cat,codes,value,extra=(),note="",frek=""):
    el=[("*Observation.status","final","Status hasil")]+co("Observation.category[0].coding[0]",OC,cat,CATD.get(cat,cat))
    for i,(s,c,d) in enumerate(codes): el+=[("*"+p,v,k) for p,v,k in co(f"Observation.code.coding[{i}]",s,c,d)]
    el+=OBSM+list(value)+list(extra)
    add(tahap,kel,var,"Observation",el,note,frek)
def qty(unit,code=None): return [("Observation.valueQuantity.value","(Decimal)","Nilai hasil"),("Observation.valueQuantity.unit",unit,""),("Observation.valueQuantity.system",UC,""),("Observation.valueQuantity.code",code or unit,"")]
PAT="Patient/{IHS pasien}"; ENC="Encounter/{ID kunjungan}"; PR="Practitioner/{IHS nakes}"
STR=[("Observation.valueString","(String)","Narasi temuan")]
STRNOTE="Di sumber tertulis Observation.valueQuantity.value (Tipe data String) — seharusnya valueString; di sini dinormalisasi ke valueString."

T="1. Pendaftaran pasien"
add(T,"Identitas pasien","Nomor SATUSEHAT (IHS) pasien","Patient",[("Patient.identifier[i]","Nomor IHS pasien","GET ke Master Patient Index (MPI)")],"Detail identitas mengikuti playbook MPI.","Sekali per pasien")
T="2. Pendaftaran kunjungan"
add(T,"Kunjungan","Kunjungan rawat jalan","Encounter",[
 ("*Encounter.identifier[i].system","http://sys-ids.kemkes.go.id/encounter/{Organization_ID}","Nomor kunjungan"),("*Encounter.identifier[i].value","(String)",""),
 ("*Encounter.status","arrived","Pasien datang namun belum bertemu dokter"),("*Encounter.status","in-progress","Pasien dalam proses pelayanan"),
 ("*Encounter.statusHistory[i].status / period","Riwayat status + waktu",""),
 ("*Encounter.class.system",HL+"v3-ActCode",""),("*Encounter.class.code","AMB","Jenis kunjungan"),("*Encounter.class.display","ambulatory",""),
 ("*Encounter.classHistory[i].class / period","Riwayat kelas kunjungan",""),
 ("Encounter.serviceType.coding","Lihat Lampiran Standar Terminologi","Tipe pelayanan"),
 ("*Encounter.subject",PAT,""),("*Encounter.participant[i].type / individual",PR,""),
 ("*Encounter.location","Location/{ID ruangan/poli}","Ruangan/poli"),
 ("Encounter.location.extension.serviceClass.value.valueCodeableConcept.coding.system",KM+"/CodeSystem/locationServiceClass-Outpatient","Kelas"),
 ("Encounter.location.extension.serviceClass.value.valueCodeableConcept.coding.code","reguler",""),("Encounter.location.extension.serviceClass.value.valueCodeableConcept.coding.display","Kelas Reguler",""),
 ("Encounter.location.extension.serviceClass.value.valueCodeableConcept.coding.code","eksekutif",""),("Encounter.location.extension.serviceClass.value.valueCodeableConcept.coding.display","Kelas Eksekutif",""),
 ("Encounter.location.extension.serviceClass.upgradeClassIndicator.valueCodeableConcept.coding.system",KM+"/CodeSystem/locationUpgradeClass","Perubahan kelas"),
 ("Encounter.location.extension.serviceClass.upgradeClassIndicator.valueCodeableConcept.coding.code","kelas-tetap",""),("Encounter.location.extension.serviceClass.upgradeClassIndicator.valueCodeableConcept.coding.display","Kelas Tetap Perawatan",""),
 ("Encounter.location.extension.serviceClass.upgradeClassIndicator.valueCodeableConcept.coding.code","naik-kelas",""),("Encounter.location.extension.serviceClass.upgradeClassIndicator.valueCodeableConcept.coding.display","Kenaikan Kelas Perawatan",""),
 ("Encounter.location.extension.serviceClass.upgradeClassIndicator.valueCodeableConcept.coding.code","turun-kelas",""),("Encounter.location.extension.serviceClass.upgradeClassIndicator.valueCodeableConcept.coding.display","Penurunan Kelas Perawatan",""),
 ("Encounter.location.extension.serviceClass.upgradeClassIndicator.valueCodeableConcept.coding.code","titip-rawat",""),("Encounter.location.extension.serviceClass.upgradeClassIndicator.valueCodeableConcept.coding.display","Titip Kelas Perawatan",""),
 ("*Encounter.period.start","(DateTime)","Tanggal & waktu masuk"),("*Encounter.diagnosis[i].condition","Condition/{ID}","Diisi saat selesai"),
 ("*Encounter.hospitalization.dischargeDisposition","Cara keluar / RTL","Diisi saat selesai"),("*Encounter.serviceProvider","Organization/{ID faskes}","")],
 "* = wajib (daftar wajib RJ juga memuat classHistory & dischargeDisposition, yang tidak wajib di ANC).","Setiap kunjungan")

T="3. Anamnesis"; K="Anamnesis"
CM=[("*Condition.subject",PAT,""),("*Condition.encounter",ENC,"")]
ECLCF="ECL: < 404684003 |Clinical finding|"
add(T,K,"Keluhan utama","Condition",co("Condition.category.coding",KM,"chief-complaint","Chief Complaint")+[("*Condition.code.coding.system",SN,""),("*Condition.code.coding.code",ECLCF,"Kode SNOMED keluhan"),("*Condition.code.coding.display","SNOMED CT Description",""),("Condition.onsetDateTime","(DateTime)","")]+CM+
 [("Encounter.diagnosis.condition","Condition/{ID keluhan utama}",""),("Encounter.diagnosis.use.coding.system",HL+"diagnosis-role",""),("Encounter.diagnosis.use.coding.code","CC",""),("Encounter.diagnosis.use.coding.display","Chief Complaint","")],
 "Saat PUT Encounter finished, sertakan Encounter.diagnosis untuk keluhan utama. Category system di sumber: http://terminology.kemkes.go.id (tanpa /CodeSystem/...).")
add(T,K,"Keluhan penyerta","Condition",co("Condition.category.coding",HL+"condition-category","problem-list-item","Problem List Item")+[("*Condition.code.coding.system",SN,""),("*Condition.code.coding.code",ECLCF,""),("*Condition.code.coding.display","SNOMED CT Description","")]+CM)
add(T,K,"Riwayat penyakit pribadi","Condition",co("Condition.category.coding",KM,"previous-condition","Previous Condition")+[("*Condition.code.coding.system",SN,""),("*Condition.code.coding.code","ECL: < 417662000 OR < 443508001","History / No history of clinical finding in subject"),("*Condition.code.coding.display","SNOMED CT Description","")]+
 opts("Condition.clinicalStatus.coding",HL+"condition-clinical",[("active","Active","masih berlangsung"),("inactive","Inactive","sudah berakhir")])+CM)
add(T,K,"Riwayat penyakit keluarga","FamilyMemberHistory",[("*FamilyMemberHistory.status","(status)",""),("*FamilyMemberHistory.patient",PAT,"")]+[("*"+p,v,k) for p,v,k in co("FamilyMemberHistory.relationship.coding",HL+"v3-RoleCode","FAMMEMB","Family member")]+
 [("*FamilyMemberHistory.condition.code.coding.system",SN,""),("*FamilyMemberHistory.condition.code.coding.code","ECL: < 416471007 OR < 160266009","Family history / No family history of clinical finding"),("*FamilyMemberHistory.condition.code.coding.display","SNOMED CT Description",""),
  ("FamilyMemberHistory.condition.outcome.system",SN,""),("FamilyMemberHistory.condition.outcome.code","ECL: < 418138009 |Patient condition finding|",""),("FamilyMemberHistory.condition.outcome.display","SNOMED CT Description",""),
  ("FamilyMemberHistory.condition.contributedToDeath","(Boolean)",""),("FamilyMemberHistory.condition.onset[x]","(Age | Range | Period | String)",""),("FamilyMemberHistory.deceasedBoolean","(Boolean)","Sumber tertulis 'deceasedbooelan'")])
add(T,K,"Riwayat alergi","AllergyIntolerance",[("*AllergyIntolerance.code.coding","Lihat Lampiran Standar Terminologi",""),
 ("*AllergyIntolerance.category","medication",""),("*AllergyIntolerance.category","food",""),("*AllergyIntolerance.category","environment",""),("*AllergyIntolerance.category","biologic",""),
 ("AllergyIntolerance.clinicalStatus.system",HL+"allergyintolerance-clinical",""),("AllergyIntolerance.clinicalStatus.code","active","Tampil: Ya"),("AllergyIntolerance.clinicalStatus.display","Active",""),("AllergyIntolerance.clinicalStatus.code","inactive","Tampil: Tidak"),("AllergyIntolerance.clinicalStatus.display","Inactive",""),
 ("*AllergyIntolerance.patient",PAT,""),("*AllergyIntolerance.encounter",ENC,""),("*AllergyIntolerance.recorder",PR,""),("*AllergyIntolerance.reaction[i].manifestation","Manifestasi reaksi","")])
add(T,K,"Riwayat pengobatan","MedicationStatement",[("*MedicationStatement.status","Lihat Lampiran Standar Terminologi",""),
 ("*MedicationStatement.medicationCodeableConcept.coding.system",KFA,""),("*MedicationStatement.medicationCodeableConcept.coding.code","93005512","Contoh: merk obat diketahui (kode produk KFA)"),("*MedicationStatement.medicationCodeableConcept.coding.display","Ampicillin Trihydrate 500 mg Tablet (PHARMA LABORATORIES)",""),
 ("*MedicationStatement.medicationCodeableConcept.coding.code","92001087","Contoh: merk tidak diketahui (kode generik KFA)"),("*MedicationStatement.medicationCodeableConcept.coding.display","Ampicillin Trihydrate 500 mg Tablet",""),
 ("MedicationStatement.note.text","(String)",""),("*MedicationStatement.subject",PAT,"")])

T="4. Pemeriksaan fisik"; K="Tanda vital"
obs(T,K,"Denyut jantung (nadi)","vital-signs",[(LN,"8867-4","Heart rate")],qty("beats/min","/min"))
obs(T,K,"Pernapasan","vital-signs",[(LN,"9279-1","Respiratory rate")],qty("breaths/min","/min"))
obs(T,K,"Tekanan darah sistolik","vital-signs",[(LN,"8480-6","Systolic blood pressure")],qty("mm[Hg]"))
obs(T,K,"Tekanan darah diastolik","vital-signs",[(LN,"8462-4","Diastolic blood pressure")],qty("mm[Hg]"))
obs(T,K,"Suhu tubuh","vital-signs",[(LN,"8310-5","Body temperature")],qty("C","Cel"))
obs(T,"Tingkat kesadaran","Tingkat kesadaran","exam",[(LN,"67775-7","Level of responsiveness")],opts("Observation.valueCodeableConcept.coding[0]",SN,[("248234008","Mentally alert","Sadar baik / Alert"),("300202002","Response to voice","Berespon dengan kata-kata / Voice"),("450847001","Responds to pain","Respons hanya jika dirangsang nyeri / Pain"),("422768004","Unresponsive","Tidak sadar / Unresponsive"),("130987000","Acute confusion","Gelisah atau bingung"),("2776000","Delirium","Acute Confusional States")]))
K="Head to toe"
for v,codes in [("Kepala",[(LN,"10199-8","Physical findings of Head Narrative")]),("Mata",[(LN,"10197-2","Physical findings of Eye Narrative")]),("Telinga",[(LN,"10195-6","Physical findings of Ear Narrative")]),
 ("Hidung",[(LN,"10203-8","Physical findings of Nose Narrative")]),("Rambut",[(LN,"32436-8","Physical findings of Hair")]),("Bibir",[(LN,"32446-7","Physical findings of Lip")]),
 ("Gigi geligi",[(LN,"85910-8","Physical findings of Teeth and Gum Narrative")]),("Lidah",[(LN,"32483-0","Physical findings of Tongue")]),
 ("Langit-langit",[(LN,"10201-2","Physical findings of Mouth and Throat and Teeth Narrative"),(SN,"72914001","Palatal structure")]),("Leher",[(LN,"11411-6","Physical findings of Neck Narrative")]),
 ("Tenggorokan",[(LN,"56867-5","Physical findings of Throat Narrative")]),("Tonsil",[(LN,"10201-2","Physical findings of Mouth and Throat and Teeth Narrative"),(SN,"91636008","Bilateral palatine tonsils")]),
 ("Dada",[(LN,"11391-0","Physical findings of Chest Narrative")]),("Payudara",[(LN,"10193-1","Physical findings of Breasts Narrative")]),("Punggung",[(LN,"10192-3","Physical findings of Back Narrative")]),
 ("Perut",[(LN,"10191-5","Physical findings of Abdomen Narrative")]),("Genital",[(LN,"11400-9","Physical findings of Genitalia Narrative")]),
 ("Anus / dubur",[(LN,"11388-6","Physical findings of Buttocks Narrative"),(SN,"53505006","Anal structure")]),("Lengan atas",[(LN,"11386-0","Physical findings of Upper Arm Narrative")]),
 ("Lengan bawah",[(LN,"11398-5","Physical findings of Forearm Narrative")]),("Jari tangan",[(LN,"11404-1","Physical findings of Hand Narrative"),(SN,"7569003","Finger structure")]),
 ("Kuku tangan",[(LN,"32456-6","Physical findings of Nail"),(SN,"770812000","Entire nail unit of finger")]),("Persendian tangan",[(LN,"11415-7","Physical findings of Wrist Narrative")]),
 ("Tungkai atas",[(LN,"11414-0","Physical findings of Thigh Narrative")]),("Tungkai bawah",[(LN,"11389-4","Physical findings of Calf Narrative")]),
 ("Jari kaki",[(LN,"11397-7","Physical findings of Foot Narrative"),(SN,"29707007","Toe structure")]),("Kuku kaki",[(LN,"32456-6","Physical findings of Nail"),(SN,"770805009","Structure of nail unit of toe")]),
 ("Persendian kaki",[(LN,"11385-2","Physical findings of Ankle Narrative"),(SN,"26552008","Foot joint structure")])]:
    obs(T,K,v,"exam",codes,STR,note=STRNOTE)
K="Antropometri"
obs(T,K,"Tinggi badan","vital-signs",[(LN,"8302-2","Body height")],qty("cm"))
obs(T,K,"Berat badan","vital-signs",[(LN,"29463-7","Body weight")],qty("kg"))
obs(T,K,"Luas permukaan tubuh (anak)","vital-signs",[(LN,"8277-6","Body surface area")],qty("m²"))
T="5. Pemeriksaan fungsional"
obs(T,"Fungsional","Status psikologis","survey",[(LN,"8693-4","Mental Status")],opts("Observation.valueCodeableConcept.coding[0]",SN,[("17326005","Well in self","Tidak ada kelainan"),("48694002","Feeling anxious","Cemas"),("1402001","Afraid","Takut"),("75408008","Feeling angry","Marah"),("420038007","Feeling unhappy","Sedih"),("74964007","Other","Lain-lain (free text)")])+[("Observation.valueCodeableConcept.text","(String)","Isian bebas untuk 'Lain-lain'")])
T="6. Riwayat perjalanan penyakit"
CIM=[("*ClinicalImpression.status","(status)",""),("*ClinicalImpression.subject",PAT,""),("*ClinicalImpression.encounter",ENC,""),("*ClinicalImpression.investigation.code","Kode investigasi","wajib menurut pemetaan nilai"),("*ClinicalImpression.prognosisCodeableConcept","Prognosis","wajib menurut pemetaan nilai")]
add(T,"Riwayat penyakit","Riwayat perjalanan penyakit","ClinicalImpression",CIM[:1]+co("ClinicalImpression.code.coding",SN,"312850006","History of disorder")+[("ClinicalImpression.summary","(String)","Narasi perjalanan penyakit")]+CIM[1:])
T="7. Tujuan perawatan"
add(T,"Tujuan","Tujuan perawatan","Goal",[("*Goal.lifecycleStatus","planned",""),("Goal.achievementStatus.system",HL+"goal-achievement",""),("Goal.achievementStatus.code","Kode ketercapaian tujuan","Lihat Lampiran Standar Terminologi"),("Goal.achievementStatus.display","Deskripsi ketercapaian","")]+
 co("Goal.category.coding",HL+"goal-category","nursing","Nursing")+[("Goal.addresses","Condition/{ID}",""),("*Goal.description.coding.system",SN,""),("*Goal.description.coding.code",ECLCF,""),("*Goal.description.coding.display","SNOMED CT Description",""),
 ("Goal.outcomeCode.system",SN,""),("Goal.outcomeCode.code","ECL: < 390800000 |Goal achievement finding|",""),("Goal.outcomeCode.display","SNOMED CT Description",""),("Goal.outcomeReference","Observation/{ID}",""),
 ("Goal.target.measure.system",LN,""),("Goal.target.measure.code","LOINC Code","Lihat Lampiran Standar Terminologi"),("Goal.target.measure.display","LOINC Description",""),
 ("Goal.target.detail[x]","(Quantity | Range | CodeableConcept | String | Boolean | Integer | Ratio)",""),("Goal.target.dueDate","(DateTime)",""),("Goal.expressedBy",PR,""),("*Goal.subject",PAT,"")])

T="8. Rencana rawat pasien"
CPM=[("*CarePlan.status","(status)",""),("*CarePlan.intent","(intent)",""),("*CarePlan.title","(String)","Judul rencana")]
CPE=[("*CarePlan.subject",PAT,""),("*CarePlan.encounter",ENC,""),("*CarePlan.author",PR,""),("*CarePlan.activity[i].detail.status","(status aktivitas)","")]
add(T,"Rencana rawat","Rencana rawat","CarePlan",CPM+co("CarePlan.category.coding",SN,"736271009","Outpatient care plan")+[("*CarePlan.description","(String)","Rencana terapi, tindakan, lama rawat"),("CarePlan.goal","Goal/{ID}","")]+CPE)
T="9. Instruksi medik & keperawatan"
add(T,"Instruksi","Instruksi medik dan keperawatan","CarePlan",CPM+co("CarePlan.category.coding",SN,"736271009","Outpatient care plan")+[("*CarePlan.description","(String)","Instruksi medik/keperawatan")]+CPE,"Kategori sama dengan Rencana rawat (736271009); pembeda hanya isi description.")

T="10. Pemeriksaan penunjang laboratorium"; K="Laboratorium"
SRM=[("*ServiceRequest.status","(status)",""),("*ServiceRequest.intent","(intent)","")]
add(T,K,"Permintaan pemeriksaan laboratorium","ServiceRequest",SRM+[("ServiceRequest.identifier.system","http://sys-ids.kemkes.go.id/servicerequest/{Organization_ID}","Nomor permintaan"),("ServiceRequest.identifier.value","(String)","")]+
 co("ServiceRequest.category.coding",SN,"108252007","Laboratory procedure")+
 [("*ServiceRequest.code.coding.system",LN,""),("*ServiceRequest.code.coding.code","LOINC Code","Lihat Lampiran LOINC Laboratorium (kategori Permintaan / Permintaan & Hasil)"),("*ServiceRequest.code.coding.display","LOINC Description",""),
  ("*ServiceRequest.code.coding.system",KM+"/CodeSystem/kptl",""),("*ServiceRequest.code.coding.code","Kode KPTL","Sepadan dengan kode LOINC"),("*ServiceRequest.code.coding.display","Deskripsi KPTL",""),
  ("*ServiceRequest.subject",PAT,""),("*ServiceRequest.encounter",ENC,"Juga sumber nama faskes & unit pengirim"),("ServiceRequest.authoredOn","(DateTime)","Waktu permintaan"),
  ("*ServiceRequest.requester",PR,"Dokter pengirim (no. telepon ditarik dari data Practitioner)"),("*ServiceRequest.performer","Practitioner / Organization pelaksana",""),
  ("ServiceRequest.priority","stat","CITO"),("ServiceRequest.priority","routine","Non CITO"),("ServiceRequest.reasonReference","Condition/{ID}","Diagnosis/masalah (atau reasonCode)"),
  ("ServiceRequest.note","(String)","Catatan permintaan"),("ServiceRequest.supportingInfo","Procedure/{ID status puasa}","")],"1 ServiceRequest = 1 kode pemeriksaan/panel.")
FAST=[("*Procedure.status","done","Puasa"),("*Procedure.status","not-done","Tidak puasa")]+co("Procedure.category.coding",SN,"103693007","Diagnostic procedure")+[("*"+p,v,k) for p,v,k in co("Procedure.code.coding",SN,"792805006","Fasting")]+[("*Procedure.subject",PAT,""),("*Procedure.encounter",ENC,""),("*Procedure.performer[i].actor",PR,"")]
add(T,K,"Status puasa pasien","Procedure + Specimen",FAST+opts("Specimen.collection.fastingStatusCodeableConcept.coding",HL+"v2-0916",[("F","Patient was fasting prior to the procedure.","Puasa"),("NF","The patient indicated they did not fast prior to the procedure.","Tidak puasa")]),"Dikirim dua cara: Procedure (dirujuk dari ServiceRequest.supportingInfo) dan/atau Specimen.collection.fastingStatus.")
add(T,K,"Spesimen laboratorium","Specimen + Substance",[("*Specimen.status","(status)",""),("*Specimen.type.coding.system",SN,"Asal sumber spesimen"),("*Specimen.type.coding.code","ECL: < 123038009 |Specimen|",""),("*Specimen.type.coding.display","SNOMED CT Description",""),("*Specimen.subject",PAT,""),
 ("Specimen.collection.bodySite.coding.system",SN,"Lokasi pengambilan"),("Specimen.collection.bodySite.coding.code","ECL: < 123037004 |Body structure|",""),("Specimen.collection.bodySite.coding.display","SNOMED CT Description",""),
 ("Specimen.collection.quantity.value","(Decimal)","Jumlah & volume"),("Specimen.collection.quantity.unit","UCUM unit",""),("Specimen.collection.quantity.system",UC,""),("Specimen.collection.quantity.code","UCUM code",""),
 ("Specimen.collection.method.coding.system",SN,"Metode pengambilan"),("Specimen.collection.method.coding.code","ECL: < 118292001 |Removal|",""),("Specimen.collection.method.coding.display","SNOMED CT Description",""),
 ("Specimen.collection.collectedDateTime","(DateTime)","Waktu pengambilan"),("Specimen.condition.text","(String)","Kondisi spesimen saat diambil (sumber: condition.coding.text)"),
 ("Specimen.processing.procedure.coding.system",SN,"Fiksasi"),("Specimen.processing.procedure.coding.code","787378005",""),("Specimen.processing.procedure.coding.display","Fixation of specimen",""),("Specimen.processing.timeDateTime","(DateTime)","Waktu fiksasi"),
 ("Specimen.processing.additive","Substance/{ID}","Cairan fiksasi"),("*Substance.status","(status)",""),("*Substance.category","(kategori)",""),("*Substance.code.coding.system",KFA,""),("*Substance.code.coding.code","Kode alkes KFA","Sementara: 32999999 (virtual) / 33999999 (aktual)"),("*Substance.code.coding.display","Nama alat kesehatan",""),
 ("Substance.instance.quantity.value","(Decimal)","Volume cairan fiksasi"),("Substance.instance.quantity.unit","mL",""),("Substance.instance.quantity.system",UC,""),("Substance.instance.quantity.code","mL",""),
 ("Specimen.collection.collector",PR,"Petugas pengambil"),("Specimen.extension:transportedPerson.valueContactDetail.name","(String)","Petugas pengantar"),("Specimen.extension:receivedPerson.valueReference",PR,"Petugas penerima"),
 ("Specimen.processing.procedure.coding.system",SN,"Prosedur pemeriksaan/pengolahan"),("Specimen.processing.procedure.coding.code","ECL: ≤ 9265001 |Specimen processing|",""),("Specimen.processing.procedure.coding.display","SNOMED CT Description",""),("Specimen.processing.timeDateTime","(DateTime)","Waktu pemeriksaan/pengolahan")],"1 Specimen = 1 jenis spesimen.")
add(T,K,"Hasil pemeriksaan laboratorium","Observation",[("*Observation.status","(status)","")]+co("Observation.category.coding",OC,"laboratory","Laboratory")+
 [("*Observation.code.coding.system",LN,""),("*Observation.code.coding.code","LOINC Code","Lihat Lampiran LOINC Laboratorium"),("*Observation.code.coding.display","LOINC Description",""),("*Observation.subject",PAT,""),("*Observation.encounter",ENC,""),
  ("*Observation.value[x]","Sesuai tipe hasil","valueCodeableConcept untuk nominal/ordinal, valueQuantity untuk kuantitatif, dst."),
  ("Observation.interpretation.coding.system",HL+"v3-ObservationInterpretation","Normal/tidak normal & interpretasi"),("Observation.interpretation.coding.code","Kode interpretasi",""),("Observation.interpretation.coding.display","Deskripsi interpretasi","Sumber menulis .value, seharusnya .display"),
  ("Observation.referenceRange","Nilai rujukan & nilai kritis","Direkomendasikan selalu diisi"),("*Observation.performer","Practitioner/{ID}","Analis, validator, dokter penginterpretasi"),("*Observation.performer","Organization/{ID}","Faskes pemeriksa"),
  ("Observation.effectiveDateTime","(DateTime)","Waktu hasil keluar dari lab"),("Observation.issued","(DateTime)","Waktu hasil diterima unit pengirim")],"1 Observation = 1 parameter hasil.")
DRM=[("*DiagnosticReport.status","(status)",""),("*DiagnosticReport.subject",PAT,""),("*DiagnosticReport.encounter",ENC,""),("*DiagnosticReport.performer","Practitioner / Organization","")]
add(T,K,"Laporan pemeriksaan laboratorium","DiagnosticReport",DRM[:1]+[("DiagnosticReport.category.coding.system",HL+"v2-0074",""),("DiagnosticReport.category.coding.code","Kode kategori laporan","Lihat Lampiran Standar Terminologi"),("DiagnosticReport.category.coding.display","Deskripsi kategori",""),
 ("*DiagnosticReport.code.coding.system",LN,""),("*DiagnosticReport.code.coding.code","LOINC Code","Sama dengan ServiceRequest.code"),("*DiagnosticReport.code.coding.display","LOINC Description",""),
 ("*DiagnosticReport.result","Observation/{ID}",""),("*DiagnosticReport.specimen","Specimen/{ID}",""),("*DiagnosticReport.basedOn","ServiceRequest/{ID}",""),("DiagnosticReport.conclusionCode","Kode kesimpulan","FHIR / SNOMED / Kemkes"),("DiagnosticReport.conclusion","(String)","")]+DRM[1:])

T="11. Pemeriksaan penunjang radiologi"; K="Radiologi"
add(T,K,"Permintaan pemeriksaan radiologi","ServiceRequest",SRM+[("ServiceRequest.identifier[0].system","http://sys-ids.kemkes.go.id/servicerequest/{Organization_ID}","Nomor permintaan"),("ServiceRequest.identifier[0].value","(String)",""),
 ("ServiceRequest.identifier[1].type.coding.system",HL+"v2-0203",""),("ServiceRequest.identifier[1].type.coding.code","ACSN","Accession number"),("ServiceRequest.identifier[1].system","http://sys-ids.kemkes.go.id/acsn/{Organization_ID}",""),("ServiceRequest.identifier[1].value","(String)","")]+
 [("*"+p,v,k) for p,v,k in co("ServiceRequest.category.coding",SN,"363679005","Imaging")]+
 [("*ServiceRequest.code.coding.system",LN,""),("*ServiceRequest.code.coding.code","LOINC Code","Lihat Terminologi Radiologi"),("*ServiceRequest.code.coding.display","LOINC Description",""),
  ("*ServiceRequest.code.coding.system",KM+"/CodeSystem/kptl",""),("*ServiceRequest.code.coding.code","Kode KPTL",""),("*ServiceRequest.code.coding.display","Deskripsi KPTL",""),
  ("*ServiceRequest.subject",PAT,""),("*ServiceRequest.encounter",ENC,""),("ServiceRequest.authoredOn","(DateTime)",""),("*ServiceRequest.requester",PR,"Dokter pengirim"),("*ServiceRequest.performer","Practitioner / Organization",""),
  ("ServiceRequest.priority","stat","CITO"),("ServiceRequest.priority","routine","Non CITO"),("ServiceRequest.reasonReference","Condition/{ID}","Diagnosis kerja"),("ServiceRequest.note","(String)",""),
  ("ServiceRequest.supportingInfo","AllergyIntolerance / Observation / Procedure","Alergi kontras, status kehamilan, status puasa"),("ServiceRequest.occurrenceDateTime","(DateTime)","Waktu pemeriksaan"),
  ("ServiceRequest.orderDetail.coding.system",KFA,"Jenis bahan kontras"),("ServiceRequest.orderDetail.coding.code","Kode KFA",""),("ServiceRequest.orderDetail.coding.display","Deskripsi KFA",""),
  ("ServiceRequest.orderDetail[0].coding.system","http://dicom.nema.org/resources/ontology/DCM","Modalitas"),("ServiceRequest.orderDetail[0].coding.code","Kode DICOM (mis. US)",""),
  ("ServiceRequest.orderDetail[1].coding.system","http://sys-ids.kemkes.go.id/ae-title","AE Title"),("ServiceRequest.orderDetail[1].coding.display","(String)","")])
add(T,K,"Status alergi bahan kontras","AllergyIntolerance",[("*AllergyIntolerance.category","medication",""),("*AllergyIntolerance.code.coding","Lihat Lampiran Standar Terminologi",""),("*AllergyIntolerance.patient",PAT,""),("*AllergyIntolerance.encounter",ENC,""),("*AllergyIntolerance.recorder",PR,""),("*AllergyIntolerance.reaction[i].manifestation","Manifestasi","")])
add(T,K,"Status kehamilan","Observation",[("*Observation.status","final","")]+co("Observation.category.coding",SN,"survey","Survey","Sumber menulis system SNOMED untuk kode 'survey' — seharusnya observation-category")+
 [("*"+p,v,k) for p,v,k in co("Observation.code.coding",LN,"82810-3","Pregnancy status")]+OBSM+opts("Observation.valueCodeableConcept.coding",SN,[("77386006","Pregnancy","Hamil"),("60001007","Not pregnant","Tidak hamil")]))
add(T,K,"Status puasa (radiologi)","Procedure",FAST)
add(T,K,"Citra DICOM","ImagingStudy",[("*ImagingStudy.identifier[i]","Accession number",""),("*ImagingStudy.status","(status)",""),("*ImagingStudy.modality","Kode DICOM",""),("*ImagingStudy.subject",PAT,""),("*ImagingStudy.started","(DateTime)",""),
 ("*ImagingStudy.basedOn","ServiceRequest/{ID}",""),("*ImagingStudy.endpoint","Endpoint NIDR (WADO URL)",""),("*ImagingStudy.series.uid","DICOM Series Instance UID",""),("*ImagingStudy.series.modality","Kode DICOM",""),("ImagingStudy.interpreter",PR,"Dokter penginterpretasi")],"Dikirim oleh DICOM router ke NIDR.")
add(T,K,"Hasil (bacaan) radiologi","Observation",[("*Observation.status","(status)","")]+co("Observation.category.coding",OC,"imaging","Imaging")+[("*Observation.code.coding.system",LN,""),("*Observation.code.coding.code","LOINC Code",""),("*Observation.code.coding.display","LOINC Description",""),
 ("*Observation.subject",PAT,""),("*Observation.encounter",ENC,""),("*Observation.issued","(Instant)",""),("*Observation.performer",PR,""),("Observation.derivedFrom","ImagingStudy/{ID}",""),("*Observation.valueString","(String)","Bacaan hasil")])
add(T,K,"Laporan / kesimpulan radiologi","DiagnosticReport",DRM[:1]+[("DiagnosticReport.category.coding.system",HL+"v2-0074",""),("DiagnosticReport.category.coding.code","Kode kategori laporan",""),("DiagnosticReport.category.coding.display","Deskripsi kategori",""),
 ("*DiagnosticReport.code.coding.system",LN,""),("*DiagnosticReport.code.coding.code","LOINC Code","Sama dengan ServiceRequest.code"),("*DiagnosticReport.code.coding.display","LOINC Description",""),
 ("*DiagnosticReport.result","Observation/{ID}",""),("*DiagnosticReport.imagingStudy","ImagingStudy/{ID}",""),("*DiagnosticReport.basedOn","ServiceRequest/{ID}",""),("DiagnosticReport.conclusionCode","Kode kesimpulan",""),("*DiagnosticReport.conclusion","(String)","")]+DRM[1:])
T="12. Rasional klinis"
add(T,"Rasional klinis","Rasional klinis","ClinicalImpression",CIM[:1]+co("ClinicalImpression.code.coding",KM,"TK000056","Rasional Klinis")+[("ClinicalImpression.summary","(String)","Dasar penegakan diagnosis"),
 ("ClinicalImpression.investigation.item","Observation | QuestionnaireResponse | FamilyMemberHistory | DiagnosticReport | RiskAssessment | ImagingStudy",""),("ClinicalImpression.problem","Condition | AllergyIntolerance","")]+CIM[1:])

T="13. Diagnosis"
add(T,"Diagnosis","Diagnosis","Condition",co("Condition.category.coding",HL+"condition-category","encounter-diagnosis","Encounter Diagnosis")+
 [("*Condition.code.coding[0].system","http://hl7.org/fhir/sid/icd-10",""),("*Condition.code.coding[0].code","Kode ICD-10",""),("*Condition.code.coding[0].display","ICD-10 Description",""),
  ("*Condition.code.coding[1].system",SN,"Padanan SNOMED"),("*Condition.code.coding[1].code",ECLCF,""),("*Condition.code.coding[1].display","SNOMED CT Description",""),
  ("Condition.stage.assessment","ClinicalImpression/{ID rasional klinis}","")]+CM+
 [("*Encounter.diagnosis[i].condition","Condition/{ID}","Saat PUT Encounter finished"),("Encounter.diagnosis[i].use","Peran diagnosis",""),("Encounter.diagnosis[i].rank","1 = primer, 2+ = sekunder","")],"1 Condition = 1 diagnosis (ICD-10 + padanan SNOMED).")
T="14. Penilaian risiko"
add(T,"Risiko","Penilaian risiko","RiskAssessment",[("*RiskAssessment.status","(status)",""),("RiskAssessment.code.coding.system",SN,""),("RiskAssessment.code.coding.code","ECL: < 225338004 |Risk assessment|",""),("RiskAssessment.code.coding.display","SNOMED CT Description",""),
 ("*RiskAssessment.subject",PAT,""),("RiskAssessment.condition","Condition/{ID diagnosis}",""),("RiskAssessment.reasonReference","Condition / Observation",""),
 ("RiskAssessment.prediction.outcome.coding.system",SN,""),("RiskAssessment.prediction.outcome.coding.code","ECL: < 64572001 |Disease|",""),("RiskAssessment.prediction.outcome.coding.display","SNOMED CT Description",""),
 ("RiskAssessment.prediction.probabilityDecimal","(Decimal)",""),("RiskAssessment.prediction.qualitativeRisk.coding.system",HL+"risk-probability",""),("RiskAssessment.prediction.qualitativeRisk.coding.code","Kode risiko kualitatif",""),("RiskAssessment.prediction.qualitativeRisk.coding.display","Deskripsi",""),
 ("RiskAssessment.prediction.relativeRisk","(Decimal)",""),("RiskAssessment.prediction.whenPeriod.start / end","(DateTime)",""),("RiskAssessment.prediction.whenRange.low / high","(Quantity)",""),
 ("RiskAssessment.mitigation","(String)",""),("RiskAssessment.note","(String)",""),("ClinicalImpression.prognosisReference","RiskAssessment/{ID}","Ditambahkan pada Rasional Klinis")],"Sumber banyak menulis 'RiskAssesment' (typo) dan judul tabel 'Resource Procedure'.")
T="15. Tindakan / prosedur medis"; K="Tindakan"
add(T,K,"Permintaan tindakan","ServiceRequest",SRM+[("ServiceRequest.category.coding.system",SN,""),("ServiceRequest.category.coding.code","Kode kategori pemeriksaan","Lihat Lampiran Standar Terminologi"),("ServiceRequest.category.coding.display","SNOMED CT Description",""),
 ("*ServiceRequest.code.coding.system","http://hl7.org/fhir/sid/icd-9-cm",""),("*ServiceRequest.code.coding.code","Kode ICD-9-CM",""),("*ServiceRequest.code.coding.display","ICD-9-CM Description",""),
 ("*ServiceRequest.code.coding.system",KM+"/CodeSystem/kptl",""),("*ServiceRequest.code.coding.code","Kode KPTL","Sepadan dengan ICD-9-CM"),("*ServiceRequest.code.coding.display","Deskripsi KPTL",""),
 ("*ServiceRequest.subject",PAT,""),("*ServiceRequest.encounter",ENC,""),("*ServiceRequest.requester",PR,""),("*ServiceRequest.performer","Practitioner / Organization","")])
add(T,K,"Pelaksanaan tindakan","Procedure",[("*Procedure.status","(status)",""),("Procedure.category.coding.system",SN,""),("Procedure.category.coding.code","ECL: < 71388002 |Procedure|",""),("Procedure.category.coding.display","SNOMED CT Description",""),
 ("*Procedure.code.coding[0].system","http://hl7.org/fhir/sid/icd-9-cm",""),("*Procedure.code.coding[0].code","Kode ICD-9-CM","Nama tindakan"),("*Procedure.code.coding[0].display","ICD-9-CM Description",""),
 ("*Procedure.code.coding[1].system",SN,""),("*Procedure.code.coding[1].code","ECL: < 71388002 |Procedure|",""),("*Procedure.code.coding[1].display","SNOMED CT Description",""),
 ("*Procedure.subject",PAT,""),("*Procedure.encounter",ENC,""),("*Procedure.performer[i].actor",PR,"Petugas pelaksana"),("Procedure.performedPeriod.start","(DateTime)",""),("Procedure.performedPeriod.end","(DateTime)",""),
 ("Procedure.usedCode.coding.system",KFA,"Farmasi & alat medis yang digunakan"),("Procedure.usedCode.coding.code","Kode KFA","Alkes sementara: 32999999 / 33999999"),("Procedure.usedCode.coding.display","Deskripsi KFA",""),
 ("*Procedure.focalDevice[i].manipulated","Device/{ID}","Wajib menurut pemetaan nilai")],"Hasil tindakan diagnostik dikirim via Observation (mengikuti ketentuan lab/radiologi).")
T="16. Peresepan obat"; K="Farmasi"
add(T,K,"Peresepan obat","Medication + MedicationRequest",[("*Medication.identifier[i]","ID obat lokal",""),("*Medication.extension:medicationType","Jenis obat (NC non-racikan / racikan)",""),
 ("Medication.code.coding.system",KFA,""),("Medication.code.coding.code","Kode obat KFA","ID & nama obat (92/93/94xxxxxx)"),("Medication.code.coding.display","Nama obat KFA",""),
 ("Medication.form.coding.system",KM+"/CodeSystem/medication-form",""),("Medication.form.coding.code","Kode bentuk/sediaan",""),("Medication.form.coding.display","Deskripsi sediaan",""),
 ("Medication.ingredient.itemCodeableConcept.coding","Kode KFA zat aktif / produk","Wajib untuk obat racikan"),("Medication.ingredient.strength.numerator / denominator","Kekuatan (UCUM / v3-orderableDrugForm)","mis. 500 mg / 1 TAB"),
 ("*MedicationRequest.identifier.system","http://sys-ids.kemkes.go.id/prescription/{Organization_ID}","Nomor resep"),("*MedicationRequest.identifier.use","official",""),("*MedicationRequest.identifier.value","Nomor lokal resep",""),
 ("*MedicationRequest.identifier.system","http://sys-ids.kemkes.go.id/prescription-item/{Organization_ID}","Nomor per-item obat"),("*MedicationRequest.identifier.value","Nomor lokal item",""),
 ("*MedicationRequest.status","Kode status resep","FHIR terminology"),("*MedicationRequest.intent","(intent)",""),("*MedicationRequest.medicationReference","Medication/{ID}",""),("*MedicationRequest.subject",PAT,""),
 ("MedicationRequest.dispenseRequest.quantity.value","(Decimal)","Jumlah obat"),("MedicationRequest.dispenseRequest.quantity.unit / system / code","UCUM",""),
 ("*MedicationRequest.dosageInstruction[i].route.coding.system","http://www.whocc.no/atc","Rute pemberian"),("*MedicationRequest.dosageInstruction[i].route.coding.code","Kode rute WHO ATC",""),("*MedicationRequest.dosageInstruction[i].route.coding.display","Deskripsi rute",""),
 ("MedicationRequest.dosageInstruction.doseAndRate.doseQuantity.value","(Decimal)","Dosis"),("MedicationRequest.dosageInstruction.doseAndRate.doseQuantity.unit","UCUM unit","Unit"),
 ("*MedicationRequest.dosageInstruction[i].timing.repeat","frequency / period / periodUnit / when …","Frekuensi (mis. TID = 3 per 1 d)"),
 ("MedicationRequest.dosageInstruction.additionalInstruction.coding.system",SN,"Aturan tambahan"),("MedicationRequest.dosageInstruction.additionalInstruction.coding.code","ECL: < 419492006 |Additional dosage instructions|",""),("MedicationRequest.dosageInstruction.additionalInstruction.coding.display","SNOMED CT Description",""),("MedicationRequest.dosageInstruction.additionalInstruction.text","(String)",""),
 ("MedicationRequest.note","(String)","Catatan resep"),("MedicationRequest.requester",PR,"Dokter penulis resep"),("MedicationRequest.authoredOn","(DateTime)","Tanggal & jam penulisan"),("*MedicationRequest.substitution.allowed[x]","(Boolean)","")],
 "Bisa 2× POST (Medication + MedicationRequest) atau 1× POST dengan Medication di contained.")
T="17. Pengkajian resep"; K="Farmasi"
el=[("*QuestionnaireResponse.status","completed",""),("QuestionnaireResponse.questionnaire","https://fhir.kemkes.go.id/Questionnaire/Q0007","")]
for g,items in [("1","Persyaratan administrasi",),("2","Persyaratan farmasetik"),("3","Persyaratan klinis")] if False else []: pass
ADM=["Nama, umur, jenis kelamin, BB & TB pasien","Nama, nomor ijin, alamat & paraf dokter","Tanggal resep","Ruangan/unit asal resep"]
FAR=["Nama obat, bentuk & kekuatan sediaan","Dosis & jumlah obat","Stabilitas","Aturan & cara penggunaan"]
KLI=["Duplikasi pengobatan","Alergi & ROTD","Kontraindikasi","Interaksi obat"]
for grp,lst in [("Persyaratan administrasi",ADM),("Persyaratan farmasetik",FAR)]:
    el.append(("QuestionnaireResponse.item.text",grp,"grup"))
    for i,t in enumerate(lst,1):
        el+=[("*QuestionnaireResponse.item.item.linkId",str(i),t),("*QuestionnaireResponse.item.item.answer.valueCoding.system",KM+"/CodeSystem/clinical-term",""),
             ("*QuestionnaireResponse.item.item.answer.valueCoding.code","OV000052",""),("*QuestionnaireResponse.item.item.answer.valueCoding.display","Sesuai",""),
             ("*QuestionnaireResponse.item.item.answer.valueCoding.code","OV000053",""),("*QuestionnaireResponse.item.item.answer.valueCoding.display","Tidak Sesuai",""),
             ("QuestionnaireResponse.item.item.answer.valueString","(String)","Keterangan")]
el.append(("QuestionnaireResponse.item.text","Persyaratan klinis","grup"))
el+=[("*QuestionnaireResponse.item.item.linkId","1","Ketepatan indikasi, dosis & waktu penggunaan"),("*QuestionnaireResponse.item.item.answer.valueCoding.code","OV000052 / OV000053","Sesuai / Tidak Sesuai")]
for i,t in enumerate(KLI,2): el+=[("*QuestionnaireResponse.item.item.linkId",str(i),t),("*QuestionnaireResponse.item.item.answer.valueBoolean","true / false","Ya / Tidak"),("QuestionnaireResponse.item.item.answer.valueString","(String)","Keterangan")]
el+=[("QuestionnaireResponse.item.linkId","4","Resep yang dikaji"),("QuestionnaireResponse.item.answer.valueReference","MedicationRequest/{ID}",""),
     ("*QuestionnaireResponse.subject",PAT,""),("*QuestionnaireResponse.encounter",ENC,""),("*QuestionnaireResponse.author",PR,"Apoteker"),("*QuestionnaireResponse.source",PAT,"")]
add(T,K,"Pengkajian resep","QuestionnaireResponse",el,"linkId item.item diulang 1–4 di tiap grup (sumber tidak menyebut linkId grup 1–3).")
T="18. Pengeluaran obat"
add(T,"Farmasi","Pengeluaran obat","Medication + MedicationDispense",[("*MedicationDispense.identifier[i]","ID resep","Sama dengan MedicationRequest.identifier"),("*MedicationDispense.status","Kode status pengeluaran","FHIR terminology"),
 ("*MedicationDispense.medicationReference","Medication/{ID}",""),("Medication.code.coding.system",KFA,""),("Medication.code.coding.code","Kode obat KFA",""),("Medication.code.coding.display","Nama obat KFA",""),
 ("Medication.form.coding.system",KM+"/CodeSystem/medication-form",""),("Medication.form.coding.code","Kode sediaan",""),("Medication.form.coding.display","Deskripsi sediaan",""),
 ("Medication.batch.lotNumber","(String)","Nomor batch"),("Medication.batch.expirationDate","(DateTime)","Tanggal kedaluwarsa"),
 ("MedicationDispense.quantity.value","(Decimal)","Jumlah"),("MedicationDispense.quantity.unit / system / code","UCUM",""),
 ("MedicationDispense.dosageInstruction.route.coding.system","http://www.whocc.no/atc",""),("MedicationDispense.dosageInstruction.route.coding.code","Kode rute WHO ATC",""),("MedicationDispense.dosageInstruction.route.coding.display","Deskripsi rute",""),
 ("MedicationDispense.dosageInstruction.doseAndRate.doseQuantity.value","(Decimal)",""),("MedicationDispense.dosageInstruction.doseAndRate.doseQuantity.unit","UCUM unit",""),
 ("MedicationDispense.dosageInstruction.timing","timing.repeat","Frekuensi"),
 ("MedicationDispense.dosageInstruction.additionalInstruction.coding.system",SN,""),("MedicationDispense.dosageInstruction.additionalInstruction.coding.code","ECL: < 419492006",""),("MedicationDispense.dosageInstruction.additionalInstruction.coding.display","SNOMED CT Description",""),("MedicationDispense.dosageInstruction.additionalInstruction.text","(String)",""),
 ("MedicationDispense.performer.actor",PR,"Petugas yang mengeluarkan obat"),("MedicationDispense.whenPrepared","(DateTime)",""),("MedicationDispense.whenHandedOver","(DateTime)",""),
 ("MedicationDispense.authorizingPrescription","MedicationRequest/{ID}",""),("*MedicationDispense.subject",PAT,""),("*MedicationDispense.context",ENC,""),
 ("*Medication.identifier[i]","ID obat lokal",""),("*Medication.extension:medicationType","Jenis obat","")])

T="19. Pemberian obat"
add(T,"Farmasi","Pemberian obat","Medication + MedicationAdministration",[("*MedicationAdministration.status","Kode status pemberian","FHIR terminology"),
 ("Medication.code.coding.system",KFA,""),("Medication.code.coding.code","Kode obat KFA",""),("Medication.code.coding.display","Nama obat KFA",""),("MedicationAdministration.medicationReference","Medication/{ID}",""),
 ("Medication.form.coding.system",KM+"/CodeSystem/medication-form",""),("Medication.form.coding.code","Kode sediaan",""),("Medication.form.coding.display","Deskripsi sediaan",""),
 ("MedicationAdministration.dosage.route.coding.system","http://www.whocc.no/atc",""),("MedicationAdministration.dosage.route.coding.code","Kode rute WHO ATC",""),("MedicationAdministration.dosage.route.coding.display","Deskripsi rute",""),
 ("MedicationAdministration.dosage.dose.value","(Decimal)","Dosis"),("MedicationAdministration.dosage.dose.unit","UCUM unit",""),("MedicationAdministration.performer.actor",PR,"Pemberi obat"),
 ("MedicationAdministration.effectivePeriod","(DateTime)","Tanggal & jam pemberian (sumber: 'effecticePeriod')"),("*Medication.identifier[i]","ID obat lokal",""),("*Medication.extension:medicationType","Jenis obat","")],"Judul tabel di sumber tertulis 'Resource Composition'.")
T="20. Diet"
add(T,"Diet","Diet","NutritionOrder",[("*NutritionOrder.status","(status)",""),("*NutritionOrder.intent","proposal","Hanya rekomendasi"),("*NutritionOrder.intent","order","Arahan untuk dietisien"),
 ("*NutritionOrder.patient",PAT,""),("*NutritionOrder.encounter",ENC,""),("*NutritionOrder.dateTime","(DateTime)",""),
 ("NutritionOrder.oralDiet.type.coding","Kode jenis diet (SNOMED / Kemkes)","Lihat Lampiran Terminologi jenis diet"),
 ("NutritionOrder.oralDiet.nutrient.modifier.coding.system",SN,""),("NutritionOrder.oralDiet.nutrient.modifier.coding.code","ECL: < 226355009 |Nutrients| & < 87918000 |Mineral|",""),("NutritionOrder.oralDiet.nutrient.modifier.coding.display","SNOMED CT Description",""),
 ("NutritionOrder.oralDiet.nutrient.amount.value","(Decimal)",""),("NutritionOrder.oralDiet.nutrient.amount.unit / system / code","UCUM","Sumber menulis 'nutrition.amount'"),
 ("NutritionOrder.excludeFoodModifier.coding.system",SN,""),("NutritionOrder.excludeFoodModifier.coding.code","ECL: < 255620007 |Food|",""),("NutritionOrder.excludeFoodModifier.coding.display","SNOMED CT Description",""),
 ("NutritionOrder.note.text","(String)","")],"Ketentuan lengkap di use case Gizi.")
T="21. Edukasi"
EDU=[("84635008","Disease process or condition education","Proses penyakit, diagnosis, rencana asuhan"),("967006","Medication education","Obat-obatan"),("410082002","Rehabilitation therapy education","Rehabilitasi medis"),
     ("712651001","Education about pain","Manajemen nyeri"),("61310001","Nutrition education","Gizi"),("698608004","Hand washing education","Cuci tangan"),("362978005","Medical equipment or device education","Penggunaan alat medis")]
add(T,"Edukasi","Edukasi","Procedure",[("*Procedure.status","completed","")]+co("Procedure.category.coding",SN,"409073007","Education")+
 [("*"+p,v,k) for p,v,k in co("Procedure.code.coding[0]",KM+"/CodeSystem/kptl","10913","Edukasi Kesehatan Individu","KPTL edukasi umum")]+
 [("*"+p,v,k) for p,v,k in opts("Procedure.code.coding[1]",SN,EDU)]+[("*Procedure.subject",PAT,""),("*Procedure.encounter",ENC,""),("*Procedure.performer[i].actor",PR,"")],
 "Wajib 2 Procedure.code dalam 1 payload (KPTL + SNOMED). Kode SNOMED hanya contoh; ruang lingkup ECL < 409073007 |Education|.")
T="22. Prognosis"
add(T,"Prognosis","Prognosis","ClinicalImpression",CIM[:1]+co("ClinicalImpression.code.coding",SN,"20481000","Determination of prognosis")+
 [("*"+p,v,k) for p,v,k in opts("ClinicalImpression.prognosisCodeableConcept[i].coding",SN,[("170968001","Prognosis good","Baik"),("65872000","Fair prognosis","Dubia et bonam"),("67334001","Guarded prognosis","Dubia et malam"),("170969009","Prognosis bad","Tidak baik")])]+CIM[1:4])
T="23. Rencana tindak lanjut"
RT=[("737481003","Inpatient care management","Rawat inap (rujukan internal / eksternal)"),("185389009","Follow-up visit","Kontrol ulang (internal)"),("11429006","Consultation","Konsultasi (internal)"),("737492002","Outpatient care management","Rawat jalan (rujukan eksternal)")]
add(T,"RTL","Rencana tindak lanjut","ServiceRequest",SRM+co("ServiceRequest.category.coding",SN,"3457005","Patient referral")+[("*"+p,v,k) for p,v,k in opts("ServiceRequest.code.coding",SN,RT)]+[("*ServiceRequest.subject",PAT,""),("*ServiceRequest.encounter",ENC,"")])
T="24. Instruksi tindak lanjut & transportasi rujuk"
add(T,"RTL","Instruksi tindak lanjut & sarana transportasi rujuk","ServiceRequest",SRM+[("*ServiceRequest.code","Kode instruksi",""),("ServiceRequest.locationCode.coding.system",HL+"v3-RoleCode",""),
 ("ServiceRequest.locationCode.coding.code","OF",""),("ServiceRequest.locationCode.coding.display","Outpatient facility","Kontrol ke poli"),
 ("ServiceRequest.locationCode.coding.code","HOSP",""),("ServiceRequest.locationCode.coding.display","Hospital","Kontrol ke fasyankes"),
 ("ServiceRequest.locationCode.coding.code","PC",""),("ServiceRequest.locationCode.coding.display","Primary care clinic","Kontrol ke fasyankes"),
 ("ServiceRequest.locationCode.text","(String)","Lain-lain (free text)"),("ServiceRequest.locationReference","Location/{ID}","Rujukan internal antar poli"),
 ("ServiceRequest.locationCode.coding.code","AMB","Sarana transportasi rujuk"),("ServiceRequest.locationCode.coding.display","Ambulance",""),
 ("ServiceRequest.occurrenceDateTime","(DateTime)","Tanggal kontrol"),("ServiceRequest.patientInstruction","(String)","Kontak dalam keadaan darurat"),
 ("*ServiceRequest.subject",PAT,""),("*ServiceRequest.encounter",ENC,""),("*ServiceRequest.performer","Practitioner / Organization","")],"Sumber menulis path 'locationCode.code.coding.code' (typo).")
T="25. Kondisi saat meninggalkan faskes"
add(T,"Pulang","Kondisi saat meninggalkan RS (Condition)","Condition",co("Condition.category.coding",HL+"condition-category","problem-list-item","Problem List Item")+
 [("*"+p,v,k) for p,v,k in opts("Condition.code.coding",SN,[("359746009","Patient's condition stable","Stabil"),("162668006","Patient's condition unstable","Tidak stabil"),("268910001","Patient's condition improved","Perbaikan")])]+CM)
DD=[("aadvice","Left against advice","Pulang paksa",HL+"discharge-disposition"),("other-hcf","Other healthcare facility","Dirujuk",HL+"discharge-disposition"),
    ("exp-lt48h","Meninggal <48 jam","Meninggal <48 jam",KM+"/CodeSystem/discharge-disposition"),("exp-gt48h","Meninggal >48 jam","Meninggal >48 jam",KM+"/CodeSystem/discharge-disposition"),("oth","Other","Lain-lain (free text)",HL+"discharge-disposition")]
el=[]
for c,d,k,s in DD: el+=[("*Encounter.hospitalization.dischargeDisposition.coding.system",s,""),("*Encounter.hospitalization.dischargeDisposition.coding.code",c,k),("*Encounter.hospitalization.dischargeDisposition.coding.display",d,"")]
el.append(("Encounter.hospitalization.dischargeDisposition.text","(String)","Keterangan lain-lain"))
add(T,"Pulang","Kondisi saat meninggalkan RS (Encounter)","Encounter",el)
T="26. Cara keluar dari faskes"
add(T,"Pulang","Cara keluar dari RS","Encounter",[x for c,d,k in [("home","Home","Pulang atas persetujuan dokter"),("aadvice","Left against advice","Pulang atas permintaan sendiri"),("oth","Other","Lain-lain (free text)")] for x in
 [("*Encounter.hospitalization.dischargeDisposition.coding.system",HL+"discharge-disposition",""),("*Encounter.hospitalization.dischargeDisposition.coding.code",c,k),("*Encounter.hospitalization.dischargeDisposition.coding.display",d,"")]])
T="27. Pembaruan data kunjungan"
add(T,"Update Encounter","Kunjungan selesai","Encounter",[("*Encounter.status","finished",""),("*Encounter.period.end","(DateTime)",""),("*Encounter.diagnosis[i].condition","Condition/{ID}","Keluhan utama, diagnosis primer & sekunder"),
 ("Encounter.length","(Duration, menit)","Lama perawatan"),("*Encounter.hospitalization.dischargeDisposition","Kondisi/cara keluar & RTL","")],"PUT Encounter setelah kunjungan selesai.","Setiap kunjungan")
T="28. Resume medis"
SEC=[("Anamnesis",KM,"TK000003","Anamnesis",None),("Keluhan utama",LN,"10154-3","Chief complaint Narrative - Reported","Condition"),("Keluhan penyerta",LN,"11450-4","Problem list - Reported","Condition"),
 ("Riwayat alergi",LN,"48765-2","Allergies","AllergyIntolerance"),("Riwayat penyakit pribadi terdahulu",LN,"11348-0","History of Past illness Narrative","Condition (inactive)"),("Riwayat penyakit pribadi sekarang",LN,"10164-2","History of Present illness Narrative","Condition (active)"),
 ("Riwayat penyakit keluarga",LN,"10157-6","History of family member diseases Narrative","FamilyMemberHistory"),("Riwayat pengobatan",LN,"10160-0","History of Medication use Narrative","MedicationStatement"),
 ("Pemeriksaan fisik",KM,"TK000007","Pemeriksaan Fisik",None),("Tanda vital",LN,"8716-3","Vital signs","Observation"),("Head to toe",LN,"10187-3","Review of systems Narrative - Reported","Observation"),
 ("Pemeriksaan fungsional",LN,"47420-5","Functional status assessment note","Observation"),("Perencanaan perawatan",LN,"18776-5","Plan of care note","ClinicalImpression, Goal, CarePlan"),
 ("Pemeriksaan penunjang",KM,"TK000009","Hasil Pemeriksaan Penunjang",None),("Laboratorium",LN,"11502-2","Laboratory report","ServiceRequest, Procedure, Specimen, Observation, DiagnosticReport"),("Radiologi",LN,"18782-3","Radiology Study observation (narrative)","ServiceRequest, Observation, Procedure, AllergyIntolerance, DiagnosticReport"),
 ("Diagnosis",KM,"TK000004","Diagnosis",None),("Diagnosis awal",LN,"42347-5","Admission diagnosis (narrative)","Condition"),("Diagnosis akhir",LN,"78375-3","Discharge diagnosis Narrative","ClinicalImpression, Condition, RiskAssessment"),
 ("Tindakan/prosedur medis",KM,"TK000005","Tindakan/Prosedur Medis","ServiceRequest, Procedure, Observation"),("Farmasi",KM,"TK000013","Obat",None),("Obat saat kunjungan",LN,"42346-7","Medications on admission (narrative)","MedicationRequest, MedicationDispense, MedicationAdministration"),
 ("Obat pulang",LN,"75311-1","Discharge medications Narrative","MedicationRequest, MedicationDispense"),("Rekomendasi diet",LN,"42344-2","Discharge diet (narrative)","NutritionOrder (proposal)"),("Diet yang diberikan",LN,"61144-2","Diet and nutrition Narrative","NutritionOrder (order)"),
 ("Edukasi",LN,"34895-3","Education note","Procedure"),("Kondisi saat meninggalkan RS",LN,"10184-0","Hospital discharge physical findings Narrative","ClinicalImpression, Condition"),
 ("Rencana tindak lanjut",LN,"8653-8","Hospital Discharge instructions","Observation, CarePlan, ServiceRequest"),("Perjalanan kunjungan pasien",LN,"8648-8","Hospital course Narrative","text.div (narasi)")]
el=[("*Composition.status","(status)","")]+[("*"+p,v,k) for p,v,k in co("Composition.type.coding",LN,"88645-7","Outpatient hospital Discharge summary")]+co("Composition.category.coding",LN,"LP173421-1","Report")+\
 [("*Composition.subject",PAT,""),("*Composition.date","(DateTime)",""),("*Composition.author[i]",PR,""),("*Composition.title","(String)",""),("*Composition.attester.mode","(mode)",""),("*Composition.relatesTo[i].code / target","Relasi dokumen","")]
for t,s,c,d,ent in SEC:
    p="Composition.section" if ent is None or t in ("Pemeriksaan fungsional","Perencanaan perawatan","Tindakan/prosedur medis","Edukasi","Kondisi saat meninggalkan RS","Rencana tindak lanjut","Perjalanan kunjungan pasien") else "Composition.section.section"
    el+=[(p+".title",t,"")]+co(p+".code.coding",s,c,d)+([(p+".entry",ent,"")] if ent else [])
add(T,"Resume","Resume medis","Composition",el,"Section Diet di sumber memakai path section.code (bukan section.section.code) untuk subsection; section Diagnosis kehilangan baris display.")

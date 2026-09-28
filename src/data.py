# Sumber: SATUSEHAT Playbook ANC (disunting 2 Okt 2025) + Lampiran Terminologi ANC (disunting 1 Nov 2024)
L="LOINC"; S="SNOMED CT"; KCT="Kemkes clinical-term"; KANC="Kemkes anc-custom-codes"; WHO="WHO anc-custom-codes"; I="HL7 v3 ObservationInterpretation"
NA="N/A=Normal · A=Abnormal (tampil: Normal / Tidak Normal)"
# kolom: tahap, kelompok, variabel, resource, kategori, sistem, kode, display, kode_anc, tipe, satuan, pilihan, catatan, frekuensi
R=[]
def r(tahap,kel,var,res,kat="",sis="",kode="",disp="",anc="",tipe="",sat="",pil="",cat="",frek=""):
    R.append(dict(tahap=tahap,kel=kel,var=var,res=res,kat=kat,sis=sis,kode=kode,disp=disp,anc=anc,tipe=tipe,sat=sat,pil=pil,cat=cat,frek=frek))

T0="0. Prasyarat & aturan umum"
r(T0,"Prasyarat","Autentikasi ke SATUSEHAT","—",cat="Wajib sebelum pengiriman data (token akses).",frek="Sekali per sesi")
r(T0,"Prasyarat","Registrasi struktur organisasi (sub-organisasi layanan ANC)","Organization",frek="Sekali (setup)")
r(T0,"Prasyarat","Registrasi struktur lokasi (ruang/poli KIA)","Location",frek="Sekali (setup)")
r(T0,"Prasyarat","Nomor IHS tenaga kesehatan","Practitioner",cat="GET dari Master Nakes Index; nakes pemeriksa tidak di-POST, cukup direferensikan.",frek="Sekali per nakes")
r(T0,"Aturan umum","Format waktu","Semua",cat="Kirim dalam UTC+00 (WIB −7, WITA −8, WIT −9). Contoh 17.35 WIB 23-08-2023 → 2023-08-23T10:35:00+00:00. Tanggal tidak boleh < 03-06-2014.")
r(T0,"Aturan umum","Cakupan kunjungan","—",cat="Pelaporan mengikuti Permenkes 21/2021. Kunjungan ke-berapa (K1 akses/murni, K2–K6) dikirim di Encounter.identifier (lihat tahap 16).")
r(T0,"Aturan umum","Variabel pelayanan umum","—",cat="Pendaftaran, penunjang, diagnosis, tindakan, farmasi, RTL, kondisi/cara keluar mengikuti modul Rawat Jalan / IGD / Rawat Inap. Sheet ini hanya merinci yang khusus ANC.")

T1="1. Pendaftaran pasien"
r(T1,"Identitas pasien","Nomor SATUSEHAT (IHS) pasien","Patient",cat="Didapat dari Master Patient Index (MPI) via GET; simpan di sistem internal. Identitas lain di bawah = data demografi MPI, tidak perlu dikirim ulang tiap transaksi.",frek="Sekali per pasien")
for v in ["Nama lengkap","Nomor rekam medis","NIK","No. identitas lain (WNA: paspor/KITAS)","Nama ibu kandung","Tempat lahir","Tanggal lahir","Jenis kelamin","Bahasa yang dikuasai","Alamat lengkap, RT, RW","Kelurahan/desa, kecamatan, kab/kota, provinsi (kode wilayah)","Kode pos, negara","No. telepon rumah & seluler","Status pernikahan"]:
    r(T1,"Identitas pasien",v,"Patient")

T2="2. Pendaftaran kunjungan"
r(T2,"Kunjungan","Kunjungan ANC (Encounter)","Encounter",cat="Satu rangkaian pelayanan = 1 Encounter. Wajib: status, statusHistory, class, subject, participant, period, location, serviceProvider; diagnosis saat selesai. Isi Encounter.episodeOfCare dengan UUID EpisodeOfCare kehamilan.",frek="Setiap kunjungan")

T3="3. Memulai episode kehamilan"
r(T3,"Episode kehamilan","Episode kehamilan (EpisodeOfCare)","EpisodeOfCare",kode="ANC",disp="type = ANC",tipe="status active",cat="POST sekali saja pada kunjungan ANC pertama. period.start = tanggal HPHT (jika ada). Kunjungan berikutnya: GET dengan patient + type ANC + status active (opsional + organization) untuk ambil UUID, lalu tautkan ke Encounter.episodeOfCare.",frek="Sekali per kehamilan")

T4="4. Kondisi pasien / status obstetri"
K="Status obstetri"
r(T4,K,"Gravida","Observation","survey",L,"11996-6","[#] Pregnancies","WHO ANC.B6.DE24","Integer",frek="Kunjungan pertama / bila berubah")
r(T4,K,"Partus","Observation","survey",L,"11977-6","[#] Parity","WHO ANC.B6.DE32","Integer")
r(T4,K,"Abortus","Observation","survey",L,"69043-8","Other pregnancy outcomes #","WHO ANC.B6.DE25","Integer")
r(T4,K,"Tanggal HPHT","Observation","survey",L,"8665-2","Last menstrual period start date","WHO ANC.B6.DE14","DateTime",cat="Juga dipakai sebagai EpisodeOfCare.period.start dan dasar batas 44 minggu penutupan episode.")
r(T4,K,"Hari Perkiraan Lahir (HPL)","Observation","survey",L,"11778-8","Delivery date Estimated","WHO ANC.B6.DE22","DateTime")
r(T4,K,"Berat badan sebelum hamil","Observation","survey",L,"56077-1","Body weight --pre current pregnancy","WHO ANC.B8.DE2","Decimal","kg")
r(T4,K,"Tinggi badan","Observation","vital-signs",L,"8302-2","Body height","WHO ANC.B8.DE1","Decimal","cm")
r(T4,K,"IMT sebelum hamil","Observation","exam",KCT,"OC000010","Indeks Massa Tubuh Sebelum Hamil","Kemkes ANC.SS.DE58","Decimal","kg/m2",
  "interpretation (SNOMED): 248342006 Underweight = Kurus (≤18,4) · 43664005 Normal weight = Normal (18,5–24,9) · 238131007 Overweight = Gemuk (25–29,9) · 414915002 Obese = Obesitas (≥30)",
  "Lampiran 1. Versi 1.0 memakai kode Kemkes 'BMI-Normal' dst. → v1.1 diganti SNOMED.")
r(T4,K,"Target kenaikan berat badan","Observation","exam",KCT,"OC000011","Target Kenaikan Berat Badan","WHO ANC.B8.DE10","CodeableConcept","",
  "Kemkes clinical-term: OV000008 5–9 kg (IMT ≥30) · OV000009 7–11,5 kg (IMT 25–29,9) · OV000010 11,5–16 kg (IMT 18,5–24,9) · OV000011 12,5–18 kg (IMT <18,5)",
  "Diturunkan dari kategori IMT sebelum hamil.")
r(T4,K,"Jarak kehamilan saat ini dengan sebelumnya","Observation","survey",KCT,"OC000001","Jarak kehamilan","Kemkes ANC.SS.DE53","Decimal","mo (bulan)")
K="Imunisasi tetanus"
r(T4,K,"Riwayat status imunisasi TT (T1–T5)","Immunization","","KFA","VG139","Td","","status completed / not-done","",
  "doseNumberPositiveInt 1–5 = T1–T5 · reportOrigin: recall (ingatan pasien) / record (catatan tertulis)",
  "primarySource = false. reasonCode IM-WUS 'Imunisasi Program Rutin Lanjutan Wanita Usia Subur'. Tanggal pemberian di occurrenceDateTime.")
r(T4,K,"Riwayat status imunisasi TT (T0 / belum pernah)","Immunization","","KFA","VG139","Td","","status not-done","","reportOrigin: recall",
  "primarySource = false; occurrenceString (bukan DateTime); reasonCode IM-WUS. Tanpa doseNumber.")
r(T4,K,"Pemberian imunisasi TT saat kunjungan (T1–T5)","Immunization","","KFA","(lihat Lampiran 4 terminologi imunisasi)","","","status completed","","doseNumberPositiveInt 1–5 = T1–T5",
  "primarySource = true (diberikan di faskes ini); reasonCode IM-WUS.")

T5="5. Data kunjungan kehamilan"
r(T5,"Usia kehamilan","Usia kehamilan","Observation","survey",L,"18185-9","Gestational age","WHO ANC.B6.DE17","Decimal","wk (minggu)",frek="Setiap kunjungan")
r(T5,"Usia kehamilan","Trimester ke-","Observation","survey",L,"32418-6","Obstetric trimester Stated","Kemkes ANC.SS.DE13","Integer","","1 / 2 / 3",frek="Setiap kunjungan")

T6="6. Pelayanan kehamilan"
K="6a. Pemeriksaan ibu"
fq="Setiap kunjungan"
r(T6,K,"Berat badan","Observation","vital-signs",L,"29463-7","Body weight","WHO ANC.B8.DE3","Decimal","kg",frek=fq)
r(T6,K,"Lingkar lengan atas (LiLA)","Observation","exam",S,"284473002","Mid upper arm circumference","Kemkes ANC.SS.DE3","Decimal","cm",
  "interpretation: OI000018 KEK (LiLA <23 cm) · OI000035 Risiko KEK (23–<23,5 cm) [Kemkes] · N Normal (≥23,5 cm) [HL7]",frek=fq)
r(T6,K,"Tinggi fundus uteri","Observation","exam",L,"11881-0","Uterus Fundal height Tape measure","WHO ANC.B8.DE105","Decimal","cm",frek=fq)
r(T6,K,"Tekanan darah sistolik","Observation","vital-signs",L,"8480-6","Systolic blood pressure","WHO ANC.B8.DE17","Decimal","mm[Hg]",frek=fq)
r(T6,K,"Tekanan darah diastolik","Observation","vital-signs",L,"8462-4","Diastolic blood pressure","WHO ANC.B8.DE19","Decimal","mm[Hg]",frek=fq)
r(T6,K,"Nadi","Observation","vital-signs",L,"8867-4","Heart rate","WHO ANC.B8.DE36","Decimal","/min",frek=fq)
r(T6,K,"Suhu","Observation","vital-signs",L,"8310-5","Body temperature","WHO ANC.B8.DE34","Decimal","Cel",frek=fq)
r(T6,K,"Pernapasan","Observation","vital-signs",L,"9279-1","Respiratory rate","Kemkes ANC.SS.DE2","Decimal","/min",frek=fq)
r(T6,K,"Golongan darah","Observation","laboratory",L,"883-9","ABO group [Type] in Blood","WHO ANC.B9.DE24","CodeableConcept","","LOINC: LA19710-5 A · LA19709-7 B · LA19708-9 O · LA28449-9 AB")
r(T6,K,"Rhesus","Observation","laboratory",L,"10331-7","Rh [Type] in Blood","WHO ANC.B9.DE29","CodeableConcept","","LOINC: LA6576-8 Positif · LA6577-6 Negatif")
r(T6,K,"Makanan Tambahan (MT) ibu hamil — grup","QuestionnaireResponse","","Questionnaire Q0002","linkId 1","Makanan Tambahan Ibu Hamil","","Group")
r(T6,K,"Jika LiLA <23,5, apakah mendapat MT?","QuestionnaireResponse","","Questionnaire Q0002","linkId 1.1","","","Boolean","","Ya / Tidak")
r(T6,K,"Jenis MT","QuestionnaireResponse","","Questionnaire Q0002","linkId 1.2","","","Coding","","Kemkes clinical-term: FO000001 MT Lokal · FO000002 MT Pabrikan")
K="6b. Pemeriksaan fisik ibu"
for v,sys,c,d,anc,bs in [("Konjungtiva",L,"10197-2","Physical findings of Eye Narrative","ANC.SS.DE26","bodySite SNOMED 29445007 Conjunctival structure"),
 ("Sklera",L,"10197-2","Physical findings of Eye Narrative","ANC.SS.DE27","bodySite SNOMED 18619003 Scleral structure"),
 ("Leher",L,"11411-6","Physical findings of Neck Narrative","ANC.SS.DE28",""),
 ("Gigi dan mulut",S,"423066003","Finding of mouth region","ANC.SS.DE29",""),
 ("THT",S,"297268004","Ear, nose and throat finding","ANC.SS.DE30",""),
 ("Dada (jantung)",L,"10200-4","Physical findings of Heart Narrative","ANC.SS.DE31",""),
 ("Dada (paru)",S,"301230006","Lung finding","ANC.SS.DE32",""),
 ("Perut",L,"10191-5","Physical findings of Abdomen Narrative","ANC.SS.DE33",""),
 ("Tungkai",S,"116312005","Finding of lower limb","ANC.SS.DE34","")]:
    r(T6,K,v,"Observation","exam",sys,c,d,"Kemkes "+anc,"interpretation","",NA,bs)
K="6c. Pemeriksaan janin"
r(T6,K,"Denyut jantung janin (DJJ)","Observation","exam",L,"55283-6","Fetal Heart rate","WHO ANC.B8.DE107","Decimal","{beats}/min",frek=fq)
r(T6,K,"Kepala terhadap PAP","Observation","exam",S,"249111004","Engagement of head","Kemkes ANC.SS.DE46","CodeableConcept","","SNOMED: 249112006 Head engaged = Masuk panggul · 62098001 Head not engaged = Belum masuk panggul","v1.0: kode Kemkes OC000002 / OV000001 / OV000002 → v1.1 SNOMED (Lampiran 3).")
r(T6,K,"Taksiran berat janin (TBJ)","Observation","exam",L,"89087-1","Fetal Body weight Estimated","Kemkes ANC.SS.DE1","Decimal","g")
r(T6,K,"Presentasi janin","Observation","exam",L,"72155-5","Position in womb Fetus [RHEA]","WHO ANC.B8.DE111","CodeableConcept","","SNOMED: 1209182005 Presentasi kepala · 6096002 Presentasi bokong · 288203005 Letak lintang","v1.0: OV000003/4/5 → v1.1 SNOMED (Lampiran 3).")
r(T6,K,"Jumlah janin","Observation","exam",S,"246435002","Number of fetuses","WHO ANC.B8.DE109","Integer","","","v1.0: Kemkes OC000003 → v1.1 SNOMED.")
K="6d. Pemeriksaan USG"
for v,c,d,anc,t,u in [("Gestational sac (GS) diameter","11850-5","Gestational sac Mean diameter US","Kemkes ANC.SS.DE36","Decimal","cm"),
 ("Crown rump length (CRL)","11957-8","Fetal Crown Rump length US","Kemkes ANC.SS.DE37","Decimal","cm"),
 ("DJJ (USG)","11948-7","Fetal Heart rate US","Kemkes ANC.SS.DE38","Decimal","{beats}/min"),
 ("Usia kehamilan (USG)","11888-5","Gestational age US composite estimate","WHO ANC.B6.DE20","Decimal","wk"),
 ("HPL (USG)","11781-2","Delivery date US composite estimate","Kemkes ANC.SS.DE40","DateTime","")]:
    r(T6,K,v,"Observation","imaging",L,c,d,anc,t,u)
r(T6,K,"Letak janin (USG)","Observation","imaging",S,"271692001","Presentation of fetus","Kemkes ANC.SS.DE41","CodeableConcept","","SNOMED: 398236008 Intrauteri · 298109001 Ekstrauteri","v1.0: OC000004 / OV000006 / OV000007 → v1.1 SNOMED.")
for v,c,d,anc,u in [("Biparietal diameter (BPD)","11820-8","Fetal Head Diameter.biparietal US","ANC.SS.DE59","cm"),
 ("Head circumference (HC)","11984-2","Fetal Head Circumference US","ANC.SS.DE42","cm"),
 ("Abdominal circumference (AC)","11979-2","Fetal Abdomen Circumference US","ANC.SS.DE43","cm"),
 ("Femur length (FL)","11963-6","Fetal Femur diaphysis [Length] US","ANC.SS.DE44","cm"),
 ("Berat janin (USG)","11727-5","Fetal Body weight estimated by US","ANC.SS.DE45","g")]:
    r(T6,K,v,"Observation","imaging",L,c,d,"Kemkes "+anc,"Decimal",u)
r(T6,K,"Tindakan USG kehamilan","Procedure",cat="Tindakan USG dicatat sebagai Procedure (status, category, code, performedPeriod); citra DICOM via ImagingStudy mengikuti modul Radiologi.")
K="6e. Pemeriksaan 10T (lab)"
RX="SNOMED: 11214006 Reactive · 131194007 Non-Reactive"
r(T6,K,"Hemoglobin","Observation","laboratory",L,"718-7","Hemoglobin [Mass/volume] in Blood","WHO ANC.B9.DE175","Decimal","g/dL",cat="Tes dasar")
r(T6,K,"Skrining PPIA HIV","Observation","laboratory",L,"68961-2","HIV 1 Ab [Presence] ... by Rapid immunoassay","WHO ANC.B9.DE32","CodeableConcept","",RX,"Tes dasar")
r(T6,K,"Skrining PPIA Sifilis (RPR)","Observation","laboratory",L,"20508-8","Reagin Ab [Units/volume] ... by RPR","WHO ANC.B9.DE96","CodeableConcept","",RX,"Tes dasar")
r(T6,K,"Skrining PPIA Sifilis (VDRL)","Observation","laboratory",L,"14904-7","Reagin Ab [Presence] in Specimen by VDRL","WHO ANC.B9.DE96","CodeableConcept","",RX,"Tes dasar")
r(T6,K,"Skrining PPIA Hepatitis B","Observation","laboratory",L,"75410-1","HBsAg [Presence] ... by Rapid immunoassay","WHO ANC.B9.DE60","CodeableConcept","",RX,"Tes dasar")
r(T6,K,"Gula darah (sewaktu)","Observation","laboratory",L,"74774-1","Glucose [Mass/volume] in Serum, Plasma or Blood","WHO ANC.B9.DE159","Decimal","mg/dL",cat="Tes lain")
r(T6,K,"Protein urin","Observation","laboratory",L,"5804-0","Protein [mass/volume] in urine by test strip","WHO ANC.B9.DE114","Decimal","mg/dL",cat="Tes lain")
K="6f. Pemantauan & pendampingan (4T)"
r(T6,K,"Pemantauan & pendampingan — grup","QuestionnaireResponse","","Questionnaire Q0002","linkId 2","Pemantauan & Pendampingan","","Group")
for lid,v in [("2.1","Terlalu muda usia melahirkan (<21 tahun)"),("2.2","Terlalu rapat jarak kelahiran (<2 tahun)"),("2.3","Terlalu tua (kehamilan >35 tahun)"),("2.4","Terlalu sering melahirkan (anak >3)")]:
    r(T6,K,v,"QuestionnaireResponse","","Questionnaire Q0002","linkId "+lid,"","","Boolean","","Ya / Tidak","Inkonsistensi di dokumen asli: teks item 2.1 tertulis 'di bawah 20 tahun'." if lid=="2.1" else "")
K="6g. Riwayat penyakit & risiko"
r(T6,K,"Komplikasi / penyulit kehamilan","Condition","problem-list-item","ICD-10","(lihat sheet Komplikasi ICD-10)","","","","","59 kode ICD-10 bab O, dikelompokkan trimester 1 dan 2–3","Lampiran 2.")
r(T6,K,"Riwayat penyakit menular","Condition","problem-list-item",S,"ECL: < 417662000 OR < 443508001","History / No history of clinical finding in subject","","","","Kode SNOMED turunan konsep tsb","Kode lengkap di Lampiran Standar Terminologi SATUSEHAT (umum).")
r(T6,K,"Riwayat penyakit keluarga","Condition","problem-list-item",S,"ECL: < 416471007 OR < 160266009","Family history / No family history of clinical finding","","","","Kode SNOMED turunan konsep tsb","Kode lengkap di Lampiran Standar Terminologi SATUSEHAT (umum).")
r(T6,K,"Merokok","Observation","social-history",L,"72166-2","Tobacco smoking status","","CodeableConcept","","SNOMED: 77176002 Smoker = Ya · 43381005 Passive smoker = Pasif · 8392000 Non-smoker = Tidak")
r(T6,K,"Konsumsi alkohol","Observation","social-history",L,"11331-6","History of Alcohol use","","CodeableConcept","","SNOMED: 219006 Current drinker = Ya · 105542008 Non-drinker = Tidak")
K="6h. Kondisi lainnya"
r(T6,K,"Lainnya — grup","QuestionnaireResponse","","Questionnaire Q0002","linkId 3","Lainnya","","Group")
r(T6,K,"Apakah disabilitas?","QuestionnaireResponse","","Questionnaire Q0002","linkId 3.1","","","Boolean","","Ya / Tidak")
r(T6,K,"Apakah mengikuti kelas ibu hamil?","QuestionnaireResponse","","Questionnaire Q0002","linkId 3.2","","","Boolean","","Ya / Tidak")

T7="7. Pemeriksaan penunjang"
r(T7,"Lab & radiologi","Permintaan, spesimen, hasil & laporan penunjang","ServiceRequest, Specimen, Observation, DiagnosticReport, ImagingStudy",cat="Rujuk modul Rawat Jalan/IGD/Ranap. Mencakup: nama & nomor pemeriksaan, waktu permintaan, dokter pengirim, prioritas CITO/non-CITO, diagnosis kerja, status puasa, data spesimen (jenis, lokasi, volume, metode, waktu ambil/fiksasi, petugas), nilai hasil, nilai rujukan/kritis, interpretasi, validator; radiologi: status alergi kontras, status kehamilan, jenis kontras, citra DICOM, interpretasi.")
T8="8. Diagnosis"
r(T8,"Diagnosis","Diagnosis awal/masuk, diagnosis primer & sekunder","Condition + Encounter.diagnosis","","ICD-10",cat="Rujuk modul Rawat Jalan/IGD/Ranap (use, rank).")
T9="9. Tindakan / prosedur medis"
r(T9,"Tindakan","Tindakan/prosedur medis","Procedure","","ICD-9-CM",cat="Rujuk modul Rawat Jalan/IGD/Ranap.")
T10="10. Konseling / temu wicara / edukasi"
K="Edukasi"
r(T10,K,"Edukasi gizi","Procedure","",S,"61310001","Nutrition education",cat="1 payload Procedure per topik edukasi (2 edukasi = 2 Procedure).")
for c,d in [("ED000008","Edukasi Tanda Bahaya Kehamilan, Bersalin dan Nifas"),("ED000009","Edukasi IMD dan ASI Eksklusif"),("ED000010","Edukasi PHBS"),("ED000011","Edukasi KB pasca salin"),("ED000012","Edukasi lainnya")]:
    r(T10,K,d,"Procedure","",KCT,c,d)
r(T10,K,"Tidak diberikan konseling","Procedure","",S,"409073007","Education","","status not-done")
T11="11. Farmasi"
r(T11,"Farmasi","Peresepan obat","Medication + MedicationRequest","","KFA",cat="Nama obat, sediaan, jumlah, rute, dosis, unit, frekuensi, aturan tambahan, dokter penulis, waktu & status resep. Rujuk modul Rawat Jalan/IGD/Ranap.")
r(T11,"Farmasi","Pengkajian resep (administrasi, farmasetik, klinis)","QuestionnaireResponse",cat="Rujuk modul Pelayanan Kefarmasian.")
r(T11,"Farmasi","Pengeluaran obat / obat dibawa pulang","Medication + MedicationDispense","","KFA",cat="Rujuk modul Rawat Jalan/IGD/Ranap.")
T12="12. Rencana tindak lanjut & transportasi rujuk"
r(T12,"RTL","Rencana tindak lanjut","ServiceRequest (+ Encounter.hospitalization.dischargeDisposition)",cat="Rujuk modul terkait.")
r(T12,"RTL","Sarana transportasi untuk rujuk","ServiceRequest (locationCode)",cat="Rujuk modul terkait.")
T13="13. Instruksi tindak lanjut"
r(T13,"RTL","Instruksi untuk tindak lanjut (mis. jadwal kontrol)","ServiceRequest",cat="Rujuk modul terkait.")
T14="14. Kondisi saat meninggalkan faskes"
r(T14,"Pulang","Kondisi saat meninggalkan RS/faskes","Condition + Encounter",cat="Rujuk modul terkait.")
r(T14,"Pulang","Waktu kematian (bila meninggal)","Observation","exam",L,"81956-5","Date and time of death [TimeStamp]","Kemkes ANC.SS.DE56","DateTime")
T15="15. Cara keluar dari faskes"
r(T15,"Pulang","Cara keluar dari RS/faskes","Encounter (hospitalization.dischargeDisposition)",cat="Rujuk modul terkait.")
T16="16. Pembaruan data kunjungan"
r(T16,"Update Encounter","Sedang dilayani","Encounter",tipe="status in-progress",cat="Disarankan catat mulai/selesai di statusHistory; jika realtime, isi Encounter.period sesuai dan status in-progress.")
r(T16,"Update Encounter","Kunjungan selesai","Encounter",cat="PUT Encounter (id = UUID dari POST awal) berisi diagnosis, periode selesai, kondisi & cara keluar, RTL, status kunjungan ANC, dan UUID EpisodeOfCare.",frek="Setiap kunjungan")
r(T16,"Update Encounter","Status kunjungan ANC (K1–K6)","Encounter","","episodeofcare/ANC (identifier)","K1A · K1M · K2 · K3 · K4 · K5 · K6","","","identifier value","",
  "K1A = K1 akses · K1M = K1 murni · K2 · K3 · K4 · K5 · K6","System: http://terminology.kemkes.go.id/CodeSystem/episodeofcare/ANC. Dikirim di setiap kunjungan ANC.",frek="Setiap kunjungan")
T17="17. Menutup episode kehamilan"
r(T17,"Episode kehamilan","Tutup EpisodeOfCare","EpisodeOfCare",tipe="status finished",
  pil="Waktu berakhir = (a) waktu persalinan · (b) waktu keguguran/kuret · (c) hilang kontak: HPHT + 44 minggu (308 hari)",
  cat="PATCH (sejak v2.5; sebelumnya PUT): status & statusHistory[].status = finished; period.end & statusHistory[].period.end = waktu berakhirnya kehamilan.",frek="Sekali per kehamilan")

ICD=[("O20.0","Threatened abortion","Abortus iminens","1"),("O03.4","Spontaneous abortion; incomplete; without complication","Abortus inkomplit","1"),("O03.9","Spontaneous abortion; complete or unspecified; without complication","Abortus komplit","1"),("O02.0","Blighted ovum and nonhydatidiform mole","Blighted Ovum","1"),("O02.1","Missed abortion","Dead conceptus","1"),("O00.1","Tubal pregnancy","Kehamilan ektopik","1"),("O00.0","Abdominal pregnancy","Abdo. Pregnancy","1"),("O01.0","Classical hydatidiform mole","Mola hidatidosa","1"),("O01.1","Incomplete and partial hydatidiform mole","Mola Parsial","1"),("O21.0","Mild hyperemesis gravidarum","Emesis gravidarum","1"),("O21.1","Hyperemesis gravidarum with metabolic disturbance","Hiperemesis","1"),("O08.0","Genital tract and pelvic infection following abortion and ectopic and molar pregnancy","Infeksiosa","1"),("O08.1","Delayed or excessive haemorrhage following abortion and ectopic and molar pregnancy","Fluxus profus","1"),("O08.3","Shock following abortion and ectopic and molar pregnancy","Syok","1"),("O08.5","Metabolic disorders following abortion and ectopic and molar pregnancy","Gx metabolik","1"),("O08.6","Damage to pelvic organs and tissues following abortion and ectopic and molar pregnancy","Preforasi","1"),("O10.0","Pre-existing essential hypertension complicating pregnancy; childbirth and the puerperium","Hipertensi kronis","2-3"),("O11","Pre-existing hypertensive disorder with superimposed proteinuria","Hipertensi kronis si PE","2-3"),("O13","Gestational [pregnancy-induced] hypertension without significant proteinuria","Hipertensi gestasional","2-3"),("O14.0","Moderate pre-eclampsia","Preeklampsia (PE)","2-3"),("O14.1","Severe pre-eclampsia","Preeklampsia Berat (PEB)","2-3"),("O14.2","HELLP syndrome","HELLP Syndrome","2-3"),("O15.0","Eclampsia in pregnancy","Eklampsia","2-3"),("O22.4","Haemorrhoids in pregnancy","Hemoroid","2-3"),("O23.3","Infections of other parts of urinary tract in pregnancy","ISK","2-3"),("O23.5","Infections of the genital tract in pregnancy","BV / fluor albus","2-3"),("O24.3","Pre-existing diabetes mellitus; unspecified","DM Pragest","2-3"),("O24.4","Diabetes mellitus arising in pregnancy","DM gest","2-3"),("O99.2","Endocrine; nutritional and metabolic diseases complicating pregnancy; childbirth and the puerperium","Obesitas","2-3"),("O25","Malnutrition in pregnancy","Underweight","2-3"),("O26.2","Pregnancy care of habitual aborter","RPL Hamil","2-3"),("O26.6","Liver disorders in pregnancy; childbirth and the puerperium","Kehamilan liver","2-3"),("O30.0","Twin pregnancy","Hamil Kembar 2","2-3"),("O30.1","Triplet pregnancy","Hamil Kembar 3","2-3"),("O31.8","Other complications specific to multiple gestation","Komplikasi kembar","2-3"),("O32.1","Maternal care for breech presentation","Presentasi sungsang","2-3"),("O32.2","Maternal care for transverse and oblique lie","Presentasi lintang","2-3"),("O34.0","Maternal care for congenital malformation of uterus","Kelainan uterus","2-3"),("O34.1","Maternal care for tumour of corpus uteri","Tumor uterus","2-3"),("O34.2","Maternal care due to uterine scar from previous surgery","Bekas SC","2-3"),("O34.3","Maternal care for cervical incompetence","Cervix inkompeten","2-3"),("O34.8","Maternal care for other abnormalities of pelvic organs","Prolaps uteri","2-3"),("O35.9","Maternal care for (suspected) fetal abnormality and damage; unspecified","Komplikasi Kongenital janin","2-3"),("O36.0","Maternal care for rhesus isoimmunization","Rhesus Isoimunisasi","2-3"),("O36.2","Maternal care for hydrops fetalis","Hidrops fetalis","2-3"),("O36.4","Maternal care for intrauterine death","IUFD","2-3"),("O36.5","Maternal care for poor fetal growth","IUGR","2-3"),("O36.6","Maternal care for excessive fetal growth","Makrosomia","2-3"),("O40","Polyhydramnios","Hidramnion","2-3"),("O41.0","Oligohydramnios","Oligohidramnion","2-3"),("O41.1","Infection of amniotic sac and membranes","Korioamnionitis","2-3"),("O42.2","Premature rupture of membranes; labour delayed by therapy","KPP konservatif","2-3"),("O42.0","Premature rupture of membranes; onset of labour within 24 hours","KPP < 24 jam","2-3"),("O42.1","Premature rupture of membranes; onset of labour after 24 hours","KPP > 24 jam","2-3"),("O43.2","Morbidly adherent placenta","Plasenta akreta","2-3"),("O44.1","Placenta praevia with haemorrhage","Plasenta previa","2-3"),("O45.8","Other premature separation of placenta","Solusio plasenta","2-3"),("O48","Prolonged pregnancy","Postterm > 42 mgg","2-3"),("O26.9","Pregnancy-related condition; unspecified","Komplikasi Obstetri Lain","2-3")]

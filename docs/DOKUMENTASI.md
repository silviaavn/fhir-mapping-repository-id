# Dokumentasi Pekerjaan — Konsolidasi Playbook SATUSEHAT

Snapshot data: 18–19 Sep 2026 · **pembaruan 7 Okt 2026: 2 modul baru (MCU, TTE)** · Lampiran Standar Terminologi v10.3 (30 Jun 2026)

## Tujuan
Menyatukan playbook interoperabilitas SATUSEHAT dan lampirannya (yang di situs resminya terpisah halaman dan formatnya berulang) menjadi satu dokumentasi yang:

- menampilkan variabel use case beserta elemen FHIR dan nilainya (.code dan .display di baris terpisah, * = wajib, pilihan jawaban sebagai daftar system–code–display–keterangan);
- mengecek konsistensi antar playbook (crosscheck variabel dan crosscheck per resource);
- bisa dikembangkan ke 30+ use case dan menerima revisi kontributor yang terpisah dari data dasar SATUSEHAT.

## Keluaran
| Keluaran | Isi |
|---|---|
| Halaman web (artifact) | Tampilan per use case, Konsolidasi, Struktur induk–anak, Ringkasan Resource, Revisi kontributor, Dokumentasi; pencarian dengan highlight; popover status & deskripsi |
| `SATUSEHAT_Semua_UseCase_Crosscheck.xlsx` | Panduan, Ringkasan Crosscheck, Konsolidasi, Ringkasan Resource, Resource - Nilai, Struktur Induk-Anak, 1 sheet per use case, Daftar Pilihan & Lampiran |
| `satusehat_structured_all_20261007.json` · `satusehat_curated_ANC_RJ_HIV_20260918.json` · `playbook_pdf_20261007.json` | Data mentah & terstruktur hasil ekstraksi |
| `satusehat_standar_terminologi_v10.3.json` | Hasil ekstraksi Lampiran Standar Terminologi (332 path, 2.993 kode) |

## Pembaruan situs SATUSEHAT (pemeriksaan 7 Okt 2026)
Halaman indeks Panduan Interoperabilitas terakhir disunting 5 Okt 2026. Hasil pembandingan dengan snapshot 18 Sep 2026:

| Perubahan | Keterangan |
|---|---|
| **Medical Check Up (MCU)** — modul baru | v1.0, 6 Okt 2026. Halaman web tidak memuat tabel pemetaan; isinya pada Playbook PDF (232 halaman, Google Drive) + halaman Lampiran Terminologi MCU dengan 24 lampiran. Hasil ekstraksi: 148 variabel, 2.530 baris elemen |
| **Tanda Tangan Elektronik (TTE)** — modul baru | v1.0, 23 Jul 2026, berstatus *"sedang dalam tahap pengembangan (hanya tersedia di Environment Sandbox)"*. Pemetaan lengkap di halaman web. Hasil ekstraksi: 38 variabel, 309 baris elemen, resource Composition/Consent/Provenance/Task/Location/Device/DocumentReference/DiagnosticReport/ServiceRequest/Observation |
| Data Kelahiran | Disunting 29 Sep 2026, tetapi riwayat perubahan tetap v1.0 (26 Jun 2026) dan jumlah variabel tetap 98. Satu-satunya beda: tabel Observation "Golongan Darah" kini memisahkan pilihan jawaban (A/B/O/AB) ke baris tersendiri — perubahan format, bukan variabel baru |
| 28 modul lain | Tidak ada perubahan setelah 18 Sep 2026 (tanggal sunting terakhir ≤ 10 Sep 2026) |
| Modul Pelayanan | Tetap 4 (Rawat Jalan, IGD, Rawat Inap, Kefarmasian) |
| Standar Terminologi | Tetap 9 Jul 2026 (v10.3, sudah dipakai) |

## Angka utama
| Ukuran | Jumlah |
|---|---|
| Playbook / use case | **32** (3 dikurasi manual: ANC, Rawat Jalan, HIV · 29 ekstraksi otomatis) |
| Sumber PDF (dibaca dari Google Drive) | 7 (HIV, MTBS, Klaim, Mata, UBM, Rabies, **MCU**) |
| Halaman lampiran terminologi per modul | 18 |
| Variabel | **2.209** (198 dikurasi manual · 2.011 otomatis) |
| Konsep setelah deduplikasi | 1.574 |
| Konsep yang muncul di ≥2 use case | 335 (135 di >2 use case) |
| Tahap yang hanya merujuk ke modul lain (judul + tautan) | 56 (12 ANC/HIV, 44 modul otomatis) |
| Elemen pelengkap dari playbook lain (grup “Saling melengkapi”) | 206 baris di 125 variabel |
| Variabel yang punya induk (item kuesioner, komponen, bagian dokumen, kelompok) | 1.624 dari 2.209 · 280 induk (204 kelompok playbook, 76 induk sungguhan) |
| Konsep induk lintas playbook (mis. APGAR, Tekanan Darah, Anamnesis) | 31 |
| Status: Unik / Identik | 1.228 / 127 |
| Status: Saling melengkapi | 99 |
| Status perlu dicek: Kode sama, isi beda | 77 |
| Status perlu dicek: Maksud sama, kode/struktur beda | 43 |
| Elemen dengan nilai berbeda antar use case (dalam konsep bersama) | 139 |
| Elemen yang hanya dipakai sebagian use case | 955 |
| Daftar pilihan jawaban & lampiran | 747 (503 daftar P-xxx dibentuk dari pilihan jawaban) |
| Resource FHIR yang dirangkum | 40 |
| Variabel tanpa elemen inti resource-nya | 265 |
| Elemen di luar daftar elemen baku FHIR (kemungkinan salah ketik/extension) | 32 |
| Kode Lampiran Standar Terminologi yang belum muncul di playbook mana pun | 2.366 dari 2.993 · 109 path yang hanya ada di lampiran |
| Deskripsi variabel dari playbook / dibuat Claude | 541 / 1.872 |

## Yang sudah dikerjakan
1. **Kurasi manual ANC, Rawat Jalan, HIV.** Elemen wajib per resource dilengkapi. Tahap yang di playbook hanya merujuk ke modul lain **tidak lagi disalin**: ditampilkan sebagai judul tahap + kutipan + tautan ke playbook yang dirujuk (baris “Mengikuti modul lain”). Karena itu status “Identik (disalin)” tidak ada lagi.
2. **Crawl 32 modul + 18 lampiran + 7 PDF.** Hasilnya diparse otomatis: tabel baris, tabel kolom (termasuk header kolom di tengah tabel — perbaikan 19 Sep yang memulihkan ±94 baris pilihan, mis. Edukasi RANAP/GIGI/PKPR), dan lampiran bernomor.
3. **Crosscheck konsep.** Pengelompokan memakai kode utama, nama variabel, dan pasangan manual. Nama yang sama tidak digabung bila kodenya berbeda atau resource-nya berbeda.
   - Semua variabel Procedure "Edukasi…" disatukan menjadi satu konsep, sehingga pilihannya tampil sebagai satu daftar gabungan.
4. **Penjelasan status per elemen, lintas semua anggota.** Contoh Procedure.code.coding pada Edukasi:
   - ANC: ED000008–12 + 61310001
   - RJ & RANAP: KPTL 10913 + 7 SNOMED
   - GIGI: SNOMED + ED000001–2 (dengan system SNOMED)
   - GIZI: ECL
   - PKPR: kode gaya hidup
   - MATA: 385906007
5. **Konsolidasi tanpa pengulangan elemen.** Setiap elemen muncul sekali, dengan semua nilai/pilihan dan use case pemakainya. Tampilan pertama yang terbuka adalah Konsolidasi.
6. **Ringkasan Resource** (terinspirasi dari FHIR SatuSehat Mapping Explorer). Per resource ditampilkan tingkat pemakaian elemen (Inti/Umum/Kadang/Jarang), elemen pilihan `[x]` yang dihitung sekali, matriks kelengkapan per use case, nilai/kode per path dan pemakainya, elemen baku yang belum pernah dipakai, elemen di luar standar, variabel tanpa elemen inti, serta kode dan path tambahan dari Lampiran Standar Terminologi.
7. **Deskripsi variabel (popover ⓘ).** Kalimat playbook yang menyebut variabel tersebut, atau deskripsi yang disusun Claude (diberi label "belum diverifikasi"), plus konteks tahap dari playbook.
8. **Pencarian** mencakup isi daftar pilihan dan deskripsi. Kata yang cocok di-highlight. Di Konsolidasi, hasil ≤25 konsep otomatis terbuka.
9. **Hierarki induk–anak.** Variabel yang sebenarnya satu kesatuan kini bertingkat: item kuesioner dari awalan `linkId` (160), komponen satu pengukuran (6), bagian dokumen dari `Composition.section` (80), dan kelompok bawaan playbook sebagai induk sintetis (1.582). Di tampilan use case induk bisa dilipat; menu **Struktur induk–anak** membandingkan induk yang sama antar playbook dalam bentuk matriks sub-variabel × use case.
10. **Elemen pelengkap.** Pada konsep berstatus “Saling melengkapi”, elemen yang hanya ada di playbook lain ikut ditampilkan di halaman playbook yang kekurangan, ditandai “pelengkap” beserta sumbernya.
11. **Revisi kontributor** (resolve, usulan nilai, tambah pilihan, tambah elemen, catatan). Revisi mencatat nama dan institusi pengusul serta statusnya (terbuka/diterima/ditolak), dan dipisahkan dari data dasar SATUSEHAT.
12. **Penanganan pemotongan halaman PDF (modul MCU).** Pada playbook yang hanya tersedia sebagai PDF, nilai yang terpotong antar halaman sebelumnya terbaca sebagai variabel baru (mis. `bservation-category`, `oncept.coding.code`). Aturan baru menyambungkan potongan itu ke nilai sebelumnya: MCU turun dari 348 variabel semu menjadi 148 variabel dengan jumlah elemen yang hampir sama (2.530 dari 2.543). Aturan ini baru diterapkan pada MCU agar modul lain tidak berubah.

## Yang masih perlu dikerjakan
| Prioritas | Pekerjaan | Skala |
|---|---|---|
| Tinggi | Review manual 29 modul hasil ekstraksi otomatis (terutama tabel PDF yang terpotong halaman) | 2.011 variabel |
| Tinggi | Review khusus MCU: hasil ekstraksi 232 halaman PDF, judul kelompok (`kel`) masih ada yang tertukar/terpotong | 148 variabel |
| Tinggi | Tinjau konsep berstatus konflik | 77 "Kode sama, isi beda" + 43 "Maksud sama, kode/struktur beda" |
| Sedang | Lengkapi daftar elemen wajib untuk modul yang daftar wajibnya berupa gambar/tidak terbaca | 13 modul: KELAHIRAN, INC, GIGI, IMUNCOVID, MPDN, MTBS, PKPR, KLAIM, MATA, TUMBANG, UBM, RABIES, MCU |
| Sedang | Cari lampiran untuk modul tanpa halaman lampiran terpisah | 9 modul: IGD, FARMASI, PNC, JANTUNG, MATA, URONEFRO, SHK, TUMBANG, TTE |
| Sedang | Cek variabel tanpa elemen inti resource dan elemen di luar standar (kemungkinan salah ketik di playbook atau salah baca parser, mis. "coed", "conclusiondivisualisasikan", "deceasedbooelan") | 265 variabel · 32 elemen |
| Sedang | Periksa hierarki hasil tebakan otomatis — terutama kelompok sintetis dari judul tabel playbook dan item kuesioner tanpa `linkId` | 280 induk |
| Sedang | Validasi penggabungan nama generik ("Nama", "Status Hubungan", dsb.) dan tambahkan pasangan manual SAME/RELATED untuk modul selain ANC/RJ/HIV | 335 konsep lintas use case |
| Sedang | Verifikasi deskripsi yang dibuat Claude, atau ganti dengan definisi resmi | 1.872 variabel |
| Sedang | Pantau TTE: modul masih tahap pengembangan (Sandbox), kemungkinan berubah sebelum rilis produksi | 38 variabel |
| Rendah | Rapikan hasil ekstraksi Lampiran Standar Terminologi untuk resource keuangan (Claim, Coverage*, ChargeItem): kolom system tercampur teks header; beberapa heading path yang terpotong baris belum terdeteksi | ±40 path |
| Rendah | Otomatisasi pengecekan pembaruan situs SATUSEHAT (diff snapshot) — saat ini masih manual, lewat tanggal "Terakhir disunting" tiap halaman | 32 halaman |

## Alur revisi kontributor

Usulan dikirim sebagai berkas CSV (tombol **Unduh usulan (.csv)** di halaman), lalu diunggah pengelola ke `docs/revisi/` di GitHub. Halaman membaca semua CSV di folder itu saat dibuka. Baris yang mengisi kolom `aksi` (`ganti-nilai`, `pindah-konsep`, `tandai-status`, `tambah-pilihan`, `tambah-elemen`, `jadikan-anak`, `lepas-anak`) diterapkan ke isi halaman begitu kolom `status` berisi `diterima`, dan status konsep dihitung ulang. Ringkasan Resource, Excel, dan JSON tetap versi bangunan terakhir.

## Catatan metode
- Elemen generik (subject, encounter, performer, author, source, effectiveDateTime) ditampilkan, tetapi tidak dipakai untuk pencocokan.
- Coding tambahan anc-custom-codes (WHO/Kemkes) tidak dihitung sebagai konflik.
- Baris "(wajib — nilai tidak dirinci)" berarti elemen tercantum di daftar wajib pemetaan nilai, tetapi nilainya tidak dirinci di tabel variabel.
- Angka "kode lampiran yang belum dipakai" dihitung dengan membandingkan kode pada Lampiran Standar Terminologi terhadap seluruh nilai yang muncul di playbook; angka pada snapshot sebelumnya memakai cara hitung yang sedikit berbeda, jadi tidak bisa dibandingkan langsung.
- Perubahan di Excel tidak tersinkron otomatis. Kirim file yang sudah diedit, dan perubahannya akan diimpor sebagai revisi kontributor.

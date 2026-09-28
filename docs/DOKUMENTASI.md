# Dokumentasi Pekerjaan — Konsolidasi Playbook SATUSEHAT

Snapshot data: 18–19 Sep 2026 · Lampiran Standar Terminologi v10.3 (30 Jun 2026)

## Tujuan
Menyatukan playbook interoperabilitas SATUSEHAT dan lampirannya (yang di situs resminya terpisah halaman dan formatnya berulang) menjadi satu dokumentasi yang:

- menampilkan variabel use case beserta elemen FHIR dan nilainya (.code dan .display di baris terpisah, * = wajib, pilihan jawaban sebagai daftar system–code–display–keterangan);
- mengecek konsistensi antar playbook (crosscheck variabel dan crosscheck per resource);
- bisa dikembangkan ke 20+ use case dan menerima revisi kontributor yang terpisah dari data dasar SATUSEHAT.

## Keluaran
| Keluaran | Isi |
|---|---|
| Halaman web (artifact) | Tampilan per use case, Konsolidasi, Ringkasan Resource, Dokumentasi; pencarian dengan highlight; popover status & deskripsi; revisi kontributor (tersimpan bersama) |
| `SATUSEHAT_Semua_UseCase_Crosscheck.xlsx` | Panduan, Ringkasan Crosscheck, Konsolidasi, Ringkasan Resource, Resource - Nilai, 1 sheet per use case, Daftar Pilihan & Lampiran |
| `satusehat_structured_all_20260919.json` · `satusehat_curated_ANC_RJ_HIV_20260918.json` · `satusehat_playbook_pdf_20260918.json` | Data mentah & terstruktur hasil ekstraksi |
| `satusehat_standar_terminologi_v10.3.json` | Hasil ekstraksi Lampiran Standar Terminologi (332 path, 2.995 kode) |

## Angka utama
| Ukuran | Jumlah |
|---|---|
| Playbook / use case | 30 (3 dikurasi manual: ANC, Rawat Jalan, HIV · 27 ekstraksi otomatis) |
| Sumber PDF (dibaca dari Google Drive) | 6 (HIV, MTBS, Klaim, Mata, UBM, Rabies) |
| Halaman lampiran terminologi per modul | 17 |
| Variabel | 2.051 (226 dikurasi manual · 1.825 otomatis) |
| Konsep setelah deduplikasi | 1.416 |
| Konsep yang muncul di ≥2 use case | 332 (134 di >2 use case) |
| Status: Unik / Identik / Identik (disalin) | 1.073 / 131 / 14 |
| Status: Saling melengkapi | 96 |
| Status perlu dicek: Kode sama, isi beda | 60 |
| Status perlu dicek: Maksud sama, kode/struktur beda | 42 |
| Elemen dengan nilai berbeda antar use case (dalam konsep bersama) | 121 |
| Elemen yang hanya dipakai sebagian use case | 860 |
| Daftar pilihan jawaban & lampiran | 604 (384 daftar P-xxx dibentuk dari pilihan jawaban) |
| Resource FHIR yang dirangkum | 38 |
| Variabel tanpa elemen inti resource-nya | 277 |
| Elemen di luar daftar elemen baku FHIR (kemungkinan salah ketik/extension) | 27 |
| Kode Lampiran Standar Terminologi yang belum dipakai playbook mana pun | 2.163 (pada path yang dipakai) + 85 path yang hanya ada di lampiran |
| Deskripsi variabel dari playbook / dibuat Claude | 536 / 1.515 |

## Yang sudah dikerjakan
1. **Kurasi manual ANC, Rawat Jalan, HIV.** Elemen wajib per resource dilengkapi. Tahap ANC/HIV yang di playbook merujuk ke modul Rawat Jalan disalin dari RJ (status "Identik (disalin)").
2. **Crawl 30 modul + 17 lampiran + 6 PDF.** Hasilnya diparse otomatis: tabel baris, tabel kolom (termasuk header kolom di tengah tabel — perbaikan 19 Sep yang memulihkan ±94 baris pilihan, mis. Edukasi RANAP/GIGI/PKPR), dan lampiran bernomor.
3. **Crosscheck konsep.** Pengelompokan memakai kode utama, nama variabel, dan pasangan manual. Nama yang sama tidak digabung bila kodenya berbeda atau resource-nya berbeda.
   - Semua variabel Procedure "Edukasi…" disatukan menjadi satu konsep (K-083), sehingga pilihannya tampil sebagai satu daftar gabungan.
4. **Penjelasan status per elemen, lintas semua anggota.** Contoh Procedure.code.coding pada Edukasi:
   - ANC: ED000008–12 + 61310001
   - RJ & RANAP: KPTL 10913 + 7 SNOMED
   - GIGI: SNOMED + ED000001–2 (dengan system SNOMED)
   - GIZI: ECL
   - PKPR: kode gaya hidup
   - MATA: 385906007
5. **Konsolidasi tanpa pengulangan elemen.** Setiap elemen muncul sekali, dengan semua nilai/pilihan dan use case pemakainya.
6. **Ringkasan Resource** (terinspirasi dari FHIR SatuSehat Mapping Explorer). Per resource ditampilkan:
   - tingkat pemakaian elemen (Inti/Umum/Kadang/Jarang);
   - elemen pilihan [x] yang dihitung sekali (valueQuantity/valueCodeableConcept/… adalah alternatif, bukan semuanya wajib);
   - matriks kelengkapan per use case;
   - nilai/kode per path dan pemakainya;
   - elemen baku yang belum pernah dipakai;
   - elemen di luar standar;
   - variabel tanpa elemen inti;
   - kode dan path tambahan dari Lampiran Standar Terminologi.
7. **Deskripsi variabel (popover ⓘ).** Kalimat playbook yang menyebut variabel tersebut, atau deskripsi yang disusun Claude (diberi label "belum diverifikasi"), plus konteks tahap dari playbook.
8. **Pencarian** mencakup isi daftar pilihan dan deskripsi. Kata yang cocok di-highlight. Di Konsolidasi, hasil ≤25 konsep otomatis terbuka.
9. **Revisi kontributor** (resolve, usulan nilai, tambah pilihan, tambah elemen, catatan). Revisi mencatat nama dan institusi pengusul serta statusnya (terbuka/diterima/ditolak), dan dipisahkan dari data dasar SATUSEHAT.

## Yang masih perlu dikerjakan
| Prioritas | Pekerjaan | Skala |
|---|---|---|
| Tinggi | Salin detail tahap yang di playbook hanya "merujuk ke modul Rawat Jalan/IGD/Rawat Inap" untuk modul otomatis (seperti yang sudah dilakukan untuk ANC & HIV) | 17 modul, 102 kalimat rujukan (deteksi otomatis) (terbanyak: KANKER 14, MPDN 13, JANTUNG 13, NEONATUS 11, TUMBANG 11) |
| Tinggi | Review manual 27 modul hasil ekstraksi otomatis (terutama tabel PDF yang terpotong halaman) | 1.825 variabel |
| Tinggi | Tinjau konsep berstatus konflik | 60 "Kode sama, isi beda" + 42 "Maksud sama, kode/struktur beda" |
| Sedang | Lengkapi daftar elemen wajib untuk modul yang daftar wajibnya berupa gambar/tidak terbaca | 12 modul: KELAHIRAN, INC, GIGI, IMUNCOVID, MPDN, MTBS, PKPR, KLAIM, MATA, TUMBANG, UBM, RABIES |
| Sedang | Cari lampiran untuk modul tanpa halaman lampiran terpisah | 8 modul: IGD, FARMASI, PNC, JANTUNG, MATA, URONEFRO, SHK, TUMBANG |
| Sedang | Cek variabel tanpa elemen inti resource dan elemen di luar standar (kemungkinan salah ketik di playbook atau salah baca parser, mis. "coed", "valueCodeable", "Interpretation") | 277 variabel · 27 elemen |
| Sedang | Validasi penggabungan nama generik ("Nama", "Status Hubungan", dsb.) dan tambahkan pasangan manual SAME/RELATED untuk modul selain ANC/RJ/HIV | 332 konsep lintas use case |
| Sedang | Verifikasi deskripsi yang dibuat Claude, atau ganti dengan definisi resmi | 1.515 variabel |
| Rendah | Rapikan hasil ekstraksi Lampiran Standar Terminologi untuk resource keuangan (Claim, Coverage*, ChargeItem): kolom system tercampur teks header; beberapa heading path yang terpotong baris belum terdeteksi | ±40 path |
| Rendah | Otomatisasi pengecekan pembaruan situs SATUSEHAT (diff snapshot) | — |

## Catatan metode
- Elemen generik (subject, encounter, performer, author, source, effectiveDateTime) ditampilkan, tetapi tidak dipakai untuk pencocokan.
- Coding tambahan anc-custom-codes (WHO/Kemkes) tidak dihitung sebagai konflik.
- Baris "(wajib — nilai tidak dirinci)" berarti elemen tercantum di daftar wajib pemetaan nilai, tetapi nilainya tidak dirinci di tabel variabel.
- Perubahan di Excel tidak tersinkron otomatis. Kirim file yang sudah diedit, dan perubahannya akan diimpor sebagai revisi kontributor.

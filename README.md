# Crosscheck Playbook SATUSEHAT

Konsolidasi seluruh playbook interoperabilitas SATUSEHAT beserta lampiran terminologinya menjadi satu dokumentasi yang bisa dibaca dan dicek konsistensinya: **32 use case, 2.209 variabel, 1.574 konsep**, lengkap dengan elemen FHIR, nilai/kode, dan pilihan jawaban.

> **Pembaruan 7 Okt 2026.** Dua modul baru dari situs SATUSEHAT sudah masuk: **Medical Check Up (MCU)** (v1.0, 6 Okt 2026 — dari Playbook PDF 232 halaman + 24 lampiran terminologi) dan **Tanda Tangan Elektronik (TTE)** (v1.0, 23 Jul 2026, masih tahap pengembangan/Sandbox). Modul lain tidak berubah; Data Kelahiran hanya berubah format daftar pilihan. Rincian di [`docs/DOKUMENTASI.md`](docs/DOKUMENTASI.md).

Di situs resminya, playbook dan lampiran terminologi terpisah halaman dan formatnya berulang. Repo ini menyatukannya, lalu menambahkan lapisan crosscheck: variabel yang sama di beberapa use case dipasangkan, perbedaan nilainya dijelaskan per elemen, dan setiap resource FHIR diringkas (elemen apa yang biasanya ada, kode apa yang dipakai, kode mana dari Lampiran Standar Terminologi yang belum dipakai playbook mana pun).

## Buka halamannya

| Cara | Untuk siapa |
|---|---|
| **GitHub Pages** — <https://silviaavn.github.io/fhir-mapping-repository-id/> | Siapa pun. Semua tampilan jalan (per use case, Konsolidasi, Ringkasan Resource, Dokumentasi, pencarian). Tombol "Revisi" di sini dipakai untuk menyusun usulan lalu mengunduhnya sebagai CSV. |
| **Halaman di Claude** (privat) | Pengelola, untuk revisi yang disimpan langsung di halaman. |
| `data/SATUSEHAT_Semua_UseCase_Crosscheck.xlsx` | Yang lebih nyaman bekerja di Excel. |

## Hierarki induk–anak

Variabel yang sebenarnya satu kesatuan ditampilkan bertingkat: item kuesioner bertingkat (`QuestionnaireResponse.item.linkId`), komponen satu pengukuran (`Observation.component`), bagian dokumen (`Composition.section`), dan kelompok bawaan playbook. 1.624 dari 2.209 variabel punya induk, di bawah 280 induk. Menu **Struktur induk–anak** di halaman membandingkan 31 induk yang muncul di lebih dari satu playbook dalam bentuk matriks sub-variabel × use case.

## Alur revisi (ringkas)

1. Kontributor membuka halaman, klik **Revisi** pada variabel/konsep, isi usulan, lalu klik **Unduh usulan (.csv)**. Tanpa akun Claude maupun GitHub.
2. Berkas CSV itu dikirim ke pengelola.
3. Pengelola mengunggahnya ke [`docs/revisi/`](docs/revisi/) lewat **Add file → Upload files** di GitHub.
4. Halaman membaca semua CSV di folder itu setiap kali dibuka — revisi langsung tampil, tanpa build ulang. Lihat menu **Revisi kontributor** di halaman.

Detail format dan cara menandai usulan diterima/ditolak: [`docs/revisi/README.md`](docs/revisi/README.md).

## Isi

```
docs/
  index.html                  halaman lengkap (siap dibuka lewat GitHub Pages)
  DOKUMENTASI.md              apa yang sudah dikerjakan, angka-angkanya, dan sisa pekerjaan
data/
  satusehat_structured_all_20261007.json   variabel + konsep + hierarki induk-anak + deskripsi + ringkasan resource (keluaran utama)
  satusehat_standar_terminologi_v10.3.json Lampiran Standar Terminologi v10.3 (332 path, 2.993 kode)
  satusehat_playbook_raw_20261007.json     hasil crawl 32 halaman modul + 18 halaman lampiran
  satusehat_playbook_auto_extract.json     hasil parsing 29 modul otomatis
  satusehat_curated_ANC_RJ_HIV_20260918.json  kurasi manual ANC, Rawat Jalan, HIV
  hiv_lists.json                           daftar pilihan dari playbook HIV (PDF)
  SATUSEHAT_Semua_UseCase_Crosscheck.xlsx  versi Excel (8 jenis sheet)
src/
  crawl/parse.py              parser halaman & PDF playbook  -> auto_extract.json
  parse_standar_terminologi.py  parser PDF Lampiran Standar Terminologi -> std.json
  data3.py, rj.py, hiv.py     data hasil kurasi manual (ANC, Rawat Jalan, HIV)
  model.py                    penggabungan, pengelompokan konsep, status crosscheck
  hier.py                     hierarki induk-anak variabel (item kuesioner, komponen, section, kelompok)
  model2.py                   ringkasan per elemen & per resource, deskripsi variabel
  build_h.py, build_x.py      pembangun halaman HTML dan file Excel
  export_json.py              ekspor dataset terstruktur (JSON)
  make_pages.py               bungkus halaman jadi docs/index.html untuk GitHub Pages
```

## Status crosscheck

| Status | Jumlah | Arti |
|---|---|---|
| Unik | 1.228 | hanya ada di satu variabel |
| Identik | 127 | elemen & nilai sama di lebih dari satu playbook |
| Saling melengkapi | 99 | hanya ada elemen/pilihan tambahan, tidak ada nilai yang bertentangan |
| Kode sama, isi beda | 77 | kode utama sama, ada nilai yang bertentangan — **perlu diputuskan** |
| Maksud sama, kode/struktur beda | 43 | konsep setara, kode/category/resource berbeda — **perlu diputuskan** |

Rincian dan sisa pekerjaan ada di [`docs/DOKUMENTASI.md`](docs/DOKUMENTASI.md).

## Menjalankan ulang

```bash
pip install -r requirements.txt
python src/crawl/parse.py                  # perlu hasil crawl (data/..._raw_....json)
python src/parse_standar_terminologi.py    # perlu PDF Lampiran Standar Terminologi
python src/build_h.py                      # -> halaman HTML
python src/build_x.py                      # -> Excel
```

Script masih memakai path absolut dari mesin tempat data dibuat (`/home/claude/...`); sesuaikan dulu ke path lokal Anda. Merapikannya jadi argumen CLI ada di daftar pekerjaan.

## Sumber & lisensi

Data berasal dari [Buku Panduan SATUSEHAT (Playbook)](https://satusehat.kemkes.go.id/platform/docs/id/interoperability/), lampiran terminologi per modul, dan Dokumen Lampiran Standar Terminologi SATUSEHAT v10.3 (30 Juni 2026) — Pusat Data dan Teknologi Informasi, Kementerian Kesehatan RI. Dokumen-dokumen itu berklasifikasi **PUBLIK** dan boleh disebarluaskan kembali. Hak atas isinya tetap pada Kementerian Kesehatan RI.

Hasil ekstraksi bisa keliru: 29 dari 32 modul diparse otomatis dan **belum dicek manual**. Untuk keputusan integrasi, selalu rujuk dokumen resminya.

Kode di `src/` dan tampilan di `docs/` berlisensi MIT (lihat [LICENSE](LICENSE)).

## Kontribusi

Lihat [CONTRIBUTING.md](CONTRIBUTING.md) — usulan revisi terhadap isi dokumentasi dikerjakan lewat halaman Claude, sedangkan perbaikan parser, struktur data, dan tampilan lewat issue atau pull request di sini.

# Cara berkontribusi

## 1. Usulan revisi isi dokumentasi — tanpa akun apa pun

Yang termasuk: perbedaan kode antar use case yang perlu diputuskan, pilihan jawaban yang kurang, elemen yang belum tercatat, deskripsi variabel yang salah.

1. Buka halaman: <https://silviaavn.github.io/fhir-mapping-repository-id/>
2. Cari variabel atau konsepnya, klik tombol **Revisi**.
3. Isi formulir: jenis usulan, elemen, usulan nilai, alasan, nama, dan institusi.
4. Klik **Unduh usulan (.csv)** — berkas CSV tersimpan di komputer Anda. Bisa menambah beberapa usulan dulu; setiap kali diunduh, berkasnya memuat semua usulan Anda.
5. Kirim berkas itu ke pengelola (email/WA). Selesai — tidak perlu akun Claude maupun GitHub.

Punya akun GitHub gratis? Tombol **Kirim lewat GitHub Issue** di formulir yang sama membuka issue yang sudah terisi.

## 2. Untuk pengelola: memasang revisi (satu langkah)

1. Buka folder [`docs/revisi/`](docs/revisi/) di repo ini → **Add file → Upload files** → pilih berkas CSV dari kontributor → **Commit changes**.
2. Tunggu ±1 menit, muat ulang halaman. Revisi langsung muncul: jumlahnya di tombol **Revisi** tiap variabel, isinya di menu **Revisi kontributor**.

Tidak ada langkah build dan tidak ada berkas yang perlu ditimpa — halaman membaca semua CSV di folder itu saat dibuka. Nama berkas bebas asal belum dipakai. Untuk memutuskan usulan, buka CSV-nya di GitHub, klik ikon pensil, ubah kolom `status` menjadi `diterima` atau `ditolak`, lalu commit.

Format kolom CSV dijelaskan di [`docs/revisi/README.md`](docs/revisi/README.md), dengan contoh di `docs/revisi/TEMPLATE.csv`.

## 3. Perbaikan parser, data, atau tampilan (issue / pull request)

Yang termasuk: tabel playbook yang salah terbaca, path FHIR yang salah ketik, aturan pengelompokan konsep, tampilan halaman, ekspor Excel.

- **Jangan** mengedit langsung berkas hasil generate: `docs/index.html`, `data/satusehat_structured_all_*.json`, dan `data/SATUSEHAT_Semua_UseCase_Crosscheck.xlsx`. Semua itu keluaran dari `src/`.
- Ubah sumbernya:
  - salah baca tabel playbook → `src/crawl/parse.py`
  - kurasi manual ANC / Rawat Jalan / HIV → `src/data3.py`, `src/rj.py`, `src/hiv.py`
  - pengelompokan konsep & status crosscheck → `src/model.py`
  - ringkasan resource, deskripsi variabel → `src/model2.py`
  - tampilan halaman / Excel → `src/build_h.py`, `src/build_x.py`
- Sebutkan di deskripsi PR: ID variabel/konsep yang terpengaruh (mis. `ANC-085`, `K-083`) dan berapa banyak baris yang berubah.

## Menuliskan usulan dengan jelas

Sertakan:

- ID variabel (`RJ-073`) atau ID konsep (`K-083`)
- elemen/path FHIR (`Procedure.code.coding`)
- kondisi sekarang vs usulan Anda
- rujukan: halaman playbook, versi lampiran terminologi, atau ketentuan program

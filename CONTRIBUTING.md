# Cara berkontribusi

Ada dua jenis kontribusi, dan jalurnya berbeda.

## 1. Usulan revisi isi dokumentasi (lewat Claude)

Yang termasuk: perbedaan kode antar use case yang perlu diputuskan, pilihan jawaban yang kurang, elemen yang belum tercatat, deskripsi variabel yang salah.

1. Minta akses halaman crosscheck di Claude kepada pemilik repo (halaman itu privat; pemilik membagikannya lewat menu Share).
2. Buka halaman tersebut di browser, cari variabel atau konsepnya, lalu klik tombol **Revisi**.
3. Pilih jenis usulan: *Resolve perbedaan*, *Usulan revisi nilai*, *Tambah pilihan jawaban*, *Tambah elemen baru*, atau *Catatan*. Isi juga **institusi** Anda.
4. Usulan tersimpan sebagai **Revisi kontributor**, terpisah dari data dasar SATUSEHAT, lengkap dengan nama pengusul, institusi, waktu, dan statusnya (terbuka / diterima / ditolak).

Kenapa lewat Claude dan bukan pull request: revisi dicatat berdampingan dengan data dasar tanpa menimpanya, sehingga selalu jelas mana yang berasal dari dokumen resmi SATUSEHAT dan mana yang usulan kontributor. Maintainer kemudian menuangkan revisi yang diterima ke `src/` dan membangun ulang keluarannya.

Belum punya akses ke halaman itu? Buka **issue** di repo ini dengan format yang sama; maintainer yang akan memasukkannya.

## 2. Perbaikan parser, data, atau tampilan (lewat issue / pull request)

Yang termasuk: tabel playbook yang salah terbaca, path FHIR yang salah ketik, aturan pengelompokan konsep, tampilan halaman, ekspor Excel.

- **Jangan** mengedit langsung file hasil generate: `docs/index.html`, `data/satusehat_structured_all_*.json`, dan `data/SATUSEHAT_Semua_UseCase_Crosscheck.xlsx`. Semua itu keluaran dari `src/`.
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

# Folder revisi kontributor

Halaman crosscheck membaca **semua berkas `.csv` di folder ini** setiap kali dibuka. Tidak ada langkah build: unggah berkas di sini, muat ulang halaman, revisinya langsung tampil.

## Untuk pengelola

1. Terima berkas `.csv` dari kontributor (hasil tombol **Unduh usulan (.csv)** di halaman).
2. Di GitHub: **Add file → Upload files** ke folder ini, lalu **Commit changes**.
3. Tunggu ±1 menit (GitHub Pages membangun ulang), muat ulang halaman. Selesai.

Nama berkas bebas, asal berakhiran `.csv` dan belum dipakai (mis. `revisi-dinkes-kota-x-2026-09-29.csv`). Jangan menimpa berkas lama — cukup tambah berkas baru; semuanya dibaca dan digabung.

Untuk menandai usulan sudah diputuskan: buka berkasnya di GitHub, klik ikon pensil, ubah kolom `status` menjadi `diterima` atau `ditolak`, lalu commit.

## Format kolom

| Kolom | Isi |
|---|---|
| `target` | **wajib** — ID variabel (mis. `ANC-085`) atau ID konsep (mis. `K-083`). Baris dengan ID yang tidak dikenal diabaikan. |
| `elemen` | path FHIR yang dibahas (mis. `Procedure.code.coding`), boleh kosong |
| `jenis` | `resolve`, `usulan`, `tambahpilihan`, `tambahelemen`, atau `catatan` |
| `usulan` | usulan nilai / keputusan |
| `alasan` | alasan atau rujukan (halaman playbook, versi lampiran, ketentuan program) |
| `kontributor` | nama pengusul |
| `institusi` | institusi pengusul |
| `tanggal` | `YYYY-MM-DD` |
| `status` | `terbuka` (bawaan), `diterima`, atau `ditolak` |

Pemisah kolom boleh koma atau titik koma; simpan sebagai **CSV UTF-8**. Kolom yang urutannya berbeda tetap terbaca selama nama judulnya sama.

`TEMPLATE.csv` berisi contoh satu baris — silakan disalin.

## Membuat revisi benar-benar diterapkan ke halaman

Tanpa kolom `aksi`, satu baris hanya tampil sebagai usulan/catatan; isi dokumentasi tidak berubah. Isi kolom `aksi` bila Anda ingin halaman benar-benar mengubah isinya. **Aksi baru dijalankan ketika kolom `status` berisi `diterima`** — jadi unggahan kontributor aman: tetap jadi usulan sampai pengelola menyetujuinya.

| `aksi` | Yang dibutuhkan | Efeknya di halaman |
|---|---|---|
| `ganti-nilai` | `target` = ID variabel, `path` = path FHIR, `nilai_baru` (`nilai_lama` opsional sebagai penyaring) | Nilai elemen diganti; nilai lama tetap tersimpan dan muncul sebagai tooltip pada penanda "revisi" |
| `pindah-konsep` | `target` = ID variabel (atau ID konsep + `nilai_lama` berisi ID variabel), `tujuan` = ID konsep/ID variabel tujuan | Variabel pindah konsep; status kedua konsep dihitung ulang |
| `tandai-status` | `target` = ID konsep, `tujuan` = status baru (mis. `Identik`, `Sudah diputuskan`) | Status konsep dikunci ke nilai itu |
| `tambah-pilihan` | `target` = ID variabel, `path` = awalan coding (mis. `Observation.code.coding`), `nilai_baru` = `system\|code\|display` | Pilihan jawaban baru ditambahkan |
| `tambah-elemen` | `target` = ID variabel, `path`, `nilai_baru` | Elemen baru ditambahkan |
| kosong / `catatan` | — | Hanya tampil sebagai usulan |

Setelah aksi diterapkan, halaman **menghitung ulang** ringkasan elemen per konsep, perbedaan antar use case, dan status konsep (Identik / Saling melengkapi / Kode sama, isi beda / Maksud sama, kode/struktur beda). Baris dijalankan berurutan menurut `tanggal`, lalu nama berkas, lalu nomor baris — jadi aksi yang bergantung pada aksi sebelumnya (mis. pindah konsep setelah kode disamakan) tetap benar bila tanggalnya sama atau lebih baru.

Yang **tidak** ikut berubah otomatis: menu Ringkasan Resource, angka di Dokumentasi, berkas Excel, dan JSON di `data/` — semuanya hasil build. Jalankan ulang `src/build_h.py` dan `src/build_x.py` (atau minta bantuan) untuk menyamakannya secara permanen.

Contoh satu keputusan lengkap:

```csv
target,elemen,jenis,usulan,alasan,kontributor,institusi,tanggal,status,aksi,path,nilai_lama,nilai_baru,tujuan
MPDN-056,Observation.code.coding,resolve,"Ganti ke LOINC 8306-3","Panjang saat meninggal diukur telentang",Silvia,Pengelola,2026-09-29,diterima,ganti-nilai,Observation.code.coding.code,8302-2,8306-3,
MPDN-056,Observation.code.coding,resolve,"Sesuaikan display","Mengikuti kode 8306-3",Silvia,Pengelola,2026-09-29,diterima,ganti-nilai,Observation.code.coding.display,Body height,Body height --lying,
MPDN-056,Observation.valueQuantity.unit,resolve,"Satuan jadi cm","Setara, kode UCUM tetap cm",Silvia,Pengelola,2026-09-29,diterima,ganti-nilai,Observation.valueQuantity.unit,centimeter,cm,
MPDN-056,,resolve,"Pindahkan ke konsep Panjang Badan","Kode utama sudah sama",Silvia,Pengelola,2026-09-29,diterima,pindah-konsep,,,,GIZI-028
```

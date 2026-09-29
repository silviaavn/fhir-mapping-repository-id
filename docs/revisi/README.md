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

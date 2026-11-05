# Code Review Checklist - Lab Equipment Loan System

## 1. Tujuan Review

Dokumen ini digunakan untuk memeriksa kualitas implementasi backend Lab Equipment Loan System agar sesuai dengan `requirement.md`, `prd.md`, dan `architecture.md`.

Review berfokus pada kesesuaian fungsi, aturan bisnis, integritas stok, konsistensi database, kualitas API, dan keterbacaan kode.

## 2. Requirement Compliance

- [x] Implementasi menggunakan Python 3.x.
- [x] Backend menggunakan Flask.
- [x] Database menggunakan SQLite.
- [x] Pertukaran data API menggunakan JSON.
- [x] Seluruh endpoint yang ditentukan tersedia:
  - [x] `GET /items`
  - [x] `POST /items`
  - [x] `POST /loans`
  - [x] `PUT /loans/{id}/return`
  - [x] `GET /loans/student/{student_id}`
- [x] Nama field dan status transaksi sesuai spesifikasi.

## 3. Data Model dan Database

- [x] Tabel `Item` memiliki `id`, `name`, `total_stock`, dan `available_stock`.
- [x] Tabel `Loan` memiliki `id`, `student_id`, `item_id`, `quantity`, `status`, dan `created_at`.
- [x] Primary key dan foreign key didefinisikan dengan benar.
- [x] Foreign key SQLite diaktifkan pada setiap koneksi.
- [x] Stok tidak menerima nilai negatif.
- [x] `quantity` transaksi harus lebih besar dari nol.
- [x] Status transaksi hanya menggunakan nilai yang diizinkan.
- [x] `available_stock` tidak melebihi `total_stock`.
- [x] Query yang menerima input menggunakan parameterized query.
- [x] Koneksi database ditutup atau dikelola dengan benar.

## 4. Business Logic

### 4.1 Penambahan Item

- [x] Field `name` wajib diisi.
- [x] `total_stock` divalidasi sebagai bilangan bulat non-negatif.
- [x] `available_stock` otomatis diinisialisasi sama dengan `total_stock`.
- [x] Data tidak tersimpan jika validasi gagal.

### 4.2 Peminjaman

- [x] `student_id`, `item_id`, dan `quantity` divalidasi.
- [x] `quantity` harus berupa bilangan bulat positif.
- [x] Sistem memeriksa keberadaan item.
- [x] Sistem menolak peminjaman jika stok tidak mencukupi.
- [x] Sistem mengembalikan `404 Not Found` jika item tidak ditemukan.
- [x] Sistem mengembalikan `400 Bad Request` jika stok tidak mencukupi.
- [x] Sistem mengembalikan `201 Created` jika peminjaman berhasil.
- [x] Stok berkurang tepat sesuai quantity.
- [x] Status awal transaksi adalah `BORROWED`.
- [x] Pembuatan transaksi dan pengurangan stok dilakukan secara atomik.
- [x] Kegagalan salah satu operasi menyebabkan rollback.

### 4.3 Pengembalian

- [x] Sistem memeriksa keberadaan transaksi.
- [x] Sistem menolak transaksi yang sudah berstatus `RETURNED`.
- [x] Sistem mengembalikan `400 Bad Request` untuk pengembalian ulang.
- [x] Sistem mengembalikan `404 Not Found` jika transaksi tidak ditemukan.
- [x] Status transaksi berubah menjadi `RETURNED`.
- [x] Stok bertambah sesuai quantity transaksi.
- [x] Pembaruan status dan pemulihan stok dilakukan secara atomik.
- [x] Pengembalian ulang tidak menyebabkan stok bertambah dua kali.

### 4.4 Riwayat Peminjaman

- [x] Hasil pencarian difilter berdasarkan `student_id`.
- [x] Data mahasiswa lain tidak ikut ditampilkan.
- [x] Jika tidak ada transaksi, API mengembalikan daftar kosong secara konsisten.

## 5. API Contract dan HTTP Response

- [x] Endpoint menggunakan HTTP method dan path yang benar.
- [x] Request body menggunakan JSON untuk endpoint yang memerlukannya.
- [x] Response menggunakan JSON dengan struktur konsisten.
- [x] HTTP status code sesuai kondisi.
- [x] Error response memberikan pesan yang jelas.
- [x] Error tidak membocorkan SQL, stack trace, atau informasi internal.
- [x] Respons GET `/items` menampilkan stok terkini dari database.
- [x] Tidak ada nilai stok yang hanya diperbarui di memori tanpa disimpan ke database.

### 5.1 Web UI

- [x] `GET /` mengembalikan `200 OK` dan halaman HTML.
- [x] Halaman memuat stylesheet dan JavaScript dari folder `static`.
- [x] Dashboard menampilkan ringkasan stok dan daftar alat dari `GET /items`.
- [x] Formulir tambah alat memanggil `POST /items`.
- [x] Formulir peminjaman memanggil `POST /loans`.
- [x] Pencarian riwayat memanggil `GET /loans/student/{student_id}`.
- [x] Tombol pengembalian memanggil `PUT /loans/{id}/return`.
- [x] Pesan error API ditampilkan kepada pengguna tanpa membocorkan detail internal.
- [x] Data dinamis di-escape sebelum dirender untuk mencegah XSS.
- [x] UI memuat ulang data dari server setelah operasi berhasil sehingga stok tetap sinkron.

## 6. Code Quality

- [x] Route/controller tidak menampung seluruh business logic.
- [x] Aturan bisnis ditempatkan pada service layer.
- [x] Operasi query ditempatkan pada repository/data access layer.
- [x] Fungsi memiliki tanggung jawab yang jelas.
- [x] Nama variabel, fungsi, dan modul mudah dipahami.
- [x] Tidak ada duplikasi logika validasi atau transaksi yang tidak perlu.
- [x] Tidak ada hard-coded path database yang menyulitkan konfigurasi.
- [x] Tidak ada kode mati, debug print, atau TODO yang tidak dijelaskan.
- [x] Dependency tercatat di `requirements.txt`.
- [x] Aplikasi dapat dijalankan mengikuti dokumentasi.

## 7. Security dan Reliability

- [x] Input pengguna divalidasi di sisi backend.
- [x] SQL injection dicegah dengan parameterized query.
- [x] Error internal tidak dikirimkan secara mentah kepada client.
- [x] Transaksi database digunakan untuk menjaga konsistensi stok.
- [x] Operasi pengurangan stok bersyarat agar stok tidak menjadi negatif.
- [x] Pengembalian ganda dicegah melalui pemeriksaan status dalam transaksi.
- [x] Tidak ada kredensial atau secret yang disimpan di source code.

Catatan: autentikasi dan otorisasi belum ditetapkan dalam requirement/PRD. Ketiadaannya tidak otomatis dianggap sebagai kegagalan implementasi terhadap ruang lingkup saat ini, tetapi perlu dicatat sebagai batasan sebelum sistem digunakan di lingkungan nyata.

## 8. Test Evidence

- [x] Ada bukti pengujian untuk setiap endpoint.
- [x] Ada pengujian input valid dan tidak valid.
- [x] Ada pengujian stok tidak mencukupi.
- [x] Ada pengujian item dan transaksi yang tidak ditemukan.
- [x] Ada pengujian pengembalian ganda.
- [x] Ada pengujian bahwa stok tetap konsisten ketika transaksi gagal.
- [x] Ada pengujian halaman Web UI dan aset statis.
- [x] Hasil pengujian dapat diulang dengan langkah yang jelas.

Bukti pengujian:

- `pytest -q` menghasilkan **36 passed**.
- Pengujian Web UI mencakup render `GET /`, keberadaan elemen dashboard, akses `style.css`, akses `app.js`, dan penggunaan aplikasi yang sama dengan REST API.
- Smoke test HTTP terhadap server lokal mencakup kelima endpoint, termasuk skenario stok kurang, item tidak ditemukan, dan pengembalian ganda.
- Halaman `GET /` dan aset statis diverifikasi melalui server lokal.
- Koleksi Postman tersedia di `postman/lab_equipment_loan.postman_collection.json`.

## 9. Review Findings

| ID | File/Bagian | Temuan | Tingkat | Rekomendasi | Status |
|---|---|---|---|---|---|
| CR-01 | `docs/requirement.md`, `docs/prd.md` | Format Markdown sebelumnya rusak akibat line-wrap sehingga kata dan heading terpotong. | Low | Menulis ulang tanpa memotong kata. | Resolved |
| CR-02 | `app/schema.sql`, `app/services/loan_service.py` | Status `CANCELLED` diizinkan oleh constraint, tetapi belum ada alur atau endpoint pembatalan. | Low | Tetapkan alur pembatalan atau hapus dari constraint pada iterasi berikutnya. | Open |
| CR-03 | `app/services/loan_service.py` | Belum ada penanganan khusus untuk `SQLITE_BUSY` saat akses tulis bersamaan. | Low | Pertimbangkan `busy_timeout`/WAL dan pengujian konkurensi saat deployment. | Open |

Gunakan tingkat prioritas:

- **Critical:** menyebabkan kehilangan/kerusakan data, stok tidak konsisten, atau celah keamanan serius.
- **High:** aturan bisnis utama tidak berjalan atau endpoint utama gagal.
- **Medium:** validasi, respons API, atau kualitas kode bermasalah tetapi dampaknya terbatas.
- **Low:** masalah keterbacaan, konsistensi, atau perbaikan kecil.

## 10. Review Summary

- **Status:** Approved
- **Jumlah temuan Critical:** 0
- **Jumlah temuan High:** 0
- **Jumlah temuan Medium:** 0
- **Jumlah temuan Low:** 3 (1 Resolved, 2 Open)
- **Catatan reviewer:** Seluruh alur utama berjalan, kelima endpoint tersedia, Web UI terhubung ke REST API, 36 pengujian otomatis lulus, dan smoke test HTTP berhasil. Stok konsisten, pengembalian ganda dicegah, serta rollback transaksi terverifikasi. Temuan yang tersisa bersifat Low dan tidak menghalangi pemenuhan acceptance criteria.

Kode hanya layak disetujui apabila seluruh alur utama berjalan, acceptance criteria terpenuhi, dan tidak ada temuan Critical atau High yang belum diselesaikan.

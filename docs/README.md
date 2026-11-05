# Lab Equipment Loan System

REST API backend untuk mengelola peminjaman alat/fasilitas laboratorium kampus, dengan kontrol stok otomatis dan verifikasi status peminjaman.

## Teknologi

- Python 3.x
- Flask
- SQLite
- JSON

## Struktur Proyek

```text
.
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── errors.py
│   ├── validators.py
│   ├── schema.sql
│   ├── repositories/
│   │   ├── item_repository.py
│   │   └── loan_repository.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── item_routes.py
│   │   └── loan_routes.py
│   └── services/
│       ├── item_service.py
│       └── loan_service.py
├── docs/                   # seluruh dokumen Markdown
│   ├── README.md
│   ├── requirement.md
│   ├── prd.md
│   ├── architecture.md
│   ├── tasks.md
│   └── code_review.md
├── instance/               # database SQLite (tidak di-track Git)
├── postman/                # koleksi Postman
├── tests/                  # pengujian pytest
├── .gitignore
├── run.py
├── requirements.txt
├── requirements-dev.txt
└── pytest.ini
```

## Prasyarat

- Python 3.9 atau lebih baru (diuji dengan Python 3.14.7)

## Instalasi

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Jika hanya ingin menjalankan aplikasi tanpa alat pengujian:

```powershell
pip install -r requirements.txt
```

## Menjalankan Aplikasi

```powershell
.\.venv\Scripts\python.exe run.py
```

Server berjalan di `http://127.0.0.1:5000`.

Database SQLite berada di `instance/lab_equipment.db` dan **dibuat otomatis** saat aplikasi pertama kali dijalankan. Untuk membuat ulang skema secara manual:

```powershell
.\.venv\Scripts\python.exe -m flask --app run init-db
```

## Endpoint

| Method | Endpoint | Fungsi | Sukses |
|---|---|---|---|
| GET | `/items` | Menampilkan daftar alat dan stok terkini | 200 OK |
| POST | `/items` | Menambahkan master alat | 201 Created |
| POST | `/loans` | Mengajukan peminjaman | 201 Created |
| PUT | `/loans/{id}/return` | Mengembalikan alat | 200 OK |
| GET | `/loans/student/{student_id}` | Riwayat pinjaman mahasiswa | 200 OK |

### POST `/items`

```json
{
  "name": "Multimeter",
  "total_stock": 10
}
```

Respons `201 Created`:

```json
{
  "id": 1,
  "name": "Multimeter",
  "total_stock": 10,
  "available_stock": 10
}
```

### POST `/loans`

```json
{
  "student_id": "20240001",
  "item_id": 1,
  "quantity": 2
}
```

Respons `201 Created`:

```json
{
  "id": 1,
  "student_id": "20240001",
  "item_id": 1,
  "quantity": 2,
  "status": "BORROWED",
  "created_at": "2026-11-05T01:00:00Z"
}
```

### PUT `/loans/{id}/return`

Tidak memerlukan body. Respons `200 OK`:

```json
{
  "id": 1,
  "student_id": "20240001",
  "item_id": 1,
  "quantity": 2,
  "status": "RETURNED",
  "created_at": "2026-11-05T01:00:00Z"
}
```

### GET `/loans/student/{student_id}`

Respons `200 OK` berupa array transaksi milik NIM tersebut. Jika belum ada transaksi, hasilnya `[]`.

## Format Respons Error

Semua error menggunakan format yang konsisten:

```json
{
  "error": "Insufficient stock"
}
```

Status code yang digunakan:

| Kondisi | Status |
|---|---|
| Input tidak valid | 400 Bad Request |
| Stok tidak mencukupi | 400 Bad Request |
| Transaksi sudah `RETURNED` | 400 Bad Request |
| Item atau transaksi tidak ditemukan | 404 Not Found |
| Route tidak ditemukan | 404 Not Found |
| Method tidak diizinkan | 405 Method Not Allowed |
| Error internal | 500 Internal Server Error |

## Pengujian

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Pengujian mencakup validasi input, pengurangan/penambahan stok, rollback transaksi, pengembalian ganda, dan filter riwayat mahasiswa.

## Postman

Import file `postman/lab_equipment_loan.postman_collection.json` dari root proyek ke Postman, lalu jalankan request secara berurutan. Variabel koleksi `baseUrl` default-nya `http://127.0.0.1:5000`.

## Batasan

Sesuai ruang lingkup requirement dan PRD saat ini:

- Belum ada autentikasi dan otorisasi.
- Belum ada endpoint ubah/hapus master alat.
- Status `CANCELLED` tersedia di model data, tetapi alur pembatalan belum didefinisikan.
- Belum ada batas maksimum jumlah pinjaman, jatuh tempo, atau denda.
- Belum ada pagination, pencarian, dan pengurutan lanjutan.
- Belum ada konfigurasi deployment production.

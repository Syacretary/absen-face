# 📚 Hadir Otomatis (Smart Library Attendance)

> **Sistem Buku Tamu Perpustakaan Berbasis Pengenalan Wajah (Face Recognition)**
> *Developed by Syacretary - XI 3.2*

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Backend-Flask-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

Aplikasi ini dibuat untuk memodernisasi sistem pencatatan kehadiran di perpustakaan sekolah. Menggantikan buku tamu manual dengan teknologi **Face Recognition** yang cepat, akurat, dan higienis (contactless).

---

## ✨ Fitur Unggulan

1.  **Smart Face Scan:**
    *   **Auto-Capture:** Kamera otomatis memindai wajah saat pengguna melihat lurus ke kamera. Tidak perlu klik tombol.
    *   **Gaze Detection:** Memastikan pengguna fokus ke kamera untuk kualitas data wajah terbaik.
    *   **Anti-Fraud:** Mencegah satu wajah didaftarkan untuk dua identitas berbeda.

2.  **Manajemen Identitas Deterministik:**
    *   Format kelas baku (misal: `XI-MIPA-2`) mencegah kesalahan penulisan siswa.
    *   Sistem validasi form cerdas: Kelas, Jurusan, dan Ruangan menyesuaikan secara dinamis.

3.  **Efisiensi & Keamanan:**
    *   **Sleep Mode:** Kamera hanya aktif saat dibutuhkan untuk menghemat daya dan suhu perangkat.
    *   **Offline First:** Semua data (wajah & log) disimpan di database lokal (`SQLite`). Tidak butuh koneksi internet sekolah.
    *   **Daily Cooldown:** Mencegah satu siswa *spam* absen berkali-kali dalam sehari.

4.  **Admin & Reporting:**
    *   **Export to CSV/Excel:** Laporan bulanan siap dalam satu kali klik.
    *   **Configurable:** Admin bisa mengatur jumlah kelas, jurusan, dan ruangan tanpa menyentuh kodingan.

---

## 🚀 Cara Instalasi (Untuk Admin/Teknisi)

Aplikasi ini dirancang ringan dan bisa berjalan di Laptop/PC standar sekolah dengan webcam.

### Prasyarat
*   Python 3.10 atau lebih baru.
*   Webcam (Internal atau USB).

### Langkah Instalasi
1.  **Clone atau Copy Folder Proyek:**
    Simpan folder `hadir-otomatis` di dokumen komputer.

2.  **Siapkan Environment (Sekali saja di awal):**
    Buka Terminal/CMD di folder proyek, lalu jalankan:
    ```bash
    # 1. Buat Virtual Environment
    python -m venv venv

    # 2. Aktifkan Environment
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate

    # 3. Instal Dependensi
    pip install cmake
    pip install -r requirements.txt
    pip install git+https://github.com/ageitgey/face_recognition_models
    pip install setuptools
    ```

3.  **Jalankan Aplikasi:**
    Setiap pagi, cukup jalankan:
    ```bash
    python app.py
    ```
    Aplikasi akan berjalan di `http://localhost:5000`.

---

## 📖 Cara Penggunaan (Untuk Pustakawan)

### 1. Memulai Hari
1.  Nyalakan Komputer & Jalankan Aplikasi.
2.  Buka browser (Chrome/Edge) dan masuk ke `http://localhost:5000`.
3.  Tekan **F11** untuk *Full Screen* (Mode Kiosk).
4.  Tampilan siap digunakan siswa.

### 2. Alur Siswa
*   **Siswa Lama:** Klik "Mulai" -> Wajah Discan -> Pilih Kegiatan -> Selesai. (Durasi: ~3 detik).
*   **Siswa Baru:** Klik "Mulai" -> Wajah Discan -> Isi Form Nama/Kelas (Sekali saja seumur hidup) -> Pilih Kegiatan -> Selesai.

### 3. Menutup Hari / Laporan
1.  Buka `http://localhost:5000/admin`.
2.  Klik tombol hijau **Download CSV**.
3.  File laporan siap dibuka di Excel.
4.  Matikan aplikasi (tutup terminal).

---

## ⚙️ Konfigurasi Sistem

Admin bisa mengubah struktur kelas (misal tahun depan ada jurusan baru) melalui menu:
`Admin Dashboard` -> `⚙️ Pengaturan Kelas`.

*   **Tingkat Kelas:** Atur apakah Kelas X punya jurusan atau tidak.
*   **Jumlah Ruangan:** Tentukan maksimal ruangan per jurusan.
*   **Daftar Jurusan:** Tambah jurusan baru (misal: "DKV", "TBSM") dengan memisahkannya pakai koma.

---

## 🛠️ Troubleshooting (Masalah Umum)

| Masalah | Solusi |
| :--- | :--- |
| **Kamera tidak muncul** | Pastikan kabel webcam tercolok. Coba refresh halaman (F5). Pastikan tidak ada aplikasi lain (Zoom/Gmeet) yang sedang memakai kamera. |
| **Wajah sulit terdeteksi** | Pastikan pencahayaan ruangan cukup terang. Jangan membelakangi cahaya (backlight). |
| **Data Salah Input** | Admin tidak bisa edit manual. Solusi: Minta siswa daftar ulang dengan wajah yang sama (akan ditolak), atau hapus database jika perlu reset total. |

---

## 📂 Struktur Folder
```
hadir-otomatis/
├── app.py                 # Otak utama aplikasi (Server Flask)
├── config.py              # Konfigurasi dasar
├── database.py            # Model Database
├── requirements.txt       # Daftar pustaka yang dibutuhkan
├── school_config.json     # Konfigurasi kelas (Dinamis)
├── instance/
│   └── hadir_otomatis.db  # Database Tersimpan di sini (JANGAN DIHAPUS)
├── static/
│   ├── css/style.css      # Desain Tampilan (UI)
│   └── js/main.js         # Logika Kamera Client-side
└── templates/             # Halaman-halaman HTML
```

---

*Dibuat dengan ❤️ untuk kemajuan literasi sekolah.*

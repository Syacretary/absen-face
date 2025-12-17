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

## 🆚 Mengapa Beralih dari Google Form?

Banyak perpustakaan sekolah saat ini menggunakan **Google Form** di komputer pintu masuk. Meskipun digital, metode ini memiliki kelemahan fatal:

| Fitur | Google Form Manual ❌ | Hadir Otomatis (Face AI) ✅ |
| :--- | :--- | :--- |
| **Kecepatan** | Lambat (1-2 menit/siswa). Harus mengetik Nama, memilih Kelas, Scroll panjang. | **Instan (3 detik).** Scan wajah -> Pilih aktivitas -> Selesai. |
| **Antrian** | Menyebabkan antrian panjang saat jam istirahat karena proses ketik yang lama. | **Anti-Macet.** Alur super cepat mengurai antrian siswa. |
| **Akurasi Data** | **Rentan Typo.** Siswa sering salah ketik nama atau asal pilih kelas. | **100% Akurat.** Identitas terkunci pada wajah. Tidak ada lagi data "Nama: asdfgh". |
| **Keamanan** | Bisa titip absen (isikan punya teman). | **Anti-Joki.** Wajah siswa harus ada di depan kamera. |
| **Kesehatan** | **Tidak Higienis.** Ratusan siswa menyentuh keyboard/mouse yang sama bergantian. | **Contactless.** Tidak perlu menyentuh apapun (kecuali pilih aktivitas opsional), wajah dideteksi otomatis. |

> *"Ubah komputer Google Form lama Anda menjadi Kiosk AI Canggih tanpa biaya tambahan."*

---

## 🚀 Cara Instalasi (Untuk Admin/Teknisi)

Aplikasi ini dirancang ringan dan bisa berjalan di Laptop/PC standar sekolah dengan webcam.

### Prasyarat
*   **Python 3.10 atau lebih baru** (Disarankan menggunakan Python versi stabil terbaru).
*   **Webcam** (Internal atau USB).
*   **Alat Kompilasi C++:** `face_recognition` dan `dlib` membutuhkan alat kompilasi C++ (`cmake`, `build-essential` di Linux, atau `Developer Tools` di macOS, `Build Tools for Visual Studio` di Windows). Pastikan ini terinstal di sistem Anda.

### Langkah Instalasi
1.  **Clone atau Copy Folder Proyek:**
    Simpan folder `hadir-otomatis` di dokumen komputer.

2.  **Siapkan Environment (Sekali saja di awal):**
    Buka Terminal/CMD di folder proyek, lalu jalankan:
    ```bash
    # 1. Buat Virtual Environment
    python -m venv venv

    # 2. Aktifkan Environment
    # Windows (Command Prompt):
    # venv\Scripts\activate.bat
    # Windows (PowerShell):
    # .\venv\Scripts\Activate.ps1
    # Linux/Mac:
    source venv/bin/activate

    # 3. Instal Dependensi Utama
    # Instal 'cmake' terlebih dahulu (diperlukan oleh dlib/face_recognition)
    pip install cmake

    # Instal dependensi dari requirements.txt
    pip install -r requirements.txt

    # 4. Solusi untuk Masalah 'face_recognition_models' (Penting!)
    # Jika face_recognition mengeluh 'face_recognition_models' tidak terinstal,
    # meskipun sudah di requirements.txt, itu karena ketergantungan 'pkg_resources'
    # yang kadang hilang di Python versi baru. Instal setuptools.
    pip install setuptools

    # Lalu instal ulang face_recognition_models dari git (paksa)
    pip install --force-reinstall git+https://github.com/ageitgey/face_recognition_models
    ```
    **Penting:** Jika Anda masih mengalami masalah setelah langkah-langkah ini, pastikan alat kompilasi C++ Anda sudah terinstal dengan benar di sistem.

3.  **Jalankan Aplikasi:**
    Setiap kali ingin menggunakan aplikasi:
    ```bash
    # 1. Pastikan environment aktif
    # Windows: venv\Scripts\activate
    # Linux/Mac: source venv/bin/activate

    # 2. Jalankan server Flask
    python app.py
    ```
    Aplikasi akan berjalan di `http://localhost:5000`.

---

## 📖 Cara Penggunaan (Untuk Pustakawan)

### 1. Memulai Hari
1.  Nyalakan Komputer & Jalankan Aplikasi (ikuti langkah "Jalankan Aplikasi" di atas).
2.  Buka browser (Chrome/Edge) dan masuk ke `http://localhost:5000`.
3.  Tekan **F11** untuk *Full Screen* (Mode Kiosk).
4.  Tampilan siap digunakan siswa.

### 2. Alur Siswa
*   **Mulai Check-In:** Siswa klik tombol "Mulai Check-In".
*   **Scan Wajah Otomatis:** Posisikan wajah lurus ke kamera. Sistem akan otomatis mendeteksi dan memindai wajah.
*   **Siswa Baru:** Jika wajah belum terdaftar, siswa akan diarahkan ke form pendaftaran. Setelah isi data dan pilih aktivitas, data akan tersimpan permanen.
*   **Siswa Lama:** Jika wajah dikenali, siswa akan langsung diarahkan untuk memilih aktivitas.
*   **Cooldown:** Siswa hanya bisa absen sekali sehari. Jika mencoba scan dua kali, akan muncul notifikasi.

### 3. Menutup Hari / Laporan
1.  Akses halaman Admin: `http://localhost:5000/admin`.
2.  Klik tombol hijau **"📥 Download CSV / Excel"**.
3.  File laporan kunjungan (`laporan_kehadiran.csv`) akan terunduh dan bisa dibuka di Microsoft Excel atau Google Sheets.
4.  Untuk mematikan aplikasi, cukup tutup jendela terminal tempat Anda menjalankan `python app.py`.

---

## ⚙️ Konfigurasi Sistem (Admin)

Admin bisa mengubah struktur kelas dan jurusan melalui menu:
`Admin Dashboard` (`http://localhost:5000/admin`) -> Klik tombol **"⚙️ Pengaturan Kelas"**.

*   **Tingkat Kelas:**
    *   Setiap tingkat (X, XI, XII) bisa diatur apakah memiliki jurusan atau tidak (`Ada Jurusan` / `Tidak Ada Jurusan`).
    *   Tentukan jumlah maksimal ruangan (`Max Ruang`) untuk setiap tingkat (jika tidak ada jurusan) atau per jurusan (jika ada jurusan).
*   **Daftar Jurusan:**
    *   Masukkan daftar nama jurusan yang tersedia di sekolah, pisahkan dengan koma (contoh: `MIPA, IPS, BAHASA, AGAMA`).

Perubahan yang disimpan di halaman ini akan langsung mempengaruhi formulir pendaftaran siswa dan validasi data.

---

## 🛠️ Troubleshooting (Masalah Umum)

| Masalah | Solusi |
| :--- | :--- |
| **Kamera tidak muncul/tidak aktif** | Pastikan webcam tercolok dan berfungsi. Coba refresh halaman (F5). Pastikan tidak ada aplikasi lain (Zoom/GMeet/OBS) yang sedang memakai kamera. Di browser, cek izin kamera untuk `localhost`. |
| **Wajah sulit terdeteksi/scan gagal terus** | Pastikan pencahayaan ruangan cukup terang. Hindari *backlight*. Posisikan wajah lurus dan penuh di depan kamera (ikuti panduan oval di layar). |
| **Error `ModuleNotFoundError: No module named 'pkg_resources'` atau `face_recognition_models` tidak terinstal** | Ikuti langkah instalasi di bagian **"🚀 Cara Instalasi"** dengan teliti, terutama langkah 4 (`pip install setuptools` dan `pip install --force-reinstall git+...`). Ini adalah masalah umum di Python versi baru. |
| **Identitas sudah terdaftar padahal belum pernah** | Cek kembali data yang diinput (Nama, Kelas, No Absen). Mungkin ada kesalahan pengetikan atau identitas yang sama sudah terdaftar dengan wajah lain (ini fitur anti-fraud). |
| **Data Salah Input (Nama/Kelas)** | Aplikasi tidak memiliki fitur edit data identitas secara langsung untuk User. Jika ada kesalahan input saat pendaftaran, admin perlu mengakses database secara manual (menggunakan SQLite Browser) untuk mengedit atau menghapus data User tersebut. Atau, minta siswa mendaftar ulang dengan wajah yang sama (sistem akan menolak jika identitas duplikat), lalu input data yang benar. |
| **Bagaimana jika siswa naik kelas?** | Admin dapat mengekspor data user ke CSV, melakukan perubahan massal di Excel (misal: `X` diganti `XI-MIPA`), lalu mengimpor kembali ke database (fitur import belum tersedia, update manual di DB jika butuh cepat, atau lakukan copy-paste ke halaman register untuk setiap siswa). **Saran:** Fitur export ini memudahkan update massal di Excel. |

---

## 📂 Struktur Folder
```
hadir-otomatis/
├── app.py                 # Otak utama aplikasi (Server Flask)
├── config.py              # Konfigurasi dasar
├── database.py            # Model Database
├── requirements.txt       # Daftar pustaka yang dibutuhkan
├── school_config.json     # Konfigurasi kelas (Dinamis, bisa diedit via Admin UI)
├── instance/
│   └── hadir_otomatis.db  # Database Tersimpan di sini (JANGAN DIHAPUS, berisi data sekolah!)
├── static/
│   ├── css/style.css      # Desain Tampilan (UI & Responsivitas)
│   └── js/main.js         # Logika Kamera Client-side & Auto-Scan
└── templates/             # Halaman-halaman HTML
    ├── activity.html      # Pilih Aktivitas
    ├── admin.html         # Dashboard Admin & Laporan
    ├── admin_config.html  # Pengaturan Kelas & Jurusan (Admin)
    ├── index.html         # Halaman Landing (Mulai Check-In)
    ├── register.html      # Form Pendaftaran Siswa Baru
    └── scan.html          # Halaman Auto-Scan Wajah
```

---

*Dibuat dengan ❤️ untuk kemajuan literasi sekolah.*
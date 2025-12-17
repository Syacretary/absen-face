@echo off
TITLE Hadir Otomatis - Server
COLOR 0A

echo ========================================================
echo        SISTEM KEHADIRAN PERPUSTAKAAN (AI FACE)
echo        Developed by Syacretary
echo ========================================================
echo.
echo [INFO] Sedang menyiapkan sistem...
echo [INFO] Mohon jangan tutup jendela ini selama aplikasi berjalan.
echo.

:: Pindah ke direktori tempat file ini berada
cd /d "%~dp0"

:: Cek apakah folder venv ada
if not exist "venv" (
    COLOR 0C
    echo [ERROR] Folder 'venv' tidak ditemukan!
    echo Silakan install dulu sesuai petunjuk di README.md
    echo.
    pause
    exit
)

:: Aktivasi Virtual Environment
call venv\Scripts\activate

:: Buka browser otomatis (tunggu 5 detik biar server siap dulu)
timeout /t 5 /nobreak >nul
start http://localhost:5000

:: Jalankan Aplikasi Flask
echo [INFO] Server berjalan... Akses di http://localhost:5000
python app.py

pause

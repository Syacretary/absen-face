document.addEventListener('DOMContentLoaded', () => {
    const webcamFeed = document.getElementById('webcamFeed');
    const captureButton = document.getElementById('captureButton');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const loadingOverlay = document.getElementById('loadingOverlay');

    // Toast Notification Function
    function showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerText = message;
        container.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Access webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            webcamFeed.srcObject = stream;
        })
        .catch((err) => {
            console.error("Error accessing webcam: ", err);
            showToast("Gagal mengakses kamera. Periksa izin browser.", 'error');
            captureButton.disabled = true;
            captureButton.innerText = "Kamera Tidak Tersedia";
        });

    captureButton.addEventListener('click', () => {
        // Show loading state
        loadingOverlay.style.display = 'flex';
        captureButton.disabled = true;
        captureButton.innerText = "Memproses...";

        // Set canvas dimensions
        canvas.width = webcamFeed.videoWidth;
        canvas.height = webcamFeed.videoHeight;
        
        // Capture image
        context.drawImage(webcamFeed, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg');

        fetch('/detect_face', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageData }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Backend decides where to go
                if (data.redirect_url) {
                    window.location.href = data.redirect_url;
                }
            } else {
                showToast(data.message || "Gagal mendeteksi wajah.", 'error');
                resetButton();
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            showToast("Kesalahan koneksi server.", 'error');
            resetButton();
        });
    });

    function resetButton() {
        loadingOverlay.style.display = 'none';
        captureButton.disabled = false;
        captureButton.innerText = "Scan Wajah";
    }
});

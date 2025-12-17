import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'hadir_otomatis.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
TEMP_FACE_IMAGE_PATH = os.path.join(BASE_DIR, 'instance', 'temp_face.jpg')
FACE_DETECTION_THRESHOLD = 0.6 # Lower this for stricter matching, higher for more lenient

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(TEMP_FACE_IMAGE_PATH), exist_ok=True) # Ensure 'instance' directory exists for temp_face.jpg
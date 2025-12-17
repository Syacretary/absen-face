import os
import datetime
import base64
import re
import json
import csv
import io
from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session, make_response
import face_recognition
import numpy as np
from PIL import Image
from sqlalchemy.orm import sessionmaker

from config import DATABASE_PATH, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from database import User, Visit, engine, init_db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'kuncirahasia_super_aman' 

init_db()
Session = sessionmaker(bind=engine)

# --- Helper Functions ---

CONFIG_FILE_PATH = 'school_config.json'

def load_school_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Default config if file not found
        return {
            "grades": [
                {"label": "X (Sepuluh)", "value": "X", "has_majors": False, "max_rooms": 10},
                {"label": "XI (Sebelas)", "value": "XI", "has_majors": True, "max_rooms": 4},
                {"label": "XII (Dua Belas)", "value": "XII", "has_majors": True, "max_rooms": 4}
            ],
            "majors": ["MIPA", "IPS", "BAHASA"]
        }

def save_school_config(config_data):
    with open(CONFIG_FILE_PATH, 'w') as f:
        json.dump(config_data, f, indent=4)

def get_face_encodings_from_image(image_data_url):
    try:
        base64_data = re.sub('^data:image/.+;base64,', '', image_data_url)
        binary_data = base64.b64decode(base64_data)
        img = Image.open(BytesIO(binary_data)).convert('RGB')
        img_np = np.array(img)
        
        face_locations = face_recognition.face_locations(img_np)
        if not face_locations: return None, "Wajah tidak ditemukan."
        if len(face_locations) > 1: return None, "Satu orang saja."

        face_landmarks_list = face_recognition.face_landmarks(img_np, face_locations)
        if face_landmarks_list:
            landmarks = face_landmarks_list[0]
            left_eye = np.mean(landmarks['left_eye'], axis=0)
            right_eye = np.mean(landmarks['right_eye'], axis=0)
            nose_bridge = np.mean(landmarks['nose_bridge'], axis=0)
            ratio = np.linalg.norm(left_eye - nose_bridge) / np.linalg.norm(right_eye - nose_bridge)
            if ratio < 0.6 or ratio > 1.4: return None, "Harap lihat lurus ke kamera."

        face_encodings = face_recognition.face_encodings(img_np, face_locations)
        if not face_encodings: return None, "Gagal memproses fitur wajah."

        return face_encodings[0], None
    except Exception as e:
        return None, f"Error: {str(e)}"

# --- Routes ---

@app.route('/')
def index():
    session.pop('temp_face', None)
    session.pop('temp_user_data', None)
    session.pop('temp_user_id', None)
    return render_template('index.html')

@app.route('/scan')
def scan_page():
    return render_template('scan.html')

@app.route('/detect_face', methods=['POST'])
def detect_face():
    db_session = Session()
    try:
        image_data_url = request.json['image']
        current_encoding, error = get_face_encodings_from_image(image_data_url)

        if error: return jsonify({"status": "retry", "message": error})
        
        known_users = db_session.query(User).all()
        if known_users:
            known_encodings = [user.get_face_encoding_array() for user in known_users]
            matches = face_recognition.compare_faces(known_encodings, current_encoding, tolerance=0.45)
            face_distances = face_recognition.face_distance(known_encodings, current_encoding)
            best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else -1

            if best_match_index != -1 and matches[best_match_index]:
                user = known_users[best_match_index]
                today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0)
                recent_visit = db_session.query(Visit).filter(Visit.user_id == user.id, Visit.timestamp >= today_start).first()

                if recent_visit:
                     return jsonify({"status": "success", "redirect_url": url_for('index'), "alert": f"Halo {user.name}, Anda sudah absen hari ini."})

                session['temp_user_id'] = user.id
                return jsonify({"status": "success", "redirect_url": url_for('activity_existing')})

        session['temp_face'] = current_encoding.tolist()
        return jsonify({"status": "success", "redirect_url": url_for('register')})

    except Exception as e: return jsonify({"status": "error", "message": "Server Error"})
    finally: db_session.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'temp_face' not in session:
        flash("Sesi habis. Silakan scan wajah ulang.", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form['name'].strip().upper()
        grade_val = request.form['grade']
        absent_number = request.form['absent_number']
        
        full_class_name = ""
        grade_config = next((g for g in load_school_config()['grades'] if g['value'] == grade_val), None)
        if grade_config and grade_config['has_majors']:
            major = request.form['major']
            room = request.form['room']
            full_class_name = f"{grade_val}-{major}-{room}"
        else:
            room = request.form['room']
            full_class_name = f"{grade_val}-{room}"

        db_session = Session()
        existing_user = db_session.query(User).filter_by(
            name=name, 
            class_name=full_class_name, 
            absent_number=absent_number
        ).first()
        db_session.close()

        if existing_user:
            flash(f"Gagal! Identitas '{name} ({full_class_name} No.{absent_number})' sudah terdaftar dengan wajah lain.", "error")
            config = load_school_config()
            return render_template('register.html', config=config)

        session['temp_user_data'] = {
            'name': name,
            'class_name': full_class_name,
            'absent_number': absent_number
        }
        return redirect(url_for('activity_new'))

    config = load_school_config()
    return render_template('register.html', config=config)

@app.route('/activity/new', methods=['GET', 'POST'])
def activity_new():
    if 'temp_face' not in session or 'temp_user_data' not in session: return redirect(url_for('index'))
    user_data = session['temp_user_data']
    if request.method == 'POST':
        db_session = Session()
        try:
            activity_type = request.form['activity_type']
            if activity_type == 'other': activity_type = request.form['custom_activity']
            
            exists = db_session.query(User).filter_by(name=user_data['name'], class_name=user_data['class_name']).first()
            if exists:
                flash("Identitas sudah terdaftar.", "error")
                return redirect(url_for('index'))

            face_encoding_bytes = np.array(session['temp_face']).tobytes()
            new_user = User(name=user_data['name'], class_name=user_data['class_name'], absent_number=user_data['absent_number'], face_encoding=face_encoding_bytes)
            db_session.add(new_user)
            db_session.flush()
            new_visit = Visit(user_id=new_user.id, activity=activity_type)
            db_session.add(new_visit)
            db_session.commit()
            flash(f"Selamat Datang, {new_user.name}!", "success")
            return redirect(url_for('index'))
        except Exception: db_session.rollback(); return redirect(url_for('index'))
        finally: db_session.close()
    return render_template('activity.html', user_name=user_data['name'], is_new=True)

@app.route('/activity/existing', methods=['GET', 'POST'])
def activity_existing():
    if 'temp_user_id' not in session: return redirect(url_for('index'))
    user_id = session['temp_user_id']
    db_session = Session()
    user = db_session.query(User).get(user_id)
    if request.method == 'POST':
        try:
            activity_type = request.form['activity_type']
            if activity_type == 'other': activity_type = request.form['custom_activity']
            new_visit = Visit(user_id=user_id, activity=activity_type)
            db_session.add(new_visit)
            db_session.commit()
            flash(f"Berhasil check-in: {activity_type}", "success")
            return redirect(url_for('index'))
        except Exception: pass
        finally: db_session.close()
    db_session.close()
    return render_template('activity.html', user_name=user.name, is_new=False)

@app.route('/admin')
def admin():
    db_session = Session()
    visits = db_session.query(Visit).order_by(Visit.timestamp.desc()).all()
    visit_data = []
    for visit in visits:
        user = db_session.query(User).get(visit.user_id)
        visit_data.append({'name': user.name if user else 'Unknown', 'class_name': user.class_name if user else '-', 'absent_number': user.absent_number if user else '-', 'activity': visit.activity, 'timestamp': visit.timestamp.strftime('%H:%M - %d/%m/%Y')})
    db_session.close()
    return render_template('admin.html', visits=visit_data)

@app.route('/admin/config', methods=['GET', 'POST'])
def admin_config():
    config = load_school_config()
    if request.method == 'POST':
        try:
            new_grades = []
            for i in range(len(config['grades'])):
                grade_value = request.form[f'grade_{i}_value']
                grade_label = request.form[f'grade_{i}_label']
                has_majors = 'true' == request.form.get(f'grade_{i}_has_majors', 'false')
                max_rooms = int(request.form[f'grade_{i}_max_rooms'])
                new_grades.append({
                    "label": grade_label,
                    "value": grade_value,
                    "has_majors": has_majors,
                    "max_rooms": max_rooms
                })
            
            new_majors_str = request.form['majors_list']
            new_majors = [m.strip().upper() for m in new_majors_str.split(',') if m.strip()]

            new_config = {
                "grades": new_grades,
                "majors": new_majors
            }
            save_school_config(new_config)
            flash("Konfigurasi berhasil disimpan!", "success")
            return redirect(url_for('admin_config'))
        except Exception as e:
            flash(f"Gagal menyimpan konfigurasi: {e}", "error")
            return redirect(url_for('admin_config'))

    return render_template('admin_config.html', config=config)


@app.route('/admin/export/csv')
def export_csv():
    db_session = Session()
    visits = db_session.query(Visit).order_by(Visit.timestamp.desc()).all()
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Timestamp', 'Nama', 'Kelas', 'No Absen', 'Aktivitas'])
    
    for visit in visits:
        user = db_session.query(User).get(visit.user_id)
        cw.writerow([
            visit.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            user.name if user else 'Unknown',
            user.class_name if user else 'N/A',
            user.absent_number if user else 'N/A',
            visit.activity
        ])
    
    db_session.close()
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=laporan_kehadiran.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

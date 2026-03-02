"""
Flask Web Application for Team Thiran - Diabetic Retinopathy Detection
This is a separate interface to the backend. The original Tkinter GUI (blindness.py) remains unchanged.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import timedelta
from urllib.parse import unquote
import mysql.connector
from dotenv import load_dotenv
from PIL import Image
import io
import base64

# Add parent directory to path for backend imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.model import model, inference, test_transforms, classes, main
from reports.report_generator import create_report, MedicalReportGenerator
from reports.pdf_report import create_pdf_report

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'team-thiran-secret-key-medical-app')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize ML Model (model is already loaded in backend.model)
print("[Flask App] DR Detection Model imported successfully")
print(f"[Flask App] ✅ Model ready with {len(classes)} classification levels")

# Database connection function
def get_db_connection():
    """Get MySQL database connection with credentials from environment"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'dr_user'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'BLINDNESS'),
            autocommit=True
        )
        return connection
    except mysql.connector.Error as e:
        print(f"[Flask App] Database connection error: {e}")
        return None

# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            return render_template('login.html', error='Username and password required')

        try:
            conn = get_db_connection()
            if not conn:
                return render_template('login.html', error='Database connection failed')

            cursor = conn.cursor()
            query = "SELECT 1 FROM THEGREAT WHERE USERNAME = %s AND PASSWORD = %s"
            cursor.execute(query, (username, password))

            if cursor.fetchone():
                session['user_id'] = username
                session.permanent = True
                cursor.close()
                conn.close()
                return redirect(url_for('dashboard'))
            else:
                cursor.close()
                conn.close()
                return render_template('login.html', error='Invalid username or password')

        except Exception as e:
            return render_template('login.html', error=f'Login error: {str(e)}')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup route"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        # Validation
        if not username or not password:
            return render_template('signup.html', error='Username and password required')

        if len(username) < 3:
            return render_template('signup.html', error='Username must be at least 3 characters')

        if len(password) < 6:
            return render_template('signup.html', error='Password must be at least 6 characters')

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        try:
            conn = get_db_connection()
            if not conn:
                return render_template('signup.html', error='Database connection failed')

            cursor = conn.cursor()

            # Check if user exists
            check_query = "SELECT 1 FROM THEGREAT WHERE USERNAME = %s"
            cursor.execute(check_query, (username,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return render_template('signup.html', error='Username already exists')

            # Insert new user
            insert_query = "INSERT INTO THEGREAT (USERNAME, PASSWORD) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, password))

            cursor.close()
            conn.close()

            return render_template('signup.html', success='Account created successfully! Please login.')

        except Exception as e:
            return render_template('signup.html', error=f'Signup error: {str(e)}')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    return redirect(url_for('login'))

# ============================================================================
# MAIN APPLICATION ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home page - redirect to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html', username=session.get('user_id'))

@app.route('/upload')
@login_required
def upload():
    """Image upload page"""
    return render_template('upload.html')

@app.route('/api/predict', methods=['POST'])
@login_required
def api_predict():
    """API endpoint for DR prediction"""
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Validate file type
        allowed_extensions = {'jpg', 'jpeg', 'png', 'bmp', 'tiff'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': 'Invalid file format. Allowed: JPG, PNG, BMP, TIFF'}), 400

        # Read and process image
        image = Image.open(io.BytesIO(file.read())).convert('RGB')

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        # Run inference using backend model
        prediction, prediction_class, confidence_score = inference(
            model,
            filepath,
            test_transforms,
            classes,
            return_confidence=True
        )

        # Create base64 thumbnail for display
        thumb = image.copy()
        thumb.thumbnail((300, 300))
        thumb_io = io.BytesIO()
        thumb.save(thumb_io, format='PNG')
        thumb_io.seek(0)
        thumb_b64 = base64.b64encode(thumb_io.getvalue()).decode()

        return jsonify({
            'success': True,
            'prediction': int(prediction),
            'severity': prediction_class,
            'confidence': f'{confidence_score:.2%}',
            'image_path': filepath,
            'thumbnail': f'data:image/png;base64,{thumb_b64}'
        })

    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/api/generate-report', methods=['POST'])
@login_required
def api_generate_report():
    """API endpoint to generate medical report"""
    try:
        data = request.get_json()

        prediction = data.get('prediction')
        confidence = data.get('confidence', '95.00%')
        patient_info = data.get('patient_info', {})
        image_path = data.get('image_path')

        if prediction is None:
            return jsonify({'error': 'Prediction required'}), 400

        # Extract confidence value (remove % if present)
        confidence_value = float(confidence.replace('%', '')) if isinstance(confidence, str) else confidence

        # Create report using correct function signature
        report = create_report(
            username=patient_info.get('name', 'Anonymous'),
            severity_level=prediction,
            confidence_score=confidence_value,
            image_path=image_path,
            age=patient_info.get('age', 'Not provided'),
            gender=patient_info.get('gender', 'Not specified')
        )

        # Create PDF
        pdf_path = create_pdf_report(report)

        return jsonify({
            'success': True,
            'report': report,
            'pdf_path': pdf_path,
            'report_id': report.get('report_id')
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500

@app.route('/api/download-report/<report_id>', methods=['GET'])
@login_required
def api_download_report(report_id):
    """Download generated PDF report by report ID"""
    try:
        safe_report_id = unquote(report_id).strip()
        if not safe_report_id or '..' in safe_report_id or '/' in safe_report_id or '\\' in safe_report_id:
            return jsonify({'error': 'Invalid report ID'}), 400

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        reports_dir = os.path.join(project_root, 'reports', 'generated_reports')
        pdf_file = os.path.join(reports_dir, f"{safe_report_id}.pdf")

        if not os.path.exists(pdf_file):
            return jsonify({'error': 'Report file not found'}), 404

        return send_file(
            pdf_file,
            as_attachment=True,
            download_name=f"{safe_report_id}.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': f'Unable to download report: {str(e)}'}), 500

@app.route('/api/send-notification', methods=['POST'])
@login_required
def api_send_notification():
    """Notifications are intentionally disabled for demo mode"""
    return jsonify({
        'error': 'Notification module is disabled for the current demo build. Please download the report PDF instead.'
    }), 503

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  TEAM THIRAN - DIABETIC RETINOPATHY DETECTION (Web Interface)")
    print("="*70)
    print(f"  📱 Flask App starting on http://localhost:5000")
    print(f"  ✅ Model status: {'Loaded' if model else 'NOT LOADED'}")
    print(f"  📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print("="*70 + "\n")

    # Run Flask development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Prevent model from loading twice
    )

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import sys
import threading

# Add parent directory to path to import automation code
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from src.automation import DiceAutomation
from src.utils.webdriver_setup import setup_driver

# Initialize Flask app with correct template and static folders
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'your_secret_key'

# Configuration
UPLOAD_FOLDER = os.path.join(parent_dir, 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB limit
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create necessary directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)

# Store current automation status and resume path
automation_status = {
    "status": "idle",
    "message": "",
    "jobs_processed": 0,
    "applications_submitted": 0
}
current_resume_path = None

def allowed_file(filename):
    """Check if uploaded file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def status_callback(status):
    """Callback function to update automation status."""
    global automation_status
    automation_status.update(status)
    print(f"Status updated: {status}")  # Debug print

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/status')
def status():
    """Render the status page."""
    return render_template('status.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle resume file uploads."""
    global current_resume_path

    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the file
            file.save(filepath)
            current_resume_path = filepath
            
            print(f"Resume saved at: {current_resume_path}")  # Debug print
            
            return jsonify({
                "message": "File uploaded successfully",
                "filename": filename,
                "path": filepath
            })
        except Exception as e:
            print(f"Error saving file: {str(e)}")  # Debug print
            return jsonify({"error": f"Failed to save file: {str(e)}"}), 500
    
    return jsonify({"error": "Invalid file type"}), 400

@app.route('/api/start', methods=['POST'])
def start_automation():
    """Start the automation process."""
    global current_resume_path
    data = request.json
    print(f"Received data: {data}")  # Debug print

    # Validate input
    required_fields = ['username', 'password', 'keyword', 'max_applications']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Extract filters from request data
        filters = {
            'today_only': data.get('filters', {}).get('today_only', False),
            'third_party': data.get('filters', {}).get('third_party', False)
        }
        
        print(f"Current resume path: {current_resume_path}")  # Debug print
        print(f"Extracted filters: {filters}")  # Debug print

        if not current_resume_path or not os.path.exists(current_resume_path):
            return jsonify({"error": "Please upload a resume first"}), 400

        # Setup WebDriver
        driver, wait = setup_driver()

        # Create a DiceAutomation instance with filters
        automation = DiceAutomation(
            driver=driver,
            wait=wait,
            username=data['username'],
            password=data['password'],
            keyword=data['keyword'],
            max_applications=int(data['max_applications']),
            filters=filters,
            status_callback=status_callback
        )

        # Update config with current resume path
        from config import RESUME_SETTINGS
        RESUME_SETTINGS['path'] = current_resume_path
        print(f"Updated resume path in config: {RESUME_SETTINGS['path']}")  # Debug print

        # Validate login
        if not automation.login():
            driver.quit()
            return jsonify({"error": "Invalid credentials. Please check your username and password."}), 401

        # Start the automation in a separate thread
        def run_automation():
            try:
                print("Starting automation with filters:", filters)
                print("Using resume path:", current_resume_path)
                result = automation.run()
                print("Automation result:", result)  # Debug print
            except Exception as e:
                print(f"Error in automation thread: {e}")  # Debug print
            finally:
                driver.quit()

        automation_thread = threading.Thread(target=run_automation)
        automation_thread.daemon = True
        automation_thread.start()

        return jsonify({
            "message": "Login successful. Automation started!",
            "filters_applied": filters,
            "resume_path": current_resume_path
        }), 200

    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        print(f"Error starting automation: {e}")  # Debug print
        return jsonify({"error": str(e)}), 500

@app.route('/api/status')
def get_status():
    """Return the current automation status."""
    return jsonify(automation_status)

import os

if __name__ == "__main__":
    print(f"Template directory: {template_dir}")
    print(f"Static directory: {static_dir}")
    print(f"Upload directory: {UPLOAD_FOLDER}")

    # Fetch the PORT from environment variables or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    try:
        app.run(host="0.0.0.0", port=port, debug=False)  # Use 0.0.0.0 for external access
    except OSError as e:
        print(f"Failed to start on port {port}. Please check your configuration.")
        raise

# from flask import Flask, render_template, request, jsonify
# from werkzeug.utils import secure_filename
# import os
# import sys
# import threading

# # Add parent directory to path to import automation code
# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(parent_dir)

# from src.automation import DiceAutomation
# from src.utils.webdriver_setup import setup_driver

# # Initialize Flask app with correct template and static folders
# template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
# static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
# app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
# app.secret_key = 'your_secret_key'

# # Configuration
# UPLOAD_FOLDER = os.path.join(parent_dir, 'uploads')
# ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Create necessary directories
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)

# # Store automation status
# automation_status = {
#     "status": "idle",
#     "message": "",
#     "total_jobs": 0,
#     "jobs_processed": 0,
#     "applications_submitted": 0,
#     "current_job": 0
# }

# def allowed_file(filename):
#     """Check if uploaded file has allowed extension."""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def status_callback(status):
#     """Callback function to update automation status."""
#     global automation_status
#     automation_status.update(status)

# @app.route('/')
# def index():
#     """Render the main page."""
#     return render_template('index.html')

# @app.route('/status')
# def status():
#     """Render the status page."""
#     return render_template('status.html')

# @app.route('/api/start', methods=['POST'])
# def start_automation():
#     """Start the automation process."""
#     data = request.json
#     print("Received data in /api/start:", data)  # Debug print
#     print("Filters received:", data.get('filters'))  # Debug print

#     # Validate input
#     required_fields = ['username', 'password', 'keyword', 'max_applications']
#     if not all(field in data for field in required_fields):
#         return jsonify({"error": "Missing required fields"}), 400

#     try:
#         # Extract filters from request data
#         filters = {
#             'today_only': data.get('filters', {}).get('today_only', False),
#             'third_party': data.get('filters', {}).get('third_party', False)
#         }
#         print(f"Extracted filters: {filters}")  # Debug print

#         # Setup WebDriver
#         driver, wait = setup_driver()

#         # Create a DiceAutomation instance with filters
#         automation = DiceAutomation(
#             driver=driver,
#             wait=wait,
#             username=data['username'],
#             password=data['password'],
#             keyword=data['keyword'],
#             max_applications=int(data['max_applications']),
#             filters=filters,  # Pass filters here
#             status_callback=status_callback
#         )

#         # Validate login
#         if not automation.login():
#             driver.quit()
#             return jsonify({"error": "Invalid credentials. Please check your username and password."}), 401

#         # Start the automation in a separate thread
#         def run_automation():
#             try:
#                 print("Starting automation with filters:", filters)  # Debug print
#                 automation.run()
#             except Exception as e:
#                 print(f"Error in automation thread: {e}")
#             finally:
#                 driver.quit()

#         automation_thread = threading.Thread(target=run_automation)
#         automation_thread.daemon = True
#         automation_thread.start()

#         return jsonify({
#             "message": "Login successful. Automation started!",
#             "filters_applied": filters  # Return applied filters in response
#         }), 200

#     except Exception as e:
#         if 'driver' in locals():
#             driver.quit()
#         print(f"Error starting automation: {e}")  # Debug print
#         return jsonify({"error": str(e)}), 500

# @app.route('/api/status')
# def get_status():
#     """Return the current automation status."""
#     return jsonify(automation_status)

# @app.route('/api/upload', methods=['POST'])
# def upload_file():
#     """Handle resume file uploads."""
#     if 'resume' not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files['resume']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#         return jsonify({
#             "message": "File uploaded successfully",
#             "filename": filename,
#             "path": filepath
#         })

#     return jsonify({"error": "Invalid file type"}), 400

# if __name__ == '__main__':
#     print(f"Template directory: {template_dir}")
#     print(f"Static directory: {static_dir}")
#     print(f"Upload directory: {UPLOAD_FOLDER}")
#     try:
#         app.run(debug=True, port=5001)
#     except OSError as e:
#         print(f"Failed to start on port 5001. Trying alternative port 5002...")
#         try:
#             app.run(debug=True, port=5002)
#         except OSError:
#             print("Failed to start on port 5002 as well. Please specify a different port.")
#             raise

from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_cors import CORS
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
from werkzeug.utils import secure_filename
import threading

app = Flask(__name__)
CORS(app)

# Set the upload folder
app.config['UPLOADED_FILES_DEST'] = 'static/uploads'
if not os.path.exists(app.config['UPLOADED_FILES_DEST']):
    os.makedirs(app.config['UPLOADED_FILES_DEST'])

# Define supported file types
DOCUMENTS = ('pdf', 'doc', 'docx')
AUDIO = ('mp3',)

# Initialize UploadSet with supported file types
files = UploadSet('files', IMAGES + DOCUMENTS + AUDIO)
configure_uploads(app, files)

# Function to handle unicast communication
def handle_unicast(message, recipient):
    # Implement unicast logic here
    pass

# Function to handle multicast communication
def handle_multicast(message, recipients):
    # Implement multicast logic here
    pass

# Function to handle broadcast communication
def handle_broadcast(message):
    # Implement broadcast logic here
    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    recipients = data.get('recipients')
    if isinstance(recipients, list):
        threading.Thread(target=handle_multicast, args=(message, recipients)).start()
    elif recipients == 'all':
        threading.Thread(target=handle_broadcast, args=(message,)).start()
    else:
        threading.Thread(target=handle_unicast, args=(message, recipients)).start()
    return jsonify({"status": "Message sent"}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOADED_FILES_DEST'], filename))
        return jsonify({"status": "File uploaded"}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_FILES_DEST'], filename)

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    port = int(os.getenv('PORT', 11008))  # Ubah nilai default port menjadi 11008
    app.run(host='0.0.0.0', port=port, threaded=True)

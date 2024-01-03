import os
from datetime import datetime
from flask import Flask, redirect, request, flash, render_template, url_for, send_file
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpeg', 'jpg', 'gif'}

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def check_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', uploaded_files = os.listdir(app.config['UPLOAD_FOLDER']))

# Upload File
@app.route('/upload', methods = ['POST'])
def upload():
    # Check file get
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect('/')
    
    # Check file selected
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect('/')
    
    # Check allowed file and upload
    if file and check_allowed_file(file.filename):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = secure_filename(f"{timestamp}_{file.filename}")

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/')
    else:
        flash('No alowed file', 'error')
        return redirect('/')

# Download File
@app.route('/download/<filename>', methods = ['POST'])
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

# Delete File
@app.route('/delete/<filename>', methods = ['POST'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        os.remove(file_path)
        flash(f'File {filename} deleted successfully', 'success')
    except OSError as e:
        flash(f'Error deleting file {filename}: {str(e)}', 'error')
    return redirect('/')

# Edit File(Image)
@app.route('/edit/<filename>', methods = ['POST'])
def edit(filename):
    return render_template('editor.html', filename = filename)

@socketio.on('mousemove')
def handle_mousemove(data):
    x = data['x']
    y = data['y']
    print(f"Received mouse coordinates: ({x}, {y})")

if __name__ == '__main__':
    socketio.run(app, debug=True)
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash

UPLOAD_FOLDER = '/home/diachenkorp/Desktop/Git/NG_ImgEdit/frontend/static/uploaded_images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

webserver = Flask(__name__)
webserver.secret_key = 'seckey'
webserver.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@webserver.route('/')
def index():
    uploaded_images = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", uploaded_images = uploaded_images)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@webserver.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_images = os.listdir(UPLOAD_FOLDER)
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename) and len(uploaded_images) == 0:
            filename = secure_filename(file.filename)
            file.save(os.path.join(webserver.config['UPLOAD_FOLDER'], filename))
            flash("File uploaded", 'info')
            return redirect('/')
        else:
            flash("Not correct file extension or file has been uploaded", 'error')
        return redirect('/')
    
    return redirect('/')


webserver.run('0.0.0.0', port = 10000, debug = True)
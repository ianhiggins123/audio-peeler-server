from app import app
from pathlib import Path    
from flask import Flask, flash, request, redirect, url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename
import os
import random
import string



UPLOAD_FOLDER = Path('/root/demucs/upload_files/')
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'flac'}



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def demucsServer():
    if request.method == 'POST':
            #letters = string.hexdigits
            #randUrl = ( ''.join(random.choice(letters) for i in range (16)))
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                filePath = '/root/demucs/upload_files/' + filename
                command = "python3 -m demucs.separate -d cpu " + filePath
                os.system(command)
                return '''<h1>SUCCESS</h1>'''#redirect(request.url)#+randUrl+'/')
    #if request.method == 'GET':
            
    return ''
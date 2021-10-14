from app import app
from pathlib import Path    
from flask import Flask, flash, request, redirect, url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename
import os
import random
import string
import shutil



UPLOAD_FOLDER = 'uploaded_files/'
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'flac'}



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def demucsServer():
    if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                letters = string.hexdigits
                randUrl = ( ''.join(random.choice(letters) for i in range (16)))
                filename = secure_filename(file.filename)
                filePath = UPLOAD_FOLDER + randUrl + '/'
                os.makedirs(filePath)
                file.save(os.path.join(filePath, filename))
                command = "python3 -m demucs.separate -d cpu " + filePath + filename + " --out=" + filePath
                os.system(command)
                returnUrl = 'http://172.105.151.238:5000/uploaded_files/' + randUrl +'/' + filename
                returnHTML = '''<p>Go to <a href=''' + returnUrl + '''>this</a> link to download your split files'''
                return returnHTML #redirect(request.url)#+randUrl+'/')

@app.route('/uploaded_files/<returnURL>/<returnSongName>', methods=['GET', 'POST'])
def getFile(returnURL, returnSongName):
    returnFile = Path(returnSongName).stem
    returnFilePath = UPLOAD_FOLDER + returnURL + '/' + 'demucs_quantized/' + returnFile
    shutil.make_archive(UPLOAD_FOLDER + returnURL + '/' + returnFile, 'zip', returnFilePath)
    currDir = os.getcwd()
    print(currDir)
    readyToSend = currDir + '/' + UPLOAD_FOLDER + returnURL + '/'
    returnAsZip = returnFile + '.zip'
   
    try:
        return send_from_directory(directory=readyToSend, path=returnAsZip, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/test')
def test():
    return '''<form method="post" action="/" enctype="multipart/form-data">
    <dl>
		<p>
			<input type="file" name="file" autocomplete="off" required>
		</p>
    </dl>
    <p>
		<input type="submit" value="Submit">
	</p>
</form>'''
    
    return ''
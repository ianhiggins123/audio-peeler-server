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
    """Sets allowed extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'OPTIONS'])
#This is the main URL for receiving audio files.  This is the basic function that receives  a file from the home page of the front-end of the app

def demucsServer():
    """If file is usable, this function generates a path for the file to be stored on the server, saves the file in that directory and then runs demucs on the file.  After that, it stores the zip file in a directory under where the sent file is stored.  This function returns a URL from which a GET request will return the .zip file."""

    if request.method == 'OPTIONS' or 'POST':
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
                command = "sudo python3 -m demucs.separate -d cpu " + filePath + filename + " --out=" + filePath
                os.system(command)
                returnUrl = 'https://audio-peeler-server.com/uploaded_files/' + randUrl +'/' + filename
                #return redirect(returnUrl)
                return returnUrl
                #return returnHTML #redirect(request.url)#+randUrl+'/')

@app.route('/uploaded_files/<returnURL>/<returnSongName>', methods=['GET', 'POST'])
#This is a dynamic URL that will return the .zip file created previously in a POST request.  The 'returnURL' and 'returnSongName' parameters are used to locate the file on the demucs server.

def getFile(returnURL, returnSongName):
    """This function finds the requested song and returns the .zip file containing the song's 4 equalized tracks"""

    returnFile = Path(returnSongName).stem
    returnFilePath = UPLOAD_FOLDER + returnURL + '/' + 'demucs_quantized/' + returnFile
    shutil.make_archive(UPLOAD_FOLDER + returnURL + '/' + returnFile, 'zip', returnFilePath)
    currDir = os.getcwd()
    readyToSend = currDir + '/' + UPLOAD_FOLDER + returnURL + '/'
    returnAsZip = returnFile + '.zip'
    try:
        return send_from_directory(directory=readyToSend, path=returnAsZip, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/urlDownload', methods=['POST', 'OPTIONS'])
#This is the URL used for receiving URLs from the designated 3rd Party applications (Youtube, Soundcloud and Spotify), pulling a usable song from those pages and then running demucs on the audio files.

def urlDownload():
    """This function first checks for the type of URL sent (request.form), runs the appropriate URL-to-mp3 function, and then runs demucs on it.  It functions almost identically to the demucsServer function."""

    if request.method == 'OPTIONS' or 'POST':
        letters = string.hexdigits
        randUrl = ( ''.join(random.choice(letters) for i in range (16)))
        if request.form['soundcloudUrl']:
            soundcloudSongUrl = request.form['soundcloudUrl']
            filePath = UPLOAD_FOLDER + randUrl + '/'
            os.makedirs(filePath)
            soundcloudCommand = "sc-dl -u " + soundcloudSongUrl + " --dir uploaded_files/" + randUrl + "/"
            os.system(soundcloudCommand)
            soundcloudSongPath = os.listdir(UPLOAD_FOLDER + randUrl + "/")[0]            
            soundcloudDemucs = "sudo python3 -m demucs.separate -d cpu " + filePath + "\"" + soundcloudSongPath + "\" --out=" + UPLOAD_FOLDER + randUrl + "/"
            os.system(soundcloudDemucs)
            soundcloudReturnUrl = 'https://audio-peeler-server.com/uploaded_files/' + randUrl + '/' + soundcloudSongPath
            return soundcloudReturnUrl
        if request.form['youtubeUrl']:
            youtubeSongUrl = request.form['youtubeUrl']
            songID = youtubeSongUrl.replace('https://www.youtube.com/watch?v=', '')
            youtubeCommand = "youtube-dl -x --audio-format mp3 " + youtubeSongUrl + " -o  './uploaded_files/" + randUrl + "/%(id)s.mp3' --force-ipv4 --rm-cache-dir"
            os.system(youtubeCommand)
            youtubePath = UPLOAD_FOLDER + randUrl + '/'
            youtubeDemucs = "sudo python3 -m demucs.separate -d cpu " + youtubePath + songID + ".mp3 --out=" + youtubePath
            os.system(youtubeDemucs)
            youtubeReturnUrl = 'https://audio-peeler-server.com/uploaded_files/' + randUrl + '/' + songID
            return youtubeReturnUrl
        #if request.form['spotifyUrl']:


@app.route('/test')
#This is a URL for testing the demucsServer function.  It returns a basic HTML form from which a file can be uploaded and submitted to the server.
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

@app.route('/urlDownloadTest')
#This is a URL for testing the urlDownload function.  It returns three basic forms from which the respective 3rd Party Web URLs may be submitted to the server.

def urlDownloadTest():
    return '''<form method="post" action="/urlDownload" enctype="multipart/form-data">
    <dl>
        <h1>Note: Don't do more than one submit at once! </h1>
        <dt>Youtube</dt>
        <dd>
            Post your Youtube URL: <input type="text" name="youtubeUrl" autocomplete="off">
        </dd>

        <dt>Soundcloud</dt>
        <dd>
            Post your Soundcloud URL: <input type="text" name="soundcloudUrl" autocomplete="off">
        </dd>
        <dt>Spotify</dt>
        <dd>
            Post your Spotify: <input type="text" name="spotifyUrl" autocomplete="off">
        </dd>
    </dl>
    <p>
        <input type="submit" value="Submit">
    </p>
</form>'''

    return ''

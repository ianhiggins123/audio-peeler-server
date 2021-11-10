import os
from flask import Flask, flash, request, redirect, url_for, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

"""Sets the flask name as variable 'app' and then sets CORS"""
app = Flask(__name__)
CORS(app)

"""Runs the server!"""
if __name__ == "__main__":
	app.run(ssl_context=("/etc/letsencrypt/live/audio-peeler-server.com/fullchain.pem", "/etc/letsencrypt/live/audio-peeler-server.com/privkey.pem"))

from app import api

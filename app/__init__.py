import os
from flask import Flask, flash, request, redirect, url_for, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

from app import api
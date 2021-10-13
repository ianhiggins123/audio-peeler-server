import os
from flask import Flask, flash, request, redirect, url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

from app import api
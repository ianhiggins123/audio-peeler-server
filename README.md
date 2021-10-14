# audio-peeler-server

## Installation

Due to file size, dependencies cannot be stored in this repository.  Make sure to recreate these steps when installing server for first time.

 From directory "audio-peeler-server" in your terminal: 
- python3 -m venv venv
- . venv/bin/activate
- pip install flask
- pip3 install demucs

## Running

To run the program, first set your flask app's path using this command in terminal:
- export FLASK_APP=audioFileServer.py

Then we run it facing externally with this command:
- flask run --host=0.0.0.0

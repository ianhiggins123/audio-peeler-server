# audio-peeler-server

## Installation

Due to file size, dependencies cannot be stored in this repository.  Make sure to recreate these steps when installing server for first time.

From directory "audio-peeler-server" in your terminal: 
 - python3 -m venv venv
 - . venv/bin/activate
 - pip install flask
 - pip3 install demucs

## Running

When running the server, make sure you are in the venv environment.  You can usually tell from the "(venv)" that appears at the front of your command line.  If you aren't, run this command from the "audio-peeler-server" directory:

 - . venv/bin/activate


To run the program, first set your flask app's path using this command in terminal:
 - export FLASK_APP=audioFileServer.py

Then we run it facing externally with this command:
 - flask run --host=0.0.0.0

## Dependencies

### 3rd Party Web Content

#### Youtube-dl

 - https://github.com/ytdl-org/youtube-dl

#### Soundcloud-dl
 - https://github.com/Suyash458/soundcloud-dl

#### youtube_search
 - https://github.com/joetats/youtube_search

#### Savify (spotify library)

 - https://github.com/LaurenceRawlings/savify
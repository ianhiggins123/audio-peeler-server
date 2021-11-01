from app import app as application
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/audio-peeler-server.com/audio-peeler-server/')
sys.path.append('/var/www/audio-peeler-server.com/audio-peeler-server/app/')
sys.path.append('/var/www/audio-peeler-server.com/audio-peeler-server/audioFileServer.py')
sys.path.append('/var/www/audio-peeler-server.com/audio-peeler-server/venv/lib/python3.9/site-packages/')

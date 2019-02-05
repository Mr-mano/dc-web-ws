from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask import render_template
import time
import threading
from imapclient import IMAPClient
import RPi.GPIO as GPIO

app = Flask(__name__)
socketio = SocketIO(app)

DEBUG = True
 
HOSTNAME = 'imap.gmail.com'
USERNAME = ''
PASSWORD = ''
MAILBOX = 'Inbox'
 
NEWMAIL_OFFSET = 0   # my unread messages never goes to zero, yours might
MAIL_CHECK_FREQ = 10 # check mail every 60 seconds
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GREEN_LED = 18
RED_LED = 24
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
 
def loop():
    server = IMAPClient(HOSTNAME, use_uid=True, ssl=True)
    server.login(USERNAME, PASSWORD)
 
    if DEBUG:
        socketio.emit('alert', 'Logging in as ' + USERNAME, Broadcast=True)
        select_info = server.select_folder(MAILBOX)
        socketio.emit('alert','%d messages in INBOX' % select_info[b'EXISTS'], Broadcast=True)
 
    folder_status = server.folder_status(MAILBOX, 'UNSEEN')
    newmails = int(folder_status[b'UNSEEN'])
 
    if DEBUG:
        socketio.emit('alert','You have'+ str(newmails)+ 'new emails!', Broadcast=True)
 
    if newmails > NEWMAIL_OFFSET:
        GPIO.output(GREEN_LED, True)
        GPIO.output(RED_LED, False)
    else:
        GPIO.output(GREEN_LED, False)
        GPIO.output(RED_LED, True)
 
    time.sleep(MAIL_CHECK_FREQ)


@app.route("/")
def index():
    return render_template('index.html')


def message_loop():
    while True:
        loop()

# Vue que notre méthode pour lire nos message est une boucle infinie
# Elle bloquerait notre serveur. Qui ne pourrait répondre à aucune requête.
# Ici nous créons un Thread qui va permettre à notre fonction de se lancer 
# en parallèle du serveur.

read_loop = threading.Thread(target=message_loop)
read_loop.start()

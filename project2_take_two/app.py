import os

from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_socketio import SocketIO, emit
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or 'this-is-the-secret-key'
socketio = SocketIO(app)
session.clear()

channels = { 'test channel': [{'text': 'message 2', 'display_name': 'Neal', 'timestamp': datetime.datetime(2020, 4, 19, 16, 10, 10, 181420).isoformat()},
                              {'text': 'message 1', 'display_name': 'Nathan', 'timestamp': datetime.datetime(2020, 4, 19, 12, 29, 46, 181420).isoformat()}] }

@app.route("/", methods=['GET','POST'])
def index():
    return render_template('index.html', title='Home', channels=channels)
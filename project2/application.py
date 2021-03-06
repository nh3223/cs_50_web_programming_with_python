import os

from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_socketio import SocketIO, emit
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or 'this-is-the-secret-key'
socketio = SocketIO(app)

channels = { 'test channel': [{'text': 'message 2', 'display_name': 'Neal', 'timestamp': datetime.datetime(2020, 4, 19, 16, 10, 10, 181420).isoformat()},
                              {'text': 'message 1', 'display_name': 'Nathan', 'timestamp': datetime.datetime(2020, 4, 19, 12, 29, 46, 181420).isoformat()}] }

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', title='Home', channels=channels)

@app.route('/create_channel', methods=['POST'])
def create_channel():
    new_channel_name=request.form.get('new_channel_name')
    if new_channel_name:
        channels[new_channel_name] = []
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

 

@socketio.on("submit message")
def message(data):
    channel_name = data['channel_name']
    message_data = { 'text': data['message_text'],
                     'display_name': data['user_name'],
                     'timestamp': datetime.datetime.now().isoformat() }
    channels[channel_name].append(message_data)
    emit("new message", message_data, broadcast=True)


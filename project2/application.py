import os

from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_socketio import SocketIO, emit
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or 'this-is-the-secret-key'
socketio = SocketIO(app)

channels = { 'test channel': [{'text': 'message 2', 'display_name': 'Neal', 'timestamp': datetime.datetime(2020, 4, 19, 16, 10, 10, 181420)},
                              {'text': 'message 1', 'display_name': 'Nathan', 'timestamp': datetime.datetime(2020, 4, 19, 12, 29, 46, 181420)}] }

class New_Channel_Form(FlaskForm):
    channel = StringField('Channel Name', validators=[DataRequired()])
    submit = SubmitField('Create New Channel')

@app.route("/", methods=['GET','POST'])
def index():
    form = New_Channel_Form()
    if form.validate_on_submit():
        new_channel = form.channel.data
        if new_channel in channels:
            flash('Channel already exists')
            return redirect(url_for('index'))
        else:
            channels[new_channel] = []
            return render_template('channel.html', channel_name=new_channel, messages=channels[new_channel])
    return render_template('index.html', title='Home', form=form, channels=channels)

@app.route("/channel/<channel_name>")
def channel(channel_name):
    channel_data = { 'channel_name': channel_name, 'messages': channels[channel_name]}
    return render_template('channel.html', title=channel_name, channel_data=channel_data)

@socketio.on("submit message")
def vote(data):
    channel_name = data['channel_name']
    message_data = { 'text': data['message_text'],
                     'display_name': data['user_name'],
                     'timestamp': datetime.datetime.now() }
    channels[channel_name].append(message_data)
    print(channels)
    emit("announce vote", message_data, broadcast=True)
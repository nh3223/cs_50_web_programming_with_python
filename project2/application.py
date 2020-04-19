import os

from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or 'this-is-the-secret-key'
socketio = SocketIO(app)

channels = { 'test channel': ['message 1', 'message 2'] }

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
    messages = channels[channel_name]
    return render_template('channel.html', title=channel_name, channel_name=channel_name, messages=messages)

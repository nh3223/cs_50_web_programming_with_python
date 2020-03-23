from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Neal'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Seattle!'
        },
        {
            'author': {'username': 'Alice'},
            'body': 'The Princess Bride is my favorite movie!'
        }
    ]
    return render_template('index.html', title = 'Home Page', user=user, posts=posts)


from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import Login_Form, Registration_Form, Search_Form, Review_Form
from app.models import User, Book, Review
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route("/", methods=['GET','POST'])
@app.route("/index", methods=['GET','POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user/<current_user>'))
    form = Login_Form
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user)
        return redirect(url_for('user/<user>'))
    return render_template("index.html", title="Home", form=form)

@app.route("/search")
def search():
    form = Search_Form
    if form.validate_on_submit():
        isbn = Book.query.filter_by(isbn=form.isbn.data).first()
        title = Book.query.filter_by(title=form.title.data)
        author = Book.query.filter_by(author=author.title.data)
        if isbn is None and title is None and author is None:
            flash('Please enter a search request.')
            return redirect(url_for('search'))
        
    return render_template("search.html", title="Search Books" form=form)

@app.route("/book/<book>", )
def book():
    return render_template("book.html")

@app.route("/login", methods=['GET','POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        return redirect(url_for("search"))
    return render_template("login.html", title="Log In", form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    reviews = user.reviews.paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=reviews.next_num) if reviews.has_next else None
    prev_url = url_for('user', username=user.username, page=reviews.prev_num) if reviews.has_prev else None
    return render_template('user.html', user=user, reviews=reviews.items,
                            next_url=next_url, prev_url=prev_url)

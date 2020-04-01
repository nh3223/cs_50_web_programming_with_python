from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import Login_Form, Registration_Form, Search_Form, Review_Form
from app.models import User, Book, Review
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route("/", methods=['GET','POST'])
@app.route("/index", methods=['GET','POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    reviews = current_user.reviews.paginate(page, app.config['REVIEWS_PER_PAGE'], False)
    next_url = url_for('index', page=reviews.next_num) if reviews.has_next else None
    prev_url = url_for('index', page=reviews.prev_num) if reviews.has_prev else None
    return render_template('index.html', title = 'Home', reviews=reviews.items, next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Login_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Registration_Form()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

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
        
    return render_template("search.html", title="Search Books", form=form)

@app.route("/book/<isbn>", methods=['GET','POST'])
def book(isbn):
    print(isbn)
    book=Book.query.filter_by(isbn=isbn).first_or_404()
    #form = Review_Form()
    #if form.validate_on_submit():
    #    flash('Thank you for your review!')
    #    review = Review(rating=form.rating.data, review=form.review.data, user_id=current_user.id, book_id=book.id)
    #    return redirect(url_for('book', isbn=book.isbn))
    page = request.args.get('page', 1, type=int)
    #reviews = book.reviews.paginate(page, app.config['REVIEWS_PER_PAGE'], False)
    #next_url = url_for('book', isbn=book.isbn, page=reviews.next_num) if reviews.has_next else None
    #prev_url = url_for('book', isbn=book.isbn, page=reviews.prev_num) if reviews.has_prev else None
    return render_template("book.html", book=book)#, form=form, reviews=reviews.items, next_url=next_url, prev_url=prev_url
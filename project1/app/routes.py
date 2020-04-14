from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import Login_Form, Registration_Form, Search_Form, Review_Form
from app.models import User, Book, Review
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import requests

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

@app.route("/search", methods=['GET','POST'])
@login_required
def search():
    form = Search_Form()
    if form.validate_on_submit():
        books = Book.query.filter(getattr(Book, form.search_type.data).contains(form.search_term.data)).all()
        return render_template("search.html", title="Search Results", books=books, form=form)
    return render_template("search.html", title="Search Books", form=form)

@app.route("/book/<isbn>", methods=['GET','POST'])
def book(isbn):
    GOODREADS_KEY='mnxb1MhpDSrxdVn6QSDbg'
    book=Book.query.filter_by(isbn=isbn).first_or_404()
    goodreads_data = requests.get('https://www.goodreads.com/book/review_counts.json', 
                                   params={'key': GOODREADS_KEY, 'isbns': isbn})
    goodreads_data = goodreads_data.json()
    goodreads = {'number_of_ratings': goodreads_data['books'][0]['work_ratings_count'],
                 'average_rating': goodreads_data['books'][0]['average_rating']}
    form = Review_Form()
    if form.validate_on_submit():
        flash('Thank you for your review!')
        review = Review(rating=int(form.rating.data), review=form.review.data, user_id=current_user.id, book_id=book.id)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('book', isbn=book.isbn))
    page = request.args.get('page', 1, type=int)
    reviews = book.reviews.paginate(page, app.config['REVIEWS_PER_PAGE'], False)
    print(reviews.items[0].rating)
    next_url = url_for('book', isbn=book.isbn, page=reviews.next_num) if reviews.has_next else None
    prev_url = url_for('book', isbn=book.isbn, page=reviews.prev_num) if reviews.has_prev else None
    return render_template("book.html", goodreads=goodreads, book=book, form=form, reviews=reviews.items, next_url=next_url, prev_url=prev_url)
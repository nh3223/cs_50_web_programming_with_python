from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Book(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    isbn    = db.Column(db.String, nullable=False)
    title   = db.Column(db.String, nullable=False)
    author  = db.Column(db.String, nullable=False)
    year    = db.Column(db.Integer, nullable=False)
    reviews = db.relationship("Review", backref="book", lazy=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.column(db.String(128))
    reviews = db.relationship("Review", backref="user", lazy="dynamic")
    
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Review(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    rating  = db.Column(db.Integer)
    review  = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
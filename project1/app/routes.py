from flask import render_template
from app import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/book")
def book():
    return render_template("book.html")
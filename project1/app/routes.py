from flask import render_template
from app import app
from app.forms import Login_Form

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/book")
def book():
    return render_template("book.html")

@app.route("/login", methods=['GET','POST'])
def login():
    form = Login_Form()
    if form.validate_on_submit():
        return redirect(url_for("search"))
    return render_template("login.html", title="Log In", form=form)
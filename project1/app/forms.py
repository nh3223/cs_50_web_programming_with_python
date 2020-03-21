from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class Login_Form(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign In')

class Logout_Form(FlaskForm):
    submit = SubmitField('Log Out')

class Registration_Form(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Register')

class Search_Form(FlaskForm):
    isbn = StringField('ISBN Number')
    author = StringField('Author')
    title = StringField('Title')
    submit = SubmitField('Search')

class Review_Form(FlaskForm):
    rating = IntegerField('Rating')
    review = StringField('Review')
    submit = SubmitField('Save Review')



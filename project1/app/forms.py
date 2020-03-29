from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, RadioField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import User

class Login_Form(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign In')

class Registration_Form(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    password2   = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class Search_Form(FlaskForm):
    isbn = StringField('ISBN Number')
    author = StringField('Author')
    title = StringField('Title')
    submit = SubmitField('Search')

class Review_Form(FlaskForm):
    rating = RadioField('Rating', choices=[1,2,3,4,5])
    review = TextAreaField('Review', Length(min=1, max=1400))
    submit = SubmitField('Save Review')



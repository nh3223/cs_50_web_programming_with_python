from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, RadioField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import User, Book, Review

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
    search_term = StringField('ISBN/Author/Title', validators = [DataRequired()])
    search_type = SelectField(u'Search Type', choices=[('isbn','ISBN'),('author','Author'),('book_title','Title')], 
                                validators = [DataRequired()])
    submit = SubmitField('Search')

class Review_Form(FlaskForm):
    rating = RadioField('My Rating', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[DataRequired()])
    review = TextAreaField('My Review', validators=[DataRequired(),Length(min=1, max=1400)])
    submit = SubmitField('Save Review')



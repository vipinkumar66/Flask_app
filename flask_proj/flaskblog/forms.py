from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed #this one here we are using for the profile picture updation
from .models import User
from flask_login import current_user
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50, min=2)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

    #THese are the custom validators which will be checking that whether the email and the username given by the user already exists in our system or not.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already taken!! Try another username.")
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email is already taken! Try with another email.")
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField('Login')

class AccountUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50, min=2)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) #remember this file allowed part in this we are not giving nay equal sign here we are directly passing the allowed file types as an arguments to it
    submit = SubmitField('Update Profile')

    #THese are the custom validators which will be checking that whether the email and the username given by the user already exists in our system or not.
    def validate_username(self, username):
        if username.data != current_user.username: #this will avoid the error if the user submits the form without doing any chnages
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is already taken!! Try another username.")
    
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email is already taken! Try with another email.")
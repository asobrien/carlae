from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, \
        SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.

class RegisterForm(Form):
    name        = TextField('Username', validators = [DataRequired(), Length(min=6, max=25)])
    email       = TextField('Email', validators = [DataRequired(), Length(min=6, max=40)])
    password    = PasswordField('Password', validators = [DataRequired(), Length(min=6, max=40)])
    confirm     = PasswordField('Repeat Password', [DataRequired(), EqualTo('password', message='Passwords must match')])

class LoginForm(Form):
    name        = TextField('Username', [DataRequired()])
    password    = PasswordField('Password', [DataRequired()])
    remember    = BooleanField('Remember Me', default=True)

class ForgotForm(Form):
    email       = TextField('Email', validators = [DataRequired(), Length(min=6, max=40)])

class AddUserForm(Form):
    name        = TextField('Username', validators = [DataRequired(), Length(min=6, max=25)])
    email       = TextField('Email', validators = [DataRequired(), Length(min=6, max=40)])

class UrlForm(Form):
    url = TextField('http://', validators = [DataRequired(), Length(min=3, max=1500)])

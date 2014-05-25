from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, \
        SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, Required
import random
import string

from models import InviteUser

# Set your classes here.

class RegisterForm(Form):
    name        = TextField('Username', validators = [DataRequired(), Length(min=2, max=25)])
    email       = TextField('Email', validators = [DataRequired(), Length(min=6, max=40)])

class LoginForm(Form):
    email        = TextField('Email', [DataRequired()])
    password    = PasswordField('Password', [DataRequired()])
    remember    = BooleanField('Remember Me', default=True)

class ForgotForm(Form):
    email       = TextField('Email', validators = [DataRequired(), Length(min=6, max=40)])

class AddUserForm(Form):
    name        = TextField('Username', validators = [DataRequired(), Length(min=6, max=25)])
    email       = TextField('Email', validators = [DataRequired(), Length(min=6, max=40)])

class InviteUserForm(Form):
    email        = TextField('Email', validators = [DataRequired(), Length(min=6, max=40)])

class UrlForm(Form):
    url = TextField('http://', validators = [DataRequired(), Length(min=3, max=1500)])

class ActivateUserForm(Form):
    password    = PasswordField('Password', [Required(),
                                             Length(min=6, max=-1, message="Passwords must be at least 6 characters."),
                                             EqualTo('confirm', message='Passwords must match.')])
    confirm     = PasswordField('Confirm Password', [Required(), Length(min=6, max=-1)])


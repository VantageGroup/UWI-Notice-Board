import os
from flask import Flask, render_template

from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SubmitField,
    PasswordField
)

from wtforms.validators import (
    InputRequired,
    EqualTo, 
    Email
)

app = Flask(__name__)

class SignUp(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    faculty = StringField('Faculty', validators=[InputRequired()])
    dept = StringField('Department', validators=[InputRequired()])
    submit = SubmitField('Sign Up', render_kw={'class': 'btn waves-effect waves-light white-text'})
import os
from flask import Flask, render_template

from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SubmitField,
    PasswordField
)

from wtforms.validators import (
    InputRequired
)

app = Flask(__name__)

class LogIn(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light white-text'})
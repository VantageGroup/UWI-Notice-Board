import os
from flask import Flask, render_template

from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditorField

from flask_wtf import FlaskForm
from flask_uploads import (
    UploadSet, 
    IMAGES, 
    configure_uploads
)
from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)
from flask_wtf.file import (
    FileField, 
    FileRequired, 
    FileAllowed
)
from wtforms.validators import (
    InputRequired,
    EqualTo, 
    Email,
    DataRequired,
    Length
)


app = Flask(__name__)
# app.config['UPLOADED_PHOTOS_DEST'] = app.instance_path

# photos = UploadSet('photos', IMAGES)
# configure_uploads(app, photos)


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[Email(), InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Login')


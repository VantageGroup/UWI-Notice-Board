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
    SubmitField,
    TextAreaField,
    IntegerField,
    BooleanField,
    SelectField,
    RadioField
)
from flask_wtf.file import (
    FileField, 
    FileRequired, 
    FileAllowed
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length
)


app = Flask(__name__)
# app.config['UPLOADED_PHOTOS_DEST'] = app.instance_path

# photos = UploadSet('photos', IMAGES)
# configure_uploads(app, photos)


class SignUpForm(FlaskForm):
    
    submit= SubmitField("Submit")


class LoginForm(FlaskForm):
    
    submit= SubmitField("Submit")
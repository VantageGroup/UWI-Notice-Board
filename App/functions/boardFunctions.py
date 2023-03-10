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


class BoardForm(FlaskForm):
    title = StringField( "Title", validators =[DataRequired()] )
    faculty = SelectField(
        'Select Faculty', 
        choices = [
            ('FST', 'Science and Technology'),
            ('FMS', 'Medical Sciences'),
            ('FSS', 'Social Sciences'),
            ('ENG', 'Engineering'),
            ('LAW', 'Law'),
            ('FHE', 'Humanities and Education'),
            ('FFA', 'Food and Agriculture'),
            ('SPORT', 'Sport')
        ]
    )
    # dept = StringField( "Title", validators =[DataRequired()] )
    # photo = FileField(validators=[
    #     FileAllowed(photos, 'Only images are allowed')
    # ]
    # )
    submit= SubmitField("Submit")
 
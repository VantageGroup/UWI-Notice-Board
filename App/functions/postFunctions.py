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
    RadioField,
    DateField,
    DateTimeLocalField
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

from datetime import datetime, date


app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = app.instance_path

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class PostForm(FlaskForm):
    title = StringField( "Title", validators =[DataRequired()] )
    message = CKEditorField( "Message" )
    photo = FileField(validators=[
        FileAllowed(photos, 'Only images are allowed')
    ])
    startDate = DateField('Event Start Date', format= '%Y-%m-%d')
    endDate = DateField('Event End Date', format= '%Y-%m-%d')
    submit = SubmitField("Submit")
    schedulePostDate = DateTimeLocalField('When would you like this post to be published?', format= '%Y-%m-%dT%H:%M', validators =[DataRequired()])
    scheduledDeleteDate = DateTimeLocalField('When would you like this post to be removed?', format= '%Y-%m-%dT%H:%M')


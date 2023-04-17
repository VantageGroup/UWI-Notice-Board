import os
from flask import Flask

from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from flask_uploads import (
    UploadSet, 
    IMAGES, 
    configure_uploads
)
from wtforms import (
    StringField,
    SubmitField,
    DateField,
    DateTimeLocalField
)
from flask_wtf.file import (
    FileField, 
    FileAllowed
)
from wtforms.validators import (
    InputRequired,
    Length
)

from models import (
    Post,
    Event
)

from datetime import datetime, date


app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = app.instance_path

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class PostForm(FlaskForm):
    title = StringField( "Title", 
        validators = [
            InputRequired(), 
            Length(min=1, max=24, message="Name must be a between of %(min)d and %(max)d characters in length")
        ] 
    )
    message = CKEditorField( "Message" )
    photo = FileField(validators=[
        FileAllowed(photos, 'Only images are allowed')
    ])
    startDate = DateField('Event Start Date', format= '%Y-%m-%d')
    endDate = DateField('Event End Date', format= '%Y-%m-%d')
    submit = SubmitField("Submit")
    schedulePostDate = DateTimeLocalField('When would you like this post to be published?', format= '%Y-%m-%dT%H:%M')
    scheduledDeleteDate = DateTimeLocalField('When would you like this post to be removed?', format= '%Y-%m-%dT%H:%M')


# Retrieve all Posts from the Database
def RetrieveAllPosts():
  list = Post.query.order_by(Post.id.desc()).all()
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieve all Events from the Database
def RetrieveAllEvents():
  list = Event.query.all()
  list = [entry.toDict() for entry in list]
  
  return list
import os
from flask import Flask

from flask_wtf import FlaskForm
from flask_uploads import (
    UploadSet, 
    IMAGES, 
    configure_uploads
)
from wtforms import (
    StringField,
    SubmitField
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
    Board,
    Faculty,
    FacultyDept
)


app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = app.instance_path

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class BoardForm(FlaskForm):
    title = StringField( "Title", 
        validators = [
            InputRequired(), 
            Length(min=3, max=16, message="Name must be a between of %(min)d and %(max)d characters in length")
        ] 
    )
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed')
        ]
    )
    submit= SubmitField("Submit")


# Retrieve all Boards from the Database
def RetrieveAllBoards():
  list = Board.query.all()
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieve all Facuties from the Database
def RetrieveFacultyList():
  list = Faculty.query.all()
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieve all Departments from the Database
def RetrieveDepartmentList():
  list = FacultyDept.query.all()
  list = [entry.toDict() for entry in list]
  
  return list
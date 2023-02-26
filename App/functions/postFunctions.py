from flask import Flask, render_template

from flask_uploads import (
    UploadSet, 
    IMAGES, 
    configure_uploads
)
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    IntegerField,
    BooleanField,
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
app.config['UPLOADED_PHOTOS_DEST'] = '/App/user/images'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class PostForm(FlaskForm):
    title= StringField("Title of post", validators =[DataRequired()] )
    message = StringField("Post content", validators =[DataRequired()] )
    photo = FileField(validators=[
        FileAllowed(photos, 'Only images are allowed')
    ]
    )
    submit= SubmitField("Submit")


class SearchForm(FlaskForm):
    search = StringField("searchCriteria")
    submit = SubmitField("Submit")

#Creating a form class
 
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    IntegerField,
    BooleanField,
    RadioField
)

from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length
)

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"

class PostForm(FlaskForm):
    title= StringField("Title of post", validators =[DataRequired()] )
    message = StringField("Post content", validators =[DataRequired()] )
    submit= SubmitField("Submit")


class SearchForm(FlaskForm):
    search = StringField("searchCriteria")
    submit = SubmitField("Submit")

#Creating a form class
 
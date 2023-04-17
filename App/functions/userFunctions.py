import os
from flask import Flask

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)
from wtforms.validators import (
    InputRequired,
    EqualTo, 
    Email
)
from flask_login import (
  current_user
)

from models import (
    Profile,
    Follow,
    Subscriber
)
from functions.postFunctions import (
    RetrieveAllEvents,
    RetrieveAllPosts
)


app = Flask(__name__)


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


# Retrieves all User Profiles from the Database
def RetreveProfiles():
  list = Profile.query.all()
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieve User Subscribed Boards
def RetrieveUserBoards():
  list = Subscriber.query.filter_by(user=current_user.id)
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieve User Post Feed
def RetrieveFeedSub():
  all_posts = RetrieveAllPosts() 
  boards = RetrieveUserBoards()
  
  posts = []

  for board in boards:
    for post in all_posts:
      if (post['bID'] == board['board']):
        posts.append(post)
  
  return posts

#  Retrieve User Followed Posts
def RetrieveUserFollowed():
  list = Follow.query.filter_by(user=current_user.id)
  list = [entry.toDict() for entry in list]
  
  return list
  
# Retrieve User Followed Events
def RetrieveFollowedEvents():
  all_events = RetrieveAllEvents() 
  follow = RetrieveUserFollowed()
  
  events = []

  for post in follow:
    for event in all_events:
      if (event['post'] == post['post']):
        events.append(event)
  
  return events
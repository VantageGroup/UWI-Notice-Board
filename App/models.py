from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_migrate import Migrate

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length
)
from werkzeug.security import (
    generate_password_hash, 
    check_password_hash
)
from flask_login import UserMixin

from datetime import datetime, date

import os
import click
import csv


db = SQLAlchemy()

def get_migrate(app):
  return Migrate(app, db)

def create_db(app):
  db.init_app(app)
  with app.app_context():
    db.create_all()
  
def init_db(app):
  db.init_app(app)
  
def reCreate_db():
  db.create_all()
    
    
'''#'''
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  bID = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
  owner = db.Column(db.Integer, db.ForeignKey('user.id'))
  ownerName = db.Column(db.String(64), nullable=False)
  title = db.Column(db.String(64), nullable=False)
  message = db.Column(db.String(2048), nullable=False)
  faculty = db.Column(db.String(8), nullable=False)
  dept = db.Column(db.String(8), nullable=True)
  dateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  
  image = db.Column(db.Boolean)
  imageLocation = db.Column(db.String(256), nullable=True)
  
  event = db.Column(db.Boolean)
  startDate = db.Column(db.Date,  default=date.today, index=True)
  endDate = db.Column(db.Date,  default=date.today, index=True)
  schedulePostDate = db.Column(db.DateTime,  default=datetime.utcnow, index=True)
  scheduledDeleteDate = db.Column(db.DateTime,  default=datetime.utcnow, index=True, nullable=True)
  
  viewCount = db.Column(db.Integer, nullable=True, default = 0)
  
  def toDict(self):
    return{
      "id": self.id,
      "bID": self.bID,
      "owner": self.owner,
      "ownerName":self.ownerName,
      "title": self.title,
      "message": self.message,
      "faculty": self.faculty,
      "dept": self.dept,
      "image": self.image,
      "imageLocation": self.imageLocation,
      "dateCreated": self.dateCreated,
      "startDate" : self.startDate,
      "endDate" : self.endDate,
      "schedulePostDate" : self.schedulePostDate,
      "scheduledDeleteDate" : self.scheduledDeleteDate,
      "viewCount": self.viewCount
    }

'''#'''
class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
  title = db.Column(db.String(64), nullable=False)
  startDate = db.Column(db.Date,  default=date.today, index=True)
  endDate = db.Column(db.Date,  default=date.today, index=True)
  url = db.Column(db.String, nullable=False)
  
  def toDict(self):
    return{
      "id": self.id,
      "post": self.post,
      "title":self.title,
      "startDate" : self.startDate,
      "endDate" : self.endDate,
      "url":self.url
    }

'''#'''
class Follow(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
  user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  
  def toDict(self):
    return{
      "id": self.id,
      "post": self.post,
      "user": self.user
    }


'''#'''
class Board(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(64), nullable=False)
  faculty = db.Column(db.String(8), nullable=False)
  dept = db.Column(db.String(8), nullable=True)
  image = db.Column(db.Boolean)
  imageLocation = db.Column(db.String(256), nullable=True)
  subscribers = db.Column(db.Integer, nullable=True, default = 1)
  
  def toDict(self):
    return{
      "id": self.id,
      "title": self.title,
      "faculty": self.faculty,
      "dept": self.dept,
      "image": self.image,
      "imageLocation": self.imageLocation,
      "subscribers": self.subscribers
    }
   
'''#'''
class Subscriber(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  board = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
  user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  isAdmin = db.Column(db.Boolean)
  isSubscribed = db.Column(db.Boolean)
  
  def toDict(self):
    return{
      "id": self.id,
      "board": self.board,
      "user": self.user,
      "isAdmin": self.isAdmin,
      "isSubscribed" : self.isSubscribed
    }
  

  def delete(self):
        db.session.delete(self)
        db.session.commit()


'''#'''
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=True, nullable=False)
  email = db.Column(db.String, nullable=False)
  password = db.Column(db.String, nullable=False)
  isAdmin = db.Column(db.Boolean, nullable=True)
  
  def toDict(self):
    return{
      "id": self.id,
      "username": self.username,
      "password": self.password,
      "email": self.email,
      "isAdmin" : self.isAdmin
    }
  
  #hashes the password parameter and stores it in the object
  def set_password(self, password):
    """Create hashed password."""
    self.password = generate_password_hash(password, method='sha256')
  
  #Returns true if the parameter is equal to the object's password property
  def check_password(self, password):
    """Check hashed password."""
    return check_password_hash(self.password, password)
  
  #To String method
  def __repr__(self):
    return '<User {}>'.format(self.username)

'''#'''
class Profile(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  username = db.Column(db.String(64), unique=True, nullable=False)
  image = db.Column(db.Boolean, nullable = False)
  imageLocation = db.Column(db.String(256), nullable=True)
  
  def toDict(self):
    return{
      "id": self.id,
      "user": self.user,
      "username": self.username,
      "image": self.image,
      "imageLocation": self.imageLocation
    }
  

'''#'''
class Faculty(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(64), nullable=False, unique=True)
  label = db.Column(db.String(8), nullable=False, unique=True)
  
  def toDict(self):
    return{
      "id": self.id,
      "title": self.title,
      "label": self.label
    }
  
  def initialize():
    facList = FacultyDept.facultyList()
    
    for val in facList:
      if (
        Faculty.query.filter(Faculty.label == val.label).first() == None
      ):
        db.session.add(val)
        db.session.commit()
    
    print("Faculty Database initialised")
    return

'''#'''
class FacultyDept(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  faculty = db.Column(db.String(64), nullable=False)
  fLabel = db.Column(db.String(8), nullable=False)
  department = db.Column(db.String(64), nullable=True)
  dLabel = db.Column(db.String(8), nullable=True)
  
  def toDict(self):
    return{
      "id": self.id,
      "faculty": self.faculty,
      "fLabel": self.fLabel,
      "department": self.department,
      "dLabel": self.dLabel
    }
  
  def initialize():
    with open('fac-dept.csv') as csvFile:
      csvData = csv.DictReader(csvFile, delimiter=',')
      
      facDept = []
      for row in csvData:
        fD = FacultyDept(
          faculty = row['Faculty'],
          fLabel = row['Flabel'],
          department  = row['Department'],
          dLabel = row['Dlabel']
        )
        
        if (
          FacultyDept.query.filter(
            FacultyDept.department == fD.department and 
            FacultyDept.dLabel == fD.dLabel).first()
        ):
          if (
            FacultyDept.query.filter(
              FacultyDept.fLabel == fD.fLabel).first() == None
          ):
            db.session.add(fD)
            db.session.commit()
        else:
          db.session.add(fD)
          db.session.commit()
        
      print('Faculty-Department Database inialized')
      return
  
  def facultyList():
    facList = []
    
    for val in db.session.query(FacultyDept.fLabel).distinct():
      fac = Faculty(
        title=FacultyDept.query.filter_by(fLabel = val.fLabel).first().faculty,
        label=val.fLabel
      )
      
      facList.append(fac)
  
    return facList

    
'''#'''
class SearchForm(FlaskForm):
    search = StringField("searchCriteria", validators =[DataRequired()])
    submit = SubmitField("Submit")
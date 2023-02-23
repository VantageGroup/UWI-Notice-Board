from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_migrate import Migrate

db = SQLAlchemy()

def get_migrate(app):
  return Migrate(app, db)

def create_db(app):
  db.init_app(app)
  with app.app_context():
    db.create_all()
  
def init_db(app):
  db.init_app(app)
  
class Test(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  text = db.Column(db.String(50))
  
  def toDict(self):
    return{
      "id": self.id,
      "text": self.text
    }
    
    

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  # board = db.Column(db.Integer, db.ForeignKey('board.id'))
  # owner = db.Column(db.String(64), db.ForeignKey('user.id'))
  title = db.Column(db.String(64), nullable=False)
  message = db.Column(db.String(2048), nullable=False)
  # viewerCount = db.Column(db.Integer, nullable=True)
  # image = db.Column()
  # imageLocation = db.Column()
  # dateCreated = db.Column()
  
  def toDict(self):
    return{
      "id": self.id,
      # "board": self.baord,
      # "owner": self.owner,
      "title": self.title,
      "message": self.message 
      # "viewerCount": self.viewerCount
      # "image": self.image
      # "imageLocation": self.imageLocation
      # "dateCreated": self.dateCreate
      
    }
    

class Board(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(64), nullable=False)
  
  def toDict(self):
    return{
      "id": self.id,
      "title": self.title
    }
    

class User(db.Model):
  username = db.Column(db.String(64), primary_key=True, nullable=False)
  email = db.Column(db.String(64), nullable=False)
  password = db.Column(db.String(64), nullable=False)
  
  def toDict(self):
    return{
      "username": self.username,
      "password": self.password
    }
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func 
#from werkzeug.security import generate_password_hash
from flask_migrate import Migrate
# from app import app

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
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64), nullable=False)
  message = db.Column(db.String(2048), nullable=False)

  # post_date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# def __init__(self, id, title, message):
#   self.id = id
#   self.title = title
#   self.message = message

# def __repr__(self):
#     return f'<Post {self.id} - {self.title} - {self.message}>'


# def toDict(self):
#  return {
#     "id": self.id,
#     "title": self.title,
#     "message": self.message,
#     "post_date_time": self.post_date_time
#     }


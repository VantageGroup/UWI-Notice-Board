from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func 
#from werkzeug.security import generate_password_hash
from app import app
db = SQLAlchemy(app)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64), nullable=False)
  message = db.Column(db.String(2048), nullable=False)

  # post_date_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

def __init__(self, id, title, message):
  self.id = id
  self.title = title
  self.message = message

def __repr__(self):
    return f'<Post {self.id} - {self.title} - {self.message}>'


def toDict(self):
 return {
    "id": self.id,
    "title": self.title,
    "message": self.message,
    "post_date_time": self.post_date_time
    }


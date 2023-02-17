import click, sys
from models import db, Post
from app import app


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  Post1 = Post('1', 'Post1', 'Welcome')
  db.session.add(Post1)
  db.session.commit()
  print(Post1)
  print('database intialized')
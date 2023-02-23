import click
from flask import Flask
from models import create_db, db, app,Post, Test

@app.cli.command("init")
def initialize():
  create_db(app)
  

# @app.cli.command("init", help="Creates and initializes the database")
# def initialize():
db.drop_all()
db.init_app(app)
db.create_all()
#   Post1 = Post('Post1', 'Welcome to the UWI notice board')
#   Post2 = Post('Post2', 'Welcome to the UWI notice board')
#   Post3 = Post('Post3', 'Welcome to the UWI notice board')
#   db.session.add(Post1)
#   db.session.add(Post2)
#   db.session.add(Post3)
#   db.session.commit()
  
import click
from flask import Flask
from models import create_db, db, app,Post

@app.cli.command("init")
def initialize():
  create_db(app)
  
db.drop_all()
db.init_app(app)
db.create_all()





  
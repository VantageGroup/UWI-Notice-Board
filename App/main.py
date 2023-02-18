import os
import requests
from flask import Flask, redirect, render_template, request, jsonify, send_from_directory, flash, url_for
from flask_cors import CORS
from sqlalchemy.exc import OperationalError
from models import db, get_migrate, create_db
from models import Test, Post, Board, User

def create_app():
  app = Flask(__name__, static_url_path='/static')
  CORS(app)
  app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
  app.config['TEMPLATE_AUTO_RELOAD'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
  app.config['DEBUG'] = True
  app.config['SECRET_KEY'] = 'MySecretKey'
  app.config['PREFERRED_URL_SCHEME'] = 'https'
  create_db(app)
  app.app_context().push()
  return app
  
  
app = create_app()

migrate = get_migrate(app)


def TestPostData():
  post = Post(
    title="Test Post #1",
    message="This is the first test post"
  )
  return post

@app.route('/')
def home():
  test = TestPostData()
  
  return render_template('index.html', post=test)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=8080)
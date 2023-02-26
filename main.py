import os
# import requests
from flask import Flask, redirect, render_template, request, jsonify, send_from_directory, flash, url_for
from flask_cors import CORS
from sqlalchemy.exc import OperationalError
from models import db, get_migrate, create_db
from models import Test, Post, Board
from webforms import SearchForm, PostForm

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





@app.route('/')
def home():
  num_rows_deleted = db.session.query(Post).delete()
  num_rows_deleted_boards = db.session.query(Board).delete()
  db.session.commit()
  Post1 = Post()
  Board1 = Board()
  Post1 = Post( title='Post1', message='Welcome to the UWI notice board.')
  Post2 = Post(title='Post2', message='This is for the second post.')
  Post3 = Post(title='Post3', message='This is for the third post.')
  Board1 = Board( title='DCIT Board')
  Board2 = Board(title='Physics Board')
  Board3 = Board(title='Engineering Board')
  db.session.add(Post1)
  db.session.add(Post2)
  db.session.add(Post3)
  db.session.add(Board1)
  db.session.add(Board2)
  db.session.add(Board3)
  db.session.commit()
 
  dbPosts = Post.query
  queryAll = Post.query.all()
  return render_template('index.html',dbPosts = dbPosts)

@app.context_processor
def base():
  form = SearchForm()
  return dict(form=form) 


@app.route('/search',methods=["POST"])
def search():
  form = SearchForm()
  dbPosts = Post.query
  queryAll = Post.query.all()
  if 1 == 1:
   post_searched = form.searched.data
   dbPosts = dbPosts.filter(Post.message.like( '%' + post_searched + '%'))
   dbPosts = dbPosts.order_by(Post.title).all()
   return render_template('search.html', form=form, searched = post_searched, queryAll = queryAll, dbPosts = dbPosts)

#creating form page
@app.route('/createPost', methods=['GET', 'POST'])
def createPost():
  title = None
  message = None
  form = PostForm()
  if form.validate_on_submit():
    title = form.title.data
    form.title.data = ''
    message = form.message.data
    form.message.data = ''
  return render_template("form.html", title = title, message = message, form = form)

@app.route('/renderBoards',methods=['GET','POST'])
def renderBoards():
  dbBoards = Board.query
  queryAll = Board.query.all()
  if 1 == 1:
   return render_template('boards.html', dbBoards = dbBoards)



if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=8080)
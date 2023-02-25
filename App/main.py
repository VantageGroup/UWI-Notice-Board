import os
import requests
from flask import (
  Flask, 
  redirect, 
  render_template, 
  request, 
  jsonify, 
  send_from_directory, 
  flash, 
  url_for
)

from flask_cors import CORS
from sqlalchemy.exc import OperationalError
from models import (
  db, 
  get_migrate, 
  create_db
)

from models import (
  Post, 
  Board, 
  User
)

from functions.postFunctions import (
  SearchForm,
  PostForm
)
# from postFunctions import SearchForm

# from searchForm import ()


def create_app():
  app = Flask(__name__, static_url_path='/static')
  CORS(app)
  app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
  app.config['TEMPLATE_AUTO_RELOAD'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
  app.config['DEBUG'] = True
  app.config['SECRET_KEY'] = 'password'
  app.config['PREFERRED_URL_SCHEME'] = 'https'
  create_db(app)
  app.app_context().push()
  return app
  
  
app = create_app()

@app.context_processor
def base():
  form = SearchForm()
  return dict(form=form) 

migrate = get_migrate(app)


def RetrievePosts():
  posts = Post.query.all()
  posts = [entry.toDict() for entry in posts]
  
  return posts


# Landing Page
@app.route('/')
def home():
  feed = RetrievePosts()
  
  return render_template('index.html', 
      posts=feed)


#Search Posts
@app.route('/search', methods=["POST"])
def search():
  # form = SearchForm()
  
  postsDb = Post.query
  search = request.form.get('searchCriteria')
  
  print("Searched for " + request.form.get('searchCriteria'))
  
  foundMessage = postsDb.filter( db.or_ (
    (Post.message.like( '%' + search + '%' )), 
    (Post.title.like( '%' + search + '%' ))
    )
  )
  # foundTitle = postsDb.filter( Post.title.like( '%' + search + '%' ) )
  
  found = foundMessage
  # found = found.union(foundTitle)
  # [found.join(f) for f in foundTitle if f not in found]
  
  found = found.order_by(Post.title).all()
  
  return render_template('search.html', 
    # form = form, 
    searched = search, 
    dbPosts = found
  )


# Create a Post Route
@app.route('/create-post', methods=['GET'])
def createPost():
  form = PostForm()
    
  return render_template("form.html",
    form = form
  )

# Upload Post Route
@app.route('/create-post', methods=['GET', 'POST'])
def uploadPost():
  title = request.form.get("title")
  message = request.form.get("message")
  
  newPost = Post (
    title=title,
    message=message
  )
  print("New Post Title:" + newPost.title)
  print("New Post Message:" + newPost.message)
  
  db.session.add(newPost)
  db.session.commit()
    
  return redirect(url_for('home'))

# Temp Route to purge all Databases
@app.route('/purge', methods=['GET', 'POST'])
def delete():
  posts = Post.query
  boards = Board.query
  users = User.query
  
  for p in posts:
    print(p.id)
    db.session.delete(p)
    
  # db.session.delete(boards)
  # db.session.delete(users)
  db.session.commit()
  
  return redirect(url_for('home'))
  
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=8080)
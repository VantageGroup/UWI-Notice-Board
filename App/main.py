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
from flask_cors import (
  CORS
)
from flask_uploads import (
  UploadSet, 
  IMAGES, 
  configure_uploads
)

from sqlalchemy.exc import OperationalError
from werkzeug.utils import secure_filename

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


def create_app():
  app = Flask(__name__, static_url_path='/static')
  CORS(app)
  app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
  app.config['TEMPLATE_AUTO_RELOAD'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
  app.config['DEBUG'] = True
  app.config['PREFERRED_URL_SCHEME'] = 'https'
  
  os.makedirs(os.path.join(app.instance_path, 'post'), exist_ok=True)
  os.makedirs(os.path.join(app.instance_path, 'board'), exist_ok=True)
  os.makedirs(os.path.join(app.instance_path, 'user'), exist_ok=True)
  # os.makedirs(os.path.join(app.instance_path, 'post'), exist_ok=True)
  # os.makedirs(os.path.join(app.instance_path, 'board'), exist_ok=True)
  # os.makedirs(os.path.join(app.instance_path, 'user'), exist_ok=True)
  
  app.config['UPLOADED_PHOTOS_DEST'] = app.instance_path
  
  app.config['UPLOAD_FOLDER'] = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'post')
  app.config['BOARD_FOLDER'] = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'board')
  app.config['PROFILE_FOLDER'] = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'profile')
  
  app.config['SECRET_KEY'] = 'password'
  
  configure_uploads(app, UploadSet('photos', IMAGES))
  create_db(app)
  
  app.app_context().push()
  
  return app
  
  
app = create_app()

@app.context_processor
def base():
  form = SearchForm()
  return dict(form=form) 

migrate = get_migrate(app)


'''Functions'''

# Retrieve all Posts from the Database
def RetrievePosts():
  posts = Post.query.all()
  posts = [entry.toDict() for entry in posts]
  
  return posts


'''App Routes'''

# Landing Page
@app.route('/')
def home():
  feed = RetrievePosts()
  
  return render_template('index.html', 
      posts=feed)


#Search Posts
@app.route('/search', methods=["POST"])
def search():
  postsDb = Post.query
  search = request.form.get('searchCriteria')
  
  print("Searched for " + request.form.get('searchCriteria'))
  
  foundMessage = postsDb.filter( db.or_ (
    (Post.message.like( '%' + search + '%' )), 
    (Post.title.like( '%' + search + '%' ))
    )
  )
  
  found = foundMessage
  found = found.order_by(Post.title).all()
  
  return render_template('search.html',
    searched = search, 
    posts = found
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
  form = PostForm()
  
  if (form.validate_on_submit()):
    title = request.form.get("title")
    message = request.form.get("message")
    
    if (form.photo.data !=  None):
      image = True
      
      f = request.files['photo']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
      
      imageLocation = f.filename
      print(imageLocation)
    else:
      image = False
      imageLocation = ""
    
    newPost = Post (
      title=title,
      message=message,
      image=image,
      imageLocation=imageLocation
    )
    
    print("New Post Title:" + newPost.title)
    print("New Post Message:" + newPost.message)
    
    db.session.add(newPost)
    db.session.commit()
  
  return redirect(url_for('home'))

# Retrieve Uploaded Image
@app.route('/<filename>')
def get_file(filename): 
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Explore Boards Route
@app.route('/boards')
def boards():
  return render_template('boards.html')


'''Remove from Production'''

# Temp Route to purge all Databases
@app.route('/purge', methods=['GET', 'POST'])
def delete():
  posts = Post.query
  boards = Board.query
  users = User.query
  
  for p in posts:
    db.session.delete(p)
  
  for b in posts:
    db.session.delete(b)
    
  for u in posts:
    db.session.delete(u)
  
  
  db.session.commit()
  
  return redirect(url_for('home'))
  
# Drops all tables and recreates them
@app.route('/drop', methods=['GET', 'POST'])
def dropAll():
  db.drop_all()
  
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=8080)
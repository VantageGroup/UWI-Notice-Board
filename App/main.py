import json
import os
import requests

from sqlalchemy.exc import OperationalError
from werkzeug.utils import secure_filename

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
from flask_ckeditor import CKEditor

from sqlalchemy.exc import OperationalError, IntegrityError
from werkzeug.utils import secure_filename

from models import (
  db, 
  get_migrate, 
  create_db,
  reCreate_db
)
from models import (
  Post, 
  Board, 
  User,
  Faculty,
  FacultyDept,
  SearchForm
)

from functions.postFunctions import (
  PostForm
)
from functions.boardFunctions import (
  BoardForm
)

# FOR LOGIN
from functions.loginFunctions import (
  LogIn
)

from functions.signupFunctions import (
  SignUp
)

# FOR LOGIN 
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

''' Begin Flask Login Functions '''
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


''' End Flask Login Functions '''

def create_app():
  app = Flask(__name__, static_url_path='/static')
  CORS(app)
  app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
  app.config['TEMPLATE_AUTO_RELOAD'] = True
  app.config['DEBUG'] = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.config['PREFERRED_URL_SCHEME'] = 'https'
  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
  
  # FOR LOGIN
  login_manager.init_app(app)

  editor = CKEditor()
  editor.init_app(app)
  
  os.makedirs(os.path.join(app.instance_path, 'post'), exist_ok=True)
  os.makedirs(os.path.join(app.instance_path, 'board'), exist_ok=True)
  os.makedirs(os.path.join(app.instance_path, 'user'), exist_ok=True)
  
  app.config['UPLOADED_PHOTOS_DEST'] = app.instance_path
  
  app.config['UPLOAD_FOLDER'] = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'post')
  app.config['BOARD_FOLDER'] = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'board')
  app.config['PROFILE_FOLDER'] = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'user')
  
  app.config['SECRET_KEY'] = 'password'
  
  configure_uploads(app, UploadSet('photos', IMAGES))
  create_db(app)
  
  app.app_context().push()
  
  return app


app = create_app()

@app.context_processor
def base():
  searchPost = SearchForm()
  return dict(form=searchPost) 

migrate = get_migrate(app)

FacultyDept.initialize()
Faculty.initialize()


'''Functions'''

# Retrieve all Posts from the Database
def RetrieveAllPosts():
  posts = Post.query.all()
  posts = [entry.toDict() for entry in posts]
  
  return posts

#
def RetrieveAllBoards():
  boards = Board.query.all()
  boards = [entry.toDict() for entry in boards]
  
  return boards


'''App Routes'''

# Landing Page
@app.route('/')
def home():
  feed = RetrieveAllPosts()
  
  return render_template('index.html', 
      posts=feed)

# Retrieve Uploaded Image
@app.route('/<filename>')
def get_file(filename): 
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#Search Posts
@app.route('/search', methods=["POST"])
def search():
  postsDb = Post.query
  boardsDb = Board.query
  
  search = request.form.get('searchCriteria')
  
  print("Searched for " + request.form.get('searchCriteria'))
  
  found = postsDb.filter( db.or_ 
    (
    (Post.message.like( '%' + search + '%' )), 
    (Post.title.like( '%' + search + '%' ))
    )
  )
  foundPosts = found
  foundPosts = foundPosts.order_by(Post.title).all()
  
  
  found = boardsDb.filter(
    (
    (Board.title.like( '%' + search + '%' ))
    )
  )
  foundBoards = found
  foundBoards = foundBoards.order_by(Board.title).all()
  
  return render_template('search.html',
    searched = search, 
    boards = foundBoards,
    posts = foundPosts
  )


'''Post Related Routes'''

# Create a Post Route
@app.route('/board<boardID>=create-post', methods=['GET'])
def createPost(boardID):
  form = PostForm()
    
  return render_template("form.html",
    formPost = form
  )

# Upload Post Route
@app.route('/board<boardID>=create-post', methods=['GET', 'POST'])
def uploadPost(boardID):
  form = PostForm()
  
  if (form.validate_on_submit()):
    title = request.form.get("title")
    message = request.form.get("message")
    bID = boardID
    
    if (form.photo.data !=  None):
      image = True
      
      f = request.files['photo']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
      
      imageLocation = f.filename
      print(imageLocation)
    else:
      image = False
      imageLocation = ""
    
    newPost = Post(
      title=title,
      message=message,
      board=bID,
      image=image,
      imageLocation=imageLocation
    )
    
    print("New Post Title:" + newPost.title + " to board: " + newPost.board)
    print("New Post Message:" + newPost.message)
    
    db.session.add(newPost)
    db.session.commit()
  
  return redirect(url_for('home'))


'''Board Related Routes'''

# View Boards Route
@app.route('/boards', methods=['GET', 'POST'])
@app.route('/boards=<sortF>', methods=['GET', 'POST'])
@app.route('/boards=<sortF>,<sortD>', methods=['GET', 'POST'])
def boards(sortF = None, sortD = None):
  boards = RetrieveAllBoards()
  print ("Faculty: " + sortF)
  print ("Department: " + sortD)
  
  return render_template('boards.html', 
    boards=boards, 
    sortF=sortF
  )

# View Board Route
@app.route('/board<bID>', methods=['GET'])
def board(bID):
  # board = Board()
  board = Board.query.get(bID)
  
  posts = Post.query.filter_by(board=bID)
  posts = [entry.toDict() for entry in posts]
  boardId = bID
  
  print(board)

  return render_template("boardPosts.html", 
    posts=posts, boardId=boardId, board=board
  )

# Create a Board Route
@app.route('/create-board', methods=['GET'])
def createBoard():
  form = BoardForm()
    
  return render_template("form.html",
    formBoard = form
  )

# Upload Board Route
@app.route('/create-board', methods=['GET', 'POST'])
def uploadBoard():
  form = BoardForm()
  
  if (form.validate_on_submit()):
    title = request.form.get("title")
    faculty = request.form.get("faculty")
    dept = None
    
    # if (form.photo.data !=  None):
    #   image = True
      
    #   f = request.files['photo']
    #   f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
      
    #   imageLocation = f.filename
    #   print(imageLocation)
    # else:
    #   image = False
    #   imageLocation = ""
    
    newBoard = Board(
      title=title,
      faculty=faculty,
      dept=dept
      # image=image,
      # imageLocation=imageLocation
    )
    
    print("New Board Title:" + newBoard.title)
    
    db.session.add(newBoard)
    db.session.commit()
  
  return redirect(url_for('boards'))


'''Remove from Production'''

# Temp Route to purge all Databases
@app.route('/purge', methods=['GET', 'POST'])
def delete():
  posts = Post.query
  boards = Board.query
  users = User.query
  
  for p in posts:
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], "/post/", p))
    db.session.delete(p)
  
  for b in boards:
    db.session.delete(b)
    
  for u in users:
    db.session.delete(u)
  
  
  db.session.commit()
  
  return redirect(url_for('home'))
  
# Drops all tables and recreates them
@app.route('/drop', methods=['GET', 'POST'])
def dropAll():
  db.drop_all()
  reCreate_db()
  db.session.commit()
  
  FacultyDept.initalise()
  
  return redirect(url_for('home'))

# LOGIN FORM
@app.route('/login', methods=['GET'])
def login():
    form = LogIn()
    return render_template('login.html', form=form)

# SUBMIT LOGIN FORM
@app.route('/login', methods=['POST'])
def loginAction():
    form = LogIn()
    if form.validate_on_submit():  # respond to form submission
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):  # check credentials
            flash('Logged in successfully.')  # send message to next page
            login_user(user)  # login the user
            return redirect(url_for('home'))  # redirect to main page if login successful
    flash('Invalid credentials')
    return redirect(url_for('login'))

# SHOW USER DATA
@app.route('/users', methods=['GET'])
def get_user():
    users = User.query.all()
    return json.dumps([user.toDict() for user in users])

# SIGN UP FORM
@app.route('/signup', methods=['GET'])
def signup():
    signup = SignUp()  # create form object
    return render_template('signup.html', form=signup)  # pass form object to template

# SUBMIT SIGN UP FORM
@app.route('/signup', methods=['POST'])
def signupAction():
    form = SignUp()  # create form object
    if form.validate_on_submit():
        data = request.form  # get data from form submission
        newuser = User(username=data['username'],
                       email=data['email'],
                       faculty=data['faculty'],
                       dept=data['dept'])  # create user object
        newuser.set_password(data['password'])  # set password
        db.session.add(newuser)  # save new user
        db.session.commit()
        flash('Account Created!')  # send message
        return redirect(url_for('login'))  # redirect to login page
    flash('Error invalid input!')
    return redirect(url_for('signup'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=8080)
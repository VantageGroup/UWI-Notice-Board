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
from flask_login import (
  LoginManager, 
  current_user, 
  login_user, 
  login_required, 
  logout_user
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

from flask_login import LoginManager, current_user, login_user, login_required, logout_user
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
  Subscriber,
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
from functions.userFunctions import (
  LoginForm,
  SignUpForm
)

from datetime import datetime, date
import datetime

def create_app():
  app = Flask(__name__, static_url_path='/static')
  CORS(app)
  app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
  app.config['TEMPLATE_AUTO_RELOAD'] = True
  app.config['DEBUG'] = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.config['PREFERRED_URL_SCHEME'] = 'https'
  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
  
  os.makedirs(os.path.join(app.instance_path, 'post'), exist_ok=True)
  os.makedirs(os.path.join(app.instance_path, 'board'), exist_ok=True)
  os.makedirs(os.path.join(app.instance_path, 'user'), exist_ok=True)
  app.config['UPLOADED_PHOTOS_DEST'] = app.instance_path
  
  app.config['POST_FOLDER'] = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'post')
  app.config['BOARD_FOLDER'] = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'board')
  app.config['PROFILE_FOLDER'] = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], 'user')
  
  app.config['SECRET_KEY'] = 'password'
  
  configure_uploads(app, UploadSet('photos', IMAGES))
  create_db(app)

  editor = CKEditor()
  editor.init_app(app)
  
  login_manager.init_app(app)
  
  app.app_context().push()
  
  return app


login_manager = LoginManager()

app = create_app()
migrate = get_migrate(app)

@login_manager.user_loader
def load_user(user_id):
  return db.session.get(User, user_id)

@app.context_processor
def base():
  searchPost = SearchForm()
  return dict(form=searchPost)

FacultyDept.initialize()
Faculty.initialize()


'''Functions'''

# Retrieve all Posts from the Database
def RetrieveAllPosts():
  posts = Post.query.all()
  posts = [entry.toDict() for entry in posts]
  
  return posts

# Retrieve all Boards from the Database
def RetrieveAllBoards():
  boards = Board.query.all()
  boards = [entry.toDict() for entry in boards]
  
  return boards

#
def RetrieveFacultyList():
  list = Faculty.query.all()
  list = [entry.toDict() for entry in list]
  
  return list

#
def RetrieveDepartmentList():
  list = FacultyDept.query.all()
  list = [entry.toDict() for entry in list]
  
  return list

#
def RetrieveUserBoards(uID):
  boards = Subscriber.query.filter(user=uID)
  boards = [entry.toDict() for entry in boards]
  
  return boards

#
def RetrieveFeed(uID):
  boards = RetrieveUserBoards(uID)
  
  for board in boards:
    posts.append( Post.query.filter(bID=board.id) )
  
  posts = [entry.toDict() for entry in posts]
  
  return posts


'''App Routes'''

# Landing Page
@app.route('/')
@app.route('/|<sortF>', methods=['GET', 'POST'])
@app.route('/|<sortF>,<sortD>', methods=['GET', 'POST'])
def home(sortF = None, sortD = None):
  feed = RetrieveAllPosts()
  boards = RetrieveAllBoards()
  faculty = RetrieveFacultyList()
  department = RetrieveDepartmentList()
  
  if sortF != None:
    print ("Sorting by Faculty: " + sortF)
    
  if sortD != None:
    print ("Sorting by Department: " + sortD)
  
  return render_template('index.html', 
    posts=feed,
    boards=boards,
    sortF=sortF,
    sortD=sortD,
    faculty=faculty,
    department=department
  )

# Retrieve Uploaded Image
@app.route('/<filename>')
def get_file(filename): 
  return send_from_directory(app.config['POST_FOLDER'], filename)

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

# App Route for Calendar
@app.route('/cal')
def cal():
  posts = Post.query.all()

  events = [{
    'title' : 'TestEvent',
      'start' : '2023-03-10',
      'end'   :  '',
      'url'   : 'https://youtube.com'

  }, ]

  
  for post in posts: 
   events.append({
      'title' : post.title,
      'start' : post.startDate,
      'end'   : post.endDate,
      'url'   : 'https://youtube.com'
     },
  )

  return render_template("cal.html", events=events)


'''Post Related Routes'''

# Create a Post Route
@app.route('/board<bID>=create-post', methods=['GET'])
def createPost(bID):
  form = PostForm()
    
  return render_template("form.html",
    formPost = form
  )
  
# Edit a Post Route
@app.route('/board<bID>=edit-post<pID>', methods=['GET'])
def editPost(bID, pID):
  board = db.session.get(Board, bID)
  post = db.session.get(Post, pID)
  
  form = PostForm(
    title = post.title,
    message = post.message,
    # photo = 
    startDate = post.startDate,
    endDate = post.endDate
  )
    
  return render_template("form.html",
    formPost = form
  )

# Upload Post Route
@app.route('/board<bID>=create-post', methods=['POST'])
def uploadPost(bID):
  form = PostForm()
  board = db.session.get(Board, bID)
  
  if (form.validate_on_submit):
    bID = bID
    title = request.form.get("title")
    message = request.form.get("message")
    fac = board.faculty
    dept = board.dept
    
    creation = datetime.datetime.now()
    startDate = request.form.get("startDate")
    endDate = request.form.get("endDate")

    if (startDate != '' and endDate != ''):
      event = True
      
      startDateObj = datetime.datetime.strptime(startDate, '%Y-%m-%d')
      endDateObj = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    elif (startDate == '' and endDate != ''):
      event = True
      
      startDateObj = datetime.datetime.strptime(endDate, '%Y-%m-%d')
      endDateObj = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    else:
      event = False
      
      startDateObj = datetime.datetime.now()
      endDateObj = datetime.datetime.now()
    
    if (form.photo.data !=  None):
      image = True
      
      f = request.files['photo']
      f.save(os.path.join(app.config['POST_FOLDER'], f.filename))
      
      imageLocation = f.filename
      print(imageLocation)
    else:
      image = False
      imageLocation = ""
    
    newPost = Post(
      bID=bID,
      title=title,
      message=message,
      
      faculty=fac,
      dept=dept,
      
      image=image,
      imageLocation=imageLocation,
      
      dateCreated=creation,
      
      event=event,
      startDate=startDateObj,
      endDate=endDateObj
    )
    
    print("New Post Title:" + newPost.title + " to board: " + newPost.bID)
    print("New Post Message:" + newPost.message)
    print(newPost.dateCreated)
    
    db.session.add(newPost)
    db.session.commit()

    events = [ {
      'title' : title,
      'start' : startDateObj,
      'end' : endDateObj,
      'url' : 'https://youtube.com'
      }
    ]
  else:
    print("Form did not validate on submit")  
  
  return render_template('cal.html', events=events)

# Upload Editted Post Route
@app.route('/board<bID>=edit-post,pID>', methods=['POST'])
def uploadEdittedPost(bID):
  board = db.session.get(Board, bID)
  form = PostForm()
  
  if (form.validate_on_submit):
    bID = bID
    title = request.form.get("title")
    message = request.form.get("message")
    fac = board.faculty
    dept = board.dept
    
    creation = datetime.datetime.now()
    startDate = request.form.get("startDate")
    endDate = request.form.get("endDate")

    if (startDate != '' and endDate != ''):
      event = True
      
      startDateObj = datetime.datetime.strptime(startDate, '%Y-%m-%d')
      endDateObj = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    elif (startDate == '' and endDate != ''):
      event = True
      
      startDateObj = datetime.datetime.strptime(endDate, '%Y-%m-%d')
      endDateObj = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    else:
      event = False
      
      startDateObj = datetime.datetime.now()
      endDateObj = datetime.datetime.now()
    
    if (form.photo.data !=  None):
      image = True
      
      f = request.files['photo']
      f.save(os.path.join(app.config['POST_FOLDER'], f.filename))
      
      imageLocation = f.filename
      print(imageLocation)
    else:
      image = False
      imageLocation = ""
    
    newPost = Post(
      bID=bID,
      title=title,
      message=message,
      
      faculty=fac,
      dept=dept,
      
      image=image,
      imageLocation=imageLocation,
      
      dateCreated=creation,
      
      event=event,
      startDate=startDateObj,
      endDate=endDateObj
    )
    
    print("New Post Title:" + newPost.title + " to board: " + newPost.bID)
    print("New Post Message:" + newPost.message)
    print(newPost.dateCreated)
    
    db.session.add(newPost)
    db.session.commit()

    events = [ {
      'title' : title,
      'start' : startDateObj,
      'end' : endDateObj,
      'url' : 'https://youtube.com'
      }
    ]
  else:
    print("Form did not validate on submit")  
  
  return render_template('cal.html', events=events)


'''Board Related Routes'''

# View Boards Route
@app.route('/boards', methods=['GET', 'POST'])
@app.route('/boards|<sortF>', methods=['GET', 'POST'])
@app.route('/boards|<sortF>,<sortD>', methods=['GET', 'POST'])
def boards(sortF = None, sortD = None):
  boards = RetrieveAllBoards()
  faculty = RetrieveFacultyList()
  department = RetrieveDepartmentList()
  
  if sortF != None:
    print ("Sorting by Faculty: " + sortF)
    
  if sortD != None:
    print ("Sorting by Department: " + sortD)
  
  return render_template('boards.html', 
    boards=boards, 
    sortF=sortF,
    sortD=sortD,
    faculty=faculty,
    department=department
  )

# View Board Route
@app.route('/board<bID>', methods=['GET'])
def board(bID):
  board = db.session.get(Board, bID)
  
  posts = Post.query.filter_by(bID=bID)
  posts = [entry.toDict() for entry in posts]
  boardId = bID
  
  print(board)
  print(posts)

  return render_template("boardPosts.html",  
    boardId=boardId, 
    board=board,
    posts=posts
  )

# Create a Board Route
@app.route('/create-board', methods=['GET'])
def createBoard():
  form = BoardForm()
  faculty = RetrieveFacultyList()
  department = RetrieveDepartmentList()
    
  return render_template("form.html",
    formBoard = form,
    faculty=faculty,
    department=department,
    choice=None
  )

# Edit a Board Route
@app.route('/edit-board<bID>', methods=['GET'])
def editBoard(bID):
  board = db.session.get(Board, bID)
  
  form = BoardForm(
    title=board.title
  )
  choice = str(board.faculty) + "+" + str(board.dept)
  print(choice)
  
  faculty = RetrieveFacultyList()
  department = RetrieveDepartmentList()
    
  return render_template("form.html",
    formBoard = form,
    faculty=faculty,
    department=department,
    choice=choice
  )

# Upload Board Route
@app.route('/create-board', methods=['POST'])
def uploadBoard():
  form = BoardForm()
  
  if (form.validate_on_submit()):
    title = request.form.get("title")
    faculty = None
    dept = None
    
    assign = request.form.get("faculty")
    if "+" in assign:
      faculty = assign.split("+")[0]
      dept = assign.split("+")[1]
      
      print("Faculty = " + faculty)
      print("Department = " + dept)
    else:
      faculty = assign
      dept = None
      
      print("Faculty = " + faculty)
    
    # if (form.photo.data !=  None):
    #   image = True
      
    #   f = request.files['photo']
    #   f.save(os.path.join(app.config['POST_FOLDER'], f.filename))
      
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

# Upload Editted Board Record Route
@app.route('/edit-board<bID>', methods=['POST'])
def uploadEdittedBoard(bID):
  board = Board.query.get(bID)
  form = BoardForm()
  
  if (form.validate_on_submit()):
    title = request.form.get("title")
    faculty = None
    dept = None
    
    assign = request.form.get("faculty")
    if "+" in assign:
      faculty = assign.split("+")[0]
      dept = assign.split("+")[1]
      
      print("Faculty = " + faculty)
      print("Department = " + dept)
    else:
      faculty = assign
      dept = None
      
      print("Faculty = " + faculty)
    
    # if (form.photo.data !=  None):
    #   image = True
      
    #   f = request.files['photo']
    #   f.save(os.path.join(app.config['POST_FOLDER'], f.filename))
      
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


'''User Related Routes'''

# Login Form Route
@app.route('/login', methods=['GET'])
def login():
  form = LoginForm()
    
  return render_template('login.html', form=form)

# Upload Login Route
@app.route('/login', methods=['POST'])
def loginAction():
  form = LoginForm()
    
  if form.validate_on_submit():
    data = request.form
        
    user = User.query.filter_by(username=data['username']).first()
        
    if user and user.check_password(data['password']):
      flash('Logged in successfully.')
      login_user(user)
            
      return redirect(url_for('home'))
          
    flash('Invalid credentials')
    return redirect(url_for('login'))

# SIgnup Form Route
@app.route('/signup', methods=['GET'])
def signup():
  signup = SignUpForm()
    
  return render_template('signup.html', form=signup)

# Upload Signup Route
@app.route('/signup', methods=['POST'])
def signupAction():
  form = SignUpForm()
    
  if form.validate_on_submit():
    data = request.form
        
    newuser = User(
      username=data['username'],
      email=data['email'],
      faculty=data['faculty'],
      dept=data['dept']
    )
        
    newuser.set_password(data['password'])
        
    db.session.add(newuser)
    db.session.commit()
        
    flash('Account Created!')
    return redirect(url_for('login'))
      
  flash('Error invalid input!')
  return redirect(url_for('signup'))


'''Remove from Production'''

# Temp Route to purge all Databases
@app.route('/purge', methods=['GET', 'POST'])
def delete():
  posts = Post.query
  boards = Board.query
  users = User.query
  
  for p in posts:
    os.remove(os.path.join(app.config['POST_FOLDER'], p.imageLocation))
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
  
  FacultyDept.initialize()
  Faculty.initialize()
  
  return redirect(url_for('home'))

# User Table
@app.route('/users', methods=['GET'])
def get_user():
  users = User.query.all()
  return json.dumps([user.toDict() for user in users])


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, port=8080)
#hello world

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
  url_for,
  session
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

from flask_login import (
  LoginManager, 
  current_user, 
  login_user, 
  login_required, 
  logout_user
)

from models import (
  db, 
  get_migrate, 
  create_db,
  reCreate_db
)
from models import (
  Post, 
  Event,
  Follow,
  
  Board, 
  Subscriber,
  
  User,
  Profile,
  
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
import pytz

from functools import wraps
from flask import abort

from sqlalchemy import desc


def create_app():
  app = Flask(__name__)
  CORS(app)
  app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
  app.config['TEMPLATE_AUTO_RELOAD'] = True
  app.config['DEBUG'] = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.config['PREFERRED_URL_SCHEME'] = 'https'
  
  app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://uwi_notice_board_user:a7L2PrFm9cj9YPqxezyO8na4JxQKMi96@dpg-cgpecfpeuhlq286280og-a.oregon-postgres.render.com/uwi_notice_board'
  #postgres://uwi_notice_board_user:a7L2PrFm9cj9YPqxezyO8na4JxQKMi96@dpg-cgpecfpeuhlq286280og-a.oregon-postgres.render.com/uwi_notice_board
  
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
  return User.query.get(int(user_id))

@app.context_processor
def base():
  searchPost = SearchForm()
  return dict(form=searchPost)

FacultyDept.initialize()
Faculty.initialize()


'''Functions'''
# Decorator function to restrict route access to admins
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.isAdmin:
            abort(403) # Forbidden
        return f(*args, **kwargs)
    return decorated_function




# Retrieve all Posts from the Database
def RetrieveAllPosts():
  list = Post.query.order_by(Post.id.desc()).all()
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieve all Boards from the Database
def RetrieveAllBoards():
  list = Board.query.all()
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieve all Events from the Database
def RetrieveAllEvents():
  list = Event.query.all()
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieves all User Profiles from the Database
def RetreveProfiles():
  list = Profile.query.all()
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieve all Facuties from the Database
def RetrieveFacultyList():
  list = Faculty.query.all()
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieve all Departments from the Database
def RetrieveDepartmentList():
  list = FacultyDept.query.all()
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieve User Subscribed Boards
def RetrieveUserBoards():
  list = Subscriber.query.filter_by(user=current_user.id)
  list = [entry.toDict() for entry in list]
  
  return list

# Retrieve User Post Feed
def RetrieveFeedSub():
  all_posts = RetrieveAllPosts() 
  boards = RetrieveUserBoards()
  
  posts = []

  for board in boards:
    for post in all_posts:
      if (post['bID'] == board['board']):
        posts.append(post)
  
  return posts

#
def RetrieveUserFollowed():
  list = Follow.query.filter_by(user=current_user.id)
  list = [entry.toDict() for entry in list]
  
  return list
  

# Retrieve User Followed Events
def RetrieveFollowedEvents():
  all_events = RetrieveAllEvents() 
  follow = RetrieveUserFollowed()
  
  events = []

  for post in follow:
    for event in all_events:
      print(post['id'])
      if (event['post'] == post['post']):
        events.append(event)
  
  return events

#############################################


'''App Routes'''

# Landing Page
@app.route('/')
@app.route('/|<sortF>', methods=['GET', 'POST'])
@app.route('/|<sortF>,<sortD>', methods=['GET', 'POST'])
def home(sortF = None, sortD = None):
  if (current_user.is_authenticated):
    currentSysDateTime = datetime.datetime.now()

    boards = RetrieveAllBoards()
    faculty = RetrieveFacultyList()
    department = RetrieveDepartmentList()
    
    feed = Post.query.filter(Post.schedulePostDate<=currentSysDateTime, Post.scheduledDeleteDate>=currentSysDateTime)
    feed = feed.order_by(Post.schedulePostDate.desc())
    
    for post in feed:
      profile = Profile.query.filter_by(user=post.owner).first()
      
      post = post.toDict()
      
      post['username'] = profile.username
      post['userImage'] = profile.image
      post['userImageLocation'] = profile.imageLocation
      
  
    
    return render_template('index.html', 
      posts=feed,
      boards=boards,
      sortF=sortF,
      sortD=sortD,
      faculty=faculty,
      department=department
    )
 
  else:
    return redirect(url_for('login'))

# Feed Route
@app.route('/feed', methods=['GET'])
@app.route('/feed|<sortF>', methods=['GET', 'POST'])
@app.route('/feed|<sortF>,<sortD>', methods=['GET', 'POST'])
def feed(sortF = None, sortD = None):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  currentSysDateTime = datetime.datetime.now()
  
  feed = Post.query.filter(Post.schedulePostDate<=currentSysDateTime, Post.scheduledDeleteDate>=currentSysDateTime)
  feed = feed.order_by(Post.schedulePostDate.desc())
  faculty = RetrieveFacultyList()
  department = RetrieveDepartmentList()
  boards = RetrieveAllBoards()
  subBoards = Subscriber.query.filter_by(user = current_user.id)
  subBoards = [entry.toDict() for entry in subBoards]
  
  newFeed = []

  for board in subBoards:
    for singlePost in feed:
      if singlePost.bID == board['board']:
        newFeed.append(singlePost)

  newFeed = [singlePost.toDict() for singlePost in newFeed]
  
  
  return render_template('feed.html', 
    posts=newFeed,
    boards=boards,
    sortF=sortF, 
    sortD=sortD, 
    faculty=faculty, 
    department=department
  )

# Retrieve Post Uploaded Image
@app.route('/pimage<filename>')
def get_post_image(filename): 
  return send_from_directory(app.config['POST_FOLDER'], filename)

# Retrieve Board Uploaded Image
@app.route('/bimage<filename>')
def get_board_image(filename): 
  return send_from_directory(app.config['BOARD_FOLDER'], filename)

# Retrieve User Uploaded Image
@app.route('/uimage<filename>')
def get_user_image(filename): 
  return send_from_directory(app.config['PROFILE_FOLDER'], filename)

#Search Posts
@app.route('/search', methods=["POST"])
@app.route('/search|sortF=<sortF>', methods=['GET', 'POST'])
@app.route('/search|sortF=<sortF>,sortD?=<sortD>', methods=['GET', 'POST'])
def search(sortF = None, sortD = None):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  currentSysDateTime = datetime.datetime.now()
  
  postsDb = Post.query.filter(Post.schedulePostDate<=currentSysDateTime, Post.scheduledDeleteDate>=currentSysDateTime)
  boardsDb = Board.query.all()
  faculty = RetrieveFacultyList()
  department = RetrieveDepartmentList()
  
  search = request.form.get('searchCriteria')
  
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
    posts = foundPosts,
    sortF = sortF,
    sortD = sortD,
    faculty=faculty,
    department=department
  )

# Calendar
@app.route('/cal')
def cal():
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  events = RetrieveFollowedEvents()
  
  return render_template("cal.html", events=events)

#############################################


'''Post Related Routes'''

# View Post
@app.route('/post<pID>', methods=['GET'])
def viewPost(pID):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    post = db.session.query(Post).get(pID)
    if post is None:
        abort(404)

    post.viewCount += 1
    db.session.add(post)
    db.session.commit()

    return render_template('post.html', post=post.toDict())

# Create a Post Route
@app.route('/board<bID>=create-post', methods=['GET'])
@admin_required
def createPost(bID):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  form = PostForm()
    
  return render_template("form.html",
    formPost = form
  )
  
# Edit a Post Route
@app.route('/board<bID>=edit-post<pID>', methods=['GET'])
@admin_required
def editPost(bID, pID):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  post = db.session.get(Post, pID)
  print (db.session.get(Post, pID))

  form = PostForm(
    title = post.title,
    message = post.message,
    # photo = 
    startDate = post.startDate,
    endDate = post.endDate,
    schedulePostDate = post.schedulePostDate,
    scheduledDeleteDate = post.scheduledDeleteDate
  )
    
  return render_template("form.html",
    formPost = form
  )

# Upload Post Route
@app.route('/board<bID>=create-post', methods=['POST'])
def uploadPost(bID):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
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
    schedulePostDate = request.form.get("schedulePostDate")
    scheduledDeleteDate = request.form.get("scheduledDeleteDate")
    
    if (startDate != '' and endDate != ''):
      event = True
      
      startDateObj = datetime.datetime.strptime(startDate, '%Y-%m-%d')
      endDateObj = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    elif (startDate == '' and endDate != ''):
      event = True
      
      startDateObj = datetime.datetime.strptime(endDate, '%Y-%m-%d')
      endDateObj = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    elif (startDate != '' and endDate == ''):
      event = True
      
      startDateObj = datetime.datetime.strptime(startDate, '%Y-%m-%d')
      endDateObj = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    else:
      event = False
      
      startDateObj = None
      endDateObj = None

    if (schedulePostDate != ''):
      schedulePostDateObj = datetime.datetime.strptime(schedulePostDate, '%Y-%m-%dT%H:%M')
    else:
      schedulePostDateObj = datetime.datetime.now()

    if (scheduledDeleteDate != ''):
      scheduledDeleteDateObj = datetime.datetime.strptime(scheduledDeleteDate, '%Y-%m-%dT%H:%M')
    else:
      scheduledDeleteDateObj = None
    
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
      owner=current_user.id,
      title=title,
      message=message,
      
      faculty=fac,
      dept=dept,
      
      image=image,
      imageLocation=imageLocation,
      
      dateCreated=creation,
      
      event=event,
      startDate=startDateObj,
      endDate=endDateObj,

      schedulePostDate = schedulePostDateObj,
      scheduledDeleteDate = scheduledDeleteDateObj,
    )
    db.session.add(newPost)
    db.session.commit()

    latest_entry = Post.query.order_by(Post.id.desc()).first()
    
    print(latest_entry.event)
    if (latest_entry.event == True):
      newEvent = Event(
        post = latest_entry.id,
        title = latest_entry.title,
        startDate = startDateObj,
        endDate = endDateObj,
        url = request.base_url + url_for('viewPost', pID=latest_entry.id)
      )
      
      follow = Follow(
        post = latest_entry.id,
        user = current_user.id
      )
      
      db.session.add(newEvent)
      db.session.add(follow)
      db.session.commit()

  else:
    print("Form did not validate on submit")  
  
  return  redirect(url_for('board', bID=bID))

# Upload Edited Post Route
@app.route('/board<bID>=edit-post<pID>', methods=['POST'])
@admin_required
def uploadEdittedPost(bID, pID):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  board = db.session.get(Board, bID)
  post = db.session.get(Post, pID)
  eventObj = Event.query.filter_by(post=post.id)
  
  form = PostForm()
  
  if (form.validate_on_submit):
    title = request.form.get("title")
    message = request.form.get("message")
    fac = board.faculty
    dept = board.dept
    
    startDate = request.form.get("startDate")
    endDate = request.form.get("endDate")
    schedulePostDate = request.form.get("schedulePostDate")
    scheduledDeleteDate = request.form.get("scheduledDeleteDate")

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


    if (schedulePostDate != ''):
      schedulePostDateObj = datetime.datetime.strptime(schedulePostDate, '%Y-%m-%dT%H:%M')
    else:
      schedulePostDateObj = datetime.datetime.now()

    if (scheduledDeleteDate != ''):
      scheduledDeleteDateObj = datetime.datetime.strptime(schedulePostDate, '%Y-%m-%dT%H:%M')
      
    if (form.photo.data !=  None):
      image = True
      
      f = request.files['photo']
      f.save(os.path.join(app.config['POST_FOLDER'], f.filename))
      
      imageLocation = f.filename
      print(imageLocation)
    else:
      image = False
      imageLocation = ""
                   
    post.title = title
    post.message = message
    post.faculty = fac
    post.dept = dept
    post.image = image
    post.imageLocation = imageLocation
    post.event = event
    post.startDate = startDateObj
    post.endDate = endDateObj
    post.schedulePostDate = schedulePostDateObj
    post.scheduledDeleteDate = scheduledDeleteDateObj
    
    eventObj.title = post.title
    eventObj.startDate = startDateObj
    eventObj.endDate = endDateObj
    
    db.session.commit()
  else:
    print("Form did not validate on submit")  
  
  return  redirect(url_for('board', bID=bID))

# Follow a post
@app.route('/follow<pID>', methods=['GET'])
def follow(pID):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  if (Follow.query.filter_by(post=pID, user=current_user.id).first()):
    print("The user is already following post")
  elif (Event.query.filter_by(post=pID).first() == None):
    print("Post is not event")
  else:
    following = Follow(
      post = pID,
      user = current_user.id
    )
    
    db.session.add(following)
    db.session.commit()

  return redirect(url_for('feed'))

#############################################


'''Board Related Routes'''

# View Boards Route
@app.route('/boards', methods=['GET', 'POST'])
@app.route('/boards|<sortF>', methods=['GET', 'POST'])
@app.route('/boards|<sortF>,<sortD>', methods=['GET', 'POST'])
def boards(sortF = None, sortD = None):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  boards = RetrieveAllBoards()
  faculty = RetrieveFacultyList()
  department = RetrieveDepartmentList()
  
  subscribers = Subscriber.query.filter_by(user=current_user.id)
  subscribers = [entry.toDict() for entry in subscribers]
  
  for board in boards:
    board['currentUserIsSubd'] = False
    for sub in subscribers:
        if sub['board'] == board['id']:
            board['currentUserIsSubd'] = True
            break
    
  return render_template('boards.html', 
    boards=boards, 
    sortF=sortF,
    sortD=sortD,
    faculty=faculty,
    department=department,
    subscribers=subscribers
  )
  
# View Saved Boards Route
@app.route('/user-boards', methods=['GET', 'POST'])
@app.route('/user-boards|<sortF>', methods=['GET', 'POST'])
@app.route('/user-boards|<sortF>,<sortD>', methods=['GET', 'POST'])
def savedBoards(sortF = None, sortD = None):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  userBoards = RetrieveUserBoards()
  boards = RetrieveAllBoards()
  faculty = RetrieveFacultyList()
  department = RetrieveDepartmentList()
  
  return render_template('savedBoards.html', 
    userBoards=userBoards,
    boards=boards, 
    sortF=sortF,
    sortD=sortD,
    faculty=faculty,
    department=department
  )

# View Board Route
@app.route('/board<bID>', methods=['GET'])
def board(bID):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  currentSysDateTime = datetime.datetime.now()
  board = db.session.get(Board, bID)
  posts = Post.query.filter(Post.schedulePostDate<=currentSysDateTime, Post.scheduledDeleteDate>=currentSysDateTime)
  posts = Post.query.filter_by(bID=bID)
  
  
  
  posts = posts.order_by(Post.schedulePostDate.desc())
    
  posts = [entry.toDict() for entry in posts]
  boardId = bID

  return render_template("boardPosts.html",  
    boardID=boardId, 
    board=board,
    posts=posts
  )

# Create a Board Route
@app.route('/create-board', methods=['GET'])
@admin_required
def createBoard():
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  form = BoardForm()
  faculty = RetrieveFacultyList()
  department = RetrieveDepartmentList()
    
  return render_template("form.html",
    formBoard = form,
    faculty=faculty,
    department=department,
    choice=None
  )


# Delete a Board
@app.route('/edit-board<bID>', methods=['GET'])
@login_required
@admin_required
def deleteBoard(bID):
  board = db.session.get(Board, bID)
  return redirect(url_for('boards'))


# Edit a Board Route
@app.route('/edit-board<bID>', methods=['GET'])
# @login_required
@admin_required
def editBoard(bID):
  if (current_user.is_authenticated):
    return redirect(url_for('login'))
  
  board = db.session.get(Board, bID)
  
  form = BoardForm(
    title=board.title
  )
  
  choice = str(board.faculty) + "+" + str(board.dept)
  
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
@admin_required
def uploadBoard():
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
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
    
    if (form.photo.data !=  None):
      image = True
      
      f = request.files['photo']
      f.save(os.path.join(app.config['BOARD_FOLDER'], f.filename))
      
      imageLocation = f.filename
      print(imageLocation)
    else:
      image = False
      imageLocation = ""
    
    newBoard = Board(
      title=title,
      faculty=faculty,
      dept=dept,
      image=image,
      imageLocation=imageLocation
    )
    db.session.add(newBoard)
    db.session.commit()


    latest_entry = Board.query.order_by(Board.id.desc()).first()

    subscriber = Subscriber(
      board = latest_entry.id,
      user = current_user.id,
      isAdmin = True,
      isSubscribed = True
    )
    db.session.add(subscriber)
    db.session.commit()
  
  return redirect(url_for('boards'))

# Upload Editted Board Record Route
@app.route('/edit-board<bID>', methods=['POST'])
@admin_required
def uploadEdittedBoard(bID):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
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
    
    if (form.photo.data !=  None):
      image = True
      
      f = request.files['photo']
      f.save(os.path.join(app.config['POST_FOLDER'], f.filename))
      
      imageLocation = f.filename
      print(imageLocation)
    else:
      image = False
      imageLocation = ""
    
    board.title = title
    board.faculty = faculty
    board.dept = dept
    board.image = image,
    board.imageLocation = imageLocation
    
    db.session.commit()
  
  return redirect(url_for('boards'))

# Join Board Route
@app.route('/join<bID>', methods=['GET'])
def join(bID):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  board = db.session.get(Board,bID)
  
  if (Subscriber.query.filter_by(board=bID, user=current_user.id).first()):
   print("The user is already subscribed")
  else:
    subscriber = Subscriber(
      board = bID,
      user = current_user.id,
      isAdmin = False,
      isSubscribed = True
    )
    db.session.add(subscriber)

    board.subscribers = board.subscribers + 1

  db.session.commit()

  return redirect(url_for('board',bID=bID))

# Leave Board Route
@app.route('/leave<bID>', methods=['GET'])
def leave(bID):
  if (current_user.is_authenticated == False):
    return redirect(url_for('login'))
  
  board = db.session.get(Board,bID)
  
  if (Subscriber.query.filter_by(board=board.id, user=current_user.id).first()):
    print("deleting entry")
    Subscriber.query.filter_by(board=bID, user=current_user.id).first().delete()
    board.subscribers = board.subscribers - 1
    db.session.commit()

  return redirect(url_for('board',bID=bID))





#############################################


'''User Related Routes'''

# Login Form Route
@app.route('/login', methods=['GET'])
def login():
  form = LoginForm()
    
  return render_template('newlogin.html', form=form)

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
  
# Signup Form Route
@app.route('/signup', methods=['GET'])
def signup():
  signup = SignUpForm()
    
  return render_template('newsignup.html', form=signup)

# Upload Signup Route
@app.route('/signup', methods=['POST'])
def signupAction():
  form = SignUpForm()
    
  if form.validate_on_submit():
    data = request.form
        
    newUser = User(
      username = data['username'],
      email = data['email'],
      isAdmin = True
    )
    newUser.set_password(data['password'])
    db.session.add(newUser)
    db.session.commit()
    
    latest_entry = User.query.order_by(User.id.desc()).first()
    profile = Profile(
      user = latest_entry.id,
      username = latest_entry.username,
      image = False,
      imageLocation = None
    )
    db.session.add(profile)
    db.session.commit()
    
    flash('Account Created!')
    return redirect(url_for('login'))
      
  flash('Error invalid input!')
  return redirect(url_for('signup'))

# Logout a User
@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('login'))
  
#############################################


'''Remove from Production'''

# Temp Route to purge all Databases
@app.route('/purge', methods=['GET', 'POST'])
def delete():
  if (current_user.is_authenticated):
    return redirect(url_for('login'))
  
  posts = Post.query
  boards = Board.query
  users = User.query
  
  for p in posts:
    os.remove(os.path.join(app.config['POST_FOLDER'], p.imageLocation))
    db.session.delete(p)
  
  for b in boards:
    os.remove(os.path.join(app.config['BOARD_FOLDER'], p.imageLocation))
    db.session.delete(b)
    
  for u in users:
    os.remove(os.path.join(app.config['PROFILE_FOLDER'], p.imageLocation))
    db.session.delete(u)
  
  
  db.session.commit()
  
  return redirect(url_for('home'))
  
# Drops all tables and recreates them
@app.route('/drop', methods=['GET', 'POST'])
def dropAll():
  if (current_user.is_authenticated):
    return redirect(url_for('login'))
  
  db.drop_all()
  reCreate_db()
  db.session.commit()
  
  FacultyDept.initialize()
  Faculty.initialize()
  
  return redirect(url_for('home'))

# User Table
@app.route('/users', methods=['GET'])
def get_user():
  if (current_user.is_authenticated):
    users = User.query.all()
    return json.dumps([user.toDict() for user in users])
  
  return redirect(url_for('login'))

# Subscriber Table
@app.route('/subscribers', methods=['GET'])
def get_subs():
  if (current_user.is_authenticated):
    subs = Subscriber.query.all()
    return json.dumps([sub.toDict() for sub in subs])
  
  return redirect(url_for('login'))
  
#############################################


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
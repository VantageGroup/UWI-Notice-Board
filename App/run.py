from app import create_app

app = create_app()


# @app.cli.command('ínit', with_appcontext=True)
# def initialize():
#   create_db(app)
  
#   with open('fac-dept.csv') as csvFile:
#     csvData = csv.DictReader(csvFile, delimiter=',')
    
#     facDept = []
#     for row in csvData:
#       fD = FacultyDept(
#         faculty = row['Faculty'],
#         fLabel = row['Flabel'],
#         department  = row['Department'],
#         dLabel = row['Dlabel']
#       )
      
#       facDept.append(fD)
    
#     db.session.add(facDept)
#     db.session.commit()
#     click.echo('databse inialized')
        
  
  
# import click, sys
# from models import db, Post
# from app import app


# @app.cli.command("init", help="Creates and initializes the database")
# def initialize():
#   db.drop_all()
#   db.init_app(app)
#   db.create_all()
#   Post1 = Post('1', 'Post1', 'Welcome')
#   db.session.add(Post1)
#   db.session.commit()
#   print(Post1)
#   print('database intialized')
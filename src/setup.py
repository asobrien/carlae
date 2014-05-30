from models import db

def create_db():
    db.create_all()  # Boom, there is the database!

def create_user(email, password):
    from models import User
    user = User(email)
    user.create_user(password)

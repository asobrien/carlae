from carlae.models import db, User

def initialize_db():
    """Initializes database for Carlae.

    #TODO: Full usage example?
    """
    db.create_all()  # Boom, there is the database!

def create_user(email, password):
    """Creates a user in the database.
    """
    user = User(email)
    user.create_user(password)

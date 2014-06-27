__author__ = 'aobrien'

from carlae.utils import db

# Create the database and tables
db.initialize_db()  # there it is

# Add the initial user
db.create_user('demo@carlae.com', 'shortenIT')

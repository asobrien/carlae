import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Enable form validation.
CSRF_ENABLED = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'my precious'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

# Set the root URL for the site
BASE_URL = 'http://oxygen.local:5000'

# Set the email address for the service (e.g., admin@example.com)
APP_EMAIL = 'admin@example.com'
APP_EMAIL_NAME = 'carlae'  # or None if you don't want to use an name for the address book

# Set the message sent on invitation here
INVITATION_EMAIL_TEMPLATE = u"""
Howdy,

You've been invited to join carlae, a private, self-hosted bit shortener service.

Go ahead and click the link (or paste into your browser) the link below to register & activate your account.

%s

Welcome!
"""

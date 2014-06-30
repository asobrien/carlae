# -*- coding: utf-8 -*-

import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Demo mode, change to false in a production enviroment
DEMO_MODE = True

# Enable debug mode.
DEBUG = True

# Enable form validation.
CSRF_ENABLED = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'A_NICE_STRONG_RANDOM_SECRET_KEY_GOES_HERE'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

# Set the root URL for the site
BASE_URL = 'http://0.0.0.0:5000'

# Set the email address for the service (e.g., admin@example.com)
APP_EMAIL = 'admin@example.com'
APP_EMAIL_NAME = 'carlae'  # or None if you don't want to use an name for the address book

# We use Mailgun to send emails, enter credentials here
MAILGUN_DOMAIN = "example.com"
MAILGUN_API_KEY = "APIKEY_GOES_HERE"

# Set the message sent on invitation here
INVITATION_EMAIL_TEMPLATE = u"""
Howdy,

You've been invited to join Carlae, a URL shortening service.

Go ahead and use the link to register & activate your account:

%s

Activation codes eventually expire; request a new one if that's the case.

Welcome!
"""

# Development info
CARLAE_VERSION = ''
CARLAE_BUILD = ''
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#

from main import db
from main import bcrypt
# from carlae.main import db, bcrypt

import base64
import urlparse
import uuid
import random
import string
import hashlib
import datetime
import urllib
import os
import mail
import config
import shortener

#----------------------------------------------------------------------------#
# DB Config.
#----------------------------------------------------------------------------#

# Set your classes here.

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, email):
        self.email = email
        self.get_user_details()

    def get_user_details(self):
        uname = User.query.filter_by(email=self.email).first()
        if uname is not None:
            for var, val in vars(uname).iteritems():
                setattr(self, var, val)

    def create_user(self, password):
        user = User(self.email)
        user.password = bcrypt.generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        self.get_user_details()  # update object with details

    def delete_user(self):
        user = User.query.get(self.id)
        db.session.delete(user)
        db.session.commit()
        # TODO: reset instance state
        self.reset()

    def reset(self):
        # how do we reset an instance (or kill it)
        pass

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generate_password(self, length=10):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def change_password(self, password):
        user = User.query.get(self.id)
        user.password = bcrypt.generate_password_hash(password)  # update pass
        db.session.commit()

    ### Flask-Login required methods ###
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)
    ### END Flask-Login required methods ###

    def __repr__(self):
        return '<User %r>' % self.email



class InviteUser(db.Model):
    __tablename__ = "invites"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    activation_code = db.Column(db.String(64))
    activation_date = db.Column(db.DateTime)
    is_activated = db.Column(db.Boolean, default=False)

    def __init__(self, email):
        self.email = email
        self.get_user_details()
        if self.email_exists():
            self.regenerate_activation_code()
            self.generate_activation_url()
        else:
            self.generate_activation_code()
            self.generate_activation_url()
            self.commit()
        self.get_user_details()  # get user details if they exist

    def get_user_details(self):
        user = InviteUser.query.filter_by(email=self.email).first()
        if user is not None:
            for var, val in vars(user).iteritems():
                setattr(self, var, val)

    def email_exists(self):
        user = InviteUser.query.filter_by(email=self.email).first()
        if user is not None:
            return True
        return False

    def generate_activation_code(self):
        self.activation_code = base64.urlsafe_b64encode(hashlib.sha512 \
                                (str(random.getrandbits(1024))).digest()).rstrip('==')
        # TODO: Ensure activation code is unique... loop until a unique solution is found. Actually, there's really no
        # need for a unique activation_code, because it's paired with an email, and there is so much entropy there.
        # Actually, it's best if unique... we'll deal with that later.

    def generate_activation_url(self):
        url = os.path.join(config.BASE_URL, 'activate')
        params = {'email':self.email, "code":self.activation_code}
        query = urllib.urlencode(params)
        full_url = url + '?' + query
        self.activation_url = full_url

    def send_activation_email(self):
        # GET THE LATEST FROM THE DATABASE
        usr = InviteUser.query.get(self.id)
        usr.generate_activation_url()
        from_email = config.APP_EMAIL
        to_list = [usr.email]
        subject = "Activate your account"
        message = config.INVITATION_EMAIL_TEMPLATE % (usr.activation_url)
        return mail.send_simple_message(from_email, to_list, subject, message, from_name=config.APP_EMAIL_NAME)

    def commit(self):
        self.activation_date = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()

    def regenerate_activation_code(self):
        usr = InviteUser.query.get(self.id)
        usr.generate_activation_code()
        usr.generate_activation_url()
        usr.activation_date = datetime.datetime.now()
        db.session.commit()



class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(1500), unique=True, nullable=False)
    shortlink = db.Column(db.String(6), nullable=True)
    counter = db.Column(db.Integer, default=0)

    def __init__(self, source_url):
        self.source = self.cleanup_url(source_url)
        self.already_exits()
        if self.shortlink is None:
            self.add_url_to_db()  # commits to db, get an id this way
            self.generate_shortlink()
            db.session.commit()  # update the db

    def already_exits(self):
        url = Url.query.filter_by(source=self.source).first()
        if url is not None:
            self.shortlink = url.shortlink
            self.id = url.id
            self.counter = url.counter
        else:
            self.shortlink = None

    def generate_shortlink(self):
        self.shortlink = shortener.encode_id(self.id)

    def cleanup_url(self, source_url):
        source_url = self.check_protocol(source_url)
        return urlparse.urlsplit(source_url).geturl()

    def is_valid_link(self):
        """Checks whether `source_url` is valid."""
        pass

    def check_protocol(self, url):
        return url if (url.lower().startswith('http://') or url.lower().startswith('https://')) else "http://" + url

    def _make_shortlink_unique(self):
        shortlink = self.shortlink
        while Url.query.filter_by(shortlink=shortlink).first() is not None:
            # need to regenerate shortlink
            random_seq = str(uuid.uuid4())
            shortlink = self.generate_shortlink(random_seq)
        self.shortlink = shortlink

    def add_url_to_db(self):
        db.session.add(self)
        db.session.commit()



class ReverseUrl(object):
    def __init__(self, shortlink):
        self.shortlink = shortlink

    def get_source_url(self):
        shortlink = self.shortlink
        source_url = Url.query.get(shortener.decode_id(shortlink))
        if source_url is not None:
            self.id = source_url.id
            self.update_counter()
            source_url = source_url.source
        self.source = source_url

    def update_counter(self):
        rec = Url.query.get(self.id)
        rec.counter = rec.counter + 1
        db.session.commit()

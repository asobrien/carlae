##########################
# This is declarative
#
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String
#from app import db
#
#engine = create_engine('sqlite:///database.db', echo=True)
#db_session = scoped_session(sessionmaker(autocommit=False,
#                                         autoflush=False,
#                                         bind=engine))
#Base = declarative_base()
#Base.query = db_session.query_property()
#
# END OF DECLARATIVE
###########################


#----------------------------------------------------------------------------#
# DB Config.
#----------------------------------------------------------------------------#

from app import db

# Set your classes here.

'''
class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password
'''


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username):
        self.username = username
        self.get_user_details()

    def get_user_details(self):
        uname = User.query.filter_by(username=self.username).first()
        if uname is not None:
            for var, val in vars(uname).iteritems():
                setattr(self, var, val)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def create_user(self, email, password):
        user = User(self.username)
        user.email = email
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

    def authenticate_user(self, password):
        self.logged_in = bcrypt.check_password_hash(self.password, password)

    def change_password(self, password):
        user = User.query.get(self.id)
        user.password = bcrypt.generate_password_hash(password)  # update pass
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username



class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(1500), unique=True, nullable=False)
    shortlink = db.Column(db.String(6), unique=True, nullable=False)
    counter = db.Column(db.Integer, default=0)

    def __init__(self, source_url):
        self.source = self.cleanup_url(source_url)
        self.shortlink = self.generate_shortlink(self.source)
        self._make_shortlink_unique()  # short links need to unique so let's ensure this


    def generate_shortlink(self, source_url):
        url_digest = md5(source_url).digest()
        encode = base64.urlsafe_b64encode(url_digest)
        return encode[0:7]

    def cleanup_url(self, source_url):
        source_url = self.check_protocol(source_url)
        return urlparse.urlsplit(source_url).geturl()

    def is_valid_link(self):
        """Checks whether `source_url` is valid."""
        pass

    def check_protocol(self, url):
        return url if "://" in url else "http://" + url

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
        source_url = Url.query.filter_by(shortlink=shortlink).first()
        if source_url is not None:
            self.id = source_url.id
            self.update_counter()
            source_url = source_url.source
        self.source = source_url

    def update_counter(self):
        rec = Url.query.get(self.id)
        rec.counter = rec.counter + 1
        db.session.commit()








# Create tables.
#Base.metadata.create_all(bind=engine)

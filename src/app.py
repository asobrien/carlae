#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#

from flask import *  # do not use '*'; actually input the dependencies.
from flask import flash, redirect, Markup
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask_reggie import Reggie  # Regex Routing
import logging
from logging import Formatter, FileHandler
from forms import *
from werkzeug.routing import BaseConverter  # for regex urls
import os
import config

# app specific
#import models
#from forms import UrlForm
import models

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
Reggie(app)

# Automatically tear down SQLAlchemy.
# not needed with Flask-SqlAlchemy?
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

# prevent resubmission of form

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    login_form = LoginForm(request.form)
    url_form = UrlForm(request.form)

    if request.method == 'POST':
        url = models.Url(request.form['url'])
        url_key = '@' + url.shortlink
        short_url = os.path.join(config.BASE_URL, url_key)
        # build short_url as link & stylize here
        url_out = "<h2 class='text-center'><a href='%s'>%s</a></h2>" % (short_url, short_url)

        flash(Markup(url_out), 'alert-success')
        return redirect(url_for('home'))

    return render_template('pages/index.html', login_form=login_form, url_form=url_form)

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)

@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form = form)

@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form = form)

# Shortlink Handler

@app.route('/<regex("[@,%40][0-9a-zA-Z]{7}"):shorturl>')
def example(shorturl):
    shorturl = shorturl.lstrip('@')
    url = models.ReverseUrl(shorturl)
    url.get_source_url()
    if url.source is not None:
        return redirect(url.source, code=301)  # permanent redirect
    return render_template('errors/404.html'), 404  # shortlink not found


# Raw DataBase Dump
@app.route('/rawdump')
def rawdump():
    urls =  models.Url.query.all()
    raw = ["shortlink, source_url"]
    for url in urls:
        raw.append("@%s, %s" %(url.shortlink, url.source))
    raw_string = ('\n').join(raw)
    return Response(raw_string, mimetype="text/plain")

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    models.db.session.rollback()  # rollback db on 500 error
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def internal_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

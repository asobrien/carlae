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
import datetime
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, current_user, login_required

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

login_manager = LoginManager()
login_manager.init_app(app)

# login_manager.login_message_category = "alert-info"

# user_loader callback
@login_manager.user_loader
def load_user(userid):
    return models.User.query.get(userid)

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

@app.route("/logintest")
@login_required
def logintest():
    return "You are logged in! That What this message means."

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():

    login_form = LoginForm(request.form)
    url_form = UrlForm(request.form)

    if login_form.validate_on_submit():
        # login and validate the user...

        # set the boolean checkbox
        # http://nesv.blogspot.com/2011/10/flask-gotcha-with-html-forms-checkboxes.html
        remember_me = False
        if 'remember' in request.form:
            remember_me = True


        return '%s' % remember_me
        user = models.User(request.form['email'])
        if user is None:
            flash("Email address is incorrect.", "alert-danger")
            return redirect(url_for('home'))

        login_user(user, remember=remember_me)
        flash("Logged in successfully.", "alert-success")
        return redirect(request.args.get("next") or url_for("home"))
    return render_template("pages/index.html", login_form=login_form)

    # if request.method == 'POST':
    #     url = models.Url(request.form['url'])
    #     url_key = '@' + url.shortlink
    #     short_url = os.path.join(config.BASE_URL, url_key)
    #     # build short_url as link & stylize here
    #     url_out = "<h2 class='text-center'><a href='%s'>%s</a></h2>" % (short_url, short_url)
    #
    #     flash(Markup(url_out), 'alert-success')
    #     return redirect(url_for('home'))
    #
    # return render_template('pages/index.html', login_form=login_form, url_form=url_form)

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':

        user = models.User(request.form['name'])
        password = user.generate_password()
        user.create_user(request.form['email'], password)
        message = "User: %s\nPassword: %s" % (user.username, password)
        flash(message, category="alert-info")
        return redirect(url_for('home'))
    return render_template('forms/register.html', form = form)


@app.route('/invite', methods=['GET', 'POST'])
def invite():
    form = InviteUserForm(request.form)
    if request.method == 'POST':
        user = models.InviteUser(request.form['email'])
        if user.is_activated:
            message = Markup("<b>%s</b> has already activated an account" % user.email)
            flash(message, category='alert-danger')
            return redirect(url_for('invite'))
        try:
            mailgun = user.send_activation_email()
        except:
            message = Markup("There was an error sending an invitation to <b>%s</b>. Go ahead and try sending another invite." % user.email)
            flash(message, category='alert-danger')
            return redirect(url_for('invite'))
        if mailgun.status_code != 200:
            message = Markup("There was an error sending an invitation to <b>%s</b>. Go ahead and try sending another invite." % user.email)
            flash(message, category='alert-danger')
            return redirect(url_for('invite'))
        
        message = Markup("An invitation email has been sent to <b>%s</b>" % user.email)
        flash(message, category='alert-success')
        return redirect(url_for('invite'))

    return render_template('forms/invite.html', form = form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form = form)

@app.route('/activate', methods=['GET', 'POST'])
def activate():
    email = request.args.get('email')
    code = request.args.get('code')

    check_code = models.InviteUser.query.filter_by(activation_code=code).first()
    check_email = models.InviteUser.query.filter_by(email=email).first()
    check = check_email


    # Email & code must be in database
    if check_code is None or check_email is None:
        flash(Markup("<b>Invalid activation code</b>. Please request a new invitation."),
              category='alert-danger')
        return redirect(url_for('home'))
    else:
        check_code = check_code.activation_code
        check_email = check_email.email
    # Activation & email must match db values
    if not (check.activation_code==code) and (check_email==email):
        flash(Markup("<b>Invalid activation code</b>. Please request a new invitation."),
              category='alert-danger')
        return redirect(url_for('home'))

    # Activation must not be expired
    elapsed_time = datetime.datetime.now() - check.activation_date
    if elapsed_time > datetime.timedelta(weeks=2):
        # TODO: Set config with activation expiration option, currently 2 weeks.
        flash(Markup("<b>Expired activation code</b>. Please request a new invitation."),
              category='alert-danger')
        return redirect(url_for('home'))

    # Activate the form
    form = ActivateUserForm(request.form)
    if form.validate_on_submit():
        # now we create the new user
        usr = models.User(email)
        usr.create_user(request.form['password'])
        # change activation status
        inv = models.InviteUser.query.get(check.id)
        inv.is_activated = True
        models.db.session.commit()
        message = Markup("<b>%s</b> has been successfully activated. You're good to go!" % usr.email)
        flash(Markup(message), 'alert-success')
        return redirect(url_for('home'))
    return render_template('forms/activate.html', form=form, email=email)

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

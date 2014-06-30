#!/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#

# from flask import *  # do not use '*'; actually input the dependencies.
from flask import Flask, flash, redirect, Markup, g, render_template, request, url_for, Response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask_reggie import Reggie  # Regex Routing
import logging
from logging import Formatter, FileHandler
from forms import *
import os

import datetime
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, login_required, current_user, fresh_login_required

# app specific
import models
# import config
from carlae import config




#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('carlae.config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
Reggie(app)

login_manager = LoginManager()
login_manager.init_app(app)

# login manager settings.
login_manager.refresh_view = "login"
login_manager.needs_refresh_message = (
    u"To protect your account, please reauthenticate to access this page.")
login_manager.needs_refresh_message_category = "alert-info"

# user_loader callback
@login_manager.user_loader
def load_user(userid):
    return models.User.query.get(userid)

# @app.teardown_request
# def shutdown_session(exception=None):
#     db_session.remove()




#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.before_request
def before_request():
    g.user = current_user

if config.DEMO_MODE:
    @app.route('/')
    def index():
        return redirect(url_for('home'))


@app.route('/+', methods=['GET', 'POST'])
def home():
    # Display the URL shortcode form if there is authenticated user
    if g.user.is_authenticated():
        url_form = UrlForm(request.form)
        if url_form.validate_on_submit():
            url = models.Url(request.form['url'])
            url_key = '+' + url.shortlink
            short_url = os.path.join(config.BASE_URL, url_key)
            # build short_url as link & stylize here
            url_out = "<h3 class='text-center'>Here's your shortlink:</h3>" \
                      "<h2 class='text-center'><a class='alert-link' href='%s'>%s</a></h2>" % (short_url, short_url)
            flash(Markup(url_out), 'alert-success')
            return redirect(url_for('home'))
        return render_template("pages/index.html", form=url_form)
    else:
        login_form = LoginForm(request.form)
        if login_form.validate_on_submit():
            # login and validate the user...
            # set the boolean checkbox
            # http://nesv.blogspot.com/2011/10/flask-gotcha-with-html-forms-checkboxes.html
            remember_me = False
            if 'remember' in request.form:
                remember_me = True
            user = models.User(request.form['email'])
            login_user(user, remember=remember_me)
            return redirect(request.args.get("next") or url_for("home"))
        return render_template("pages/index.html", form=login_form)


# in case we need a fresh login
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if login_form.validate_on_submit():
        # login and validate the user...
        # set the boolean checkbox
        # http://nesv.blogspot.com/2011/10/flask-gotcha-with-html-forms-checkboxes.html
        remember_me = False
        if 'remember' in request.form:
            remember_me = True
        user = models.User(request.form['email'])
        login_user(user, remember=remember_me)
        return redirect(request.args.get("next") or url_for("home"))
    return render_template('forms/login.html', form=login_form)


@app.route("/logout")
@login_required
def logout():
    logout_user()  # logouts out user, deletes cookies, etc.
    return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('pages/about.html')


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
            message = Markup("There was an error sending an invitation to <b>%s</b>. Go ahead and try sending another invite."
                             % user.email)
            flash(message, category='alert-danger')
            return redirect(url_for('invite'))
        if mailgun.status_code != 200:
            message = Markup("There was an error sending an invitation to <b>%s</b>. Go ahead and try sending another invite."
                             % user.email)
            flash(message, category='alert-danger')
            return redirect(url_for('invite'))
        
        message = Markup("An invitation email has been sent to <b>%s</b>" % user.email)
        flash(message, category='alert-success')
        return redirect(url_for('invite'))

    return render_template('forms/invite.html', form = form)


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


### Shortlink Handler ###

@app.route('/<regex("[\+][0-9a-zA-Z]{6}"):shorturl>')
def example(shorturl):
    shorturl = shorturl.lstrip('+')
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
        raw.append("+%s, %s" %(url.shortlink, url.source))
    raw_string = ('\n').join(raw)
    return Response(raw_string, mimetype="text/plain")


@app.route('/top10')
def top10():
    top_urls = models.Url.query.order_by(models.Url.counter.desc()).limit(10).all()
    return render_template('pages/top10.html', urls=top_urls)


@app.route('/changepassword', methods=['GET', 'POST'])
@fresh_login_required
def changepassword():
    pass_form = ActivateUserForm(request.form)
    if pass_form.validate_on_submit():
        user = g.user
        user.change_password(request.form['password'])
        flash("Your password has been successfully changed!", 'alert-success')
        return redirect(url_for('home'))
    return render_template('forms/changepass.html', form=pass_form)


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
    app.run(host='0.0.0.0')

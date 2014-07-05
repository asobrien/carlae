#! /var/www/carlae/venv/bin/python

"""This script resets carlae.
"""

# Dependencies
import subprocess
import os
import sys

# Settings
APP_ROOT = "/var/www/carlae/"
DATABASE_FILE = "database.db"
DEMO_USER = "demo@carlae.com"
DEMO_PASSWORD = "shortenIT"

sys.path.append(APP_ROOT)

# Shutdown uWSGI
subprocess.call("stop uwsgi", shell=True)

# Remove the database
DB = os.path.join(APP_ROOT, DATABASE_FILE)
subprocess.call("rm -f %s" % DB, shell=True)

# Now recreate db
import setup  # how to import from project
setup.create_db()
setup.create_user(DEMO_USER, DEMO_PASSWORD)
subprocess.call("chown www-data:www-data %s" % DB, shell=True)

# Restart uWSGI
subprocess.call("start uwsgi", shell=True)

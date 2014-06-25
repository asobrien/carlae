__author__ = 'aobrien'

"""This script sets ups and activates the virtualenv.
"""

import subprocess

# Create venv
subprocess.call("virtualenv venv", shell=True)
# Unless you have a conda installation!
# then you need to do something else

# Activate virtual env
subprocess.call(". venv/bin/activate")


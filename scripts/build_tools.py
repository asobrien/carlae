# -*- coding: utf-8 -*-

__author__ = 'aobrien'

import subprocess
import os
from binascii import b2a_base64

# GIT FUNCTIONS
def get_git_branch_name():
    return subprocess.check_output(["git",
                                    "rev-parse",
                                    "--abbrev-ref",
                                    "HEAD"]).strip()

def get_git_commit_hash(short=True):
    if short:
        VER = subprocess.check_output(["git",
                                       "rev-parse",
                                       "--short",
                                       "HEAD"]).strip()
    else:
        VER = subprocess.check_output(["git",
                                       "rev-parse",
                                       "HEAD"]).strip()
    return VER

def get_git_latest_tag():
    return subprocess.check_output(["git",
                                    "describe",
                                    "--abbrev=0",
                                    "--tags"]).strip().lstrip('v')
# Others
def generate_secret_key(length=35):
    """Generate a random key in base64 encoding."""
    return b2a_base64(os.urandom(length)).strip()

# GIT INFO
GIT_BRANCH_NAME = get_git_branch_name()
GIT_COMMIT_HASH = get_git_commit_hash()
GIT_VERSION_TAG = get_git_latest_tag()

# Others
SECRET_KEY = generate_secret_key()

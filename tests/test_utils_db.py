# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'aobrien'

from carlae.utils import db

def test_create_user():
    # Add the user
    email = "user2@example.com"
    password = "1234567890"
    db.create_user(email, password)
    user = db.User(email)
    assert user.email == email


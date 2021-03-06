# -*- coding: utf-8 -*-

__author__ = 'aobrien'

"""This module incorporates email sending using mailgun."""

import os
import requests
import config

# Enter the domain associated with your Mailgun account here
DOMAIN = os.getenv('MAILGUN_DOMAIN')

# Enter your Mailgun API Key here
API_KEY = os.getenv('MAILGUN_API_KEY')

def send_simple_message(from_email, to_list, subject, message, from_name=None):
    """
    Parameters
    ----------
    from_email : str
        A string specify the email address of sender (e.g., 'admin@example.com').
    to_list : list of strings
        A list of strings containing recipient email addresses.
    subject : str
        A string specifying subject.
    message : str
        A string containing the body of the email.
    from_name: str (optional)
        A string specifying the name of the sender.
    """
    FROM_FIELD = build_sender(from_email, from_name)
    return requests.post(
        "https://api.mailgun.net/v2/%s/messages" % DOMAIN,
        auth=("api", API_KEY),
        data={"from": FROM_FIELD,
              "to": to_list,
              "subject": subject,
              "text": message})


def build_sender(from_email, from_name):
    if from_name is None:
        return from_email
    else:
        return "%s <%s>" % (from_name, from_email)

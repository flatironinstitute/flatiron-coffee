# -*- coding: utf-8 -*-

__all__ = ["send_message"]

import requests


def send_message(config, emails, message, subject=None):
    if subject is None:
        subject = "Flatiron coffee"
    if config["debug"]:
        emails = ["foreman.mackey@gmail.com"]
        subject = "[TEST] " + subject
    url = "https://api.mailgun.net/v3/{0}/messages".format(
        config["mailgun_domain"]
    )
    auth = ("api", config["mailgun_api_key"])
    data = {
        "from": config["sender_email"],
        "to": emails,
        "subject": subject,
        "text": message,
    }
    return requests.post(url, auth=auth, data=data)

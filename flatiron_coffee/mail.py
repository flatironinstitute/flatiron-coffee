# -*- coding: utf-8 -*-

__all__ = ["send_message"]

import requests

from .config import get_config


def send_message(emails, message):
    config = get_config()
    url = "https://api.mailgun.net/v3/{0}/messages".format(
        config["mailgun_domain"])
    auth = ("api", config["mailgun_api_key"])
    data = {
        "from": config["sender_email"],
        "to": emails,
        "subject": "Flatiron coffee",
        "text": message,
    }
    return requests.post(url, auth=auth, data=data)

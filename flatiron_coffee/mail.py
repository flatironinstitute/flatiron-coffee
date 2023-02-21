# -*- coding: utf-8 -*-

__all__ = ["send_message"]

from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

import requests

def send_message(config, emails, message, subject=None):
    if "mailgun_api_key" in config:
        return send_message_api(config, emails, message, subject=subject)
    else:
        return send_message_smtp(config, emails, message, subject=subject)


def send_message_api(config, emails, message, subject=None):
    if subject is None:
        subject = config.get("email_subject", "Flatiron coffee")
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


def send_message_smtp(config, emails, message, subject=None):
    smtp_user = config["mailgun_smtp_user"]
    smtp_pass = config["mailgun_smtp_password"]
    smtp_host = "smtp.mailgun.org"
    smtp_port = 465
    if subject is None:
        subject = config.get("email_subject", "Flatiron coffee")
    if config["debug"]:
        subject = "[TEST] " + subject

    msg = MIMEText(message, "plain")
    msg["Subject"] = subject
    msg["From"] = config["sender_email"]
    msg["To"] = ",".join(emails)
    msg["Reply-To"] = ",".join(emails)

    with SMTP(smtp_host, port=smtp_port) as conn:
        conn.set_debuglevel(False)
        conn.login(smtp_user, smtp_pass)
        conn.sendmail(config["sender_email"], emails, msg.as_string())

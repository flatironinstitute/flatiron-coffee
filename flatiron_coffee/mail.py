# -*- coding: utf-8 -*-

import time
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

import requests

class Email:
    def __init__(self, config):
        self.config = config
    
    def __enter__(self):
        if "mailgun_api_key" in self.config:
            self.smtp_conn = None
        else:
            smtp_user = self.config["mailgun_smtp_user"]
            smtp_pass = self.config["mailgun_smtp_password"]
            smtp_host = "smtp.mailgun.org"
            smtp_port = 465
            self.smtp_conn = SMTP(smtp_host, port=smtp_port)
            self.smtp_conn.set_debuglevel(False)
            self.smtp_conn.login(smtp_user, smtp_pass)
        return self
    
    def __exit__(self, *_):
        if self.smtp_conn is not None:
            self.smtp_conn.quit()

    def send_message(self, emails, message, subject=None):
        if "mailgun_api_key" in self.config:
            return self.send_message_api(emails, message, subject=subject)
        else:
            return self.send_message_smtp(emails, message, subject=subject)

    def send_message_api(self, emails, message, subject=None):
        if subject is None:
            subject = self.config.get("email_subject", "Flatiron coffee")
        if self.config["debug"]:
            emails = ["foreman.mackey@gmail.com"]
            subject = "[TEST] " + subject
        url = "https://api.mailgun.net/v3/{0}/messages".format(
            self.config["mailgun_domain"]
        )
        auth = ("api", self.config["mailgun_api_key"])
        data = {
            "from": self.config["sender_email"],
            "to": emails,
            "subject": subject,
            "text": message,
        }
        return requests.post(url, auth=auth, data=data)

    def send_message_smtp(self, emails, message, subject=None):
        if subject is None:
            subject = self.config.get("email_subject", "Flatiron coffee")
        if self.config["debug"]:
            subject = "[TEST] " + subject

        print(f"Sending email to {', '.join(emails)}...")

        msg = MIMEText(message, "plain")
        msg["Subject"] = subject
        msg["From"] = self.config["sender_email"]
        msg["To"] = ",".join(emails)
        msg["Reply-To"] = ",".join(emails)

        for _ in range(3):
            try:
                self.smtp_conn.sendmail(self.config["sender_email"], emails, msg.as_string())

            except Exception as e:
                print(f"... Failed: {e}.")
                print("Retrying after 1 second.")
                time.sleep(1)

            else:
                break

        print("... Sent.")

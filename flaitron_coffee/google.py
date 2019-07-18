# -*- coding: utf-8 -*-

__all__ = ["get_sheet", "send_invite"]

import os
import base64
import pickle
import pandas as pd
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from .config import get_config

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


def get_creds():
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


def get_sheet(sheet_id, sheet_name):
    """Load a Google Sheet as a pandas DataFrame

    Args:
        sheet_id (str): The ID of the sheet
        sheet_name (str): The name of the sheet

    Returns:
        DataFrame: The sheet formatted as a pandas DataFrame

    """
    service = build("sheets", "v4", credentials=get_creds())
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=sheet_name).execute()
    values = result.get("values", [])
    return pd.DataFrame(data=values[1:], columns=values[0])


def send_message(service, user_id, message):
    message = service.users().messages().send(
        userId=user_id, body=message).execute()
    return message


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    return {"raw": base64.urlsafe_b64encode(
        message.as_string().encode("utf-8")).decode("utf-8")}


def send_invite(name1, email1, name2, email2):
    """Send an invitation email connecting two emails

    Args:
        name1 (str): The name of the first user
        email1 (str): The email of the first user
        name2 (str): The name of the second user
        email2 (str): The email of the second user

    """
    service = build("gmail", "v1", credentials=get_creds())

    sender = get_config()["sender_email"]
    to = "{0} <{1}>, {2} <{3}>".format(name1, email1, name2, email2)
    subject = "Random coffee"
    message_text = "This is a test."
    message = create_message(sender, to, subject, message_text)

    send_message(service, "me", message)

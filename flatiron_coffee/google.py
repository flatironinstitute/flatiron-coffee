# -*- coding: utf-8 -*-

__all__ = ["get_sheet"]

import os
import pickle
import pandas as pd

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


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
                "credentials.json", SCOPES
            )
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
    result = (
        sheet.values().get(spreadsheetId=sheet_id, range=sheet_name).execute()
    )
    values = result.get("values", [])
    return pd.DataFrame(data=values[1:], columns=values[0])

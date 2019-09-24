# -*- coding: utf-8 -*-

__all__ = ["get_sheet"]

import pandas as pd

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_creds(config):
    return service_account.Credentials.from_service_account_file(
        config["cred_file"], scopes=SCOPES
    )


def get_service(config):
    return build("sheets", "v4", credentials=get_creds(config)).spreadsheets()


def get_sheet(config):
    values = (
        get_service(config)
        .values()
        .get(spreadsheetId=config["sheet_id"], range=config["sheet_name"])
        .execute()
        .get("values", [])
    )
    return pd.DataFrame(data=values[1:], columns=values[0])

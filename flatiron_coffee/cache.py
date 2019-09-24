# -*- coding: utf-8 -*-

__all__ = ["save_pairs", "get_all_previous_pairs"]

from .google import get_service


def save_pairs(config, pairs):
    service = get_service(config)
    body = dict(values=[list(sorted(pair)) for pair in pairs])
    service.values().append(
        spreadsheetId=config["sheet_id"],
        range=config["cache_name"],
        body=body,
        valueInputOption="RAW",
    ).execute()


def get_all_previous_pairs(config):
    return (
        get_service(config)
        .values()
        .get(spreadsheetId=config["sheet_id"], range=config["cache_name"])
        .execute()
        .get("values", [])
    )

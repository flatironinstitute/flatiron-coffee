# -*- coding: utf-8 -*-

__all__ = ["find_matches"]

import random
import pkg_resources

from .config import get_config
from . import cache, google, pair, mail


def find_matches():
    config = get_config()
    previous = cache.get_all_previous_pairs()
    sheet = google.get_sheet(config["sheet_id"], config["sheet_name"])
    email_map = dict(zip(sheet["Email Address"], sheet.index))
    emails = list(email_map.keys())
    random.shuffle(emails)
    matches, unmatched = pair.find_pairs(emails, previous)

    matched_temp = pkg_resources.resource_string(
        "flatiron_coffee", "templates/matched.txt"
    ).decode("utf-8")
    unmatched_temp = pkg_resources.resource_string(
        "flatiron_coffee", "templates/unmatched.txt"
    ).decode("utf-8")

    for match in matches:
        email1, email2 = match
        name1 = sheet.loc[email_map[email1]]["Preferred name"]
        name2 = sheet.loc[email_map[email2]]["Preferred name"]
        txt = matched_temp.replace("{{ name1 }}", name1).replace(
            "{{ name2 }}", name2
        )
        mail.send_message([email1, email2], txt)
        cache.save_pair(*match)

    for email in unmatched:
        name = sheet.loc[email_map[email]]["Preferred name"]
        txt = unmatched_temp.replace("{{ name }}", name)
        mail.send_message([email], txt)

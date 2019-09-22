# -*- coding: utf-8 -*-

__all__ = ["find_matches"]

import random
import pkg_resources
from datetime import date

from .config import get_config
from . import cache, google, pair, mail


def find_matches(dry_run=True):
    config = get_config()
    previous = cache.get_all_previous_pairs()

    # Get the list of sign ups
    sheet = google.get_sheet(config["sheet_id"], config["sheet_name"])

    # Remove those who have opted out
    sheet = sheet[sheet["Opt in"] == "Yes"]

    # A map between emails and IDs
    email_map = dict(zip(sheet["Email Address"], sheet.index))
    emails = list(email_map.keys())

    # Seed with the date
    today = date.today()
    random.seed(int("{0.year:04d}{0.month:02d}{0.day:02d}".format(today)))

    # Find the matches
    matches, unmatched = pair.find_pairs(emails, previous, shuffle=True)

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
        if not dry_run:
            mail.send_message([email1, email2], txt)
            if not config["debug"]:
                cache.save_pair(*match)
        else:
            print("Match: {0} {1}".format(email1, email2))

    for email in unmatched:
        name = sheet.loc[email_map[email]]["Preferred name"]
        txt = unmatched_temp.replace("{{ name }}", name)
        if not dry_run:
            mail.send_message([email], txt)
        else:
            print("Unmatched: {0} {1}".format(email1, email2))

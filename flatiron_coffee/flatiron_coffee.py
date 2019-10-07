# -*- coding: utf-8 -*-

__all__ = ["find_matches"]

import random
import textwrap
import pkg_resources
from datetime import date

from .config import get_config
from . import cache, google, pair, mail


def _load_and_wrap(config, filename):
    txt = (
        pkg_resources.resource_string("flatiron_coffee", filename)
        .decode("utf-8")
        .format(**config)
    )
    return "\n\n".join(
        ["\n".join(textwrap.wrap(par, width=79)) for par in txt.split("\n\n")]
    )


def find_matches(dry_run=True):
    config = get_config()
    if dry_run:
        config["debug"] = True
    previous = cache.get_all_previous_pairs(config)

    # Get the list of sign ups
    sheet = google.get_sheet(config)

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

    # Send the summary to the admin
    admin_email = config.get("admin_email", None)
    if admin_email is not None:
        msg = "Matched:\n\n"
        msg += "\n".join(map("{0[0]}, {0[1]}".format, matches))
        msg += "\n\nUnmatched:\n\n"
        msg += "\n".join(unmatched)
        mail.send_message(config, [admin_email], msg)

    # Load the templates
    matched_temp = _load_and_wrap(config, "templates/matched.txt")
    unmatched_temp = _load_and_wrap(config, "templates/unmatched.txt")

    for match in matches:
        email1, email2 = match
        name1 = sheet.loc[email_map[email1]]["Preferred name"]
        name2 = sheet.loc[email_map[email2]]["Preferred name"]
        txt = matched_temp.format(name1=name1, name2=name2)
        if not config["debug"]:
            mail.send_message(config, [email1, email2], txt)
        else:
            print("Match: {0} {1}".format(email1, email2))

    if not config["debug"]:
        cache.save_pairs(config, matches)

    for email in unmatched:
        name = sheet.loc[email_map[email]]["Preferred name"]
        txt = unmatched_temp.format(name=name)
        if not config["debug"]:
            mail.send_message(config, [email], txt)
        else:
            print("Unmatched: {0}".format(email))

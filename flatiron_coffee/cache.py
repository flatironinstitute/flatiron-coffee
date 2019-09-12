# -*- coding: utf-8 -*-

import os
import sqlite3

CACHE_FILENAME = "pairs.db"


def save_pair(email1, email2):
    email1, email2 = sorted((email1, email2))
    key = email1 + " : " + email2

    with sqlite3.connect(CACHE_FILENAME) as conn:
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS pairs "
            "(key TEXT PRIMARY KEY, email1 TEXT, email2 TEXT)"
        )
        c.execute(
            "INSERT OR REPLACE INTO pairs (key, email1, email2) "
            "VALUES (?, ?, ?)",
            (key, email1, email2),
        )


def get_all_previous_pairs():
    if not os.path.exists(CACHE_FILENAME):
        return []
    with sqlite3.connect(CACHE_FILENAME) as conn:
        c = conn.cursor()
        c.execute("SELECT email1, email2 FROM pairs")
        return c.fetchall()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from flatiron_coffee import find_matches

parser = argparse.ArgumentParser()
parser.add_argument("site", help="the site name")
parser.add_argument("--send", action="store_true", help="send the emails")
args = parser.parse_args()

dry_run = True
if args.send:
    dry_run = False

find_matches(args.site, dry_run)

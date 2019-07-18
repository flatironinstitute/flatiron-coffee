#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["get_config"]

import yaml


def get_config(filename="config.yaml"):
    with open(filename, "r") as f:
        return yaml.safe_load(f)
# -*- coding: utf-8 -*-

from .pair import find_pairs


def test_no_matches():
    emails = ["email{0}".format(i) for i in range(3)]
    previous_pairs = {
        (emails[0], emails[1]),
        (emails[0], emails[2]),
        (emails[1], emails[2]),
    }
    graph = set(find_pairs(emails, previous_pairs))
    assert len(graph & previous_pairs) == 0

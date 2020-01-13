# -*- coding: utf-8 -*-

__all__ = ["find_pairs"]

import random
import itertools
import networkx as nx


def find_pairs(emails, previous_pairs, shuffle=False, group_map=None):
    """Find a set of pairings that have not previously been suggested

    This implementation is based closely on the implementation from the MIT
    licensed "Yelp Beans" project (https://github.com/Yelp/beans). Their
    implementation lives in ``yelp_beans/matching/pair_match.py``. The heavy
    lifting is done by networkx using the "Blossom" algorithm.

    Args:
        emails (list): A list of all the email addresses to match
        previous_pairs (list): A list of tuples containing preiovsly assigned
        pairs

    Returns:
        list: A list of tuples defining pairs

    """
    if group_map is None:
        group_map = dict()

    # Construct the set of all possible meetings
    possible_meetings = {
        tuple(sorted(meeting)) for meeting in itertools.combinations(emails, 2)
    }

    # Remove previous pairings
    meetings = possible_meetings - set(
        tuple(sorted(p)) for p in previous_pairs
    )

    # Set things up for networkx
    # w = ({"weight": 1.0},)
    # meetings = [m + w for m in sorted(meetings)]
    edges = []
    for meeting in meetings:
        k1 = group_map.get(meeting[0], "unknown")
        k2 = group_map.get(meeting[1], "unknown")
        if k1 == k2:
            edges.append((meeting[0], meeting[1], {"weight": 0.1}))
        else:
            edges.append((meeting[0], meeting[1], {"weight": 1.0}))
    if shuffle:
        random.shuffle(edges)

    # Build the graph
    graph = nx.Graph()
    graph.add_nodes_from(emails)
    graph.add_edges_from(edges)

    # Use https://en.wikipedia.org/wiki/Blossom_algorithm to find the maximal
    # matching
    matches = list(tuple(sorted(p)) for p in nx.max_weight_matching(graph))

    # Find the unmatched emails
    all_matched = set(e for pair in matches for e in pair)
    unmatched = [e for e in emails if e not in all_matched]

    return list(sorted(matches)), list(sorted(unmatched))

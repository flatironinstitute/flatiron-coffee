# -*- coding: utf-8 -*-

__all__ = ["find_pairs"]

import itertools
import networkx as nx


def find_pairs(emails, previous_pairs):
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

    # Construct the set of all possible meetings
    possible_meetings = {
        tuple(sorted(meeting)) for meeting in itertools.combinations(emails, 2)
    }

    # Remove previous pairings
    meetings = possible_meetings - set(
        tuple(sorted(p)) for p in previous_pairs
    )

    # Set things up for networkx
    w = ({"weight": 1.0},)
    meetings = [m + w for m in meetings]

    # Build the graph
    graph = nx.Graph()
    graph.add_nodes_from(emails)
    graph.add_edges_from(meetings)

    # Use https://en.wikipedia.org/wiki/Blossom_algorithm to find the maximal
    # matching
    matches = list(tuple(sorted(p)) for p in nx.max_weight_matching(graph))

    # Find the unmatched emails
    all_matched = set(e for pair in matches for e in pair)
    unmatched = [e for e in emails if e not in all_matched]

    return matches, unmatched

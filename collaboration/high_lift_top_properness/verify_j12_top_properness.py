#!/usr/bin/env python3
"""Sanity control for automatic j=12 -> j=13 top-properness.

This constructs one proper 17-edge-colouring of K17 and checks the exact
missing-colour count in Theorem 1.  The theorem itself is parameter-free
at order 17 and does not depend on this example.
"""

from __future__ import annotations

import itertools
from collections import Counter


def main():
    order = 17
    vertices = tuple(range(order))
    inverse_two = pow(2, -1, order)
    colouring = {
        edge: (sum(edge) * inverse_two) % order
        for edge in itertools.combinations(vertices, 2)
    }

    missing = {}
    for vertex in vertices:
        incident = {
            colour
            for edge, colour in colouring.items()
            if vertex in edge
        }
        assert len(incident) == order - 1
        absent = set(range(order)) - incident
        assert len(absent) == 1
        missing[vertex] = next(iter(absent))

    assert len(set(missing.values())) == order
    assert missing == {vertex: vertex for vertex in vertices}

    class_sizes = Counter(colouring.values())
    assert class_sizes == Counter({colour: 8 for colour in vertices})
    missing_counts = {
        colour: order - 2 * class_sizes[colour]
        for colour in vertices
    }
    assert missing_counts == {colour: 1 for colour in vertices}
    assert sum(missing_counts.values()) == order

    print(
        "cyclic K17 control:",
        "136 edges, 17 matching classes of size 8,",
        "one distinct missing colour per vertex: PASS",
    )
    print(
        "scope: sanity control for the proved j=12 implication only; "
        "no lower-level or #835 conclusion"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Audit the prescribed-link LSTS(19) boundary for every golf-square pair.

This checker does not solve a completion problem.  It independently verifies
the exact partial triple colouring and all incidence counts used in
``radius5_large_set_equivalence.md``.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parents[1]
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))
from global_latin_audit import construct_golf17


COLORS = tuple(range(17))
SQUARES = tuple(range(15))
MOVING = tuple(range(17))
A, B = 17, 18
ALL_POINTS = MOVING + (A, B)


def translate(subset: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return tuple(sorted((x + amount) % 17 for x in subset))


def triple_representatives() -> list[tuple[int, int, int]]:
    representatives = []
    unseen = set(combinations(MOVING, 3))
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, shift) for shift in MOVING)
        representatives.append(representative)
        for shift in MOVING:
            unseen.discard(translate(representative, shift))
    assert len(representatives) == 40
    return representatives


def difference_class(edge: tuple[int, int]) -> int:
    x, y = edge
    difference = (y - x) % 17
    return min(difference, 17 - difference)


def boundary_for_pair(
    golf: list[list[list[int]]], i: int, j: int
) -> dict[tuple[int, int, int], int]:
    """Return the 289 prescribed triples from equation (5)."""
    boundary: dict[tuple[int, int, int], int] = {}
    for x in MOVING:
        boundary[tuple(sorted((A, B, x)))] = x
    for x, y in combinations(MOVING, 2):
        boundary[tuple(sorted((A, x, y)))] = golf[i][x][y]
        boundary[tuple(sorted((B, x, y)))] = golf[j][x][y]
    assert len(boundary) == 289
    return boundary


def audit_pair(
    golf: list[list[list[int]]], i: int, j: int
) -> dict[str, object]:
    boundary = boundary_for_pair(golf, i, j)
    by_pair_colour: dict[tuple[tuple[int, int], int], list[tuple[int, int, int]]] = (
        defaultdict(list)
    )
    for triple, colour in boundary.items():
        assert colour in COLORS
        for pair in combinations(triple, 2):
            by_pair_colour[pair, colour].append(triple)

    # A partial large set may use each pair at most once in any colour class.
    assert all(len(triples) == 1 for triples in by_pair_colour.values())

    per_colour = Counter(boundary.values())
    assert set(per_colour) == set(COLORS)
    assert set(per_colour.values()) == {17}

    # The boundary completely fills pairs touching A or B.  Every moving pair
    # has exactly the two distinct prescribed link colours and hence exactly
    # fifteen missing colours/third points.
    complete_pairs = moving_pairs = 0
    for pair in combinations(ALL_POINTS, 2):
        used = {
            colour
            for (seen_pair, colour), triples in by_pair_colour.items()
            if seen_pair == pair and triples
        }
        if A in pair or B in pair:
            assert used == set(COLORS)
            complete_pairs += 1
        else:
            x, y = pair
            assert used == {golf[i][x][y], golf[j][x][y]}
            assert len(used) == 2
            moving_pairs += 1
    assert complete_pairs == 35
    assert moving_pairs == 136

    # For each colour, the two prescribed links are disjoint matchings of
    # size eight on the moving 17-set.  Their 16-edge union leaves 120 edges,
    # exactly forty triangles in any completion.
    for colour in COLORS:
        left = {
            (x, y)
            for x, y in combinations(MOVING, 2)
            if golf[i][x][y] == colour
        }
        right = {
            (x, y)
            for x, y in combinations(MOVING, 2)
            if golf[j][x][y] == colour
        }
        assert len(left) == len(right) == 8
        assert left.isdisjoint(right)
        assert len(set(combinations(MOVING, 2)) - left - right) == 120

    return {
        "pair": [i, j],
        "boundary_triples": len(boundary),
        "blocks_per_colour": 17,
        "complete_boundary_pairs": complete_pairs,
        "moving_pairs_with_two_link_colours": moving_pairs,
        "uncoloured_moving_triples": 680,
        "required_completion_blocks_per_colour": 40,
    }


def main() -> None:
    golf = construct_golf17()

    # Recheck the cyclic covariance used by the 40-orbit exact-cover quotient.
    for i in SQUARES:
        for x, y in combinations(MOVING, 2):
            for shift in MOVING:
                lhs = golf[i][(x + shift) % 17][(y + shift) % 17]
                rhs = (golf[i][x][y] + shift) % 17
                assert lhs == rhs

    # Audit the eight-class compact exact-cover reduction.  Translation does
    # not change an edge difference, so these counts are phase-independent.
    representatives = triple_representatives()
    slot_differences = Counter(
        difference_class(edge)
        for triple in representatives
        for edge in combinations(triple, 2)
    )
    assert slot_differences == Counter({difference: 15 for difference in range(1, 9)})
    for i in SQUARES:
        for colour in COLORS:
            matching = [
                edge
                for edge in combinations(MOVING, 2)
                if golf[i][edge[0]][edge[1]] == colour
            ]
            assert len(matching) == 8
            assert {
                difference_class(edge) for edge in matching
            } == set(range(1, 9))

    reports = [audit_pair(golf, i, j) for i, j in combinations(SQUARES, 2)]
    assert len(reports) == 105
    summary = {
        "status": "PASS",
        "golf_square_pairs": len(reports),
        "boundary_triples_per_pair": 289,
        "partial_blocks_per_colour": 17,
        "unknown_triples_per_pair": 680,
        "completion_blocks_per_colour": 40,
        "cyclic_covariance_checks": 15 * 136 * 17,
        "triple_orbit_edge_slots_per_difference": 15,
        "matching_edges_per_difference": 1,
        "scope": (
            "boundary incidence and cyclic quotient only; "
            "no LSTS completion and no shared N table claimed"
        ),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

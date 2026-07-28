#!/usr/bin/env python3
"""Audit finite arithmetic in the solver-free terminal-K7 proof."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product


U = tuple(range(7))
S = tuple(range(5))
NONE = 5


def edge_types(omission: str) -> tuple[tuple[int, ...], ...]:
    """Enumerate (UU, US, Uz, SS, Sz) endpoint solutions."""
    epsilon_u = int(omission == "U")
    epsilon_s = int(omission == "S")
    epsilon_z = int(omission == "z")
    result = []
    for a in range(4):
        for b in range(6):
            for c in range(2):
                for d in range(3):
                    for e in range(2):
                        if 2 * a + b + c != 7 - epsilon_u:
                            continue
                        if b + 2 * d + e != 5 - epsilon_s:
                            continue
                        if c + e != 1 - epsilon_z:
                            continue
                        result.append((a, b, c, d, e))
    return tuple(result)


def verify_type_table() -> None:
    expected = {
        "U": (
            (0, 5, 1, 0, 0),
            (1, 3, 1, 1, 0),
            (1, 4, 0, 0, 1),
            (2, 1, 1, 2, 0),
            (2, 2, 0, 1, 1),
            (3, 0, 0, 2, 1),
        ),
        "S": (
            (1, 4, 1, 0, 0),
            (2, 2, 1, 1, 0),
            (2, 3, 0, 0, 1),
            (3, 0, 1, 2, 0),
            (3, 1, 0, 1, 1),
        ),
        "z": (
            (1, 5, 0, 0, 0),
            (2, 3, 0, 1, 0),
            (3, 1, 0, 2, 0),
        ),
    }
    assert {
        omission: edge_types(omission)
        for omission in ("U", "S", "z")
    } == expected

    d_zero = tuple(
        (omission, row)
        for omission, rows in expected.items()
        for row in rows
        if row[3] == 0 and row[0] == 2
    )
    assert d_zero == (("S", (2, 3, 0, 0, 1)),)

    ordinary_failure = tuple(
        (omission, row)
        for omission, rows in expected.items()
        for row in rows
        if row[0] >= 2 and row[3] == 1
    )
    assert ordinary_failure == (
        ("U", (2, 2, 0, 1, 1)),
        ("S", (2, 2, 1, 1, 0)),
        ("S", (3, 1, 0, 1, 1)),
        ("z", (2, 3, 0, 1, 0)),
    )
    assert all(row[1] >= 1 for _, row in ordinary_failure)
    assert tuple(
        (omission, row)
        for omission, row in ordinary_failure
        if row[1] == 1
    ) == (("S", (3, 1, 0, 1, 1)),)
    print("PASS exact endpoint-type table and exceptional rows")


def bad_pairs(labels: tuple[int, ...]) -> frozenset[tuple[int, int]]:
    result = set()
    for edge in combinations(U, 2):
        remaining = [labels[u] for u in U if u not in edge]
        if len(set(remaining)) == 1 and remaining[0] != NONE:
            result.add(edge)
    return frozenset(result)


def matching_number_at_most_one(
    edges: frozenset[tuple[int, int]],
) -> bool:
    return all(
        set(left) & set(right)
        for left, right in combinations(edges, 2)
    )


def verify_hall_bad_pairs() -> None:
    checked = 0
    for labels in product((*S, NONE), repeat=7):
        # A vertex has at most one missing separator neighbour by design.
        counts = Counter(label for label in labels if label != NONE)
        bad = bad_pairs(labels)
        maximum = max(counts.values(), default=0)
        if maximum <= 4:
            assert not bad
        elif maximum == 5:
            assert len(bad) == 1
        elif maximum == 6:
            assert len(bad) == 6
            assert matching_number_at_most_one(bad)
        elif maximum == 7:
            assert len(bad) == 21
        if maximum < 7:
            assert matching_number_at_most_one(bad)
        checked += 1
    assert checked == 6**7
    print(
        "PASS Hall bad-pair classification for all "
        f"{checked} missing-label assignments"
    )


def perfect_matchings_four() -> tuple[
    tuple[tuple[int, int], tuple[int, int]], ...
]:
    return (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )


def verify_exceptional_distinct_edge() -> None:
    checked = 0
    for distinct_three in permutations(S, 3):
        for central in (*S, NONE):
            labels = (*distinct_three, central)
            for matching in perfect_matchings_four():
                assert any(
                    labels[left] != labels[right]
                    for left, right in matching
                )
                checked += 1
    assert checked == 5 * 4 * 3 * 6 * 3
    print(
        "PASS exceptional four-endpoint matching always has "
        f"a distinct-label edge ({checked} cases)"
    )


def verify_degree_forcing() -> None:
    # Common missing neighbour:
    # four residual U-S' edges + two selected incidences still need unused uz.
    assert 4 + 2 < 7
    assert 4 + 2 + 1 == 7

    # Size-six ordinary fallback:
    # four B edges + one P-internal edge + at most one other selected edge.
    assert 4 + 1 + 1 < 7
    assert 4 + 1 + 1 + 1 == 7

    # Exceptional cross vertex:
    # four B edges + one selected cross edge + one selected internal edge.
    assert 4 + 1 + 1 < 7
    assert 4 + 1 + 1 + 1 == 7
    print("PASS all degree-seven forcing equalities")


def main() -> None:
    verify_type_table()
    verify_hall_bad_pairs()
    verify_exceptional_distinct_edge()
    verify_degree_forcing()
    print("PASS terminal K7 switching arithmetic")
    print("SCOPE: audit aid for the solver-free proof; no optimizer used")


if __name__ == "__main__":
    main()

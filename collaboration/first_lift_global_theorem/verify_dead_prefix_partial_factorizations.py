#!/usr/bin/env python3
"""Verify class-B-prime realizations of three dead-prefix supports."""

from __future__ import annotations

from collections import Counter
from itertools import combinations

from verify_r1_minimum_layer_repair import build_instance
from verify_r3_dead_seven_prefixes import CASES, VERTICES, endpoints


N_COLOURS = 17
OUTSIDE = frozenset(range(13, 18))
ALL_VERTICES = VERTICES | OUTSIDE
PALETTE = frozenset(range(N_COLOURS))
PARTIAL_EDGES = frozenset(
    edge
    for edge in combinations(sorted(ALL_VERTICES), 2)
    if not set(edge) <= VERTICES
)


CERTIFICATES = {
    "r1": {
        "cross": (
            (16, 15, 4, 1, 14),
            (15, 2, 1, 16, 13),
            (13, 16, 14, 5, 3),
            (4, 14, 2, 13, 16),
            (5, 6, 13, 14, 15),
            (14, 13, 3, 15, 6),
            (0, 4, 5, 2, 1),
            (7, 1, 11, 4, 8),
            (1, 7, 9, 11, 2),
            (12, 3, 10, 7, 5),
            (2, 8, 12, 9, 4),
            (10, 5, 15, 8, 12),
            (6, 9, 16, 10, 11),
        ),
        "internal": (
            (0, 1, 11),
            (0, 2, 8),
            (0, 3, 3),
            (0, 4, 9),
            (1, 2, 0),
            (1, 3, 12),
            (1, 4, 10),
            (2, 3, 6),
            (2, 4, 7),
            (3, 4, 0),
        ),
    },
    "C_in_G": {
        "cross": (
            (9, 10, 12, 2, 7),
            (0, 8, 9, 7, 11),
            (8, 7, 10, 11, 9),
            (11, 12, 7, 8, 10),
            (12, 9, 4, 10, 8),
            (7, 11, 8, 12, 3),
            (10, 1, 11, 9, 12),
            (3, 6, 2, 14, 13),
            (2, 0, 15, 13, 1),
            (13, 15, 3, 0, 2),
            (4, 3, 14, 1, 15),
            (1, 2, 0, 3, 4),
            (14, 16, 1, 5, 0),
        ),
        "internal": (
            (0, 1, 5),
            (0, 2, 16),
            (0, 3, 15),
            (0, 4, 6),
            (1, 2, 13),
            (1, 3, 4),
            (1, 4, 14),
            (2, 3, 6),
            (2, 4, 5),
            (3, 4, 16),
        ),
    },
    "D_in_G": {
        "cross": (
            (9, 12, 7, 10, 2),
            (10, 7, 8, 5, 9),
            (7, 9, 11, 3, 8),
            (11, 10, 1, 8, 7),
            (0, 8, 12, 7, 11),
            (8, 6, 9, 11, 10),
            (4, 11, 10, 9, 13),
            (12, 3, 14, 13, 0),
            (1, 13, 3, 2, 15),
            (14, 2, 15, 0, 1),
            (3, 0, 2, 1, 4),
            (2, 14, 0, 15, 12),
            (16, 1, 4, 12, 3),
        ),
        "internal": (
            (0, 1, 15),
            (0, 2, 13),
            (0, 3, 6),
            (0, 4, 5),
            (1, 2, 5),
            (1, 3, 4),
            (1, 4, 16),
            (2, 3, 16),
            (2, 4, 6),
            (3, 4, 14),
        ),
    },
}


def support_instances() -> dict[str, tuple[frozenset[int], ...]]:
    _, r1_selected, r1_remaining = build_instance()
    result = {
        "r1": tuple((*r1_selected, *r1_remaining)),
    }
    for name, case in CASES.items():
        prefix = case["prefix"]
        remaining_complements = case["remaining_complements"]
        assert isinstance(prefix, tuple)
        assert isinstance(remaining_complements, tuple)
        result[name] = (
            *(endpoints(layer) for layer in prefix),
            *(VERTICES - complement for complement in remaining_complements),
        )
    return result


def literal_colouring(
    certificate: dict[str, tuple[tuple[int, ...], ...]],
) -> dict[tuple[int, int], int]:
    cross = certificate["cross"]
    internal = certificate["internal"]
    assert len(cross) == len(VERTICES) == 13
    assert all(len(row) == len(OUTSIDE) == 5 for row in cross)
    assert all(colour in PALETTE for row in cross for colour in row)

    colouring = {
        (vertex, 13 + outside): colour
        for vertex, row in enumerate(cross)
        for outside, colour in enumerate(row)
    }
    expected_internal_pairs = frozenset(combinations(range(5), 2))
    assert len(internal) == 10
    assert frozenset(
        (left, right) for left, right, _ in internal
    ) == expected_internal_pairs
    assert all(colour in PALETTE for _, _, colour in internal)
    colouring.update({
        (13 + left, 13 + right): colour
        for left, right, colour in internal
    })
    assert len(colouring) == 75
    assert frozenset(colouring) == PARTIAL_EDGES
    return colouring


def verify_case(
    name: str,
    supports: tuple[frozenset[int], ...],
    certificate: dict[str, tuple[tuple[int, ...], ...]],
) -> None:
    assert len(supports) == N_COLOURS
    assert all(len(support) in {8, 10, 12} for support in supports)
    assert all(
        sum(vertex in support for support in supports) == 12
        for vertex in VERTICES
    )

    colouring = literal_colouring(certificate)
    by_colour = {
        colour: frozenset(
            edge
            for edge, current_colour in colouring.items()
            if current_colour == colour
        )
        for colour in PALETTE
    }
    assert sum(map(len, by_colour.values())) == 75
    assert frozenset().union(*by_colour.values()) == PARTIAL_EDGES

    # Properness at all eighteen vertices, with full saturation at P.
    for vertex in ALL_VERTICES:
        incident_colours = [
            colour
            for edge, colour in colouring.items()
            if vertex in edge
        ]
        assert len(incident_colours) == len(set(incident_colours))
        if vertex in OUTSIDE:
            assert len(incident_colours) == N_COLOURS
            assert frozenset(incident_colours) == PALETTE
        else:
            assert len(incident_colours) == 5

    # Each partial colour class is a matching saturating P, and the hole
    # vertices it leaves unmatched are exactly its prescribed support.
    for colour, support in enumerate(supports):
        colour_edges = by_colour[colour]
        colour_endpoints = [
            vertex for edge in colour_edges for vertex in edge
        ]
        assert len(colour_endpoints) == len(set(colour_endpoints))
        assert OUTSIDE <= frozenset(colour_endpoints)
        used_hole_vertices = frozenset(colour_endpoints) & VERTICES
        assert VERTICES - used_hole_vertices == support

    missing_multiplicities = Counter(
        len(VERTICES - support) for support in supports
    )
    profile = Counter(map(len, supports))
    assert set(missing_multiplicities) <= {1, 3, 5}
    print(
        f"PASS {name}: proper 17-colouring partitions all 75 "
        "edges of K18-E(K13)"
    )
    print(
        f"PASS {name}: outside vertices saturated; induced profile "
        f"{dict(sorted(profile.items()))}"
    )


def main() -> None:
    supports = support_instances()
    assert set(supports) == set(CERTIFICATES) == {
        "r1",
        "C_in_G",
        "D_in_G",
    }
    for name in ("r1", "C_in_G", "D_in_G"):
        verify_case(name, supports[name], CERTIFICATES[name])
    print("PASS all three dead-prefix support matrices are class-B-prime")
    print("SCOPE: partial-factorization realizations; no fan realization claimed")


if __name__ == "__main__":
    main()

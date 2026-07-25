#!/usr/bin/env python3
"""Verify the finite claims in defect_facet_map_audit.md."""

from __future__ import annotations

from math import comb


Edge = tuple[int, int]
Matching = tuple[Edge, ...]


ZERO: tuple[int, Matching, Matching, Matching] = (
    5,
    (
        (10, 16), (4, 11), (1, 15), (2, 12),
        (3, 8), (9, 13), (6, 7), (0, 14),
    ),
    (
        (4, 9), (5, 14), (1, 11), (12, 15),
        (3, 13), (0, 2), (8, 10), (6, 16),
    ),
    (
        (8, 15), (13, 14), (12, 16), (7, 11),
        (0, 3), (5, 10), (2, 9), (1, 6),
    ),
)
ZERO_UNMATCHED = (5, 7, 4)

ONE: tuple[Matching, Matching, Matching] = (
    (
        (0, 10), (1, 9), (2, 12), (3, 4),
        (5, 13), (6, 14), (7, 16), (8, 15),
    ),
    (
        (0, 6), (1, 8), (2, 13), (3, 12),
        (4, 15), (7, 9), (10, 11), (14, 16),
    ),
    (
        (0, 3), (1, 14), (2, 5), (4, 9),
        (6, 7), (8, 11), (12, 16), (13, 15),
    ),
)
ONE_UNMATCHED = (11, 5, 10)

TWO: tuple[Matching, Matching, Matching] = (
    (
        (7, 15), (10, 13), (5, 6), (1, 16),
        (2, 8), (11, 14), (3, 9), (0, 12),
    ),
    (
        (7, 9), (0, 3), (11, 16), (4, 14),
        (2, 6), (8, 15), (10, 12), (5, 13),
    ),
    (
        (10, 14), (6, 15), (4, 7), (9, 16),
        (3, 12), (11, 13), (2, 5), (1, 8),
    ),
)
TWO_UNMATCHED = (4, 1, 0)

ZERO_COMPLETION: tuple[Matching, ...] = (
    (
        (0, 1), (2, 16), (3, 6), (4, 5), (7, 8),
        (9, 10), (11, 14), (12, 13), (15, 17),
    ),
    (
        (0, 4), (1, 2), (3, 10), (5, 12), (6, 8),
        (7, 16), (9, 11), (13, 15), (14, 17),
    ),
    (
        (0, 5), (1, 4), (2, 3), (6, 9), (7, 15),
        (8, 13), (10, 11), (12, 14), (16, 17),
    ),
    (
        (0, 6), (1, 8), (2, 13), (3, 5), (4, 7),
        (9, 14), (10, 12), (11, 17), (15, 16),
    ),
    (
        (0, 7), (1, 3), (2, 4), (5, 16), (6, 10),
        (8, 17), (9, 12), (11, 13), (14, 15),
    ),
    (
        (0, 8), (1, 10), (2, 6), (3, 11), (4, 12),
        (5, 15), (7, 14), (9, 16), (13, 17),
    ),
    (
        (0, 9), (1, 12), (2, 7), (3, 15), (4, 8),
        (5, 11), (6, 13), (10, 17), (14, 16),
    ),
    (
        (0, 10), (1, 7), (2, 15), (3, 9), (4, 13),
        (5, 8), (6, 14), (11, 16), (12, 17),
    ),
    (
        (0, 11), (1, 17), (2, 10), (3, 16), (4, 15),
        (5, 9), (6, 12), (7, 13), (8, 14),
    ),
    (
        (0, 12), (1, 13), (2, 8), (3, 7), (4, 16),
        (5, 6), (9, 17), (10, 14), (11, 15),
    ),
    (
        (0, 13), (1, 16), (2, 5), (3, 14), (4, 10),
        (6, 17), (7, 12), (8, 11), (9, 15),
    ),
    (
        (0, 15), (1, 5), (2, 14), (3, 17), (4, 6),
        (7, 10), (8, 9), (11, 12), (13, 16),
    ),
    (
        (0, 16), (1, 14), (2, 17), (3, 4), (5, 13),
        (6, 11), (7, 9), (8, 12), (10, 15),
    ),
    (
        (0, 17), (1, 9), (2, 11), (3, 12), (4, 14),
        (5, 7), (6, 15), (8, 16), (10, 13),
    ),
)


def normalize(edge: Edge) -> Edge:
    left, right = edge
    assert left != right
    return (left, right) if left < right else (right, left)


def validate_matchings(
    matchings: tuple[Matching, Matching, Matching],
    expected_unmatched: tuple[int, int, int],
) -> tuple[set[Edge], set[Edge], set[Edge]]:
    edge_sets: list[set[Edge]] = []
    observed_unmatched: list[int] = []
    universe = set(range(17))

    for matching in matchings:
        edges = {normalize(edge) for edge in matching}
        assert len(edges) == 8
        used: set[int] = set()
        for left, right in edges:
            assert 0 <= left < 17 and 0 <= right < 17
            assert left not in used and right not in used
            used.add(left)
            used.add(right)
        missing = universe - used
        assert len(missing) == 1
        observed_unmatched.append(next(iter(missing)))
        edge_sets.append(edges)

    assert tuple(observed_unmatched) == expected_unmatched
    assert len(set(observed_unmatched)) == 3
    assert edge_sets[0].isdisjoint(edge_sets[1])
    assert edge_sets[0].isdisjoint(edge_sets[2])
    assert edge_sets[1].isdisjoint(edge_sets[2])
    return edge_sets[0], edge_sets[1], edge_sets[2]


def rainbow_triangles(
    edge_sets: tuple[set[Edge], set[Edge], set[Edge]],
) -> list[tuple[int, int, int]]:
    answer: list[tuple[int, int, int]] = []
    for a in range(17):
        for b in range(a + 1, 17):
            for c in range(b + 1, 17):
                triangle_edges = (
                    normalize((a, b)),
                    normalize((a, c)),
                    normalize((b, c)),
                )
                colours = []
                for edge in triangle_edges:
                    hits = [
                        colour
                        for colour, edges in enumerate(edge_sets)
                        if edge in edges
                    ]
                    if len(hits) != 1:
                        break
                    colours.append(hits[0])
                if len(colours) == 3 and len(set(colours)) == 3:
                    answer.append((a, b, c))
    return answer


def pairwise_disjoint(triangles: list[tuple[int, int, int]]) -> bool:
    used: set[int] = set()
    for triangle in triangles:
        if used.intersection(triangle):
            return False
        used.update(triangle)
    return True


def verify_zero_completion() -> None:
    extended_given: list[Matching] = []
    for matching, unmatched in zip(
        (ZERO[1], ZERO[2], ZERO[3]), ZERO_UNMATCHED
    ):
        extended_given.append(matching + ((unmatched, 17),))

    all_factors = tuple(extended_given) + ZERO_COMPLETION
    assert len(all_factors) == 17
    seen: set[Edge] = set()
    universe = set(range(18))
    for factor in all_factors:
        assert len(factor) == 9
        used: set[int] = set()
        for raw_edge in factor:
            edge = normalize(raw_edge)
            left, right = edge
            assert 0 <= left < 18 and 0 <= right < 18
            assert left not in used and right not in used
            assert edge not in seen
            used.update(edge)
            seen.add(edge)
        assert used == universe
    assert len(seen) == comb(18, 2) == 153


def arithmetic() -> None:
    r = 15
    blocks = comb(2 * r + 1, r - 1) // r
    facets = comb(2 * r + 1, r - 1)
    assert blocks == 17_678_835
    assert facets == 265_182_525
    assert facets == r * blocks
    assert (r + 1) // 2 == 8
    assert (r + 2) // 3 == 5

    contained_average = (
        blocks * comb(r + 1, 2) // comb(2 * r + 1, r + 2)
    )
    assert contained_average == (r + 1) // 2
    assert r * blocks + 3 * blocks == (r + 3) * blocks
    assert (r * blocks) % 2 == 1
    assert (3 * blocks) % 2 == 1
    assert ((r + 3) * blocks) % 2 == 0


def main() -> None:
    arithmetic()
    verify_zero_completion()

    zero_matchings = (ZERO[1], ZERO[2], ZERO[3])
    cases = (
        ("zero", zero_matchings, ZERO_UNMATCHED, []),
        ("one", ONE, ONE_UNMATCHED, [(2, 5, 13)]),
        ("two", TWO, TWO_UNMATCHED, [(0, 3, 12), (2, 5, 6)]),
    )
    for name, matchings, unmatched, expected in cases:
        edges = validate_matchings(matchings, unmatched)
        triangles = rainbow_triangles(edges)
        assert triangles == expected, (name, triangles)
        assert pairwise_disjoint(triangles)
        assert len(triangles) <= 5
        print(
            f"{name}: unmatched={unmatched}, "
            f"rainbow_triangles={triangles}"
        )

    print("defect-facet local audit: PASS")


if __name__ == "__main__":
    main()

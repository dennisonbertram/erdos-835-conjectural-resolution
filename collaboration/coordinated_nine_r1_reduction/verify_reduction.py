#!/usr/bin/env python3
"""Audit the r=1 coordinated-ninth reduction and explicit pair obstruction."""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path


VERTICES = frozenset(range(13))
EDGES = frozenset(combinations(sorted(VERTICES), 2))


def odd_partitions(total: int, parts: int, minimum: int = 1):
    if parts == 0:
        if total == 0:
            yield ()
        return
    for first in range(minimum, total + 1, 2):
        for rest in odd_partitions(total - first, parts - 1, first):
            yield (first, *rest)


def core_edges(blocks: tuple[int, ...]) -> int:
    total = sum(blocks)
    return (total * total - sum(block * block for block in blocks)) // 2


def core_degree(blocks: tuple[int, ...]) -> int:
    return sum(blocks) - min(blocks)


def coarsened_catalogue(
    cross_matching_degree: int,
) -> tuple[tuple[int, tuple[int, ...]], ...]:
    """Odd partitions allowed by delta(G)>=4 after deleting k matchings."""
    result = []
    for separator in range(5):
        outside = 10 - separator
        parts = separator + 2
        for blocks in odd_partitions(outside, parts):
            # For a vertex in the smallest block:
            # 4 <= (c-1) + separator + cross_matching_degree.
            if min(blocks) - 1 + separator + cross_matching_degree < 4:
                continue
            result.append((separator, blocks))
    return tuple(result)


def reuse_ceiling(
    selected_edges: int,
    rho_offset: int,
    core_order: int,
    edge_count: int,
    maximum_degree: int,
    inventory: int,
) -> int:
    outside = 13 - core_order
    touch_correction = max(
        0,
        selected_edges - edge_count - comb(outside, 2),
    )
    core_degree_sum = 2 * edge_count + touch_correction
    outside_capacity = (
        2 * selected_edges
        - core_degree_sum
        - rho_offset * outside
    )
    return min(
        inventory,
        12 - maximum_degree,
        outside_capacity // 3,
    )


def verify_catalogues() -> None:
    initial = []
    for separator in range(5):
        for blocks in odd_partitions(10 - separator, separator + 2):
            if core_degree(blocks) <= 5:
                initial.append((separator, blocks))
    assert initial == [
        (0, (5, 5)),
        (4, (1, 1, 1, 1, 1, 1)),
    ]

    after_one = coarsened_catalogue(1)
    assert after_one == (
        (0, (5, 5)),
        (1, (3, 3, 3)),
        (3, (1, 1, 1, 1, 3)),
        (4, (1, 1, 1, 1, 1, 1)),
    )

    # K333 has zero outside complement capacity under rho=d_E-2,
    # so it cannot lie in a remaining support whose triple contributes 3.
    assert 2 * 31 - 2 * 27 - 2 * 4 == 0 < 3

    sequential = (
        ((5, 5), 10, 25, 5),
        ((1, 1, 1, 1, 3), 7, 18, 6),
        ((1, 1, 1, 1, 1, 1), 6, 15, 5),
    )
    assert tuple(
        reuse_ceiling(31, 2, order, edges, degree, 5)
        for _, order, edges, degree in sequential
    ) == (1, 4, 5)

    after_two = coarsened_catalogue(2)
    assert after_two == (
        (0, (3, 7)),
        (0, (5, 5)),
        (1, (3, 3, 3)),
        (2, (1, 1, 1, 5)),
        (2, (1, 1, 3, 3)),
        (3, (1, 1, 1, 1, 3)),
        (4, (1, 1, 1, 1, 1, 1)),
    )
    final_rows = tuple(
        (
            blocks,
            sum(blocks),
            core_edges(blocks),
            core_degree(blocks),
        )
        for _, blocks in after_two
    )
    assert tuple(
        reuse_ceiling(37, 3, order, edges, degree, 5)
        for _, order, edges, degree in final_rows
    ) == (3, 2, 1, 4, 3, 5, 5)
    print("PASS exact one- and two-matching Tutte catalogues and reuse rows")


def verify_six_prefix_reduction() -> None:
    assert 4 * 4 + 2 * 5 == 26
    assert 4 * 5 + 6 * 3 + 1 == 39
    assert 10 * (5 - 1) == 40 > 39
    assert 6 * (5 - 1) == 24 > 4 * 5 + 1

    for overlap in range(6):
        if overlap <= 3:
            assert 2 * comb(6, 2) - comb(overlap, 2) > 26
        else:
            common_vertex_degree = 2 * 5 - (overlap - 1)
            assert common_vertex_degree > 5

    # Separator-three local endpoint equation.
    assert tuple(
        (tt, tc)
        for tt in range(3)
        for tc in range(4)
        if 2 * tt + tc == 4
    ) == ((1, 2), (2, 0))
    # A perfect matching on two 3-sets has either one or three cross edges.
    assert tuple(
        cross
        for cross in range(4)
        if (3 - cross) % 2 == 0
    ) == (1, 3)
    print("PASS K55 capacity, unique-K6, reuse, and rigid-type arithmetic")


def clique(vertices) -> frozenset[tuple[int, int]]:
    return frozenset(combinations(sorted(vertices), 2))


def verify_forced_edge_frontier() -> None:
    # Refine the one-deleted-matching catalogue to one deleted edge.
    # A block vertex with internal+separator degree below four needs to be
    # an endpoint of that sole edge; at most two vertices can be deficient.
    forced_rows = []
    for separator, blocks in coarsened_catalogue(1):
        deficient_vertices = sum(
            block
            for block in blocks
            if block - 1 + separator < 4
        )
        if deficient_vertices <= 2:
            forced_rows.append((separator, blocks))
    assert forced_rows == [
        (0, (5, 5)),
        (4, (1, 1, 1, 1, 1, 1)),
    ]

    # K5,5-e requires 38 remaining incidences on its support, while its
    # own outside triple requires three more; only 39 exist globally.
    assert 8 * 4 + 2 * 3 + 3 == 41 > 39

    # K6-e has four degree-five and two degree-at-least-four vertices.
    # If all six triples avoid it, only the four fives+singleton can pay.
    assert 4 * 4 + 2 * 3 == 22 > 4 * 5 + 1

    # Exhaust the tiny coexistence claim for two K6-minus-edge cores.
    base_vertices = frozenset(range(6))
    base_missing = (0, 1)
    base = clique(base_vertices) - frozenset((base_missing,))
    feasible = []
    for vertices in combinations(sorted(VERTICES), 6):
        vertices = frozenset(vertices)
        for missing in combinations(sorted(vertices), 2):
            current = clique(vertices) - frozenset((missing,))
            union = base | current
            degrees = Counter(
                vertex
                for edge in union
                for vertex in edge
            )
            if len(union) <= 26 and max(degrees.values()) <= 5:
                feasible.append((vertices, missing))
    assert len(feasible) == 15
    assert all(vertices == base_vertices for vertices, _ in feasible)
    print("PASS exact forced-edge rows and K6-minus-edge coexistence")


def endpoints(matching: frozenset[tuple[int, int]]) -> frozenset[int]:
    return frozenset(vertex for edge in matching for vertex in edge)


def perfect_matchings(vertices: frozenset[int]):
    ordered = tuple(sorted(vertices))
    if not ordered:
        yield frozenset()
        return
    first = ordered[0]
    for index in range(1, len(ordered)):
        second = ordered[index]
        rest = frozenset(ordered[1:index] + ordered[index + 1 :])
        edge = tuple(sorted((first, second)))
        for tail in perfect_matchings(rest):
            yield frozenset((edge, *tail))


def normalize_matching(raw) -> frozenset[tuple[int, int]]:
    return frozenset(tuple(sorted(edge)) for edge in raw)


def verify_pair_certificates() -> None:
    path = Path(__file__).with_name("pair_obstructions.json")
    records = json.loads(path.read_text())
    assert tuple(record["label"] for record in records) == (
        "triple-intersection-0",
        "triple-intersection-1",
        "triple-intersection-2",
    )

    observed_tables = {}
    for record in records:
        prefix = tuple(
            normalize_matching(matching)
            for matching in record["prefix"]
        )
        remaining_fives = tuple(
            frozenset(current)
            for current in record["remaining_fives"]
        )
        remaining_triples = tuple(
            frozenset(current)
            for current in record["remaining_triples"]
        )
        singleton = frozenset(record["singleton"])
        obstructed_pair = tuple(record["obstructed_pair"])

        assert len(remaining_fives) == 4
        assert len(remaining_triples) == 6
        assert len(singleton) == 1
        assert len(
            remaining_triples[obstructed_pair[0]]
            & remaining_triples[obstructed_pair[1]]
        ) == int(record["label"][-1])

        used: set[tuple[int, int]] = set()
        selected_complements = []
        for index, matching in enumerate(prefix):
            expected_edges = 4 if index < 4 else 5
            assert len(matching) == expected_edges
            assert len(endpoints(matching)) == 2 * expected_edges
            assert used.isdisjoint(matching)
            used.update(matching)
            selected_complements.append(VERTICES - endpoints(matching))

        assert len(used) == 26
        degrees = Counter(vertex for edge in used for vertex in edge)
        assert max(degrees.values()) == 5
        assert min(degrees.values()) >= 1

        complements = (
            *selected_complements,
            *remaining_fives,
            *remaining_triples,
            singleton,
        )
        assert Counter(map(len, complements)) == Counter(
            {5: 8, 3: 8, 1: 1}
        )
        assert all(
            sum(vertex in complement for complement in complements) == 5
            for vertex in VERTICES
        )

        deleted = frozenset(used)
        families = []
        for triple in remaining_triples:
            families.append(
                tuple(
                    matching
                    for matching in perfect_matchings(VERTICES - triple)
                    if matching.isdisjoint(deleted)
                )
            )

        left, right = obstructed_pair
        assert tuple(map(len, (families[left], families[right]))) == (24, 24)
        pair_counts = {
            (first_index, second_index): sum(
                first.isdisjoint(second)
                for first in families[first_index]
                for second in families[second_index]
            )
            for first_index, second_index in combinations(range(6), 2)
        }
        assert pair_counts[obstructed_pair] == 0
        assert all(
            count > 0
            for pair, count in pair_counts.items()
            if pair != obstructed_pair
        )
        observed_tables[record["label"]] = (
            tuple(map(len, families)),
            pair_counts,
        )

    individual_counts, pair_counts = observed_tables[
        "triple-intersection-2"
    ]
    assert individual_counts == (24, 24, 120, 150, 144, 150)
    assert pair_counts == {
        (0, 1): 0,
        (0, 2): 1536,
        (0, 3): 2496,
        (0, 4): 2472,
        (0, 5): 2800,
        (1, 2): 1536,
        (1, 3): 2490,
        (1, 4): 2406,
        (1, 5): 2772,
        (2, 3): 11760,
        (2, 4): 9216,
        (2, 5): 11628,
        (3, 4): 14556,
        (3, 5): 15612,
        (4, 5): 12444,
    }
    print("PASS literal class-B pair obstructions at intersections 0, 1, 2")
    print("PASS exact all-15-pair table for the intersection-2 certificate")


def main() -> None:
    verify_catalogues()
    verify_six_prefix_reduction()
    verify_forced_edge_frontier()
    verify_pair_certificates()
    print("PASS coordinated-nine r=1 reduction")
    print("SCOPE: finite reduction and pair counterexample; no ninth theorem")


if __name__ == "__main__":
    main()

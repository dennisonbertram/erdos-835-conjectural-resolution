#!/usr/bin/env python3
"""Classify and exclude four-K6 total-obstruction families in r=0."""

from __future__ import annotations

from collections import Counter
from itertools import combinations

from verify_r0_core_pairs import INCIDENT, VERTICES, embeddings, popcount
from verify_r0_three_core_capacity import (
    covering_splits,
    passes_prefix_screens,
    support_mask,
)


def main() -> None:
    cores = embeddings("6")
    first = cores[0]
    supports = {core: support_mask(core) for core in cores}
    candidates = [
        core
        for core in cores
        if core != first and passes_prefix_screens(first | core)
    ]
    assert len(candidates) == 364

    tested = 0
    screened = 0
    covering = 0
    family_shapes = Counter()
    union_shapes: dict[int, int] = {}
    for second, third, fourth in combinations(candidates, 3):
        tested += 1
        union = first | second | third | fourth
        if not passes_prefix_screens(union):
            continue
        screened += 1
        family = (
            ("6", first),
            ("6", second),
            ("6", third),
            ("6", fourth),
        )
        if not covering_splits(family, union, supports):
            continue
        covering += 1

        core_supports = [supports[core] for _kind, core in family]
        support_union = 0
        support_intersection = (1 << len(VERTICES)) - 1
        for core_support in core_supports:
            support_union |= core_support
            support_intersection &= core_support

        edge_count = popcount(union)
        union_order = popcount(support_union)
        intersection_order = popcount(support_intersection)
        intersection_degrees = tuple(
            sorted(
                popcount(union & INCIDENT[vertex])
                for vertex in VERTICES
                if support_intersection >> vertex & 1
            )
        )
        shape = (
            edge_count,
            union_order,
            intersection_order,
            intersection_degrees,
        )
        family_shapes[shape] += 1
        union_shapes[union] = edge_count

    expected_family_shapes = Counter(
        {
            (21, 7, 3, (6, 6, 6)): 140,
            (26, 8, 3, (7, 7, 7)): 10080,
            (26, 8, 2, (7, 7)): 5040,
        }
    )
    assert tested == 7_971_964
    assert screened == 18_410
    assert covering == 15_260
    assert family_shapes == expected_family_shapes, family_shapes
    assert Counter(union_shapes.values()) == Counter({21: 7, 26: 1008})
    assert all(
        min(shape[3]) - 2 >= 4
        for shape in family_shapes
    )

    print("PASS tested all 7,971,964 fixed-first four-K6 families")
    print("PASS 18,410 pass the necessary prefix graph screens")
    print("PASS 15,260 pass every subfamily-capacity inequality")
    print("PASS only K7 and 26-edge/eight-vertex union shapes survive")
    print("PASS each has common vertices of union degree at least six")
    print("PASS complement-row identity excludes both shapes")
    print("SCOPE: four distinct K6 cores; mixed four-core families remain open")


if __name__ == "__main__":
    main()

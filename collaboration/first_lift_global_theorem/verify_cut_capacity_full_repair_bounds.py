#!/usr/bin/env python3
"""Verify exact one-cut lower bounds for three dead-prefix repairs."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from verify_r1_minimum_layer_repair import build_instance
from verify_r3_dead_seven_prefixes import CASES, VERTICES, endpoints


Layer = frozenset[tuple[int, int]]
Support = frozenset[int]
DISTINGUISHED_VERTEX = max(VERTICES)


@dataclass(frozen=True)
class CutReport:
    side: Support
    demand: int
    selected_crossings: tuple[int, ...]
    selected_capacities: tuple[int, ...]
    remaining_capacities: tuple[int, ...]
    deficit: int
    decreasing_gains: tuple[int, ...]
    minimum_changes: int


def crossing_count(layer: Layer, side: Support) -> int:
    return sum((left in side) != (right in side) for left, right in layer)


def cut_capacity(support: Support, side: Support) -> int:
    return min(len(support & side), len(support - side))


def cut_report(
    prefix: tuple[Layer, ...],
    selected_supports: tuple[Support, ...],
    remaining_supports: tuple[Support, ...],
    side: Support,
) -> CutReport:
    assert prefix
    assert len(prefix) == len(selected_supports)
    assert all(endpoints(layer) == support for layer, support in zip(
        prefix,
        selected_supports,
    ))

    demand = len(side) * (len(VERTICES) - len(side))
    selected_crossings = tuple(
        crossing_count(layer, side) for layer in prefix
    )
    selected_capacities = tuple(
        cut_capacity(support, side) for support in selected_supports
    )
    remaining_capacities = tuple(
        cut_capacity(support, side) for support in remaining_supports
    )
    gains = tuple(
        capacity - crossing
        for capacity, crossing in zip(
            selected_capacities,
            selected_crossings,
        )
    )
    assert all(gain >= 0 for gain in gains)
    decreasing_gains = tuple(sorted(gains, reverse=True))
    deficit = (
        demand
        - sum(selected_crossings)
        - sum(remaining_capacities)
    )

    target = max(deficit, 0)
    recovered = 0
    minimum_changes = 0
    while recovered < target:
        assert minimum_changes < len(decreasing_gains)
        recovered += decreasing_gains[minimum_changes]
        minimum_changes += 1

    return CutReport(
        side=side,
        demand=demand,
        selected_crossings=selected_crossings,
        selected_capacities=selected_capacities,
        remaining_capacities=remaining_capacities,
        deficit=deficit,
        decreasing_gains=decreasing_gains,
        minimum_changes=minimum_changes,
    )


def canonical_nontrivial_cuts() -> tuple[Support, ...]:
    """Represent every unordered cut once by excluding vertex twelve."""

    other_vertices = tuple(sorted(VERTICES - {DISTINGUISHED_VERTEX}))
    cuts = tuple(
        frozenset(
            vertex
            for index, vertex in enumerate(other_vertices)
            if mask & (1 << index)
        )
        for mask in range(1, 1 << len(other_vertices))
    )
    assert len(cuts) == 2 ** (len(VERTICES) - 1) - 1 == 4095
    return cuts


def exhaustive_cut_bounds(
    prefix: tuple[Layer, ...],
    selected_supports: tuple[Support, ...],
    remaining_supports: tuple[Support, ...],
) -> tuple[int, Counter[int], frozenset[Support]]:
    reports = tuple(
        cut_report(
            prefix,
            selected_supports,
            remaining_supports,
            side,
        )
        for side in canonical_nontrivial_cuts()
    )
    distribution = Counter(report.minimum_changes for report in reports)
    maximum = max(distribution)
    maximizers = frozenset(
        report.side
        for report in reports
        if report.minimum_changes == maximum
    )
    return maximum, distribution, maximizers


def verify_r1() -> None:
    selected, selected_supports, remaining_supports = build_instance()
    prefix = tuple(selected)
    selected_support_tuple = tuple(selected_supports)
    remaining_support_tuple = tuple(remaining_supports)
    core = frozenset(range(6))

    witness = cut_report(
        prefix,
        selected_support_tuple,
        remaining_support_tuple,
        core,
    )
    assert witness.demand == 42
    assert witness.selected_crossings == (0,) * 7
    assert witness.remaining_capacities == (4, 4, 4, 4, 4, 4, 1, 1, 2, 2)
    assert sum(witness.remaining_capacities) == 30
    assert witness.decreasing_gains == (6, 4, 4, 4, 4, 4, 4)
    assert witness.deficit == 12
    assert witness.minimum_changes == 3

    maximum, distribution, maximizers = exhaustive_cut_bounds(
        prefix,
        selected_support_tuple,
        remaining_support_tuple,
    )
    assert maximum == 3
    assert distribution == Counter({0: 4075, 1: 10, 2: 8, 3: 2})
    assert maximizers == frozenset({
        frozenset(range(6)),
        frozenset(range(7)),
    })
    print("PASS r=1: exact strongest one-cut lower bound is 3 changes")


def r3_instance(
    name: str,
) -> tuple[tuple[Layer, ...], tuple[Support, ...], tuple[Support, ...]]:
    case = CASES[name]
    prefix = case["prefix"]
    remaining_complements = case["remaining_complements"]
    assert isinstance(prefix, tuple)
    assert isinstance(remaining_complements, tuple)
    selected_supports = tuple(endpoints(layer) for layer in prefix)
    remaining_supports = tuple(
        VERTICES - complement for complement in remaining_complements
    )
    return prefix, selected_supports, remaining_supports


def verify_r3_c_in_g() -> None:
    prefix, selected_supports, remaining_supports = r3_instance("C_in_G")
    core = frozenset(range(7))
    witness = cut_report(
        prefix,
        selected_supports,
        remaining_supports,
        core,
    )
    assert witness.demand == 42
    assert witness.selected_crossings == (0, 0, 0, 0, 0, 1, 1)
    assert witness.selected_capacities == (2, 2, 2, 2, 4, 5, 5)
    assert witness.remaining_capacities == (2, 2, 2, 2, 2, 2, 3, 3, 3, 5)
    assert sum(witness.remaining_capacities) == 26
    assert witness.decreasing_gains == (4, 4, 4, 2, 2, 2, 2)
    assert witness.deficit == 14
    assert witness.minimum_changes == 4

    maximum, distribution, maximizers = exhaustive_cut_bounds(
        prefix,
        selected_supports,
        remaining_supports,
    )
    assert maximum == 4
    assert distribution == Counter({0: 4074, 1: 7, 2: 12, 3: 1, 4: 1})
    assert maximizers == frozenset({core})
    print("PASS r=3 C_in_G: exact strongest one-cut lower bound is 4 changes")


def verify_r3_d_in_g() -> None:
    prefix, selected_supports, remaining_supports = r3_instance("D_in_G")
    core = frozenset(range(7))
    witness = cut_report(
        prefix,
        selected_supports,
        remaining_supports,
        core,
    )
    assert witness.demand == 42
    assert witness.selected_crossings == (0,) * 7
    assert witness.selected_capacities == (2, 2, 2, 2, 4, 6, 6)
    assert witness.remaining_capacities == (2, 2, 2, 2, 2, 3, 4, 3, 3, 5)
    assert sum(witness.remaining_capacities) == 28
    assert witness.decreasing_gains == (6, 6, 4, 2, 2, 2, 2)
    assert witness.deficit == 14
    assert witness.minimum_changes == 3

    maximum, distribution, maximizers = exhaustive_cut_bounds(
        prefix,
        selected_supports,
        remaining_supports,
    )
    assert maximum == 3
    assert distribution == Counter({0: 4073, 1: 14, 2: 6, 3: 2})
    assert maximizers == frozenset({
        core,
        core | {10},
    })
    print("PASS r=3 D_in_G: exact strongest one-cut lower bound is 3 changes")


def main() -> None:
    verify_r1()
    verify_r3_c_in_g()
    verify_r3_d_in_g()
    print("PASS all 4095 unordered nontrivial cuts checked in every instance")
    print("SCOPE: exact one-cut lower bounds, not universal repair distances")


if __name__ == "__main__":
    main()

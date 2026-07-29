#!/usr/bin/env python3
"""Verify exact prefix-layer repair distances for the two r=3 certificates."""

from __future__ import annotations

from itertools import combinations

from verify_r3_dead_seven_prefixes import (
    ALL_EDGES,
    CASES,
    VERTICES,
    endpoints,
    matching,
    perfect_matching,
)


Layer = frozenset[tuple[int, int]]


REPAIRS = {
    "C_in_G": {
        "eighth_replacement_colour": 0,
        "eighth_replacement": matching(
            (0, 5),
            (2, 6),
            (3, 7),
            (4, 10),
        ),
        "remaining_index": 0,
        "eighth": matching(
            (4, 8),
            (6, 9),
            (7, 10),
            (11, 12),
        ),
        "full_completion": (
            matching((0, 5), (2, 4), (3, 10), (6, 7)),
            matching((0, 4), (1, 3), (2, 5), (7, 9)),
            matching((1, 2), (3, 5), (4, 6), (10, 12)),
            matching((0, 2), (1, 4), (3, 6), (8, 12)),
            matching((0, 9), (1, 5), (2, 7), (3, 12), (6, 8)),
            matching(
                (0, 3),
                (1, 7),
                (2, 8),
                (4, 9),
                (5, 10),
                (6, 11),
            ),
            matching(
                (0, 11),
                (1, 6),
                (2, 12),
                (3, 8),
                (4, 10),
                (5, 9),
            ),
            matching((4, 12), (6, 9), (7, 8), (10, 11)),
            matching((0, 7), (6, 10), (8, 9), (11, 12)),
            matching((3, 11), (5, 8), (7, 12), (9, 10)),
            matching((1, 10), (5, 7), (8, 11), (9, 12)),
            matching((0, 12), (4, 8), (7, 10), (9, 11)),
            matching((1, 12), (2, 9), (7, 11), (8, 10)),
            matching((0, 10), (1, 11), (2, 6), (3, 4), (5, 12)),
            matching((0, 6), (1, 8), (2, 11), (3, 9), (4, 5)),
            matching((0, 1), (2, 3), (4, 7), (5, 11), (6, 12)),
            matching(
                (0, 8),
                (1, 9),
                (2, 10),
                (3, 7),
                (4, 11),
                (5, 6),
            ),
        ),
        "retained": frozenset({1, 2, 3}),
        "forbidden_retained_count": 4,
    },
    "D_in_G": {
        "eighth_replacement_colour": 0,
        "eighth_replacement": matching(
            (0, 6),
            (1, 2),
            (3, 8),
            (5, 12),
        ),
        "remaining_index": 0,
        "eighth": matching(
            (5, 7),
            (6, 11),
            (8, 12),
            (9, 10),
        ),
        "full_completion": (
            matching((0, 6), (1, 2), (3, 5), (8, 12)),
            matching((0, 5), (1, 6), (2, 4), (7, 11)),
            matching((1, 3), (2, 5), (4, 6), (7, 12)),
            matching((0, 1), (3, 4), (5, 6), (9, 11)),
            matching((0, 3), (1, 7), (2, 8), (4, 9), (5, 11)),
            matching(
                (0, 7),
                (2, 6),
                (3, 11),
                (4, 10),
                (5, 8),
                (9, 12),
            ),
            matching(
                (0, 10),
                (1, 9),
                (2, 7),
                (3, 12),
                (4, 8),
                (6, 11),
            ),
            matching((5, 9), (6, 7), (8, 10), (11, 12)),
            matching((0, 9), (6, 12), (7, 10), (8, 11)),
            matching((3, 8), (4, 11), (7, 9), (10, 12)),
            matching((2, 12), (4, 7), (8, 9), (10, 11)),
            matching((0, 12), (1, 11), (7, 8), (9, 10)),
            matching((1, 5), (2, 10), (3, 9), (6, 8)),
            matching((0, 11), (1, 4), (2, 9), (3, 10), (5, 12)),
            matching((0, 2), (1, 8), (3, 6), (4, 12), (5, 10)),
            matching((0, 4), (1, 12), (2, 3), (5, 7), (6, 10)),
            matching(
                (0, 8),
                (1, 10),
                (2, 11),
                (3, 7),
                (4, 5),
                (6, 9),
            ),
        ),
        "retained": frozenset({0, 1, 2, 3}),
        "forbidden_retained_count": 5,
    },
}


def supports_for(case: dict[str, object]) -> tuple[frozenset[int], ...]:
    prefix = case["prefix"]
    remaining_complements = case["remaining_complements"]
    assert isinstance(prefix, tuple)
    assert isinstance(remaining_complements, tuple)
    return (
        *(endpoints(current) for current in prefix),
        *(VERTICES - complement for complement in remaining_complements),
    )


def crossing_edges(
    layer: Layer,
    cut: frozenset[int],
) -> int:
    return sum((left in cut) != (right in cut) for left, right in layer)


def crossing_capacity(
    support: frozenset[int],
    cut: frozenset[int],
) -> int:
    return min(len(support & cut), len(support - cut))


def cut_change_lower_bound(
    prefix: tuple[Layer, ...],
    supports: tuple[frozenset[int], ...],
    cut: frozenset[int],
) -> tuple[int, int, tuple[int, ...], tuple[int, ...], int]:
    """Return the cut lower bound and its exact capacity data."""

    cut_size = len(cut) * len(VERTICES - cut)
    actual = tuple(crossing_edges(layer, cut) for layer in prefix)
    selected_capacities = tuple(
        crossing_capacity(support, cut)
        for support in supports[:7]
    )
    remaining_capacity = sum(
        crossing_capacity(support, cut)
        for support in supports[7:]
    )
    deficit = cut_size - remaining_capacity - sum(actual)
    gains = tuple(
        capacity - used
        for capacity, used in zip(selected_capacities, actual)
    )
    assert all(gain >= 0 for gain in gains)
    if deficit <= 0:
        return 0, deficit, actual, gains, remaining_capacity
    recovered = 0
    for changed, gain in enumerate(sorted(gains, reverse=True), start=1):
        recovered += gain
        if recovered >= deficit:
            return changed, deficit, actual, gains, remaining_capacity
    raise AssertionError("cut capacity rules out every full completion")


def verify_case(
    name: str,
    case: dict[str, object],
    repair: dict[str, object],
) -> None:
    prefix = case["prefix"]
    remaining_complements = case["remaining_complements"]
    assert isinstance(prefix, tuple)
    assert isinstance(remaining_complements, tuple)
    supports = supports_for(case)

    replacement_colour = repair["eighth_replacement_colour"]
    replacement = repair["eighth_replacement"]
    remaining_index = repair["remaining_index"]
    eighth = repair["eighth"]
    completion = repair["full_completion"]
    retained = repair["retained"]
    forbidden_retained_count = repair["forbidden_retained_count"]
    assert isinstance(replacement_colour, int)
    assert isinstance(replacement, frozenset)
    assert isinstance(remaining_index, int)
    assert isinstance(eighth, frozenset)
    assert isinstance(completion, tuple)
    assert isinstance(retained, frozenset)
    assert isinstance(forbidden_retained_count, int)

    prefix_union = frozenset().union(*prefix)
    remaining_supports = supports[7:]
    assert all(
        perfect_matching(support, ALL_EDGES - prefix_union) is None
        for support in remaining_supports
    )

    fixed_six = frozenset().union(
        *(
            current
            for colour, current in enumerate(prefix)
            if colour != replacement_colour
        )
    )
    assert replacement != prefix[replacement_colour]
    assert endpoints(replacement) == supports[replacement_colour]
    assert replacement.isdisjoint(fixed_six)
    assert endpoints(eighth) == remaining_supports[remaining_index]
    assert eighth.isdisjoint(fixed_six | replacement)
    assert len(prefix[replacement_colour] - replacement) == 2

    assert len(completion) == len(supports) == 17
    assert all(
        endpoints(current) == support
        for current, support in zip(completion, supports)
    )
    completion_union = frozenset().union(*completion)
    assert sum(map(len, completion)) == len(completion_union) == 78
    assert completion_union == ALL_EDGES
    actual_retained = frozenset(
        colour
        for colour in range(7)
        if completion[colour] == prefix[colour]
    )
    assert actual_retained == retained
    assert forbidden_retained_count == len(retained) + 1

    full_distance = 7 - len(retained)
    strongest_bound = -1
    strongest_cuts = set()
    cuts_checked = 0
    for size in range(1, len(VERTICES)):
        for vertices in combinations(sorted(VERTICES - {0}), size - 1):
            cut = frozenset({0, *vertices})
            lower_bound, _, _, _, _ = cut_change_lower_bound(
                prefix,
                supports,
                cut,
            )
            cuts_checked += 1
            if lower_bound > strongest_bound:
                strongest_bound = lower_bound
                strongest_cuts = {cut}
            elif lower_bound == strongest_bound:
                strongest_cuts.add(cut)

    expected_strongest = {
        "C_in_G": {frozenset(range(7))},
        "D_in_G": {
            frozenset(range(7)),
            frozenset({*range(7), 10}),
        },
    }
    assert cuts_checked == 4095
    assert strongest_bound == full_distance
    assert strongest_cuts == expected_strongest[name]

    core_cut = frozenset(range(7))
    core_bound, deficit, actual, gains, remaining_capacity = (
        cut_change_lower_bound(prefix, supports, core_cut)
    )
    assert core_bound == full_distance
    assert deficit == 14
    if name == "C_in_G":
        assert actual == (0, 0, 0, 0, 0, 1, 1)
        assert remaining_capacity == 26
        assert tuple(sorted(gains, reverse=True)) == (4, 4, 4, 2, 2, 2, 2)
    else:
        assert actual == (0, 0, 0, 0, 0, 0, 0)
        assert remaining_capacity == 28
        assert tuple(sorted(gains, reverse=True)) == (6, 6, 4, 2, 2, 2, 2)

    print(
        f"PASS {name}: eighth-admission layer distance is one "
        "(two changed edges in the replacement layer)"
    )
    print(
        f"PASS {name}: full-completion layer distance is {full_distance}; "
        f"crossing-cut deficit={deficit}, gains={tuple(sorted(gains, reverse=True))}"
    )
    print(
        f"PASS {name}: exhaustive audit of {cuts_checked} canonical cuts "
        f"has strongest lower bound {strongest_bound}"
    )


def main() -> None:
    for name, case in CASES.items():
        verify_case(name, case, REPAIRS[name])
    print("SCOPE: exact repair distances for these two r=3 certificates only")


if __name__ == "__main__":
    main()

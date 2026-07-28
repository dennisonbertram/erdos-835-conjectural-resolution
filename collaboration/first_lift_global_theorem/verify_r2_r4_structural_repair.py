#!/usr/bin/env python3
"""Verify r=2/r=4 repairs, cut bounds, and class-B-prime witnesses."""

from __future__ import annotations

from itertools import combinations

import verify_r2_dead_seven_prefix as r2
import verify_r4_dead_seven_prefix as r4
from verify_r1_minimum_layer_repair import build_instance as r1_instance
from verify_r3_dead_seven_prefixes import CASES as R3_CASES
from verify_r3_dead_seven_prefixes import endpoints


Layer = frozenset[tuple[int, int]]
VERTICES = frozenset(range(13))
OUTSIDE = frozenset(range(13, 18))
ALL_VERTICES = VERTICES | OUTSIDE
PALETTE = frozenset(range(17))
PARTIAL_EDGES = frozenset(
    current
    for current in combinations(sorted(ALL_VERTICES), 2)
    if not set(current) <= VERTICES
)


def matching(
    *pairs: tuple[int, int],
) -> frozenset[tuple[int, int]]:
    return frozenset(tuple(sorted(current)) for current in pairs)


REPAIRS = {
    "r2": {
        "module": r2,
        "replacement_colour": 5,
        "replacement": matching(
            (0, 5),
            (1, 4),
            (2, 7),
            (3, 12),
            (8, 11),
            (9, 10),
        ),
        "remaining_index": 5,
        "eighth": matching(
            (0, 6),
            (1, 10),
            (2, 3),
            (4, 11),
            (5, 12),
        ),
        "retained": frozenset({3, 4, 5, 6}),
        "full_completion": (
            matching((2, 11), (3, 12), (4, 9), (5, 10)),
            matching((0, 9), (2, 7), (4, 12), (5, 11)),
            matching((1, 9), (2, 8), (4, 11), (5, 12)),
            matching((0, 1), (3, 5), (7, 8), (10, 12)),
            matching((0, 3), (1, 2), (6, 11), (7, 10), (8, 9)),
            matching(
                (0, 5),
                (1, 4),
                (2, 3),
                (7, 12),
                (8, 11),
                (9, 10),
            ),
            matching(
                (0, 4),
                (1, 3),
                (2, 9),
                (6, 12),
                (7, 11),
                (8, 10),
            ),
            matching((1, 8), (6, 7), (9, 12), (10, 11)),
            matching((0, 10), (6, 8), (7, 9), (11, 12)),
            matching((2, 10), (3, 7), (6, 9), (8, 12)),
            matching((0, 12), (1, 6), (3, 4), (5, 8)),
            matching((4, 8), (5, 7), (6, 10), (9, 11)),
            matching((0, 11), (1, 10), (2, 12), (3, 6), (4, 5)),
            matching((0, 7), (1, 12), (2, 4), (3, 8), (5, 6)),
            matching((0, 6), (1, 11), (2, 5), (3, 9), (4, 10)),
            matching((0, 2), (1, 7), (3, 11), (4, 6), (5, 9)),
            matching((0, 8), (1, 5), (2, 6), (3, 10), (4, 7)),
        ),
        "core_cut": frozenset(range(6)),
        "cut_data": (
            3,
            12,
            (0, 0, 0, 0, 0, 0, 1),
            (6, 4, 4, 4, 4, 4, 4),
            29,
        ),
    },
    "r4": {
        "module": r4,
        "replacement_colour": 0,
        "replacement": matching(
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
        "retained": frozenset({0, 1, 2}),
        "full_completion": (
            matching((0, 5), (2, 6), (3, 4), (7, 10)),
            matching((0, 4), (1, 3), (2, 5), (7, 9)),
            matching((1, 2), (3, 5), (4, 6), (10, 12)),
            matching((0, 2), (1, 6), (3, 12), (4, 8)),
            matching((0, 6), (1, 8), (2, 12), (3, 7), (5, 9)),
            matching(
                (0, 10),
                (1, 9),
                (2, 11),
                (3, 8),
                (4, 7),
                (5, 6),
            ),
            matching(
                (0, 11),
                (1, 4),
                (2, 9),
                (3, 10),
                (5, 12),
                (6, 8),
            ),
            matching((4, 12), (6, 7), (8, 11), (9, 10)),
            matching((0, 7), (6, 10), (8, 12), (9, 11)),
            matching((3, 9), (5, 10), (7, 8), (11, 12)),
            matching((1, 7), (5, 11), (8, 10), (9, 12)),
            matching((0, 8), (4, 9), (7, 12), (10, 11)),
            matching((1, 12), (2, 10), (7, 11), (8, 9)),
            matching((0, 3), (1, 5), (2, 4), (6, 11)),
            matching((0, 1), (2, 7), (3, 11), (4, 5), (6, 12)),
            matching(
                (0, 12),
                (1, 10),
                (2, 3),
                (4, 11),
                (5, 8),
                (6, 9),
            ),
            matching(
                (0, 9),
                (1, 11),
                (2, 8),
                (3, 6),
                (4, 10),
                (5, 7),
            ),
        ),
        "core_cut": frozenset(range(7)),
        "cut_data": (
            4,
            14,
            (0, 0, 0, 0, 0, 1, 1),
            (4, 4, 4, 2, 2, 2, 2),
            26,
        ),
    },
}


PRIME_CERTIFICATES = {
    "r2": {
        "cross": (
            (7, 9, 0, 11, 2),
            (0, 11, 8, 9, 1),
            (11, 7, 10, 3, 8),
            (8, 2, 11, 1, 7),
            (3, 8, 9, 7, 4),
            (4, 6, 7, 8, 9),
            (1, 0, 3, 2, 5),
            (10, 14, 2, 12, 0),
            (15, 12, 1, 0, 14),
            (16, 3, 12, 10, 13),
            (2, 1, 13, 15, 10),
            (9, 10, 16, 13, 3),
            (14, 15, 4, 16, 11),
        ),
        "internal": (
            (0, 1, 13),
            (0, 2, 6),
            (0, 3, 5),
            (0, 4, 12),
            (1, 2, 5),
            (1, 3, 4),
            (1, 4, 16),
            (2, 3, 14),
            (2, 4, 15),
            (3, 4, 6),
        ),
    },
    "r4": {
        "cross": (
            (10, 12, 9, 2, 7),
            (8, 9, 11, 7, 0),
            (9, 8, 7, 10, 11),
            (7, 11, 12, 8, 10),
            (4, 10, 8, 9, 12),
            (12, 7, 3, 11, 8),
            (11, 1, 10, 12, 9),
            (13, 15, 6, 3, 2),
            (14, 2, 1, 0, 13),
            (2, 3, 0, 13, 14),
            (3, 13, 4, 14, 1),
            (1, 0, 2, 4, 3),
            (0, 16, 13, 1, 5),
        ),
        "internal": (
            (0, 1, 5),
            (0, 2, 15),
            (0, 3, 16),
            (0, 4, 6),
            (1, 2, 14),
            (1, 3, 6),
            (1, 4, 4),
            (2, 3, 5),
            (2, 4, 16),
            (3, 4, 15),
        ),
    },
}


def crossing_edges(layer: Layer, cut: frozenset[int]) -> int:
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
    if deficit <= 0:
        return 0, deficit, actual, gains, remaining_capacity
    recovered = 0
    for changed, gain in enumerate(sorted(gains, reverse=True), start=1):
        recovered += gain
        if recovered >= deficit:
            return changed, deficit, actual, gains, remaining_capacity
    raise AssertionError("cut capacity rules out every full completion")


def verify_prime(
    supports: tuple[frozenset[int], ...],
    certificate: dict[str, tuple[tuple[int, ...], ...]],
) -> None:
    cross = certificate["cross"]
    internal = certificate["internal"]
    assert len(cross) == 13 and all(len(row) == 5 for row in cross)
    colouring = {
        (vertex, 13 + outside): colour
        for vertex, row in enumerate(cross)
        for outside, colour in enumerate(row)
    }
    assert frozenset((a, b) for a, b, _ in internal) == frozenset(
        combinations(range(5), 2)
    )
    colouring.update({
        (13 + left, 13 + right): colour
        for left, right, colour in internal
    })
    assert frozenset(colouring) == PARTIAL_EDGES
    assert all(colour in PALETTE for colour in colouring.values())
    for vertex in ALL_VERTICES:
        colours = [
            colour
            for current, colour in colouring.items()
            if vertex in current
        ]
        assert len(colours) == len(set(colours))
        if vertex in OUTSIDE:
            assert frozenset(colours) == PALETTE
        else:
            assert len(colours) == 5
    for colour, support in enumerate(supports):
        endpoints_by_colour = frozenset(
            vertex
            for current, assigned in colouring.items()
            if assigned == colour
            for vertex in current
        )
        assert OUTSIDE <= endpoints_by_colour
        assert VERTICES - (endpoints_by_colour & VERTICES) == support


def verify_case(name: str, data: dict[str, object]) -> None:
    module = data["module"]
    prefix, complements = module.build_certificate()
    supports = module.verify_certificate(prefix, complements)
    replacement_colour = data["replacement_colour"]
    replacement = data["replacement"]
    remaining_index = data["remaining_index"]
    eighth = data["eighth"]
    completion = data["full_completion"]
    retained = data["retained"]
    assert isinstance(replacement_colour, int)
    assert isinstance(replacement, frozenset)
    assert isinstance(remaining_index, int)
    assert isinstance(eighth, frozenset)
    assert isinstance(completion, tuple)
    assert isinstance(retained, frozenset)

    fixed = frozenset().union(
        *(
            layer
            for colour, layer in enumerate(prefix)
            if colour != replacement_colour
        )
    )
    assert replacement != prefix[replacement_colour]
    assert endpoints(replacement) == supports[replacement_colour]
    assert replacement.isdisjoint(fixed)
    assert endpoints(eighth) == supports[7 + remaining_index]
    assert eighth.isdisjoint(fixed | replacement)
    assert len(prefix[replacement_colour] - replacement) == 2

    assert len(completion) == len(supports) == 17
    assert all(
        endpoints(layer) == support
        for layer, support in zip(completion, supports)
    )
    assert sum(map(len, completion)) == 78
    assert frozenset().union(*completion) == r2.ALL_EDGES
    actual_retained = frozenset(
        colour
        for colour in range(7)
        if completion[colour] == prefix[colour]
    )
    assert actual_retained == retained
    full_distance = 7 - len(retained)

    core_cut = data["core_cut"]
    assert isinstance(core_cut, frozenset)
    bound, deficit, actual, gains, remaining_capacity = (
        cut_change_lower_bound(prefix, supports, core_cut)
    )
    expected_bound, expected_deficit, expected_actual, expected_gains, expected_remaining = data[
        "cut_data"
    ]
    assert bound == expected_bound == full_distance
    assert deficit == expected_deficit
    assert actual == expected_actual
    assert tuple(sorted(gains, reverse=True)) == expected_gains
    assert remaining_capacity == expected_remaining

    strongest = -1
    strongest_cuts = set()
    cuts_checked = 0
    for size in range(1, 13):
        for rest in combinations(sorted(VERTICES - {0}), size - 1):
            cut = frozenset({0, *rest})
            current, _, _, _, _ = cut_change_lower_bound(
                prefix, supports, cut
            )
            cuts_checked += 1
            if current > strongest:
                strongest = current
                strongest_cuts = {cut}
            elif current == strongest:
                strongest_cuts.add(cut)
    assert cuts_checked == 4095
    assert strongest == full_distance

    verify_prime(supports, PRIME_CERTIFICATES[name])
    print(
        f"PASS {name}: eighth-admission distance 1 with a two-edge switch; "
        f"full-completion distance {full_distance}"
    )
    print(
        f"PASS {name}: all-cut census strongest bound {strongest} on "
        f"{len(strongest_cuts)} canonical cuts"
    )
    print(f"PASS {name}: literal class-B-prime partial factorization")


def verify_lift_invariance() -> None:
    r1_prefix, r1_selected, r1_remaining = r1_instance()
    r1_supports = tuple((*r1_selected, *r1_remaining))
    r1_data = cut_change_lower_bound(
        tuple(r1_prefix),
        r1_supports,
        frozenset(range(6)),
    )
    r2_prefix, r2_complements = r2.build_certificate()
    r2_supports = r2.verify_certificate(r2_prefix, r2_complements)
    r2_data = cut_change_lower_bound(
        r2_prefix,
        r2_supports,
        frozenset(range(6)),
    )
    assert r1_data[0:2] == r2_data[0:2] == (3, 12)
    assert tuple(sorted(r1_data[3], reverse=True)) == tuple(
        sorted(r2_data[3], reverse=True)
    )
    assert r1_data[4] == 30 and r2_data[4] == 29
    assert sum(r1_data[2]) == 0 and sum(r2_data[2]) == 1

    r3_case = R3_CASES["C_in_G"]
    r3_prefix = r3_case["prefix"]
    r3_complements = r3_case["remaining_complements"]
    assert isinstance(r3_prefix, tuple)
    assert isinstance(r3_complements, tuple)
    r3_supports = (
        *(endpoints(layer) for layer in r3_prefix),
        *(VERTICES - complement for complement in r3_complements),
    )
    r3_data = cut_change_lower_bound(
        r3_prefix,
        tuple(r3_supports),
        frozenset(range(7)),
    )
    r4_prefix, r4_complements = r4.build_certificate()
    r4_supports = r4.verify_certificate(r4_prefix, r4_complements)
    r4_data = cut_change_lower_bound(
        r4_prefix,
        r4_supports,
        frozenset(range(7)),
    )
    assert r3_data == r4_data
    assert r3_data[0:2] == (4, 14)
    print("PASS r1->r2 and r3(C)->r4 lifts preserve the sharp cut bound")


def main() -> None:
    verify_case("r2", REPAIRS["r2"])
    verify_case("r4", REPAIRS["r4"])
    verify_lift_invariance()
    print(
        "SCOPE: these four explicit prefix certificates; no universal "
        "switching or fan-realizability theorem"
    )


if __name__ == "__main__":
    main()

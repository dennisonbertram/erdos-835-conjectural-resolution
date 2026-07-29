#!/usr/bin/env python3
"""Finite arithmetic checks for the independent r=0 cut-cover theorem."""

from __future__ import annotations

from itertools import combinations, product
from math import comb


ROWS = frozenset(range(7))
TRIPLES = tuple(frozenset(t) for t in combinations(ROWS, 3))


def six_family(a_set: frozenset[int], g_value: int) -> frozenset[frozenset[int]]:
    """Triples obstructed by a six-cut with residual edge count g_value."""
    return frozenset(t for t in TRIPLES if len(t & a_set) > g_value)


def seven_family(
    a_set: frozenset[int],
    b_set: frozenset[int],
    g_value: int,
) -> frozenset[frozenset[int]]:
    """Triples obstructed by a seven-cut."""
    return frozenset(
        t for t in TRIPLES if 2 * len(t & a_set) + len(t & b_set) > g_value
    )


def all_subsets(
    universe: frozenset[int],
    maximum_size: int | None = None,
) -> tuple[frozenset[int], ...]:
    """Return all subsets, optionally with a cardinality cap."""
    cap = len(universe) if maximum_size is None else maximum_size
    return tuple(
        frozenset(choice)
        for size in range(cap + 1)
        for choice in combinations(universe, size)
    )


def check_source_and_cut_catalogue() -> None:
    assert sum((4, 4, 4, 5, 5, 5)) == 27
    assert 7 * 3 + 4 * 5 == 2 * 27 - 13 == 41

    # The degree lower bound and automatic large cuts.
    lower_bounds = {}
    for size in range(6, 14):
        numerator = size * (size - 6)
        lower_bounds[size] = (numerator + 1) // 2
    assert lower_bounds == {6: 0, 7: 4, 8: 8, 9: 14, 10: 20, 11: 28, 12: 36, 13: 46}
    assert all(lower_bounds[size] >= 3 * (size - 5) for size in range(9, 14))

    # Directly enumerate the intersection-size patterns of the three rows.
    intersections = tuple(product(range(4), repeat=3))
    for g_value in range(3):
        for pattern in intersections:
            demand = sum(max(0, 1 - value) for value in pattern)
            assert (demand > g_value) == (pattern.count(0) > g_value)

    for g_value in (4, 5):
        for pattern in intersections:
            demand = sum(max(0, 2 - value) for value in pattern)
            types = tuple("A" if value == 0 else "B" if value == 1 else "O" for value in pattern)
            expected = (
                (types.count("A") == 3 or (types.count("A") == 2 and types.count("B") == 1))
                if g_value == 4
                else types.count("A") == 3
            )
            assert (demand > g_value) == expected

    for pattern in intersections:
        demand = sum(max(0, 3 - value) for value in pattern)
        assert (demand > 8) == (pattern == (0, 0, 0))


def check_overlap_arithmetic() -> None:
    six_six = [5 * k + 2 * comb(6 - k, 2) for k in range(1, 6)]
    assert six_six == [25, 22, 21, 22, 25]
    assert max(six_six) < 26

    seven_seven = [5 * k + 2 * comb(7 - k, 2) for k in range(1, 7)]
    assert seven_seven == [35, 30, 27, 26, 27, 30]
    assert max(seven_seven[1:]) < 32

    six_seven_middle = [
        5 * k + comb(6 - k, 2) + comb(7 - k, 2) for k in range(2, 6)
    ]
    assert six_seven_middle == [26, 24, 24, 26]
    assert max(six_seven_middle) < 29

    feasible_at_six = {
        (g_six, g_seven)
        for g_six in range(3)
        for g_seven in (4, 5)
        if 36 - g_six - g_seven <= 30
    }
    assert feasible_at_six == {(1, 5), (2, 4), (2, 5)}

    # Separated tight-eight maxima.  These are deliberately coarse where
    # the total seven-edge budget on the complementary five-set is stronger.
    six_maxima = [10, 7, 6, 7, 10, 11]
    seven_maxima = [11, 9, 9, 11, 11, 15]
    assert max(six_maxima) < 13
    assert max(seven_maxima) < 16


def check_row_budgets() -> None:
    g4_values = []
    g5_values = []
    for a_size in range(8):
        for b_size in range(8 - a_size):
            if 3 * a_size + 2 * b_size <= 14:
                covered = comb(a_size, 3) + comb(a_size, 2) * b_size
                g4_values.append((covered, a_size, b_size))
            if 3 * a_size + 2 * b_size <= 16:
                g5_values.append((comb(a_size, 3), a_size, b_size))
    assert max(g4_values) == (10, 4, 1)
    assert max(value[0] for value in g5_values) == 10
    assert max(value[1] for value in g5_values) == 5

    # A tight eight-cut forces at least twelve triple incidences on the cut.
    assert max(a_size for a_size in range(8) if 3 * (7 - a_size) >= 12) == 3

    # Complement-side budget 3|A_U| <= 17 + 2g - c.
    assert [((17 + 2 * g_value) // 3) for g_value in range(3)] == [5, 6, 7]
    assert (17 + 2 * 1 - 2) // 3 == 5


def check_fixed_prefix_cover() -> None:
    all_sets = all_subsets(ROWS)

    # Verify the exact all-cover thresholds in the three six-cut classes.
    thresholds = {}
    for g_value in range(3):
        thresholds[g_value] = min(
            len(a_set)
            for a_set in all_sets
            if len(six_family(a_set, g_value)) == len(TRIPLES)
        )
    assert thresholds == {0: 5, 1: 6, 2: 7}

    # A non-all-cover g=0 cut is alone and misses at least one row triple.
    max_g0 = max(
        len(six_family(a_set, 0)) for a_set in all_sets if len(a_set) <= 4
    )
    assert max_g0 == 34

    # A g=1 cut can coexist only with a disjoint g=2 cut.  A coexisting
    # seven-cut has g=5 and A_7 subset A_1, hence adds no new family.
    max_g1_g2 = 0
    for a_one in all_sets:
        if len(a_one) > 5:
            continue
        remaining = ROWS - a_one
        for a_two in all_subsets(remaining, 6):
            family = six_family(a_one, 1) | six_family(a_two, 2)
            max_g1_g2 = max(max_g1_g2, len(family))
    assert max_g1_g2 == 30

    # If every critical six-cut has g=2, disjoint A-sets of total size at
    # most seven cover at most C(6,3)=20; the unique seven-cut adds <=10.
    max_g2_only = 0
    for a_first in all_sets:
        if len(a_first) > 6:
            continue
        remaining = ROWS - a_first
        for a_second in all_subsets(remaining, 6):
            family = six_family(a_first, 2) | six_family(a_second, 2)
            max_g2_only = max(max_g2_only, len(family))
    assert max_g2_only == 20
    assert max_g2_only + 10 == 30

    # Check the seven-cut family bounds directly over labelled occurrence
    # sets satisfying the sharp row budgets.
    max_g4 = 0
    max_g5 = 0
    for a_set in all_sets:
        for b_set in all_subsets(ROWS - a_set):
            if 3 * len(a_set) + 2 * len(b_set) <= 14:
                max_g4 = max(max_g4, len(seven_family(a_set, b_set, 4)))
            if 3 * len(a_set) + 2 * len(b_set) <= 16:
                max_g5 = max(max_g5, len(seven_family(a_set, b_set, 5)))
    assert (max_g4, max_g5) == (10, 10)

    fixed_prefix_max = max(max_g0, max_g1_g2, max_g2_only + max_g4)
    assert fixed_prefix_max == 34 < len(TRIPLES)


def main() -> None:
    check_source_and_cut_catalogue()
    check_overlap_arithmetic()
    check_row_budgets()
    check_fixed_prefix_cover()
    print("independent cut-cover arithmetic: PASS")
    print("35 row triples; maximum relaxed obstruction cover without an all-cover six-cut: 34")
    print("remaining theorem gap: cut sufficiency / prescribed three-colour factor")


if __name__ == "__main__":
    main()

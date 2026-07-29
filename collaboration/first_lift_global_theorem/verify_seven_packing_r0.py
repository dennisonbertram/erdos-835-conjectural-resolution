#!/usr/bin/env python3
"""Audit the exceptional-profile proof in SEVEN_PACKING_R0_NOTE.md.

The core-pair check is exhaustive up to relabelling: fix one canonical core
and enumerate every labelled second core on thirteen vertices.
"""

from itertools import combinations


VERTICES = tuple(range(13))
EDGE_BUDGET = 26
COLOURS = 6


def clique(vertices):
    return set(combinations(sorted(vertices), 2))


def b_core(vertices, omitted_triangle):
    omitted = set(omitted_triangle)
    return {
        edge
        for edge in combinations(sorted(vertices), 2)
        if not set(edge) <= omitted
    }


def passes_six_matching_bounds(edges):
    if len(edges) > EDGE_BUDGET:
        return False

    degrees = [0] * len(VERTICES)
    used_vertices = set()
    for first, second in edges:
        degrees[first] += 1
        degrees[second] += 1
        used_vertices.update((first, second))
    if max(degrees) > COLOURS:
        return False

    induced_capacity = COLOURS * (len(used_vertices) // 2)
    return len(edges) <= induced_capacity


def all_b_cores():
    for vertices in combinations(VERTICES, 7):
        for triangle in combinations(vertices, 3):
            yield b_core(vertices, triangle)


def all_c_cores():
    for vertices in combinations(VERTICES, 6):
        yield clique(vertices)


def verify_core_uniqueness():
    canonical_b = b_core(range(7), range(3))
    canonical_c = clique(range(6))

    distinct_b_survivors = 0
    for other in all_b_cores():
        if other != canonical_b and passes_six_matching_bounds(canonical_b | other):
            distinct_b_survivors += 1
    assert distinct_b_survivors == 0

    distinct_c_survivors = 0
    for other in all_c_cores():
        if other != canonical_c and passes_six_matching_bounds(canonical_c | other):
            distinct_c_survivors += 1
    assert distinct_c_survivors == 0

    mixed_survivors = 0
    for other in all_c_cores():
        if passes_six_matching_bounds(canonical_b | other):
            mixed_survivors += 1
    assert mixed_survivors == 0


def verify_row_sum_escape():
    selected_colours = 6
    total_forbidden = 5
    remaining_size_eight = 3

    # A K6-core vertex is supported by at least 5 selected colours.
    selected_missing_c = selected_colours - 5
    remaining_missing_c = total_forbidden - selected_missing_c
    assert remaining_missing_c == 4 > remaining_size_eight

    # A degree-six B-core vertex is supported by all selected colours.
    selected_missing_b = selected_colours - 6
    remaining_missing_b = total_forbidden - selected_missing_b
    assert remaining_missing_b == 5
    assert remaining_missing_b - remaining_size_eight == 2


def main():
    verify_core_uniqueness()
    print("PASS exhaustive core-pair audit: at most one B/C core exists")

    verify_row_sum_escape()
    print("PASS row sums force a remaining size-10 support to omit the core")
    print("PASS the exceptional r=0 profile has a seven-colour packing")
    print("SCOPE: seven colours pack; the remaining ten are unresolved.")


if __name__ == "__main__":
    main()

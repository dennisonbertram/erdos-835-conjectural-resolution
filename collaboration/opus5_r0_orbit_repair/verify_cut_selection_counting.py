#!/usr/bin/env python3
"""Check every finite arithmetic table in the r=0 cut-selection theorem."""

from __future__ import annotations

from math import comb


def compatible_intersections(
    first_size: int,
    first_edges: int,
    second_size: int,
    second_edges: int,
    *,
    same_type: bool = False,
) -> list[int]:
    """Return intersections not excluded by the edge and degree ledgers."""
    result = []
    lower = max(0, first_size + second_size - 13)
    for intersection in range(lower, min(first_size, second_size) + 1):
        if first_size == second_size and intersection == first_size:
            continue
        if comb(intersection, 2) < first_edges + second_edges - 27:
            continue
        degree_rhs = (
            first_edges
            + second_edges
            - comb(first_size - intersection, 2)
            - comb(second_size - intersection, 2)
        )
        if 5 * intersection < degree_rhs:
            continue
        result.append(intersection)
    return result


def main() -> None:
    dense_maximum = max(
        comb(a, 3) + comb(b, 3)
        for a in range(6)
        for b in range(6)
        if a + b <= 7
    )
    assert dense_maximum == 10

    seven_overlap = [
        5 * k + 2 * comb(7 - k, 2)
        for k in range(1, 7)
    ]
    assert seven_overlap == [35, 30, 27, 26, 27, 30]

    seventeen_cover = max(
        comb(a, 3) + comb(a, 2) * b
        for a in range(5)
        for b in range(8 - a)
    )
    assert seventeen_cover == 22
    assert dense_maximum + seventeen_cover + 1 == 33

    assert compatible_intersections(6, 13, 6, 13, same_type=True) == [0]
    assert compatible_intersections(6, 13, 7, 17) == [6]
    assert compatible_intersections(6, 13, 7, 16) == [6]
    assert compatible_intersections(6, 13, 8, 20) == []
    assert compatible_intersections(7, 17, 7, 17, same_type=True) == []
    assert compatible_intersections(7, 17, 7, 16) == []
    assert compatible_intersections(7, 16, 7, 16, same_type=True) == []
    assert compatible_intersections(7, 17, 8, 20) == []
    assert compatible_intersections(7, 16, 8, 20) == []

    six_seven_overlap = [
        5 * k + comb(6 - k, 2) + comb(7 - k, 2)
        for k in range(7)
    ]
    assert six_seven_overlap == [36, 30, 26, 24, 24, 26, 30]

    independent_counts = [
        comb(7, 3) - comb(t, 2) * (7 - t) - comb(t, 3)
        for t in range(1, 6)
    ]
    assert independent_counts == [35, 30, 22, 13, 5]

    nested_dense_seventeen = max(
        comb(a, 3) + comb(a - mu, 2) * nu
        for a in range(6)
        for mu in range(a + 1)
        for nu in range(8 - a)
        for crossing in range(2)
        if 3 * a - mu + 2 * nu <= 14 - crossing
    )
    assert nested_dense_seventeen == 11

    print("PASS r=0 cut-selection counting arithmetic")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact checks for the Hoffman/intersection/Odd-cover audit.

The script checks only finite arithmetic and elementary subset geometry.  It
does not search for, or certify the nonexistence of, a full colouring.
"""

from fractions import Fraction
from itertools import combinations
from math import comb


def intersection_distribution(k: int) -> list[Fraction]:
    """Return (m_0,...,m_{k-1}) from the binomial inversion in the note."""
    b = k - 1
    lambdas = [
        (
            Fraction(comb(2 * k - 1 - j, k - 2 - j), k - 1 - j)
            if j < b
            else Fraction(1)
        )
        for j in range(b + 1)
    ]
    return [
        Fraction(comb(b, r))
        * sum(
            (
                Fraction((-1) ** (j - r) * comb(b - r, j - r))
                * lambdas[j]
            )
            for j in range(r, b + 1)
        )
        for r in range(b + 1)
    ]


def neighbours(vertex: frozenset[int], points: frozenset[int]):
    """Neighbours in KG(2k-1,k-1)."""
    size = len(vertex)
    for candidate in combinations(points - vertex, size):
        yield frozenset(candidate)


def length_three_paths(
    start: frozenset[int],
    end: frozenset[int],
    points: frozenset[int],
) -> list[tuple[frozenset[int], ...]]:
    """Enumerate simple length-three paths with fixed endpoints."""
    paths = []
    for first in neighbours(start, points):
        for second in neighbours(first, points):
            if second == start or end not in set(neighbours(second, points)):
                continue
            paths.append((start, first, second, end))
    return paths


def check_nonreversal_pairing() -> None:
    """The proved coordinate inequalities do not force reversal."""
    pairs = [(("0", "1"), ("1", "2")),
             (("0", "2"), ("2", "0")),
             (("1", "0"), ("2", "1"))]
    directed = {edge for pair in pairs for edge in pair}
    assert directed == {
        (a, b) for a in "012" for b in "012" if a != b
    }
    assert all(left[0] != right[0] and left[1] != right[1]
               for left, right in pairs)
    assert any(right != left[::-1] for left, right in pairs)


def main() -> None:
    expected = {
        2: [0, 1],
        4: [0, 6, 0, 1],
        6: [0, 15, 20, 30, 0, 1],
        16: [
            0, 120, 3360, 49140, 349440, 1417416, 3363360, 4877730,
            4324320, 2362360, 768768, 147420, 14560, 840, 0, 1,
        ],
    }
    for k, target in expected.items():
        distribution = intersection_distribution(k)
        assert distribution == target
        assert distribution[0] == 0
        assert distribution[1] == comb(k, 2)
        assert sum(distribution) == Fraction(comb(2 * k - 1, k - 1), k + 1)
        total_intersection_two = comb(k, 2) * (k - 1)
        per_other_colour = (
            total_intersection_two - distribution[1]
        ) // k
        assert per_other_colour == comb(k - 1, 2)

    # Canonical endpoints with one common point have exactly the two paths
    # displayed in the note.  k=4 and k=6 are small independent controls.
    for k in (4, 6):
        points = frozenset(range(2 * k - 1))
        start = frozenset(range(k - 1))
        end = frozenset([0, *range(k - 1, 2 * k - 3)])
        assert start & end == {0}
        paths = length_three_paths(start, end, points)
        assert len(paths) == 2
        assert all(len(set(path)) == 4 for path in paths)

    check_nonreversal_pairing()

    fibre_size = comb(31, 15) // 17
    assert fibre_size == 17_678_835 and fibre_size % 2 == 1
    assert comb(15, 2) == 105 and comb(15, 2) % 2 == 1

    print("PASS: exact intersection, two-geodesic, and parity controls")
    print("STATUS: necessary conditions only; no nonexistence proof")


if __name__ == "__main__":
    main()

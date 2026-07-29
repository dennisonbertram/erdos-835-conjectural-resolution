#!/usr/bin/env python3
"""Dependency-free description of the exterior-S5-symmetric N=0 model."""

from __future__ import annotations

import itertools
from collections import Counter
from collections.abc import Iterable


V = tuple(range(13))
CUBE = tuple(range(8))
OUTSIDE = tuple(range(8, 13))
PAIRS = ((0, 1), (2, 3), (4, 5), (6, 7))

# q*N + sign*D = rhs, where D is the raw d-mass on the subset.
RECURRENCE = {
    5: (2, 1, 13),
    6: (3, -1, 39),
    7: (4, 1, 195),
    8: (5, -1, 325),
    9: (6, 1, 702),
    10: (7, -1, 546),
    11: (8, 1, 858),
}


OrbitKey = tuple[tuple[int, ...], int]


def orbit_key(block: Iterable[int]) -> OrbitKey:
    """Return (cube part, number of exterior points)."""
    block_tuple = tuple(sorted(block))
    cube_part = tuple(x for x in block_tuple if x in CUBE)
    return cube_part, len(block_tuple) - len(cube_part)


def canonical_representatives(size: int) -> tuple[tuple[int, ...], ...]:
    """One subset representative per orbit of the exterior S5 action."""
    answer = []
    for outside_count in range(6):
        cube_count = size - outside_count
        if 0 <= cube_count <= 8:
            outside_part = OUTSIDE[:outside_count]
            for cube_part in itertools.combinations(CUBE, cube_count):
                answer.append(tuple(sorted((*cube_part, *outside_part))))
    return tuple(answer)


def orbit_keys() -> tuple[OrbitKey, ...]:
    """The 163 orbits of four-subsets under exterior S5."""
    return tuple(
        sorted(
            {
                orbit_key(block)
                for block in itertools.combinations(V, 4)
            }
        )
    )


def coefficient_signature(
    subsets: Iterable[tuple[int, ...]],
) -> tuple[tuple[OrbitKey, int], ...]:
    """Collapse a multiset of four-subsets into orbit coefficients."""
    counts = Counter(orbit_key(block) for block in subsets)
    return tuple(sorted(counts.items()))


def load_signature(triple: tuple[int, ...]) -> tuple[tuple[OrbitKey, int], ...]:
    """Orbit-variable coefficients in the triple load L_T."""
    triple_set = set(triple)
    return coefficient_signature(
        block
        for block in itertools.combinations(V, 4)
        if triple_set.issubset(block)
    )


def subset_signature(subset: tuple[int, ...]) -> tuple[tuple[OrbitKey, int], ...]:
    """Orbit-variable coefficients in D_S=sum_{Q subset S} d_Q."""
    return coefficient_signature(itertools.combinations(subset, 4))


def cube_cells() -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
]:
    """Return the positive and negative cells of the normalized four-cube."""
    positive = []
    negative = []
    for bits in itertools.product((0, 1), repeat=4):
        block = tuple(sorted(PAIRS[i][bits[i]] for i in range(4)))
        (positive if sum(bits) % 2 == 0 else negative).append(block)
    return tuple(positive), tuple(negative)


def model_statistics() -> dict[str, object]:
    recurrence_counts = {
        size: len(canonical_representatives(size))
        for size in RECURRENCE
    }
    return {
        "d_orbits": len(orbit_keys()),
        "triple_orbits": len(canonical_representatives(3)),
        "recurrence_orbits": recurrence_counts,
        "recurrence_total": sum(recurrence_counts.values()),
        "integer_variables": len(orbit_keys()) + sum(recurrence_counts.values()),
        "constraints": (
            len(canonical_representatives(3))
            + sum(recurrence_counts.values())
            + 2
        ),
    }


def main() -> None:
    stats = model_statistics()
    print(f"d_orbits: {stats['d_orbits']}")
    print(f"triple_orbits: {stats['triple_orbits']}")
    print(f"recurrence_orbits: {stats['recurrence_orbits']}")
    print(f"recurrence_total: {stats['recurrence_total']}")
    print(f"integer_variables: {stats['integer_variables']}")
    print(f"constraints: {stats['constraints']}")


if __name__ == "__main__":
    main()

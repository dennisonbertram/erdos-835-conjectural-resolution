#!/usr/bin/env python3
"""Independent finite check for the k=4 case of Erdős Problem #835.

A 5-colouring of J(8,4) at the clique lower bound would partition the
70 four-subsets of an eight-set into five Steiner systems S(3,4,8).
There is one S(3,4,8) up to relabelling: the affine planes of F_2^3.
This script generates all 30 labelled copies and checks every 5-tuple.
"""

from itertools import combinations, permutations
from typing import Optional, Tuple


POINTS = tuple(range(8))
FOUR_SETS = tuple(combinations(POINTS, 4))
FOUR_SET_INDEX = {block: index for index, block in enumerate(FOUR_SETS)}
FULL_MASK = (1 << len(FOUR_SETS)) - 1


def xor_sum(block: tuple[int, ...]) -> int:
    value = 0
    for point in block:
        value ^= point
    return value


BASE_BLOCKS = tuple(block for block in FOUR_SETS if xor_sum(block) == 0)


def relabelled_mask(permutation: tuple[int, ...]) -> int:
    mask = 0
    for block in BASE_BLOCKS:
        image = tuple(sorted(permutation[point] for point in block))
        mask |= 1 << FOUR_SET_INDEX[image]
    return mask


def labelled_systems() -> tuple[int, ...]:
    return tuple(sorted({relabelled_mask(p) for p in permutations(POINTS)}))


def find_partition(systems: Tuple[int, ...]) -> Optional[Tuple[int, ...]]:
    # Fix the first system by transitivity under relabelling.  Any partition
    # can be relabelled so that one of its systems is systems[0].
    chosen = [0]

    def search(start: int, union: int) -> Optional[Tuple[int, ...]]:
        if len(chosen) == 5:
            return tuple(chosen) if union == FULL_MASK else None

        for index in range(start, len(systems)):
            candidate = systems[index]
            if union & candidate:
                continue
            chosen.append(index)
            result = search(index + 1, union | candidate)
            if result is not None:
                return result
            chosen.pop()
        return None

    return search(1, systems[0])


def maximum_disjoint_family(systems: Tuple[int, ...]) -> Tuple[int, ...]:
    """Return indices of a largest pairwise block-disjoint family."""
    best: Tuple[int, ...] = ()

    def search(
        start: int, chosen: Tuple[int, ...], union: int
    ) -> None:
        nonlocal best
        if len(chosen) > len(best):
            best = chosen

        # Even if every remaining system could be used, this branch cannot
        # improve the incumbent.
        if len(chosen) + len(systems) - start <= len(best):
            return

        for index in range(start, len(systems)):
            candidate = systems[index]
            if union & candidate:
                continue
            search(index + 1, chosen + (index,), union | candidate)

    search(0, (), 0)
    return best


def main() -> None:
    systems = labelled_systems()
    assert len(BASE_BLOCKS) == 14
    assert len(systems) == 30
    assert all(bin(mask).count("1") == 14 for mask in systems)

    partition = find_partition(systems)
    maximum_family = maximum_disjoint_family(systems)
    print(f"labelled S(3,4,8) systems: {len(systems)}")
    print(f"blocks per system: {len(BASE_BLOCKS)}")
    print(f"maximum pairwise disjoint systems: {len(maximum_family)}")
    print(f"partition into five systems: {partition}")
    assert len(maximum_family) == 2
    assert partition is None
    print("conclusion: no 5-colouring exists for k=4")


if __name__ == "__main__":
    main()

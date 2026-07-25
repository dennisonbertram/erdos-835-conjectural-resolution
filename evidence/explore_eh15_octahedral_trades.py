#!/usr/bin/env python3
"""Enumerate 8+8 octahedral S(3,4) trades in the EH 15-system core.

For four disjoint point-pairs, the eight even and eight odd transversals
have identical triple incidence.  Replacing one side by the other inside a
Steiner quadruple system therefore preserves the SQS property.  This script
checks whether such trades can move the rigid Etzion--Hartman near-solution
while retaining fifteen pairwise disjoint systems.

This is exploratory; absence of these small trades is not a universal
obstruction.
"""

from __future__ import annotations

import itertools

from generate_eh_15_seed import etzion_hartman_systems


def transversals(
    first: tuple[int, ...],
    second: tuple[int, ...],
) -> tuple[frozenset[tuple[int, ...]], frozenset[tuple[int, ...]]]:
    even = set()
    odd = set()
    for bits in itertools.product(range(2), repeat=4):
        block = tuple(sorted(
            (first[i], second[i])[bits[i]]
            for i in range(4)
        ))
        (odd if sum(bits) & 1 else even).add(block)
    return frozenset(even), frozenset(odd)


def trades_in(
    system: set[tuple[int, ...]],
) -> set[tuple[frozenset[tuple[int, ...]], frozenset[tuple[int, ...]]]]:
    blocks = sorted(system)
    answer = set()
    for left_index, left in enumerate(blocks):
        left_set = set(left)
        for right in blocks[left_index + 1:]:
            if left_set & set(right):
                continue
            for permutation in itertools.permutations(right):
                even, odd = transversals(left, permutation)
                if even <= system:
                    answer.add((even, odd))
                if odd <= system:
                    answer.add((odd, even))
    return answer


def main() -> None:
    systems = etzion_hartman_systems()
    used = set().union(*systems)
    total = 0
    usable = 0
    for colour, system in enumerate(systems):
        trades = trades_in(system)
        available = [
            trade for trade in trades
            if not ((trade[1] - trade[0]) & used)
        ]
        total += len(trades)
        usable += len(available)
        print(
            f"colour {colour}: {len(trades)} octahedral trades, "
            f"{len(available)} preserve disjointness"
        )
    print(f"total trades {total}; initially usable {usable}")


if __name__ == "__main__":
    main()

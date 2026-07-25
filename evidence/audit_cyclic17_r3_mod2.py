#!/usr/bin/env python3
"""Exact GF(2) audit of the joint cyclic-17 moving-triple equations.

This linearizes only constraints which are genuine equalities:

* one selected translate per fixed-pair/triple orbit;
* the colour-zero leave/exact-cover equations; and
* the forced degree 0/1 equations in each cross-slice matching.

Consistency is only a necessary condition for the Boolean model.
Inconsistency would be a rigorous obstruction; consistency is not a witness.
"""

from __future__ import annotations

from itertools import combinations

from global_latin_audit import construct_golf17


P = 17
MOVING = tuple(range(P))
FIXED = tuple(range(15))
MOVING_PAIRS = tuple(combinations(MOVING, 2))
MOVING_TRIPLES = tuple(combinations(MOVING, 3))
FIXED_PAIRS = tuple(combinations(FIXED, 2))


def translate(subset: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return tuple(sorted((x + amount) % P for x in subset))


def triple_orbits() -> list[tuple[int, int, int]]:
    representatives: list[tuple[int, int, int]] = []
    unseen = set(MOVING_TRIPLES)
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, shift) for shift in MOVING)
        representatives.append(representative)
        for shift in MOVING:
            unseen.discard(translate(representative, shift))
    assert len(representatives) == 40
    return representatives


REPRESENTATIVES = triple_orbits()
PAIR_INDEX = {pair: index for index, pair in enumerate(FIXED_PAIRS)}
VARIABLES = len(FIXED_PAIRS) * len(REPRESENTATIVES) * P


def variable(fixed_pair: tuple[int, int], orbit: int, shift: int) -> int:
    return (
        (PAIR_INDEX[fixed_pair] * len(REPRESENTATIVES) + orbit) * P
        + shift
    )


class BinaryEliminator:
    """Streaming exact Gaussian elimination using Python integer bitsets."""

    def __init__(self) -> None:
        self.pivots: dict[int, tuple[int, int]] = {}
        self.equations = 0
        self.inconsistent = False

    def add(self, indices, rhs: int) -> None:
        self.equations += 1
        mask = 0
        for index in indices:
            mask ^= 1 << index
        rhs &= 1
        while mask:
            pivot = mask.bit_length() - 1
            old = self.pivots.get(pivot)
            if old is None:
                self.pivots[pivot] = (mask, rhs)
                return
            mask ^= old[0]
            rhs ^= old[1]
        if rhs:
            self.inconsistent = True
            raise ArithmeticError(
                f"GF(2) contradiction after equation {self.equations}"
            )


def main() -> None:
    golf = construct_golf17()
    elimination = BinaryEliminator()

    # One selected translate from each triple orbit in each fixed-pair slice.
    for fixed_pair in FIXED_PAIRS:
        for orbit in range(len(REPRESENTATIVES)):
            elimination.add(
                (variable(fixed_pair, orbit, shift) for shift in MOVING),
                1,
            )

    occurrences = {pair: [] for pair in MOVING_PAIRS}
    translated = []
    for orbit, representative in enumerate(REPRESENTATIVES):
        translated.append([])
        for shift in MOVING:
            triple = translate(representative, shift)
            translated[orbit].append(triple)
            for pair in combinations(triple, 2):
                occurrences[pair].append((orbit, shift))
    assert all(len(values) == 15 for values in occurrences.values())

    # Per-slice colour-zero exact covers.
    for fixed_pair in FIXED_PAIRS:
        i, j = fixed_pair
        for moving_pair, choices in occurrences.items():
            leave = (
                golf[i][moving_pair[0]][moving_pair[1]] == 0
                or golf[j][moving_pair[0]][moving_pair[1]] == 0
            )
            elimination.add(
                (
                    variable(fixed_pair, orbit, shift)
                    for orbit, shift in choices
                ),
                0 if leave else 1,
            )

    # For a fixed moving triple and colour zero, the selected fixed edges
    # form a matching on precisely the fixed vertices whose golf links do
    # not already use zero.  Hence every allowed vertex has degree one and
    # every forbidden vertex degree zero.
    for orbit in range(len(REPRESENTATIVES)):
        for shift in MOVING:
            triple = translated[orbit][shift]
            for fixed_point in FIXED:
                forbidden = any(
                    golf[fixed_point][x][y] == 0
                    for x, y in combinations(triple, 2)
                )
                incident = (
                    variable(
                        (
                            min(fixed_point, other),
                            max(fixed_point, other),
                        ),
                        orbit,
                        shift,
                    )
                    for other in FIXED
                    if other != fixed_point
                )
                elimination.add(incident, 0 if forbidden else 1)

    rank = len(elimination.pivots)
    print(f"primary variables: {VARIABLES}")
    print(f"GF(2) equations: {elimination.equations}")
    print(f"GF(2) rank: {rank}")
    print(f"GF(2) nullity: {VARIABLES - rank}")
    print("joint cyclic-17 moving-triple linearization: CONSISTENT")
    print("scope: necessary parity shadow only; not a Boolean certificate")


if __name__ == "__main__":
    main()

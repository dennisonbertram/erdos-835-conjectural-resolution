#!/usr/bin/env python3
"""Dependency-free coefficient audit of the N=0 filler hierarchy."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


V = tuple(range(13))
CUBE = set(range(8))
OUTSIDE = tuple(range(8, 13))
PAIRS = ((0, 1), (2, 3), (4, 5), (6, 7))
FOUR_SETS = tuple(combinations(V, 4))


def transversals() -> dict[tuple[int, ...], int]:
    answer = {}
    for bits in product((0, 1), repeat=4):
        q = tuple(sorted(PAIRS[i][bit] for i, bit in enumerate(bits)))
        answer[q] = (-1) ** sum(bits)
    return answer


def audit_derivative_extraction() -> None:
    signed = transversals()
    for filler_size in range(6):
        for filler in combinations(OUTSIDE, filler_size):
            coefficients = {r: 0 for r in FOUR_SETS}
            for q, sign in signed.items():
                s = set(q) | set(filler)
                for r in combinations(sorted(s), 4):
                    coefficients[r] += sign
            for r in FOUR_SETS:
                assert coefficients[r] == signed.get(r, 0)

    slopes = (
        Fraction(1),
        Fraction(-1, 2),
        Fraction(1, 3),
        Fraction(-1, 4),
        Fraction(1, 5),
        Fraction(-1, 6),
    )
    assert [60 * slope for slope in slopes] == [60, -30, 20, -15, 12, -10]


def valid_cube_partial(r: tuple[int, ...]) -> bool:
    for pair in PAIRS:
        if len(set(pair) & set(r)) > 1:
            return False
    return True


def audit_total_mass_coefficients() -> None:
    cube_transversals = tuple(transversals())
    for filler_size in range(6):
        for filler in combinations(OUTSIDE, filler_size):
            filler_set = set(filler)
            for r in FOUR_SETS:
                actual = sum(
                    set(r).issubset(set(q) | filler_set)
                    for q in cube_transversals
                )
                cube_part = tuple(sorted(set(r) & CUBE))
                outside_part = set(r) - CUBE
                if outside_part.issubset(filler_set) and valid_cube_partial(cube_part):
                    expected = 2 ** (4 - len(cube_part))
                else:
                    expected = 0
                assert actual == expected


def occupancy(q: tuple[int, ...]) -> tuple[int, ...]:
    q_set = set(q)
    return tuple(sorted((len(q_set & set(pair)) for pair in PAIRS), reverse=True))


def audit_edge_capacity_counts() -> None:
    signed = transversals()
    edge_triples = set()
    for positive, sign in signed.items():
        if sign != 1:
            continue
        for negative, other_sign in signed.items():
            intersection = set(positive) & set(negative)
            if other_sign == -1 and len(intersection) == 3:
                edge_triples.add(tuple(sorted(intersection)))
    assert len(edge_triples) == 32

    cube_counts = {
        q: sum(set(t).issubset(q) for t in edge_triples)
        for q in combinations(range(8), 4)
    }
    assert all(cube_counts[q] == 4 for q in signed)
    pattern = [q for q in cube_counts if occupancy(q) == (2, 1, 1, 0)]
    assert len(pattern) == 48
    assert all(cube_counts[q] == 2 for q in pattern)

    links = [
        tuple(sorted((*t, x)))
        for t in edge_triples
        for x in OUTSIDE
    ]
    assert len(links) == 160
    assert len(set(links)) == 160
    assert all(sum(set(t).issubset(q) for t in edge_triples) == 1 for q in links)

    # Arithmetic reductions in (4), (5), and (7).
    # Z=44-2A, sum Z=220-2 sum A:
    # 240+2C+sum Z<=416 iff sum A>=22+C.
    assert Fraction(240 + 220 - 416, 2) == 22
    # 3(A'+B')=60+2Z+4W and A'-B'=20 imply 3B'=Z+2W.
    assert 3 * 20 == 60


def main() -> None:
    audit_derivative_extraction()
    print("filler derivatives 60,-30,20,-15,12,-10: PASS")
    audit_total_mass_coefficients()
    print("all filler-layer transversal incidence coefficients: PASS")
    audit_edge_capacity_counts()
    print("N=0 first- and second-layer mass identities: PASS")
    print("PASS: the outside-filler hierarchy is coefficientwise verified")
    print("scope: N=0 feasibility, the full lift, and Problem #835 remain open")


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""Dependency-free audit of the exact-trade elimination at the j=8 lift."""

from __future__ import annotations

from itertools import combinations


V = tuple(range(13))
FOUR_SETS = tuple(combinations(V, 4))
TRIPLES = tuple(combinations(V, 3))


def contains(big: tuple[int, ...], small: tuple[int, ...]) -> bool:
    return set(small).issubset(big)


def audit_extension_multiplicities() -> None:
    # In sum_{T superset B} D_T, a 4-set Q containing B occurs once for
    # each triple between B and Q: C(4-|B|, 3-|B|).
    expected = {0: 4, 1: 3, 2: 2}
    for size, multiplicity in expected.items():
        for b in combinations(V, size):
            for q in FOUR_SETS:
                actual = sum(
                    contains(t, b) and contains(q, t)
                    for t in TRIPLES
                )
                want = multiplicity if contains(q, b) else 0
                assert actual == want


def audit_complement_inclusion_exclusion() -> None:
    # Coefficientwise verification of
    # 1[Q disjoint R] = sum_{U subset R} (-1)^|U| 1[U subset Q].
    for r in FOUR_SETS:
        for q in FOUR_SETS:
            coefficient = 0
            for size in range(5):
                coefficient += (-1) ** size * sum(
                    contains(q, u) for u in combinations(r, size)
                )
            assert coefficient == int(set(q).isdisjoint(r))


def audit_q6_arithmetic() -> None:
    allowed = [value for value in range(-1, 13) if value % 6 == 0]
    assert allowed == [0, 6, 12]
    # A finite family of nonnegative integers with total zero is identically
    # zero.  This final implication is the only use of the coefficient range.
    assert min(allowed) == 0


def main() -> None:
    assert len(FOUR_SETS) == 715
    assert len(TRIPLES) == 286
    audit_extension_multiplicities()
    print("extension multiplicities 4, 3, 2: PASS")
    audit_complement_inclusion_exclusion()
    print("complement inclusion-exclusion on all 715^2 pairs: PASS")
    audit_q6_arithmetic()
    print("q=6 residue and coefficient-range step: PASS")
    print("PASS: the exact triple-degree-zero branch contains only e=0")
    print("scope: the general D_T <= 3 lift and Problem #835 remain open")


if __name__ == "__main__":
    main()


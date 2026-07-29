#!/usr/bin/env python3
"""Exact checks for r15_second_moment_incidence_tautology.md.

The proof in the note is symbolic.  This script independently checks:

1. every entry of
       N^T N = C(r,2) I + (r-1) A1 + A2
   for the manageable complete universes r=3 and r=5;
2. the coefficient parities in the combined formula for r=3,5,15;
3. the claimed Mersenne-parameter parity for several symbolic controls.

No existence of an S(14,15,31) or of mates at r=15 is assumed.
"""

from itertools import combinations
from math import comb


def check_matrix_entries(r):
    v = 2 * r + 1
    hs = list(combinations(range(v), r + 1))
    checked = 0
    for H in hs:
        h = set(H)
        for K in hs:
            k = set(K)
            union_size = len(h | k)
            actual = (
                comb(v - union_size, r + 3 - union_size)
                if union_size <= r + 3
                else 0
            )
            intersection = len(h & k)
            expected = 0
            if H == K:
                expected = comb(r, 2)
            elif intersection == r:
                expected = r - 1
            elif intersection == r - 1:
                expected = 1
            assert actual == expected, (r, H, K, actual, expected)
            checked += 1
    print(f"[r={r}] integer N^T N identity: PASS ({checked} entries)")


def parameter_row(r):
    v = 2 * r + 1
    mu = (r + 3) // 2
    n_rows = comb(v, r + 3)
    assert comb(v, r - 1) % r == 0
    b = comb(v, r - 1) // r
    containment_term = (mu * mu * n_rows) & 1
    diagonal_coefficient = comb(r, 2) & 1

    # Formula: E3+X3 = containment_term
    #                    + diagonal_coefficient * (b-t)  (mod 2).
    values = []
    for t in (0, 1):
        combined = (
            containment_term + diagonal_coefficient * ((b - t) & 1)
        ) & 1
        values.append(combined)

    print(
        f"[r={r}] mu={mu}, C(v,r+3)%2={n_rows & 1}, "
        f"C(r,2)%2={diagonal_coefficient}, b%2={b & 1}, "
        f"(combined at t=0,1)={tuple(values)}"
    )
    return containment_term, diagonal_coefficient, b & 1, tuple(values)


def main():
    check_matrix_entries(3)
    check_matrix_entries(5)

    r3 = parameter_row(3)
    r5 = parameter_row(5)
    r15 = parameter_row(15)
    assert r3 == (1, 1, 1, (0, 1))
    assert r5 == (0, 0, 0, (0, 0))
    assert r15 == (1, 1, 1, (0, 1))

    for s in range(2, 8):
        r = (1 << s) - 1
        first, diagonal, b_parity, values = parameter_row(r)
        assert (first, diagonal, b_parity, values) == (1, 1, 1, (0, 1))
    print("Mersenne-family tautology: PASS")
    print("second-moment incidence audit: PASS")


if __name__ == "__main__":
    main()

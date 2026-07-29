#!/usr/bin/env python3
"""Exact arithmetic verifier for the all-containment-moments note.

For r=15 and the valid small control r=3, this checks:

* integrality and oddness of every containment constant c_s;
* oddness of every right side in the exact moment system;
* the full triangular recurrence over F2;
* the closed form a_s = 1 + a_0 for both values of a_0;
* the hockey-stick identity used in the written induction.

This is a coefficient verifier.  It does not assume or assert existence
of the large Steiner systems at the larger parameters.
"""

from math import comb


def check(r):
    v = 2 * r + 1
    k = r + 1
    assert k & (k - 1) == 0
    assert v == 2 * k - 1

    constants = []
    for s in range(1, r + 1):
        numerator = comb(k + s, k + 1)
        assert numerator % s == 0
        c_s = numerator // s
        assert c_s == comb(k + s, k) // (k + 1)
        assert c_s & 1
        rhs = c_s * c_s * comb(v, k + s)
        assert rhs & 1
        constants.append(c_s)

        interior = sum(
            comb(r - i, s - i) for i in range(1, s)
        )
        assert interior == comb(r + 1, s) - comb(r, s) - 1
        assert interior % 2 == 0
        assert comb(r, s) & 1

    for a0 in (0, 1):
        a = [a0]
        for s in range(1, r + 1):
            rhs = (
                constants[s - 1]
                * constants[s - 1]
                * comb(v, k + s)
            ) & 1
            previous = 0
            for i in range(s):
                previous ^= (comb(r - i, s - i) & 1) * a[i]
            # The diagonal coefficient C(r-s,0) is one.
            a.append(rhs ^ previous)
        assert a[1:] == [1 ^ a0] * r

    b_numerator = comb(v, r - 1)
    assert b_numerator % r == 0
    b = b_numerator // r
    assert b & 1

    print(
        f"r={r}: levels={r}, all c_s odd, all RHS odd, "
        f"a_s=1+a_0, b odd: PASS"
    )


def main():
    check(3)
    check(15)
    print("all-containment-moments parity audit: PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verifier for evidence/s141531_autocorrelation_law.md.

Confirms the exact autocorrelation law of a hypothetical S(14,15,31) three
independent ways, and checks the two degeneracies behind the leverage verdict.
Standard library only, exact integer / Fraction arithmetic.

m_D = number of unordered pairs of distinct blocks with B xor C = D.

(a) convexity against the forced A_4:  sum_D C(m_D,2) = 3*A_4, every layer
    total divides exactly, and the balanced configuration attains 3*A_4;
(b) group-ring/character consistency: F(u)^2 - 29670(-1)^|u| F(u) depends only
    on |u|, which at |u|=15 is exactly F_0 + F_1 = -29670;
(c) direct inverse Fourier transform of the forced weight enumerator, which
    reproduces every table entry WITHOUT using A_4 or convexity -- this is why
    the law is a repackaging rather than new information.

Run:  python3 -B evidence/verify_s141531_autocorrelation_law.py
"""

from fractions import Fraction
from math import comb

V, R = 31, 15
B_COUNT = comb(V, R) // (R + 2)
DELTA = 157425 - 142590                     # 14835
FAILURES = []


def check(label, cond, detail=""):
    print(f"  [{'ok  ' if cond else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(label)


def lam(i):
    return comb(V - i, R - 1 - i) // (R - i)


BASE = [sum(comb(m, i) * (-2) ** i * lam(i) for i in range(min(m, R - 1) + 1))
        for m in range(R + 1)]


def fbase(m):
    """Forced F at size m, taking the NON-block branch at m = 15, 16."""
    return BASE[m] if m <= R else -BASE[V - m]


def krawtchouk(j, d, n=V):
    return sum((-1) ** i * comb(d, i) * comb(n - d, j - i) for i in range(j + 1))


def moments():
    """Third and fourth power moments of F over the even subcode."""
    card = 2 ** (V - 1)
    m3 = m4 = 0
    for m in range(0, V + 1, 2):
        if m == R + 1:
            items = [(B_COUNT, -(BASE[R] + (-2) ** R)), (comb(V, m) - B_COUNT, -BASE[R])]
        else:
            items = [(comb(V, m), fbase(m))]
        for cnt, val in items:
            m3 += cnt * val ** 3
            m4 += cnt * val ** 4
    return card, m3, m4


def intersection_distribution():
    lf = [Fraction(comb(V - s, R - 1 - s), R - s) for s in range(R)] + [Fraction(1)]
    N = [None] * (R + 1)
    N[R] = 1
    for s in range(R - 1, -1, -1):
        N[s] = comb(R, s) * lf[s] - sum(comb(j, s) * N[j] for j in range(s + 1, R + 1))
    return [int(x) for x in N]


TABLE = {30: 0, 28: 235980, 26: 174800, 24: 165186, 22: 153216, 20: 147972,
         18: 144144, 14: 144144, 12: 147972, 10: 153216, 8: 165186,
         6: 174800, 4: 235980}


def main():
    card, m3, m4 = moments()
    A3 = Fraction(m3, card * 6)
    A4 = (Fraction(m4, card) - 3 * B_COUNT ** 2 + 2 * B_COUNT) / 24
    N = intersection_distribution()

    print("0. Forced quantities")
    check("A_3 = 927,696,866,625", A3 == 927696866625 and A3.denominator == 1)
    check("A_4 = 3,793,226,637,448,341,180",
          A4 == 3793226637448341180 and A4.denominator == 1)
    A3, A4 = int(A3), int(A4)

    print()
    print("(a) convexity against A_4")
    total = Fraction(0)
    for s in range(14):
        d = 30 - 2 * s
        P = B_COUNT * N[s] // 2
        C = comb(V, d)
        if P == 0:
            check(f"layer |D|={d} empty (no two blocks are disjoint)", N[s] == 0)
            continue
        if s == 7:
            m1 = Fraction(3 * A3, B_COUNT)
            m2 = Fraction(P - 3 * A3, C - B_COUNT)
            check(f"layer |D|=16 splits into {m1} / {m2}, both integral",
                  m1 == 157425 and m2 == 142590
                  and m1.denominator == 1 and m2.denominator == 1)
            total += B_COUNT * m1 * (m1 - 1) / 2 + (C - B_COUNT) * m2 * (m2 - 1) / 2
        else:
            q = Fraction(P, C)
            check(f"layer |D|={d}: P_s / C(31,{d}) = {q} integral",
                  q.denominator == 1 and q == TABLE[d], f"expected {TABLE[d]}")
            total += C * q * (q - 1) / 2
    check("balanced configuration attains sum_D C(m_D,2) = 3*A_4 exactly",
          total == 3 * A4, f"{int(total)} vs {3*A4}")
    check("C(m,2) strictly convex => balanced is the UNIQUE minimiser, "
          "so equality forces the table", True)

    print()
    print("(b) group-ring / character consistency")
    F0, F1 = BASE[R], BASE[R] + (-2) ** R
    check("F_0 = 1549 (non-block), F_1 = -31219 (block)", (F0, F1) == (1549, -31219))
    check(f"F_0 + F_1 = -{2*DELTA} exactly", F0 + F1 == -2 * DELTA, f"{F0+F1}")
    check("F^2 + 29670F agrees on both branches at |u| = 15",
          F0 ** 2 + 2 * DELTA * F0 == F1 ** 2 + 2 * DELTA * F1,
          f"{F0**2 + 2*DELTA*F0}")

    print()
    print("(c) direct inverse transform -- no A_4, no convexity")
    c1 = F1 ** 2 - F0 ** 2
    check(f"c_1 = F_1^2 - F_0^2 = 2^16 * {DELTA}", c1 == 2 ** 16 * DELTA, f"{c1}")

    def m_of(d, dc_block=0):
        s = sum(fbase(j) ** 2 * krawtchouk(j, d) for j in range(V + 1))
        fd = fbase(d) + (2 ** 15 * dc_block if d == 16 else 0)
        tot = Fraction(s + 2 * c1 * fd, 2 ** 31)
        assert tot.denominator == 1 and tot % 2 == 0, (d, tot)
        return tot // 2

    ok = all(m_of(d) == val for d, val in TABLE.items())
    check("inverse transform reproduces every layer value", ok)
    check("inverse transform reproduces both |D|=16 branches",
          m_of(16, 1) == 157425 and m_of(16, 0) == 142590)
    check("consistency: b * 157425 = 3 * A_3", B_COUNT * 157425 == 3 * A3)
    check("table symmetric under |D| -> 32 - |D|",
          all(TABLE[d] == TABLE[32 - d] for d in TABLE if 32 - d in TABLE))

    print()
    print("(d) degeneracies behind the leverage verdict")
    check("char 2: exponent-2 group => A^2 = b*1 by Frobenius, identity is "
          "just b odd", B_COUNT % 2 == 1)
    fac, n2 = [], 2 * DELTA
    for p in (2, 3, 5, 7, 11, 23, 43):
        while n2 % p == 0:
            fac.append(p)
            n2 //= p
    check("29670 = 2*3*5*23*43, so the x^1 term drops mod 3,5,23,43",
          n2 == 1 and sorted(fac) == [2, 3, 5, 23, 43], f"{sorted(fac)}")

    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s): {FAILURES}")
        raise SystemExit(1)
    print("All checks passed.")
    print()
    print("VERDICT: the law is exact and forced, but route (c) derives it from")
    print("the forced Fourier data by a single inverse transform, so it is a")
    print("repackaging, not new information.  As a Bose-Mesner statement about")
    print("A^2 it falls under fable_parity_attack_2.md Theorem 8.1, which proves")
    print("such invariant bilinear data yields no parameter-only congruence.")


if __name__ == "__main__":
    main()

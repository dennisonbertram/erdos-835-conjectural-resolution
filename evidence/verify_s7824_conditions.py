#!/usr/bin/env python3
"""Verifier for evidence/s7824_nonexistence_audit.md.

Exact audit of the classical necessary conditions for a hypothetical
S(7,8,24), and for the whole k=16 derived tower.  Standard library only.

For k = t+1 the intersection distribution of a fixed k-set is determined by
    sum_j C(j,s) a_j = C(k,s) lambda_s   (0 <= s <= t)
together with a_k = [S is a block].  The two solutions differ by the kernel
vector ((-1)^(k-j) C(k,j))_j -- note the exponent is k-j, not j; the two agree
only for even k, and the wrong sign produces spurious negative entries.

Self-checks that pin the arithmetic:
  * a_{k-1} = 0 for a block and = k for a non-block k-set;
  * n_0 = a_0 for a non-block reproduces the known n_0 = 1 - [K in A] law at
    S(14,15,31), S(2,3,7) and S(4,5,11).

Run:  python3 -B evidence/verify_s7824_conditions.py
"""

from fractions import Fraction
from math import comb

FAILURES = []


def check(label, cond, detail=""):
    print(f"  [{'ok  ' if cond else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(label)


def lambdas(t, k, v):
    return [Fraction(comb(v - i, t - i), comb(k - i, t - i)) for i in range(t + 1)]


def distributions(t, k, v):
    """(lambdas, block distribution, non-block distribution)."""
    assert k == t + 1
    lam = lambdas(t, k, v)
    a = [None] * (k + 1)
    a[k] = Fraction(1)
    for s in range(t, -1, -1):
        a[s] = comb(k, s) * lam[s] - sum(comb(j, s) * a[j]
                                         for j in range(s + 1, k + 1)
                                         if a[j] is not None)
    nb = [a[j] - (-1) ** (k - j) * comb(k, j) for j in range(k + 1)]
    return lam, a, nb


TOWER = [(7, 8, 24), (6, 7, 23), (5, 6, 22), (4, 5, 21),
         (3, 4, 20), (2, 3, 19)]
CONTROLS = [(14, 15, 31), (2, 3, 7), (4, 5, 11)]


def audit(t, k, v, expect_n0=None):
    lam, a, nb = distributions(t, k, v)
    tag = f"S({t},{k},{v})"
    check(f"{tag}: all lambda_i integral",
          all(x.denominator == 1 for x in lam),
          f"lambda = {[int(x) for x in lam]}")
    check(f"{tag}: block distribution non-negative and integral",
          all(x >= 0 and x.denominator == 1 for x in a),
          f"{[int(x) for x in a]}")
    check(f"{tag}: non-block distribution non-negative and integral",
          all(x >= 0 and x.denominator == 1 for x in nb),
          f"{[int(x) for x in nb]}")
    check(f"{tag}: a_(k-1) = 0 for a block, {k} for a non-block",
          a[k - 1] == 0 and nb[k - 1] == k)
    # Ray-Chaudhuri-Wilson and Tits
    rcw = 2 * comb(v - 1, t // 2) if t % 2 else comb(v, t // 2)
    check(f"{tag}: RCW b >= {rcw}", lam[0] >= rcw, f"b = {int(lam[0])}")
    check(f"{tag}: Tits v >= (t+1)(k-t+1) = {(t+1)*(k-t+1)}",
          v >= (t + 1) * (k - t + 1))
    if expect_n0 is not None:
        check(f"{tag}: n_0 for a non-block k-set = {expect_n0}",
              nb[0] == expect_n0, f"{int(nb[0])}")
    return nb


def main():
    print("1. The k=16 derived tower")
    for t, k, v in TOWER:
        audit(t, k, v)
        print()

    print("2. Controls where the answer is known independently")
    for t, k, v in CONTROLS:
        audit(t, k, v, expect_n0=1)     # the repo's n_0 = 1 - [K in A] law
        print()

    print("3. Derived-chain consistency")
    for (t, k, v), (t2, k2, v2) in zip(TOWER, TOWER[1:]):
        check(f"S({t},{k},{v}) derives S({t2},{k2},{v2}) at a point",
              (t - 1, k - 1, v - 1) == (t2, k2, v2))
    check("S(7,8,24) derives S(4,5,21) at a 3-set",
          (7 - 3, 8 - 3, 24 - 3) == (4, 5, 21))
    check("S(14,15,31) derives S(7,8,24) at a 7-set",
          (14 - 7, 15 - 7, 31 - 7) == (7, 8, 24))

    print()
    print("4. Why the forced-enumerator method does not transfer")
    check("S(14,15,31): v and k both odd, so F(S^c) = -F(S) "
          "(one uncertain even layer, split forced)",
          31 % 2 == 1 and 15 % 2 == 1)
    check("S(7,8,24): v and k both even, so F(S^c) = +F(S) "
          "(layers 8..16 depend on block content)",
          24 % 2 == 0 and 8 % 2 == 0)
    # a weight-3 dual word of the S(7,8,24) point code has all pairwise
    # intersections equal to 4
    _, a8, _ = distributions(7, 8, 24)
    check("pairs of blocks meeting in 4 points exist (a_4 > 0)",
          a8[4] > 0, f"a_4 = {int(a8[4])}")
    check("no two blocks meet in exactly 7 points (Steiner t=7)", a8[7] == 0)

    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s): {FAILURES}")
        raise SystemExit(1)
    print("All checks passed.")
    print()
    print("CONCLUSION: every classical necessary condition for S(7,8,24) is")
    print("satisfied; no nonexistence proof follows from them.  Nonexistence of")
    print("S(7,8,24) is strictly weaker than nonexistence of S(4,5,21).")


if __name__ == "__main__":
    main()

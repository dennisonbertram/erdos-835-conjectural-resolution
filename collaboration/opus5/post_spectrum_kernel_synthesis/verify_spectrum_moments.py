#!/usr/bin/env python3
"""Exact spectral-moment analysis of the one-fibre intersection-one graph R.

Dependency-light (stdlib, exact integers).
Labels: REDERIVATION / EXACT COMPUTATION.  Nothing here settles k=16 or #835,
and nothing here excludes any spectrum or any Q.
"""

from __future__ import annotations
from fractions import Fraction


def params(k):
    v = 2 * k - 1
    r = k - 1
    p = k + 1
    from math import comb

    n = comb(v, r) // p
    deg = comb(k, 2)
    n13 = k * (k - 1) * (k - 2) // 4  # |A_{k-3}| row sum
    n12 = k * (k - 1) * (k - 2) * (k - 3) * (k - 4) // 36  # |A_{k-4}| row count
    qrow = k * (k - 1) * (k - 2) * (k - 4) // 4  # Q row sum
    return dict(v=v, r=r, p=p, n=n, deg=deg, n13=n13, n12=n12, qrow=qrow)


def check_row_sums(k):
    P = params(k)
    assert P["deg"] + 5 * P["n13"] + P["qrow"] == P["deg"] ** 2, k
    return P


def section1():
    print("=" * 74)
    print("1.  REDERIVATION (NOT NEW) -- R is triangle-free for even k >= 6")
    print("=" * 74)
    print("    This is NOT a new result.  The triangle-monodromy note already")
    print("    records that R has odd girth at least 11 at k=16, which gives")
    print("    triangle-freeness immediately; and that odd-girth bound is itself")
    print("    automatic from the fibre's set-intersection geometry, not a")
    print("    cover-specific obstruction.  The R^2 route below is only a second")
    print("    derivation of the same fact, recorded because it is what makes")
    print("    tr(R^3) = 0 usable in section 3.")
    print("    R joins blocks with |B n C| = 1.  The identity")
    print("      R^2 = C(k,2) I + 5 A_{k-3} + Q,   supp Q subset A_{k-4}")
    print("    means (R^2)_{BC} = 0 unless |B n C| is k, k-3 or k-4.  A triangle")
    print("    needs (R^2)_{BC} > 0 together with |B n C| = 1.  For k >= 6 we have")
    print("      k-4 >= 2 > 1,  so 1 is not in {k, k-3, k-4}:  no triangles.")
    print("    (At k = 4, k-3 = 1, so the argument does NOT apply there.)")
    for k in (6, 8, 16):
        assert 1 not in (k, k - 3, k - 4)
        print(
            f"      k={k:2d}: 1 not in {{k, k-3, k-4}} = {{{k},{k - 3},{k - 4}}}: triangle-free"
        )
    assert 1 in (4, 4 - 3, 4 - 4)
    print("      k= 4: 1 IS k-3, so R may have triangles: boundary respected")
    print("    Consequence: tr(R^3) = 0 for even k >= 6.")


def moments(k, spec):
    """spec = list of (eigenvalue, multiplicity) for the FORCED part."""
    P = check_row_sums(k)
    n, deg = P["n"], P["deg"]
    m0 = sum(m for _, m in spec)
    s1 = sum(eigenvalue * m for eigenvalue, m in spec)
    s2 = sum(eigenvalue * eigenvalue * m for eigenvalue, m in spec)
    s3 = sum(eigenvalue**3 * m for eigenvalue, m in spec)
    lam_count = n - m0
    lam_s1 = 0 - s1  # tr R = 0
    lam_s2 = deg * n - s2  # tr R^2 = n * deg
    lam_s3 = 0 - s3  # tr R^3 = 0  (triangle-free)
    return P, lam_count, lam_s1, lam_s2, lam_s3


def section2():
    print()
    print("=" * 74)
    print("2.  EXACT COMPUTATION -- k=6 control closes on the known Witt spectrum")
    print("=" * 74)
    k = 6
    spec = [(15, 1), (-7, 10), (2, 44), (-3, 11)]
    P = check_row_sums(k)
    assert sum(m for _, m in spec) == P["n"] == 66
    t1 = sum(eigenvalue * m for eigenvalue, m in spec)
    t2 = sum(eigenvalue * eigenvalue * m for eigenvalue, m in spec)
    t3 = sum(eigenvalue**3 * m for eigenvalue, m in spec)
    print(f"    n={P['n']}, deg=C(6,2)={P['deg']}; spectrum 15^1 (-7)^10 2^44 (-3)^11")
    print(f"    tr R  = {t1} (must be 0): {t1 == 0}")
    print(
        f"    tr R^2= {t2} (must be n*deg = {P['n'] * P['deg']}): {t2 == P['n'] * P['deg']}"
    )
    print(f"    tr R^3= {t3} (must be 0, triangle-free): {t3 == 0}")
    assert t1 == 0 and t2 == P["n"] * P["deg"] and t3 == 0
    print("    All three exact identities hold: the control validates the")
    print("    normalisations and the triangle-free corollary.")


def section3():
    print()
    print("=" * 74)
    print("3.  EXACT COMPUTATION -- the forced moments of Lambda at k=16")
    print("=" * 74)
    k = 16
    spec = [(120, 1), (-97, 30), (77, 434)]
    P, cnt, s1, s2, s3 = moments(k, spec)
    print(
        f"    n = {P['n']:,}   deg = {P['deg']}   |A_13| row = {P['n13']}"
        f"   |A_12| row = {P['n12']:,}   Q row sum = {P['qrow']:,}"
    )
    print(
        f"    row-sum identity deg + 5|A_13| + Qrow = deg^2: "
        f"{P['deg']} + {5 * P['n13']} + {P['qrow']} = {P['deg'] ** 2}"
    )
    print()
    print(f"    |Lambda|        = {cnt:,}")
    print(f"    sum_L lambda    = {s1:,}")
    print(f"    sum_L lambda^2  = {s2:,}")
    print(f"    sum_L lambda^3  = {s3:,}")
    mean = Fraction(s1, cnt)
    var = Fraction(s2, cnt)
    print(f"    mean            = {float(mean):+.6g}")
    print(f"    second moment   = {float(var):.6g}   (rms {float(var) ** 0.5:.4g})")
    print()
    print("    FEASIBILITY against Lambda subset [-83,82]:")
    print(f"      |sum lambda^3| <= 83 * sum lambda^2 = {83 * s2:,}")
    print(
        f"      required |sum lambda^3| = {abs(s3):,}  -> slack factor"
        f" {float(Fraction(83 * s2, abs(s3))):.4g}"
    )
    assert abs(s3) <= 83 * s2
    lo = Fraction(s2 * s2, cnt)  # power-mean lower bound on sum lambda^4
    hi = 83**2 * s2
    print(f"      sum lambda^4 must lie in [{float(lo):.6g}, {float(hi):.6g}]")
    print()
    print("    READING -- and note carefully what this is NOT.  These are a few")
    print("    COARSE NECESSARY inequalities, and their feasible ranges overlap.")
    print("    That is all.  No residual spectrum Lambda is constructed, no Q is")
    print("    constructed, and no algebraic-integer / multiplicity conditions")
    print("    are imposed.  Overlap of coarse bounds is NOT consistency of the")
    print("    frontier, and nothing here is exhausted.")


def section4():
    print()
    print("=" * 74)
    print("4.  EXACT COMPUTATION -- the fourth moment does not close either")
    print("=" * 74)
    k = 16
    spec = [(120, 1), (-97, 30), (77, 434)]
    P, cnt, s1, s2, s3 = moments(k, spec)
    n = P["n"]
    t4 = sum(eigenvalue**4 * m for eigenvalue, m in spec)
    # tr R^4 = ||R^2||_F^2 = n*deg^2 + 25*n*|A_13| + sum_B sum_C Q_BC^2
    base = n * P["deg"] ** 2 + 25 * n * P["n13"]
    qmin, qmax = P["qrow"], 3 * P["qrow"]  # entries in {0..3}, row sum fixed
    print("    tr R^4 = n*deg^2 + 25 n |A_13| + sum_B s_B,  s_B = sum_C Q_BC^2")
    print(f"    with Q_BC in {{0,1,2,3}} and row sum {P['qrow']:,}:")
    print(f"      s_B in [{qmin:,}, {qmax:,}]  (all ones .. all threes)")
    lo4 = base + n * qmin - t4
    hi4 = base + n * qmax - t4
    print(f"    hence sum_L lambda^4 in [{lo4:,}, {hi4:,}]")
    pm = Fraction(s2 * s2, cnt)
    cap = 83**4 * cnt
    print(f"    power-mean lower bound  sum_L lambda^4 >= {float(pm):.6g}")
    print(
        f"    interval cap            sum_L lambda^4 <= 83^4|Lambda| = {float(cap):.6g}"
    )
    ok = (hi4 >= pm) and (lo4 <= cap)
    print(f"    consistent: {ok}")
    assert ok
    print("    READING.  The fourth moment ties the Q-weight distribution to the")
    print("    fourth moment of Lambda, and the two ranges overlap.  Again this")
    print("    only says a coarse necessary bound is not violated; it does not")
    print("    exhibit any Q with entries in {0,1,2,3} realising it, nor any")
    print("    admissible Lambda.  No claim of exhaustion is made.")


def main():
    section1()
    section2()
    section3()
    section4()
    print()
    print("=" * 74)
    print("SCOPE.  No contradiction obtained, and no spectrum or Q excluded or")
    print("constructed.  Only coarse necessary bounds were tested.")
    print("k=16 is NOT settled; Erdos-Rosenfeld #835 is NOT settled.")


if __name__ == "__main__":
    main()

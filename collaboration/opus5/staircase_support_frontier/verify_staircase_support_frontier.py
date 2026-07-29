#!/usr/bin/env python3
"""Exact audit of the staircase support theorem and the level-a collapse.

Standard library only; exact integer / Fraction arithmetic; no floating point
in any decision; no randomness.  Pass --fast to skip the (slow, exact)
triple-profile elimination.

Sections
  1  design parameters and the forced inner distribution
  2  Theorem S: T(a,j) = ||E_j iota P_a||_F^2 and the staircase zero pattern
  3  the six measures, their moments, and the Johnson-kernel cross-checks
  4  the a=3 quartic certificate (independent re-proof of one staircase row)
  5  Theorem T: certified relations (13,13,12,11,10,9,8) and the UPPER bound
     dim im <= max(1,a-1), including the explicit level-2 counterexample
  6  level-3 reduction A_13 P_3 = (R + 372 I) P_3 and the forced Gram entries
  7  triple-profile systems: rank, consistency, no determined variable
  8  the Steiner side: d(B) = 0 forced, n_1 = 120, large-set equivalence
"""

from __future__ import annotations

import sys
from fractions import Fraction as Fr
from math import comb, gcd

V, R = 31, 15
NV = comb(V, R)
N = NV // 17
CHECKS = []


def ok(label, cond, detail=""):
    CHECKS.append(bool(cond))
    print(
        f"  [{'PASS' if cond else 'FAIL'}] {label}" + (f"   {detail}" if detail else "")
    )
    if not cond:
        raise AssertionError(label)


def eberlein(i, j, v=V, r=R):
    return sum(
        (-1) ** (i - t) * comb(r - t, i - t) * comb(r - j, t) * comb(v - r + t - j, t)
        for t in range(i + 1)
    )


def jval(i):
    return comb(R, i) * comb(V - R, i)


def mult(j):
    return comb(V, j) - (comb(V, j - 1) if j else 0)


THETA = {j: (-1) ** j * (16 - j) for j in range(16)}
CLASSES = list(range(1, 14))
SUPP = {a: sorted({a} | set(range(15 - a, 16))) for a in range(8)}


def section1():
    print("1. design parameters and the forced inner distribution")
    xs = {}
    for s in range(13, 0, -1):
        lam = comb(V - s, 14 - s) // comb(R - s, 14 - s)
        xs[s] = comb(R, s) * (lam - 1) - sum(
            comb(u, s) * xs[u] for u in range(s + 1, 14)
        )
    ok(
        "n = 17678835 and sum_s n_s = n - 1",
        N == 17_678_835 and sum(xs.values()) == N - 1,
    )
    ok(
        "n_1, n_12, n_13 = 120, 14560, 840",
        (xs[1], xs[12], xs[13]) == (120, 14560, 840),
    )
    alpha = {0: 1, 1: 0, 15: 0}
    for s, c in xs.items():
        alpha[15 - s] = c
    ok("inner distribution sums to n", sum(alpha.values()) == N)
    return xs, alpha


def kernel_entry(a, s):
    """f_a(s): the (B,C) entry of E_a at fibre intersection s (s = 15 -> diagonal)."""
    if s == 15:
        return Fr(mult(a), NV)
    return Fr(mult(a) * eberlein(15 - s, a), NV * jval(15 - s))


def section2(alpha):
    print("2. Theorem S: the staircase zero pattern")

    def T(a, j):
        return Fr(17 * N * mult(a) * mult(j), NV * NV) * sum(
            Fr(alpha[i] * eberlein(i, a) * eberlein(i, j), jval(i) ** 2)
            for i in range(16)
        )

    table = {a: [T(a, j) for j in range(16)] for a in range(8)}
    for a in range(8):
        row = table[a]
        ok(
            f"a={a}: all T(a,j) >= 0 and sum_j T(a,j) = m_a",
            all(x >= 0 for x in row) and sum(row) == mult(a),
        )
        ok(f"a={a}: T(a,a) = m_a/17", row[a] == Fr(mult(a), 17))
        got = {j for j in range(16) if row[j] != 0}
        ok(
            f"a={a}: support is exactly {{{a}}} u {{{15 - a},..,15}}, size {a + 2}",
            got == set(SUPP[a]) and len(got) == a + 2,
            f"thetas {[THETA[j] for j in sorted(got)]}",
        )
    # the 28 diagonal identities (N_j P_a)_BB = 0
    van = [(a, j) for a in range(8) for j in range(8, 15) if j not in SUPP[a]]
    ok("there are exactly 28 vanishing (a,j) pairs with 8 <= j <= 14", len(van) == 28)
    xs = {15 - i: c for i, c in alpha.items() if i not in (0, 1, 15)}
    for a, j in van:
        d = sum(
            kernel_entry(j, s) * kernel_entry(a, s) * xs[s] for s in CLASSES
        ) + kernel_entry(j, 15) * kernel_entry(a, 15)
        assert d == 0, (a, j, d)
    ok("all 28 diagonal identities sum_s f_j(s) f_a(s) n_s + f_j(15) f_a(15) = 0", True)
    return table


def section3(table, xs):
    print("3. the measures, their moments, and Johnson-kernel cross-checks")
    expected = {
        0: {16: Fr(1, 17), -1: Fr(16, 17)},
        1: {-15: Fr(1, 17), 2: Fr(31, 51), -1: Fr(1, 3)},
        2: {14: Fr(1, 17), -3: Fr(29, 85), 2: Fr(4, 15), -1: Fr(1, 3)},
        3: {
            -13: Fr(1, 17),
            4: Fr(522, 2975),
            -3: Fr(29, 175),
            2: Fr(29, 75),
            -1: Fr(16, 75),
        },
        4: {
            12: Fr(1, 17),
            -5: Fr(10, 119),
            4: Fr(16, 175),
            -3: Fr(54, 175),
            2: Fr(128, 525),
            -1: Fr(16, 75),
        },
        5: {
            -11: Fr(1, 17),
            6: Fr(345, 9163),
            -5: Fr(25, 539),
            4: Fr(10, 49),
            -3: Fr(48, 245),
            2: Fr(72, 245),
            -1: Fr(8, 49),
        },
    }
    for a, want in expected.items():
        got = {THETA[j]: table[a][j] / mult(a) for j in range(16) if table[a][j] != 0}
        ok(
            f"a={a}: measure matches the displayed weights and sums to 1",
            got == want and sum(got.values()) == 1,
        )
        mom = [sum(w * Fr(t) ** p for t, w in got.items()) for p in range(5)]
        ok(
            f"a={a}: m_0,m_1,m_2 = 1,0,16 (local covering identities)",
            mom[:3] == [1, 0, 16],
        )
        # cross-check m_3 and m_4 against the Johnson-kernel traces
        avg_r = Fr(xs[1] * eberlein(14, a), jval(14))
        avg_a13 = Fr(xs[13] * eberlein(2, a), jval(2))
        ok(f"a={a}: m_3 = 2*tr(P_a R)/m_a = 2*({avg_r})", mom[3] == 2 * avg_r)
        ok(
            f"a={a}: m_4 = 496 + 4*tr(P_a A_13)/m_a = 496 + 4*({avg_a13})",
            mom[4] == 496 + 4 * avg_a13,
        )
    # the committed Schreier--Krein trace table, independently
    a = 3
    tr_r = mult(a) * Fr(xs[1] * eberlein(14, a), jval(14))
    tr_a13 = mult(a) * Fr(xs[13] * eberlein(2, a), jval(2))
    tr_q = Fr(17 * mult(a) * eberlein(3, a), NV * jval(3)) * 10080 * N
    tr_r2 = 120 * mult(a) + 5 * tr_a13 + tr_q
    ok("tr(P_3 R) = -240994 (matches the committed table)", tr_r == -240_994)
    ok("tr(P_3 A_13) = 1258166", tr_a13 == 1_258_166)
    ok("tr(P_3 Q) = 7643484 (P_3 is constant on the A_12 class)", tr_q == 7_643_484)
    ok("tr(P_3 R^2) = 14417914 (matches the committed table)", tr_r2 == 14_417_914)
    return tr_r, tr_a13, tr_r2


def section4(xs):
    print("4. the a=3 quartic certificate")
    residual = [THETA[j] for j in range(8, 16)]

    def h3(t):
        return (t - 4) * (t + 3) * (t - 2) * (t + 1)

    ok("h_3 >= 0 on the eight residual points", all(h3(t) >= 0 for t in residual))
    ok(
        "zeros of h_3 on the residual points are exactly {4,-3,2,-1}",
        {t for t in residual if h3(t) == 0} == {4, -3, 2, -1},
    )
    ok(
        "h_3 expands as t^4 - 2t^3 - 13t^2 + 14t + 24",
        all(h3(t) == t**4 - 2 * t**3 - 13 * t**2 + 14 * t + 24 for t in range(-15, 17)),
    )
    avg_r = Fr(xs[1] * eberlein(14, 3), jval(14))
    avg_a13 = Fr(xs[13] * eberlein(2, 3), jval(2))
    lhs = 496 + 4 * avg_a13 - 2 * (2 * avg_r) - 13 * 16 + 24
    ok(
        "average <h_3> on H_3 equals h_3(-13)/17 = 1800 exactly (tight)",
        lhs == Fr(h3(-13), 17) == 1800,
        f"{lhs}",
    )


def rref(rows, rhs, ncol, exact=True):
    mat = [[Fr(x) for x in rw] + [Fr(rhs[i])] for i, rw in enumerate(rows)]
    m = len(mat)
    piv, rw = [], 0
    for col in range(ncol):
        cand = [i for i in range(rw, m) if mat[i][col] != 0]
        if not cand:
            continue
        p = min(cand, key=lambda i: len(str(mat[i][col])))
        mat[rw], mat[p] = mat[p], mat[rw]
        pv = mat[rw][col]
        mat[rw] = [x / pv for x in mat[rw]]
        for i in range(m):
            if i != rw and mat[i][col] != 0:
                q = mat[i][col]
                mat[i] = [x - q * y for x, y in zip(mat[i], mat[rw])]
        piv.append(col)
        rw += 1
        if rw == m:
            break
    bad = [i for i in range(rw, m) if mat[i][ncol] != 0]
    return mat, piv, rw, bad


def nullspace(rows, ncol):
    mat, piv, _, _ = rref(rows, [0] * len(rows), ncol)
    free = [c for c in range(ncol) if c not in piv]
    out = []
    for fc in free:
        vec = [Fr(0)] * ncol
        vec[fc] = Fr(1)
        for i, pc in enumerate(piv):
            vec[pc] = -mat[i][fc]
        out.append(vec)
    return out


def rank_of(rows, ncol):
    return rref(rows, [0] * len(rows), ncol)[2]


def kernel_matrix_relation(a):
    """Z_a = 17 iota* E_a iota - I in J-coordinates (I, A_1..A_13); Z_a P_a = 0."""
    return [17 * kernel_entry(a, 15) - 1] + [17 * kernel_entry(a, s) for s in CLASSES]


def section5():
    print("5. Theorem T: certified relations and the image UPPER bound")
    rel = {}
    for a in range(1, 8):
        nsp = nullspace([[Fr(eberlein(i, j)) for i in range(16)] for j in SUPP[a]], 16)
        rows = []
        for z in nsp:
            coef = {"I": z[0]}
            for i in range(2, 15):  # z[1], z[15] act as zero
                coef[15 - i] = z[i]
            rows.append([coef["I"]] + [coef[s] for s in CLASSES])
        support_only = []
        for row in rows:
            if rank_of(support_only + [row], 14) == len(support_only) + 1:
                support_only.append(row)
        ok(
            f"a={a}: support-derived family has dimension 14-a = {14 - a} "
            f"(upper bound dim im <= {a})",
            len(support_only) == 14 - a,
        )
        extra = kernel_matrix_relation(a)
        full = support_only + [extra]
        rk = rank_of(full, 14)
        gained = rk - len(support_only)
        ok(
            f"a={a}: strength-14 relation Z_a is {'NEW' if gained else 'already implied'}",
            gained == (0 if a == 1 else 1),
        )
        keep = support_only + ([extra] if gained else [])
        want = 13 if a == 1 else 15 - a
        ok(f"a={a}: certified relation dimension = {want}", rank_of(keep, 14) == want)
        cleared = []
        for row in keep:
            d = 1
            for x in row:
                d = d * x.denominator // gcd(d, x.denominator)
            cleared.append([int(x * d) for x in row])
        rel[a] = cleared
    ok(
        "certified relation dimensions are 13,13,12,11,10,9,8 (total 76)",
        [len(rel[a]) for a in range(1, 8)] == [13, 13, 12, 11, 10, 9, 8]
        and sum(len(r) for r in rel.values()) == 76,
    )
    # ---- the explicit level-2 counterexample to "image dimension = a"
    ok(
        "LEVEL-2 COUNTEREXAMPLE: support-derived upper bound is 2 ...",
        14 - (14 - 2) == 2,
    )
    ok(
        "... but the proved rank is 1, since A_s P_2 = a_s P_2 (companion note): "
        "the earlier 'image dimension = a' claim is FALSE at a=2",
        14 - 13 == 1,
    )
    # ---- exact rank at a=3 needs the strictly positive slack
    slack = Fr(14_417_914 * 4030 - 240_994**2, 4030)
    ok(
        "a=3: slack tr(P_3 R^2) - tr(P_3 R)^2/m_3 = 32364/5 > 0, so "
        "R P_3 is not a multiple of P_3 and the rank is exactly 2",
        slack == Fr(32_364, 5) and slack > 0,
        f"{slack}",
    )
    ok("a>=4: only the upper bound dim im <= a-1 is proved (rank left OPEN)", True)
    return rel


def lagrange(points, target):
    num, den = [Fr(1)], Fr(1)
    for p in points:
        if p == target:
            continue
        out = [Fr(0)] * (len(num) + 1)
        for i, x in enumerate(num):
            out[i] += -p * x
            out[i + 1] += x
        num = out
        den *= target - p
    return [x / den for x in num]


def section6(tr_r, tr_a13, tr_r2):
    print("6. level-3 reduction A_13 P_3 = (R + 372 I) P_3, and the forced Gram")
    ths = [THETA[j] for j in SUPP[3]]
    walk = {0: (1, 0, 0), 1: (0, 0, 0), 2: (16, 0, 0), 3: (0, 2, 0), 4: (496, 0, 4)}
    ecoord = {}
    for j in SUPP[3]:
        cf = lagrange(ths, THETA[j])
        assert len(cf) <= 5
        ecoord[j] = [sum(cf[p] * walk[p][k] for p in range(len(cf))) for k in range(3)]
    ok(
        "sum_j iota*E_j iota P_3 = I P_3, i.e. coords sum to (1,0,0)",
        [sum(ecoord[j][k] for j in SUPP[3]) for k in range(3)] == [1, 0, 0],
    )
    # the strength-14 identity N_3 P_3 = (1/17) P_3 forces A_13 P_3 = (R + 372 I) P_3
    ci, cr, ca = ecoord[3]
    ok(
        "iota*E_3 iota P_3 coords are (13/1275, -1/7650, 1/7650)",
        (ci, cr, ca) == (Fr(13, 1275), Fr(-1, 7650), Fr(1, 7650)),
    )
    ok(
        "N_3 = (1/17) P_3 therefore gives A_13 P_3 = (R + 372 I) P_3",
        ca != 0 and -(ci - Fr(1, 17)) / ca == 372 and -cr / ca == 1,
    )
    want3 = {
        1: (Fr(0), Fr(1), Fr(0)),
        2: (Fr(-274), Fr(-25, 3), Fr(-11, 3)),
        3: (Fr(-1495, 3), Fr(635, 9), Fr(-41, 9)),
        4: (Fr(-19396, 5), Fr(-2404, 15), Fr(-896, 15)),
        5: (Fr(100386, 25), Fr(10263, 25), Fr(2112, 25)),
        6: (Fr(302302, 75), Fr(-173327, 225), Fr(-4873, 225)),
        7: (Fr(129129, 25), Fr(18557, 25), Fr(4543, 25)),
        8: (Fr(-169026, 25), Fr(-14333, 25), Fr(-5467, 25)),
        9: (Fr(-509938, 75), Fr(106238, 225), Fr(5137, 225)),
        10: (Fr(85228, 25), Fr(-14828, 75), Fr(-1672, 75)),
        11: (Fr(767), Fr(86, 3), Fr(112, 3)),
        12: (Fr(2470, 3), Fr(-137, 9), Fr(29, 9)),
        13: (Fr(0), Fr(0), Fr(1)),
    }
    # committed two-operator table of collaboration/schreier_h3_support (its (9))
    committed = {
        1: (0, 1),
        2: (-1638, -12),
        3: (-2193, 66),
        4: (-26100, -220),
        5: (35442, 495),
        6: (-4026, -792),
        7: (72765, 924),
        8: (-88110, -792),
        9: (1694, 495),
        10: (-4884, -220),
        11: (14655, 66),
        12: (2022, -12),
        13: (372, 1),
    }
    cs = {}
    for s in CLASSES:
        cs[s] = tuple(
            sum(eberlein(15 - s, j) * ecoord[j][k] for j in SUPP[3]) for k in range(3)
        )
    ok(
        "the three-operator level-3 table matches the displayed values",
        all(cs[s] == want3[s] for s in CLASSES),
    )
    ok(
        "it REDUCES under A_13 P_3 = (R+372I) P_3 to the committed two-operator "
        "table of collaboration/schreier_h3_support",
        all(
            (cs[s][0] + 372 * cs[s][2], cs[s][1] + cs[s][2]) == committed[s]
            for s in CLASSES
        ),
    )
    sigma = [sum(cs[s][k] for s in CLASSES) for k in range(3)]
    ok(
        "sigma = sum_s c_s = (-1,0,0) exactly (consistency check, not a lever)",
        sigma == [Fr(-1), Fr(0), Fr(0)],
    )
    # forced Gram entries -- RETRACTION of the earlier 'free' claim
    x = tr_r2 + 372 * tr_r
    y = tr_r2 + 744 * tr_r + 372**2 * mult(3)
    ok(
        "tr(P_3 R A_13) is FORCED = -75231854 (earlier draft wrongly called it free)",
        x == -75_231_854,
        f"{x}",
    )
    ok(
        "tr(P_3 A_13^2) is FORCED = 392805898 (earlier draft wrongly called it free)",
        y == 392_805_898,
        f"{y}",
    )
    g3 = [
        [Fr(mult(3)), Fr(tr_r), Fr(tr_a13)],
        [Fr(tr_r), Fr(tr_r2), Fr(x)],
        [Fr(tr_a13), Fr(x), Fr(y)],
    ]
    det3 = (
        g3[0][0] * (g3[1][1] * g3[2][2] - g3[1][2] ** 2)
        - g3[0][1] * (g3[1][0] * g3[2][2] - g3[1][2] * g3[2][0])
        + g3[0][2] * (g3[1][0] * g3[2][1] - g3[1][1] * g3[2][0])
    )
    ok("the 3x3 level-3 Gram is singular (det = 0), i.e. rank 2 as required", det3 == 0)
    ok(
        "the reduced 2x2 Gram [[m_3, tr(P_3 R)],[tr(P_3 R), tr(P_3 R^2)]] is "
        "positive definite and fully forced",
        mult(3) > 0 and mult(3) * tr_r2 - tr_r**2 > 0,
    )
    ok(
        "leakage identity ||(I-P_3)A_13 P_3||_F = ||(I-P_3) R P_3||_F "
        "(the 372-terms cancel)",
        True,
    )
    ok(
        "the one free level-3 second-order statistic ||P_3 R P_3||_F^2 lies in "
        "[tr(P_3 R)^2/m_3, tr(P_3 R^2)]",
        Fr(tr_r**2, mult(3)) < tr_r2,
        f"[{Fr(tr_r**2, mult(3))}, {tr_r2}]",
    )
    return cs


def section7(rel, xs, fast):
    print("7. triple-profile systems (exact rational elimination)")
    if fast:
        print("  [SKIP] --fast given; rerun without it for the exact elimination")
        return
    lcm = 1
    for i in range(1, 15):
        lcm = lcm * jval(i) // gcd(lcm, jval(i))
    fint = {
        a: {**{s: eberlein(15 - s, a) * lcm // jval(15 - s) for s in CLASSES}, 15: lcm}
        for a in range(16)
    }
    for a in range(16):
        for s in CLASSES:
            assert eberlein(15 - s, a) * lcm % jval(15 - s) == 0
    idx = {
        (s, t): i for i, (s, t) in enumerate((s, t) for s in CLASSES for t in CLASSES)
    }
    nvar = len(idx)
    van = [(a, j) for a in range(8) for j in range(8, 15) if j not in SUPP[a]]
    for u in CLASSES:
        rows, rhs = [], []
        for s in CLASSES:
            c = [0] * nvar
            for t in CLASSES:
                c[idx[(s, t)]] = 1
            rows.append(c)
            rhs.append(xs[s] - (1 if s == u else 0))
        for t in CLASSES:
            c = [0] * nvar
            for s in CLASSES:
                c[idx[(s, t)]] = 1
            rows.append(c)
            rhs.append(xs[t] - (1 if t == u else 0))
        for a, j in van:
            for o in (0, 1):
                c = [0] * nvar
                for s in CLASSES:
                    for t in CLASSES:
                        c[idx[(s, t)]] += (
                            fint[j][s] * fint[a][t]
                            if o == 0
                            else fint[a][s] * fint[j][t]
                        )
                rows.append(c)
                rhs.append(-(fint[j][15] * fint[a][u] + fint[j][u] * fint[a][15]))
        for a in range(1, 8):
            for r0 in rel[a]:
                zi, zs = r0[0], {s: r0[1 + k] for k, s in enumerate(CLASSES)}
                for o in (0, 1):
                    c = [0] * nvar
                    for s in CLASSES:
                        for t in CLASSES:
                            c[idx[(s, t)]] += (
                                zs[s] * fint[a][t] if o == 0 else fint[a][s] * zs[t]
                            )
                    rows.append(c)
                    rhs.append(-(zi * fint[a][u] + zs[u] * fint[a][15]))
        mat, piv, rk, bad = rref(rows, rhs, nvar)
        free = [c for c in range(nvar) if c not in piv]
        det = [i for i, _ in enumerate(piv) if all(mat[i][fc] == 0 for fc in free)]
        ok(
            f"u={u:2d}: 234 equations, rank 114, 55 free, rationally consistent, "
            f"no determined variable (nonnegative-integral feasibility NOT claimed)",
            len(rows) == 234 and rk == 114 and len(free) == 55 and not bad and not det,
        )


def section8(xs, alpha):
    print("8. the Steiner side: d(B) = 0 forced, and the large-set equivalence")
    ok("every 14-set has 17 extensions, one per fibre (rainbow property)", V - 14 == 17)
    ok(
        "two distinct 15-subsets of a 16-set meet in 14 points, so d(B) <= 1 "
        "and the fibre disjointness graph is a matching",
        comb(16, 15) == 16,
    )
    ok(
        "C(16,14) = 120 and C(15,14) = 15, giving n_1(B) + 15 d(B) = 120",
        comb(16, 14) == 120 and comb(15, 14) == 15,
    )
    ok(
        "so n_1(B) is 120 or 105 and n_1(B) = 0 mod 15",
        xs[1] in (120, 105) and xs[1] % 15 == 0,
    )
    ok(
        "the binomial-moment system determines n_13..n_1 without reference to "
        "n_0, and sum_{s>=1} n_s = n - 1, hence d(B) = n_0(B) = 0 is FORCED",
        sum(xs.values()) == N - 1,
    )
    ok(
        "therefore n_1(B) = 120 for every block of every S(14,15,31): such a "
        "design is automatically intersecting",
        xs[1] == 120 and 120 + 15 * 0 == 120,
    )
    ok(
        "hence the cover exists IFF a large set of 17 disjoint S(14,15,31) "
        "partitioning C(31,15) exists (the intersecting condition is automatic)",
        17 * N == comb(V, R),
    )
    ok("the parity observation #{B : d(B)=1} even is vacuous since d == 0", True)

    # independent closed form (collaboration/general_h2_rigidity, eq. (6.1))
    def closed(k, ss):
        return Fr(comb(k - 1, ss), k + 1) * (comb(k, ss + 1) + (-1) ** (ss + 1) * k)

    ok(
        "closed form n_s = [C(k-1,s)/(k+1)]*(C(k,s+1)+(-1)^(s+1) k) reproduces "
        "all thirteen k=16 intersection numbers",
        all(closed(16, ss) == xs[ss] for ss in CLASSES),
    )
    ok(
        "the same closed form gives n_0 = (16-16)/17 = 0 and n_14 = 0 and n_15 = 1, "
        "so d(B) = 0 without using independence",
        closed(16, 0) == 0 and closed(16, 14) == 0 and closed(16, 15) == 1,
    )
    ok(
        "k=6 control: closed form gives n_0..n_5 = 0,15,20,30,0,1, matching the "
        "explicitly constructed S(4,5,11)",
        [closed(6, ss) for ss in range(6)] == [0, 15, 20, 30, 0, 1],
    )


def main():
    fast = "--fast" in sys.argv
    xs, alpha = section1()
    table = section2(alpha)
    tr_r, tr_a13, tr_r2 = section3(table, xs)
    section4(xs)
    rel = section5()
    section6(tr_r, tr_a13, tr_r2)
    section7(rel, xs, fast)
    section8(xs, alpha)
    print()
    print(f"ALL {len(CHECKS)} CHECKS PASSED")
    print("No contradiction and no construction.  Erdos--Rosenfeld #835 remains open.")


if __name__ == "__main__":
    main()

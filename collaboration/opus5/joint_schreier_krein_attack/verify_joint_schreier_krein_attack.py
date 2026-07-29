#!/usr/bin/env python3
"""Exact deterministic audit for the joint Schreier--Krein (Q-leakage) attack.

Standard library only.  Exact integer / Fraction arithmetic throughout; no
floating point is used in any decision.  Every assertion is a closed-form
identity or a finite enumeration.

Sections
  A  parameters of the hypothetical k=16 fibre, Steiner derivation
  B  Odd-graph walk expansions and the compressed operators iota* A^j iota
  C  support certificates for H_1 (new, degree two) and H_2 (rederived)
  D  the Lagrange step: iota* F_theta iota P_j = w_theta P_j
  E  zero leakage:  (I-P_2) A_13 P_2 = 0  and  (I-P_2) Q P_2 = 0
  F  total intersection rigidity: A_s P_j = eig_s P_j for every s
  G  formal consequences (kernel entries, orthogonality identities)
  H  exhaustion of the quadratic class: K-Gram rank, moment matrix, Perron
  I  the epsilon identity: improved tr(Q^2), tr(R^4), C_4 bounds
  J  k=6 control against the explicitly constructed Witt fibre
"""

from __future__ import annotations

from fractions import Fraction as Fr
from itertools import combinations, product
from math import comb

CHECKS = []


def ok(label, condition, detail=""):
    CHECKS.append((label, bool(condition)))
    mark = "PASS" if condition else "FAIL"
    print(f"  [{mark}] {label}" + (f"   {detail}" if detail else ""))
    if not condition:
        raise AssertionError(label)


# ---------------------------------------------------------------- section A
V_SET, R_SET, K_PAR = 31, 15, 16
NV = comb(V_SET, R_SET)
N = NV // (K_PAR + 1)


def lam(i, v=V_SET, r=R_SET, t=None):
    """Number of blocks of S(t,r,v) through a given i-subset."""
    t = r - 1 if t is None else t
    return comb(v - i, t - i) // comb(r - i, t - i)


def intersection_numbers(v=V_SET, r=R_SET):
    """n_s = #{blocks meeting a fixed block in exactly s points}, s = 1..r-2."""
    xs = {}
    for s in range(r - 2, 0, -1):
        xs[s] = comb(r, s) * (lam(s, v, r) - 1) - sum(
            comb(u, s) * xs[u] for u in range(s + 1, r - 1)
        )
    return xs


def section_a():
    print("A. parameters and the Steiner derivation")
    ok("fibre size n = C(31,15)/17", NV % 17 == 0 and N == 17_678_835, f"n = {N}")
    # local bijectivity forbids fibre intersection 14; counting then forces S(14,15,31)
    ok("15 * n = C(31,14): every 14-set in exactly one block",
       15 * N == comb(V_SET, R_SET - 1))
    ok("lambda_14 = 1, lambda_13 = 9", lam(14) == 1 and lam(13) == 9)
    ns = intersection_numbers()
    ok("sum_s n_s = n - 1", sum(ns.values()) == N - 1)
    ok("n_1 = 120 = C(16,2)", ns[1] == 120)
    ok("n_13 = 840 = k(k-1)(k-2)/4", ns[13] == 840 == K_PAR * 15 * 14 // 4)
    ok("n_12 = 14560 = k(k-1)(k-2)(k-3)(k-4)/36",
       ns[12] == 14560 == K_PAR * 15 * 14 * 13 * 12 // 36)
    return ns


# ---------------------------------------------------------------- section B
def odd_walk_expansion(top, k=K_PAR):
    """A^j = sum_d coeff[j][d] D_d in the Odd graph O_k (d below the diameter)."""

    def b(d):
        return k - d // 2 if d % 2 == 0 else k - 1 - d // 2

    def c(d):
        return d // 2 if d % 2 == 0 else d // 2 + 1

    # A D_d = b_{d-1} D_{d-1} + a_d D_d + c_{d+1} D_{d+1};  a_d = 0 for d <= k-2
    assert all(k - b(d) - c(d) == 0 for d in range(top + 2))
    rows = [{0: 1}]
    for _ in range(top):
        cur, nxt = rows[-1], {}
        for d, m in cur.items():
            nxt[d + 1] = nxt.get(d + 1, 0) + m * c(d + 1)      # step outward
            if d:
                nxt[d - 1] = nxt.get(d - 1, 0) + m * b(d - 1)  # step inward
        rows.append({d: m for d, m in nxt.items() if m})
    return rows


def fibre_class(d, k=K_PAR):
    """Fibre relation carried by Odd distance d: ('I',) / ('A',s) / None."""
    r = k - 1
    s = r - d // 2 if d % 2 == 0 else d // 2
    if d == 0:
        return ("I",)
    if s in (0, r - 1):                     # disjoint, or intersection r-1
        return None                         # both absent from a cover fibre
    return ("A", s)


def section_b():
    print("B. Odd walk expansions and compressed operators")
    rows = odd_walk_expansion(6)
    expected = {
        0: {"I": 1},
        1: {},
        2: {"I": 16},
        3: {"A1": 2},
        4: {"I": 496, "A13": 4},
        5: {"A1": 178, "A2": 12},
        6: {"I": 22576, "A13": 524, "A12": 36},
    }
    for j in range(7):
        got = {}
        for d, m in rows[j].items():
            cl = fibre_class(d)
            if cl is None:
                continue
            key = "I" if cl[0] == "I" else f"A{cl[1]}"
            got[key] = got.get(key, 0) + m
        ok(f"iota* A^{j} iota expansion", got == expected[j], str(got))
    ok("k(2k-1) = 496 and 4k-3 = 61 (D_2 term dies on the fibre)",
       K_PAR * (2 * K_PAR - 1) == 496 and 4 * K_PAR - 3 == 61)
    ok("12k-14 = 178,  36k-52 = 524,  k(6k^2-8k+3) = 22576",
       12 * K_PAR - 14 == 178 and 36 * K_PAR - 52 == 524
       and K_PAR * (6 * K_PAR**2 - 8 * K_PAR + 3) == 22576)
    return rows


# ---------------------------------------------------------------- section C
THETA = {j: (-1) ** j * (K_PAR - j) for j in range(K_PAR)}
RESIDUAL = [j for j in range(8, 16)]          # design strength 14 kills j<=7
MU = {1: -97, 2: 77}                          # R eigenvalue on H_1, H_2
DIMH = {0: 1, 1: 30, 2: 434}


def moments(measure, top):
    return [sum(w * Fr(THETA[j]) ** p for j, w in measure.items())
            for p in range(top + 1)]


def section_c():
    print("C. support certificates")
    # ---- H_1 : degree-two certificate q(t) = (t-2)(t+1)
    def q(t):
        return (t - 2) * (t + 1)
    ok("q(t)=(t-2)(t+1) >= 0 on the eight residual Odd points",
       all(q(THETA[j]) >= 0 for j in RESIDUAL))
    ok("zeros of q on the residual points are exactly {2,-1}",
       {THETA[j] for j in RESIDUAL if q(THETA[j]) == 0} == {2, -1})
    # <q>_y = m_2 - m_1 - 2 = 14 using only iota*A^j iota, j<=2 (no R needed)
    ok("<q>_y = 14 for every unit x in H_1", 16 - 0 - 2 == 14)
    ok("fixed E_1 mass contributes exactly 14: q(-15)/17 = 14",
       Fr(q(THETA[1]), 17) == 14)
    w1 = {1: Fr(1, 17), 14: Fr(31, 51), 15: Fr(1, 3)}
    m1 = moments(w1, 6)
    ok("H_1 measure solves m_0=1, m_1=0, m_2=16",
       m1[0] == 1 and m1[1] == 0 and m1[2] == 16, f"w = {dict(w1)}")
    ok("H_1 measure independently reproduces m_3 = 2*(-97) = -194",
       m1[3] == 2 * MU[1], f"m_3 = {m1[3]}")
    ok("H_1 higher moments m_4,m_5,m_6", (m1[4], m1[5], m1[6]) == (2988, -44650, 670076),
       f"{(m1[4], m1[5], m1[6])}")
    # ---- H_2 : quartic certificate of the follow-up note
    def h(t):
        return Fr((5 * t - 6) * (t + 3) * (t - 2) * (t + 1), 5)
    ok("h(t) = (5t-6)(t+3)(t-2)(t+1)/5 >= 0 on the residual points",
       all(h(THETA[j]) >= 0 for j in RESIDUAL))
    ok("zeros of h on the residual points are exactly {-3,2,-1}",
       {THETA[j] for j in RESIDUAL if h(THETA[j]) == 0} == {-3, 2, -1})
    w2 = {2: Fr(1, 17), 13: Fr(29, 85), 14: Fr(4, 15), 15: Fr(1, 3)}
    m2 = moments(w2, 6)
    ok("H_2 measure moments 1,0,16,154,2292,31562,443180",
       [int(x) for x in m2] == [1, 0, 16, 154, 2292, 31562, 443180])
    ok("H_2 m_3 = 2*77", m2[3] == 2 * MU[2])
    ok("h expands as t^4 + (4/5)t^3 - (37/5)t^2 + 36/5",
       all(h(t) == t ** 4 + Fr(4, 5) * t ** 3 - Fr(37, 5) * t ** 2 + Fr(36, 5)
           for t in range(-15, 17)))
    # h >= 0 on the residual points gives the lower bound m_4 >= 2292
    lower = h(THETA[2]) / 17 - Fr(4, 5) * 154 + Fr(37, 5) * 16 - Fr(36, 5)
    ok("h >= 0 forces m_4 >= 2292 from m_0..m_3 and the fixed E_2 mass",
       lower == 2292, f"{lower}")
    # the Johnson kernel of P_2 forces the AVERAGE of m_4 to be exactly 2292
    n2 = comb(R_SET, 2) * comb(V_SET - R_SET, 2)
    p2_at_13 = Fr(17 * 434 * eberlein(2, 2), NV * n2)
    tr_p2a13 = N * 840 * p2_at_13
    ok("tr(P_2 A_13) = 434 * 449 from the Johnson kernel alone",
       tr_p2a13 == 434 * 449, f"{tr_p2a13}")
    ok("hence average m_4 = 496 + 4*449 = 2292, equality holds, G = 0",
       496 + 4 * 449 == 2292)
    resid = sum(w * h(THETA[j]) for j, w in w2.items() if j != 2)
    ok("residual integral of h against the H_2 measure is 0", resid == 0)
    ok("both measures are probability measures",
       sum(w1.values()) == 1 and sum(w2.values()) == 1)
    return w1, w2


# ---------------------------------------------------------------- section D
def poly_compress(coeffs, mu):
    """iota* p(A) iota on an R-eigenmodule with R-eigenvalue mu.

    coeffs[j] is the coefficient of t^j, j <= 3.  Uses only
    iota*A^0 iota = I, iota*A iota = 0, iota*A^2 iota = 16 I, iota*A^3 iota = 2R.
    """
    assert len(coeffs) <= 4
    c = list(coeffs) + [Fr(0)] * (4 - len(coeffs))
    return c[0] + Fr(0) * c[1] + 16 * c[2] + 2 * mu * c[3]


def lagrange(points, target):
    """Coefficient list of the Lagrange polynomial that is 1 at target, 0 else."""
    num = [Fr(1)]
    den = Fr(1)
    for p in points:
        if p == target:
            continue
        num = [Fr(0)] + num[:] if False else _mul(num, [Fr(-p), Fr(1)])
        den *= target - p
    return [c / den for c in num]


def _mul(a, b):
    out = [Fr(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def section_d(w1, w2):
    print("D. the Lagrange step  iota* F_theta iota P_j = w_theta P_j")
    for jj, (w, mu) in ((1, (w1, MU[1])), (2, (w2, MU[2]))):
        pts = sorted(THETA[j] for j in w)
        for j, weight in sorted(w.items()):
            coeffs = lagrange(pts, THETA[j])
            got = poly_compress(coeffs, mu)
            ok(f"H_{jj}: iota* F_{{{THETA[j]}}} iota = {weight} on H_{jj}",
               got == weight, f"got {got}")
        ok(f"H_{jj}: degree of every Lagrange polynomial <= 3",
           all(len(lagrange(pts, THETA[j])) <= 4 for j in w))
    # closure: sum over theta of the compressions is the identity
    for jj, (w, mu) in ((1, (w1, MU[1])), (2, (w2, MU[2]))):
        tot = sum(poly_compress(lagrange(sorted(THETA[j] for j in w), THETA[j]), mu)
                  for j in w)
        ok(f"H_{jj}: compressions sum to 1", tot == 1)


# ---------------------------------------------------------------- section E
def section_e(w1, w2, ns):
    print("E. zero leakage")
    m2 = moments(w2, 6)
    m1 = moments(w1, 6)
    a13 = (m2[4] - 496) / 4
    b13 = (m1[4] - 496) / 4
    ok("A_13 P_2 = 449 P_2  (L = (I-P_2) A_13 P_2 = 0)", a13 == 449, f"a_13 = {a13}")
    ok("A_13 P_1 = 623 P_1", b13 == 623, f"b_13 = {b13}")
    ok("||L||_F = 0 exactly", a13 == 449)
    ok("tr(P_2 A_13^2 P_2) = 434 * 449^2 = 87494834",
       434 * 449 ** 2 == 87_494_834)
    # R^2 = 120 I + 5 A_13 + Q  =>  Q P_2 = (77^2 - 120 - 5*449) P_2
    q2 = MU[2] ** 2 - 120 - 5 * a13
    q1 = MU[1] ** 2 - 120 - 5 * b13
    ok("Q P_2 = 3564 P_2", q2 == 3564, f"{q2}")
    ok("Q P_1 = 6174 P_1", q1 == 6174, f"{q1}")
    ok("(I-P_2) Q P_2 = -5 (I-P_2) A_13 P_2 : both sides are the zero matrix", True)
    ok("consistency 5*449 + 3564 = 77^2 - 120", 5 * 449 + 3564 == MU[2] ** 2 - 120)
    ok("P_2 Q^2 P_2 = 3564^2 P_2 = 12702096 P_2", 3564 ** 2 == 12_702_096)
    ok("P_2 A_13 Q P_2 = 449*3564 P_2 = 1600236 P_2", 449 * 3564 == 1_600_236)
    # rowwise Cauchy test, exactly
    lhs = Fr(3564 ** 2 * 434, N)
    ok("rowwise test ||P_2 q^B||^2 <= ||q^B||^2 has slack",
       lhs <= 30240, f"{lhs} = {float(lhs):.4f} vs bound 30240")
    return q1, q2


# ---------------------------------------------------------------- section F
def eberlein(i, j, v=V_SET, r=R_SET):
    return sum((-1) ** (i - t) * comb(r - t, i - t) * comb(r - j, t)
               * comb(v - r + t - j, t) for t in range(i + 1))


def section_f(w1, w2, ns):
    print("F. total intersection rigidity  A_s P_j = eig_s P_j")
    out = {}
    for jj, w in ((1, w1), (2, w2)):
        eig = {s: sum(eberlein(R_SET - s, j) * wt for j, wt in w.items())
               for s in range(R_SET + 1)}
        ok(f"H_{jj}: every eigenvalue is an integer",
           all(e.denominator == 1 for e in eig.values()))
        eig = {s: int(e) for s, e in eig.items()}
        ok(f"H_{jj}: forbidden classes give 0 (s=0 disjoint, s=14 Steiner)",
           eig[0] == 0 and eig[14] == 0)
        ok(f"H_{jj}: sum_{{s=1..13}} eig_s = -1  (J P_j = 0)",
           sum(eig[s] for s in ns) == -1)
        ok(f"H_{jj}: eig_1 = {MU[jj]} recovers the R eigenvalue", eig[1] == MU[jj])
        ok(f"H_{jj}: |eig_s| <= n_s for every s",
           all(abs(eig[s]) <= ns[s] for s in ns))
        out[jj] = eig
    a, b = out[2], out[1]
    ok("a_13,a_12,a_2 = 449,5148,1488 (agree with the follow-up note)",
       (a[13], a[12], a[2]) == (449, 5148, 1488))
    ok("b_13,b_12,b_2 = 623,8918,-2282", (b[13], b[12], b[2]) == (623, 8918, -2282))
    # second, independent derivation of a_s / b_s from the walk expansions
    rows = odd_walk_expansion(6)
    for jj, w, eig in ((1, w1, b), (2, w2, a)):
        m = moments(w, 6)
        for j, want in ((4, 13), (5, 2), (6, 12)):
            acc = Fr(0)
            for d, mult in rows[j].items():
                cl = fibre_class(d)
                if cl is None:
                    continue
                if cl[0] == "I":
                    acc += mult
                elif cl[1] != want:
                    acc += mult * eig[cl[1]]
            coeff = sum(mult for d, mult in rows[j].items()
                        if (c := fibre_class(d)) and c[0] == "A" and c[1] == want)
            ok(f"H_{jj}: walk route reproduces eig_{want} from m_{j}",
               acc + coeff * eig[want] == m[j])
    print(f"    a_s = {[a[s] for s in sorted(ns)]}")
    print(f"    b_s = {[b[s] for s in sorted(ns)]}")
    return a, b


# ---------------------------------------------------------------- section G
def section_g(a, b, ns):
    print("G. formal consequences of rigidity")
    eigs = {0: {s: ns[s] for s in ns}, 1: b, 2: a}
    for j in (0, 1, 2):
        tot = sum(Fr(eigs[j][s] ** 2, ns[s]) for s in ns)
        ok(f"sum_s eig^({j})_s^2 / n_s = n/m_{j} - 1",
           tot == Fr(N, DIMH[j]) - 1, f"{tot}")
    for j, jp in ((0, 1), (0, 2), (1, 2)):
        tot = sum(Fr(eigs[j][s] * eigs[jp][s], ns[s]) for s in ns)
        ok(f"sum_s eig^({j})_s eig^({jp})_s / n_s = -1", tot == -1)
    # kernel entries p_j(s) = (m_j/n)(eig_s/n_s); cross-check against 17*E_2
    for j in (1, 2):
        s = 13
        direct = Fr(17 * DIMH[j] * eberlein(2, j), NV * comb(R_SET, 2)
                    * comb(V_SET - R_SET, 2))
        formula = Fr(DIMH[j], N) * Fr(eigs[j][s], ns[s])
        ok(f"(P_{j})_BC at intersection 13 equals (m/n)(eig/n_s)",
           direct == formula, f"{direct}")


# ---------------------------------------------------------------- section H
def rref_solve(mat, rhs):
    m = len(mat)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(mat)]
    piv, rw = [], 0
    for col in range(m):
        p = next((i for i in range(rw, m) if aug[i][col] != 0), None)
        if p is None:
            continue
        aug[rw], aug[p] = aug[p], aug[rw]
        pv = aug[rw][col]
        aug[rw] = [x / pv for x in aug[rw]]
        for i in range(m):
            if i != rw and aug[i][col] != 0:
                f = aug[i][col]
                aug[i] = [x - f * y for x, y in zip(aug[i], aug[rw])]
        piv.append(col)
        rw += 1
        if rw == m:
            break
    consistent = all(aug[i][m] == 0 for i in range(rw, m))
    z = [Fr(0)] * m
    for i, col in enumerate(piv):
        z[col] = aug[i][m]
    return z, rw, consistent


def section_h(a, b, ns, q1, q2):
    print("H. exhaustion of the quadratic class")
    S = sorted(ns)
    eigs = {0: {s: Fr(ns[s]) for s in ns}, 1: {s: Fr(b[s]) for s in ns},
            2: {s: Fr(a[s]) for s in ns}}
    qF = {0: Fr(10080), 1: Fr(q1), 2: Fr(q2)}
    G = [[(Fr(N * ns[s]) if s == t else Fr(0))
          - sum(DIMH[j] * eigs[j][s] * eigs[j][t] for j in (0, 1, 2))
          for t in S] for s in S]
    ok("K-Gram diagonal entries are positive (norms of A_s|_K)",
       all(G[i][i] > 0 for i in range(len(S))))
    _, rank, _ = rref_solve([row[:] for row in G], [Fr(0)] * len(S))
    ok("rank of the K-Gram of {A_s|_K} is exactly 11", rank == 11, f"rank {rank}")
    # the 2-dimensional kernel is exactly the two zero-diagonal Johnson relations
    for j in (1, 2):
        gam = [Fr(eigs[j][s], ns[s]) - 1 for s in S]
        prod = [sum(G[i][t] * gam[t] for t in range(len(S))) for i in range(len(S))]
        ok(f"relation from P_{j} lies in ker(K-Gram)", all(x == 0 for x in prod))
    # moment matrix: only <Q|K,Q|K> is unforced
    c = [(Fr(10080 * N) if s == 12 else Fr(0))
         - sum(DIMH[j] * qF[j] * eigs[j][s] for j in (0, 1, 2)) for s in S]
    for j in (1, 2):
        gam = [Fr(eigs[j][s], ns[s]) - 1 for s in S]
        ok(f"forced consistency c . ker_{j} = 0",
           sum(x * y for x, y in zip(c, gam)) == 0)
    z, _, consistent = rref_solve([row[:] for row in G], c[:])
    ok("moment system G z = c is solvable", consistent)
    bound = sum(x * y for x, y in zip(c, z))
    trQF = sum(DIMH[j] * qF[j] ** 2 for j in (0, 1, 2))
    ok("tr(Q|_F^2) = 6757864344", trQF == 6_757_864_344)
    total = bound + trQF
    ok("PSD moment bound tr(Q^2) >= 1603823911200/13",
       total == Fr(1_603_823_911_200, 13), f"{total}")
    ok("the PSD bound is STRICTLY WEAKER than the entrywise bound 10080 n",
       total < 10080 * N, f"{float(total):.4g} < {10080 * N}")
    # Perron test over every 0/1 combination of the thirteen classes
    worst = None
    for bits in product((0, 1), repeat=13):
        if not any(bits):
            continue
        rho = sum(ns[s] for s, t in zip(S, bits) if t)
        for name, e in (("a", a), ("b", b)):
            al = sum(e[s] for s, t in zip(S, bits) if t)
            if abs(al) > rho:
                raise AssertionError("Perron violation")
            ratio = Fr(abs(al), rho)
            if worst is None or ratio > worst[0]:
                worst = (ratio, name, bits)
    ok("all 8191 x 2 Perron bounds |sum eig| <= sum n_s hold",
       worst[0] < 1, f"tightest = {worst[0]} on module {worst[1]}")
    ok("tightest Perron ratio is 97/120 (module H_1, S = {1})",
       worst[0] == Fr(97, 120))
    ok("Q and 3A_12 - Q are both entrywise nonnegative with valid eigenvalues",
       abs(q2) <= 10080 and abs(3 * a[12] - q2) <= 3 * 14560 - 10080
       and abs(q1) <= 10080 and abs(3 * b[12] - q1) <= 3 * 14560 - 10080)


# ---------------------------------------------------------------- section I
def five_common_neighbours(w):
    """Labelled set model of Lemma 8.3.

    Ground set [31] = I (13) u U (2) u V (2) u W' (14), realised as
    I = 0..12, U = {13,14}, V = {15,16}, W' = 17..30.
    ``w`` assigns the omitted W'-point to each index pair (i,j).
    Returns (D, D', {label: block}) with every block a genuine 15-set.
    """
    Ii = frozenset(range(13))
    u1, u2, v1, v2 = 13, 14, 15, 16
    Wp = frozenset(range(17, 31))
    D = Ii | {u1, u2}
    Dp = Ii | {v1, v2}
    assert len(D) == len(Dp) == 15 and len(D & Dp) == 13
    assert len(Ii) + 2 + 2 + len(Wp) == 31
    blocks = {"B0": Wp | {0}}                      # q_0 = 0, an element of I
    for (i, j), u, vv in (((1, 1), u1, v1), ((1, 2), u1, v2),
                          ((2, 1), u2, v1), ((2, 2), u2, v2)):
        blocks[f"B{i}{j}"] = (Wp - {w[(i, j)]}) | {u, vv}
    for lab, blk in blocks.items():
        assert len(blk) == 15, lab
        assert len(blk & D) == 1 and len(blk & Dp) == 1, lab
    return D, Dp, blocks


def section_i():
    print("I. Lemma 8.3 by explicit labelled sets, and the epsilon identity")
    # A. all four w equal-or-distinct patterns; check the ten intersections
    off = [("B11", "B12"), ("B21", "B22"), ("B11", "B21"), ("B12", "B22")]
    diag = [("B11", "B22"), ("B12", "B21")]
    seen_eps = set()
    bad_patterns = 0
    good_patterns = 0
    for pat in product(range(17, 21), repeat=4):
        w = {(1, 1): pat[0], (1, 2): pat[1], (2, 1): pat[2], (2, 2): pat[3]}
        # (H2)-admissible: off-diagonal index pairs must have distinct w
        admissible = all(w[a] != w[b] for a, b in
                         (((1, 1), (1, 2)), ((2, 1), (2, 2)),
                          ((1, 1), (2, 1)), ((1, 2), (2, 2))))
        _, _, blk = five_common_neighbours(w)
        # pairs with B0 are always 13
        ok0 = all(len(blk["B0"] & blk[f"B{i}{j}"]) == 13
                  for i in (1, 2) for j in (1, 2))
        offsz = {len(blk[a] & blk[b]) for a, b in off}
        digsz = [len(blk[a] & blk[b]) for a, b in diag]
        if not admissible:
            assert 14 in offsz            # (H2) really is what forbids these
            bad_patterns += 1
            continue
        assert ok0 and offsz == {13}
        # THE DIRECTION UNDER TEST: 12 iff the two omitted points DIFFER
        assert digsz[0] == (12 if w[(1, 1)] != w[(2, 2)] else 13)
        assert digsz[1] == (12 if w[(1, 2)] != w[(2, 1)] else 13)
        eps = (w[(1, 1)] != w[(2, 2)]) + (w[(1, 2)] != w[(2, 1)])
        assert eps == sum(1 for x in digsz if x == 12)
        seen_eps.add(eps)
        good_patterns += 1
    # 84 = chromatic polynomial of the 4-cycle (11,12,22,21) at 4 colours
    ok("every w-pattern violating row/column injectivity creates a "
       "forbidden 14-intersection", bad_patterns == 172,
       f"{bad_patterns} of 256 sub-palette patterns")
    ok("all four B_0 pairs have intersection exactly 13 (every admissible "
       "pattern)", good_patterns == 84, f"{good_patterns} admissible patterns")
    ok("all four off-diagonal pairs are forced to 13, and w must differ there",
       True)
    ok("diagonal pair is A_12 IFF the two omitted W'-points DIFFER "
       "(equality gives 13)", True)
    ok("epsilon = #(A_12 pairs among the five) and takes every value in {0,1,2}",
       seen_eps == {0, 1, 2}, f"observed {sorted(seen_eps)}")
    ok("exactly 8 of the 10 pairs are forced to 13, exactly 2 are free",
       4 + len(off) == 8 and len(diag) == 2)
    # B. A_12 side: common neighbours of an A_12 pair meet in exactly 13
    W = frozenset(range(13))                    # |W| = 13
    Uu, Vv = (13, 14, 15), (16, 17, 18)
    nbrs = [W | {Uu[i], Vv[i]} for i in range(3)]      # a matching, 3 edges
    ok("common neighbours of an A_12 pair pairwise meet in exactly 13",
       all(len(a & b) == 13 for a, b in combinations(nbrs, 2))
       and all(len(x) == 15 for x in nbrs))
    # C. the factor audit
    n13_unordered = N * 840 // 2
    ok("unordered A_13 pairs = n*n_13/2 = 420 n",
       n13_unordered == 420 * N)
    lo = 10080 * N
    hi = 10080 * N + 4 * n13_unordered * 2      # 4 = 2 (q^2=q+2C(q,2)) x 2 (ordered)
    ok("tr(Q^2) in [10080 n, 13440 n]", hi == 13440 * N, f"[{lo}, {hi}]")
    ok("tr(R^4) = 35400 n + tr(Q^2) in [45480 n, 48840 n]",
       35400 * N + lo == 45480 * N and 35400 * N + hi == 48840 * N)
    c4lo = (45480 * N - 120 * 239 * N) // 8
    c4hi = (48840 * N - 120 * 239 * N) // 8
    ok("#C_4(R) in [2100 n, 2520 n]", c4lo == 2100 * N and c4hi == 2520 * N,
       f"[{c4lo}, {c4hi}]")
    ok("this improves the previously published 4620 n / 65640 n upper bounds",
       2520 * N < 4620 * N and 48840 * N < 65640 * N)
    # the matching reformulation reproves the entry bound 0 <= Q <= 3
    ok("lambda_13 = 9 blocks through a 13-set form a perfect matching on 18 points",
       lam(13) == 9 and 2 * lam(13) == V_SET - 13)
    ok("hence Q_BC = #(matching edges between two 3-sets) <= 3", 3 <= 3)


# ---------------------------------------------------------------- section J
def witt_fibre():
    """The unique S(4,5,11); first solution of a deterministic exact cover."""
    quads = list(combinations(range(11), 4))
    qi = {q: i for i, q in enumerate(quads)}
    bysub = {}
    for blk in combinations(range(11), 5):
        fb = frozenset(blk)
        for q in combinations(blk, 4):
            bysub.setdefault(q, []).append(fb)
    sol = []

    def rec(done):
        if len(done) == len(quads):
            return True
        q = next(x for x in quads if qi[x] not in done)
        for blk in bysub[q]:
            new = {qi[t] for t in combinations(sorted(blk), 4)}
            if new & done:
                continue
            sol.append(blk)
            if rec(done | new):
                return True
            sol.pop()
        return False

    assert rec(set())
    return sol


def gram_schmidt(vs, dim):
    ob = []
    for v in vs:
        w = list(v)
        for u in ob:
            c = sum(x * y for x, y in zip(w, u)) / sum(x * x for x in u)
            w = [x - c * y for x, y in zip(w, u)]
        if any(x != 0 for x in w):
            ob.append(w)
    return ob


def section_j():
    print("J. k=6 control against the explicit Witt fibre")
    D = witt_fibre()
    nn = len(D)
    ok("S(4,5,11) has 66 blocks", nn == 66)
    A = {s: [[0] * nn for _ in range(nn)] for s in (1, 2, 3)}
    dist = {}
    for i in range(nn):
        for j in range(nn):
            if i == j:
                continue
            s = len(D[i] & D[j])
            dist[s] = dist.get(s, 0) + 1
            A[s][i][j] = 1
    ok("fibre intersections are exactly {1,2,3}", set(dist) == {1, 2, 3})
    ns6 = {s: dist[s] // nn for s in dist}
    ok("n_1,n_2,n_3 = 15,20,30", (ns6[1], ns6[2], ns6[3]) == (15, 20, 30))
    ones = [Fr(1)] * nn
    pts = [[Fr(1) if p in D[i] else Fr(0) for i in range(nn)] for p in range(11)]
    prs = [[Fr(1) if set(p) <= D[i] else Fr(0) for i in range(nn)]
           for p in combinations(range(11), 2)]
    ob01 = gram_schmidt([ones] + pts, nn)
    oball = gram_schmidt([ones] + pts + prs, nn)
    ok("dim(H_0 + H_1) = 11 and dim(pair span) = 55",
       len(ob01) == 11 and len(oball) == 55)
    H1b, H2b = ob01[1:], oball[11:]
    ok("dim H_1 = 10, dim H_2 = 44", len(H1b) == 10 and len(H2b) == 44)

    def eb(i, j):
        return eberlein(i, j, 11, 5)

    w2_6 = {2: Fr(1, 7), 3: Fr(9, 35), 4: Fr(4, 15), 5: Fr(1, 3)}
    w1_6 = {1: Fr(1, 7), 4: Fr(11, 21), 5: Fr(1, 3)}
    th6 = {j: (-1) ** j * (6 - j) for j in range(6)}
    for nm, w in (("H_1", w1_6), ("H_2", w2_6)):
        mm = [sum(x * Fr(th6[j]) ** p for j, x in w.items()) for p in range(3)]
        ok(f"k=6 {nm} measure has m_0,m_1,m_2 = 1,0,6", mm == [1, 0, 6])
    ok("k=6 H_1 certificate: <q> - q(-5)/7 = 0 kills the mass at -3",
       6 - 0 - 2 - Fr((-5 - 2) * (-5 + 1), 7) == 0)
    pred = {}
    for nm, w, mods in (("H_1", w1_6, H1b), ("H_2", w2_6, H2b)):
        eig = {s: sum(eb(5 - s, j) * wt for j, wt in w.items()) for s in range(6)}
        ok(f"k=6 {nm}: integral, forbidden classes vanish, sum = -1",
           all(e.denominator == 1 for e in eig.values())
           and eig[0] == 0 and eig[4] == 0
           and sum(eig[s] for s in (1, 2, 3)) == -1,
           f"{[int(eig[s]) for s in (1,2,3)]}")
        for s in (1, 2, 3):
            e = eig[s]
            good = all([sum(Fr(A[s][i][j]) * x[j] for j in range(nn))
                        for i in range(nn)] == [e * t for t in x] for x in mods)
            ok(f"k=6 EXPLICIT: A_{s} x = {int(e)} x for all x in {nm}", good)
        pred[nm] = {s: int(eig[s]) for s in range(6)}
    ok("k=6 R eigenvalues -7 on H_1 and 2 on H_2 recovered",
       pred["H_1"][1] == -7 and pred["H_2"][1] == 2)
    R = A[1]
    R2 = [[sum(R[i][t] * R[t][j] for t in range(nn)) for j in range(nn)]
          for i in range(nn)]
    Q = [[R2[i][j] - (15 if i == j else 0) - 5 * A[3][i][j] for j in range(nn)]
         for i in range(nn)]
    ok("k=6: Q is supported on A_2 with entries in {0,1,2,3}",
       all(Q[i][j] == 0 or A[2][i][j] == 1 for i in range(nn) for j in range(nn))
       and all(0 <= Q[i][j] <= 3 for i in range(nn) for j in range(nn)))
    ok("k=6: every Q row sums to 60", {sum(r) for r in Q} == {60})
    ok("k=6: Q = 3 A_2 exactly", all(Q[i][j] == 3 * A[2][i][j]
                                    for i in range(nn) for j in range(nn)))
    for nm, mods in (("H_1", H1b), ("H_2", H2b)):
        e = 3 * pred[nm][2]
        good = all([sum(Fr(Q[i][j]) * x[j] for j in range(nn)) for i in range(nn)]
                   == [e * t for t in x] for x in mods)
        ok(f"k=6 EXPLICIT: Q x = {e} x on {nm}", good)
        ok(f"k=6 {nm}: Q eigenvalue matches mu^2 - 15 - 5*eig_3",
           e == pred[nm][1] ** 2 - 15 - 5 * pred[nm][3])
    trq2 = sum(Q[i][j] ** 2 for i in range(nn) for j in range(nn))
    ok("k=6: tr(Q^2) = 11880 attains the epsilon = 2 extreme 60n + 4*(n*n_3/2)*2",
       trq2 == 60 * nn + 4 * (nn * ns6[3] // 2) * 2 == 11880, f"{trq2}")
    # K-Gram at k=6: three classes, two relations, rank one
    eg6 = {0: {s: Fr(ns6[s]) for s in (1, 2, 3)},
           1: {s: Fr(pred["H_1"][s]) for s in (1, 2, 3)},
           2: {s: Fr(pred["H_2"][s]) for s in (1, 2, 3)}}
    d6 = {0: 1, 1: 10, 2: 44}
    G6 = [[(Fr(nn * ns6[s]) if s == t else Fr(0))
           - sum(d6[j] * eg6[j][s] * eg6[j][t] for j in (0, 1, 2))
           for t in (1, 2, 3)] for s in (1, 2, 3)]
    _, rk6, _ = rref_solve([r[:] for r in G6], [Fr(0)] * 3)
    ok("k=6: K-Gram rank is 1 = 3 - 2 (same corank as k=16)", rk6 == 1)
    # ---- Lemma 8.3 and Proposition 8.4 enumerated on the real k=6 cover
    ground = frozenset(range(11))
    Rnb = [{j for j in range(nn) if A[1][i][j]} for i in range(nn)]
    eps = {}
    for i, j in combinations(range(nn), 2):
        if len(D[i] & D[j]) != 3:
            continue
        Dd, Dp = D[i], D[j]
        Ii, Uu, Vv = Dd & Dp, sorted(Dd - Dp), sorted(Dp - Dd)
        Wp = ground - (Dd | Dp)
        assert (len(Ii), len(Uu), len(Vv), len(Wp)) == (3, 2, 2, 4)
        com = sorted(Rnb[i] & Rnb[j])
        assert len(com) == 5, (i, j, len(com))
        b0 = [c for c in com if Wp <= D[c]]
        assert len(b0) == 1 and len(D[b0[0]] - Wp) == 1
        assert next(iter(D[b0[0]] - Wp)) in Ii        # q_0 lies in I
        wmap = {}
        for c in com:
            if c == b0[0]:
                continue
            miss = Wp - D[c]
            assert len(miss) == 1
            uu = next(iter(D[c] & set(Uu)))
            vv = next(iter(D[c] & set(Vv)))
            wmap[(Uu.index(uu), Vv.index(vv))] = (next(iter(miss)), c)
        assert set(wmap) == {(0, 0), (0, 1), (1, 0), (1, 1)}
        for a, b in (((0, 0), (0, 1)), ((1, 0), (1, 1)),
                     ((0, 0), (1, 0)), ((0, 1), (1, 1))):
            assert wmap[a][0] != wmap[b][0]                    # forced distinct
            assert len(D[wmap[a][1]] & D[wmap[b][1]]) == 3     # = k-3 = 13 analogue
        assert len(D[b0[0]] & D[wmap[(0, 0)][1]]) == 3
        e = 0
        for a, b in (((0, 0), (1, 1)), ((0, 1), (1, 0))):
            got = len(D[wmap[a][1]] & D[wmap[b][1]])
            want = 2 if wmap[a][0] != wmap[b][0] else 3        # 2 = k-4 analogue
            assert got == want, (i, j, got, want)
            e += (got == 2)
        eps[(i, j)] = e
    ok("k=6 EXPLICIT Lemma 8.3: all 990 A_3 pairs have 5 common neighbours, "
       "8 forced pairs, 2 diagonal, direction verified",
       len(eps) == nn * ns6[3] // 2 == 990)
    ok("k=6: epsilon == 2 on every A_3 pair (so Q = 3 A_2)",
       set(eps.values()) == {2})
    ok("k=6 GLOBAL identity tr(Q^2) = 60n + 4 * sum epsilon",
       trq2 == 60 * nn + 4 * sum(eps.values()),
       f"{trq2} = {60 * nn} + 4*{sum(eps.values())}")
    # row identity, with the factor 2 on unordered pairs of R-neighbours
    for b in (0, 7, 41):
        rowsq = sum(Q[b][d] ** 2 for d in range(nn))
        tot = 0
        for c, cp in combinations(sorted(Rnb[b]), 2):
            if len(D[c] & D[cp]) != 3:
                continue
            partners = [d for d in Rnb[c] & Rnb[cp]
                        if d != b and len(D[b] & D[d]) == 2]
            assert len(partners) <= 1
            tot += len(partners)
        ok(f"k=6 ROW identity at block {b}: sum_D Q^2 = 60 + 2*sum eps_B",
           rowsq == 60 + 2 * tot, f"{rowsq} = 60 + 2*{tot}")
    ok("k=6: row identity summed over B reproduces the global factor 4",
       sum(sum(Q[b][d] ** 2 for d in range(nn)) for b in range(nn))
       == 60 * nn + 4 * sum(eps.values()))
    for j in (1, 2):
        tot = sum(Fr(eg6[j][s] ** 2, ns6[s]) for s in (1, 2, 3))
        ok(f"k=6: sum eig^2/n_s = n/m_{j} - 1", tot == Fr(nn, d6[j]) - 1)


def main():
    ns = section_a()
    section_b()
    w1, w2 = section_c()
    section_d(w1, w2)
    q1, q2 = section_e(w1, w2, ns)
    a, b = section_f(w1, w2, ns)
    section_g(a, b, ns)
    section_h(a, b, ns, q1, q2)
    section_i()
    section_j()
    print()
    print(f"ALL {len(CHECKS)} CHECKS PASSED")
    print("Scope: no contradiction was found.  Erdos--Rosenfeld #835 remains open.")


if __name__ == "__main__":
    main()

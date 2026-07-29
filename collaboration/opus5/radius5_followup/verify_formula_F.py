#!/usr/bin/env python3
"""Line-by-line audit of the flag Alon-Tarsi formula (F).

    prod_{i,u} AT(Q^{i,u}) = (-1)^(k(k-1)/2) * AT(T) * prod_i delta(S_i)

VERDICT: PROVED, and every ingredient verified on real radius-3 data.

Stdlib only, no solver.  Labels: PROVED / COMPUTATION / OPEN.

Key point that makes non-degenerate testing possible: steps 1-5 all depend on
L and M only.  The VALUES of N never enter -- only its forced image sets do.
So the whole right-hand side and every step factor is testable at k = 6 (real
radius-3 families) and k = 16 (Wallis), even though no radius-5 object exists.

Run:  python3 -B collaboration/opus5/radius5_followup/verify_formula_F.py
"""
from __future__ import annotations

import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from verify_radius3_census_and_k6_obstruction import (  # noqa: E402
    all_sils, discordant_families, wallis_sils)


def sgn_seq(seq):
    s, seq = 1, list(seq)
    n = len(seq)
    seen = [False] * n
    for i in range(n):
        if seen[i]:
            continue
        L, j = 0, i
        while not seen[j]:
            seen[j] = True
            L += 1
            j = seq[j]
        if L % 2 == 0:
            s = -s
    return s


def sgn_map(dom, tgt, f):
    ti = {x: t for t, x in enumerate(tgt)}
    return sgn_seq([ti[f[d]] for d in dom])


def ent(S, a, b):
    return S[(min(a, b), max(a, b))] if a != b else a


# ------------------------------------------------------------------ primitives

def section0():
    print("=" * 74)
    print("0.  The two primitives (PROVED, and verified on random instances)")
    print("=" * 74)
    print("    DELETION RULE.  Deleting domain position r and its image")
    print("    position s multiplies the sign by (-1)^(r+s).")
    print()
    print("    LEMMA (C).  For g: D -> C\\{a,b}, f_a = g + (* -> b) into C\\{a},")
    print("    f_b = g + (* -> a) into C\\{b}, with * last in the domain:")
    print("        sgn(f_a) sgn(f_b) = (-1)^(pos(a)+pos(b)+1).")
    print("    Proof.  By the deletion rule sgn(f_a) = (-1)^(r+s_a) sgn(g) and")
    print("    sgn(f_b) = (-1)^(r+s_b) sgn(g) with the same r (=|D|), so the")
    print("    product is (-1)^(s_a+s_b).  Now")
    print("      s_a = pos_{C\\{a}}(b) = pos(b) - [pos(a) < pos(b)],")
    print("      s_b = pos_{C\\{b}}(a) = pos(a) - [pos(b) < pos(a)],")
    print("    and exactly one indicator is 1 since a != b, so")
    print("    s_a + s_b = pos(a) + pos(b) - 1. []")
    rnd = random.Random(7)
    badC = badD = 0
    for _ in range(3000):
        m = rnd.randrange(1, 7)
        C = list(range(m + 2))
        a, b = rnd.sample(C, 2)
        rest = [c for c in C if c not in (a, b)]
        D = list(range(m))
        img = rest[:]
        rnd.shuffle(img)
        g = {d: img[t] for t, d in enumerate(D)}
        fa = {**g, '*': b}
        fb = {**g, '*': a}
        dom = D + ['*']
        sa = sgn_map(dom, [c for c in C if c != a], fa)
        sb = sgn_map(dom, [c for c in C if c != b], fb)
        if sa * sb != (-1) ** (C.index(a) + C.index(b) + 1):
            badC += 1
        n = rnd.randrange(2, 7)
        perm = list(range(n))
        rnd.shuffle(perm)
        full = sgn_seq(perm)
        r = rnd.randrange(n)
        s = perm[r]
        sub = [x - (1 if x > s else 0) for t, x in enumerate(perm) if t != r]
        if sgn_seq(sub) != (-1) ** (r + s) * full:
            badD += 1
    print(f"    3000 random instances each: lemma (C) violations {badC},"
          f" deletion-rule violations {badD}")
    assert badC == 0 and badD == 0


# ------------------------------------------------------------------ the audit

def analyse(F, n, INF):
    V = [c for c in range(n) if c != INF]
    k = len(V)
    A = list(range(len(F)))
    assert k == len(A) + 1 and k % 2 == 0
    Corder = V + [INF]
    L = [{u: ent(F[i], INF, u) for u in V} for i in A]
    pos = {x: t for t, x in enumerate(V)}
    sgnL = [sgn_map(V, V, L[i]) for i in A]

    def delta(S):
        d = 1
        for q in range(n):
            d *= sgn_map(range(n), range(n), {y: ent(S, q, y) for y in range(n)})
        return d

    s1, per_u = 1, []
    for u in V:
        f = 1
        for a in range(len(A)):
            for b in range(a + 1, len(A)):
                f *= (-1) ** (pos[L[a][u]] + pos[L[b][u]] + 1)
        per_u.append(f)
        s1 *= f
    s2 = 1
    for i in A:
        for a in range(k):
            for b in range(a + 1, k):
                s2 *= (-1) ** (pos[L[i][V[a]]] + pos[L[i][V[b]]] + 1)
    s3 = s4 = s5 = 1
    for i in A:
        p4 = 1
        for u in V:
            sym = [c for c in Corder if c != L[i][u]]
            cols = [v for v in V if v != u] + ['*']
            lrow = {v: L[i][v] for v in V if v != u}
            lrow['*'] = INF
            s3 *= sgn_map(cols, sym, lrow)
            mrow = {v: ent(F[i], u, v) for v in V if v != u}
            mrow['*'] = u
            p4 *= sgn_map(cols, sym, mrow)
        assert p4 == delta(F[i]) * sgnL[i], ("step 4 identity", i)
        s4 *= p4
    for u in V:
        for i in A:
            sym = [c for c in Corder if c != L[i][u]]
            rows = [j for j in A if j != i] + ['m', 'l']
            col = {j: L[j][u] for j in A if j != i}
            col['m'] = u
            col['l'] = INF
            s5 *= sgn_map(rows, sym, col)
    Trows = A + ['e']
    T = {(i, u): L[i][u] for i in A for u in V}
    for u in V:
        T[('e', u)] = u
    RT = 1
    for r in Trows:
        RT *= sgn_map(V, V, {u: T[(r, u)] for u in V})
    CT = 1
    for u in V:
        CT *= sgn_map(Trows, V, {r: T[(r, u)] for r in Trows})
    prodL = 1
    for i in A:
        prodL *= sgnL[i]
    assert RT == prodL, "R(T) must equal prod_i sgn(L_i)"
    c = (-1) ** (k * (k - 1) // 2)
    assert s5 == c * CT, ("step 5 identity", s5, c, CT)
    assert s3 == 1 and s2 == 1
    rhs = c * RT * CT
    for i in A:
        rhs *= delta(F[i])
    return dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, per_u=set(per_u),
                terms=s1 * s2 * s3 * s4 * s5, rhs=rhs, k=k)


def section1():
    print()
    print("=" * 74)
    print("1.  The five steps -- audited and VERIFIED on real radius-3 data")
    print("=" * 74)
    print("    Step 1 (existing rows).  Pair row j of Q^{i,u} with row i of")
    print("      Q^{j,u}.  They share the N-part, whose image is")
    print("      C\\{L_i(u), L_j(u)} by the forced trace, so (C) applies with")
    print("      a = L_i(u), b = L_j(u).  For fixed u the exponent is")
    print("        (k-2) * sum_i pos(L_i(u))  +  C(k-1,2);")
    print("      k even makes the first term even, and summing C(k-1,2) over")
    print("      the k values of u makes the second even too.  Total +1.")
    print("      PRECISION: at k = 16 the PER-u factor is (-1)^105 = -1, since")
    print("      C(15,2) = 105 is odd.  The cancellation happens ACROSS u")
    print("      (16 of them), not within a single u.")
    print("    Step 2 (existing columns).  Pair column v of Q^{i,u} with column")
    print("      u of Q^{i,v}; common image C\\{L_i(u), L_i(v)} by condition 4.")
    print("      Exponent (k-1)*sum_u pos(L_i(u)) + C(k,2) = k(k-1) mod 2 = 0.")
    print("    Step 3 (l-rows).  The l-row is the permutation v->L_i(v),")
    print("      inf->inf with domain u and image L_i(u) deleted, so its sign")
    print("      is (-1)^(pos(u)+pos(L_i(u))) sgn(L_i); over u this gives")
    print("      sgn(L_i)^k * (-1)^(k(k-1)) = +1.")
    print("    Step 4 (m-rows).  Delete domain inf / image L_i(u) from row u of")
    print("      S_i, then move u to last.  The bookkeeping exponent is")
    print("      k(k-1), even, so prod_u sgn(m-row) = prod_u sgn(pi_{i,u})")
    print("      = delta(S_i) sgn(L_i), row inf of S_i having sign sgn(L_i).")
    print("    Step 5 (*-columns).  Extend to Lambda_u on A u {m,l}; deleting")
    print("      i gives the *-column.  k-1 odd keeps one factor of")
    print("      sgn(Lambda_u), and prod_{i,u} = (-1)^(k(k-1)/2) C(T).")
    print()
    print("    Assembling: 1 * [prod_i delta(S_i) * R(T)] * 1 * 1 *")
    print("    [(-1)^(k(k-1)/2) C(T)] = (-1)^(k(k-1)/2) AT(T) prod_i delta(S_i).")
    print("    That is exactly (F).  []")

    n = 7
    sq = all_sils(n)
    fams = discordant_families(sq, n, n - 2)
    rnd = random.Random(3)
    bad = 0
    seen = set()
    peru = set()
    for t, fi in enumerate(fams):
        F = [sq[j] for j in fi]
        for INF in ([rnd.randrange(n)] if t % 10 else range(n)):
            r = analyse(F, n, INF)
            seen.add((r["s1"], r["s2"], r["s3"]))
            peru |= r["per_u"]
            if r["terms"] != r["rhs"]:
                bad += 1
    print()
    print(f"    k=6, all {len(fams)} real radius-3 families:")
    print(f"      (step1, step2, step3) values seen -> {sorted(seen)}")
    print(f"      per-u step-1 factors seen -> {sorted(peru)}")
    print(f"      assembled 5-term product == RHS of (F): mismatches {bad}")
    assert bad == 0 and seen == {(1, 1, 1)}
    W = wallis_sils()
    r = analyse(W, 17, 16)
    print(f"    k=16 Wallis: steps = "
          f"{(r['s1'], r['s2'], r['s3'], r['s4'], r['s5'])}, "
          f"per-u step-1 factors {sorted(r['per_u'])}")
    print(f"      5-term product {r['terms']}, RHS of (F) {r['rhs']},"
          f" equal = {r['terms'] == r['rhs']}")
    assert r["terms"] == r["rhs"]


def section2():
    print()
    print("=" * 74)
    print("2.  k = 2, the genuine control -- and what it can and cannot test")
    print("=" * 74)
    # A = {0}, V = {0,1}, C = {0,1,inf=2}
    L0 = {0: 1, 1: 0}
    S = {(0, 1): 2, (0, 2): 1, (1, 2): 0}
    d = 1
    for q in range(3):
        d *= sgn_map(range(3), range(3),
                     {y: (y if y == q else S[(min(q, y), max(q, y))])
                      for y in range(3)})
    Trows = [0, 'e']
    T = {(0, 0): 1, (0, 1): 0, ('e', 0): 0, ('e', 1): 1}
    RT = 1
    for r in Trows:
        RT *= sgn_map([0, 1], [0, 1], {u: T[(r, u)] for u in [0, 1]})
    CT = 1
    for u in [0, 1]:
        CT *= sgn_map(Trows, [0, 1], {r: T[(r, u)] for r in Trows})
    rhs = (-1) ** (2 * 1 // 2) * RT * CT * d
    print(f"    delta(S) = {d}, AT(T) = R*C = {RT}*{CT} = {RT*CT},"
          f" (-1)^(k(k-1)/2) = {(-1)**1}")
    print(f"    RHS of (F) = {rhs}")
    print("    LHS: both flag squares have order 2, and every order-2 Latin")
    print("    square has AT = +1, so the LHS is +1.  MATCH.")
    assert rhs == 1
    print()
    print("    LIMITATION.  At k = 2, |A| = 1, so there are NO pairs ij and no")
    print("    pairs uv: steps 1 and 2 are VACUOUS.  The k=2 control therefore")
    print("    tests only steps 3, 4, 5 and the overall constant.  Steps 1 and")
    print("    2 are covered instead by the k=6 and k=16 runs in section 1,")
    print("    which exercise them on real L data.")


def section3():
    print()
    print("=" * 74)
    print("3.  Relation to the symbol product -- identity proved, value OPEN")
    print("=" * 74)
    print("    For every Latin square of order k, rho*gamma*sigma = c with")
    print("    c = (-1)^(k(k-1)/2) universal.  Hence for signs")
    print("        sigma(Q) = c * AT(Q).")
    print("    The number of flags is |A|*|V| = k(k-1), which is EVEN for")
    print("    every k.  Therefore")
    print("        prod_{i,u} sigma(Q^{i,u}) = c^(k(k-1)) * prod_{i,u} AT(Q^{i,u})")
    print("                                  = prod_{i,u} AT(Q^{i,u}).")
    k = 16
    assert (k * (k - 1)) % 2 == 0
    print(f"    At k = 16: k(k-1) = {k*(k-1)} flags, even, so c^{k*(k-1)} = +1.")
    print()
    print("    Thus the global symbol-sign product and the global AT product")
    print("    are the same invariant in any actual extension.  This does NOT")
    print("    independently evaluate the symbol side.  A further theorem")
    print("    deriving its value directly from the forced partial fibers could")
    print("    still contradict (F), and would then be a genuine obstruction.")
    print("    The R_tau lemma establishes reference-independence for the")
    print("    generic partial-fiber contribution but does not determine that")
    print("    contribution.  Such a second value formula remains OPEN. []")


def main():
    section0()
    section1()
    section2()
    section3()
    print()
    print("=" * 74)
    print("SCOPE OF (F).  PROVED for every even k.  It evaluates the global")
    print("flag AT product ENTIRELY from radius-3 (L, M) data: the values of N")
    print("cancel, only its forced image sets are used.  It is therefore a")
    print("conditional structural evaluation, NOT a contradiction.  The Wallis")
    print("radius-3/4 data make the RHS and all five algebraic factors +1, but")
    print("there is no known Wallis radius-5 extension on which to evaluate the")
    print("actual LHS.  No independent forced-fiber value has been derived.")
    print("Erdos-Rosenfeld #835 remains OPEN.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""The partial-fiber identity (H), the theorem E = +1, and a RETRACTION.

Stdlib only, no solver.  Labels: PROVED / COMPUTATION / OPEN / RETRACTED.

  1  PROVED      (H), as a corollary of (1), (7), (10), with its exact
                 CONDITIONAL scope.
  2  PROVED      E(L,M) = +1 for every even k and every chart satisfying
                 conditions 1 and 2.  Hence (H) simplifies.
  3  RETRACTED   an earlier "no universal-constant second evaluation is
                 possible" argument, which was a vacuous-truth error.
  4  COMPUTATION radius-3 controls, with H_required kept strictly distinct
                 from any observed partial-fiber product.
  5  OPEN        the real question, sharpened.

TERMINOLOGY, used throughout and not interchangeably:
  H_observed(L,M,N) -- the actual product of partial-fiber signs.  It EXISTS
                       ONLY for a genuine radius-5 structure.
  H_required(L,M)   -- the value that (H) forces H_observed to take IF such a
                       structure exists over this chart.  It is computable
                       from radius-3 data alone and is defined for charts that
                       do not extend at all.

Run:  python3 -B collaboration/opus5/radius5_followup/verify_H_identity.py
"""
from __future__ import annotations

import os
import random
import sys
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from verify_radius3_census_and_k6_obstruction import (  # noqa: E402
    all_sils, discordant_families, wallis_sils)
from verify_formula_F import analyse, sgn_map, ent  # noqa: E402


def rand_latin(k, rnd):
    L = [[-1] * k for _ in range(k)]

    def rec(p):
        if p == k * k:
            return True
        r, c = divmod(p, k)
        cand = [s for s in range(k)
                if s not in L[r][:c] and all(L[t][c] != s for t in range(r))]
        rnd.shuffle(cand)
        for s in cand:
            L[r][c] = s
            if rec(p + 1):
                return True
            L[r][c] = -1
        return False

    rec(0)
    return L


def check10(Q, k):
    rows = cols = list(range(k))
    m, l, star = k - 2, k - 1, k - 1
    ER = [r for r in rows if r not in (m, l)]
    EC = [c for c in cols if c != star]
    INF, U = Q[l][star], Q[m][star]
    Sigma = 1
    for x in range(k):
        Sigma *= sgn_map(rows, cols, {r: Q[r].index(x) for r in rows})
    prodPhi = prodEps = 1
    for x in range(k):
        dom = [r for r in ER if Q[r].index(x) != star]
        tgt = [c for c in EC if all(Q[r][c] != x for r in (m, l))]
        prodPhi *= sgn_map(dom, tgt, {r: Q[r].index(x) for r in dom})
        if x not in (INF, U):
            vM, vL = Q[m].index(x), Q[l].index(x)
            prodEps *= 1 if EC.index(vM) < EC.index(vL) else -1
    return Sigma, (-1) ** (comb(k - 2, 2) + 1) * prodEps * prodPhi


def E_value(F, n, INF, order=None):
    V = [c for c in range(n) if c != INF]
    if order:
        V = [V[t] for t in order]
    pos = {x: t for t, x in enumerate(V)}
    E = 1
    for i in range(len(F)):
        S = F[i]
        L = {u: ent(S, INF, u) for u in V}
        Linv = {c: u for u, c in L.items()}
        for u in V:
            for x in V:
                if x == u or x == L[u]:
                    continue
                vM = [w for w in V if w != u and ent(S, u, w) == x][0]
                E *= 1 if pos[vM] < pos[Linv[x]] else -1
    return E


def section1():
    print("=" * 74)
    print("1.  (H) -- PROVED, and strictly CONDITIONAL")
    print("=" * 74)
    print("    Multiplying (10) over the k(k-1) flags (an even count for every")
    print("    k) cancels the fixed per-flag factor, so")
    print("      prod_{i,u} Sigma(Q^{i,u}) = E(L,M) * H_observed(L,M,N).")
    print("    By (7) that equals prod AT, and by (1)")
    print("      H_observed = E(L,M) (-1)^(k(k-1)/2) AT(T) prod_i delta(S_i). []")
    print()
    print("    CONDITIONAL SCOPE.  H_observed exists ONLY for a genuine")
    print("    radius-5 structure, since the Phi_{i,u,x} are its partial")
    print("    fibers.  (H) says: IF a structure exists over this chart, THEN")
    print("    its H_observed equals the right-hand side.  We name that")
    print("    right-hand side H_required(L,M); it is computable from radius-3")
    print("    data and is defined even for charts that never extend.")


def section2():
    print()
    print("=" * 74)
    print("2.  THEOREM (PROVED): E(L,M) = +1 for every even k")
    print("=" * 74)
    print("    Only conditions 1 and 2 are used -- no N, no trace.")
    print()
    print("    Fix i and a colour x, and put v = L_i^-1(x).  A term of E exists")
    print("    exactly for the generic u, i.e. u != x and u != v, so u runs")
    print("    over V\\{x,v}.  By condition 2 the colour-x class of M_i is a")
    print("    perfect matching of V\\{x,v}; let mu be that involution, so")
    print("    v_M = mu(u) and v_L = v.  Since mu is a bijection of V\\{x,v},")
    print("      block(i,x) = prod_{u} eps(mu(u), v) = prod_{w != x,v} eps(w,v),")
    print("    which no longer mentions mu at all.  Hence")
    print("      block(i,x) = (-1)^(#{w in V : w > v} - [x > v]).")
    print("    Regrouping E = prod_i prod_x block(i,x) and substituting")
    print("    x = L_i(v) turns the exponent into")
    print("      sum_v (k-1-pos(v))  +  #{v : L_i(v) > v}  =  k(k-1)/2 + a_i.")
    print("    Finally condition 1 gives {L_i(v) : i in A} = V\\{v} for each v,")
    print("    so summing the ascent counts over i,")
    print("      sum_i a_i = sum_v #{w != v : w > v} = k(k-1)/2.")
    print("    Therefore the total exponent is")
    print("      (k-1)*k(k-1)/2 + k(k-1)/2 = k * k(k-1)/2 = k^2(k-1)/2,")
    print("    and for k = 2m this is 2m^2(2m-1), even.  So E = +1. []")
    print()
    print("    CONSEQUENCE.  (H) simplifies to")
    print("      H_required(L,M) = (-1)^(k(k-1)/2) AT(T) prod_i delta(S_i),")
    print("    i.e. H_required = RHS(F) exactly.  What was a CONJECTURE in the")
    print("    previous revision is now a theorem.")

    rnd = random.Random(5)
    n = 7
    sq = all_sils(n)
    fams = discordant_families(sq, n, n - 2)
    F0 = [sq[j] for j in fams[0]]
    vals = {E_value(F0, n, 0, order=rnd.sample(range(6), 6)) for _ in range(40)}
    print(f"    COMPUTATION: 40 random orders on V give E in {vals}"
          f" (order-invariance, = the R_tau lemma)")
    assert vals == {1}
    seen = set()
    for fi in fams:
        for INF in range(n):
            seen.add(E_value([sq[j] for j in fi], n, INF))
    print(f"    COMPUTATION k=6: E over all {len(fams)*n} chart/root cases"
          f" -> {seen}")
    assert seen == {1}
    W = wallis_sils()
    seen16 = {E_value(W, 17, INF) for INF in range(17)}
    print(f"    COMPUTATION k=16 Wallis: E over all 17 root colours -> {seen16}")
    assert seen16 == {1}


def section3():
    print()
    print("=" * 74)
    print("3.  RETRACTION")
    print("=" * 74)
    print("    The previous revision argued: because H_required takes BOTH")
    print("    signs over the k=6 radius-3 census, no universal-constant second")
    print("    evaluation H = C is possible.")
    print()
    print("    THAT INFERENCE IS INVALID, and is withdrawn.  NONE of the 1680")
    print("    k=6 radius-3 families extends to radius 4/5 -- every one dies at")
    print("    radius 4.  So no N-table and no H_observed exists in any of those")
    print("    controls: the computed values are H_required, conditionals with")
    print("    FALSE antecedents, hence vacuously true and constraining nothing.")
    print("    A theorem quantified over GENUINE radius-5 structures may well")
    print("    assert H_observed = C; combined with (H) it would simply exclude")
    print("    every chart whose H_required differs from C.  The k=6 census")
    print("    cannot be a counterexample to such a theorem -- it contains no")
    print("    instances of it.")
    print()
    print("    Nothing else in this file depended on that inference.")


def section4():
    print()
    print("=" * 74)
    print("4.  COMPUTATION -- radius-3 controls (H_required only)")
    print("=" * 74)
    rnd = random.Random(11)
    for k in (4, 6, 8):
        bad = sum(1 for _ in range(200)
                  if (lambda t: t[0] != t[1])(check10(rand_latin(k, rnd), k)))
        print(f"    identity (10) on 200 random Latin squares of order {k}:"
              f" mismatches {bad}")
        assert bad == 0
    n = 7
    sq = all_sils(n)
    fams = discordant_families(sq, n, n - 2)
    dist = {}
    for fi in fams:
        F = [sq[j] for j in fi]
        for INF in range(n):
            dist[analyse(F, n, INF)["rhs"]] = \
                dist.get(analyse(F, n, INF)["rhs"], 0) + 1
    print(f"    k=6, all {len(fams)} labelled families x {n} root colours:")
    print(f"      H_required distribution -> {dict(sorted(dist.items()))}")
    print("      NB none of these charts extends to radius 4/5, so NO")
    print("      H_observed exists for any of them.  These are conditionals.")
    W = wallis_sils()
    r = analyse(W, 17, 16)["rhs"]
    allr = {analyse(W, 17, INF)["rhs"] for INF in range(17)}
    print(f"    k=16 Wallis: E = +1, H_required = {r}; over all 17 roots {allr}")
    print("      Wallis has a certified radius-4 extension, but whether it")
    print("      extends to radius 5 is UNKNOWN; no H_observed is available.")


def section5():
    print()
    print("=" * 74)
    print("5.  The real open question, sharpened")
    print("=" * 74)
    print("    With E = +1 proved, (H) reads")
    print("      H_observed = (-1)^(k(k-1)/2) AT(T) prod_i delta(S_i),")
    print("    and at k = 16 the leading factor is +1, so")
    print("      H_observed = AT(T) prod_i delta(S_i).")
    print()
    print("    OPEN.  Can genuine two-sided N-tables force a value of")
    print("    H_observed -- universal, or a function of (L,M)?")
    print()
    print("    WHY THIS IS NOW A REAL EXCLUSION ROUTE.  Suppose some theorem")
    print("    about the forced fiberings gives H_observed = C for every")
    print("    genuine radius-5 structure.  Combined with (H) that is an")
    print("    outright NECESSARY CONDITION ON THE RADIUS-3 CHART:")
    print("      AT(T) prod_i delta(S_i) = C (-1)^(k(k-1)/2),")
    print("    and every chart failing it cannot extend.  At k = 16 Wallis has")
    print("    AT(T) prod_i delta(S_i) = +1, so a theorem with C = -1 would")
    print("    exclude Wallis outright -- and would exclude unrestricted k = 16")
    print("    iff no admissible chart attains +1.")
    print()
    print("    NOT SETTLED HERE, in either direction.  I have neither derived")
    print("    such a C from the per-ij or per-uv fiberings nor shown that none")
    print("    exists.  The one-sided synthetic falsification (build N-tables")
    print("    obeying only the per-ij constraints, then only the per-uv ones,")
    print("    and see whether H_observed takes both signs) is the natural next")
    print("    step and was not carried out.")


def main():
    section1()
    section2()
    section3()
    section4()
    section5()
    print()
    print("=" * 74)
    print("No contradiction and no construction.  Excluding k=16 would in any")
    print("case leave the other prime cases, so the unrestricted existential")
    print("problem is untouched.  Erdos-Rosenfeld #835 remains OPEN.")


if __name__ == "__main__":
    main()

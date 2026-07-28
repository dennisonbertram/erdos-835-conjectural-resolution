#!/usr/bin/env python3
"""Exact r=0 obstruction to the complement-cover six-prefix route.

Standard library only.  No optimizer, no SAT solver.

Contents
--------
1.  An explicit class-B target instance of profile (n8, n10, n12) = (7, 10, 0)
    on 13 vertices (every vertex in exactly five complements).
2.  An explicit complement-cover six-prefix of support pattern 8^3 10^3:
    three five-set complements and three triple complements whose union
    covers all thirteen vertices, together with six pairwise edge-disjoint
    prescribed perfect matchings.
3.  A proof by exhaustion that of the eleven remaining supports exactly two
    admit a perfect matching in the residual graph, so the prefix extends to
    eight and never to nine.
4.  A witness eight-packing, and an exhaustive maximum-packing computation
    for the whole instance (over all 17 supports) showing the instance
    itself is not a counterexample to coordinated nine.
"""

import itertools
import sys

N = 13
VERTS = tuple(range(N))

# ---------------------------------------------------------------- utilities


def edges_of(vs):
    return [frozenset(e) for e in itertools.combinations(sorted(vs), 2)]


def perfect_matchings(support, allowed):
    """All perfect matchings of the graph (support, allowed-edges)."""
    support = tuple(sorted(support))
    if len(support) % 2:
        return []
    out = []

    def rec(rest, acc):
        if not rest:
            out.append(tuple(acc))
            return
        a = rest[0]
        for i in range(1, len(rest)):
            b = rest[i]
            e = frozenset((a, b))
            if e in allowed:
                rec(rest[1:i] + rest[i + 1:], acc + [e])

    rec(support, [])
    return out


def has_perfect_matching(support, allowed):
    support = tuple(sorted(support))
    if len(support) % 2:
        return False

    def rec(rest):
        if not rest:
            return True
        a = rest[0]
        for i in range(1, len(rest)):
            b = rest[i]
            if frozenset((a, b)) in allowed:
                if rec(rest[1:i] + rest[i + 1:]):
                    return True
        return False

    return rec(support)


# --------------------------------------------------------------- the instance

C = [0, 1, 2, 3, 4, 5]          # the K6 block of the prefix union

# selected complements (the six-prefix)
G1 = frozenset({0, 1, 6, 10, 11})
G2 = frozenset({2, 4, 7, 11, 12})
G3 = frozenset({3, 5, 6, 7, 12})
T1 = frozenset({6, 7, 8})
T2 = frozenset({6, 7, 9})
T3 = frozenset({6, 7, 10})
SELECTED = [G1, G2, G3, T1, T2, T3]

# remaining complements
REM_FIVE = [frozenset(set(C) - {c}) for c in (0, 1, 2, 3)]
REM_W_TRIPLES = [frozenset(t) for t in
                 ({8, 9, 10}, {8, 9, 11}, {8, 10, 12}, {9, 11, 12}, {10, 11, 12})]
Ta = frozenset({0, 1, 8})
Tb = frozenset({2, 3, 9})
REMAINING = REM_FIVE + REM_W_TRIPLES + [Ta, Tb]

COMPLEMENTS = SELECTED + REMAINING
SUPPORTS = [frozenset(VERTS) - c for c in COMPLEMENTS]

# the six prescribed matchings of the prefix
M_G1 = [(3, 4), (2, 5), (7, 9), (8, 12)]
M_G2 = [(1, 3), (0, 5), (6, 8), (9, 10)]
M_G3 = [(0, 4), (1, 2), (8, 9), (10, 11)]
M_T1 = [(0, 1), (2, 3), (4, 5), (9, 11), (10, 12)]
M_T2 = [(0, 2), (1, 4), (3, 5), (8, 10), (11, 12)]
M_T3 = [(0, 3), (1, 5), (2, 4), (8, 11), (9, 12)]
PREFIX = [M_G1, M_G2, M_G3, M_T1, M_T2, M_T3]
PREFIX = [[frozenset(e) for e in m] for m in PREFIX]


def main():
    ok = True

    def check(label, cond):
        nonlocal ok
        print(("PASS  " if cond else "FAIL  ") + label)
        ok = ok and bool(cond)

    # ---- 1. class-B arithmetic --------------------------------------------
    sizes = sorted(len(c) for c in COMPLEMENTS)
    check("17 complements", len(COMPLEMENTS) == 17)
    check("profile: seven 5-sets and ten 3-sets",
          sizes == [3] * 10 + [5] * 7)
    mult = {v: sum(1 for c in COMPLEMENTS if v in c) for v in VERTS}
    check("every vertex in exactly five complements",
          all(m == 5 for m in mult.values()))
    supp_sizes = sorted(len(s) for s in SUPPORTS)
    check("support profile (n8,n10,n12)=(7,10,0)",
          supp_sizes == [8] * 7 + [10] * 10)

    # ---- 2. the six-prefix -------------------------------------------------
    cover = set().union(*SELECTED)
    check("selected complements cover all 13 vertices", cover == set(VERTS))
    check("selected: three 5-sets and three 3-sets",
          sorted(len(c) for c in SELECTED) == [3, 3, 3, 5, 5, 5])

    good = True
    for c, m in zip(SELECTED, PREFIX):
        sup = set(VERTS) - set(c)
        covered = set()
        for e in m:
            covered |= set(e)
        good = good and covered == sup and 2 * len(m) == len(sup)
    check("each prefix matching is a perfect matching on its support", good)

    allpref = [e for m in PREFIX for e in m]
    check("prefix matchings pairwise edge-disjoint",
          len(set(allpref)) == len(allpref))
    D = set(allpref)
    check("|E(D)| = 27", len(D) == 27)

    degD = {v: sum(1 for e in D if v in e) for v in VERTS}
    check("Delta(D) <= 5", max(degD.values()) <= 5)
    sigma = {v: sum(1 for c in SELECTED if v in c) for v in VERTS}
    check("d_D(v) = 6 - sigma(v) for all v",
          all(degD[v] == 6 - sigma[v] for v in VERTS))
    rho = {v: sum(1 for c in REMAINING if v in c) for v in VERTS}
    check("rho(v) = d_D(v) - 1 for all v",
          all(rho[v] == degD[v] - 1 for v in VERTS))

    K6 = set(edges_of(C))
    check("D restricted to C is exactly K6",
          {e for e in D if e <= set(C)} == K6)
    check("D has no edge between C and its complement",
          not any(len(e & set(C)) == 1 for e in D))
    check("|D outside C| = 12",
          len([e for e in D if not (e & set(C))]) == 12)

    ALL = set(edges_of(VERTS))
    H = ALL - D
    degH = {v: sum(1 for e in H if v in e) for v in VERTS}
    check("delta(H) >= 7", min(degH.values()) >= 7)

    # ---- 3. exhaustive blocking of the eleven remaining supports ----------
    HO = {e for e in H if not (e & set(C))}
    check("H restricted to the outside 7-set has 9 edges", len(HO) == 9)
    # maximum matching of H[O] by brute force
    best = 0
    for r in (3, 2, 1):
        found = False
        for comb in itertools.combinations(sorted(HO, key=sorted), r):
            vs = set()
            bad = False
            for e in comb:
                if e & vs:
                    bad = True
                    break
                vs |= set(e)
            if not bad:
                found = True
                break
        if found:
            best = r
            break
    check("matching number of H[O] is exactly 2", best == 2)

    unblocked = []
    for c, s in zip(REMAINING, [frozenset(VERTS) - c for c in REMAINING]):
        if has_perfect_matching(s, H):
            unblocked.append(c)
    check("exactly two of the eleven remaining supports are extendable",
          len(unblocked) == 2 and set(unblocked) == {Ta, Tb})
    print("      extendable remaining complements:",
          [sorted(c) for c in unblocked])

    # ---- 4. the prefix does extend to eight, and never to nine ------------
    sA = frozenset(VERTS) - Ta
    sB = frozenset(VERTS) - Tb
    eight = None
    for ma in perfect_matchings(sA, H):
        H2 = H - set(ma)
        for mb in perfect_matchings(sB, H2):
            eight = (ma, mb)
            break
        if eight:
            break
    check("the prefix extends to eight", eight is not None)
    check("the prefix never extends to nine (only two candidates exist)",
          len(unblocked) == 2)

    # ---- 5. a nine-packing for the whole instance --------------------------
    # depth-first search over subsets of the 17 supports, stopped at nine.
    order = sorted(range(17), key=lambda i: len(SUPPORTS[i]))
    found9 = [None]

    def rec(i, used, chosen):
        if len(chosen) == 9:
            found9[0] = list(chosen)
            return True
        if len(chosen) + (17 - i) < 9:
            return False
        idx = order[i]
        s = SUPPORTS[idx]
        for m in perfect_matchings(s, ALL - used):
            if rec(i + 1, used | set(m), chosen + [(idx, m)]):
                return True
        return rec(i + 1, used, chosen)

    rec(0, frozenset(), [])
    check("the instance itself admits nine pairwise edge-disjoint "
          "support matchings (different prefix)", found9[0] is not None)
    if found9[0] is not None:
        print("      nine-packing uses complements:",
              [sorted(COMPLEMENTS[i]) for i, _ in found9[0]])

    print()
    print("ALL CHECKS PASS" if ok else "SOME CHECK FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Verifier for Theorems A, B, C of NOTE.md.

NOT EXECUTED in the session that wrote it (no interpreter was available).
The theorems are proved by hand in NOTE.md; this script is independent audit
surface only.

Part 1 (combinatorial skeleton) needs nothing external.
Part 2 uses the repository's committed cyclic LS(2,3,19) from
`evidence/verify_defect_cross_link_lsts19.py` purely as an executable
*control* for Theorem B and Theorem C.  If that import fails, Part 2 prints
SKIP and Part 1 still runs in full.

Standard library only.  Deterministic.
"""

import importlib.util
import itertools
import os
import sys

FAILURES = []


def check(name, cond):
    print(("PASS  " if cond else "FAIL  ") + name)
    if not cond:
        FAILURES.append(name)


# ------------------------------------------------------------------ Part 1
def part1():
    print("--- Part 1: the coordinate map of Theorem A (no external data) ---")
    W = list(range(19))
    R = W[:6]
    A = W[6:]
    Rs, As = set(R), set(A)

    T = [Z for Z in itertools.combinations(W, 3) if Rs & set(Z)]
    check("|T| = C(19,3) - C(13,3) = 683", len(T) == 683)

    seen = {}
    ok = True
    for Z in T:
        B = frozenset(Z) & As
        Q = frozenset(Rs - set(Z))
        if len(Q) != len(B) + 3:
            ok = False
        if (B, Q) in seen:
            ok = False
        seen[(B, Q)] = Z
    check("Z -> (Z n A, R \\ (Z n R)) is injective with |Q| = |B| + 3", ok)

    targets = set()
    for j in range(3):
        for B in itertools.combinations(A, j):
            for Q in itertools.combinations(R, j + 3):
                targets.add((frozenset(B), frozenset(Q)))
    check("the map is onto all pairs (B,Q), |B| <= 2, |Q| = |B|+3",
          set(seen) == targets)

    # every pair of W lies in exactly 17 triples; those inside A have all 17
    # in T only when the pair meets R
    ok = True
    for Y in itertools.combinations(W, 2):
        star = [Z for Z in itertools.combinations(W, 3) if set(Y) <= set(Z)]
        if len(star) != 17:
            ok = False
        inT = [Z for Z in star if Rs & set(Z)]
        want = 17 if (Rs & set(Y)) else 6
        if len(inT) != want:
            ok = False
    check("every pair-star has 17 triples; it lies in T iff the pair meets R,"
          " else exactly 6 of it does", ok)

    # the general level-j shape: |W| = j + 17
    ok = all((j + 4) + 13 == j + 17 for j in range(14))
    check("general level: |R| + |A| = (j+4) + 13 = j + 17", ok)


# ------------------------------------------------------------------ Part 2
def load_ls():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, "..", "..", ".."))
    path = os.path.join(root, "evidence", "verify_defect_cross_link_lsts19.py")
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location("lsts19_control", path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
        return mod.construct_lsts19()
    except Exception:
        return None


def part2():
    print()
    print("--- Part 2: Theorems B and C on the committed LS(2,3,19) control ---")
    col = load_ls()
    if col is None:
        print("SKIP  committed LS(2,3,19) control unavailable")
        return
    pts = sorted({p for Z in col for p in Z})
    check("control has 19 points and 969 coloured triples",
          len(pts) == 19 and len(col) == 969)
    C = sorted(set(col.values()))
    check("control uses exactly 17 colours", len(C) == 17)

    def c(*Z):
        return col[tuple(sorted(Z))]

    ok = True
    for Y in itertools.combinations(pts, 2):
        vals = [c(*(Y + (w,))) for w in pts if w not in Y]
        if len(set(vals)) != 17:
            ok = False
    check("control is a proper 17-colouring of J(19,3)", ok)

    # choose several splits W = R u A and check Theorems B and C on each
    splits = [tuple(pts[:6]), tuple(pts[1:7]), tuple(pts[13:19]),
              (pts[0], pts[2], pts[4], pts[6], pts[8], pts[10])]
    for R in splits:
        A = [p for p in pts if p not in R]
        tag = "R=%s" % (R,)

        # --- Theorem B.1: e_a is a proper 17-edge-colouring of K_R
        e = {a: {frozenset((u, v)): c(u, v, a)
                 for u, v in itertools.combinations(R, 2)} for a in A}
        ok = True
        for a in A:
            for u in R:
                at_u = [e[a][frozenset((u, v))] for v in R if v != u]
                if len(set(at_u)) != 5:
                    ok = False
        check("B.1 every e_a is a proper edge-colouring of K_6  " + tag, ok)

        # --- Theorem B.3: a -> e_a(Y) is a bijection onto C \ Lambda(Y)
        ok = True
        for u, v in itertools.combinations(R, 2):
            Y = frozenset((u, v))
            lam = {c(*sorted(set(Y) | {w})) for w in R if w not in Y}
            vals = [e[a][Y] for a in A]
            if len(lam) != 4 or len(set(vals)) != 13 or set(vals) | lam != set(C):
                ok = False
        check("B.3 a -> e_a(Y) bijects onto the complement of the 4 link "
              "colours  " + tag, ok)

        # --- Theorem B.2 and Corollary B1
        app = {(a, x): {e[a][frozenset((x, v))] for v in R if v != x}
               for a in A for x in R}
        supp = {(g, x): [a for a in A if g not in app[(a, x)]]
                for g in C for x in R}
        tau = {(g, x): sum(1 for Z in itertools.combinations(R, 3)
                           if x in Z and c(*Z) == g)
               for g in C for x in R}
        check("B1 |V_g(P_x)| = 8 + 2 tau  " + tag,
              all(len(supp[(g, x)]) == 8 + 2 * tau[(g, x)]
                  for g in C for x in R))
        check("B1 every support size is 8, 10 or 12  " + tag,
              all(len(supp[(g, x)]) in (8, 10, 12) for g in C for x in R))

        t = {g: sum(1 for Z in itertools.combinations(R, 3) if c(*Z) == g)
             for g in C}
        check("B1 sum_a u_{a,g} = 15 - 3 t_g  " + tag,
              all(sum(sum(1 for Y in e[a] if e[a][Y] == g) for a in A)
                  == 15 - 3 * t[g] for g in C))
        check("B1 t_g <= 4 and tau <= 2  " + tag,
              all(t[g] <= 4 for g in C)
              and all(tau[(g, x)] <= 2 for g in C for x in R))

        # --- Theorem C: the six same-colour matchings
        M = {(g, x): [frozenset((a, b))
                      for a, b in itertools.combinations(A, 2)
                      if c(x, a, b) == g]
             for g in C for x in R}
        ok = True
        for g in C:
            for x in R:
                cov = [p for Y in M[(g, x)] for p in Y]
                if sorted(cov) != sorted(supp[(g, x)]):
                    ok = False
        check("C  M_g(P_x) is a perfect matching on V_g(P_x)  " + tag, ok)
        check("C  the six matchings of each colour are pairwise disjoint  "
              + tag,
              all(not (set(M[(g, x)]) & set(M[(g, y)]))
                  for g in C for x, y in itertools.combinations(R, 2)))
        check("C  sum_x |M_g(P_x)| = 24 + 3 t_g  " + tag,
              all(sum(len(M[(g, x)]) for x in R) == 24 + 3 * t[g] for g in C))
        check("C  grand total is 6 * 78 = 468  " + tag,
              sum(len(M[(g, x)]) for g in C for x in R) == 468)

        # --- Corollary C2: the single-edge list is always big enough
        ok = True
        for a, b in itertools.combinations(A, 2):
            for x in R:
                lst = (set(C) - app[(a, x)]) & (set(C) - app[(b, x)])
                if len(lst) < 7:
                    ok = False
        check("C2 |mu_a(x) n mu_b(x)| >= 7 > 6  " + tag, ok)


def main():
    part1()
    part2()
    print()
    if FAILURES:
        print("FAILURES: %d" % len(FAILURES))
        return 1
    print("ALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

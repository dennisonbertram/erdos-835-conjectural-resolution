#!/usr/bin/env python3
"""Legacy verifier for `cyclic17_star_threshold_and_colour_transitive_scope.md`.

SUPERSEDED: its Theorem D narration omits the complementation factor in
Aut(J(32,16)), and the companion note's structural Hall explanation is
incomplete. Use `verify_cyclic17_star_hall_theorem.py` for the repaired
Theorem D and the chart-independent Hall theorem. This legacy script is kept
only to reproduce the two-chart exhaustive control and the heuristic table.

Three parts, with sharply different logical status:

  (A) PROOF   -- Theorem D: every colour-transitive tight 17-colouring of
                 J(32,16) satisfies the cyclic-17 ansatz.  Arithmetic checked.
  (B) COMPUTATION -- two-chart exhaustive Hall control only; the PROOF is in
                 verify_cyclic17_star_hall_theorem.py (Theorem E).
  (C) HEURISTIC -- a first-moment "break-even family size" model that places
                 the minimum star obstruction at exactly 6 rows.  This is a
                 MODEL, not a proof, and the file says so where it prints.

Stdlib only; no solver; no family enumeration.

Run:  python3 -B evidence/verify_cyclic17_star_threshold.py
"""
from __future__ import annotations

import math
import os
import random
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from verify_cyclic17_z2_equivariant_reduction import (  # noqa: E402
    P, triple_orbits, layer2_data, load_design, check_golf_design)

# Exhaustively enumerated centre-0 Wallis family sizes for rows (0,2)..(0,14),
# as reported by the independent DFS run this note audits.
REPORTED = {2: 449, 3: 462, 4: 499, 5: 475, 6: 526, 7: 488, 8: 456,
            9: 479, 10: 477, 11: 523, 12: 476, 13: 488, 14: 516}

FIRST_HALF_COLUMNS = (
    tuple(range(2, 17)),
    (5, 1, 7, 8, 9, 16, 14, 4, 13, 15, 10, 6, 11, 3, 12),
    (9, 10, 12, 2, 15, 13, 16, 14, 4, 7, 5, 8, 1, 11, 6),
    (14, 12, 2, 13, 3, 8, 9, 16, 7, 5, 1, 15, 6, 10, 11),
    (16, 11, 13, 15, 1, 3, 6, 10, 2, 14, 4, 7, 8, 12, 9),
    (13, 15, 16, 1, 14, 11, 4, 7, 12, 8, 9, 3, 10, 5, 2),
    (15, 4, 1, 14, 11, 2, 10, 3, 5, 6, 13, 16, 12, 9, 8),
    (12, 13, 14, 11, 10, 9, 2, 6, 16, 3, 15, 1, 7, 4, 5),
)


def wallis_golf_17():
    out = []
    for sq in range(15):
        a = [0] + [FIRST_HALF_COLUMNS[j - 1][sq] for j in range(1, 9)]
        a.extend([-1] * 8)
        for j in range(9, 17):
            a[j] = (a[17 - j] + j) % 17
        assert sorted(a) == list(range(17))
        edges = set()
        for d in range(1, 17):
            y = (-a[d]) % 17
            x = (y + d) % 17
            if x != y:
                edges.add(frozenset((x, y)))
        out.append(frozenset(edges))
    return tuple(out)


# ------------------------------------------------------------------ (A)

def section_a():
    print("=" * 74)
    print("(A) SUPERSEDED -- Theorem D narration below is INCOMPLETE")
    print("=" * 74)
    print("    It treats G as a subgroup of Sym(32) and omits the")
    print("    complementation factor: Aut(J(32,16)) = Sym(32) x C_2.  It also")
    print("    asserts the Sylow-image step without justification.  The")
    print("    repaired proof (trivial C_2 component via eps = eps^17, plus the")
    print("    index computation [G/K:phi(S)] = [G:S]/[K:S cap K]) is in")
    print("    verify_cyclic17_star_hall_theorem.py.  The CONCLUSION is")
    print("    unchanged; only the argument below is deficient.")
    print("=" * 74)
    # 17-part of 32!: only one multiple of 17 is <= 32, so 17^1 || 32!.
    mult = [n for n in range(1, 33) if n % 17 == 0]
    assert mult == [17]
    e17 = sum(32 // 17 ** t for t in range(1, 3))
    assert e17 == 1, e17
    print(f"    multiples of 17 up to 32: {mult}; so 17^{e17} exactly divides 32!")
    print("    => every Sylow 17-subgroup of Sym(32) has order 17, and every")
    print("       element of order 17 has cycle type 17 + 1^15 on the points,")
    assert 17 * 1 + 15 == 32 and 17 * 2 > 32
    print(f"       because 17*2 = {17*2} > 32 forces exactly one 17-cycle.")
    # an order-17 element of Sym(17) is a 17-cycle, hence transitive on colours
    print("    An order-17 element of Sym(17 colours) is a 17-cycle, so it is")
    print("    transitive on the colours.")
    print()
    print("    Theorem D.  Let a tight 17-colouring of J(32,16) admit an")
    print("    automorphism group G transitive on the 17 colour classes.  Let")
    print("    K be the kernel of G -> Sym(colours).  Then 17 | |G/K|, so a")
    print("    Sylow 17-subgroup S of G has nontrivial image; pick sigma in S")
    print("    with nontrivial image.  |S| divides the 17-part of |Sym(32)|,")
    print("    which is 17, so sigma has order 17; its image is an order-17")
    print("    element of Sym(17), i.e. a 17-cycle on colours.  On the 32")
    print("    points sigma has exactly one 17-cycle A and 15 fixed points F.")
    print("    Relabelling colours by Z_17 so that sigma sends q to q+1 gives")
    print("    precisely the cyclic ansatz of cyclic17_equivariant_reduction.md.")
    print("    []")
    print()
    print("    CONSEQUENCE (scope).  A no-go for the cyclic-17 ansatz over ALL")
    print("    golf designs of Z_17 would refute every COLOUR-TRANSITIVE tight")
    print("    17-colouring of J(32,16).  It would NOT refute tight colourings")
    print("    with no colour-transitive automorphism group, so it would still")
    print("    not settle Erdos-Rosenfeld #835.")
    print("    A no-go for ONE golf chart (e.g. Wallis) proves strictly less:")
    print("    it excludes only that chart.")


# ------------------------------------------------------------------ (B)

def star_domains(design, centre, reps, F):
    D = {}
    for j in range(15):
        if j == centre:
            continue
        for q in range(40):
            D[(j, q)] = frozenset(c for c in range(P)
                                  if c not in F[centre][q] and c not in F[j][q])
    return D


def section_b(charts, reps):
    print()
    print("=" * 74)
    print("(B) COMPUTATION -- two-chart Hall control (proof is Theorem E elsewhere)")
    print("=" * 74)
    for label, design in charts:
        F = layer2_data(design, reps)
        mn = 99
        fails = 0
        pairs = 0
        for centre in range(15):
            D = star_domains(design, centre, reps, F)
            rows = [j for j in range(15) if j != centre]
            mn = min(mn, min(len(D[(j, q)]) for j in rows for q in range(40)))
            for q in range(40):
                pairs += 1
                # exhaustive over ALL subsets of the 14 rows
                for r in range(1, len(rows) + 1):
                    bad = any(len(set().union(*[D[(j, q)] for j in T])) < r
                              for T in combinations(rows, r))
                    if bad:
                        fails += 1
                        break
        print(f"    {label:16s} min domain {mn}; Hall failures over "
              f"{pairs} (centre, orbit) pairs: {fails}")
        assert fails == 0
    print("    WITHDRAWN reason (do not cite): an earlier revision claimed a")
    print("    violation 'would need >= 12 rows whose domains all lie in one")
    print("    common 11-set'.  That covers only |T| = 12; at |T| = 13 and 14 a")
    print("    violation needs union <= 12 and <= 13 respectively, which is a")
    print("    weaker condition than a common 11-set.  The check above is")
    print("    therefore only a two-chart COMPUTATION, not a proof.")
    print("    The chart-independent proof (Theorem E, via |B_c(q)| <= 3) is in")
    print("    verify_cyclic17_star_hall_theorem.py.  Its conclusion stands:")
    print("    the star infeasibility is not a single-orbit phenomenon.")


# ------------------------------------------------------------------ (C)

def p_distinct(D, S, q):
    """Exact weighted permanent: P(independent uniform draws all distinct)."""
    idx = {j: t for t, j in enumerate(S)}
    full = (1 << len(S)) - 1
    dp = {0: 1.0}
    for v in range(P):
        nd = dict(dp)
        for mask, w in dp.items():
            for j in S:
                b = 1 << idx[j]
                if not (mask & b) and v in D[(j, q)]:
                    nd[mask | b] = nd.get(mask | b, 0.0) + w / len(D[(j, q)])
        dp = nd
    return dp.get(full, 0.0)


def log10_pq(D, S):
    tot = 0.0
    for q in range(40):
        p = p_distinct(D, S, q)
        if p == 0.0:
            return float("-inf")
        tot += math.log10(p)
    return tot


def section_c(charts, reps):
    print()
    print("=" * 74)
    print("(C) HEURISTIC MODEL -- break-even family size.  NOT A PROOF.")
    print("=" * 74)
    mean_obs = sum(REPORTED.values()) / len(REPORTED)
    print(f"    Reported exhaustive centre-0 Wallis families: "
          f"{min(REPORTED.values())}..{max(REPORTED.values())}, mean "
          f"{mean_obs:.0f}")
    print("    Model: each row draws, independently at each of the 40 orbits,")
    print("    a uniform phase from that cell's domain.  Then")
    print("        E(S) = prod_j |F_j| * prod_q P_q(S),")
    print("    and the break-even size F*(m) solves E = 1 with all |F_j| = F*:")
    print("        log10 F*(m) = -(1/m) * sum_q log10 P_q(S).")
    random.seed(835)
    for label, design in charts:
        F = layer2_data(design, reps)
        D = star_domains(design, 0, reps, F)
        rows = [j for j in range(2, 15)]
        print(f"\n    {label}, centre 0:")
        print(f"      {'m':>2} {'sum_q log10 P_q':>17} {'break-even F*':>14}"
              f" {'vs actual ~486':>16}")
        for m in range(2, 8):
            subs = list(combinations(rows, m))
            if len(subs) > 30:
                subs = random.sample(subs, 30)
            mean = sum(log10_pq(D, S) for S in subs) / len(subs)
            fstar = 10 ** (-mean / m)
            verdict = "tuples expected" if fstar < mean_obs else "NOT expected"
            print(f"      {m:>2} {mean:>17.2f} {fstar:>14.0f} {verdict:>16}")
    F = layer2_data(charts[0][1], reps)
    D = star_domains(charts[0][1], 0, reps, F)
    core = tuple(range(2, 8))
    logE = sum(math.log10(REPORTED[j]) for j in core) + log10_pq(D, core)
    print(f"\n    Reported core (0,2)..(0,7) with its true sizes: "
          f"log10 E = {logE:+.2f}")
    print()
    print("    READING.  F* crosses the actual family size (~486) between")
    print("    m = 5 and m = 6.  That is why the minimum star obstruction is")
    print("    six rows.  The two charts agree to three significant figures,")
    print("    so the (-1)-symmetric chart is NOT expected to escape.")
    print()
    print("    LIMITS.  E < 1 does not prove non-existence: the families are")
    print("    fixed, not random.  The model is systematically optimistic for")
    print("    UNSAT -- it gives E ~ 10^-0.4 at m = 5 although every 5-subset")
    print("    is reported SAT, and predicts about 1716 * 10^-5.3 = 0.008 SAT")
    print("    6-subsets although 4 are reported.  It locates the transition,")
    print("    it does not count.")


def main():
    print("SUPERSEDED CONTROL: use verify_cyclic17_star_hall_theorem.py for")
    print("the repaired scope theorem and chart-independent Hall proof.")
    print()
    reps = triple_orbits()
    wallis = wallis_golf_17()
    sym, _ = load_design()
    for d in (wallis, sym):
        check_golf_design(d)
    charts = (("Wallis", wallis), ("(-1)-symmetric", sym))
    section_a()
    section_b(charts, reps)
    section_c(charts, reps)
    print()
    print("Erdos-Rosenfeld #835 remains OPEN; nothing here bears on it except")
    print("through the explicitly stated scope of Theorem D.")


if __name__ == "__main__":
    main()

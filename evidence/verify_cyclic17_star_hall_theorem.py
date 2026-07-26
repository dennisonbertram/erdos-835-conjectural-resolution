#!/usr/bin/env python3
"""Repaired audit of two claims from
`cyclic17_star_threshold_and_colour_transitive_scope.md`.

(A) Theorem D, repaired for Aut(J(2k,k)) = Sym(32) x C_2.
(B) Theorem E: Hall's condition holds at every orbit of every star, for
    EVERY golf design of Z_17 -- strengthened from an exhaustive check on two
    charts to a chart-independent proof.  The previous note gave a bad reason
    ("all domains inside a common 11-set"), which only covers |T| = 12.

Stdlib only, no solver.
Run:  python3 -B evidence/verify_cyclic17_star_hall_theorem.py
"""
from __future__ import annotations

import os
import random
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from verify_cyclic17_z2_equivariant_reduction import (  # noqa: E402
    P, triple_orbits, layer2_data, load_design, check_golf_design, diff_class)
from verify_cyclic17_star_threshold import wallis_golf_17  # noqa: E402


# --------------------------------------------------------------- Theorem D

def section_d():
    print("=" * 74)
    print("(A) Theorem D, REPAIRED for Aut(J(32,16)) = Sym(32) x C_2")
    print("=" * 74)
    print("    The previous statement silently assumed G <= Sym(32).  At")
    print("    n = 2k the Johnson graph also admits complementation")
    print("    c: B -> B^c, and c commutes with the Sym(32) action because")
    print("    (pi B)^c = pi(B^c).  So Aut(J(32,16)) = Sym(32) x <c>, |<c>| = 2.")
    print()
    # 17-part of |Sym(32) x C_2|
    mult = [n for n in range(1, 33) if n % 17 == 0]
    assert mult == [17]
    e17_sym = sum(32 // 17 ** t for t in range(1, 3))
    assert e17_sym == 1
    assert 2 % 17 != 0
    print(f"    17-part of |Sym(32)|: multiples of 17 up to 32 are {mult}, so")
    print(f"    17^{e17_sym} exactly divides 32!.  17 does not divide |C_2| = 2.")
    print("    Hence the 17-part of |Sym(32) x C_2| is 17, and every Sylow")
    print("    17-subgroup has order 17.")
    print()
    print("    STEP 1 (trivial complement component).  Let sigma = (pi, eps)")
    print("    have order 17.  Then eps = eps^17 = (eps^2)^8 * eps ... more")
    print("    directly: sigma^17 = (pi^17, eps^17) = (1,1), and eps^2 = 1 with")
    print("    17 odd gives eps = eps^17 = 1.  So sigma = (pi, 1) lies in")
    print("    Sym(32) x {1}.  Equivalently: an odd-order subgroup has trivial")
    print("    projection to C_2.  Verified as arithmetic:")
    for e in (0, 1):                      # C_2 written additively
        assert (17 * e) % 2 == e % 2
        assert (e if 17 % 2 else 0) == e
    assert pow(1, 17, 2) == 1
    print("      for eps in C_2, eps^17 = eps, and sigma^17 = 1 forces eps = 1: ok")
    print()
    print("    STEP 2 (Sylow image).  Let K = ker(G -> Sym(colours)) and let")
    print("    phi be that map.  For a Sylow p-subgroup S of G, phi(S) is a")
    print("    Sylow p-subgroup of G/K.  Reason: |phi(S)| = |S|/|S cap K| is a")
    print("    p-power, and")
    print("      [G/K : phi(S)] = [G:S] / [K : S cap K],")
    print("    where [G:S] is prime to p because S is Sylow, and S cap K is a")
    print("    Sylow p-subgroup of K so [K : S cap K] is prime to p.  Hence")
    print("    the index is prime to p and phi(S) is Sylow.")
    print()
    print("    STEP 3.  G colour-transitive => G/K <= Sym(17) is transitive =>")
    print("    17 | |G/K| => Sylow 17-subgroups of G/K are nontrivial =>")
    print("    phi(S) != 1.  Since |S| = 17 is prime, phi is injective on S, so")
    print("    EVERY non-identity sigma in S has nontrivial image.  Its image")
    print("    has order 17 in Sym(17), hence is a 17-cycle: colour-transitive.")
    print()
    print("    STEP 4.  By step 1, sigma = (pi,1) with |pi| = 17, so pi has")
    print("    cycles of length 1 or 17 on the 32 points; 2*17 = 34 > 32 forces")
    assert 17 * 2 > 32 and 17 + 15 == 32
    print("    exactly one 17-cycle A and |F| = 15 fixed points.  Relabelling")
    print("    colours by Z_17 so sigma sends q to q+1 gives the cyclic ansatz.")
    print("    []")
    print()
    print("    SCOPE unchanged: a no-go over ALL golf designs of Z_17 would")
    print("    refute every COLOUR-TRANSITIVE tight 17-colouring of J(32,16);")
    print("    it would not refute colourings with no colour-transitive")
    print("    automorphism group, so it would not settle #835.")


# --------------------------------------------------------------- Theorem E

def hole_sizes(design, reps):
    """|B_c(q)| for every orbit and colour, where B_c(q) = {i : c in F_i(q)}."""
    F = layer2_data(design, reps)
    out = []
    for q in range(40):
        for c in range(P):
            out.append(sum(1 for i in range(15) if c in F[i][q]))
    return out


def random_golf_designs(n, reps, seed=835):
    """Random golf designs of Z_17 by randomised greedy over starters."""
    rng = random.Random(seed)
    edges = [frozenset(e) for e in combinations(range(1, P), 2)]

    def starters_through(avail):
        """One random starter inside `avail` (set of edges), or None."""
        order = list(range(1, P))

        def rec(free, used, acc):
            if not free:
                return list(acc)
            v = min(free)
            cand = [w for w in free - {v}
                    if frozenset((v, w)) in avail
                    and diff_class(frozenset((v, w))) not in used]
            rng.shuffle(cand)
            for w in cand:
                r = rec(free - {v, w}, used | {diff_class(frozenset((v, w)))},
                        acc + [frozenset((v, w))])
                if r:
                    return r
            return None

        del order
        return rec(frozenset(range(1, P)), frozenset(), [])

    found = []
    for _ in range(4000):
        if len(found) >= n:
            break
        avail = set(edges)
        design = []
        for _ in range(15):
            st = starters_through(avail)
            if st is None:
                break
            design.append(frozenset(st))
            avail -= set(st)
        if len(design) == 15 and not avail:
            d = tuple(design)
            if frozenset(d) not in {frozenset(x) for x in found}:
                found.append(d)
    return found


def section_e(reps):
    print()
    print("=" * 74)
    print("(B) Theorem E: Hall holds at every orbit, for EVERY golf design")
    print("=" * 74)
    print("    WITHDRAWN reason from the previous note: 'a violation needs >=12")
    print("    rows whose domains all lie inside one common 11-set'.  That is")
    print("    only valid at |T| = 12.  At |T| = 13 a violation needs the union")
    print("    to have size <= 12, and at |T| = 14 size <= 13; neither is a")
    print("    common 11-set.  The claim as written did not cover r = 13, 14.")
    print()
    print("    Theorem E.  Fix a golf design of Z_17, a centre i, an orbit q,")
    print("    and a set T of star rows.  Then")
    print("        | union_{j in T} D_ij(q) |  >=  |T|.")
    print("    Proof.  D_ij(q) = (Z_17 \\ F_i(q)) \\ F_j(q), so")
    print("        union_{j in T} D_ij(q) = (Z_17 \\ F_i(q)) \\ intersect_{j in T} F_j(q),")
    print("    and c lies in intersect_{j in T} F_j(q) iff T is contained in")
    print("    B_c(q) = {j : c in F_j(q)}.  Every |B_c(q)| is 1 or 3, because")
    print("    the three edges of the translate T_q + c that avoid 0 lie in")
    print("    three DISTINCT starters (a starter is a matching, so it cannot")
    print("    own two edges of a triangle), and exactly one edge avoids 0 when")
    print("    0 is in T_q + c.  Hence:")
    print("      * |T| >= 4 : the intersection is empty, so the union is all of")
    print("        Z_17 \\ F_i(q), of size 14 >= |T| since a star has 14 rows;")
    print("      * |T| <= 3 : the union contains a single domain, of size")
    print("        17 - |F_i(q) union F_j(q)| >= 17 - 6 = 11 >= 3 >= |T|.")
    print("    []")
    print()
    print("    Note the proof uses ONLY |B_c(q)| <= 3 and |F_i(q)| = 3, both")
    print("    forced by the golf-design axioms.  It is chart-independent.")
    print()
    charts = [("Wallis", wallis_golf_17()), ("(-1)-symmetric", load_design()[0])]
    extra = random_golf_designs(3, reps)
    charts += [(f"random golf design #{t}", d) for t, d in enumerate(extra)]
    print(f"    additional golf designs found by randomised greedy: {len(extra)}")
    print("    (the theorem above is chart-independent, so the computational")
    print("     check below is a control, not the evidence for the claim)")
    for label, design in charts:
        check_golf_design(design)
        hs = hole_sizes(design, reps)
        assert set(hs) <= {1, 3}, sorted(set(hs))
        assert hs.count(1) == 120 and hs.count(3) == 560, (hs.count(1), hs.count(3))
        F = layer2_data(design, reps)
        assert all(len(F[i][q]) == 3 for i in range(15) for q in range(40))
        # exhaustive Hall check over ALL subsets of the 14 rows, all centres
        worst = 99
        for centre in range(15):
            rows = [j for j in range(15) if j != centre]
            for q in range(40):
                D = {j: frozenset(c for c in range(P)
                                  if c not in F[centre][q] and c not in F[j][q])
                     for j in rows}
                for r in range(1, 15):
                    for T in combinations(rows, r):
                        u = len(set().union(*[D[j] for j in T]))
                        worst = min(worst, u - r)
                        assert u >= r, (label, centre, q, T)
        print(f"    {label:24s} |B_c(q)| in {{1,3}} (120 / 560): ok; "
              f"Hall slack min = {worst}")
    print()
    print("    => the star infeasibility is NOT a single-orbit phenomenon, for")
    print("       ANY golf design of Z_17.  No Hall/SDR argument at one orbit")
    print("       can prove it; any proof must couple the 40 orbits.")


def main():
    reps = triple_orbits()
    section_d()
    section_e(reps)
    print()
    print("All checks passed.  Erdos-Rosenfeld #835 remains OPEN.")


if __name__ == "__main__":
    main()

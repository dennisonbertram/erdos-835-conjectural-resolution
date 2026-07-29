#!/usr/bin/env python3
"""Structure, controls and audits for the LS(3,4,20) / S(4,5,21) targets.

Stdlib only.  No solver.  Reads two committed data files READ-ONLY and writes
nothing outside this directory.

  A  CONTROL   k=4: the LS(3,4,.) shadow correctly excludes k=4.
  B  THEOREM   every pair of points induces a one-factorization of K_18,
               and intersecting pairs induce discordant ones.  Checked
               against the verified EH 4,773-block partial.
  C  BRANCHING lossless symmetry-safe cube decomposition for the canonical
               LS(3,4,20) CNF, and the exhaustiveness count for the seven
               S(4,5,21) branches.
  D  AUDIT     the canonical LS(3,4,20) CNF: dimensions recomputed, and a
               sound implied strengthening that is currently absent.

Run:  python3 -B collaboration/opus5/radius5_followup/verify_ls3420_structure_and_branching.py
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EH = os.path.join(REPO, "evidence", "ls_3_4_20_eh15_partial.txt")
MANIFEST = os.path.join(REPO, "evidence", "ls_3_4_20_generic_cnf", "manifest.json")


# ---------------------------------------------------------------- A. control

def all_sqs(v):
    """Every S(3,4,v) on [v], by exhaustive backtracking on the least
    uncovered triple.  For v = 8 this returns the 30 labelled SQS(8)."""
    triples = [frozenset(t) for t in combinations(range(v), 3)]
    out, blocks = [], []
    covered = set()

    def rec():
        rem = [t for t in triples if t not in covered]
        if not rem:
            out.append(tuple(sorted(tuple(sorted(b)) for b in blocks)))
            return
        T = min(rem, key=lambda s: sorted(s))
        for x in range(v):
            if x in T:
                continue
            B = frozenset(T | {x})
            sub = [frozenset(c) for c in combinations(B, 3)]
            if any(s in covered for s in sub):
                continue
            for s in sub:
                covered.add(s)
            blocks.append(B)
            rec()
            blocks.pop()
            for s in sub:
                covered.discard(s)

    rec()
    return out


def max_disjoint(systems):
    n = len(systems)
    sets = [set(s) for s in systems]
    ok = [[not (sets[a] & sets[b]) for b in range(n)] for a in range(n)]
    best = 0

    def expand(cur, cand):
        nonlocal best
        if len(cur) + len(cand) <= best:
            return
        best = max(best, len(cur))
        for v in sorted(cand):
            expand(cur + [v], {w for w in cand if w > v and ok[v][w]})
            cand = cand - {v}
            if len(cur) + len(cand) <= best:
                return

    expand([], set(range(n)))
    return best


def section_a():
    print("=" * 74)
    print("A.  CONTROL -- the LS(3,4,.) shadow at k = 4")
    print("=" * 74)
    print("    A tight (k+1)-colouring at k forces LS(3,4,k+4).  At k = 16 that")
    print("    is LS(3,4,20).  At k = 4 it is LS(3,4,8): a partition of the")
    print("    C(8,4) = 70 quadruples into 5 disjoint SQS(8) of 14 blocks each.")
    sqs8 = all_sqs(8)
    assert len(sqs8) == 30, len(sqs8)
    for S in sqs8:
        assert len(S) == 14
        seen = set()
        for B in S:
            for t in combinations(B, 3):
                assert t not in seen
                seen.add(t)
        assert len(seen) == 56
    m = max_disjoint(sqs8)
    need = 70 // 14
    print(f"    labelled SQS(8): {len(sqs8)};  max pairwise block-disjoint: {m};"
          f"  need {need}")
    assert m == 2 and need == 5
    print("    => LS(3,4,8) is IMPOSSIBLE, so the shadow correctly excludes k=4.")
    print()
    print("    k=2 control: the same shadow needs SQS(6), which does not exist")
    print("    (v = 6 is not 2 or 4 mod 6), so the LS(3,4,.) test has no content")
    print("    at k = 2.  It cannot produce a false positive there, but it is")
    print("    also not evidence that the test is calibrated.")


# ---------------------------------------------------------------- B. theorem

def load_eh():
    colour = {}
    with open(EH) as fh:
        for line in fh:
            p = line.split()
            if len(p) != 5:
                continue
            B = tuple(sorted(int(x) for x in p[:4]))
            colour[B] = int(p[4])
    assert len(colour) == 4845, len(colour)
    return colour


def section_b():
    print()
    print("=" * 74)
    print("B.  THEOREM -- every pair induces a one-factorization of K_18")
    print("=" * 74)
    print("    Let c be an LS(3,4,20) colouring.  Fix a pair {a,b} and let")
    print("    W = [20] \\ {a,b}, |W| = 18.  Define phi_{ab}({q,y}) =")
    print("    c({a,b,q,y}).  Then phi_{ab} is a proper edge colouring of K_W")
    print("    with all 17 colours at every vertex, i.e. a ONE-FACTORIZATION")
    print("    of K_18.")
    print("    Proof.  Fix q in W.  For y, y' in W \\ {q} distinct, the blocks")
    print("    {a,b,q,y} and {a,b,q,y'} both contain the triple {a,b,q}; a")
    print("    colour class is an S(3,4,20), so it contains exactly one")
    print("    extension of that triple, hence the two colours differ.  So")
    print("    y -> phi_{ab}({q,y}) is injective on the 17 points of W\\{q}")
    print("    into 17 colours, hence bijective. []")
    print()
    print("    COROLLARY (discordance).  If {a,b} and {a,d} share a point then")
    print("    for all q,y outside {a,b,d}, phi_{ab}({q,y}) != phi_{ad}({q,y}):")
    print("    the blocks {a,b,q,y} and {a,d,q,y} are distinct and share the")
    print("    triple {a,q,y}. []")
    print()
    print("    NORMALIZED FORM.  Identify the 17 colours with Q = [20]\\{0,1,2}")
    print("    by c({0,1,2,q}) = q (this is exactly the CNF's symmetry unit).")
    print("    Then S_ab(q,y) = c({a,b,q,y}) for {a,b} in {01,02,12}, extended")
    print("    by S_ab(q,q) = q, are three SYMMETRIC IDEMPOTENT LATIN SQUARES")
    print("    of order 17 on Q, pairwise discordant off the diagonal.")
    print("    (S_ab(q,y) != q because {a,b,q,y} and {0,1,2,q} share {a,b,q}")
    print("    when {a,b} u {q} is a triple of the normalizing block.)")

    colour = load_eh()
    full = {c: [B for B, cc in colour.items() if cc == c] for c in range(17)}
    complete = [c for c in range(17) if len(full[c]) == 285]
    partial = [c for c in range(17) if 0 < len(full[c]) < 285]
    uncoloured = sum(1 for v in colour.values() if v < 0)
    print()
    print(f"    Checked against the verified EH partial: {4845 - uncoloured}"
          f" coloured blocks, {uncoloured} uncoloured")
    print(f"      complete colour classes (285 blocks): {len(complete)}")
    print(f"      partial colour classes: {len(partial)} "
          f"(sizes {sorted(len(full[c]) for c in partial)})")
    assert len(complete) == 15 and len(partial) == 2
    assert 4845 - uncoloured == 4773
    # every complete class is a genuine S(3,4,20)
    for c in complete:
        seen = set()
        for B in full[c]:
            for t in combinations(B, 3):
                assert t not in seen
                seen.add(t)
        assert len(seen) == 1140
    print("      each of the 15 complete classes is a genuine S(3,4,20): ok")
    # the theorem, as far as the partial data determines it
    bad_proper = bad_disc = tested = 0
    for a, b in combinations(range(20), 2):
        W = [x for x in range(20) if x not in (a, b)]
        at = {q: {} for q in W}
        for q, y in combinations(W, 2):
            B = tuple(sorted((a, b, q, y)))
            col = colour[B]
            if col < 0:
                continue
            for (p1, p2) in ((q, y), (y, q)):
                if col in at[p1]:
                    bad_proper += 1
                at[p1][col] = p2
            tested += 1
    print(f"      partial one-factorization property over all "
          f"{len(list(combinations(range(20),2)))} pairs: "
          f"{bad_proper} violations in {tested} coloured cells")
    assert bad_proper == 0
    for a in range(20):
        rest = [x for x in range(20) if x != a]
        for b, d in combinations(rest, 2):
            W = [x for x in range(20) if x not in (a, b, d)]
            for q, y in combinations(W, 2):
                c1 = colour[tuple(sorted((a, b, q, y)))]
                c2 = colour[tuple(sorted((a, d, q, y)))]
                if c1 >= 0 and c2 >= 0:
                    if c1 == c2:
                        bad_disc += 1
    print(f"      discordance for intersecting pairs: {bad_disc} violations")
    assert bad_disc == 0


# ---------------------------------------------------------------- C. branching

def partitions_min2(n):
    """Partitions of n with every part >= 2."""
    def rec(rem, lo):
        if rem == 0:
            yield ()
            return
        for p in range(lo, rem + 1):
            if rem - p == 0 or rem - p >= 2:
                for tail in rec(rem - p, p):
                    yield (p,) + tail
    return list(rec(n, 2))


def section_c():
    print()
    print("=" * 74)
    print("C.  BRANCHING -- lossless symmetry-safe decompositions")
    print("=" * 74)
    print("    S(4,5,21), the seven branches (audited, not re-derived here):")
    p8 = partitions_min2(8)
    print(f"      partitions of 8 with all parts >= 2: {len(p8)}  {p8}")
    assert len(p8) == 7
    print("      matches the recorded seven cases exactly.")
    print()
    print("    LS(3,4,20), a NEW lossless branch.  After the CNF's colour")
    print("    normalization the residual symmetry is Sym{0,1,2} x Sym(Q),")
    print("    |Q| = 17, where Sym(Q) permutes points and colours together.")
    print("    Sym(Q) is transitive, so fix one q0 in Q; row q0 of S_01 is a")
    print("    DERANGEMENT g of Q\\{q0} (16 points), since S_01(q0,y) != y.")
    print("    The stabiliser Sym(Q\\{q0}) acts on g by conjugation, so the")
    print("    cycle type of g is a complete lossless branch label.")
    p16 = partitions_min2(16)
    print(f"      partitions of 16 with all parts >= 2: {len(p16)}")
    assert len(p16) == 55
    print("      => a provably lossless 55-way cube decomposition.")
    print("      (Not all 55 need be realisable; 55 is an upper bound on the")
    print("       number of branches, which is what exhaustiveness requires.)")

    # Target the verified 4,773-block Etzion--Hartman partial after applying
    # the same root-star colour normalization as the canonical CNF.
    colour = load_eh()
    old_colour_to_point = {
        colour[(0, 1, 2, point)]: point for point in range(3, 20)
    }
    assert len(old_colour_to_point) == 17
    permutation = {
        point: old_colour_to_point[colour[(0, 1, 3, point)]]
        for point in range(4, 20)
    }
    assert set(permutation) == set(permutation.values()) == set(range(4, 20))
    assert all(permutation[point] != point for point in permutation)
    unseen = set(permutation)
    cycle_lengths = []
    while unseen:
        start = min(unseen)
        point = start
        length = 0
        while point in unseen:
            unseen.remove(point)
            length += 1
            point = permutation[point]
        assert point == start
        cycle_lengths.append(length)
    eh_type = tuple(sorted(cycle_lengths))
    assert eh_type == (16,)
    assert p16.index(eh_type) == 54
    print()
    print("    The verified 4,773-block Etzion--Hartman partial has all 16")
    print("    entries of this row assigned.  After the canonical root-star")
    print("    colour normalization, that row is one 16-cycle: branch 54.")
    print("    This targets a near-completion search; it does not make branch")
    print("    54 WLOG for arbitrary solutions.")


# ---------------------------------------------------------------- D. CNF audit

def section_d():
    print()
    print("=" * 74)
    print("D.  AUDIT of the canonical LS(3,4,20) CNF")
    print("=" * 74)
    man = json.load(open(MANIFEST))
    c = man["counts"]
    blocks, triples, cols = 4845, 1140, 17
    assert len(list(combinations(range(20), 4))) == blocks
    assert len(list(combinations(range(20), 3))) == triples
    assert c["primary_variables"] == blocks * cols == 82365
    assert c["auxiliary_variables"] == blocks * (cols - 1) == 77520
    assert c["block_alo_clauses"] == blocks
    assert c["block_amo_clauses"] == blocks * (3 * cols - 4) == 227715
    assert c["star_alo_clauses"] == triples * cols == 19380
    assert c["symmetry_unit_clauses"] == cols
    tot = (c["block_alo_clauses"] + c["block_amo_clauses"]
           + c["star_alo_clauses"] + c["symmetry_unit_clauses"])
    assert tot == c["clauses"] == 251957
    print("    dimensions recomputed independently from (20,4,3,17): ok")
    print(f"      {c['primary_variables']} primary + {c['auxiliary_variables']}"
          f" Sinz aux = {c['variables']} variables, {c['clauses']} clauses")
    print()
    print("    SYMMETRY BREAKING is lossless.  Each colour class is an")
    print("    S(3,4,20), so it holds exactly one of the 17 extensions of")
    print("    {0,1,2}; those 17 blocks therefore realise all 17 colours")
    print("    bijectively, and the free Sym(17) colour action can always be")
    print("    used to put them in point order.  It uses the colour symmetry")
    print("    fully and the Sym(20) point symmetry not at all.")
    print()
    print("    MISSING IMPLIED CLAUSES.  The encoding has star AT-LEAST-ONE")
    print("    (19,380 clauses) but no star AT-MOST-ONE.  Exactly-one per")
    print("    (triple, colour) IS implied: each of the 17 extensions of a")
    print("    triple carries exactly one colour, and all 17 colours occur, so")
    print("    by pigeonhole each occurs exactly once.  Adding the at-most-one")
    print("    side is therefore SOUND and changes no solution, but it is what")
    print("    a solver needs for direct propagation.")
    extra = triples * cols * (cols * (cols - 1) // 2)
    print(f"      pairwise form: {triples} x {cols} x C({cols},2) = {extra:,}"
          f" binary clauses")
    assert extra == 2635680
    print("      This is a lossless strengthening, not a new constraint.")


def main():
    section_a()
    section_b()
    section_c()
    section_d()
    print()
    print("=" * 74)
    print("SCOPE.  Neither LS(3,4,20) nor S(4,5,21) is resolved here.  UNSAT")
    print("for either would exclude k=16 but would NOT settle #835, since")
    print("other prime cases remain.  SAT for either is a necessary shadow")
    print("only.  Erdos-Rosenfeld #835 remains OPEN.")


if __name__ == "__main__":
    main()

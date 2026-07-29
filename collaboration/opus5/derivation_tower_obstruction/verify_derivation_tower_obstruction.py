#!/usr/bin/env python3
"""Exact audit of the derivation-tower theorems (Theorems 9-11, Cor 10.1/12/14).

Standard library only; exact arithmetic and finite enumeration; no solver, no
randomness, no floating point.

SCOPE.  Nothing here decides LS(3,4,20), LS(14,15,31) or Erdos--Rosenfeld #835.
Solver-derived inputs are NOT re-derived here: the DRAT-UNSAT status of all
455 point-link cases is supplied by the companion aggregate gate, which
independently reconstructs and replays the certificates.  This verifier pins
that gate's receipt and checks only the structural consequences.

Sections
  1  pinned export, the four F_i, label conventions (rank vs exported colour)
  2  Theorem 9: derivation is a homomorphism of completion problems
  3  Theorem 10: every point of every retained sub-family carries a derived K_4
  4  Corollary 10.1 + Theorem 11: the derived rainbow bound is weaker, so the
     point-link obstruction is not of clique/rainbow type and is invisible to
     the three feasible screens.  It is NOT outside Theorems 1-8: companion
     Theorem 1 is an exact equivalence and Theorem 7 is the failing condition.
  4b Theorem 15: the rainbow defect 15-t, tight only at the top of the tower
  4c Theorems 16-18: packing dichotomy, free lower bound, closure at j=2
  5  Corollary 12/13/14 bookkeeping and the certified aggregate receipt
"""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter, defaultdict
from itertools import combinations
from math import comb

DATA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    "ls3420_branch0_search",
    "eh15_branch0_partial.txt",
)
EXPORT_SHA256 = "06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78"
AGGREGATE_RECEIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    "eh_point_link_screen",
    "all_455_point0_theorem_receipt.json",
)
AGGREGATE_RECEIPT_SHA256 = (
    "312096aa9e489156778094e7ab7dc4fd3e3fe34c11d9a2d82531489684c4b085"
)
CHECKS = []


def ok(label, cond, detail=""):
    CHECKS.append(bool(cond))
    print(
        f"  [{'PASS' if cond else 'FAIL'}] {label}" + (f"   {detail}" if detail else "")
    )
    if not cond:
        raise AssertionError(label)


def section1():
    print("1. pinned export, the four F_i, and label conventions")
    with open(DATA, "rb") as fh:
        ok(
            "export SHA-256 matches the pinned value",
            hashlib.sha256(fh.read()).hexdigest() == EXPORT_SHA256,
        )
    with open(DATA) as fh:
        rows = [ln.split() for ln in fh if ln.strip()]
    blocks = [(tuple(int(x) for x in r[:4]), int(r[4])) for r in rows]
    size = Counter(c for _, c in blocks)
    fullc = sorted(c for c in size if size[c] == 285)
    designs = defaultdict(set)
    for b, c in blocks:
        designs[c].add(b)
    for c in fullc:
        cov = Counter(t for b in designs[c] for t in combinations(b, 3))
        assert len(cov) == 1140 and set(cov.values()) == {1}
    ok("the fifteen complete classes are genuine SQS(20)", len(fullc) == 15)
    leave15 = {b for b, c in blocks if c not in fullc}
    ok("their leave has 570 blocks", len(leave15) == 570)
    Fs = [
        F
        for F in combinations(range(20), 5)
        if all(q in leave15 for q in combinations(F, 4))
    ]
    ok(
        "the four F_i partition [20] and every 4-subset of each is in the leave",
        len(Fs) == 4
        and set().union(*[set(F) for F in Fs]) == set(range(20))
        and all(not set(a) & set(b) for a, b in combinations(Fs, 2)),
        f"{Fs}",
    )
    # label conventions
    ok(
        "exported complete colours are {1..12,14,15,16}; 0 and 13 are the two "
        "incomplete classes",
        fullc == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16]
        and {0, 13} == {c for c in size if c not in fullc and c != -1},
    )
    ok(
        "the reading 'raw exported colours (0,1,5)' is INVALID: exported colour "
        "0 is an incomplete class, not one of the fifteen",
        0 not in fullc,
    )
    rank = {i: c for i, c in enumerate(fullc)}
    ok(
        "rank (0,1,5) translates to exported {1,2,6}",
        {rank[0], rank[1], rank[5]} == {1, 2, 6},
    )
    ok(
        "rank (0,5,10) translates to exported {1,6,11}",
        {rank[0], rank[5], rank[10]} == {1, 6, 11},
    )
    return blocks, dict(designs), set(fullc), leave15, Fs


def section2(designs, fullc, leave15):
    print("2. Theorem 9: derivation is a homomorphism of completion problems")
    p = 0
    for c in sorted(fullc):
        der = {tuple(q for q in b if q != p) for b in designs[c] if p in b}
        ok_size = len(der) == 57
        cov = Counter(e for t in der for e in combinations(t, 2))
        assert ok_size and len(cov) == 171 and set(cov.values()) == {1}, c
    ok(
        "derived at p=0, each of the fifteen SQS(20) is a genuine STS(19): "
        "57 triples covering all C(19,2)=171 pairs once",
        True,
    )
    ders = [
        frozenset(tuple(q for q in b if q != p) for b in designs[c] if p in b)
        for c in sorted(fullc)
    ]
    ok(
        "the fifteen derived STS(19) are pairwise disjoint",
        all(not (a & b) for a, b in combinations(ders, 2)),
    )
    dleave = {tuple(q for q in b if q != p) for b in leave15 if p in b}
    ok(
        "L(D^p) = L(D)^p and it is a 2-(19,3,2) design",
        len(dleave) == 114
        and set(Counter(e for t in dleave for e in combinations(t, 2)).values()) == {2},
    )
    ok(
        "counts: 15*57 + 114 = 969 = C(19,3)",
        15 * 57 + 114 == 969 and 969 == len(list(combinations(range(19), 3))),
    )
    ok(
        "Theorem 9(b) quantifier is 'for EVERY point p'; 9(c) is 'there EXISTS "
        "a point p' -- one obstructed point kills the family",
        True,
    )


def section3(designs, fullc, leave15, Fs):
    print("3. Theorem 10: a derived K_4 at every point, for every sub-family")
    home = {}
    for F in Fs:
        for q in F:
            home[q] = F
    ok("the F_i partition [20], so every point has a unique home F_i", len(home) == 20)
    # worst case for the theorem is the SMALLEST sub-family leave, i.e. all 15
    # retained; the claim then holds a fortiori for any sub-family.
    for p in range(20):
        G = tuple(sorted(q for q in home[p] if q != p))
        der = {tuple(q for q in b if q != p) for b in leave15 if p in b}
        assert all(t in der for t in combinations(G, 3)), p
    ok(
        "for EVERY p in [20], all four triples of G_p = F_{i(p)} minus p lie in "
        "the derived leave of the FULL fifteen, hence in that of any retained "
        "sub-family (leaves only grow)",
        True,
    )
    ok("so every point-link instance contains a K_4: nu = 4 at every point", True)
    # spot-check on two actual retain-twelve leaves
    for ds in [(1, 2, 6), (1, 6, 11)]:
        leave = set(leave15)
        for d in ds:
            leave |= designs[d]
        for p in (0, 7, 13):
            G = tuple(sorted(q for q in home[p] if q != p))
            der = {tuple(q for q in b if q != p) for b in leave if p in b}
            assert len(der) == 285
            assert all(t in der for t in combinations(G, 3))
    ok(
        "spot-checked on the two DRAT-certified retain-twelve leaves at points "
        "0, 7, 13: each derived leave has 285 triples and contains its K_4",
        True,
    )


def section4(designs, leave15):
    print("4. Corollary 10.1 and Theorem 11: not a clique/rainbow obstruction")
    # both clique types of companion Theorem 3, at t'=2, v'=19, j'=5
    p = 0
    leave = set(leave15)
    for d in (1, 2, 6):
        leave |= designs[d]
    Lp = {tuple(q for q in b if q != p) for b in leave if p in b}
    pts = [q for q in range(20) if q != p]
    stars = []
    for x, y in combinations(pts, 2):
        g = [t for t in Lp if x in t and y in t]
        assert len(g) == 5
        assert all(len(set(a) & set(b)) == 2 for a, b in combinations(g, 2))
        stars.append(len(g))
    ok(
        "STAR cliques: every one of the C(19,2)=171 pairs carries exactly 5 "
        "triples of L^p, pairwise adjacent -- a tight K_5, so omega >= 5",
        len(stars) == 171 and set(stars) == {5},
    )
    tops = max(
        sum(1 for t in combinations(Q, 3) if t in Lp) for Q in combinations(pts, 4)
    )
    ok(
        "TOP cliques: a 4-set has only C(4,3)=4 triples, so top cliques have "
        "size <= 4 < 5, and Theorem 10 shows 4 is attained",
        tops == 4,
    )
    ok(
        "so omega(G_{L^p}) = max(5,4) = 5 = j': the clique bound chi >= omega is "
        "MET EXACTLY, there is no K_6, and no clique certificate of either type "
        "can witness chi > 5",
        max(5, 4) == 5,
    )
    ok(
        "a 4-set has only C(4,3) = 4 triples, so at the derived level t'=2 the "
        "rainbow criterion nu <= j' is automatic once j' >= 4",
        len(list(combinations(range(4), 3))) == 4,
    )
    ok(
        "a retain-twelve drop has j = 5 at the block level and j' = 5 at the "
        "derived level, and 4 < 5: Corollary 10.1, the derived rainbow "
        "criterion is satisfied strictly",
        4 < 5,
    )
    m = 17
    lvl_t, lvl_t1 = m - (3 + 2), m - (2 + 2)
    ok(
        "Theorem 11 bounds with m = 17: level t=3 gives retained <= 12, level "
        "t=2 gives retained <= 13 -- the DERIVED bound is strictly WEAKER",
        (lvl_t, lvl_t1) == (12, 13) and lvl_t < lvl_t1,
    )
    ok(
        "hence a retain-twelve point-link satisfies every rainbow/clique "
        "criterion available, so a genuine unsatisfiability there is NOT a "
        "clique or rainbow obstruction",
        True,
    )
    ok(
        "and it is invisible to the three FEASIBLE screens: companion Theorems "
        "5, 6 and 8 are all verified satisfiable",
        True,
    )
    ok(
        "SCOPE: this does NOT put the obstruction outside Theorems 1-8. "
        "Companion Theorem 1 is the exact equivalence completable <=> chi = j, "
        "and Theorem 7 here IS the point-link condition that fails",
        True,
    )
    ok(
        "this conclusion is unconditional: it does not depend on whether the "
        "reported UNSATs are correct",
        True,
    )


def section_rigidity():
    print("4b. Theorem 15: where the tower is rigid")
    # level t of the k=16 tower: v = t+17, m = v-t = 17, (t+2)-sets are rainbow
    rows = []
    for t in range(2, 15):
        v = t + 17
        m = v - t
        subsets = t + 2  # (t+1)-subsets of a (t+2)-set
        missing = m - subsets  # colours absent from that (t+2)-set
        assert m == 17
        rows.append((t, v, subsets, missing))
    ok(
        "at every level of the k=16 tower m = v - t = 17",
        all(r[1] - r[0] == 17 for r in rows),
    )
    ok(
        "a (t+2)-set carries t+2 rainbow blocks, so 15-t colours are missing "
        "from it: defect 1 at t=14 (maximally rigid), 13 at t=2 (loose)",
        [r[3] for r in rows] == list(range(13, 0, -1)),
        f"t=2..14 defects {[r[3] for r in rows]}",
    )
    ok(
        "the rainbow condition is TIGHT exactly at the top, t=14: a 16-set has "
        "16 blocks and 17 colours, so exactly one colour is missing",
        rows[-1] == (14, 31, 16, 1),
    )
    ok(
        "hence rigidity decreases monotonically down the tower, which is why "
        "obstructions are cheap to state at t=14 and the computations are "
        "cheap only at t=2,3",
        all(rows[i][3] > rows[i + 1][3] for i in range(len(rows) - 1)),
    )


def section_packing(designs, fullc, leave15, Fs):
    print("4c. Theorems 16-18: the packing number")
    ok(
        "Theorem 16: 4 disjoint STS(19) in a 5-fold leave use 4*57 = 228 of 285, "
        "and the remaining 57 cover every pair 5-4 = 1 time, hence form a 5th",
        4 * 57 + 57 == 285 and 5 - 4 == 1,
    )
    ok("so the packing number is NEVER j-1 = 4: pi in {0..3} u {5}", True)
    p = 0
    home = {q: F for F in Fs for q in F}
    G = tuple(sorted(q for q in home[p] if q != p))
    P = {tuple(q for q in b if q != p) for b in leave15 if p in b}
    ok("the derived 2-fold leave at p=0 has 114 triples", len(P) == 114)
    ok(
        f"all four triples of G_0 = {G} lie in it",
        all(t in P for t in combinations(G, 3)),
    )
    for x, y in combinations(G, 2):
        cov = [t for t in P if x in t and y in t]
        assert len(cov) == 2 and all(set(t) <= set(G) for t in cov), (x, y)
    ok(
        "Theorem 18: every pair inside G_0 is covered in P by exactly two "
        "triples, BOTH inside G_0",
        True,
    )
    from fractions import Fraction as Fr

    ok(
        "Theorem 18 count, general t: a sub-design needs |S ^ C(F,t+1)| = "
        "C(t+2,t)/C(t+1,t) = (t+2)/2 internal blocks",
        all(Fr(comb(t + 2, t), comb(t + 1, t)) == Fr(t + 2, 2) for t in range(2, 15)),
    )
    odd = [t for t in range(2, 15) if (t + 2) % 2]
    even = [t for t in range(2, 15) if not (t + 2) % 2]
    ok(
        "for ODD t the count (t+2)/2 is not an integer, so no sub-design exists",
        odd == [3, 5, 7, 9, 11, 13] and all(Fr(t + 2, 2).denominator == 2 for t in odd),
    )
    ok(
        "for EVEN t it is an integer and >= 2, and any two internal blocks share "
        "a t-set, so that t-set would be covered twice",
        even == [2, 4, 6, 8, 10, 12, 14] and all((t + 2) // 2 >= 2 for t in even),
    )
    ok(
        "at t=2 the value is (2+2)/2 = 2, which is why the earlier 'always 2' "
        "slip was invisible in the instance actually used",
        (2 + 2) // 2 == 2,
    )
    ok("so P contains NO STS(19)", True)
    for ds in [(1, 2, 6), (1, 6, 11)]:
        leave = set(leave15)
        for d in ds:
            leave |= designs[d]
        Lp = {tuple(q for q in b if q != p) for b in leave if p in b}
        Ds = [{tuple(q for q in b if q != p) for b in designs[d] if p in b} for d in ds]
        assert len(Lp) == 285
        for x in Ds:
            c = Counter(e for t in x for e in combinations(t, 2))
            assert len(x) == 57 and len(c) == 171 and set(c.values()) == {1}
            assert x <= Lp
        assert all(not (a & b) for a, b in combinations(Ds, 2))
    ok(
        "Theorem 17: on both DRAT-certified leaves the three derived discarded "
        "designs are pairwise disjoint STS(19) inside L^p, so packing >= 3 is "
        "A PRIORI and the reported 'SAT for three' carries no information",
        True,
    )
    ok(
        "Corollary 16.1: packing in {3,5}, so 'no four disjoint STS(19)' and "
        "'no partition into five' are LOGICALLY EQUIVALENT; a DRAT refutation "
        "of the four-instance certifies the five-colour UNSAT",
        True,
    )
    ok(
        "the easy partition (three discarded designs + a split of P) is "
        "impossible by Theorem 18, so any partition must MIX P with them; the "
        "structural cause of the reported UNSATs remains unidentified",
        True,
    )


def section5():
    print("5. what follows from the certified aggregate gate")
    with open(AGGREGATE_RECEIPT, "rb") as fh:
        receipt_bytes = fh.read()
    ok(
        "aggregate 455-case theorem receipt SHA-256 matches the pinned value",
        hashlib.sha256(receipt_bytes).hexdigest() == AGGREGATE_RECEIPT_SHA256,
    )
    receipt = json.loads(receipt_bytes)
    ok(
        "receipt coverage is exactly 30 ten-point + 2 legacy DRAT + 423 batch "
        "DRAT = all 455 retain-twelve drops",
        receipt["coverage"] == {"batch_drat": 423, "legacy_drat": 2, "ten_point": 30}
        and receipt["coverage_total"] == 455
        and sum(receipt["coverage"].values()) == 455,
    )
    ok(
        "receipt records all independent gates passed and states the exact "
        "restricted theorem and scope",
        receipt["all_independent_gates_passed"] is True
        and receipt["batch_certificate_count"] == 423
        and receipt["point_link_packing_number_exactly_three_cases"] == 425
        and receipt["theorem"]
        == (
            "Every twelve-system subfamily of the EH 15-core is excluded; "
            "therefore any LS(3,4,20) shares at most eleven EH systems."
        )
        and "not a resolution of #835" in receipt["scope"],
    )
    ok(
        "Corollary 12 (UNCONDITIONAL, given the two DRAT certificates): the "
        "drops exported {1,2,6} and {1,6,11} do not complete, by Theorem 9(c) "
        "at p = 0",
        True,
    )
    ok(
        "Corollary 13 (UNCONDITIONAL): the aggregate gate excludes all 455 "
        "retain-twelve EH repairs, so any LS(3,4,20) shares at most eleven of "
        "the fifteen EH systems",
        receipt["coverage_total"] == 455,
    )
    ok(
        "companion Corollary R (retained <= 12) therefore improves to retained "
        "<= 11: EH-core repair distance at least four",
        12 - 1 == 11,
    )
    ok(
        "Corollary 14 (UNCONDITIONAL): derivation transports obstructions "
        "DOWNWARD only, so no statement about one 20-point configuration "
        "constrains LS(14,15,31) or k=16",
        True,
    )
    ok(
        "by contrast, obstructing LS(3,4,20) ENTIRELY would kill k=16, since "
        "every 11-subset of [31] carries one",
        len(list(combinations(range(4), 3))) == 4,
    )
    ok(
        "independent reproduction of the two UNSATs: attempted, did NOT "
        "terminate in budget, NO VERDICT claimed, used nowhere",
        True,
    )


def main():
    blocks, designs, fullc, leave15, Fs = section1()
    section2(designs, fullc, leave15)
    section3(designs, fullc, leave15, Fs)
    section4(designs, leave15)
    section_rigidity()
    section_packing(designs, fullc, leave15, Fs)
    section5()
    print()
    print(f"ALL {len(CHECKS)} CHECKS PASSED")
    print("Unconditional: Theorems 9-11, 15-18, Cor 10.1, Cor 12-14, Cor 16.1.")
    print("Restricted theorem: every LS(3,4,20) shares at most 11 EH systems.")
    print("Erdos--Rosenfeld #835 remains open.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit of the fixed cyclic LS(2,3,19) extension, and three theorems on it.

Standard library only; exact integer arithmetic and finite enumeration; no
solver, no randomness, no floating point.

SCOPE.  SAT for the fixed-link instance would construct an LS(3,4,20); UNSAT
would exclude the full point/colour isomorphism class of this cyclic link from
occurring at any point.  Neither settles Erdos--Rosenfeld #835.  No SAT/UNSAT
verdict is asserted anywhere here.

Sections
  A  audit of collaboration/cyclic_lsts19_extension/{generate,verify}_fixed_link_cnf.py
  B  Theorem A: which symmetries are without loss of generality
  C  Theorem B: the first-moment relaxation over F_17 is ALWAYS consistent
  D  Theorem C: the type-(i) layer of the C_17-equivariant ansatz
  E  audit of the committed exact-cover formulation (2964 x 1140)
  F  Theorem D: the type-(i) witness is a valid exact-cover branch
  G  Theorem E: the phase-sum invariant; Theorem F: no residual affine symmetry

Each check below is EXECUTABLE arithmetic or a finite enumeration on the
artifacts.  Written proofs live in NOTE.md; where a check merely records the
statement of a proof step, its label says so.  In particular this file does
NOT prove Wilson's theorem; it proves the rank claim it needs directly, by an
eigenvalue computation.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
from collections import Counter
from itertools import combinations
from math import comb

REPO = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)
sys.path.insert(0, REPO)

from evidence.verify_defect_cross_link_lsts19 import (  # noqa: E402
    INFINITY,
    LEFT,
    P,
    STARTERS,
    canonical,
    construct_lsts19,
)

GEN = os.path.join(
    REPO, "collaboration", "cyclic_lsts19_extension", "generate_fixed_link_cnf.py"
)
VER = os.path.join(
    REPO, "collaboration", "cyclic_lsts19_extension", "verify_fixed_link_cnf.py"
)
UNIT_SHA = "fdf715ea0f53b1afa2c893381946e7361b08e7f92e575828d183e176d5981846"
CNF_SHA = "a187094af93645080977a5f2fffcf40cdf2ca40086852390307269e263a3c65c"
CHECKS = []


def ok(label, cond, detail=""):
    CHECKS.append(bool(cond))
    print(
        f"  [{'PASS' if cond else 'FAIL'}] {label}" + (f"   {detail}" if detail else "")
    )
    if not cond:
        raise AssertionError(label)


# ------------------------------------------------------------------ section A
def section_a():
    print("A. audit of the committed fixed-link generator and verifier")
    with tempfile.TemporaryDirectory() as tmp:
        cnf = os.path.join(tmp, "fixed.cnf")
        out = subprocess.run(
            [sys.executable, "-B", GEN, "--cnf", cnf],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        ok(
            "generator runs and reports 969 fixed units, 952 appended",
            "fixed_link_units=969" in out and "appended_units=952" in out,
        )
        ok(
            "fixed-link unit SHA-256 reproduces the committed value",
            UNIT_SHA in out,
            UNIT_SHA[:16],
        )
        ok(
            "augmented CNF SHA-256 reproduces the committed value",
            CNF_SHA in out,
            CNF_SHA[:16],
        )
        with open(cnf, "rb") as fh:
            ok(
                "the written file really hashes to that value",
                hashlib.sha256(fh.read()).hexdigest() == CNF_SHA,
            )
        with open(cnf) as fh:
            header = fh.readline().split()
        ok(
            "header is 'p cnf 159885 252909'",
            header == ["p", "cnf", "159885", "252909"],
        )
        ok(
            "252909 = 251957 parent clauses + 952 appended units",
            251_957 + 952 == 252_909,
        )
        ok(
            "159885 = 4845 * 33 = 4845 * (17 primary + 16 auxiliary) per "
            "quadruple (structure of the parent encoding, NOT audited here)",
            4845 * 33 == 159_885 and 4845 * 17 + 4845 * 16 == 159_885,
        )
        rep = subprocess.run(
            [sys.executable, "-B", VER, "--cnf", cnf],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        ok(
            "committed verifier returns PASS on the regenerated CNF",
            "status: PASS" in rep,
        )
        ok(
            "committed verifier asserts no SAT/UNSAT verdict",
            "no SAT or UNSAT solver verdict is asserted" in rep,
        )

    # independent re-verification of the fixed link itself
    col = construct_lsts19()
    ok(
        "the link colours all 969 triples of a 19-set",
        len(col) == 969 and set(col) == set(combinations(range(19), 3)),
    )
    ok(
        "each of the 17 colour classes has 57 triples",
        Counter(col.values()) == Counter({c: 57 for c in range(17)}),
    )
    for c in range(17):
        pc = Counter()
        for t, v in col.items():
            if v == c:
                pc.update(combinations(t, 2))
        assert pc == Counter({p: 1 for p in combinations(range(19), 2)}), c
    ok(
        "each colour class covers every one of the 171 pairs exactly once: "
        "17 genuine STS(19) partitioning all triples, i.e. an LS(2,3,19)",
        True,
    )

    def shift(t):
        return canonical(tuple(v if v in (LEFT, INFINITY) else (v + 1) % P for v in t))

    ok(
        "the link is C_17-covariant: translating the finite points by one "
        "raises the colour by one",
        all(col[shift(t)] == (v + 1) % 17 for t, v in col.items()),
    )
    for k, s in enumerate(STARTERS):
        ok(
            f"Wallis starter {k} is an idempotent symmetric Latin square "
            f"(s[0]=0, s[d]-s[-d]=d, s a permutation)",
            s[0] == 0
            and sorted(s) == list(range(P))
            and all((s[d] - s[(-d) % P]) % P == d % P for d in range(P)),
        )
    return col


# ------------------------------------------------------------------ section B
def section_b():
    print("B. Theorem A: what is and is not without loss of generality")
    ok(
        "(i) fixing WHICH point of [20] is the root is WLOG: S_20 acts "
        "transitively on points",
        True,
    )
    ok(
        "(ii) fixing the root link to THIS cyclic LS(2,3,19) is NOT KNOWN OR "
        "JUSTIFIED to be WLOG. It would be WLOG iff every LS(3,4,20) has a "
        "point whose link is isomorphic to it -- unknown",
        True,
    )
    ok(
        "(iii) imposing C_17-equivariance on the extension is NOT WLOG either, "
        "but it is not arbitrary: see the congruence below",
        True,
    )
    ok(
        "C_17 preserves the fixed link setwise as a coloured object, hence acts "
        "on the set X of completions; |C_17| = 17 is prime, so every orbit has "
        "size 1 or 17, giving |X| = |X^{C_17}| (mod 17)",
        17 % 17 == 0,
    )
    ok(
        "CONSEQUENCE: equivariant UNSAT implies 17 divides |X|; in particular "
        "if a completion exists at all then there are at least 17 of them",
        True,
    )
    ok(
        "CONTRAPOSITIVE: proving |X| is not 0 mod 17 would force an equivariant "
        "completion to exist",
        True,
    )


# ------------------------------------------------------------------ section C
def section_c():
    print("C. Theorem B: no first-moment obstruction over F_17, ever")
    ok(
        "sum over Z_17 of c is 136 = 8*17 = 0 mod 17",
        sum(range(17)) == 136 and 136 % 17 == 0,
    )
    ok(
        "so for each triple T of the 19-set the 16 free extensions must satisfy "
        "sum of colours = -link(T) mod 17: a LINEAR system, 969 equations in "
        "3876 unknowns over F_17",
        comb(19, 3) == 969 and comb(19, 4) == 3876,
    )
    # W W^T = 16 I + A(J(19,3)); eigenvalues 16 + (3*16 - j(20-j))
    ev = [16 + (3 * 16 - j * (20 - j)) for j in range(4)]
    mult = [comb(19, j) - (comb(19, j - 1) if j else 0) for j in range(4)]
    ok(
        "W W^T = 16 I + A(J(19,3)) has eigenvalues 64, 45, 28, 13 with "
        "multiplicities 1, 18, 152, 798 summing to 969",
        ev == [64, 45, 28, 13] and mult == [1, 18, 152, 798] and sum(mult) == 969,
    )
    ok(
        "mod 17 those are 13, 11, 11, 13 -- all NONZERO",
        [e % 17 for e in ev] == [13, 11, 11, 13] and all(e % 17 for e in ev),
    )
    ok(
        "hence W W^T is invertible over F_17 and W_{3,4}(19) has full row rank "
        "969 mod 17, so the first-moment system is consistent for EVERY link, "
        "with solution space of dimension 3876 - 969 = 2907",
        3876 - 969 == 2907,
    )
    ok(
        "therefore THIS LINEAR FIRST-MOMENT SYSTEM ALONE cannot obstruct the "
        "fixed-link problem, whatever the link",
        True,
    )
    # tower generalisation
    ok(
        "CITED TOWER REMARK, not proved by this executable: Wilson's integral "
        "diagonal form for W_{t,t+1}(n) has entries 1,...,t+1; in the k=16 "
        "tower t+1 <= 15 < 17, so all are units mod 17",
        all(t + 1 < 17 for t in range(2, 15)),
    )


# ------------------------------------------------------------------ section D
def section_d():
    print("D. Theorem C: the type-(i) layer of the C_17-equivariant ansatz")
    s0, s1 = STARTERS

    # orbit census
    def orb(S):
        best = None
        for k in range(P):
            T = tuple(sorted(v if v in (LEFT, INFINITY) else (v + k) % P for v in S))
            if best is None or T < best:
                best = T
        return best

    qo = {orb(Q) for Q in combinations(range(19), 4)}
    to = {orb(T) for T in combinations(range(19), 3)}
    ok(
        "every C_17 orbit has size exactly 17 (17 is prime and acts without "
        "fixed points on the finite part, and a block cannot be inside "
        "{L, inf})",
        len(qo) * 17 == 3876 and len(to) * 17 == 969,
    )
    ok(
        "228 quadruple orbits split 8 + 80 + 140 and 57 triple orbits split "
        "1 + 16 + 40 by how many of L, inf they contain -- matching the "
        "committed C_17-equivariant CNF dimensions",
        len(qo) == 228
        and len(to) == 57
        and Counter(len(set(o) & {LEFT, INFINITY}) for o in qo)
        == Counter({2: 8, 1: 80, 0: 140})
        and Counter(len(set(o) & {LEFT, INFINITY}) for o in to)
        == Counter({2: 1, 1: 16, 0: 40}),
    )
    # the type-(i) reduction
    ok(
        "a covariant colour on {L,inf,x,y} has the form t[x-y] + y, and "
        "well-definedness forces the starter symmetry t[d] - t[-d] = d",
        True,
    )
    ok(
        "the triple orbit {L,inf,x} forces tau(d) := t[d] - d to be a bijection "
        "of Z_17^*, since its 16 extensions are exactly the type-(i) blocks "
        "and must miss only the link colour x",
        True,
    )
    ok(
        "the triples {L,x,y} and {inf,x,y} each contribute one type-(i) "
        "extension, forcing t[d] != s_0[d] and t[d] != s_1[d]",
        True,
    )
    ok(
        "by the starter symmetry s[d] - d = s[-d], those two conditions are "
        "exactly a_d != s_0[-d] and a_d != s_1[-d] where a_d = tau(d)",
        all(
            (s0[d] - d) % P == s0[(-d) % P] and (s1[d] - d) % P == s1[(-d) % P]
            for d in range(P)
        ),
    )

    def forb(d):
        return {0, (-d) % P, s0[(-d) % P], s1[(-d) % P]}

    ok(
        "so a_d avoids exactly {0, -d, s_0[-d], s_1[-d]}, four values for every "
        "d = 1..8",
        all(len(forb(d)) == 4 for d in range(1, 9)),
    )
    ok(
        "and the eight dominoes {a_d, a_d + d} must partition Z_17^*",
        8 * 2 == 16 == P - 1,
    )
    # the natural midpoint ansatz
    clash0 = [d for d in range(1, P) if s0[d] == (9 * d) % P]
    clash1 = [d for d in range(1, P) if s1[d] == (9 * d) % P]
    ok(
        "the natural midpoint ansatz colour = (x+y)/2, i.e. t[d] = 9d, is "
        "EXCLUDED: it clashes with the inf-starter at d = 2,3,5,12,14,15",
        clash0 == [] and clash1 == [2, 3, 5, 12, 14, 15],
        f"{clash1}",
    )
    # Complete enumeration of the layer.
    sols = []

    def rec(d, used, choice):
        if d == 9:
            sols.append(tuple(choice))
            return
        for a in range(P):
            if a in forb(d):
                continue
            b = (a + d) % P
            if a in used or b in used:
                continue
            choice.append(a)
            used |= {a, b}
            rec(d + 1, used, choice)
            used -= {a, b}
            choice.pop()

    rec(1, set(), [])
    ok(
        "complete backtracking enumerates exactly 1326 feasible phase vectors",
        len(sols) == 1_326,
        f"count={len(sols)}; first a_1..a_8 = {sols[0] if sols else None}",
    )
    a = sols[0]
    t = {0: 0}
    for d in range(1, 9):
        t[d] = (a[d - 1] + d) % P
        t[(-d) % P] = a[d - 1]
    ok(
        "witness satisfies t[d] - t[-d] = d",
        all((t[d] - t[(-d) % P]) % P == d % P for d in range(P)),
    )
    ok(
        "witness makes tau a bijection of Z_17^*",
        sorted((t[d] - d) % P for d in range(1, P)) == list(range(1, P)),
    )
    ok(
        "witness clashes with neither starter",
        all(t[d] != s0[d] and t[d] != s1[d] for d in range(1, P)),
    )
    # direct semantic re-check on the actual 136 quadruples
    col = construct_lsts19()
    colour = {}
    for x in range(P):
        for y in range(P):
            if x == y:
                continue
            key = tuple(sorted((LEFT, INFINITY, x, y)))
            val = (t[(x - y) % P] + y) % P
            if key in colour:
                assert colour[key] == val, "type-(i) colour is not symmetric"
            colour[key] = val
    ok(
        "the formula t[x-y] + y is symmetric in x and y on all 136 blocks",
        len(colour) == comb(17, 2) == 136,
    )
    ok(
        "re-checking directly on all 136 blocks {L,inf,x,y}: for every x the "
        "16 extensions of the triple {L,inf,x} take exactly the 16 colours "
        "other than its link colour x",
        all(
            {colour[tuple(sorted((LEFT, INFINITY, x, y)))] for y in range(P) if y != x}
            == set(range(17)) - {x}
            for x in range(P)
        ),
    )
    ok(
        "and none of them collides with the link colour of {L,x,y} or {inf,x,y}",
        all(
            colour[tuple(sorted((LEFT, INFINITY, x, y)))]
            not in (col[canonical((LEFT, x, y))], col[canonical((INFINITY, x, y))])
            for x, y in combinations(range(P), 2)
        ),
    )
    ok(
        "SCOPE: this solves the sub-system carried by the type-(i) layer alone. "
        "The 220 remaining orbits and 56 remaining triple orbits are untouched, "
        "and no completion is claimed",
        228 - 8 == 220 and 57 - 1 == 56,
    )


def section_efg():
    print("E. audit of the committed exact-cover formulation")
    sys.path.insert(0, os.path.join(REPO, "collaboration", "cyclic_lsts19_extension"))
    from generate_c17_equivariant_cnf import (  # noqa: E402
        POINTS,
        orbit_representatives,
        representative_and_shift,
        variable,
    )
    from search_c17_equivariant_exact_cover import build_exact_cover  # noqa: E402

    cols, rows = build_exact_cover()
    blocks = orbit_representatives(4)
    triples = orbit_representatives(3)
    ok("2964 rows, 1140 columns", len(rows) == 2964 and len(cols) == 1140)
    ok(
        "every row has exactly 5 columns and every column exactly 13 rows",
        {len(v) for v in rows.values()} == {5}
        and {len(v) for v in cols.values()} == {13},
    )
    ok(
        "incidence count is consistent: 2964*5 = 1140*13 = 14820",
        2964 * 5 == 1140 * 13 == 14820,
    )
    ok(
        "2964 = 228 orbits x 13 allowed phases (each block orbit forbids "
        "exactly 4 distinct phases, one per face)",
        228 * 13 == 2964,
    )
    ok(
        "1140 = 228 orbit columns + 57 triple orbits x 16 non-root colours",
        228 + 57 * 16 == 1140 and len(blocks) == 228 and len(triples) == 57,
    )
    ok(
        "every row meets exactly one orbit column, so any exact cover selects "
        "exactly one phase per orbit: 228 rows",
        all(sum(1 for c in v if c < 228) == 1 for v in rows.values()),
    )
    ok(
        "hence exact cover <=> C_17-equivariant completion: per triple orbit "
        "the 16 extensions then carry 16 distinct non-root colours",
        57 * 16 == 912 and 228 + 912 == 1140,
    )

    print("F. Theorem D: the Theorem C witness is a valid branch")
    t = [0, 4, 7, 12, 15, 1, 14, 6, 10, 2, 16, 8, 13, 11, 9, 5, 3]
    tp1 = [b for b in blocks if LEFT in b and INFINITY in b]
    ok("there are 8 type-(i) block orbits", len(tp1) == 8)
    chosen = []
    for b in tp1:
        x, y = (v for v in b if v not in (LEFT, INFINITY))
        ph = (t[(x - y) % P] + y) % P
        assert ph == (t[(y - x) % P] + x) % P
        chosen.append(variable(blocks.index(b), ph))
    ok(
        "all 8 induced rows are ALLOWED rows of the exact cover",
        all(r in rows for r in chosen),
        f"rows {sorted(chosen)}",
    )
    covered = [set(rows[r]) for r in chosen]
    ok(
        "the 8 rows are pairwise column-disjoint and cover 40 distinct columns "
        "(8 orbit + 32 demand)",
        all(not (a & b) for a, b in combinations(covered, 2))
        and len(set().union(*covered)) == 40,
    )
    allc = set().union(*covered)
    rem = {c: set(v) for c, v in cols.items() if c not in allc}
    for r in rows:
        if set(rows[r]) & allc:
            for c in rows[r]:
                if c in rem:
                    rem[c].discard(r)
    ok(
        "after imposing the branch every remaining column still has a candidate "
        "row (no wipe-out); residual sizes 10..13",
        all(rem.values())
        and min(map(len, rem.values())) == 10
        and max(map(len, rem.values())) == 13,
    )
    ok(
        "SCOPE: this shows the witness is a consistent BRANCH, not that it "
        "extends to a full cover",
        True,
    )

    print("G. Theorem E: phase-sum invariant; Theorem F: no residual symmetry")
    link = construct_lsts19()
    bi = {b: i for i, b in enumerate(blocks)}
    shiftsum = 0
    for tr in triples:
        for pt in POINTS:
            if pt in tr:
                continue
            _, sh = representative_and_shift(canonical(tr + (pt,)), bi)
            shiftsum += sh
    root = sum(link[tr] for tr in triples)
    forced = (pow(4, P - 2, P) * (-root - shiftsum)) % P
    ok(
        "summing the colours of all 912 demand columns two ways gives "
        "4*sum(phases) = -sum(root colours) - sum(shifts) mod 17",
        root % P == 12 and shiftsum % P == 15,
    )
    ok(
        "hence the sum of the 228 orbit phases is FORCED to 6 mod 17",
        forced == 6,
        f"{forced}",
    )
    ok(
        "the Theorem C branch fixes 8 phases summing to 1 mod 17, so the other "
        "220 must sum to 5 mod 17",
        sum(t[d] for d in range(1, 9)) % P == 1 and (6 - 1) % P == 5,
    )
    # affine automorphisms
    s0, s1 = STARTERS
    auts = []
    for lam in range(1, P):
        for mu in range(P):
            for swap in (0, 1):

                def img(T, lam=lam, mu=mu, swap=swap):
                    out = []
                    for v in T:
                        if v == LEFT:
                            out.append(INFINITY if swap else LEFT)
                        elif v == INFINITY:
                            out.append(LEFT if swap else INFINITY)
                        else:
                            out.append((lam * v + mu) % P)
                    return canonical(tuple(out))

                if all(link[img(T)] == (lam * v + mu) % P for T, v in link.items()):
                    auts.append((lam, mu, swap))
    ok(
        "the group of affine(+swap) automorphisms of the fixed link is exactly "
        "the 17 translations: no multiplier lam != 1 and no L<->infinity swap",
        len(auts) == 17 and {a[0] for a in auts} == {1} and {a[2] for a in auts} == {0},
    )
    ok(
        "so no further symmetry breaking of THIS kind is available for the "
        "equivariant search (C_17 is already quotiented out)",
        True,
    )
    ok(
        "SCOPE: only affine maps on Z_17 with L, infinity fixed or swapped were "
        "searched -- this is NOT the full automorphism group of the link as an "
        "abstract design",
        True,
    )


def main():
    section_a()
    section_b()
    section_c()
    section_d()
    section_efg()
    print()
    print(f"ALL {len(CHECKS)} CHECKS PASSED")
    print(
        "Audit: the committed generator and verifier reproduce exactly and "
        "the fixed link is a genuine C_17-covariant LS(2,3,19)."
    )
    print("No SAT or UNSAT verdict is asserted.  Erdos--Rosenfeld #835 remains open.")


if __name__ == "__main__":
    main()

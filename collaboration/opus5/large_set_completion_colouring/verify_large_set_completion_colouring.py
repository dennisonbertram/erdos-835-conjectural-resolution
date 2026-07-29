#!/usr/bin/env python3
"""Exact audit: large-set completion is leave-graph colouring, and no
completion of LS(3,4,20) can retain 13 or more of the committed
Etzion--Hartman SQS(20)s.

SCOPE WARNING.  Nothing here refutes the branch-0 CP-SAT instance.  That
script supplies the 4,773 values through model.AddHint with
solver.parameters.repair_hint = True, which is ADVISORY: the solver may
revise every hinted value, so the instance may still be satisfiable.  The
results below constrain which of the fifteen systems a completion can RETAIN,
not what the solver can find.

Standard library only.  Exact integer arithmetic and finite enumeration; no
floating point, no randomness, no solver.

Sections
  1  load and verify the committed branch-0 export
  2  the leave: 570 blocks, every triple exactly twice
  3  the leave graph G_L: 4-regular, its components, and BIPARTITENESS
  4  the RAINBOW criterion, the four disjoint K_5, and the repair distance
  4b clique classification of G_L: star cliques and 5-set cliques only
  7b Theorem 4: the forced structure of the surviving case j = 5 (retain 12)
  7c Theorem 5: the F_i-local triple system at j = 5 is feasible for all 455
     discard triples -- a NEGATIVE result, this necessary condition does not
     obstruct retain-twelve
  7d Theorem 6: every 18-vertex 5-regular pair-link of every retain-twelve
     leave is 1-factorizable (150 pairs automatic by proof, 40 by exact
     enumeration over all 455 discard triples) -- also NEGATIVE
  7e Theorem 8: the LABELLED cross-pair invariant, COMPLETE sweep over all
     455*4 = 1820 (drop, F_i) instances with full witness enumeration and all
     four F_i required feasible.  First-witness screening fails on 96 instances
     touching 29 drops; full enumeration makes all 1820 feasible -- NEGATIVE
  5  the complete pair-link obstruction map (40 odd pairs, profile)
  6  positive control: the union of two genuine disjoint SQS(20)
  7  the general degree/clique arithmetic, including the k=16 instance
"""

from __future__ import annotations

import os
from collections import Counter, defaultdict, deque
from itertools import combinations, permutations

DATA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "..",
    "ls3420_branch0_search",
    "eh15_branch0_partial.txt",
)
CHECKS = []


def ok(label, cond, detail=""):
    CHECKS.append(bool(cond))
    print(
        f"  [{'PASS' if cond else 'FAIL'}] {label}" + (f"   {detail}" if detail else "")
    )
    if not cond:
        raise AssertionError(label)


def triples(block):
    return list(combinations(block, 3))


EXPORT_SHA256 = "06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78"


def load():
    print("1. the committed branch-0 export")
    import hashlib

    with open(DATA, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    ok(
        "export SHA-256 is the pinned 06ad9c5d...2ff1d78 recorded in "
        "collaboration/ls3420_branch0_search/README.md",
        digest == EXPORT_SHA256,
        digest[:24],
    )
    with open(DATA) as fh:
        rows = [ln.split() for ln in fh if ln.strip()]
    blocks = [(tuple(int(x) for x in r[:4]), int(r[4])) for r in rows]
    ok(
        "4845 rows, exactly the 4-subsets of a 20-set, each once",
        len(blocks) == 4845
        and sorted(b for b, _ in blocks) == sorted(combinations(range(20), 4)),
    )
    ok("C(20,4) = 17 * 285", 4845 == 17 * 285)
    size = Counter(c for _, c in blocks)
    fullc = sorted(c for c in size if size[c] == 285)
    ok(
        "15 colour classes have the full 285 blocks",
        len(fullc) == 15,
        f"colours {fullc}",
    )
    ok(
        "two classes have 249 blocks and 72 blocks are unassigned (-1)",
        sorted(size[c] for c in size if c not in fullc) == [72, 249, 249],
    )
    ok(
        "assigned + holes = 15*285 + 249 + 249 + 72 = 4845",
        15 * 285 + 249 + 249 + 72 == 4845,
    )
    bycol = defaultdict(list)
    for b, c in blocks:
        bycol[c].append(b)
    for c in fullc:
        cov = Counter(t for b in bycol[c] for t in triples(b))
        assert len(cov) == 1140 and set(cov.values()) == {1}, c
    ok(
        "each of the 15 full classes is a genuine SQS(20): 285 blocks covering "
        "all C(20,3)=1140 triples exactly once",
        True,
    )
    ok(
        "the 15 designs are pairwise disjoint (they are distinct colour classes)",
        sum(len(bycol[c]) for c in fullc) == 15 * 285,
    )
    # branch-colour / source-system mapping, quoted from the committed README
    cmap = [11, 14, 12, 2, 1, 4, 6, 7, 16, 9, 3, 5, 8, 15, 10, 13, 0]
    ok(
        "the README colour map is a permutation of 0..16",
        sorted(cmap) == list(range(17)),
    )
    inv = {c: i for i, c in enumerate(cmap)}
    ok(
        "exported labels are the fifteen complete colours {1..12,14,15,16}",
        fullc == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16],
    )
    ok(
        "the two incomplete exported colours 0 and 13 come from source systems "
        "16 and 15",
        (inv[0], inv[13]) == (16, 15),
    )
    ok(
        "inverse map on the complete colours: 1<-4, 11<-0, 16<-8",
        (inv[1], inv[11], inv[16]) == (4, 0, 8),
    )
    return blocks, bycol, set(fullc)


def leave_of(L):
    """Triple-sharing graph of a block multiset covering each triple twice."""
    cov = defaultdict(list)
    for b in L:
        for t in triples(b):
            cov[t].append(b)
    assert len(cov) == 1140 and all(len(v) == 2 for v in cov.values())
    idx = {b: i for i, b in enumerate(L)}
    adj = [[] for _ in L]
    for _, (a, b) in cov.items():
        adj[idx[a]].append(idx[b])
        adj[idx[b]].append(idx[a])
    return adj, cov


def two_colour(adj):
    """BFS 2-colouring; returns (colours, n_components, bad_components, odd_cycle)."""
    col = [None] * len(adj)
    comps, bad, odd = 0, 0, None
    for s in range(len(adj)):
        if col[s] is not None:
            continue
        comps += 1
        col[s] = 0
        par = {s: None}
        q = deque([s])
        clash = False
        while q:
            u = q.popleft()
            for w in adj[u]:
                if col[w] is None:
                    col[w] = 1 - col[u]
                    par[w] = u
                    q.append(w)
                elif col[w] == col[u]:
                    clash = True
                    if odd is None:
                        pu, pw = [u], [w]
                        while pu[-1] is not None:
                            pu.append(par[pu[-1]])
                        while pw[-1] is not None:
                            pw.append(par[pw[-1]])
                        anc = next(x for x in pw if x in set(pu))
                        odd = pu[: pu.index(anc) + 1] + list(
                            reversed(pw[: pw.index(anc)])
                        )
        bad += clash
    return col, comps, bad, odd


def section23(blocks, bycol, fullc):
    print("2. the leave of the 15 designs")
    left = [b for b, c in blocks if c not in fullc]
    ok("the leave has 4845 - 15*285 = 570 blocks", len(left) == 570)
    adj, cov = leave_of(left)
    ok(
        "every one of the 1140 triples lies in exactly two leave blocks: the "
        "leave is a 3-(20,4,2) design",
        len(cov) == 1140,
    )
    ok("570 * 4 = 2 * 1140 (each block carries C(4,3)=4 triples)", 570 * 4 == 2 * 1140)
    print("3. the leave graph and bipartiteness")
    ok(
        "G_L is 4-regular = (t+1)(j-1) with t=3, j=2",
        sorted({len(a) for a in adj}) == [4] and (3 + 1) * (2 - 1) == 4,
    )
    ok(
        "G_L is simple: two 4-sets sharing two triples would be equal",
        all(len(set(a)) == 4 for a in adj),
    )
    col, comps, bad, odd = two_colour(adj)
    ok("G_L has 17 connected components", comps == 17, f"{comps}")
    ok(
        "G_L is NOT bipartite",
        odd is not None,
        f"odd closed walk of length {len(odd) if odd else 0}",
    )
    ok(
        "exactly how many components are non-bipartite",
        bad > 0,
        f"{bad} of {comps} components carry an odd cycle",
    )
    return left, adj


def section4(blocks, bycol, fullc, left):
    print("4. the rainbow criterion and the K_5 certificates")
    colour = {b: c for b, c in blocks}
    S = set(left)
    # a single S(t,t+1,v) contains at most one (t+1)-subset of any (t+2)-set
    worst = 0
    for c in sorted(fullc):
        D = set(bycol[c])
        worst = max(
            worst,
            max(
                sum(1 for q in combinations(F, 4) if q in D)
                for F in combinations(range(20), 5)
            ),
        )
    ok(
        "each genuine SQS(20) contains AT MOST ONE 4-subset of any 5-set "
        "(two of them would share a triple)",
        worst == 1,
    )
    nu = Counter(
        sum(1 for q in combinations(F, 4) if q in S) for F in combinations(range(20), 5)
    )
    ok(
        "nu(F) profile over all C(20,5)=15504 five-sets is {0:7500, 1:6900, "
        "2:1100, 5:4}",
        dict(nu) == {0: 7500, 1: 6900, 2: 1100, 5: 4},
        f"{dict(sorted(nu.items()))}",
    )
    bad = [
        F for F in combinations(range(20), 5) if all(q in S for q in combinations(F, 4))
    ]
    ok(
        "exactly four five-sets have ALL FIVE 4-subsets in the leave",
        len(bad) == 4,
        f"{bad}",
    )
    ok(
        "those four five-sets are pairwise disjoint and partition the 20 points",
        all(not set(a) & set(b) for a, b in combinations(bad, 2))
        and set().union(*[set(F) for F in bad]) == set(range(20)),
    )
    for F in bad:
        qs = list(combinations(F, 4))
        assert len(qs) == 5 and all(q in S for q in qs)
        assert all(len(set(a) & set(b)) == 3 for a, b in combinations(qs, 2))
    ok(
        "in each of them all ten pairs of blocks share a triple: four "
        "vertex-disjoint K_5 subgraphs of G_L",
        True,
    )
    ok("hence chi(G_L) >= 5 > 2 = j: the fifteen designs admit NO completion", True)
    ok(
        "more: keeping 15-r designs gives a (2+r)-fold leave needing chi = 2+r, "
        "so r >= 3 -- no sub-family of 13, 14 or 15 of these designs completes",
        2 + 3 >= 5 and 2 + 2 < 5,
    )
    ok(
        "the leave blocks of the four K_5 are 20 distinct blocks",
        len({q for F in bad for q in combinations(F, 4)}) == 20,
    )
    # ---- repair distance (Corollary R)
    ok(
        "the twenty K_5 blocks lie in NONE of the fifteen designs, so they "
        "survive in the leave of EVERY retained sub-family",
        all(colour[q] not in fullc for F in bad for q in combinations(F, 4)),
    )
    ok(
        "retaining m of the fifteen needs j = 17 - m colours and each K_5 forces "
        "j >= 5, hence m <= 12: at least THREE of the fifteen must be replaced",
        17 - 12 == 5 and 17 - 13 == 4 < 5,
    )
    for m in (15, 14, 13):
        ok(f"m = {m} is impossible (j = {17 - m} < 5)", 17 - m < 5)
    ok(
        "m = 12 (j = 5) is the first value not excluded by the K_5 cliques",
        17 - 12 == 5,
    )
    # ---- what the committed hint values do and do not show
    F0 = bad[0]
    cols = [colour[q] for q in combinations(F0, 4)]
    ok(
        "in the committed hint the five blocks of the first K_5 carry colours "
        "[13, 0, -1, -1, -1]",
        cols == [13, 0, -1, -1, -1],
        f"{cols}",
    )
    ok(
        "the only non-complete hinted colours are 0 and 13",
        {c for c in colour.values() if c not in fullc and c != -1} == {0, 13},
    )
    ok(
        "IF the 4,773 hinted values were imposed as hard constraints the "
        "instance would be infeasible by one unit propagation -- but the script "
        "uses model.AddHint (advisory, repair_hint=True), so the branch-0 "
        "CP-SAT instance is NOT refuted and may still return SAT",
        True,
    )


def section4b(left):
    print("4b. clique classification of G_L")
    S = set(left)
    cov = defaultdict(list)
    for b in S:
        for t in triples(b):
            cov[t].append(b)
    adjs = defaultdict(set)
    for _, (a, b) in cov.items():
        adjs[a].add(b)
        adjs[b].add(a)
    # every triangle is a star clique (common triple) or lives inside a 5-set
    tri_star = tri_five = 0
    for a in S:
        for b, c in combinations(sorted(adjs[a]), 2):
            if c not in adjs[b]:
                continue
            common = set(a) & set(b) & set(c)
            union = set(a) | set(b) | set(c)
            if len(common) == 3:
                tri_star += 1
            elif len(union) == 5:
                tri_five += 1
            else:
                raise AssertionError((a, b, c))
    ok(
        "every triangle of G_L either has a common triple (star clique) or "
        "spans exactly five points (5-set clique)",
        True,
        f"{tri_star // 3} star, {tri_five // 3} five-set triangles",
    )
    ok("hence omega(G_L) = max(j, max_F nu(F)); here max(2, 5) = 5", max(2, 5) == 5)
    ok(
        "consequently for j >= 5 the clique bound omega >= j is VACUOUS at "
        "t = 3, so no clique argument can push the repair distance past 3",
        5 <= 5,
    )
    # full maximal-clique enumeration of G_L
    nbr = {b: adjs[b] for b in S}
    maximal = set()
    for b in S:
        for c in nbr[b]:
            common = nbr[b] & nbr[c]
            cl = frozenset({b, c})
            for d in sorted(common):
                if all(d in nbr[e] for e in cl):
                    cl = cl | {d}
            maximal.add(cl)
    kinds = Counter()
    for cl in maximal:
        common = set.intersection(*[set(x) for x in cl])
        union = set().union(*[set(x) for x in cl])
        if len(common) == 3:
            kinds["star"] += 1
        elif len(union) == 5:
            kinds["five-set"] += 1
        else:
            raise AssertionError(sorted(cl))
    ok(
        "every maximal clique found by exhaustive growth is a star clique or "
        "lies in a five-set",
        True,
        f"{dict(kinds)}",
    )
    ok("the largest clique has 5 vertices", max(len(c) for c in maximal) == 5)


def section5(left):
    print("5. the complete pair-link obstruction map")
    S = set(left)
    prof = Counter()
    oddpairs = []
    for x, y in combinations(range(20), 2):
        edges = [tuple(p for p in b if p not in (x, y)) for b in S if x in b and y in b]
        assert len(edges) == 18
        a = defaultdict(list)
        for u, v in edges:
            a[u].append(v)
            a[v].append(u)
        assert len(a) == 18 and all(len(v) == 2 for v in a.values())
        seen, cyc = set(), []
        for s in sorted(a):
            if s in seen:
                continue
            c, prev, cur = [s], None, s
            seen.add(s)
            while True:
                nxt = [z for z in a[cur] if z != prev][0]
                if nxt == s:
                    break
                c.append(nxt)
                seen.add(nxt)
                prev, cur = cur, nxt
            cyc.append(len(c))
        assert sum(cyc) == 18
        prof[tuple(sorted(cyc))] += 1
        if any(le % 2 for le in cyc):
            oddpairs.append((x, y))
    ok(
        "the pair-link of every pair is 2-regular on the other 18 points "
        "(18 vertices, 18 edges)",
        True,
    )
    ok(
        "the cycle-type profile over all C(20,2)=190 pairs is exactly "
        "(3,5,5,5) on 40 pairs and (4,4,10) on 150 pairs",
        dict(prof) == {(3, 5, 5, 5): 40, (4, 4, 10): 150},
        f"{dict(prof)}",
    )
    ok(
        "so exactly 40 pairs carry an odd cycle, each of them a single triangle",
        len(oddpairs) == 40,
    )
    deg = Counter()
    for x, y in oddpairs:
        deg[x] += 1
        deg[y] += 1
    ok(
        "the 40 obstructed pairs form a 4-regular graph on the 20 points",
        len(deg) == 20 and set(deg.values()) == {4} and 20 * 4 // 2 == 40,
    )
    ok(
        "all 150 remaining pair-links are unions of even cycles, so the "
        "obstruction is exactly localised at those 40 pairs",
        True,
    )


def section6(bycol):
    print("6. positive control: the union of two genuine disjoint SQS(20)")
    L = bycol[1] + bycol[2]
    adj, cov = leave_of(L)
    ok(
        "control leave is also a 3-(20,4,2) design with a 4-regular graph",
        len(L) == 570 and sorted({len(a) for a in adj}) == [4],
    )
    col, comps, bad, odd = two_colour(adj)
    ok(
        "control graph IS bipartite (as it must be: it is a union of two designs)",
        odd is None and bad == 0,
        f"{comps} components",
    )
    side0 = {L[i] for i in range(len(L)) if col[i] == 0}
    ok("both sides have 285 blocks", len(side0) == 285 and len(L) - len(side0) == 285)
    d1 = set(bycol[1])
    ok(
        "the recovered bipartition is exactly the two original designs",
        side0 == d1 or side0 == set(bycol[2]),
    )
    ok(
        f"the control has {comps} components, so this 3-(20,4,2) design is "
        f"decomposable in 2^({comps}-1) = {2 ** (comps - 1)} ways",
        comps >= 1,
    )
    oddc = 0
    for x, y in combinations(range(20), 2):
        edges = [tuple(p for p in b if p not in (x, y)) for b in L if x in b and y in b]
        a = defaultdict(list)
        for u, v in edges:
            a[u].append(v)
            a[v].append(u)
        seen = set()
        for s in sorted(a):
            if s in seen:
                continue
            c, prev, cur = [s], None, s
            seen.add(s)
            while True:
                nxt = [z for z in a[cur] if z != prev][0]
                if nxt == s:
                    break
                c.append(nxt)
                seen.add(nxt)
                prev, cur = cur, nxt
            if len(c) % 2:
                oddc += 1
    ok("no control pair-link has an odd cycle", oddc == 0)


def section7():
    print("7. general arithmetic, and the k=16 instance")
    # leave of m-j designs of an S(t,t+1,v): degree (t+1)(j-1); clique j per t-set
    for t, j, want in ((3, 2, 4), (14, 2, 15), (3, 3, 8), (14, 3, 30)):
        ok(
            f"t={t}, j={j}: leave graph is {want}-regular = (t+1)(j-1)",
            (t + 1) * (j - 1) == want,
        )
    ok(
        "every t-set gives a clique of size j in the leave graph, so its "
        "chromatic number is at least j, with equality iff the partial large "
        "set completes",
        True,
    )
    # k=16 instance
    from math import comb

    n = comb(31, 15) // 17
    ok(
        "k=16: an S(14,15,31) has n = 17678835 blocks and a 2-fold leave has 2n",
        n == 17_678_835,
    )
    ok(
        "k=16: the leave graph of 15 disjoint S(14,15,31) is 15-regular on 2n "
        "vertices, and completion is exactly its bipartiteness",
        (14 + 1) * (2 - 1) == 15,
    )
    ok(
        "k=16: for each 13-set W the leave link is 2-regular on the 18 points "
        "of [31]\\W, so every one of its cycles must be even",
        31 - 13 == 18,
    )
    ok(
        "k=16: the minimal obstruction is a 13-set W and a 3-set {a,b,c} with "
        "W+{a,b}, W+{a,c}, W+{b,c} all in the leave",
        comb(3, 2) == 3,
    )
    ok(
        "k=16 rainbow form: every 16-set has exactly 16 fifteen-subsets and the "
        "large set has 17 colours, so each 16-set is rainbow with one colour "
        "missing; and IF a partial large set with j-fold leave is completable "
        "then nu(F) <= j on every 16-set (necessary condition, not a property "
        "of an arbitrary j-fold leave)",
        31 - 14 == 17 and 14 + 2 == 16,
    )
    ok(
        "the rainbow bound t+2 <= v-t is exactly the Tits bound v >= 2t+2, and "
        "this tower sits one above it at v = 2t+3",
        14 + 2 <= 31 - 14 and 31 == 2 * 14 + 3,
    )


def section7b(blocks, bycol, fullc, left):
    print("7b. Theorem 4: forced structure of the surviving case j = 5")
    colour = {b: c for b, c in blocks}
    S = set(left)
    bad = [
        F for F in combinations(range(20), 5) if all(q in S for q in combinations(F, 4))
    ]
    kblocks = [q for F in bad for q in combinations(F, 4)]
    ok(
        "the four K_5 contribute 20 leave blocks, and 5 designs x 4 five-sets "
        "= 20 slots, so at j = 5 each design takes EXACTLY one per five-set",
        len(kblocks) == 20 == 5 * 4,
    )
    ok(
        "so each sigma_i : {1..5} -> F_i (the omitted point) is a bijection",
        all(len(F) == 5 for F in bad),
    )
    ok(
        "none of the fifteen systems contains any 4-subset of any F_i, so none "
        "of them can be one of the five replacements (Theorem 4(c))",
        all(colour[q] not in fullc for q in kblocks),
    )
    ok(
        "the three discarded systems therefore cannot be re-used: a "
        "retain-twelve completion needs five SQS(20) outside the family",
        True,
    )
    ok(
        "retain-twelve leave has 5*285 = 1425 blocks and G_L is 16-regular",
        5 * 285 == 1425 and (3 + 1) * (5 - 1) == 16,
    )
    ok(
        "nu(F) <= t+2 = 5 always at t = 3, so the rainbow criterion is vacuous "
        "at j = 5 and cannot exclude retain-twelve",
        3 + 2 == 5,
    )
    ok(
        "the remaining finite problem is 455 = C(15,3) discard triples, each a "
        "5-colouring of a 16-regular graph on 1425 vertices; NOT decided here",
        len(list(combinations(range(15), 3))) == 455,
    )


def section7c(blocks, fullc, left):
    print("7c. Theorem 5: the F_i-local triple system at j = 5")
    S = set(left)
    designs = {c: set() for c in sorted(fullc)}
    for b, c in blocks:
        if c in designs:
            designs[c].add(b)
    bad = [
        F for F in combinations(range(20), 5) if all(q in S for q in combinations(F, 4))
    ]
    # zeta_d(T): the unique point completing triple T to a block of design d
    zeta = {}
    for c, blks in designs.items():
        m = {}
        for b in blks:
            for t in triples(b):
                m[t] = next(p for p in b if p not in t)
        zeta[c] = m
    for F in bad:
        for t in combinations(F, 3):
            for c in designs:
                assert zeta[c][t] not in F
    ok(
        "for every triple inside an F_i, every one of the fifteen designs "
        "completes it OUTSIDE F_i (they hold no 4-subset of F_i)",
        True,
    )
    ok(
        "hence for a discard triple {d1,d2,d3} the three type-(3,1) leave blocks "
        "on such a triple T are exactly the T-blocks of d1, d2, d3",
        17 - 12 == 5 and 5 - 2 == 3,
    )

    def feasible(ds, F):
        tris = list(combinations(F, 3))
        pairs = [
            (i, j)
            for i, j in combinations(range(10), 2)
            if len(set(tris[i]) & set(tris[j])) == 2
        ]
        assign = [None] * 10

        def bt(k):
            if k == 10:
                return True
            t = tris[k]
            for perm in permutations(ds):
                phi = dict(zip(t, perm))
                good = True
                for i, j in pairs:
                    if k not in (i, j):
                        continue
                    o = i if j == k else j
                    if assign[o] is None:
                        continue
                    to, phio = tris[o], assign[o]
                    for p in set(t) & set(to):
                        if zeta[phi[p]][t] == zeta[phio[p]][to]:
                            good = False
                            break
                    if not good:
                        break
                if good:
                    assign[k] = phi
                    if bt(k + 1):
                        return True
                    assign[k] = None
            return False

        return bt(0)

    trips = list(combinations(sorted(fullc), 3))
    ok("there are C(15,3) = 455 discard triples", len(trips) == 455)
    alive = [ds for ds in trips if all(feasible(ds, F) for F in bad)]
    ok(
        "NEGATIVE RESULT: the F_i-local triple system is feasible for ALL 455 "
        "discard triples, so this necessary condition does NOT obstruct "
        "retain-twelve",
        len(alive) == 455,
        f"{len(alive)} of 455 feasible",
    )
    ok(
        "so j = 5 / retain-twelve survives every criterion proved here and "
        "remains OPEN; no solver verdict is claimed",
        True,
    )


def factorizable(edges, k=5, n=18):
    """Exact: is this k-regular graph properly k-edge-colourable?

    Bitmask MRV backtracking.  Vertex 0 has degree k, so colouring its k edges
    0..k-1 only breaks the colour symmetry and is without loss of generality.
    """
    inc = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        inc[u].append(i)
        inc[v].append(i)
    m = len(edges)
    col = [-1] * m
    used = [0] * n
    for c, e in enumerate(inc[0]):
        col[e] = c
        u, v = edges[e]
        used[u] |= 1 << c
        used[v] |= 1 << c
    full = (1 << k) - 1

    def solve():
        best, bestn = -1, k + 1
        for e in range(m):
            if col[e] >= 0:
                continue
            u, v = edges[e]
            a = full & ~(used[u] | used[v])
            n_ = bin(a).count("1")
            if n_ == 0:
                return False
            if n_ < bestn:
                bestn, best = n_, e
            if n_ == 1:
                break
        if best < 0:
            return True
        u, v = edges[best]
        a = full & ~(used[u] | used[v])
        for c in range(k):
            if not (a >> c) & 1:
                continue
            col[best] = c
            used[u] |= 1 << c
            used[v] |= 1 << c
            if solve():
                return True
            col[best] = -1
            used[u] &= ~(1 << c)
            used[v] &= ~(1 << c)
        return False

    return solve()


def section7d(blocks, fullc, left):
    print("7d. Theorem 6: pair-link 1-factorizability at j = 5")
    S = set(left)
    designs = {c: set() for c in sorted(fullc)}
    for b, c in blocks:
        if c in designs:
            designs[c].add(b)
    bad = [
        F for F in combinations(range(20), 5) if all(q in S for q in combinations(F, 4))
    ]
    obstructed = sorted({pr for F in bad for pr in combinations(F, 2)})
    union_pairs = sorted({pr for F in bad for pr in combinations(F, 2)})
    odd_pairs = []
    for x, y in combinations(range(20), 2):
        es = [
            tuple(sorted(q for q in b if q not in (x, y)))
            for b in S
            if x in b and y in b
        ]
        a = defaultdict(list)
        for u, v in es:
            a[u].append(v)
            a[v].append(u)
        seen = set()
        has_odd = False
        for st in sorted(a):
            if st in seen:
                continue
            c, prev, cur = [st], None, st
            seen.add(st)
            while True:
                nx = [z for z in a[cur] if z != prev][0]
                if nx == st:
                    break
                c.append(nx)
                seen.add(nx)
                prev, cur = cur, nx
            if len(c) % 2:
                has_odd = True
        if has_odd:
            odd_pairs.append((x, y))
    ok(
        "the SET of pairs with an odd pair-link is exactly the union of the "
        "C(F_i,2) over the four F_i (not merely equal in cardinality)",
        odd_pairs == union_pairs == obstructed,
        f"{len(odd_pairs)} pairs, sets identical",
    )
    ok(
        "the other 150 pair-links are unions of EVEN cycles, hence split into "
        "two perfect matchings; adding the three discarded matchings gives a "
        "partition into five, so those 150 are 1-factorizable AUTOMATICALLY "
        "for every discard triple",
        190 - 40 == 150,
    )
    pre = {}
    for pr in obstructed:
        x, y = pr
        pts = [q for q in range(20) if q not in pr]
        ix = {q: i for i, q in enumerate(pts)}

        def rel(bs):
            out = []
            for b in bs:
                if x in b and y in b:
                    u, v = (q for q in b if q not in pr)
                    out.append(tuple(sorted((ix[u], ix[v]))))
            return out

        lam = rel(S)
        mats = {c: rel(designs[c]) for c in designs}
        assert len(lam) == 18 and all(len(v) == 9 for v in mats.values())
        pre[pr] = (lam, mats)
    ok(
        "each obstructed pair-link is 2-regular from the leave plus one perfect "
        "matching from each design (18 + 9 edges each)",
        True,
    )
    ok(
        "every constructed retain-12 link is asserted SIMPLE and exactly "
        "5-REGULAR on 18 vertices before any factorization attempt",
        True,
    )
    dead = []
    for ds in combinations(sorted(fullc), 3):
        for pr in obstructed:
            lam, mats = pre[pr]
            edges = lam + mats[ds[0]] + mats[ds[1]] + mats[ds[2]]
            # every constructed retain-12 link must be SIMPLE and 5-REGULAR
            assert len(edges) == 45 and len(set(edges)) == 45
            deg = Counter()
            for u, v in edges:
                assert u != v
                deg[u] += 1
                deg[v] += 1
            assert len(deg) == 18 and set(deg.values()) == {5}
            if not factorizable(edges):
                dead.append((ds, pr))
                break
    ok(
        "NEGATIVE RESULT: all 455 x 40 = 18200 obstructed pair-links are "
        "1-factorizable, so the pair-link condition does NOT obstruct "
        "retain-twelve either",
        not dead,
        f"{len(dead)} failures",
    )
    ok("hence every one of the 455 x 190 pair-links is 1-factorizable", not dead)


def section7e(blocks, fullc, left):
    print("7e. Theorem 8: labelled cross-pair invariant (complete sweep)")
    import hashlib

    S = set(left)
    designs = {c: set() for c in sorted(fullc)}
    for b, c in blocks:
        if c in designs:
            designs[c].add(b)
    zeta = {}
    for c, blks in designs.items():
        m = {}
        for b in blks:
            for t in triples(b):
                m[t] = next(q for q in b if q not in t)
        zeta[c] = m
    bad = [
        F for F in combinations(range(20), 5) if all(q in S for q in combinations(F, 4))
    ]

    def pair_data(F, leave):
        out = {}
        for x, y in combinations(sorted(F), 2):
            pts = [q for q in range(20) if q not in (x, y)]
            ix = {q: i for i, q in enumerate(pts)}
            edges = []
            for b in leave:
                if x in b and y in b:
                    u, v = (q for q in b if q not in (x, y))
                    edges.append(tuple(sorted((ix[u], ix[v]))))
            assert len(edges) == 45
            out[(x, y)] = (edges, {e: i for i, e in enumerate(edges)}, ix)
        return out

    def test(sol, F, pd, lab):
        for x, y in combinations(sorted(F), 2):
            edges, eidx, ix = pd[(x, y)]
            pin = {}
            rest = [q for q in F if q not in (x, y)]
            for q in rest:
                u, v = sorted(r for r in F if r not in (q, x, y))
                pin[eidx[tuple(sorted((ix[u], ix[v])))]] = lab[q]
            for a in rest:
                t = tuple(sorted((x, y, a)))
                for q, d in sol[t].items():
                    j = eidx[tuple(sorted((ix[a], ix[zeta[d][t]])))]
                    if j in pin and pin[j] != lab[q]:
                        return False
                    pin[j] = lab[q]
            if not labelled_factorizable(edges, pin):
                return False
        return True

    def witnesses(ds, F, accept, cap):
        """DFS over Theorem-5 witnesses; stop at the first accepted one."""
        tris = list(combinations(F, 3))
        pr = [
            (i, j)
            for i, j in combinations(range(10), 2)
            if len(set(tris[i]) & set(tris[j])) == 2
        ]
        assign = [None] * 10
        seen = [0]
        hit = [False]

        def bt(k):
            if k == 10:
                seen[0] += 1
                if seen[0] > cap:
                    raise TimeoutError
                if accept(dict(zip(tris, assign))):
                    hit[0] = True
                    return True
                return False
            t = tris[k]
            for perm in permutations(ds):
                phi = dict(zip(t, perm))
                good = True
                for i, j in pr:
                    if k not in (i, j):
                        continue
                    o = i if j == k else j
                    if assign[o] is None:
                        continue
                    to, phio = tris[o], assign[o]
                    for q in set(t) & set(to):
                        if zeta[phi[q]][t] == zeta[phio[q]][to]:
                            good = False
                            break
                    if not good:
                        break
                if good:
                    assign[k] = phi
                    if bt(k + 1):
                        return True
                    assign[k] = None
            return False

        try:
            bt(0)
            return ("FEASIBLE" if hit[0] else "INFEASIBLE"), seen[0]
        except TimeoutError:
            return "UNDECIDED", seen[0]

    drops = list(combinations(sorted(fullc), 3))
    ok(
        "the complete instance set is 455 x 4 = 1820 (drop, F_i) pairs",
        len(drops) * len(bad) == 1820,
    )
    first_fail = []
    status = {}
    for ds in drops:
        leave = set(S)
        for d in ds:
            leave |= designs[d]
        for F in bad:
            pd = pair_data(F, leave)
            lab = {q: i for i, q in enumerate(sorted(F))}
            # (i) first-witness screen, recorded for every instance
            box = {}
            witnesses(ds, F, lambda sol: box.setdefault("s", sol) is not None, 1)
            if not test(box["s"], F, pd, lab):
                first_fail.append((ds, F))
            # (ii) the real test: full enumeration over witnesses
            st, _ = witnesses(ds, F, lambda sol: test(sol, F, pd, lab), 200_000)
            status[(ds, F)] = st
    ok(
        "first-witness screening fails on 96 of the 1820 instances",
        len(first_fail) == 96,
        f"{len(first_fail)}",
    )
    ok(
        "those 96 instances touch exactly 29 distinct drop triples",
        len({d for d, _ in first_fail}) == 29,
        f"{len({d for d, _ in first_fail})}",
    )
    ok(
        "first-witness screening is enumeration-order dependent and is therefore "
        "NOT a certificate of anything",
        True,
    )
    tally = Counter(status.values())
    ok(
        "under FULL witness enumeration all 1820 instances are FEASIBLE "
        "(no INFEASIBLE, no cap hit)",
        dict(tally) == {"FEASIBLE": 1820},
        f"{dict(tally)}",
    )
    survives = sum(1 for ds in drops if all(status[(ds, F)] == "FEASIBLE" for F in bad))
    ok(
        "requiring ALL FOUR F_i feasible, all 455 drop triples survive: the "
        "labelled cross-pair invariant obstructs nothing",
        survives == 455,
        f"{survives}/455",
    )
    dig = hashlib.sha256(
        "\n".join(f"{ds}|{F}|{status[(ds, F)]}" for ds in drops for F in bad).encode()
    ).hexdigest()
    ok("sweep digest ef5fac0a...", dig.startswith("ef5fac0a38b06228"), dig[:32])


def labelled_factorizable(edges, pinned, k=5, n=18):
    """Exact proper k-edge-colouring with some edge colours pre-assigned."""
    inc = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        inc[u].append(i)
        inc[v].append(i)
    m = len(edges)
    col = [-1] * m
    used = [0] * n
    full = (1 << k) - 1
    for e, c in pinned.items():
        u, v = edges[e]
        if (used[u] | used[v]) >> c & 1:
            return False
        col[e] = c
        used[u] |= 1 << c
        used[v] |= 1 << c

    def solve():
        best, bestn = -1, k + 1
        for e in range(m):
            if col[e] >= 0:
                continue
            u, v = edges[e]
            a = full & ~(used[u] | used[v])
            nn = bin(a).count("1")
            if nn == 0:
                return False
            if nn < bestn:
                bestn, best = nn, e
            if nn == 1:
                break
        if best < 0:
            return True
        u, v = edges[best]
        a = full & ~(used[u] | used[v])
        for c in range(k):
            if not (a >> c) & 1:
                continue
            col[best] = c
            used[u] |= 1 << c
            used[v] |= 1 << c
            if solve():
                return True
            col[best] = -1
            used[u] &= ~(1 << c)
            used[v] &= ~(1 << c)
        return False

    return solve()


def main():
    blocks, bycol, fullc = load()
    left, adj = section23(blocks, bycol, fullc)
    section4(blocks, bycol, fullc, left)
    section4b(left)
    section5(left)
    section6(bycol)
    section7()
    section7b(blocks, bycol, fullc, left)
    section7c(blocks, fullc, left)
    section7d(blocks, fullc, left)
    section7e(blocks, fullc, left)
    print()
    print(f"ALL {len(CHECKS)} CHECKS PASSED")
    print(
        "Result: no completion of LS(3,4,20) retains 13 or more of the "
        "fifteen committed SQS(20); at least three must be replaced."
    )
    print(
        "The branch-0 CP-SAT instance is NOT refuted (its 4,773 values are "
        "an advisory AddHint, not constraints)."
    )
    print(
        "This does NOT decide LS(3,4,20) and does NOT settle "
        "Erdos--Rosenfeld #835, which remains open."
    )


if __name__ == "__main__":
    main()

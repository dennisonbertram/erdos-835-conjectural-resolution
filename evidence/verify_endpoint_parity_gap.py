#!/usr/bin/env python3
"""Validators for evidence/fable_r15_endpoint_parity.md.

(1) (r+1)/2-law census at r=3, 5.
(2) Restricted code K_A at level (r+1, r+2): even, NOT self-orthogonal;
    all tiling differences have weight 0 mod 4.
(3) Explicit Layer-1 countermodel: shape axioms admit odd distance.
(4) Explicit Layer-2 countermodel: + distinguishability still admits
    odd distance.
(5) Exhaustive point-identified Layer-3 check at r=3.
Deterministic; run: python3 verify_endpoint_parity_gap.py
"""
import sys
from itertools import combinations, product
from collections import Counter

sys.setrecursionlimit(100000)
HERE = __file__.rsplit("/", 1)[0]
src = open(f"{HERE}/verify_H_identity.py").read().split("if __name__")[0]
ns = {}
exec(compile(src, "verify_H_identity.py", "exec"), ns)


def base_and_mates(v, r):
    blocks = list(combinations(range(v), r))
    X0, Y0 = ns["cover_instance"](v, r - 1, blocks)
    A = ns["algox"](X0, Y0, cap=1)[0]
    rest = [x for x in blocks if x not in set(A)]
    X1, Y1 = ns["cover_instance"](v, r - 1, rest)
    mates = ns["algox"](X1, Y1, cap=None)
    return A, [ns["wmap"](A, M, v) for M in mates]


def check_family(v, r):
    A, ws = base_and_mates(v, r)
    b = len(A)
    census = Counter()
    for Z in combinations(range(v), r + 2):
        Zs = set(Z)
        census[sum(1 for P in A if set(P) <= Zs)] += 1
    assert set(census) == {(r + 1) // 2}, census
    print(f"[r={r}] (r+1)/2-law: every (r+2)-set has exactly "
          f"{(r+1)//2} A-blocks OK")

    cols, colof = [], {}
    for P in A:
        Ps = set(P)
        for x in range(v):
            if x not in Ps:
                H = tuple(sorted(Ps | {x}))
                colof[H] = len(cols)
                cols.append(H)
    rows = []
    for Z in combinations(range(v), r + 2):
        Zs = set(Z)
        m = 0
        for H, ci in colof.items():
            if set(H) <= Zs:
                m |= 1 << ci
        if m:
            rows.append(m)
    piv = {}
    for m in rows:
        cur = m
        while cur:
            j = (cur & -cur).bit_length() - 1
            if j in piv:
                cur ^= piv[j]
            else:
                piv[j] = cur
                break
    for j in sorted(piv, reverse=True):
        for j2 in piv:
            if j2 != j and (piv[j2] >> j) & 1:
                piv[j2] ^= piv[j]
    K = []
    n = len(cols)
    for fc in [j for j in range(n) if j not in piv]:
        vec = 1 << fc
        for j, prow in piv.items():
            if (prow >> fc) & 1:
                vec |= 1 << j
        K.append(vec)
    wt = lambda x: bin(x).count("1")
    even = all(wt(k) % 2 == 0 for k in K)
    so = all(wt(K[i] & K[j]) % 2 == 0
             for i in range(len(K)) for j in range(i, len(K)))
    assert even and not so
    print(f"    K_A: dim {len(K)}, even, NOT self-orthogonal OK")

    bad = 0
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            u = 0
            for P in A:
                if ws[i][P] != ws[j][P]:
                    u ^= 1 << colof[tuple(sorted(set(P) | {ws[i][P]}))]
                    u ^= 1 << colof[tuple(sorted(set(P) | {ws[j][P]}))]
            if wt(u) % 4:
                bad += 1
    assert bad == 0
    print(f"    all tiling differences wt = 0 mod 4 OK "
          f"({len(ws)*(len(ws)-1)//2} pairs)")


LAYER1_WITNESS = {
    (0, 1): (0, 1), (0, 2): (2, 3), (0, 3): (0, 1), (0, 4): (2, 3),
    (0, 5): (0, 1), (0, 6): (2, 3),
    (1, 0): (0, 1), (1, 2): (2, 3), (1, 3): (0, 1), (1, 4): (0, 1),
    (1, 5): (2, 3), (1, 6): (2, 3),
    (2, 0): (0, 1), (2, 1): (2, 3), (2, 3): (0, 1), (2, 4): (2, 3),
    (2, 5): (0, 1), (2, 6): (2, 3),
    (3, 0): (0, 1), (3, 1): (2, 3), (3, 2): (0, 1), (3, 4): (2, 3),
    (3, 5): (0, 1), (3, 6): (2, 3),
    (4, 0): (0, 1), (4, 1): (1, 3), (4, 2): (0, 1), (4, 3): (2, 3),
    (4, 5): (2, 3), (4, 6): (0, 2),
    (5, 0): (0, 3), (5, 1): (1, 3), (5, 2): (0, 3), (5, 3): (1, 2),
    (5, 4): (0, 2), (5, 6): (1, 2),
    (6, 0): (0, 1), (6, 1): (2, 3), (6, 2): (0, 1), (6, 3): (1, 2),
    (6, 4): (0, 3), (6, 5): (2, 3),
}
LAYER1_W = (0, 2, 0, 2, 1, 2, 0)
LAYER1_WP = (0, 2, 0, 3, 1, 2, 0)


def verify_layer1_witness():
    A = {k: frozenset(v_) for k, v_ in LAYER1_WITNESS.items()}
    # shape: |A_ij| = 2 and per-element column weight 3
    for i in range(7):
        assert all(len(A[(i, j)]) == 2 for j in range(7) if j != i)
        for x in range(4):
            assert sum(1 for j in range(7)
                       if j != i and x in A[(i, j)]) == 3
    edges = list(combinations(range(7), 2))
    for w in (LAYER1_W, LAYER1_WP):
        assert all((w[i] in A[(i, j)]) + (w[j] in A[(j, i)]) == 1
                   for i, j in edges)
    d = sum(1 for i in range(7) if LAYER1_W[i] != LAYER1_WP[i])
    assert d == 1
    print("layer-1 witness verified: shape axioms hold, both assignments "
          "are transversal covers, fibre-distance 1 (odd)")


LAYER2_WITNESS = {
    (0, 1): (1, 2), (0, 2): (0, 1), (0, 3): (2, 3), (0, 4): (0, 3),
    (0, 5): (0, 1), (0, 6): (2, 3),
    (1, 0): (2, 3), (1, 2): (1, 3), (1, 3): (1, 2), (1, 4): (0, 1),
    (1, 5): (0, 2), (1, 6): (0, 3),
    (2, 0): (0, 3), (2, 1): (0, 3), (2, 3): (0, 2), (2, 4): (1, 3),
    (2, 5): (1, 2), (2, 6): (1, 2),
    (3, 0): (0, 1), (3, 1): (1, 2), (3, 2): (1, 3), (3, 4): (2, 3),
    (3, 5): (0, 2), (3, 6): (0, 3),
    (4, 0): (0, 3), (4, 1): (0, 2), (4, 2): (0, 3), (4, 3): (1, 2),
    (4, 5): (1, 3), (4, 6): (1, 2),
    (5, 0): (0, 1), (5, 1): (1, 2), (5, 2): (0, 1), (5, 3): (2, 3),
    (5, 4): (2, 3), (5, 6): (0, 3),
    (6, 0): (0, 2), (6, 1): (0, 1), (6, 2): (0, 3), (6, 3): (2, 3),
    (6, 4): (1, 3), (6, 5): (1, 2),
}
LAYER2_W = (0, 3, 1, 1, 2, 2, 2)
LAYER2_WP = (2, 0, 0, 2, 3, 0, 3)


def verify_layer2_witness():
    A = {k: frozenset(v_) for k, v_ in LAYER2_WITNESS.items()}
    for i in range(7):
        others = [j for j in range(7) if j != i]
        assert all(len(A[(i, j)]) == 2 for j in others)
        for x in range(4):
            assert sum(1 for j in others if x in A[(i, j)]) == 3
        pats = {x: frozenset(j for j in others if x in A[(i, j)])
                for x in range(4)}
        assert len(set(pats.values())) == 4, f"fibre {i} not distinguishable"
    edges = list(combinations(range(7), 2))
    for w in (LAYER2_W, LAYER2_WP):
        assert all((w[i] in A[(i, j)]) + (w[j] in A[(j, i)]) == 1
                   for i, j in edges)
    d = sum(1 for i in range(7) if LAYER2_W[i] != LAYER2_WP[i])
    assert d == 7
    print("layer-2 witness verified: shape + distinguishability hold, "
          "both assignments are covers, fibre-distance 7 (odd)")


def layer3_categorical():
    """Layer 3 at the r=3 scale: point-identified families.
    Enumerate ALL families of 7 distinct triples on [7] pairwise
    intersecting in exactly one point; for each, enumerate all tiling
    solutions (every 5-set contains exactly one H_i = B_i u {w(i)}).
    Checks: every family is a Fano plane (Steiner, replication 3,
    2-law), has exactly 8 solutions, and no two solutions are at odd
    fibre-distance."""
    triples = list(combinations(range(7), 3))
    tset = [set(t) for t in triples]
    fams = []

    def bt(start, chosen):
        if len(chosen) == 7:
            fams.append(tuple(chosen))
            return
        for k in range(start, len(triples)):
            if all(len(tset[k] & tset[c]) == 1 for c in chosen):
                chosen.append(k)
                bt(k + 1, chosen)
                chosen.pop()

    bt(0, [])
    assert len(fams) == 30, len(fams)
    five_sets = list(combinations(range(7), 5))
    for fam in fams:
        B = [tset[k] for k in fam]
        assert all(sum(1 for Bi in B if {p, q} <= Bi) == 1
                   for p, q in combinations(range(7), 2))  # Steiner
        fibres = [[x for x in range(7) if x not in Bi] for Bi in B]
        inc = []
        for Z in five_sets:
            Zs = set(Z)
            inc.append([(i, x) for i in range(7) for x in fibres[i]
                        if B[i] <= Zs and x in Zs])
        sols = []
        for w in product(*fibres):
            if all(sum(1 for (i, x) in lst if w[i] == x) == 1
                   for lst in inc):
                sols.append(w)
        assert len(sols) == 8
        for a in range(8):
            for b2 in range(a + 1, 8):
                d = sum(1 for i in range(7) if sols[a][i] != sols[b2][i])
                assert d % 2 == 0
    print("layer-3 categorical check: all 30 pairwise-1 families on [7] "
          "are Fano planes; 8 tiling solutions each; all distances even")


if __name__ == "__main__":
    check_family(7, 3)
    check_family(11, 5)
    verify_layer1_witness()
    verify_layer2_witness()
    layer3_categorical()

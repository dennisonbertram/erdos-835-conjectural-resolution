#!/usr/bin/env python3
"""Self-contained verifier for `radius5_followup/STATUS.md`.

Stdlib only.  No solver.  No dependency on evidence/ (the Wallis array is
embedded).  Nothing here is launched as an unbounded search: every
non-existence claim is an exhaustive enumeration that terminates.

Parts:
  A  UNRESTRICTED radius-3 census at k = 2, 4, 6  (new)
  B  the k = 6 radius-4 obstruction and its mechanism  (new)
  C  independent audit of the "minimal trace is forced" lemma at k = 16

Run:   python3 -B collaboration/opus5/radius5_followup/verify_radius3_census_and_k6_obstruction.py
       ... --quick     (samples the k=6 families instead of all 1680)
"""
from __future__ import annotations

import sys
from itertools import combinations

# --------------------------------------------------------------------------
# Symmetric idempotent Latin squares of odd order n.
# Equivalently: near-one-factorisations of K_n with the class of c missing c.
# The unrestricted radius-3 ball of O_k needs k-1 of them, of order n = k+1,
# pairwise disagreeing in EVERY off-diagonal cell.
# --------------------------------------------------------------------------

def all_sils(n):
    edges = [(x, y) for x in range(n) for y in range(x + 1, n)]
    out, S = [], {}

    def rec(t):
        if t == len(edges):
            out.append(dict(S))
            return
        x, y = edges[t]
        ux = {S[e] for e in edges[:t] if x in e}
        uy = {S[e] for e in edges[:t] if y in e}
        for c in range(n):
            if c == x or c == y or c in ux or c in uy:
                continue
            S[(x, y)] = c
            rec(t + 1)
            del S[(x, y)]

    rec(0)
    return out


def check_sils(S, n):
    for x in range(n):
        vals = sorted(S[(min(x, y), max(x, y))] for y in range(n) if y != x)
        assert vals == sorted(set(range(n)) - {x}), "not a symmetric idempotent LS"
    return True


def _compat_bits(sq, n):
    """compat[a] = bitmask of squares discordant with a, in EVERY off-diagonal
    cell.  Built with big-int bitsets so it is fast even at n = 7 (6240
    squares); the pairwise definition is identical."""
    m = len(sq)
    edges = [(x, y) for x in range(n) for y in range(x + 1, n)]
    # same[e][c] = bitmask of squares whose value at edge e is c
    same = {e: [0] * n for e in edges}
    for a, S in enumerate(sq):
        bit = 1 << a
        for e in edges:
            same[e][S[e]] |= bit
    full = (1 << m) - 1
    compat = []
    for a, S in enumerate(sq):
        agree = 0
        for e in edges:
            agree |= same[e][S[e]]        # shares the value at e (includes a)
        compat.append(full & ~agree)
    return compat


def _iter_bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def max_discordant(sq, n):
    compat = _compat_bits(sq, n)
    best, sol = 0, ()

    def expand(cur, cand):
        nonlocal best, sol
        c = bin(cand).count("1")
        if len(cur) + c <= best:
            return
        if len(cur) > best:
            best, sol = len(cur), tuple(cur)
        for v in _iter_bits(cand):
            expand(cur + [v], cand & compat[v] & ~((1 << (v + 1)) - 1))
            cand ^= 1 << v
            if len(cur) + bin(cand).count("1") <= best:
                return

    expand([], (1 << len(sq)) - 1)
    return best, sol


def discordant_families(sq, n, need, limit=10 ** 9):
    compat = _compat_bits(sq, n)
    out = []

    def rec(cur, cand):
        if len(out) >= limit:
            return
        if len(cur) == need:
            out.append(tuple(cur))
            return
        c = bin(cand).count("1")
        if len(cur) + c < need:
            return
        for v in _iter_bits(cand):
            rec(cur + [v], cand & compat[v] & ~((1 << (v + 1)) - 1))
            cand ^= 1 << v
            if len(cur) + bin(cand).count("1") < need or len(out) >= limit:
                return

    rec([], (1 << len(sq)) - 1)
    return out


# --------------------------------------------------------------------------
# Radius-4: the 120 (in general C(k,2)) independent prescribed-hole problems.
# --------------------------------------------------------------------------

def radius4_holes(F, n, infp, u, v):
    """H_i = {M_i(uv), L_i(u), L_i(v)} where L_i(u)=S_i(inf,u), M_i(uv)=S_i(u,v)."""
    H = []
    for S in F:
        e = lambda a, b: S[(min(a, b), max(a, b))]
        H.append(frozenset({e(u, v), e(infp, u), e(infp, v)}))
    return H


def edge_colouring_exists(H, nA, nC):
    """Proper edge colouring of K_{nA} with nC colours, vertex i missing H[i].
    Exhaustive backtracking: a False return is a proof of non-existence."""
    edges = [(a, b) for a in range(nA) for b in range(a + 1, nA)]
    used = [set() for _ in range(nA)]

    def rec(t):
        if t == len(edges):
            return True
        a, b = edges[t]
        for c in range(nC):
            if c in H[a] or c in H[b] or c in used[a] or c in used[b]:
                continue
            used[a].add(c)
            used[b].add(c)
            if rec(t + 1):
                return True
            used[a].discard(c)
            used[b].discard(c)
        return False

    return rec(0)


# --------------------------------------------------------------------------

def section_a():
    print("=" * 74)
    print("A.  UNRESTRICTED radius-3 census (no cyclic / GF(16) / Wallis ansatz)")
    print("=" * 74)
    print("    The radius-3 ball of O_k needs k-1 symmetric idempotent Latin")
    print("    squares of order n = k+1, pairwise discordant off the diagonal.")
    print("    (That identification is prior art: evidence/odd_graph_local_ball/")
    print("     lmn_large_set.md.  The census below is not.)")
    verdict = {}
    for k in (2, 4, 6):
        n, need = k + 1, k - 1
        sq = all_sils(n)
        for S in sq:
            check_sils(S, n)
        best, fam = max_discordant(sq, n)
        exists = best >= need
        if exists:
            F = [sq[i] for i in fam[:need]]
            for x in range(n):
                for y in range(x + 1, n):
                    vals = {S[(x, y)] for S in F}
                    assert len(vals) == need == len(set(range(n)) - {x, y})
        verdict[k] = exists
        print(f"    k={k:2d}  n={n:2d}  symmetric idempotent LS: {len(sq):6d}   "
              f"max discordant {best:2d}  need {need:2d}   radius-3 "
              f"{'EXISTS' if exists else 'IMPOSSIBLE'}")
    assert verdict == {2: True, 4: False, 6: True}
    print()
    print("    k=2 CONTROL (a tight colouring exists): not obstructed. ok")
    print("    k=4 CONTROL (no tight colouring): the UNRESTRICTED radius-3 ball")
    print("        is already impossible -- only 1 of the 6 symmetric idempotent")
    print("        Latin squares of order 5 can be used, and 3 are needed.")
    return verdict


def section_b(quick):
    print()
    print("=" * 74)
    print("B.  k = 6: every radius-3 family dies at radius 4, and why")
    print("=" * 74)
    k, n, need = 6, 7, 5
    nA, nC = k - 1, k + 1
    sq = all_sils(n)
    fams = discordant_families(sq, n, need)
    print(f"    radius-3 discordant families (labelled): {len(fams)}")
    assert len(fams) == 1680
    sample = fams if not quick else fams[:24]
    if quick:
        print(f"    [--quick] sampling {len(sample)} of them")
    survivors = 0
    infeasible = feasible = mech = other = 0
    for fi in sample:
        F = [sq[i] for i in fi]
        alive = False
        for infp in range(n):
            V = [x for x in range(n) if x != infp]
            all_ok = True
            for u, v in combinations(V, 2):
                H = radius4_holes(F, n, infp, u, v)
                assert all(len(h) == 3 for h in H)
                B = {c: frozenset(i for i in range(nA) if c in H[i])
                     for c in range(nC)}
                assert sorted(len(b) for b in B.values()) == [1, 1, 1] + [3] * 4
                triples = [B[c] for c in range(nC) if len(B[c]) == 3]
                forced = [frozenset(set(range(nA)) - b) for b in triples]
                assert all(len(f) == 2 for f in forced)
                if edge_colouring_exists(H, nA, nC):
                    feasible += 1
                else:
                    infeasible += 1
                    all_ok = False
                    if len(set(forced)) < len(forced):
                        mech += 1
                    else:
                        other += 1
            if all_ok:
                alive = True
                break
        if alive:
            survivors += 1
    print(f"    families surviving radius-4 for SOME choice of root colour: "
          f"{survivors}")
    assert survivors == 0
    print(f"    radius-4 subproblems: {feasible} feasible, {infeasible} infeasible")
    print(f"      infeasible via forced-edge collision: {mech}")
    print(f"      infeasible for any other reason:      {other}")
    assert other == 0
    print()
    print("    MECHANISM.  A colour c with |B_c| = 3 has its class equal to a")
    print("    perfect matching of A \\ B_c, which has |A| - 3 = k - 4 vertices.")
    print("    At k = 6 that is exactly 2 vertices, i.e. ONE FORCED EDGE.  Two")
    print("    distinct triple-hole colours with the same B_c force the same")
    print("    edge twice, and the colour classes must be disjoint.  Every")
    print("    infeasible subproblem above is of exactly this kind.")
    print()
    print("    SCOPE.  At k = 16, |A| - 3 = 12, so a triple-hole class is a")
    print("    perfect matching on 12 vertices and nothing is forced.  This")
    print("    mechanism does NOT transfer to k = 16.")


# --------------------------------------------------------------------------
# C.  minimal-trace audit at k = 16 (Wallis array embedded)
# --------------------------------------------------------------------------

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


def wallis_sils():
    Q = 17
    out = []
    for sq in range(15):
        a = [0] + [FIRST_HALF_COLUMNS[j - 1][sq] for j in range(1, 9)]
        a.extend([-1] * 8)
        for j in range(9, 17):
            a[j] = (a[17 - j] + j) % Q
        assert sorted(a) == list(range(Q))
        M = set()
        for d in range(1, Q):
            y = (-a[d]) % Q
            x = (y + d) % Q
            if x != y:
                M.add(frozenset((x, y)))
        S = {}
        for c in range(Q):
            for e in M:
                x, y = tuple(e)
                p, q = sorted(((x + c) % Q, (y + c) % Q))
                S[(p, q)] = c
        out.append(S)
    return out


def section_c():
    print()
    print("=" * 74)
    print("C.  Audit: 'the minimal trace is forced' (coordinator lemma), k = 16")
    print("=" * 74)
    Q = 17
    SQ = wallis_sils()
    for S in SQ:
        check_sils(S, Q)
    for x in range(Q):
        for y in range(x + 1, Q):
            vals = {S[(x, y)] for S in SQ}
            assert len(vals) == 15 and vals == set(range(Q)) - {x, y}
    print("    15 symmetric idempotent Latin squares of order 17, discordant: ok")

    INF = 16
    V = [u for u in range(Q) if u != INF]
    ent = lambda S, a, b: S[(min(a, b), max(a, b))]
    L = [{u: ent(S, INF, u) for u in V} for S in SQ]

    def a_cov(i, x, u):
        return any(ent(SQ[i], u, v) == x for v in V if v != u)

    for i in range(15):
        for u in V:
            assert a_cov(i, INF, u), "the inf-class of M_i must cover all of V"
        Linv = {c: w for w, c in L[i].items()}
        for x in V:
            assert {u for u in V if not a_cov(i, x, u)} == {x, Linv[x]}
            assert Linv[x] != x, "L_i must be a derangement"
        for j in range(15):
            if i != j:
                Lj = {c: w for w, c in L[j].items()}
                for x in V:
                    assert Linv[x] != Lj[x]
    print("    a_{i,inf}(u) = 1 for all u: ok")
    print("    a_{i,x}(u) = 0 exactly on {x, L_i^-1(x)}, and L_i^-1(x) != x: ok")
    print("    L_i^-1(x) != L_j^-1(x) for i != j: ok")

    k = len(V)
    for i in range(15):
        for j in range(i + 1, 15):
            for x in [INF] + V:
                odd = sum(1 for u in V
                          if (1 + a_cov(i, x, u) + a_cov(j, x, u)) % 2)
                assert odd == (k if x == INF else k - 2), (i, j, x, odd)
    print(f"    odd-degree vertices of D_x: {k} for x=inf, {k-2} for finite x: ok")
    lo = k // 2 + k * ((k - 2) // 2)
    assert lo == k * (k - 1) // 2
    print(f"    forced lower bounds {k//2} + {k}*{(k-2)//2} = {lo} = |E(K_{k})|")
    print("    => EQUALITY, so |D_inf| = 8 is a perfect matching of V and")
    print("       |D_x| = 7 is a perfect matching of V \\ {L_i^-1(x), L_j^-1(x)}.")
    e_inf = k * (k - 1) // 2 - 3 * (k // 2)
    e_fin = k * (k - 1) // 2 - 3 * ((k - 2) // 2)
    assert e_inf % 3 == 0 and e_fin % 3 == 0
    tot = e_inf // 3 + k * (e_fin // 3)
    assert tot == k * (k - 1) * (k - 2) // 6
    print(f"    cross-check: |E(G_ij,inf)| = {e_inf} ({e_inf//3} triangles), "
          f"|E(G_ij,x)| = {e_fin} ({e_fin//3})")
    print(f"    total x-coloured triples {e_inf//3} + {k}*{e_fin//3} = {tot} "
          f"= C({k},3): ok")
    assert 8 % 3 == 2 and 7 % 3 == 1
    print("    the mod-3 filter (2) of radius5_reduction.md reads 8=2, 7=1 mod 3,")
    print("    so it is IMPLIED by the equality and adds nothing once known.")
    print()
    print("    VERDICT: the lemma is CORRECT.  One scope caveat -- the parity")
    print("    input comes from 'G_ij,x is triangle-decomposable', which")
    print("    presupposes a radius-5 extension.  So the trace is forced for")
    print("    any radius-4 colouring THAT EXTENDS to radius 5; it is not")
    print("    forced by the radius-4 data alone.")


def main():
    quick = "--quick" in sys.argv
    section_a()
    section_b(quick)
    section_c()
    print()
    print("Erdos-Rosenfeld #835 remains OPEN.  Nothing above is a global")
    print("construction or an unrestricted theorem at k = 16.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Complete brute-force decision of radius-4 and radius-5 existence at k=4.

Pure Python from the definitions (no SAT).  Exhausts:
  L: triples of derangements of V with the column condition,
  M: per-index edge-colourings of K_4 with the condition-2 vertex lists,
     filtered by the condition-3 transversal,
  N: per-edge edge-colourings of K_3 with the condition-4 vertex lists,
  P: per-index-pair colourings of the 4 triples (condition (1) of
     radius5_reduction.md).
Reports exact counts at every level and writes witnesses if any.
"""

import json
import sys
import time
from itertools import combinations, permutations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ball_defs  # noqa: E402

K = 4
V = tuple(range(4))
A = tuple(range(3))
INF = 4
C = tuple(range(5))
VE = tuple(combinations(V, 2))       # 6 edges of K_V
AE = tuple(combinations(A, 2))       # 3 edges of K_A
VT = tuple(combinations(V, 3))       # 4 triples


def derangements():
    return [
        p for p in permutations(V) if all(p[u] != u for u in V)
    ]


def all_L():
    out = []
    for rows in product(derangements(), repeat=3):
        ok = all(
            {rows[i][u] for i in A} == set(V) - {u} for u in V
        )
        if ok:
            out.append(rows)
    return out


def all_M_for(Li):
    """All edge-colourings M_i of K_4 whose colours at u are exactly
    C \\ {u, Li[u]}."""
    lists = {u: set(C) - {u, Li[u]} for u in V}
    edge_allowed = [
        sorted(lists[u] & lists[v]) for (u, v) in VE
    ]
    out = []
    for combo in product(*edge_allowed):
        ok = True
        for u in V:
            got = sorted(
                combo[ei] for ei, e in enumerate(VE) if u in e
            )
            if got != sorted(lists[u]):
                ok = False
                break
        if ok:
            out.append(combo)
    return out


def n_options(L, M, e):
    """All condition-4 colourings N_e of K_3 (edges AE) for edge e."""
    u, v = e
    lists = {
        i: set(C) - {M[i][VE.index(e)], L[i][u], L[i][v]} for i in A
    }
    if any(len(s) != 2 for s in lists.values()):
        return []
    out = []
    for combo in product(C, repeat=len(AE)):
        ok = True
        for i in A:
            got = sorted(
                combo[fi] for fi, f in enumerate(AE) if i in f
            )
            if got != sorted(lists[i]):
                ok = False
                break
        if ok:
            out.append(combo)
    return out


def p_exists(allowed_per_edge):
    """Given allowed 2-colour sets per uv edge, does a colouring of the 4
    triples exist with, per uv, {P(uv w): w} = allowed(uv) exactly?"""
    for combo in product(C, repeat=len(VT)):
        ok = True
        for ei, e in enumerate(VE):
            got = sorted(
                combo[ti] for ti, t in enumerate(VT) if set(e) <= set(t)
            )
            if got != sorted(allowed_per_edge[ei]):
                ok = False
                break
        if ok:
            return combo
    return None


def main():
    t0 = time.time()
    Ls = all_L()
    print(f"L candidates (derangement triples, column condition): {len(Ls)}")

    r4_witness = None
    r5_witness = None
    n_LM = 0
    n_LM_with_full_N = 0
    n_r4_structures = 0        # (L, M, N) complete radius-4 structures
    n_r5_structures = 0
    m_cache = {}

    for L in Ls:
        m_opts = []
        for i in A:
            key = L[i]
            if key not in m_cache:
                m_cache[key] = all_M_for(key)
            m_opts.append(m_cache[key])
        for M in product(*m_opts):
            # condition 3 transversal
            ok = all(
                sorted(M[i][ei] for i in A)
                == sorted(c for c in C if c not in VE[ei])
                for ei in range(len(VE))
            )
            if not ok:
                continue
            n_LM += 1
            nopts = [n_options(L, M, e) for e in VE]
            if any(not o for o in nopts):
                continue
            n_LM_with_full_N += 1
            counts = 1
            for o in nopts:
                counts *= len(o)
            n_r4_structures += counts
            if r4_witness is None:
                choice = [o[0] for o in nopts]
                r4_witness = (L, M, choice)
            # radius 5: iterate all N combinations
            for nchoice in product(*nopts):
                Ps = []
                feasible = True
                for (i, j) in AE:
                    fi = AE.index((i, j))
                    allowed = [
                        sorted(
                            set(C)
                            - {
                                nchoice[ei][fi],
                                M[i][ei],
                                M[j][ei],
                            }
                        )
                        for ei in range(len(VE))
                    ]
                    p = p_exists(allowed)
                    if p is None:
                        feasible = False
                        break
                    Ps.append(((i, j), p))
                if feasible:
                    n_r5_structures += 1
                    if r5_witness is None:
                        r5_witness = (L, M, nchoice, Ps)

    print(f"(L,M) pairs passing conditions 1-3: {n_LM}")
    print(
        "(L,M) pairs with a condition-4 N on every edge: "
        f"{n_LM_with_full_N}"
    )
    print(f"complete radius-4 structures (L,M,N): {n_r4_structures}")
    print(f"complete radius-5 structures (L,M,N) with P: {n_r5_structures}")
    print(f"elapsed: {time.time() - t0:.1f}s")

    def pack(L, M, nchoice, Ps=None):
        Ld = [list(L[i]) for i in A]
        Md = {(i, *VE[ei]): M[i][ei] for i in A for ei in range(len(VE))}
        Nd = {
            (VE[ei], AE[fi]): nchoice[ei][fi]
            for ei in range(len(VE))
            for fi in range(len(AE))
        }
        Pd = None
        if Ps is not None:
            Pd = {
                (f, VT[ti]): p[ti]
                for (f, p) in Ps
                for ti in range(len(VT))
            }
        return Ld, Md, Nd, Pd

    if r4_witness:
        L, M, choice = r4_witness
        Ld, Md, Nd, _ = pack(L, M, choice)
        fails = ball_defs.check_radius4(K, Ld, Md, Nd)
        assert not fails, fails
        with open(HERE / "k4_radius4_witness.json", "w") as fh:
            json.dump(ball_defs.to_json_dict(K, Ld, Md, Nd), fh, indent=1)
        print("radius-4 k=4: SAT, witness verified semantically, written")
    else:
        print("radius-4 k=4: UNSAT (exhaustive)")

    if r5_witness:
        L, M, nchoice, Ps = r5_witness
        Ld, Md, Nd, Pd = pack(L, M, nchoice, Ps)
        fails = ball_defs.check_radius5(K, Ld, Md, Nd, Pd)
        assert not fails, fails
        with open(HERE / "k4_radius5_witness.json", "w") as fh:
            json.dump(
                ball_defs.to_json_dict(K, Ld, Md, Nd, Pd), fh, indent=1
            )
        print("radius-5 k=4: SAT, witness verified semantically, written")
    else:
        print("radius-5 k=4: UNSAT (exhaustive)")


if __name__ == "__main__":
    main()

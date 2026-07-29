#!/usr/bin/env python3
"""Semantic definitions of radius-4 / radius-5 local-ball structures at even k.

Transcribed directly from
  evidence/odd_graph_local_ball/radius4_reduction.md   (conditions 1-4)
  evidence/odd_graph_local_ball/radius5_reduction.md   (exact condition (1))
No solver or encoder imports.  All checks are multiset (sorted-list)
equalities, which is exactly what "the colours on the d edges ... are
exactly [a d-element set]" means.

Conventions: V = 0..k-1, A = 0..k-2, INF = k, C = 0..k.
L[i][u] in V;  M[(i,u,v)] with u<v;  N[((u,v),(i,j))] with u<v,i<j;
P[((i,j),(u,v,w))] with i<j, u<v<w.
"""

from itertools import combinations


def sets(k):
    V = tuple(range(k))
    A = tuple(range(k - 1))
    INF = k
    C = tuple(range(k + 1))
    return V, A, INF, C


def check_radius4(k, L, M, N, collect_all=False):
    """Return list of failure strings (empty == PASS)."""
    V, A, INF, C = sets(k)
    fails = []

    def fail(msg):
        fails.append(msg)
        if not collect_all and len(fails) >= 50:
            raise RuntimeError("too many failures; aborting early")

    # Condition 1: for every u, {L_i(u) : i in A} = V \ {u}.
    for u in V:
        got = sorted(L[i][u] for i in A)
        want = sorted(x for x in V if x != u)
        if got != want:
            fail(f"cond1 u={u}: {got} != {want}")

    # Condition 2: each L_i is a derangement permutation of V, and the
    # colours on the k-1 edges of M_i at u are exactly C \ {u, L_i(u)}.
    for i in A:
        row = [L[i][u] for u in V]
        if sorted(row) != list(V):
            fail(f"cond2 i={i}: L_{i} not a permutation: {row}")
        if any(row[u] == u for u in V):
            fail(f"cond2 i={i}: L_{i} has a fixed point: {row}")
        for u in V:
            got = sorted(M[(i, min(u, v), max(u, v))] for v in V if v != u)
            want = sorted(c for c in C if c not in (u, L[i][u]))
            if got != want:
                fail(f"cond2 i={i} u={u}: incident colours {got} != {want}")

    # Condition 3: for every edge uv, {M_i(uv) : i in A} = C \ {u, v}.
    for u, v in combinations(V, 2):
        got = sorted(M[(i, u, v)] for i in A)
        want = sorted(c for c in C if c not in (u, v))
        if got != want:
            fail(f"cond3 uv={u},{v}: {got} != {want}")

    # Condition 4: for every uv, N_uv is an edge-colouring of K_A whose
    # colours at index i are exactly C \ {M_i(uv), L_i(u), L_i(v)}.
    for u, v in combinations(V, 2):
        for i in A:
            got = sorted(
                N[((u, v), (min(i, j), max(i, j)))] for j in A if j != i
            )
            excluded = {M[(i, u, v)], L[i][u], L[i][v]}
            if len(excluded) != 3:
                fail(f"cond4 uv={u},{v} i={i}: excluded set not size 3")
            want = sorted(c for c in C if c not in excluded)
            if got != want:
                fail(f"cond4 uv={u},{v} i={i}: {got} != {want}")

    return fails


def check_radius5(k, L, M, N, P, collect_all=False):
    """Radius-4 conditions plus exact extension condition (1) of
    radius5_reduction.md: for every ij, uv,
      {P_ij(uvw) : w not in {u,v}} = C \\ {N_uv(ij), M_i(uv), M_j(uv)}.
    """
    V, A, INF, C = sets(k)
    fails = check_radius4(k, L, M, N, collect_all=collect_all)
    for i, j in combinations(A, 2):
        for u, v in combinations(V, 2):
            got = sorted(
                P[((i, j), tuple(sorted((u, v, w))))]
                for w in V
                if w not in (u, v)
            )
            excluded = {N[((u, v), (i, j))], M[(i, u, v)], M[(j, u, v)]}
            if len(excluded) != 3:
                fails.append(
                    f"r5 ij={i},{j} uv={u},{v}: excluded set not size 3"
                )
            want = sorted(c for c in C if c not in excluded)
            if got != want:
                fails.append(f"r5 ij={i},{j} uv={u},{v}: {got} != {want}")
    return fails


# ---- JSON (de)serialization of witnesses -------------------------------

def to_json_dict(k, L, M, N, P=None):
    d = {
        "k": k,
        "L": [[L[i][u] for u in range(k)] for i in range(k - 1)],
        "M": {f"{i},{u},{v}": c for (i, u, v), c in sorted(M.items())},
        "N": {
            f"{u},{v}|{i},{j}": c
            for ((u, v), (i, j)), c in sorted(N.items())
        },
    }
    if P is not None:
        d["P"] = {
            f"{i},{j}|{u},{v},{w}": c
            for ((i, j), (u, v, w)), c in sorted(P.items())
        }
    return d


def from_json_dict(d):
    k = d["k"]
    L = [list(row) for row in d["L"]]
    M = {}
    for key, c in d["M"].items():
        i, u, v = map(int, key.split(","))
        M[(i, u, v)] = c
    N = {}
    for key, c in d["N"].items():
        left, right = key.split("|")
        u, v = map(int, left.split(","))
        i, j = map(int, right.split(","))
        N[((u, v), (i, j))] = c
    P = None
    if "P" in d:
        P = {}
        for key, c in d["P"].items():
            left, right = key.split("|")
            i, j = map(int, left.split(","))
            u, v, w = map(int, right.split(","))
            P[((i, j), (u, v, w))] = c
    return k, L, M, N, P

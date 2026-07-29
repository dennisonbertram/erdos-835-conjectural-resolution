#!/usr/bin/env python3
"""Independent CP-SAT model (native IntVar/AllDifferent encoding) of the
radius-4 / radius-5 ball conditions at even k.  Second decision procedure,
structurally different from the CNF encoder.

Usage: solve_cpsat.py K RADIUS [timeout_s] [workers] [witness_out.json]
Exit prints FEASIBLE/INFEASIBLE/UNKNOWN with solver stats.
"""

import json
import sys
import time
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ball_defs  # noqa: E402


def build(k, radius):
    V = tuple(range(k))
    A = tuple(range(k - 1))
    C = tuple(range(k + 1))
    VE = tuple(combinations(V, 2))
    AE = tuple(combinations(A, 2))
    VT = tuple(combinations(V, 3))

    m = cp_model.CpModel()
    L = {}
    for i in A:
        for u in V:
            L[i, u] = m.NewIntVarFromDomain(
                cp_model.Domain.FromValues([x for x in V if x != u]),
                f"L{i}_{u}",
            )
    M = {}
    for i in A:
        for (u, v) in VE:
            M[i, (u, v)] = m.NewIntVarFromDomain(
                cp_model.Domain.FromValues(
                    [c for c in C if c not in (u, v)]
                ),
                f"M{i}_{u}_{v}",
            )
    # radius=3 mode: conditions 1-3 only (no N layer) — structural probe.
    N = {}
    if radius >= 4:
        for e in VE:
            for f in AE:
                N[e, f] = m.NewIntVar(0, k, f"N{e}_{f}")

    # cond 1 (columns) + permutation rows (cond 2 first half)
    for i in A:
        m.AddAllDifferent([L[i, u] for u in V])
    for u in V:
        m.AddAllDifferent([L[i, u] for i in A])

    # cond 2: at u, edge colours + {u, L_i(u)} = C
    for i in A:
        for u in V:
            edges = [
                M[i, (min(u, v), max(u, v))] for v in V if v != u
            ]
            m.AddAllDifferent(edges + [L[i, u]])

    # cond 3
    for e in VE:
        m.AddAllDifferent([M[i, e] for i in A])

    # cond 4: at index i, N_e edge colours + {M_i(e), L_i(u), L_i(v)} = C
    if radius >= 4:
        for e in VE:
            u, v = e
            for i in A:
                edges = [
                    N[e, (min(i, j), max(i, j))] for j in A if j != i
                ]
                m.AddAllDifferent(edges + [M[i, e], L[i, u], L[i, v]])

    P = {}
    if radius == 5:
        for f in AE:
            for t in VT:
                P[f, t] = m.NewIntVar(0, k, f"P{f}_{t}")
        for f in AE:
            i, j = f
            for e in VE:
                u, v = e
                slots = [
                    P[f, tuple(sorted((u, v, w)))]
                    for w in V
                    if w not in e
                ]
                m.AddAllDifferent(
                    slots + [N[e, f], M[i, e], M[j, e]]
                )

    return m, L, M, N, P


def main():
    k = int(sys.argv[1])
    radius = int(sys.argv[2])
    timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    out = sys.argv[5] if len(sys.argv) > 5 else None

    model, L, M, N, P = build(k, radius)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = timeout
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = 1
    t0 = time.time()
    status = solver.Solve(model)
    t1 = time.time()
    name = solver.StatusName(status)
    print(
        f"k={k} radius={radius}: {name} in {t1 - t0:.1f}s "
        f"(branches={solver.NumBranches()}, "
        f"conflicts={solver.NumConflicts()})"
    )

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        A = tuple(range(k - 1))
        V = tuple(range(k))
        Ld = [[solver.Value(L[i, u]) for u in V] for i in A]
        Md = {
            (i, e[0], e[1]): solver.Value(var)
            for (i, e), var in M.items()
        }
        Nd = {(e, f): solver.Value(var) for (e, f), var in N.items()}
        Pd = None
        if radius == 5:
            Pd = {(f, t): solver.Value(var) for (f, t), var in P.items()}
        if radius == 3:
            # inline check of conditions 1-3 only
            from itertools import combinations as comb
            C_ = tuple(range(k + 1))
            fails = []
            for u in range(k):
                if sorted(Ld[i][u] for i in A) != sorted(
                    x for x in range(k) if x != u
                ):
                    fails.append(f"cond1 u={u}")
            for i in A:
                if sorted(Ld[i]) != list(range(k)) or any(
                    Ld[i][u] == u for u in range(k)
                ):
                    fails.append(f"cond2 perm i={i}")
                for u in range(k):
                    got = sorted(
                        Md[(i, min(u, v), max(u, v))]
                        for v in range(k)
                        if v != u
                    )
                    if got != sorted(
                        c for c in C_ if c not in (u, Ld[i][u])
                    ):
                        fails.append(f"cond2 i={i} u={u}")
            for u, v in comb(range(k), 2):
                if sorted(Md[(i, u, v)] for i in A) != sorted(
                    c for c in C_ if c not in (u, v)
                ):
                    fails.append(f"cond3 {u}{v}")
        elif radius == 4:
            fails = ball_defs.check_radius4(k, Ld, Md, Nd)
        else:
            fails = ball_defs.check_radius5(k, Ld, Md, Nd, Pd)
        print(
            "semantic check:",
            "PASS" if not fails else f"FAIL {fails[:5]}",
        )
        if out and not fails:
            with open(out, "w") as fh:
                json.dump(
                    ball_defs.to_json_dict(k, Ld, Md, Nd, Pd),
                    fh,
                    indent=1,
                )
            print(f"witness written: {out}")


if __name__ == "__main__":
    main()

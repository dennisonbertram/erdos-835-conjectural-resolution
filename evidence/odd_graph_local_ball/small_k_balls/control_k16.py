#!/usr/bin/env python3
"""k=16 control: the verified Wallis/golf chart must PASS the radius-4
semantic checker, and the CNF encoder restricted to the Wallis L/M must
be SAT with a decoded N that passes the same checker.

L_i(u) = golf[i][u][16], M_i(uv) = golf[i][u][v]  (i in 0..14, u,v in 0..15).
N is not part of the chart; each N_uv is an independent list-edge-colouring
of K_15, solved per edge exactly as in
evidence/global_latin_radius4_certificate.py (construct_one_n).
"""

import json
import sys
import time
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_EVIDENCE = HERE.parent.parent
sys.path.insert(0, str(REPO_EVIDENCE))
sys.path.insert(0, str(HERE))

from global_latin_audit import construct_golf17  # noqa: E402
import ball_defs  # noqa: E402

from ortools.sat.python import cp_model  # noqa: E402

K = 16
INF = 16
SQUARES = tuple(range(15))
FINITE = tuple(range(16))
COLORS = tuple(range(17))


def solve_one_n(golf, u, v):
    allowed = [
        set(COLORS)
        - {golf[i][u][v], golf[i][u][INF], golf[i][v][INF]}
        for i in SQUARES
    ]
    assert all(len(a) == 14 for a in allowed)
    model = cp_model.CpModel()
    var = {}
    for i, j in combinations(SQUARES, 2):
        dom = sorted(allowed[i] & allowed[j])
        var[i, j] = model.NewIntVarFromDomain(
            cp_model.Domain.FromValues(dom), f"n{i}_{j}"
        )
    for i in SQUARES:
        model.AddAllDifferent(
            [var[min(i, j), max(i, j)] for j in SQUARES if j != i]
        )
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 0
    solver.parameters.max_time_in_seconds = 60
    status = solver.Solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE), (u, v)
    return {e: solver.Value(x) for e, x in var.items()}


def main():
    golf = construct_golf17()
    L = [[golf[i][u][INF] for u in FINITE] for i in SQUARES]
    M = {
        (i, u, v): golf[i][u][v]
        for i in SQUARES
        for u, v in combinations(FINITE, 2)
    }

    t0 = time.time()
    N = {}
    for u, v in combinations(FINITE, 2):
        cert = solve_one_n(golf, u, v)
        for (i, j), c in cert.items():
            N[((u, v), (i, j))] = c
    t1 = time.time()
    print(f"N solved per-edge by CP-SAT: 120/120 in {t1 - t0:.1f}s")

    fails = ball_defs.check_radius4(K, L, M, N, collect_all=False)
    if fails:
        print("SEMANTIC RADIUS-4 CHECK: FAIL")
        for f in fails[:20]:
            print("  ", f)
        sys.exit(1)
    print("SEMANTIC RADIUS-4 CHECK on Wallis chart + solved N: PASS")

    out = HERE / "wallis_k16_radius4_witness.json"
    with open(out, "w") as fh:
        json.dump(ball_defs.to_json_dict(K, L, M, N), fh)
    print(f"witness written: {out}")

    fix = HERE / "wallis_k16_LM_fix.json"
    with open(fix, "w") as fh:
        json.dump(
            {
                "L": L,
                "M": {f"{i},{u},{v}": c for (i, u, v), c in M.items()},
            },
            fh,
        )
    print(f"L/M fix file for encoder control: {fix}")


if __name__ == "__main__":
    main()

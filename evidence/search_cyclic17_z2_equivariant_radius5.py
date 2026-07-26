#!/usr/bin/env python3
"""Search the Z_2-equivariant cyclic-17 radius-five boundary.

Uses the (-1)-symmetric golf design in `cyclic17_symmetric_golf_design.json`.
The involution

    Phi'(sigma i, sigma j, tau q) = a_q - Phi(i, j, q)

is verified well defined by `verify_cyclic17_z2_equivariant_reduction.py`.
Here the model is built on involution ORBITS, so it genuinely has 2,072 free
phases instead of 4,200 (the 56 symmetry-fixed cells are constants).

IMPORTANT SCOPE.
  * A witness would be an equivariant radius-five boundary for ONE non-Wallis
    golf design.  That is an intermediate object: it is not a large set
    LS(15,16,32) and does not resolve Erdos-Rosenfeld #835.
  * INFEASIBLE here would exclude only the Z_2-EQUIVARIANT solutions for THIS
    golf design.  It would say nothing about non-equivariant solutions for the
    same design, about the Wallis design, or about #835.
  * A solver status of UNKNOWN is a resource result and is never evidence.

Run:  python3 -B evidence/search_cyclic17_z2_equivariant_radius5.py \
          --seconds 600 --workers 1
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from itertools import combinations

from ortools.sat.python import cp_model

from verify_cyclic17_z2_equivariant_reduction import (
    P, load_design, check_golf_design, multiplier_group, triple_orbits,
    layer2_data, sigma_tau)

HERE = os.path.dirname(os.path.abspath(__file__))


def build(design, reps, F, sigma, tau, a):
    """Model on involution orbits.  Returns (model, lit, rep_of)."""
    nu = {}                      # cell -> its image under the involution
    for (i, j) in combinations(range(15), 2):
        si, sj = sorted((sigma[i], sigma[j]))
        for q in range(40):
            nu[(i, j, q)] = (si, sj, tau[q])
    dom = {}
    for (i, j) in combinations(range(15), 2):
        for q in range(40):
            dom[(i, j, q)] = [c for c in range(P)
                              if c not in F[i][q] and c not in F[j][q]]

    model = cp_model.CpModel()
    TRUE = model.NewBoolVar("true")
    model.Add(TRUE == 1)
    FALSE = TRUE.Not()

    inv2 = pow(2, P - 2, P)
    var = {}                     # representative cell -> {colour: BoolVar}
    forced = {}                  # fixed cell -> its forced phase
    for x in sorted(nu):
        y = nu[x]
        if y == x:
            forced[x] = (a[x[2]] * inv2) % P
            assert forced[x] in dom[x], x
            continue
        if x > y:
            continue             # y is the representative
        var[x] = {c: model.NewBoolVar(f"p{x}_{c}") for c in dom[x]}
        model.AddExactlyOne(var[x].values())

    def lit(cell, c):
        """Literal for 'Phi(cell) = c'."""
        if c not in dom[cell]:
            return FALSE
        if cell in forced:
            return TRUE if forced[cell] == c else FALSE
        y = nu[cell]
        if cell < y:
            return var[cell][c]
        # cell is the partner: Phi(cell) = a_q - Phi(y), q = y's orbit
        cc = (a[y[2]] - c) % P
        return var[y][cc] if cc in var[y] else FALSE

    # rows: the 40 selected triples decompose K_17 - M_i - M_j
    all_edges = [frozenset(e) for e in combinations(range(P), 2)]
    for (i, j) in combinations(range(15), 2):
        residual = [e for e in all_edges
                    if e not in design[i] and e not in design[j]]
        cover = {e: [] for e in residual}
        for q, T in enumerate(reps):
            for c in dom[(i, j, q)]:
                lt = lit((i, j, q), c)
                sh = tuple((v + c) % P for v in T)
                for e in (frozenset(x) for x in combinations(sh, 2)):
                    cover[e].append(lt)
        for e in residual:
            model.AddExactlyOne(cover[e])

    # columns: at each orbit and fixed point the 14 phases exhaust Z_17 \ F_i(q)
    for q in range(40):
        for i in range(15):
            for c in range(P):
                if c in F[i][q]:
                    continue
                model.AddExactlyOne(
                    lit((min(i, j), max(i, j), q), c)
                    for j in range(15) if j != i)
    return model, var, forced, nu, dom


def extract(solver, var, forced, nu, dom, a):
    sol = {}
    for x, d in var.items():
        for c, v in d.items():
            if solver.Value(v):
                sol[x] = c
                sol[nu[x]] = (a[x[2]] - c) % P
    sol.update(forced)
    assert len(sol) == 4200, len(sol)
    return sol


def verify(design, reps, F, sol, sigma, tau, a):
    """Full independent semantic check of the UNREDUCED system."""
    all_edges = [frozenset(e) for e in combinations(range(P), 2)]
    for (i, j) in combinations(range(15), 2):
        residual = {e for e in all_edges
                    if e not in design[i] and e not in design[j]}
        got = []
        for q, T in enumerate(reps):
            sh = tuple((v + sol[(i, j, q)]) % P for v in T)
            got.extend(frozenset(x) for x in combinations(sh, 2))
        assert len(got) == len(set(got)) == len(residual) and set(got) == residual
    for q in range(40):
        for i in range(15):
            vals = [sol[(min(i, j), max(i, j), q)] for j in range(15) if j != i]
            assert len(set(vals)) == 14
            assert set(vals) == set(range(P)) - F[i][q], (q, i)
    # and it really is equivariant
    for (i, j) in combinations(range(15), 2):
        si, sj = sorted((sigma[i], sigma[j]))
        for q in range(40):
            assert sol[(si, sj, tau[q])] == (a[q] - sol[(i, j, q)]) % P
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=600.0)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    design, sha = load_design()
    check_golf_design(design)
    assert multiplier_group(design) == [1, 16]
    reps = triple_orbits()
    F = layer2_data(design, reps)
    sigma, tau, a = sigma_tau(design, reps)
    model, var, forced, nu, dom = build(design, reps, F, sigma, tau, a)
    print(f"golf design SHA-256 {sha}")
    print(f"free phase cells {len(var)}, forced cells {len(forced)}, "
          f"total {2 * len(var) + len(forced)}")
    sys.stdout.flush()

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.random_seed = args.seed
    st = solver.Solve(model)
    name = solver.StatusName(st)
    print(f"status {name} after {solver.WallTime():.1f}s, "
          f"{solver.NumBranches()} branches, {solver.NumConflicts()} conflicts")

    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = extract(solver, var, forced, nu, dom, a)
        verify(design, reps, F, sol, sigma, tau, a)
        print("witness independently verified as a radius-five boundary")
        print("SCOPE: this is an intermediate layer-2 object for one golf "
              "design; it is NOT a solution of Erdos-Rosenfeld #835.")
        out = args.output or os.path.join(
            HERE, "cyclic17_z2_equivariant_radius5_certificate.json")
        with open(out, "w") as fh:
            json.dump({"golf_design_sha256": sha,
                       "phases": {f"{i},{j},{q}": c
                                  for (i, j, q), c in sorted(sol.items())}},
                      fh, indent=1)
        print(f"certificate written to {out}")
    elif name == "INFEASIBLE":
        print("SCOPE: this excludes only Z_2-EQUIVARIANT solutions for THIS "
              "golf design.  It does not exclude non-equivariant solutions, "
              "the Wallis design, or anything about #835.")
    else:
        print("UNKNOWN is a resource result, not evidence.")


if __name__ == "__main__":
    main()

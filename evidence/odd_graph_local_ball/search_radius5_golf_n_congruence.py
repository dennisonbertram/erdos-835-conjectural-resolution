#!/usr/bin/env python3
"""Find a full N layer satisfying all forced radius-five congruences.

This is an intermediate exact search only.  It omits P and therefore never
claims a radius-five ball; its output is a coherent N-layer hint for the
complete joint model.  Every constraint retained here is an N constraint of
the complete model or a consequence forced by its P triangle decomposition.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from ortools.sat.python import cp_model

from search_radius5_golf_joint import IJS, SQUARES, UVS, golf_sha256, n_allowed, verify_l_m
from search_radius5_golf_joint_tight import add_forced_triangle_congruences
from global_latin_audit import construct_golf17

SCHEMA = "odd-graph-o16-radius5-fixed-golf-n-congruence-v1"


def build_n_model():
    golf = construct_golf17()
    verify_l_m(golf)
    model = cp_model.CpModel()
    n = {}
    for uv in UVS:
        for ij in IJS:
            i, j = ij
            domain = sorted(n_allowed(golf, i, uv) & n_allowed(golf, j, uv))
            n[uv + ij] = model.NewIntVarFromDomain(cp_model.Domain.FromValues(domain), f"n_{uv[0]}_{uv[1]}_{i}_{j}")
    for uv in UVS:
        for i in SQUARES:
            model.AddAllDifferent([n[uv + (min(i, j), max(i, j))] for j in SQUARES if j != i])
    literal_count = add_forced_triangle_congruences(model, n, golf)
    return model, n, golf, literal_count


def make_payload(solver, n, golf, literal_count):
    payload = {
        "schema": SCHEMA,
        "golf_sha256": golf_sha256(golf),
        "n_order": "uv-major then ij-major, lexicographic combinations",
        "n_values": [solver.Value(n[uv + ij]) for uv in UVS for ij in IJS],
        "triangle_congruence_literals": literal_count,
    }
    payload["sha256_without_hash"] = hashlib.sha256((json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=120.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    model, n, golf, literal_count = build_n_model()
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    status = solver.Solve(model)
    result = {"schema": SCHEMA, "status": solver.StatusName(status), "golf_sha256": golf_sha256(golf), "triangle_congruence_literals": literal_count, "wall_time_seconds": solver.WallTime(), "branches": solver.NumBranches(), "conflicts": solver.NumConflicts()}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        payload = make_payload(solver, n, golf, literal_count)
        result["n_sha256_without_hash"] = payload["sha256_without_hash"]
        if args.output:
            args.output.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

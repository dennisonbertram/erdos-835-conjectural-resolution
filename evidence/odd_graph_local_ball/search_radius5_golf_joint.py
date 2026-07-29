#!/usr/bin/env python3
"""Complete joint radius-5 CP-SAT extension model for the fixed golf L/M."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model

EVIDENCE = Path(__file__).resolve().parents[1]
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))
from global_latin_audit import construct_golf17

COLORS = tuple(range(17))
FINITE = tuple(range(16))
SQUARES = tuple(range(15))
UVS = tuple(combinations(FINITE, 2))
IJS = tuple(combinations(SQUARES, 2))
TRIPLES = tuple(combinations(FINITE, 3))
SCHEMA = "odd-graph-o16-radius5-fixed-golf-joint-v1"


def n_allowed(golf: list[list[list[int]]], i: int, uv: tuple[int, int]) -> set[int]:
    u, v = uv
    return set(COLORS) - {golf[i][u][v], golf[i][u][16], golf[i][v][16]}


def verify_l_m(golf: list[list[list[int]]]) -> None:
    for u in FINITE:
        assert {golf[i][u][16] for i in SQUARES} == set(FINITE) - {u}
    for i in SQUARES:
        assert {golf[i][u][16] for u in FINITE} == set(FINITE)
        assert all(golf[i][u][16] != u for u in FINITE)
        for u in FINITE:
            assert {golf[i][min(u, v)][max(u, v)] for v in FINITE if v != u} == set(COLORS) - {u, golf[i][u][16]}
    for u, v in UVS:
        assert {golf[i][u][v] for i in SQUARES} == set(COLORS) - {u, v}


def golf_sha256(golf: list[list[list[int]]]) -> str:
    return hashlib.sha256(bytes(value for square in golf for row in square for value in row)).hexdigest()


def build_model():
    golf = construct_golf17()
    verify_l_m(golf)
    model = cp_model.CpModel()
    n: dict[tuple[int, int, int, int], cp_model.IntVar] = {}
    p: dict[tuple[int, int, int, int, int], cp_model.IntVar] = {}
    n_domain_values = p_domain_values = 0
    for u, v in UVS:
        for i, j in IJS:
            domain = sorted(n_allowed(golf, i, (u, v)) & n_allowed(golf, j, (u, v)))
            n_domain_values += len(domain)
            n[u, v, i, j] = model.NewIntVarFromDomain(cp_model.Domain.FromValues(domain), f"n_{u}_{v}_{i}_{j}")
    n_all_different = 0
    for u, v in UVS:
        for i in SQUARES:
            model.AddAllDifferent([n[u, v, min(i, j), max(i, j)] for j in SQUARES if j != i])
            n_all_different += 1
    for i, j in IJS:
        for triple in TRIPLES:
            forbidden = {golf[i][u][v] for u, v in combinations(triple, 2)} | {golf[j][u][v] for u, v in combinations(triple, 2)}
            domain = sorted(set(COLORS) - forbidden)
            p_domain_values += len(domain)
            u, v, w = triple
            p[i, j, u, v, w] = model.NewIntVarFromDomain(cp_model.Domain.FromValues(domain), f"p_{i}_{j}_{u}_{v}_{w}")
    p_all_different = n_p_not_equal = 0
    for i, j in IJS:
        for u, v in UVS:
            values = []
            for w in FINITE:
                if w in (u, v):
                    continue
                triple = tuple(sorted((u, v, w)))
                value = p[(i, j) + triple]
                values.append(value)
                model.Add(value != n[u, v, i, j])
                n_p_not_equal += 1
            model.AddAllDifferent(values)
            p_all_different += 1
    stats = {
        "n_variables": len(n), "p_variables": len(p), "integer_variables": len(n) + len(p),
        "n_domain_values": n_domain_values, "p_domain_values": p_domain_values,
        "n_all_different": n_all_different, "p_all_different": p_all_different,
        "n_p_not_equal": n_p_not_equal, "constraints": n_all_different + p_all_different + n_p_not_equal,
    }
    assert stats["n_variables"] == 12600 and stats["p_variables"] == 58800 and stats["integer_variables"] == 71400
    assert stats["n_all_different"] == 1800 and stats["p_all_different"] == 12600 and stats["n_p_not_equal"] == 176400
    return model, n, p, golf, stats


def certificate_payload(solver, n, p, golf, stats):
    n_values = [solver.Value(n[u, v, i, j]) for u, v in UVS for i, j in IJS]
    p_values = [solver.Value(p[i, j, u, v, w]) for i, j in IJS for u, v, w in TRIPLES]
    payload: dict[str, object] = {
        "schema": SCHEMA, "golf_sha256": golf_sha256(golf), "counts": stats,
        "n_order": "uv-major then ij-major, lexicographic combinations", "n_values": n_values,
        "p_order": "ij-major then uvw-major, lexicographic combinations", "p_values": p_values,
    }
    canonical = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    payload["sha256_without_hash"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--no-presolve", action="store_true", help="bounded search diagnostic; does not change the model")
    args = parser.parse_args()
    model, n, p, golf, stats = build_model()
    if args.audit_only:
        print(json.dumps({"schema": SCHEMA, "golf_sha256": golf_sha256(golf), "counts": stats}, indent=2, sort_keys=True))
        return
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    if args.no_presolve:
        solver.parameters.cp_model_presolve = False
    status = solver.Solve(model)
    result: dict[str, object] = {"schema": SCHEMA, "status": solver.StatusName(status), "golf_sha256": golf_sha256(golf), "counts": stats, "no_presolve": args.no_presolve, "wall_time_seconds": solver.WallTime(), "branches": solver.NumBranches(), "conflicts": solver.NumConflicts()}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        payload = certificate_payload(solver, n, p, golf, stats)
        from verify_radius5_golf_joint import verify_payload
        verify_payload(payload, semantic_ball=True)
        result["certificate_verified"] = True
        result["certificate_sha256_without_hash"] = payload["sha256_without_hash"]
        if args.certificate is not None:
            args.certificate.parent.mkdir(parents=True, exist_ok=True)
            args.certificate.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

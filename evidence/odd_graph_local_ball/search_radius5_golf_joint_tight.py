#!/usr/bin/env python3
"""Exact joint radius-five search strengthened by forced triangle congruences.

The added constraints are consequences of the existing P constraints: for
every ij and colour x, the residual graph intended for x-coloured triples
must have an even degree at every vertex and an edge count divisible by 3.
They therefore do not alter SAT instances; they expose propagation that is
otherwise hidden behind the 58,800 triple variables.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model

from search_radius5_golf_joint import (
    COLORS,
    FINITE,
    IJS,
    SQUARES,
    UVS,
    build_model,
    certificate_payload,
    golf_sha256,
    n_allowed,
)
from verify_radius5_golf_joint import verify_payload
from global_latin_radius4_certificate import construct_one_n


def _m_covers(golf, i: int, u: int, x: int) -> int:
    """Whether the x-matching of M_i covers u (direct, no formula assumed)."""
    return int(any(golf[i][min(u, v)][max(u, v)] == x for v in FINITE if v != u))


def add_forced_triangle_congruences(model: cp_model.CpModel, n, golf):
    """Add the edge-count and degree-parity conditions from radius5_reduction."""
    use = {}
    by_ij_colour = defaultdict(list)
    by_ij_colour_point = defaultdict(list)
    for uv in UVS:
        u, v = uv
        for ij in IJS:
            i, j = ij
            domain = n_allowed(golf, i, uv) & n_allowed(golf, j, uv)
            for x in domain:
                bit = model.NewBoolVar(f"n_is_{u}_{v}_{i}_{j}_{x}")
                model.Add(n[uv + ij] == x).OnlyEnforceIf(bit)
                model.Add(n[uv + ij] != x).OnlyEnforceIf(bit.Not())
                use[uv + ij + (x,)] = bit
                by_ij_colour[ij + (x,)].append(bit)
                by_ij_colour_point[ij + (x, u)].append(bit)
                by_ij_colour_point[ij + (x, v)].append(bit)
    for ij in IJS:
        i, j = ij
        for x in COLORS:
            # Equation (2): t_infty = 2 mod 3, t_finite = 1 mod 3.
            count = by_ij_colour[ij + (x,)]
            quotient = model.NewIntVar(0, 40, f"count_q_{i}_{j}_{x}")
            model.Add(sum(count) == (2 if x == 16 else 1) + 3 * quotient)
            # Equation (3), re-derived directly from the fixed M tables.
            for u in FINITE:
                parity = (1 + _m_covers(golf, i, u, x) + _m_covers(golf, j, u, x)) % 2
                incident = by_ij_colour_point[ij + (x, u)]
                quotient = model.NewIntVar(0, 8, f"degree_q_{i}_{j}_{u}_{x}")
                model.Add(sum(incident) == parity + 2 * quotient)
    return len(use)


def add_audited_n_hints(model: cp_model.CpModel, n, golf) -> None:
    for uv in UVS:
        table, _allowed = construct_one_n(golf, *uv)
        for ij in IJS:
            model.AddHint(n[uv + ij], table[ij])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--hint-audited-n", action="store_true")
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    model, n, p, golf, stats = build_model()
    stats = dict(stats)
    stats["triangle_congruence_literals"] = add_forced_triangle_congruences(model, n, golf)
    if args.hint_audited_n:
        add_audited_n_hints(model, n, golf)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    if args.hint_audited_n:
        solver.parameters.repair_hint = True
        solver.parameters.hint_conflict_limit = 100_000
    status = solver.Solve(model)
    result: dict[str, object] = {
        "schema": "odd-graph-o16-radius5-fixed-golf-joint-v1",
        "search": "joint-plus-forced-triangle-congruences",
        "hint_audited_n": args.hint_audited_n,
        "status": solver.StatusName(status),
        "golf_sha256": golf_sha256(golf),
        "counts": stats,
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        payload = certificate_payload(solver, n, p, golf, {k: v for k, v in stats.items() if k != "triangle_congruence_literals"})
        verify_payload(payload, semantic_ball=True)
        result["certificate_verified"] = True
        result["certificate_sha256_without_hash"] = payload["sha256_without_hash"]
        if args.certificate is not None:
            args.certificate.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

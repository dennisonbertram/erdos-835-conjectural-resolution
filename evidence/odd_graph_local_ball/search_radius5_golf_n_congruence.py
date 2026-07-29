#!/usr/bin/env python3
"""Find a full fixed-golf N layer satisfying the forced radius-five trace.

This is an intermediate exact search only.  It omits P and therefore never
claims a radius-five ball; its output is a coherent N-layer hint for the
complete joint model.  Every constraint retained here is an N constraint of
the complete model or a consequence forced by its P triangle decomposition.
In particular, every fixed ``ij,u`` trace is all-different, as proved without
any golf or cyclic assumption in ``radius5_minimal_trace_forced.md``.
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
from global_latin_radius4_certificate import construct_one_n

SCHEMA = "odd-graph-o16-radius5-fixed-golf-n-forced-trace-v2"


def add_forced_trace_stars(model: cp_model.CpModel, n) -> int:
    """Add the 105*16 lossless all-different consequences on the N layer."""

    count = 0
    for ij in IJS:
        for u in range(16):
            model.AddAllDifferent(
                [
                    n[(min(u, v), max(u, v)) + ij]
                    for v in range(16)
                    if v != u
                ]
            )
            count += 1
    assert count == 1_680
    return count


def build_n_model(include_redundant_congruences: bool = False):
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
    trace_star_count = add_forced_trace_stars(model, n)
    # The exact trace stars already force |D_infinity|=8 and |D_x|=7, with
    # the parity pattern from radius5_minimal_trace_forced.md.  Hence the
    # older reified mod-3/parity constraints are logically redundant.  Keep
    # them as an optional propagation experiment, not in the lean default.
    literal_count = (
        add_forced_triangle_congruences(model, n, golf)
        if include_redundant_congruences
        else 0
    )
    return model, n, golf, literal_count, trace_star_count


def make_payload(solver, n, golf, literal_count, trace_star_count):
    payload = {
        "schema": SCHEMA,
        "golf_sha256": golf_sha256(golf),
        "n_order": "uv-major then ij-major, lexicographic combinations",
        "n_values": [solver.Value(n[uv + ij]) for uv in UVS for ij in IJS],
        "triangle_congruence_literals": literal_count,
        "forced_trace_stars": trace_star_count,
    }
    payload["sha256_without_hash"] = hashlib.sha256((json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
    return payload


def add_audited_radius4_hints(model: cp_model.CpModel, n, golf) -> int:
    """Hint the independently solved radius-four N tables before trace repair."""

    count = 0
    for uv in UVS:
        table, _allowed = construct_one_n(golf, *uv)
        for ij in IJS:
            model.AddHint(n[uv + ij], table[ij])
            count += 1
    assert count == 12_600
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=120.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--redundant-congruences",
        action="store_true",
        help=(
            "Also instantiate the older 143,640 reified parity/mod-3 literals. "
            "They are consequences of the exact forced trace and may slow presolve."
        ),
    )
    parser.add_argument(
        "--hint-audited-n",
        action="store_true",
        help=(
            "Use the verified independent radius-four N tables as a repair hint. "
            "The hint need not satisfy the forced trace and is not fixed."
        ),
    )
    args = parser.parse_args()
    model, n, golf, literal_count, trace_star_count = build_n_model(
        args.redundant_congruences
    )
    hinted_values = (
        add_audited_radius4_hints(model, n, golf)
        if args.hint_audited_n
        else 0
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    if args.hint_audited_n:
        solver.parameters.repair_hint = True
        solver.parameters.hint_conflict_limit = 1_000_000
    status = solver.Solve(model)
    result = {
        "schema": SCHEMA,
        "status": solver.StatusName(status),
        "golf_sha256": golf_sha256(golf),
        "triangle_congruence_literals": literal_count,
        "forced_trace_stars": trace_star_count,
        "hint_audited_n": args.hint_audited_n,
        "hinted_values": hinted_values,
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        payload = make_payload(solver, n, golf, literal_count, trace_star_count)
        result["n_sha256_without_hash"] = payload["sha256_without_hash"]
        if args.output:
            args.output.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

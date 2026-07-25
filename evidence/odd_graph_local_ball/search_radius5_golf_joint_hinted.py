#!/usr/bin/env python3
"""Hinted exact search for the fixed-golf joint radius-five model.

This is deliberately only a search front end.  It imports the complete
model from ``search_radius5_golf_joint.py`` unchanged, then supplies the
independently audited radius-four N tables as a CP-SAT solution hint.  The
hint is known not to extend at one P layer, so it is not a witness; it merely
gives the solver a coherent starting point from which to repair N/P jointly.
Any returned certificate is checked by the independent semantic verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from ortools.sat.python import cp_model

from search_radius5_golf_joint import (
    IJS,
    UVS,
    build_model,
    certificate_payload,
    golf_sha256,
)
from verify_radius5_golf_joint import verify_payload
from global_latin_radius4_certificate import construct_one_n


def add_audited_n_hints(model: cp_model.CpModel, n, golf) -> None:
    """Seed every N variable with the separately verified radius-4 table."""
    for uv in UVS:
        table, _allowed = construct_one_n(golf, *uv)
        for ij in IJS:
            model.AddHint(n[uv + ij], table[ij])


def add_serialized_n_hints(model: cp_model.CpModel, n, golf, source: Path) -> str:
    """Load a self-hashed N-only congruence certificate as a nonbinding hint."""
    payload = json.loads(source.read_text(encoding="utf-8"))
    unhashed = dict(payload)
    recorded = unhashed.pop("sha256_without_hash", None)
    expected = hashlib.sha256((json.dumps(unhashed, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
    if (payload.get("schema") != "odd-graph-o16-radius5-fixed-golf-n-congruence-v1"
            or recorded != expected or payload.get("golf_sha256") != golf_sha256(golf)):
        raise ValueError("N hint has the wrong self-hash or golf chart")
    values = payload.get("n_values")
    if not isinstance(values, list) or len(values) != len(UVS) * len(IJS):
        raise ValueError("N hint has wrong vector length")
    for value, uv, ij in zip(values, (uv for uv in UVS for _ij in IJS), (ij for _uv in UVS for ij in IJS)):
        if not isinstance(value, int):
            raise ValueError("N hint contains a noninteger")
        model.AddHint(n[uv + ij], value)
    return recorded


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--n-hint", type=Path, help="self-hashed N-only congruence witness to use as a repair hint")
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    model, n, p, golf, stats = build_model()
    if args.n_hint is None:
        hint_source = "audited-radius4-N"
        add_audited_n_hints(model, n, golf)
    else:
        hint_source = "N-only-congruence:" + add_serialized_n_hints(model, n, golf, args.n_hint)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    solver.parameters.repair_hint = True
    solver.parameters.hint_conflict_limit = 100_000
    status = solver.Solve(model)
    result: dict[str, object] = {
        "schema": "odd-graph-o16-radius5-fixed-golf-joint-v1",
        "search": "audited-radius4-N-hint-repair",
        "hint_source": hint_source,
        "status": solver.StatusName(status),
        "golf_sha256": golf_sha256(golf),
        "counts": stats,
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        payload = certificate_payload(solver, n, p, golf, stats)
        verify_payload(payload, semantic_ball=True)
        result["certificate_verified"] = True
        result["certificate_sha256_without_hash"] = payload["sha256_without_hash"]
        if args.certificate is not None:
            args.certificate.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

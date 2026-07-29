#!/usr/bin/env python3
"""Decode a cadical model of the centre-0 star CNF into a phase witness.

Reads cadical's ``v`` lines, rebuilds the exact variable layout by calling
``build_cnf`` from the repo encoder (never edited), and writes a JSON witness

    {"centre": 0, "convention": ..., "rows": {"j": [s_0, ..., s_39]}}

where s is the translate amount: triple = translate(REPRESENTATIVES[k], s).
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_BALL = Path(
    "/Users/dennison/Documents/Math Problem/evidence/odd_graph_local_ball"
)
sys.path.insert(0, str(REPO_BALL))

from search_radius5_golf_cyclic_star_sat import build_cnf  # noqa: E402


def parse_model(log_path: Path) -> set[int]:
    positive = set()
    for line in log_path.read_text().splitlines():
        if line.startswith("v "):
            for token in line[2:].split():
                literal = int(token)
                if literal > 0:
                    positive.add(literal)
    if not positive:
        raise SystemExit("no v-lines found in solver log")
    return positive


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("solver_log", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--centre", type=int, default=0)
    args = parser.parse_args()

    clauses, variable, domains, pairs, stats = build_cnf(args.centre)
    positive = parse_model(args.solver_log)

    rows: dict[str, list[int]] = {}
    for fixed_pair in pairs:
        outer = fixed_pair[0] if fixed_pair[1] == args.centre else fixed_pair[1]
        selected_row = []
        for orbit_index in range(40):
            chosen = [
                shift
                for shift in sorted(domains[fixed_pair + (orbit_index,)])
                if variable[fixed_pair, orbit_index, shift] in positive
            ]
            if len(chosen) != 1:
                raise SystemExit(
                    f"cell {fixed_pair},{orbit_index} selects {len(chosen)} phases"
                )
            selected_row.append(chosen[0])
        rows[str(outer)] = selected_row

    witness = {
        "centre": args.centre,
        "convention": (
            "rows[j][k] = s with selected triple = "
            "translate(REPRESENTATIVES[k], s) for pair (centre, j)"
        ),
        "rows": rows,
    }
    encoded = (json.dumps(witness, indent=2, sort_keys=True) + "\n").encode()
    args.output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "status": "DECODED",
                "witness_sha256": hashlib.sha256(encoded).hexdigest(),
                "counts": stats,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

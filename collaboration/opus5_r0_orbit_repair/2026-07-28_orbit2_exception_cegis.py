#!/usr/bin/env python3
"""Switch CEGIS for every orbit-2 doubled-root and 03 obstruction type."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def load(name: str, filename: str):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SWITCH = load("orbit2_switch", "2026-07-28_orbit2_switch_cegis.py")
CENSUS = load("orbit2_census", "2026-07-28_orbit2_obstruction_census.py")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--jsonl", type=Path)
    parser.add_argument("--without-pair-compatibility", action="store_true")
    args = parser.parse_args()

    summary, records = CENSUS.census_records()
    obstructions = [record for record in records if not record["colourable"]]
    assert len(obstructions) == (
        summary["leaf_at_three_unlabeled"]
        + summary["double_uncolourable_directed_root_types"]
    )

    cnf, deleted = SWITCH.build_base(
        pair_compatible=not args.without_pair_compatibility
    )
    output = None
    if args.jsonl:
        args.jsonl.parent.mkdir(parents=True, exist_ok=True)
        output = args.jsonl.open("w", encoding="utf-8")
    try:
        for record in obstructions:
            factor = frozenset(tuple(edge) for edge in record["factor"])
            result = SWITCH.solve_factor_case(
                cnf,
                deleted,
                record["case"],
                factor,
                args.output_dir,
            )
            result["branch"] = record["branch"]
            result["graph6"] = record["graph6"]
            result["root"] = record["root"]
            line = json.dumps(result, sort_keys=True)
            print(line, flush=True)
            if output:
                output.write(line + "\n")
                output.flush()
    finally:
        if output:
            output.close()


if __name__ == "__main__":
    main()

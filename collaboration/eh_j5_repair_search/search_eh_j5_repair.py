#!/usr/bin/env python3
"""Search for a five-colouring after dropping three EH SQS(20)s.

The authenticated Etzion--Hartman seed contains fifteen disjoint complete
SQS(20)s, labelled 0,...,14.  If exactly three of them are dropped, the
remaining 1,425 blocks form a five-fold leave: every triple has exactly five
extensions in the leave.  A proper five-colouring of that leave, together
with the twelve retained systems, is exactly an LS(3,4,20).

CP-SAT INFEASIBLE/UNKNOWN output is reconnaissance, not a portable
nonexistence certificate.  A FEASIBLE/OPTIMAL output is written as a complete
4,845-row witness and can be checked without OR-Tools by
``verify_eh_j5_witness.py``.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from ortools.sat.python import cp_model


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
FULL_SOURCE = REPO / "evidence" / "ls_3_4_20_eh15_seed.txt"
PARTIAL_SOURCE = REPO / "evidence" / "ls_3_4_20_eh15_partial.txt"
FULL_SHA256 = "b1ea090d3e3b88366c87e95660c1c82a406d2c3b100cc1d39bcc2c7e8fde47f9"
PARTIAL_SHA256 = "bca36685508a4cf396cec015c2cfe06239f018b1dba32cff41ea11ee6c601f33"

POINTS = tuple(range(20))
BLOCKS = tuple(itertools.combinations(POINTS, 4))
TRIPLES = tuple(itertools.combinations(POINTS, 3))
REFERENCE_TRIPLE = (0, 1, 2)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_rows(path: Path, expected_sha256: str) -> dict[tuple[int, ...], int]:
    """Strictly load an authenticated, lexicographically ordered seed."""

    actual = digest(path)
    if actual != expected_sha256:
        raise AssertionError(
            f"{path}: SHA-256 {actual} != authenticated {expected_sha256}"
        )
    rows = path.read_text(encoding="ascii").splitlines()
    if len(rows) != len(BLOCKS):
        raise AssertionError(f"{path}: expected 4,845 rows")
    result: dict[tuple[int, ...], int] = {}
    for expected_block, raw in zip(BLOCKS, rows):
        fields = tuple(map(int, raw.split()))
        if len(fields) != 5 or fields[:4] != expected_block:
            raise AssertionError(
                f"{path}: malformed/out-of-order row for {expected_block}"
            )
        result[expected_block] = fields[4]
    return result


def verify_sources(
    full: dict[tuple[int, ...], int],
    partial: dict[tuple[int, ...], int],
) -> tuple[tuple[frozenset[tuple[int, ...]], ...], int]:
    """Audit the fifteen systems and the 72-hole proper partial."""

    if Counter(full.values()) != Counter({label: 285 for label in range(17)}):
        raise AssertionError("full seed is not balanced into 17 classes")
    systems = tuple(
        frozenset(block for block, label in full.items() if label == colour)
        for colour in range(15)
    )
    used: set[tuple[int, ...]] = set()
    for colour, system in enumerate(systems):
        if len(system) != 285 or used.intersection(system):
            raise AssertionError(f"source colour {colour} is not disjoint")
        counts: Counter[tuple[int, ...]] = Counter(
            triple for block in system for triple in itertools.combinations(block, 3)
        )
        if set(counts) != set(TRIPLES) or set(counts.values()) != {1}:
            raise AssertionError(f"source colour {colour} is not an SQS(20)")
        used.update(system)

    expected_partial_counts = Counter({label: 285 for label in range(15)})
    expected_partial_counts.update({15: 249, 16: 249, -1: 72})
    if Counter(partial.values()) != expected_partial_counts:
        raise AssertionError("partial source has unexpected colour counts")
    for block in BLOCKS:
        if full[block] < 15 and partial[block] != full[block]:
            raise AssertionError("partial source changed a complete EH system")

    for triple in TRIPLES:
        assigned = [
            partial[tuple(sorted((*triple, point)))]
            for point in POINTS
            if point not in triple
        ]
        assigned = [value for value in assigned if value >= 0]
        if len(assigned) != len(set(assigned)):
            raise AssertionError(f"partial conflict over triple {triple}")
    return systems, 72


def build_leave(
    systems: tuple[frozenset[tuple[int, ...]], ...],
    dropped: tuple[int, int, int],
) -> tuple[
    tuple[tuple[int, ...], ...],
    dict[tuple[int, ...], tuple[int, ...]],
]:
    kept = [system for colour, system in enumerate(systems) if colour not in dropped]
    used = set().union(*kept)
    residual = tuple(block for block in BLOCKS if block not in used)
    if len(residual) != 5 * 285:
        raise AssertionError("five-fold leave does not have 1,425 blocks")

    residual_index = {block: index for index, block in enumerate(residual)}
    by_triple: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for block, index in residual_index.items():
        for triple in itertools.combinations(block, 3):
            by_triple[triple].append(index)
    if set(by_triple) != set(TRIPLES):
        raise AssertionError("five-fold leave misses a triple")
    if set(map(len, by_triple.values())) != {5}:
        raise AssertionError("leave is not five-fold")
    return residual, {triple: tuple(rows) for triple, rows in by_triple.items()}


def reference_labelling(
    residual: tuple[tuple[int, ...], ...],
    by_triple: dict[tuple[int, ...], tuple[int, ...]],
    full: dict[tuple[int, ...], int],
    dropped: tuple[int, int, int],
) -> tuple[tuple[int, ...], dict[int, int]]:
    """Map solver colours to original labels using the reference star."""

    labels = tuple(full[residual[row]] for row in by_triple[REFERENCE_TRIPLE])
    expected = set(dropped) | {15, 16}
    if len(labels) != 5 or set(labels) != expected:
        raise AssertionError(
            "reference star is not rainbow in the authenticated full seed"
        )
    return labels, {label: colour for colour, label in enumerate(labels)}


def internal_verify(
    values: dict[tuple[int, ...], int],
    systems: tuple[frozenset[tuple[int, ...]], ...],
    dropped: tuple[int, int, int],
) -> None:
    """Check a found witness independently of the model's constraints."""

    if set(values) != set(BLOCKS):
        raise AssertionError("candidate does not assign every block")
    if not set(values.values()) <= set(range(17)):
        raise AssertionError("candidate has a label outside 0,...,16")
    for triple in TRIPLES:
        star = [
            values[tuple(sorted((*triple, point)))]
            for point in POINTS
            if point not in triple
        ]
        if set(star) != set(range(17)):
            raise AssertionError(f"candidate conflict over triple {triple}")
    for colour, system in enumerate(systems):
        if colour not in dropped and any(values[block] != colour for block in system):
            raise AssertionError(f"candidate changed retained system {colour}")


def write_witness(path: Path, values: dict[tuple[int, ...], int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join("{} {} {} {} {}\n".format(*block, values[block]) for block in BLOCKS)
    path.write_text(text, encoding="ascii")


def solve_case(
    full: dict[tuple[int, ...], int],
    partial: dict[tuple[int, ...], int],
    systems: tuple[frozenset[tuple[int, ...]], ...],
    dropped: tuple[int, int, int],
    seconds: float,
    workers: int,
    seed: int,
    witness_dir: Path,
    log_search: bool,
    minimize_changes: bool,
) -> dict[str, object]:
    residual, by_triple = build_leave(systems, dropped)
    solver_to_label, label_to_solver = reference_labelling(
        residual, by_triple, full, dropped
    )

    model = cp_model.CpModel()
    colour = [model.new_int_var(0, 4, f"c_{row}") for row in range(len(residual))]
    for rows in by_triple.values():
        model.add_all_different([colour[row] for row in rows])

    for value, row in enumerate(by_triple[REFERENCE_TRIPLE]):
        model.add(colour[row] == value)

    hinted: list[tuple[int, int]] = []
    for row, block in enumerate(residual):
        source_label = partial[block]
        if source_label in label_to_solver:
            hinted.append((row, label_to_solver[source_label]))
            model.add_hint(colour[row], label_to_solver[source_label])
    if len(hinted) != len(residual) - 72:
        raise AssertionError("proper partial did not leave exactly 72 hints open")

    if minimize_changes:
        changed = []
        for row, hint in hinted:
            difference = model.new_bool_var(f"d_{row}")
            model.add(colour[row] == hint).only_enforce_if(difference.Not())
            model.add(colour[row] != hint).only_enforce_if(difference)
            changed.append(difference)
        model.minimize(sum(changed))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    solver.parameters.log_search_progress = log_search
    solver.parameters.symmetry_level = 3

    started = time.time()
    status = solver.solve(model)
    elapsed = time.time() - started
    status_name = solver.status_name(status)
    record: dict[str, object] = {
        "schema": 1,
        "drop": list(dropped),
        "status": status_name,
        "portable_unsat_certificate": False,
        "seconds_limit": seconds,
        "workers": workers,
        "seed": seed,
        "minimize_changes": minimize_changes,
        "wall_seconds": round(solver.wall_time, 6),
        "elapsed_seconds": round(elapsed, 6),
        "conflicts": solver.num_conflicts,
        "branches": solver.num_branches,
        "leave_blocks": len(residual),
        "triple_stars": len(by_triple),
        "hinted_blocks": len(hinted),
        "unhinted_blocks": len(residual) - len(hinted),
        "solver_to_output_label": list(solver_to_label),
        "full_source_sha256": FULL_SHA256,
        "partial_source_sha256": PARTIAL_SHA256,
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        values = {
            block: label
            for label, system in enumerate(systems)
            if label not in dropped
            for block in system
        }
        for row, block in enumerate(residual):
            values[block] = solver_to_label[solver.value(colour[row])]
        internal_verify(values, systems, dropped)
        witness = witness_dir / ("ls3420_drop_" + "_".join(map(str, dropped)) + ".txt")
        write_witness(witness, values)
        record["witness"] = str(witness)
        record["witness_sha256"] = digest(witness)
        if minimize_changes:
            record["changed_hinted_blocks"] = round(solver.objective_value)
    return record


def canonical_case(values: Iterable[int]) -> tuple[int, int, int]:
    case = tuple(sorted(values))
    if len(case) != 3 or len(set(case)) != 3 or case[0] < 0 or case[-1] >= 15:
        raise argparse.ArgumentTypeError(
            "each drop case needs three distinct labels in 0,...,14"
        )
    return case


def parse_case(text: str) -> tuple[int, int, int]:
    try:
        return canonical_case(map(int, text.split(",")))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "case must be comma-separated, for example 1,3,8"
        ) from exc


def case_order(
    requested: list[tuple[int, int, int]],
    sweep: bool,
    seed: int,
) -> list[tuple[int, int, int]]:
    cases: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int, int]] = set()
    for case in requested:
        if case not in seen:
            seen.add(case)
            cases.append(case)
    if sweep:
        # Interleave the lexicographic list deterministically.  Multiplication
        # by 173 permutes the 455 indices and samples the whole construction
        # before returning to neighbouring cases.
        all_cases = list(itertools.combinations(range(15), 3))
        offset = seed % len(all_cases)
        for step in range(len(all_cases)):
            case = all_cases[(offset + 173 * step) % len(all_cases)]
            if case not in seen:
                seen.add(case)
                cases.append(case)
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--case",
        type=parse_case,
        action="append",
        default=[],
        help="drop case C1,C2,C3; may be repeated",
    )
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="after explicit cases, sample all 455 drop triples",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="maximum number of cases this invocation (0 means all)",
    )
    parser.add_argument("--seconds", type=float, default=30.0)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--log-search", action="store_true")
    parser.add_argument(
        "--minimize-changes",
        action="store_true",
        help="minimize changes from the authenticated 72-hole proper partial",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=HERE / "reconnaissance.jsonl",
    )
    parser.add_argument(
        "--witness-dir",
        type=Path,
        default=HERE / "witnesses",
    )
    args = parser.parse_args()
    if not args.case and not args.sweep:
        parser.error("supply at least one --case or --sweep")
    if args.seconds <= 0 or not 1 <= args.workers <= 2 or args.limit < 0:
        parser.error("require seconds>0, 1<=workers<=2, and limit>=0")

    full = load_rows(FULL_SOURCE, FULL_SHA256)
    partial = load_rows(PARTIAL_SOURCE, PARTIAL_SHA256)
    systems, holes = verify_sources(full, partial)
    print(
        f"source audit PASS: 15 disjoint SQS(20)s; proper partial has {holes} holes",
        flush=True,
    )

    cases = case_order(args.case, args.sweep, args.seed)
    if args.limit:
        cases = cases[: args.limit]
    args.results.parent.mkdir(parents=True, exist_ok=True)
    found = False
    with args.results.open("a", encoding="utf-8") as output:
        for case_number, dropped in enumerate(cases, 1):
            record = solve_case(
                full=full,
                partial=partial,
                systems=systems,
                dropped=dropped,
                seconds=args.seconds,
                workers=args.workers,
                seed=args.seed + case_number - 1,
                witness_dir=args.witness_dir,
                log_search=args.log_search,
                minimize_changes=args.minimize_changes,
            )
            output.write(json.dumps(record, sort_keys=True) + "\n")
            output.flush()
            print(
                f"[{case_number}/{len(cases)}] "
                f"drop={dropped} status={record['status']} "
                f"wall={record['wall_seconds']}s "
                f"conflicts={record['conflicts']} "
                f"branches={record['branches']}",
                flush=True,
            )
            if "witness" in record:
                print(f"EXACT WITNESS: {record['witness']}", flush=True)
                found = True
                break
    if not found:
        print(
            "No witness found. INFEASIBLE/UNKNOWN rows are reconnaissance "
            "only; no portable nonexistence conclusion is claimed.",
            flush=True,
        )


if __name__ == "__main__":
    main()

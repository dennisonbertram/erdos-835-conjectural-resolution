#!/usr/bin/env python3
"""Adversarial exact search at the coordinated-nine frontier.

A class-B support instance on K_13 is represented by seventeen complement
sets.  For profile r, their sizes are

    5^(7+r), 3^(10-2r), 1^r,

and every vertex occurs in exactly five complements.  The corresponding
supports have sizes 8, 10, and 12.

For each fixed instance, this program computes the exact maximum number of
pairwise edge-disjoint support-perfect matchings.  It offers three campaigns:

* random: deterministic two-switch walks through row-regular instances;
* duplicates: highly duplicated instances, generated from multiplicity
  partitions with at most five copies of one complement;
* certificates: the six dead-prefix support instances already committed in
  collaboration/first_lift_global_theorem/.

OR-Tools CP-SAT is required.  "OPTIMAL" is an exact result for the fixed
instance.  A finite campaign is not an exhaustive theorem over all instances.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import time
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from types import ModuleType
from typing import Iterable

from ortools.sat.python import cp_model


VERTICES = tuple(range(13))
VERTEX_SET = frozenset(VERTICES)
EDGES = tuple(combinations(VERTICES, 2))

Complements = tuple[frozenset[int], ...]
Matching = frozenset[tuple[int, int]]


def profile_sizes(r: int) -> tuple[int, ...]:
    """Return complement sizes for the class-B profile r."""
    if r not in range(6):
        raise ValueError(f"profile r must lie in 0..5, got {r}")
    return (5,) * (7 + r) + (3,) * (10 - 2 * r) + (1,) * r


def validate_instance(complements: Complements, r: int) -> None:
    """Check the exact class-B column and row conditions."""
    assert len(complements) == 17
    assert Counter(map(len, complements)) == Counter(profile_sizes(r))
    assert all(current <= VERTEX_SET for current in complements)
    assert all(
        sum(vertex in current for current in complements) == 5
        for vertex in VERTICES
    )


def initial_matrix(r: int) -> Complements:
    """Construct one deterministic row-regular matrix for profile r."""
    model = cp_model.CpModel()
    x = {
        (colour, vertex): model.new_bool_var(f"x_{colour}_{vertex}")
        for colour in range(17)
        for vertex in VERTICES
    }
    for colour, size in enumerate(profile_sizes(r)):
        model.add(sum(x[colour, vertex] for vertex in VERTICES) == size)
    for vertex in VERTICES:
        model.add(sum(x[colour, vertex] for colour in range(17)) == 5)

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 8350 + r
    status = solver.solve(model)
    if status != cp_model.OPTIMAL:
        raise RuntimeError(
            f"failed to construct initial profile r={r}: "
            f"{solver.status_name(status)}"
        )
    result = tuple(
        frozenset(
            vertex
            for vertex in VERTICES
            if solver.value(x[colour, vertex])
        )
        for colour in range(17)
    )
    validate_instance(result, r)
    return result


def two_switch(
    complements: Complements,
    rng: random.Random,
    attempts: int = 100,
) -> Complements:
    """Apply one row- and column-sum-preserving 2-switch when possible."""
    rows = [set(current) for current in complements]
    for _ in range(attempts):
        left, right = rng.sample(range(17), 2)
        left_only = tuple(rows[left] - rows[right])
        right_only = tuple(rows[right] - rows[left])
        if not left_only or not right_only:
            continue
        first = rng.choice(left_only)
        second = rng.choice(right_only)
        rows[left].remove(first)
        rows[left].add(second)
        rows[right].remove(second)
        rows[right].add(first)
        return tuple(frozenset(current) for current in rows)
    return complements


def randomize(
    complements: Complements,
    rng: random.Random,
    steps: int,
) -> Complements:
    """Take a deterministic-seed Markov walk of 2-switches."""
    result = complements
    for _ in range(steps):
        result = two_switch(result, rng)
    return result


def verify_matchings(
    complements: Complements,
    matchings: tuple[Matching, ...],
    selected: tuple[bool, ...],
) -> None:
    """Independently verify the literal packing returned by CP-SAT."""
    assert len(complements) == len(matchings) == len(selected) == 17
    used: set[tuple[int, int]] = set()
    for colour, (complement, matching, is_selected) in enumerate(
        zip(complements, matchings, selected)
    ):
        support = VERTEX_SET - complement
        if not is_selected:
            assert not matching
            continue
        endpoints = [
            vertex
            for edge in matching
            for vertex in edge
        ]
        assert len(matching) == len(support) // 2, colour
        assert len(endpoints) == len(set(endpoints)), colour
        assert frozenset(endpoints) == support, colour
        assert used.isdisjoint(matching), colour
        used.update(matching)


def packing_number(
    complements: Complements,
    seconds: float,
) -> tuple[
    int | None,
    tuple[Matching, ...] | None,
    str,
    float,
]:
    """Solve the exact packing number of one fixed support instance."""
    supports = tuple(VERTEX_SET - current for current in complements)
    model = cp_model.CpModel()
    selected = [
        model.new_bool_var(f"selected_{colour}")
        for colour in range(17)
    ]
    use = {
        (colour, edge): model.new_bool_var(
            f"use_{colour}_{edge[0]}_{edge[1]}"
        )
        for colour, support in enumerate(supports)
        for edge in combinations(sorted(support), 2)
    }

    # A selected colour has degree exactly one at every support vertex;
    # an unselected colour uses no edge.
    for colour, support in enumerate(supports):
        for vertex in support:
            model.add(
                sum(
                    use[colour, tuple(sorted((vertex, other)))]
                    for other in support
                    if other != vertex
                )
                == selected[colour]
            )

    # The colour matchings must be pairwise edge-disjoint.
    for edge in EDGES:
        model.add(
            sum(
                use[colour, edge]
                for colour, support in enumerate(supports)
                if edge[0] in support and edge[1] in support
            )
            <= 1
        )

    model.maximize(sum(selected))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 8359
    status = solver.solve(model)
    status_name = solver.status_name(status)
    if status != cp_model.OPTIMAL:
        return None, None, status_name, solver.wall_time

    optimum = int(round(solver.objective_value))
    selected_values = tuple(
        bool(solver.value(current))
        for current in selected
    )
    matchings = tuple(
        frozenset(
            edge
            for edge in combinations(sorted(support), 2)
            if solver.value(use[colour, edge])
        )
        for colour, support in enumerate(supports)
    )
    assert sum(selected_values) == optimum
    verify_matchings(complements, matchings, selected_values)

    # The profile has total matching demand 78.  Thus an optimum of 17
    # necessarily partitions all edges of K_13.
    if optimum == 17:
        union = frozenset().union(*matchings)
        assert sum(map(len, matchings)) == len(union) == len(EDGES) == 78
        assert union == frozenset(EDGES)

    return optimum, matchings, status_name, solver.wall_time


def statistics(complements: Complements) -> dict[str, int]:
    """Return structural statistics used by the adversarial campaign."""
    return {
        "duplicate_columns": 17 - len(set(complements)),
        "max_pair_overlap": max(
            len(complements[left] & complements[right])
            for left, right in combinations(range(17), 2)
        ),
        "distinct_vertex_rows": len(
            {
                tuple(vertex in current for current in complements)
                for vertex in VERTICES
            }
        ),
    }


def serialized(complements: Complements) -> list[list[int]]:
    return [sorted(current) for current in complements]


def solve_and_record(
    complements: Complements,
    r: int,
    seconds: float,
    label: str,
) -> dict[str, object]:
    validate_instance(complements, r)
    optimum, matchings, status, wall = packing_number(complements, seconds)
    record: dict[str, object] = {
        "label": label,
        "r": r,
        "status": status,
        "optimum": optimum,
        "wall_seconds": wall,
        **statistics(complements),
    }
    if optimum is not None and optimum <= 8:
        # This is enough to replay the candidate exactly.  A publication-grade
        # upper-bound certificate should additionally be emitted by a proof-
        # logging SAT backend before treating it as a mathematical counterexample.
        record["counterexample_complements"] = serialized(complements)
        record["optimum_matchings"] = [
            sorted(list(edge) for edge in matching)
            for matching in (matchings or ())
        ]
    return record


def summarize(records: list[dict[str, object]]) -> dict[str, object]:
    optima = Counter(record["optimum"] for record in records)
    statuses = Counter(str(record["status"]) for record in records)
    exact_records = [
        record
        for record in records
        if record["optimum"] is not None
    ]
    return {
        "tested": len(records),
        "statuses": dict(sorted(statuses.items())),
        "optima": {
            str(key): value
            for key, value in sorted(
                optima.items(),
                key=lambda item: (
                    item[0] is None,
                    -1 if item[0] is None else int(item[0]),
                ),
            )
        },
        "max_wall_seconds": max(
            (float(record["wall_seconds"]) for record in records),
            default=0.0,
        ),
        "max_duplicate_columns": max(
            (
                int(record["duplicate_columns"])
                for record in exact_records
            ),
            default=0,
        ),
        "max_pair_overlap": max(
            (
                int(record["max_pair_overlap"])
                for record in exact_records
            ),
            default=0,
        ),
        "min_distinct_vertex_rows": min(
            (
                int(record["distinct_vertex_rows"])
                for record in exact_records
            ),
            default=0,
        ),
    }


def random_campaign(args: argparse.Namespace) -> list[dict[str, object]]:
    rng = random.Random(args.seed)
    records: list[dict[str, object]] = []
    for r in args.profiles:
        complements = initial_matrix(r)
        seen: set[tuple[tuple[int, ...], ...]] = set()
        profile_records = []
        attempts = 0
        while len(profile_records) < args.samples:
            attempts += 1
            complements = randomize(complements, rng, args.switches)
            key = tuple(tuple(sorted(current)) for current in complements)
            if key in seen:
                if attempts > 10 * args.samples:
                    raise RuntimeError(
                        f"too many duplicate Markov states for r={r}"
                    )
                continue
            seen.add(key)
            record = solve_and_record(
                complements,
                r,
                args.seconds,
                f"random-r{r}-sample{len(profile_records) + 1}",
            )
            profile_records.append(record)
            if (
                record["optimum"] is not None
                and int(record["optimum"]) <= args.stop_at
            ):
                print(json.dumps({"counterexample": record}, sort_keys=True))
                return [*records, *profile_records]
        records.extend(profile_records)
        print(
            json.dumps(
                {
                    "campaign": "random",
                    "r": r,
                    "summary": summarize(profile_records),
                },
                sort_keys=True,
            ),
            flush=True,
        )
    return records


def partitions(total: int, maximum: int = 5) -> tuple[tuple[int, ...], ...]:
    """Integer partitions used as duplicate-column multiplicities."""
    result: list[tuple[int, ...]] = []

    def visit(
        remaining: int,
        ceiling: int,
        prefix: tuple[int, ...],
    ) -> None:
        if not remaining:
            result.append(prefix)
            return
        for current in range(
            min(remaining, ceiling, maximum),
            0,
            -1,
        ):
            visit(remaining - current, current, (*prefix, current))

    visit(total, total, ())
    return tuple(result)


def solve_duplicate_groups(
    groups: tuple[tuple[int, int], ...],
) -> Complements | None:
    """Find one row-regular realization of fixed size/multiplicity groups."""
    model = cp_model.CpModel()
    x = {
        (group, vertex): model.new_bool_var(f"x_{group}_{vertex}")
        for group in range(len(groups))
        for vertex in VERTICES
    }
    for group, (size, _) in enumerate(groups):
        model.add(sum(x[group, vertex] for vertex in VERTICES) == size)
    for vertex in VERTICES:
        model.add(
            sum(
                multiplicity * x[group, vertex]
                for group, (_, multiplicity) in enumerate(groups)
            )
            == 5
        )

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 8359
    status = solver.solve(model)
    if status != cp_model.OPTIMAL:
        return None

    result: list[frozenset[int]] = []
    for group, (_, multiplicity) in enumerate(groups):
        current = frozenset(
            vertex
            for vertex in VERTICES
            if solver.value(x[group, vertex])
        )
        result.extend([current] * multiplicity)
    return tuple(result)


def duplicate_campaign(args: argparse.Namespace) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for r in args.profiles:
        counts = (7 + r, 10 - 2 * r, r)
        partition_families = tuple(
            partitions(count) if count else ((),)
            for count in counts
        )
        multiplicity_shapes = sorted(
            product(*partition_families),
            key=lambda current: sum(map(len, current)),
        )
        minimum_groups: int | None = None
        profile_records = []
        for shape in multiplicity_shapes:
            group_count = sum(map(len, shape))
            if (
                minimum_groups is not None
                and group_count > minimum_groups + 2
            ):
                break
            groups = tuple(
                (size, multiplicity)
                for size, multiplicities in zip((5, 3, 1), shape)
                for multiplicity in multiplicities
            )
            complements = solve_duplicate_groups(groups)
            if complements is None:
                continue
            validate_instance(complements, r)
            if minimum_groups is None:
                minimum_groups = group_count
            record = solve_and_record(
                complements,
                r,
                args.seconds,
                f"duplicates-r{r}-shape{shape}",
            )
            record["generating_groups"] = group_count
            record["multiplicity_shape"] = shape
            profile_records.append(record)
            if (
                record["optimum"] is not None
                and int(record["optimum"]) <= args.stop_at
            ):
                print(json.dumps({"counterexample": record}, sort_keys=True))
                return [*records, *profile_records]
            if len(profile_records) >= args.duplicates_limit:
                break
        records.extend(profile_records)
        report = summarize(profile_records)
        report["minimum_generating_groups"] = minimum_groups
        print(
            json.dumps(
                {
                    "campaign": "duplicates",
                    "r": r,
                    "summary": report,
                },
                sort_keys=True,
            ),
            flush=True,
        )
    return records


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import certificate module {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def complements_from_completion(
    completion: Iterable[Iterable[tuple[int, int]]],
) -> Complements:
    result = []
    for matching in completion:
        endpoints = frozenset(
            vertex
            for edge in matching
            for vertex in edge
        )
        result.append(VERTEX_SET - endpoints)
    return tuple(result)


def certificate_instances() -> tuple[tuple[str, int, Complements], ...]:
    root = Path(__file__).resolve().parents[2]
    source = root / "collaboration" / "first_lift_global_theorem"
    r1 = load_module(
        source / "verify_r1_dead_seven_prefix.py",
        "coordinated_nine_dead_r1",
    )
    r2 = load_module(
        source / "verify_r2_dead_seven_prefix.py",
        "coordinated_nine_dead_r2",
    )
    r3 = load_module(
        source / "verify_r3_dead_seven_prefixes.py",
        "coordinated_nine_dead_r3",
    )
    r4 = load_module(
        source / "verify_r4_dead_seven_prefix.py",
        "coordinated_nine_dead_r4",
    )
    r5 = load_module(
        source / "verify_r5_dead_seven_prefix.py",
        "coordinated_nine_dead_r5",
    )
    return (
        (
            "dead-prefix-r1",
            1,
            complements_from_completion(r1.FULL_COMPLETION),
        ),
        (
            "dead-prefix-r2",
            2,
            complements_from_completion(r2.FULL_COMPLETION),
        ),
        (
            "dead-prefix-r3-C-in-G",
            3,
            complements_from_completion(
                r3.CASES["C_in_G"]["full_completion"]
            ),
        ),
        (
            "dead-prefix-r3-D-in-G",
            3,
            complements_from_completion(
                r3.CASES["D_in_G"]["full_completion"]
            ),
        ),
        (
            "dead-prefix-r4",
            4,
            complements_from_completion(r4.FULL_COMPLETION),
        ),
        (
            "dead-prefix-r5",
            5,
            complements_from_completion(r5.FULL_COMPLETION),
        ),
    )


def certificate_campaign(args: argparse.Namespace) -> list[dict[str, object]]:
    records = [
        solve_and_record(complements, r, args.seconds, label)
        for label, r, complements in certificate_instances()
        if r in args.profiles
    ]
    print(
        json.dumps(
            {
                "campaign": "certificates",
                "summary": summarize(records),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--campaign",
        choices=("random", "duplicates", "certificates", "all"),
        default="all",
    )
    parser.add_argument(
        "--profiles",
        type=int,
        nargs="+",
        default=list(range(6)),
    )
    parser.add_argument("--samples", type=int, default=10)
    parser.add_argument("--switches", type=int, default=500)
    parser.add_argument("--duplicates-limit", type=int, default=20)
    parser.add_argument("--seconds", type=float, default=10.0)
    parser.add_argument("--seed", type=int, default=8359)
    parser.add_argument(
        "--stop-at",
        type=int,
        default=8,
        help="stop and print the instance if an exact optimum is <= this",
    )
    args = parser.parse_args()
    if args.samples <= 0 or args.switches < 0:
        parser.error("--samples must be positive and --switches nonnegative")
    if args.duplicates_limit <= 0 or args.seconds <= 0:
        parser.error("--duplicates-limit and --seconds must be positive")
    if any(r not in range(6) for r in args.profiles):
        parser.error("--profiles must contain only values 0..5")
    args.profiles = tuple(dict.fromkeys(args.profiles))

    started = time.time()
    records: list[dict[str, object]] = []
    if args.campaign in ("random", "all"):
        records.extend(random_campaign(args))
    if args.campaign in ("duplicates", "all"):
        records.extend(duplicate_campaign(args))
    if args.campaign in ("certificates", "all"):
        records.extend(certificate_campaign(args))
    final = summarize(records)
    final["elapsed_seconds"] = time.time() - started
    final["scope"] = (
        "exact for each fixed tested instance; not an exhaustive theorem"
    )
    print(
        json.dumps(
            {"campaign": args.campaign, "final": final},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

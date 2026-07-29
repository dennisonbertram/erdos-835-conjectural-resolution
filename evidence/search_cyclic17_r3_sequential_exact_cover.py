#!/usr/bin/env python3
"""Sequential randomized exact-cover search for the cyclic joint r=3 layer.

Assign the 105 fixed-pair edges one at a time.  For one fixed pair ij, its
forty phase choices are a 160-column exact cover: forty triple-orbit columns
and the 120 residual moving-edge columns.  Phases already used on an assigned
edge incident with i or j are deleted before solving the slice.  Thus every
accepted slice is exact and every cross constraint involving earlier slices
is preserved.

The per-slice solver is a small randomized Algorithm X implementation.  A
failed or node-limited restart has no mathematical meaning.  A complete
assignment is passed to the independent full radius-five semantic verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import threading
import time
from itertools import combinations
from pathlib import Path

from pysat.solvers import Solver


EVIDENCE = Path(__file__).resolve().parent
BALL = EVIDENCE / "odd_graph_local_ball"
for directory in (str(EVIDENCE), str(BALL)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from convert_cyclic17_r3_to_radius5 import convert
from global_latin_audit import construct_golf17
from search_radius5_golf_cyclic_compact import (
    FIXED_PAIRS,
    P,
    POINTS,
    REPRESENTATIVES,
    REPRESENTATIVE_EDGE_COORDINATES,
    SQUARES,
    allowed_shifts,
    translate,
    zero_positions,
)


MOVING_EDGES = tuple(combinations(POINTS, 2))


def solve_slice_sat(
    fixed_pair: tuple[int, int],
    used: dict[tuple[int, int], set[int]],
    zeros: dict[tuple[int, int], int],
    rng: random.Random,
    seconds: float,
    solver_name: str,
) -> tuple[list[int] | None, int, bool]:
    """Solve one restricted slice with the compact collision-only CNF."""
    i, j = fixed_pair
    domains = {}
    variable = {}
    next_variable = 1
    for orbit_index in range(len(REPRESENTATIVES)):
        banned = used[i, orbit_index] | used[j, orbit_index]
        domain = [
            shift
            for shift in allowed_shifts(
                fixed_pair, orbit_index, zeros
            )
            if shift not in banned
        ]
        if not domain:
            return None, 0, True
        rng.shuffle(domain)
        domains[orbit_index] = tuple(domain)
        for shift in domain:
            variable[orbit_index, shift] = next_variable
            next_variable += 1

    clauses: list[list[int]] = []

    def at_most_one(literals: list[int]) -> None:
        clauses.extend(
            [-first, -second]
            for first, second in combinations(literals, 2)
        )

    for orbit_index in range(len(REPRESENTATIVES)):
        literals = [
            variable[orbit_index, shift]
            for shift in domains[orbit_index]
        ]
        clauses.append(literals)
        at_most_one(literals)

    collision_groups = {
        (difference, position): []
        for difference in range(1, 9)
        for position in POINTS
    }
    for orbit_index, coordinates in enumerate(
        REPRESENTATIVE_EDGE_COORDINATES
    ):
        for shift in domains[orbit_index]:
            literal = variable[orbit_index, shift]
            for difference, offset in coordinates:
                collision_groups[
                    difference, (offset + shift) % P
                ].append(literal)
    for literals in collision_groups.values():
        at_most_one(literals)

    preferred = []
    for orbit_index in range(len(REPRESENTATIVES)):
        favourite = rng.choice(domains[orbit_index])
        preferred.extend(
            variable[orbit_index, shift]
            if shift == favourite
            else -variable[orbit_index, shift]
            for shift in domains[orbit_index]
        )

    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        try:
            solver.set_phases(preferred)
        except NotImplementedError:
            pass
        timer = None
        if seconds > 0:
            timer = threading.Timer(seconds, solver.interrupt)
            timer.daemon = True
            timer.start()
            status = solver.solve_limited(expect_interrupt=True)
            timer.cancel()
        else:
            status = solver.solve()
        stats = solver.accum_stats()
        work = int(stats.get("conflicts", 0))
        if status is not True:
            return None, work, status is False
        positive = {
            literal for literal in solver.get_model()
            if literal > 0
        }

    shifts = []
    for orbit_index in range(len(REPRESENTATIVES)):
        selected = [
            shift for shift in domains[orbit_index]
            if variable[orbit_index, shift] in positive
        ]
        assert len(selected) == 1
        shifts.append(selected[0])
    return shifts, work, True


def solve_slice_exact_cover(
    fixed_pair: tuple[int, int],
    used: dict[tuple[int, int], set[int]],
    zeros: dict[tuple[int, int], int],
    rng: random.Random,
    node_limit: int,
    deadline: float,
) -> tuple[list[int] | None, int, bool]:
    """Return selected shifts, nodes, and whether the search was exhaustive."""
    i, j = fixed_pair
    leave = {
        edge for edge in MOVING_EDGES
        if edge in {
            tuple(sorted(
                (
                    zeros[square, difference],
                    (
                        zeros[square, difference] + difference
                    )
                    % P,
                )
            ))
            for square in fixed_pair
            for difference in range(1, 9)
        }
    }
    assert len(leave) == 16
    residual_edges = tuple(edge for edge in MOVING_EDGES if edge not in leave)
    assert len(residual_edges) == 120
    edge_column = {
        edge: len(REPRESENTATIVES) + index
        for index, edge in enumerate(residual_edges)
    }

    row_keys: list[tuple[int, int]] = []
    row_columns: list[tuple[int, int, int, int]] = []
    column_rows = {
        column: set()
        for column in range(len(REPRESENTATIVES) + len(residual_edges))
    }
    for orbit_index, representative in enumerate(REPRESENTATIVES):
        banned = used[i, orbit_index] | used[j, orbit_index]
        domain = [
            shift
            for shift in allowed_shifts(
                fixed_pair, orbit_index, zeros
            )
            if shift not in banned
        ]
        if not domain:
            return None, 0, True
        for shift in domain:
            triple = translate(representative, shift)
            moving_columns = tuple(
                edge_column[edge]
                for edge in combinations(triple, 2)
            )
            columns = (orbit_index,) + moving_columns
            assert len(set(columns)) == 4
            row_index = len(row_keys)
            row_keys.append((orbit_index, shift))
            row_columns.append(columns)
            for column in columns:
                column_rows[column].add(row_index)

    uncovered = set(column_rows)
    available = set(range(len(row_keys)))
    nodes = 0
    limited = False

    def search(
        current_uncovered: set[int],
        current_available: set[int],
        solution: list[int],
    ) -> list[int] | None:
        nonlocal nodes, limited
        nodes += 1
        if nodes > node_limit or time.monotonic() >= deadline:
            limited = True
            return None
        if not current_uncovered:
            return solution[:]

        best_column = -1
        best_candidates: list[int] | None = None
        for column in current_uncovered:
            candidates = list(column_rows[column] & current_available)
            if not candidates:
                return None
            if (
                best_candidates is None
                or len(candidates) < len(best_candidates)
            ):
                best_column = column
                best_candidates = candidates
                if len(candidates) == 1:
                    break
        assert best_candidates is not None and best_column >= 0
        rng.shuffle(best_candidates)

        # Prefer rows whose other columns are currently tight.
        def row_score(row_index: int) -> int:
            return sum(
                len(column_rows[column] & current_available)
                for column in row_columns[row_index]
                if column in current_uncovered
            )

        best_candidates.sort(key=row_score)
        for row_index in best_candidates:
            if row_index not in current_available:
                continue
            covered = set(row_columns[row_index])
            conflicting: set[int] = set()
            for column in covered:
                conflicting.update(column_rows[column])
            answer = search(
                current_uncovered - covered,
                current_available - conflicting,
                solution + [row_index],
            )
            if answer is not None:
                return answer
            if limited:
                return None
        return None

    selected_rows = search(uncovered, available, [])
    if selected_rows is None:
        return None, nodes, not limited
    shifts = [-1] * len(REPRESENTATIVES)
    for row_index in selected_rows:
        orbit_index, shift = row_keys[row_index]
        assert shifts[orbit_index] == -1
        shifts[orbit_index] = shift
    assert all(shift in POINTS for shift in shifts)
    return shifts, nodes, True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=1200.0)
    parser.add_argument("--restarts", type=int, default=100)
    parser.add_argument("--slice-node-limit", type=int, default=250_000)
    parser.add_argument(
        "--slice-backend",
        choices=("sat", "algorithm-x"),
        default="sat",
    )
    parser.add_argument("--sat-solver", default="maplechrono")
    parser.add_argument("--slice-seconds", type=float, default=10.0)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--phase-output", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()

    golf = construct_golf17()
    zeros = zero_positions(golf)
    deadline = time.monotonic() + args.seconds
    best_depth = 0
    total_nodes = 0
    complete: dict[tuple[int, int], list[int]] | None = None

    for restart in range(1, args.restarts + 1):
        if time.monotonic() >= deadline:
            break
        rng = random.Random(args.seed + restart)
        order = list(FIXED_PAIRS)
        rng.shuffle(order)
        used = {
            (fixed_point, orbit_index): set()
            for fixed_point in SQUARES
            for orbit_index in range(len(REPRESENTATIVES))
        }
        assigned: dict[tuple[int, int], list[int]] = {}
        exhaustive_failure = False
        for depth, fixed_pair in enumerate(order, start=1):
            if args.slice_backend == "sat":
                shifts, nodes, exhaustive = solve_slice_sat(
                    fixed_pair,
                    used,
                    zeros,
                    rng,
                    min(
                        args.slice_seconds,
                        max(0.001, deadline - time.monotonic()),
                    ),
                    args.sat_solver,
                )
            else:
                shifts, nodes, exhaustive = solve_slice_exact_cover(
                    fixed_pair,
                    used,
                    zeros,
                    rng,
                    args.slice_node_limit,
                    deadline,
                )
            total_nodes += nodes
            if shifts is None:
                exhaustive_failure = exhaustive
                break
            assigned[fixed_pair] = shifts
            i, j = fixed_pair
            for orbit_index, shift in enumerate(shifts):
                assert shift not in used[i, orbit_index]
                assert shift not in used[j, orbit_index]
                used[i, orbit_index].add(shift)
                used[j, orbit_index].add(shift)
            if depth > best_depth:
                best_depth = depth
                print(
                    f"restart={restart} new_best_depth={best_depth}/105 "
                    f"total_nodes={total_nodes}",
                    flush=True,
                )
            if depth == len(FIXED_PAIRS):
                complete = assigned
                break
        if complete is not None:
            break
        print(
            f"restart={restart} stopped_depth={len(assigned)}/105 "
            f"failure={'exhaustive' if exhaustive_failure else 'limited'}",
            flush=True,
        )

    if complete is None:
        print(
            json.dumps(
                {
                    "status": "UNKNOWN",
                    "best_assigned_slices": best_depth,
                    "total_nodes": total_nodes,
                    "scope": "randomized sequential search only",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    phases = {
        f"{i},{j}": [(-shift) % P for shift in complete[i, j]]
        for i, j in FIXED_PAIRS
    }
    encoded = (
        json.dumps(phases, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    if args.phase_output is not None:
        args.phase_output.write_bytes(encoded)
    payload = convert(phases)
    if args.certificate is not None:
        args.certificate.write_text(
            json.dumps(payload, sort_keys=True, separators=(",", ":"))
            + "\n",
            encoding="utf-8",
        )
    print(
        json.dumps(
            {
                "status": "FEASIBLE",
                "phase_sha256": hashlib.sha256(encoded).hexdigest(),
                "certificate_sha256_without_hash": payload[
                    "sha256_without_hash"
                ],
                "semantic_ball_verified": True,
                "total_nodes": total_nodes,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

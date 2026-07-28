#!/usr/bin/env python3
"""Find partial K18 one-factorizations inducing three support certificates.

This is a CP-SAT discovery helper.  The durable verifier uses only literal
certificate data and the Python standard library.
"""

from __future__ import annotations

import argparse
from itertools import combinations

from ortools.sat.python import cp_model

from verify_r1_minimum_layer_repair import build_instance
from verify_r3_dead_seven_prefixes import CASES, VERTICES, endpoints


N_COLOURS = 17
OUTSIDE_SIZE = 5
CaseSupports = tuple[frozenset[int], ...]


def instances() -> dict[str, CaseSupports]:
    _, r1_selected, r1_remaining = build_instance()
    result = {
        "r1": tuple((*r1_selected, *r1_remaining)),
    }
    for name, case in CASES.items():
        prefix = case["prefix"]
        remaining_complements = case["remaining_complements"]
        assert isinstance(prefix, tuple)
        assert isinstance(remaining_complements, tuple)
        result[name] = (
            *(endpoints(layer) for layer in prefix),
            *(VERTICES - complement for complement in remaining_complements),
        )
    return result


def solve(
    supports: CaseSupports,
    seconds: float,
) -> tuple[
    str,
    tuple[tuple[int, ...], ...] | None,
    tuple[tuple[int, int, int], ...] | None,
]:
    model = cp_model.CpModel()
    missing = frozenset(
        (vertex, colour)
        for colour, support in enumerate(supports)
        for vertex in VERTICES - support
    )
    cross = {
        (outside, vertex, colour): model.new_bool_var(
            f"cross_{outside}_{vertex}_{colour}"
        )
        for vertex, colour in missing
        for outside in range(OUTSIDE_SIZE)
    }
    outside_edges = tuple(combinations(range(OUTSIDE_SIZE), 2))
    internal = {
        (left, right, colour): model.new_bool_var(
            f"internal_{left}_{right}_{colour}"
        )
        for left, right in outside_edges
        for colour in range(N_COLOURS)
    }

    # Each missing colour occurrence at a hole vertex is assigned to one
    # outside neighbour, and every cross edge receives one such colour.
    for vertex, colour in missing:
        model.add(
            sum(
                cross[outside, vertex, colour]
                for outside in range(OUTSIDE_SIZE)
            )
            == 1
        )
    for outside in range(OUTSIDE_SIZE):
        for vertex in VERTICES:
            model.add(
                sum(
                    cross[outside, vertex, colour]
                    for colour in range(N_COLOURS)
                    if (vertex, colour) in missing
                )
                == 1
            )

    # Every edge of the outside K5 receives exactly one colour.
    for left, right in outside_edges:
        model.add(
            sum(
                internal[left, right, colour]
                for colour in range(N_COLOURS)
            )
            == 1
        )

    # Every outside vertex sees every colour exactly once.
    for outside in range(OUTSIDE_SIZE):
        for colour in range(N_COLOURS):
            model.add(
                sum(
                    cross[outside, vertex, colour]
                    for vertex in VERTICES
                    if (vertex, colour) in missing
                )
                + sum(
                    internal[
                        min(outside, other),
                        max(outside, other),
                        colour,
                    ]
                    for other in range(OUTSIDE_SIZE)
                    if other != outside
                )
                == 1
            )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 835
    status = solver.solve(model)
    status_name = solver.status_name(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return status_name, None, None

    cross_rows = tuple(
        tuple(
            next(
                colour
                for colour in range(N_COLOURS)
                if (outside, vertex, colour) in cross
                and solver.value(cross[outside, vertex, colour])
            )
            for outside in range(OUTSIDE_SIZE)
        )
        for vertex in VERTICES
    )
    internal_rows = tuple(
        (
            left,
            right,
            next(
                colour
                for colour in range(N_COLOURS)
                if solver.value(internal[left, right, colour])
            ),
        )
        for left, right in outside_edges
    )
    return status_name, cross_rows, internal_rows


def print_certificate(
    name: str,
    status: str,
    cross_rows: tuple[tuple[int, ...], ...] | None,
    internal_rows: tuple[tuple[int, int, int], ...] | None,
) -> None:
    print(f"{name}: partial_factorization_status={status}")
    if cross_rows is None or internal_rows is None:
        return
    print('"cross": (')
    for row in cross_rows:
        print(f"    {row},")
    print("),")
    print('"internal": (')
    for row in internal_rows:
        print(f"    {row},")
    print("),")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--case",
        choices=("all", "r1", "C_in_G", "D_in_G"),
        default="all",
    )
    parser.add_argument("--seconds", type=float, default=60.0)
    args = parser.parse_args()

    selected = instances()
    names = tuple(selected) if args.case == "all" else (args.case,)
    for name in names:
        status, cross_rows, internal_rows = solve(
            selected[name],
            args.seconds,
        )
        print_certificate(name, status, cross_rows, internal_rows)


if __name__ == "__main__":
    main()

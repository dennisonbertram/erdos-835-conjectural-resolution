#!/usr/bin/env python3
"""SAT backend for the GF(16) radius-4 L/M ansatz.

This encodes the same M constraints as `search_radius4_design.py` as
plain CNF exact-one clauses and uses a PySAT backend.  PySAT is needed
only to locate a witness; all extracted data are checked by the
backend-independent verification functions before being reported.
"""

from __future__ import annotations

import argparse
import json
import threading
import time
from itertools import combinations
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver

from search_radius4_design import (
    COLOURS,
    CORE_EDGES,
    FINITE,
    INDEX_EDGES,
    INDICES,
    INFINITY,
    assemble_and_verify,
    solve_n_for_edge,
    verify_m,
)


def add_exactly_one(cnf: CNF, literals: list[int]) -> None:
    assert literals
    cnf.append(literals)
    for first, second in combinations(literals, 2):
        cnf.append([-first, -second])


def build_cnf(second_anchor: int):
    variable = {}
    reverse = {}
    next_variable = 1

    def missing(index: int, vertex: int) -> set[int]:
        return {vertex, vertex ^ index}

    for index in INDICES:
        for left, right in CORE_EDGES:
            for colour in COLOURS:
                if (
                    colour in missing(index, left)
                    or colour in missing(index, right)
                ):
                    continue
                key = (index, left, right, colour)
                variable[key] = next_variable
                reverse[next_variable] = key
                next_variable += 1

    cnf = CNF()

    for index in INDICES:
        for left, right in CORE_EDGES:
            add_exactly_one(
                cnf,
                [
                    variable[index, left, right, colour]
                    for colour in COLOURS
                    if (index, left, right, colour) in variable
                ],
            )

    for index in INDICES:
        for vertex in FINITE:
            for colour in COLOURS:
                if colour in missing(index, vertex):
                    continue
                add_exactly_one(
                    cnf,
                    [
                        variable[
                            index,
                            min(vertex, other),
                            max(vertex, other),
                            colour,
                        ]
                        for other in FINITE
                        if other != vertex
                        and (
                            index,
                            min(vertex, other),
                            max(vertex, other),
                            colour,
                        )
                        in variable
                    ],
                )

    for left, right in CORE_EDGES:
        for colour in COLOURS:
            if colour in (left, right):
                continue
            add_exactly_one(
                cnf,
                [
                    variable[index, left, right, colour]
                    for index in INDICES
                    if (index, left, right, colour) in variable
                ],
            )

    for left, right in CORE_EDGES:
        cnf.append([variable[left ^ right, left, right, INFINITY]])
    cnf.append([variable[2, 0, 1, 4]])
    cnf.append([variable[1, 0, 2, second_anchor]])
    return cnf, variable, reverse


def solve_with_timeout(
    cnf: CNF, solver_name: str, seconds: float
) -> tuple[object, list[int] | None, dict]:
    solver = Solver(name=solver_name, bootstrap_with=cnf.clauses)
    timer = None
    if seconds > 0:
        timer = threading.Timer(seconds, solver.interrupt)
        timer.start()
    started = time.monotonic()
    try:
        status = solver.solve_limited(expect_interrupt=True)
        model = solver.get_model() if status is True else None
        statistics = solver.accum_stats()
    finally:
        if timer is not None:
            timer.cancel()
        elapsed = time.monotonic() - started
        solver.delete()
    statistics["wall_time_seconds"] = elapsed
    return status, model, statistics


def extract_m(model: list[int], reverse):
    positive = {literal for literal in model if literal > 0}
    colouring = {}
    for literal in positive:
        if literal not in reverse:
            continue
        index, left, right, colour = reverse[literal]
        key = (index, left, right)
        assert key not in colouring
        colouring[key] = colour
    assert len(colouring) == len(INDICES) * len(CORE_EDGES)
    return colouring


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--solver",
        default="glucose42",
        choices=(
            "glucose42",
            "maplechrono",
            "maplesat",
        ),
        help=(
            "Only backends whose PySAT bindings support interruptible "
            "limited solving are offered."
        ),
    )
    parser.add_argument("--seconds", type=float, default=600)
    parser.add_argument("--n-seconds", type=float, default=30)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--second-anchor", type=int, choices=(4, 5, 6, 7, 8), required=True
    )
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()

    cnf, _, reverse = build_cnf(args.second_anchor)
    print(
        json.dumps(
            {
                "variables": cnf.nv,
                "clauses": len(cnf.clauses),
                "solver": args.solver,
                "second_anchor": args.second_anchor,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    status, model, statistics = solve_with_timeout(
        cnf, args.solver, args.seconds
    )
    print(
        json.dumps(
            {
                "sat_status": status,
                "statistics": statistics,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    if status is not True or model is None:
        return

    m_colouring = extract_m(model, reverse)
    verify_m(m_colouring)
    print("M witness independently verified", flush=True)

    n_colouring = {}
    n_statistics = {}
    for edge_number, (left, right) in enumerate(CORE_EDGES):
        edge_colouring, stats = solve_n_for_edge(
            (left, right),
            m_colouring,
            args.n_seconds,
            args.workers,
            10000 + edge_number,
        )
        n_statistics[left, right] = stats
        if edge_colouring is None:
            print(
                json.dumps(
                    {
                        "N_failure_edge": [left, right],
                        "statistics": stats,
                    },
                    sort_keys=True,
                )
            )
            return
        for (first, second), colour in edge_colouring.items():
            n_colouring[left, right, first, second] = colour
        if (edge_number + 1) % 10 == 0:
            print(f"N checks {edge_number + 1}/120", flush=True)

    vertices, _, assignment = assemble_and_verify(m_colouring, n_colouring)
    result = {
        "status": "FEASIBLE",
        "radius": 4,
        "vertices": len(vertices),
        "certificate_verified": True,
        "solver": args.solver,
        "second_anchor": args.second_anchor,
        "n_total_wall_time_seconds": sum(
            item["wall_time_seconds"] for item in n_statistics.values()
        ),
        "n_max_wall_time_seconds": max(
            item["wall_time_seconds"] for item in n_statistics.values()
        ),
    }
    if args.certificate is not None:
        payload = {
            "metadata": result,
            "m": [
                [
                    m_colouring[index, left, right]
                    for left, right in CORE_EDGES
                ]
                for index in INDICES
            ],
            "n": [
                [
                    n_colouring[left, right, first, second]
                    for first, second in INDEX_EDGES
                ]
                for left, right in CORE_EDGES
            ],
            "ball_assignment": assignment,
        }
        args.certificate.parent.mkdir(parents=True, exist_ok=True)
        args.certificate.write_text(
            json.dumps(payload, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

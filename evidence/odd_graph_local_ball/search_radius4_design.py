#!/usr/bin/env python3
"""Search the exact radius-4 design reduction under a GF(16) ansatz.

Finite colours are the 4-bit vectors 0,...,15, addition is XOR, and
the fifteeen sphere-coordinate indices are the nonzero vectors.
We prescribe

    L_i(u) = u XOR i.

By default we also prescribe the infinity-coloured matching in M_i to
be the translation matching {u, u XOR i}.  This is a constructive
ansatz, not a without-loss-of-generality reduction.  Any solution is
assembled into the actual 14,657-vertex ball and independently checked.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

from ortools.sat.python import cp_model

from search_local_cover import (
    FULL_MASK,
    ROOT,
    generate_ball,
    verify_assignment,
)


FINITE = tuple(range(16))
INFINITY = 16
COLOURS = tuple(range(17))
INDICES = tuple(range(1, 16))
CORE_EDGES = tuple(
    (left, right) for left in FINITE for right in FINITE if left < right
)
INDEX_EDGES = tuple(
    (left, right) for left in INDICES for right in INDICES if left < right
)
B_MASK = FULL_MASK ^ ROOT


def bit_positions(mask: int) -> list[int]:
    result = []
    while mask:
        bit = mask & -mask
        result.append(bit.bit_length() - 1)
        mask ^= bit
    return result


def make_solver(seconds: float, workers: int, seed: int) -> cp_model.CpSolver:
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = seed
    return solver


def build_m_model(fix_infinity: bool, second_anchor: Optional[int]):
    model = cp_model.CpModel()
    choice = {}

    def missing(index: int, vertex: int) -> set[int]:
        return {vertex, vertex ^ index}

    for index in INDICES:
        for left, right in CORE_EDGES:
            allowed = [
                colour
                for colour in COLOURS
                if colour not in missing(index, left)
                and colour not in missing(index, right)
            ]
            variables = []
            for colour in allowed:
                variable = model.NewBoolVar(
                    f"m_{index}_{left}_{right}_{colour}"
                )
                choice[index, left, right, colour] = variable
                variables.append(variable)
            model.AddExactlyOne(variables)

    # At fixed (i,u), the incident colours are C \ {u,u+i}.
    for index in INDICES:
        for vertex in FINITE:
            for colour in COLOURS:
                if colour in missing(index, vertex):
                    continue
                incident = [
                    choice[index, min(vertex, other), max(vertex, other), colour]
                    for other in FINITE
                    if other != vertex
                    and (
                        index,
                        min(vertex, other),
                        max(vertex, other),
                        colour,
                    )
                    in choice
                ]
                model.AddExactlyOne(incident)

    # At fixed uv, the fifteen M_i values are C \ {u,v}.
    for left, right in CORE_EDGES:
        for colour in COLOURS:
            if colour in (left, right):
                continue
            across_indices = [
                choice[index, left, right, colour]
                for index in INDICES
                if (index, left, right, colour) in choice
            ]
            model.AddExactlyOne(across_indices)

    if fix_infinity:
        # The translation matchings partition E(K_16), so these assignments
        # satisfy both the vertex and transversal requirements for infinity.
        for left, right in CORE_EDGES:
            index = left ^ right
            model.Add(choice[index, left, right, INFINITY] == 1)

        # After fixing the translation matchings, AGL(4,2) still acts by
        # simultaneously relabelling vertices, finite colours, and nonzero
        # indices.  At edge {0,1}, for any i != 1 the colour M_i(01) lies
        # outside span{1,i}.  A linear map can therefore send the independent
        # triple (1,i,M_i(01)) to (1,2,4).  This anchor is without loss within
        # the present ansatz.
        model.Add(choice[2, 0, 1, 4] == 1)

        # The stabilizer of 1,2,4 has five orbits on the allowed value of
        # M_1(02), represented by 4,5,6,7,8.  Supplying one representative
        # selects a branch; leaving it unset searches all five.
        if second_anchor is not None:
            if second_anchor not in (4, 5, 6, 7, 8):
                raise ValueError("second_anchor must be one of 4,5,6,7,8")
            model.Add(choice[1, 0, 2, second_anchor] == 1)

    return model, choice


def extract_m(solver: cp_model.CpSolver, choice):
    colouring = {}
    for index in INDICES:
        for left, right in CORE_EDGES:
            colouring[index, left, right] = next(
                colour
                for colour in COLOURS
                if (index, left, right, colour) in choice
                and solver.BooleanValue(choice[index, left, right, colour])
            )
    return colouring


def verify_m(colouring) -> None:
    for index in INDICES:
        for vertex in FINITE:
            incident = [
                colouring[index, min(vertex, other), max(vertex, other)]
                for other in FINITE
                if other != vertex
            ]
            assert len(incident) == len(set(incident)) == 15
            assert set(incident) == set(COLOURS) - {vertex, vertex ^ index}
    for left, right in CORE_EDGES:
        across = [
            colouring[index, left, right] for index in INDICES
        ]
        assert len(across) == len(set(across)) == 15
        assert set(across) == set(COLOURS) - {left, right}


def solve_n_for_edge(
    core_edge: tuple[int, int],
    m_colouring,
    seconds: float,
    workers: int,
    seed: int,
):
    left, right = core_edge
    missing = {
        index: {
            m_colouring[index, left, right],
            left ^ index,
            right ^ index,
        }
        for index in INDICES
    }
    assert all(len(values) == 3 for values in missing.values())

    model = cp_model.CpModel()
    choice = {}
    for first, second in INDEX_EDGES:
        allowed = [
            colour
            for colour in COLOURS
            if colour not in missing[first] and colour not in missing[second]
        ]
        variables = []
        for colour in allowed:
            variable = model.NewBoolVar(
                f"n_{left}_{right}_{first}_{second}_{colour}"
            )
            choice[first, second, colour] = variable
            variables.append(variable)
        model.AddExactlyOne(variables)

    for index in INDICES:
        for colour in COLOURS:
            if colour in missing[index]:
                continue
            incident = [
                choice[min(index, other), max(index, other), colour]
                for other in INDICES
                if other != index
                and (min(index, other), max(index, other), colour) in choice
            ]
            model.AddExactlyOne(incident)

    solver = make_solver(seconds, workers, seed)
    status = solver.Solve(model)
    statistics = {
        "status": solver.StatusName(status),
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return None, statistics

    colouring = {
        (first, second): next(
            colour
            for colour in COLOURS
            if (first, second, colour) in choice
            and solver.BooleanValue(choice[first, second, colour])
        )
        for first, second in INDEX_EDGES
    }
    for index in INDICES:
        incident = [
            colouring[min(index, other), max(index, other)]
            for other in INDICES
            if other != index
        ]
        assert len(incident) == len(set(incident)) == 14
        assert set(incident) == set(COLOURS) - missing[index]
    return colouring, statistics


def add_m_nogood(model, choice, m_colouring, core_edge) -> None:
    left, right = core_edge
    model.AddBoolOr(
        [
            choice[
                index,
                left,
                right,
                m_colouring[index, left, right],
            ].Not()
            for index in INDICES
        ]
    )


def assemble_and_verify(m_colouring, n_colouring):
    vertices, distances = generate_ball(4)
    assignment = [-1] * len(vertices)

    for position, (vertex, distance) in enumerate(zip(vertices, distances)):
        if distance == 0:
            assignment[position] = INFINITY
        elif distance == 1:
            omitted = B_MASK ^ vertex
            positions = bit_positions(omitted)
            assert len(positions) == 1
            assignment[position] = positions[0] - 15
        elif distance == 2:
            added = bit_positions(vertex & B_MASK)
            omitted = bit_positions(ROOT ^ (vertex & ROOT))
            assert len(added) == len(omitted) == 1
            u = added[0] - 15
            index = omitted[0] + 1
            assignment[position] = u ^ index
        elif distance == 3:
            omitted = bit_positions(B_MASK ^ (vertex & B_MASK))
            retained = bit_positions(vertex & ROOT)
            assert len(omitted) == 2 and len(retained) == 1
            left, right = sorted(item - 15 for item in omitted)
            index = retained[0] + 1
            assignment[position] = m_colouring[index, left, right]
        elif distance == 4:
            added = bit_positions(vertex & B_MASK)
            omitted = bit_positions(ROOT ^ (vertex & ROOT))
            assert len(added) == len(omitted) == 2
            left, right = sorted(item - 15 for item in added)
            first, second = sorted(item + 1 for item in omitted)
            assignment[position] = n_colouring[
                left, right, first, second
            ]
        else:
            raise AssertionError(distance)

    assert all(colour >= 0 for colour in assignment)
    verify_assignment(vertices, distances, assignment, 4)
    return vertices, distances, assignment


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m-seconds", type=float, default=600)
    parser.add_argument("--n-seconds", type=float, default=30)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--max-m-solutions", type=int, default=20)
    parser.add_argument(
        "--free-infinity",
        action="store_true",
        help="Do not fix the natural translation matching for colour infinity.",
    )
    parser.add_argument(
        "--second-anchor",
        type=int,
        choices=(4, 5, 6, 7, 8),
        help="Select one residual symmetry branch for M_1({0,2}).",
    )
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()

    model, m_choice = build_m_model(
        not args.free_infinity, args.second_anchor
    )
    attempt_summaries = []
    construction = None

    for attempt in range(1, args.max_m_solutions + 1):
        print(f"M attempt {attempt}: solving", flush=True)
        m_solver = make_solver(args.m_seconds, args.workers, attempt)
        m_status = m_solver.Solve(model)
        m_summary = {
            "attempt": attempt,
            "status": m_solver.StatusName(m_status),
            "wall_time_seconds": m_solver.WallTime(),
            "branches": m_solver.NumBranches(),
            "conflicts": m_solver.NumConflicts(),
        }
        attempt_summaries.append(m_summary)
        print(json.dumps(m_summary, sort_keys=True), flush=True)
        if m_status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            break

        m_colouring = extract_m(m_solver, m_choice)
        verify_m(m_colouring)
        n_colouring = {}
        failed_edges = []
        n_statistics = {}
        for edge_number, core_edge in enumerate(CORE_EDGES):
            edge_colouring, stats = solve_n_for_edge(
                core_edge,
                m_colouring,
                args.n_seconds,
                args.workers,
                1000 * attempt + edge_number,
            )
            n_statistics[core_edge] = stats
            if edge_colouring is None:
                failed_edges.append(core_edge)
            else:
                left, right = core_edge
                for (first, second), colour in edge_colouring.items():
                    n_colouring[left, right, first, second] = colour
            if (edge_number + 1) % 10 == 0 or edge_colouring is None:
                print(
                    f"N checks {edge_number + 1}/120; "
                    f"failures={len(failed_edges)}",
                    flush=True,
                )

        if not failed_edges:
            vertices, distances, assignment = assemble_and_verify(
                m_colouring, n_colouring
            )
            construction = (
                m_colouring,
                n_colouring,
                vertices,
                distances,
                assignment,
                n_statistics,
            )
            break

        # Each N_e depends only on the fifteen M_i(e) values.  Exclude every
        # failed vector before asking for another global M solution.
        for core_edge in failed_edges:
            add_m_nogood(model, m_choice, m_colouring, core_edge)

    result = {
        "ansatz": {
            "L": "u XOR i",
            "infinity_matching_fixed": not args.free_infinity,
            "first_anchor": "M_2({0,1})=4"
            if not args.free_infinity
            else None,
            "second_anchor": args.second_anchor,
        },
        "m_attempts": attempt_summaries,
        "status": "FEASIBLE" if construction is not None else "UNKNOWN",
    }

    if construction is not None:
        (
            m_colouring,
            n_colouring,
            vertices,
            distances,
            assignment,
            n_statistics,
        ) = construction
        result.update(
            {
                "radius": 4,
                "vertices": len(vertices),
                "certificate_verified": True,
                "n_total_wall_time_seconds": sum(
                    item["wall_time_seconds"] for item in n_statistics.values()
                ),
                "n_max_wall_time_seconds": max(
                    item["wall_time_seconds"] for item in n_statistics.values()
                ),
            }
        )
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

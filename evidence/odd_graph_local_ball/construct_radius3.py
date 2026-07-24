#!/usr/bin/env python3
"""Construct a radius-3 local cover by fifteen small edge-colouring CSPs.

Write the root as A, with |A|=15, and its complement as B, with |B|=16.
Index B and the nonzero colours by t in F_17^*.  Index the points of A
by m in F_17^* \ {1}.  A distance-two vertex has the form

    (A - {m}) union {t},

and is prescribed colour m*t.  Thus every distance-one closed
neighbourhood already has all seventeen colours.

For fixed m, distance-three vertices correspond to the edges {t,u} of
K_16.  We find an edge colouring in which the colours incident with t
are exactly F_17 \ {t,m*t}.  The fifteen values of m are independent.
The resulting assignment is then checked against the graph itself.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ortools.sat.python import cp_model

from search_local_cover import (
    COLOR_COUNT,
    FULL_MASK,
    ROOT,
    generate_ball,
    neighbours,
    verify_assignment,
)


NONZERO = tuple(range(1, COLOR_COUNT))
MULTIPLIERS = tuple(range(2, COLOR_COUNT))
EDGES = tuple(
    (left, right)
    for left in NONZERO
    for right in NONZERO
    if left < right
)


def solve_column(multiplier: int, seconds: float, workers: int):
    """Return an exact K_16 edge colouring for one multiplier."""

    model = cp_model.CpModel()
    choices: dict[tuple[int, int, int], cp_model.IntVar] = {}

    def missing(vertex: int) -> set[int]:
        return {vertex, multiplier * vertex % COLOR_COUNT}

    for left, right in EDGES:
        allowed = [
            colour
            for colour in range(COLOR_COUNT)
            if colour not in missing(left) and colour not in missing(right)
        ]
        edge_choices = []
        for colour in allowed:
            variable = model.NewBoolVar(f"x_{left}_{right}_{colour}")
            choices[left, right, colour] = variable
            edge_choices.append(variable)
        model.AddExactlyOne(edge_choices)

    for vertex in NONZERO:
        for colour in range(COLOR_COUNT):
            incident = [
                choices[min(vertex, other), max(vertex, other), colour]
                for other in NONZERO
                if other != vertex
                and (min(vertex, other), max(vertex, other), colour) in choices
            ]
            if colour in missing(vertex):
                assert not incident
            else:
                model.AddExactlyOne(incident)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    status = solver.Solve(model)
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return solver.StatusName(status), None, {
            "wall_time_seconds": solver.WallTime(),
            "branches": solver.NumBranches(),
            "conflicts": solver.NumConflicts(),
        }

    colouring = {}
    for left, right in EDGES:
        colour = next(
            colour
            for colour in range(COLOR_COUNT)
            if (left, right, colour) in choices
            and solver.BooleanValue(choices[left, right, colour])
        )
        colouring[left, right] = colour

    # Independent small-instance check.
    for vertex in NONZERO:
        incident = [
            colouring[min(vertex, other), max(vertex, other)]
            for other in NONZERO
            if other != vertex
        ]
        assert set(incident) == set(range(COLOR_COUNT)) - missing(vertex)
        assert len(incident) == len(set(incident)) == 15

    return solver.StatusName(status), colouring, {
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }


def construct(seconds: float, workers: int):
    columns = {}
    statistics = {}
    for multiplier in MULTIPLIERS:
        status, colouring, stats = solve_column(multiplier, seconds, workers)
        statistics[multiplier] = {"status": status, **stats}
        if colouring is None:
            return None, statistics
        columns[multiplier] = colouring

    vertices, distances = generate_ball(3)
    index = {vertex: position for position, vertex in enumerate(vertices)}
    assignment = [-1] * len(vertices)
    assignment[index[ROOT]] = 0

    root_neighbours = list(neighbours(ROOT))
    assert len(root_neighbours) == 16
    branch_label = {}
    for label, vertex in enumerate(root_neighbours, start=1):
        branch_label[vertex] = label
        assignment[index[vertex]] = label

    # Bits 0,...,14 of ROOT correspond, in order, to multipliers 2,...,16.
    for root_neighbour, label in branch_label.items():
        second_layer = [
            vertex for vertex in neighbours(root_neighbour) if vertex != ROOT
        ]
        assert len(second_layer) == 15
        for multiplier, vertex in zip(MULTIPLIERS, second_layer):
            assignment[index[vertex]] = multiplier * label % COLOR_COUNT

    # A distance-three vertex has exactly two distance-two neighbours; their
    # branch labels give the corresponding edge of K_16.  Its shared ROOT bit
    # identifies the multiplier column.
    for position, vertex in enumerate(vertices):
        if distances[position] != 3:
            continue
        parents = [
            adjacent
            for adjacent in neighbours(vertex)
            if adjacent in index and distances[index[adjacent]] == 2
        ]
        assert len(parents) == 2
        labels = []
        multiplier = None
        for parent in parents:
            added_bit = parent & (FULL_MASK ^ ROOT)
            assert bin(added_bit).count("1") == 1
            root_neighbour = (FULL_MASK ^ ROOT) ^ added_bit
            labels.append(branch_label[root_neighbour])

            retained_root_bit = vertex & ROOT
            assert bin(retained_root_bit).count("1") == 1
            bit_index = retained_root_bit.bit_length() - 1
            candidate_multiplier = bit_index + 2
            if multiplier is None:
                multiplier = candidate_multiplier
            else:
                assert multiplier == candidate_multiplier

        assert multiplier is not None
        left, right = sorted(labels)
        assignment[position] = columns[multiplier][left, right]

    assert all(colour >= 0 for colour in assignment)
    verify_assignment(vertices, distances, assignment, 3)
    return (vertices, distances, assignment), statistics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds-per-column", type=float, default=60)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()

    construction, statistics = construct(args.seconds_per_column, args.workers)
    result = {
        "radius": 3,
        "column_statistics": statistics,
        "status": "FEASIBLE" if construction is not None else "UNKNOWN",
    }
    if construction is not None:
        vertices, distances, assignment = construction
        result.update(
            {
                "vertices": len(vertices),
                "certificate_verified": True,
            }
        )
        if args.certificate is not None:
            payload = {
                "metadata": result,
                "vertices": [
                    {
                        "mask": vertex,
                        "distance": distance,
                        "colour": colour,
                    }
                    for vertex, distance, colour in zip(
                        vertices, distances, assignment
                    )
                ],
            }
            args.certificate.parent.mkdir(parents=True, exist_ok=True)
            args.certificate.write_text(
                json.dumps(payload, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

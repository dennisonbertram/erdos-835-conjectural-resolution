#!/usr/bin/env python3
"""Search a finite ball of O_16 for a locally bijective 17-colouring.

Vertices of O_16 are 15-subsets of a 31-set, represented by bit masks.
Two vertices are adjacent exactly when they are disjoint.  Every vertex
has 16 neighbours.  For every centre whose complete closed neighbourhood
lies in the generated ball, we require those 17 vertices to receive all
17 colours.

A feasible finite ball is only a consistency check, not a global
colouring.  An infeasible ball would be a rigorous finite obstruction.
"""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path

from ortools.sat.python import cp_model


POINT_COUNT = 31
SUBSET_SIZE = 15
COLOR_COUNT = 17
FULL_MASK = (1 << POINT_COUNT) - 1
ROOT = (1 << SUBSET_SIZE) - 1


def neighbours(vertex: int):
    """Yield the 16 disjoint 15-sets in deterministic bit order."""

    complement = FULL_MASK ^ vertex
    remaining = complement
    while remaining:
        omitted_bit = remaining & -remaining
        remaining ^= omitted_bit
        yield complement ^ omitted_bit


def generate_ball(radius: int) -> tuple[list[int], list[int]]:
    vertices = [ROOT]
    distances = [0]
    index = {ROOT: 0}
    queue = deque([ROOT])

    while queue:
        vertex = queue.popleft()
        distance = distances[index[vertex]]
        if distance == radius:
            continue
        for adjacent in neighbours(vertex):
            if adjacent not in index:
                index[adjacent] = len(vertices)
                vertices.append(adjacent)
                distances.append(distance + 1)
                queue.append(adjacent)

    return vertices, distances


def verify_assignment(
    vertices: list[int], distances: list[int], colours: list[int], radius: int
) -> None:
    index = {vertex: position for position, vertex in enumerate(vertices)}
    assert len(colours) == len(vertices)
    assert all(0 <= colour < COLOR_COUNT for colour in colours)
    for position, vertex in enumerate(vertices):
        if distances[position] >= radius:
            continue
        closed_colours = [colours[position]]
        for adjacent in neighbours(vertex):
            assert adjacent in index
            closed_colours.append(colours[index[adjacent]])
        assert sorted(closed_colours) == list(range(COLOR_COUNT))


def solve(radius: int, seconds: float, workers: int, encoding: str):
    vertices, distances = generate_ball(radius)
    index = {vertex: position for position, vertex in enumerate(vertices)}
    layer_sizes = [
        sum(distance == layer for distance in distances)
        for layer in range(radius + 1)
    ]

    model = cp_model.CpModel()
    colour = None
    indicator = None
    if encoding == "integer":
        colour = [
            model.NewIntVar(0, COLOR_COUNT - 1, f"c_{position}")
            for position in range(len(vertices))
        ]
    else:
        indicator = [
            [
                model.NewBoolVar(f"x_{position}_{assigned_colour}")
                for assigned_colour in range(COLOR_COUNT)
            ]
            for position in range(len(vertices))
        ]
        for row in indicator:
            model.AddExactlyOne(row)

    centre_count = 0
    for position, vertex in enumerate(vertices):
        if distances[position] >= radius:
            continue
        closed_positions = [position]
        closed_positions.extend(index[adjacent] for adjacent in neighbours(vertex))
        if encoding == "integer":
            assert colour is not None
            model.AddAllDifferent([colour[item] for item in closed_positions])
        else:
            assert indicator is not None
            for assigned_colour in range(COLOR_COUNT):
                model.AddExactlyOne(
                    indicator[item][assigned_colour] for item in closed_positions
                )
        centre_count += 1

    def fix(vertex: int, assigned_colour: int) -> None:
        if encoding == "integer":
            assert colour is not None
            model.Add(colour[index[vertex]] == assigned_colour)
        else:
            assert indicator is not None
            model.Add(indicator[index[vertex]][assigned_colour] == 1)

    # Remove the global S_17 colour symmetry.
    fix(ROOT, 0)
    root_neighbours = list(neighbours(ROOT))
    for assigned_colour, adjacent in enumerate(root_neighbours, start=1):
        fix(adjacent, assigned_colour)

    # The stabilizer of ROOT still permutes its 15 points freely.  Once the
    # root neighbours have their colours fixed, this permutes the 15
    # non-root neighbours of any one root neighbour.  Their colours must be
    # exactly the 15 colours other than the centre's colour and colour 0, so
    # prescribe their order to remove the residual S_15 symmetry.
    if radius >= 2:
        first_root_neighbour = root_neighbours[0]
        second_layer_branch = [
            adjacent
            for adjacent in neighbours(first_root_neighbour)
            if adjacent != ROOT
        ]
        assert len(second_layer_branch) == 15
        for assigned_colour, vertex in enumerate(second_layer_branch, start=2):
            fix(vertex, assigned_colour)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = workers
    status = solver.Solve(model)

    result = {
        "radius": radius,
        "layer_sizes": layer_sizes,
        "vertices": len(vertices),
        "constrained_centres": centre_count,
        "encoding": encoding,
        "status": solver.StatusName(status),
        "wall_time_seconds": solver.WallTime(),
        "branches": solver.NumBranches(),
        "conflicts": solver.NumConflicts(),
    }
    assignment = None
    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        if encoding == "integer":
            assert colour is not None
            assignment = [solver.Value(variable) for variable in colour]
        else:
            assert indicator is not None
            assignment = [
                next(
                    assigned_colour
                    for assigned_colour in range(COLOR_COUNT)
                    if solver.BooleanValue(indicator[position][assigned_colour])
                )
                for position in range(len(vertices))
            ]
        verify_assignment(vertices, distances, assignment, radius)
        result["certificate_verified"] = True
    return result, vertices, distances, assignment


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius", type=int, default=3)
    parser.add_argument("--seconds", type=float, default=300)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--encoding",
        choices=("boolean", "integer"),
        default="boolean",
        help="Boolean exact-cover is usually much faster than integer AllDifferent.",
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        help="Optional JSON path for a feasible assignment",
    )
    args = parser.parse_args()
    if args.radius < 1:
        parser.error("--radius must be positive")

    result, vertices, distances, assignment = solve(
        args.radius, args.seconds, args.workers, args.encoding
    )
    print(json.dumps(result, indent=2, sort_keys=True))

    if args.certificate is not None and assignment is not None:
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


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Decode a SAT model for the generic radius-4 CNF and verify its meaning.

This verifier checks the mathematical colouring rather than trusting the
SAT solver's status line.  It accepts standard SAT-competition ``v``
lines (as written by CaDiCaL ``-w``), recovers the 249,169 primary
one-hot variables, and independently verifies every closed
neighbourhood and all 32 symmetry normalizations.
"""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Iterator


POINTS = 31
SET_SIZE = 15
COLOURS = 17
RADIUS = 4
ALL_POINTS = (1 << POINTS) - 1
ROOT = (1 << SET_SIZE) - 1


def neighbours(vertex: int) -> Iterator[int]:
    unused = ALL_POINTS ^ vertex
    while unused:
        omitted = unused & -unused
        unused ^= omitted
        yield (ALL_POINTS ^ vertex) ^ omitted


def make_ball() -> tuple[list[int], list[int], dict[int, int]]:
    vertices, distances, locations = [ROOT], [0], {ROOT: 0}
    queue = deque([ROOT])
    while queue:
        vertex = queue.popleft()
        level = distances[locations[vertex]]
        if level == RADIUS:
            continue
        for next_vertex in neighbours(vertex):
            if next_vertex not in locations:
                locations[next_vertex] = len(vertices)
                vertices.append(next_vertex)
                distances.append(level + 1)
                queue.append(next_vertex)
    return vertices, distances, locations


def primary(vertex: int, colour: int) -> int:
    return COLOURS * vertex + colour + 1


def required_units(vertices: list[int], locations: dict[int, int]) -> list[tuple[int, int]]:
    units = [(locations[ROOT], 0)]
    root_neighbours = list(neighbours(ROOT))
    units.extend((locations[vertex], colour) for colour, vertex in enumerate(root_neighbours, 1))
    branch = [vertex for vertex in neighbours(root_neighbours[0]) if vertex != ROOT]
    units.extend((locations[vertex], colour) for colour, vertex in enumerate(branch, 2))
    assert len(units) == 32
    return units


def model_literals(path: Path) -> set[int]:
    positives: set[int] = set()
    saw_sat = False
    saw_assignment = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        fields = raw.split()
        if not fields or fields[0] == "c":
            continue
        if fields[0] == "s":
            if "SATISFIABLE" in fields[1:]:
                saw_sat = True
            elif "UNSATISFIABLE" in fields[1:]:
                raise ValueError("model file declares UNSATISFIABLE")
            continue
        if fields[0] != "v":
            raise ValueError(f"unsupported SAT-output line: {raw[:80]}")
        saw_assignment = True
        for field in fields[1:]:
            literal = int(field)
            if literal == 0:
                continue
            if literal > 0:
                positives.add(literal)
    if not saw_sat or not saw_assignment:
        raise ValueError("expected SATISFIABLE status and at least one v-line")
    return positives


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True, help="SAT-competition style model file")
    args = parser.parse_args()

    vertices, distances, locations = make_ball()
    if [sum(distance == item for distance in distances) for item in range(5)] != [1, 16, 240, 1800, 12600]:
        raise AssertionError("unexpected radius-4 ball")
    positive = model_literals(args.model)
    colours: list[int] = []
    for vertex in range(len(vertices)):
        selected = [colour for colour in range(COLOURS) if primary(vertex, colour) in positive]
        if len(selected) != 1:
            raise AssertionError(f"vertex {vertex} has {len(selected)} positive primary colours")
        colours.append(selected[0])
    for vertex, colour in required_units(vertices, locations):
        if colours[vertex] != colour:
            raise AssertionError(f"symmetry unit x({vertex},{colour}) is false")
    centres = 0
    for centre, vertex in enumerate(vertices):
        if distances[centre] == RADIUS:
            continue
        closed_colours = [colours[centre]] + [colours[locations[other]] for other in neighbours(vertex)]
        if sorted(closed_colours) != list(range(COLOURS)):
            raise AssertionError(f"closed neighbourhood at vertex position {centre} is not bijective")
        centres += 1
    print(json.dumps({
        "status": "PASS",
        "vertices": len(vertices),
        "constrained_centres": centres,
        "symmetry_units": 32,
        "colour_histogram": [colours.count(colour) for colour in range(COLOURS)],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

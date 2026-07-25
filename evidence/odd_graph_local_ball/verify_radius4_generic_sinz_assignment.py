#!/usr/bin/env python3
"""Independently verify a complete assignment for the generic radius-4 CNF.

This verifier has no dependency on the L/M/N constructor or the CNF generator.
It independently reconstructs the Odd-graph ball, checks the selected primary
colour of every vertex and every local closed neighbourhood, then streams the
given DIMACS file to check every clause under the complete model assignment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from pathlib import Path
from typing import Iterator


POINTS, SET_SIZE, COLOURS, RADIUS = 31, 15, 17, 4
ROOT = (1 << SET_SIZE) - 1
ALL_POINTS = (1 << POINTS) - 1
VERTICES = 14657
PRIMARY_COUNT = VERTICES * COLOURS
VARIABLES = PRIMARY_COUNT + VERTICES * (COLOURS - 1)


def neighbours(vertex: int) -> Iterator[int]:
    unused = ALL_POINTS ^ vertex
    while unused:
        omitted = unused & -unused
        unused ^= omitted
        yield (ALL_POINTS ^ vertex) ^ omitted


def make_ball() -> tuple[list[int], list[int], dict[int, int]]:
    vertices, distances, positions = [ROOT], [0], {ROOT: 0}
    queue = deque([ROOT])
    while queue:
        vertex = queue.popleft()
        distance = distances[positions[vertex]]
        if distance == RADIUS:
            continue
        for other in neighbours(vertex):
            if other not in positions:
                positions[other] = len(vertices)
                vertices.append(other)
                distances.append(distance + 1)
                queue.append(other)
    return vertices, distances, positions


def x(vertex: int, colour: int) -> int:
    return COLOURS * vertex + colour + 1


def required_units(vertices: list[int], positions: dict[int, int]) -> list[tuple[int, int]]:
    result = [(positions[ROOT], 0)]
    first_layer = list(neighbours(ROOT))
    result.extend((positions[vertex], colour) for colour, vertex in enumerate(first_layer, 1))
    branch = [vertex for vertex in neighbours(first_layer[0]) if vertex != ROOT]
    result.extend((positions[vertex], colour) for colour, vertex in enumerate(branch, 2))
    if len(result) != 32:
        raise AssertionError("wrong number of normal-form units")
    return result


def parse_model(path: Path) -> list[bool]:
    assignment: list[bool | None] = [None] * (VARIABLES + 1)
    status = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        fields = raw.split()
        if not fields or fields[0] == "c":
            continue
        if fields[0] == "s":
            status = fields[1:] == ["SATISFIABLE"]
            continue
        if fields[0] != "v":
            raise ValueError(f"unexpected model line: {raw[:80]}")
        for token in fields[1:]:
            literal = int(token)
            if literal == 0:
                continue
            if not 1 <= abs(literal) <= VARIABLES:
                raise ValueError(f"out-of-range literal {literal}")
            value = literal > 0
            previous = assignment[abs(literal)]
            if previous is not None and previous != value:
                raise ValueError(f"contradictory assignment for {abs(literal)}")
            assignment[abs(literal)] = value
    if not status or any(value is None for value in assignment[1:]):
        raise ValueError("expected SATISFIABLE and exactly one truth value for every variable")
    return [False] + [bool(value) for value in assignment[1:]]


def check_semantics(assignment: list[bool]) -> dict[str, object]:
    vertices, distances, positions = make_ball()
    if len(vertices) != VERTICES or [distances.count(i) for i in range(5)] != [1, 16, 240, 1800, 12600]:
        raise AssertionError("wrong radius-four ball")
    colours: list[int] = []
    for vertex in range(VERTICES):
        chosen = [colour for colour in range(COLOURS) if assignment[x(vertex, colour)]]
        if len(chosen) != 1:
            raise AssertionError(f"primary one-hot violation at vertex {vertex}")
        colours.append(chosen[0])
    for vertex, colour in required_units(vertices, positions):
        if colours[vertex] != colour:
            raise AssertionError(f"failed generic normal-form unit x({vertex},{colour})")
    centres = 0
    for centre, vertex in enumerate(vertices):
        if distances[centre] == RADIUS:
            continue
        closed = [colours[centre]] + [colours[positions[other]] for other in neighbours(vertex)]
        if sorted(closed) != list(range(COLOURS)):
            raise AssertionError(f"closed neighbourhood at {centre} is not rainbow")
        centres += 1
    return {"vertices": len(vertices), "constrained_centres": centres, "colour_histogram": [colours.count(c) for c in range(COLOURS)]}


def check_cnf(path: Path, assignment: list[bool]) -> tuple[int, str]:
    clauses = 0
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        header_seen = False
        for raw in stream:
            digest.update(raw)
            fields = raw.split()
            if not fields or fields[0] == b"c":
                continue
            if fields[0] == b"p":
                if header_seen or fields != [b"p", b"cnf", str(VARIABLES).encode(), b"738537"]:
                    raise ValueError("unexpected CNF header")
                header_seen = True
                continue
            if not header_seen or fields[-1] != b"0":
                raise ValueError("malformed DIMACS clause")
            literals = [int(token) for token in fields[:-1]]
            if not literals or any(abs(literal) > VARIABLES or literal == 0 for literal in literals):
                raise ValueError("invalid DIMACS literal")
            if not any(assignment[abs(literal)] == (literal > 0) for literal in literals):
                raise AssertionError(f"unsatisfied CNF clause {clauses + 1}")
            clauses += 1
    if clauses != 738537:
        raise AssertionError(f"wrong CNF clause count: {clauses}")
    return clauses, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    args = parser.parse_args()
    assignment = parse_model(args.model)
    semantic = check_semantics(assignment)
    clauses, cnf_sha256 = check_cnf(args.cnf, assignment)
    print(json.dumps({"status": "PASS", **semantic, "checked_clauses": clauses, "cnf_sha256": cnf_sha256}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

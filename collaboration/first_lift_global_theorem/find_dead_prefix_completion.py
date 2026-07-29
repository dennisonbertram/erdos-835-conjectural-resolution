#!/usr/bin/env python3
"""Find one full completion for the explicit dead-prefix support instance.

This is a search/derivation helper, not the durable verifier.  It imports the
repository's exact depth-first completion solver and prints a colouring that
the independent verifier can embed and re-check from first principles.
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path

from ortools.sat.python import cp_model


ROOT = Path(__file__).resolve().parents[2]
LIBRARY = ROOT / "collaboration/opus5/first_lift_k13_hole/first_lift.py"


def load_library():
    spec = importlib.util.spec_from_file_location("first_lift", LIBRARY)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def forbidden_rows() -> list[int]:
    missing_by_colour = [
        {6, 7, 10, 11, 12},
        {3, 7, 8, 11, 12},
        {3, 4, 8, 9, 12},
        {4, 5, 8, 9, 10},
        {5, 6, 9},
        {8, 9, 10, 11, 12},
        {0, 1, 2, 8, 9},
        {0, 3, 10, 11, 12},
        {0, 3, 10},
        {1, 4, 11},
        {1, 2, 3},
        {1, 2, 4},
        {0, 4, 5},
        {0, 5, 6},
        {1, 5, 7},
        {2, 6, 7},
        {2, 6, 7},
    ]
    rows = [0] * 13
    for colour, missing in enumerate(missing_by_colour):
        for vertex in missing:
            rows[vertex] |= 1 << colour
    return rows


def find_partial_witness(rows: list[int]):
    model = cp_model.CpModel()
    incidences = [
        (vertex, colour)
        for vertex in range(13)
        for colour in range(17)
        if (rows[vertex] >> colour) & 1
    ]
    labels = {
        incidence: model.new_int_var(0, 4, f"label_{incidence[0]}_{incidence[1]}")
        for incidence in incidences
    }
    for vertex in range(13):
        model.add_all_different(
            labels[vertex, colour]
            for colour in range(17)
            if (vertex, colour) in labels
        )
    missing_vertices = {
        colour: [
            vertex
            for vertex in range(13)
            if (vertex, colour) in labels
        ]
        for colour in range(17)
    }
    for colour, vertices in missing_vertices.items():
        model.add_all_different(labels[vertex, colour] for vertex in vertices)

    pairs = list(itertools.combinations(range(5), 2))
    size_three = [
        colour for colour, vertices in missing_vertices.items() if len(vertices) == 3
    ]
    choice = {
        (colour, pair_index): model.new_bool_var(
            f"pair_{colour}_{pair_index}"
        )
        for colour in size_three
        for pair_index in range(10)
    }
    for colour in size_three:
        model.add(sum(choice[colour, p] for p in range(10)) == 1)
    for pair_index in range(10):
        model.add(sum(choice[colour, pair_index] for colour in size_three) == 1)
    for colour in size_three:
        for pair_index, pair in enumerate(pairs):
            for vertex in missing_vertices[colour]:
                for label in pair:
                    model.add(labels[vertex, colour] != label).only_enforce_if(
                        choice[colour, pair_index]
                    )

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    status = solver.solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    array = [
        [
            next(
                colour
                for colour in range(17)
                if (vertex, colour) in labels
                and solver.value(labels[vertex, colour]) == label
            )
            for label in range(5)
        ]
        for vertex in range(13)
    ]
    pair_colours = {}
    for colour in size_three:
        pair_index = next(
            p for p in range(10) if solver.value(choice[colour, p])
        )
        pair_colours[pairs[pair_index]] = colour
    return array, pair_colours


def main() -> None:
    library = load_library()
    rows = forbidden_rows()
    library.check_instance_shape(13, 17, rows)
    assert library.in_class_B(13, 17, rows)
    array, pair_colours = find_partial_witness(rows)
    print("partial array:")
    for row in array:
        print(row)
    print(f"internal pair colours: {sorted(pair_colours.items())}")
    status, colouring, nodes = library.solve(13, 17, rows)
    assert status == "SAT" and colouring is not None
    print(f"status={status} nodes={nodes}")
    for colour in range(17):
        edges = sorted(edge for edge, value in colouring.items() if value == colour)
        print(f"{colour}: {edges}")


if __name__ == "__main__":
    main()

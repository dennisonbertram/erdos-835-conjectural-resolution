#!/usr/bin/env python3
"""Search the minimum selected-layer changes completing the r=1 instance."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations

from ortools.sat.python import cp_model

from verify_r1_minimum_layer_repair import all_perfect_matchings, build_instance


def main() -> None:
    selected, selected_supports, remaining_supports = build_instance()
    supports = (*selected_supports, *remaining_supports)
    all_edges = tuple(
        (left, right)
        for left in range(13)
        for right in range(left + 1, 13)
    )

    for repair_distance in range(1, 8):
        for changed_colours_tuple in combinations(range(7), repair_distance):
            changed_colours = frozenset(changed_colours_tuple)
            completion = solve_with_changed_colours(
                selected,
                supports,
                all_edges,
                changed_colours,
            )
            if completion is None:
                continue

            print(
                f"MINIMUM_FULL_REPAIR_DISTANCE={repair_distance} "
                f"changed_colours={changed_colours_tuple}"
            )
            print("FULL_COMPLETION = (")
            for current in completion:
                print(f"    {tuple(sorted(current))},")
            print(")")
            return

    print("NO full repair found")


def solve_with_changed_colours(
    selected: list[frozenset[tuple[int, int]]],
    supports: tuple[frozenset[int], ...],
    all_edges: tuple[tuple[int, int], ...],
    changed_colours: frozenset[int],
) -> list[frozenset[tuple[int, int]]] | None:
    model = cp_model.CpModel()
    variables_by_colour: list[list[tuple[object, frozenset[tuple[int, int]]]]] = []
    variables_by_edge: dict[
        tuple[int, int],
        list[object],
    ] = defaultdict(list)

    for colour, support in enumerate(supports):
        if colour < 7 and colour not in changed_colours:
            candidates = (selected[colour],)
        else:
            candidates = tuple(
                frozenset(matching)
                for matching in all_perfect_matchings(tuple(sorted(support)))
            )

        colour_variables = []
        for candidate_index, candidate in enumerate(candidates):
            variable = model.new_bool_var(f"x_{colour}_{candidate_index}")
            colour_variables.append((variable, candidate))
            for current in candidate:
                variables_by_edge[current].append(variable)
        variables_by_colour.append(colour_variables)
        model.add_exactly_one(variable for variable, _ in colour_variables)

    for current in all_edges:
        model.add_exactly_one(variables_by_edge[current])

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 83513
    status = solver.solve(model)
    print(
        f"changed_colours={tuple(sorted(changed_colours))} "
        f"status={solver.status_name(status)} "
        f"wall={solver.wall_time:.3f}s"
    )
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None

    completion = []
    for colour_variables in variables_by_colour:
        chosen = [
            candidate
            for variable, candidate in colour_variables
            if solver.value(variable)
        ]
        assert len(chosen) == 1
        completion.append(chosen[0])

    return completion


if __name__ == "__main__":
    main()

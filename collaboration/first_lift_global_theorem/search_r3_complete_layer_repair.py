#!/usr/bin/env python3
"""Search for full completions maximizing retained r=3 prefix layers.

This is a discovery helper.  The durable verifier uses only the standard
library and literal completion certificates found here.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations

from ortools.sat.python import cp_model

from verify_r3_dead_seven_prefixes import (
    ALL_EDGES,
    CASES,
    VERTICES,
    edge,
    endpoints,
    perfect_matching,
)


Matching = tuple[tuple[int, int], ...]


@lru_cache(maxsize=None)
def all_perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for rest in all_perfect_matchings(remaining):
            result.append((edge(first, second), *rest))
    return tuple(result)


def find_eighth_repair(
    name: str,
    case: dict[str, object],
) -> None:
    prefix = case["prefix"]
    remaining_complements = case["remaining_complements"]
    assert isinstance(prefix, tuple)
    assert isinstance(remaining_complements, tuple)
    selected_supports = tuple(endpoints(current) for current in prefix)
    remaining_supports = tuple(
        VERTICES - complement for complement in remaining_complements
    )
    best = None
    for colour, (original, support) in enumerate(
        zip(prefix, selected_supports)
    ):
        fixed = frozenset().union(
            *(
                current
                for index, current in enumerate(prefix)
                if index != colour
            )
        )
        for candidate_tuple in all_perfect_matchings(tuple(sorted(support))):
            candidate = frozenset(candidate_tuple)
            if candidate == original or not candidate.isdisjoint(fixed):
                continue
            for remaining_index, remaining_support in enumerate(
                remaining_supports
            ):
                for eighth_tuple in all_perfect_matchings(
                    tuple(sorted(remaining_support))
                ):
                    eighth = frozenset(eighth_tuple)
                    if eighth.isdisjoint(fixed | candidate):
                        key = (
                            len(original - candidate),
                            colour,
                            tuple(sorted(candidate)),
                            remaining_index,
                            tuple(sorted(eighth)),
                        )
                        if best is None or key < best[0]:
                            best = (key, candidate, remaining_index, eighth)
                        break
    assert best is not None
    key, candidate, remaining_index, eighth = best
    print(
        f"{name}: A changed=1, edge_changes={key[0]}, colour={key[1]}, "
        f"replacement={tuple(sorted(candidate))}, remaining={remaining_index}, "
        f"eighth={tuple(sorted(eighth))}"
    )


def solve_case(
    name: str,
    case: dict[str, object],
) -> tuple[int, tuple[frozenset[tuple[int, int]], ...]]:
    prefix = case["prefix"]
    remaining_complements = case["remaining_complements"]
    assert isinstance(prefix, tuple)
    assert isinstance(remaining_complements, tuple)
    selected_supports = tuple(endpoints(current) for current in prefix)
    remaining_supports = tuple(
        VERTICES - complement for complement in remaining_complements
    )
    supports = (*selected_supports, *remaining_supports)
    assert Counter(map(len, supports)) == {8: 10, 10: 4, 12: 3}

    model = cp_model.CpModel()
    variables = {}
    for colour, support in enumerate(supports):
        for current in combinations(sorted(support), 2):
            variables[colour, current] = model.new_bool_var(
                f"x_{colour}_{current[0]}_{current[1]}"
            )

    for current in combinations(sorted(VERTICES), 2):
        model.add(
            sum(
                variables[colour, current]
                for colour, support in enumerate(supports)
                if current[0] in support and current[1] in support
            )
            == 1
        )

    for colour, support in enumerate(supports):
        for vertex in support:
            model.add(
                sum(
                    variables[colour, edge(vertex, other)]
                    for other in support
                    if other != vertex
                )
                == 1
            )

    retained = []
    for colour, original in enumerate(prefix):
        keep = model.new_bool_var(f"retained_{colour}")
        retained.append(keep)
        for current in original:
            model.add(variables[colour, current] == 1).only_enforce_if(keep)
        model.add(
            sum(variables[colour, current] for current in original)
            <= len(original) - 1 + keep
        )
    model.maximize(sum(retained))

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 835
    status = solver.solve(model)
    assert status == cp_model.OPTIMAL
    optimum = sum(solver.value(keep) for keep in retained)
    completion = tuple(
        frozenset(
            current
            for current in combinations(sorted(support), 2)
            if solver.value(variables[colour, current])
        )
        for colour, support in enumerate(supports)
    )
    assert sum(map(len, completion)) == 78
    print(f"{name}: retained={optimum}/7, changed={7 - optimum}")
    for colour, current in enumerate(completion):
        marker = " RETAINED" if colour < 7 and current == prefix[colour] else ""
        print(f"{colour}: {tuple(sorted(current))}{marker}")
    return optimum, completion


def diagnose_retained_subsets(
    name: str,
    case: dict[str, object],
    retained_count: int,
) -> None:
    prefix = case["prefix"]
    assert isinstance(prefix, tuple)
    supports = (
        *(endpoints(current) for current in prefix),
        *(
            VERTICES - complement
            for complement in case["remaining_complements"]
        ),
    )
    direct = 0
    hard = []
    for fixed_colours in combinations(range(7), retained_count):
        fixed_union = frozenset().union(
            *(prefix[colour] for colour in fixed_colours)
        )
        blocked = [
            colour
            for colour, support in enumerate(supports)
            if colour not in fixed_colours
            and perfect_matching(support, ALL_EDGES - fixed_union) is None
        ]
        if blocked:
            direct += 1
        else:
            hard.append(fixed_colours)
    print(
        f"{name}: retained-subset direct obstruction "
        f"{direct}/{direct + len(hard)}; hard={hard}"
    )


def main() -> None:
    for name, case in CASES.items():
        find_eighth_repair(name, case)
        optimum, _ = solve_case(name, case)
        diagnose_retained_subsets(name, case, optimum + 1)


if __name__ == "__main__":
    main()

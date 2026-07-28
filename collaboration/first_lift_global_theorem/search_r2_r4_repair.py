#!/usr/bin/env python3
"""Discover maximum-retention full repairs for the r=2/r=4 prefixes."""

from __future__ import annotations

from itertools import combinations

from ortools.sat.python import cp_model

import verify_r2_dead_seven_prefix as r2
import verify_r4_dead_seven_prefix as r4


def solve_case(name: str, certificate: object) -> None:
    prefix, complements = certificate.build_certificate()
    supports = certificate.verify_certificate(prefix, complements)
    model = cp_model.CpModel()
    variables = {
        (colour, current): model.new_bool_var(
            f"x_{colour}_{current[0]}_{current[1]}"
        )
        for colour, support in enumerate(supports)
        for current in combinations(sorted(support), 2)
    }
    for current in sorted(r2.ALL_EDGES):
        model.add(
            sum(
                variables[colour, current]
                for colour, support in enumerate(supports)
                if set(current) <= support
            )
            == 1
        )
    for colour, support in enumerate(supports):
        for vertex in support:
            model.add(
                sum(
                    variables[colour, tuple(sorted((vertex, other)))]
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
    solver.parameters.random_seed = 83524
    status = solver.solve(model)
    assert status == cp_model.OPTIMAL
    completion = tuple(
        frozenset(
            current
            for current in combinations(sorted(support), 2)
            if solver.value(variables[colour, current])
        )
        for colour, support in enumerate(supports)
    )
    kept = tuple(
        colour
        for colour in range(7)
        if completion[colour] == prefix[colour]
    )
    assert len(kept) == round(solver.objective_value)
    assert frozenset().union(*completion) == r2.ALL_EDGES
    print(
        f"{name}: status=OPTIMAL retained={len(kept)}/7 "
        f"changed={7 - len(kept)} kept={kept} wall={solver.wall_time:.6f}"
    )
    print(
        "COMPLETION =",
        tuple(tuple(sorted(current)) for current in completion),
    )


def main() -> None:
    solve_case("r2", r2)
    solve_case("r4", r4)


if __name__ == "__main__":
    main()

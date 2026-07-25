#!/usr/bin/env python3
"""Global CP-SAT maximum-partial-colouring search for LS(3,4,20).

There is one Boolean variable for every (4-set, colour) pair.  A block gets
at most one colour, and for each (triple, colour) at most one extension gets
that colour.  Thus every feasible assignment is a proper partial colouring
of J(20,4).  Objective 4,845 is exactly an LS(3,4,20), and any such solution
is written as a certificate for the independent verifier.

Failure or an objective below 4,845 proves nothing about existence.
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path

from ortools.sat.python import cp_model


V = 20
Q = 17
BLOCKS = list(itertools.combinations(range(V), 4))
INDEX = {block: r for r, block in enumerate(BLOCKS)}


def load_partial(path: Path) -> list[int]:
    values: list[int] = []
    with path.open(encoding="utf-8") as handle:
        for row, line in enumerate(handle):
            fields = [int(value) for value in line.split()]
            if len(fields) != 5:
                raise ValueError(f"line {row + 1}: expected five integers")
            block = tuple(fields[:4])
            if row >= len(BLOCKS) or block != BLOCKS[row]:
                raise ValueError(f"line {row + 1}: unexpected block order")
            if not -1 <= fields[4] < Q:
                raise ValueError(f"line {row + 1}: bad colour")
            values.append(fields[4])
    if len(values) != len(BLOCKS):
        raise ValueError(f"expected {len(BLOCKS)} rows, got {len(values)}")
    return values


def verify_partial(values: list[int]) -> None:
    for triple in itertools.combinations(range(V), 3):
        colours = [
            values[INDEX[tuple(sorted(triple + (x,)))]]
            for x in range(V)
            if x not in triple
        ]
        assigned = [colour for colour in colours if colour >= 0]
        if len(assigned) != len(set(assigned)):
            raise ValueError(f"initial conflict at triple {triple}")


class FullSolution(cp_model.CpSolverSolutionCallback):
    def __init__(
        self,
        variables: list[list[cp_model.IntVar]],
        output: Path,
    ) -> None:
        super().__init__()
        self.variables = variables
        self.output = output
        self.best = 0

    def on_solution_callback(self) -> None:
        objective = round(self.objective_value)
        if objective > self.best:
            self.best = objective
            print(
                f"CP-SAT partial objective {objective}; "
                f"uncoloured {len(BLOCKS) - objective}; "
                f"time {self.wall_time:.3f}s",
                flush=True,
            )
        if objective != len(BLOCKS):
            return

        colours = []
        for row in self.variables:
            selected = [
                colour for colour, variable in enumerate(row)
                if self.value(variable)
            ]
            if len(selected) != 1:
                raise RuntimeError("full objective without unique colour")
            colours.append(selected[0])

        verify_partial(colours)
        self.output.parent.mkdir(parents=True, exist_ok=True)
        with self.output.open("w", encoding="utf-8") as handle:
            for block, colour in zip(BLOCKS, colours):
                handle.write("{} {} {} {} {}\n".format(*block, colour))
        print(
            f"FOUND and internally verified LS(3,4,20); wrote {self.output}",
            flush=True,
        )
        self.stop_search()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("partial", type=Path)
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--lns-only", action="store_true")
    parser.add_argument("--log", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evidence/ls_3_4_20_witness.txt"),
    )
    args = parser.parse_args()

    initial = load_partial(args.partial)
    verify_partial(initial)
    print(
        f"verified warm start with {sum(c < 0 for c in initial)} "
        "uncoloured blocks"
    )

    model = cp_model.CpModel()
    selected = [
        [model.new_bool_var(f"x_{r}_{colour}") for colour in range(Q)]
        for r in range(len(BLOCKS))
    ]
    for row in selected:
        model.add_at_most_one(row)

    for triple in itertools.combinations(range(V), 3):
        star = [
            INDEX[tuple(sorted(triple + (x,)))]
            for x in range(V)
            if x not in triple
        ]
        for colour in range(Q):
            model.add_at_most_one(selected[r][colour] for r in star)

    # Fix the global colour permutation at a completely assigned star,
    # preserving the supplied warm start.
    for triple in itertools.combinations(range(V), 3):
        star = [
            INDEX[tuple(sorted(triple + (x,)))]
            for x in range(V)
            if x not in triple
        ]
        if all(initial[r] >= 0 for r in star):
            assert len({initial[r] for r in star}) == Q
            for r in star:
                model.add(selected[r][initial[r]] == 1)
            print(f"fixed colour symmetry at triple {triple}")
            break
    else:
        raise ValueError("warm start has no fully assigned triple-star")

    for r, colour in enumerate(initial):
        for c in range(Q):
            model.add_hint(selected[r][c], int(c == colour))

    objective = sum(variable for row in selected for variable in row)
    initial_objective = sum(colour >= 0 for colour in initial)
    # The supplied complete Boolean hint witnesses this lower bound.  Keeping
    # it explicit prevents the portfolio from spending time on worse partial
    # colourings before launching repair neighbourhoods.
    model.add(objective >= initial_objective)
    model.maximize(objective)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    solver.parameters.log_search_progress = args.log
    solver.parameters.use_lns_only = args.lns_only
    # Presolve's additional graph-automorphism symmetry breaking need not
    # preserve a complete warm-start hint.  Colour symmetry is already fixed
    # explicitly above, so disable it to keep the 4,773-block incumbent.
    solver.parameters.symmetry_level = 0
    callback = FullSolution(selected, args.output)
    status = solver.solve(model, callback)
    print(
        f"status={solver.status_name(status)} "
        f"best_objective={callback.best} "
        f"bound={solver.best_objective_bound:.0f} "
        f"wall={solver.wall_time:.3f}s"
    )
    if callback.best != len(BLOCKS):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Native CP-SAT search for the C17-equivariant LS(3,4,20) extension.

This is a witness search, not a proof of infeasibility.  SAT output must be
replayed by ``verify_c17_equivariant_cnf.py --model`` before it is used as a
mathematical certificate.  UNKNOWN, including a timeout, has no negative
evidentiary value.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ortools.sat.python import cp_model

from generate_c17_equivariant_cnf import P, variable
from search_c17_equivariant_exact_cover import build_exact_cover
from search_c17_equivariant_min_conflicts import build_csp, star_penalty


def write_model(path: Path, assignment: tuple[int, ...]) -> None:
    """Write the selected positive DIMACS literals without overwriting."""

    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    literals = [
        variable(orbit, phase)
        for orbit, phase in enumerate(assignment)
    ]
    path.write_text(
        "s SATISFIABLE\nv " + " ".join(map(str, literals)) + " 0\n",
        encoding="ascii",
    )


def solve_phase_model(
    args: argparse.Namespace,
) -> tuple[cp_model.CpSolver, int, tuple[int, ...] | None]:
    """Preserve the 57 native all-different constraints."""

    blocks, stars, domains, _affected = build_csp()
    model = cp_model.CpModel()
    phases = [
        model.new_int_var_from_domain(
            cp_model.Domain.from_values(domain),
            f"phase_{orbit}",
        )
        for orbit, domain in enumerate(domains)
    ]

    for star_index, entries in enumerate(stars):
        colours = []
        for entry_index, (orbit, shift) in enumerate(entries):
            colour = model.new_int_var(
                0,
                P - 1,
                f"colour_{star_index}_{entry_index}",
            )
            model.add_modulo_equality(
                colour,
                phases[orbit] + shift,
                P,
            )
            colours.append(colour)
        model.add_all_different(colours)

    solver = configured_solver(args)
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver, status, None
    assignment = tuple(solver.value(phase) for phase in phases)
    assert len(assignment) == len(blocks) == 228
    assert all(
        assignment[orbit] in domains[orbit]
        for orbit in range(len(assignment))
    )
    assert all(
        star_penalty(list(assignment), entries) == 0
        for entries in stars
    )
    return solver, status, assignment


def solve_exact_cover_model(
    args: argparse.Namespace,
) -> tuple[cp_model.CpSolver, int, tuple[int, ...] | None]:
    """Use one Boolean per allowed orbit phase and 1,140 exact-one rows."""

    columns, rows = build_exact_cover()
    model = cp_model.CpModel()
    selected = {
        row: model.new_bool_var(f"row_{row}")
        for row in rows
    }
    for column, options in columns.items():
        model.add_exactly_one(selected[row] for row in options)
    if args.fixed_rows_json is not None:
        fixed = json.loads(args.fixed_rows_json.read_text())["selected_rows"]
        assert len(fixed) == len(set(fixed))
        for row in fixed:
            model.add(selected[row] == 1)
    if args.hint_rows_json is not None:
        hinted = set(
            json.loads(args.hint_rows_json.read_text())["selected_rows"]
        )
        assert hinted <= set(rows)
        for row, literal in selected.items():
            model.add_hint(literal, int(row in hinted))

    solver = configured_solver(args)
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return solver, status, None
    chosen = tuple(
        sorted(row for row in rows if solver.value(selected[row]))
    )
    assert len(chosen) == 228
    assignment = [-1] * 228
    for row in chosen:
        orbit, phase = divmod(row - 1, P)
        assert assignment[orbit] == -1
        assignment[orbit] = phase
    assert all(phase >= 0 for phase in assignment)
    return solver, status, tuple(assignment)


def configured_solver(args: argparse.Namespace) -> cp_model.CpSolver:
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    solver.parameters.log_search_progress = args.log_search
    return solver


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--log-search", action="store_true")
    parser.add_argument(
        "--encoding",
        choices=("phase", "exact-cover"),
        default="phase",
    )
    parser.add_argument("--fixed-rows-json", type=Path)
    parser.add_argument("--hint-rows-json", type=Path)
    args = parser.parse_args()
    if args.encoding != "exact-cover" and (
        args.fixed_rows_json is not None
        or args.hint_rows_json is not None
    ):
        parser.error("row fixing and hints require --encoding exact-cover")

    if args.encoding == "phase":
        solver, status, assignment = solve_phase_model(args)
    else:
        solver, status, assignment = solve_exact_cover_model(args)
    print(
        f"status={solver.status_name(status)} "
        f"encoding={args.encoding} "
        f"wall={solver.wall_time:.3f} "
        f"branches={solver.num_branches} "
        f"conflicts={solver.num_conflicts}"
    )

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(
            "scope: non-SAT status is telemetry unless independently "
            "certified; no portable infeasibility claim"
        )
        raise SystemExit(2)

    assert assignment is not None
    write_model(args.output, assignment)
    print(f"SAT_CANDIDATE phases={len(assignment)} output={args.output}")
    print("scope: candidate only until independent semantic verification")


if __name__ == "__main__":
    main()

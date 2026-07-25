#!/usr/bin/env python3
"""Search the first genuinely global layer of a cyclic-17 tight colouring.

The moving points and the colours are Z/17.  The fifteen fixed points are
indexed by the fifteen circulant golf squares in ``global_latin_audit``.
For each pair {i,j} of fixed points, this script seeks a translation-
equivariant colour map on moving triples such that every moving-pair star,
together with the two already fixed golf-square colours, is rainbow.

Each fixed-pair slice is a finite CSP.  Slices are independent only for the
pair-star equations; a genuine next-layer boundary must additionally satisfy
the shared compatibility encoded by ``--joint``.  Even a joint solution is
only a block-layer-three certificate, not a full LS(15,16,32).
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

from global_latin_audit import construct_golf17


P = 17
POINTS = tuple(range(P))
FIXED = tuple(range(15))
MOVING_PAIRS = tuple(combinations(POINTS, 2))
MOVING_TRIPLES = tuple(combinations(POINTS, 3))
FIXED_PAIRS = tuple(combinations(FIXED, 2))


def translate(subset: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return tuple(sorted((x + amount) % P for x in subset))


def orbit_table(
    subsets: tuple[tuple[int, ...], ...],
) -> tuple[list[tuple[int, ...]], dict[tuple[int, ...], tuple[int, int]]]:
    """Return canonical representatives and (orbit index, shift) for subsets."""
    representatives: list[tuple[int, ...]] = []
    lookup: dict[tuple[int, ...], tuple[int, int]] = {}
    unseen = set(subsets)
    while unseen:
        seed = min(unseen)
        orbit = [translate(seed, t) for t in POINTS]
        representative = min(orbit)
        orbit_index = len(representatives)
        representatives.append(representative)
        for shift in POINTS:
            member = translate(representative, shift)
            assert member not in lookup
            lookup[member] = (orbit_index, shift)
            unseen.discard(member)
    assert len(lookup) == len(subsets)
    return representatives, lookup


PAIR_REPRESENTATIVES, PAIR_LOOKUP = orbit_table(MOVING_PAIRS)
TRIPLE_REPRESENTATIVES, TRIPLE_LOOKUP = orbit_table(MOVING_TRIPLES)


def solve_fixed_pair(
    golf: list[list[list[int]]],
    fixed_pair: tuple[int, int],
    seconds: float,
    seed: int,
) -> tuple[str, list[int] | None]:
    """Solve one of the 105 independent translation-quotient problems.

    We use the colour-zero exact-cover form.  Its leave is the union of the
    two one-factors on which the two golf squares take value zero.  Choose
    exactly one translate from each moving-triple orbit so that the chosen
    forty triples decompose every edge outside that leave exactly once.
    """
    i, j = fixed_pair
    model = cp_model.CpModel()
    chosen = [
        [
            model.NewBoolVar(f"x_{orbit_index}_{shift}")
            for shift in POINTS
        ]
        for orbit_index in range(len(TRIPLE_REPRESENTATIVES))
    ]
    for orbit_variables in chosen:
        model.AddExactlyOne(orbit_variables)

    leave = {
        pair
        for pair in MOVING_PAIRS
        if golf[i][pair[0]][pair[1]] == 0
        or golf[j][pair[0]][pair[1]] == 0
    }
    assert len(leave) == 16
    for pair in MOVING_PAIRS:
        occurrences: list[cp_model.BoolVar] = []
        for orbit_index, representative in enumerate(TRIPLE_REPRESENTATIVES):
            for shift in POINTS:
                if set(pair) <= set(translate(representative, shift)):
                    occurrences.append(chosen[orbit_index][shift])
        assert len(occurrences) == 15
        if pair in leave:
            model.Add(sum(occurrences) == 0)
        else:
            model.Add(sum(occurrences) == 1)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = seed
    status = solver.Solve(model)
    name = solver.StatusName(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return name, None
    phases: list[int] = []
    for orbit_variables in chosen:
        selected = [
            shift
            for shift, variable in enumerate(orbit_variables)
            if solver.Value(variable)
        ]
        assert len(selected) == 1
        phases.append((-selected[0]) % P)
    return name, phases


def solve_fixed_pair_sat(
    golf: list[list[list[int]]],
    fixed_pair: tuple[int, int],
    solver_name: str,
) -> tuple[str, list[int] | None]:
    """The same exact-cover model using an independently installed SAT core."""
    i, j = fixed_pair

    def variable(orbit_index: int, shift: int) -> int:
        return 1 + P * orbit_index + shift

    def exactly_one(variables: list[int], clauses: list[list[int]]) -> None:
        clauses.append(variables)
        clauses.extend([-a, -b] for a, b in combinations(variables, 2))

    clauses: list[list[int]] = []
    for orbit_index in range(len(TRIPLE_REPRESENTATIVES)):
        exactly_one(
            [variable(orbit_index, shift) for shift in POINTS],
            clauses,
        )

    leave = {
        pair
        for pair in MOVING_PAIRS
        if golf[i][pair[0]][pair[1]] == 0
        or golf[j][pair[0]][pair[1]] == 0
    }
    assert len(leave) == 16
    for pair in MOVING_PAIRS:
        occurrences: list[int] = []
        for orbit_index, representative in enumerate(TRIPLE_REPRESENTATIVES):
            for shift in POINTS:
                if set(pair) <= set(translate(representative, shift)):
                    occurrences.append(variable(orbit_index, shift))
        assert len(occurrences) == 15
        if pair in leave:
            clauses.extend([[-literal] for literal in occurrences])
        else:
            exactly_one(occurrences, clauses)

    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        if not solver.solve():
            return "INFEASIBLE", None
        positive = {literal for literal in solver.get_model() if literal > 0}

    phases: list[int] = []
    for orbit_index in range(len(TRIPLE_REPRESENTATIVES)):
        selected = [
            shift
            for shift in POINTS
            if variable(orbit_index, shift) in positive
        ]
        assert len(selected) == 1
        phases.append((-selected[0]) % P)
    return "FEASIBLE", phases


def solve_fixed_pair_sat_worker(
    task: tuple[tuple[int, int], str],
) -> tuple[tuple[int, int], str, list[int] | None]:
    """Pickle-safe worker for a portfolio of independent fixed-pair slices."""
    fixed_pair, solver_name = task
    status, phases = solve_fixed_pair_sat(
        construct_golf17(), fixed_pair, solver_name
    )
    return fixed_pair, status, phases


def colour_from_phases(triple: tuple[int, int, int], phases: list[int]) -> int:
    orbit_index, shift = TRIPLE_LOOKUP[triple]
    return (phases[orbit_index] + shift) % P


def verify_certificate(certificate: dict[str, list[int]]) -> None:
    """Backend-independent semantic verification of every stored phase list."""
    golf = construct_golf17()
    assert len(PAIR_REPRESENTATIVES) == 8
    assert len(TRIPLE_REPRESENTATIVES) == 40
    assert len(certificate) == len(FIXED_PAIRS)

    for i, j in FIXED_PAIRS:
        phases = certificate[f"{i},{j}"]
        assert len(phases) == len(TRIPLE_REPRESENTATIVES)
        assert all(isinstance(value, int) and 0 <= value < P for value in phases)

        for pair in MOVING_PAIRS:
            star_colours = {
                golf[i][pair[0]][pair[1]],
                golf[j][pair[0]][pair[1]],
            }
            for z in POINTS:
                if z not in pair:
                    triple = tuple(sorted((*pair, z)))
                    star_colours.add(colour_from_phases(triple, phases))
            assert star_colours == set(POINTS)

        for triple in MOVING_TRIPLES:
            for shift in POINTS:
                translated = translate(triple, shift)
                assert colour_from_phases(
                    translated, phases
                ) == (colour_from_phases(triple, phases) + shift) % P


def verify_single_fixed_pair(
    certificate: dict[str, list[int]],
    fixed_pair: tuple[int, int],
) -> None:
    """Verify one diagnostic slice without pretending all 105 are present."""
    golf = construct_golf17()
    i, j = fixed_pair
    phases = certificate[f"{i},{j}"]
    assert len(phases) == len(TRIPLE_REPRESENTATIVES)
    assert all(isinstance(value, int) and 0 <= value < P for value in phases)
    for pair in MOVING_PAIRS:
        colours = {golf[i][pair[0]][pair[1]], golf[j][pair[0]][pair[1]]}
        colours.update(
            colour_from_phases(tuple(sorted((*pair, z))), phases)
            for z in POINTS
            if z not in pair
        )
        assert colours == set(POINTS)
    for triple in MOVING_TRIPLES:
        for shift in POINTS:
            assert colour_from_phases(
                translate(triple, shift), phases
            ) == (colour_from_phases(triple, phases) + shift) % P


def verify_joint_compatibility(certificate: dict[str, list[int]]) -> None:
    """Check the cross-slice condition needed before the next block layer."""
    verify_certificate(certificate)
    for fixed_triple in combinations(FIXED, 3):
        fixed_edges = tuple(combinations(fixed_triple, 2))
        for moving_triple in MOVING_TRIPLES:
            colours = {
                colour_from_phases(
                    moving_triple,
                    certificate[f"{edge[0]},{edge[1]}"],
                )
                for edge in fixed_edges
            }
            assert len(colours) == 3


def solve_joint_sat(
    golf: list[list[list[int]]],
    solver_name: str,
) -> tuple[str, dict[str, list[int]] | None, dict[str, int]]:
    """Solve all 105 slices with their required shared-boundary constraints."""
    pair_index = {pair: index for index, pair in enumerate(FIXED_PAIRS)}
    orbit_count = len(TRIPLE_REPRESENTATIVES)
    primary_count = len(FIXED_PAIRS) * orbit_count * P

    def variable(fixed_pair: tuple[int, int], orbit_index: int, shift: int) -> int:
        return (
            1
            + ((pair_index[fixed_pair] * orbit_count + orbit_index) * P)
            + shift
        )

    pool = IDPool(start_from=primary_count + 1)
    clauses: list[list[int]] = []

    def exactly_one(literals: list[int]) -> None:
        clauses.extend(
            CardEnc.equals(
                lits=literals,
                bound=1,
                vpool=pool,
                encoding=EncType.seqcounter,
            ).clauses
        )

    def at_most_one(literals: list[int]) -> None:
        clauses.extend(
            CardEnc.atmost(
                lits=literals,
                bound=1,
                vpool=pool,
                encoding=EncType.seqcounter,
            ).clauses
        )

    translated_triples = [
        [translate(representative, shift) for shift in POINTS]
        for representative in TRIPLE_REPRESENTATIVES
    ]
    triples_containing_pair: dict[tuple[int, int], list[tuple[int, int]]] = {
        pair: [] for pair in MOVING_PAIRS
    }
    for orbit_index in range(orbit_count):
        for shift in POINTS:
            triple = translated_triples[orbit_index][shift]
            for pair in combinations(triple, 2):
                triples_containing_pair[pair].append((orbit_index, shift))
    assert all(
        len(occurrences) == 15
        for occurrences in triples_containing_pair.values()
    )

    for fixed_pair in FIXED_PAIRS:
        for orbit_index in range(orbit_count):
            exactly_one(
                [
                    variable(fixed_pair, orbit_index, shift)
                    for shift in POINTS
                ]
            )

        i, j = fixed_pair
        leave = {
            pair
            for pair in MOVING_PAIRS
            if golf[i][pair[0]][pair[1]] == 0
            or golf[j][pair[0]][pair[1]] == 0
        }
        assert len(leave) == 16
        for moving_pair, occurrences in triples_containing_pair.items():
            literals = [
                variable(fixed_pair, orbit_index, shift)
                for orbit_index, shift in occurrences
            ]
            if moving_pair in leave:
                clauses.extend([[-literal] for literal in literals])
            else:
                exactly_one(literals)

    # If two fixed-pair slices share a fixed point, the corresponding
    # r=3 blocks are adjacent.  For every moving-triple orbit, their phases
    # must therefore differ.  In colour-zero translates this says at most
    # one incident fixed edge may select a given shift.
    for fixed_point in FIXED:
        incident = [
            pair for pair in FIXED_PAIRS if fixed_point in pair
        ]
        assert len(incident) == 14
        for orbit_index in range(orbit_count):
            for shift in POINTS:
                at_most_one(
                    [
                        variable(fixed_pair, orbit_index, shift)
                        for fixed_pair in incident
                    ]
                )

    stats = {
        "primary_variables": primary_count,
        "total_variables": pool.top,
        "clauses": len(clauses),
    }
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        if not solver.solve():
            return "INFEASIBLE", None, stats
        positive = {literal for literal in solver.get_model() if literal > 0}

    certificate: dict[str, list[int]] = {}
    for fixed_pair in FIXED_PAIRS:
        phases: list[int] = []
        for orbit_index in range(orbit_count):
            selected = [
                shift
                for shift in POINTS
                if variable(fixed_pair, orbit_index, shift) in positive
            ]
            assert len(selected) == 1
            phases.append((-selected[0]) % P)
        certificate[f"{fixed_pair[0]},{fixed_pair[1]}"] = phases
    return "FEASIBLE", certificate, stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds-per-pair", type=float, default=30.0)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--backend", choices=("sat", "cp-sat"), default="sat")
    parser.add_argument("--sat-solver", default="cadical195")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="reuse and extend an existing --output JSON checkpoint",
    )
    parser.add_argument(
        "--only-fixed-pair",
        help="solve one pair i,j instead of all 105 (diagnostic/checkpoint mode)",
    )
    parser.add_argument(
        "--joint",
        action="store_true",
        help="solve all slices together with the required cross-slice constraints",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()

    if args.verify is not None:
        certificate = json.loads(args.verify.read_text())
        if args.only_fixed_pair is not None:
            fixed_pair = tuple(sorted(map(int, args.only_fixed_pair.split(","))))
            assert len(fixed_pair) == 2 and fixed_pair in FIXED_PAIRS
            verify_single_fixed_pair(certificate, fixed_pair)
            print(f"single fixed-pair {fixed_pair} certificate: PASS")
        elif args.joint:
            verify_joint_compatibility(certificate)
            print("joint cyclic-17 moving-triple certificate: PASS")
        else:
            verify_certificate(certificate)
            print("slice-wise cyclic-17 moving-triple certificate: PASS")
        return

    golf = construct_golf17()
    if args.joint:
        assert args.only_fixed_pair is None
        status, certificate, stats = solve_joint_sat(golf, args.sat_solver)
        print(f"joint model: {stats}")
        print(f"joint status: {status}", flush=True)
        if certificate is None:
            return
        verify_joint_compatibility(certificate)
        print("joint cyclic-17 moving-triple certificate: PASS")
        if args.output is not None:
            args.output.write_text(
                json.dumps(certificate, indent=2, sort_keys=True) + "\n"
            )
            print(f"wrote {args.output}")
        return

    certificate: dict[str, list[int]] = {}
    if args.resume and args.output is not None and args.output.exists():
        certificate = json.loads(args.output.read_text())
    requested_pairs = FIXED_PAIRS
    if args.only_fixed_pair is not None:
        fixed_pair = tuple(map(int, args.only_fixed_pair.split(",")))
        assert len(fixed_pair) == 2 and tuple(sorted(fixed_pair)) in FIXED_PAIRS
        requested_pairs = (tuple(sorted(fixed_pair)),)

    unsolved_pairs = tuple(
        fixed_pair
        for fixed_pair in requested_pairs
        if f"{fixed_pair[0]},{fixed_pair[1]}" not in certificate
    )

    def record(
        index: int,
        fixed_pair: tuple[int, int],
        status: str,
        phases: list[int] | None,
    ) -> bool:
        print(
            f"{index:3d}/{len(requested_pairs)} fixed pair {fixed_pair}: {status}",
            flush=True,
        )
        if phases is None:
            print("No complete certificate was found.")
            return False
        certificate[f"{fixed_pair[0]},{fixed_pair[1]}"] = phases
        if args.output is not None:
            args.output.write_text(
                json.dumps(certificate, indent=2, sort_keys=True) + "\n"
            )
        return True

    if args.backend == "sat" and args.jobs > 1 and len(unsolved_pairs) > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as executor:
            futures = {
                executor.submit(
                    solve_fixed_pair_sat_worker,
                    (fixed_pair, args.sat_solver),
                ): fixed_pair
                for fixed_pair in unsolved_pairs
            }
            completed = len(requested_pairs) - len(unsolved_pairs)
            for future in as_completed(futures):
                completed += 1
                fixed_pair, status, phases = future.result()
                if not record(completed, fixed_pair, status, phases):
                    return
    else:
        for offset, fixed_pair in enumerate(unsolved_pairs, start=1):
            index = len(requested_pairs) - len(unsolved_pairs) + offset
            if args.backend == "sat":
                status, phases = solve_fixed_pair_sat(
                    golf, fixed_pair, args.sat_solver
                )
            else:
                status, phases = solve_fixed_pair(
                    golf, fixed_pair, args.seconds_per_pair, args.seed + index
                )
            if not record(index, fixed_pair, status, phases):
                return

    if requested_pairs == FIXED_PAIRS:
        verify_certificate(certificate)
        print("cyclic-17 moving-triple certificate: PASS")
    else:
        i, j = requested_pairs[0]
        verify_single_fixed_pair(certificate, (i, j))
        print("single fixed-pair cyclic-17 certificate: PASS")
    if args.output is not None:
        print(f"wrote {args.output}")


if __name__ == "__main__":
    main()

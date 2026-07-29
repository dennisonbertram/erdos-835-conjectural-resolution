#!/usr/bin/env python3
"""Explore two-fixed-block intersection profiles in a hypothetical S(14,15,31).

Fix two blocks B1 and B2 with intersection size ``s`` and partition the
31-point set into

    I = B1 cap B2,
    U = B1 \ B2,
    V = B2 \ B1,
    W = X \ (B1 union B2).

For every possible block-profile (a,b,c,d) against (I,U,V,W), introduce
the aggregate count N[a,b,c,d].  All factorial moments of total degree at
most 14 are forced by the design parameters.  This script puts those
equations, nonnegativity, and the elementary Steiner intersection zeros
into a linear program.

The LP is an exploratory discriminator.  A floating-point optimum is not
itself a proof; any decisive bound must subsequently be converted to an
exact rational certificate or an integer enumeration.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
from math import comb

from ortools.linear_solver import pywraplp


POINTS = 31
DESIGN_T = 14
BLOCK_SIZE = 15
BLOCKS = comb(POINTS, DESIGN_T) // BLOCK_SIZE
LAMBDA = tuple(
    comb(POINTS - level, DESIGN_T - level) // (BLOCK_SIZE - level)
    for level in range(DESIGN_T + 1)
)


def bounded_compositions(total: int, capacities: tuple[int, ...]):
    """Yield all vectors bounded by ``capacities`` with the requested sum."""
    for values in product(*(range(capacity + 1) for capacity in capacities)):
        if sum(values) == total:
            yield values


def facet_types(capacities: tuple[int, ...]):
    """Yield all 14-subset profiles.

    The degree-14 equations imply every lower factorial moment: sum the
    relevant facet equations over the 14-subsets containing a fixed
    smaller subset.  Keeping only this top layer is therefore lossless and
    much better conditioned numerically.
    """
    yield from bounded_compositions(DESIGN_T, capacities)


def coefficient(profile: tuple[int, ...], moment: tuple[int, ...]) -> int:
    answer = 1
    for present, selected in zip(profile, moment):
        if selected > present:
            return 0
        answer *= comb(present, selected)
    return answer


def build_solver(
    intersection: int,
    objective_profile: tuple[int, int, int, int],
    maximize: bool,
) -> tuple[
    pywraplp.Solver,
    dict[tuple[int, int, int, int], pywraplp.Variable],
    tuple[
        tuple[
            tuple[int, int, int, int],
            int,
            pywraplp.Constraint,
        ],
        ...,
    ],
]:
    capacities = (
        intersection,
        BLOCK_SIZE - intersection,
        BLOCK_SIZE - intersection,
        intersection + 1,
    )
    if any(
        value < 0 or value > capacity
        for value, capacity in zip(objective_profile, capacities)
    ) or sum(objective_profile) != BLOCK_SIZE:
        raise ValueError(
            f"invalid objective profile {objective_profile} "
            f"for capacities {capacities}"
        )

    profiles = tuple(bounded_compositions(BLOCK_SIZE, capacities))
    first = (intersection, BLOCK_SIZE - intersection, 0, 0)
    second = (intersection, 0, BLOCK_SIZE - intersection, 0)

    def forced_zero(profile: tuple[int, int, int, int]) -> bool:
        meet_first = profile[0] + profile[1]
        meet_second = profile[0] + profile[2]
        return (meet_first >= DESIGN_T and profile != first) or (
            meet_second >= DESIGN_T and profile != second
        )

    live_profiles = tuple(
        profile
        for profile in profiles
        if profile not in (first, second) and not forced_zero(profile)
    )
    if objective_profile not in live_profiles:
        raise ValueError("objective profile is fixed or forced to zero")

    solver = pywraplp.Solver.CreateSolver("GLOP")
    if solver is None:
        raise RuntimeError("OR-Tools GLOP is unavailable")
    variables = {
        profile: solver.NumVar(0.0, solver.infinity(), f"N_{'_'.join(map(str, profile))}")
        for profile in live_profiles
    }

    # The complete strength-14 factorial-moment system.
    constraints = []
    for moment in facet_types(capacities):
        total = sum(moment)
        rhs = LAMBDA[total]
        for capacity, selected in zip(capacities, moment):
            rhs *= comb(capacity, selected)
        # Remove the two fixed blocks, whose aggregate counts are exactly one.
        rhs -= coefficient(first, moment)
        rhs -= coefficient(second, moment)
        constraint = solver.Constraint(float(rhs), float(rhs))
        for profile, variable in variables.items():
            value = coefficient(profile, moment)
            if value:
                constraint.SetCoefficient(variable, float(value))
        constraints.append((moment, rhs, constraint))

    objective = solver.Objective()
    objective.SetCoefficient(variables[objective_profile], 1.0)
    if maximize:
        objective.SetMaximization()
    else:
        objective.SetMinimization()
    return solver, variables, tuple(constraints)


def exact_dual_audit(
    variables: dict[tuple[int, int, int, int], pywraplp.Variable],
    constraints: tuple[
        tuple[
            tuple[int, int, int, int],
            int,
            pywraplp.Constraint,
        ],
        ...,
    ],
    objective_profile: tuple[int, int, int, int],
    maximize: bool,
) -> dict[str, object]:
    """Rationally reconstruct and check the floating-point LP dual."""
    dual = []
    for moment, rhs, constraint in constraints:
        value = constraint.dual_value()
        if abs(value) > 1e-8:
            dual.append(
                (
                    moment,
                    rhs,
                    Fraction(value).limit_denominator(1_000_000_000),
                )
            )

    exact_objective = sum(
        Fraction(rhs) * multiplier for _, rhs, multiplier in dual
    )
    minimum_slack: Fraction | None = None
    violated = []
    for profile in variables:
        dual_coefficient = sum(
            multiplier * coefficient(profile, moment)
            for moment, _, multiplier in dual
        )
        objective_coefficient = Fraction(profile == objective_profile)
        slack = (
            dual_coefficient - objective_coefficient
            if maximize
            else objective_coefficient - dual_coefficient
        )
        if minimum_slack is None or slack < minimum_slack:
            minimum_slack = slack
        if slack < 0:
            violated.append((profile, slack))
    return {
        "nonzero_dual_entries": len(dual),
        "exact_dual_objective": str(exact_objective),
        "minimum_exact_slack": str(minimum_slack),
        "violations": len(violated),
        "largest_denominator": max(
            (entry[2].denominator for entry in dual), default=1
        ),
    }


def solve(
    intersection: int,
    objective_profile: tuple[int, int, int, int],
    maximize: bool,
) -> dict[str, object]:
    solver, variables, constraints = build_solver(
        intersection, objective_profile, maximize
    )
    status = solver.Solve()
    label = {
        pywraplp.Solver.OPTIMAL: "OPTIMAL",
        pywraplp.Solver.FEASIBLE: "FEASIBLE",
        pywraplp.Solver.INFEASIBLE: "INFEASIBLE",
        pywraplp.Solver.UNBOUNDED: "UNBOUNDED",
        pywraplp.Solver.ABNORMAL: "ABNORMAL",
        pywraplp.Solver.NOT_SOLVED: "NOT_SOLVED",
    }.get(status, f"STATUS_{status}")
    answer = {
        "status": label,
        "maximize": maximize,
        "objective": (
            variables[objective_profile].solution_value()
            if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE)
            else None
        ),
        "profiles": len(variables),
        "moments": len(constraints),
        "iterations": solver.iterations(),
        "wall_ms": solver.wall_time(),
    }
    if status == pywraplp.Solver.OPTIMAL:
        answer["exact_dual_audit"] = exact_dual_audit(
            variables,
            constraints,
            objective_profile,
            maximize,
        )
    return answer


def parse_profile(raw: str) -> tuple[int, int, int, int]:
    values = tuple(int(value) for value in raw.split(","))
    if len(values) != 4:
        raise argparse.ArgumentTypeError("profile must have four comma-separated integers")
    return values  # type: ignore[return-value]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intersection", type=int, default=6)
    parser.add_argument("--profile", type=parse_profile, default=(0, 4, 4, 7))
    args = parser.parse_args()

    assert BLOCKS == 17_678_835
    assert LAMBDA == (
        17_678_835,
        8_554_275,
        3_991_995,
        1_789_515,
        766_935,
        312_455,
        120_175,
        43_263,
        14_421,
        4_389,
        1_197,
        285,
        57,
        9,
        1,
    )

    print(
        {
            "intersection": args.intersection,
            "capacities": (
                args.intersection,
                BLOCK_SIZE - args.intersection,
                BLOCK_SIZE - args.intersection,
                args.intersection + 1,
            ),
            "objective_profile": args.profile,
            "minimum": solve(args.intersection, args.profile, False),
            "maximum": solve(args.intersection, args.profile, True),
            "scope": "floating-point LP exploration; not a certificate",
        }
    )


if __name__ == "__main__":
    main()

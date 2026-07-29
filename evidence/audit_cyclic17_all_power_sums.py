#!/usr/bin/env python3
"""Audit every linearized power-sum consequence of the compact cyclic layer.

Each slice AllDifferent constraint is a prescribed 15-subset of F_17 and
each cross constraint is a prescribed 14-subset.  Their power sums for
degrees 1,...,16 are therefore fixed.  At degree m, the coefficient of the
new lifted monomials x_v^m is the same 1,440 by 4,200 first-moment matrix.
Every left-kernel vector of that matrix cancels the new monomials and gives
an exact linear constraint on lower lifted powers.

The script constructs all 120 such cancellations at every degree through
16 and checks their joint consistency over F_17.  Consistency is only a
relaxation result; inconsistency would be a rigorous obstruction to the
fixed-Wallis, C17-equivariant radius-five ansatz.
"""

from __future__ import annotations

import math
from collections import defaultdict

from audit_cyclic17_phase_sums_mod17 import (
    DIFFERENCES,
    EDGE_COORDINATES,
    FIXED_PAIRS,
    P,
    POINTS,
    SQUARES,
    construct_golf17,
    left_dependencies,
    make_rows,
    zero_positions,
)


def field_power_sum(degree: int) -> int:
    return sum(pow(value, degree, P) for value in POINTS) % P


def power_rows(
    degree: int,
) -> list[tuple[dict[tuple[int, int], int], int]]:
    """Return the 1,440 degree-m equations keyed by (power, phase variable)."""
    zeros = zero_positions(construct_golf17())
    pair_index = {
        fixed_pair: index
        for index, fixed_pair in enumerate(FIXED_PAIRS)
    }
    orbit_count = len(EDGE_COORDINATES)

    def variable(
        fixed_pair: tuple[int, int],
        orbit_index: int,
    ) -> int:
        return pair_index[fixed_pair] * orbit_count + orbit_index

    full_sum = field_power_sum(degree)
    rows: list[tuple[dict[tuple[int, int], int], int]] = []

    for fixed_pair in FIXED_PAIRS:
        i, j = fixed_pair
        for difference in DIFFERENCES:
            coefficients: dict[tuple[int, int], int] = defaultdict(int)
            constant = 0
            for orbit_index, coordinates in enumerate(EDGE_COORDINATES):
                for current_difference, offset in coordinates:
                    if current_difference != difference:
                        continue
                    constant += pow(offset, degree, P)
                    phase = variable(fixed_pair, orbit_index)
                    for power in range(1, degree + 1):
                        coefficients[power, phase] += (
                            math.comb(degree, power)
                            * pow(offset, degree - power, P)
                        )
            rhs = (
                full_sum
                - pow(zeros[i, difference], degree, P)
                - pow(zeros[j, difference], degree, P)
                - constant
            ) % P
            rows.append(
                (
                    {
                        key: value % P
                        for key, value in coefficients.items()
                        if value % P
                    },
                    rhs,
                )
            )

    for fixed_point in SQUARES:
        for orbit_index, coordinates in enumerate(EDGE_COORDINATES):
            coefficients = {
                (
                    degree,
                    variable(
                        (
                            min(fixed_point, other),
                            max(fixed_point, other),
                        ),
                        orbit_index,
                    ),
                ): 1
                for other in SQUARES
                if other != fixed_point
            }
            forbidden = {
                (zeros[fixed_point, difference] - offset) % P
                for difference, offset in coordinates
            }
            assert len(forbidden) == 3
            rhs = (
                full_sum
                - sum(pow(value, degree, P) for value in forbidden)
            ) % P
            rows.append((coefficients, rhs))

    assert len(rows) == 1440
    return rows


def cancelled_rows(
    degree: int,
    dependencies: list[dict[int, int]],
) -> list[tuple[dict[int, int], int]]:
    """Cancel degree-m monomials and flatten all lower powers into columns."""
    expanded = power_rows(degree)
    variable_count = len(FIXED_PAIRS) * len(EDGE_COORDINATES)
    answer = []
    for dependency in dependencies:
        coefficients: dict[int, int] = defaultdict(int)
        rhs = 0
        for row_index, weight in dependency.items():
            row, row_rhs = expanded[row_index]
            rhs += weight * row_rhs
            for (power, variable), value in row.items():
                if power == degree:
                    continue
                column = (power - 1) * variable_count + variable
                coefficients[column] += weight * value
        leading = defaultdict(int)
        for row_index, weight in dependency.items():
            for (power, variable), value in expanded[row_index][0].items():
                if power == degree:
                    leading[variable] += weight * value
        assert all(value % P == 0 for value in leading.values())
        answer.append(
            (
                {
                    column: value % P
                    for column, value in coefficients.items()
                    if value % P
                },
                rhs % P,
            )
        )
    assert len(answer) == 120
    return answer


class SparseEliminator:
    """Incremental row-echelon form over F_17."""

    def __init__(self) -> None:
        self.basis: dict[int, tuple[dict[int, int], int]] = {}
        self.consistent = True

    def add(self, coefficients: dict[int, int], right_hand_side: int) -> None:
        if not self.consistent:
            return
        row = {
            variable: coefficient % P
            for variable, coefficient in coefficients.items()
            if coefficient % P
        }
        rhs = right_hand_side % P
        while row:
            pivot = min(row)
            coefficient = row[pivot]
            if pivot not in self.basis:
                inverse = pow(coefficient, -1, P)
                row = {
                    variable: (value * inverse) % P
                    for variable, value in row.items()
                    if (value * inverse) % P
                }
                self.basis[pivot] = row, rhs * inverse % P
                return
            old_row, old_rhs = self.basis[pivot]
            factor = coefficient
            for variable, value in old_row.items():
                new_value = (row.get(variable, 0) - factor * value) % P
                if new_value:
                    row[variable] = new_value
                else:
                    row.pop(variable, None)
            rhs = (rhs - factor * old_rhs) % P
        self.consistent = rhs == 0


def main() -> None:
    first_rows, variable_count = make_rows()
    dependencies = left_dependencies(first_rows)
    eliminator = SparseEliminator()
    for coefficients, rhs in first_rows:
        eliminator.add(coefficients, rhs)
    assert eliminator.consistent
    row_count = len(first_rows)
    report = []
    for degree in range(2, P):
        additions = cancelled_rows(degree, dependencies)
        for coefficients, rhs in additions:
            eliminator.add(coefficients, rhs)
        row_count += len(additions)
        rank = len(eliminator.basis)
        consistent = eliminator.consistent
        report.append((degree, rank, consistent))
        print(
            f"degree<={degree}: rows={row_count} "
            f"rank={rank} status={'CONSISTENT' if consistent else 'INCONSISTENT'}",
            flush=True,
        )
        if not consistent:
            break

    assert variable_count == 4200
    assert len(dependencies) == 120
    print(
        {
            "status": (
                "CONSISTENT"
                if report and report[-1][2] and report[-1][0] == 16
                else "INCONSISTENT"
            ),
            "scope": (
                "all dependency-cancelled power sums through degree 16; "
                "not a radius-five witness"
            ),
            "first_moment_rank": 1320,
            "left_dependencies_per_degree": len(dependencies),
            "final_rank": report[-1][1],
        }
    )


if __name__ == "__main__":
    main()

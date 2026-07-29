#!/usr/bin/env python3
"""Exact F_17 audit of low-moment cyclic radius-five equations.

Every compact slice AllDifferent(15) constraint is a permutation of the
fifteen residual cyclic edge positions.  Every cross AllDifferent(14)
constraint is a permutation of the fourteen shifts not forbidden by one golf
square.  Taking sums produces 1,440 linear equations in the 4,200 selected
triple-orbit phases.

This stdlib-only script constructs those equations directly from the Wallis
golf array and computes their rank by sparse Gaussian elimination over F_17.
It also computes all 120 dependencies among the first-moment rows and uses
them to cancel the quadratic terms in the corresponding second-moment
identities.  Those 120 derived linear equations add no rank.  Consistency is
only a relaxation result; it is not a radius-five witness.
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parent
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))

from global_latin_audit import construct_golf17


P = 17
POINTS = tuple(range(P))
SQUARES = tuple(range(15))
FIXED_PAIRS = tuple(combinations(SQUARES, 2))
MOVING_EDGES = tuple(combinations(POINTS, 2))
MOVING_TRIPLES = tuple(combinations(POINTS, 3))
DIFFERENCES = tuple(range(1, 9))


def translate(
    subset: tuple[int, ...], amount: int
) -> tuple[int, ...]:
    return tuple(sorted((value + amount) % P for value in subset))


def triple_representatives() -> list[tuple[int, int, int]]:
    representatives: list[tuple[int, int, int]] = []
    unseen = set(MOVING_TRIPLES)
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, shift) for shift in POINTS)
        representatives.append(representative)
        for shift in POINTS:
            unseen.discard(translate(representative, shift))
    assert len(representatives) == 40
    return representatives


def edge_coordinate(edge: tuple[int, int]) -> tuple[int, int]:
    x, y = edge
    forward = (y - x) % P
    if forward <= 8:
        return forward, x
    return P - forward, y


def representative_edge_coordinates():
    answer = []
    multiplicities = {difference: 0 for difference in DIFFERENCES}
    for representative in triple_representatives():
        coordinates = tuple(
            edge_coordinate(edge)
            for edge in combinations(representative, 2)
        )
        answer.append(coordinates)
        for difference, _ in coordinates:
            multiplicities[difference] += 1
    assert multiplicities == {difference: 15 for difference in DIFFERENCES}
    return answer


EDGE_COORDINATES = representative_edge_coordinates()


def zero_positions(golf) -> dict[tuple[int, int], int]:
    answer = {}
    for square in SQUARES:
        for edge in MOVING_EDGES:
            if golf[square][edge[0]][edge[1]] != 0:
                continue
            difference, position = edge_coordinate(edge)
            key = square, difference
            assert key not in answer
            answer[key] = position
    assert len(answer) == len(SQUARES) * len(DIFFERENCES)
    return answer


def make_rows():
    zeros = zero_positions(construct_golf17())
    pair_index = {
        fixed_pair: index
        for index, fixed_pair in enumerate(FIXED_PAIRS)
    }
    orbit_count = len(EDGE_COORDINATES)

    def variable(fixed_pair: tuple[int, int], orbit_index: int) -> int:
        return pair_index[fixed_pair] * orbit_count + orbit_index

    rows: list[tuple[dict[int, int], int]] = []

    # For a fixed pair and difference, the fifteen modular edge positions
    # sum to all seventeen positions minus the two zero-factor positions.
    for fixed_pair in FIXED_PAIRS:
        i, j = fixed_pair
        for difference in DIFFERENCES:
            coefficients = {}
            offset_sum = 0
            for orbit_index, coordinates in enumerate(EDGE_COORDINATES):
                offsets = [
                    position for current_difference, position in coordinates
                    if current_difference == difference
                ]
                if offsets:
                    coefficients[variable(fixed_pair, orbit_index)] = (
                        len(offsets) % P
                    )
                    offset_sum = (offset_sum + sum(offsets)) % P
            assert sum(coefficients.values()) == 15
            right_hand_side = (
                -zeros[i, difference]
                - zeros[j, difference]
                - offset_sum
            ) % P
            rows.append((coefficients, right_hand_side))

    # At one fixed point and triple orbit, the fourteen incident phases are
    # exactly all shifts outside the three shifts at which one triangle edge
    # belongs to that golf square's zero matching.
    for fixed_point in SQUARES:
        for orbit_index, coordinates in enumerate(EDGE_COORDINATES):
            coefficients = {
                variable(
                    (min(fixed_point, other), max(fixed_point, other)),
                    orbit_index,
                ): 1
                for other in SQUARES
                if other != fixed_point
            }
            forbidden = {
                (zeros[fixed_point, difference] - position) % P
                for difference, position in coordinates
            }
            assert len(coefficients) == 14
            assert len(forbidden) == 3
            rows.append((coefficients, (-sum(forbidden)) % P))

    assert len(rows) == 105 * 8 + 15 * 40 == 1440
    return rows, len(FIXED_PAIRS) * orbit_count


def global_second_moment_linear_row():
    """Cancel quadratic terms between all slice and all cross identities.

    Squaring every forced permutation identity gives quadratic equations.
    Across all slice equations each phase square occurs three times, while
    across all cross equations it occurs twice.  Twice the global slice sum
    minus three times the global cross sum therefore cancels every square and
    leaves one additional exact linear equation over F_17.
    """
    zeros = zero_positions(construct_golf17())
    pair_index = {
        fixed_pair: index
        for index, fixed_pair in enumerate(FIXED_PAIRS)
    }
    orbit_count = len(EDGE_COORDINATES)

    def variable(fixed_pair, orbit_index):
        return pair_index[fixed_pair] * orbit_count + orbit_index

    coefficients = {}
    slice_rhs_after_constants = 0
    for fixed_pair in FIXED_PAIRS:
        i, j = fixed_pair
        for difference in DIFFERENCES:
            offsets = []
            for orbit_index, coordinates in enumerate(EDGE_COORDINATES):
                for current_difference, position in coordinates:
                    if current_difference != difference:
                        continue
                    offsets.append(position)
                    key = variable(fixed_pair, orbit_index)
                    coefficients[key] = (
                        coefficients.get(key, 0) + 4 * position
                    ) % P
            slice_rhs_after_constants = (
                slice_rhs_after_constants
                - zeros[i, difference] ** 2
                - zeros[j, difference] ** 2
                - sum(position ** 2 for position in offsets)
            ) % P

    cross_rhs = 0
    for fixed_point in SQUARES:
        for coordinates in EDGE_COORDINATES:
            forbidden = {
                (zeros[fixed_point, difference] - position) % P
                for difference, position in coordinates
            }
            assert len(forbidden) == 3
            cross_rhs = (
                cross_rhs - sum(value ** 2 for value in forbidden)
            ) % P

    coefficients = {
        variable: value
        for variable, value in coefficients.items()
        if value
    }
    right_hand_side = (
        2 * slice_rhs_after_constants - 3 * cross_rhs
    ) % P
    return coefficients, right_hand_side


def second_moment_expansions():
    """Return quadratic coefficients, linear terms, and constants per row."""
    zeros = zero_positions(construct_golf17())
    pair_index = {
        fixed_pair: index
        for index, fixed_pair in enumerate(FIXED_PAIRS)
    }
    orbit_count = len(EDGE_COORDINATES)

    def variable(fixed_pair, orbit_index):
        return pair_index[fixed_pair] * orbit_count + orbit_index

    answer = []
    for fixed_pair in FIXED_PAIRS:
        i, j = fixed_pair
        for difference in DIFFERENCES:
            quadratic = {}
            linear = {}
            offset_squares = 0
            for orbit_index, coordinates in enumerate(EDGE_COORDINATES):
                offsets = [
                    position
                    for current_difference, position in coordinates
                    if current_difference == difference
                ]
                if not offsets:
                    continue
                key = variable(fixed_pair, orbit_index)
                quadratic[key] = len(offsets) % P
                linear[key] = (2 * sum(offsets)) % P
                offset_squares += sum(position ** 2 for position in offsets)
            rhs = (
                -zeros[i, difference] ** 2
                - zeros[j, difference] ** 2
                - offset_squares
            ) % P
            answer.append((quadratic, linear, rhs))

    for fixed_point in SQUARES:
        for orbit_index, coordinates in enumerate(EDGE_COORDINATES):
            quadratic = {
                variable(
                    (min(fixed_point, other), max(fixed_point, other)),
                    orbit_index,
                ): 1
                for other in SQUARES
                if other != fixed_point
            }
            forbidden = {
                (zeros[fixed_point, difference] - position) % P
                for difference, position in coordinates
            }
            assert len(forbidden) == 3
            answer.append(
                (
                    quadratic,
                    {},
                    (-sum(value ** 2 for value in forbidden)) % P,
                )
            )
    assert len(answer) == 1440
    return answer


def left_dependencies(
    rows: list[tuple[dict[int, int], int]]
) -> list[dict[int, int]]:
    """Return a sparse basis of dependencies among row coefficient vectors."""
    basis = {}
    dependencies = []
    for row_index, (coefficients, _) in enumerate(rows):
        row = {
            variable: coefficient % P
            for variable, coefficient in coefficients.items()
            if coefficient % P
        }
        combination = {row_index: 1}
        while row:
            pivot = min(row)
            coefficient = row[pivot]
            if pivot not in basis:
                inverse = pow(coefficient, -1, P)
                row = {
                    variable: (value * inverse) % P
                    for variable, value in row.items()
                    if (value * inverse) % P
                }
                combination = {
                    index: (value * inverse) % P
                    for index, value in combination.items()
                    if (value * inverse) % P
                }
                basis[pivot] = row, combination
                break
            old_row, old_combination = basis[pivot]
            factor = coefficient
            for variable, value in old_row.items():
                new_value = (row.get(variable, 0) - factor * value) % P
                if new_value:
                    row[variable] = new_value
                else:
                    row.pop(variable, None)
            for index, value in old_combination.items():
                new_value = (
                    combination.get(index, 0) - factor * value
                ) % P
                if new_value:
                    combination[index] = new_value
                else:
                    combination.pop(index, None)
        else:
            assert combination
            dependencies.append(combination)
    assert len(basis) == 1320
    assert len(dependencies) == 120
    return dependencies


def cancelled_second_moment_rows(rows):
    """Use every row dependency to cancel phase squares exactly."""
    expansions = second_moment_expansions()
    assert all(
        {
            variable: value % P
            for variable, value in quadratic.items()
            if value % P
        }
        == rows[index][0]
        for index, (quadratic, _, _) in enumerate(expansions)
    )
    answer = []
    for dependency in left_dependencies(rows):
        coefficients = {}
        rhs = 0
        first_rhs = 0
        for row_index, weight in dependency.items():
            _, linear, second_rhs = expansions[row_index]
            for variable, value in linear.items():
                coefficients[variable] = (
                    coefficients.get(variable, 0) + weight * value
                ) % P
            rhs = (rhs + weight * second_rhs) % P
            first_rhs = (
                first_rhs + weight * rows[row_index][1]
            ) % P
        # The already-audited first-moment system must respect every row
        # dependency; this also checks the dependency bookkeeping.
        assert first_rhs == 0
        coefficients = {
            variable: value
            for variable, value in coefficients.items()
            if value
        }
        answer.append((coefficients, rhs))
    assert len(answer) == 120
    return answer


def rank_and_consistency(
    rows: list[tuple[dict[int, int], int]]
) -> tuple[int, bool]:
    basis: dict[int, tuple[dict[int, int], int]] = {}
    for coefficients, right_hand_side in rows:
        row = {
            variable: coefficient % P
            for variable, coefficient in coefficients.items()
            if coefficient % P
        }
        rhs = right_hand_side % P
        while row:
            pivot = min(row)
            coefficient = row[pivot]
            if pivot not in basis:
                inverse = pow(coefficient, -1, P)
                row = {
                    variable: (value * inverse) % P
                    for variable, value in row.items()
                    if (value * inverse) % P
                }
                rhs = (rhs * inverse) % P
                basis[pivot] = row, rhs
                break
            old_row, old_rhs = basis[pivot]
            factor = coefficient
            for variable, value in old_row.items():
                new_value = (row.get(variable, 0) - factor * value) % P
                if new_value:
                    row[variable] = new_value
                else:
                    row.pop(variable, None)
            rhs = (rhs - factor * old_rhs) % P
        else:
            if rhs:
                return len(basis), False
    return len(basis), True


def main() -> None:
    rows, variables = make_rows()
    rank, consistent = rank_and_consistency(rows)
    second_moment_row = global_second_moment_linear_row()
    strengthened_rank, strengthened_consistent = rank_and_consistency(
        rows + [second_moment_row]
    )
    cancelled_rows = cancelled_second_moment_rows(rows)
    all_second_rank, all_second_consistent = rank_and_consistency(
        rows + cancelled_rows
    )
    assert variables == 4200
    assert len(rows) == 1440
    assert rank == 1320
    assert consistent
    assert strengthened_consistent
    print("cyclic phase-sum audit over F_17: PASS")
    print(f"variables: {variables}")
    print(f"equations: {len(rows)}")
    print(f"rank: {rank}")
    print(f"nullity: {variables - rank}")
    print(
        "global second-moment cancellation: "
        f"CONSISTENT, rank {strengthened_rank}"
    )
    print(
        "all 120 second-moment cancellations: "
        f"{'CONSISTENT' if all_second_consistent else 'INCONSISTENT'}, "
        f"rank {all_second_rank}"
    )
    print("status: CONSISTENT")
    print(
        "scope: first moments plus every linear second-moment "
        "cancellation; not a radius-five witness"
    )


if __name__ == "__main__":
    main()

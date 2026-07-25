#!/usr/bin/env python3
"""Exact CP-SAT layer for the normalized rank-four Pfaffian descendant.

The rank-four normalization in pfaffian_full_rank4.md leaves 16 points
v_r in F_17^4, r=0,...,15, with coordinate 0 fixed to
(0,2,3,...,16) and coordinates 1,2,3 each a permutation of that same set.

This model adds every 3-star containing exactly two of the four basis
points. There are 6*16=96 such stars. Each of its 17 determinants is
encoded modulo 17 and constrained AllDifferent. This is a necessary
layer of the full 1,140-star predicate, not the full rank-four problem.

The model contains only exact integer constraints. OR-Tools status
INFEASIBLE means it has completed its search for this displayed layer.
CP-SAT does not emit a solver-independent proof trace, so an infeasible
status is reproducible computational evidence, not yet a portable
certificate of rank-four impossibility.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import platform
import random
from dataclasses import dataclass

from ortools import __version__ as ORTOOLS_VERSION
from ortools.sat.python import cp_model


P = 17
VALUES = tuple(range(P))
# For a tail row after e_0,...,e_3, the basis star missing e_c gives
# (-1)^(3-c) x_c.  Its 16 tail coordinates therefore omit that signed unit.
TAIL_BY_AXIS = tuple(
    tuple(value for value in VALUES if value != (-1 if (3 - axis) % 2 else 1) % P)
    for axis in range(4)
)
AXES = range(4)


def permutation_sign(permutation: list[int]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inversions % 2 else 1


@dataclass(frozen=True)
class TailPoint:
    row: int


class RankFourTwoBasisModel:
    def __init__(self, symmetry_break: bool = True, explain_core: bool = False) -> None:
        self.model = cp_model.CpModel()
        self.x: list[list[cp_model.IntVar | int]] = [
            [TAIL_BY_AXIS[0][row]]
            + [
                self.model.new_int_var_from_domain(
                    cp_model.Domain.FromValues(TAIL_BY_AXIS[col]), f"x_{row}_{col}"
                )
                for col in range(1, 4)
            ]
            for row in range(16)
        ]
        for col in range(1, 4):
            self.model.add_all_different([self.x[row][col] for row in range(16)])
        # No coordinate-order breaker is used: the signed omitted values
        # depend on the displayed basis order.  The parameter remains for
        # reproducibility of earlier command lines, but is intentionally inert.
        self.mod_count = 0
        self.product_count = 0
        self.star_count = 0
        self.explain_core = explain_core
        self.assumption_stars: dict[int, tuple[int, int, int]] = {}
        self._add_two_basis_stars()

    def _new_mod_linear(self, terms, name: str) -> cp_model.IntVar:
        result = self.model.new_int_var(0, P - 1, f"{name}_mod")
        quotient = self.model.new_int_var(-32, 32, f"{name}_quot")
        self.model.add(sum(coefficient * term for coefficient, term in terms) == result + P * quotient)
        self.mod_count += 1
        return result

    def _product(self, left, right, name: str) -> cp_model.IntVar:
        product = self.model.new_int_var(0, (P - 1) ** 2, name)
        self.model.add_multiplication_equality(product, left, right)
        self.product_count += 1
        return product

    @staticmethod
    def _ordered_indices(basis: tuple[int, ...], tail_rows: tuple[int, ...]) -> list[int]:
        return sorted((*basis, *(4 + row for row in tail_rows)))

    def _determinant_with_at_least_two_basis(
        self, basis: tuple[int, ...], tails: tuple[int, ...], name: str
    ) -> cp_model.IntVar:
        ordered = self._ordered_indices(basis, tails)
        row_at_position: list[int | TailPoint] = [
            index if index < 4 else TailPoint(index - 4) for index in ordered
        ]
        missing = [axis for axis in AXES if axis not in basis]
        if len(tails) == 1:
            tail = tails[0]
            mapping = [
                row if isinstance(row, int) else missing[0] for row in row_at_position
            ]
            sign = permutation_sign(mapping)
            return self._new_mod_linear([(sign, self.x[tail][missing[0]])], name)
        if len(tails) != 2:
            raise ValueError("this layer has exactly one or two tail rows")
        first, second = tails
        c, d = missing
        term_specs = []
        for first_axis, second_axis in ((c, d), (d, c)):
            assignment = []
            for row in row_at_position:
                if isinstance(row, int):
                    assignment.append(row)
                elif row.row == first:
                    assignment.append(first_axis)
                else:
                    assignment.append(second_axis)
            sign = permutation_sign(assignment)
            product = self._product(
                self.x[first][first_axis],
                self.x[second][second_axis],
                f"{name}_p_{first_axis}{second_axis}",
            )
            term_specs.append((sign, product))
        return self._new_mod_linear(term_specs, name)

    def _add_two_basis_stars(self) -> None:
        for basis in itertools.combinations(AXES, 2):
            for row in range(16):
                triple = tuple(sorted((*basis, 4 + row)))
                values = []
                for outside in range(20):
                    if outside in triple:
                        continue
                    outside_basis = tuple(sorted((*basis, outside))) if outside < 4 else basis
                    tails = (row,) if outside < 4 else tuple(sorted((row, outside - 4)))
                    values.append(
                        self._determinant_with_at_least_two_basis(
                            outside_basis,
                            tails,
                            f"d_{basis[0]}_{basis[1]}_{row}_{outside}",
                        )
                    )
                assert len(values) == P
                if self.explain_core:
                    enabled = self.model.new_bool_var(
                        f"enable_{basis[0]}_{basis[1]}_{row}"
                    )
                    self.assumption_stars[enabled.Index()] = triple
                    self.model.add_assumption(enabled)
                    for left, right in itertools.combinations(values, 2):
                        self.model.add(left != right).only_enforce_if(enabled)
                else:
                    self.model.add_all_different(values)
                self.star_count += 1


def determinant(rows: list[tuple[int, int, int, int]]) -> int:
    answer = 0
    for permutation in itertools.permutations(range(4)):
        sign = permutation_sign(list(permutation))
        product = 1
        for row, column in enumerate(permutation):
            product = product * rows[row][column] % P
        answer = (answer + sign * product) % P
    return answer


def encoded_two_basis_determinant(points, basis: tuple[int, ...], tails: tuple[int, ...]) -> int:
    """The same two-term/one-term formula as the CP model, without CP-SAT."""
    ordered = sorted((*basis, *(4 + row for row in tails)))
    row_at_position: list[int | TailPoint] = [
        index if index < 4 else TailPoint(index - 4) for index in ordered
    ]
    missing = [axis for axis in AXES if axis not in basis]
    if len(tails) == 1:
        mapping = [row if isinstance(row, int) else missing[0] for row in row_at_position]
        return permutation_sign(mapping) * points[4 + tails[0]][missing[0]] % P
    first, second = tails
    c, d = missing
    answer = 0
    for first_axis, second_axis in ((c, d), (d, c)):
        assignment = []
        for row in row_at_position:
            if isinstance(row, int):
                assignment.append(row)
            elif row.row == first:
                assignment.append(first_axis)
            else:
                assignment.append(second_axis)
        answer += (
            permutation_sign(assignment)
            * points[4 + first][first_axis]
            * points[4 + second][second_axis]
        )
    return answer % P


def audit_formulae() -> None:
    """Independently compare the CP formula with direct 4x4 determinants."""
    rng = random.Random(835)
    for _ in range(20):
        points = [tuple(1 if row == col else 0 for col in AXES) for row in AXES]
        points.extend(tuple(rng.randrange(P) for _ in AXES) for _ in range(16))
        for basis in itertools.combinations(AXES, 2):
            for row in range(16):
                for outside in range(20):
                    triple = (*basis, 4 + row)
                    if outside in triple:
                        continue
                    outside_basis = tuple(sorted((*basis, outside))) if outside < 4 else basis
                    tails = (row,) if outside < 4 else tuple(sorted((row, outside - 4)))
                    expected = determinant([points[index] for index in sorted((*triple, outside))])
                    actual = encoded_two_basis_determinant(points, outside_basis, tails)
                    assert actual == expected, (
                        basis,
                        row,
                        outside,
                        actual,
                        expected,
                    )


def reconstruct_points(solver: cp_model.CpSolver, model: RankFourTwoBasisModel):
    points = [tuple(1 if row == col else 0 for col in AXES) for row in AXES]
    points.extend(tuple(int(solver.value(model.x[row][col])) for col in AXES) for row in range(16))
    return points


def independently_check_two_basis(points) -> None:
    for basis in itertools.combinations(AXES, 2):
        for row in range(16):
            triple = tuple(sorted((*basis, 4 + row)))
            values = {
                determinant([points[index] for index in sorted((*triple, outside))])
                for outside in range(20)
                if outside not in triple
            }
            assert len(values) == P, (triple, values)


def check_full(points) -> tuple[bool, tuple[int, int, int] | None, int]:
    for triple in itertools.combinations(range(20), 3):
        values = {
            determinant([points[index] for index in sorted((*triple, outside))])
            for outside in range(20)
            if outside not in triple
        }
        if len(values) != P:
            return False, triple, len(values)
    return True, None, P


def proto_digest(model: cp_model.CpModel) -> str:
    # This installed OR-Tools exposes a pybind CpModelProto rather than the
    # protobuf serializer.  Its deterministic text representation still
    # fingerprints the displayed model for reruns on this version.
    return hashlib.sha256(str(model.proto).encode()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--log", action="store_true")
    parser.add_argument("--no-symmetry-break", action="store_true")
    parser.add_argument(
        "--core",
        action="store_true",
        help="gate each star and print an OR-Tools sufficient infeasibility core",
    )
    args = parser.parse_args()
    audit_formulae()
    print("independent CP-formula determinant audit: PASS")
    rank4 = RankFourTwoBasisModel(
        symmetry_break=not args.no_symmetry_break, explain_core=args.core
    )
    print(
        "rank-4 two-basis CSP:"
        f" stars={rank4.star_count} mod-values={rank4.mod_count}"
        f" products={rank4.product_count} ortools={ORTOOLS_VERSION}"
        f" python={platform.python_version()} symmetry-break=False"
        f" core-mode={args.core}"
        f" proto-sha256={proto_digest(rank4.model)}"
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.seconds
    solver.parameters.num_workers = args.workers
    solver.parameters.log_search_progress = args.log
    solver.parameters.cp_model_presolve = True
    status = solver.solve(rank4.model)
    print(f"CP-SAT status: {solver.status_name(status)}")
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        if status == cp_model.INFEASIBLE and args.core:
            core = solver.sufficient_assumptions_for_infeasibility()
            triples = [rank4.assumption_stars[abs(literal)] for literal in core]
            print(f"sufficient star core ({len(triples)} of 96): {triples}")
        return 0 if status == cp_model.INFEASIBLE else 2
    points = reconstruct_points(solver, rank4)
    independently_check_two_basis(points)
    full, bad_triple, distinct = check_full(points)
    print("independent two-basis check: PASS")
    print(f"full 1,140-star check: {'PASS' if full else 'FAIL'}")
    if not full:
        print(f"first full-star failure: T={bad_triple}, distinct={distinct}/17")
    print(f"normalized points: {points}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

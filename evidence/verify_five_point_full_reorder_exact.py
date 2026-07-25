#!/usr/bin/env python3
"""Verify an exact rational five-point star-gluing certificate for ER #835.

The certificate is a SoPlex ``-X`` primal solution.  Unlisted variables are
zero.  This checker regenerates all k=16 geometry and the exact triple witness,
quotients four- and five-point variables by every admissible position reorder,
and checks every rational equality and nonnegativity condition without
floating-point arithmetic.

Passing this checker proves feasibility only of the stated necessary
five-point relaxation.  It is not a coloring of O_16 and does not solve
Erdos--Rosenfeld Problem #835.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import solve_five_point_star_gluing_lp as model


VARIABLE_RE = re.compile(r"^x([0-9]+)[ \t]+([^ \t]+)$")


def load_solution(path):
    values = {}
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for raw_line in stream:
            digest.update(raw_line)
            line = raw_line.decode("ascii").strip()
            match = VARIABLE_RE.match(line)
            if not match:
                continue
            index = int(match.group(1))
            assert index not in values
            value = Fraction(match.group(2))
            assert value >= 0
            if value:
                values[index] = value
    assert values
    return values, digest.hexdigest()


class ExactRows:
    def __init__(self, solution):
        self.solution = solution
        self.count = 0
        self.nonzeros = 0

    def add(self, terms, rhs, label):
        combined = defaultdict(Fraction)
        for index, coefficient in terms:
            if coefficient:
                combined[index] += Fraction(coefficient)
        lhs = Fraction()
        for index, coefficient in combined.items():
            if coefficient:
                self.nonzeros += 1
                lhs += coefficient * self.solution.get(index, Fraction())
        assert lhs == Fraction(rhs), (label, lhs, Fraction(rhs))
        self.count += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "solution",
        nargs="?",
        default=str(
            Path(__file__).with_name(
                "five_point_full_reorder_exact_seeded_strict.sol"
            )
        ),
    )
    args = parser.parse_args()

    solution, solution_sha256 = load_solution(args.solution)
    (
        orbits,
        orbit_index,
        transitions,
        q,
        categories,
        four_records,
        five_records,
    ) = model.prepare()
    variable_count, four_vars, four_partitions = model.build_variables(
        four_records, five_records
    )
    variable_count, reorder_stats = model.collapse_full_reorder_symmetry(
        variable_count,
        four_records,
        four_vars,
        five_records,
    )
    assert max(solution) < variable_count

    rows = ExactRows(solution)
    model.add_four_endpoint_rows(
        rows, four_records, four_partitions, four_vars, q
    )
    model.add_four_symmetry_rows(
        rows,
        four_records,
        four_partitions,
        four_vars,
        orbit_index,
    )
    model.add_local_bijection_rows(
        rows,
        orbits,
        transitions,
        q,
        four_partitions,
        four_vars,
    )
    model.add_slot_marginal_rows(
        rows,
        five_records,
        categories,
        four_partitions,
        four_vars,
    )

    # Check all four re-based projections explicitly.  In the full position
    # quotient they are symmetry images of one another, but checking all four
    # guards that implication in the certificate verifier itself.
    for name, positions in (
        ("drop-y-w2", (0, 3, 2, 4)),
        ("drop-y-w1", (0, 4, 2, 3)),
        ("drop-x-w2", (1, 3, 2, 4)),
        ("drop-x-w1", (1, 4, 2, 3)),
    ):
        model.add_rebased_rows(
            rows,
            name,
            positions,
            five_records,
            orbits,
            transitions,
            orbit_index,
            four_partitions,
            four_vars,
        )

    print(
        {
            "status": "PASS",
            "scope": (
                "exact five-point necessary relaxation only; "
                "not a coloring and not a solution of ER #835"
            ),
            "variables": variable_count,
            "positive_certificate_variables": len(solution),
            "checked_equalities": rows.count,
            "checked_nonzero_coefficients": rows.nonzeros,
            "reorder_symmetry": reorder_stats,
            "solution_sha256": solution_sha256,
        }
    )


if __name__ == "__main__":
    main()

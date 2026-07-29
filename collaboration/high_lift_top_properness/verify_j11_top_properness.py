#!/usr/bin/env python3
"""Audit the j=11 -> j=12 top-properness argument.

Part A checks the finite arithmetic in the full-tower recurrence at the
actual parameters |P|=16 and |A|=13.

Part B checks a small boundary certificate satisfying only the immediate
lambda/phi slice constraints.  It deliberately has a repeated lambda value
in one column.  This is *not* a counterexample to the full-tower theorem:
the certificate contains no maps on the other P-faces and does not satisfy
the recurrence audited in Part A.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction


LAMBDA = (
    (0, 3, 2),
    (0, 6, 2),
    (3, 5, 6),
    (1, 6, 4),
    (1, 6, 4),
    (6, 5, 3),
)

PHI = {
    (0, 1): (
        (-1, 2, 6, 5, 4, 1),
        (2, -1, 1, 4, 5, 3),
        (6, 1, -1, 2, 0, 4),
        (5, 4, 2, -1, 3, 0),
        (4, 5, 0, 3, -1, 2),
        (1, 3, 4, 0, 2, -1),
    ),
    (0, 2): (
        (-1, 5, 1, 6, 3, 4),
        (5, -1, 4, 3, 6, 1),
        (1, 4, -1, 5, 2, 0),
        (6, 3, 5, -1, 0, 2),
        (3, 6, 2, 0, -1, 5),
        (4, 1, 0, 2, 5, -1),
    ),
    (1, 2): (
        (-1, 1, 4, 0, 5, 6),
        (1, -1, 0, 5, 3, 4),
        (4, 0, -1, 3, 1, 2),
        (0, 5, 3, -1, 2, 1),
        (5, 3, 1, 2, -1, 0),
        (6, 4, 2, 1, 0, -1),
    ),
}


def audit_full_recurrence() -> None:
    """Check every numerical ingredient used in the full j=11 proof."""

    alpha = {1: Fraction(0)}
    expected = {
        2: 8,
        3: 32,
        4: 108,
        5: 256,
        6: 472,
        7: 672,
        8: 758,
        9: 672,
        10: 472,
        11: 256,
        12: 108,
    }
    for size in range(2, 13):
        alpha[size] = (
            Fraction(math.comb(16, size - 1), size) - alpha[size - 1]
        )
        assert alpha[size].denominator == 1
        assert alpha[size] == expected[size]

    modulus = math.lcm(*range(2, 13))
    assert modulus == 27_720
    assert modulus > 16

    # If every d_a is equal and sum_a d_a <= 16, then d is 0 or 1.
    assert [d for d in range(17) if 13 * d <= 16] == [0, 1]

    # There are 16*13 entries.  A color with d=1 contributes 13 entries.
    assert 16 * 13 // 13 == 16
    print(
        "full j=11 recurrence arithmetic:",
        "alpha_2..alpha_12 integral, lcm(2..12)=27720,",
        "multiplicity forced to 0 or 1: PASS",
    )


def audit_weakened_boundary_certificate() -> None:
    """Check the small certificate for the immediate slice constraints."""

    vertices = range(6)
    palette = set(range(7))

    # Constraint 1: every lambda row is injective.
    for row in LAMBDA:
        assert len(set(row)) == 3

    # Desired next top-properness fails in column 0 (vertices 0 and 1).
    assert LAMBDA[0][0] == LAMBDA[1][0] == 0

    # Constraint 2: phi_ab is a proper edge-colouring of K6 and, at
    # vertex x, its two missing colors are lambda_x(a), lambda_x(b).
    for pair, matrix in PHI.items():
        a, b = pair
        for x in vertices:
            assert matrix[x][x] == -1
            assert all(matrix[x][y] == matrix[y][x] for y in vertices)
            incident = {matrix[x][y] for y in vertices if y != x}
            assert len(incident) == 5
            assert palette - incident == {LAMBDA[x][a], LAMBDA[x][b]}

    # Constraint 3: on every P-edge xy, the three phi_ab values form a
    # proper edge-colouring of K3, equivalently they are all distinct.
    for x, y in itertools.combinations(vertices, 2):
        values = {PHI[pair][x][y] for pair in PHI}
        assert len(values) == 3

    print(
        "weakened m=3, |P|=6 boundary certificate:",
        "immediate lambda/phi constraints hold with a column repeat: PASS",
    )
    print(
        "delimiter:",
        "this certificate omits the other lower-tower faces and does not",
        "refute full-tower automaticity",
    )


def main() -> int:
    audit_full_recurrence()
    audit_weakened_boundary_certificate()
    print(
        "scope:",
        "the full recurrence proves only j=11 -> j=12 top-properness;",
        "it does not construct a 17-colouring or solve #835",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

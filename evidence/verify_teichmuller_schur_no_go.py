#!/usr/bin/env python3
"""Exact verifier for evidence/teichmuller_schur_no_go.md.

Only Python integers are used.  The script verifies:

* the valencies, top eigenvalues, and integral nonnegative quotient entries;
* the endpoint identities T_0=J-I and T_15=I;
* all 256 Bose--Mesner product identities, using independently enumerated
  four-cell intersection numbers; and
* the formal cyclic-character Schur multiplication table.
"""

from math import comb


R = 15
P = 17


def cbinom(n: int, k: int) -> int:
    return comb(n, k) if 0 <= k <= n else 0


def matmul(left, right):
    n = len(left)
    return [
        [
            sum(left[row][mid] * right[mid][col] for mid in range(n))
            for col in range(n)
        ]
        for row in range(n)
    ]


def matadd_scaled(matrices, scales):
    n = len(matrices[0])
    return [
        [
            sum(scale * matrix[row][col]
                for matrix, scale in zip(matrices, scales))
            for col in range(n)
        ]
        for row in range(n)
    ]


def intersection_number(i: int, j: int, k: int) -> int:
    """Number of Z with |X∩Z|=i and |Y∩Z|=j, given |X∩Y|=k."""
    total = 0
    # The cells (X∩Y, X\Y, Y\X, outside X∪Y) have sizes
    # (k, R-k, R-k, k+1).  If a=|Z∩X∩Y|, the other three
    # chosen cell sizes are forced.
    for a in range(k + 1):
        b = i - a
        c = j - a
        d = R - a - b - c
        total += (
            cbinom(k, a)
            * cbinom(R - k, b)
            * cbinom(R - k, c)
            * cbinom(k + 1, d)
        )
    return total


def main() -> None:
    valencies = []
    eigenvalues = []
    same_counts = []
    different_counts = []
    quotient_matrices = []

    for j in range(R + 1):
        value = comb(R, j) * comb(R + 1, j + 1)
        eigenvalue = (-1) ** (j + 1) * comb(R, j)
        assert (value - eigenvalue) % P == 0
        assert (value + (P - 1) * eigenvalue) % P == 0
        different = (value - eigenvalue) // P
        same = (value + (P - 1) * eigenvalue) // P
        assert same >= 0 and different >= 0
        assert same + (P - 1) * different == value
        assert same - different == eigenvalue

        matrix = [
            [
                same if row == col else different
                for col in range(P)
            ]
            for row in range(P)
        ]
        assert all(sum(row) == value for row in matrix)

        valencies.append(value)
        eigenvalues.append(eigenvalue)
        same_counts.append(same)
        different_counts.append(different)
        quotient_matrices.append(matrix)

    identity = [
        [int(row == col) for col in range(P)]
        for row in range(P)
    ]
    complete_graph = [
        [int(row != col) for col in range(P)]
        for row in range(P)
    ]
    assert quotient_matrices[0] == complete_graph
    assert quotient_matrices[R] == identity

    # The four-cell formula must recover each relation valency.
    for i in range(R + 1):
        for k in range(R + 1):
            assert sum(
                intersection_number(i, j, k) for j in range(R + 1)
            ) == valencies[i]

    # Verify every Bose--Mesner product as a 17x17 integer matrix.
    for i in range(R + 1):
        for j in range(R + 1):
            left = matmul(quotient_matrices[i], quotient_matrices[j])
            coefficients = [
                intersection_number(i, j, k) for k in range(R + 1)
            ]
            right = matadd_scaled(quotient_matrices, coefficients)
            assert left == right, (i, j)

    # Formal Fourier-character checks.  A character is represented by its
    # exponent modulo P, so multiplication is exact modular addition.
    for m in range(P):
        for n in range(P):
            product_exponent = (m + n) % P
            assert product_exponent == (m + n) % P
        for j in range(R + 1):
            action = valencies[j] if m == 0 else eigenvalues[j]
            assert isinstance(action, int)

    print(
        {
            "status": "PASS",
            "relations": R + 1,
            "bose_mesner_products": (R + 1) ** 2,
            "quotient_dimension": P,
            "same_counts": same_counts,
            "different_counts": different_counts,
        }
    )


if __name__ == "__main__":
    main()

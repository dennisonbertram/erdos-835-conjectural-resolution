#!/usr/bin/env python3
"""Exact checks for evidence/nilpotent_shift_obstruction.md.

Only Python integers and fractions are used.  The exact-cover engine is
the repository's deterministic Algorithm X implementation.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from disjoint_mates import algox_solutions, steiner_cover_instance  # noqa: E402


def inverse_mod(value, prime):
    return pow(value % prime, -1, prime)


def projector_entry(k, t):
    return Fraction((-1) ** (k - t), (k + 1) * comb(k, t))


def determinant(matrix):
    """Fraction-preserving Gaussian determinant."""
    matrix = [list(row) for row in matrix]
    answer = Fraction(1)
    for column in range(len(matrix)):
        pivot = next(
            (row for row in range(column, len(matrix))
             if matrix[row][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            matrix[pivot], matrix[column] = matrix[column], matrix[pivot]
            answer = -answer
        value = matrix[column][column]
        answer *= value
        for j in range(column, len(matrix)):
            matrix[column][j] /= value
        for row in range(column + 1, len(matrix)):
            value = matrix[row][column]
            if not value:
                continue
            for j in range(column, len(matrix)):
                matrix[row][j] -= value * matrix[column][j]
    return answer


def verify_kernel_formula():
    for k in (2, 4, 6, 16):
        q = k + 1
        assert projector_entry(k, k) == Fraction(1, q)
        for t in range(k):
            assert (
                (k - t) * projector_entry(k, t + 1)
                + (t + 1) * projector_entry(k, t)
            ) == 0


def verify_first_adic_tangent():
    for q in (3, 5, 7, 17):
        k = q - 1
        q2 = q * q
        harmonic = 0
        for t in range(k + 1):
            if t:
                harmonic = (harmonic + inverse_mod(t, q)) % q
            denominator = comb(k, t)
            signed_inverse = (
                ((-1) ** (k - t)) * inverse_mod(denominator, q2)
            ) % q2
            assert (signed_inverse - 1) % q == 0
            tangent = ((signed_inverse - 1) // q) % q
            assert tangent == harmonic

        n = comb(2 * k, k)
        assert n % q == 0
        d = n // q
        assert d % q == q - 1


def exact_cover_family(v, block_size):
    blocks = list(combinations(range(v), block_size))
    rows, columns = steiner_cover_instance(v, block_size - 1, blocks)
    base = frozenset(algox_solutions(rows, columns, cap=1)[0])
    remaining = [block for block in blocks if block not in base]
    rows, columns = steiner_cover_instance(
        v, block_size - 1, remaining
    )
    mates = [
        frozenset(solution)
        for solution in algox_solutions(rows, columns)
    ]
    return base, mates


def verify_negative_controls():
    expected = {
        (7, 3): (7, 8, Counter({1: 28})),
        (11, 5): (66, 144, Counter({6: 6336, 18: 3960})),
    }
    for parameters, (base_size, mate_count, distribution) in expected.items():
        base, mates = exact_cover_family(*parameters)
        assert len(base) == base_size
        assert len(mates) == mate_count
        observed = Counter(
            len(mates[i] & mates[j])
            for i, j in combinations(range(len(mates)), 2)
        )
        assert observed == distribution


def verify_k2_positive_control():
    points = range(4)
    omega = list(combinations(points, 2))
    index = {edge: i for i, edge in enumerate(omega)}
    fibres = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    colour = {}
    for a, fibre in enumerate(fibres):
        for edge in fibre:
            colour[tuple(sorted(edge))] = a

    # Every 1-star is rainbow.
    for point in points:
        assert {
            colour[edge] for edge in omega if point in edge
        } == {0, 1, 2}

    pmat = [
        [
            projector_entry(2, len(set(left) & set(right)))
            for right in omega
        ]
        for left in omega
    ]

    # P^2=P exactly.
    for i in range(6):
        for j in range(6):
            assert sum(pmat[i][h] * pmat[h][j] for h in range(6)) == (
                pmat[i][j]
            )

    # Q is the projector onto the two centred colour indicators, and Q<=P.
    qmat = [
        [
            Fraction(
                3 * int(colour[left] == colour[right]) - 1,
                6,
            )
            for right in omega
        ]
        for left in omega
    ]
    for i in range(6):
        for j in range(6):
            assert sum(qmat[i][h] * qmat[h][j] for h in range(6)) == (
                qmat[i][j]
            )
            assert sum(pmat[i][h] * qmat[h][j] for h in range(6)) == (
                qmat[i][j]
            )

    # The two high principal-minor sectors are uniform.
    for r in (1, 2):
        sectors = defaultdict(Fraction)
        for subset in combinations(range(6), r):
            principal = [
                [pmat[i][j] for j in subset]
                for i in subset
            ]
            residue = sum(colour[omega[i]] for i in subset) % 3
            sectors[residue] += determinant(principal)
        assert sectors == {
            a: Fraction(comb(2, r), 3) for a in range(3)
        }


def verify_hilbert_schmidt_value():
    q = 17
    n = 17_678_835
    same = Fraction(2 * n * (3 * q - 1), q * q * (q + 1))
    trace = Fraction(2 * n, q)
    different = (trace - same) / (q - 1)
    assert same == Fraction(98_215_750, 289)
    assert different == Fraction(31_429_040, 289)
    assert q * (same - different) == 3_928_630


def main():
    verify_kernel_formula()
    verify_first_adic_tangent()
    verify_k2_positive_control()
    verify_negative_controls()
    verify_hilbert_schmidt_value()
    print("kernel recurrence and 17-adic tangent: exact")
    print("k=2 shift/principal-minor control: exact")
    print("k=4 Fano and k=6 Witt controls: exhaustive exact cover")
    print("k=16 Hilbert--Schmidt value: 3928630")
    print("ALL NILPOTENT-SHIFT CHECKS PASSED")


if __name__ == "__main__":
    main()

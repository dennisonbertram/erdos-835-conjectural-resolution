#!/usr/bin/env python3
"""Exact controls for the deleted-colour Hadamard-kernel obstruction.

All linear algebra and enumeration are over the prime field F_p.  The
script deliberately writes no output files.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product
from math import comb
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "evidence"))

from disjoint_mates import algox_solutions, steiner_cover_instance  # noqa: E402


def inv(value: int, prime: int) -> int:
    return pow(value % prime, -1, prime)


def rref_mod(matrix: list[list[int]], prime: int) -> tuple[list[list[int]], list[int]]:
    work = [[entry % prime for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivots: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        found = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if found is None:
            continue
        work[pivot_row], work[found] = work[found], work[pivot_row]
        scale = inv(work[pivot_row][column], prime)
        work[pivot_row] = [scale * entry % prime for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                (left - scale * right) % prime
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return work, pivots


def nullspace_mod(matrix: list[list[int]], prime: int) -> list[list[int]]:
    reduced, pivots = rref_mod(matrix, prime)
    pivot_set = set(pivots)
    free = [column for column in range(len(matrix[0])) if column not in pivot_set]
    basis: list[list[int]] = []
    for free_column in free:
        vector = [0] * len(matrix[0])
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column] % prime
        basis.append(vector)
    return basis


def first_steiner_system(k: int) -> tuple[list[tuple[int, ...]], set[tuple[int, ...]]]:
    blocks = list(combinations(range(2 * k), k))
    rows, columns = steiner_cover_instance(2 * k, k - 1, blocks)
    system = set(algox_solutions(rows, columns, cap=1)[0])
    return blocks, system


def deleted_colour_matrix(
    k: int,
) -> tuple[list[list[int]], list[tuple[int, ...]], set[tuple[int, ...]]]:
    blocks, system = first_steiner_system(k)
    rows = list(combinations(range(2 * k), k - 1))
    row_index = {row: index for index, row in enumerate(rows)}
    remaining = [block for block in blocks if block not in system]
    matrix = [[0] * len(remaining) for _ in rows]
    for column, block in enumerate(remaining):
        for facet in combinations(block, k - 1):
            matrix[row_index[facet]][column] = 1
    assert len(matrix) == len(remaining)
    return matrix, remaining, system


def scale(value: int, vector: tuple[int, ...], prime: int) -> tuple[int, ...]:
    return tuple(value * entry % prime for entry in vector)


def ambient_vector(
    coordinates: tuple[int, ...], basis: list[list[int]], prime: int
) -> tuple[int, ...]:
    return tuple(
        sum(
            coefficient * basis[row][column]
            for row, coefficient in enumerate(coordinates)
        )
        % prime
        for column in range(len(basis[0]))
    )


def product_signature(
    left: tuple[int, ...],
    right: tuple[int, ...],
    matrix: list[list[int]],
    prime: int,
) -> tuple[int, ...]:
    """M(left*right), with its first coordinate subtracted from all others."""
    values = [
        sum(row[column] * left[column] * right[column] for column in range(len(left)))
        % prime
        for row in matrix
    ]
    return tuple((value - values[0]) % prime for value in values[1:])


def projective_vectors(dimension: int, prime: int):
    """One normalized representative of every line of F_p^dimension."""
    for first in range(dimension):
        for tail in product(range(prime), repeat=dimension - first - 1):
            yield (0,) * first + (1,) + tail


def projective_normalize(vector: tuple[int, ...], prime: int) -> tuple[int, ...]:
    first = next(entry for entry in vector if entry)
    return scale(inv(first, prime), vector, prime)


def maximal_totally_constant_product_dimension(
    matrix: list[list[int]], prime: int
) -> tuple[int, list[tuple[int, ...]], int]:
    """Find the largest U in ker(M) with M(x*y) constant for x,y in U.

    The return value contains dim ker M, the isotropic projective lines,
    and the exact maximum for the controls in which no compatible pair
    exists.  This finite enumeration is intended only for k=2 and k=4.
    """
    basis = nullspace_mod(matrix, prime)
    dimension = len(basis)
    candidates = [
        ambient_vector(vector, basis, prime)
        for vector in projective_vectors(dimension, prime)
    ]
    isotropic = [
        vector
        for vector in candidates
        if not any(product_signature(vector, vector, matrix, prime))
    ]

    # The finite controls below have no compatible pair of distinct lines,
    # so their maximum is one.  Keep this direct all-pairs certificate
    # simpler than a generic subspace backtracker.
    compatible_pair = any(
        not any(product_signature(left, right, matrix, prime))
        for left, right in combinations(isotropic, 2)
    )
    maximum = 2 if compatible_pair else int(bool(isotropic))
    return dimension, isotropic, maximum


def disjoint_mates(k: int, base: set[tuple[int, ...]]) -> list[set[tuple[int, ...]]]:
    blocks = list(combinations(range(2 * k), k))
    remaining = [block for block in blocks if block not in base]
    rows, columns = steiner_cover_instance(2 * k, k - 1, remaining)
    return [set(solution) for solution in algox_solutions(rows, columns)]


def check_control(k: int, prime: int, expected: tuple[int, int, int]) -> None:
    assert prime == k + 1
    matrix, remaining, system = deleted_colour_matrix(k)
    kernel_dimension, isotropic, maximum = maximal_totally_constant_product_dimension(
        matrix, prime
    )
    observed = (kernel_dimension, len(isotropic), maximum)
    assert observed == expected, (k, observed, expected)

    # In both exhaustive controls, the projective isotropic lines are
    # exactly h_C = 1 + 1_C for the Steiner systems C disjoint from the
    # deleted base system.
    column_index = {block: index for index, block in enumerate(remaining)}
    mate_lines = set()
    mates = disjoint_mates(k, system)
    for mate in mates:
        indicator = [0] * len(remaining)
        for block in mate:
            indicator[column_index[block]] = 1
        h_vector = tuple((entry + 1) % prime for entry in indicator)
        assert not any(
            sum(row[column] * h_vector[column] for column in range(len(h_vector)))
            % prime
            for row in matrix
        )
        assert not any(product_signature(h_vector, h_vector, matrix, prime))
        mate_lines.add(projective_normalize(h_vector, prime))
    assert mate_lines == {projective_normalize(vector, prime) for vector in isotropic}

    # Pairwise product incompatibility is exactly the absence of two
    # disjoint mates: h_C*h_D has nonconstant star sums.
    for left, right in combinations(mate_lines, 2):
        assert any(product_signature(left, right, matrix, prime))
    print(
        f"k={k}, p={prime}: |D|={len(system)}, deleted square={len(matrix)}, "
        f"kernel={observed[0]}, isotropic lines={observed[1]} "
        f"(all {len(mates)} disjoint mates), "
        f"max totally-constant-product dimension={observed[2]}"
    )


def extend_boundary_system(
    boundary: set[tuple[int, ...]], k: int
) -> set[tuple[int, ...]]:
    old_points = set(range(2 * k - 1))
    infinity = 2 * k - 1
    extended: set[tuple[int, ...]] = set()
    for block in boundary:
        extended.add(tuple(sorted(set(block) | {infinity})))
        extended.add(tuple(sorted(old_points - set(block))))
    return extended


def check_k6_complement_profile() -> None:
    """Verify the intersection equations forcing complement closure."""
    lambdas = tuple(comb(12 - s, 5 - s) // (6 - s) for s in range(5))
    assert lambdas == (132, 66, 30, 12, 4)

    n4 = comb(6, 4) * (lambdas[4] - 1)
    n3 = comb(6, 3) * (lambdas[3] - 1) - 4 * n4
    n2 = comb(6, 2) * (lambdas[2] - 1) - 3 * n3 - 6 * n4
    n1 = comb(6, 1) * (lambdas[1] - 1) - 2 * n2 - 3 * n3 - 4 * n4
    n0 = lambdas[0] - 1 - n1 - n2 - n3 - n4
    assert (n0, n1, n2, n3, n4) == (1, 0, 45, 40, 45)


def check_k6_mate_sector() -> None:
    """Check the 144 design-valued lines at the false k=6 control.

    This does not enumerate every projective isotropic line in the much
    larger deleted kernel.  It exactly checks the entire idempotent
    (Steiner-mate) sector.
    """
    k, prime = 6, 7
    check_k6_complement_profile()
    boundary_blocks = list(combinations(range(11), 5))
    rows, columns = steiner_cover_instance(11, 4, boundary_blocks)
    base_boundary = set(algox_solutions(rows, columns, cap=1)[0])
    remaining_boundary = [
        block for block in boundary_blocks if block not in base_boundary
    ]
    rows, columns = steiner_cover_instance(11, 4, remaining_boundary)
    boundary_mates = [set(solution) for solution in algox_solutions(rows, columns)]
    assert len(boundary_mates) == 144

    base = extend_boundary_system(base_boundary, k)
    all_blocks = list(combinations(range(12), 6))
    remaining = [block for block in all_blocks if block not in base]
    row_sets = list(combinations(range(12), 5))
    row_index = {row: index for index, row in enumerate(row_sets)}
    matrix = [[0] * len(remaining) for _ in row_sets]
    for column, block in enumerate(remaining):
        for facet in combinations(block, 5):
            matrix[row_index[facet]][column] = 1
    assert len(matrix) == len(remaining) == 792
    column_index = {block: index for index, block in enumerate(remaining)}

    extended_mates = []
    row_supports = [
        [column for column, entry in enumerate(row) if entry] for row in matrix
    ]
    assert all(len(support) == k for support in row_supports)
    for boundary_mate in boundary_mates:
        mate = extend_boundary_system(boundary_mate, k)
        assert not (mate & base)
        extended_mates.append(mate)
        indicator = [0] * len(remaining)
        for block in mate:
            indicator[column_index[block]] = 1
        h_vector = tuple((entry + 1) % prime for entry in indicator)
        assert all(
            sum(h_vector[column] for column in support) % prime == 0
            for support in row_supports
        )
        square_sums = {
            sum(h_vector[column] ** 2 for column in support) % prime
            for support in row_supports
        }
        assert square_sums == {2}
        # This is the direct matrix assertion
        # M(h_C*h_C)=2*1, i.e. the projective line [h_C] is isotropic.

    intersections = {
        len(left & right) for left, right in combinations(extended_mates, 2)
    }
    assert intersections == {12, 36}
    # For h_C=1+1_C and h_D=1+1_D,
    # M(h_C*h_D)=1+M(1_{C intersect D}).  The common blocks have disjoint
    # facet sets and cover 6|C intersect D| rows.  Since the observed
    # intersections are nonempty and smaller than 132, this vector takes
    # both values 1 and 2 and is therefore not constant.
    assert all(0 < overlap < len(base) for overlap in intersections)
    print(
        "k=6, p=7 idempotent sector: 144 deleted-base mate lines are "
        "isotropic; every pair is product-incompatible "
        "(top intersections 12 or 36)"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--k6",
        action="store_true",
        help="also exhaust the 144 design-valued k=6 mate lines",
    )
    args = parser.parse_args()
    check_control(2, 3, (1, 1, 1))
    check_control(4, 5, (7, 8, 1))
    if args.k6:
        check_k6_mate_sector()
    print("ALL DELETED-COLOUR HADAMARD-KERNEL CHECKS PASSED")


if __name__ == "__main__":
    main()

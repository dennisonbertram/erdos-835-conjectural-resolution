#!/usr/bin/env python3
"""Exact audit of the full integral -1 eigenspace of the Odd graph.

For O_k put r=k-1 and v=2r+1.  The full integral -1 eigenlattice is

    L_r = ker_Z W_{r-1,r}(v),

where W is the unsigned inclusion matrix from (r-1)-sets to r-sets.

The computationally nontrivial part of this verifier is the k=4 control
case.  It enumerates *all* vectors of norm at most 14 in L_3 by an exact
Fincke--Pohst recursion over Fraction-valued LDL data.  It then checks that
the graph on norm-14 vectors, with adjacency x.y=7, has no K_4.  Thus L_3
does not contain a copy of sqrt(7) A_4, even abstractly.

Only exact integer/rational arithmetic is used for the enumeration and
final tests.  NumPy is used merely to batch the 14-term integer dot
products used to construct the graph.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import comb, isqrt

import numpy as np
from sympy import Matrix, factorint
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

try:
    from verify_saturated_support_lattice import (
        binary_nullspace,
        gf2_rank,
        saturated_integer_kernel,
    )
except ModuleNotFoundError:
    from evidence.verify_saturated_support_lattice import (
        binary_nullspace,
        gf2_rank,
        saturated_integer_kernel,
    )


def inclusion_matrix(v, r):
    blocks = list(combinations(range(v), r))
    facets = list(combinations(range(v), r - 1))
    matrix = [
        [int(set(facet) <= set(block)) for block in blocks]
        for facet in facets
    ]
    return matrix, blocks


def ceil_div(a, b):
    assert b > 0
    return -((-a) // b)


def enumerate_short_vectors(basis, bound):
    """Enumerate all z*basis with squared norm at most ``bound`` exactly."""
    reduced = Matrix(basis).lll()
    gram = reduced * reduced.T
    lower, diagonal = gram.LDLdecomposition(hermitian=False)
    dimension = reduced.rows

    lower_q = [
        [
            Fraction(int(lower[i, j].p), int(lower[i, j].q))
            for j in range(dimension)
        ]
        for i in range(dimension)
    ]
    diagonal_q = [
        Fraction(int(diagonal[i, i].p), int(diagonal[i, i].q))
        for i in range(dimension)
    ]

    coefficients = [0] * dimension
    coefficient_vectors = []

    def recurse(index, used):
        if index < 0:
            coefficient_vectors.append(tuple(coefficients))
            return

        center_offset = sum(
            lower_q[j][index] * coefficients[j]
            for j in range(index + 1, dimension)
        )
        remaining = Fraction(bound) - used
        radius_squared = remaining / diagonal_q[index]

        # Solve (b*z+a)^2 * v <= u*b^2 with integer arithmetic.
        a = center_offset.numerator
        b = center_offset.denominator
        u = radius_squared.numerator
        v = radius_squared.denominator
        maximum = isqrt((u * b * b) // v)
        low = ceil_div(-maximum - a, b)
        high = (maximum - a) // b

        for value in range(low, high + 1):
            term = (
                diagonal_q[index]
                * (Fraction(value) + center_offset) ** 2
            )
            if term <= remaining:
                coefficients[index] = value
                recurse(index - 1, used + term)
        coefficients[index] = 0

    recurse(dimension - 1, Fraction(0))

    vectors = []
    for coefficients_ in coefficient_vectors:
        vector = tuple(
            sum(
                coefficients_[i] * int(reduced[i, j])
                for i in range(dimension)
            )
            for j in range(reduced.cols)
        )
        assert sum(entry * entry for entry in vector) <= bound
        vectors.append(vector)
    return vectors


def dot_seven_graph(vectors):
    """Return adjacency sets for the exact graph x~y iff x.y=7."""
    array = np.asarray(vectors, dtype=np.int16)
    adjacency = [set() for _ in vectors]
    block_size = 256
    for low in range(0, len(vectors), block_size):
        high = min(low + block_size, len(vectors))
        dots = array[low:high] @ array.T
        for local, index in enumerate(range(low, high)):
            neighbours = np.flatnonzero(dots[local, :index] == 7)
            for other_ in neighbours:
                other = int(other_)
                adjacency[index].add(other)
                adjacency[other].add(index)
    return adjacency


def find_k4(adjacency):
    """Find a four-clique, or return None after an exhaustive bitset test."""
    masks = []
    for neighbours in adjacency:
        mask = 0
        for neighbour in neighbours:
            mask |= 1 << neighbour
        masks.append(mask)

    for first, neighbours in enumerate(adjacency):
        for second in neighbours:
            if second <= first:
                continue
            common = masks[first] & masks[second]
            remaining = common
            while remaining:
                lowest = remaining & -remaining
                third = lowest.bit_length() - 1
                if masks[third] & (common ^ lowest):
                    fourth_mask = masks[third] & (common ^ lowest)
                    fourth = (fourth_mask & -fourth_mask).bit_length() - 1
                    return first, second, third, fourth
                remaining ^= lowest
    return None


def mod2_a4_check(basis):
    """Exhibit the required quadratic space inside L/2L at k=4."""
    # Coefficients in the deterministic saturated basis.
    words = [0x24, 0x48, 0x6D, 0x109]
    lifts = [
        [
            sum(((word >> i) & 1) * basis[i][j] for i in range(len(basis)))
            for j in range(len(basis[0]))
        ]
        for word in words
    ]
    polar = [
        [
            sum(x * y for x, y in zip(left, right)) % 2
            for right in lifts
        ]
        for left in lifts
    ]
    quadratic = [
        (sum(entry * entry for entry in lift) // 2) % 2
        for lift in lifts
    ]
    target_polar = [
        [int(i != j) for j in range(4)]
        for i in range(4)
    ]
    assert polar == target_polar
    assert quadratic == [1, 1, 1, 1]
    return words, polar, quadratic


def determinant_prime_exponents(r):
    """Prime exponents in disc ker_Z W_{r-1,r}(2r+1)."""
    exponents = Counter()
    v = 2 * r + 1
    for i in range(r):
        multiplicity = comb(v, i) - (comb(v, i - 1) if i else 0)
        for prime, exponent in factorint(r + 2 - i).items():
            exponents[int(prime)] += int(exponent) * multiplicity
        for prime, exponent in factorint(r - i).items():
            exponents[int(prime)] -= int(exponent) * multiplicity
    assert all(exponent >= 0 for exponent in exponents.values())
    return dict(sorted(exponents.items()))


def base_p_digits(number, prime):
    digits = []
    while number:
        digits.append(number % prime)
        number //= prime
    return digits or [0]


def contains_to_base_p(s, t, prime):
    """James's f_p(s,t) for two-row Specht decomposition numbers."""
    if s <= 0:
        return 0
    if t == 0:
        return 1
    s_digits = base_p_digits(s + 1, prime)
    t_digits = base_p_digits(t, prime)
    return int(
        len(s_digits) > len(t_digits)
        and all(
            t_digit in (0, s_digit)
            for s_digit, t_digit in zip(s_digits, t_digits)
        )
    )


def prime_valuation(number, prime):
    exponent = 0
    while number % prime == 0:
        number //= prime
        exponent += 1
    return exponent


def specht_jordan_multiplicities(n, m, prime):
    """p-adic Gram elementary-divisor multiplicities for S^(n-m,m).

    This implements Künzer--Nebe, Theorem 2.5: James's two-row
    decomposition matrix followed by the Jantzen/Schaper exponents.
    The result maps valuation -> multiplicity.
    """
    decomposition = Matrix.zeros(m + 1)
    for i in range(m + 1):
        for j in range(i + 1):
            decomposition[i, j] = contains_to_base_p(
                n - 2 * j,
                i - j,
                prime,
            )
    assert decomposition.det() == 1
    specht_dimensions = Matrix(
        [
            comb(n, j) - (comb(n, j - 1) if j else 0)
            for j in range(m + 1)
        ]
    )
    simple_dimensions = decomposition.inv() * specht_dimensions
    simple_dimensions = [int(value) for value in simple_dimensions]
    assert all(value > 0 for value in simple_dimensions)

    multiplicities = Counter()
    for j in range(m):
        exponent = sum(
            (
                prime_valuation(n + 1 - m - i, prime)
                - prime_valuation(m - i, prime)
            )
            * contains_to_base_p(n - 2 * j, i - j, prime)
            for i in range(j, m)
        )
        assert exponent >= 0
        if exponent:
            multiplicities[exponent] += simple_dimensions[j]

    rank = comb(n, m) - comb(n, m - 1)
    multiplicities[0] = rank - sum(multiplicities.values())
    assert multiplicities[0] == simple_dimensions[m]
    return dict(sorted(multiplicities.items()))


def main():
    matrix, _ = inclusion_matrix(7, 3)
    basis, row_rank = saturated_integer_kernel(matrix)
    assert row_rank == 21
    assert len(basis) == 14

    basis_matrix = Matrix(basis)
    gram = basis_matrix * basis_matrix.T
    determinant = int(gram.det())
    determinant_factors = dict(sorted(factorint(determinant).items()))
    assert determinant_factors == {2: 6, 3: 13, 5: 1}

    smith = smith_normal_form(gram, domain=ZZ)
    smith_diagonal = [abs(int(smith[i, i])) for i in range(smith.rows)]
    assert smith_diagonal == [
        1, 3, 3, 3, 3, 3, 3, 3, 6, 6, 6, 6, 6, 30
    ]

    short = enumerate_short_vectors(basis, 14)
    norm_counts = Counter(sum(x * x for x in vector) for vector in short)
    assert norm_counts == {0: 1, 8: 210, 12: 1260, 14: 5280}

    norm_14 = sorted(
        vector
        for vector in short
        if sum(x * x for x in vector) == 14
    )
    assert all(
        Counter(abs(entry) for entry in vector if entry) == {1: 14}
        for vector in norm_14
    )
    digest = sha256(
        b"".join(
            bytes(entry + 1 for entry in vector)
            for vector in norm_14
        )
    ).hexdigest()

    adjacency = dot_seven_graph(norm_14)
    degrees = [len(neighbours) for neighbours in adjacency]
    edge_count = sum(degrees) // 2
    assert edge_count == 403_200
    assert min(degrees) == 152
    assert max(degrees) == 168
    assert find_k4(adjacency) is None

    packed_gram_rows = [
        sum((int(gram[i, j]) & 1) << j for j in range(gram.cols))
        for i in range(gram.rows)
    ]
    polar_rank = gf2_rank(packed_gram_rows)
    radical = binary_nullspace(
        [
            [int(gram[i, j]) & 1 for j in range(gram.cols)]
            for i in range(gram.rows)
        ]
    )
    assert polar_rank == 8
    assert len(radical) == 6
    for word in radical:
        lift = [
            sum(((word >> i) & 1) * basis[i][j] for i in range(len(basis)))
            for j in range(len(basis[0]))
        ]
        assert (sum(entry * entry for entry in lift) // 2) % 2 == 0

    words, polar, quadratic = mod2_a4_check(basis)

    exponents_16 = determinant_prime_exponents(15)
    assert exponents_16 == {
        2: 45_703_018,
        3: 40_050_449,
        5: 34_011_401,
        7: 18_936_940,
        11: 539_400,
        13: 26_536,
        17: 1,
    }
    total_vertices = comb(31, 15)
    fibre_size = total_vertices // 17
    assert total_vertices == 300_540_195
    assert fibre_size == 17_678_835
    assert fibre_size % 17 == 8

    jordan_4 = {
        prime: specht_jordan_multiplicities(7, 3, prime)
        for prime in (2, 3, 5)
    }
    assert jordan_4 == {
        2: {0: 8, 1: 6},
        3: {0: 1, 1: 13},
        5: {0: 13, 1: 1},
    }
    # The target 7*A_4 is 3-unimodular of rank four.
    assert jordan_4[3][0] < 4
    jordan_16 = {
        prime: specht_jordan_multiplicities(31, 15, prime)
        for prime in (2, 3, 5, 7, 11, 13, 17)
    }
    assert jordan_16 == {
        2: {0: 32_768, 1: 24_946_816, 2: 10_378_056, 3: 30},
        3: {0: 1, 1: 30_664_889, 2: 4_692_780},
        5: {0: 1_346_269, 1: 34_011_401},
        7: {0: 16_420_730, 1: 18_936_940},
        11: {0: 34_818_270, 1: 539_400},
        13: {0: 35_331_134, 1: 26_536},
        17: {0: 35_357_669, 1: 1},
    }
    # Required target capacities: unit rank 16 at 2,7,11,13; scale-two
    # rank 16 at 3; scale-one rank 16 at 5; and ranks 15+1 at 17.
    assert jordan_16[2][0] >= 16
    assert jordan_16[3][2] >= 16
    assert jordan_16[5][1] >= 16
    assert all(jordan_16[prime][0] >= 16 for prime in (7, 11, 13))
    assert jordan_16[17][0] >= 15 and jordan_16[17][1] == 1

    # At p=r+2, coordinate projection gives the L discriminant coefficient
    # 2/p.  The n-scaled A_{p-1} coefficient is -n^{-1}/p.
    coefficient_l = 2 % 17
    coefficient_s = (-pow(fibre_size, -1, 17)) % 17
    assert coefficient_l == coefficient_s == 2

    print("k=4 full eigenlattice rank:", len(basis))
    print("k=4 Gram Smith diagonal:", smith_diagonal)
    print("k=4 discriminant factors:", determinant_factors)
    print("k=4 exact short-vector counts:", dict(sorted(norm_counts.items())))
    print("k=4 norm-14 vector SHA-256:", digest)
    print(
        "k=4 dot-7 graph:",
        f"{len(norm_14)} vertices, {edge_count} edges,",
        f"degrees {min(degrees)}..{max(degrees)}, K4 absent",
    )
    print(
        "k=4 mod-2 form:",
        f"polar rank {polar_rank}, radical {len(radical)};",
        "target witness coefficients",
        [hex(word) for word in words],
    )
    print("k=4 target polar matrix:", polar, "q:", quadratic)
    print("k=4 p-adic Jordan multiplicities:", jordan_4)
    print("k=16 full eigenlattice rank:", comb(31, 15) - comb(31, 14))
    print("k=16 discriminant prime exponents:", exponents_16)
    print("k=16 p-adic Jordan multiplicities:", jordan_16)
    print("k=16 fibre size:", fibre_size, "(mod 17 =", fibre_size % 17, ")")
    print("k=16 17-primary coefficients: L=2/17, target=2/17")
    print("full eigenlattice audit: PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact audit for the primitive b*A_16 lattice route at k=16.

This verifier checks:

* the target parameters and factorization;
* the determinant of ker_Z W_{14,15}(31) from the Wilson data;
* the complete relevant p-adic Specht/Jordan multiplicities;
* equality of the target and ambient 17-primary coefficients;
* an explicit primitive embedding of b*A_16 in Z^68.

The last item is a countermodel to determinant-only reasoning, not an
embedding in the actual incidence kernel.
"""

from math import comb, gcd

from sympy import Matrix, factorint
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

try:
    from verify_full_eigenlattice import specht_jordan_multiplicities
except ModuleNotFoundError:
    from evidence.verify_full_eigenlattice import (
        specht_jordan_multiplicities,
    )


def determinant_prime_exponents(r):
    """Prime valuations of det ker_Z W_{r-1,r}(2r+1)."""
    exponents = {}
    v = 2 * r + 1
    for i in range(r):
        multiplicity = comb(v, i) - (comb(v, i - 1) if i else 0)
        for prime, exponent in factorint(r + 2 - i).items():
            exponents[int(prime)] = (
                exponents.get(int(prime), 0)
                + int(exponent) * multiplicity
            )
        for prime, exponent in factorint(r - i).items():
            exponents[int(prime)] = (
                exponents.get(int(prime), 0)
                - int(exponent) * multiplicity
            )
    return {
        prime: exponent
        for prime, exponent in sorted(exponents.items())
        if exponent
    }


def explicit_embedding():
    """Return a basis matrix for a primitive b*A_16 in Z^68."""
    coefficients = (2495, 1883, 80, 2811)
    assert gcd(gcd(coefficients[0], coefficients[1]),
               gcd(coefficients[2], coefficients[3])) == 1
    b = sum(value * value for value in coefficients)
    assert b == 17_678_835

    # Standard basis e_i-e_16 of A_16, repeated in four coordinate
    # blocks and scaled by the four-square coefficients.
    rows = []
    for i in range(16):
        row = []
        for coefficient in coefficients:
            row.extend(
                coefficient * (int(j == i) - int(j == 16))
                for j in range(17)
            )
        rows.append(row)

    embedding = Matrix(rows)
    gram = embedding * embedding.T
    target = b * (Matrix.eye(16) + Matrix.ones(16))
    assert gram == target
    assert int(gram.det()) == 17 * b**16

    # All invariant factors are one, exactly certifying that the row
    # lattice is primitive in Z^68.
    smith = smith_normal_form(embedding, domain=ZZ)
    diagonal = [
        abs(int(smith[i, i]))
        for i in range(min(smith.rows, smith.cols))
        if smith[i, i]
    ]
    assert diagonal == [1] * 16
    return coefficients, diagonal


def target_mod2_form():
    """Check that odd-scaled A_16 is the split even unimodular form."""
    zero_count = 0
    one_count = 0
    for word in range(1 << 16):
        weight = bin(word).count("1")
        # In the basis e_i-e_16, the squared norm of a 0/1
        # coefficient lift is weight + weight^2.
        quadratic = ((weight + weight * weight) // 2) & 1
        if quadratic:
            one_count += 1
        else:
            zero_count += 1
    # In dimension 16, 2^15 + 2^7 zeros is Arf invariant zero.
    assert (zero_count, one_count) == (32_896, 32_640)
    return zero_count, one_count


def main():
    total = comb(31, 15)
    b = total // 17
    rank = comb(31, 15) - comb(31, 14)
    assert total == 300_540_195
    assert b == 17_678_835
    assert rank == 35_357_670 == 2 * b
    assert dict(factorint(b)) == {
        3: 2,
        5: 1,
        19: 1,
        23: 1,
        29: 1,
        31: 1,
    }
    assert b % 17 == 8

    determinant = determinant_prime_exponents(15)
    assert determinant == {
        2: 45_703_018,
        3: 40_050_449,
        5: 34_011_401,
        7: 18_936_940,
        11: 539_400,
        13: 26_536,
        17: 1,
    }

    jordan = {
        prime: specht_jordan_multiplicities(31, 15, prime)
        for prime in (2, 3, 5, 7, 11, 13, 17)
    }
    assert jordan == {
        2: {0: 32_768, 1: 24_946_816, 2: 10_378_056, 3: 30},
        3: {0: 1, 1: 30_664_889, 2: 4_692_780},
        5: {0: 1_346_269, 1: 34_011_401},
        7: {0: 16_420_730, 1: 18_936_940},
        11: {0: 34_818_270, 1: 539_400},
        13: {0: 35_331_134, 1: 26_536},
        17: {0: 35_357_669, 1: 1},
    }

    # Required local capacities.
    assert jordan[2][0] >= 16
    assert jordan[3][2] >= 16
    assert jordan[5][1] >= 16
    assert all(jordan[p][0] >= 16 for p in (7, 11, 13))
    assert jordan[17][0] >= 15 and jordan[17][1] == 1

    # Discriminant coefficients modulo squares at p=17.
    ambient_17 = 2 % 17
    target_17 = (-pow(b, -1, 17)) % 17
    assert ambient_17 == target_17 == 2

    coefficients, smith = explicit_embedding()
    mod2_counts = target_mod2_form()

    print("b factorization:", dict(factorint(b)))
    print("rank L:", rank)
    print("det L prime exponents:", determinant)
    print("p-adic Jordan ranks:", jordan)
    print("17-primary coefficient: ambient = target = 2/17")
    print("four-square countermodel coefficients:", coefficients)
    print("embedding Smith factors:", smith)
    print("target mod-2 q counts (zero, one):", mod2_counts)
    print("primitive lattice embedding audit: PASS")


if __name__ == "__main__":
    main()

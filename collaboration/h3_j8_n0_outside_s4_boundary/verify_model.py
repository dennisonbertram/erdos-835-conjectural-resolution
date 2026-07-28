#!/usr/bin/env python3
"""Dependency-free audit of the one-fixed-exterior/S4 N=0 model."""

from __future__ import annotations

import itertools
import math


V = tuple(range(13))
CUBE = tuple(range(8))
FIXED = (8,)
SYMMETRIC = tuple(range(9, 13))
PAIRS = ((0, 1), (2, 3), (4, 5), (6, 7))
RECURRENCE = {
    5: (2, 1, 13),
    6: (3, -1, 39),
    7: (4, 1, 195),
    8: (5, -1, 325),
    9: (6, 1, 702),
    10: (7, -1, 546),
    11: (8, 1, 858),
}


def orbit_key(block):
    return (
        tuple(x for x in block if x in CUBE),
        tuple(x for x in block if x in FIXED),
        sum(x in SYMMETRIC for x in block),
    )


def representatives(size):
    result = []
    for fixed_count in range(2):
        fixed_part = FIXED[:fixed_count]
        for symmetric_count in range(5):
            cube_count = size - fixed_count - symmetric_count
            if 0 <= cube_count <= 8:
                symmetric_part = SYMMETRIC[:symmetric_count]
                for cube_part in itertools.combinations(CUBE, cube_count):
                    result.append(
                        tuple(
                            sorted(
                                (*cube_part, *fixed_part, *symmetric_part)
                            )
                        )
                    )
    return tuple(result)


def canonical_subset(subset):
    cube_part = tuple(x for x in subset if x in CUBE)
    fixed_part = tuple(x for x in subset if x in FIXED)
    symmetric_count = sum(x in SYMMETRIC for x in subset)
    return tuple(
        sorted((*cube_part, *fixed_part, *SYMMETRIC[:symmetric_count]))
    )


def sparse_subset_row(subset, key_index):
    row = {}
    for block in itertools.combinations(subset, 4):
        column = key_index[orbit_key(block)]
        row[column] = row.get(column, 0) + 1
    return row


def sparse_load_row(triple, key_index):
    row = {}
    triple_set = set(triple)
    for block in itertools.combinations(V, 4):
        if triple_set.issubset(block):
            column = key_index[orbit_key(block)]
            row[column] = row.get(column, 0) + 1
    return row


def rank_mod_prime(rows, prime):
    pivots = {}
    for original in rows:
        row = {
            column: coefficient % prime
            for column, coefficient in original.items()
            if coefficient % prime
        }
        while row:
            pivot = min(row)
            if pivot in pivots:
                multiplier = row[pivot]
                for column, coefficient in pivots[pivot].items():
                    value = (
                        row.get(column, 0) - multiplier * coefficient
                    ) % prime
                    if value:
                        row[column] = value
                    else:
                        row.pop(column, None)
            else:
                inverse = pow(row[pivot], -1, prime)
                pivots[pivot] = {
                    column: coefficient * inverse % prime
                    for column, coefficient in row.items()
                }
                break
    return len(pivots)


def augmented(rows, rhs_values, rhs_column):
    result = []
    for row, rhs in zip(rows, rhs_values):
        new_row = dict(row)
        if rhs:
            new_row[rhs_column] = rhs
        result.append(new_row)
    return result


def audit_orbits():
    permutations = tuple(
        dict(zip(SYMMETRIC, permuted))
        for permuted in itertools.permutations(SYMMETRIC)
    )
    blocks = tuple(itertools.combinations(V, 4))
    keys = tuple(sorted({orbit_key(block) for block in blocks}))
    assert len(blocks) == 715
    assert len(keys) == 256

    for key in keys:
        members = {block for block in blocks if orbit_key(block) == key}
        cube_part, fixed_part, symmetric_count = key
        canonical = tuple(
            sorted(
                (
                    *cube_part,
                    *fixed_part,
                    *SYMMETRIC[:symmetric_count],
                )
            )
        )
        generated = {
            tuple(sorted(permutation.get(x, x) for x in canonical))
            for permutation in permutations
        }
        assert generated == members
        assert len(members) == math.comb(4, symmetric_count)
    return keys


def audit_constraint_orbits(keys):
    key_index = {key: index for index, key in enumerate(keys)}
    expected = {
        3: 130,
        5: 381,
        6: 456,
        7: 456,
        8: 381,
        9: 256,
        10: 130,
        11: 46,
    }
    for size, count in expected.items():
        reps = representatives(size)
        assert len(reps) == count
        if size == 3:
            signatures = {
                rep: sparse_load_row(rep, key_index) for rep in reps
            }
            for subset in itertools.combinations(V, size):
                assert (
                    sparse_load_row(subset, key_index)
                    == signatures[canonical_subset(subset)]
                )
        else:
            signatures = {
                rep: sparse_subset_row(rep, key_index) for rep in reps
            }
            for subset in itertools.combinations(V, size):
                assert (
                    sparse_subset_row(subset, key_index)
                    == signatures[canonical_subset(subset)]
                )
    assert sum(expected[size] for size in range(5, 12)) == 2106
    return key_index


def audit_recurrence_equations():
    constants = {
        5: 4,
        6: 18,
        7: 40,
        8: 79,
        9: 96,
        10: 108,
        11: 66,
    }
    for size, (modulus, sign, rhs) in RECURRENCE.items():
        parity_sign = (-1) ** size
        assert sign == -parity_sign
        assert (
            modulus * constants[size]
            - parity_sign * math.comb(size, 4)
            == rhs
        )


def audit_rank_reductions(key_index):
    rows = {
        size: [
            sparse_subset_row(subset, key_index)
            for subset in representatives(size)
        ]
        for size in (5, 6, 8, 9, 10)
    }
    expected_ranks = {5: (2, 163), 6: (3, 135), 8: (5, 126), 10: (7, 84)}
    for size, (prime, expected_rank) in expected_ranks.items():
        assert rank_mod_prime(rows[size], prime) == expected_rank

    rhs_column = len(key_index)
    size5_affine = augmented(
        rows[5],
        [1] * len(rows[5]),
        rhs_column,
    )
    size9_mod2 = augmented(
        rows[9],
        [0] * len(rows[9]),
        rhs_column,
    )
    assert rank_mod_prime(size5_affine, 2) == 163
    assert rank_mod_prime((*size5_affine, *size9_mod2), 2) == 163

    size6_homogeneous = augmented(
        rows[6],
        [0] * len(rows[6]),
        rhs_column,
    )
    size9_mod3 = augmented(
        rows[9],
        [0] * len(rows[9]),
        rhs_column,
    )
    assert rank_mod_prime(size6_homogeneous, 3) == 135
    assert (
        rank_mod_prime((*size6_homogeneous, *size9_mod3), 3)
        == 135
    )


def transform_bits(bits, permutation, translation):
    moved = frozenset(permutation[index] for index in bits)
    return moved.symmetric_difference(translation)


def audit_cube_symmetry_and_partition():
    coordinates = tuple(range(4))
    even_translations = tuple(
        frozenset(bits)
        for size in (0, 2, 4)
        for bits in itertools.combinations(coordinates, size)
    )
    group = tuple(
        (permutation, translation)
        for permutation in itertools.permutations(coordinates)
        for translation in even_translations
    )
    positive = {
        frozenset(bits)
        for size in (0, 2, 4)
        for bits in itertools.combinations(coordinates, size)
    }
    reference_positive = frozenset()
    assert len(group) == 192
    assert {
        transform_bits(reference_positive, *element) for element in group
    } == positive

    positive_stabilizer = tuple(
        element
        for element in group
        if transform_bits(reference_positive, *element)
        == reference_positive
    )
    weight_two = {
        frozenset(bits) for bits in itertools.combinations(coordinates, 2)
    }
    reference_weight_two = frozenset((2, 3))
    assert len(positive_stabilizer) == 24
    assert {
        transform_bits(reference_weight_two, *element)
        for element in positive_stabilizer
    } == weight_two

    double_stabilizer = tuple(
        element
        for element in positive_stabilizer
        if transform_bits(reference_weight_two, *element)
        == reference_weight_two
    )
    crossing = {
        bits
        for bits in weight_two
        if len(bits & reference_weight_two) == 1
    }
    reference_crossing = frozenset((1, 3))
    assert len(double_stabilizer) == 4
    assert {
        transform_bits(reference_crossing, *element)
        for element in double_stabilizer
    } == crossing

    possible_weight_two_maxima = {}
    for maximum in range(8, 14):
        lower = math.ceil((60 - 2 * maximum) / 6)
        possible_weight_two_maxima[maximum] = tuple(
            range(lower, maximum + 1)
        )
    assert possible_weight_two_maxima == {
        8: (8,),
        9: (7, 8, 9),
        10: (7, 8, 9, 10),
        11: (7, 8, 9, 10, 11),
        12: (6, 7, 8, 9, 10, 11, 12),
        13: (6, 7, 8, 9, 10, 11, 12, 13),
    }


def audit_reduced_model_totals():
    count_variables = 163 + 135 + 456 + 126 + 84 + 46
    assert 256 + count_variables == 1266
    recurrence_rows = 381 + 135 + 456 + 126 + 84 + 46
    assert recurrence_rows == 1228
    base_rows = 130 + recurrence_rows + 2
    assert base_rows == 1360
    breaker_rows = 7 + 5 + 3
    assert base_rows + breaker_rows == 1375
    assert base_rows + breaker_rows + 1 == 1376
    assert base_rows + breaker_rows + 2 == 1377


def main():
    keys = audit_orbits()
    print("715 four-sets -> 256 one-fixed-exterior/S4 orbits: PASS")
    key_index = audit_constraint_orbits(keys)
    print("130 load rows and 2,106 full recurrence rows: PASS")
    audit_recurrence_equations()
    print("raw-d recurrence equations for sizes 5..11: PASS")
    audit_rank_reductions(key_index)
    print("F2/F3/F5/F7 ranks and size-9 redundancy: PASS")
    audit_cube_symmetry_and_partition()
    print("cube breakers and complete (m,w) branch partition: PASS")
    audit_reduced_model_totals()
    print("reduced model totals (1,266 variables; 1,360 base rows): PASS")
    print("scope: model semantics only; no infeasibility is certified here")


if __name__ == "__main__":
    main()

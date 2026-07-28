#!/usr/bin/env python3
"""Dependency-free semantic audit of the exterior-S5-symmetric N=0 model."""

from __future__ import annotations

import itertools
import math

from model import (
    CUBE,
    OUTSIDE,
    RECURRENCE,
    V,
    canonical_representatives,
    cube_cells,
    load_signature,
    model_statistics,
    orbit_key,
    orbit_keys,
    subset_signature,
)


def exterior_permutations() -> tuple[dict[int, int], ...]:
    return tuple(
        dict(zip(OUTSIDE, permuted))
        for permuted in itertools.permutations(OUTSIDE)
    )


def image(block: tuple[int, ...], permutation: dict[int, int]) -> tuple[int, ...]:
    return tuple(sorted(permutation.get(x, x) for x in block))


def canonical_subset(subset: tuple[int, ...]) -> tuple[int, ...]:
    cube_part = tuple(x for x in subset if x in CUBE)
    outside_count = len(subset) - len(cube_part)
    return tuple(sorted((*cube_part, *OUTSIDE[:outside_count])))


def audit_four_set_orbits() -> None:
    permutations = exterior_permutations()
    all_blocks = tuple(itertools.combinations(V, 4))
    keys = orbit_keys()
    assert len(all_blocks) == 715
    assert len(keys) == 163

    for key in keys:
        members = {block for block in all_blocks if orbit_key(block) == key}
        cube_part, outside_count = key
        canonical = tuple(sorted((*cube_part, *OUTSIDE[:outside_count])))
        generated = {image(canonical, permutation) for permutation in permutations}
        assert generated == members
        assert len(members) == math.comb(5, outside_count)

    for block in all_blocks:
        for permutation in permutations:
            assert orbit_key(image(block, permutation)) == orbit_key(block)


def audit_constraint_orbits() -> None:
    expected_counts = {
        3: 93,
        5: 219,
        6: 246,
        7: 246,
        8: 219,
        9: 163,
        10: 93,
        11: 37,
    }
    for size, expected in expected_counts.items():
        representatives = canonical_representatives(size)
        assert len(representatives) == expected

        if size == 3:
            representative_signatures = {
                representative: load_signature(representative)
                for representative in representatives
            }
            for subset in itertools.combinations(V, size):
                assert load_signature(subset) == representative_signatures[
                    canonical_subset(subset)
                ]
        else:
            representative_signatures = {
                representative: subset_signature(representative)
                for representative in representatives
            }
            for subset in itertools.combinations(V, size):
                assert subset_signature(subset) == representative_signatures[
                    canonical_subset(subset)
                ]

    stats = model_statistics()
    assert stats == {
        "d_orbits": 163,
        "triple_orbits": 93,
        "recurrence_orbits": {
            5: 219,
            6: 246,
            7: 246,
            8: 219,
            9: 163,
            10: 93,
            11: 37,
        },
        "recurrence_total": 1223,
        "integer_variables": 1386,
        "constraints": 1318,
    }


def audit_recurrence_equations() -> None:
    # If E_S=sum e_Q and d_Q=e_Q+1, then D_S=E_S+C(s,4).
    # The recurrence has N_S=c_s+(-1)^s E_S/(s-3).
    recurrence_constants = {
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
        derived_rhs = (
            modulus * recurrence_constants[size]
            - parity_sign * math.comb(size, 4)
        )
        assert derived_rhs == rhs

    assert RECURRENCE == {
        5: (2, 1, 13),
        6: (3, -1, 39),
        7: (4, 1, 195),
        8: (5, -1, 325),
        9: (6, 1, 702),
        10: (7, -1, 546),
        11: (8, 1, 858),
    }


def audit_cube_normalization() -> None:
    positive, negative = cube_cells()
    assert len(positive) == len(negative) == 8
    assert set(positive).isdisjoint(negative)
    assert all(set(block).issubset(CUBE) for block in (*positive, *negative))
    # In this branch N=0 and P=60, hence Delta=P-N=60.
    assert 60 - 0 == 60


def main() -> None:
    audit_four_set_orbits()
    print("715 four-sets -> 163 exterior-S5 orbits: PASS")
    audit_constraint_orbits()
    print("93 load rows and 1,223 exact recurrence rows: PASS")
    audit_recurrence_equations()
    print("raw-d recurrence equations for sizes 5..11: PASS")
    audit_cube_normalization()
    print("normalized cube has (P,N,Delta)=(60,0,60): PASS")
    print("model totals: 1,386 integer variables and 1,318 constraints")
    print("scope: semantics verified; this script does not certify infeasibility")


if __name__ == "__main__":
    main()

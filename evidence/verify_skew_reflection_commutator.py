#!/usr/bin/env python3
"""Exact verifier for the skew reflection-commutator attack.

The exhaustive r=5 ranks are computed over F_7, the field with
characteristic r+2.  A full modular rank proves nonsingularity over Q.
The script also records the complete binary-nullity census.  Typical
runtime is about 20 seconds.
"""

from collections import Counter
from itertools import combinations
from math import isqrt

import numpy as np

from verify_cross_gram_signature import (
    boundary_gram,
    exact_cover_family,
    rank_mod,
    t_sign,
)


def prepare_mate(base, mate, v, r):
    selected = []
    selected_sign = []
    block_to_sphere = {}
    for sphere, base_block in enumerate(base):
        block = next(
            block for block in mate if set(block).isdisjoint(base_block)
        )
        selected.append(block)
        selected_sign.append(t_sign(block, base_block, v))
        block_to_sphere[block] = sphere
    facet_map = {
        block[:i] + block[i + 1 :]: (block, i)
        for block in mate
        for i in range(r)
    }
    return {
        "selected": selected,
        "selected_sign": selected_sign,
        "block_to_sphere": block_to_sphere,
        "blocks": set(mate),
        "facet_map": facet_map,
    }


def fast_k0(base, left, right, v, r):
    """Build K0=Z^T-Z in coordinates indexed by active A-spheres."""
    active = [
        sphere
        for sphere in range(len(base))
        if left["selected"][sphere] != right["selected"][sphere]
    ]
    active_position = {sphere: i for i, sphere in enumerate(active)}
    all_points = set(range(v))

    # Invert the signed direct matching B0 -> C0, retaining the
    # fixed-A sphere index of each C0 block.
    direct_inverse = {}
    for left_position, sphere in enumerate(active):
        block = left["selected"][sphere]
        complement = all_points - set(block)
        target = next(
            tuple(sorted(complement - {x}))
            for x in complement
            if tuple(sorted(complement - {x})) in right["blocks"]
        )
        target_sphere = right["block_to_sphere"][target]
        assert target_sphere in active_position
        direct_inverse[target_sphere] = (
            left_position,
            t_sign(block, target, v),
        )

    zmat = np.zeros((len(active), len(active)), dtype=np.int64)
    for row, sphere in enumerate(active):
        base_block = base[sphere]
        for removed_position in range(r):
            facet = (
                base_block[:removed_position]
                + base_block[removed_position + 1 :]
            )
            target, added_position = right["facet_map"][facet]
            target_sphere = right["block_to_sphere"][target]
            if target_sphere not in active_position:
                continue
            column, direct_sign = direct_inverse[target_sphere]
            gram_sign = (-1) ** (removed_position + added_position)
            zmat[row, column] += (
                left["selected_sign"][sphere]
                * gram_sign
                * direct_sign
            )
    return active, zmat.T - zmat


def dense_k0(base, left_mate, right_mate, v, r):
    """Definition (2.2), used to cross-check the fast construction."""
    shared = set(left_mate) & set(right_mate)
    b0 = sorted(set(left_mate) - shared)
    c0 = sorted(set(right_mate) - shared)
    a0 = sorted(
        next(block for block in base if set(block).isdisjoint(source))
        for source in b0
    )
    xmat = np.array(
        [[t_sign(source, block, v) for block in a0] for source in b0],
        dtype=np.int64,
    )
    pmat = np.array(
        [[t_sign(source, block, v) for block in c0] for source in b0],
        dtype=np.int64,
    )
    gram = np.array(
        [[boundary_gram(a, c) for c in c0] for a in a0],
        dtype=np.int64,
    )
    zmat = xmat @ gram @ pmat.T
    return zmat.T - zmat


def verify_boundary_factorization(base, left_mate, right_mate, v, r):
    """Check (2.4)--(2.7) directly on one deterministic pair."""
    shared = set(left_mate) & set(right_mate)
    b0 = sorted(set(left_mate) - shared)
    c0 = sorted(set(right_mate) - shared)
    a0 = sorted(
        next(block for block in base if set(block).isdisjoint(source))
        for source in b0
    )
    facets = list(combinations(range(v), r - 1))
    facet_index = {facet: i for i, facet in enumerate(facets)}

    xmat = np.array(
        [[t_sign(source, block, v) for block in a0] for source in b0],
        dtype=np.int64,
    )
    pmat = np.array(
        [[t_sign(source, block, v) for block in c0] for source in b0],
        dtype=np.int64,
    )

    d_a = np.zeros((len(b0), len(facets)), dtype=np.int64)
    d_t = np.zeros_like(d_a)
    paired_a = []
    paired_t = []
    for row in range(len(b0)):
        a_column = next(column for column in range(len(a0)) if xmat[row, column])
        t_column = next(column for column in range(len(c0)) if pmat[row, column])
        a = a0[a_column]
        target = c0[t_column]
        paired_a.append(a)
        paired_t.append(target)
        for position in range(r):
            d_a[
                row, facet_index[a[:position] + a[position + 1 :]]
            ] = xmat[row, a_column] * (-1) ** position
            d_t[
                row,
                facet_index[target[:position] + target[position + 1 :]],
            ] = pmat[row, t_column] * (-1) ** position

    zmat = d_a @ d_t.T
    k0 = zmat.T - zmat
    assert np.array_equal(
        k0, (d_t - d_a) @ (d_t + d_a).T
    )
    emat = (d_t + d_a) % 2
    assert np.array_equal(k0 % 2, (emat @ emat.T) % 2)

    for row, (a, target) in enumerate(zip(paired_a, paired_t)):
        removed = set(a) - set(target)
        added = set(target) - set(a)
        assert len(removed) == len(added) == 1
        t_label = next(iter(removed))
        b_label = next(iter(added))
        for column, other_a in enumerate(paired_a):
            if row == column:
                predicted = True
            else:
                predicted = (
                    len(set(a) & set(other_a)) == r - 2
                    and t_label not in set(other_a)
                    and b_label in set(other_a)
                )
            # Column `row` of Z is paired with target T_row.
            assert (zmat[column, row] != 0) == predicted
    return k0


def bareiss_det(matrix):
    """Fraction-free exact determinant with row pivoting."""
    a = [[int(x) for x in row] for row in matrix.tolist()]
    n = len(a)
    if n == 0:
        return 1
    previous = 1
    sign = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot_row = next(
                (i for i in range(k + 1, n) if a[i][k] != 0), None
            )
            if pivot_row is None:
                return 0
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
        previous = pivot
        for i in range(k + 1, n):
            a[i][k] = 0
    return sign * a[n - 1][n - 1]


def verify_r1():
    base, mates = exact_cover_family(3, 1)
    assert len(mates) == 2
    prepared = [prepare_mate(base, mate, 3, 1) for mate in mates]
    active, k0 = fast_k0(base, prepared[0], prepared[1], 3, 1)
    assert len(active) == 1
    assert k0.tolist() == [[0]]
    print("[r=1] t=1, rank(K0)=0, nullity=1")


def verify_r3():
    base, mates = exact_cover_family(7, 3)
    prepared = [prepare_mate(base, mate, 7, 3) for mate in mates]
    assert len(mates) == 8
    result = Counter()
    support_lines = 0
    for i, j in combinations(range(8), 2):
        active, k0 = fast_k0(base, prepared[i], prepared[j], 7, 3)
        assert np.array_equal(
            k0, dense_k0(base, mates[i], mates[j], 7, 3)
        ) or rank_mod(k0, 5) == rank_mod(
            dense_k0(base, mates[i], mates[j], 7, 3), 5
        )
        rank = rank_mod(k0, 5)
        result[(len(active), rank, len(active) - rank)] += 1

        shared_block = next(iter(set(mates[i]) & set(mates[j])))
        shared_sphere = next(
            block for block in base if set(block).isdisjoint(shared_block)
        )
        leftover = next(
            iter(set(range(7)) - set(shared_block) - set(shared_sphere))
        )
        coordinate_blocks = [prepared[i]["selected"][sphere] for sphere in active]
        contains = [
            q for q, block in enumerate(coordinate_blocks) if leftover in block
        ]
        avoids = [
            q for q, block in enumerate(coordinate_blocks) if leftover not in block
        ]
        assert len(contains) == len(avoids) == 3
        assert rank_mod(k0[:, contains], 5) == 2
        assert rank_mod(k0[:, avoids], 5) == 2
        support_lines += 1

    assert result == Counter({(6, 4, 2): 28})
    assert support_lines == 28
    print(
        "[r=3] 28/28: t=6, rank=4, nullity=2; "
        "kernel=one line on x-star plus one line on its complement"
    )


def verify_r5():
    base, mates = exact_cover_family(11, 5)
    prepared = [prepare_mate(base, mate, 11, 5) for mate in mates]
    assert len(mates) == 144
    result = Counter()
    binary_result = Counter()
    representatives = {}

    for i, j in combinations(range(144), 2):
        active, k0 = fast_k0(base, prepared[i], prepared[j], 11, 5)
        rank = rank_mod(k0, 7)
        binary_rank = rank_mod(k0, 2)
        intersection = 66 - len(active)
        result[(intersection, len(active), rank, len(active) - rank)] += 1
        binary_result[
            (intersection, len(active) - binary_rank)
        ] += 1
        if (i, j) in ((0, 4), (0, 1)):
            representatives[(i, j)] = k0

    expected = Counter({
        (6, 60, 60, 0): 6336,
        (18, 48, 48, 0): 3960,
    })
    assert result == expected, result
    expected_binary = Counter({
        (18, 2): 3960,
        (6, 0): 4750,
        (6, 2): 792,
        (6, 4): 794,
    })
    assert binary_result == expected_binary, binary_result

    expected_determinants = {
        (0, 4): 6_997_155_201,
        (0, 1): 864_900,
    }
    pfaffian_magnitudes = {}
    for pair, expected_det in expected_determinants.items():
        dense = verify_boundary_factorization(
            base, mates[pair[0]], mates[pair[1]], 11, 5
        )
        assert abs(bareiss_det(dense)) == expected_det
        determinant = bareiss_det(representatives[pair])
        assert abs(determinant) == expected_det
        root = isqrt(abs(determinant))
        assert root * root == abs(determinant)
        pfaffian_magnitudes[pair] = root

    print(f"[r=5 exact mod 7=r+2] {dict(result)}")
    print(f"[r=5 exact binary nullities] {dict(binary_result)}")
    print(
        "[r=5 exact representative |Pfaffian|] "
        f"(0,4): {pfaffian_magnitudes[(0, 4)]}; "
        f"(0,1): {pfaffian_magnitudes[(0, 1)]}"
    )


def main():
    verify_r1()
    verify_r3()
    verify_r5()
    print("RESULT: ALL CHECKS PASSED")


if __name__ == "__main__":
    main()

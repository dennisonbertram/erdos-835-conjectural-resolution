#!/usr/bin/env python3
"""Explore the point-deleted complement pairing on simplicial cycle spaces.

This is an exact small-parameter diagnostic for the parity/topology route in
Erdos--Rosenfeld #835.  Over F_2, C_{r-1} has the r-subsets of [2r+1] as its
basis, and ``boundary`` is the unsigned simplicial boundary.  For a fixed point
x, K_x pairs complementary r-subsets of [2r+1] \ {x}.  We compute the rank of
the bilinear form z^T K_x w after restricting it to ker(boundary).
"""

from itertools import combinations
from math import comb
import sys


def parity(value):
    return bin(value).count("1") & 1


def row_reduce(rows):
    """Return a reduced independent row basis, keyed by pivot position."""
    pivots = {}
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    # Echelon rows use their highest set bit as pivot.  Eliminate the lower
    # pivots from all higher-pivot rows in increasing-pivot order.
    for pivot in sorted(pivots):
        row = pivots[pivot]
        for old_pivot in sorted(pivots):
            if old_pivot > pivot and ((pivots[old_pivot] >> pivot) & 1):
                pivots[old_pivot] ^= row
    return pivots


def nullspace_basis(rows, ncols):
    pivots = row_reduce(rows)
    pivot_cols = set(pivots)
    free_cols = [column for column in range(ncols) if column not in pivot_cols]
    basis = []
    for free in free_cols:
        vector = 1 << free
        for pivot, row in pivots.items():
            if (row >> free) & 1:
                vector |= 1 << pivot
        basis.append(vector)
    for row in rows:
        for vector in basis:
            assert parity(row & vector) == 0
    return basis, len(pivots)


def restricted_gram_rank(r):
    v = 2 * r + 1
    blocks = list(combinations(range(v), r))
    index = {block: i for i, block in enumerate(blocks)}
    faces = list(combinations(range(v), r - 1))
    boundary_rows = []
    for face in faces:
        face_set = set(face)
        row = 0
        for point in range(v):
            if point not in face_set:
                row |= 1 << index[tuple(sorted(face + (point,)))]
        boundary_rows.append(row)

    kernel, boundary_rank = nullspace_basis(boundary_rows, len(blocks))

    x = v - 1
    universe_without_x = set(range(v - 1))
    complement_index = [-1] * len(blocks)
    for i, block in enumerate(blocks):
        if x not in block:
            complement = tuple(sorted(universe_without_x.difference(block)))
            complement_index[i] = index[complement]

    def apply_k(vector):
        result = 0
        for i, target in enumerate(complement_index):
            if target >= 0 and ((vector >> target) & 1):
                result |= 1 << i
        return result

    transformed = [apply_k(vector) for vector in kernel]

    def gram_rank(images):
        gram_rows = []
        for left in kernel:
            row = 0
            for j, right_image in enumerate(images):
                if parity(left & right_image):
                    row |= 1 << j
            gram_rows.append(row)
        return len(row_reduce(gram_rows))

    point_gram_rank = gram_rank(transformed)

    total_images = []
    for vector in kernel:
        image = 0
        for deleted_point in range(v):
            complement_map = [-1] * len(blocks)
            universe = set(range(v))
            universe.remove(deleted_point)
            for i, block in enumerate(blocks):
                if deleted_point not in block:
                    complement_map[i] = index[
                        tuple(sorted(universe.difference(block)))
                    ]
            for i, target in enumerate(complement_map):
                if target >= 0 and ((vector >> target) & 1):
                    image ^= 1 << i
        total_images.append(image)
    total_gram_rank = gram_rank(total_images)
    total_action_is_identity = all(
        image == vector for image, vector in zip(total_images, kernel)
    )

    quadratic_values = []
    for vector in kernel:
        q = 0
        seen = set()
        for i, target in enumerate(complement_index):
            if target >= 0 and i not in seen:
                seen.add(i)
                seen.add(target)
                q ^= ((vector >> i) & 1) & ((vector >> target) & 1)
        quadratic_values.append(q)

    return {
        "r": r,
        "v": v,
        "columns": len(blocks),
        "boundary_rows": len(faces),
        "boundary_rank": boundary_rank,
        "kernel_dimension": len(kernel),
        "point_gram_rank": point_gram_rank,
        "total_gram_rank": total_gram_rank,
        "total_action_is_identity": total_action_is_identity,
        "basis_q_weight": sum(quadratic_values),
    }


def algebraic_mate_shell_r3():
    """Exhaust the linear/quadratic necessary conditions at r=3."""
    r = 3
    v = 7
    blocks = list(combinations(range(v), r))
    index = {block: i for i, block in enumerate(blocks)}
    rows = []
    for face in combinations(range(v), r - 1):
        face_set = set(face)
        row = 0
        for point in range(v):
            if point not in face_set:
                row |= 1 << index[tuple(sorted(face + (point,)))]
        rows.append(row)
    for block in blocks:
        block_set = set(block)
        row = 1 << index[block]
        for other in blocks:
            if block_set.isdisjoint(other):
                row |= 1 << index[other]
        rows.append(row)
    eigenspace, rank = nullspace_basis(rows, len(blocks))

    complement_pairs = []
    for x in range(v):
        universe = set(range(v))
        universe.remove(x)
        pairs = []
        seen = set()
        for block in blocks:
            if x in block:
                continue
            other = tuple(sorted(universe.difference(block)))
            i, j = index[block], index[other]
            if i not in seen:
                seen.add(i)
                seen.add(j)
                pairs.append((i, j))
        complement_pairs.append(pairs)

    def q_x(vector, x):
        value = 0
        for i, j in complement_pairs[x]:
            value ^= ((vector >> i) & 1) & ((vector >> j) & 1)
        return value

    shell = []
    for mask in range(1 << len(eigenspace)):
        vector = 0
        for i, basis_vector in enumerate(eigenspace):
            if (mask >> i) & 1:
                vector ^= basis_vector
        if all(q_x(vector, x) == 1 for x in range(v)):
            shell.append(vector)
    nonorthogonal_pairs = sum(
        parity(shell[i] & shell[j])
        for i in range(len(shell))
        for j in range(i + 1, len(shell))
    )
    weight_14_shell = [vector for vector in shell if bin(vector).count("1") == 14]
    weight_14_nonorthogonal_pairs = sum(
        parity(weight_14_shell[i] & weight_14_shell[j])
        for i in range(len(weight_14_shell))
        for j in range(i + 1, len(weight_14_shell))
    )

    base_blocks = [
        block for block in blocks
        if (block[0] + 1) ^ (block[1] + 1) ^ (block[2] + 1) == 0
    ]
    base_mask = sum(1 << index[block] for block in base_blocks)
    fixed_base_shell = [
        vector for vector in weight_14_shell
        if (vector & base_mask) == base_mask
    ]
    fixed_base_nonorthogonal_pairs = sum(
        parity(fixed_base_shell[i] & fixed_base_shell[j])
        for i in range(len(fixed_base_shell))
        for j in range(i + 1, len(fixed_base_shell))
    )
    return {
        "eigenspace_rank": rank,
        "eigenspace_dimension": len(eigenspace),
        "quadratic_shell_size": len(shell),
        "shell_nonorthogonal_pairs": nonorthogonal_pairs,
        "weight14_shell_size": len(weight_14_shell),
        "weight14_nonorthogonal_pairs": weight_14_nonorthogonal_pairs,
        "fixed_base_shell_size": len(fixed_base_shell),
        "fixed_base_nonorthogonal_pairs": fixed_base_nonorthogonal_pairs,
    }


def main():
    parameters = [int(value) for value in sys.argv[1:]] or [1, 3, 5]
    for r in parameters:
        result = restricted_gram_rank(r)
        print(" ".join(f"{key}={value}" for key, value in result.items()))
        assert result["columns"] - result["boundary_rank"] == comb(2 * r, r)
    if 3 in parameters:
        result = algebraic_mate_shell_r3()
        print("r3_shell " + " ".join(
            f"{key}={value}" for key, value in result.items()
        ))


if __name__ == "__main__":
    main()

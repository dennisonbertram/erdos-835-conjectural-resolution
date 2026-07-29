#!/usr/bin/env python3
"""Exact checks for the triangle-Pfaffian determinant identity."""

from itertools import combinations, permutations


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    right_t = transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column)) for column in right_t]
        for row in left
    ]


def determinant(matrix):
    """Bareiss fraction-free determinant over the integers."""
    work = [row[:] for row in matrix]
    n = len(work)
    if n == 0:
        return 1
    sign = 1
    denominator = 1
    for pivot_index in range(n - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                (
                    row
                    for row in range(pivot_index + 1, n)
                    if work[row][pivot_index] != 0
                ),
                None,
            )
            if swap is None:
                return 0
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign = -sign
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, n):
            for column in range(pivot_index + 1, n):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % denominator == 0
                work[row][column] = numerator // denominator
        denominator = pivot
        for row in range(pivot_index + 1, n):
            work[row][pivot_index] = 0
    return sign * work[-1][-1]


def signed_permutation(permutation, signs):
    size = len(permutation)
    matrix = [[0] * size for _ in range(size)]
    for column, row in enumerate(permutation):
        matrix[row][column] = signs[column]
    return matrix


def permutation_sign(permutation):
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def block_matrix(blocks):
    row_heights = [len(row[0]) for row in blocks]
    column_widths = [len(blocks[0][column][0]) for column in range(len(blocks[0]))]
    out = []
    for block_row, height in zip(blocks, row_heights):
        for local_row in range(height):
            row = []
            for block, width in zip(block_row, column_widths):
                assert len(block[local_row]) == width
                row.extend(block[local_row])
            out.append(row)
    return out


def scale(matrix, scalar):
    return [[scalar * value for value in row] for row in matrix]


def add(left, right):
    return [
        [a + b for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def identity(size):
    return [[int(row == column) for column in range(size)] for row in range(size)]


def zero(size):
    return [[0] * size for _ in range(size)]


def check_case(permutation, signs):
    size = len(permutation)
    h = signed_permutation(permutation, signs)
    ht = transpose(h)
    eye = identity(size)
    skew = block_matrix(
        [
            [zero(size), eye, eye],
            [scale(eye, -1), zero(size), h],
            [scale(eye, -1), scale(ht, -1), zero(size)],
        ]
    )
    assert transpose(skew) == scale(skew, -1)

    for t in (-3, -1, 0, 1, 2):
        left = determinant(add(identity(3 * size), scale(skew, t)))
        right_matrix = add(
            scale(eye, 1 + 3 * t * t),
            scale(add(h, scale(ht, -1)), -(t ** 3)),
        )
        right = determinant(right_matrix)
        assert left == right
        assert left > 0


def signed_disjoint_entry(left, right, point_count):
    """Coefficient of e_right in i_u(*e_left), with natural orientations."""
    left = tuple(sorted(left))
    complement = tuple(point for point in range(point_count) if point not in left)
    omitted = next(point for point in complement if point not in right)
    hodge_sign = permutation_sign(list(left) + list(complement))
    contraction_sign = -1 if complement.index(omitted) % 2 else 1
    return hodge_sign * contraction_sign


def matching_minor_sign(left_system, right_system, point_count):
    left = sorted(left_system)
    right = sorted(right_system)
    matching = []
    entry_product = 1
    for block in left:
        hits = [
            (index, other)
            for index, other in enumerate(right)
            if set(block).isdisjoint(other)
        ]
        assert len(hits) == 1
        index, other = hits[0]
        matching.append(index)
        entry_product *= signed_disjoint_entry(block, other, point_count)
    return permutation_sign(matching) * entry_product


def all_fano_planes():
    base = [
        block
        for block in combinations(range(7), 3)
        if (block[0] + 1) ^ (block[1] + 1) ^ (block[2] + 1) == 0
    ]
    systems = set()
    for point_permutation in permutations(range(7)):
        systems.add(
            tuple(
                sorted(
                    tuple(sorted(point_permutation[point] for point in block))
                    for block in base
                )
            )
        )
    assert len(systems) == 30
    return sorted(systems)


def check_negative_fano_cycle():
    systems = all_fano_planes()
    cycle = [systems[index] for index in (0, 9, 12, 21)]
    expected = [
        ("012", "034", "056", "135", "146", "236", "245"),
        ("013", "025", "046", "126", "145", "234", "356"),
        ("014", "023", "056", "125", "136", "246", "345"),
        ("015", "024", "036", "126", "134", "235", "456"),
    ]
    rendered = [
        tuple("".join(map(str, block)) for block in system)
        for system in cycle
    ]
    assert rendered == expected

    edge_indices = ((0, 1), (1, 2), (2, 3), (0, 3))
    signs = []
    for left, right in edge_indices:
        assert set(cycle[left]).isdisjoint(cycle[right])
        signs.append(matching_minor_sign(cycle[left], cycle[right], 7))
    assert signs == [1, -1, 1, 1]
    assert signs[0] * signs[1] * signs[2] * signs[3] == -1
    return signs


def main():
    # One odd 5-cycle, a mixture of odd and even cycles, and signed cycles.
    cases = [
        ([1, 2, 3, 4, 0], [1, 1, 1, 1, 1]),
        ([1, 0, 2, 4, 3], [1, 1, 1, 1, 1]),
        ([1, 2, 0, 4, 3], [-1, 1, 1, -1, 1]),
    ]
    for permutation, signs in cases:
        check_case(permutation, signs)
    fano_signs = check_negative_fano_cycle()

    print("triangle Pfaffian/Hodge determinant identity: VERIFIED")
    print("odd and even monodromy cycles both satisfy every tested identity")
    print(f"canonical Fano 4-cycle minor signs: {fano_signs}, product -1")
    print("skew/Pfaffian positivity alone gives no cycle-parity obstruction")


if __name__ == "__main__":
    main()

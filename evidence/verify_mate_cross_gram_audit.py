#!/usr/bin/env python3
"""Exact negative controls for the mate cross-Gram determinant route.

This is deliberately stdlib-only.  It constructs the deterministic Fano and
Witt bases by exact cover, enumerates the mates of that base, and checks the
integer cross-Gram matrices used in mate_cross_gram_determinant_audit.md.
"""

from itertools import combinations


def exact_cover(columns, rows, cap=None):
    """Algorithm X, with deterministic branching."""
    answers, chosen = [], []

    def select(row):
        removed = []
        for column in rows[row]:
            for other in columns[column]:
                for other_column in rows[other]:
                    if other_column != column:
                        columns[other_column].remove(other)
            removed.append(columns.pop(column))
        return removed

    def deselect(row, removed):
        for column in reversed(rows[row]):
            columns[column] = removed.pop()
            for other in columns[column]:
                for other_column in rows[other]:
                    if other_column != column:
                        columns[other_column].add(other)

    def search():
        if cap is not None and len(answers) >= cap:
            return
        if not columns:
            answers.append(tuple(chosen))
            return
        column = min(columns, key=lambda item: len(columns[item]))
        for row in sorted(columns[column]):
            chosen.append(row)
            removed = select(row)
            search()
            deselect(row, removed)
            chosen.pop()
            if cap is not None and len(answers) >= cap:
                return

    search()
    return answers


def bareiss_det(matrix):
    """Fraction-free exact determinant (with row-pivoting)."""
    matrix = [list(row) for row in matrix]
    size = len(matrix)
    if size == 0:
        return 1
    prior, sign = 1, 1
    for pivot_index in range(size - 1):
        if matrix[pivot_index][pivot_index] == 0:
            swap = next(
                (row for row in range(pivot_index + 1, size)
                 if matrix[row][pivot_index]),
                None,
            )
            if swap is None:
                return 0
            matrix[pivot_index], matrix[swap] = (
                matrix[swap], matrix[pivot_index]
            )
            sign = -sign
        pivot = matrix[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    matrix[row][column] * pivot
                    - matrix[row][pivot_index] * matrix[pivot_index][column]
                )
                assert numerator % prior == 0
                matrix[row][column] = numerator // prior
        prior = pivot
        for row in range(pivot_index + 1, size):
            matrix[row][pivot_index] = 0
    return sign * matrix[-1][-1]


def delete_row_column(matrix, index):
    return [
        row[:index] + row[index + 1:]
        for row_index, row in enumerate(matrix)
        if row_index != index
    ]


def build_base_and_mates(n, r):
    blocks = [frozenset(block) for block in combinations(range(n), r)]
    facets = list(combinations(range(n), r - 1))
    columns = {facet: set() for facet in facets}
    rows = {}
    for index, block in enumerate(blocks):
        rows[index] = [facet for facet in facets if frozenset(facet) <= block]
        for facet in rows[index]:
            columns[facet].add(index)

    first = exact_cover({facet: set(items) for facet, items in columns.items()},
                        rows, cap=1)[0]
    base = frozenset(blocks[index] for index in first)
    allowed = {index for index, block in enumerate(blocks) if block not in base}
    mates = [
        frozenset(blocks[index] for index in solution)
        for solution in exact_cover(
            {facet: {index for index in items if index in allowed}
             for facet, items in columns.items()},
            rows,
        )
    ]
    return base, mates


def sphere_ordered_blocks(base, mate, n):
    """Index a mate's blocks by the base sphere that it meets."""
    points = frozenset(range(n))
    ordered_base = sorted(base, key=lambda block: tuple(sorted(block)))
    ordered_mate = []
    for block in ordered_base:
        choices = [other for other in mate if not (block & other)]
        assert len(choices) == 1
        other = choices[0]
        # The unique omitted point is the mate-map value.  This also checks
        # that other is the r-subset of X\block specified by that value.
        assert len(points - block - other) == 1
        ordered_mate.append(other)
    assert len(set(ordered_mate)) == len(ordered_mate)
    return ordered_mate


def cross_gram(left, right, r):
    """Facet-incidence Gram matrix E_left^T E_right."""
    answer = []
    for block in left:
        row = []
        for other in right:
            if block == other:
                row.append(r)
            elif len(block & other) == r - 1:
                row.append(1)
            else:
                row.append(0)
        answer.append(row)
    assert all(sum(row) == r for row in answer)
    assert all(sum(row[column] for row in answer) == r
               for column in range(len(answer)))
    return answer


def laplacian(matrix, r):
    return [
        [(r if row == column else 0) - matrix[row][column]
        for column in range(len(matrix))]
        for row in range(len(matrix))
    ]


def check_r3():
    base, mates = build_base_and_mates(7, 3)
    assert len(base) == 7 and len(mates) == 8
    maps = [sphere_ordered_blocks(base, mate, 7) for mate in mates]
    for left_index in range(len(mates)):
        for right_index in range(left_index + 1, len(mates)):
            assert len(mates[left_index] & mates[right_index]) == 1
            matrix = cross_gram(maps[left_index], maps[right_index], 3)
            # The diagonal has six 1's and one 3: tr=7+2*1=9.
            assert sum(matrix[index][index] for index in range(7)) == 9
            # All 28 pairs have the same nonzero determinant.  Thus even
            # the full integral determinant carries no further distinction
            # of the (already fixed) agreement parity in this control.
            assert bareiss_det(matrix) == 27
            # The natural directed matrix-tree cofactor is zero.
            assert bareiss_det(delete_row_column(laplacian(matrix, 3), 0)) == 0
    print("r=3: 8 mates, 28 pairs; cross-Gram det=27 and tree cofactor=0")


def check_r5():
    base, mates = build_base_and_mates(11, 5)
    assert len(base) == 66 and len(mates) == 144
    maps = [sphere_ordered_blocks(base, mate, 11) for mate in mates]

    # These two pairs are produced by deterministic Algorithm X indexing.
    # Both satisfy the full endpoint Steiner exact-cover constraints.
    dense = cross_gram(maps[0], maps[1], 5)
    sparse = cross_gram(maps[0], maps[4], 5)
    assert len(mates[0] & mates[1]) == 18
    assert len(mates[0] & mates[4]) == 6
    assert sum(dense[index][index] for index in range(66)) == 66 + 4 * 18
    assert sum(sparse[index][index] for index in range(66)) == 66 + 4 * 6

    dense_det = bareiss_det(dense)
    sparse_det = bareiss_det(sparse)
    assert dense_det == 934696197509765625
    assert sparse_det == 0
    assert dense_det % 16 == 9
    assert bareiss_det(delete_row_column(laplacian(dense, 5), 0)) == 0
    assert bareiss_det(delete_row_column(laplacian(sparse, 5), 0)) == 0
    print("r=5: valid pairs i=18 and i=6 have cross-Gram determinants")
    print("      {} and 0 (respectively); both tree cofactors are 0".format(
        dense_det
    ))


def main():
    check_r3()
    check_r5()
    print("mate cross-Gram determinant audit: PASS")


if __name__ == "__main__":
    main()

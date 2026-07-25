#!/usr/bin/env python3
"""Exact checks for ``tits_equality_local_audit.md`` (stdlib only).

The two finite controls are the unique S(3,4,8) and S(5,6,12).  They
are obtained by taking the deterministic S(k-2,k-1,2k-1) returned by
``build_restricted_matrix`` and applying Mendelsohn's unique extension.

The script verifies:

* complementation and all local nonblock bijections;
* the relative permutations on adjacent nonblocks;
* the fixed-block intersection distribution;
* the edge-by-edge matching matrix G_2 and its exact rank;
* the linked symmetric unipotent Latin squares encoded by G_2; and
* the triangle decompositions forced at the next layer G_3.

It also checks all numerical consequences quoted for the open k=16
parameter without assuming that the putative design exists.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb

try:
    from verify_saturated_support_lattice import build_restricted_matrix
except ModuleNotFoundError:
    from evidence.verify_saturated_support_lattice import (
        build_restricted_matrix,
    )


def subsets(points, size):
    return [
        frozenset(choice)
        for choice in combinations(sorted(points), size)
    ]


def extend_boundary_design(k):
    """Return the canonical small S(k-1,k,2k), for k=4 or 6."""
    _, _, boundary, _ = build_restricted_matrix(2 * k - 1, k - 1)
    old_points = set(range(2 * k - 1))
    infinity = 2 * k - 1
    blocks = set()
    for block in boundary:
        blocks.add(frozenset(set(block) | {infinity}))
        blocks.add(frozenset(old_points - set(block)))
    return set(range(2 * k)), frozenset(blocks)


def validate_steiner_system(points, blocks, k):
    assert all(len(block) == k for block in blocks)
    facet_owner = {}
    for block in blocks:
        for facet in combinations(sorted(block), k - 1):
            facet = frozenset(facet)
            assert facet not in facet_owner
            facet_owner[facet] = block
    assert set(facet_owner) == set(subsets(points, k - 1))
    for block in blocks:
        assert frozenset(points - set(block)) in blocks
    return facet_owner


def local_bijections(points, blocks, facet_owner, k):
    """Construct phi_X:X -> X^c for every nonblock X."""
    all_middle = set(subsets(points, k))
    nonblocks = all_middle - set(blocks)
    maps = {}
    for middle in nonblocks:
        image = {}
        for point in middle:
            facet = middle - {point}
            owner = facet_owner[facet]
            added = owner - facet
            assert len(added) == 1
            added_point = next(iter(added))
            assert added_point not in middle
            image[point] = added_point
        assert set(image) == set(middle)
        assert set(image.values()) == points - set(middle)
        maps[middle] = image
    return nonblocks, maps


def cycle_type(permutation):
    seen = set()
    lengths = []
    for start in sorted(permutation):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return tuple(sorted(lengths))


def adjacent_relative_cycle_types(points, nonblocks, maps):
    """Audit the canonical comparison of adjacent local bijections."""
    types = Counter()
    edge_count = 0
    ordered_nonblocks = sorted(
        nonblocks, key=lambda block: tuple(sorted(block))
    )
    order = {
        block: index for index, block in enumerate(ordered_nonblocks)
    }

    for middle in ordered_nonblocks:
        phi = maps[middle]
        phi_inverse = {value: key for key, value in phi.items()}
        for removed in middle:
            for added in points - set(middle):
                if added == phi[removed]:
                    # This swap is the unique block through middle-{removed}.
                    continue
                neighbour = frozenset(
                    (set(middle) - {removed}) | {added}
                )
                assert neighbour in nonblocks
                if order[middle] >= order[neighbour]:
                    continue

                psi = maps[neighbour]
                preimage = phi_inverse[added]
                assert preimage != removed

                # Transport the changed domain point removed -> added and the
                # changed codomain point added -> removed, then compare with
                # phi as a permutation of the original domain.
                relative = {}
                for point in middle:
                    transported_domain = (
                        added if point == removed else point
                    )
                    target = psi[transported_domain]
                    transported_back = added if target == removed else target
                    relative[point] = phi_inverse[transported_back]

                fixed = {
                    point for point, image in relative.items()
                    if point == image
                }
                assert fixed == {removed, preimage}
                types[cycle_type(relative)] += 1
                edge_count += 1

    expected = len(nonblocks) * k_global(nonblocks) * (
        k_global(nonblocks) - 1
    ) // 2
    assert edge_count == expected
    return edge_count, types


def k_global(nonblocks):
    return len(next(iter(nonblocks)))


def intersection_distribution(k):
    """Return a_i=#blocks meeting a fixed block in exactly i points."""
    values = [Fraction(0) for _ in range(k + 1)]
    values[k] = Fraction(1)
    for size in range(k - 1, -1, -1):
        lambda_size = Fraction(
            comb(2 * k - size, k - 1 - size),
            k - size,
        )
        moment = comb(k, size) * lambda_size
        values[size] = moment - sum(
            comb(intersection, size) * values[intersection]
            for intersection in range(size + 1, k + 1)
        )
    assert all(value.denominator == 1 for value in values)
    result = [int(value) for value in values]
    assert result == list(reversed(result))
    return result


def incidence_layers(points, blocks, base, k):
    """Return the matrices G_2 and G_3 relative to base and its complement."""
    complement = frozenset(points - set(base))
    assert complement in blocks
    matrices = {}
    indices = {}
    for size in (2, 3):
        row_sets = subsets(base, size)
        column_sets = subsets(complement, size)
        matrix = [
            [
                int(
                    frozenset(
                        set(row_set)
                        | (set(complement) - set(column_set))
                    )
                    in blocks
                )
                for column_set in column_sets
            ]
            for row_set in row_sets
        ]
        matrices[size] = matrix
        indices[size] = (row_sets, column_sets)
    return complement, matrices, indices


def is_perfect_matching(edges, points):
    degree = Counter()
    for edge in edges:
        assert len(edge) == 2
        for point in edge:
            degree[point] += 1
    return len(edges) == len(points) // 2 and all(
        degree[point] == 1 for point in points
    )


def fraction_rank_and_pivots(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_rows = []
    pivot_columns = []
    active_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(active_row, row_count)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[active_row], work[pivot] = work[pivot], work[active_row]
        pivot_rows.append(pivot)
        pivot_columns.append(column)
        scale = work[active_row][column]
        work[active_row] = [value / scale for value in work[active_row]]
        for row in range(row_count):
            if row == active_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                left - scale * right
                for left, right in zip(work[row], work[active_row])
            ]
        active_row += 1
        if active_row == row_count:
            break
    return len(pivot_columns), tuple(pivot_columns)


def independent_row_indices(matrix):
    transpose = [list(column) for column in zip(*matrix)]
    _, indices = fraction_rank_and_pivots(transpose)
    return indices


def bareiss_determinant(matrix):
    work = [list(map(int, row)) for row in matrix]
    size = len(work)
    assert all(len(row) == size for row in work)
    if size == 0:
        return 1
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot = next(
            (
                row for row in range(column, size)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        for row in range(column + 1, size):
            for other in range(column + 1, size):
                numerator = (
                    work[row][other] * pivot_value
                    - work[row][column] * work[column][other]
                )
                assert numerator % previous == 0
                work[row][other] = numerator // previous
        previous = pivot_value
    return sign * work[-1][-1]


def audit_matching_matrix(base, complement, matrix, row_edges, column_edges):
    k = len(base)
    edge_count = comb(k, 2)
    assert len(matrix) == len(matrix[0]) == edge_count

    row_neighbours = []
    for row in matrix:
        neighbours = [
            column_edges[index]
            for index, value in enumerate(row)
            if value
        ]
        assert is_perfect_matching(neighbours, complement)
        row_neighbours.append(neighbours)

    column_neighbours = []
    for column in range(edge_count):
        neighbours = [
            row_edges[row]
            for row in range(edge_count)
            if matrix[row][column]
        ]
        assert is_perfect_matching(neighbours, base)
        column_neighbours.append(neighbours)

    # The k-1 matchings indexed by the star at a point form a complete
    # one-factorization on the opposite side.
    for point in base:
        factor_rows = [
            index
            for index, edge in enumerate(row_edges)
            if point in edge
        ]
        covered = Counter(
            edge
            for index in factor_rows
            for edge in row_neighbours[index]
        )
        assert set(covered) == set(column_edges)
        assert set(covered.values()) == {1}
    for point in complement:
        factor_columns = [
            index
            for index, edge in enumerate(column_edges)
            if point in edge
        ]
        covered = Counter(
            edge
            for index in factor_columns
            for edge in column_neighbours[index]
        )
        assert set(covered) == set(row_edges)
        assert set(covered.values()) == {1}

    # Directly check R_B G=J and G R_C^T=J.
    for point in base:
        for column in range(edge_count):
            assert sum(
                matrix[row][column]
                for row, edge in enumerate(row_edges)
                if point in edge
            ) == 1
    for row in range(edge_count):
        for point in complement:
            assert sum(
                matrix[row][column]
                for column, edge in enumerate(column_edges)
                if point in edge
            ) == 1

    rank, pivot_columns = fraction_rank_and_pivots(matrix)
    pivot_rows = independent_row_indices(matrix)
    assert len(pivot_rows) == rank
    minor = [
        [matrix[row][column] for column in pivot_columns]
        for row in pivot_rows
    ]
    determinant = bareiss_determinant(minor)
    assert abs(determinant) == 1
    assert rank == comb(k, 2) - k + 1

    overlaps = Counter()
    for left, right in combinations(range(edge_count), 2):
        if row_edges[left].isdisjoint(row_edges[right]):
            overlap = sum(
                a * b for a, b in zip(matrix[left], matrix[right])
            )
            overlaps[overlap] += 1

    total_pairs = 3 * comb(k, 4)
    total_overlap = comb(k, 2) * comb(k // 2, 2)
    assert sum(overlaps.values()) == total_pairs
    assert sum(value * count for value, count in overlaps.items()) == (
        total_overlap
    )
    return rank, determinant, overlaps


def linked_latin_squares(base, complement, matrix, row_edges, column_edges):
    """Build L_b(a,x) from G_2 and verify every linked identity."""
    lookup = {
        (row_edges[row], column_edges[column])
        for row in range(len(row_edges))
        for column in range(len(column_edges))
        if matrix[row][column]
    }
    squares = {}
    for diagonal_symbol in complement:
        square = {}
        for left in base:
            for right in base:
                if left == right:
                    square[left, right] = diagonal_symbol
                    continue
                edge = frozenset({left, right})
                matching_edge = next(
                    column
                    for row, column in lookup
                    if row == edge and diagonal_symbol in column
                )
                square[left, right] = next(
                    point
                    for point in matching_edge
                    if point != diagonal_symbol
                )
        for left in base:
            assert {
                square[left, right] for right in base
            } == set(complement)
        for left in base:
            for right in base:
                assert square[left, right] == square[right, left]
        squares[diagonal_symbol] = square

    for left, right in combinations(sorted(base), 2):
        image = {
            symbol: squares[symbol][left, right]
            for symbol in complement
        }
        assert set(image) == set(complement)
        assert all(image[symbol] != symbol for symbol in complement)
        assert all(image[image[symbol]] == symbol for symbol in complement)
    return squares


def audit_triangle_layer(
    base,
    complement,
    g2,
    g3,
    edge_indices,
    triple_indices,
):
    row_edges, column_edges = edge_indices
    row_triples, column_triples = triple_indices
    row_edge_index = {edge: index for index, edge in enumerate(row_edges)}
    column_edge_index = {
        edge: index for index, edge in enumerate(column_edges)
    }
    row_triple_index = {
        triple: index for index, triple in enumerate(row_triples)
    }
    column_triple_index = {
        triple: index for index, triple in enumerate(column_triples)
    }
    expected_triangles = len(base) * (len(base) - 4) // 6

    def check_columns():
        counts = Counter()
        for triple in column_triples:
            constituent_edges = subsets(triple, 2)
            leave = {
                row_edges[row]
                for row in range(len(row_edges))
                if any(
                    g2[row][column_edge_index[edge]]
                    for edge in constituent_edges
                )
            }
            assert len(leave) == 3 * len(base) // 2
            degree = Counter(
                point for edge in leave for point in edge
            )
            assert all(degree[point] == 3 for point in base)

            selected = [
                row_triple
                for row_triple in row_triples
                if g3[row_triple_index[row_triple]][
                    column_triple_index[triple]
                ]
            ]
            covered = Counter(
                edge
                for row_triple in selected
                for edge in subsets(row_triple, 2)
            )
            expected = set(row_edges) - leave
            assert set(covered) == expected
            assert set(covered.values()) <= {1}
            assert len(selected) == expected_triangles
            counts[len(selected)] += 1
        return counts

    column_counts = check_columns()

    # Repeat after transposing B and C.
    transposed_g2 = [list(column) for column in zip(*g2)]
    transposed_g3 = [list(column) for column in zip(*g3)]
    row_counts = audit_triangle_columns_only(
        complement,
        base,
        transposed_g2,
        transposed_g3,
        column_edges,
        row_edges,
        column_triples,
        row_triples,
    )
    return column_counts, row_counts


def audit_triangle_columns_only(
    base,
    complement,
    g2,
    g3,
    row_edges,
    column_edges,
    row_triples,
    column_triples,
):
    column_edge_index = {
        edge: index for index, edge in enumerate(column_edges)
    }
    row_triple_index = {
        triple: index for index, triple in enumerate(row_triples)
    }
    column_triple_index = {
        triple: index for index, triple in enumerate(column_triples)
    }
    expected_triangles = len(base) * (len(base) - 4) // 6
    counts = Counter()
    for triple in column_triples:
        leave = {
            row_edges[row]
            for row in range(len(row_edges))
            if any(
                g2[row][column_edge_index[edge]]
                for edge in subsets(triple, 2)
            )
        }
        degree = Counter(point for edge in leave for point in edge)
        assert all(degree[point] == 3 for point in base)
        selected = [
            row_triple
            for row_triple in row_triples
            if g3[row_triple_index[row_triple]][
                column_triple_index[triple]
            ]
        ]
        covered = Counter(
            edge
            for row_triple in selected
            for edge in subsets(row_triple, 2)
        )
        assert set(covered) == set(row_edges) - leave
        assert set(covered.values()) <= {1}
        assert len(selected) == expected_triangles
        counts[len(selected)] += 1
    return counts


def audit_control(k):
    points, blocks = extend_boundary_design(k)
    facet_owner = validate_steiner_system(points, blocks, k)
    nonblocks, maps = local_bijections(
        points, blocks, facet_owner, k
    )
    adjacent_edges, relative_types = adjacent_relative_cycle_types(
        points, nonblocks, maps
    )

    base = min(blocks, key=lambda block: tuple(sorted(block)))
    actual_distribution = Counter(len(base & block) for block in blocks)
    expected_distribution = intersection_distribution(k)
    assert [
        actual_distribution[index] for index in range(k + 1)
    ] == expected_distribution

    complement, matrices, indices = incidence_layers(
        points, blocks, base, k
    )
    g2 = matrices[2]
    g3 = matrices[3]
    row_edges, column_edges = indices[2]
    rank, determinant, overlaps = audit_matching_matrix(
        base, complement, g2, row_edges, column_edges
    )
    linked_latin_squares(
        base, complement, g2, row_edges, column_edges
    )
    triangle_columns, triangle_rows = audit_triangle_layer(
        base,
        complement,
        g2,
        g3,
        indices[2],
        indices[3],
    )
    return {
        "blocks": len(blocks),
        "nonblocks": len(nonblocks),
        "adjacent_edges": adjacent_edges,
        "relative_types": dict(relative_types),
        "distribution": expected_distribution,
        "g2_rank": rank,
        "unimodular_minor": determinant,
        "overlaps": dict(overlaps),
        "triangle_columns": dict(triangle_columns),
        "triangle_rows": dict(triangle_rows),
    }


def audit_k16_numbers():
    k = 16
    distribution = intersection_distribution(k)
    assert distribution == [
        1,
        0,
        960,
        17_920,
        196_560,
        1_118_208,
        3_779_776,
        7_687_680,
        9_755_460,
        7_687_680,
        3_779_776,
        1_118_208,
        196_560,
        17_920,
        960,
        0,
        1,
    ]
    local_degrees = [
        distribution[size] // comb(k, size)
        for size in range(k + 1)
    ]
    assert local_degrees == [
        1, 0, 8, 32, 108, 256, 472, 672, 758,
        672, 472, 256, 108, 32, 8, 0, 1,
    ]

    edge_count = comb(k, 2)
    disjoint_pairs = 3 * comb(k, 4)
    total_overlap = edge_count * comb(k // 2, 2)
    assert (edge_count, disjoint_pairs, total_overlap) == (
        120, 5_460, 3_360
    )
    assert Fraction(total_overlap, disjoint_pairs) == Fraction(8, 13)
    assert edge_count - k + 1 == 105
    assert k * (k - 4) // 6 == 32
    return distribution, local_degrees


def main():
    results = {k: audit_control(k) for k in (4, 6)}
    _, k16_degrees = audit_k16_numbers()

    for k in (4, 6):
        result = results[k]
        print(
            f"k={k}: blocks={result['blocks']}, "
            f"nonblocks={result['nonblocks']}, "
            f"adjacent nonblock edges={result['adjacent_edges']}"
        )
        print(
            f"  relative cycle types={result['relative_types']}, "
            f"rank(G2)={result['g2_rank']}, "
            f"unimodular minor={result['unimodular_minor']}"
        )
        print(
            f"  disjoint-row overlaps={result['overlaps']}, "
            f"G3 column counts={result['triangle_columns']}"
        )

    print(f"k=16 fixed-block layer degrees: {k16_degrees}")
    print(
        "k=16: G2 is 120x120, degree 8, rank <=105; "
        "5460 disjoint row-pairs have total overlap 3360 (average 8/13)"
    )
    print(
        "k=16: every G2 column-triple leaves a cubic graph and forces "
        "a 32-triangle decomposition of its complement"
    )
    print("Tits-equality local audit: PASS")


if __name__ == "__main__":
    main()

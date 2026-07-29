#!/usr/bin/env python3
"""Exact checks for evidence/three_way_trade.md.

The script uses only the Python standard library.  It verifies the closed
intersection formulas at r=3,5,15 and independently checks the r=3
nowhere-zero-F_4 obstruction by exhaustive Fano-plane generation and binary
linear algebra.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb


def popcount(x):
    """Python-3.7-compatible population count."""
    return bin(x).count("1")


def external_distribution(r):
    out = []
    for j in range(r):
        numerator = comb(r, j) * (comb(r + 1, j + 1) + (-1) ** j)
        assert numerator % (r + 2) == 0
        out.append(numerator // (r + 2))
    return out + [0]


def internal_distribution(r):
    out = []
    for j in range(r):
        numerator = comb(r, j) * (
            comb(r + 1, j + 1) - (r + 1) * ((-1) ** j)
        )
        assert numerator % (r + 2) == 0
        out.append(numerator // (r + 2))
    return out + [1]


def lambdas(r):
    return [
        Fraction(comb(2 * r + 1 - i, r - 1 - i), r - i)
        for i in range(r)
    ]


def check_moments(r, distribution):
    lam = lambdas(r)
    assert all(value.denominator == 1 for value in lam)
    for i in range(r):
        lhs = sum(comb(j, i) * distribution[j] for j in range(i, r + 1))
        rhs = comb(r, i) * int(lam[i])
        assert lhs == rhs, (r, i, lhs, rhs)


def binary_rank(rows):
    pivots = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return len(pivots)


def binary_null_basis(rows, ncols):
    """Return a basis of the nullspace of a binary matrix given as bit rows."""
    work = list(rows)
    pivot_columns = []
    rank = 0
    for column in range(ncols):
        pivot_row = next(
            (
                i
                for i in range(rank, len(work))
                if (work[i] >> column) & 1
            ),
            None,
        )
        if pivot_row is None:
            continue
        work[rank], work[pivot_row] = work[pivot_row], work[rank]
        for i in range(len(work)):
            if i != rank and ((work[i] >> column) & 1):
                work[i] ^= work[rank]
        pivot_columns.append(column)
        rank += 1
        if rank == len(work):
            break

    free_columns = [
        column for column in range(ncols) if column not in pivot_columns
    ]
    basis = []
    for free in free_columns:
        word = 1 << free
        for i, pivot in enumerate(pivot_columns):
            if (work[i] >> free) & 1:
                word |= 1 << pivot
        basis.append(word)
    assert len(basis) == ncols - binary_rank(rows)
    return basis


def span(basis):
    words = []
    for mask in range(1 << len(basis)):
        word = 0
        for i, vector in enumerate(basis):
            if (mask >> i) & 1:
                word ^= vector
        words.append(word)
    return words


def all_fano_planes():
    points = range(7)
    triples = list(combinations(points, 3))
    pairs = list(combinations(points, 2))
    containing = {
        pair: [
            i for i, block in enumerate(triples) if set(pair).issubset(block)
        ]
        for pair in pairs
    }
    systems = []

    def extend(used_pairs, selected):
        if len(used_pairs) == len(pairs):
            systems.append(frozenset(selected))
            return
        pair = next(pair for pair in pairs if pair not in used_pairs)
        for block_index in containing[pair]:
            block_pairs = list(combinations(triples[block_index], 2))
            if any(item in used_pairs for item in block_pairs):
                continue
            extend(used_pairs.union(block_pairs), selected + [block_index])

    extend(set(), [])
    assert len(systems) == 30
    return triples, pairs, systems


def check_fano_and_flow_obstruction():
    triples, pairs, systems = all_fano_planes()
    disjoint_degree = []
    triangle_found = False
    for i, first in enumerate(systems):
        neighbors = [
            j
            for j, second in enumerate(systems)
            if i != j and first.isdisjoint(second)
        ]
        disjoint_degree.append(len(neighbors))
        for left, right in combinations(neighbors, 2):
            if systems[left].isdisjoint(systems[right]):
                triangle_found = True
    assert set(disjoint_degree) == {8}
    assert not triangle_found

    first = systems[0]
    mates = [system for system in systems if first.isdisjoint(system)]
    assert len(mates) == 8
    assert Counter(len(a.intersection(b)) for a, b in combinations(mates, 2)) == {
        1: 28
    }

    second = mates[0]
    union_design = [
        i
        for i in range(len(triples))
        if i not in first and i not in second
    ]
    assert len(union_design) == 21

    # It is a simple 2-(7,3,3) design.
    for pair in pairs:
        degree = sum(
            set(pair).issubset(triples[index]) for index in union_design
        )
        assert degree == 3

    incidence_rows = []
    for pair in pairs:
        row = 0
        for column, block_index in enumerate(union_design):
            if set(pair).issubset(triples[block_index]):
                row |= 1 << column
        incidence_rows.append(row)

    basis = binary_null_basis(incidence_rows, len(union_design))
    words = span(basis)
    assert len(basis) == 6
    assert Counter(popcount(word) for word in words) == {0: 1, 8: 21, 12: 42}
    assert all(popcount(word) % 4 == 0 for word in words)
    assert all(popcount(a & b) % 2 == 0 for a in basis for b in basis)

    # A nowhere-zero F_4 flow is a pair of binary kernel words whose
    # supports cover every coordinate.
    best_cover = max(popcount(a | b) for a in words for b in words)
    assert best_cover == 18
    assert best_cover < len(union_design)
    return best_cover


def main():
    expected_r15 = [
        1,
        105,
        3465,
        48685,
        350805,
        1414413,
        3368365,
        4871295,
        4330755,
        2357355,
        771771,
        146055,
        15015,
        735,
        15,
        0,
    ]

    for r in (3, 5, 15):
        external = external_distribution(r)
        internal = internal_distribution(r)
        check_moments(r, external)
        check_moments(r, internal)
        block_count = comb(2 * r + 1, r) // (r + 2)
        assert sum(external) == block_count
        assert sum(internal) == block_count
        assert external[0] == 1
        assert internal[0] == 0
        print(
            "r={}: b={}, moments pass, n_0(external/internal)=1/0".format(
                r, block_count
            )
        )

    assert external_distribution(15) == expected_r15
    assert all(value % 2 == 1 for value in expected_r15[:-1])
    assert comb(31, 15) // 17 == 17678835
    print("r=15 external distribution and oddness pass")

    block_count = comb(31, 15) // 17
    full_boundary_rank = comb(30, 14)
    pair_complement_size = 15 * block_count
    pair_kernel_dimension_lower_bound = (
        pair_complement_size - full_boundary_rank
    )
    pair_kernel_radical_upper_bound = 2 * block_count
    assert pair_complement_size == 265182525
    assert full_boundary_rank == 145422675
    assert pair_kernel_dimension_lower_bound == 119759850
    assert pair_kernel_radical_upper_bound == 35357670
    assert pair_kernel_dimension_lower_bound > pair_kernel_radical_upper_bound
    print(
        "r=15 pair-trade dimension no-go: dim(C)>={} > "
        "rad(C)<={}".format(
            pair_kernel_dimension_lower_bound,
            pair_kernel_radical_upper_bound,
        )
    )

    best_cover = check_fano_and_flow_obstruction()
    print("r=3: 30 Fano planes, disjointness graph triangle-free")
    print(
        "r=3 lambda=3 example: binary kernel [21,6], "
        "weights 0/8/12, maximum two-word support={}".format(best_cover)
    )
    print("all three-way trade checks pass")


if __name__ == "__main__":
    main()

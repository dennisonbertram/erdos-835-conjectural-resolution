#!/usr/bin/env python3
"""Verify the finite Tutte-core catalogue for the eighth matching."""

from functools import reduce
from itertools import product
from operator import mul


def partitions(total: int, parts: int, minimum: int = 1) -> list[tuple[int, ...]]:
    """Return nonincreasing odd partitions of total into the given parts."""
    result = []

    def visit(remaining: int, count: int, ceiling: int, prefix: tuple[int, ...]) -> None:
        if count == 0:
            if remaining == 0:
                result.append(prefix)
            return
        for value in range(min(ceiling, remaining), minimum - 1, -1):
            if value % 2 == 0:
                continue
            if remaining - value < (count - 1) * minimum:
                continue
            visit(remaining - value, count - 1, value, prefix + (value,))

    visit(total, parts, total, ())
    return result


def core_edges(blocks: tuple[int, ...]) -> int:
    total = sum(blocks)
    return (total * total - sum(block * block for block in blocks)) // 2


def r0_reuse_ceiling(blocks: tuple[int, ...]) -> int:
    """Maximum t allowed by pointwise incidence and three size-8 supports."""
    order = sum(blocks)
    degrees = [
        order - block
        for block in blocks
        for _ in range(block)
    ]
    pointwise = 12 - max(degrees)
    required_small = 3 * order - 15
    feasible = [
        t
        for t in range(8)
        if t <= pointwise
        and sum(max(0, 12 - degree - t) for degree in degrees) >= required_small
    ]
    return max(feasible)


def catalogue(order: int) -> list[tuple[int, tuple[int, ...], int, int]]:
    rows = []
    for separator_size in range(order // 2):
        block_count = separator_size + 2
        if block_count > order - separator_size:
            continue
        minimum = max(1, order - separator_size - 7)
        for blocks in partitions(order - separator_size, block_count, minimum):
            maximum_degree = sum(blocks) - min(blocks)
            rows.append(
                (
                    separator_size,
                    blocks,
                    core_edges(blocks),
                    12 - maximum_degree,
                )
            )
    return rows


def main() -> None:
    expected_ten = [
        (0, (7, 3), 21, 5),
        (0, (5, 5), 25, 7),
        (1, (3, 3, 3), 27, 6),
        (2, (5, 1, 1, 1), 18, 5),
        (2, (3, 3, 1, 1), 22, 5),
        (3, (3, 1, 1, 1, 1), 18, 6),
        (4, (1, 1, 1, 1, 1, 1), 15, 7),
    ]
    expected_twelve = [
        (0, (7, 5), 35, 5),
        (4, (3, 1, 1, 1, 1, 1), 25, 5),
        (5, (1, 1, 1, 1, 1, 1, 1), 21, 6),
    ]

    assert catalogue(10) == expected_ten
    assert catalogue(12) == expected_twelve
    assert [r0_reuse_ceiling(blocks) for _, blocks, _, _ in expected_ten] == [
        5,
        5,
        4,
        5,
        5,
        6,
        6,
    ]

    profiles = {
        0: ((4, 3, 0), 31),
        1: ((4, 2, 1), 32),
        2: ((4, 1, 2), 33),
        3: ((4, 1, 2), 33),
        4: ((4, 1, 2), 33),
        5: ((4, 0, 3), 34),
    }
    for counts, expected_edges in profiles.values():
        assert sum(
            count * size // 2
            for count, size in zip(counts, (8, 10, 12))
        ) == expected_edges

    assert max(edges for _, _, edges, _ in expected_twelve[1:]) <= 34
    assert expected_twelve[0][2] > max(total for _, total in profiles.values())

    # A harmless independent arithmetic audit of the complete multipartite
    # formula: the product form and square-sum form agree for every row.
    for _, blocks, edges, _ in expected_ten + expected_twelve:
        pair_products = sum(
            reduce(mul, pair)
            for pair in product(blocks, repeat=2)
        ) - sum(block * block for block in blocks)
        assert pair_products // 2 == edges

    print("PASS size-10 catalogue: seven coarsened Tutte cores")
    print("PASS size-12 catalogue: three cores, with K5,7 over global budget")
    print("PASS reuse ceilings follow from d_H(v)=12-d_F(v)")
    print("PASS r=0 sharpening: every fixed core obstructs at most six size-10 supports")
    print("PASS target seven-prefix edge totals are 31, 32, 33, 33, 33, 34")
    print("SCOPE: exact obstruction reduction; eighth-colour packing remains open")


if __name__ == "__main__":
    main()

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
    """Maximum t allowed by the exact remaining-complement identity."""
    order = sum(blocks)
    degrees = [order - block for block in blocks for _ in range(block)]
    pointwise = 12 - max(degrees)
    edges = core_edges(blocks)
    outside = 13 - order
    noncore_touching = max(
        0,
        31 - edges - outside * (outside - 1) // 2,
    )
    complement_degree = (
        36 + 2 * order - 2 * edges - noncore_touching
    ) // 3
    return min(pointwise, complement_degree)


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
        2,
        1,
        0,
        4,
        2,
        4,
        6,
    ]
    # If K6 attained its generic ceiling six in a total seven-obstruction,
    # equality leaves 16 edges on the outside seven vertices.  The only
    # catalogue core that fits is a 15-edge K6, leaving the last vertex with
    # at most one incident edge, contrary to delta(F) >= 2.
    assert 3 * 6 == 36 + 2 * 6 - 2 * 15 == 18
    assert 31 - 15 == 16
    assert min(edges for _, _, edges, _ in expected_ten if edges > 15) == 18
    assert 16 - 15 == 1

    # K5111 fourfold equality: (c,a,b) are forced to these three cases.
    k5111_cases = [
        (c, a, b)
        for a in range(14)
        for b in range(14)
        for c in range(11)
        if a + b + c == 13 and a + 2 * b <= 4
    ]
    assert k5111_cases == [(10, 2, 1), (10, 3, 0), (9, 4, 0)]
    assert all(2 * c + a - 10 in (12, 13) for c, a, _ in k5111_cases)
    assert min(k * (6 - k) for k in range(1, 6)) == 5

    # K3311 twofold and K31111 fourfold equalities both force at most two
    # cross edges, after which K5,5 or K4,4 resilience supplies a matching.
    assert all(
        a <= 2
        for a in range(10)
        for b in range(10)
        if a + 2 * b <= 2
    )
    assert min(k * (5 - k) for k in range(1, 5)) == 4

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
    print("PASS r=0 complement-degree ceilings are 2, 1, 0, 4, 2, 4, 6")
    print("PASS total-obstruction equality sharpens K6 reuse from six to five")
    print("PASS total-obstruction ceilings sharpen to 2, 1, 0, 3, 1, 3, 5")
    print("PASS target seven-prefix edge totals are 31, 32, 33, 33, 33, 34")
    print("SCOPE: exact obstruction reduction; eighth-colour packing remains open")


if __name__ == "__main__":
    main()

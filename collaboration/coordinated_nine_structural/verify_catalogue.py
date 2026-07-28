#!/usr/bin/env python3
"""Verify the exact structural catalogue for a coordinated ninth matching."""

from __future__ import annotations

from dataclasses import dataclass
from math import comb


@dataclass(frozen=True)
class Core:
    support_size: int
    separator_size: int
    blocks: tuple[int, ...]
    order: int
    edges: int
    maximum_degree: int
    degree_three_edges: int


PROFILES = {
    0: {
        "edges": 36,
        "maximum_degree": 8,
        "selected": (4, 4, 0),
        "remaining": {8: 3, 10: 6, 12: 0},
    },
    1: {
        "edges": 37,
        "maximum_degree": 7,
        "selected": (4, 3, 1),
        "remaining": {8: 4, 10: 5, 12: 0},
    },
    2: {
        "edges": 38,
        "maximum_degree": 7,
        "selected": (4, 2, 2),
        "remaining": {8: 5, 10: 4, 12: 0},
    },
    3: {
        "edges": 38,
        "maximum_degree": 7,
        "selected": (4, 2, 2),
        "remaining": {8: 6, 10: 2, 12: 1},
    },
    4: {
        "edges": 38,
        "maximum_degree": 7,
        "selected": (4, 2, 2),
        "remaining": {8: 7, 10: 0, 12: 2},
    },
    5: {
        "edges": 40,
        "maximum_degree": 7,
        "selected": (4, 0, 4),
        "remaining": {8: 8, 10: 0, 12: 1},
    },
}


def odd_partitions(total: int, parts: int, minimum: int = 1):
    if parts == 0:
        if total == 0:
            yield ()
        return
    for first in range(minimum, total + 1, 2):
        for rest in odd_partitions(total - first, parts - 1, first):
            yield (first, *rest)


def core_from(
    support_size: int,
    separator_size: int,
    blocks: tuple[int, ...],
) -> Core:
    order = sum(blocks)
    edges = (
        order * order - sum(block * block for block in blocks)
    ) // 2
    degrees = [
        order - block
        for block in blocks
        for _ in range(block)
    ] + [0] * (13 - order)
    deficits = [max(0, 3 - degree) for degree in degrees]
    degree_three_edges = max(
        max(deficits),
        (sum(deficits) + 1) // 2,
    )
    return Core(
        support_size=support_size,
        separator_size=separator_size,
        blocks=blocks,
        order=order,
        edges=edges,
        maximum_degree=max(degrees),
        degree_three_edges=degree_three_edges,
    )


def raw_cores(support_size: int) -> tuple[Core, ...]:
    return tuple(
        core_from(support_size, separator_size, blocks)
        for separator_size in range((support_size - 2) // 2 + 1)
        for blocks in odd_partitions(
            support_size - separator_size,
            separator_size + 2,
        )
    )


def surviving_cores(
    support_size: int,
    edge_total: int,
    maximum_degree: int,
) -> tuple[Core, ...]:
    return tuple(
        core
        for core in raw_cores(support_size)
        if core.maximum_degree <= maximum_degree
        and core.edges + core.degree_three_edges <= edge_total
    )


def blocks(cores: tuple[Core, ...]) -> tuple[tuple[int, ...], ...]:
    return tuple(core.blocks for core in cores)


SIZE_EIGHT = (
    (1, 7),
    (3, 5),
    (1, 1, 5),
    (1, 3, 3),
    (1, 1, 1, 3),
    (1, 1, 1, 1, 1),
)
SIZE_TEN_DEGREE_EIGHT = (
    (3, 7),
    (5, 5),
    (1, 1, 7),
    (1, 3, 5),
    (3, 3, 3),
    (1, 1, 1, 5),
    (1, 1, 3, 3),
    (1, 1, 1, 1, 3),
    (1, 1, 1, 1, 1, 1),
)
SIZE_TEN_DEGREE_SEVEN = (
    (3, 7),
    (5, 5),
    (3, 3, 3),
    (1, 1, 1, 5),
    (1, 1, 3, 3),
    (1, 1, 1, 1, 3),
    (1, 1, 1, 1, 1, 1),
)
SIZE_TWELVE_BASE = (
    (1, 1, 1, 1, 5),
    (1, 1, 1, 3, 3),
    (1, 1, 1, 1, 1, 3),
    (1, 1, 1, 1, 1, 1, 1),
)
SIZE_TWELVE_COVER = (
    (5, 7),
    (1, 1, 1, 1, 1, 3),
    (1, 1, 1, 1, 1, 1, 1),
)


def verify_catalogues() -> None:
    assert blocks(surviving_cores(8, 36, 8)) == SIZE_EIGHT
    assert blocks(surviving_cores(8, 40, 7)) == SIZE_EIGHT
    assert blocks(surviving_cores(10, 36, 8)) == SIZE_TEN_DEGREE_EIGHT
    assert blocks(surviving_cores(10, 40, 7)) == SIZE_TEN_DEGREE_SEVEN

    assert blocks(surviving_cores(12, 36, 8)) == SIZE_TWELVE_BASE
    assert blocks(surviving_cores(12, 37, 8)) == SIZE_TWELVE_BASE
    assert blocks(surviving_cores(12, 38, 8)) == (
        (5, 7),
        *SIZE_TWELVE_BASE,
    )
    assert blocks(surviving_cores(12, 40, 7)) == SIZE_TWELVE_COVER

    five_three_three = core_from(12, 1, (3, 3, 5))
    assert five_three_three.edges == 39
    assert five_three_three.maximum_degree == 8
    assert five_three_three.degree_three_edges == 3
    assert five_three_three.edges + five_three_three.degree_three_edges == 42
    print("PASS exact size-8, size-10, and size-12 Tutte catalogues")


def verify_near_factor_reduction() -> None:
    degree_five_obstructions = tuple(
        core.blocks
        for core in raw_cores(12)
        if core.maximum_degree <= 6
    )
    degree_four_obstructions = tuple(
        core.blocks
        for core in raw_cores(12)
        if core.maximum_degree <= 7
    )
    assert degree_five_obstructions == (
        (1, 1, 1, 1, 1, 1, 1),
    )
    assert degree_four_obstructions == SIZE_TWELVE_COVER

    # Numerical equalities used by the K_{5,7} four-edge switch.
    assert 5 * (7 - 4 - 1) == 10
    assert 2 * 5 == 10
    assert 4 - 1 == 6 // 2
    print("PASS two-near-factor lemma and exact terminal core reduction")


def core_lookup(
    support_size: int,
    expected_blocks: tuple[tuple[int, ...], ...],
) -> dict[tuple[int, ...], Core]:
    candidates = {core.blocks: core for core in raw_cores(support_size)}
    return {current: candidates[current] for current in expected_blocks}


def reuse_bound(
    core: Core,
    support_size: int,
    edge_total: int,
    remaining_count: int,
) -> int:
    outside = 13 - core.order
    correction = max(
        0,
        edge_total - core.edges - comb(outside, 2),
    )
    complement_capacity = (
        2 * edge_total
        - 39
        + 3 * core.order
        - 2 * core.edges
        - correction
    )
    complement_size = 13 - support_size
    return min(
        remaining_count,
        12 - core.maximum_degree,
        complement_capacity // complement_size,
    )


def verify_profiles() -> None:
    total_profiles = {
        r: (7 + r, 10 - 2 * r, r)
        for r in range(6)
    }
    for r, data in PROFILES.items():
        selected = data["selected"]
        remaining = data["remaining"]
        assert isinstance(selected, tuple)
        assert isinstance(remaining, dict)
        assert tuple(
            selected[index] + remaining[size]
            for index, size in enumerate((8, 10, 12))
        ) == total_profiles[r]
        assert sum(selected) == 8
        assert sum(remaining.values()) == 9
        assert (
            4 * selected[0] + 5 * selected[1] + 6 * selected[2]
            == data["edges"]
        )
        remaining_complement_incidence = sum(
            (13 - size) * count for size, count in remaining.items()
        )
        assert remaining_complement_incidence == 2 * data["edges"] - 39
    print("PASS exact selected profiles and rho(v)=d_F(v)-3 totals")


def verify_reuse_tables() -> None:
    size_eight_cores = core_lookup(8, SIZE_EIGHT)
    size_ten_eight = core_lookup(10, SIZE_TEN_DEGREE_EIGHT)
    size_ten_seven = core_lookup(10, SIZE_TEN_DEGREE_SEVEN)
    size_twelve = core_lookup(12, SIZE_TWELVE_COVER)

    expected_eight = {
        0: (3, 3, 3, 3, 3, 3),
        1: (4, 3, 4, 3, 4, 4),
        2: (5, 3, 4, 4, 5, 5),
        3: (5, 3, 4, 4, 5, 6),
        4: (5, 3, 4, 4, 5, 6),
        5: (5, 4, 5, 4, 5, 6),
    }
    for r, expected in expected_eight.items():
        data = PROFILES[r]
        assert tuple(
            reuse_bound(
                core,
                8,
                data["edges"],
                data["remaining"][8],
            )
            for core in size_eight_cores.values()
        ) == expected

    expected_ten = {
        0: (3, 1, 4, 2, 1, 4, 3, 5, 6),
        1: (3, 2, 1, 4, 3, 5, 5),
        2: (3, 2, 1, 4, 3, 4, 4),
        3: (2, 2, 1, 2, 2, 2, 2),
    }
    for r, expected in expected_ten.items():
        data = PROFILES[r]
        current_cores = size_ten_eight if r == 0 else size_ten_seven
        assert tuple(
            reuse_bound(
                core,
                10,
                data["edges"],
                data["remaining"][10],
            )
            for core in current_cores.values()
        ) == expected

    expected_twelve = {
        3: (0, 1, 1),
        4: (0, 2, 2),
        5: (1, 1, 1),
    }
    for r, expected in expected_twelve.items():
        data = PROFILES[r]
        assert tuple(
            reuse_bound(
                core,
                12,
                data["edges"],
                data["remaining"][12],
            )
            for core in size_twelve.values()
        ) == expected

    print("PASS every profile-specific fixed-core reuse ceiling")


def main() -> None:
    verify_catalogues()
    verify_near_factor_reduction()
    verify_profiles()
    verify_reuse_tables()
    print("PASS exact finite reduction for the coordinated ninth frontier")
    print("SCOPE: necessary core/reuse system; no universal ninth theorem")


if __name__ == "__main__":
    main()

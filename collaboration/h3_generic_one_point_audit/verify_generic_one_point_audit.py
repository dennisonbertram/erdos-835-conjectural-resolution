#!/usr/bin/env python3
"""Independent finite checks for the generic one-point-lift audit.

This file deliberately does not import either Opus verifier.  It checks:

* the labelled two-sided round trip at s=1;
* explicit false positives after deleting two points;
* complete enumeration and packing maxima for S(2,3,7), S(3,4,8),
  S(3,4,10), and S(4,5,11).

All searches are deterministic, exact, and use only the standard library.
"""

from __future__ import annotations

from itertools import combinations, permutations
from math import factorial


def popcount(value: int) -> int:
    # Compatible with Python versions predating int.bit_count().
    return bin(value).count("1")


def check_s_one() -> None:
    """Exhaust both maps for LS(0,1,m) with class labels retained."""
    for m in (3, 4, 5, 6, 7):
        palette = tuple(range(m))
        deleted = m - 1
        colouring_count = 0

        # A proper m-colouring of K_{m-1} is an injection into the palette.
        for restricted in permutations(palette, m - 1):
            missing = (set(palette) - set(restricted)).pop()
            completed = restricted + (missing,)
            assert len(set(completed)) == m
            assert completed[:deleted] == restricted
            colouring_count += 1
        assert colouring_count == factorial(m)

        large_set_count = 0
        # A labelled LS(0,1,m) is a bijection point -> class label.
        for labelled_large_set in permutations(palette):
            restricted = labelled_large_set[:deleted]
            assert len(set(restricted)) == m - 1
            missing = (set(palette) - set(restricted)).pop()
            rebuilt = restricted + (missing,)
            assert rebuilt == labelled_large_set
            large_set_count += 1
        assert large_set_count == factorial(m)

        print(
            "s=1, m={}: {} labelled colourings <-> {} labelled large sets".format(
                m, colouring_count, large_set_count
            )
        )


def is_proper_johnson(
    points: tuple[int, ...], size: int, colouring: dict[frozenset[int], int]
) -> bool:
    blocks = [frozenset(block) for block in combinations(points, size)]
    if set(colouring) != set(blocks):
        return False
    for i, left in enumerate(blocks):
        for right in blocks[i + 1 :]:
            if len(left & right) == size - 1:
                if colouring[left] == colouring[right]:
                    return False
    return True


def check_two_point_false_positives() -> None:
    """Construct the two colourings used to show that a second deletion loses
    the exact completion property."""
    points5 = tuple(range(5))
    colouring_53 = {}
    full5 = frozenset(points5)
    for block in combinations(points5, 3):
        b = frozenset(block)
        edge = sorted(full5 - b)
        colouring_53[b] = (edge[0] + edge[1]) % 5
    assert is_proper_johnson(points5, 3, colouring_53)

    # Round-robin one-factorisation of K_6 on Z_5 union {infinity=5}.
    edge_colour = {}
    for colour in range(5):
        edge_colour[frozenset((colour, 5))] = colour
        for delta in (1, 2):
            edge_colour[
                frozenset(((colour - delta) % 5, (colour + delta) % 5))
            ] = colour
    assert len(edge_colour) == 15
    assert all(
        len({edge_colour[e] for e in edge_colour if x in e}) == 5
        for x in range(6)
    )

    points6 = tuple(range(6))
    full6 = frozenset(points6)
    colouring_64 = {
        frozenset(block): edge_colour[full6 - frozenset(block)]
        for block in combinations(points6, 4)
    }
    assert is_proper_johnson(points6, 4, colouring_64)
    print("two-point controls: J(5,3) and J(6,4) explicit 5-colourings")


def enumerate_steiner(v: int, t: int):
    """Enumerate every labelled S(t,t+1,v) by integer-bitset Algorithm X."""
    subs = list(combinations(range(v), t))
    blocks = list(combinations(range(v), t + 1))
    sub_index = {sub: i for i, sub in enumerate(subs)}

    columns_of_row = []
    rows_of_column = [0] * len(subs)
    for row, block in enumerate(blocks):
        columns = tuple(
            sub_index[sub] for sub in combinations(block, t)
        )
        columns_of_row.append(columns)
        for column in columns:
            rows_of_column[column] |= 1 << row

    systems = []

    def search(uncovered: int, available: int, chosen: int) -> None:
        if uncovered == 0:
            systems.append(chosen)
            return

        remaining_columns = uncovered
        candidates = 0
        best_count = len(blocks) + 1
        while remaining_columns:
            low = remaining_columns & -remaining_columns
            column = low.bit_length() - 1
            rows = rows_of_column[column] & available
            count = popcount(rows)
            if count < best_count:
                candidates = rows
                best_count = count
            if count <= 1:
                break
            remaining_columns -= low

        while candidates:
            row_bit = candidates & -candidates
            row = row_bit.bit_length() - 1
            candidates -= row_bit

            conflicts = 0
            new_uncovered = uncovered
            for column in columns_of_row[row]:
                conflicts |= rows_of_column[column]
                new_uncovered &= ~(1 << column)
            search(
                new_uncovered,
                available & ~conflicts,
                chosen | row_bit,
            )

    search((1 << len(subs)) - 1, (1 << len(blocks)) - 1, 0)
    assert len(systems) == len(set(systems))
    return blocks, systems


def apply_block_permutation(mask: int, row_map: list[int]) -> int:
    image = 0
    while mask:
        low = mask & -mask
        row = low.bit_length() - 1
        mask -= low
        image |= 1 << row_map[row]
    return image


def point_orbit(seed: int, v: int, blocks: list[tuple[int, ...]]) -> set[int]:
    """Orbit under adjacent transpositions, which generate S_v."""
    block_index = {block: i for i, block in enumerate(blocks)}
    row_maps = []
    for point in range(v - 1):
        permutation = list(range(v))
        permutation[point], permutation[point + 1] = (
            permutation[point + 1],
            permutation[point],
        )
        row_maps.append(
            [
                block_index[
                    tuple(sorted(permutation[x] for x in block))
                ]
                for block in blocks
            ]
        )

    orbit = {seed}
    frontier = [seed]
    while frontier:
        system = frontier.pop()
        for row_map in row_maps:
            image = apply_block_permutation(system, row_map)
            if image not in orbit:
                orbit.add(image)
                frontier.append(image)
    return orbit


def maximum_clique(
    system_masks: list[int], vertices: list[int]
) -> tuple[list[int], int]:
    """Exhaustive clique search in the induced disjointness graph."""
    count = len(vertices)
    adjacency = [0] * count
    for left in range(count):
        left_mask = system_masks[vertices[left]]
        for right in range(left + 1, count):
            if left_mask & system_masks[vertices[right]] == 0:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left

    best = []

    def search(candidates: int, current: list[int]) -> None:
        nonlocal best
        if len(current) + popcount(candidates) <= len(best):
            return
        if candidates == 0:
            if len(current) > len(best):
                best = list(current)
            return

        while candidates:
            if len(current) + popcount(candidates) <= len(best):
                return
            low = candidates & -candidates
            vertex = low.bit_length() - 1
            candidates -= low
            search(
                candidates & adjacency[vertex],
                current + [vertex],
            )

    search((1 << count) - 1, [])
    edge_count = sum(popcount(row) for row in adjacency) // 2
    return [vertices[x] for x in best], edge_count


def audit_design(v: int, t: int, expected_count: int, expected_max: int):
    blocks, systems = enumerate_steiner(v, t)
    assert len(systems) == expected_count

    # This comparison independently proves that every enumerated design is in
    # one S_v-orbit, legitimising the fixed-base reduction below.
    orbit = point_orbit(systems[0], v, blocks)
    assert orbit == set(systems)

    seed = systems[0]
    mates = [
        index for index, system in enumerate(systems)
        if seed & system == 0
    ]
    local_clique, mate_edges = maximum_clique(systems, mates)
    packing = [0] + local_clique
    assert len(packing) == expected_max
    assert all(
        systems[packing[i]] & systems[packing[j]] == 0
        for i in range(len(packing))
        for j in range(i + 1, len(packing))
    )

    # Transitivity proves the upper bound: every global clique can have one
    # member moved to the seed, leaving a clique inside the seed's mate graph.
    assert expected_max == 1 + len(local_clique)

    name = "S({},{},{})".format(t, t + 1, v)
    print(
        "{}: labelled={}, fixed mates={}, mate edges={}, packing max={}".format(
            name, len(systems), len(mates), mate_edges, expected_max
        )
    )
    return {
        "name": name,
        "labelled": len(systems),
        "mates": len(mates),
        "mate_edges": mate_edges,
        "packing_max": expected_max,
    }


def main() -> None:
    check_s_one()
    check_two_point_false_positives()

    results = [
        audit_design(7, 2, 30, 2),
        audit_design(8, 3, 30, 2),
        audit_design(10, 3, 2520, 5),
        audit_design(11, 4, 5040, 2),
    ]
    expected_rows = [
        ("S(2,3,7)", 30, 8, 0, 2),
        ("S(3,4,8)", 30, 8, 0, 2),
        ("S(3,4,10)", 2520, 144, 576, 5),
        ("S(4,5,11)", 5040, 144, 0, 2),
    ]
    assert [
        (
            result["name"],
            result["labelled"],
            result["mates"],
            result["mate_edges"],
            result["packing_max"],
        )
        for result in results
    ] == expected_rows

    print("PASS: independent one-point boundary and small-tower audit")
    print("STATUS: theorem valid; audit findings reproduced (see README for remediation)")


if __name__ == "__main__":
    main()

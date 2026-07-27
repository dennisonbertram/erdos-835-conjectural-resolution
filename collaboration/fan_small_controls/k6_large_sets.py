#!/usr/bin/env python3
"""Construct and exhaustively classify the large sets LS(2,3,9).

The two representatives are the type A and type B arrays in Bryant, Grannell,
and Griggs, *Large sets of large sets of Steiner triple systems of order 9*
(2003).  The classification check itself is independent and exhaustive:

* enumerate all 840 labelled STS(9)s as exact triangle decompositions of K_9;
* count every exact partition of the 84 triples into seven STS(9)s;
* compute the two representatives' automorphism groups over all of S_9; and
* use orbit--stabilizer and unequal stabilizer orders to exhaust the count.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations, permutations
from math import factorial


POINTS = tuple(range(9))
PAIRS = tuple(combinations(POINTS, 2))
TRIPLES = tuple(combinations(POINTS, 3))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
TRIPLE_INDEX = {triple: index for index, triple in enumerate(TRIPLES)}
FULL_MASK = (1 << len(TRIPLES)) - 1
FULL_PAIR_MASK = (1 << len(PAIRS)) - 1
TRIPLE_PAIR_MASKS = tuple(
    sum(1 << PAIR_INDEX[pair] for pair in combinations(triple, 2)) for triple in TRIPLES
)

Block = frozenset[int]
System = frozenset[Block]
Link = dict[Block, int]


def array_sts(rows: tuple[tuple[int, ...], ...]) -> System:
    """Return the 12 lines of the affine 3x3 array representation."""
    if len(rows) != 3 or any(len(row) != 3 for row in rows):
        raise AssertionError("an STS(9) array must be 3 by 3")
    blocks: list[Block] = []
    blocks.extend(frozenset(rows[row]) for row in range(3))
    blocks.extend(
        frozenset(rows[row][column] for row in range(3)) for column in range(3)
    )
    blocks.extend(
        frozenset(rows[row][(offset + row) % 3] for row in range(3))
        for offset in range(3)
    )
    blocks.extend(
        frozenset(rows[row][(offset - row) % 3] for row in range(3))
        for offset in range(3)
    )
    answer = frozenset(blocks)
    if len(answer) != 12:
        raise AssertionError("array did not produce twelve distinct lines")
    return answer


def relabel_system(system: System, mapping: dict[int, int]) -> System:
    return frozenset(
        frozenset(mapping.get(point, point) for point in block) for block in system
    )


def systems_to_link(systems: tuple[System, ...]) -> Link:
    link: Link = {}
    for colour, system in enumerate(systems):
        for block in system:
            if block in link:
                raise AssertionError("large-set systems are not disjoint")
            link[block] = colour
    if len(link) != 84:
        raise AssertionError("large set does not partition all triples")
    return link


def type_a_systems() -> tuple[System, ...]:
    """The order-42-automorphism representative (points 7,8 are infinities)."""
    base = array_sts(((7, 8, 0), (1, 2, 4), (5, 6, 3)))
    return tuple(
        relabel_system(base, {point: (point + shift) % 7 for point in range(7)})
        for shift in range(7)
    )


def type_b_systems() -> tuple[System, ...]:
    """The order-54-automorphism representative (6=infinity, 7=A, 8=B)."""
    exceptional = array_sts(((6, 7, 8), (0, 2, 4), (3, 1, 5)))
    base = array_sts(((6, 0, 1), (7, 2, 5), (3, 8, 4)))
    mapping = {6: 6, 7: 8, 8: 7, **{point: (point + 1) % 6 for point in range(6)}}
    orbit: list[System] = []
    current = base
    for _ in range(6):
        orbit.append(current)
        current = relabel_system(current, mapping)
    return (exceptional, *orbit)


def system_mask(system: System) -> int:
    answer = 0
    for block in system:
        answer |= 1 << TRIPLE_INDEX[tuple(sorted(block))]
    return answer


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    answer = 0
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        index = bit.bit_length() - 1
        mapped = tuple(sorted(permutation[point] for point in TRIPLES[index]))
        answer |= 1 << TRIPLE_INDEX[mapped]
        remaining ^= bit
    return answer


def enumerate_labelled_system_masks() -> tuple[int, ...]:
    """Exhaustively enumerate exact triangle decompositions of K_9."""
    by_pair: list[list[int]] = [[] for _ in PAIRS]
    for triple_index, pair_mask in enumerate(TRIPLE_PAIR_MASKS):
        remaining = pair_mask
        while remaining:
            bit = remaining & -remaining
            by_pair[bit.bit_length() - 1].append(triple_index)
            remaining ^= bit

    systems: set[int] = set()

    def search(covered_pairs: int, blocks: int) -> None:
        if covered_pairs == FULL_PAIR_MASK:
            systems.add(blocks)
            return
        uncovered = (~covered_pairs) & FULL_PAIR_MASK
        first_uncovered = (uncovered & -uncovered).bit_length() - 1
        for triple_index in by_pair[first_uncovered]:
            pair_mask = TRIPLE_PAIR_MASKS[triple_index]
            if covered_pairs & pair_mask:
                continue
            search(
                covered_pairs | pair_mask,
                blocks | (1 << triple_index),
            )

    search(0, 0)
    if len(systems) != 840:
        raise AssertionError(f"expected 840 labelled STS(9)s, got {len(systems)}")
    return tuple(sorted(systems))


def system_orbit_masks(seed: System) -> tuple[int, ...]:
    """Generate the labelled S_9 orbit of one STS(9)."""
    seed_mask = system_mask(seed)
    systems = {
        permute_mask(seed_mask, permutation) for permutation in permutations(POINTS)
    }
    return tuple(sorted(systems))


def count_large_sets(systems: tuple[int, ...]) -> tuple[int, int]:
    """Count exact covers of the 84 triples by seven labelled STS masks."""
    by_triple: list[list[int]] = [[] for _ in TRIPLES]
    for system in systems:
        remaining = system
        while remaining:
            bit = remaining & -remaining
            by_triple[bit.bit_length() - 1].append(system)
            remaining ^= bit

    states = 0

    @lru_cache(maxsize=None)
    def count(covered: int) -> int:
        nonlocal states
        states += 1
        if covered == FULL_MASK:
            return 1
        first_uncovered = (
            (~covered) & FULL_MASK & -(~covered & FULL_MASK)
        ).bit_length() - 1
        return sum(
            count(covered | system)
            for system in by_triple[first_uncovered]
            if not (covered & system)
        )

    answer = count(0)
    return answer, states


def automorphism_order(systems: tuple[System, ...]) -> int:
    """Count point permutations stabilizing an unlabelled large set."""
    target = tuple(sorted(system_mask(system) for system in systems))
    return sum(
        tuple(sorted(permute_mask(system, permutation) for system in target)) == target
        for permutation in permutations(POINTS)
    )


def verify_classification() -> dict[str, int]:
    """Exhaustively verify that type A and type B are all isomorphism types."""
    type_a = type_a_systems()
    type_b = type_b_systems()
    systems_to_link(type_a)
    systems_to_link(type_b)

    labelled_systems = enumerate_labelled_system_masks()
    if system_orbit_masks(type_a[0]) != labelled_systems:
        raise AssertionError("the exhaustive STS(9) list is not one S_9 orbit")
    large_set_count, search_states = count_large_sets(labelled_systems)
    automorphisms_a = automorphism_order(type_a)
    automorphisms_b = automorphism_order(type_b)
    if automorphisms_a == automorphisms_b:
        raise AssertionError("the two representatives were not distinguished")

    orbit_a = factorial(9) // automorphisms_a
    orbit_b = factorial(9) // automorphisms_b
    if orbit_a + orbit_b != large_set_count:
        raise AssertionError("the two orbits do not exhaust all large sets")
    return {
        "labelled_sts": len(labelled_systems),
        "large_sets_on_fixed_points": large_set_count,
        "search_states": search_states,
        "aut_a": automorphisms_a,
        "aut_b": automorphisms_b,
        "orbit_a": orbit_a,
        "orbit_b": orbit_b,
    }


def main() -> None:
    result = verify_classification()
    for key, value in result.items():
        print(f"{key}: {value}")
    print("classification: PASS (exactly two isomorphism types)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exhaust the k=4 top-rung partials and their minimum odd unitrades."""

from __future__ import annotations

from itertools import combinations, permutations


POINTS = tuple(range(8))
BLOCKS = tuple(combinations(POINTS, 4))
BLOCK_INDEX = {block: i for i, block in enumerate(BLOCKS)}
TRIPLES = tuple(combinations(POINTS, 3))
TRIPLE_INDEX = {triple: i for i, triple in enumerate(TRIPLES)}


def bitmask(items: tuple[int, ...]) -> int:
    mask = 0
    for item in items:
        mask |= 1 << item
    return mask


def canonical_sqs() -> tuple[tuple[int, ...], ...]:
    """The 14 affine planes of AG(3,2), labelled by binary integers."""
    system = tuple(block for block in BLOCKS if block[0] ^ block[1] ^ block[2] ^ block[3] == 0)
    assert len(system) == 14
    return system


def all_labelled_systems() -> tuple[tuple[int, ...], ...]:
    base = canonical_sqs()
    systems: set[tuple[int, ...]] = set()
    for perm in permutations(POINTS):
        image = tuple(
            sorted(
                BLOCK_INDEX[tuple(sorted(perm[point] for point in block))]
                for block in base
            )
        )
        systems.add(image)
    result = tuple(sorted(systems))
    assert len(result) == 30
    return result


def check_steiner(system: tuple[int, ...]) -> None:
    multiplicities = [0] * len(TRIPLES)
    for block_index in system:
        for triple in combinations(BLOCKS[block_index], 3):
            multiplicities[TRIPLE_INDEX[triple]] += 1
    assert all(value == 1 for value in multiplicities)
    assert all(BLOCK_INDEX[tuple(sorted(set(POINTS) - set(BLOCKS[index])))] in system for index in system)


def p9_unitrades() -> tuple[int, ...]:
    """All 3-by-3 product unitrades W_2 x W_2, as 70-bit block masks."""
    trades: set[int] = set()
    for support in combinations(POINTS, 6):
        support_set = set(support)
        first = support[0]
        for other_two in combinations(support[1:], 2):
            left = (first, *other_two)
            right = tuple(sorted(support_set - set(left)))
            blocks = tuple(
                BLOCK_INDEX[tuple(sorted(left_pair + right_pair))]
                for left_pair in combinations(left, 2)
                for right_pair in combinations(right, 2)
            )
            trades.add(bitmask(blocks))
    result = tuple(sorted(trades))
    assert len(result) == 280
    for trade in result:
        assert trade.bit_count() == 9
        facet_parities = [0] * len(TRIPLES)
        for block_index in range(len(BLOCKS)):
            if trade >> block_index & 1:
                for triple in combinations(BLOCKS[block_index], 3):
                    facet_parities[TRIPLE_INDEX[triple]] ^= 1
        assert not any(facet_parities)
    return result


def gf2_consistent(rows: list[int], variables: int) -> bool:
    """Rows encode an augmented GF(2) system with RHS in bit `variables`."""
    pivots: dict[int, int] = {}
    for original in rows:
        row = original
        while True:
            lhs = row & ((1 << variables) - 1)
            if not lhs:
                if row >> variables & 1:
                    return False
                break
            pivot = lhs.bit_length() - 1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return True


def common_odd_transversal_exists(union: tuple[int, ...]) -> bool:
    """Solve Q^T a = 1 with one variable for each of the 56 triples."""
    rows: list[int] = []
    for block_index in union:
        lhs = bitmask(tuple(TRIPLE_INDEX[t] for t in combinations(BLOCKS[block_index], 3)))
        rows.append(lhs | 1 << len(TRIPLES))
    return gf2_consistent(rows, len(TRIPLES))


def main() -> None:
    systems = all_labelled_systems()
    for system in systems:
        check_steiner(system)
    system_masks = tuple(bitmask(system) for system in systems)
    trades = p9_unitrades()

    disjoint_pairs = 0
    for i, j in combinations(range(len(systems)), 2):
        if not system_masks[i] & system_masks[j]:
            disjoint_pairs += 1

    partials = 0
    transversal_positive = 0
    p9_counts: list[int] = []
    colour_profiles: set[tuple[int, int, int]] = set()

    for i, j, ell in combinations(range(len(systems)), 3):
        if system_masks[i] & system_masks[j]:
            continue
        if system_masks[i] & system_masks[ell]:
            continue
        if system_masks[j] & system_masks[ell]:
            continue

        partials += 1
        union_mask = system_masks[i] | system_masks[j] | system_masks[ell]
        union = tuple(index for index in range(len(BLOCKS)) if union_mask >> index & 1)
        assert len(union) == 42

        if common_odd_transversal_exists(union):
            transversal_positive += 1

        contained = [trade for trade in trades if trade & ~union_mask == 0]
        p9_counts.append(len(contained))
        for trade in contained:
            profile = tuple((trade & system_masks[index]).bit_count() for index in (i, j, ell))
            colour_profiles.add(tuple(sorted(profile)))

    # The top-rung k-1=3 premise is itself impossible at k=4.
    assert disjoint_pairs > 0
    assert partials == 0
    assert transversal_positive == 0
    assert not p9_counts
    assert not colour_profiles

    print(f"labelled S(3,4,8) systems: {len(systems)}")
    print(f"disjoint system pairs: {disjoint_pairs}")
    print(f"pairwise-disjoint three-system partials: {partials}")
    print(f"partials with a common odd transversal: {transversal_positive}")
    print(f"classified 9-block product unitrades: {len(trades)}")
    print("RESULT: PASS")
    print(
        "Scope: exhaustive k=4 top-rung premise control only; "
        "no k=16 or #835 claim."
    )


if __name__ == "__main__":
    main()

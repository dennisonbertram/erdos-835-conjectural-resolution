#!/usr/bin/env python3
"""Exact classification of local excess graphs in a 9-block C(10,4,2).

Assume points 0,...,5 have degree 4 and points 6,...,9 have degree 3.
Every pair involving a low point has multiplicity exactly one.  On the six
high points the excess multiplicities z_ij=lambda_ij-1 form a loopless cubic
multigraph.  There are exactly nine such multigraphs up to S_6.

This verifier:

1. generates every labeled loopless cubic multigraph on six vertices;
2. quotients them canonically under all 720 high-point permutations;
3. for each of the nine canonical types, performs a complete, solver-free
   backtracking search for nine *distinct* 4-subsets with the prescribed pair
   multiplicities.

To make the finite search small and transparent, the three blocks through low
point 6 must partition the other nine points into three triples.  We enumerate
all 280 such partitions, then exactly fill the remaining pair demands.
"""

from __future__ import annotations

import itertools
from functools import lru_cache


HIGH = tuple(range(6))
POINTS = tuple(range(10))
EDGES6 = tuple(itertools.combinations(HIGH, 2))
PAIRS10 = tuple(itertools.combinations(POINTS, 2))
PAIR_INDEX = {p: i for i, p in enumerate(PAIRS10)}
BLOCKS = tuple(itertools.combinations(POINTS, 4))
BLOCK_PAIR_IDS = tuple(
    tuple(PAIR_INDEX[p] for p in itertools.combinations(b, 2)) for b in BLOCKS
)
BLOCKS_BY_PAIR = tuple(
    tuple(i for i, ids in enumerate(BLOCK_PAIR_IDS) if p in ids)
    for p in range(len(PAIRS10))
)


def labeled_cubic_multigraphs() -> list[tuple[int, ...]]:
    ans: list[tuple[int, ...]] = []

    def rec(i: int, degrees: list[int], weights: list[int]) -> None:
        if i == len(EDGES6):
            if degrees == [3] * 6:
                ans.append(tuple(weights))
            return
        a, b = EDGES6[i]
        for value in range(min(3 - degrees[a], 3 - degrees[b]) + 1):
            degrees[a] += value
            degrees[b] += value
            weights.append(value)
            rec(i + 1, degrees, weights)
            weights.pop()
            degrees[a] -= value
            degrees[b] -= value

    rec(0, [0] * 6, [])
    return ans


def canonical(weights: tuple[int, ...]) -> tuple[int, ...]:
    weight = {edge: weights[i] for i, edge in enumerate(EDGES6)}
    return min(
        tuple(weight[tuple(sorted((perm[a], perm[b])))] for a, b in EDGES6)
        for perm in itertools.permutations(HIGH)
    )


def triple_partitions(values: tuple[int, ...]):
    """Yield each partition into unlabeled triples exactly once."""
    if not values:
        yield ()
        return
    first = values[0]
    rest = values[1:]
    for mates in itertools.combinations(rest, 2):
        group = (first,) + mates
        unused = tuple(x for x in rest if x not in mates)
        for tail in triple_partitions(unused):
            yield (group,) + tail


PARTITIONS = tuple(triple_partitions(tuple(x for x in POINTS if x != 6)))
assert len(PARTITIONS) == 280


def target_demands(weights: tuple[int, ...]) -> tuple[int, ...]:
    excess = {edge: weights[i] for i, edge in enumerate(EDGES6)}
    return tuple(1 + excess.get(pair, 0) for pair in PAIRS10)


def realize(weights: tuple[int, ...]):
    target = target_demands(weights)
    node_count = 0

    for partition in PARTITIONS:
        initial_blocks = tuple(
            BLOCKS.index(tuple(sorted((6,) + group))) for group in partition
        )
        remaining = list(target)
        valid = True
        for bi in initial_blocks:
            for p in BLOCK_PAIR_IDS[bi]:
                remaining[p] -= 1
                if remaining[p] < 0:
                    valid = False
        if not valid:
            continue

        @lru_cache(maxsize=None)
        def dfs(
            demands: tuple[int, ...], used: tuple[int, ...], blocks_left: int
        ):
            nonlocal node_count
            node_count += 1
            if sum(demands) != 6 * blocks_left:
                return None
            if blocks_left == 0:
                return () if not any(demands) else None

            used_set = set(used)
            best_candidates = None
            for p, demand in enumerate(demands):
                if demand == 0:
                    continue
                feasible = []
                for bi in BLOCKS_BY_PAIR[p]:
                    if bi in used_set:
                        continue
                    ids = BLOCK_PAIR_IDS[bi]
                    if all(demands[q] > 0 for q in ids):
                        feasible.append(bi)
                if not feasible:
                    return None
                if best_candidates is None or len(feasible) < len(best_candidates):
                    best_candidates = feasible

            assert best_candidates is not None
            for bi in best_candidates:
                new_demands = list(demands)
                for q in BLOCK_PAIR_IDS[bi]:
                    new_demands[q] -= 1
                new_used = tuple(sorted(used + (bi,)))
                tail = dfs(tuple(new_demands), new_used, blocks_left - 1)
                if tail is not None:
                    return (bi,) + tail
            return None

        tail = dfs(tuple(remaining), tuple(sorted(initial_blocks)), 6)
        if tail is not None:
            witness_ids = initial_blocks + tail
            witness = tuple(BLOCKS[i] for i in witness_ids)
            assert len(set(witness)) == 9
            got = [0] * len(PAIRS10)
            for bi in witness_ids:
                for p in BLOCK_PAIR_IDS[bi]:
                    got[p] += 1
            assert tuple(got) == target
            return witness, node_count
    return None, node_count


def main() -> int:
    labeled = labeled_cubic_multigraphs()
    classes = sorted({canonical(w) for w in labeled})
    assert len(labeled) == 760
    assert len(classes) == 9
    print("labeled_cubic_multigraphs", len(labeled))
    print("isomorphism_classes", len(classes))

    realizable = []
    for type_id, weights in enumerate(classes):
        witness, nodes = realize(weights)
        status = "REALIZABLE" if witness is not None else "IMPOSSIBLE"
        print("type", type_id, status, "nodes", nodes, "weights", weights)
        if witness is not None:
            realizable.append(type_id)
            for block in witness:
                print(" block", *block)

    assert realizable == [0, 1, 2, 4]
    print("realizable_types", *realizable)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

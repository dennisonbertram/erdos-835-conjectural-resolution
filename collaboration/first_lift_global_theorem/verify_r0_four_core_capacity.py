#!/usr/bin/env python3
"""Screen an arbitrary four-core type multiset by subset capacity."""

from __future__ import annotations

import argparse
import math
from collections import Counter
from itertools import combinations

from verify_r0_core_pairs import embeddings, popcount
from verify_r0_three_core_capacity import (
    BASE_CAPACITY,
    KINDS,
    PAIR_COUNTS,
    covering_splits,
    passes_prefix_screens,
    support_mask,
)


def anchor_cost(
    anchor: str,
    pattern: tuple[str, ...],
) -> int:
    remaining = Counter(pattern)
    remaining[anchor] -= 1
    cost = 1
    for kind, count in remaining.items():
        cost *= math.comb(PAIR_COUNTS[anchor, kind], count)
    return cost


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("kinds", nargs=4, choices=KINDS)
    parser.add_argument("--stop-cover", action="store_true")
    args = parser.parse_args()

    pattern = tuple(sorted(args.kinds, key=KINDS.index))
    if sum(BASE_CAPACITY[kind] for kind in pattern) < 7:
        raise SystemExit("pattern has total base capacity below seven")

    cores = {kind: embeddings(kind) for kind in set(pattern)}
    anchor_kind = min(
        set(pattern),
        key=lambda kind: anchor_cost(kind, pattern),
    )
    first = cores[anchor_kind][0]
    remaining = Counter(pattern)
    remaining[anchor_kind] -= 1
    groups = [(kind, count) for kind, count in remaining.items() if count]

    pools = {}
    for kind, _count in groups:
        pools[kind] = [
            core
            for core in cores[kind]
            if core != first and passes_prefix_screens(first | core)
        ]
        assert len(pools[kind]) == PAIR_COUNTS[anchor_kind, kind]

    supports = {
        core: support_mask(core)
        for values in cores.values()
        for core in values
    }
    tested = 0
    screened = 0
    covering = 0
    covering_example = None
    union_edges = Counter()

    def search(
        group_index: int,
        chosen: tuple[tuple[str, int], ...],
        union: int,
    ) -> bool:
        nonlocal tested, screened, covering, covering_example
        if group_index == len(groups):
            tested += 1
            screened += 1
            family = ((anchor_kind, first), *chosen)
            splits = covering_splits(family, union, supports)
            if not splits:
                return False
            covering += 1
            union_edges[popcount(union)] += 1
            if covering_example is None:
                covering_example = (popcount(union), splits[0])
            return args.stop_cover

        kind, count = groups[group_index]
        for selection in combinations(
            pools[kind],
            count,
        ):
            next_union = union
            for core in selection:
                next_union |= core
            if not passes_prefix_screens(next_union):
                continue
            next_chosen = chosen + tuple((kind, core) for core in selection)
            if search(group_index + 1, next_chosen, next_union):
                return True
        return False

    search(0, (), first)
    print(f"pattern={pattern} anchor={anchor_kind}")
    print(
        "pool_sizes="
        + repr({kind: len(pool) for kind, pool in pools.items()})
    )
    print(
        f"screened_leaves={screened} covering_families={covering} "
        f"example={covering_example}"
    )
    print(f"covering_union_edge_counts={dict(sorted(union_edges.items()))}")
    if covering:
        print("OPEN: subset-capacity inequalities admit a four-core cover")
    else:
        print("PASS: four-core type multiset cannot cover seven supports")


if __name__ == "__main__":
    main()

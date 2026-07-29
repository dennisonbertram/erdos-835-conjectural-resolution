#!/usr/bin/env python3
"""Screen an arbitrary four- or five-core multiset by subset capacity."""

from __future__ import annotations

import argparse
import math
from collections import Counter

from verify_r0_core_pairs import INCIDENT, VERTICES, embeddings, popcount
from verify_r0_three_core_capacity import (
    BASE_CAPACITY,
    KINDS,
    PAIR_COUNTS,
    covering_splits,
    passes_prefix_screens,
    support_mask,
)


def row_rank_violation(
    family: tuple[tuple[str, int], ...],
    union: int,
    supports: dict[int, int],
    split: tuple[int, ...],
) -> tuple[tuple[int, ...], int, int] | None:
    """Return a vertex-set violation of the exact complement-row rank bound."""
    degrees = [popcount(union & INCIDENT[vertex]) for vertex in VERTICES]
    # A violating set never needs a vertex of J-degree at most two:
    # deleting one weakly raises the lower bound and lowers the capacity.
    relevant = tuple(vertex for vertex in VERTICES if degrees[vertex] >= 3)
    for subset_bits in range(1, 1 << len(relevant)):
        subset = tuple(
            relevant[index]
            for index in range(len(relevant))
            if subset_bits >> index & 1
        )
        required_triple_incidences = sum(
            degrees[vertex] - 2 for vertex in subset
        ) - 3 * min(5, len(subset))
        if required_triple_incidences <= 0:
            continue

        available_triple_incidences = 0
        for multiplicity, (_kind, core) in zip(split, family):
            outside_count = sum(not (supports[core] >> vertex & 1) for vertex in subset)
            available_triple_incidences += multiplicity * min(
                3,
                outside_count,
            )
        if required_triple_incidences > available_triple_incidences:
            return (
                subset,
                required_triple_incidences,
                available_triple_incidences,
            )
    return None


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
    parser.add_argument("kinds", nargs="+", choices=KINDS)
    parser.add_argument("--stop-cover", action="store_true")
    args = parser.parse_args()
    if len(args.kinds) not in (4, 5):
        parser.error("provide exactly four or five core types")

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
        core: support_mask(core) for values in cores.values() for core in values
    }
    tested = 0
    screened = 0
    covering = 0
    row_identity_excluded = 0
    row_rank_excluded = 0
    unresolved = 0
    covering_example = None
    row_rank_example = None
    unresolved_example = None
    union_edges = Counter()

    def search(
        group_index: int,
        chosen: tuple[tuple[str, int], ...],
        union: int,
    ) -> bool:
        nonlocal tested, screened, covering
        nonlocal row_identity_excluded, row_rank_excluded, unresolved
        nonlocal covering_example, row_rank_example, unresolved_example
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
            intersection = (1 << len(VERTICES)) - 1
            for _kind, core in family:
                intersection &= supports[core]
            intersection_degrees = [
                popcount(union & INCIDENT[vertex])
                for vertex in VERTICES
                if intersection >> vertex & 1
            ]
            if intersection_degrees and max(intersection_degrees) >= 6:
                row_identity_excluded += 1
                return False

            rank_checks = [
                (
                    split,
                    row_rank_violation(
                        family,
                        union,
                        supports,
                        split,
                    ),
                )
                for split in splits
            ]
            if all(violation is not None for _split, violation in rank_checks):
                row_rank_excluded += 1
                if row_rank_example is None:
                    row_rank_example = (
                        popcount(union),
                        rank_checks[0],
                    )
                return False

            unresolved += 1
            if unresolved_example is None:
                surviving_split = next(
                    split for split, violation in rank_checks if violation is None
                )
                unresolved_example = (
                    popcount(union),
                    surviving_split,
                    tuple(intersection_degrees),
                )
            return args.stop_cover

        kind, count = groups[group_index]
        pool = pools[kind]

        def choose_group(
            start: int,
            needed: int,
            selection: tuple[int, ...],
            partial_union: int,
        ) -> bool:
            if needed == 0:
                next_chosen = chosen + tuple((kind, core) for core in selection)
                return search(
                    group_index + 1,
                    next_chosen,
                    partial_union,
                )
            last_start = len(pool) - needed
            for index in range(start, last_start + 1):
                core = pool[index]
                next_union = partial_union | core
                if not passes_prefix_screens(next_union):
                    continue
                if choose_group(
                    index + 1,
                    needed - 1,
                    (*selection, core),
                    next_union,
                ):
                    return True
            return False

        if choose_group(0, count, (), union):
            return True
        return False

    search(0, (), first)
    print(f"pattern={pattern} anchor={anchor_kind}")
    print("pool_sizes=" + repr({kind: len(pool) for kind, pool in pools.items()}))
    print(
        f"screened_leaves={screened} covering_families={covering} "
        f"example={covering_example}"
    )
    print(
        f"row_identity_excluded={row_identity_excluded} "
        f"row_rank_excluded={row_rank_excluded} "
        f"row_rank_example={row_rank_example} "
        f"unresolved={unresolved} unresolved_example={unresolved_example}"
    )
    print(f"covering_union_edge_counts={dict(sorted(union_edges.items()))}")
    if covering == 0:
        print(f"PASS: {len(pattern)}-core type multiset cannot cover seven supports")
    elif unresolved == 0:
        print("PASS: complement-row identity excludes every capacity cover")
    else:
        print("OPEN: subset capacity and common-row identity leave a cover")


if __name__ == "__main__":
    main()

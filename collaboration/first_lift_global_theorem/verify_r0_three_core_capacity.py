#!/usr/bin/env python3
"""Exhaust three-core families under the r=0 complement-capacity bound."""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from itertools import permutations, product

from verify_r0_core_pairs import (
    CLIQUE,
    INCIDENT,
    N,
    NINE_CLIQUES,
    VERTICES,
    embeddings,
    popcount,
)


KINDS = ("5111", "3311", "31111", "6")
BASE_CAPACITY = {"5111": 3, "3311": 1, "31111": 3, "6": 4}
PAIR_COUNTS = {
    ("5111", "5111"): 245,
    ("5111", "3311"): 190,
    ("5111", "31111"): 205,
    ("5111", "6"): 25,
    ("3311", "5111"): 38,
    ("3311", "3311"): 81,
    ("3311", "31111"): 214,
    ("3311", "6"): 27,
    ("31111", "5111"): 246,
    ("31111", "3311"): 1284,
    ("31111", "31111"): 1264,
    ("31111", "6"): 133,
    ("6", "5111"): 1050,
    ("6", "3311"): 5670,
    ("6", "31111"): 4655,
    ("6", "6"): 364,
}
ALL_VERTICES = (1 << N) - 1
SHARED_A_PATTERNS = {
    ("5111", "5111", "31111"),
    ("5111", "5111", "6"),
}


@lru_cache(maxsize=None)
def passes_prefix_screens(union: int) -> bool:
    edge_count = popcount(union)
    if edge_count > 31:
        return False
    degrees = [popcount(union & INCIDENT[v]) for v in VERTICES]
    if max(degrees) > 7:
        return False
    deficit = sum(max(0, 2 - degree) for degree in degrees)
    if edge_count + (deficit + 1) // 2 > 31:
        return False
    return edge_count < 29 or all(
        popcount(union & clique) <= 28 for clique in NINE_CLIQUES
    )


def support_mask(core: int) -> int:
    return sum(1 << v for v in VERTICES if core & INCIDENT[v])


def capacity(
    kind: str,
    core: int,
    union: int,
    core_support: int,
) -> int:
    outside = ALL_VERTICES ^ core_support
    core_degree_sum = sum(
        popcount(union & INCIDENT[v]) for v in VERTICES if core_support >> v & 1
    )
    remaining_edges = 31 - popcount(union)
    free_outside_edges = popcount(CLIQUE[outside] & ~union)
    forced_touch = max(0, remaining_edges - free_outside_edges)
    incidence_bound = (
        36 + 2 * popcount(core_support) - core_degree_sum - forced_touch
    ) // 3
    return max(0, min(BASE_CAPACITY[kind], incidence_bound))


def best_order(
    pattern: tuple[str, str, str],
    cores: dict[str, list[int]],
) -> tuple[str, str, str]:
    return min(
        set(permutations(pattern)),
        key=lambda order: PAIR_COUNTS[order[0], order[1]] * len(cores[order[2]]),
    )


def subset_capacity(
    union: int,
    common_support: int,
) -> int:
    outside = ALL_VERTICES ^ common_support
    remaining_edges = 31 - popcount(union)
    free_outside_edges = popcount(CLIQUE[outside] & ~union)
    forced_touch = max(0, remaining_edges - free_outside_edges)
    return max(
        0,
        36
        + 2 * popcount(common_support)
        - sum(
            popcount(union & INCIDENT[v]) for v in VERTICES if common_support >> v & 1
        )
        - forced_touch,
    )


@lru_cache(maxsize=None)
def split_demands(
    capacities: tuple[int, ...],
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """Return each positive seven-split and its demands by subset bitmask."""
    demands = []
    for split in product(*(range(1, cap + 1) for cap in capacities)):
        if sum(split) != 7:
            continue
        demands.append(
            (
                split,
                tuple(
                    3
                    * sum(
                        split[index]
                        for index in range(len(split))
                        if subset >> index & 1
                    )
                    for subset in range(1, 1 << len(split))
                ),
            )
        )
    return tuple(demands)


@lru_cache(maxsize=None)
def subset_order(size: int) -> tuple[int, ...]:
    """Put cheap singleton constraints before larger common-support bounds."""
    return tuple(
        sorted(
            range(1, 1 << size),
            key=lambda subset: (popcount(subset), subset),
        )
    )


def covering_splits(
    family: tuple[tuple[str, int], ...],
    union: int,
    support_masks: dict[int, int],
) -> list[tuple[int, ...]]:
    supports = tuple(support_masks[core] for _kind, core in family)
    common_supports = [ALL_VERTICES] * (1 << len(family))
    capacities = tuple(BASE_CAPACITY[kind] for kind, _core in family)
    survivors = split_demands(capacities)
    for subset in subset_order(len(family)):
        lowest = subset & -subset
        index = lowest.bit_length() - 1
        common_supports[subset] = common_supports[subset ^ lowest] & supports[index]
        bound = subset_capacity(union, common_supports[subset])
        survivors = tuple(
            (split, demands)
            for split, demands in survivors
            if demands[subset - 1] <= bound
        )
        if not survivors:
            return []
    return [split for split, _demands in survivors]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("kinds", nargs=3, choices=KINDS)
    parser.add_argument(
        "--stop-at-seven",
        action="store_true",
        help="stop after finding a union whose summed bound reaches seven",
    )
    args = parser.parse_args()
    pattern = tuple(sorted(args.kinds, key=KINDS.index))
    if sum(BASE_CAPACITY[kind] for kind in pattern) < 7:
        raise SystemExit("pattern has total base capacity below seven")

    cores = {kind: embeddings(kind) for kind in set(pattern)}
    order = best_order(pattern, cores)
    first_kind, second_kind, third_kind = order
    first = cores[first_kind][0]
    first_support = support_mask(first)
    support_masks = {
        core: support_mask(core) for values in cores.values() for core in values
    }

    seconds = [
        core
        for core in cores[second_kind]
        if core != first and passes_prefix_screens(first | core)
    ]
    assert len(seconds) == PAIR_COUNTS[first_kind, second_kind]
    thirds = [
        core
        for core in cores[third_kind]
        if core != first and passes_prefix_screens(first | core)
    ]
    assert len(thirds) == PAIR_COUNTS[first_kind, third_kind]

    maximum = -1
    best = None
    ordered_families = 0
    unions: dict[int, tuple[int, int, int]] = {}
    high_capacity_families = 0
    shared_a_failures = 0
    shared_a_bounds = set()
    covering_families = 0
    covering_example = None
    for second in seconds:
        pair = first | second
        for third in thirds:
            if third == first or third == second:
                continue
            union = pair | third
            if not passes_prefix_screens(union):
                continue
            ordered_families += 1
            capacities = (
                capacity(first_kind, first, union, first_support),
                capacity(
                    second_kind,
                    second,
                    union,
                    support_masks[second],
                ),
                capacity(
                    third_kind,
                    third,
                    union,
                    support_masks[third],
                ),
            )
            family = (
                (first_kind, first),
                (second_kind, second),
                (third_kind, third),
            )
            splits = covering_splits(family, union, support_masks)
            if splits:
                covering_families += 1
                if covering_example is None:
                    covering_example = (popcount(union), splits[0])
            total = sum(capacities)
            if total > maximum:
                maximum = total
                best = (popcount(union), capacities)
            unions[union] = max(
                unions.get(union, capacities),
                capacities,
                key=lambda item: (sum(item), item),
            )
            if total >= 7 and pattern in SHARED_A_PATTERNS:
                high_capacity_families += 1
                a_cores = [core for kind, core in family if kind == "5111"]
                a_supports = {support_masks[core] for core in a_cores}
                if len(a_supports) != 1:
                    shared_a_failures += 1
                else:
                    common_support = next(iter(a_supports))
                    common_bound = (
                        36
                        + 2 * popcount(common_support)
                        - sum(
                            popcount(union & INCIDENT[v])
                            for v in VERTICES
                            if common_support >> v & 1
                        )
                    )
                    shared_a_bounds.add(common_bound)
            if args.stop_at_seven and splits:
                print(f"pattern={pattern} order={order}")
                print(
                    "OPEN SUBSET-CAPACITY WITNESS: "
                    f"edges={popcount(union)} split={splits[0]}"
                )
                print("SCOPE: necessary union screens and summed capacity only")
                return

    histogram = Counter(
        (popcount(union), tuple(sorted(capacities)))
        for union, capacities in unions.items()
    )
    print(f"pattern={pattern} order={order}")
    print(f"ordered_families={ordered_families} distinct_unions={len(unions)}")
    print(f"maximum_summed_capacity={maximum} best={best}")
    print(f"covering_families={covering_families} covering_example={covering_example}")
    print(f"union_histogram={dict(sorted(histogram.items()))}")
    if pattern in SHARED_A_PATTERNS:
        assert high_capacity_families > 0
        assert shared_a_failures == 0
        assert max(shared_a_bounds) < 12
        print("PASS: every capacity-seven family has two A cores on one support")
        print(
            "PASS: their common outside capacity is below the twelve "
            "incidences required by four triples"
        )
        assert covering_families == 0
    elif covering_families == 0:
        print("PASS: subset capacities cannot cover seven supports")
    else:
        print("OPEN: subset-capacity bounds alone do not eliminate pattern")


if __name__ == "__main__":
    main()

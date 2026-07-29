#!/usr/bin/env python3
"""Search a category-dependent covariant formula for one invariant matching.

The existing 272-formula screen uses one (blend, multiplier, rank) rule on all
quadruple orbits.  For a single matching, C17 covariance also permits a
different rule for quadruples containing zero, one, or two fixed points.  This
script performs deterministic coordinate descent over that larger ansatz.
Failure is only a formula-family search result, never an UNSAT result.
"""

from __future__ import annotations

import argparse
import random
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "h3_simultaneous_fan_attack_2"
sys.path.insert(0, str(SOURCE))

from screen_cyclic_invariant_fan_formulas import labels_for_formula  # noqa: E402
from search_cyclic_invariant_matching_local import verify_matching  # noqa: E402
from verify_fan_kernel_reduction import (  # noqa: E402
    build_orbit_hypergraph,
    construct_large_set,
    verify_large_set,
)


Q_GROUPS = 228
TC_GROUPS = 912

Pattern = tuple[int, ...]
Parameters = tuple[int, int, int]


def contribution(
    selected: Pattern,
    cell_tc: tuple[tuple[int, ...], ...],
) -> Counter[int]:
    counts: Counter[int] = Counter()
    for cell in selected:
        counts.update(cell_tc[cell])
    return counts


def collision(count: int) -> int:
    return count * (count - 1) // 2


def combine_score(
    indices: list[int],
    contributions: list[list[Counter[int]]],
) -> int:
    counts = [0] * TC_GROUPS
    for category, option in enumerate(indices):
        for group, value in contributions[category][option].items():
            counts[group] += value
    return sum(map(collision, counts))


def best_coordinate(
    indices: list[int],
    category: int,
    contributions: list[list[Counter[int]]],
) -> tuple[int, int]:
    base = [0] * TC_GROUPS
    for other_category, option in enumerate(indices):
        if other_category == category:
            continue
        for group, value in contributions[other_category][option].items():
            base[group] += value
    base_score = sum(map(collision, base))
    best = (10**9, -1)
    for option, delta_counts in enumerate(contributions[category]):
        score = base_score
        for group, value in delta_counts.items():
            score += collision(base[group] + value) - collision(base[group])
        best = min(best, (score, option))
    return best


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--restarts", type=int, default=20)
    parser.add_argument("--rounds", type=int, default=20)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()

    link = construct_large_set()
    verify_large_set(link)
    cells, groups = build_orbit_hypergraph(link)
    cell_tc_lists: list[list[int]] = [[] for _ in cells]
    for group_number, group in enumerate(groups[Q_GROUPS:]):
        for cell in group:
            cell_tc_lists[cell].append(group_number)
    cell_tc = tuple(tuple(items) for items in cell_tc_lists)
    if {len(items) for items in cell_tc} != {4}:
        raise AssertionError("each cell should have four TC incidences")

    q_category = []
    for group in groups[:Q_GROUPS]:
        categories = {
            sum(point >= 17 for point in cells[cell][0]) for cell in group
        }
        if len(categories) != 1:
            raise AssertionError("a Q-group crosses fixed-point categories")
        q_category.append(categories.pop())
    category_census = Counter(q_category)
    if category_census != Counter({0: 140, 1: 80, 2: 8}):
        raise AssertionError(f"unexpected Q-category census {category_census}")

    pattern_maps: list[dict[Pattern, Parameters]] = [dict() for _ in range(3)]
    for blend in range(17):
        for multiplier in range(1, 17):
            labels = labels_for_formula(link, cells, blend, multiplier)
            for rank in range(13):
                chosen: list[list[int]] = [[], [], []]
                for group_number, group in enumerate(groups[:Q_GROUPS]):
                    hits = [cell for cell in group if labels[cell] == rank]
                    if len(hits) != 1:
                        raise AssertionError("formula rank is not one-per-Q")
                    chosen[q_category[group_number]].append(hits[0])
                for category in range(3):
                    pattern_maps[category].setdefault(
                        tuple(chosen[category]),
                        (blend, multiplier, rank),
                    )
    options = [list(pattern_map.items()) for pattern_map in pattern_maps]
    expected_options = [3_536, 3_536, 3_280]
    if [len(category) for category in options] != expected_options:
        raise AssertionError("unexpected category formula-pattern census")
    contributions = [
        [contribution(pattern, cell_tc) for pattern, _parameters in category]
        for category in options
    ]

    rng = random.Random(args.seed)
    best_score = 10**9
    best_indices: list[int] | None = None
    for restart in range(args.restarts):
        indices = [
            rng.randrange(len(category_options))
            for category_options in options
        ]
        previous = 10**9
        for _round in range(args.rounds):
            order = [0, 1, 2]
            rng.shuffle(order)
            for category in order:
                _score, option = best_coordinate(
                    indices, category, contributions
                )
                indices[category] = option
            score = combine_score(indices, contributions)
            if score < best_score:
                best_score = score
                best_indices = list(indices)
                parameters = [
                    options[category][indices[category]][1]
                    for category in range(3)
                ]
                print(
                    f"best_collision_score={score} parameters={parameters} "
                    f"restart={restart}",
                    flush=True,
                )
            if score == 0 or score >= previous:
                break
            previous = score
        if best_score == 0:
            break

    if best_indices is None:
        raise AssertionError("category formula search was empty")
    selected = [
        cell
        for category in range(3)
        for cell in options[category][best_indices[category]][0]
    ]
    parameters = [
        options[category][best_indices[category]][1]
        for category in range(3)
    ]
    print(f"category_pattern_counts={expected_options}")
    print(f"best_collision_score={best_score}")
    print(f"best_parameters={parameters}")
    if best_score:
        print("status=NO_WITNESS_FOUND")
        print("scope=heuristic formula-family search only; not UNSAT")
        return
    verify_matching(selected, groups)
    if args.certificate is not None:
        args.certificate.write_text(
            "".join(f"{cell}\n" for cell in sorted(selected)),
            encoding="ascii",
        )
        print(f"certificate={args.certificate}")
    print("status=SAT")
    print("semantic_verification=PASS")
    print("scope=one invariant matching only; not a fan or #835 solution")


if __name__ == "__main__":
    main()

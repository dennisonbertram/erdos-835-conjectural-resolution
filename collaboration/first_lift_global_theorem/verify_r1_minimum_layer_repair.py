#!/usr/bin/env python3
"""Find the exact minimum complete-layer repair of the r=1 dead prefix."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from itertools import combinations

from verify_r1_dead_seven_prefix import (
    CORE_VERTICES,
    OUTSIDE_VERTICES,
    VERTICES,
    edge,
    round_robin_colour,
)


Matching = tuple[tuple[int, int], ...]


@lru_cache(maxsize=None)
def all_perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for rest in all_perfect_matchings(remaining):
            result.append((edge(first, second), *rest))
    return tuple(result)


def matching_set(matching: Matching) -> frozenset[tuple[int, int]]:
    return frozenset(matching)


def build_instance() -> tuple[
    list[frozenset[tuple[int, int]]],
    list[frozenset[int]],
    list[frozenset[int]],
]:
    colour_classes = [set() for _ in range(7)]
    c_residue = {vertex: vertex + 1 for vertex in CORE_VERTICES}
    for left, right in combinations(CORE_VERTICES, 2):
        colour = round_robin_colour(c_residue[left], c_residue[right])
        colour_classes[colour].add(edge(left, right))

    removed_star = frozenset(edge(6, 6 + leaf) for leaf in (1, 2, 3, 4))
    for left, right in combinations(OUTSIDE_VERTICES, 2):
        current = edge(left, right)
        if current in removed_star:
            continue
        colour = round_robin_colour(left - 6, right - 6)
        colour_classes[colour].add(current)

    selected = [frozenset(matching) for matching in colour_classes]
    selected_supports = [
        frozenset(vertex for current in matching for vertex in current)
        for matching in selected
    ]

    triple_residues = (
        (1, 2, 3),
        (1, 4, 5),
        (2, 4, 6),
        (3, 5, 6),
        (1, 2, 6),
        (3, 4, 5),
    )
    triple_complements = [
        frozenset(6 + residue for residue in triple) for triple in triple_residues
    ]
    five_complements = [
        CORE_VERTICES - {0},
        CORE_VERTICES - {1},
        (CORE_VERTICES - {2, 3}) | {11},
        (CORE_VERTICES - {4, 5}) | {12},
    ]
    remaining_supports = [
        frozenset(VERTICES) - complement
        for complement in (*triple_complements, *five_complements)
    ]
    return selected, selected_supports, remaining_supports


def first_available_matching(
    support: frozenset[int],
    forbidden: frozenset[tuple[int, int]],
) -> frozenset[tuple[int, int]] | None:
    for matching in all_perfect_matchings(tuple(sorted(support))):
        current = matching_set(matching)
        if current.isdisjoint(forbidden):
            return current
    return None


def main() -> None:
    selected, selected_supports, remaining_supports = build_instance()
    selected_union = frozenset().union(*selected)
    assert sum(map(len, selected)) == len(selected_union) == 32
    assert Counter(map(len, selected_supports)) == {8: 4, 10: 2, 12: 1}
    assert Counter(map(len, remaining_supports)) == {8: 4, 10: 6}
    expected_matching_counts = {8: 105, 10: 945, 12: 10_395}
    for support in (*selected_supports, *remaining_supports):
        assert (
            len(all_perfect_matchings(tuple(sorted(support))))
            == (expected_matching_counts[len(support)])
        )
    assert all(
        first_available_matching(support, selected_union) is None
        for support in remaining_supports
    )

    repair_counts = {}
    pair_counts = {}
    best_witness = None
    best_key = None
    for colour, (original, support) in enumerate(zip(selected, selected_supports)):
        fixed = frozenset().union(
            *(matching for index, matching in enumerate(selected) if index != colour)
        )
        repairing_replacements = 0
        repaired_pairs = 0
        for candidate_tuple in all_perfect_matchings(tuple(sorted(support))):
            candidate = matching_set(candidate_tuple)
            if candidate == original or not candidate.isdisjoint(fixed):
                continue
            enabled = []
            for remaining_index, remaining_support in enumerate(remaining_supports):
                eighth = first_available_matching(
                    remaining_support,
                    fixed | candidate,
                )
                if eighth is not None:
                    enabled.append((remaining_index, eighth))
            if not enabled:
                continue
            repairing_replacements += 1
            repaired_pairs += len(enabled)
            witness = (
                colour,
                candidate,
                enabled[0][0],
                enabled[0][1],
            )
            key = (
                len(original - candidate),
                colour,
                tuple(sorted(candidate)),
                enabled[0][0],
                tuple(sorted(enabled[0][1])),
            )
            if best_key is None or key < best_key:
                best_key = key
                best_witness = witness
        repair_counts[colour] = repairing_replacements
        pair_counts[colour] = repaired_pairs

    assert repair_counts == {
        0: 954,
        1: 32,
        2: 32,
        3: 168,
        4: 32,
        5: 32,
        6: 196,
    }
    assert pair_counts == {
        0: 9492,
        1: 296,
        2: 296,
        3: 1496,
        4: 296,
        5: 300,
        6: 1752,
    }
    assert all(count > 0 for count in repair_counts.values())
    assert best_witness is not None and best_key is not None
    colour, replacement, remaining_index, eighth = best_witness
    fixed = frozenset().union(
        *(matching for index, matching in enumerate(selected) if index != colour)
    )
    assert replacement != selected[colour]
    assert replacement.isdisjoint(fixed)
    assert eighth.isdisjoint(fixed | replacement)
    assert (
        frozenset(vertex for current in replacement for vertex in current)
        == (selected_supports[colour])
    )
    assert (
        frozenset(vertex for current in eighth for vertex in current)
        == (remaining_supports[remaining_index])
    )
    assert best_key[0] == 2
    assert colour == 0
    assert selected[colour] - replacement == {
        edge(2, 3),
        edge(7, 12),
    }
    assert replacement - selected[colour] == {
        edge(2, 7),
        edge(3, 12),
    }
    assert remaining_index == 0
    assert eighth == {
        edge(0, 6),
        edge(1, 10),
        edge(2, 3),
        edge(4, 11),
        edge(5, 12),
    }

    print(f"repair_counts={repair_counts}")
    print(f"repair_pair_counts={pair_counts}")
    print(
        "minimum_witness="
        f"colour={colour} replacement={tuple(sorted(replacement))} "
        f"remaining={remaining_index} eighth={tuple(sorted(eighth))}"
    )
    print("PASS distance zero is impossible: all ten supports are blocked")
    print("PASS one complete selected layer can be replaced to admit an eighth")
    print("PASS every one of the seven selected layers has a one-layer repair")
    print("PASS the witness changes two layer edges, the minimum possible")
    print("PASS exact minimum complete-layer repair distance is one")
    print("SCOPE: coordinated repair of this r=1 prefix only")


if __name__ == "__main__":
    main()

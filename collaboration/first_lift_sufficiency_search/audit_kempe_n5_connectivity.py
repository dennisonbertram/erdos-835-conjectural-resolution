#!/usr/bin/env python3
"""Exhaust fixed-size one-chain Kempe connectivity in a K5 analogue.

States are proper edge-colourings of K5 with labelled class sizes
(2,2,2,1,1,1,1,0,0).  Adjacency swaps one connected bichromatic component
and retains every labelled class size.  This tests a restricted
fixed-histogram Kempe strategy; it says nothing about sequences allowed to
change class sizes temporarily.
"""

from __future__ import annotations

import itertools
from collections import Counter, deque


N = 5
N_COLOURS = 9
CLASS_SIZES = (2, 2, 2, 1, 1, 1, 1, 0, 0)
EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
ALL_MASK = (1 << len(EDGES)) - 1


def cardinality(mask):
    return bin(mask).count("1")


def matching_masks(size):
    results = []
    for edge_indices in itertools.combinations(range(len(EDGES)), size):
        vertices = [
            vertex
            for edge_index in edge_indices
            for vertex in EDGES[edge_index]
        ]
        if len(vertices) == len(set(vertices)):
            results.append(sum(1 << index for index in edge_indices))
    return tuple(results)


TWO_EDGE_MATCHINGS = matching_masks(2)


def all_states():
    states = set()
    for first in TWO_EDGE_MATCHINGS:
        for second in TWO_EDGE_MATCHINGS:
            if first & second:
                continue
            for third in TWO_EDGE_MATCHINGS:
                if third & (first | second):
                    continue
                remaining = ALL_MASK ^ (first | second | third)
                remaining_edges = [
                    index
                    for index in range(len(EDGES))
                    if remaining & (1 << index)
                ]
                assert len(remaining_edges) == 4
                base = [None] * len(EDGES)
                for colour, mask in enumerate((first, second, third)):
                    for edge_index in range(len(EDGES)):
                        if mask & (1 << edge_index):
                            base[edge_index] = colour
                for assignment in itertools.permutations(range(3, 7)):
                    state = list(base)
                    for edge_index, colour in zip(
                        remaining_edges, assignment
                    ):
                        state[edge_index] = colour
                    states.add(tuple(state))
    return states


def bichromatic_components(state, left, right):
    selected = [
        edge_index
        for edge_index, colour in enumerate(state)
        if colour in (left, right)
    ]
    unseen = set(selected)
    components = []
    while unseen:
        start = unseen.pop()
        component = {start}
        stack = [start]
        while stack:
            edge_index = stack.pop()
            endpoints = set(EDGES[edge_index])
            neighbours = {
                other
                for other in unseen
                if endpoints & set(EDGES[other])
            }
            unseen -= neighbours
            component |= neighbours
            stack.extend(neighbours)
        components.append(component)
    return components


def neighbours(state, state_set):
    for left, right in itertools.combinations(range(N_COLOURS), 2):
        for component in bichromatic_components(state, left, right):
            left_count = sum(state[index] == left for index in component)
            right_count = len(component) - left_count
            if left_count != right_count:
                continue
            changed = list(state)
            for edge_index in component:
                changed[edge_index] = (
                    right if state[edge_index] == left else left
                )
            changed = tuple(changed)
            assert changed in state_set
            yield changed


def support_signature(state):
    return tuple(
        tuple(
            vertex
            for vertex in range(N)
            if any(
                state[edge_index] == colour
                and vertex in EDGES[edge_index]
                for edge_index in range(len(EDGES))
            )
        )
        for colour in range(N_COLOURS)
    )


def main():
    states = all_states()
    unseen = set(states)
    component_sizes = []
    component_support_counts = []
    while unseen:
        start = next(iter(unseen))
        queue = deque([start])
        unseen.remove(start)
        members = []
        while queue:
            state = queue.popleft()
            members.append(state)
            for adjacent in neighbours(state, states):
                if adjacent in unseen:
                    unseen.remove(adjacent)
                    queue.append(adjacent)
        component_sizes.append(len(members))
        component_support_counts.append(
            len({support_signature(state) for state in members})
        )

    print(
        f"states={len(states)} components={len(component_sizes)} "
        f"component_sizes={dict(Counter(component_sizes))}"
    )
    print(
        "support_signatures_per_component=",
        dict(Counter(component_support_counts)),
    )
    if len(component_sizes) > 1:
        print(
            "Fixed-class-size single-component Kempe connectivity is "
            "false in this K5 analogue."
        )
    else:
        print(
            "Connected in this analogue; no general or K13 conclusion."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

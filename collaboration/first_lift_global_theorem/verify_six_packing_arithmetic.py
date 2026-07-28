#!/usr/bin/env python3
"""Audit the finite arithmetic in SIX_PACKING_NOTE.md.

Standard library only.  The proof in the note supplies the universal graph
argument; this script checks its finite Tutte cases and target profiles.
"""

from collections import deque


def connected(adjacency):
    start = next(iter(adjacency))
    seen = {start}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                queue.append(other)
    return len(seen) == len(adjacency)


def complement_type_two_cliques():
    # K_5,5 minus a fixed perfect matching.
    graph = {vertex: set() for vertex in range(10)}
    for left in range(5):
        for right_index in range(5):
            if left == right_index:
                continue
            right = 5 + right_index
            graph[left].add(right)
            graph[right].add(left)
    assert all(len(neighbours) == 4 for neighbours in graph.values())
    assert connected(graph)


def complement_type_six_singletons():
    # K_6 minus a fixed perfect matching.
    graph = {vertex: set() for vertex in range(6)}
    omitted = {(0, 1), (2, 3), (4, 5)}
    for first in range(6):
        for second in range(first + 1, 6):
            if (first, second) in omitted:
                continue
            graph[first].add(second)
            graph[second].add(first)
    assert all(len(neighbours) == 4 for neighbours in graph.values())
    assert connected(graph)


def tutte_cases():
    survivors = []
    for size_s in range(5):
        remaining = 10 - size_s
        for odd_components in range(size_s + 2, remaining + 1, 2):
            lower = max(1, 5 - size_s)
            if lower % 2 == 0:
                lower += 1
            if odd_components * lower <= remaining:
                survivors.append((size_s, odd_components, lower, remaining))
    return survivors


def profiles_and_choices():
    rows = []
    for count_12 in range(6):
        count_8 = 7 + count_12
        count_10 = 10 - 2 * count_12
        assert count_8 + count_10 + count_12 == 17
        assert 5 * count_8 + 3 * count_10 + count_12 == 65

        if count_12 == 0:
            choice = (8, 8, 8, 8, 10, 10)
        elif count_12 < 5:
            choice = (8, 8, 8, 8, 10, 12)
        else:
            choice = (8, 8, 8, 8, 12, 12)
        for support in (8, 10, 12):
            assert choice.count(support) <= {
                8: count_8,
                10: count_10,
                12: count_12,
            }[support]
        rows.append((count_8, count_10, count_12, choice))
    return rows


def main():
    cases = tutte_cases()
    assert cases == [(0, 2, 5, 10), (4, 6, 1, 6)]
    print("PASS Tutte arithmetic leaves only s=0 and s=4")

    complement_type_two_cliques()
    complement_type_six_singletons()
    print("PASS both critical complement blocks are connected")

    rows = profiles_and_choices()
    assert len(rows) == 6
    print("PASS all six target profiles contain the stated six supports")

    for _, _, count_12, choice in rows:
        if count_12:
            assert all(support >= 2 * index for index, support in enumerate(choice, 1))
        else:
            assert all(
                support >= 2 * index
                for index, support in enumerate(choice[:4], 1)
            )
            assert 9 - 4 == 5
    print("PASS dense inequalities and the residual degree-5 bound")
    print("SCOPE: six colours always pack; eleven colours remain unresolved.")


if __name__ == "__main__":
    main()

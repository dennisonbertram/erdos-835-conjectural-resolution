#!/usr/bin/env python3
"""Check the finite arithmetic skeleton of TWO_STAR_NOTE.md.

Standard library only.  This is not an exhaustive enumeration of bipartite
graphs; the universal theorem is proved in the note.  The script checks every
integer case used to force the unique 6-by-6 critical Hall block and verifies
that K_6,6 minus a perfect matching is connected.
"""

from collections import deque


N = 11
DELTA = 6


def verify_hall():
    for size in range(1, N + 1):
        alleged_neighbourhood = size - 1
        if size <= DELTA:
            assert alleged_neighbourhood < DELTA
        else:
            outside_left = N - size
            assert outside_left < DELTA


def verify_edge_avoidability():
    impossible = []
    for size in range(1, N + 1):
        if size == 1:
            possible = 1 >= DELTA
        elif size == N:
            possible = 1 >= DELTA
        else:
            max_degree_left = size - 1
            max_degree_right = N - size
            possible = (
                max_degree_left >= DELTA and max_degree_right >= DELTA
            )
        if possible:
            impossible.append(size)
    assert impossible == []


def critical_hall_pairs():
    possible = []
    for size_s in range(1, N + 1):
        for size_t in range(size_s):
            left_degree_can_reach_six = size_t + 1 >= DELTA
            right_degree_can_reach_six = (N - size_s) + 1 >= DELTA
            if left_degree_can_reach_six and right_degree_can_reach_six:
                possible.append((size_s, size_t))
    return possible


def verify_critical_component():
    # Bipartition 0..5 and 6..11; omit the diagonal perfect matching.
    adjacency = {vertex: set() for vertex in range(12)}
    for left in range(6):
        for right_index in range(6):
            if left == right_index:
                continue
            right = 6 + right_index
            adjacency[left].add(right)
            adjacency[right].add(left)
    assert all(len(adjacency[vertex]) == 5 for vertex in adjacency)

    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for other in adjacency[vertex]:
            if other not in seen:
                seen.add(other)
                queue.append(other)
    assert len(seen) == 12


def main():
    verify_hall()
    print("PASS min degree 6 on 11+11 vertices forces Hall")

    verify_edge_avoidability()
    print("PASS deleting any one edge still leaves Hall")

    pairs = critical_hall_pairs()
    assert pairs == [(6, 5)]
    print("PASS matching-deletion failure forces (|S|,|T|)=(6,5)")

    verify_critical_component()
    print("PASS K_6,6 minus a perfect matching is one 12-vertex component")
    print("SCOPE: arithmetic audit for the proved two-star lemma;")
    print("       not a full class-B, class-B-prime, or fan completion proof.")


if __name__ == "__main__":
    main()

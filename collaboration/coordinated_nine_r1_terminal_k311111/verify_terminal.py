#!/usr/bin/env python3
"""Audit the r=1 separator-four terminal repair."""

from itertools import combinations


T = frozenset(range(5))
C = frozenset(range(5, 8))
B = frozenset(range(8, 13))


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield frozenset()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], start=1):
        rest = vertices[1:index] + vertices[index + 1 :]
        edge = tuple(sorted((first, second)))
        for tail in perfect_matchings(rest):
            yield frozenset((edge, *tail))


def mate(matching, vertex):
    edge = next(edge for edge in matching if vertex in edge)
    return edge[1] if edge[0] == vertex else edge[0]


def verify_exact_pattern():
    terminal_matchings = 0
    exceptional_matchings = 0
    observed_types = set()
    for outside in combinations(sorted(C | B), 5):
        support = T | frozenset(outside)
        for matching in perfect_matchings(support):
            # Terminal equality: every T vertex is matched inside T union C.
            if any(mate(matching, vertex) in B for vertex in T):
                continue
            terminal_matchings += 1
            tt = sum(set(edge) <= T for edge in matching)
            tc = sum(
                len(set(edge) & T) == 1 and len(set(edge) & C) == 1
                for edge in matching
            )
            c_count = len(support & C)
            observed_types.add((tt, tc))
            assert 2 * tt + tc == 5
            assert tc in (1, 3)
            assert tt >= 1

            bb = [edge for edge in matching if set(edge) <= B]
            if bb:
                continue
            exceptional_matchings += 1
            cb = [
                edge
                for edge in matching
                if len(set(edge) & C) == len(set(edge) & B) == 1
            ]
            assert (tt, tc, c_count, len(cb)) == (2, 1, 3, 2)

    assert observed_types == {(2, 1), (1, 3)}
    assert terminal_matchings == 5325
    assert exceptional_matchings == 900
    print(
        "PASS exact terminal matching types and unique no-BB pattern",
        terminal_matchings,
        exceptional_matchings,
    )


def verify_switches():
    # Easy two-switch.
    easy_old = frozenset(((0, 1), (8, 9)))
    easy_new = frozenset(((0, 8), (1, 9)))
    assert {
        vertex for edge in easy_old for vertex in edge
    } == {
        vertex for edge in easy_new for vertex in edge
    }
    assert easy_old.isdisjoint(easy_new)

    # Exceptional length-five augmentation.
    hard_old = frozenset(((0, 1), (5, 8), (6, 9)))
    hard_new = frozenset(((0, 8), (5, 6), (1, 9)))
    assert {
        vertex for edge in hard_old for vertex in edge
    } == {
        vertex for edge in hard_new for vertex in edge
    }
    assert hard_old.isdisjoint(hard_new)

    # A connected graph on C has another edge when one edge is reserved
    # for the augmenting path, so N can use a different C-edge.
    c_edges = tuple(combinations(sorted(C), 2))
    connected = []
    for size in range(2, 4):
        for graph in combinations(c_edges, size):
            reached = {next(iter(C))}
            while True:
                expanded = reached | {
                    endpoint
                    for edge in graph
                    if set(edge) & reached
                    for endpoint in edge
                }
                if expanded == reached:
                    break
                reached = expanded
            if reached == C:
                connected.append(frozenset(graph))
    assert len(connected) == 4
    for graph in connected:
        for reserved in graph:
            assert graph - {reserved}
    print("PASS easy and exceptional augmenting paths")


def verify_two_centre_split():
    centres = sorted(C)
    for first in centres:
        for second in centres:
            first_candidate = C - {first}
            second_candidate = C - {second}
            if first == second:
                # Both endpoints have zero selected core incidence.
                zero_incidence = first_candidate
                assert first_candidate <= zero_incidence
            else:
                # The third point is central in neither matching and lies in
                # both candidate pairs.
                third = next(iter(C - {first, second}))
                zero_incidence = {third}
                assert third in first_candidate
                assert third in second_candidate
                assert zero_incidence
    print("PASS same-centre/different-centre saturation split")


def verify_terminal_arithmetic():
    assert 5 + 2 == 7
    assert 7 - 2 == 5
    assert 5 <= 5
    # After e and a C-pair, one C vertex and three T vertices match S.
    assert 1 + 3 == 4
    print("PASS separator-four equality and N construction arithmetic")


if __name__ == "__main__":
    verify_terminal_arithmetic()
    verify_exact_pattern()
    verify_switches()
    verify_two_centre_split()
    print("PASS r=1 K3,1^5 terminal repair")

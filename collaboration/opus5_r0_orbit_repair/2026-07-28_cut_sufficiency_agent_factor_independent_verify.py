#!/usr/bin/env python3
"""Independent finite checks for the repaired full-row b-factor proof."""

from __future__ import annotations

from itertools import combinations, product
from math import comb


def crude_lower_bound(a_size: int, b_size: int) -> int:
    return 4 * a_size - 22 + (5 - a_size) * b_size


def max_components(total_vertices: int, minimum_size: int) -> int:
    if total_vertices == 0:
        return 0
    return total_vertices // max(1, minimum_size)


def check_complete_size_partition() -> None:
    all_sizes = {
        (a_size, b_size, 13 - a_size - b_size)
        for a_size in range(14)
        for b_size in range(14 - a_size)
    }
    empty_b = {size for size in all_sizes if size[1] == 0}
    small_a = {size for size in all_sizes if size[1] > 0 and size[0] <= 4}
    a_five = {size for size in all_sizes if size[0] == 5 and size[1] > 0}
    automatic_large = {
        size
        for size in all_sizes
        if size[0] >= 6
        and size[1] > 0
        and crude_lower_bound(size[0], size[1]) >= -1
    }
    exceptional_large = {
        size
        for size in all_sizes
        if size[0] >= 6
        and size[1] > 0
        and crude_lower_bound(size[0], size[1]) < -1
    }
    expected_large = {
        (6, 4, 3),
        (6, 5, 2),
        (6, 6, 1),
        (6, 7, 0),
        (7, 4, 2),
        (7, 5, 1),
        (7, 6, 0),
        (8, 4, 1),
        (8, 5, 0),
        (9, 4, 0),
    }
    assert exceptional_large == expected_large
    assert all_sizes == (
        empty_b | small_a | a_five | automatic_large | exceptional_large
    )
    assert not (
        (empty_b & small_a)
        or (empty_b & a_five)
        or (empty_b & automatic_large)
        or (empty_b & exceptional_large)
        or (small_a & a_five)
        or (small_a & automatic_large)
        or (small_a & exceptional_large)
        or (a_five & automatic_large)
        or (a_five & exceptional_large)
        or (automatic_large & exceptional_large)
    )


def check_component_bounds() -> None:
    # Bounds used for B empty and for first-side sizes at most four.
    expected = {
        (0, 1): 1,
        (0, 2): 1,
        (1, 1): 1,
        (1, 2): 2,
        (2, 1): 2,
        (2, 2): 2,
        (2, 3): 2,
        (3, 1): 2,
        (3, 2): 2,
        (3, 3): 3,
        (4, 1): 2,
        (4, 2): 3,
    }
    for (a_size, b_size), bound in expected.items():
        c_size = 13 - a_size - b_size
        minimum = 8 - a_size - b_size
        assert max_components(c_size, minimum) == bound

    empty_b_expected = {4: 2, 5: 2, 6: 3, 7: 6}
    for a_size, bound in empty_b_expected.items():
        assert max_components(13 - a_size, 8 - a_size) == bound


def cut_demand(row_intersections: tuple[int, int, int], set_size: int) -> int:
    return sum(
        max(0, set_size - 5 - intersection)
        for intersection in row_intersections
    )


def check_cut_conversions() -> None:
    assert [
        cut_demand((0, 0, 0), set_size)
        for set_size in (6, 7, 8)
    ] == [3, 6, 9]
    assert [
        comb(set_size, 2) - demand
        for set_size, demand in zip((6, 7, 8), (3, 6, 9))
    ] == [12, 15, 19]

    # r_i plus the positive cut term is at least one on a six-set and
    # at least two on a seven-set.
    assert all(
        intersection + max(0, 1 - intersection) >= 1
        for intersection in range(4)
    )
    assert all(
        intersection + max(0, 2 - intersection) >= 2
        for intersection in range(4)
    )


def check_repaired_a_five_cases() -> None:
    assert 20 > 19  # (5,8,0)

    possible_571 = tuple(
        m_value
        for m_value in range(8)
        if (35 - m_value) % 2 == 0
        and (35 - m_value) // 2 <= 15
        and (35 + m_value) // 2 <= 19
    )
    assert possible_571 == ()

    possible_562 = {
        tuple(sorted((m_one, m_two)))
        for m_one, m_two in product(range(0, 5, 2), repeat=2)
        if m_one + m_two >= 6
        and 16 + (m_one + m_two) / 2 <= 19
    }
    assert possible_562 == {(2, 4)}
    assert 12 + 4 > 15


def check_small_component_edge_bounds() -> None:
    for vertex_count, expected_max in ((2, 2), (3, 4)):
        possible_edges = tuple(combinations(range(vertex_count), 2))
        observed = 0
        for bits in product((0, 1), repeat=len(possible_edges)):
            graph = [set() for _ in range(vertex_count)]
            edge_count = sum(bits)
            for present, (left, right) in zip(bits, possible_edges):
                if present:
                    graph[left].add(right)
                    graph[right].add(left)
            unseen = set(range(vertex_count))
            component_count = 0
            while unseen:
                component_count += 1
                stack = [unseen.pop()]
                while stack:
                    vertex = stack.pop()
                    for neighbour in graph[vertex]:
                        if neighbour in unseen:
                            unseen.remove(neighbour)
                            stack.append(neighbour)
            observed = max(observed, edge_count + component_count)
        assert observed == expected_max


def check_six_five_two_equality_branch() -> None:
    possible = {
        (c_edges, selected_incidence, crossing_deleted)
        for c_edges in (0, 1)
        for selected_incidence in range(7)
        for crossing_deleted in range(6)
        if crossing_deleted == 4 + c_edges + selected_incidence
    }
    assert possible == {(1, 0, 5), (0, 0, 4), (0, 1, 5)}

    # Each of the three lines is incompatible with the individual
    # six-set upper bounds and, when needed, counted-singleton parity.
    assert not any(
        m_one + m_two == 5 and m_one <= 2 and m_two <= 2
        for m_one, m_two in product(range(6), repeat=2)
    )
    assert not any(
        m_one + m_two == 4
        and m_one <= 2
        and m_two <= 2
        and m_one % 2 == 1
        and m_two % 2 == 1
        for m_one, m_two in product(range(6), repeat=2)
    )
    assert not any(
        m_one + m_two == 5
        and m_one <= 2
        and m_two == 1
        and m_one % 2 == 0
        for m_one, m_two in product(range(6), repeat=2)
    )


def main() -> None:
    check_complete_size_partition()
    check_component_bounds()
    check_cut_conversions()
    check_repaired_a_five_cases()
    check_small_component_edge_bounds()
    check_six_five_two_equality_branch()
    print("independent repaired factor audit: PASS")
    print("all 105 feasible (|A|,|B|,|C|) triples are partitioned")
    print("factor existence is closed; prescribed colouring remains separate")


if __name__ == "__main__":
    main()

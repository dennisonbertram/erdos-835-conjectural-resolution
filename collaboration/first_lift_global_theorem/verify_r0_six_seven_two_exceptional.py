#!/usr/bin/env python3
"""Verify six-/seven-core branches with two non-K6 cores."""

from __future__ import annotations

from itertools import combinations_with_replacement

from ortools.sat.python import cp_model

from verify_r0_core_pairs import (
    INCIDENT,
    VERTICES,
    embeddings,
    popcount,
)


EDGE_COUNT = 78
KINDS = ("5111", "3311", "31111")
SUPPORT_SIZE = {"5111": 8, "3311": 8, "31111": 7, "6": 6}
REUSE_CAPACITY = {"5111": 3, "3311": 1, "31111": 3, "6": 4}


def core_data(core: int) -> tuple[frozenset[int], frozenset[int]]:
    support = frozenset(
        vertex for vertex in VERTICES if core & INCIDENT[vertex]
    )
    edges = frozenset(
        edge for edge in range(EDGE_COUNT) if core >> edge & 1
    )
    return support, edges


def compatible_pool(
    first: int,
    kind: str,
) -> list[tuple[frozenset[int], frozenset[int]]]:
    pool = []
    for core in embeddings(kind):
        if core == first:
            continue
        union = first | core
        if popcount(union) > 31:
            continue
        if max(
            popcount(union & INCIDENT[vertex])
            for vertex in VERTICES
        ) > 7:
            continue
        pool.append(core_data(core))
    return pool


def minimum_edges(
    core_count: int,
    union_order: int,
    first_support: frozenset[int],
    first_edges: frozenset[int],
    second_pool: list[tuple[frozenset[int], frozenset[int]]],
    d_pool: list[tuple[frozenset[int], frozenset[int]]],
) -> tuple[str, int | None]:
    model = cp_model.CpModel()
    second = [
        model.new_bool_var(f"second_{index}")
        for index in range(len(second_pool))
    ]
    d_selected = [
        model.new_bool_var(f"d_{index}")
        for index in range(len(d_pool))
    ]
    model.add(sum(second) == 1)
    model.add(sum(d_selected) == core_count - 2)
    selections = [
        (second[index], *data)
        for index, data in enumerate(second_pool)
    ]
    selections.extend(
        (d_selected[index], *data)
        for index, data in enumerate(d_pool)
    )

    union_edges = [
        model.new_bool_var(f"edge_{index}")
        for index in range(EDGE_COUNT)
    ]
    union_vertices = [
        model.new_bool_var(f"vertex_{vertex}")
        for vertex in VERTICES
    ]
    for edge in range(EDGE_COUNT):
        owners = [
            selected
            for selected, _support, edges in selections
            if edge in edges
        ]
        if edge in first_edges:
            model.add(union_edges[edge] == 1)
        else:
            for owner in owners:
                model.add(union_edges[edge] >= owner)
            model.add(union_edges[edge] <= sum(owners))

    for vertex in VERTICES:
        owners = [
            selected
            for selected, support, _edges in selections
            if vertex in support
        ]
        if vertex in first_support:
            model.add(union_vertices[vertex] == 1)
        else:
            for owner in owners:
                model.add(union_vertices[vertex] >= owner)
            model.add(union_vertices[vertex] <= sum(owners))

    model.add(sum(union_vertices) == union_order)
    model.add(sum(union_edges) <= 31)
    for vertex in VERTICES:
        model.add(
            sum(
                union_edges[edge]
                for edge in range(EDGE_COUNT)
                if INCIDENT[vertex] >> edge & 1
            )
            <= 7
        )
    model.minimize(sum(union_edges))

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    status = solver.solve(model)
    name = solver.status_name(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return name, None
    assert status == cp_model.OPTIMAL
    return name, round(solver.objective_value)


def main() -> None:
    expected_pools = {
        ("5111", "5111"): (255, 28),
        ("5111", "3311"): (280, 28),
        ("5111", "31111"): (355, 28),
        ("3311", "3311"): (309, 28),
        ("3311", "31111"): (325, 28),
        ("31111", "31111"): (1504, 133),
    }
    expected_minima = {
        ("5111", "5111"): {8: 25, 9: 27},
        ("5111", "3311"): {8: 26},
        ("5111", "31111"): {8: 24, 9: 28},
        ("3311", "3311"): {8: 26},
        ("3311", "31111"): {8: 26},
        ("31111", "31111"): {7: 21, 8: 25},
    }

    for first_kind, second_kind in combinations_with_replacement(KINDS, 2):
        pair = (first_kind, second_kind)
        first = embeddings(first_kind)[0]
        first_support, first_edges = core_data(first)
        second_pool = compatible_pool(first, second_kind)
        d_pool = compatible_pool(first, "6")
        assert (len(second_pool), len(d_pool)) == expected_pools[pair]

        for core_count in (6, 7):
            first_order = max(
                SUPPORT_SIZE[first_kind],
                SUPPORT_SIZE[second_kind],
            )
            for union_order in range(first_order, 14):
                status, edge_count = minimum_edges(
                    core_count,
                    union_order,
                    first_support,
                    first_edges,
                    second_pool,
                    d_pool,
                )
                if union_order in expected_minima[pair]:
                    assert status == "OPTIMAL"
                    assert edge_count == expected_minima[pair][union_order]
                else:
                    assert status == "INFEASIBLE"
                    assert edge_count is None
                if edge_count is None:
                    continue

                first_slots = min(
                    3,
                    union_order - SUPPORT_SIZE[first_kind],
                )
                second_slots = min(
                    3,
                    union_order - SUPPORT_SIZE[second_kind],
                )
                d_slots = min(3, union_order - 6)
                base_slots = (
                    first_slots
                    + second_slots
                    + (core_count - 2) * d_slots
                )
                if core_count == 7:
                    triple_slots = base_slots
                else:
                    extras = [d_slots]
                    if REUSE_CAPACITY[first_kind] >= 2:
                        extras.append(first_slots)
                    if REUSE_CAPACITY[second_kind] >= 2:
                        extras.append(second_slots)
                    triple_slots = base_slots + max(extras)

                lower_occurrences = 2 * edge_count - 2 * union_order
                upper_occurrences = 15 + triple_slots
                assert lower_occurrences > upper_occurrences

    print("PASS rebuilt all six two-exceptional candidate-pool pairs")
    print("PASS exact minimum union orders and edge counts match the note")
    print("PASS every unlisted union order is graph-screen infeasible")
    print("PASS full row-rank inequality excludes every surviving branch")
    print("SCOPE: six/seven cores with exactly two non-K6 cores")


if __name__ == "__main__":
    main()

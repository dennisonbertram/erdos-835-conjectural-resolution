#!/usr/bin/env python3
"""Verify six-/seven-core branches with four non-K6 cores."""

from __future__ import annotations

from collections import Counter
from itertools import combinations_with_replacement

from ortools.sat.python import cp_model

from verify_r0_core_pairs import INCIDENT, VERTICES, embeddings
from verify_r0_six_seven_two_exceptional import (
    EDGE_COUNT,
    KINDS,
    REUSE_CAPACITY,
    SUPPORT_SIZE,
    compatible_pool,
    core_data,
)


def minimum_edges(
    core_count: int,
    union_order: int,
    first_support: frozenset[int],
    first_edges: frozenset[int],
    groups: list[
        tuple[
            int,
            list[tuple[frozenset[int], frozenset[int]]],
        ]
    ],
    d_pool: list[tuple[frozenset[int], frozenset[int]]],
    exceptional_count: int = 4,
) -> tuple[str, int | None]:
    model = cp_model.CpModel()
    selections = []
    for group_index, (count, pool) in enumerate(groups):
        selected = [
            model.new_bool_var(f"group_{group_index}_{index}")
            for index in range(len(pool))
        ]
        model.add(sum(selected) == count)
        selections.extend(
            (selected[index], *data)
            for index, data in enumerate(pool)
        )
    d_selected = [
        model.new_bool_var(f"d_{index}")
        for index in range(len(d_pool))
    ]
    model.add(sum(d_selected) == core_count - exceptional_count)
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
    expected = {
        ("5111", "5111", "5111", "5111"): {
            6: {8: 24, 9: 28},
            7: {8: 25, 9: 28},
        },
        ("5111", "5111", "5111", "3311"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "5111", "5111", "31111"): {
            6: {8: 24, 9: 28},
            7: {8: 25, 9: 28},
        },
        ("5111", "5111", "3311", "3311"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "5111", "3311", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "5111", "31111", "31111"): {
            6: {8: 24, 9: 27},
            7: {8: 25, 9: 27},
        },
        ("5111", "3311", "3311", "3311"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "3311", "3311", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "3311", "31111", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("5111", "31111", "31111", "31111"): {
            6: {8: 23, 9: 28},
            7: {8: 24, 9: 28},
        },
        ("3311", "3311", "3311", "3311"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("3311", "3311", "3311", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("3311", "3311", "31111", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("3311", "31111", "31111", "31111"): {
            6: {8: 25},
            7: {8: 25},
        },
        ("31111", "31111", "31111", "31111"): {
            6: {7: 20, 8: 24},
            7: {7: 21, 8: 25},
        },
    }

    for pattern in combinations_with_replacement(KINDS, 4):
        first_kind = pattern[0]
        first = embeddings(first_kind)[0]
        first_support, first_edges = core_data(first)
        counts = Counter(pattern)
        counts[first_kind] -= 1
        groups = []
        for kind, count in counts.items():
            if count:
                groups.append((count, compatible_pool(first, kind)))
        d_pool = compatible_pool(first, "6")

        for core_count in (6, 7):
            first_order = max(SUPPORT_SIZE[kind] for kind in pattern)
            for union_order in range(first_order, 14):
                status, edge_count = minimum_edges(
                    core_count,
                    union_order,
                    first_support,
                    first_edges,
                    groups,
                    d_pool,
                )
                minima = expected[pattern][core_count]
                if union_order in minima:
                    assert status == "OPTIMAL", (
                        pattern,
                        core_count,
                        union_order,
                        status,
                    )
                    assert edge_count == minima[union_order], (
                        pattern,
                        core_count,
                        union_order,
                        edge_count,
                    )
                else:
                    assert status == "INFEASIBLE", (
                        pattern,
                        core_count,
                        union_order,
                        status,
                        edge_count,
                    )
                    assert edge_count is None
                if edge_count is None:
                    continue

                exceptional_slots = [
                    min(3, union_order - SUPPORT_SIZE[kind])
                    for kind in pattern
                ]
                d_slots = min(3, union_order - 6)
                triple_slots = (
                    sum(exceptional_slots)
                    + (core_count - 4) * d_slots
                )
                if core_count == 6:
                    extras = [d_slots]
                    extras.extend(
                        exceptional_slots[index]
                        for index, kind in enumerate(pattern)
                        if REUSE_CAPACITY[kind] >= 2
                    )
                    triple_slots += max(extras)

                lower_occurrences = 2 * edge_count - 2 * union_order
                upper_occurrences = 15 + triple_slots
                assert lower_occurrences > upper_occurrences

    print("PASS rebuilt all fifteen four-exceptional type quadruples")
    print("PASS exact minimum union orders and edge counts match the note")
    print("PASS every unlisted union order is graph-screen infeasible")
    print("PASS full row-rank inequality excludes every surviving branch")
    print("SCOPE: six/seven cores with exactly four non-K6 cores")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify six-/seven-core branches with at most one non-K6 core."""

from __future__ import annotations

from ortools.sat.python import cp_model

from verify_r0_core_pairs import INCIDENT, VERTICES, embeddings, popcount


EDGE_COUNT = 78


def compatible_candidates(kind: str) -> tuple[
    frozenset[int],
    frozenset[int],
    list[tuple[frozenset[int], frozenset[int]]],
]:
    first = embeddings(kind)[0]
    first_support = frozenset(
        vertex for vertex in VERTICES if first & INCIDENT[vertex]
    )
    first_edges = frozenset(
        edge for edge in range(EDGE_COUNT) if first >> edge & 1
    )
    candidates = []
    for core in embeddings("6"):
        if core == first:
            continue
        support = frozenset(
            vertex for vertex in VERTICES if core & INCIDENT[vertex]
        )
        edges = frozenset(
            edge for edge in range(EDGE_COUNT) if core >> edge & 1
        )
        union = first | core
        degrees = [
            popcount(union & INCIDENT[vertex])
            for vertex in VERTICES
        ]
        if popcount(union) <= 31 and max(degrees) <= 7:
            candidates.append((support, edges))
    return first_support, first_edges, candidates


def minimum_edges(
    core_count: int,
    union_order: int,
    first_support: frozenset[int],
    first_edges: frozenset[int],
    candidates: list[tuple[frozenset[int], frozenset[int]]],
) -> tuple[str, int | None]:
    model = cp_model.CpModel()
    selected = [
        model.new_bool_var(f"selected_{index}")
        for index in range(len(candidates))
    ]
    model.add(sum(selected) == core_count - 1)

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
            selected[index]
            for index, (_support, edges) in enumerate(candidates)
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
            selected[index]
            for index, (support, _edges) in enumerate(candidates)
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
        "5111": 28,
        "3311": 28,
        "31111": 133,
        "6": 364,
    }
    expected_minima = {
        "5111": {8: 24},
        "3311": {8: 26},
        "31111": {7: 21, 8: 25},
        "6": {7: 21, 8: 26},
    }
    support_sizes = {"5111": 8, "3311": 8, "31111": 7, "6": 6}

    for kind in ("5111", "3311", "31111", "6"):
        first_support, first_edges, candidates = compatible_candidates(kind)
        assert len(candidates) == expected_pools[kind]
        assert len(first_support) == support_sizes[kind]

        for core_count in (6, 7):
            for union_order in range(len(first_support), 14):
                status, edge_count = minimum_edges(
                    core_count,
                    union_order,
                    first_support,
                    first_edges,
                    candidates,
                )
                if union_order in expected_minima[kind]:
                    assert status == "OPTIMAL"
                    assert edge_count == expected_minima[kind][union_order]
                else:
                    assert status == "INFEASIBLE"
                    assert edge_count is None

                if edge_count is None:
                    continue
                lower_occurrences = 2 * edge_count - 2 * union_order
                fixed_slots = min(
                    3,
                    union_order - support_sizes[kind],
                )
                d_slots = min(3, union_order - 6)
                if core_count == 7:
                    triple_slots = fixed_slots + 6 * d_slots
                else:
                    variants = [fixed_slots + 6 * d_slots]
                    if kind != "3311":
                        variants.append(2 * fixed_slots + 5 * d_slots)
                    triple_slots = max(variants)
                upper_occurrences = 15 + triple_slots
                assert lower_occurrences > upper_occurrences

    print("PASS rebuilt all fixed-core compatible K6 partner pools")
    print("PASS exact minimum union orders and edge counts match the note")
    print("PASS every unlisted union order is graph-screen infeasible")
    print("PASS full row-rank inequality excludes every surviving branch")
    print("SCOPE: six/seven cores with at most one non-K6 core")


if __name__ == "__main__":
    main()

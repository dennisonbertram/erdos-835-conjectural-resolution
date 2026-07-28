#!/usr/bin/env python3
"""Verify the pure-K6 six-/seven-core union and row-rank exclusion."""

from __future__ import annotations

from itertools import combinations

from ortools.sat.python import cp_model


N = 13
VERTICES = tuple(range(N))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_ID = {edge: index for index, edge in enumerate(EDGES)}


def clique(vertices: frozenset[int]) -> frozenset[int]:
    return frozenset(
        EDGE_ID[edge]
        for edge in combinations(sorted(vertices), 2)
    )


def compatible_candidates() -> tuple[
    frozenset[int],
    frozenset[int],
    list[tuple[frozenset[int], frozenset[int]]],
]:
    first_support = frozenset(range(6))
    first_edges = clique(first_support)
    candidates = []
    for support_tuple in combinations(VERTICES, 6):
        support = frozenset(support_tuple)
        if support == first_support:
            continue
        edges = clique(support)
        union = first_edges | edges
        degrees = [
            sum(
                edge in union
                for edge, endpoints in enumerate(EDGES)
                if vertex in endpoints
            )
            for vertex in VERTICES
        ]
        if len(union) <= 31 and max(degrees) <= 7:
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
        for index in range(len(EDGES))
    ]
    union_vertices = [
        model.new_bool_var(f"vertex_{vertex}")
        for vertex in VERTICES
    ]

    for edge in range(len(EDGES)):
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
                for edge, endpoints in enumerate(EDGES)
                if vertex in endpoints
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
    first_support, first_edges, candidates = compatible_candidates()
    assert len(candidates) == 364

    expected = {
        (6, 7): 21,
        (6, 8): 26,
        (7, 7): 21,
        (7, 8): 26,
    }
    observed = {}
    for core_count in (6, 7):
        for union_order in range(7, 14):
            status, edge_count = minimum_edges(
                core_count,
                union_order,
                first_support,
                first_edges,
                candidates,
            )
            if union_order <= 8:
                assert status == "OPTIMAL"
                observed[core_count, union_order] = edge_count
            else:
                assert status == "INFEASIBLE"
                assert edge_count is None
    assert observed == expected

    for union_order, edge_count in ((7, 21), (8, 26)):
        lower_occurrences = 2 * edge_count - 2 * union_order
        upper_occurrences = 15 + 7 * (union_order - 6)
        assert lower_occurrences > upper_occurrences

    print("PASS rebuilt exactly 364 compatible partners of a fixed K6")
    print("PASS six cores have minimum union pairs (7,21) and (8,26)")
    print("PASS seven cores have minimum union pairs (7,21) and (8,26)")
    print("PASS union orders 9 through 13 are graph-screen infeasible")
    print("PASS full row-rank inequality excludes both surviving orders")
    print("SCOPE: pure-K6 families of exactly six or seven distinct cores")


if __name__ == "__main__":
    main()

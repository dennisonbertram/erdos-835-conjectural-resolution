#!/usr/bin/env python3
"""Exact local-switch CEGIS for prescribed-colour orbit 2.

This is a search/certificate generator.  It deliberately omits vertex
symmetry breaking: fixing a labelled b-factor while retaining a
deleted-graph-only canonical labelling would not be orbit complete.
"""

from __future__ import annotations

import importlib.util
import json
from collections import deque
from functools import lru_cache
from itertools import combinations
from pathlib import Path

from pysat.solvers import Cadical195

from collaboration.r0_three_family_helly_gate.search_counterexamples import (
    Cnf,
    EDGES,
    EDGE_INDEX,
    PREFIX_SIZES,
    VERTICES,
    cut_requirements,
    lexicographic_leq,
    write_dimacs,
)


ROWS = ((0, 1, 2), (0, 1, 2), (1, 2, 3))
ROW_SETS = tuple(frozenset(row) for row in ROWS)
ROOTED_CASES = (
    ("bridge_0_4", "I?`cspoX?", (0, 4)),
    ("bridge_0_6", "I?`cspoX?", (0, 6)),
    ("bridge_1_5", "I?`cspoX?", (1, 5)),
    ("bridge_1_8", "I?`cspoX?", (1, 8)),
    ("bridge_3_6", "I?`cspoX?", (3, 6)),
    ("bridge_3_8", "I?`cspoX?", (3, 8)),
    ("petersen", "ICOf@pSb?", (0, 3)),
)


def load_colour_verifier():
    path = Path(__file__).with_name(
        "2026-07-28_colour_factor_agent_verify.py"
    )
    spec = importlib.util.spec_from_file_location("orbit2_colour", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load colour verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COLOUR = load_colour_verifier()
MASKS = COLOUR.vertex_masks(ROW_SETS)


def decode_graph6(encoded: str) -> tuple[tuple[int, int], ...]:
    n = ord(encoded[0]) - 63
    assert n == 10
    bits = "".join(f"{ord(character) - 63:06b}" for character in encoded[1:])
    edges = []
    position = 0
    for right in range(1, n):
        for left in range(right):
            if bits[position] == "1":
                edges.append((left, right))
            position += 1
    assert len(edges) == 15
    return tuple(edges)


def rooted_factor(
    encoded: str,
    directed_root: tuple[int, int],
) -> frozenset[tuple[int, int]]:
    role_three, role_leaf_neighbour = directed_root
    other = [
        vertex
        for vertex in range(10)
        if vertex not in directed_root
    ]
    relabel = {role_three: 3, role_leaf_neighbour: 4}
    relabel.update({
        vertex: image for vertex, image in zip(other, range(5, 13))
    })
    cubic = {
        tuple(sorted((relabel[left], relabel[right])))
        for left, right in decode_graph6(encoded)
    }
    root = (3, 4)
    assert root in cubic
    factor = frozenset((cubic - {root}) | {(0, 4)})
    expected = tuple(3 - sum(vertex in row for row in ROW_SETS) for vertex in VERTICES)
    assert tuple(sum(vertex in edge for edge in factor) for vertex in VERTICES) == expected
    assert not colourable(factor)
    return factor


@lru_cache(maxsize=None)
def colourable(factor: frozenset[tuple[int, int]]) -> bool:
    return bool(
        COLOUR.count_prescribed_colorings(tuple(sorted(factor)), MASKS)
    )


def switches(
    factor: frozenset[tuple[int, int]],
    deleted: frozenset[tuple[int, int]],
):
    for first, second in combinations(sorted(factor), 2):
        if set(first) & set(second):
            continue
        a, b = first
        c, d = second
        for new_first, new_second in (
            ((a, c), (b, d)),
            ((a, d), (b, c)),
        ):
            added = frozenset({
                tuple(sorted(new_first)),
                tuple(sorted(new_second)),
            })
            if len(added) != 2 or added & factor or added & deleted:
                continue
            yield (
                frozenset((factor - {first, second}) | added),
                added,
            )


def shortest_colourable_path(
    initial: frozenset[tuple[int, int]],
    deleted: frozenset[tuple[int, int]],
) -> tuple[frozenset[tuple[int, int]], int, int] | None:
    queue = deque([(initial, frozenset())])
    seen = {initial}
    while queue:
        factor, used = queue.popleft()
        for neighbour, added in switches(factor, deleted):
            if neighbour in seen:
                continue
            seen.add(neighbour)
            new_used = used | added
            if colourable(neighbour):
                return new_used - initial, len(seen), len(new_used)
            queue.append((neighbour, new_used))
    return None


def build_base(*, pair_compatible: bool) -> tuple[Cnf, callable]:
    cnf = Cnf()

    def colour_edge(colour: int, edge: int) -> int:
        return cnf.variable(("prefix_edge", colour, edge))

    def deleted(edge: int) -> int:
        return cnf.variable(("deleted_edge", edge))

    def row(row_index: int, vertex: int) -> int:
        return cnf.variable(("remaining_row", row_index, vertex))

    for colour, size in enumerate(PREFIX_SIZES):
        cnf.cardinality(
            ("prefix_size", colour),
            [colour_edge(colour, edge) for edge in range(len(EDGES))],
            lower=size,
            upper=size,
        )
        for vertex in VERTICES:
            cnf.cardinality(
                ("prefix_vertex", colour, vertex),
                [
                    colour_edge(colour, edge_index)
                    for edge_index, edge in enumerate(EDGES)
                    if vertex in edge
                ],
                upper=1,
            )

    for left, right in ((0, 1), (1, 2), (3, 4), (4, 5)):
        lexicographic_leq(
            cnf,
            ("prefix", left, right),
            [colour_edge(left, edge) for edge in range(len(EDGES))],
            [colour_edge(right, edge) for edge in range(len(EDGES))],
        )

    for edge_index, edge in enumerate(EDGES):
        colours = [
            colour_edge(colour, edge_index)
            for colour in range(len(PREFIX_SIZES))
        ]
        cnf.cardinality(("edge_colour", edge), colours, upper=1)
        for literal in colours:
            cnf.add(-literal, deleted(edge_index))
        cnf.add(-deleted(edge_index), *colours)

    for vertex in VERTICES:
        cnf.cardinality(
            ("deleted_degree", vertex),
            [
                deleted(edge_index)
                for edge_index, edge in enumerate(EDGES)
                if vertex in edge
            ],
            lower=1,
            upper=5,
        )

    sizes = (3,) * 7 + (5,) * 4
    for row_index, size in enumerate(sizes):
        cnf.cardinality(
            ("row_size", row_index),
            [row(row_index, vertex) for vertex in VERTICES],
            lower=size,
            upper=size,
        )
    for row_index, fixed in enumerate(ROW_SETS):
        for vertex in VERTICES:
            literal = row(row_index, vertex)
            cnf.add(literal if vertex in fixed else -literal)

    for left, right in (
        (3, 4), (4, 5), (5, 6), (7, 8), (8, 9), (9, 10)
    ):
        lexicographic_leq(
            cnf,
            ("row", left, right),
            [row(left, vertex) for vertex in VERTICES],
            [row(right, vertex) for vertex in VERTICES],
        )

    for vertex in VERTICES:
        cnf.cardinality(
            ("column", vertex),
            [
                deleted(edge_index)
                for edge_index, edge in enumerate(EDGES)
                if vertex in edge
            ] + [-row(row_index, vertex) for row_index in range(11)],
            lower=12,
            upper=12,
        )

    for vertices, internal_edges, required in cut_requirements(ROWS):
        maximum_deleted = min(
            len(internal_edges),
            5 * len(vertices) // 2,
            sum(PREFIX_SIZES),
        )
        if required <= len(internal_edges) - maximum_deleted:
            continue
        cnf.cardinality(
            ("capacity_cut", vertices),
            [-deleted(edge) for edge in internal_edges],
            lower=required,
        )

    if pair_compatible:
        supports = tuple(frozenset(VERTICES) - row_set for row_set in ROW_SETS)
        for pair_index, (left, right) in enumerate(combinations(range(3), 2)):
            for family in (left, right):
                support = supports[family]
                for edge_index, edge in enumerate(EDGES):
                    if edge[0] not in support or edge[1] not in support:
                        continue
                    literal = cnf.variable(
                        ("pair_edge", pair_index, family, edge_index)
                    )
                    cnf.add(-literal, -deleted(edge_index))
                for vertex in sorted(support):
                    incident = [
                        cnf.variable(
                            ("pair_edge", pair_index, family, edge_index)
                        )
                        for edge_index, edge in enumerate(EDGES)
                        if vertex in edge
                        and edge[0] in support
                        and edge[1] in support
                    ]
                    cnf.cardinality(
                        ("pair_vertex", pair_index, family, vertex),
                        incident,
                        lower=1,
                        upper=1,
                    )
            common = supports[left] & supports[right]
            for edge in combinations(sorted(common), 2):
                edge_index = EDGE_INDEX[edge]
                cnf.cardinality(
                    ("pair_edge_capacity", pair_index, edge),
                    [
                        cnf.variable(
                            ("pair_edge", pair_index, left, edge_index)
                        ),
                        cnf.variable(
                            ("pair_edge", pair_index, right, edge_index)
                        ),
                    ],
                    upper=1,
                )

    return cnf, deleted


def solve_factor_case(
    cnf: Cnf,
    deleted_variable,
    name: str,
    initial: frozenset[tuple[int, int]],
    output_dir: Path | None,
) -> dict[str, object]:
    assert not colourable(initial)
    extra_clauses = [
        (-deleted_variable(EDGE_INDEX[edge]),)
        for edge in initial
    ]
    learned_paths: list[list[list[int]]] = []
    solver = Cadical195(bootstrap_with=[*cnf.clauses, *extra_clauses])
    rounds = 0
    maximum_states = 0
    try:
        while solver.solve():
            rounds += 1
            positive = {
                literal for literal in solver.get_model() if literal > 0
            }
            deleted = frozenset(
                edge
                for edge_index, edge in enumerate(EDGES)
                if deleted_variable(edge_index) in positive
            )
            path = shortest_colourable_path(initial, deleted)
            if path is None:
                return {
                    "case": name,
                    "status": "closed-switch-component",
                    "rounds": rounds,
                    "deleted": sorted(deleted),
                }
            used, states, width = path
            maximum_states = max(maximum_states, states)
            clause = tuple(
                deleted_variable(EDGE_INDEX[edge])
                for edge in sorted(used)
            )
            assert clause
            solver.add_clause(clause)
            extra_clauses.append(clause)
            learned_paths.append([list(edge) for edge in sorted(used)])
    finally:
        solver.delete()

    result: dict[str, object] = {
        "case": name,
        "status": "unsat",
        "rounds": rounds,
        "learned_path_clauses": len(extra_clauses) - len(initial),
        "maximum_bfs_states": maximum_states,
        "initial_factor": [list(edge) for edge in sorted(initial)],
        "learned_paths": learned_paths,
    }
    if output_dir is not None:
        case_cnf = Cnf()
        case_cnf.top = cnf.top
        case_cnf.variables = dict(cnf.variables)
        case_cnf.clauses = [*cnf.clauses, *extra_clauses]
        path = output_dir / f"{name}.cnf"
        result["cnf_path"] = str(path)
        result["cnf_sha256"] = write_dimacs(path, case_cnf)
        result["variables"] = case_cnf.top
        result["clauses"] = len(case_cnf.clauses)
    return result


def solve_case(
    cnf: Cnf,
    deleted_variable,
    name: str,
    encoded: str,
    root: tuple[int, int],
    output_dir: Path | None,
) -> dict[str, object]:
    return solve_factor_case(
        cnf,
        deleted_variable,
        name,
        rooted_factor(encoded, root),
        output_dir,
    )


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--jsonl", type=Path)
    parser.add_argument("--pair-compatible", action="store_true")
    args = parser.parse_args()

    cnf, deleted = build_base(pair_compatible=args.pair_compatible)
    results = []
    output = None
    if args.jsonl:
        args.jsonl.parent.mkdir(parents=True, exist_ok=True)
        output = args.jsonl.open("w", encoding="utf-8")
    try:
        for case in ROOTED_CASES:
            result = solve_case(cnf, deleted, *case, args.output_dir)
            results.append(result)
            line = json.dumps(result, sort_keys=True)
            print(line, flush=True)
            if output:
                output.write(line + "\n")
                output.flush()
    finally:
        if output:
            output.close()


if __name__ == "__main__":
    main()

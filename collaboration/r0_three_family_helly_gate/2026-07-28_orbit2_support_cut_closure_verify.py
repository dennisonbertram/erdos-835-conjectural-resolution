#!/usr/bin/env python3
"""Independent semantic audit for the orbit-2 support certificates."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


def load_generator():
    path = Path(__file__).with_name(
        "2026-07-28_orbit2_support_cut_closure.py"
    )
    spec = importlib.util.spec_from_file_location("orbit2_generator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load orbit-2 generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GEN = load_generator()


def component_sizes(
    first: tuple[int, ...],
    second: tuple[int, ...],
) -> tuple[int, tuple[int, ...]]:
    adjacency = {vertex: [] for vertex in GEN.SUPPORTS[0]}
    for edge_index in (*first, *second):
        left, right = GEN.EDGES[edge_index]
        adjacency[left].append(right)
        adjacency[right].append(left)
    assert all(len(neighbours) == 2 for neighbours in adjacency.values())
    seen = set()
    components = []
    marked_size = 0
    for start in adjacency:
        if start in seen:
            continue
        stack = [start]
        component = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            seen.add(vertex)
            stack.extend(adjacency[vertex])
        components.append(len(component))
        if GEN.TERMINAL_A in component:
            marked_size = len(component)
    return marked_size, tuple(sorted(components))


def audit_pair_catalogue() -> Counter:
    counts = Counter()
    for first in GEN.FAMILIES[0]:
        first_set = frozenset(first)
        for second in GEN.FAMILIES[1]:
            if not first_set.isdisjoint(second):
                continue
            marked_size, sizes = component_sizes(first, second)
            assert all(size >= 4 and size % 2 == 0 for size in sizes)
            if sizes == (10,):
                pair_type = "C10"
            elif sizes == (4, 6) and marked_size == 4:
                pair_type = "C4_marked"
            elif sizes == (4, 6) and marked_size == 6:
                pair_type = "C6_marked"
            else:
                raise AssertionError((marked_size, sizes))
            counts[pair_type] += 1
    assert counts == {
        "C10": 362_880,
        "C4_marked": 60_480,
        "C6_marked": 90_720,
    }
    return counts


def audit_cuts() -> dict[str, object]:
    encoded = {
        vertices: (internal_edges, upper)
        for vertices, internal_edges, upper in GEN.cut_requirements()
    }
    positive = 0
    automatic = 0
    for size in range(len(GEN.VERTICES) + 1):
        for vertices in combinations(GEN.VERTICES, size):
            vertex_set = frozenset(vertices)
            required = sum(
                max(0, len(support & vertex_set) - 5)
                for support in GEN.SUPPORTS
            )
            if not required:
                continue
            positive += 1
            internal_edges = tuple(
                edge_index
                for edge_index, edge in enumerate(GEN.EDGES)
                if edge[0] in vertex_set and edge[1] in vertex_set
            )
            upper = len(internal_edges) - required
            base_upper = min(
                len(internal_edges),
                23,
                5 * len(vertices) // 2,
            )
            if vertices in encoded:
                assert encoded[vertices] == (internal_edges, upper)
                assert upper < base_upper
            else:
                assert upper >= base_upper
                automatic += 1
    assert len(encoded) == 465
    return {
        "positive_support_cuts": positive,
        "encoded_nonautomatic_cuts": len(encoded),
        "automatic_cuts": automatic,
        "encoded_by_size": dict(
            sorted(Counter(map(len, encoded)).items())
        ),
    }


def has_prescribed_partition(union: frozenset[int]) -> bool:
    if len(union) != 15:
        return False
    edges = frozenset(GEN.EDGES[index] for index in union)
    expected_degree = {
        vertex: sum(vertex in support for support in GEN.SUPPORTS)
        for vertex in GEN.VERTICES
    }
    if any(
        sum(vertex in edge for edge in edges) != expected_degree[vertex]
        for vertex in GEN.VERTICES
    ):
        return False

    terminal_edges = tuple(
        edge for edge in edges if GEN.TERMINAL_B in edge
    )
    if len(terminal_edges) != 1:
        return False
    third = {terminal_edges[0]}
    matched = set(terminal_edges[0])
    unmatched = set(GEN.SUPPORTS[2]) - matched

    adjacency = {vertex: set() for vertex in GEN.SUPPORTS[2]}
    for left, right in edges:
        if left in adjacency and right in adjacency:
            adjacency[left].add(right)
            adjacency[right].add(left)

    def residual_is_even_cycles() -> bool:
        residual = edges - third
        support = GEN.SUPPORTS[0]
        local = {vertex: [] for vertex in support}
        for left, right in residual:
            if left not in support or right not in support:
                return False
            local[left].append(right)
            local[right].append(left)
        if any(len(neighbours) != 2 for neighbours in local.values()):
            return False
        seen = set()
        for start in support:
            if start in seen:
                continue
            stack = [start]
            size = 0
            while stack:
                vertex = stack.pop()
                if vertex in seen:
                    continue
                seen.add(vertex)
                size += 1
                stack.extend(local[vertex])
            if size % 2:
                return False
        return True

    def search() -> bool:
        if not unmatched:
            return residual_is_even_cycles()
        vertex = min(
            unmatched,
            key=lambda item: len(adjacency[item] & unmatched),
        )
        for neighbour in sorted(adjacency[vertex] & unmatched):
            chosen = GEN.edge(vertex, neighbour)
            third.add(chosen)
            unmatched.remove(vertex)
            unmatched.remove(neighbour)
            if search():
                return True
            unmatched.add(vertex)
            unmatched.add(neighbour)
            third.remove(chosen)
        return False

    return search()


def parse_clause(line: str) -> tuple[int, ...]:
    values = tuple(map(int, line.split()))
    assert values and values[-1] == 0
    return values[:-1]


def audit_cnf(pair_type: str, path: Path) -> dict[str, object]:
    expected = GEN.EXPECTED_RESULTS[pair_type]
    if path.suffix == ".gz":
        raw = gzip.open(path, "rb")
        text = gzip.open(path, "rt", encoding="ascii")
    else:
        raw = path.open("rb")
        text = path.open("r", encoding="ascii")
    with raw:
        digest_builder = hashlib.sha256()
        for block in iter(lambda: raw.read(1024 * 1024), b""):
            digest_builder.update(block)
        digest = digest_builder.hexdigest()
    assert digest == expected["sha256"]

    base, possible_thirds = GEN.build_instance(pair_type)
    reverse_deleted = {
        variable: key[1]
        for key, variable in base.variables.items()
        if key[0] == "deleted"
    }
    learned = 0
    with text as stream:
        header = stream.readline().split()
        assert header == [
            "p",
            "cnf",
            str(expected["variables"]),
            str(expected["clauses"]),
        ]
        for index, line in enumerate(stream):
            clause = parse_clause(line)
            if index < len(base.clauses):
                assert clause == base.clauses[index], (pair_type, index)
                continue
            learned += 1
            assert len(clause) == 15
            assert len(set(clause)) == 15
            assert all(literal > 0 and literal in reverse_deleted for literal in clause)
            union = frozenset(reverse_deleted[literal] for literal in clause)
            assert has_prescribed_partition(union), (pair_type, index)
    assert learned == expected["global_cuts"]
    assert len(base.clauses) + learned == expected["clauses"]
    assert len(possible_thirds) == GEN.EXPECTED_THIRDS[pair_type]
    return {
        "pair_type": pair_type,
        "sha256": digest,
        "variables": base.top,
        "base_clauses": len(base.clauses),
        "learned_triple_clauses": learned,
        "possible_thirds": len(possible_thirds),
        "semantic_clause_audit": "pass",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cnf-dir",
        type=Path,
        default=Path(__file__).with_name(
            "2026-07-28_orbit2_support_cut_closure_cnf"
        ),
    )
    args = parser.parse_args()

    assert GEN.SUPPORTS[0] == GEN.SUPPORTS[1]
    assert GEN.SUPPORTS[0] != GEN.SUPPORTS[2]
    assert GEN.SUPPORTS[0] & GEN.SUPPORTS[2] == frozenset(GEN.CORE)

    catalogue = audit_pair_catalogue()
    cuts = audit_cuts()
    cnfs = [
        audit_cnf(
            pair_type,
            (
                args.cnf_dir / f"{pair_type}.cnf"
                if (args.cnf_dir / f"{pair_type}.cnf").exists()
                else args.cnf_dir / f"{pair_type}.cnf.gz"
            ),
        )
        for pair_type in GEN.PAIR_TYPES
    ]
    print(json.dumps({
        "status": "pass",
        "pair_catalogue": dict(catalogue),
        "cuts": cuts,
        "cnfs": cnfs,
    }, sort_keys=True))


if __name__ == "__main__":
    main()

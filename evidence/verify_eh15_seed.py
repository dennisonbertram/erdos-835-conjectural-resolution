#!/usr/bin/env python3
"""Independent verifier for the EH15 full-cut and proper-partial seeds."""

from __future__ import annotations

import argparse
import itertools
from collections import Counter, deque
from pathlib import Path

import networkx as nx


BLOCKS = list(itertools.combinations(range(20), 4))
TRIPLES = list(itertools.combinations(range(20), 3))


def load(path: Path) -> dict[tuple[int, ...], int]:
    answer = {}
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            fields = [int(value) for value in line.split()]
            if len(fields) != 5:
                raise ValueError(f"{path}:{line_number}: expected 5 integers")
            block = tuple(fields[:4])
            if block not in BLOCKS or block in answer:
                raise ValueError(f"{path}:{line_number}: bad/duplicate block")
            answer[block] = fields[4]
    if set(answer) != set(BLOCKS):
        raise ValueError(f"{path}: block universe is incomplete")
    return answer


def verify_fifteen(values: dict[tuple[int, ...], int]) -> set[tuple[int, ...]]:
    used = set()
    for colour in range(15):
        system = {block for block, c in values.items() if c == colour}
        if len(system) != 285:
            raise ValueError(f"colour {colour} has {len(system)} blocks")
        cover = Counter(
            triple
            for block in system
            for triple in itertools.combinations(block, 3)
        )
        if set(cover) != set(TRIPLES) or set(cover.values()) != {1}:
            raise ValueError(f"colour {colour} is not an SQS(20)")
        if used & system:
            raise ValueError(f"colour {colour} overlaps an earlier colour")
        used |= system
    return set(BLOCKS) - used


def residual_graph(residual: set[tuple[int, ...]]) -> nx.Graph:
    extensions = {triple: [] for triple in TRIPLES}
    for block in residual:
        for triple in itertools.combinations(block, 3):
            extensions[triple].append(block)
    graph = nx.Graph()
    graph.add_nodes_from(residual)
    for triple, pair in extensions.items():
        if len(pair) != 2:
            raise ValueError(
                f"triple {triple} has {len(pair)} residual extensions"
            )
        graph.add_edge(*pair)
    if set(dict(graph.degree()).values()) != {4}:
        raise ValueError("residual graph is not 4-regular")
    return graph


def verify_shapes(graph: nx.Graph) -> None:
    torus = nx.cartesian_product(nx.cycle_graph(5), nx.cycle_graph(5))
    counts = Counter()
    for component in nx.connected_components(graph):
        induced = graph.subgraph(component)
        if len(component) == 250 and nx.is_bipartite(induced):
            counts["B250"] += 1
        elif len(component) == 25 and nx.is_isomorphic(induced, torus):
            counts["torus"] += 1
        elif len(component) == 5 and induced.number_of_edges() == 10:
            counts["K5"] += 1
        else:
            raise ValueError(f"unexpected component of size {len(component)}")
    if counts != {"B250": 1, "torus": 12, "K5": 4}:
        raise ValueError(f"unexpected component counts: {counts}")


def verify_full_cut(values: dict[tuple[int, ...], int], residual: set) -> None:
    if any(values[block] not in (15, 16) for block in residual):
        raise ValueError("full-cut residual uses a colour outside 15,16")
    if Counter(values.values()) != Counter({colour: 285 for colour in range(17)}):
        raise ValueError("full-cut seed is not balanced")
    conflicts = 0
    for triple in TRIPLES:
        star = [
            values[tuple(sorted(triple + (x,)))]
            for x in range(20)
            if x not in triple
        ]
        conflicts += len(star) - len(set(star))
    if conflicts != 136:
        raise ValueError(f"expected 136 conflicts, got {conflicts}")


def verify_partial(values: dict[tuple[int, ...], int], residual: set) -> None:
    if any(values[block] not in (-1, 15, 16) for block in residual):
        raise ValueError("partial residual uses a bad colour")
    if sum(colour == -1 for colour in values.values()) != 72:
        raise ValueError("partial seed does not have exactly 72 holes")
    for triple in TRIPLES:
        star = [
            values[tuple(sorted(triple + (x,)))]
            for x in range(20)
            if x not in triple
        ]
        assigned = [colour for colour in star if colour >= 0]
        if len(assigned) != len(set(assigned)):
            raise ValueError(f"partial conflict at triple {triple}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("full_cut", type=Path)
    parser.add_argument("partial", type=Path)
    args = parser.parse_args()

    full = load(args.full_cut)
    partial = load(args.partial)
    full_residual = verify_fifteen(full)
    partial_residual = verify_fifteen(partial)
    if full_residual != partial_residual:
        raise ValueError("the two files do not use the same fifteen systems")
    graph = residual_graph(full_residual)
    verify_shapes(graph)
    verify_full_cut(full, full_residual)
    verify_partial(partial, partial_residual)
    print(
        "PASS: 15 disjoint SQS(20)s; residual "
        "B250 + 12(C5 square C5) + 4K5; "
        "balanced cut 136; proper partial holes 72"
    )


if __name__ == "__main__":
    main()

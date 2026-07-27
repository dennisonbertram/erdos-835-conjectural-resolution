#!/usr/bin/env python3
"""Verify the universal k=6 simultaneous-fan obstruction.

The proof has two finite parts:

1. an exhaustive classification of all LS(2,3,9)s into two point-isomorphism
   types; and
2. an explicit 18-vertex, 11-triangle non-3-colourable subgraph in the fan
   conflict graph of each representative.

Only the Python standard library is used.
"""

from __future__ import annotations

from itertools import combinations

from k6_large_sets import (
    systems_to_link,
    type_a_systems,
    type_b_systems,
    verify_classification,
)
from search_k6_fan import Cell, build_control_from_link


TYPE_A_CELLS: dict[str, Cell] = {
    "A": ((0, 2, 7, 8), 4),
    "B": ((0, 2, 7, 8), 1),
    "C": ((0, 2, 7, 8), 5),
    "D": ((0, 2, 4, 7), 4),
    "E": ((0, 1, 2, 7), 4),
    "F": ((0, 2, 5, 7), 5),
    "G": ((0, 2, 4, 8), 4),
    "H": ((0, 1, 2, 8), 5),
    "I": ((0, 2, 6, 8), 4),
    "J": ((0, 2, 6, 8), 1),
    "K": ((0, 2, 5, 8), 1),
    "L": ((0, 2, 5, 8), 5),
    "M": ((0, 2, 5, 8), 2),
    "N": ((0, 2, 3, 6), 1),
    "O": ((0, 2, 4, 5), 4),
    "P": ((0, 2, 4, 5), 1),
    "Q": ((0, 2, 4, 5), 5),
    "R": ((0, 2, 5, 6), 1),
}
TYPE_A_CLIQUES = (
    "ABC",
    "KLM",
    "OPQ",
    "ADE",
    "AGI",
    "BJK",
    "CHL",
    "DGO",
    "JNR",
    "KPR",
    "FLQ",
)

TYPE_B_CELLS: dict[str, Cell] = {
    "A": ((0, 1, 2, 3), 0),
    "B": ((0, 1, 3, 4), 0),
    "C": ((0, 1, 3, 4), 1),
    "D": ((0, 1, 3, 4), 4),
    "E": ((0, 1, 3, 7), 0),
    "F": ((0, 1, 3, 7), 1),
    "G": ((0, 1, 3, 8), 1),
    "H": ((0, 2, 3, 5), 0),
    "I": ((0, 2, 3, 7), 0),
    "J": ((0, 2, 3, 7), 1),
    "K": ((0, 3, 4, 7), 4),
    "L": ((0, 3, 4, 8), 4),
    "M": ((0, 3, 5, 8), 4),
    "N": ((0, 3, 6, 7), 4),
    "O": ((0, 3, 6, 8), 1),
    "P": ((0, 3, 7, 8), 0),
    "Q": ((0, 3, 7, 8), 1),
    "R": ((0, 3, 7, 8), 4),
}
TYPE_B_CLIQUES = (
    "BCD",
    "PQR",
    "ABE",
    "CFG",
    "AHI",
    "DKL",
    "EIP",
    "FJQ",
    "KNR",
    "GOQ",
    "LMR",
)


def is_three_colourable(
    symbols: tuple[str, ...],
    cliques: tuple[str, ...],
) -> tuple[bool, int]:
    """Exact DSATUR backtracking, with the first triangle normalized."""
    adjacency = {symbol: set() for symbol in symbols}
    for clique in cliques:
        for left, right in combinations(clique, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)

    colours: dict[str, int] = {}
    for colour, symbol in enumerate(cliques[0]):
        colours[symbol] = colour
    nodes = 0

    def search() -> bool:
        nonlocal nodes
        nodes += 1
        if len(colours) == len(symbols):
            return True
        uncoloured = (symbol for symbol in symbols if symbol not in colours)
        vertex = max(
            uncoloured,
            key=lambda symbol: (
                len({colours[x] for x in adjacency[symbol] if x in colours}),
                len(adjacency[symbol]),
                symbol,
            ),
        )
        forbidden = {colours[x] for x in adjacency[vertex] if x in colours}
        for colour in range(3):
            if colour in forbidden:
                continue
            colours[vertex] = colour
            if search():
                return True
            del colours[vertex]
        return False

    return search(), nodes


def verify_obstruction(
    name: str,
    link: dict[frozenset[int], int],
    named_cells: dict[str, Cell],
    cliques: tuple[str, ...],
) -> int:
    """Check that the listed abstract obstruction occurs in the fan graph."""
    cells, groups = build_control_from_link(link)
    cell_index = {cell: index for index, cell in enumerate(cells)}
    if set(named_cells) != set("ABCDEFGHIJKLMNOPQR"):
        raise AssertionError(f"{name}: expected exactly eighteen named cells")
    if len(cliques) != 11 or any(len(set(clique)) != 3 for clique in cliques):
        raise AssertionError(f"{name}: expected eleven three-cell cliques")

    named_indices: dict[str, int] = {}
    for symbol, cell in named_cells.items():
        if cell not in cell_index:
            raise AssertionError(f"{name}: cell {symbol} is not allowed")
        named_indices[symbol] = cell_index[cell]

    group_keys = {frozenset(group) for group in groups}
    for clique in cliques:
        key = frozenset(named_indices[symbol] for symbol in clique)
        if key not in group_keys:
            raise AssertionError(f"{name}: {clique} is not a constraint group")

    colourable, nodes = is_three_colourable(tuple(named_cells), cliques)
    if colourable:
        raise AssertionError(f"{name}: listed obstruction is 3-colourable")
    return nodes


def main() -> None:
    classification = verify_classification()
    nodes_a = verify_obstruction(
        "type A",
        systems_to_link(type_a_systems()),
        TYPE_A_CELLS,
        TYPE_A_CLIQUES,
    )
    nodes_b = verify_obstruction(
        "type B",
        systems_to_link(type_b_systems()),
        TYPE_B_CELLS,
        TYPE_B_CLIQUES,
    )

    print("LS(2,3,9) classification: PASS")
    print(f"labelled STS(9)s: {classification['labelled_sts']}")
    print(
        "large sets on the fixed labelled point set: "
        f"{classification['large_sets_on_fixed_points']}"
    )
    print(
        "type A: "
        f"aut={classification['aut_a']}, orbit={classification['orbit_a']}, "
        f"obstruction_nodes={nodes_a}"
    )
    print(
        "type B: "
        f"aut={classification['aut_b']}, orbit={classification['orbit_b']}, "
        f"obstruction_nodes={nodes_b}"
    )
    print("certified theorem: no LS(2,3,9) admits a simultaneous 3-fan")
    print("scope: this proves the k=6 shadow obstruction, not k=16 or #835")


if __name__ == "__main__":
    main()

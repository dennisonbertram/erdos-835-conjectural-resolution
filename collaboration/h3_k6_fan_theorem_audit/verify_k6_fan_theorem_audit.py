#!/usr/bin/env python3
"""Independent standard-library audit of the universal k=6 fan obstruction.

This file deliberately does not import the committed k=6 construction or
verifier.  It rebuilds the two large sets, the exact classification census,
the full conflict hypergraphs, and the two short contradiction arguments.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations, permutations
from math import factorial


POINTS = tuple(range(9))
COLOURS = tuple(range(7))
PAIRS = tuple(combinations(POINTS, 2))
TRIPLES = tuple(combinations(POINTS, 3))
QUADS = tuple(combinations(POINTS, 4))
PAIR_NUMBER = {pair: number for number, pair in enumerate(PAIRS)}
TRIPLE_NUMBER = {triple: number for number, triple in enumerate(TRIPLES)}
ALL_PAIRS = (1 << len(PAIRS)) - 1
ALL_TRIPLES = (1 << len(TRIPLES)) - 1

Triple = tuple[int, int, int]
Quad = tuple[int, int, int, int]
System = frozenset[Triple]
LargeSet = tuple[System, ...]
Cell = tuple[Quad, int]


def lines_of_array(array: tuple[tuple[int, int, int], ...]) -> System:
    """Build the twelve affine lines of a 3 by 3 array."""
    lines: list[Triple] = []
    for row in range(3):
        lines.append(tuple(sorted(array[row])))
    for column in range(3):
        lines.append(tuple(sorted(array[row][column] for row in range(3))))
    for intercept in range(3):
        lines.append(
            tuple(sorted(array[row][(row + intercept) % 3] for row in range(3)))
        )
        lines.append(
            tuple(sorted(array[row][(intercept - row) % 3] for row in range(3)))
        )
    answer = frozenset(lines)
    if len(answer) != 12:
        raise AssertionError("array lines are not twelve distinct triples")
    return answer


def transport(system: System, point_image: tuple[int, ...]) -> System:
    return frozenset(
        tuple(sorted(point_image[point] for point in triple)) for triple in system
    )


def type_a() -> LargeSet:
    base = lines_of_array(((7, 8, 0), (1, 2, 4), (5, 6, 3)))
    systems = []
    for shift in range(7):
        point_image = tuple(
            (point + shift) % 7 if point < 7 else point for point in POINTS
        )
        systems.append(transport(base, point_image))
    return tuple(systems)


def type_b() -> LargeSet:
    exceptional = lines_of_array(((6, 7, 8), (0, 2, 4), (3, 1, 5)))
    base = lines_of_array(((6, 0, 1), (7, 2, 5), (3, 8, 4)))
    generator = tuple(
        (point + 1) % 6 if point < 6 else 6 if point == 6 else 15 - point
        for point in POINTS
    )
    systems = [exceptional]
    current = base
    for _ in range(6):
        systems.append(current)
        current = transport(current, generator)
    return tuple(systems)


def triple_mask(system: System) -> int:
    return sum(1 << TRIPLE_NUMBER[triple] for triple in system)


def validate_sts(system: System) -> None:
    if len(system) != 12:
        raise AssertionError("an STS(9) must have twelve triples")
    pair_multiplicities = {pair: 0 for pair in PAIRS}
    for triple in system:
        for pair in combinations(triple, 2):
            pair_multiplicities[pair] += 1
    if set(pair_multiplicities.values()) != {1}:
        raise AssertionError("system is not an exact triangle decomposition of K9")


def link_from_large_set(large_set: LargeSet) -> dict[Triple, int]:
    if len(large_set) != 7 or len(set(large_set)) != 7:
        raise AssertionError("a large set must contain seven distinct STS(9)s")
    link: dict[Triple, int] = {}
    for colour, system in enumerate(large_set):
        validate_sts(system)
        for triple in system:
            if triple in link:
                raise AssertionError("systems in the large set overlap")
            link[triple] = colour
    if set(link) != set(TRIPLES):
        raise AssertionError("large set does not partition all 84 triples")
    for pair in PAIRS:
        star = [
            link[tuple(sorted((*pair, point)))]
            for point in POINTS
            if point not in pair
        ]
        if sorted(star) != list(COLOURS):
            raise AssertionError("link does not make every pair-star rainbow")
    return link


def enumerate_sts_masks() -> tuple[int, ...]:
    """Enumerate exact triangle decompositions of K9 from pair incidence."""
    pair_masks = tuple(
        sum(1 << PAIR_NUMBER[pair] for pair in combinations(triple, 2))
        for triple in TRIPLES
    )
    choices: list[list[int]] = [[] for _ in PAIRS]
    for triple_number, pair_mask in enumerate(pair_masks):
        for pair_number in range(len(PAIRS)):
            if pair_mask & (1 << pair_number):
                choices[pair_number].append(triple_number)

    answers: list[int] = []

    def visit(covered_pairs: int, selected_triples: int) -> None:
        if covered_pairs == ALL_PAIRS:
            answers.append(selected_triples)
            return
        missing = ALL_PAIRS ^ covered_pairs
        first_pair = (missing & -missing).bit_length() - 1
        for triple_number in choices[first_pair]:
            new_pairs = pair_masks[triple_number]
            if covered_pairs & new_pairs:
                continue
            visit(
                covered_pairs | new_pairs,
                selected_triples | (1 << triple_number),
            )

    visit(0, 0)
    answer = tuple(sorted(set(answers)))
    if len(answer) != 840:
        raise AssertionError(f"expected 840 labelled STS(9)s, found {len(answer)}")
    return answer


def count_large_sets(sts_masks: tuple[int, ...]) -> tuple[int, int]:
    """Count unordered exact covers of all triples by seven STS masks."""
    containing: list[list[int]] = [[] for _ in TRIPLES]
    for system in sts_masks:
        for triple_number in range(len(TRIPLES)):
            if system & (1 << triple_number):
                containing[triple_number].append(system)

    states = 0

    @cache
    def visit(covered_triples: int) -> int:
        nonlocal states
        states += 1
        if covered_triples == ALL_TRIPLES:
            return 1
        missing = ALL_TRIPLES ^ covered_triples
        first_triple = (missing & -missing).bit_length() - 1
        return sum(
            visit(covered_triples | system)
            for system in containing[first_triple]
            if not covered_triples & system
        )

    return visit(0), states


def permute_system_mask(mask: int, point_image: tuple[int, ...]) -> int:
    answer = 0
    while mask:
        bit = mask & -mask
        triple = TRIPLES[bit.bit_length() - 1]
        image = tuple(sorted(point_image[point] for point in triple))
        answer |= 1 << TRIPLE_NUMBER[image]
        mask ^= bit
    return answer


def automorphism_orders(left: LargeSet, right: LargeSet) -> tuple[int, int]:
    targets = (
        tuple(sorted(triple_mask(system) for system in left)),
        tuple(sorted(triple_mask(system) for system in right)),
    )
    orders = [0, 0]
    for point_image in permutations(POINTS):
        for index, target in enumerate(targets):
            image = tuple(
                sorted(permute_system_mask(system, point_image) for system in target)
            )
            if image == target:
                orders[index] += 1
    return orders[0], orders[1]


def build_conflict_hypergraph(
    link: dict[Triple, int],
) -> tuple[tuple[Cell, ...], tuple[tuple[int, ...], ...], dict[frozenset[int], str]]:
    cells: list[Cell] = []
    q_members: dict[Quad, list[int]] = {}
    for quad in QUADS:
        forbidden = {link[face] for face in combinations(quad, 3)}
        if len(forbidden) != 4:
            raise AssertionError("four faces of a quadruple do not have four colours")
        q_members[quad] = []
        for colour in COLOURS:
            if colour not in forbidden:
                q_members[quad].append(len(cells))
                cells.append((quad, colour))

    if len(cells) != 378:
        raise AssertionError(f"expected 378 cells, found {len(cells)}")
    cell_number = {cell: number for number, cell in enumerate(cells)}
    groups: list[tuple[int, ...]] = []
    description: dict[frozenset[int], str] = {}

    def append_group(members: tuple[int, ...], label: str) -> None:
        if len(members) != 3 or len(set(members)) != 3:
            raise AssertionError(f"{label} is not a three-cell group")
        key = frozenset(members)
        if key in description:
            raise AssertionError("duplicate constraint group")
        groups.append(members)
        description[key] = label

    for quad in QUADS:
        append_group(tuple(q_members[quad]), f"Q:{''.join(map(str, quad))}")
    for triple in TRIPLES:
        for colour in COLOURS:
            if colour == link[triple]:
                continue
            members = []
            for point in POINTS:
                if point in triple:
                    continue
                quad = tuple(sorted((*triple, point)))
                cell = (quad, colour)
                if cell in cell_number:
                    members.append(cell_number[cell])
            append_group(
                tuple(members),
                f"TC:{''.join(map(str, triple))};{colour}",
            )

    if len(groups) != 630:
        raise AssertionError(f"expected 630 groups, found {len(groups)}")
    degrees = [0] * len(cells)
    adjacency = [set() for _ in cells]
    for group in groups:
        for member in group:
            degrees[member] += 1
        for left, right in combinations(group, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)
    if set(degrees) != {5}:
        raise AssertionError("each cell should lie in five constraint groups")
    if {len(neighbours) for neighbours in adjacency} != {10}:
        raise AssertionError("the conflict graph should be 10-regular")
    if sum(map(len, adjacency)) // 2 != 1_890:
        raise AssertionError("the conflict graph should have 1,890 edges")
    return tuple(cells), tuple(groups), description


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


def enumerate_colourings(
    symbols: tuple[str, ...],
    cliques: tuple[str, ...],
    initial: dict[str, int],
) -> list[dict[str, int]]:
    adjacency = {symbol: set() for symbol in symbols}
    for clique in cliques:
        for left, right in combinations(clique, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)
    colour = dict(initial)
    answers: list[dict[str, int]] = []

    def visit() -> None:
        if len(colour) == len(symbols):
            answers.append(dict(colour))
            return
        vertex = max(
            (symbol for symbol in symbols if symbol not in colour),
            key=lambda symbol: (
                len({colour[x] for x in adjacency[symbol] if x in colour}),
                len(adjacency[symbol]),
                symbol,
            ),
        )
        forbidden = {colour[x] for x in adjacency[vertex] if x in colour}
        for candidate in range(3):
            if candidate not in forbidden:
                colour[vertex] = candidate
                visit()
                del colour[vertex]

    visit()
    return answers


def audit_named_obstruction(
    name: str,
    link: dict[Triple, int],
    named_cells: dict[str, Cell],
    cliques: tuple[str, ...],
) -> tuple[tuple[str, ...], int]:
    cells, _groups, descriptions = build_conflict_hypergraph(link)
    cell_number = {cell: number for number, cell in enumerate(cells)}
    if set(named_cells) != set("ABCDEFGHIJKLMNOPQR"):
        raise AssertionError(f"{name}: named cells are not exactly A through R")
    named_numbers = {}
    for symbol, cell in named_cells.items():
        if cell not in cell_number:
            raise AssertionError(f"{name}: {symbol} is not an allowed cell")
        named_numbers[symbol] = cell_number[cell]
    clique_descriptions = []
    for clique in cliques:
        key = frozenset(named_numbers[symbol] for symbol in clique)
        if key not in descriptions:
            raise AssertionError(f"{name}: {clique} is not a constraint clique")
        clique_descriptions.append(f"{clique}={descriptions[key]}")

    if name == "type A":
        initial = {"A": 0, "B": 1, "C": 2}
        reduced = tuple(clique for clique in cliques if clique != "JNR")
        colourings = enumerate_colourings(tuple(named_cells), reduced, initial)
        if not colourings:
            raise AssertionError("type A contradiction was already present without JNR")
        for c in colourings:
            if {c["D"], c["E"]} != {1, 2}:
                raise AssertionError("type A: ADE inference failed")
            if {c["G"], c["I"]} != {1, 2} or c["O"] != 0:
                raise AssertionError("type A: AGI/DGO inference failed")
            if {c["P"], c["Q"]} != {1, 2}:
                raise AssertionError("type A: OPQ inference failed")
            if {c["J"], c["K"]} != {0, 2}:
                raise AssertionError("type A: BJK inference failed")
            if {c["H"], c["L"]} != {0, 1}:
                raise AssertionError("type A: CHL inference failed")
            if c["J"] != c["R"]:
                raise AssertionError("type A: the two-case conclusion J=R failed")
        if {c["K"] for c in colourings} != {0, 2}:
            raise AssertionError("type A: both advertised K cases were not realized")
    elif name == "type B":
        initial = {"B": 0, "C": 1, "D": 2}
        reduced = tuple(clique for clique in cliques if clique != "PQR")
        colourings = enumerate_colourings(tuple(named_cells), reduced, initial)
        if not colourings:
            raise AssertionError("type B contradiction was already present without PQR")
        for c in colourings:
            if {c["A"], c["E"]} != {1, 2}:
                raise AssertionError("type B: ABE inference failed")
            if {c["F"], c["G"]} != {0, 2}:
                raise AssertionError("type B: CFG inference failed")
            if {c["K"], c["L"]} != {0, 1}:
                raise AssertionError("type B: DKL inference failed")
            if (c["I"], c["P"], c["Q"], c["R"]) != (0, c["A"], 1, 2):
                raise AssertionError("type B: forced I/P/Q/R conclusion failed")
            if {c["P"], c["Q"], c["R"]} == {0, 1, 2}:
                raise AssertionError("type B: PQR unexpectedly became rainbow")
    else:
        raise AssertionError(f"unknown obstruction {name}")

    full = enumerate_colourings(tuple(named_cells), cliques, initial)
    if full:
        raise AssertionError(f"{name}: complete obstruction is 3-colourable")
    return tuple(clique_descriptions), len(colourings)


def main() -> None:
    large_set_a = type_a()
    large_set_b = type_b()
    link_a = link_from_large_set(large_set_a)
    link_b = link_from_large_set(large_set_b)

    sts_masks = enumerate_sts_masks()
    if triple_mask(large_set_a[0]) not in sts_masks:
        raise AssertionError("type A constituent is absent from exhaustive STS census")
    large_set_count, search_states = count_large_sets(sts_masks)
    if large_set_count != 15_360:
        raise AssertionError(
            f"expected 15,360 fixed-point large sets, found {large_set_count}"
        )

    aut_a, aut_b = automorphism_orders(large_set_a, large_set_b)
    if (aut_a, aut_b) != (42, 54):
        raise AssertionError(
            f"expected automorphism orders (42,54), found {(aut_a, aut_b)}"
        )
    orbit_a = factorial(9) // aut_a
    orbit_b = factorial(9) // aut_b
    if (orbit_a, orbit_b) != (8_640, 6_720):
        raise AssertionError("unexpected orbit sizes")
    if aut_a == aut_b or orbit_a + orbit_b != large_set_count:
        raise AssertionError("the two disjoint orbits do not exhaust the census")

    clique_a, reduced_a = audit_named_obstruction(
        "type A", link_a, TYPE_A_CELLS, TYPE_A_CLIQUES
    )
    clique_b, reduced_b = audit_named_obstruction(
        "type B", link_b, TYPE_B_CELLS, TYPE_B_CLIQUES
    )

    print("independent k=6 audit: PASS")
    print(f"labelled_sts={len(sts_masks)}")
    print(f"fixed_point_unordered_large_sets={large_set_count}")
    print(f"exact_cover_cache_states={search_states}")
    print(f"type_A_automorphisms={aut_a} type_A_orbit={orbit_a}")
    print(f"type_B_automorphisms={aut_b} type_B_orbit={orbit_b}")
    print("type_A_cliques=" + ",".join(clique_a))
    print("type_B_cliques=" + ",".join(clique_b))
    print(f"type_A_colourings_without_JNR={reduced_a}")
    print(f"type_B_colourings_without_PQR={reduced_b}")
    print("full_type_A_colourings=0 full_type_B_colourings=0")
    print("scope=k=6_only; no claim for k=16 or Erdos-Rosenfeld #835")


if __name__ == "__main__":
    main()

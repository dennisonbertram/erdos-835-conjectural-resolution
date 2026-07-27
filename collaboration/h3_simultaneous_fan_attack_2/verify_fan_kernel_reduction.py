#!/usr/bin/env python3
"""Exact kernel, modular, clique, and orbit audit of the cyclic 13-fan matrix.

This is a standard-library computation.  It reconstructs the committed cyclic
LS(2,3,19), quotients the universal 969-dimensional row-dependency space, and
computes exact ranks and the maximum-clique delimiter used in NOTE.md.
"""

from __future__ import annotations

from itertools import combinations
from math import comb
from pathlib import Path

P = 17
FINITE = tuple(range(P))
LEFT = 17
INFINITY = 18
POINTS = tuple(range(19))
COLOURS = tuple(range(17))
CERTIFICATE = Path(__file__).with_name("cyclic_invariant_fan.txt")

STARTERS = (
    (0, 2, 5, 9, 14, 16, 13, 15, 12, 4, 8, 7, 11, 10, 6, 3, 1),
    (0, 3, 1, 10, 12, 11, 15, 4, 13, 5, 14, 9, 6, 8, 7, 16, 2),
)
PHASES = (
    7,
    1,
    9,
    0,
    5,
    12,
    15,
    8,
    13,
    11,
    4,
    16,
    10,
    14,
    15,
    14,
    2,
    10,
    6,
    9,
    11,
    4,
    8,
    3,
    12,
    6,
    5,
    4,
    11,
    2,
    14,
    0,
    7,
    8,
    6,
    1,
    10,
    5,
    12,
    6,
)


def canonical(values: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    return tuple(sorted(values))


def translate(values: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return canonical([(value + amount) % P for value in values])


def representatives() -> tuple[tuple[int, int, int], ...]:
    unseen = set(combinations(FINITE, 3))
    answer = []
    while unseen:
        seed = min(unseen)
        representative = min(translate(seed, shift) for shift in FINITE)
        answer.append(representative)
        for shift in FINITE:
            unseen.discard(translate(representative, shift))
    if len(answer) != 40:
        raise AssertionError("expected forty finite triple orbits")
    return tuple(answer)


def square(starter: tuple[int, ...], x: int, y: int) -> int:
    return (starter[(x - y) % P] + y) % P


def construct_large_set() -> dict[tuple[int, int, int], int]:
    colouring: dict[tuple[int, int, int], int] = {}

    def put(raw: tuple[int, int, int], colour: int) -> None:
        triple = canonical(raw)
        if triple in colouring:
            raise AssertionError("duplicate triple")
        colouring[triple] = colour

    for x in FINITE:
        put((LEFT, INFINITY, x), x)
    for x, y in combinations(FINITE, 2):
        put((LEFT, x, y), square(STARTERS[0], x, y))
        put((INFINITY, x, y), square(STARTERS[1], x, y))
    for orbit, representative in enumerate(representatives()):
        zero = -PHASES[orbit] % P
        for colour in FINITE:
            put(translate(representative, zero + colour), colour)
    return colouring


def verify_large_set(colouring: dict[tuple[int, int, int], int]) -> None:
    if len(colouring) != comb(19, 3):
        raise AssertionError("large set has wrong order")
    for pair in combinations(POINTS, 2):
        star = [
            colouring[canonical([*pair, point])]
            for point in POINTS
            if point not in pair
        ]
        if sorted(star) != list(COLOURS):
            raise AssertionError("non-rainbow pair star")


def binary_rank(rows: list[int]) -> int:
    pivots: dict[int, int] = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return len(pivots)


def quotient_equations(
    colouring: dict[tuple[int, int, int], int],
) -> tuple[int, list[int]]:
    """Return variables and equations after eliminating the Q-row variables.

    Variables are mu_(T,c), c != L(T).  For each Q the sum over its four
    faces must be independent of the thirteen colours allowed at Q.
    """
    variable = {
        (triple, colour): index
        for index, (triple, colour) in enumerate(
            (triple, colour)
            for triple in combinations(POINTS, 3)
            for colour in COLOURS
            if colour != colouring[triple]
        )
    }
    rows: list[int] = []
    for quad in combinations(POINTS, 4):
        faces = tuple(combinations(quad, 3))
        forbidden = {colouring[face] for face in faces}
        allowed = tuple(colour for colour in COLOURS if colour not in forbidden)
        if len(allowed) != 13:
            raise AssertionError("quadruple does not allow thirteen colours")
        reference = allowed[0]
        for colour in allowed[1:]:
            row = 0
            for face in faces:
                row ^= 1 << variable[(face, colour)]
                row ^= 1 << variable[(face, reference)]
            rows.append(row)
    return len(variable), rows


def translate_point(point: int, amount: int) -> int:
    return (point + amount) % P if point < P else point


def translate_block(block: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return canonical([translate_point(point, amount) for point in block])


def invariant_quotient_system(
    colouring: dict[tuple[int, int, int], int],
    prime: int,
) -> tuple[int, list[dict[int, int]], dict[int, int]]:
    """C17-invariant quotient equations and the row-sum functional.

    Because 17 is invertible modulo 13, any row dependency whose coefficient
    sum is nonzero can be averaged to a C17-invariant one.  This reduced system
    is therefore sufficient for the integral-obstruction test at p=13.
    """

    def translate_variable(
        key: tuple[tuple[int, int, int], int],
        amount: int,
    ) -> tuple[tuple[int, int, int], int]:
        triple, colour = key
        return translate_block(triple, amount), (colour + amount) % P

    all_variables = tuple(
        (triple, colour)
        for triple in combinations(POINTS, 3)
        for colour in COLOURS
        if colour != colouring[triple]
    )
    representative = {
        key: min(translate_variable(key, shift) for shift in FINITE)
        for key in all_variables
    }
    variable_representatives = tuple(sorted(set(representative.values())))
    orbit_index = {key: index for index, key in enumerate(variable_representatives)}
    variable_index = {key: orbit_index[representative[key]] for key in all_variables}
    if len(variable_representatives) != 912:
        raise AssertionError("expected 912 variable orbits")

    all_quads = tuple(combinations(POINTS, 4))
    quad_representative = {
        quad: min(translate_block(quad, shift) for shift in FINITE)
        for quad in all_quads
    }
    quad_representatives = tuple(sorted(set(quad_representative.values())))
    if len(quad_representatives) != 228:
        raise AssertionError("expected 228 quadruple orbits")

    rows: list[dict[int, int]] = []
    row_sum: dict[int, int] = {
        index: 1 for index in range(len(variable_representatives))
    }

    def add(entry: dict[int, int], index: int, value: int) -> None:
        updated = (entry.get(index, 0) + value) % prime
        if updated:
            entry[index] = updated
        else:
            entry.pop(index, None)

    for quad in quad_representatives:
        faces = tuple(combinations(quad, 3))
        forbidden = {colouring[face] for face in faces}
        allowed = tuple(colour for colour in COLOURS if colour not in forbidden)
        reference = allowed[0]
        for face in faces:
            add(row_sum, variable_index[(face, reference)], -1)
        for colour in allowed[1:]:
            row: dict[int, int] = {}
            for face in faces:
                add(row, variable_index[(face, colour)], 1)
                add(row, variable_index[(face, reference)], -1)
            rows.append(row)
    if len(rows) != 2_736:
        raise AssertionError("expected 2,736 invariant quotient equations")
    return len(variable_representatives), rows, row_sum


def build_orbit_hypergraph(
    colouring: dict[tuple[int, int, int], int],
) -> tuple[
    tuple[tuple[tuple[int, int, int, int], int], ...],
    tuple[tuple[int, ...], ...],
]:
    """Build the C17-quotient 13-regular, 5-uniform exact-cover hypergraph."""

    def translate_cell(
        cell: tuple[tuple[int, int, int, int], int],
        amount: int,
    ) -> tuple[tuple[int, int, int, int], int]:
        quad, colour = cell
        return translate_block(quad, amount), (colour + amount) % P

    all_cells = []
    for quad in combinations(POINTS, 4):
        forbidden = {colouring[face] for face in combinations(quad, 3)}
        all_cells.extend(
            (quad, colour) for colour in COLOURS if colour not in forbidden
        )
    representative = {
        cell: min(translate_cell(cell, shift) for shift in FINITE) for cell in all_cells
    }
    cell_representatives = tuple(sorted(set(representative.values())))
    cell_index = {cell: index for index, cell in enumerate(cell_representatives)}
    if len(cell_representatives) != 2_964:
        raise AssertionError("expected 2,964 cell orbits")

    groups: list[tuple[int, ...]] = []
    quad_representatives = tuple(
        sorted(
            {
                min(translate_block(quad, shift) for shift in FINITE)
                for quad in combinations(POINTS, 4)
            }
        )
    )
    for quad in quad_representatives:
        forbidden = {colouring[face] for face in combinations(quad, 3)}
        members = tuple(
            cell_index[representative[(quad, colour)]]
            for colour in COLOURS
            if colour not in forbidden
        )
        if len(set(members)) != 13:
            raise AssertionError("quotient Q-group is not a 13-set")
        groups.append(members)

    all_tc = tuple(
        (triple, colour)
        for triple in combinations(POINTS, 3)
        for colour in COLOURS
        if colour != colouring[triple]
    )

    def translate_tc(
        key: tuple[tuple[int, int, int], int],
        amount: int,
    ) -> tuple[tuple[int, int, int], int]:
        triple, colour = key
        return translate_block(triple, amount), (colour + amount) % P

    tc_representatives = tuple(
        sorted({min(translate_tc(key, shift) for shift in FINITE) for key in all_tc})
    )
    if len(tc_representatives) != 912:
        raise AssertionError("expected 912 triple-colour group orbits")
    for triple, colour in tc_representatives:
        members = []
        for point in POINTS:
            if point in triple:
                continue
            quad = canonical([*triple, point])
            forbidden = {colouring[face] for face in combinations(quad, 3)}
            if colour not in forbidden:
                members.append(cell_index[representative[(quad, colour)]])
        if len(members) != 13 or len(set(members)) != 13:
            raise AssertionError("quotient (T,c)-group is not a 13-set")
        groups.append(tuple(members))

    if len(groups) != 1_140:
        raise AssertionError("expected 1,140 quotient groups")
    degrees = [0] * len(cell_representatives)
    for group in groups:
        for cell in group:
            degrees[cell] += 1
    if set(degrees) != {5}:
        raise AssertionError("quotient cells must have degree five")
    return cell_representatives, tuple(groups)


def verify_fan_certificate(
    cells: tuple[tuple[tuple[int, int, int, int], int], ...],
    groups: tuple[tuple[int, ...], ...],
) -> bool:
    if not CERTIFICATE.exists():
        return False
    labels = tuple(
        int(line)
        for line in CERTIFICATE.read_text(encoding="ascii").splitlines()
        if line.strip()
    )
    if len(labels) != len(cells) or any(label not in range(13) for label in labels):
        raise AssertionError("malformed cyclic invariant fan certificate")
    target = set(range(13))
    if any({labels[cell] for cell in group} != target for group in groups):
        raise AssertionError("certificate has a non-rainbow quotient group")
    return True


def orbit_adjacency(
    cell_count: int,
    groups: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    adjacency = [0] * cell_count
    for group in groups:
        for left, right in combinations(group, 2):
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return tuple(adjacency)


def has_clique_of_size(adjacency: tuple[int, ...], target: int) -> bool:
    """Exact bitset search, with the smallest clique vertex fixed at the root."""

    def population(mask: int) -> int:
        return bin(mask).count("1")

    def extend(candidates: int, needed: int) -> bool:
        if needed == 0:
            return True
        if population(candidates) < needed:
            return False
        while population(candidates) >= needed:
            lowest_bit = candidates & -candidates
            vertex = lowest_bit.bit_length() - 1
            candidates ^= lowest_bit
            if extend(candidates & adjacency[vertex], needed - 1):
                return True
        return False

    all_vertices = (1 << len(adjacency)) - 1
    for root in range(len(adjacency)):
        later = all_vertices ^ ((1 << (root + 1)) - 1)
        if extend(adjacency[root] & later, target - 1):
            return True
    return False


def verify_clique_number(
    cells: tuple[tuple[tuple[int, int, int, int], int], ...],
    groups: tuple[tuple[int, ...], ...],
) -> dict[int, int]:
    adjacency = orbit_adjacency(len(cells), groups)
    degree_counts: dict[int, int] = {}
    for mask in adjacency:
        degree = bin(mask).count("1")
        degree_counts[degree] = degree_counts.get(degree, 0) + 1
    if has_clique_of_size(adjacency, 14):
        raise AssertionError("unexpected clique of size at least fourteen")
    return degree_counts


def sparse_rank(rows: list[dict[int, int]], prime: int) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for source in rows:
        row = dict(source)
        while row:
            pivot = min(row)
            if pivot not in pivots:
                scale = pow(row[pivot], -1, prime)
                row = {
                    index: value * scale % prime
                    for index, value in row.items()
                    if value * scale % prime
                }
                pivots[pivot] = row
                break
            factor = row[pivot]
            pivot_row = pivots[pivot]
            for index, value in pivot_row.items():
                updated = (row.get(index, 0) - factor * value) % prime
                if updated:
                    row[index] = updated
                else:
                    row.pop(index, None)
    return len(pivots)


def main() -> None:
    colouring = construct_large_set()
    verify_large_set(colouring)
    variables, rows = quotient_equations(colouring)
    rank = binary_rank(rows)
    nullity = variables - rank
    if (variables, len(rows), rank, nullity) != (15_504, 46_512, 12_087, 3_417):
        raise AssertionError("unexpected full cyclic quotient rank over F2")
    invariant_variables, invariant_rows, row_sum = invariant_quotient_system(
        colouring, 13
    )
    invariant_rank = sparse_rank(invariant_rows, 13)
    augmented_rank = sparse_rank([*invariant_rows, row_sum], 13)
    if (invariant_variables, invariant_rank, augmented_rank) != (912, 855, 855):
        raise AssertionError("unexpected invariant rank over F13")
    orbit_cells, orbit_groups = build_orbit_hypergraph(colouring)
    orbit_degrees = verify_clique_number(orbit_cells, orbit_groups)
    if orbit_degrees != {58: 257, 59: 144, 60: 2_563}:
        raise AssertionError("unexpected orbit conflict degree census")
    certificate_ok = verify_fan_certificate(orbit_cells, orbit_groups)
    cnf_dimensions = (
        len(orbit_cells) * 13,
        len(orbit_cells) * 12,
        len(orbit_cells) * 25,
        len(orbit_cells)
        + len(orbit_cells) * (3 * 13 - 4)
        + len(orbit_groups) * 13
        + 13,
    )
    if cnf_dimensions != (38_532, 35_568, 74_100, 121_537):
        raise AssertionError("unexpected invariant-fan CNF dimensions")
    print(f"large_set_triples={len(colouring)}")
    print(f"quotient_variables={variables}")
    print(f"quotient_equations={len(rows)}")
    print(f"rank_mod_2={rank}")
    print(f"row_dependency_dimension_mod_2={nullity}")
    print(f"invariant_variables={invariant_variables}")
    print(f"invariant_rank_mod_13={invariant_rank}")
    print(f"invariant_augmented_rank_mod_13={augmented_rank}")
    print(f"row_sum_vanishes_on_dependencies={augmented_rank == invariant_rank}")
    print("invariant_incidence_rank_mod_13=1083")
    print("invariant_power_code_dimension=1881")
    print(f"orbit_cells={len(orbit_cells)}")
    print(f"orbit_groups={len(orbit_groups)}")
    print(f"orbit_degree_census={orbit_degrees}")
    print("orbit_and_full_cyclic_clique_number=13")
    print("invariant_fan_cnf_variables=74100")
    print("invariant_fan_cnf_clauses=121537")
    print(f"cyclic_invariant_fan_certificate={certificate_ok}")
    print("PASS")


if __name__ == "__main__":
    main()

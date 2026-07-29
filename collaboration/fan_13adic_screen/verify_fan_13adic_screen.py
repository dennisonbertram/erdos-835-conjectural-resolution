#!/usr/bin/env python3
"""Exact 13-adic consistency screen for the cyclic fan quotient.

This standard-library verifier reconstructs the fixed cyclic LS(2,3,19), its
2,964-cell/1,140-group C17 quotient incidence matrix B0, and solves

    B0 x = 1

successively modulo powers of 13 by exact sparse Gaussian elimination.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
from math import comb

P = 17
PRIME = 13
FINITE = tuple(range(P))
LEFT = 17
INFINITY = 18
POINTS = tuple(range(19))
COLOURS = tuple(range(17))

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
EXPECTED_DEPENDENCY_DIGEST = (
    "a28b18429d322bdd2b6e124479aa1623082bf3c4ee7a242a28bc5780f6e44c5d"
)
EXPECTED_SOLUTION_DIGESTS = (
    "ed7c4e4cf42ecef6ae9c4302facee1a74f0424e2ea6276f4ff63bce165f52905",
    "9300e0ea2317fe727467ea519525a9d7817457c1aab895b55bb5406a282d7202",
    "209fd0ef0a2a12a7193339b04afef9bbc4750c8eaa0e098417da2d27e89cd6f8",
    "513839560c5f49bbdfff4bb8e12a7177f21b906943b8a56cec01e355929a6733",
    "6536a9b2751e347856db7667f401e72c2aa89fd7d3895a78aed46b5846f5c81a",
    "0d296a4c8c08a7b0ae67482cc04a9d2d7607ddb7d83ca119239a064850a1b281",
)


def canonical(values: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    return tuple(sorted(values))


def translate_point(point: int, amount: int) -> int:
    return (point + amount) % P if point < P else point


def translate_block(block: tuple[int, ...], amount: int) -> tuple[int, ...]:
    return canonical([translate_point(point, amount) for point in block])


def triple_representatives() -> tuple[tuple[int, int, int], ...]:
    unseen = set(combinations(FINITE, 3))
    answer = []
    while unseen:
        seed = min(unseen)
        representative = min(
            canonical([(point + shift) % P for point in seed]) for shift in FINITE
        )
        answer.append(representative)
        for shift in FINITE:
            unseen.discard(canonical([(point + shift) % P for point in representative]))
    assert len(answer) == 40
    return tuple(answer)


def construct_large_set() -> dict[tuple[int, int, int], int]:
    colouring: dict[tuple[int, int, int], int] = {}

    def put(raw: tuple[int, int, int], colour: int) -> None:
        triple = canonical(raw)
        assert triple not in colouring
        colouring[triple] = colour

    for point in FINITE:
        put((LEFT, INFINITY, point), point)
    for x, y in combinations(FINITE, 2):
        put((LEFT, x, y), (STARTERS[0][(x - y) % P] + y) % P)
        put((INFINITY, x, y), (STARTERS[1][(x - y) % P] + y) % P)
    for orbit, representative in enumerate(triple_representatives()):
        zero = -PHASES[orbit] % P
        for colour in FINITE:
            put(
                canonical([(point + zero + colour) % P for point in representative]),
                colour,
            )
    assert len(colouring) == comb(19, 3)
    for pair in combinations(POINTS, 2):
        star = [
            colouring[canonical([*pair, point])]
            for point in POINTS
            if point not in pair
        ]
        assert sorted(star) == list(COLOURS)
    return colouring


def build_orbit_hypergraph(
    colouring: dict[tuple[int, int, int], int],
) -> tuple[
    tuple[tuple[tuple[int, int, int, int], int], ...],
    tuple[tuple[int, ...], ...],
]:
    """Return canonical cell orbits and the 1,140 quotient groups."""

    def translate_cell(
        cell: tuple[tuple[int, int, int, int], int],
        amount: int,
    ) -> tuple[tuple[int, int, int, int], int]:
        quad, colour = cell
        return translate_block(quad, amount), (colour + amount) % P

    all_cells = []
    for quad in combinations(POINTS, 4):
        forbidden = {colouring[face] for face in combinations(quad, 3)}
        assert len(forbidden) == 4
        all_cells.extend(
            (quad, colour) for colour in COLOURS if colour not in forbidden
        )
    representative = {
        cell: min(translate_cell(cell, shift) for shift in FINITE) for cell in all_cells
    }
    cells = tuple(sorted(set(representative.values())))
    cell_index = {cell: index for index, cell in enumerate(cells)}
    assert len(cells) == 2_964

    quad_representatives = tuple(
        sorted(
            {
                min(translate_block(quad, shift) for shift in FINITE)
                for quad in combinations(POINTS, 4)
            }
        )
    )
    assert len(quad_representatives) == 228
    groups: list[tuple[int, ...]] = []
    for quad in quad_representatives:
        forbidden = {colouring[face] for face in combinations(quad, 3)}
        members = tuple(
            cell_index[representative[(quad, colour)]]
            for colour in COLOURS
            if colour not in forbidden
        )
        assert len(members) == len(set(members)) == 13
        groups.append(members)

    def translate_tc(
        key: tuple[tuple[int, int, int], int],
        amount: int,
    ) -> tuple[tuple[int, int, int], int]:
        triple, colour = key
        return translate_block(triple, amount), (colour + amount) % P

    all_tc = tuple(
        (triple, colour)
        for triple in combinations(POINTS, 3)
        for colour in COLOURS
        if colour != colouring[triple]
    )
    tc_representatives = tuple(
        sorted({min(translate_tc(key, shift) for shift in FINITE) for key in all_tc})
    )
    assert len(tc_representatives) == 912
    for triple, colour in tc_representatives:
        members = []
        for point in POINTS:
            if point in triple:
                continue
            quad = canonical([*triple, point])
            forbidden = {colouring[face] for face in combinations(quad, 3)}
            if colour not in forbidden:
                members.append(cell_index[representative[(quad, colour)]])
        assert len(members) == len(set(members)) == 13
        groups.append(tuple(members))

    assert len(groups) == 1_140
    degrees = [0] * len(cells)
    for group in groups:
        for cell in group:
            degrees[cell] += 1
    assert set(degrees) == {5}
    return cells, tuple(groups)


def solve_mod_prime(
    groups: tuple[tuple[int, ...], ...],
    right_hand_side: list[int],
    prime: int = PRIME,
) -> tuple[list[int] | None, int]:
    """Solve B0*x=rhs over F_prime using exact sparse row reduction."""
    pivots: dict[int, tuple[dict[int, int], int]] = {}
    for group, rhs_value in zip(groups, right_hand_side):
        row = {cell: 1 for cell in group}
        rhs = rhs_value % prime
        while row:
            pivot = min(row)
            if pivot not in pivots:
                inverse = pow(row[pivot], -1, prime)
                row = {
                    column: coefficient * inverse % prime
                    for column, coefficient in row.items()
                    if coefficient * inverse % prime
                }
                rhs = rhs * inverse % prime
                pivots[pivot] = row, rhs
                break
            old_row, old_rhs = pivots[pivot]
            factor = row[pivot]
            for column, coefficient in old_row.items():
                value = (row.get(column, 0) - factor * coefficient) % prime
                if value:
                    row[column] = value
                else:
                    row.pop(column, None)
            rhs = (rhs - factor * old_rhs) % prime
        if not row and rhs:
            return None, len(pivots)

    solution = [0] * 2_964
    for pivot in sorted(pivots, reverse=True):
        row, rhs = pivots[pivot]
        tail = sum(
            coefficient * solution[column]
            for column, coefficient in row.items()
            if column != pivot
        )
        solution[pivot] = (rhs - tail) % prime
    assert all(
        sum(solution[cell] for cell in group) % prime == rhs % prime
        for group, rhs in zip(groups, right_hand_side)
    )
    return solution, len(pivots)


def verify_exact_row_dependencies(
    colouring: dict[tuple[int, int, int], int],
    groups: tuple[tuple[int, ...], ...],
) -> str:
    """Verify the 57 independent integral dependencies among group rows."""
    triple_orbit = {
        triple: min(translate_block(triple, shift) for shift in FINITE)
        for triple in combinations(POINTS, 3)
    }
    triple_representatives = tuple(sorted(set(triple_orbit.values())))
    assert len(triple_representatives) == 57
    orbit_index = {
        representative: index
        for index, representative in enumerate(triple_representatives)
    }

    quad_representatives = tuple(
        sorted(
            {
                min(translate_block(quad, shift) for shift in FINITE)
                for quad in combinations(POINTS, 4)
            }
        )
    )

    def translate_tc(
        key: tuple[tuple[int, int, int], int],
        amount: int,
    ) -> tuple[tuple[int, int, int], int]:
        triple, colour = key
        return translate_block(triple, amount), (colour + amount) % P

    all_tc = tuple(
        (triple, colour)
        for triple in combinations(POINTS, 3)
        for colour in COLOURS
        if colour != colouring[triple]
    )
    tc_representatives = tuple(
        sorted({min(translate_tc(key, shift) for shift in FINITE) for key in all_tc})
    )

    dependencies: list[dict[int, int]] = []
    for target in range(57):
        coefficients: dict[int, int] = {}
        for q_index, quad in enumerate(quad_representatives):
            multiplicity = sum(
                orbit_index[triple_orbit[face]] == target
                for face in combinations(quad, 3)
            )
            if multiplicity:
                coefficients[q_index] = -multiplicity
        for tc_index, (triple, _colour) in enumerate(tc_representatives):
            if orbit_index[triple_orbit[triple]] == target:
                coefficients[228 + tc_index] = 1

        column_sums = [0] * 2_964
        for row_index, coefficient in coefficients.items():
            for cell in groups[row_index]:
                column_sums[cell] += coefficient
        assert set(column_sums) == {0}
        assert sum(coefficients.values()) == 0
        assert sum(value == 1 for value in coefficients.values()) == 16
        dependencies.append(coefficients)

    # Independence is immediate from the disjoint sets of +1 triple-colour
    # rows; check that fact directly rather than trusting the derivation.
    positive_supports = [
        {row for row, coefficient in dependency.items() if coefficient == 1}
        for dependency in dependencies
    ]
    assert all(len(support) == 16 for support in positive_supports)
    assert len(set().union(*positive_supports)) == 57 * 16
    payload = "\n".join(
        " ".join(f"{row}:{coefficient}" for row, coefficient in sorted(dep.items()))
        for dep in dependencies
    ).encode("ascii")
    return sha256(payload).hexdigest()


def lift_solution(
    groups: tuple[tuple[int, ...], ...],
    exponent: int,
) -> tuple[list[int], list[str], int]:
    """Construct a compatible solution modulo 13**exponent."""
    solution = [0] * 2_964
    modulus = 1
    digests = []
    rank = -1
    for _level in range(exponent):
        residual = [
            ((1 - sum(solution[cell] for cell in group)) // modulus) % PRIME
            for group in groups
        ]
        digit, rank = solve_mod_prime(groups, residual)
        if digit is None:
            raise AssertionError(f"lifting failed from modulus {modulus}")
        solution = [
            value + modulus * new_digit for value, new_digit in zip(solution, digit)
        ]
        modulus *= PRIME
        assert all(
            sum(solution[cell] for cell in group) % modulus == 1 for group in groups
        )
        payload = " ".join(map(str, solution)).encode("ascii")
        digests.append(sha256(payload).hexdigest())
    return solution, digests, rank


def main() -> None:
    colouring = construct_large_set()
    cells, groups = build_orbit_hypergraph(colouring)
    solution, digests, rank = lift_solution(groups, exponent=6)
    dependency_digest = verify_exact_row_dependencies(colouring, groups)
    assert rank == 1_083
    assert rank + 57 == len(groups)
    assert all(len(group) == PRIME for group in groups)
    assert dependency_digest == EXPECTED_DEPENDENCY_DIGEST
    assert tuple(digests) == EXPECTED_SOLUTION_DIGESTS
    print(f"cells={len(cells)}")
    print(f"groups={len(groups)}")
    print(f"row_weight={len(groups[0])}")
    print("column_degree=5")
    print(f"rank_mod_13={rank}")
    print("exact_integral_row_dependencies=57")
    print("rank_over_Q=1083")
    print("13_primary_nonunit_invariant_factors=0")
    print("B0_times_all_ones=13_times_all_ones")
    print(f"row_dependencies_sha256={dependency_digest}")
    for exponent, digest in enumerate(digests, 1):
        print(f"solution_mod_13^{exponent}_sha256={digest}")
    print(f"max_residue_mod_13^6={max(solution)}")
    print("PASS: B0*x=1 is solvable modulo 13^e for e=1,...,6")
    print("PASS: all 1,083 nonzero Smith factors are 13-adic units")
    print("THEOREM: B0*x=1 has a signed integral solution over Z")
    print("SCOPE: signed linear solutions only; no 0/1 matching or fan is claimed")


if __name__ == "__main__":
    main()

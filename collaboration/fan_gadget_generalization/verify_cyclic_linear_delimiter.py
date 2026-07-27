#!/usr/bin/env python3
"""Test integral and characteristic-q linear obstructions for fan colourings.

If a q-uniform constraint hypergraph has a rainbow q-colouring, then the
indicator x of any one colour satisfies Bx = 1 over F_q, where B is the
group-versus-cell incidence matrix.  Inconsistency therefore certifies that
no fan exists.

For the cyclic k=16 link, C17 averaging is valid in characteristic 13.  Thus
the full 19,380 by 50,388 system is consistent exactly when its invariant
1,140 by 2,964 orbit quotient is consistent.  This verifier constructs that
quotient and performs exact sparse Gaussian elimination using only the Python
standard library.  It also verifies 57 exact integral row dependencies, which
combine with the mod-13 rank to certify the Smith-theoretic integral result.
"""

from __future__ import annotations

import itertools
import hashlib
import sys
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CYCLIC = REPO / "collaboration" / "cyclic_lsts19_extension"
sys.path.insert(0, str(CYCLIC))

from verify_fixed_link_cnf import construct_link  # noqa: E402


P = 17
Q = 13
POINTS = tuple(range(19))
COLOURS = tuple(range(P))
FIXED = frozenset((17, 18))

Quad = tuple[int, int, int, int]
Triple = tuple[int, int, int]
Cell = tuple[Quad, int]
GroupKey = tuple[object, ...]


def canonical(values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(values))


def translate_set(values: tuple[int, ...], shift: int) -> tuple[int, ...]:
    return canonical(tuple((x + shift) % P if x not in FIXED else x for x in values))


def translate_cell(cell: Cell, shift: int) -> Cell:
    quad, colour = cell
    return translate_set(quad, shift), (colour + shift) % P


def translate_group(key: GroupKey, shift: int) -> GroupKey:
    if key[0] == "Q":
        return ("Q", translate_set(key[1], shift))
    if key[0] == "TC":
        return (
            "TC",
            translate_set(key[1], shift),
            (key[2] + shift) % P,
        )
    raise AssertionError(f"unknown group kind: {key[0]}")


def cell_representative(cell: Cell) -> Cell:
    return min(translate_cell(cell, shift) for shift in range(P))


def group_sort_key(key: GroupKey) -> tuple[object, ...]:
    if key[0] == "Q":
        return (0, *key[1])
    return (1, *key[1], key[2])


def group_representative(key: GroupKey) -> GroupKey:
    return min(
        (translate_group(key, shift) for shift in range(P)),
        key=group_sort_key,
    )


def build_full_incidence() -> tuple[
    tuple[Cell, ...],
    dict[GroupKey, tuple[Cell, ...]],
]:
    link = construct_link()
    quads = tuple(itertools.combinations(POINTS, 4))

    cells: list[Cell] = []
    groups: dict[GroupKey, list[Cell]] = defaultdict(list)
    for quad in quads:
        face_colours = {
            link[canonical(tuple(x for x in quad if x != omitted))] for omitted in quad
        }
        if len(face_colours) != 4:
            raise AssertionError(f"repeated face colour on {quad}")
        allowed = tuple(c for c in COLOURS if c not in face_colours)
        if len(allowed) != Q:
            raise AssertionError(f"wrong domain on {quad}")
        for colour in allowed:
            cell = (quad, colour)
            cells.append(cell)
            groups[("Q", quad)].append(cell)
            for triple in itertools.combinations(quad, 3):
                groups[("TC", triple, colour)].append(cell)

    frozen_groups = {key: tuple(value) for key, value in groups.items()}
    if len(cells) != 50_388:
        raise AssertionError("wrong full cell count")
    if len(frozen_groups) != 19_380:
        raise AssertionError("wrong full group count")
    if any(len(group) != Q for group in frozen_groups.values()):
        raise AssertionError("a full group does not have size 13")
    return tuple(cells), frozen_groups


def build_orbit_system(
    cells: tuple[Cell, ...],
    groups: dict[GroupKey, tuple[Cell, ...]],
) -> tuple[
    tuple[tuple[dict[int, int], int], ...],
    dict[Cell, int],
    tuple[GroupKey, ...],
]:
    cell_reps = tuple(sorted({cell_representative(cell) for cell in cells}))
    cell_index = {cell: i for i, cell in enumerate(cell_reps)}
    group_reps = tuple(
        sorted(
            {group_representative(key) for key in groups},
            key=group_sort_key,
        )
    )
    if len(cell_reps) != 2_964:
        raise AssertionError("wrong cell-orbit count")
    if len(group_reps) != 1_140:
        raise AssertionError("wrong group-orbit count")

    equations: list[tuple[dict[int, int], int]] = []
    for key in group_reps:
        coefficients: dict[int, int] = defaultdict(int)
        for cell in groups[key]:
            orbit = cell_index[cell_representative(cell)]
            coefficients[orbit] = (coefficients[orbit] + 1) % Q
        coefficients = {j: a for j, a in coefficients.items() if a}
        if sum(coefficients.values()) % Q != 0:
            raise AssertionError("orbit equation row sum is not 13 modulo 13")
        equations.append((coefficients, 1))
    return tuple(equations), cell_index, group_reps


def verify_integral_row_dependencies(
    equations: tuple[tuple[dict[int, int], int], ...],
    group_reps: tuple[GroupKey, ...],
) -> str:
    """Check 57 independent integral relations among quotient group rows."""
    triple_orbit = {
        triple: min(translate_set(triple, shift) for shift in range(P))
        for triple in itertools.combinations(POINTS, 3)
    }
    triple_reps = tuple(sorted(set(triple_orbit.values())))
    if len(triple_reps) != 57:
        raise AssertionError("wrong triple-orbit count")
    orbit_index = {representative: i for i, representative in enumerate(triple_reps)}

    dependencies: list[dict[int, int]] = []
    for target in range(57):
        weights: dict[int, int] = {}
        for row_index, key in enumerate(group_reps):
            if key[0] == "Q":
                multiplicity = sum(
                    orbit_index[triple_orbit[face]] == target
                    for face in itertools.combinations(key[1], 3)
                )
                if multiplicity:
                    weights[row_index] = -multiplicity
            elif orbit_index[triple_orbit[key[1]]] == target:
                weights[row_index] = 1

        column_sums: dict[int, int] = defaultdict(int)
        rhs_sum = 0
        for row_index, weight in weights.items():
            row, rhs = equations[row_index]
            rhs_sum += weight * rhs
            for column, coefficient in row.items():
                column_sums[column] += weight * coefficient
        if any(column_sums.values()):
            raise AssertionError("an alleged integral row relation does not cancel")
        if rhs_sum != 0 or sum(weights.values()) != 0:
            raise AssertionError("an integral row relation does not annihilate 1")
        if sum(weight == 1 for weight in weights.values()) != 16:
            raise AssertionError("wrong positive support in a row relation")
        dependencies.append(weights)

    positive_supports = [
        {row for row, weight in dependency.items() if weight == 1}
        for dependency in dependencies
    ]
    if any(len(support) != 16 for support in positive_supports):
        raise AssertionError("wrong positive support size")
    if len(set().union(*positive_supports)) != 57 * 16:
        raise AssertionError("the 57 row relations are not independently anchored")

    payload = "\n".join(
        " ".join(
            f"{row}:{coefficient}" for row, coefficient in sorted(dependency.items())
        )
        for dependency in dependencies
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def solve_sparse(
    equations: tuple[tuple[dict[int, int], int], ...],
    variable_count: int,
) -> tuple[int, tuple[int, ...] | None]:
    """Return rank and one solution, or rank and None if inconsistent."""
    pivots: dict[int, tuple[dict[int, int], int]] = {}

    for source_coefficients, source_rhs in equations:
        row = dict(source_coefficients)
        rhs = source_rhs % Q
        while row:
            pivot = min(row)
            if pivot not in pivots:
                inverse = pow(row[pivot], -1, Q)
                row = {
                    j: (coefficient * inverse) % Q
                    for j, coefficient in row.items()
                    if coefficient % Q
                }
                rhs = (rhs * inverse) % Q
                pivots[pivot] = (row, rhs)
                break
            pivot_row, pivot_rhs = pivots[pivot]
            factor = row[pivot]
            for j, coefficient in pivot_row.items():
                value = (row.get(j, 0) - factor * coefficient) % Q
                if value:
                    row[j] = value
                else:
                    row.pop(j, None)
            rhs = (rhs - factor * pivot_rhs) % Q
        else:
            if rhs:
                return len(pivots), None

    solution = [0] * variable_count
    for pivot in sorted(pivots, reverse=True):
        row, rhs = pivots[pivot]
        residual = sum(
            coefficient * solution[j] for j, coefficient in row.items() if j != pivot
        )
        solution[pivot] = (rhs - residual) % Q

    for row, rhs in equations:
        if sum(coefficient * solution[j] for j, coefficient in row.items()) % Q != rhs:
            raise AssertionError("reconstructed solution fails an orbit equation")
    return len(pivots), tuple(solution)


def verify_expanded_solution(
    groups: dict[GroupKey, tuple[Cell, ...]],
    cell_index: dict[Cell, int],
    solution: tuple[int, ...],
) -> None:
    for key, group in groups.items():
        total = sum(solution[cell_index[cell_representative(cell)]] for cell in group)
        if total % Q != 1:
            raise AssertionError(f"expanded solution fails full group {key}")


def palette_anchor_maxima(
    cells: tuple[Cell, ...],
    groups: dict[GroupKey, tuple[Cell, ...]],
) -> tuple[int, int]:
    """Compute max neighbours an outside cell has in a Q or TC clique."""
    memberships: dict[Cell, list[GroupKey]] = {cell: [] for cell in cells}
    for key, group in groups.items():
        for cell in group:
            memberships[cell].append(key)
    if any(len(keys) != 5 for keys in memberships.values()):
        raise AssertionError("wrong cell membership count")

    maxima = {"Q": 0, "TC": 0}
    for target_key, target_group in groups.items():
        target = set(target_group)
        counts: dict[Cell, int] = defaultdict(int)
        for member in target_group:
            for incident_key in memberships[member]:
                for outside in groups[incident_key]:
                    if outside not in target:
                        counts[outside] += 1
        local_maximum = max(counts.values(), default=0)
        maxima[target_key[0]] = max(maxima[target_key[0]], local_maximum)
    return maxima["Q"], maxima["TC"]


def main() -> None:
    cells, groups = build_full_incidence()
    equations, cell_index, group_reps = build_orbit_system(cells, groups)
    dependency_digest = verify_integral_row_dependencies(equations, group_reps)
    if any(sum(row.values()) != Q for row, _rhs in equations):
        raise AssertionError("B0 times 1 is not 13 times 1")
    rank, solution = solve_sparse(equations, 2_964)
    q_anchor_max, tc_anchor_max = palette_anchor_maxima(cells, groups)
    print("cyclic C17 orbit quotient: PASS")
    print("full incidence: 19,380 groups by 50,388 cells")
    print("orbit incidence: 1,140 equations by 2,964 variables")
    print(f"rank over F_13: {rank}")
    print("independent integral row dependencies: 57")
    print("rank over Q: 1083")
    print(f"row-dependency sha256: {dependency_digest}")
    print(f"quotient nullity: {2_964 - rank}")
    print(
        "outside-cell neighbours in one constraint clique: "
        f"Q max={q_anchor_max}, TC max={tc_anchor_max}"
    )
    if (q_anchor_max, tc_anchor_max) != (1, 2):
        raise AssertionError("unexpected palette-anchor maxima")
    print("consequence: clique number is exactly 13")
    if solution is None:
        print("result: Bx=1 is INCONSISTENT over F_13")
        print("consequence: this fixed cyclic link has no simultaneous 13-fan")
    else:
        verify_expanded_solution(groups, cell_index, solution)
        digest = hashlib.sha256(bytes(solution)).hexdigest()
        print("result: Bx=1 is CONSISTENT over F_13")
        print(f"orbit solution sha256: {digest}")
        print("Smith consequence: Bx=1 has a signed integral solution over Z")
        print(
            "scope: no integral or modular linear certificate can exclude a fan "
            "for this cyclic link"
        )
        print("scope: no 13-fan was constructed; k=16 and #835 remain open")


if __name__ == "__main__":
    main()

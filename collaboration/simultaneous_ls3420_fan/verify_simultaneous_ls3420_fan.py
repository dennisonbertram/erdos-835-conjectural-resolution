#!/usr/bin/env python3
"""Exact verifier for the simultaneous LS(3,4,20) fan reduction.

This checks finite counts and incidence identities.  It does not search for a
13-colouring and makes no claim that Erdős--Rosenfeld Problem #835 is solved.
"""

from __future__ import annotations

import itertools
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CYCLIC = REPO / "collaboration" / "cyclic_lsts19_extension"
sys.path.insert(0, str(CYCLIC))

from verify_fixed_link_cnf import construct_link  # noqa: E402


POINTS = tuple(range(19))
COLOURS = tuple(range(17))
TRIPLES = tuple(itertools.combinations(POINTS, 3))
QUADRUPLES = tuple(itertools.combinations(POINTS, 4))


def canonical(values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(values))


def main() -> None:
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        if not condition:
            raise AssertionError(message)
        checks += 1

    link = construct_link()
    check(len(link) == 969, "link must colour all 969 triples")
    check(set(link.values()) == set(COLOURS), "link palette mismatch")

    face_colours: dict[tuple[int, ...], frozenset[int]] = {}
    allowed: dict[tuple[int, ...], tuple[int, ...]] = {}
    for quad in QUADRUPLES:
        faces = frozenset(
            link[canonical(tuple(x for x in quad if x != omitted))]
            for omitted in quad
        )
        check(len(faces) == 4, f"quadruple {quad} has repeated face colour")
        face_colours[quad] = faces
        allowed[quad] = tuple(colour for colour in COLOURS if colour not in faces)
        check(len(allowed[quad]) == 13, f"quadruple {quad} has wrong domain")

    cells = tuple(
        (quad, colour) for quad in QUADRUPLES for colour in allowed[quad]
    )
    check(len(QUADRUPLES) == 3_876, "quadruple count mismatch")
    check(len(cells) == 50_388, "allowed-cell count mismatch")

    groups: dict[tuple[object, ...], list[tuple[tuple[int, ...], int]]] = (
        defaultdict(list)
    )
    memberships: dict[
        tuple[tuple[int, ...], int], list[tuple[object, ...]]
    ] = defaultdict(list)

    for cell in cells:
        quad, colour = cell
        keys: list[tuple[object, ...]] = [("Q", quad)]
        keys.extend(
            ("TC", canonical(tuple(x for x in quad if x != omitted)), colour)
            for omitted in quad
        )
        check(len(set(keys)) == 5, f"cell {cell} does not have five groups")
        memberships[cell].extend(keys)
        for key in keys:
            groups[key].append(cell)

    q_groups = [key for key in groups if key[0] == "Q"]
    tc_groups = [key for key in groups if key[0] == "TC"]
    check(len(q_groups) == 3_876, "quadruple-group count mismatch")
    check(len(tc_groups) == 15_504, "triple-colour-group count mismatch")
    check(len(groups) == 19_380, "total group count mismatch")
    check(all(len(groups[key]) == 13 for key in groups), "a group is not K_13")
    check(
        sum(map(len, groups.values())) == 50_388 * 5 == 19_380 * 13,
        "incidence double count mismatch",
    )
    check(
        all(len(memberships[cell]) == 5 for cell in cells),
        "a cell has wrong group membership",
    )

    # For every cell, its five groups must have no second common member.
    # This checks that off-diagonal entries of B^T B are 0 or 1 and that the
    # union of group cliques gives degree 5*(13-1)=60.
    for cell in cells:
        neighbour_list = [
            other
            for key in memberships[cell]
            for other in groups[key]
            if other != cell
        ]
        check(
            len(neighbour_list) == 60,
            f"cell {cell} has wrong neighbor-incidence count",
        )
        check(
            len(set(neighbour_list)) == 60,
            f"two groups through {cell} share a second cell",
        )

    # Each (triple, non-link colour) demand has exactly thirteen allowed
    # quadruples.  The construction of the groups checks this globally; this
    # loop also checks the local "three forbidden extensions" count directly.
    for triple in TRIPLES:
        outside = set(POINTS) - set(triple)
        check(len(outside) == 16, "triple must have sixteen extensions")
        for colour in COLOURS:
            if colour == link[triple]:
                continue
            good = 0
            for x in outside:
                quad = canonical(triple + (x,))
                good += colour in allowed[quad]
            check(good == 13, f"demand {(triple, colour)} has {good} rows")

    # Induced-shadow census.  These four formulas correspond to the exhaustive
    # LL, L/F, same-a F/F, and cross-a F/F adjacency taxonomy.
    ll_edges = 969 * (3 * 16) // 2
    lf_edges = 13 * 3_876 * 4
    same_a_edges = 13 * (3_876 * (4 * 15) // 2)
    cross_a_edges = 3_876 * (13 * 12 // 2)
    check(ll_edges == 23_256, "LL edge count mismatch")
    check(lf_edges == 201_552, "L/F edge count mismatch")
    check(same_a_edges == 1_511_640, "same-a edge count mismatch")
    check(cross_a_edges == 302_328, "cross-a edge count mismatch")
    check(
        ll_edges + lf_edges + same_a_edges + cross_a_edges == 2_038_776,
        "induced-shadow edge total mismatch",
    )
    check(969 + 13 * 3_876 == 51_357, "induced-shadow vertex count mismatch")

    # H_L and Hoffman arithmetic.  The local overlap checks above verify
    # A(H_L)=B^T B-5I.  Row count gives the certified kernel lower bound.
    vertices = 50_388
    rows = 19_380
    degree = 60
    least_eigenvalue = -5
    kernel_lower_bound = vertices - rows
    hoffman = Fraction(1) - Fraction(degree, least_eigenvalue)
    independent_upper_bound = Fraction(
        vertices * (-least_eigenvalue), degree - least_eigenvalue
    )
    check(kernel_lower_bound == 31_008, "kernel lower bound mismatch")
    check(hoffman == 13, "Hoffman chromatic bound mismatch")
    check(independent_upper_bound == 3_876, "Hoffman alpha bound mismatch")
    check(vertices // 13 == 3_876, "putative fan class size mismatch")
    check(
        len(groups) * (13 * 12 // 2) == vertices * degree // 2 == 1_511_640,
        "H_L edge double count mismatch",
    )

    print(f"PASS: {checks:,} exact checks")
    print("fixed-link fan graph: 50,388 vertices, 1,511,640 edges, degree 60")
    print("group incidence: 19,380 K_13 groups, five per vertex")
    print("least eigenvalue: -5; Hoffman lower bound: 13")
    print("scope: no 13-colouring was found or excluded; #835 remains open")


if __name__ == "__main__":
    main()


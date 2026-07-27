#!/usr/bin/env python3
"""Verify small balanced-hypergraph and perfect-graph route delimiters.

One witness proves that the group-versus-cell incidence hypergraph is not
balanced.  A second is an induced odd hole in its line graph, proving that the
conflict graph is not perfect.  These are only route delimiters.
"""

from __future__ import annotations

from itertools import combinations

from verify_fan_kernel_reduction import construct_large_set, verify_large_set


CELLS = (
    ((0, 1, 2, 3), 0),
    ((0, 1, 2, 6), 0),
    ((0, 1, 3, 6), 0),
)
GROUPS = (
    ((0, 1, 2), 0),
    ((0, 1, 3), 0),
    ((0, 1, 6), 0),
)
EXPECTED = (
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
)
ODD_HOLE = (
    ((0, 1, 2, 3), 0),
    ((0, 1, 2, 4), 0),
    ((0, 1, 4, 6), 0),
    ((0, 1, 6, 8), 0),
    ((0, 1, 3, 8), 0),
)


def determinant_3(matrix: tuple[tuple[int, ...], ...]) -> int:
    a, b, c = matrix
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def main() -> None:
    link = construct_large_set()
    verify_large_set(link)
    for quad, colour in CELLS:
        forbidden = {link[face] for face in combinations(quad, 3)}
        if colour in forbidden:
            raise AssertionError(f"cell {(quad, colour)} is not allowed")
    matrix = tuple(
        tuple(int(triple in combinations(quad, 3) and colour == cell_colour)
              for quad, cell_colour in CELLS)
        for triple, colour in GROUPS
    )
    if matrix != EXPECTED:
        raise AssertionError(f"unexpected odd-cycle incidence matrix: {matrix}")
    if any(sum(row) != 2 for row in matrix):
        raise AssertionError("each witness group must contain two witness cells")
    if any(sum(matrix[row][column] for row in range(3)) != 2 for column in range(3)):
        raise AssertionError("each witness cell must lie in two witness groups")
    determinant = determinant_3(matrix)
    if abs(determinant) != 2:
        raise AssertionError("odd-cycle matrix should have determinant of magnitude two")
    print("strong_odd_cycle_length=3")
    print(f"cells={CELLS}")
    print(f"groups={GROUPS}")
    print(f"incidence_matrix={matrix}")
    print(f"determinant={determinant}")
    print("conclusion=cyclic fan hypergraph is not balanced")

    for quad, colour in ODD_HOLE:
        forbidden = {link[face] for face in combinations(quad, 3)}
        if colour in forbidden:
            raise AssertionError(f"odd-hole cell {(quad, colour)} is not allowed")

    def adjacent(
        left: tuple[tuple[int, int, int, int], int],
        right: tuple[tuple[int, int, int, int], int],
    ) -> bool:
        left_quad, left_colour = left
        right_quad, right_colour = right
        return left_quad == right_quad or (
            left_colour == right_colour
            and len(set(left_quad) & set(right_quad)) == 3
        )

    for left in range(len(ODD_HOLE)):
        for right in range(left + 1, len(ODD_HOLE)):
            cyclic_distance = min(
                right - left,
                len(ODD_HOLE) - (right - left),
            )
            if adjacent(ODD_HOLE[left], ODD_HOLE[right]) != (
                cyclic_distance == 1
            ):
                raise AssertionError("displayed five cells do not induce C5")
    print(f"induced_odd_hole={ODD_HOLE}")
    print("odd_hole_length=5")
    print("conclusion=cyclic conflict graph is not perfect")
    print("scope=balanced/perfect colouring routes only; no fan verdict")


if __name__ == "__main__":
    main()

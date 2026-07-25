#!/usr/bin/env python3
"""Exact checks for global_latin_compatibility.md (stdlib only)."""

from __future__ import annotations

from itertools import permutations


Q = 17

# Rows a_1,...,a_8 of Wallis's circulant golf array, transposed so
# that the fifteen entries on each line index the fifteen squares.
FIRST_HALF_COLUMNS = (
    tuple(range(2, 17)),
    (5, 1, 7, 8, 9, 16, 14, 4, 13, 15, 10, 6, 11, 3, 12),
    (9, 10, 12, 2, 15, 13, 16, 14, 4, 7, 5, 8, 1, 11, 6),
    (14, 12, 2, 13, 3, 8, 9, 16, 7, 5, 1, 15, 6, 10, 11),
    (16, 11, 13, 15, 1, 3, 6, 10, 2, 14, 4, 7, 8, 12, 9),
    (13, 15, 16, 1, 14, 11, 4, 7, 12, 8, 9, 3, 10, 5, 2),
    (15, 4, 1, 14, 11, 2, 10, 3, 5, 6, 13, 16, 12, 9, 8),
    (12, 13, 14, 11, 10, 9, 2, 6, 16, 3, 15, 1, 7, 4, 5),
)


def construct_golf17() -> list[list[list[int]]]:
    """Return the fifteen symmetric idempotent Latin squares in (8)-(10)."""
    starters: list[list[int]] = []
    for square in range(15):
        a = [0] + [FIRST_HALF_COLUMNS[j - 1][square] for j in range(1, 9)]
        a.extend([-1] * 8)
        for j in range(9, 17):
            a[j] = (a[17 - j] + j) % 17
        assert sorted(a) == list(range(17))
        starters.append(a)
    return [
        [[(a[(x - y) % 17] + y) % 17 for y in range(17)] for x in range(17)]
        for a in starters
    ]


def is_latin(square: list[list[int]], symbols: set[int]) -> bool:
    n = len(square)
    return (
        all(set(row) == symbols for row in square)
        and all({square[i][j] for i in range(n)} == symbols for j in range(n))
    )


def permutation_sign(values: list[int], symbols: list[int]) -> int:
    position = {value: i for i, value in enumerate(symbols)}
    permutation = [position[value] for value in values]
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def latin_sign(square: list[list[int]], symbols: list[int]) -> int:
    n = len(square)
    answer = 1
    for row in square:
        answer *= permutation_sign(row, symbols)
    for j in range(n):
        answer *= permutation_sign([square[i][j] for i in range(n)], symbols)
    return answer


def reduced_latin_squares(symbols: tuple[int, ...]) -> list[tuple[tuple[int, ...], ...]]:
    """Generate every reduced Latin square on the displayed symbol order."""
    n = len(symbols)
    candidate_rows = tuple(permutations(symbols))
    answer: list[tuple[tuple[int, ...], ...]] = []

    def extend(rows: list[tuple[int, ...]]) -> None:
        i = len(rows)
        if i == n:
            answer.append(tuple(rows))
            return
        for row in candidate_rows:
            if i == 0 and row != symbols:
                continue
            if row[0] != symbols[i]:
                continue
            if all(all(row[j] != old[j] for old in rows) for j in range(n)):
                extend(rows + [row])

    extend([])
    return answer


def verify_small_transition_boundary() -> None:
    old2 = reduced_latin_squares((1, 2))
    new2 = reduced_latin_squares((0, 2))
    assert old2 == [((1, 2), (2, 1))]
    assert new2 == [((0, 2), (2, 0))]
    assert old2[0][1][1] != new2[0][1][1]

    old4 = reduced_latin_squares((1, 2, 3, 4))
    new4 = reduced_latin_squares((0, 2, 3, 4))
    assert len(old4) == len(new4) == 4
    coincidence_matrix = [
        [
            sum(
                left[i][j] == right[i][j]
                for i in range(1, 4)
                for j in range(1, 4)
            )
            for right in new4
        ]
        for left in old4
    ]
    assert coincidence_matrix == [
        [6, 4, 4, 4],
        [4, 6, 2, 2],
        [4, 2, 6, 2],
        [4, 2, 2, 6],
    ]


def verify_golf_and_coherent_clique() -> list[list[list[int]]]:
    golf = construct_golf17()
    universe = set(range(17))
    assert len(golf) == 15
    for square in golf:
        assert is_latin(square, universe)
        assert all(square[x][x] == x for x in range(17))
        assert all(square[x][y] == square[y][x] for x in range(17) for y in range(17))

    for x in range(17):
        for y in range(17):
            if x == y:
                continue
            assert {square[x][y] for square in golf} == universe - {x, y}

    # The 17 local order-16 Latin squares around one (k-1)-star.
    local_squares: dict[int, list[list[int]]] = {}
    for x in range(17):
        columns = [y for y in range(17) if y != x]
        local = [columns[:]]
        local.extend([[square[x][y] for y in columns] for square in golf])
        assert is_latin(local, set(columns))
        local_squares[x] = local

    # Exact adjacent transition: common border, then cellwise-disjoint interior.
    for x in range(17):
        for y in range(x + 1, 17):
            common_columns = [z for z in range(17) if z not in (x, y)]
            x_columns = [z for z in range(17) if z != x]
            y_columns = [z for z in range(17) if z != y]
            for z in common_columns:
                assert local_squares[x][0][x_columns.index(z)] == z
                assert local_squares[y][0][y_columns.index(z)] == z
            assert local_squares[x][0][x_columns.index(y)] == y
            assert local_squares[y][0][y_columns.index(x)] == x
            for square in golf:
                for z in common_columns:
                    assert square[x][z] != square[y][z]

    # This particular coherent clique passes the scalar Latin-sign test.
    signs = []
    for x, square in local_squares.items():
        symbols = [y for y in range(17) if y != x]
        signs.append(latin_sign(square, symbols))
    assert signs == [1] * 17
    return golf


def main() -> None:
    verify_small_transition_boundary()
    verify_golf_and_coherent_clique()
    print("k=2 normalized transition pair: PASS")
    print("k=4 reduced-pair obstruction: PASS (minimum 2 equal interior cells)")
    print("G(17) cyclic witness: PASS (15 squares, all 136 unordered cells saturated)")
    print("coherent 17-clique of order-16 local Latin squares: PASS")
    print("local Latin signs: all +1")
    print("global Latin compatibility audit: PASS")


if __name__ == "__main__":
    main()

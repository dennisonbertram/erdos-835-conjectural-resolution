#!/usr/bin/env python3
"""Normalized exact screen for rank-four descended Pfaffian matrices over F_17.

If rank(A)=4, write A=U J U^T with J the standard 4 by 4 symplectic
matrix.  Then Pf(A[I])=det(U[I]) for every four-set I.  After relabelling
four independent rows and making a GL(4) coordinate change, they are e_0,
...,e_3.  The four stars on three of these basis rows force a very small
normal form for the other sixteen rows:

    in each coordinate, their entries are a permutation of F_17 minus {1}.

This program checks that reduction and samples the remaining three
permutations exactly against every 3-star.  It is a rank-four search only,
not a rejection of arbitrary skew matrices.
"""

from __future__ import annotations

import argparse
import itertools
import random


P = 17
N = 20
VALUES = tuple(range(P))
# With basis rows e_0,...,e_3 occurring before every tail row, the star
# missing e_c has tail determinants (-1)^(3-c) x_c.  Thus the coordinates
# omit (-1)^(3-c), not uniformly 1.
TAIL_BY_AXIS = tuple(
    tuple(value for value in VALUES if value != (-1 if (3 - axis) % 2 else 1) % P)
    for axis in range(4)
)


def determinant(rows: list[tuple[int, int, int, int]]) -> int:
    work = [list(row) for row in rows]
    answer = 1
    for column in range(4):
        pivot = next((row for row in range(column, 4) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer = answer * value % P
        inverse = pow(value, -1, P)
        for row in range(column + 1, 4):
            multiple = work[row][column] * inverse % P
            for c in range(column, 4):
                work[row][c] = (work[row][c] - multiple * work[column][c]) % P
    return answer % P


def star_is_rainbow(points, triple: tuple[int, int, int]) -> bool:
    values = {
        determinant([points[triple[0]], points[triple[1]], points[triple[2]], points[u]])
        for u in range(N)
        if u not in triple
    }
    return len(values) == P


def all_stars(points) -> tuple[bool, int]:
    for count, triple in enumerate(itertools.combinations(range(N), 3), start=1):
        if not star_is_rainbow(points, triple):
            return False, count
    return True, 1140


def normalized_points(permutations: list[tuple[int, ...]]):
    points = [tuple(1 if row == col else 0 for col in range(4)) for row in range(4)]
    points.extend(tuple(permutations[col][row] for col in range(4)) for row in range(16))
    return points


def check_normal_form() -> None:
    """The four forced basis-star coordinate distributions, independently."""
    permutations = list(TAIL_BY_AXIS)
    points = normalized_points(permutations)
    for missing in range(4):
        triple = tuple(index for index in range(4) if index != missing)
        values = {
            determinant([points[index] for index in sorted((*triple, u))])
            for u in range(N)
            if u not in triple
        }
        assert values == set(VALUES)


def sample(samples: int, seed: int) -> int:
    rng = random.Random(seed)
    # Permuting the sixteen non-basis vertices lets us order coordinate 0.
    # The residual exact space is consequently (16!)^3, not (16!)^4.
    first = TAIL_BY_AXIS[0]
    best = (-1, None)
    for trial in range(1, samples + 1):
        permutations = [first]
        for _ in range(3):
            values = list(TAIL_BY_AXIS[len(permutations)])
            rng.shuffle(values)
            permutations.append(tuple(values))
        points = normalized_points(permutations)
        ok, passed = all_stars(points)
        if passed > best[0]:
            best = (passed, permutations)
        if ok:
            print(f"RANK-4 CANDIDATE after {trial} samples: {points}")
            return 1
    print(
        f"rank-4: no candidate in {samples} deterministic normalized samples "
        f"of (16!)^3; best passed {best[0]}/1140 stars"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=0)
    parser.add_argument("--seed", type=int, default=835)
    args = parser.parse_args()
    check_normal_form()
    print("rank-4 normal form: four basis-star conditions VERIFIED")
    if args.sample:
        return sample(args.sample, args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Exact determinant-rainbow tests for the linear-code formulation.

For q odd set k=q-1 and n=2k. A k by n generator matrix G gives the colour
c(S)=det(G[S]) on k-subsets. The desired property is checked directly:
for every (k-1)-set T, det(G[T union {u}]) for u outside T is F_q.

This file tests named [I | A] candidates. At q=5 it additionally exhausts
all projective column scalings for every candidate that has the required
zero-support pattern. No near-MDS claim is treated as a witness without the
full determinant-value check.
"""

from __future__ import annotations

import argparse
import itertools
import random


def primitive_root(p: int) -> int:
    for candidate in range(2, p):
        if {pow(candidate, exponent, p) for exponent in range(1, p)} == set(range(1, p)):
            return candidate
    raise AssertionError("prime field has no primitive root")


def determinant(matrix: list[list[int]], p: int) -> int:
    work = [row[:] for row in matrix]
    answer = 1
    for pivot_column in range(len(work)):
        pivot = next(
            (row for row in range(pivot_column, len(work)) if work[row][pivot_column] % p),
            None,
        )
        if pivot is None:
            return 0
        if pivot != pivot_column:
            work[pivot_column], work[pivot] = work[pivot], work[pivot_column]
            answer = -answer
        value = work[pivot_column][pivot_column] % p
        answer = answer * value % p
        inverse = pow(value, -1, p)
        for row in range(pivot_column + 1, len(work)):
            factor = work[row][pivot_column] * inverse % p
            for col in range(pivot_column, len(work)):
                work[row][col] = (work[row][col] - factor * work[pivot_column][col]) % p
    return answer % p


def determinant_table(generator, p: int):
    k = p - 1
    n = 2 * k
    table = {}
    for triple in itertools.combinations(range(n), k - 1):
        entries = {}
        for outside in range(n):
            if outside not in triple:
                support = tuple(sorted((*triple, outside)))
                entries[outside] = determinant(
                    [[generator[row][column] for column in support] for row in range(k)],
                    p,
                )
        table[triple] = entries
    return table


def check_table(table, p: int):
    for triple, values_by_point in table.items():
        values = list(values_by_point.values())
        if set(values) != set(range(p)):
            return False, triple, values
    return True, None, None


def first_counterstar(generator, p: int):
    k = p - 1
    n = 2 * k
    for triple in itertools.combinations(range(n), k - 1):
        values = [
            determinant(
                [[generator[row][column] for column in sorted((*triple, outside))] for row in range(k)],
                p,
            )
            for outside in range(n)
            if outside not in triple
        ]
        if set(values) != set(range(p)):
            return triple, values
    return None


def random_check(generator, p: int, trials: int, seed: int):
    k = p - 1
    n = 2 * k
    rng = random.Random(seed)
    for _ in range(trials):
        triple = tuple(sorted(rng.sample(range(n), k - 1)))
        values = [
            determinant(
                [[generator[row][column] for column in sorted((*triple, outside))] for row in range(k)],
                p,
            )
            for outside in range(n)
            if outside not in triple
        ]
        if set(values) != set(range(p)):
            return triple, values
    return None


def identity_block(matrix, p: int):
    k = len(matrix)
    return [
        [int(row == col) if col < k else matrix[row][col - k] % p for col in range(2 * k)]
        for row in range(k)
    ]


def fourier_block(p: int):
    k = p - 1
    root = primitive_root(p)
    return [[pow(root, row * col, p) for col in range(k)] for row in range(k)]


def quadratic_residue_block(p: int):
    k = p - 1

    def chi(value: int) -> int:
        if value % p == 0:
            return 0
        return 1 if pow(value, (p - 1) // 2, p) == 1 else p - 1

    return [[chi(row - col) for col in range(k)] for row in range(k)]


def shifted_fourier_block(p: int):
    k = p - 1
    root = primitive_root(p)
    return [[pow(root, (row + 1) * (col + 1), p) for col in range(k)] for row in range(k)]


def exhaustive_q5_scaling(table) -> tuple[bool, tuple[int, ...] | None]:
    """All (5-1)^7 projective coordinate scalings, using precomputed minors."""
    p = 5
    n = 8
    for tail in itertools.product(range(1, p), repeat=n - 1):
        scales = (1, *tail)
        if all(
            {values_by_point[point] * scales[point] % p for point in values_by_point}
            == set(range(p))
            for values_by_point in table.values()
        ):
            return True, scales
    return False, None


def run_exact_small(name: str, generator, p: int, scaling_q5: bool) -> None:
    witness = first_counterstar(generator, p)
    if witness is None:
        print(f"q={p} {name}: FULL determinant-rainbow PASS")
        return
    triple, values = witness
    zero_count = values.count(0)
    print(
        f"q={p} {name}: full counterstar T={triple}; values={values}; "
        f"distinct={len(set(values))}/{p}; zeros={zero_count}"
    )
    # Column scaling cannot alter zero positions. It is useful to distinguish
    # a support failure from a possible value-only failure.
    if scaling_q5 and zero_count == 1:
        table = determinant_table(generator, p)
        feasible, scales = exhaustive_q5_scaling(table)
        print(f"q=5 {name}: exhaustive projective scaling {'FOUND' if feasible else 'NONE'} {scales or ''}")


def run_large_probe(name: str, generator, p: int, trials: int) -> None:
    witness = random_check(generator, p, trials, seed=1000 + p)
    if witness is None:
        print(f"q={p} {name}: no counterstar in {trials} exact random stars")
    else:
        triple, values = witness
        print(
            f"q={p} {name}: counterstar T={triple}; distinct={len(set(values))}/{p}; "
            f"zeros={values.count(0)}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--large-trials", type=int, default=20)
    args = parser.parse_args()
    candidates = {
        "fourier": fourier_block,
        "shifted-fourier": shifted_fourier_block,
        "quadratic-residue-circulant": quadratic_residue_block,
    }
    # q=5 and q=7 are exhaustive semantic controls; q=11 remains small
    # enough for exact all-star verification of these three matrices.
    for p in (5, 7, 11):
        for name, build in candidates.items():
            run_exact_small(name, identity_block(build(p), p), p, scaling_q5=(p == 5))
    for p in (17, 19):
        for name, build in candidates.items():
            run_large_probe(name, identity_block(build(p), p), p, args.large_trials)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

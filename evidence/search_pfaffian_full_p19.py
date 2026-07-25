#!/usr/bin/env python3
"""Exact structured screens for the p=19 principal-Pfaffian route.

The target is a 36 by 36 alternating matrix over F_19 whose 18-Pfaffians
are rainbow on every 17-star.  This program tests named skew-circulant
profiles and the F_19 trace of the Cauchy kernel on a 36th-root coset in
F_(19^2).  Each rejection is an explicit exact counterstar for that matrix.

The circulant samples are not an exhaustive search of 19^17 profiles, and
the random-star screen is not an all-star verification of a surviving one.
"""

from __future__ import annotations

import argparse
import itertools
import random


P = 19
N = 36
HALF = 18


def pfaffian(matrix: list[list[int]]) -> int:
    """Independent modular skew-elimination Pfaffian."""
    work = [row[:] for row in matrix]
    answer = 1
    size = len(work)
    for start in range(0, size, 2):
        pivot_col = next((j for j in range(start + 1, size) if work[start][j] % P), None)
        if pivot_col is None:
            return 0
        if pivot_col != start + 1:
            for row in range(size):
                work[row][start + 1], work[row][pivot_col] = work[row][pivot_col], work[row][start + 1]
            work[start + 1], work[pivot_col] = work[pivot_col], work[start + 1]
            answer = -answer
        pivot = work[start][start + 1] % P
        answer = answer * pivot % P
        inverse = pow(pivot, -1, P)
        for i in range(start + 2, size):
            for j in range(i + 1, size):
                value = (
                    work[i][j]
                    - (work[start][i] * work[start + 1][j] - work[start][j] * work[start + 1][i]) * inverse
                ) % P
                work[i][j] = value
                work[j][i] = -value % P
    return answer % P


def star_values(matrix, triple17: tuple[int, ...]) -> list[int]:
    values = []
    triple_set = set(triple17)
    for u in range(N):
        if u in triple_set:
            continue
        support = sorted((*triple17, u))
        values.append(pfaffian([[matrix[i][j] for j in support] for i in support]))
    assert len(values) == P
    return values


def find_random_counterstar(matrix, trials: int, seed: int):
    rng = random.Random(seed)
    for _ in range(trials):
        triple = tuple(sorted(rng.sample(range(N), P - 2)))
        values = star_values(matrix, triple)
        if len(set(values)) != P:
            return triple, values
    return None


def skew_circulant(profile: tuple[int, ...]) -> list[list[int]]:
    assert len(profile) == HALF - 1
    matrix = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            distance = (j - i) % N
            if distance == HALF:
                value = 0
            elif distance < HALF:
                value = profile[distance - 1]
            else:
                value = -profile[N - distance - 1] % P
            matrix[i][j] = value
            matrix[j][i] = -value % P
    return matrix


def legendre(value: int) -> int:
    if value % P == 0:
        return 0
    return 1 if pow(value, (P - 1) // 2, P) == 1 else -1 % P


def cyclic_profiles(random_count: int, seed: int):
    yield "constant", tuple(1 for _ in range(HALF - 1))
    yield "linear", tuple(distance % P for distance in range(1, HALF))
    for exponent in range(2, 9):
        yield f"power_{exponent}", tuple(pow(distance, exponent, P) for distance in range(1, HALF))
    yield "quadratic-character", tuple(legendre(distance) for distance in range(1, HALF))
    yield "character_times_distance", tuple(legendre(distance) * distance % P for distance in range(1, HALF))
    primitive = 2
    for frequency in range(1, 10):
        yield (
            f"multiplicative-wave_{frequency}",
            tuple(pow(primitive, frequency * distance, P) for distance in range(1, HALF)),
        )
    rng = random.Random(seed)
    for sample in range(random_count):
        profile = [rng.randrange(P) for _ in range(HALF - 1)]
        if not any(profile):
            profile[0] = 1
        first = next(value for value in profile if value)
        inverse = pow(first, -1, P)
        yield f"random-projective-{sample}", tuple(value * inverse % P for value in profile)


# F_(19^2)=F_19[t]/(t^2-2); 2 is a nonsquare mod 19.
Q = tuple[int, int]


def qadd(left: Q, right: Q) -> Q:
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def qneg(value: Q) -> Q:
    return (-value[0] % P, -value[1] % P)


def qsub(left: Q, right: Q) -> Q:
    return qadd(left, qneg(right))


def qmul(left: Q, right: Q) -> Q:
    return ((left[0] * right[0] + 2 * left[1] * right[1]) % P, (left[0] * right[1] + left[1] * right[0]) % P)


def qpow(value: Q, exponent: int) -> Q:
    answer = (1, 0)
    while exponent:
        if exponent & 1:
            answer = qmul(answer, value)
        value = qmul(value, value)
        exponent //= 2
    return answer


def qinv(value: Q) -> Q:
    norm = (value[0] * value[0] - 2 * value[1] * value[1]) % P
    return (value[0] * pow(norm, -1, P) % P, -value[1] * pow(norm, -1, P) % P)


def qtrace(value: Q) -> int:
    return 2 * value[0] % P


def primitive_q() -> Q:
    for a in range(P):
        for b in range(P):
            if (a, b) == (0, 0):
                continue
            candidate = (a, b)
            if all(
                qpow(candidate, (P * P - 1) // divisor) != (1, 0)
                for divisor in (2, 3, 5)
            ):
                return candidate
    raise AssertionError("no primitive field element found")


def cauchy_trace_matrix(direction: Q) -> list[list[int]]:
    generator = primitive_q()
    subgroup_generator = qpow(generator, (P * P - 1) // N)
    points = [qmul(generator, qpow(subgroup_generator, index)) for index in range(N)]
    matrix = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            numerator = qsub(points[i], points[j])
            denominator = qsub((1, 0), qmul(points[i], points[j]))
            assert denominator != (0, 0)
            value = qtrace(qmul(direction, qmul(numerator, qinv(denominator))))
            matrix[i][j] = value
            matrix[j][i] = -value % P
    return matrix


def run_family(name: str, matrix, trials: int, seed: int) -> bool:
    witness = find_random_counterstar(matrix, trials, seed)
    if witness is None:
        print(f"{name}: no counterstar in {trials} exact random stars")
        return True
    triple, values = witness
    print(
        f"{name}: counterstar T={triple}; values={values}; "
        f"distinct={len(set(values))}/19"
    )
    return False


def self_test() -> None:
    """Check Pfaffian elimination against the closed 4 by 4 formula."""
    rng = random.Random(19)
    for _ in range(100):
        matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(i + 1, 4):
                matrix[i][j] = rng.randrange(P)
                matrix[j][i] = -matrix[i][j] % P
        direct = (
            matrix[0][1] * matrix[2][3]
            - matrix[0][2] * matrix[1][3]
            + matrix[0][3] * matrix[1][2]
        ) % P
        assert pfaffian(matrix) == direct
    assert qpow(primitive_q(), P * P - 1) == (1, 0)
    print("p=19 Pfaffian and F_(19^2) arithmetic self-test: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=50)
    parser.add_argument("--random-circulants", type=int, default=25)
    parser.add_argument("--seed", type=int, default=190835)
    args = parser.parse_args()
    self_test()
    survivors = []
    for index, (name, profile) in enumerate(cyclic_profiles(args.random_circulants, args.seed)):
        if run_family(
            f"circulant/{name}",
            skew_circulant(profile),
            args.trials,
            args.seed + index,
        ):
            survivors.append(f"circulant/{name}")
    for index, direction in enumerate([(a, 1) for a in range(P)] + [(1, 0)]):
        name = f"cauchy-36th-root/trace-direction-{direction}"
        if run_family(name, cauchy_trace_matrix(direction), args.trials, args.seed + 1000 + index):
            survivors.append(name)
    print(f"survivors after this screen: {survivors}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

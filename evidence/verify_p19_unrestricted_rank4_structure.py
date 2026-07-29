#!/usr/bin/env python3
"""Finite checks for p19_unrestricted_rank4_structure.md.

This checks coefficient arithmetic and finite counts only.  It is not an
existence or nonexistence search for an ordered link.
"""

from itertools import product
from random import Random

P = 19


def symplectic(left, right):
    return (
        left[0] * right[1]
        - left[1] * right[0]
        + left[2] * right[3]
        - left[3] * right[2]
    ) % P


def add(left, right):
    return [(a + b) % P for a, b in zip(left, right)]


def scale(coefficient, vector):
    return [(coefficient * value) % P for value in vector]


def projective_points():
    for vector in product(range(P), repeat=4):
        if not any(vector):
            continue
        pivot = next(value for value in vector if value)
        if pivot != 1:
            continue
        yield vector


def check_power_sums():
    observed = [
        sum(pow(value, degree, P) for value in range(P)) % P
        for degree in range(1, 19)
    ]
    assert observed[:17] == [0] * 17
    assert observed[17] == P - 1
    print("field_power_sums=PASS")


def check_quadric_counts():
    forms = {
        "split_rank_2": lambda x: x[0] * x[1],
        "rank_3": lambda x: x[0] * x[1] + x[2] * x[2],
        "hyperbolic_rank_4": lambda x: x[0] * x[1] + x[2] * x[3],
        # 2 is a nonsquare modulo 19, so this four-form is elliptic.
        "elliptic_rank_4": (
            lambda x: x[0] * x[0] - 2 * x[1] * x[1] + x[2] * x[3]
        ),
    }
    expected = {
        "split_rank_2": 742,
        "rank_3": 381,
        "hyperbolic_rank_4": 400,
        "elliptic_rank_4": 362,
    }
    points = list(projective_points())
    assert len(points) == P**3 + P**2 + P + 1 == 7240
    for name, form in forms.items():
        count = sum(form(point) % P == 0 for point in points)
        assert count == expected[name], (name, count)
    print("projective_quadric_counts=PASS")


def check_zig_zag_identity():
    rng = Random(83519)
    vectors = [
        [rng.randrange(P) for _ in range(4)]
        for _ in range(20)
    ]
    total = [sum(vector[c] for vector in vectors) % P for c in range(4)]
    suffix = [[0, 0, 0, 0] for _ in range(21)]
    for index in range(19, -1, -1):
        suffix[index] = add(vectors[index], suffix[index + 1])
    y = [
        add(scale(2, suffix[index]), scale(-1, total))
        for index in range(21)
    ]
    assert y[0] == total
    assert y[20] == scale(-1, total)
    for index, vector in enumerate(vectors):
        assert add(y[index], scale(-1, y[index + 1])) == scale(2, vector)
        left = sum(
            symplectic(vector, vectors[j])
            for j in range(index + 1, 20)
        ) % P
        right = sum(
            symplectic(vector, vectors[j])
            for j in range(index)
        ) % P
        assert (left - right) % P == symplectic(vector, y[index + 1])
        assert symplectic(y[index], y[index + 1]) == (
            2 * symplectic(vector, y[index + 1])
        ) % P
    print("zig_zag_algebra=PASS")


def check_endpoint_expansion():
    rng = Random(190835)
    u0 = [1, 0, 0, 0]
    u19 = [0, 1, 0, 0]
    for _ in range(1000):
        x_i, y_i, s_i, t_i = [rng.randrange(P) for _ in range(4)]
        x_j, y_j, s_j, t_j = [rng.randrange(P) for _ in range(4)]
        u_i = [y_i, x_i, s_i, t_i]
        u_j = [y_j, x_j, s_j, t_j]
        assert symplectic(u0, u19) == 1
        assert symplectic(u0, u_i) == x_i
        assert symplectic(u_i, u19) == y_i
        expected = (
            y_i * x_j - x_i * y_j + s_i * t_j - t_i * s_j
        ) % P
        assert symplectic(u_i, u_j) == expected
    print("endpoint_expansion=PASS")


def main():
    check_power_sums()
    check_quadric_counts()
    check_zig_zag_identity()
    check_endpoint_expansion()
    print("p19 unrestricted rank-four structural audit: PASS")


if __name__ == "__main__":
    main()

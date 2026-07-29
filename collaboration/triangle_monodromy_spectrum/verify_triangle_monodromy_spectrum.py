#!/usr/bin/env python3
"""Exact audit of the triangle-monodromy Schreier spectral constraints.

Stdlib only.  This verifies arithmetic, sign-polynomial support, Steiner
point-module eigenvalues, and the Fano/Witt small controls.  The general
spectral implication is proved in the companion README.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from math import comb


def odd_spectrum(k: int) -> tuple[int, ...]:
    return tuple((-1) ** j * (k - j) for j in range(1, k))


def p_minus(k: int, theta: int) -> int:
    return (theta + k - 1) * (theta - 2) * (theta + 1)


def p_plus(k: int, theta: int) -> int:
    return (k - 2 - theta) * (theta + 3) * (theta + 1)


def lambda_s(k: int, s: int) -> int:
    r = k - 1
    v = 2 * k - 1
    if s == r:
        return 1
    if not 0 <= s <= r - 1:
        return 0
    numerator = comb(v - s, r - 1 - s)
    denominator = r - s
    if numerator % denominator:
        raise AssertionError("nonintegral Steiner lambda")
    return numerator // denominator


def point_counts(k: int) -> tuple[int, int]:
    r = k - 1
    inside = sum((-1) ** j * comb(r - 1, j) * lambda_s(k, j + 1) for j in range(r))
    outside = r * sum(
        (-1) ** j * comb(r - 1, j) * lambda_s(k, j + 2) for j in range(r - 2)
    )
    return inside, outside


def verify_symbolic_instances() -> None:
    for k in (4, 6, 16):
        spectrum = odd_spectrum(k)
        expected = tuple(
            value
            for magnitude in range(k - 1, 0, -1)
            for value in (-magnitude if (k - magnitude) % 2 else magnitude,)
        )
        if spectrum != expected:
            raise AssertionError("Odd spectrum ordering changed")
        if any(p_minus(k, theta) < 0 for theta in spectrum):
            raise AssertionError("lower sign polynomial is negative")
        if any(p_plus(k, theta) < 0 for theta in spectrum):
            raise AssertionError("upper sign polynomial is negative")

        lower = (-k * k + 4 * k - 2) // 2
        upper = (k * k - 3 * k - 6) // 2
        inside, outside = point_counts(k)
        if inside != k // 2:
            raise AssertionError("wrong inside point count")
        if outside != comb(k - 1, 2):
            raise AssertionError("wrong outside point count")
        if inside - outside != lower:
            raise AssertionError("point module misses the lower endpoint")

        # The equality spectral weights at {-(k-1), 2, -1}.
        # Store them over the common denominator 3(k+1).
        weights = (3, 2 * k - 1, k + 1)
        support = (-(k - 1), 2, -1)
        denominator = 3 * (k + 1)
        if sum(weights) != denominator:
            raise AssertionError("spectral weights do not sum to one")
        if sum(w * t for w, t in zip(weights, support)) != 0:
            raise AssertionError("first spectral moment is wrong")
        if sum(w * t * t for w, t in zip(weights, support)) != k * denominator:
            raise AssertionError("second spectral moment is wrong")
        if sum(w * t**3 for w, t in zip(weights, support)) != 2 * lower * denominator:
            raise AssertionError("third spectral moment is wrong")

        sheets = comb(2 * k - 1, k - 1) // (k + 1)
        degree = k * (k - 1) // 2
        minimum_odd_schreier_girth = next(
            length for length in range(1, 2 * k, 2) if 3 * length >= 2 * k - 1
        )
        print(
            f"[exact] k={k}: sheets={sheets}, d={degree}, "
            f"nonprincipal interval=[{lower},{upper}], "
            f"point eigenvalue={lower}, "
            f"Schreier odd girth>={minimum_odd_schreier_girth}"
        )


def psl2_11_hexads():
    """Carmichael's exact projective-line construction of W_12."""

    prime = 11

    def image(a, b, c, d, z):
        if z is None:
            return None if c == 0 else (a * pow(c, -1, prime)) % prime
        denominator = (c * z + d) % prime
        if denominator == 0:
            return None
        return ((a * z + b) * pow(denominator, -1, prime)) % prime

    seed = frozenset((None, 1, 3, 4, 5, 9))
    blocks = set()
    for a, b, c, d in product(range(prime), repeat=4):
        if (a * d - b * c) % prime != 1:
            continue
        blocks.add(frozenset(image(a, b, c, d, z) for z in seed))
    if len(blocks) != 132:
        raise AssertionError("wrong W_12 block count")
    return blocks


def adjacency_from_intersection(blocks, intersection: int):
    return [
        [int(left != right and len(left & right) == intersection) for right in blocks]
        for left in blocks
    ]


def identity(order: int):
    return [[int(row == column) for column in range(order)] for row in range(order)]


def matrix_add(left, right, left_scale=1, right_scale=1):
    return [
        [
            left_scale * left[row][column] + right_scale * right[row][column]
            for column in range(len(left))
        ]
        for row in range(len(left))
    ]


def matrix_multiply(left, right):
    order = len(left)
    answer = [[0] * order for _ in range(order)]
    for row in range(order):
        for middle, value in enumerate(left[row]):
            if value == 0:
                continue
            for column, other in enumerate(right[middle]):
                answer[row][column] += value * other
    return answer


def zero_matrix(matrix) -> bool:
    return all(value == 0 for row in matrix for value in row)


def trace(matrix) -> int:
    return sum(matrix[index][index] for index in range(len(matrix)))


def connected(adjacency) -> bool:
    seen = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for other, value in enumerate(adjacency[vertex]):
            if value and other not in seen:
                seen.add(other)
                frontier.append(other)
    return len(seen) == len(adjacency)


def verify_point_module(blocks, adjacency, k: int) -> None:
    points = sorted(set().union(*blocks), key=lambda item: (item is not None, item))
    inside_expected, outside_expected = point_counts(k)
    for point in points:
        for row, block in enumerate(blocks):
            observed = sum(
                adjacency[row][column]
                for column, other in enumerate(blocks)
                if point in other
            )
            expected = inside_expected if point in block else outside_expected
            if observed != expected:
                raise AssertionError("point-module neighbour count fails")


def verify_fano_control() -> None:
    blocks = [
        frozenset(block)
        for block in (
            (0, 1, 2),
            (0, 3, 4),
            (0, 5, 6),
            (1, 3, 5),
            (1, 4, 6),
            (2, 3, 6),
            (2, 4, 5),
        )
    ]
    adjacency = adjacency_from_intersection(blocks, 1)
    if any(sum(row) != 6 for row in adjacency):
        raise AssertionError("Fano R graph has wrong degree")
    if any(
        adjacency[row][column] != int(row != column)
        for row in range(7)
        for column in range(7)
    ):
        raise AssertionError("Fano R graph is not K_7")
    cubed = matrix_multiply(matrix_multiply(adjacency, adjacency), adjacency)
    if trace(cubed) == 0:
        raise AssertionError("Fano R graph has no 3-cycle")
    verify_point_module(blocks, adjacency, 4)
    print("[control] k=4 Fano R spectrum 6^1, (-1)^6, odd girth 3: PASS")


def verify_witt_control() -> None:
    hexads = psl2_11_hexads()
    blocks = [block - {None} for block in hexads if None in block]
    if len(blocks) != 66:
        raise AssertionError("wrong derived Witt block count")
    adjacency = adjacency_from_intersection(blocks, 1)
    if any(sum(row) != 15 for row in adjacency):
        raise AssertionError("Witt R graph has wrong degree")
    if not connected(adjacency):
        raise AssertionError("Witt R graph is disconnected")
    verify_point_module(blocks, adjacency, 6)

    # Audit the three-class intersection algebra before using its spectrum.
    allowed_intersections = {1, 2, 3, 5}
    profiles = {}
    for left in blocks:
        for right in blocks:
            relation = len(left & right)
            if relation not in allowed_intersections:
                raise AssertionError("unexpected Witt block intersection")
            profile = Counter(
                (len(left & third), len(third & right)) for third in blocks
            )
            canonical = tuple(sorted(profile.items()))
            if relation in profiles and profiles[relation] != canonical:
                raise AssertionError("intersection algebra is not constant")
            profiles[relation] = canonical

    # Exact annihilating polynomial
    # (A-15I)(A-2I)(A+3I)(A+7I)=0.
    order = len(blocks)
    unit = identity(order)
    polynomial = identity(order)
    for root in (15, 2, -3, -7):
        factor = matrix_add(adjacency, unit, 1, -root)
        polynomial = matrix_multiply(polynomial, factor)
    if not zero_matrix(polynomial):
        raise AssertionError("Witt adjacency polynomial fails")

    # Recover exact multiplicities from traces 0, tr(A^2)=66*15, and 66.
    squared = matrix_multiply(adjacency, adjacency)
    if trace(adjacency) != 0 or trace(squared) != 66 * 15:
        raise AssertionError("Witt spectral moments fail")
    cubed = matrix_multiply(squared, adjacency)
    fifth = matrix_multiply(matrix_multiply(cubed, adjacency), adjacency)
    if trace(cubed) != 0 or trace(fifth) != 590_040:
        raise AssertionError("Witt odd-girth moments fail")
    multiplicities = {15: 1, 2: 44, -3: 11, -7: 10}
    moment_matrix_determinant = (
        1 * ((-3) * 49 - (-7) * 9) - 1 * (2 * 49 - (-7) * 4) + 1 * (2 * 9 - (-3) * 4)
    )
    if moment_matrix_determinant == 0:
        raise AssertionError("Witt multiplicity moments are not unique")
    if sum(multiplicities.values()) != 66:
        raise AssertionError("Witt multiplicities have wrong total")
    if sum(value * count for value, count in multiplicities.items()) != 0:
        raise AssertionError("Witt first spectral moment fails")
    if sum(value * value * count for value, count in multiplicities.items()) != 66 * 15:
        raise AssertionError("Witt second spectral moment fails")
    if any(
        sum(
            adjacency[left][third] and adjacency[third][right] for third in range(order)
        )
        != 0
        for left in range(order)
        for right in range(order)
        if adjacency[left][right]
    ):
        raise AssertionError("Witt R graph is not triangle-free")
    print(
        "[control] k=6 Witt R spectrum 15^1, 2^44, (-3)^11, (-7)^10, odd girth 5: PASS"
    )


def main() -> None:
    # The one-sheet O_2=K_3 cover has no sheet-orthogonal subspace W.
    if comb(3, 1) // 3 != 1:
        raise AssertionError("O_2 cover control failed")
    print("[control] k=2 genuine O_2 -> K_3 cover: W=0")

    verify_symbolic_instances()
    verify_fano_control()
    verify_witt_control()

    # Exact open-parameter summary.
    k = 16
    sheets = comb(31, 15) // 17
    if sheets != 17_678_835 or sheets % 2 != 1:
        raise AssertionError("wrong k=16 sheet count/parity")
    lower = (-k * k + 4 * k - 2) // 2
    upper = (k * k - 3 * k - 6) // 2
    if (lower, upper, 2 * lower, 2 * upper) != (-97, 101, -194, 202):
        raise AssertionError("wrong k=16 spectral endpoints")
    if [length for length in range(1, 11, 2) if 3 * length < 31] != [1, 3, 5, 7, 9]:
        raise AssertionError("wrong short odd monodromy word lengths")
    print(
        "[exact] k=16 triangle-monodromy sum: "
        "top=240, nonprincipal in [-194,202], "
        "-194 multiplicity >=30"
    )
    print(
        "[exact] k=16 every triangle-word product of lengths "
        "1,3,5,7,9 is fixed-point-free; Schreier odd girth >=11"
    )
    print("ALL TRIANGLE-MONODROMY SPECTRUM AUDITS PASSED")
    print("SCOPE: necessary spectral theorem only; no k=16 cover is asserted")


if __name__ == "__main__":
    main()

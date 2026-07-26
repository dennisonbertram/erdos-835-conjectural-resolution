#!/usr/bin/env python3
"""Exact audit of the degree-three fibre-containment profiles.

The calculation is conditional on a hypothetical S(14,15,31) fibre in an
O_16 -> K_17 cover.  It proves necessary identities only.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb


B_POINTS = tuple(range(15))
OUTSIDE_POINTS = tuple(range(16))
INFINITY = 15


def choose(n: int, r: int) -> int:
    return comb(n, r) if 0 <= r <= n else 0


def design_lambda(t: int) -> int:
    numerator = choose(31 - t, 14 - t)
    denominator = 15 - t
    assert numerator % denominator == 0
    return numerator // denominator


def rref_unique(
    matrix: list[list[int]], right_hand_side: list[int]
) -> list[Fraction]:
    assert len(matrix) == len(right_hand_side)
    augmented = [
        [Fraction(value) for value in row] + [Fraction(rhs)]
        for row, rhs in zip(matrix, right_hand_side)
    ]
    row_count = len(augmented)
    column_count = len(matrix[0])
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        source = next(
            (
                row
                for row in range(pivot_row, row_count)
                if augmented[row][column]
            ),
            None,
        )
        if source is None:
            continue
        augmented[pivot_row], augmented[source] = (
            augmented[source],
            augmented[pivot_row],
        )
        pivot = augmented[pivot_row][column]
        augmented[pivot_row] = [
            value / pivot for value in augmented[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not augmented[row][column]:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [
                augmented[row][index]
                - multiplier * augmented[pivot_row][index]
                for index in range(column_count + 1)
            ]
        pivot_columns.append(column)
        pivot_row += 1

    for row in augmented:
        assert any(row[column] for column in range(column_count)) or not row[-1]
    assert len(pivot_columns) == column_count
    answer = [Fraction() for _ in range(column_count)]
    for row, column in enumerate(pivot_columns):
        answer[column] = augmented[row][-1]
    return answer


def solve_profile(intersection_with_triple: int, r_count: int) -> tuple[int, ...]:
    i = intersection_with_triple
    known = {s: 0 for s in range(i)}
    known[0] = 0
    known[14] = 0
    known[15] = int(i == 3)
    known[1] = r_count
    unknown = [s for s in range(16) if s not in known]
    matrix: list[list[int]] = []
    right_hand_side: list[int] = []
    for degree in range(12):
        matrix.append(
            [choose(s - i, degree) for s in unknown]
        )
        right_hand_side.append(
            choose(15 - i, degree) * design_lambda(3 + degree)
            - sum(
                choose(s - i, degree) * value
                for s, value in known.items()
            )
        )
    solved = rref_unique(matrix, right_hand_side)
    profile = [0] * 16
    for s, value in known.items():
        profile[s] = value
    assert len(unknown) == len(solved)
    for s, value in zip(unknown, solved):
        assert value.denominator == 1
        profile[s] = value.numerator
    assert all(value >= 0 for value in profile)
    return tuple(profile)


def verify_profiles() -> dict[str, tuple[int, ...]]:
    profiles = {
        "i0": solve_profile(0, 78),
        "i1_nonedge": solve_profile(1, 6),
        "i1_edge": solve_profile(1, 7),
        "i2": solve_profile(2, 0),
        "i3": solve_profile(3, 0),
    }
    assert profiles["i0"][1:13] == (
        78,
        1716,
        19_305,
        102_960,
        303_732,
        504_504,
        487_773,
        270_270,
        84_370,
        13_728,
        1053,
        26,
    )
    assert profiles["i1_nonedge"][1:14] == (
        6,
        292,
        5401,
        42_724,
        177_144,
        403_656,
        531_069,
        403_656,
        177_144,
        42_724,
        5401,
        292,
        6,
    )
    assert profiles["i1_edge"][1:14] == (
        7,
        280,
        5467,
        42_504,
        177_639,
        402_864,
        531_993,
        402_864,
        177_639,
        42_504,
        5467,
        280,
        7,
    )
    assert profiles["i2"][2:14] == (
        26,
        1053,
        13_728,
        84_370,
        270_270,
        487_773,
        504_504,
        303_732,
        102_960,
        19_305,
        1716,
        78,
    )
    assert profiles["i3"][3:14] == (
        108,
        3072,
        31_152,
        147_840,
        375_210,
        532_224,
        436_128,
        202_752,
        53_460,
        7040,
        528,
    )
    assert profiles["i3"][15] == 1
    assert all(sum(profile) == design_lambda(3) for profile in profiles.values())

    beta = tuple(
        (-1) ** index * choose(12, index) for index in range(13)
    )
    difference = tuple(
        profiles["i1_edge"][s] - profiles["i1_nonedge"][s]
        for s in range(1, 14)
    )
    assert difference == beta
    assert profiles["i1_nonedge"][1:14] == profiles["i1_nonedge"][1:14][::-1]
    assert profiles["i1_edge"][1:14] == profiles["i1_edge"][1:14][::-1]
    print("[profiles] all four triple types and the 6/7 null direction pass")
    return profiles


def cyclic_factorization() -> tuple[dict[int, set[tuple[int, int]]], dict]:
    factors: dict[int, set[tuple[int, int]]] = {
        a: set() for a in B_POINTS
    }
    for a in B_POINTS:
        factors[a].add(tuple(sorted((INFINITY, a))))
        for difference in range(1, 8):
            factors[a].add(
                tuple(
                    sorted(
                        (
                            (a + difference) % 15,
                            (a - difference) % 15,
                        )
                    )
                )
            )
    all_edges = set(combinations(OUTSIDE_POINTS, 2))
    assert all(len(factor) == 8 for factor in factors.values())
    assert set().union(*factors.values()) == all_edges
    assert sum(len(factor) for factor in factors.values()) == len(all_edges)
    edge_colour = {
        edge: colour
        for colour, factor in factors.items()
        for edge in factor
    }
    return factors, edge_colour


def verify_one_factorization_counts() -> tuple[
    dict[int, set[tuple[int, int]]], dict[tuple[int, int], int]
]:
    factors, edge_colour = cyclic_factorization()
    for triple in combinations(OUTSIDE_POINTS, 3):
        colours = {edge_colour[edge] for edge in combinations(triple, 2)}
        assert len(colours) == 3
        r_count = sum(
            sum(not (set(edge) & set(triple)) for edge in factors[a])
            for a in B_POINTS
        )
        assert r_count == 78

    type_counts = Counter()
    for a in B_POINTS:
        for pair in combinations(OUTSIDE_POINTS, 2):
            count = sum(
                not (set(edge) & set(pair)) for edge in factors[a]
            )
            expected = 7 if pair in factors[a] else 6
            assert count == expected
            type_counts[expected] += 1
    assert type_counts == {6: 1680, 7: 120}

    triangles = tuple(combinations(OUTSIDE_POINTS, 3))
    colour_sets = {
        triple: {edge_colour[edge] for edge in combinations(triple, 2)}
        for triple in triangles
    }
    for colour in B_POINTS:
        assert sum(colour in colours for colours in colour_sets.values()) == 112
        for point in OUTSIDE_POINTS:
            assert (
                sum(
                    point in triple and colour in colour_sets[triple]
                    for triple in triangles
                )
                == 21
            )
    for pair in combinations(B_POINTS, 2):
        assert (
            sum(set(pair) <= colours for colours in colour_sets.values()) == 16
        )

    overlap_profiles = Counter(
        tuple(
            Counter(
                len(set(triple) & colours)
                for colours in colour_sets.values()
            )[overlap]
            for overlap in range(4)
        )
        for triple in combinations(B_POINTS, 3)
    )
    assert overlap_profiles == {
        (271, 243, 45, 1): 360,
        (270, 246, 42, 2): 90,
        (268, 252, 36, 4): 5,
    }
    print("[matching] cyclic K16 factorization gives 78 and the 1680/120 split")
    return factors, edge_colour


def fibre_intersection_numbers() -> tuple[int, ...]:
    counts = [0] * 16
    counts[15] = 1
    for degree in range(14, -1, -1):
        counts[degree] = (
            choose(15, degree) * design_lambda(degree)
            - sum(
                choose(s, degree) * counts[s]
                for s in range(degree + 1, 16)
            )
        )
    return tuple(counts)


def verify_global_double_counts(
    profiles: dict[str, tuple[int, ...]]
) -> None:
    relation_counts = fibre_intersection_numbers()
    assert relation_counts == (
        0,
        120,
        3360,
        49_140,
        349_440,
        1_417_416,
        3_363_360,
        4_877_730,
        4_324_320,
        2_362_360,
        768_768,
        147_420,
        14_560,
        840,
        0,
        1,
    )
    aggregates = {
        0: tuple(560 * value for value in profiles["i0"]),
        1: tuple(
            1680 * profiles["i1_nonedge"][s]
            + 120 * profiles["i1_edge"][s]
            for s in range(16)
        ),
        2: tuple(1680 * value for value in profiles["i2"]),
        3: tuple(455 * value for value in profiles["i3"]),
    }
    for i, aggregate in aggregates.items():
        for s in range(16):
            expected = (
                relation_counts[s]
                * choose(s, i)
                * choose(15 - s, 3 - i)
            )
            assert aggregate[s] == expected
    print("[global] every relation-by-triple double count passes")


def hypergeometric_counts(
    universe_size: int, relevant_size: int
) -> tuple[int, int, int, int]:
    return tuple(
        choose(relevant_size, q)
        * choose(universe_size - relevant_size, 3 - q)
        for q in range(4)
    )


def add_distributions(
    *terms: tuple[int, tuple[int, int, int, int]]
) -> tuple[int, int, int, int]:
    return tuple(
        sum(multiplier * distribution[q] for multiplier, distribution in terms)
        for q in range(4)
    )


def moments(distribution: tuple[int, ...]) -> tuple[int, int, int]:
    return (
        sum(distribution),
        sum(q * count for q, count in enumerate(distribution)),
        sum(q * q * count for q, count in enumerate(distribution)),
    )


def verify_fractional_witness() -> None:
    alpha = Fraction(9, 182)
    beta = Fraction(1, 78)

    def mass(total: int, first_moment: int) -> Fraction:
        return alpha * total + beta * first_moment

    def q_mass(distribution: tuple[int, ...]) -> Fraction:
        _, first, second = moments(distribution)
        return alpha * first + beta * second

    assert tuple(alpha + beta * q for q in range(4)) == (
        Fraction(9, 182),
        Fraction(17, 273),
        Fraction(41, 546),
        Fraction(8, 91),
    )
    assert mass(455, 273) == 26
    assert mass(560, 336) == 32

    triple_domains = {
        "i0": (455, 273, 26),
        "i1_edge": (5096, 2184, 280),
        "i1_nonedge": (5096, 3120, 292),
        "i2": (30_030, 18_018, 1716),
        "i3": (123_200, 73_920, 7040),
    }
    for total, first, expected in triple_domains.values():
        assert mass(total, first) == expected

    outside_pair = tuple(
        14 * value for value in hypergeometric_counts(15, 3)
    )
    cross_pair = add_distributions(
        (21, hypergeometric_counts(14, 2)),
        (84, hypergeometric_counts(14, 3)),
    )
    inside_pair = add_distributions(
        (16, hypergeometric_counts(13, 1)),
        (192, hypergeometric_counts(13, 2)),
        (352, hypergeometric_counts(13, 3)),
    )
    assert outside_pair == (3080, 2772, 504, 14)
    assert cross_pair == (18_480, 16_632, 3024, 84)
    assert inside_pair == (77_440, 69_696, 12_672, 352)
    for distribution, expected_mass, expected_q_mass in (
        (outside_pair, 364, 252),
        (cross_pair, 2184, 1512),
        (inside_pair, 9152, 6336),
    ):
        total, first, _ = moments(distribution)
        assert mass(total, first) == expected_mass
        assert q_mass(distribution) == expected_q_mass
        assert expected_q_mass == Fraction(9, 13) * expected_mass

    edge_i1 = tuple(
        14 * value for value in hypergeometric_counts(14, 2)
    )
    nonedge_i1 = add_distributions(
        (2, hypergeometric_counts(14, 2)),
        (12, hypergeometric_counts(14, 3)),
    )
    i2_distribution = add_distributions(
        (3, hypergeometric_counts(13, 1)),
        (36, hypergeometric_counts(13, 2)),
        (66, hypergeometric_counts(13, 3)),
    )
    assert edge_i1 == (3080, 1848, 168, 0)
    assert nonedge_i1 == (2420, 2244, 420, 12)
    assert i2_distribution == (14_520, 13_068, 2376, 66)

    for overlap_distribution in (
        (271, 243, 45, 1),
        (270, 246, 42, 2),
        (268, 252, 36, 4),
    ):
        i3_distribution = add_distributions(
            *(
                (
                    overlap_distribution[overlap],
                    hypergeometric_counts(12, 3 - overlap),
                )
                for overlap in range(4)
            )
        )
        assert moments(i3_distribution) == (123_200, 73_920, 95_040)
        assert q_mass(i3_distribution) == Fraction(63_360, 13)

    potential_states = tuple(
        560 * value for value in hypergeometric_counts(15, 3)
    )
    fractional_states = tuple(
        potential_states[q] * (alpha + beta * q) for q in range(4)
    )
    assert fractional_states == (
        Fraction(79_200, 13),
        Fraction(89_760, 13),
        Fraction(19_680, 13),
        Fraction(640, 13),
    )
    assert sum(fractional_states) == 14_560
    assert sum(
        q * fractional_states[q] for q in range(4)
    ) == 10_080
    assert sum(
        choose(q, 2) * fractional_states[q] for q in range(4)
    ) == Fraction(21_600, 13)
    print("[fractional] positive X=9/182+q/78 meets all audited linear margins")


def verify_tau_frontier() -> None:
    feasible_tau: list[int] = []
    for tau in range(10_081):
        n3 = max(0, (2 * tau - 10_080 + 2) // 3)
        if n3 > tau // 3:
            continue
        n2 = tau - 3 * n3
        n1 = 10_080 - 2 * tau + 3 * n3
        n0 = 4480 + tau - n3
        states = (n0, n1, n2, n3)
        assert all(value >= 0 for value in states)
        assert sum(states) == 14_560
        assert sum(q * states[q] for q in range(4)) == 10_080
        assert sum(choose(q, 2) * states[q] for q in range(4)) == tau
        feasible_tau.append(tau)
    assert feasible_tau == [*range(10_079), 10_080]
    assert feasible_tau[:1681] == list(range(1681))
    print(
        "[states] isolated row equations exclude only tau=10079; "
        "all tau=0..1680 allowed by the stronger local bound remain feasible"
    )


def main() -> None:
    assert tuple(design_lambda(t) for t in range(3, 15)) == (
        1_789_515,
        766_935,
        312_455,
        120_175,
        43_263,
        14_421,
        4389,
        1197,
        285,
        57,
        9,
        1,
    )
    profiles = verify_profiles()
    verify_one_factorization_counts()
    verify_global_double_counts(profiles)
    verify_fractional_witness()
    verify_tau_frontier()
    print("ALL SCHREIER H3 TRIPLE-PROFILE AUDITS PASSED")
    print("SCOPE: exact necessary conditions only; no k=16 contradiction")


if __name__ == "__main__":
    main()

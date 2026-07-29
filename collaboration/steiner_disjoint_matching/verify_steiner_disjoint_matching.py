#!/usr/bin/env python3
"""Exact audit of the S(14,15,31) disjointness-matching correction.

This script verifies necessary identities conditional on the existence of a
Steiner system or large set.  It does not search for or construct either.
"""

from math import comb


CHECKS: list[str] = []


def check(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)
    print(f"[ok] {label}")


def choose(top: int, bottom: int) -> int:
    """Binomial coefficient with the zero-outside-range convention."""
    if bottom < 0 or bottom > top:
        return 0
    return comb(top, bottom)


def design_index(k: int, incidence_degree: int) -> int:
    """lambda_i for a hypothetical S(k-2,k-1,2k-1)."""
    v = 2 * k - 1
    block_size = k - 1
    strength = k - 2
    numerator = comb(v - incidence_degree, strength - incidence_degree)
    denominator = comb(block_size - incidence_degree, strength - incidence_degree)
    quotient, remainder = divmod(numerator, denominator)
    if remainder:
        raise ValueError(f"nonintegral design index at k={k}, i={incidence_degree}")
    return quotient


def closed_intersection_number(k: int, intersection: int) -> tuple[int, int]:
    """Return numerator, denominator of the general closed formula."""
    numerator = comb(k - 1, intersection) * (
        comb(k, intersection + 1) + (-1) ** (k - 1 - intersection) * k
    )
    return numerator, k + 1


def exact_closed_intersection_number(k: int, intersection: int) -> int:
    numerator, denominator = closed_intersection_number(k, intersection)
    quotient, remainder = divmod(numerator, denominator)
    if remainder:
        raise ValueError(f"nonintegral intersection number at k={k}, s={intersection}")
    return quotient


def invert_design_moments(k: int) -> list[int]:
    """Solve the triangular fixed-block intersection equations."""
    block_size = k - 1
    counts = [0] * (block_size + 1)
    counts[block_size] = 1
    for incidence_degree in range(block_size - 1, -1, -1):
        moment = comb(block_size, incidence_degree) * design_index(k, incidence_degree)
        counts[incidence_degree] = moment - sum(
            comb(intersection, incidence_degree) * counts[intersection]
            for intersection in range(incidence_degree + 1, block_size + 1)
        )
    return counts


def section_local_candidates() -> None:
    print("1. the two truncated local observations")
    complement = set(range(16))
    candidates = [complement - {point} for point in complement]
    check("there are exactly 16 disjoint-from-B candidates", len(candidates) == 16)
    check(
        "two distinct candidates always intersect in 14 points",
        {
            len(candidates[left] & candidates[right])
            for left in range(16)
            for right in range(left)
        }
        == {14},
    )
    check("C(16,14)=120 and C(15,14)=15", comb(16, 14) == 120 and comb(15, 14) == 15)
    check(
        "the truncated equation permits both (d,n1)=(0,120),(1,105)",
        all(n1 + 15 * d == 120 for d, n1 in ((0, 120), (1, 105))),
    )

    block_count = comb(31, 14) // 15
    check("the fibre has b=17,678,835 blocks", block_count == 17_678_835)
    check("b is odd", block_count % 2 == 1)
    maximum_matching = (block_count - 1) // 2
    for matching_edges in (0, 1, maximum_matching):
        matched = 2 * matching_edges
        isolated = block_count - matched
        ordered_n1 = 105 * matched + 120 * isolated
        unordered_n1 = ordered_n1 // 2
        check(
            f"matching relaxation m={matching_edges:,} satisfies all parity formulas",
            (
                isolated > 0
                and isolated % 2 == 1
                and ordered_n1 == 120 * block_count - 30 * matching_edges
                and ordered_n1 % 2 == 0
                and unordered_n1 == 60 * block_count - 15 * matching_edges
                and unordered_n1 % 2 == matching_edges % 2
            ),
        )


def section_full_moments() -> tuple[int, list[int]]:
    print()
    print("2. the full S(14,15,31) design moments")
    k = 16
    block_size = k - 1
    indices = [design_index(k, degree) for degree in range(k - 1)]
    check(
        "all fifteen design indices lambda_0,...,lambda_14 are integral",
        len(indices) == 15,
    )

    inverted = invert_design_moments(k)
    closed = [
        exact_closed_intersection_number(k, intersection) for intersection in range(k)
    ]
    expected = [
        0,
        120,
        3_360,
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
    ]
    check("triangular inversion equals the closed formula", inverted == closed)
    check("the complete displayed intersection row is exact", closed == expected)
    check("all row sizes are nonnegative", min(closed) >= 0)
    check("the row sizes sum to the fibre size", sum(closed) == indices[0])

    for degree in range(block_size):
        left = sum(
            comb(intersection, degree) * closed[intersection]
            for intersection in range(degree, block_size + 1)
        )
        right = comb(block_size, degree) * indices[degree]
        check(f"degree-{degree:02d} design moment", left == right)

    check("n_0=d=0: the within-fibre disjointness graph is empty", closed[0] == 0)
    check("n_1=120, so n_1+15d=120 is saturated at d=0", closed[1] == 120)
    check("n_14=0 is the Steiner uniqueness condition", closed[14] == 0)
    return indices[0], closed


def section_global_pairs(block_count: int, counts: list[int]) -> None:
    print()
    print("3. global intersection and parity counts")
    check(
        "every non-diagonal row degree is even (b is odd)",
        all(count % 2 == 0 for count in counts[:-1]),
    )
    unordered = [block_count * count // 2 for count in counts[:-1]]
    expected = [
        0,
        1_060_730_100,
        29_700_442_800,
        434_368_975_950,
        3_088_846_051_200,
        12_529_131_795_180,
        29_730_143_242_800,
        43_116_291_922_275,
        38_224_469_883_600,
        20_881_886_325_300,
        6_795_461_312_640,
        1_303_106_927_850,
        128_701_918_800,
        7_425_110_700,
        0,
    ]
    check("all displayed unordered pair counts are exact", unordered == expected)
    check(
        "the relation pair counts partition all unordered block pairs",
        sum(unordered) == comb(block_count, 2) == 156_270_594_639_195,
    )


def section_general_formula() -> None:
    print()
    print("4. the general automatic-intersection formula")
    for k in range(2, 51):
        block_size = k - 1
        # The closed rational row always satisfies the formal moment equations.
        numerators = [
            closed_intersection_number(k, intersection) for intersection in range(k)
        ]
        for degree in range(block_size):
            left_numerator = sum(
                comb(intersection, degree) * numerator
                for intersection, (numerator, denominator) in enumerate(numerators)
            )
            denominator = k + 1
            v = 2 * k - 1
            strength = k - 2
            index_numerator = comb(v - degree, strength - degree)
            index_denominator = comb(block_size - degree, strength - degree)
            right_numerator = comb(block_size, degree) * index_numerator * denominator
            check_denominator = index_denominator
            if left_numerator * check_denominator != right_numerator:
                raise AssertionError(
                    f"general moment formula failed at k={k}, i={degree}"
                )

        n0_numerator, n0_denominator = numerators[0]
        if k % 2 == 0:
            check(
                f"k={k}: the formal disjointness degree is zero",
                n0_numerator == 0,
            )
            n1_numerator, n1_denominator = numerators[1]
            check(
                f"k={k}: n_1=C(k,2)",
                n1_numerator == comb(k, 2) * n1_denominator,
            )
        else:
            check(
                f"k={k}: odd-k n_0=2k/(k+1) is nonintegral",
                (
                    n0_numerator == 2 * k
                    and n0_denominator == k + 1
                    and n0_numerator % n0_denominator != 0
                ),
            )


def section_large_set(block_count: int) -> None:
    print()
    print("5. conditional large-set covering arithmetic")
    fibres = 17
    degree = 16
    vertices = comb(31, 15)
    edges = vertices * degree // 2
    check("all 15-sets split as 17 fibres of size b", vertices == fibres * block_count)
    check(
        "one perfect matching over every pair of fibres gives every Odd-graph edge",
        edges == comb(fibres, 2) * block_count == 2_404_321_560,
    )
    check("every cross-fibre perfect matching has odd size", block_count % 2 == 1)
    check("a lifted base triangle cannot close after one turn", 3 * 15 > 31)

    # In KG(2r+1,r), an odd cycle of length 2q+1 has q >= r:
    # every two-step move changes at most one element.
    r = 15
    odd_girth_lower_bound = 2 * r + 1
    check(
        "the elementary two-step bound gives odd girth at least 31",
        odd_girth_lower_bound == 31,
    )
    permitted_odd_monodromy_lengths = [
        length for length in range(1, 100, 2) if 3 * length >= odd_girth_lower_bound
    ]
    check(
        "the least possible odd triangle-monodromy cycle length is 11",
        permitted_odd_monodromy_lengths[0] == 11,
    )
    check(
        "one b-cycle is an arithmetically feasible odd-sheet monodromy profile",
        block_count % 2 == 1 and block_count >= 11,
    )


def main() -> None:
    section_local_candidates()
    block_count, counts = section_full_moments()
    section_global_pairs(block_count, counts)
    section_general_formula()
    section_large_set(block_count)
    print()
    print(f"ALL {len(CHECKS)} EXACT CHECKS PASSED")
    print("The Steiner equations force d(B)=0; no matching edge exists.")
    print("No LS(14,15,31) construction or nonexistence theorem is claimed.")
    print("Erdos--Rosenfeld problem #835 remains open.")


if __name__ == "__main__":
    main()

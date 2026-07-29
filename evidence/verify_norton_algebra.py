#!/usr/bin/env python3
"""Exact audit of the top-Johnson Norton-compression attack.

For an S(r-1,r,2r+1) constituent D, let P be the orthogonal projector
onto ker W_{r-1,r}, let F_D be the diagonal coordinate projector onto D,
and put T_D=P F_D P on E=ker W.

This verifier checks:

* the universal one- and two-block intersection equations;
* the resulting exact first and second Hilbert--Schmidt moments;
* the exact cubic compression polynomial in the Fano (r=3) and Witt
  (r=5) controls;
* the negative multiplicity forced by extrapolating that polynomial to
  r=15;
* a rank-correct abstract Naimark-compression model at r=15 which has all
  axis, partition-of-unity, rank, trace, and pair-moment data, but has
  eigenvalues 1/6 and 1/9 instead of 1/3.

All decisive calculations use integers or Fraction.  NumPy is used only
for small (at most 66 by 66) integer matrix products.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb, gcd

import numpy as np

try:
    from verify_saturated_support_lattice import build_restricted_matrix
except ModuleNotFoundError:
    from evidence.verify_saturated_support_lattice import (
        build_restricted_matrix,
    )


def lcm(left, right):
    return left // gcd(left, right) * right


def projector_values(r):
    """P_{A,B} as a function of t=|A intersect B|."""
    q = r + 2
    return [
        Fraction((-1) ** (r - t) * 2, q * comb(r + 1, t + 1))
        for t in range(r + 1)
    ]


def steiner_intersection_distribution(r, same):
    """Fixed-block intersection distribution against one constituent.

    If ``same`` is true, the fixed block belongs to the constituent and
    a_r=1.  Otherwise the two constituents are block-disjoint and a_r=0.
    The remaining entries are forced by the S(r-1,r,2r+1) equations.
    """
    v = 2 * r + 1
    counts = [0] * (r + 1)
    counts[r] = int(same)
    for s in range(r - 1, -1, -1):
        numerator = comb(v - s, r - 1 - s)
        assert numerator % (r - s) == 0
        lambda_s = numerator // (r - s)
        counts[s] = (
            comb(r, s) * lambda_s
            - sum(
                comb(t, s) * counts[t]
                for t in range(s + 1, r + 1)
            )
        )
    assert all(count >= 0 for count in counts)
    return counts


def universal_moments(r):
    q = r + 2
    total_vertices = comb(2 * r + 1, r)
    assert total_vertices % q == 0
    n = total_vertices // q
    values = projector_values(r)
    same = steiner_intersection_distribution(r, True)
    cross = steiner_intersection_distribution(r, False)

    trace = Fraction(2 * n, q)
    trace2 = n * sum(
        Fraction(same[t]) * values[t] ** 2 for t in range(r + 1)
    )
    cross2 = n * sum(
        Fraction(cross[t]) * values[t] ** 2 for t in range(r + 1)
    )

    closed_trace2 = Fraction(
        2 * n * (3 * q - 1),
        q * q * (q + 1),
    )
    assert trace2 == closed_trace2
    assert trace2 + (q - 1) * cross2 == trace
    return {
        "q": q,
        "n": n,
        "dimension": 2 * n,
        "same": same,
        "cross": cross,
        "trace": trace,
        "trace2": trace2,
        "cross2": cross2,
    }


def canonical_design(r):
    _, _, base, _ = build_restricted_matrix(2 * r + 1, r)
    design = sorted(tuple(sorted(block)) for block in base)
    assert len(design) == comb(2 * r + 1, r) // (r + 2)
    return design


def scaled_compression(design, r):
    """Return L and the integer matrix A=L*(F P F)."""
    values = projector_values(r)
    scale = 1
    for value in values:
        scale = lcm(scale, value.denominator)
    matrix = np.array(
        [
            [
                int(values[len(set(left) & set(right))] * scale)
                for right in design
            ]
            for left in design
        ],
        dtype=np.int64,
    )
    return scale, matrix


def check_small_cubic(r):
    q = r + 2
    design = canonical_design(r)
    scale, matrix = scaled_compression(design, r)
    identity = np.eye(len(design), dtype=np.int64)

    # If K=A/L, this is a nonzero scalar multiple of
    # K(K-I/3)(K-(q-1)I/q).
    polynomial = (
        matrix
        @ (3 * matrix - scale * identity)
        @ (q * matrix - (q - 1) * scale * identity)
    )
    assert np.count_nonzero(polynomial) == 0

    data = universal_moments(r)
    high = Fraction(q - 1, q)
    high_multiplicity = (
        data["trace2"] - data["trace"] / 3
    ) / (high * (high - Fraction(1, 3)))
    third_multiplicity = 3 * (
        data["trace"] - high_multiplicity * high
    )
    zero_multiplicity = (
        data["dimension"] - high_multiplicity - third_multiplicity
    )

    assert high_multiplicity == 1
    assert third_multiplicity == {3: 6, 5: 54}[r]
    assert zero_multiplicity == {3: 7, 5: 77}[r]

    # Check the first three traces directly on the small integer matrix.
    trace1 = Fraction(int(np.trace(matrix)), scale)
    trace2 = Fraction(int(np.trace(matrix @ matrix)), scale**2)
    trace3 = Fraction(
        int(np.trace(matrix @ matrix @ matrix)),
        scale**3,
    )
    predicted3 = high**3 + third_multiplicity * Fraction(1, 27)
    assert trace1 == data["trace"]
    assert trace2 == data["trace2"]
    assert trace3 == predicted3
    return {
        "scale": scale,
        "high_multiplicity": high_multiplicity,
        "third_multiplicity": third_multiplicity,
        "zero_multiplicity": zero_multiplicity,
        "trace3": trace3,
    }


def affine_orbit(block, prime=17):
    return {
        frozenset((a * x + b) % prime for x in block)
        for a in range(1, prime)
        for b in range(prime)
    }


def design_parameters(blocks, prime=17):
    point_counts = Counter()
    pair_counts = Counter()
    for block in blocks:
        for point in block:
            point_counts[point] += 1
        for pair in combinations(sorted(block), 2):
            pair_counts[pair] += 1
    assert len(set(point_counts.values())) == 1
    assert len(set(pair_counts.values())) == 1
    return (
        next(iter(point_counts.values())),
        next(iter(pair_counts.values())),
    )


def check_rank_correct_model():
    """Build the exact r=15 abstract compression countermodel by counts."""
    data = universal_moments(15)
    q = data["q"]
    n = data["n"]
    h = Fraction(q - 1, q)
    z_dimension = data["dimension"] - (q - 1)

    z_trace = data["trace"] - h
    z_self2 = data["trace2"] - h**2
    z_cross2 = data["cross2"] - Fraction(1, q * q)
    assert z_trace == 2_079_862
    assert z_self2 == 339_846
    assert z_cross2 == 108_751

    # Solve x+y=z and x/6+y/9=q*tr(S_i^2).
    six_coordinates = 18 * q * int(z_self2) - 2 * z_dimension
    nine_coordinates = z_dimension - six_coordinates
    assert six_coordinates == 33_277_568
    assert nine_coordinates == 2_080_086

    six_orbit = affine_orbit({0, 1, 2, 3, 4, 6})
    quadratic_residues = {x * x % q for x in range(1, q)}
    nine_orbit = affine_orbit({0} | quadratic_residues)
    assert len(six_orbit) == 272
    assert len(nine_orbit) == 34
    assert design_parameters(six_orbit) == (96, 30)
    assert design_parameters(nine_orbit) == (18, 9)

    assert six_coordinates % len(six_orbit) == 0
    assert nine_coordinates % len(nine_orbit) == 0
    six_repeats = six_coordinates // len(six_orbit)
    nine_repeats = nine_coordinates // len(nine_orbit)
    assert six_repeats == 122_344
    assert nine_repeats == 61_179

    six_rank = six_repeats * 96
    nine_rank = nine_repeats * 18
    six_lambda = six_repeats * 30
    nine_lambda = nine_repeats * 9
    assert six_rank == 11_745_024
    assert nine_rank == 1_101_222
    assert six_lambda == 3_670_320
    assert nine_lambda == 550_611

    assert Fraction(six_rank, 6) + Fraction(nine_rank, 9) == z_trace
    assert Fraction(six_rank, 6**2) + Fraction(
        nine_rank, 9**2
    ) == z_self2
    assert Fraction(six_lambda, 6**2) + Fraction(
        nine_lambda, 9**2
    ) == z_cross2

    full_rank = 1 + six_rank + nine_rank
    zero_multiplicity = data["dimension"] - full_rank
    assert full_rank == 12_846_247
    assert full_rank <= n
    assert zero_multiplicity == 22_511_423

    # Its spectrum is {0,1/9,1/6,16/17}, so it deliberately violates
    # the small-case cubic while matching all moments through order two.
    assert all(
        root not in (Fraction(1, 3),)
        for root in (Fraction(1, 6), Fraction(1, 9))
    )
    full_trace3 = (
        h**3
        + Fraction(six_rank, 6**3)
        + Fraction(nine_rank, 9**3)
    )
    repeated_pair3 = (
        Fraction(q - 1, q**3)
        + Fraction(six_lambda, 6**3)
        + Fraction(nine_lambda, 9**3)
    )
    assert full_trace3 + (q - 1) * repeated_pair3 == data["trace2"]

    # Third-colour data already varies among triples.  This is exactly
    # the information absent from the one- and two-block equations.
    triples = [(0, 1, 2), (0, 1, 3), (0, 1, 4)]
    expected_orbit_counts = [(12, 5), (8, 4), (6, 4)]
    mixed_traces = []
    for triple, expected in zip(triples, expected_orbit_counts):
        triple_set = set(triple)
        counts = (
            sum(triple_set <= block for block in six_orbit),
            sum(triple_set <= block for block in nine_orbit),
        )
        assert counts == expected
        mixed_traces.append(
            -Fraction(1, q**3)
            + Fraction(six_repeats * counts[0], 6**3)
            + Fraction(nine_repeats * counts[1], 9**3)
        )
    assert len(set(mixed_traces)) == 3

    return {
        "six_coordinates": six_coordinates,
        "nine_coordinates": nine_coordinates,
        "rank": full_rank,
        "zero_multiplicity": zero_multiplicity,
        "trace3": full_trace3,
        "mixed_traces": mixed_traces,
    }


def main():
    small = {}
    for r in (3, 5):
        data = universal_moments(r)
        small[r] = check_small_cubic(r)
        print(
            f"[r={r}] tr(T)={data['trace']}, "
            f"tr(T^2)={data['trace2']}, "
            f"cross={data['cross2']}"
        )
        print(
            f"[r={r}] exact spectrum: "
            f"0^{small[r]['zero_multiplicity']}, "
            f"(1/3)^{small[r]['third_multiplicity']}, "
            f"({r + 1}/{r + 2})^1"
        )

    target = universal_moments(15)
    q = target["q"]
    high = Fraction(q - 1, q)
    high_multiplicity = (
        target["trace2"] - target["trace"] / 3
    ) / (high * (high - Fraction(1, 3)))
    third_multiplicity = 3 * (
        target["trace"] - high_multiplicity * high
    )
    assert high_multiplicity == Fraction(-2_471_235, 4)
    assert third_multiplicity == 7_983_990
    print(
        f"[r=15] tr(T)={target['trace']}, "
        f"tr(T^2)={target['trace2']}, "
        f"cross={target['cross2']}"
    )
    print(
        "[r=15] extrapolated cubic multiplicities: "
        f"m_16/17={high_multiplicity}, "
        f"m_1/3={third_multiplicity} (impossible)"
    )

    model = check_rank_correct_model()
    print(
        "[model] spectrum: "
        f"0^{model['zero_multiplicity']}, "
        "(1/9)^1101222, (1/6)^11745024, (16/17)^1"
    )
    print(
        f"[model] rank={model['rank']} <= {target['n']}; "
        f"tr(T^3)={model['trace3']}"
    )
    print(
        "[model] three distinct mixed cubic traces: "
        + ", ".join(str(value) for value in model["mixed_traces"])
    )
    print(
        "PASS: the small cubic is exact but not forced by the universal "
        "axis/rank/two-moment data."
    )


if __name__ == "__main__":
    main()

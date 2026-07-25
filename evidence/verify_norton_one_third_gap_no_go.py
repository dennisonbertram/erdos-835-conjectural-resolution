#!/usr/bin/env python3
"""Exact arithmetic audit for the Norton one-third-gap no-go.

The script uses only Python's standard library.  It checks the universal
trace moments, the common diagonal of K^2-K/3, the trace-ratio bound, and
the multiplicity bound for eigenvalues in (0,1/3).
"""

from fractions import Fraction
from math import ceil, comb


def target_data(r):
    q = r + 2
    total = comb(2 * r + 1, r)
    assert total % q == 0
    n = total // q

    trace = Fraction(2 * n, q)
    trace2 = Fraction(
        2 * n * (3 * q - 1),
        q * q * (q + 1),
    )
    diagonal = Fraction(
        2 * (-q * q + 8 * q - 3),
        3 * q * q * (q + 1),
    )
    ratio = trace2 / trace
    deficit = trace / 3 - trace2
    low_count_bound = ceil(36 * deficit) if deficit > 0 else 0

    # The per-row calculation and the trace calculation agree.
    assert diagonal == trace2 / n - Fraction(2, 3 * q)
    assert ratio == Fraction(3 * q - 1, q * (q + 1))
    assert deficit == Fraction(
        2 * n * (q * q - 8 * q + 3),
        3 * q * q * (q + 1),
    )

    return {
        "r": r,
        "q": q,
        "n": n,
        "trace": trace,
        "trace2": trace2,
        "diagonal": diagonal,
        "ratio": ratio,
        "deficit": deficit,
        "low_count_bound": low_count_bound,
    }


def main():
    # Positive controls: their exact spectra are the Fano and Witt spectra.
    fano = target_data(3)
    assert fano["ratio"] == Fraction(7, 15)
    assert fano["diagonal"] == Fraction(4, 75)
    assert (
        6 * Fraction(1, 3) + Fraction(4, 5)
        == fano["trace"]
    )
    assert (
        6 * Fraction(1, 9) + Fraction(16, 25)
        == fano["trace2"]
    )

    witt = target_data(5)
    assert witt["ratio"] == Fraction(5, 14)
    assert witt["diagonal"] == Fraction(1, 147)
    assert (
        54 * Fraction(1, 3) + Fraction(6, 7)
        == witt["trace"]
    )
    assert (
        54 * Fraction(1, 9) + Fraction(36, 49)
        == witt["trace2"]
    )

    target = target_data(15)
    assert target["q"] == 17
    assert target["n"] == 17_678_835
    assert target["trace"] == Fraction(35_357_670, 17)
    assert target["trace2"] == Fraction(98_215_750, 289)
    assert target["diagonal"] == Fraction(-52, 2601)
    assert target["ratio"] == Fraction(25, 153)
    assert target["ratio"] < Fraction(1, 3)
    assert target["deficit"] == Fraction(102_144_380, 289)
    assert 36 * target["deficit"] == Fraction(
        3_677_197_680,
        289,
    )
    assert target["low_count_bound"] == 12_723_868
    assert (
        Fraction(target["low_count_bound"] - 1)
        < 36 * target["deficit"]
        <= Fraction(target["low_count_bound"])
    )

    # The common diagonal changes sign before the next arithmetically
    # relevant controls: -q^2+8q-3 is negative for every integer q >= 8.
    for q in range(8, 40):
        assert -q * q + 8 * q - 3 < 0

    print(
        "Fano control: ratio=7/15, "
        "diag(K^2-K/3)=4/75"
    )
    print(
        "Witt control: ratio=5/14, "
        "diag(K^2-K/3)=1/147"
    )
    print(
        "r=15 target: ratio=25/153, "
        "diag(K^2-K/3)=-52/2601"
    )
    print(
        "r=15 forced sub-1/3 multiplicity: "
        "at least 12,723,868"
    )
    print("Norton one-third-gap no-go audit: PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify the critical-group audit for a putative O_k -> K_{k+1} cover.

The k=4 control is checked by an exact Smith normal form.  The k=16
calculation uses the known integral spectrum of the Odd graph and exact
integer arithmetic; constructing its 300,540,195-square Laplacian is
neither necessary nor useful.
"""

from collections import Counter
from itertools import combinations
from math import comb

from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ


def odd_graph_laplacian(k):
    vertices = list(combinations(range(2 * k - 1), k - 1))
    adjacency = Matrix(
        [
            [int(set(left).isdisjoint(right)) for right in vertices]
            for left in vertices
        ]
    )
    return k * Matrix.eye(len(vertices)) - adjacency


def odd_graph_spectrum(k):
    """Return (Laplacian eigenvalue, multiplicity) for O_k."""
    v = 2 * k - 1
    spectrum = []
    for i in range(k):
        adjacency_eigenvalue = (-1) ** i * (k - i)
        laplacian_eigenvalue = k - adjacency_eigenvalue
        multiplicity = comb(v, i) - (comb(v, i - 1) if i else 0)
        spectrum.append((laplacian_eigenvalue, multiplicity))
    return spectrum


def valuation(number, prime):
    exponent = 0
    while number % prime == 0:
        number //= prime
        exponent += 1
    return exponent


def predicted_p_primary(k):
    """Return p, sheet degree, and the exact p-primary critical group rank."""
    p = k + 1
    vertex_count = comb(2 * k - 1, k - 1)
    sheet_degree, remainder = divmod(vertex_count, p)
    assert remainder == 0
    assert sheet_degree % p != 0

    spectrum = odd_graph_spectrum(k)
    p_order = (
        sum(valuation(eigenvalue, p) * multiplicity
            for eigenvalue, multiplicity in spectrum
            if eigenvalue)
        - valuation(vertex_count, p)
    )
    top_multiplicity = spectrum[-1][1]
    assert spectrum[-1][0] == p
    assert all(
        eigenvalue % p != 0
        for eigenvalue, _ in spectrum[1:-1]
    )
    assert valuation(vertex_count, p) == 1
    assert p_order == top_multiplicity - 1

    # The saturated integral p-eigenspace has top_multiplicity independent
    # reductions in the mod-p Laplacian kernel.  Hence the p-rank of the
    # critical group is at least top_multiplicity-1.  Its p-order has exactly
    # that valuation, forcing every p-primary invariant factor to equal p.
    p_rank = top_multiplicity - 1
    return p, vertex_count, sheet_degree, p_rank


def main():
    # Full exact control computation.
    laplacian_4 = odd_graph_laplacian(4)
    reduced_4 = laplacian_4[:-1, :-1]
    smith_4 = smith_normal_form(reduced_4, domain=ZZ)
    diagonal_4 = [
        abs(int(smith_4[i, i]))
        for i in range(smith_4.rows)
    ]
    assert Counter(diagonal_4) == Counter({1: 20, 2: 1, 10: 8, 70: 5})
    assert sum(value % 5 == 0 for value in diagonal_4) == 13
    assert sum(valuation(value, 5) for value in diagonal_4) == 13

    p4, vertices4, sheets4, rank4 = predicted_p_primary(4)
    assert (p4, vertices4, sheets4, rank4) == (5, 35, 7, 13)

    p16, vertices16, sheets16, rank16 = predicted_p_primary(16)
    assert (
        p16,
        vertices16,
        sheets16,
        rank16,
    ) == (
        17,
        300_540_195,
        17_678_835,
        35_357_669,
    )
    assert sheets16 % 17 == 8

    print("K(O_4) Smith factors:", dict(sorted(Counter(diagonal_4).items())))
    print("Jac(O_4)[5] = (Z/5)^13; Jac(K_5) = (Z/5)^3")
    print(
        "O_16 -> K_17 candidate:",
        f"{sheets16} sheets, degree mod 17 = {sheets16 % 17}",
    )
    print(
        "Jac(O_16)[17] = (Z/17)^35357669;",
        "Jac(K_17) = (Z/17)^15",
    )
    print("critical-group cover audit: PASS (no obstruction)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify the exact arithmetic in mod17_odd_graph_jordan.md."""

from math import comb


MODULUS = 17


def main():
    eigenvalues = [(-1) ** i * (16 - i) for i in range(16)]
    assert eigenvalues == [
        16,
        -15,
        14,
        -13,
        12,
        -11,
        10,
        -9,
        8,
        -7,
        6,
        -5,
        4,
        -3,
        2,
        -1,
    ]

    vertex_count = comb(31, 15)
    fibre_size = vertex_count // 17
    minus_one_multiplicity = vertex_count - comb(31, 14)
    assert vertex_count == 300540195
    assert fibre_size == 17678835
    assert fibre_size % MODULUS == 8
    assert minus_one_multiplicity == 35357670

    def q(value):
        out = 1
        for eigenvalue in eigenvalues[1:15]:
            out *= value - eigenvalue
        return out

    g_at_16 = 17 * q(16)
    projection_scalar, remainder = divmod(g_at_16, vertex_count)
    assert remainder == 0
    assert projection_scalar == 203212800
    assert projection_scalar % MODULUS == 2
    assert q(16) % MODULUS == 16
    assert q(-1) % MODULUS == 16

    diagonal_numerator = (
        q(16) ** 2 + minus_one_multiplicity * q(-1) ** 2
    )
    q_squared_diagonal, remainder = divmod(
        diagonal_numerator, vertex_count
    )
    assert remainder == 0
    assert q_squared_diagonal % MODULUS == 15

    inverse_two = pow(2, -1, MODULUS)
    assert inverse_two == 9
    assert inverse_two * q(16) % MODULUS == 8
    assert (
        inverse_two**2 * q_squared_diagonal % MODULUS
    ) == 8

    print("mod-17 O_16 Jordan arithmetic: VERIFIED")
    print("(M+I)q(M) = 203212800 J = 2 J (mod 17)")
    print("x=(1/2)q(M)e_v has T x=1, <1,x>=8, <x,x>=8")
    print("the required nondegenerate size-two Jordan plane is present")


if __name__ == "__main__":
    main()

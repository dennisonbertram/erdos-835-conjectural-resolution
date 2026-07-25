#!/usr/bin/env python3
"""Exact MacWilliams check for the determinant-construction route at k=16.

A valid maximal-minor coloring would force an isodual [32,16,16]_17
near-MDS code.  The dependent 16-column sets would be one S(15,16,32),
so the number of weight-16 words in the dual would be

    A_16 = (17-1) * C(32,16) / 17.

This script solves the q-ary self-dual MacWilliams equations exactly and
checks whether that required value is compatible with nonnegative integral
weight coefficients.  It is a diagnostic, not by itself a proof that every
valid coloring is linear/determinantal.
"""

from math import comb
import sympy as sp


N = 32
Q = 17
K = 16


def krawtchouk(j, i):
    return sum(
        (-1) ** h
        * (Q - 1) ** (j - h)
        * comb(i, h)
        * comb(N - i, j - h)
        for h in range(max(0, j - (N - i)), min(j, i) + 1)
    )


def main():
    unknown_indices = list(range(16, N + 1))
    variables = sp.symbols(" ".join(f"A{i}" for i in unknown_indices))
    coefficient = dict(zip(unknown_indices, variables))

    def a(i):
        if i == 0:
            return sp.Integer(1)
        if i < 16:
            return sp.Integer(0)
        return coefficient[i]

    equations = []
    for j in range(N + 1):
        transformed = sum(a(i) * krawtchouk(j, i) for i in range(N + 1))
        equations.append(sp.Eq((Q ** K) * a(j), transformed))

    solution = sp.linsolve(
        [equation.lhs - equation.rhs for equation in equations],
        variables,
    )
    print(f"solution_dimension_input_variables={len(variables)}")
    print(f"macwilliams_solution={solution}")

    tuples = list(solution)
    assert len(tuples) == 1
    solved = tuples[0]
    required_a16 = (Q - 1) * comb(N, 16) // Q
    print(f"required_A16={required_a16}")

    free = sorted(
        set().union(*(entry.free_symbols for entry in solved)),
        key=str,
    )
    print("free_symbols=" + ",".join(map(str, free)))
    if len(free) == 1:
        parameter = free[0]
        value = sp.solve(
            sp.Eq(solved[0], required_a16),
            parameter,
        )[0]
        instantiated = [sp.simplify(entry.subs(parameter, value)) for entry in solved]
    elif not free:
        instantiated = list(solved)
        assert instantiated[0] == required_a16
    else:
        raise AssertionError("unexpectedly more than one free parameter")

    all_integral = all(entry.q == 1 for entry in instantiated)
    all_nonnegative = all(entry >= 0 for entry in instantiated)
    print(f"all_integral={all_integral}")
    print(f"all_nonnegative={all_nonnegative}")
    for weight, count in zip(unknown_indices, instantiated):
        print(f"A{weight}={count}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit the affine ternary radius-five ansatz for the cyclic G(17) chart.

This is deliberately a *local* calculation.  It proves only that the
displayed cyclic golf chart cannot be extended by a ternary rule

    P_ij(u,v,w) = a_ij (u+v+w) + b_ij   in F_17,

even when the missing colour and the affine parameters are allowed to vary
with ij.  It does not concern arbitrary P_ij, another golf chart, or a global
O_16 colouring.
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parent
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))
from global_latin_audit import construct_golf17


FIELD = range(17)
SQUARES = range(15)


def omitted_values(a: int, b: int, u: int, v: int, infinity: int) -> set[int]:
    """Values missing as w ranges over F_17 minus {infinity,u,v}."""
    return {(a * (u + v + w) + b) % 17 for w in (infinity, u, v)}


def main() -> None:
    golf = construct_golf17()

    # Confirm the only properties of the golf array used by the test.
    for u, v in combinations(FIELD, 2):
        assert {golf[i][u][v] for i in SQUARES} == set(FIELD) - {u, v}

    tested = 0
    surviving = []
    for infinity in FIELD:
        finite = tuple(x for x in FIELD if x != infinity)
        for i, j in combinations(SQUARES, 2):
            for a in range(1, 17):
                for b in FIELD:
                    tested += 1
                    # A radius-five rule must avoid both M_i(uv) and
                    # M_j(uv) for every pair uv.  Since the affine rule is
                    # injective in w, this is equivalent to saying that both
                    # values occur among its three omitted values.
                    if all(
                        {golf[i][u][v], golf[j][u][v]}
                        <= omitted_values(a, b, u, v, infinity)
                        for u, v in combinations(finite, 2)
                    ):
                        surviving.append((infinity, i, j, a, b))

    assert tested == 17 * 105 * 16 * 17
    assert surviving == []
    print("cyclic G(17) pair-transversal property: PASS")
    print(f"affine ternary rules tested: {tested}")
    print("surviving rules: 0")
    print("conclusion: cyclic-chart affine ternary radius-5 ansatz: REFUTED")


if __name__ == "__main__":
    main()

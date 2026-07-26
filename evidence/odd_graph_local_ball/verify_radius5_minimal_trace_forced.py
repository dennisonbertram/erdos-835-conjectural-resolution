#!/usr/bin/env python3
"""Finite audit for the theorem that radius five forces minimal N-traces.

The proof is symbolic and chart-independent.  This verifier checks its
general counting identity for a range of even k and instantiates every
matching/missing-vertex/parity count on the verified Wallis G(17).
"""

from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parents[1]
if str(EVIDENCE) not in sys.path:
    sys.path.insert(0, str(EVIDENCE))

from global_latin_audit import construct_golf17  # noqa: E402


def symbolic_audit() -> None:
    for k in range(4, 202, 2):
        infinity_odd_vertices = k
        finite_odd_vertices = k - 2
        lower_infinity = infinity_odd_vertices // 2
        lower_finite = finite_odd_vertices // 2
        assert (
            lower_infinity + k * lower_finite
            == k * (k - 1) // 2
        )


def covered_vertices(
    golf: list[list[list[int]]],
    square: int,
    colour: int,
) -> tuple[set[tuple[int, int]], set[int]]:
    finite = tuple(range(16))
    edges = {
        edge
        for edge in combinations(finite, 2)
        if golf[square][edge[0]][edge[1]] == colour
    }
    covered = {vertex for edge in edges for vertex in edge}
    assert len(covered) == 2 * len(edges)
    return edges, covered


def wallis_audit() -> dict[str, int | str]:
    golf = construct_golf17()
    finite = tuple(range(16))
    infinity = 16
    squares = tuple(range(15))
    colours = finite + (infinity,)

    traces_checked = 0
    parity_vertices_checked = 0
    for i, j in combinations(squares, 2):
        lower_sum = 0
        for colour in colours:
            edges_i, covered_i = covered_vertices(golf, i, colour)
            edges_j, covered_j = covered_vertices(golf, j, colour)
            assert edges_i.isdisjoint(edges_j)

            required_odd = {
                u
                for u in finite
                if (1 + (u in covered_i) + (u in covered_j)) % 2
            }
            parity_vertices_checked += len(finite)

            if colour == infinity:
                assert len(edges_i) == len(edges_j) == 8
                assert covered_i == covered_j == set(finite)
                assert required_odd == set(finite)
                lower = 8
            else:
                pre_i = {
                    u for u in finite if golf[i][u][infinity] == colour
                }
                pre_j = {
                    u for u in finite if golf[j][u][infinity] == colour
                }
                assert len(pre_i) == len(pre_j) == 1
                assert pre_i.isdisjoint(pre_j)
                missing_i = set(finite) - covered_i
                missing_j = set(finite) - covered_j
                assert missing_i == {colour} | pre_i
                assert missing_j == {colour} | pre_j
                assert required_odd == set(finite) - pre_i - pre_j
                assert len(required_odd) == 14
                assert len(edges_i) == len(edges_j) == 7
                lower = 7

            assert lower == len(required_odd) // 2
            lower_sum += lower
            traces_checked += 1

        assert lower_sum == len(tuple(combinations(finite, 2))) == 120

    return {
        "status": "PASS",
        "scope": (
            "symbolic count plus Wallis finite audit; "
            "the theorem itself is chart-independent"
        ),
        "even_k_values_checked": len(range(4, 202, 2)),
        "wallis_square_pairs": 105,
        "trace_colours_checked": traces_checked,
        "parity_vertex_checks": parity_vertices_checked,
        "k16_lower_bound_sum": 120,
    }


def main() -> None:
    symbolic_audit()
    print(json.dumps(wallis_audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

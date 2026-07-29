#!/usr/bin/env python3
"""Test cut and crossing-Hall screens on two exact r=0 obstructions.

This is a diagnostic verifier, not a proof of the coordinated-nine theorem.
It independently checks whether the necessary inequalities proposed in the
Opus 5 audit detect the targeted bad triple in the orbit-4 certificate and
the all-35 disconnected certificate.
"""

from __future__ import annotations

import argparse
import sys
from functools import lru_cache
from itertools import combinations
from pathlib import Path


VERTICES = frozenset(range(13))
EDGES = tuple(combinations(sorted(VERTICES), 2))

ORBIT4_PREFIX = (
    ((0, 6), (2, 4), (9, 12), (10, 11)),
    ((0, 1), (3, 7), (5, 8), (10, 12)),
    ((3, 12), (5, 10), (7, 11), (8, 9)),
    ((0, 3), (1, 5), (7, 12), (8, 10), (9, 11)),
    ((0, 4), (2, 6), (5, 9), (7, 8), (11, 12)),
    ((0, 2), (1, 6), (5, 7), (8, 11), (9, 10)),
)
ORBIT4_ROWS = ((0, 1, 2), (0, 1, 2), (0, 3, 4))

GLOBAL_PREFIX = (
    ((0, 12), (1, 2), (3, 5), (9, 10)),
    ((0, 10), (1, 11), (4, 6), (7, 8)),
    ((0, 2), (1, 12), (3, 8), (6, 7)),
    ((2, 10), (3, 6), (4, 7), (5, 8), (11, 12)),
    ((0, 11), (1, 10), (4, 8), (5, 7), (9, 12)),
    ((0, 1), (2, 11), (3, 7), (4, 5), (6, 8)),
)
GLOBAL_ROWS = ((0, 1, 2), (1, 10, 11), (1, 9, 10))


@lru_cache(maxsize=None)
def maximum_matching_size(vertices: frozenset[int], edges: frozenset[tuple[int, int]]) -> int:
    """Return the exact maximum matching size by a small recursive search."""
    if len(vertices) < 2:
        return 0
    vertex = min(vertices)
    without_vertex = maximum_matching_size(vertices - {vertex}, edges)
    with_vertex = max(
        (
            1
            + maximum_matching_size(
                vertices - {vertex, neighbour},
                edges,
            )
            for neighbour in vertices - {vertex}
            if tuple(sorted((vertex, neighbour))) in edges
        ),
        default=0,
    )
    return max(without_vertex, with_vertex)


def deficiency(vertices: frozenset[int], edges: frozenset[tuple[int, int]]) -> int:
    induced = frozenset(edge for edge in edges if set(edge) <= vertices)
    return len(vertices) - 2 * maximum_matching_size(vertices, induced)


def screens(
    prefix: tuple[tuple[tuple[int, int], ...], ...],
    rows: tuple[tuple[int, ...], ...],
) -> dict[str, list[dict[str, object]]]:
    deleted = frozenset(edge for layer in prefix for edge in layer)
    residual = frozenset(edge for edge in EDGES if edge not in deleted)
    supports = tuple(VERTICES - frozenset(row) for row in rows)
    cut_violations: list[dict[str, object]] = []
    hall_violations: list[dict[str, object]] = []

    for size in range(14):
        for u_tuple in combinations(sorted(VERTICES), size):
            left = frozenset(u_tuple)
            right = VERTICES - left
            internal_left = sum(set(edge) <= left for edge in residual)
            internal_right = sum(set(edge) <= right for edge in residual)
            phi = tuple(
                len(support & left) - len(support) // 2 for support in supports
            )
            positive = sum(max(0, value) for value in phi)
            negative = sum(max(0, -value) for value in phi)
            if positive > internal_left or negative > internal_right:
                cut_violations.append(
                    {
                        "U": sorted(left),
                        "phi": phi,
                        "positive": positive,
                        "e_U": internal_left,
                        "negative": negative,
                        "e_W": internal_right,
                    }
                )

            c_min = tuple(
                max(
                    deficiency(support & left, residual),
                    deficiency(support & right, residual),
                )
                for support in supports
            )
            for count in range(1, len(rows) + 1):
                for chosen in combinations(range(len(rows)), count):
                    crossing_union = frozenset(
                        edge
                        for index in chosen
                        for edge in residual
                        if (
                            edge[0] in supports[index]
                            and edge[1] in supports[index]
                            and ((edge[0] in left) != (edge[1] in left))
                        )
                    )
                    required = sum(c_min[index] for index in chosen)
                    if required > len(crossing_union):
                        hall_violations.append(
                            {
                                "U": sorted(left),
                                "rows": chosen,
                                "c_min": tuple(c_min[index] for index in chosen),
                                "required": required,
                                "crossing_union": len(crossing_union),
                            }
                        )

    return {"cut": cut_violations, "crossing_hall": hall_violations}


def audit_searched_orbits() -> None:
    """Regenerate the nine targeted full-row counterexamples and screen them."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from collaboration.r0_three_family_helly_gate.search_counterexamples import (
        solve_orbit,
        support_orbits,
    )

    orbits = support_orbits()
    for orbit_index in range(2, 11):
        signature, omitted_triples = orbits[orbit_index]
        result = solve_orbit(
            orbit_index,
            signature,
            omitted_triples,
            cut_batch=10_000,
            full_rows=True,
            max_rounds=0,
        )
        assert result["status"] == "counterexample"
        prefix = tuple(
            tuple(tuple(edge) for edge in layer)
            for layer in result["prefix"]
        )
        rows = tuple(
            tuple(row) for row in result["remaining_complements"][:3]
        )
        outcome = screens(prefix, rows)
        assert outcome["cut"], f"orbit {orbit_index} lacks a cut witness"
        assert not outcome["crossing_hall"], (
            f"orbit {orbit_index} unexpectedly violates crossing-Hall"
        )
        print(
            f"orbit={orbit_index} "
            f"cut_violations={len(outcome['cut'])} "
            f"crossing_hall_violations={len(outcome['crossing_hall'])}"
        )
        print(f"orbit={orbit_index} first_cut={outcome['cut'][:1]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--search-orbits",
        action="store_true",
        help="also regenerate and screen the targeted bad-prefix orbits 2--10",
    )
    args = parser.parse_args()

    orbit4 = screens(ORBIT4_PREFIX, ORBIT4_ROWS)
    global_obstruction = screens(GLOBAL_PREFIX, GLOBAL_ROWS)

    assert len(orbit4["cut"]) == 2
    assert not orbit4["crossing_hall"]
    assert len(global_obstruction["cut"]) == 2
    assert not global_obstruction["crossing_hall"]

    print(f"orbit4_cut_violations={len(orbit4['cut'])}")
    print(f"orbit4_first_cut_violation={orbit4['cut'][:1]}")
    print(
        "orbit4_crossing_hall_violations="
        f"{len(orbit4['crossing_hall'])}"
    )
    print(
        "orbit4_first_crossing_hall_violation="
        f"{orbit4['crossing_hall'][:1]}"
    )
    print(f"global_cut_violations={len(global_obstruction['cut'])}")
    print(
        "global_crossing_hall_violations="
        f"{len(global_obstruction['crossing_hall'])}"
    )
    if args.search_orbits:
        audit_searched_orbits()
    print("status=ok")


if __name__ == "__main__":
    main()

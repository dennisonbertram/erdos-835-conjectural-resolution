#!/usr/bin/env python3
"""Audit the characteristic-3 shadow of the two universal k=6 controls.

The explicit 18-cell/11-triangle gadgets are genuinely nonlinear: their
systems Bx=1 are consistent over F_3 even though they admit no rainbow
3-colouring.  The complete fan hypergraphs do have characteristic-3 linear
certificates.  This script reconstructs and checks both statements exactly.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
K6 = REPO / "collaboration" / "fan_small_controls"
sys.path.insert(0, str(K6))

from k6_large_sets import (  # noqa: E402
    systems_to_link,
    type_a_systems,
    type_b_systems,
)
from search_k6_fan import build_control_from_link  # noqa: E402
from verify_all_k6_links import TYPE_A_CLIQUES, TYPE_B_CLIQUES  # noqa: E402


P = 3


def eliminate(
    equations: tuple[tuple[dict[int, int], int], ...],
    track_certificate: bool,
) -> tuple[int, dict[int, int] | None]:
    pivots: dict[
        int,
        tuple[dict[int, int], int, dict[int, int]],
    ] = {}
    for equation_index, (source_row, source_rhs) in enumerate(equations):
        row = dict(source_row)
        rhs = source_rhs % P
        combination = {equation_index: 1}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                inverse = pow(row[pivot], -1, P)
                row = {
                    j: coefficient * inverse % P
                    for j, coefficient in row.items()
                    if coefficient % P
                }
                combination = {
                    j: coefficient * inverse % P
                    for j, coefficient in combination.items()
                    if coefficient % P
                }
                pivots[pivot] = row, rhs * inverse % P, combination
                break
            pivot_row, pivot_rhs, pivot_combination = pivots[pivot]
            factor = row[pivot]
            for j, coefficient in pivot_row.items():
                value = (row.get(j, 0) - factor * coefficient) % P
                if value:
                    row[j] = value
                else:
                    row.pop(j, None)
            rhs = (rhs - factor * pivot_rhs) % P
            if track_certificate:
                for j, coefficient in pivot_combination.items():
                    value = (combination.get(j, 0) - factor * coefficient) % P
                    if value:
                        combination[j] = value
                    else:
                        combination.pop(j, None)
        else:
            if rhs:
                return len(pivots), combination
    return len(pivots), None


def check_certificate(
    equations: tuple[tuple[dict[int, int], int], ...],
    certificate: dict[int, int],
) -> None:
    column_sums: dict[int, int] = {}
    rhs_sum = 0
    for equation_index, weight in certificate.items():
        row, rhs = equations[equation_index]
        rhs_sum = (rhs_sum + weight * rhs) % P
        for column, coefficient in row.items():
            column_sums[column] = (
                column_sums.get(column, 0) + weight * coefficient
            ) % P
    if any(column_sums.values()):
        raise AssertionError("certificate does not cancel every cell")
    if rhs_sum == 0:
        raise AssertionError("certificate does not contradict the right side")


def full_equations(
    groups: tuple[tuple[int, ...], ...],
) -> tuple[tuple[dict[int, int], int], ...]:
    return tuple(({cell: 1 for cell in group}, 1) for group in groups)


def abstract_equations(
    cliques: tuple[str, ...],
) -> tuple[tuple[dict[int, int], int], ...]:
    symbols = sorted(set("".join(cliques)))
    index = {symbol: i for i, symbol in enumerate(symbols)}
    return tuple(({index[symbol]: 1 for symbol in clique}, 1) for clique in cliques)


def palette_anchor_maxima(
    cells: tuple[tuple[tuple[int, int, int, int], int], ...],
    groups: tuple[tuple[int, ...], ...],
) -> tuple[int, int]:
    memberships: list[list[int]] = [[] for _ in cells]
    for group_index, group in enumerate(groups):
        for cell in group:
            memberships[cell].append(group_index)
    maxima = [0, 0]
    for group_index, group in enumerate(groups):
        target = set(group)
        counts: dict[int, int] = defaultdict(int)
        for member in group:
            for incident_group in memberships[member]:
                for outside in groups[incident_group]:
                    if outside not in target:
                        counts[outside] += 1
        kind = 0 if group_index < 126 else 1
        maxima[kind] = max(maxima[kind], max(counts.values(), default=0))
    return maxima[0], maxima[1]


def audit_type(
    name: str,
    systems: tuple[tuple[tuple[int, int, int], ...], ...],
    cliques: tuple[str, ...],
) -> None:
    gadget_rank, gadget_certificate = eliminate(
        abstract_equations(cliques),
        track_certificate=False,
    )
    if gadget_certificate is not None or gadget_rank != 11:
        raise AssertionError(f"{name}: unexpected affine status for 18-cell gadget")

    cells, groups = build_control_from_link(systems_to_link(systems))
    anchor_maxima = palette_anchor_maxima(cells, groups)
    if anchor_maxima != (1, 2):
        raise AssertionError(f"{name}: unexpected palette-anchor maxima")
    equations = full_equations(groups)
    rank, certificate = eliminate(equations, track_certificate=True)
    if certificate is None:
        raise AssertionError(f"{name}: full Bx=1 unexpectedly consistent")
    check_certificate(equations, certificate)
    print(
        f"{name}: gadget rank=11 and consistent; "
        f"full rank before contradiction={rank}; "
        f"certificate support={len(certificate)}; "
        f"anchor maxima={anchor_maxima}"
    )
    if len(cells) != 378 or len(groups) != 630:
        raise AssertionError(f"{name}: wrong full control size")


def main() -> None:
    audit_type("type A", type_a_systems(), TYPE_A_CLIQUES)
    audit_type("type B", type_b_systems(), TYPE_B_CLIQUES)
    print("k=6 characteristic-3 audit: PASS")
    print(
        "scope: the small 18-cell gadgets need nonlinear rainbow information; "
        "the full k=6 fan systems also have linear obstructions"
    )


if __name__ == "__main__":
    main()

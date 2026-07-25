#!/usr/bin/env python3
"""Construct and independently verify a radius-four O_16 ball certificate."""

from __future__ import annotations

import hashlib
from itertools import combinations

from ortools.sat.python import cp_model

from global_latin_audit import construct_golf17


COLORS = tuple(range(17))
FINITE = tuple(range(16))
INFINITY = 16
SQUARES = tuple(range(15))
INDEX_EDGES = tuple(combinations(SQUARES, 2))
FINITE_EDGES = tuple(combinations(FINITE, 2))


def construct_one_n(
    golf: list[list[list[int]]], u: int, v: int
) -> tuple[dict[tuple[int, int], int], list[set[int]]]:
    """Solve the exact N_uv list-edge-colouring problem on K_15."""
    allowed = [
        set(COLORS)
        - {
            golf[i][u][v],
            golf[i][u][INFINITY],
            golf[i][v][INFINITY],
        }
        for i in SQUARES
    ]
    assert all(len(values) == 14 for values in allowed)

    model = cp_model.CpModel()
    variables: dict[tuple[int, int], cp_model.IntVar] = {}
    for i, j in INDEX_EDGES:
        domain = sorted(allowed[i] & allowed[j])
        variables[i, j] = model.NewIntVarFromDomain(
            cp_model.Domain.FromValues(domain), f"n_{u}_{v}_{i}_{j}"
        )
    for i in SQUARES:
        model.AddAllDifferent(
            [variables[min(i, j), max(i, j)] for j in SQUARES if j != i]
        )

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 0
    solver.parameters.max_time_in_seconds = 30
    status = solver.Solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE), (
        (u, v),
        solver.StatusName(status),
    )
    certificate = {edge: solver.Value(variable) for edge, variable in variables.items()}

    # Backend-independent check of this edge colouring.
    for i in SQUARES:
        incident = {
            certificate[min(i, j), max(i, j)] for j in SQUARES if j != i
        }
        assert incident == allowed[i]
    return certificate, allowed


def verify_l_m(golf: list[list[list[int]]]) -> None:
    """Verify conditions 1--3 of radius4_reduction.md directly."""
    finite_set = set(FINITE)
    color_set = set(COLORS)
    for u in FINITE:
        assert {golf[i][u][INFINITY] for i in SQUARES} == finite_set - {u}

    for i in SQUARES:
        l_values = [golf[i][u][INFINITY] for u in FINITE]
        assert set(l_values) == finite_set
        assert all(l_values[u] != u for u in FINITE)
        for u in FINITE:
            incident = {
                golf[i][min(u, v)][max(u, v)]
                for v in FINITE
                if v != u
            }
            assert incident == color_set - {u, l_values[u]}

    for u, v in FINITE_EDGES:
        assert {golf[i][u][v] for i in SQUARES} == color_set - {u, v}


def main() -> None:
    golf = construct_golf17()
    verify_l_m(golf)

    serial = bytearray()
    certificates: dict[tuple[int, int], dict[tuple[int, int], int]] = {}
    for u, v in FINITE_EDGES:
        certificate, _ = construct_one_n(golf, u, v)
        certificates[u, v] = certificate
        serial.extend(certificate[edge] for edge in INDEX_EDGES)

    # Recheck all 12,600 values only from the extracted certificates.
    for u, v in FINITE_EDGES:
        certificate = certificates[u, v]
        for i in SQUARES:
            forbidden = {
                golf[i][u][v],
                golf[i][u][INFINITY],
                golf[i][v][INFINITY],
            }
            assert len(forbidden) == 3
            incident = {
                certificate[min(i, j), max(i, j)] for j in SQUARES if j != i
            }
            assert incident == set(COLORS) - forbidden

    digest = hashlib.sha256(serial).hexdigest()
    print("golf L/M layers: PASS")
    print("N_uv exact edge-colourings: 120/120 OPTIMAL")
    print("independent N verification: PASS (12,600 values)")
    print(f"certificate sha256: {digest}")
    print("radius-four O_16 ball certificate: PASS")


if __name__ == "__main__":
    main()

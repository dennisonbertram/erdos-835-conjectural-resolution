#!/usr/bin/env python3
"""Extend the cyclic G(17) chart through the radius-five O_16 ball.

This is a constructive, independently checked *finite-ball* route to a
17-colouring of O_16.  It deliberately does not identify a radius-five
certificate with a global cover.  The only inputs are the published cyclic
golf array and deterministic CP-SAT list-edge-colourings used to produce
the radius-four N layer.

For each pair ij of index vertices, a sphere-five colour P_ij(uvw) must
satisfy, for every pair uv,

  {P_ij(uvw) : w notin {u,v}}
    = C \ {N_uv(ij), M_i(uv), M_j(uv)}.

Thus, for fixed ij, each colour class is a triangle decomposition of its
allowed graph.  We solve that exact finite CSP and independently recheck
all radius-five closed neighbourhoods from the resulting values.

Run from the repository root:
  python3 -B evidence/global_construction_radius5.py --seconds-per-pair 60
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from itertools import combinations
from pathlib import Path

from ortools.sat.python import cp_model


# These are existing, independently auditable definitions.  Do not import
# their CLI: only the exact construction routines are used here.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from global_latin_audit import construct_golf17  # noqa: E402
from global_latin_radius4_certificate import (  # noqa: E402
    COLORS,
    FINITE,
    FINITE_EDGES,
    INDEX_EDGES,
    SQUARES,
    construct_one_n,
    verify_l_m,
)


TRIPLES = tuple(combinations(FINITE, 3))


def edges_of(triple: tuple[int, int, int]) -> tuple[tuple[int, int], ...]:
    return tuple(combinations(triple, 2))


TRIPLE_EDGES = {triple: edges_of(triple) for triple in TRIPLES}
TRIPLES_ON_EDGE = {
    edge: tuple(triple for triple in TRIPLES if set(edge).issubset(triple))
    for edge in FINITE_EDGES
}


def build_n_layer(golf: list[list[list[int]]]) -> dict[tuple[int, int], dict[tuple[int, int], int]]:
    """Reconstruct the deterministic radius-four N layer."""
    result = {}
    for uv in FINITE_EDGES:
        certificate, _ = construct_one_n(golf, *uv)
        result[uv] = certificate
    return result


def allowed_colours(
    golf: list[list[list[int]]],
    n_layer: dict[tuple[int, int], dict[tuple[int, int], int]],
    ij: tuple[int, int],
    uv: tuple[int, int],
) -> set[int]:
    i, j = ij
    excluded = {
        n_layer[uv][ij],
        golf[i][uv[0]][uv[1]],
        golf[j][uv[0]][uv[1]],
    }
    assert len(excluded) == 3, (ij, uv, excluded)
    return set(COLORS) - excluded


def solve_one_p(
    golf: list[list[list[int]]],
    n_layer: dict[tuple[int, int], dict[tuple[int, int], int]],
    ij: tuple[int, int],
    seconds: float,
) -> dict[tuple[int, int, int], int]:
    """Find all triangle colours for one fixed ij, with no relaxation."""
    allowed = {uv: allowed_colours(golf, n_layer, ij, uv) for uv in FINITE_EDGES}
    model = cp_model.CpModel()
    values: dict[tuple[int, int, int], cp_model.IntVar] = {}
    for triple in TRIPLES:
        domain = set(COLORS)
        for uv in TRIPLE_EDGES[triple]:
            domain &= allowed[uv]
        assert domain, (ij, triple)
        values[triple] = model.NewIntVarFromDomain(
            cp_model.Domain.FromValues(sorted(domain)),
            "p_{}_{}_{}_{}_{}".format(*ij, *triple),
        )
    for uv, triples in TRIPLES_ON_EDGE.items():
        # There are 14 extensions of uv and exactly its 14 allowed colours.
        assert len(triples) == len(allowed[uv]) == 14
        model.AddAllDifferent([values[triple] for triple in triples])

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 0
    solver.parameters.max_time_in_seconds = seconds
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(f"P_{ij}: {solver.StatusName(status)}")
    answer = {triple: solver.Value(var) for triple, var in values.items()}

    # Backend-independent pair and domain checks.
    for uv, triples in TRIPLES_ON_EDGE.items():
        got = {answer[triple] for triple in triples}
        assert got == allowed[uv], (ij, uv, got, allowed[uv])
    return answer


def n_edge_domain(
    golf: list[list[list[int]]], uv: tuple[int, int], ij: tuple[int, int]
) -> set[int]:
    """The necessary list for N_uv(ij); extension is checked afterwards."""
    i, j = ij
    left = set(COLORS) - {
        golf[i][uv[0]][uv[1]], golf[i][uv[0]][16], golf[i][uv[1]][16]
    }
    right = set(COLORS) - {
        golf[j][uv[0]][uv[1]], golf[j][uv[0]][16], golf[j][uv[1]][16]
    }
    return left & right


def construct_one_n_with_value(
    golf: list[list[list[int]]], uv: tuple[int, int], ij: tuple[int, int], value: int
) -> dict[tuple[int, int], int]:
    """Independently complete N_uv after fixing its ij entry."""
    allowed = [
        set(COLORS) - {golf[i][uv[0]][uv[1]], golf[i][uv[0]][16], golf[i][uv[1]][16]}
        for i in SQUARES
    ]
    model = cp_model.CpModel()
    variables = {}
    for edge in INDEX_EDGES:
        a, b = edge
        variables[edge] = model.NewIntVarFromDomain(
            cp_model.Domain.FromValues(sorted(allowed[a] & allowed[b])),
            f"fixed_n_{uv}_{edge}",
        )
    model.Add(variables[ij] == value)
    for i in SQUARES:
        model.AddAllDifferent([variables[min(i, j), max(i, j)] for j in SQUARES if j != i])
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 0
    solver.parameters.max_time_in_seconds = 30
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(f"N_{uv}({ij})={value}: {solver.StatusName(status)}")
    answer = {edge: solver.Value(var) for edge, var in variables.items()}
    for i in SQUARES:
        assert {answer[min(i, j), max(i, j)] for j in SQUARES if j != i} == allowed[i]
    return answer


def solve_adaptive_one_p(
    golf: list[list[list[int]]], ij: tuple[int, int], seconds: float, workers: int
) -> tuple[
    dict[tuple[int, int], dict[tuple[int, int], int]],
    dict[tuple[int, int, int], int],
]:
    """Jointly choose the N(ij) edge trace and one exact P_ij layer.

    This is a genuine local-to-global stage: all 120 values N_uv(ij) are
    selected with the 560 triangle values, then each selected value is
    completed to a full independently checked N_uv list-edge-colouring.
    Other ij entries of the N layer remain unfixed, so this is a ray, not
    a radius-five ball certificate.
    """
    model = cp_model.CpModel()
    p = {}
    for triple in TRIPLES:
        # M_i and M_j are fixed exclusions on each of the three edge stars.
        domain = set(COLORS)
        for uv in TRIPLE_EDGES[triple]:
            i, j = ij
            domain -= {golf[i][uv[0]][uv[1]], golf[j][uv[0]][uv[1]]}
        p[triple] = model.NewIntVarFromDomain(
            cp_model.Domain.FromValues(sorted(domain)), f"adaptive_p_{triple}"
        )
    for uv, triples in TRIPLES_ON_EDGE.items():
        model.AddAllDifferent([p[triple] for triple in triples])

        # The omitted value is forced to be N_uv(ij).  Eliminate that
        # variable rather than branching over 120 independent q choices:
        # every colour which cannot be N_uv(ij) must occur on this edge's
        # fourteen triples.  Since the P values are all distinct and avoid
        # the two fixed M values, this is equivalent to selecting an
        # admissible omitted colour.
        i, j = ij
        m_values = {golf[i][uv[0]][uv[1]], golf[j][uv[0]][uv[1]]}
        p_universe = set(COLORS) - m_values
        possible_q = n_edge_domain(golf, uv, ij)
        assert possible_q <= p_universe
        for forbidden_q in p_universe - possible_q:
            occurrences = []
            for triple in triples:
                indicator = model.NewBoolVar(f"uses_{uv}_{forbidden_q}_{triple}")
                model.Add(p[triple] == forbidden_q).OnlyEnforceIf(indicator)
                model.Add(p[triple] != forbidden_q).OnlyEnforceIf(indicator.Not())
                occurrences.append(indicator)
            model.AddBoolOr(occurrences)

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.random_seed = 0
    solver.parameters.max_time_in_seconds = seconds
    print(f"adaptive P_{ij}: 560 triples, 120 edge constraints; solving", flush=True)
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(
            f"adaptive P_{ij}: {solver.StatusName(status)}; "
            f"conflicts={solver.NumConflicts()} branches={solver.NumBranches()}"
        )
    p_answer = {triple: solver.Value(var) for triple, var in p.items()}
    q_answer = {}
    for uv, triples in TRIPLES_ON_EDGE.items():
        i, j = ij
        missing = (set(COLORS) - {
            golf[i][uv[0]][uv[1]], golf[j][uv[0]][uv[1]]
        }) - {p_answer[triple] for triple in triples}
        assert len(missing) == 1, (uv, missing)
        q_answer[uv] = missing.pop()
        assert q_answer[uv] in n_edge_domain(golf, uv, ij)
    print(
        f"adaptive P_{ij}: {solver.StatusName(status)} "
        f"conflicts={solver.NumConflicts()} branches={solver.NumBranches()}", flush=True
    )
    n_answer = {
        uv: construct_one_n_with_value(golf, uv, ij, q_answer[uv])
        for uv in FINITE_EDGES
    }
    for uv, triples in TRIPLES_ON_EDGE.items():
        i, j = ij
        got = {p_answer[triple] for triple in triples}
        expected = set(COLORS) - {
            n_answer[uv][ij], golf[i][uv[0]][uv[1]], golf[j][uv[0]][uv[1]]
        }
        assert got == expected, (uv, got, expected)
    return n_answer, p_answer


def verify_radius_five(
    golf: list[list[list[int]]],
    n_layer: dict[tuple[int, int], dict[tuple[int, int], int]],
    p_layer: dict[tuple[int, int], dict[tuple[int, int, int], int]],
) -> None:
    """Check every sphere-four centre's complete closed-neighbourhood list."""
    for ij in INDEX_EDGES:
        i, j = ij
        for uv in FINITE_EDGES:
            colors = {
                n_layer[uv][ij],
                golf[i][uv[0]][uv[1]],
                golf[j][uv[0]][uv[1]],
            }
            colors.update(
                p_layer[ij][tuple(sorted((uv[0], uv[1], w)))]
                for w in FINITE
                if w not in uv
            )
            assert colors == set(COLORS), (ij, uv, colors)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds-per-pair", type=float, default=60.0)
    parser.add_argument("--limit-pairs", type=int, default=None,
                        help="debug only; cannot certify the whole radius-five ball")
    parser.add_argument("--adaptive-one-pair", action="store_true",
                        help="jointly construct one P_ij ray with its N_uv(ij) trace")
    parser.add_argument("--workers", type=int, default=1,
                        help="CP-SAT workers for the adaptive ray search")
    args = parser.parse_args()
    if args.seconds_per_pair <= 0:
        parser.error("--seconds-per-pair must be positive")
    if args.workers <= 0:
        parser.error("--workers must be positive")

    if args.adaptive_one_pair:
        ij = INDEX_EDGES[0]
        _n_layer, _p_layer = solve_adaptive_one_p(golf := construct_golf17(), ij,
                                                   args.seconds_per_pair, args.workers)
        print(f"adaptive N/P ray for ij={ij}: PASS")
        print("independent N completion and radius-five star checks: PASS")
        print("scope: one radius-five ray only; not a radius-five ball or global cover")
        return

    golf = construct_golf17()
    verify_l_m(golf)
    n_layer = build_n_layer(golf)
    pairs = INDEX_EDGES[:args.limit_pairs]
    p_layer = {}
    for number, ij in enumerate(pairs, 1):
        p_layer[ij] = solve_one_p(golf, n_layer, ij, args.seconds_per_pair)
        print(f"P layer {number}/{len(pairs)} for ij={ij}: PASS", flush=True)

    if len(pairs) != len(INDEX_EDGES):
        print("partial P layer only; no radius-five certificate")
        return
    verify_radius_five(golf, n_layer, p_layer)
    serial = bytearray(
        p_layer[ij][triple] for ij in INDEX_EDGES for triple in TRIPLES
    )
    print("cyclic golf L/M layer: PASS")
    print("radius-four N layer: PASS")
    print("all 105 exact triangle-decomposition CSPs: PASS")
    print("independent radius-five neighbourhood verification: PASS")
    print(f"P-layer sha256: {hashlib.sha256(serial).hexdigest()}")
    print("scope: radius-five O_16 ball only; not a global O_16 -> K_17 cover")


if __name__ == "__main__":
    main()

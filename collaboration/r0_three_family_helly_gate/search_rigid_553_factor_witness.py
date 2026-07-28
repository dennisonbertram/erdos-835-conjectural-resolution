#!/usr/bin/env python3
"""Search the exact full-row model for the rigid 5+5+3 factor witness.

The narrowed Tutte--Lovasz audit shows that the earliest possible negative
factor inequality has a partition V=A dotcup B dotcup C with sizes 5,5,3:

* all three selected omitted triples lie in A;
* every B vertex has deleted degree five and no deleted edge to A;
* D[C] is a triangle; and
* the three B-to-C deleted degrees are (3,1,1) or (3,3,1).

Those two degree profiles make all three singleton components of G[C]
counted and give Delta(A,B)=-2.  Hence any SAT model emitted here is already
a counterexample to full-row cut sufficiency; no matching-triple CEGIS
clauses are needed.

An UNSAT result is search output until the emitted DIMACS file is checked by
an external proof-producing solver and independently audited.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from pysat.solvers import Cadical195

import freeze_full_row_cut_sufficiency as freeze
import search_counterexamples as search


def deleted(cnf: search.Cnf, edge_index: int) -> int:
    return cnf.variable(("deleted_edge", edge_index))


def exact_deleted_degree(
    cnf: search.Cnf,
    tag: tuple[object, ...],
    vertex: int,
    neighbours: tuple[int, ...],
    degree: int,
) -> None:
    literals = [
        deleted(cnf, search.EDGE_INDEX[tuple(sorted((vertex, neighbour)))])
        for neighbour in neighbours
    ]
    cnf.cardinality(tag, literals, lower=degree, upper=degree)


def install_capacity_cuts(
    cnf: search.Cnf,
    omitted_triples: tuple[tuple[int, ...], ...],
) -> int:
    count = 0
    for vertices, internal_edges, required in search.cut_requirements(
        omitted_triples
    ):
        maximum_deleted = min(
            len(internal_edges),
            5 * len(vertices) // 2,
            sum(search.PREFIX_SIZES),
        )
        if required <= len(internal_edges) - maximum_deleted:
            continue
        cnf.cardinality(
            ("cut_feasible", vertices),
            [-deleted(cnf, edge_index) for edge_index in internal_edges],
            lower=required,
        )
        count += 1
    return count


def solve_case(
    orbit_index: int,
    signature: tuple[int, ...],
    omitted_triples: tuple[tuple[int, ...], ...],
    bc_degrees: tuple[int, int, int],
    cnf_dir: Path,
    *,
    enforce_capacity_cuts: bool,
    full_rows: bool,
    fixed_prefix_sizes: bool,
) -> dict[str, object]:
    start = time.monotonic()
    cnf, _families = search.build_instance(
        omitted_triples,
        full_rows=full_rows,
        matching_constraints=False,
        fixed_prefix_sizes=fixed_prefix_sizes,
        vertex_symmetry=False,
    )

    union = frozenset().union(
        *(frozenset(triple) for triple in omitted_triples)
    )
    if len(union) > 5:
        raise ValueError("the rigid witness requires all selected rows in A")
    filler = tuple(vertex for vertex in search.VERTICES if vertex not in union)
    a = tuple(sorted((*union, *filler[: 5 - len(union)])))
    outside = tuple(vertex for vertex in search.VERTICES if vertex not in a)
    b = outside[:5]
    c = outside[5:]
    if (len(a), len(b), len(c)) != (5, 5, 3):
        raise AssertionError("bad 5+5+3 partition")

    # No deleted A--B edge, so e_G(v,A)=5 for every v in B.
    for left in a:
        for right in b:
            cnf.add(
                -deleted(
                    cnf,
                    search.EDGE_INDEX[tuple(sorted((left, right)))],
                )
            )

    # G[C] is edgeless.
    for left_index, left in enumerate(c):
        for right in c[left_index + 1 :]:
            cnf.add(
                deleted(
                    cnf,
                    search.EDGE_INDEX[tuple(sorted((left, right)))],
                )
            )

    # Equality p(v)=-1 forces deleted degree five on B.
    for vertex in b:
        exact_deleted_degree(
            cnf,
            ("rigid_553_b_degree", vertex),
            vertex,
            tuple(neighbour for neighbour in search.VERTICES if neighbour != vertex),
            5,
        )

    # Up to permuting C, the only counted-singleton profiles are (3,1,1)
    # and (3,3,1), corresponding to e_D(B,C)=5 and 7.
    for vertex, degree in zip(c, bc_degrees):
        exact_deleted_degree(
            cnf,
            ("rigid_553_bc_degree", vertex),
            vertex,
            b,
            degree,
        )

    capacity_cuts = (
        install_capacity_cuts(cnf, omitted_triples)
        if enforce_capacity_cuts
        else 0
    )
    initial_clauses = len(cnf.clauses)
    solver = Cadical195(bootstrap_with=cnf.clauses)
    try:
        satisfiable = solver.solve()
        if satisfiable:
            model = frozenset(
                literal for literal in solver.get_model() if literal > 0
            )
            prefix = [
                [
                    search.EDGES[edge_index]
                    for edge_index in range(len(search.EDGES))
                    if cnf.variable(("colour_edge", colour, edge_index))
                    in model
                ]
                for colour in range(len(search.PREFIX_SIZES))
            ]
            result: dict[str, object] = {
                "status": "counterexample",
                "prefix": prefix,
            }
            if full_rows:
                result["remaining_complements"] = [
                    [
                        vertex
                        for vertex in search.VERTICES
                        if cnf.variable(("remaining_row", row, vertex)) in model
                    ]
                    for row in range(11)
                ]
        else:
            cnf_path = (
                cnf_dir
                / f"orbit_{orbit_index}_bc_{''.join(map(str, bc_degrees))}.cnf"
            )
            result = {
                "status": "unsat",
                "cnf_path": str(cnf_path),
                "cnf_sha256": search.write_dimacs(cnf_path, cnf),
            }
    finally:
        solver.delete()

    result.update(
        {
            "orbit": orbit_index,
            "signature": signature,
            "omitted_triples": omitted_triples,
            "partition": {"A": a, "B": b, "C": c},
            "bc_degrees": bc_degrees,
            "capacity_cuts": capacity_cuts,
            "variables": cnf.top,
            "clauses": initial_clauses,
            "elapsed_seconds": round(time.monotonic() - start, 3),
            "proof_claimed": False,
            "full_rows": full_rows,
            "fixed_prefix_sizes": fixed_prefix_sizes,
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", default="all")
    parser.add_argument("--cnf-dir", type=Path, required=True)
    parser.add_argument("--jsonl", type=Path)
    parser.add_argument(
        "--skip-capacity-cuts",
        action="store_true",
        help="diagnostic only: test whether the row/prefix ledger already suffices",
    )
    parser.add_argument(
        "--prefix-only",
        action="store_true",
        help="diagnostic only: omit the exact eleven-row completion",
    )
    parser.add_argument(
        "--relax-prefix-sizes",
        action="store_true",
        help="diagnostic only: allow six arbitrary matchings totalling 27 edges",
    )
    args = parser.parse_args()

    all_orbits = freeze.support_orbits_fast()
    eligible = tuple(
        index
        for index, (signature, _representative) in enumerate(all_orbits)
        if sum(signature) <= 5
    )
    requested = (
        eligible
        if args.orbits == "all"
        else search.parse_orbits(args.orbits, len(all_orbits))
    )
    if any(index not in eligible for index in requested):
        parser.error(f"eligible orbit indices are {eligible}")

    output = args.jsonl.open("a", encoding="utf-8") if args.jsonl else None
    try:
        for orbit_index in requested:
            signature, representative = all_orbits[orbit_index]
            for bc_degrees in ((3, 1, 1), (3, 3, 1)):
                result = solve_case(
                    orbit_index,
                    signature,
                    representative,
                    bc_degrees,
                    args.cnf_dir,
                    enforce_capacity_cuts=not args.skip_capacity_cuts,
                    full_rows=not args.prefix_only,
                    fixed_prefix_sizes=not args.relax_prefix_sizes,
                )
                line = json.dumps(result, sort_keys=True)
                print(line, flush=True)
                if output:
                    output.write(line + "\n")
                    output.flush()
                if result["status"] == "counterexample":
                    return
    finally:
        if output:
            output.close()


if __name__ == "__main__":
    main()

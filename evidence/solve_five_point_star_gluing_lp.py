#!/usr/bin/env python3
"""Solve the free four/five-point star-gluing relaxation for ER #835.

The one-edge four-point coupling is a variable here.  This is essential:
the deterministic max-flow used by the earlier witness is only one point
of a large transportation polytope, and fixing it cannot yield a valid
obstruction.

Stages:

``slot``
    Endpoint triple marginals, one-edge local-bijection equations, all
    admissible four- and five-position reorder symmetries (including rare
    alternate-edge/star geometries), and a common ordered-two-neighbour lift
    with c(w1) != c(w2).

``drop-y-one``
    Additionally require the marginal on (x,w1,z,w2) to equal the same free
    one-edge four-point tensor.  With the default full-reorder quotient,
    x/y and w1/w2 symmetry make the other three re-based projections exact
    symmetry images of this one.

The later stages explicitly add those symmetry-image rows as a diagnostic.
They are useful with ``--no-full-reorders`` but redundant in the default
proof model.

The solver is numerical (HiGHS).  A feasible numerical point is not an
exact certificate; an infeasible result must be rationally certified
before it can be used as mathematics.
"""

from __future__ import annotations

import argparse
import itertools
import math
from array import array
from collections import defaultdict
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

import five_point_star_gluing_probe as probe
import verify_four_point_terwilliger_exact_witness as base


class SparseRows:
    def __init__(self, exact_lp_path=None):
        self.indices = array("i")
        self.data = array("d")
        self.indptr = array("q", [0])
        self.rhs = array("d")
        self.labels = []
        self.exact_lp = (
            open(exact_lp_path, "w", encoding="ascii")
            if exact_lp_path
            else None
        )
        if self.exact_lp:
            self.exact_lp.write("Minimize\n obj: 0\nSubject To\n")

    def add(self, terms, rhs, label):
        combined = defaultdict(Fraction)
        for index, coefficient in terms:
            if coefficient:
                combined[index] += Fraction(coefficient)
        exact_terms = []
        for index in sorted(combined):
            coefficient = combined[index]
            if coefficient:
                self.indices.append(index)
                self.data.append(float(coefficient))
                exact_terms.append((index, coefficient))
        self.indptr.append(len(self.indices))
        self.rhs.append(float(rhs))
        self.labels.append(label)
        if self.exact_lp:
            self.exact_lp.write(f" c{len(self.rhs) - 1}:")
            for index, coefficient in exact_terms:
                sign = "+" if coefficient > 0 else "-"
                magnitude = abs(coefficient)
                self.exact_lp.write(
                    f" {sign} {magnitude} x{index}"
                )
            self.exact_lp.write(f" = {Fraction(rhs)}\n")

    def finish_exact_lp(self):
        if self.exact_lp:
            self.exact_lp.write("End\n")
            self.exact_lp.close()
            self.exact_lp = None

    def matrix(self, variable_count):
        return csr_matrix(
            (
                np.frombuffer(self.data, dtype=np.float64),
                np.frombuffer(self.indices, dtype=np.int32),
                np.frombuffer(self.indptr, dtype=np.int64),
            ),
            shape=(len(self.rhs), variable_count),
        )


def relations_for_cells(cells, length):
    return tuple(
        tuple(
            probe.relation_from_cells(cells, left, right)
            for right in range(length)
        )
        for left in range(length)
    )


def transform_four_key(
    key, permutation, four_records, orbit_index
):
    cells = four_records[key]
    transformed = defaultdict(int)
    for bits, count in cells.items():
        transformed[tuple(bits[index] for index in permutation)] += count
    g = probe.triple_orbit_from_cells(
        transformed, (0, 1, 2), orbit_index
    )
    h = probe.triple_orbit_from_cells(
        transformed, (0, 1, 3), orbit_index
    )
    return (g, h)


def canonical_source_colors(source_pattern):
    return probe.TRIPLE_PARTITIONS[source_pattern]


def four_color_options(partition, source_pattern):
    source = canonical_source_colors(source_pattern)
    if probe.canonical_partition(partition[:3]) != source:
        return ()
    existing = set(source)
    w_class = partition[3]
    if w_class in existing:
        return (w_class,)
    assert w_class == max(existing) + 1
    return tuple(range(len(existing), base.P))


def prepare():
    orbits = base.geometric_orbits(base.R)
    orbit_index = {
        orbit[:4]: index for index, orbit in enumerate(orbits)
    }
    relation = base.relation_data(base.R)
    transitions = base.geometry_neighbor_transitions(base.R, orbits)
    t_by_key, _values = base.load_certificate(orbits)
    q, _alpha = base.build_q(orbits, relation, t_by_key)
    categories = [
        probe.category_data(orbit, orbit_index) for orbit in orbits
    ]
    four_records = probe.enumerate_four_orbits(
        orbits, orbit_index, categories
    )
    five_records = probe.enumerate_five_orbits(
        orbits, orbit_index, categories
    )
    return (
        orbits,
        orbit_index,
        transitions,
        q,
        categories,
        four_records,
        five_records,
    )


def build_variables(four_records, five_records):
    p4s = probe.partitions(4)
    p5s = probe.partitions(5)
    variable_count = 0

    four_vars = {}
    four_partitions = {}
    for key, cells in sorted(four_records.items()):
        relations = relations_for_cells(cells, 4)
        allowed = [
            partition
            for partition in p4s
            if probe.partition_respects_geometry(partition, relations)
        ]
        four_partitions[key] = allowed
        for partition in allowed:
            four_vars[(key, partition)] = variable_count
            variable_count += 1

    for record in five_records:
        allowed = [
            partition
            for partition in p5s
            if probe.partition_respects_geometry(
                partition, record["relations"]
            )
        ]
        record["allowed_partitions"] = allowed
        record["variables"] = {}
        for partition in allowed:
            record["variables"][partition] = variable_count
            variable_count += 1

    return variable_count, four_vars, four_partitions


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = bytearray(size)

    def find(self, item):
        parent = self.parent
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(self, left, right):
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return
        rank = self.rank
        if rank[left] < rank[right]:
            left, right = right, left
        self.parent[right] = left
        if rank[left] == rank[right]:
            rank[left] += 1


def cells_signature(cells):
    return tuple(
        sorted((tuple(bits), count) for bits, count in cells.items() if count)
    )


def permute_cells(cells, permutation):
    transformed = defaultdict(int)
    for bits, count in cells.items():
        transformed[
            tuple(bits[index] for index in permutation)
        ] += count
    return dict(transformed)


def collapse_full_reorder_symmetry(
    variable_count,
    four_records,
    four_vars,
    five_records,
):
    """Identify variables under every position reorder preserving the domain.

    Besides the generic x/y and neighbor swaps, rare geometric tuples contain
    extra Odd-graph edges or an alternate two-neighbor star.  A genuine
    coloring has identical orbit probabilities under those conditional
    reorders too.
    """
    union_find = UnionFind(variable_count)

    four_lookup = {
        cells_signature(cells): key
        for key, cells in four_records.items()
    }
    assert len(four_lookup) == len(four_records)
    four_variables_by_key = defaultdict(list)
    for (key, partition), variable in four_vars.items():
        four_variables_by_key[key].append((partition, variable))
    four_permutation_links = 0
    for key, cells in four_records.items():
        relations = relations_for_cells(cells, 4)
        for permutation in itertools.permutations(range(4)):
            if relations[permutation[2]][permutation[3]] != 0:
                continue
            target_key = four_lookup[
                cells_signature(permute_cells(cells, permutation))
            ]
            for partition, source_variable in four_variables_by_key[key]:
                target_partition = probe.canonical_partition(
                    tuple(partition[index] for index in permutation)
                )
                target_variable = four_vars[(target_key, target_partition)]
                union_find.union(source_variable, target_variable)
                four_permutation_links += 1

    five_lookup = {
        cells_signature(record["cells"]): record
        for record in five_records
    }
    assert len(five_lookup) == len(five_records)
    five_permutation_links = 0
    for record in five_records:
        relations = record["relations"]
        for permutation in itertools.permutations(range(5)):
            if (
                relations[permutation[2]][permutation[3]] != 0
                or relations[permutation[2]][permutation[4]] != 0
                or relations[permutation[3]][permutation[4]]
                != base.R - 1
            ):
                continue
            target_record = five_lookup[
                cells_signature(
                    permute_cells(record["cells"], permutation)
                )
            ]
            for partition, source_variable in record["variables"].items():
                target_partition = probe.canonical_partition(
                    tuple(partition[index] for index in permutation)
                )
                target_variable = target_record["variables"][
                    target_partition
                ]
                union_find.union(source_variable, target_variable)
                five_permutation_links += 1

    roots = sorted({union_find.find(index) for index in range(variable_count)})
    compact = {root: index for index, root in enumerate(roots)}

    for key in list(four_vars):
        four_vars[key] = compact[union_find.find(four_vars[key])]
    for record in five_records:
        for partition in list(record["variables"]):
            old = record["variables"][partition]
            record["variables"][partition] = compact[union_find.find(old)]

    return len(roots), {
        "four_permutation_links": four_permutation_links,
        "five_permutation_links": five_permutation_links,
        "variables_before_reorder_collapse": variable_count,
        "variables_after_reorder_collapse": len(roots),
    }


def add_four_endpoint_rows(
    rows, four_records, four_partitions, four_vars, q
):
    for key in sorted(four_records):
        g, h = key
        for pattern, triple_partition in probe.TRIPLE_PARTITIONS.items():
            source_terms = [
                (four_vars[(key, partition)], 1)
                for partition in four_partitions[key]
                if probe.canonical_partition(partition[:3])
                == triple_partition
            ]
            target_terms = [
                (four_vars[(key, partition)], 1)
                for partition in four_partitions[key]
                if probe.canonical_partition(
                    (partition[0], partition[1], partition[3])
                )
                == triple_partition
            ]
            rows.add(source_terms, q[g][pattern], ("four-source", key, pattern))
            rows.add(target_terms, q[h][pattern], ("four-target", key, pattern))


def add_four_symmetry_rows(
    rows,
    four_records,
    four_partitions,
    four_vars,
    orbit_index,
):
    # Swap the two non-edge vertices; reverse the distinguished edge.
    for permutation, name in (
        ((1, 0, 2, 3), "swap-nonedge"),
        ((0, 1, 3, 2), "reverse-edge"),
    ):
        for key in sorted(four_records):
            target_key = transform_four_key(
                key, permutation, four_records, orbit_index
            )
            if key > target_key:
                continue
            for partition in four_partitions[key]:
                target_partition = probe.canonical_partition(
                    tuple(partition[index] for index in permutation)
                )
                target_variable = four_vars.get(
                    (target_key, target_partition)
                )
                assert target_variable is not None
                source_variable = four_vars[(key, partition)]
                if source_variable == target_variable:
                    continue
                rows.add(
                    ((source_variable, 1), (target_variable, -1)),
                    0,
                    (name, key, partition),
                )


def add_local_bijection_rows(
    rows,
    orbits,
    transitions,
    q,
    four_partitions,
    four_vars,
):
    for g in range(len(orbits)):
        for source_pattern, source_colors in (
            probe.TRIPLE_PARTITIONS.items()
        ):
            total = q[g][source_pattern]
            if not total:
                continue
            z_color = source_colors[2]
            representatives = [
                color for color in sorted(set(source_colors))
                if color != z_color
            ]
            if len(set(source_colors)) < base.P:
                representatives.append(len(set(source_colors)))
            for color in representatives:
                terms = []
                for h, multiplicity in transitions[g].items():
                    key = (g, h)
                    for partition in four_partitions[key]:
                        options = four_color_options(
                            partition, source_pattern
                        )
                        if color in options:
                            terms.append(
                                (
                                    four_vars[(key, partition)],
                                    Fraction(multiplicity, len(options)),
                                )
                            )
                rows.add(
                    terms,
                    total,
                    ("local-bijection", g, source_pattern, color),
                )


def add_slot_marginal_rows(
    rows,
    five_records,
    categories,
    four_partitions,
    four_vars,
):
    by_first = defaultdict(list)
    by_second = defaultdict(list)
    for record in five_records:
        by_first[(record["g"], record["c"])].append(record)
        by_second[(record["g"], record["d"])].append(record)

    for (g, c), records in sorted(by_first.items()):
        h = records[0]["h1"]
        key = (g, h)
        for p4 in four_partitions[key]:
            terms = [(four_vars[(key, p4)], -15)]
            for record in records:
                weight = (
                    categories[g][record["d"]][0]
                    - int(c == record["d"])
                )
                assert weight > 0
                for p5, variable in record["variables"].items():
                    if probe.canonical_partition(p5[:4]) == p4:
                        terms.append((variable, weight))
            rows.add(terms, 0, ("drop-w2", g, c, p4))

    for (g, d), records in sorted(by_second.items()):
        h = records[0]["h2"]
        key = (g, h)
        for p4 in four_partitions[key]:
            terms = [(four_vars[(key, p4)], -15)]
            for record in records:
                weight = (
                    categories[g][record["c"]][0]
                    - int(d == record["c"])
                )
                assert weight > 0
                for p5, variable in record["variables"].items():
                    marginal = probe.canonical_partition(
                        (p5[0], p5[1], p5[2], p5[4])
                    )
                    if marginal == p4:
                        terms.append((variable, weight))
            rows.add(terms, 0, ("drop-w1", g, d, p4))


def projection_key(record, positions, orbit_index):
    cells = record["cells"]
    g = probe.triple_orbit_from_cells(
        cells, positions[:3], orbit_index
    )
    h = probe.triple_orbit_from_cells(
        cells, (positions[0], positions[1], positions[3]), orbit_index
    )
    return (g, h)


def add_rebased_rows(
    rows,
    name,
    positions,
    five_records,
    orbits,
    transitions,
    orbit_index,
    four_partitions,
    four_vars,
    max_keys=None,
    integer_scale=True,
):
    grouped = defaultdict(list)
    for record in five_records:
        grouped[projection_key(record, positions, orbit_index)].append(record)

    vertex_count = base.comb(2 * base.R + 1, base.R)
    selected_items = sorted(grouped.items())
    if max_keys is not None:
        selected_items = selected_items[:max_keys]
    for key, records in selected_items:
        total_size = sum(record["size"] for record in records)
        expected = (
            vertex_count
            * orbits[key[0]][4]
            * transitions[key[0]][key[1]]
        )
        assert total_size == expected, (name, key, total_size, expected)
        row_divisor = total_size
        for record in records:
            row_divisor = math.gcd(row_divisor, record["size"])
        for p4 in four_partitions[key]:
            if integer_scale:
                terms = [
                    (
                        four_vars[(key, p4)],
                        -(total_size // row_divisor),
                    )
                ]
            else:
                terms = [(four_vars[(key, p4)], -1)]
            for record in records:
                weight = (
                    record["size"] // row_divisor
                    if integer_scale
                    else Fraction(record["size"], total_size)
                )
                for p5, variable in record["variables"].items():
                    marginal = probe.canonical_partition(
                        tuple(p5[position] for position in positions)
                    )
                    if marginal == p4:
                        terms.append((variable, weight))
            rows.add(terms, 0, (name, key, p4))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stage",
        choices=("slot", "drop-y-one", "drop-y", "drop-x-one", "drop-x"),
        default="slot",
    )
    parser.add_argument("--time-limit", type=float, default=600.0)
    parser.add_argument("--disp", action="store_true")
    parser.add_argument("--rebase-keys", type=int)
    parser.add_argument(
        "--method",
        choices=("highs", "highs-ds", "highs-ipm"),
        default="highs",
    )
    parser.add_argument("--no-presolve", action="store_true")
    parser.add_argument("--no-crossover", action="store_true")
    parser.add_argument("--no-full-reorders", action="store_true")
    parser.add_argument("--normalized-rebase-rows", action="store_true")
    parser.add_argument(
        "--ipm-optimality-tolerance",
        type=float,
        default=1e-8,
    )
    parser.add_argument("--save-solution")
    parser.add_argument("--write-exact-lp")
    parser.add_argument("--no-solve", action="store_true")
    args = parser.parse_args()

    (
        orbits,
        orbit_index,
        transitions,
        q,
        categories,
        four_records,
        five_records,
    ) = prepare()
    (
        variable_count,
        four_vars,
        four_partitions,
    ) = build_variables(four_records, five_records)
    reorder_stats = None
    if not args.no_full_reorders:
        variable_count, reorder_stats = collapse_full_reorder_symmetry(
            variable_count,
            four_records,
            four_vars,
            five_records,
        )

    rows = SparseRows(args.write_exact_lp)
    add_four_endpoint_rows(
        rows, four_records, four_partitions, four_vars, q
    )
    add_four_symmetry_rows(
        rows,
        four_records,
        four_partitions,
        four_vars,
        orbit_index,
    )
    add_local_bijection_rows(
        rows,
        orbits,
        transitions,
        q,
        four_partitions,
        four_vars,
    )
    add_slot_marginal_rows(
        rows,
        five_records,
        categories,
        four_partitions,
        four_vars,
    )

    if args.stage in (
        "drop-y-one",
        "drop-y",
        "drop-x-one",
        "drop-x",
    ):
        add_rebased_rows(
            rows,
            "drop-y-w2",
            (0, 3, 2, 4),
            five_records,
            orbits,
            transitions,
            orbit_index,
            four_partitions,
            four_vars,
            args.rebase_keys,
            integer_scale=not args.normalized_rebase_rows,
        )
        if args.stage in ("drop-y", "drop-x-one", "drop-x"):
            add_rebased_rows(
                rows,
                "drop-y-w1",
                (0, 4, 2, 3),
                five_records,
                orbits,
                transitions,
                orbit_index,
                four_partitions,
                four_vars,
                args.rebase_keys,
                integer_scale=not args.normalized_rebase_rows,
            )
    if args.stage in ("drop-x-one", "drop-x"):
        add_rebased_rows(
            rows,
            "drop-x-w2",
            (1, 3, 2, 4),
            five_records,
            orbits,
            transitions,
            orbit_index,
            four_partitions,
            four_vars,
            args.rebase_keys,
            integer_scale=not args.normalized_rebase_rows,
        )
        if args.stage == "drop-x":
            add_rebased_rows(
                rows,
                "drop-x-w1",
                (1, 4, 2, 3),
                five_records,
                orbits,
                transitions,
                orbit_index,
                four_partitions,
                four_vars,
                args.rebase_keys,
                integer_scale=not args.normalized_rebase_rows,
            )

    rows.finish_exact_lp()
    matrix = rows.matrix(variable_count)
    print(
        {
            "stage": args.stage,
            "variables": variable_count,
            "constraints": matrix.shape[0],
            "nonzeros": matrix.nnz,
            "reorder_symmetry": reorder_stats,
        },
        flush=True,
    )
    if args.no_solve:
        return
    result = linprog(
        np.zeros(variable_count),
        A_eq=matrix,
        b_eq=np.frombuffer(rows.rhs, dtype=np.float64),
        bounds=(0, None),
        method=args.method,
        options={
            "time_limit": args.time_limit,
            "presolve": not args.no_presolve,
            "run_crossover": not args.no_crossover,
            "ipm_optimality_tolerance": args.ipm_optimality_tolerance,
            "disp": args.disp,
        },
    )
    if result.x is not None and args.save_solution:
        np.savez_compressed(
            args.save_solution,
            x=result.x,
            rhs=np.frombuffer(rows.rhs, dtype=np.float64),
        )
    recomputed_residual = (
        matrix @ result.x - np.frombuffer(rows.rhs, dtype=np.float64)
        if result.x is not None
        else None
    )
    print(
        {
            "status": result.status,
            "success": result.success,
            "message": result.message,
            "equality_residual_max": (
                float(np.max(np.abs(result.eqlin.residual)))
                if result.x is not None and len(result.eqlin.residual)
                else None
            ),
            "minimum_variable": (
                float(np.min(result.x)) if result.x is not None else None
            ),
            "recomputed_equality_residual_max": (
                float(np.max(np.abs(recomputed_residual)))
                if recomputed_residual is not None
                and len(recomputed_residual)
                else None
            ),
        },
        flush=True,
    )


if __name__ == "__main__":
    main()

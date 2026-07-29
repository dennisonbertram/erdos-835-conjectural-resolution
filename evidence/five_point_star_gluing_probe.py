#!/usr/bin/env python3
"""Probe the two-neighbour five-point lift of the exact four-point witness.

This is an exploratory exact/numerical checker.  It reconstructs the
one-edge four-point coupling from
``verify_four_point_terwilliger_exact_witness.py``, enumerates the exact
geometric five-point orbits

    (x, y, z, w1, w2),  w1,w2 in N(z), w1 != w2,

and tests successively stronger gluing conditions.
"""

from __future__ import annotations

import math
from collections import defaultdict, deque
from fractions import Fraction

import verify_four_point_terwilliger_exact_witness as base


def canonical_partition(labels):
    """Canonical restricted-growth tuple for an equality pattern."""
    rename = {}
    answer = []
    for label in labels:
        if label not in rename:
            rename[label] = len(rename)
        answer.append(rename[label])
    return tuple(answer)


def partitions(length):
    answer = []

    def visit(prefix):
        if len(prefix) == length:
            answer.append(tuple(prefix))
            return
        for value in range(max(prefix, default=-1) + 2):
            prefix.append(value)
            visit(prefix)
            prefix.pop()

    visit([])
    return answer


TRIPLE_PARTITIONS = {
    base.AAA: (0, 0, 0),
    base.AAB: (0, 0, 1),
    base.ABA: (0, 1, 0),
    base.ABB: (0, 1, 1),
    base.ABC: (0, 1, 2),
}
PARTITION_TO_TRIPLE = {
    value: key for key, value in TRIPLE_PARTITIONS.items()
}


def four_partition(source_pattern, target_pattern):
    """Unique (x,y,z,w) partition for an edge z--w."""
    source = TRIPLE_PARTITIONS[source_pattern]
    candidates = []
    for w_color in range(4):
        labels = source + (w_color,)
        if labels[2] == labels[3]:
            continue
        if canonical_partition((labels[0], labels[1], labels[3])) != (
            TRIPLE_PARTITIONS[target_pattern]
        ):
            continue
        candidates.append(canonical_partition(labels))
    candidates = sorted(set(candidates))
    assert len(candidates) == 1, (
        source_pattern,
        target_pattern,
        candidates,
    )
    return candidates[0]


class Dinic:
    def __init__(self, node_count):
        self.graph = [[] for _ in range(node_count)]

    def add_edge(self, source, target, capacity):
        source_index = len(self.graph[source])
        target_index = len(self.graph[target])
        self.graph[source].append([target, target_index, capacity, capacity])
        self.graph[target].append([source, source_index, 0, 0])
        return source_index

    def maximum_flow(self, source, sink):
        total = 0
        while True:
            level = [-1] * len(self.graph)
            level[source] = 0
            queue = deque([source])
            while queue:
                vertex = queue.popleft()
                for target, _reverse, capacity, _original in self.graph[
                    vertex
                ]:
                    if capacity and level[target] < 0:
                        level[target] = level[vertex] + 1
                        queue.append(target)
            if level[sink] < 0:
                return total
            cursor = [0] * len(self.graph)

            def augment(vertex, available):
                if vertex == sink:
                    return available
                while cursor[vertex] < len(self.graph[vertex]):
                    edge = self.graph[vertex][cursor[vertex]]
                    target, reverse, capacity, _original = edge
                    if capacity and level[target] == level[vertex] + 1:
                        pushed = augment(target, min(available, capacity))
                        if pushed:
                            edge[2] -= pushed
                            self.graph[target][reverse][2] += pushed
                            return pushed
                    cursor[vertex] += 1
                return 0

            while True:
                pushed = augment(source, 10**100)
                if not pushed:
                    break
                total += pushed


def reconstruct_four_couplings(orbits, transitions, q):
    """Return exact distributions keyed by directed geometric edge (g,h)."""
    common_denominator = 1
    for patterns_ in q:
        for value in patterns_:
            common_denominator = math.lcm(
                common_denominator, value.denominator
            )

    supply, demand = [], []
    for g, orbit in enumerate(orbits):
        size = orbit[4]
        scaled_supply = size * q[g][base.ABA] * common_denominator
        scaled_demand = size * q[g][base.ABB] * common_denominator
        assert scaled_supply.denominator == scaled_demand.denominator == 1
        supply.append(scaled_supply.numerator)
        demand.append(scaled_demand.numerator)

    preflow = {}
    for g, counts in enumerate(transitions):
        for h, ngh in counts.items():
            if g > h:
                continue
            lower = q[g][base.ABA] + q[g][base.ABB] - q[h][base.ABC]
            reverse_lower = (
                q[h][base.ABA] + q[h][base.ABB] - q[g][base.ABC]
            )
            assert lower == reverse_lower
            if lower <= 0:
                continue
            assert g != h
            edge_size = orbits[g][4] * ngh
            scaled_lower = edge_size * lower * common_denominator
            assert scaled_lower.denominator == 1
            amount = scaled_lower.numerator
            forward_forbidden = (
                q[g][base.ABA] == 0 or q[h][base.ABB] == 0
            )
            reverse_forbidden = (
                q[g][base.ABB] == 0 or q[h][base.ABA] == 0
            )
            assert forward_forbidden != reverse_forbidden
            source, target = (h, g) if forward_forbidden else (g, h)
            preflow[(source, target)] = (
                preflow.get((source, target), 0) + amount
            )
            supply[source] -= amount
            demand[target] -= amount

    assert sum(supply) == sum(demand)
    total_residual = sum(supply)
    orbit_count = len(orbits)
    source_node = 2 * orbit_count
    sink_node = source_node + 1
    graph = Dinic(2 * orbit_count + 2)
    for g in range(orbit_count):
        graph.add_edge(source_node, g, supply[g])
        graph.add_edge(orbit_count + g, sink_node, demand[g])
    transport_edges = {}
    for g, counts in enumerate(transitions):
        for h in counts:
            transport_edges[(g, h)] = graph.add_edge(
                g, orbit_count + h, total_residual
            )
    assert graph.maximum_flow(source_node, sink_node) == total_residual

    scaled_flow = dict(preflow)
    for (g, h), edge_index in transport_edges.items():
        edge = graph.graph[g][edge_index]
        amount = edge[3] - edge[2]
        if amount:
            scaled_flow[(g, h)] = scaled_flow.get((g, h), 0) + amount

    def directed_fraction(g, h):
        edge_size = orbits[g][4] * transitions[g][h]
        return Fraction(
            scaled_flow.get((g, h), 0),
            common_denominator * edge_size,
        )

    result = {}
    for g, counts in enumerate(transitions):
        for h in counts:
            a = directed_fraction(g, h)
            c = directed_fraction(h, g)
            coupling_pairs = {
                (base.ABA, base.ABB): a,
                (base.ABA, base.ABC): q[g][base.ABA] - a,
                (base.ABB, base.ABA): c,
                (base.ABB, base.ABC): q[g][base.ABB] - c,
                (base.ABC, base.ABA): q[h][base.ABA] - c,
                (base.ABC, base.ABB): q[h][base.ABB] - a,
                (base.ABC, base.ABC): (
                    q[h][base.ABC]
                    - q[g][base.ABA]
                    - q[g][base.ABB]
                    + a
                    + c
                ),
                (base.AAA, base.AAB): q[g][base.AAA],
                (base.AAB, base.AAA): q[h][base.AAA],
                (base.AAB, base.AAB): (
                    q[g][base.AAB] - q[h][base.AAA]
                ),
            }
            assert all(value >= 0 for value in coupling_pairs.values())
            distribution = defaultdict(Fraction)
            for (source_pattern, target_pattern), value in (
                coupling_pairs.items()
            ):
                distribution[
                    four_partition(source_pattern, target_pattern)
                ] += value
            assert sum(distribution.values()) == 1
            result[(g, h)] = dict(distribution)
    return result


def category_data(orbit, orbit_index):
    i, j, s, t, _size = orbit
    raw = (
        (i - s, (1, 1)),
        (base.R - i - j + s, (1, 0)),
        (base.R - i - t, (0, 1)),
        (i + j + t - base.R + 1, (0, 0)),
    )
    answer = []
    for count, (x_bit, y_bit) in raw:
        if not count:
            answer.append((0, None, x_bit, y_bit))
            continue
        target = (
            i,
            base.R - j - x_bit,
            i - s - (x_bit & y_bit),
            base.R - i - t - ((not x_bit) and y_bit),
        )
        answer.append((count, orbit_index[target], x_bit, y_bit))
    return answer


def cells_for_five(orbit, first_category, second_category):
    """Venn-cell counts for bits (x,y,z,w1,w2)."""
    i, j, s, t, _size = orbit
    triple_cells = {
        (1, 1, 1): s,
        (1, 1, 0): i - s,
        (1, 0, 1): j - s,
        (1, 0, 0): base.R - i - j + s,
        (0, 1, 1): t,
        (0, 1, 0): base.R - i - t,
        (0, 0, 1): base.R - j - t,
        (0, 0, 0): i + j + t - base.R + 1,
    }
    result = defaultdict(int)
    for triple_bits, count in triple_cells.items():
        x_bit, y_bit, z_bit = triple_bits
        if z_bit:
            result[(x_bit, y_bit, z_bit, 0, 0)] += count
            continue
        removed = int((x_bit, y_bit) == first_category) + int(
            (x_bit, y_bit) == second_category
        )
        result[(x_bit, y_bit, 0, 1, 1)] += count - removed
        if (x_bit, y_bit) == first_category:
            result[(x_bit, y_bit, 0, 0, 1)] += 1
        if (x_bit, y_bit) == second_category:
            result[(x_bit, y_bit, 0, 1, 0)] += 1
    assert all(value >= 0 for value in result.values())
    assert sum(result.values()) == 2 * base.R + 1
    return dict(result)


def relation_from_cells(cells, left, right):
    return sum(
        count
        for bits, count in cells.items()
        if bits[left] and bits[right]
    )


def triple_orbit_from_cells(cells, positions, orbit_index):
    x_pos, y_pos, z_pos = positions
    i = relation_from_cells(cells, x_pos, y_pos)
    j = relation_from_cells(cells, x_pos, z_pos)
    s = sum(
        count
        for bits, count in cells.items()
        if bits[x_pos] and bits[y_pos] and bits[z_pos]
    )
    t = sum(
        count
        for bits, count in cells.items()
        if (not bits[x_pos]) and bits[y_pos] and bits[z_pos]
    )
    return orbit_index[(i, j, s, t)]


def check_four_reorder_consistency(
    orbits, orbit_index, four, category_records
):
    """Test whether the stored edge coupling is invariant under x<->y."""
    mismatches = []
    checked = 0
    for g, categories in enumerate(category_records):
        for category_index, (count, h, x_bit, y_bit) in enumerate(
            categories
        ):
            if not count:
                continue
            second = next(
                (candidate_x, candidate_y)
                for candidate_index, (
                    candidate_count,
                    _candidate_h,
                    candidate_x,
                    candidate_y,
                ) in enumerate(categories)
                if candidate_count - int(candidate_index == category_index)
                > 0
            )
            cells = cells_for_five(
                orbits[g], (x_bit, y_bit), second
            )
            gs = triple_orbit_from_cells(cells, (1, 0, 2), orbit_index)
            hs = triple_orbit_from_cells(cells, (1, 0, 3), orbit_index)
            expected = {
                canonical_partition(
                    tuple(partition[index] for index in (1, 0, 2, 3))
                ): value
                for partition, value in four[(g, h)].items()
            }
            checked += 1
            if expected != four[(gs, hs)]:
                mismatches.append((g, h, gs, hs))
                if len(mismatches) >= 10:
                    return checked, mismatches
    return checked, mismatches


def local_star_transport_test(orbits, q, four, category_records):
    """Exact Hall test for coupling two neighbour colors with no equality."""
    failures = []
    tested = 0
    for g, categories in enumerate(category_records):
        for c, (count_c, h_c, _xb_c, _yb_c) in enumerate(categories):
            if not count_c:
                continue
            for d, (count_d, h_d, _xb_d, _yb_d) in enumerate(categories):
                if count_d - int(c == d) <= 0:
                    continue
                dist_c = four[(g, h_c)]
                dist_d = four[(g, h_d)]
                for source_pattern, source_partition in (
                    TRIPLE_PARTITIONS.items()
                ):
                    total = q[g][source_pattern]
                    if not total:
                        continue
                    labels = source_partition
                    rows = [Fraction(0) for _ in range(base.P)]
                    cols = [Fraction(0) for _ in range(base.P)]
                    for partition, value in dist_c.items():
                        if canonical_partition(partition[:3]) != labels:
                            continue
                        colors = [
                            color
                            for color in range(base.P)
                            if canonical_partition(labels + (color,))
                            == partition
                        ]
                        assert colors
                        for color in colors:
                            rows[color] += value / len(colors)
                    for partition, value in dist_d.items():
                        if canonical_partition(partition[:3]) != labels:
                            continue
                        colors = [
                            color
                            for color in range(base.P)
                            if canonical_partition(labels + (color,))
                            == partition
                        ]
                        assert colors
                        for color in colors:
                            cols[color] += value / len(colors)
                    assert sum(rows) == sum(cols) == total
                    tested += 1
                    bad = [
                        color
                        for color in range(base.P)
                        if rows[color] + cols[color] > total
                    ]
                    if bad:
                        failures.append((g, c, d, source_pattern, bad))
                        if len(failures) >= 10:
                            return tested, failures
    return tested, failures


def enumerate_five_orbits(orbits, orbit_index, category_records):
    records = []
    for g, categories in enumerate(category_records):
        for c, (count_c, h_c, x_c, y_c) in enumerate(categories):
            if not count_c:
                continue
            for d, (count_d, h_d, x_d, y_d) in enumerate(categories):
                multiplicity = count_c * (count_d - int(c == d))
                if multiplicity <= 0:
                    continue
                cells = cells_for_five(
                    orbits[g], (x_c, y_c), (x_d, y_d)
                )
                relations = tuple(
                    tuple(
                        relation_from_cells(cells, left, right)
                        for right in range(5)
                    )
                    for left in range(5)
                )
                records.append(
                    {
                        "g": g,
                        "c": c,
                        "d": d,
                        "h1": h_c,
                        "h2": h_d,
                        "multiplicity": multiplicity,
                        "size": orbits[g][4] * multiplicity,
                        "cells": cells,
                        "relations": relations,
                    }
                )
    return records


def enumerate_four_orbits(orbits, orbit_index, category_records):
    records = {}
    for g, categories in enumerate(category_records):
        for count, h, x_bit, y_bit in categories:
            if not count:
                continue
            cells5 = cells_for_five(
                orbits[g],
                (x_bit, y_bit),
                next(
                    (candidate_x, candidate_y)
                    for candidate_count, _candidate_h, candidate_x, candidate_y
                    in categories
                    if candidate_count
                    - int((candidate_x, candidate_y) == (x_bit, y_bit))
                    > 0
                ),
            )
            cells4 = defaultdict(int)
            for bits, value in cells5.items():
                cells4[bits[:4]] += value
            key = (g, h)
            if key in records:
                assert records[key] == dict(cells4)
            records[key] = dict(cells4)
    return records


def partition_respects_geometry(partition, relations):
    for left in range(len(partition)):
        for right in range(left + 1, len(partition)):
            relation = relations[left][right]
            if relation == base.R and partition[left] != partition[right]:
                return False
            if relation in (0, base.R - 1) and (
                partition[left] == partition[right]
            ):
                return False
    return True


def main():
    orbits = base.geometric_orbits(base.R)
    orbit_index = {
        orbit[:4]: index for index, orbit in enumerate(orbits)
    }
    relation = base.relation_data(base.R)
    transitions = base.geometry_neighbor_transitions(base.R, orbits)
    t_by_key, _values = base.load_certificate(orbits)
    q, _alpha = base.build_q(orbits, relation, t_by_key)
    four = reconstruct_four_couplings(orbits, transitions, q)
    categories = [
        category_data(orbit, orbit_index) for orbit in orbits
    ]

    checked, reorder_mismatches = check_four_reorder_consistency(
        orbits, orbit_index, four, categories
    )
    local_tested, local_failures = local_star_transport_test(
        orbits, q, four, categories
    )
    five_records = enumerate_five_orbits(orbits, orbit_index, categories)
    four_records = enumerate_four_orbits(orbits, orbit_index, categories)
    four_partitions = partitions(4)
    four_allowed_counts = [
        sum(
            partition_respects_geometry(
                partition,
                tuple(
                    tuple(
                        relation_from_cells(cells, left, right)
                        for right in range(4)
                    )
                    for left in range(4)
                ),
            )
            for partition in four_partitions
        )
        for cells in four_records.values()
    ]
    five_partitions = partitions(5)
    allowed_counts = [
        sum(
            partition_respects_geometry(partition, record["relations"])
            for partition in five_partitions
        )
        for record in five_records
    ]
    print(
        {
            "four_directed_orbits": len(four),
            "four_allowed_partition_variables": sum(four_allowed_counts),
            "four_allowed_partition_range": (
                min(four_allowed_counts),
                max(four_allowed_counts),
            ),
            "reorder_checked": checked,
            "reorder_mismatches": reorder_mismatches,
            "local_star_transports_tested": local_tested,
            "local_star_transport_failures": local_failures,
            "five_geometric_orbits": len(five_records),
            "five_allowed_partition_variables": sum(allowed_counts),
            "five_allowed_partition_range": (
                min(allowed_counts),
                max(allowed_counts),
            ),
        }
    )


if __name__ == "__main__":
    main()

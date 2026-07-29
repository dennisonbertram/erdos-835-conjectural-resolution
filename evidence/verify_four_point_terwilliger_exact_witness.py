#!/usr/bin/env python3
"""Verify an exact feasible point of a strong relaxation for ER #835.

The certificate is *not* a coloring of O_16.  It is an exact rational
feasible point for:

  * all color-symmetrized triple-orbit equations and support constraints;
  * the complete one-edge four-point extension (replace z by w~z);
  * every color-reduced Terwilliger positive-semidefinite block.

All certificate arithmetic is over Fraction.  The only combinatorial search
is an integer max-flow used to construct the remaining four-point couplings;
every resulting marginal and inequality is replayed exactly.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
from collections import deque
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

R = 15
P = 17
AAA, AAB, ABA, ABB, ABC = range(5)
PATTERNS = ("AAA", "AAB", "ABA", "ABB", "ABC")
DATA_SHA256 = "b2332d8b1f48a0d7dd01dfc832eadadf21ac66c91a0b4f79784e8e600d3ae5ce"


def multinomial(total: int, parts: tuple[int, ...]) -> int:
    if any(part < 0 for part in parts) or sum(parts) != total:
        return 0
    result = factorial(total)
    for part in parts:
        result //= factorial(part)
    return result


def geometric_orbits(r: int):
    """Return (i,j,s,t,size) orbits of Stab(x) on ordered pairs (y,z)."""
    result = []
    for i in range(r + 1):
        for j in range(r + 1):
            for s in range(max(0, i + j - r), min(i, j) + 1):
                inside = multinomial(
                    r, (s, i - s, j - s, r - i - j + s)
                )
                if not inside:
                    continue
                for t in range(
                    max(0, r - 1 - i - j), min(r - i, r - j) + 1
                ):
                    outside = multinomial(
                        r + 1,
                        (
                            t,
                            r - i - t,
                            r - j - t,
                            i + j + t - r + 1,
                        ),
                    )
                    if outside:
                        result.append((i, j, s, t, inside * outside))
    return result


def relation_data(r: int):
    """(valency, eigenvalue, same-color count, other-color count)."""
    p = r + 2
    result = []
    for j in range(r + 1):
        valency = comb(r, j) * comb(r + 1, j + 1)
        eigenvalue = (-1) ** (j + 1) * comb(r, j)
        same_num = valency + (p - 1) * eigenvalue
        other_num = valency - eigenvalue
        assert same_num % p == other_num % p == 0
        same = same_num // p
        other = other_num // p
        assert same >= 0 and other >= 0
        assert same + (p - 1) * other == valency
        result.append((valency, eigenvalue, same, other))
    return result


def geometry_neighbor_transitions(r: int, orbits):
    """Counts for replacing z by each one of its r+1 Odd-graph neighbors."""
    orbit_index = {
        (i, j, s, t): g for g, (i, j, s, t, _size) in enumerate(orbits)
    }
    transitions = []
    for i, j, s, t, _size in orbits:
        counts = {}
        categories = (
            (i - s, 1, 1, 0),
            (r - i - j + s, 1, 0, 0),
            (r - i - t, 0, 0, 1),
            (i + j + t - r + 1, 0, 0, 0),
        )
        for count, dx, dxy, dy_only in categories:
            if not count:
                continue
            target = (
                i,
                r - j - dx,
                i - s - dxy,
                r - i - t - dy_only,
            )
            h = orbit_index[target]
            counts[h] = counts.get(h, 0) + count
        assert sum(counts.values()) == r + 1
        transitions.append(counts)

    for g, counts in enumerate(transitions):
        for h, ngh in counts.items():
            nhg = transitions[h].get(g, 0)
            assert nhg > 0
            assert orbits[g][4] * ngh == orbits[h][4] * nhg
    return transitions


def orbit_key(orbit):
    i, j, s, t, _size = orbit
    return (tuple(sorted((i, j, s + t))), s)


def load_certificate(orbits):
    path = Path(__file__).with_name(
        "four_point_terwilliger_exact_witness_data.b85"
    )
    encoded = "".join(path.read_text(encoding="ascii").split())
    raw = __import__("zlib").decompress(base64.b85decode(encoded))
    assert hashlib.sha256(raw).hexdigest() == DATA_SHA256
    payload = json.loads(raw)

    keys = [
        (tuple(int(x) for x in item[0]), int(item[1]))
        for item in payload["keys"]
    ]
    values = [
        Fraction(int(numerator), int(denominator))
        for numerator, denominator in payload["values"]
    ]
    expected_keys = sorted({orbit_key(orbit) for orbit in orbits})
    assert keys == expected_keys
    assert len(keys) == len(values) == 885
    return dict(zip(keys, values)), values


def build_q(orbits, relation, t_by_key):
    alpha = [Fraction(same, valency) for valency, _e, same, _o in relation]
    q = []
    for orbit in orbits:
        i, j, s, t, _size = orbit
        u = s + t
        aaa = t_by_key[orbit_key(orbit)]
        patterns = (
            aaa,
            alpha[i] - aaa,
            alpha[j] - aaa,
            alpha[u] - aaa,
            Fraction(1) - alpha[i] - alpha[j] - alpha[u] + 2 * aaa,
        )
        assert all(value >= 0 for value in patterns)
        q.append(patterns)
    return q, alpha


def verify_recurrence(orbits, transitions, q, alpha):
    """Replay the 3,876 exact neighbor recurrences defining the witness."""
    for g, (i, _j, _s, _t, _size) in enumerate(orbits):
        lhs = q[g][AAA] + sum(
            count * q[h][AAA] for h, count in transitions[g].items()
        )
        assert lhs == alpha[i]


def verify_triple_layer(orbits, relation, q):
    """Replay support, symmetry, marginals, and all local-bijection rows."""
    n_vertices = comb(2 * R + 1, R)
    orbit_index = {
        (i, j, s, t): g for g, (i, j, s, t, _size) in enumerate(orbits)
    }

    for g, (i, j, s, t, _size) in enumerate(orbits):
        u = s + t
        assert sum(q[g]) == 1
        allowed = set(range(5))
        if i == R:
            allowed &= {AAA, AAB}
        if j == R:
            allowed &= {AAA, ABA}
        if u == R:
            allowed &= {AAA, ABB}
        if i == 0:
            allowed -= {AAA, AAB}
        if j == 0:
            allowed -= {AAA, ABA}
        if u == 0:
            allowed -= {AAA, ABB}
        for pattern in range(5):
            if pattern not in allowed:
                assert q[g][pattern] == 0

        gt = orbit_index[(j, i, s, t)]
        for pattern, transposed in (
            (AAA, AAA),
            (AAB, ABA),
            (ABA, AAB),
            (ABB, ABB),
            (ABC, ABC),
        ):
            assert q[g][pattern] == q[gt][transposed]

    for relation_index in range(R + 1):
        same = relation[relation_index][2]
        xy = sum(
            size * (q[g][AAA] + q[g][AAB])
            for g, (i, _j, _s, _t, size) in enumerate(orbits)
            if i == relation_index
        )
        xz = sum(
            size * (q[g][AAA] + q[g][ABA])
            for g, (_i, j, _s, _t, size) in enumerate(orbits)
            if j == relation_index
        )
        yz = sum(
            size * (q[g][AAA] + q[g][ABB])
            for g, (_i, _j, s, t, size) in enumerate(orbits)
            if s + t == relation_index
        )
        assert xy == xz == yz == same * n_vertices

    for i in range(R + 1):
        same, other = relation[i][2], relation[i][3]
        yz_edge = [
            (g, size)
            for g, (ii, _j, s, t, size) in enumerate(orbits)
            if ii == i and s + t == 0
        ]
        for pattern, target in (
            (AAB, same * (P - 1)),
            (ABA, (P - 1) * other),
            (ABC, (P - 1) * (P - 2) * other),
        ):
            assert sum(size * q[g][pattern] for g, size in yz_edge) == target

        xz_edge = [
            (g, size)
            for g, (ii, j, _s, _t, size) in enumerate(orbits)
            if ii == i and j == 0
        ]
        for pattern, target in (
            (AAB, same * (P - 1)),
            (ABB, (P - 1) * other),
            (ABC, (P - 1) * (P - 2) * other),
        ):
            assert sum(size * q[g][pattern] for g, size in xz_edge) == target

    for j in range(R + 1):
        same, other = relation[j][2], relation[j][3]
        xy_edge = [
            (g, size)
            for g, (i, jj, _s, _t, size) in enumerate(orbits)
            if i == 0 and jj == j
        ]
        for pattern, target in (
            (ABA, same * (P - 1)),
            (ABB, (P - 1) * other),
            (ABC, (P - 1) * (P - 2) * other),
        ):
            assert sum(size * q[g][pattern] for g, size in xy_edge) == target


def cbinom(n: int, k: int) -> int:
    return comb(n, k) if 0 <= k <= n else 0


def harmonic_norm(n: int, ell: int, a: int) -> int:
    if ell > min(a, n - a):
        return 0
    return (2**ell) * comb(n - 2 * ell, a - ell)


def harmonic_lambda(
    n: int, ell: int, a: int, b: int, intersection: int
) -> int:
    if ell > min(a, n - a, b, n - b):
        return 0
    return sum(
        (-1) ** (ell - q)
        * comb(ell, q)
        * cbinom(a - ell, intersection - q)
        * cbinom(n - a - ell, b - ell - intersection + q)
        for q in range(ell + 1)
    )


def terwilliger_block_specs(orbits):
    for ell in range(R // 2 + 1):
        for mm in range((R + 1) // 2 + 1):
            shells = [
                i
                for i in range(R + 1)
                if ell <= min(i, R - i) and mm <= min(R - i, i + 1)
            ]
            if not shells:
                continue
            position = {shell: index for index, shell in enumerate(shells)}
            coefficients = {
                (position[i], position[j]): []
                for i in shells
                for j in shells
            }
            for g, (i, j, s, t, _size) in enumerate(orbits):
                if i not in position or j not in position:
                    continue
                coefficient = (
                    harmonic_norm(R, ell, i)
                    * harmonic_norm(R + 1, mm, R - i)
                    * harmonic_lambda(R, ell, i, j, s)
                    * harmonic_lambda(R + 1, mm, R - i, R - j, t)
                )
                if coefficient:
                    coefficients[(position[i], position[j])].append(
                        (g, coefficient)
                    )
            yield (ell, mm), shells, coefficients


def zero_matrix(n: int):
    return [[Fraction(0) for _ in range(n)] for _ in range(n)]


def certify_rank_at_most_one_psd(matrix) -> int:
    n = len(matrix)
    assert all(
        matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)
    )
    pivot = next((i for i in range(n) if matrix[i][i] != 0), None)
    if pivot is None:
        assert all(matrix[i][j] == 0 for i in range(n) for j in range(n))
        return 0
    diagonal = matrix[pivot][pivot]
    assert diagonal > 0
    for i in range(n):
        for j in range(n):
            assert (
                matrix[i][j] * diagonal
                == matrix[i][pivot] * matrix[pivot][j]
            )
    return 1


def verify_terwilliger_psd(orbits, q):
    rank_counts = {0: 0, 1: 0}
    block_count = 0
    for _label, shells, coefficients in terwilliger_block_specs(orbits):
        d = len(shells)
        a, b, c, dd = (zero_matrix(d) for _ in range(4))
        for (ii, jj), entries in coefficients.items():
            for g, coefficient in entries:
                a[ii][jj] += coefficient * q[g][AAA]
                b[ii][jj] += Fraction(coefficient, P - 1) * q[g][AAB]
                c[ii][jj] += Fraction(coefficient, P - 1) * q[g][ABB]
                dd[ii][jj] += (
                    Fraction(coefficient, (P - 1) * (P - 2)) * q[g][ABC]
                )

        standard = zero_matrix(d)
        trivial = zero_matrix(2 * d)
        for i in range(d):
            for j in range(d):
                standard[i][j] = c[i][j] - dd[i][j]
                trivial[i][j] = a[i][j]
                trivial[i][d + j] = (P - 1) * b[i][j]
                trivial[d + i][j] = (P - 1) * b[j][i]
                trivial[d + i][d + j] = (
                    (P - 1) * c[i][j]
                    + (P - 1) * (P - 2) * dd[i][j]
                )

        for matrix in (standard, trivial):
            rank = certify_rank_at_most_one_psd(matrix)
            rank_counts[rank] += 1
            block_count += 1

    assert block_count == 144
    assert rank_counts == {0: 115, 1: 29}
    return block_count, rank_counts


def verify_four_point_edge_extension(orbits, transitions, q):
    """Construct and verify all one-edge four-point equality couplings."""
    common_denominator = 1
    for patterns in q:
        for value in patterns:
            common_denominator = math.lcm(
                common_denominator, value.denominator
            )

    supply, demand = [], []
    for g, orbit in enumerate(orbits):
        size = orbit[4]
        scaled_supply = size * q[g][ABA] * common_denominator
        scaled_demand = size * q[g][ABB] * common_denominator
        assert scaled_supply.denominator == scaled_demand.denominator == 1
        supply.append(scaled_supply.numerator)
        demand.append(scaled_demand.numerator)

    preflow = {}
    positive_pair_bounds = 0
    for g, counts in enumerate(transitions):
        for h, ngh in counts.items():
            if g > h:
                continue
            lower = q[g][ABA] + q[g][ABB] - q[h][ABC]
            reverse_lower = q[h][ABA] + q[h][ABB] - q[g][ABC]
            assert lower == reverse_lower
            if lower <= 0:
                continue
            assert g != h
            positive_pair_bounds += 1
            edge_size = orbits[g][4] * ngh
            assert edge_size == orbits[h][4] * transitions[h][g]
            scaled_lower = edge_size * lower * common_denominator
            assert scaled_lower.denominator == 1
            amount = scaled_lower.numerator

            forward_forbidden = q[g][ABA] == 0 or q[h][ABB] == 0
            reverse_forbidden = q[g][ABB] == 0 or q[h][ABA] == 0
            assert forward_forbidden != reverse_forbidden
            source, target = (h, g) if forward_forbidden else (g, h)
            preflow[(source, target)] = (
                preflow.get((source, target), 0) + amount
            )
            supply[source] -= amount
            demand[target] -= amount
            assert supply[source] >= 0 and demand[target] >= 0

    assert sum(supply) == sum(demand)
    total_residual = sum(supply)
    class Dinic:
        def __init__(self, node_count):
            self.graph = [[] for _ in range(node_count)]
            self.forward_edges = 0

        def add_edge(self, source, target, capacity):
            source_index = len(self.graph[source])
            target_index = len(self.graph[target])
            self.graph[source].append([target, target_index, capacity, capacity])
            self.graph[target].append([source, source_index, 0, 0])
            self.forward_edges += 1
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
                        edge_index = cursor[vertex]
                        edge = self.graph[vertex][edge_index]
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
                    pushed = augment(source, total_residual)
                    if not pushed:
                        break
                    total += pushed

    orbit_count = len(orbits)
    source_node = 2 * orbit_count
    sink_node = source_node + 1
    graph = Dinic(2 * orbit_count + 2)
    for g in range(len(orbits)):
        graph.add_edge(source_node, g, supply[g])
        graph.add_edge(orbit_count + g, sink_node, demand[g])
    transport_edges = {}
    for g, counts in enumerate(transitions):
        for h in counts:
            edge_index = graph.add_edge(g, orbit_count + h, total_residual)
            transport_edges[(g, h)] = edge_index

    flow_value = graph.maximum_flow(source_node, sink_node)
    assert flow_value == total_residual

    scaled_flow = dict(preflow)
    for g, counts in enumerate(transitions):
        for h in counts:
            edge = graph.graph[g][transport_edges[(g, h)]]
            amount = edge[3] - edge[2]
            if amount:
                scaled_flow[(g, h)] = scaled_flow.get((g, h), 0) + amount

    def directed_fraction(g, h):
        edge_size = orbits[g][4] * transitions[g][h]
        return Fraction(
            scaled_flow.get((g, h), 0), common_denominator * edge_size
        )

    for g, counts in enumerate(transitions):
        assert sum(
            count * directed_fraction(g, h) for h, count in counts.items()
        ) == q[g][ABA]
        assert sum(
            count * directed_fraction(h, g) for h, count in counts.items()
        ) == q[g][ABB]

    for g, counts in enumerate(transitions):
        for h in counts:
            if g > h:
                continue
            a = directed_fraction(g, h)
            c = directed_fraction(h, g)
            if g == h:
                assert a == c
            xg, yg, zg = q[g][ABA], q[g][ABB], q[g][ABC]
            xh, yh, zh = q[h][ABA], q[h][ABB], q[h][ABC]
            coupling = {
                (ABA, ABB): a,
                (ABA, ABC): xg - a,
                (ABB, ABA): c,
                (ABB, ABC): yg - c,
                (ABC, ABA): xh - c,
                (ABC, ABB): yh - a,
                (ABC, ABC): zh - xg - yg + a + c,
            }
            assert all(value >= 0 for value in coupling.values())
            for pattern in (ABA, ABB, ABC):
                assert sum(
                    value
                    for (source, _target), value in coupling.items()
                    if source == pattern
                ) == q[g][pattern]
                assert sum(
                    value
                    for (_source, target), value in coupling.items()
                    if target == pattern
                ) == q[h][pattern]

            a_component = {
                (AAA, AAB): q[g][AAA],
                (AAB, AAA): q[h][AAA],
                (AAB, AAB): q[g][AAB] - q[h][AAA],
            }
            assert all(value >= 0 for value in a_component.values())
            for pattern in (AAA, AAB):
                assert sum(
                    value
                    for (source, _target), value in a_component.items()
                    if source == pattern
                ) == q[g][pattern]
                assert sum(
                    value
                    for (_source, target), value in a_component.items()
                    if target == pattern
                ) == q[h][pattern]

    for g, counts in enumerate(transitions):
        degree = sum(counts.values())
        assert degree == P - 1
        aab_to_aaa = sum(
            count * q[h][AAA] for h, count in counts.items()
        )
        assert aab_to_aaa == q[g][AAB]
        assert (
            sum(
                count * (q[g][AAB] - q[h][AAA])
                for h, count in counts.items()
            )
            == (P - 2) * q[g][AAB]
        )

        aba_to_abb = sum(
            count * directed_fraction(g, h) for h, count in counts.items()
        )
        abb_to_aba = sum(
            count * directed_fraction(h, g) for h, count in counts.items()
        )
        assert aba_to_abb == q[g][ABA]
        assert abb_to_aba == q[g][ABB]
        assert degree * q[g][ABA] - aba_to_abb == (P - 2) * q[g][ABA]
        assert degree * q[g][ABB] - abb_to_aba == (P - 2) * q[g][ABB]

        abc_to_aba = sum(
            count * (q[h][ABA] - directed_fraction(h, g))
            for h, count in counts.items()
        )
        abc_to_abb = sum(
            count * (q[h][ABB] - directed_fraction(g, h))
            for h, count in counts.items()
        )
        assert abc_to_aba == abc_to_abb == q[g][ABC]
        abc_to_abc = sum(
            count
            * (
                q[h][ABC]
                - q[g][ABA]
                - q[g][ABB]
                + directed_fraction(g, h)
                + directed_fraction(h, g)
            )
            for h, count in counts.items()
        )
        assert abc_to_abc == (P - 3) * q[g][ABC]

    return {
        "common_denominator": common_denominator,
        "positive_pair_bounds": positive_pair_bounds,
        "flow_nodes": len(graph.graph),
        "flow_edges": graph.forward_edges,
        "nonzero_directed_flows": sum(
            amount != 0 for amount in scaled_flow.values()
        ),
    }


def main():
    orbits = geometric_orbits(R)
    assert len(orbits) == 3_876
    relation = relation_data(R)
    transitions = geometry_neighbor_transitions(R, orbits)
    t_by_key, t_values = load_certificate(orbits)
    q, alpha = build_q(orbits, relation, t_by_key)

    verify_recurrence(orbits, transitions, q, alpha)
    verify_triple_layer(orbits, relation, q)
    blocks, rank_counts = verify_terwilliger_psd(orbits, q)
    flow = verify_four_point_edge_extension(orbits, transitions, q)

    print(
        {
            "status": "PASS",
            "scope": "necessary relaxation only; not a coloring of O_16",
            "orbits": len(orbits),
            "symmetric_t_variables": len(t_values),
            "q_entries": 5 * len(q),
            "terwilliger_blocks": blocks,
            "terwilliger_rank_counts": rank_counts,
            "max_t_numerator_bits": max(
                value.numerator.bit_length() for value in t_values
            ),
            "max_t_denominator_bits": max(
                value.denominator.bit_length() for value in t_values
            ),
            **flow,
        }
    )


if __name__ == "__main__":
    main()

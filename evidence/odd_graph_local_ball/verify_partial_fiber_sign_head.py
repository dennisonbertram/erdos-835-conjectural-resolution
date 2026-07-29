#!/usr/bin/env python3
"""Exact audit of the remaining global partial-fiber sign head.

This is a finite, stdlib-only computation.  It:

* enumerates all 1,680 labelled k=6 radius-3 families;
* evaluates every one of their seven choices of the distinguished colour;
* evaluates all 17 distinguished-colour choices for the Wallis k=16 family;
* computes H_required = RHS(F)/E, the value forced on a hypothetical
  radius-5 extension, where E is the generic hole-orientation product from
  equation (10) of flag_at_exact_formula.md (no actual H is observed); and
* exhausts small synthetic one-sided matching controls used in the companion
  note.

It neither constructs a radius-5 ball nor proves that one does not exist.
"""

from __future__ import annotations

import importlib.util
from collections import Counter
from itertools import permutations
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CENSUS = (
    REPO
    / "collaboration"
    / "opus5"
    / "radius5_followup"
    / "verify_radius3_census_and_k6_obstruction.py"
)


def load_census():
    spec = importlib.util.spec_from_file_location("radius3_census", CENSUS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def product(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def sign_sequence(sequence):
    sequence = list(sequence)
    assert sorted(sequence) == list(range(len(sequence)))
    inversions = sum(
        sequence[a] > sequence[b]
        for a in range(len(sequence))
        for b in range(a + 1, len(sequence))
    )
    return -1 if inversions & 1 else 1


def sign_map(domain, target, mapping):
    position = {value: index for index, value in enumerate(target)}
    assert set(mapping) == set(domain)
    images = [position[mapping[value]] for value in domain]
    return sign_sequence(images)


def entry(square, a, b):
    if a == b:
        return a
    return square[(min(a, b), max(a, b))]


def row_sign(square, order, row):
    return sign_map(
        order,
        order,
        {column: entry(square, row, column) for column in order},
    )


def delta(square, order):
    return product(row_sign(square, order, row) for row in order)


def at_of_T(family, distinguished, order):
    """AT sign of T for the induced order V and the family order."""
    V = [value for value in order if value != distinguished]
    rows = list(range(len(family))) + ["e"]
    table = {}
    for i, square in enumerate(family):
        for u in V:
            table[(i, u)] = entry(square, distinguished, u)
    for u in V:
        table[("e", u)] = u
    row_product = product(
        sign_map(V, V, {u: table[(row, u)] for u in V}) for row in rows
    )
    column_product = product(
        sign_map(rows, V, {row: table[(row, u)] for row in rows}) for u in V
    )
    return row_product * column_product


def orientation_product(family, distinguished, order):
    """The global generic epsilon product E(L,M) in equation (10)."""
    V = [value for value in order if value != distinguished]
    answer = 1
    for square in family:
        L = {u: entry(square, distinguished, u) for u in V}
        L_inverse = {value: u for u, value in L.items()}
        assert set(L) == set(V) == set(L_inverse)
        for u in V:
            for x in V:
                if x in {u, L[u]}:
                    continue
                v_L = L_inverse[x]
                candidates = [
                    v
                    for v in V
                    if v != u and entry(square, u, v) == x
                ]
                assert len(candidates) == 1
                v_M = candidates[0]
                assert v_M != v_L
                # Removing u from the induced column order does not change
                # the relative order of v_M and v_L.
                answer *= 1 if V.index(v_M) < V.index(v_L) else -1
    return answer


def evaluate(family, distinguished, order):
    k = len(order) - 1
    assert k % 2 == 0 and len(family) == k - 1
    E = orientation_product(family, distinguished, order)
    rhs = (-1) ** (k * (k - 1) // 2)
    rhs *= at_of_T(family, distinguished, order)
    rhs *= product(delta(square, order) for square in family)
    # Division and multiplication agree for signs.
    required_H = rhs * E
    assert required_H * E == rhs
    return E, rhs, required_H


def census_values():
    census = load_census()
    squares = census.all_sils(7)
    families = census.discordant_families(squares, 7, 5)
    assert len(squares) == 6240
    assert len(families) == 1680
    order6 = list(range(7))
    k6 = Counter()
    per_family = Counter()
    for indices in families:
        family = [squares[index] for index in indices]
        values = tuple(
            evaluate(family, distinguished, order6)
            for distinguished in order6
        )
        k6.update(values)
        per_family[values] += 1
    assert all(E == 1 for E, _, _ in k6)
    assert k6 == Counter({(1, -1, -1): 6720, (1, 1, 1): 5040})
    assert len(per_family) == 35
    assert set(per_family.values()) == {48}
    assert all(
        sum(1 for _, _, required in profile if required == -1) == 4
        for profile in per_family
    )

    wallis = census.wallis_sils()
    assert len(wallis) == 15
    order16 = list(range(17))
    wallis_values = [
        evaluate(wallis, distinguished, order16)
        for distinguished in order16
    ]

    print("[exact] k=6 radius-3 families:", len(families))
    print("[exact] k=6 family/root cases:", sum(k6.values()))
    print("[exact] k=6 (E,RHS,H_required-on-an-extension) distribution:")
    for value, count in sorted(k6.items()):
        print(f"        {value}: {count}")
    print("[exact] distinct seven-root profiles:", len(per_family))
    print("[exact] every profile has four -1 roots and three +1 roots")
    print("[exact] all C(7,4)=35 profiles occur, 48 families each")

    wallis_counter = Counter(wallis_values)
    assert wallis_counter == Counter({(1, 1, 1): 17})
    print("[exact] k=16 Wallis distinguished-colour cases:", len(wallis_values))
    print("[exact] Wallis (E,RHS,H_required-on-an-extension) distribution:")
    for value, count in sorted(wallis_counter.items()):
        print(f"        {value}: {count}")
    return k6, per_family, wallis_counter


def local_fiber_controls():
    """Both signs occur for every nontrivial prescribed partial fiber.

    These controls deliberately use only the data of one forced partial
    matching: ordered domain, ordered codomain, and prescribed holes.
    """
    counts = {}
    for size in range(2, 8):
        signs = Counter(sign_sequence(image) for image in permutations(range(size)))
        assert signs[-1] == signs[1] > 0
        counts[size] = dict(sorted(signs.items()))
    print("[exact] isolated prescribed-fiber signs (domain size -> counts):")
    for size, signs in counts.items():
        print(f"        {size}: {signs}")


def complete_biregular_controls():
    """Exhaust a no-hole two-sided analogue on K4 x K4.

    Label each edge of the first K4 by one of the three one-factors of the
    second.  The dual condition holds exactly when every label class is a
    one-factor.  All six such tensors are enumerated.  Their product of all
    16 local link-permutation signs is +1.  This is a positive sanity check,
    not evidence for the holed problem.
    """
    vertices = list(range(4))
    edges = [(a, b) for a in vertices for b in range(a + 1, 4)]
    factors = (
        frozenset({(0, 1), (2, 3)}),
        frozenset({(0, 2), (1, 3)}),
        frozenset({(0, 3), (1, 2)}),
    )
    edge_factor = {
        edge: index
        for index, factor in enumerate(factors)
        for edge in factor
    }
    values = Counter()
    for relabel in permutations(range(3)):
        link_product = 1
        for i in vertices:
            domain = [j for j in vertices if j != i]
            for u in vertices:
                target = [v for v in vertices if v != u]
                mapping = {}
                for j in domain:
                    colour = relabel[edge_factor[tuple(sorted((i, j)))]]
                    mate_edge = next(
                        edge for edge in factors[colour] if u in edge
                    )
                    mapping[j] = next(v for v in mate_edge if v != u)
                link_product *= sign_map(domain, target, mapping)
        values[link_product] += 1
    assert values == Counter({1: 6})
    print("[exact] complete K4 x K4 two-sided controls:", dict(values))


def perfect_matchings(vertices):
    """All perfect matchings, as tuples of sorted edges."""
    vertices = tuple(vertices)
    if not vertices:
        return [()]
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            answer.append((tuple(sorted((first, second))),) + tail)
    return answer


def complete_k6_tensor_controls(limit=2000):
    """Enumerate exact two-sided no-hole K6 x K6 matching tensors.

    A tensor chooses a perfect matching of the second K6 for every edge of
    the first K6.  For every edge of the second K6, its chosen first-side
    edges must also form a perfect matching.  This is the closest no-hole
    analogue of the two forced trace layers.  We fix one row by finite-label
    symmetry and exhaust the remaining tree.  The companion note proves that
    this normalization preserves the global sign at even order.
    """
    vertices = tuple(range(6))
    edges = tuple(
        (a, b) for a in vertices for b in vertices if a < b
    )
    edge_index = {edge: index for index, edge in enumerate(edges)}
    matchings = tuple(perfect_matchings(vertices))
    assert len(matchings) == 15
    matching_masks = tuple(
        tuple(edge_index[edge] for edge in matching) for matching in matchings
    )
    edge_masks = tuple((1 << a) | (1 << b) for a, b in edges)
    canonical = matchings.index(((0, 1), (2, 3), (4, 5)))

    assigned = [-1] * len(edges)
    column_vertex_masks = [0] * len(edges)
    column_counts = [0] * len(edges)
    assigned[0] = canonical
    for column in matching_masks[canonical]:
        column_vertex_masks[column] |= edge_masks[0]
        column_counts[column] += 1

    signs = Counter()
    solutions = 0

    def candidates(row):
        row_mask = edge_masks[row]
        return [
            matching
            for matching, columns in enumerate(matching_masks)
            if all(
                column_counts[column] < 3
                and not (column_vertex_masks[column] & row_mask)
                for column in columns
            )
        ]

    def tensor_sign():
        answer = 1
        for i in vertices:
            domain = [j for j in vertices if j != i]
            for u in vertices:
                target = [v for v in vertices if v != u]
                mapping = {}
                for j in domain:
                    row = edge_index[tuple(sorted((i, j)))]
                    matching = matchings[assigned[row]]
                    mate_edge = next(edge for edge in matching if u in edge)
                    mapping[j] = next(v for v in mate_edge if v != u)
                answer *= sign_map(domain, target, mapping)
        return answer

    def search():
        nonlocal solutions
        if solutions >= limit:
            return
        unassigned = [row for row, value in enumerate(assigned) if value < 0]
        if not unassigned:
            assert all(count == 3 for count in column_counts)
            signs[tensor_sign()] += 1
            solutions += 1
            return
        choices = [(len(candidates(row)), row) for row in unassigned]
        _, row = min(choices)
        for matching in candidates(row):
            assigned[row] = matching
            columns = matching_masks[matching]
            old_masks = [column_vertex_masks[column] for column in columns]
            for column in columns:
                column_vertex_masks[column] |= edge_masks[row]
                column_counts[column] += 1
            search()
            for column, old_mask in zip(columns, old_masks):
                column_vertex_masks[column] = old_mask
                column_counts[column] -= 1
            assigned[row] = -1
            if solutions >= limit:
                return

    search()
    assert solutions > 0
    assert solutions == 336
    assert signs == Counter({1: 336})
    completeness = (
        "complete symmetry-normalized" if solutions < limit else "prefix"
    )
    print(
        f"[exact] {completeness} K6 x K6 tensors ({solutions}):",
        dict(sorted(signs.items())),
    )
    return signs


def holed_trace_controls(limit=2000):
    """Synthetic exact k=6 trace layer, without radius-3 M palettes.

    The cyclic Latin chart supplies only L.  Every ij-slice is required to
    have exactly the forced radius-5 trace (one perfect and six near-perfect
    colour classes).  The one-flag controls use these slices independently.
    A separate exhaustive assembly then asks every uv-slice to be a proper
    edge-colouring of K5, still without any M table or prescribed uv palette.
    """
    k = 6
    A = tuple(range(k - 1))
    V = tuple(range(k))
    infinity = k
    a_edges = tuple((i, j) for i in A for j in A if i < j)
    v_edges = tuple((u, v) for u in V for v in V if u < v)
    v_edge_index = {edge: index for index, edge in enumerate(v_edges)}
    L = tuple(
        tuple((u + i + 1) % k for u in V)
        for i in A
    )
    inverse = tuple(
        tuple(next(u for u in V if L[i][u] == x) for x in V)
        for i in A
    )

    def matching_indices(vertices):
        return tuple(
            tuple(v_edge_index[edge] for edge in matching)
            for matching in perfect_matchings(tuple(vertices))
        )

    full_matchings = matching_indices(V)
    options = {}
    for edge_index_A, (i, j) in enumerate(a_edges):
        colour_matchings = {
            infinity: full_matchings,
        }
        for x in V:
            allowed = [
                u for u in V if u not in {inverse[i][x], inverse[j][x]}
            ]
            colour_matchings[x] = matching_indices(allowed)
            assert colour_matchings[x]

        out = []

        def assemble(colour, used, assignment):
            if colour == k:
                if len(used) == len(v_edges):
                    edge_colours = [-1] * len(v_edges)
                    for x, matching in assignment.items():
                        for edge in matching:
                            edge_colours[edge] = x
                    assert set(edge_colours) == set(range(k + 1))
                    out.append(tuple(edge_colours))
                return
            for matching in colour_matchings[colour]:
                if any(edge in used for edge in matching):
                    continue
                assignment[colour] = matching
                assemble(
                    colour + 1,
                    used | set(matching),
                    assignment,
                )
                del assignment[colour]

        for infinity_matching in colour_matchings[infinity]:
            assemble(
                0,
                set(infinity_matching),
                {infinity: infinity_matching},
            )
        options[edge_index_A] = tuple(out)
        assert out

    option_counts = Counter(len(value) for value in options.values())
    assert option_counts == Counter({12: 4, 20: 4, 56: 2})

    # One-sided exact controls: every chosen ij-slice is a complete forced
    # trace decomposition.  At just one flag, require distinct mate values so
    # its local partial fiber is a genuine bijection.  Conditions at all other
    # flags, and every M-palette condition, are intentionally out of scope.
    for x in (infinity, 2):
        i, u = 0, 0
        domain = []
        for j in A:
            if j == i:
                continue
            if x != infinity and u in {inverse[i][x], inverse[j][x]}:
                continue
            domain.append(j)
        possible_mates = {}
        for j in domain:
            a_edge_index = a_edges.index(tuple(sorted((i, j))))
            possible_mates[j] = set()
            for colouring in options[a_edge_index]:
                hits = [
                    v
                    for v in V
                    if v != u
                    and colouring[
                        v_edge_index[tuple(sorted((u, v)))]
                    ]
                    == x
                ]
                assert len(hits) == 1
                possible_mates[j].add(hits[0])

        target_signs = {}

        def enumerate_flag(position, mapping):
            if position == len(domain):
                target = tuple(sorted(mapping.values()))
                sign = sign_map(domain, target, mapping)
                target_signs.setdefault(target, set()).add(sign)
                return
            j = domain[position]
            for v in sorted(possible_mates[j]):
                if v in mapping.values():
                    continue
                mapping[j] = v
                enumerate_flag(position + 1, mapping)
                del mapping[j]

        enumerate_flag(0, {})
        both = [
            target
            for target, signs_here in target_signs.items()
            if signs_here == {-1, 1}
        ]
        expected = (5, 5) if x == infinity else (4, 3)
        assert (len(target_signs), len(both)) == expected
        print(
            f"[exact] one-sided ij-trace flag x={x}: "
            f"{len(target_signs)} image sets, {len(both)} realize both signs"
        )
    used = [
        [set() for _ in A]
        for _ in v_edges
    ]
    chosen = [-1] * len(a_edges)
    signs = Counter()
    solutions = 0

    def candidates(a_edge_index):
        i, j = a_edges[a_edge_index]
        return [
            option_index
            for option_index, colouring in enumerate(options[a_edge_index])
            if all(
                colouring[v_edge] not in used[v_edge][i]
                and colouring[v_edge] not in used[v_edge][j]
                for v_edge in range(len(v_edges))
            )
        ]

    def partial_product():
        answer = 1
        for i in A:
            for u in V:
                for x in range(k + 1):
                    if x == L[i][u]:
                        continue
                    mapping = {}
                    for j in A:
                        if j == i:
                            continue
                        a_edge_index = a_edges.index(tuple(sorted((i, j))))
                        colouring = options[a_edge_index][chosen[a_edge_index]]
                        hits = [
                            v
                            for v in V
                            if v != u
                            and colouring[
                                v_edge_index[tuple(sorted((u, v)))]
                            ]
                            == x
                        ]
                        if hits:
                            assert len(hits) == 1
                            mapping[j] = hits[0]
                    target = sorted(mapping.values())
                    assert len(target) == len(set(target))
                    if mapping:
                        answer *= sign_map(sorted(mapping), target, mapping)
        return answer

    def search():
        nonlocal solutions
        if solutions >= limit:
            return
        remaining = [index for index, value in enumerate(chosen) if value < 0]
        if not remaining:
            signs[partial_product()] += 1
            solutions += 1
            return
        _, a_edge_index = min((len(candidates(index)), index) for index in remaining)
        i, j = a_edges[a_edge_index]
        for option_index in candidates(a_edge_index):
            colouring = options[a_edge_index][option_index]
            chosen[a_edge_index] = option_index
            for v_edge, x in enumerate(colouring):
                used[v_edge][i].add(x)
                used[v_edge][j].add(x)
            search()
            for v_edge, x in enumerate(colouring):
                used[v_edge][i].remove(x)
                used[v_edge][j].remove(x)
            chosen[a_edge_index] = -1
            if solutions >= limit:
                return

    search()
    assert solutions == 0
    print(f"[exact] synthetic cyclic-L k={k} ij-option counts:", dict(option_counts))
    print(
        f"[exact] no cyclic-L k={k} trace/proper control exists "
        "(in this weaker M-free model)"
    )
    return signs


def main():
    census_values()
    local_fiber_controls()
    complete_biregular_controls()
    complete_k6_tensor_controls()
    holed_trace_controls()
    print("ALL PARTIAL-FIBER SIGN-HEAD AUDITS PASSED")
    print("SCOPE: no independent value theorem for H; #835 remains open.")


if __name__ == "__main__":
    main()

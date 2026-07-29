#!/usr/bin/env python3
"""Verify the prescribed-colour boundary-flow audit on all 16 Venn types."""

from __future__ import annotations

from itertools import combinations, permutations, product


VERTICES = tuple(range(13))
COLORS = (1, 2, 3)  # the nonzero elements of F_2^2, encoded by xor
CELL_MASKS = tuple(range(1, 8))

EDGE_CERTIFICATES = (
    "3-4,3-8,3-9,4-6,4-10,5-6,5-9,5-12,6-11,7-9,7-10,7-11,8-11,8-12,10-12",
    "0-9,1-12,3-7,4-7,4-10,4-11,5-6,5-7,5-8,6-10,6-12,8-9,8-11,9-10,11-12",
    "0-8,3-7,3-10,4-5,4-6,4-7,5-10,5-12,6-8,6-9,7-11,8-12,9-10,9-11,11-12",
    "0-9,1-12,2-8,3-5,3-6,4-11,5-7,5-11,6-7,6-12,7-10,8-9,8-11,9-10,10-12",
    "0-10,1-7,3-5,3-9,4-9,4-11,5-8,5-11,6-7,6-11,6-12,7-12,8-10,8-12,9-10",
    "0-11,1-8,2-9,3-7,3-11,4-9,4-10,5-6,5-12,6-7,6-11,7-10,8-10,8-12,9-12",
    "0-5,1-7,3-10,3-11,4-6,4-11,5-6,5-10,6-8,7-9,7-12,8-9,8-12,9-12,10-11",
    "0-8,1-10,2-4,3-8,3-9,4-12,5-9,5-11,6-7,6-10,6-12,7-8,7-10,9-11,11-12",
    "0-7,0-9,3-10,3-11,4-5,4-6,5-8,5-12,6-7,6-11,7-10,8-10,8-12,9-11,9-12",
    "0-11,0-12,1-9,2-7,3-9,3-11,4-8,4-10,5-6,6-8,6-12,7-9,7-10,8-11,10-12",
    "0-4,0-5,1-11,3-7,3-10,4-12,5-8,6-7,6-9,6-12,7-9,8-9,8-11,10-11,10-12",
    "0-10,0-12,1-8,2-9,3-4,3-6,4-11,5-7,5-10,6-8,7-11,7-12,8-12,9-10,9-11",
    "0-5,0-6,1-11,2-12,3-8,3-9,4-7,4-10,5-7,6-9,7-9,8-10,8-12,10-11,11-12",
    "0-7,0-9,1-5,1-12,3-8,3-12,4-5,4-8,6-7,6-11,7-10,8-11,9-10,9-12,10-11",
    "0-9,0-11,1-7,1-12,2-9,3-4,3-12,4-10,5-6,5-12,6-8,7-10,8-10,8-11,9-11",
    "0-10,0-11,1-4,1-12,2-3,2-7,3-9,4-6,5-7,5-8,6-10,8-11,9-10,9-12,11-12",
)


def popcount(value: int) -> int:
    return bin(value).count("1")


def permuted_signature(
    signature: tuple[int, ...],
    order: tuple[int, ...],
) -> tuple[int, ...]:
    result = [0] * 7
    for old_mask, count in zip(CELL_MASKS, signature):
        new_mask = sum(
            ((old_mask >> old_index) & 1) << new_index
            for new_index, old_index in enumerate(order)
        )
        result[new_mask - 1] = count
    return tuple(result)


def canonical_signature(signature: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        permuted_signature(signature, order)
        for order in permutations(range(3))
    )


def venn_signatures() -> tuple[tuple[int, ...], ...]:
    signatures = set()
    for candidate in product(range(4), repeat=7):
        if any(
            sum(
                candidate[mask - 1]
                for mask in CELL_MASKS
                if mask & (1 << family)
            )
            != 3
            for family in range(3)
        ):
            continue
        if sum(candidate) <= 13:
            signatures.add(canonical_signature(candidate))
    result = tuple(sorted(signatures))
    assert len(result) == 16
    return result


def representative(signature: tuple[int, ...]) -> tuple[frozenset[int], ...]:
    vertices_by_mask: dict[int, tuple[int, ...]] = {}
    next_vertex = 0
    for mask in (1, 3, 5, 7, 2, 4, 6):
        count = signature[mask - 1]
        vertices_by_mask[mask] = tuple(range(next_vertex, next_vertex + count))
        next_vertex += count
    rows = tuple(
        frozenset(
            vertex
            for mask, vertices in vertices_by_mask.items()
            if mask & (1 << family)
            for vertex in vertices
        )
        for family in range(3)
    )
    assert all(len(row) == 3 for row in rows)
    return rows


def vertex_masks(rows: tuple[frozenset[int], ...]) -> tuple[int, ...]:
    return tuple(
        sum((1 << family) if vertex in row else 0 for family, row in enumerate(rows))
        for vertex in VERTICES
    )


def boundaries(masks: tuple[int, ...]) -> tuple[int, ...]:
    result = []
    for mask in masks:
        value = 0
        for family, color in enumerate(COLORS):
            if mask & (1 << family):
                value ^= color
        result.append(value)
    return tuple(result)


def parse_edges(encoded: str) -> tuple[tuple[int, int], ...]:
    edges = []
    for item in encoded.split(","):
        left, right = (int(value) for value in item.split("-"))
        edges.append(tuple(sorted((left, right))))
    return tuple(sorted(edges))


def adjacency(edges: tuple[tuple[int, int], ...]) -> tuple[frozenset[int], ...]:
    result = [set() for _ in VERTICES]
    for left, right in edges:
        result[left].add(right)
        result[right].add(left)
    return tuple(frozenset(neighbours) for neighbours in result)


def reachable(
    start: int,
    graph: tuple[frozenset[int], ...],
    banned: tuple[int, int] | None = None,
) -> frozenset[int]:
    seen = {start}
    stack = [start]
    while stack:
        vertex = stack.pop()
        for neighbour in graph[vertex]:
            if banned is not None and tuple(sorted((vertex, neighbour))) == banned:
                continue
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return frozenset(seen)


def components(graph: tuple[frozenset[int], ...]) -> tuple[frozenset[int], ...]:
    unseen = set(VERTICES)
    result = []
    while unseen:
        component = reachable(min(unseen), graph)
        result.append(component)
        unseen -= component
    return tuple(result)


def xor_on(vertices: frozenset[int], sigma: tuple[int, ...]) -> int:
    value = 0
    for vertex in vertices:
        value ^= sigma[vertex]
    return value


def bridge_boundaries(
    edges: tuple[tuple[int, int], ...],
    graph: tuple[frozenset[int], ...],
    sigma: tuple[int, ...],
) -> tuple[int, ...]:
    result = []
    for edge in edges:
        side = reachable(edge[0], graph, banned=edge)
        if edge[1] not in side:
            result.append(xor_on(side, sigma))
    return tuple(result)


def count_prescribed_colorings(
    edges: tuple[tuple[int, int], ...],
    masks: tuple[int, ...],
) -> int:
    assigned = [0] * len(edges)
    used = [0] * 13
    count = 0

    def search(done: int) -> None:
        nonlocal count
        if done == len(edges):
            count += 1
            return

        best_edge = -1
        best_options: tuple[int, ...] | None = None
        for index, (left, right) in enumerate(edges):
            if assigned[index]:
                continue
            options = tuple(
                color
                for family, color in enumerate(COLORS)
                if not (masks[left] & (1 << family))
                and not (masks[right] & (1 << family))
                and not (used[left] & (1 << color))
                and not (used[right] & (1 << color))
            )
            if best_options is None or len(options) < len(best_options):
                best_edge = index
                best_options = options

        assert best_options is not None
        if not best_options:
            return
        left, right = edges[best_edge]
        for color in best_options:
            assigned[best_edge] = color
            used[left] |= 1 << color
            used[right] |= 1 << color
            search(done + 1)
            used[left] ^= 1 << color
            used[right] ^= 1 << color
            assigned[best_edge] = 0

    search(0)
    return count


def spanning_forest(
    edges: tuple[tuple[int, int], ...],
    graph: tuple[frozenset[int], ...],
) -> tuple[
    tuple[int, ...],
    dict[int, int],
    tuple[tuple[int, int], ...],
    tuple[tuple[int, int], ...],
]:
    roots = []
    parent: dict[int, int] = {}
    order = []
    tree_edges = set()
    seen = set()
    for root in VERTICES:
        if root in seen:
            continue
        roots.append(root)
        seen.add(root)
        parent[root] = root
        stack = [(root, iter(sorted(graph[root])))]
        order.append(root)
        while stack:
            vertex, neighbours = stack[-1]
            try:
                neighbour = next(neighbours)
            except StopIteration:
                stack.pop()
                continue
            if neighbour in seen:
                continue
            seen.add(neighbour)
            parent[neighbour] = vertex
            tree_edges.add(tuple(sorted((vertex, neighbour))))
            order.append(neighbour)
            stack.append((neighbour, iter(sorted(graph[neighbour]))))
    chords = tuple(edge for edge in edges if edge not in tree_edges)
    return tuple(roots), parent, tuple(order), chords


def count_nowhere_zero_boundary_flows(
    edges: tuple[tuple[int, int], ...],
    graph: tuple[frozenset[int], ...],
    sigma: tuple[int, ...],
) -> int:
    roots, parent, order, chords = spanning_forest(edges, graph)
    count = 0
    for chord_values in product(COLORS, repeat=len(chords)):
        residual = list(sigma)
        for (left, right), value in zip(chords, chord_values):
            residual[left] ^= value
            residual[right] ^= value

        valid = True
        for vertex in reversed(order):
            if parent[vertex] == vertex:
                continue
            value = residual[vertex]
            if value == 0:
                valid = False
                break
            residual[parent[vertex]] ^= value
        if valid and all(residual[root] == 0 for root in roots):
            count += 1
    return count


def check_local_boundary_equivalence() -> None:
    for mask in range(8):
        degree = 3 - popcount(mask)
        sigma = boundaries((mask,))[0]
        required = {
            color
            for family, color in enumerate(COLORS)
            if not (mask & (1 << family))
        }
        valid_multisets = {
            tuple(sorted(labels))
            for labels in product(COLORS, repeat=degree)
            if (
                0
                if not labels
                else labels[0]
                if len(labels) == 1
                else labels[0] ^ labels[1]
                if len(labels) == 2
                else labels[0] ^ labels[1] ^ labels[2]
            )
            == sigma
        }
        assert valid_multisets == {tuple(sorted(required))}


def check_unicyclic_minimal_obstruction() -> None:
    tau = (1, 2, 1, 2)
    partial = [0]
    for value in tau[:-1]:
        partial.append(partial[-1] ^ value)
    assert set(partial) == {0, 1, 2, 3}
    assert not any(
        all((start ^ offset) != 0 for offset in partial)
        for start in range(4)
    )


def check_petersen_orbit_zero(
    edges: tuple[tuple[int, int], ...],
    masks: tuple[int, ...],
) -> None:
    active = frozenset(vertex for vertex in VERTICES if masks[vertex] == 0)
    assert len(active) == 10
    active_edges = tuple(edge for edge in edges if edge[0] in active)
    graph = adjacency(edges)
    assert all(len(graph[vertex]) == 3 for vertex in active)

    # Petersen characterization sufficient here: cubic, connected, girth
    # five, ten vertices, and diameter two.
    assert len(reachable(min(active), graph) & active) == 10
    for start in active:
        distances = {start: 0}
        queue = [start]
        while queue:
            vertex = queue.pop(0)
            for neighbour in graph[vertex]:
                if neighbour not in distances:
                    distances[neighbour] = distances[vertex] + 1
                    queue.append(neighbour)
        assert max(distances[vertex] for vertex in active) == 2
    assert len(active_edges) == 15
    for cycle_size in (3, 4):
        assert not any(
            len(choice) == cycle_size
            and sum(
                1
                for edge in active_edges
                if edge[0] in choice and edge[1] in choice
            )
            == cycle_size
            for choice in combinations(active, cycle_size)
        )


def main() -> None:
    check_local_boundary_equivalence()
    check_unicyclic_minimal_obstruction()
    signatures = venn_signatures()
    assert len(EDGE_CERTIFICATES) == len(signatures) == 16

    summaries = []
    for orbit, (signature, encoded_edges) in enumerate(
        zip(signatures, EDGE_CERTIFICATES)
    ):
        rows = representative(signature)
        masks = vertex_masks(rows)
        sigma = boundaries(masks)
        edges = parse_edges(encoded_edges)
        graph = adjacency(edges)

        assert len(edges) == len(set(edges)) == 15
        assert all(left != right for left, right in edges)
        assert all(0 <= left < right < 13 for left, right in edges)
        assert tuple(len(graph[vertex]) for vertex in VERTICES) == tuple(
            3 - popcount(mask) for mask in masks
        )
        assert all(xor_on(component, sigma) == 0 for component in components(graph))
        bridge_values = bridge_boundaries(edges, graph, sigma)
        assert all(value != 0 for value in bridge_values)

        direct_count = count_prescribed_colorings(edges, masks)
        flow_count = count_nowhere_zero_boundary_flows(edges, graph, sigma)
        assert direct_count == flow_count == 0

        if orbit == 0:
            check_petersen_orbit_zero(edges, masks)
        cycle_rank = len(edges) - len(VERTICES) + len(components(graph))
        summaries.append((orbit, len(bridge_values), cycle_rank))

    print("prescribed-colour boundary-flow audit: PASS")
    print("16/16 Venn types have balanced, bridge-admissible uncolourable b-factors")
    print("orbit summaries (orbit, bridges, total cycle rank):", summaries)
    print("remaining gap: choose a colourable b-factor using the ambient residual graph")


if __name__ == "__main__":
    main()

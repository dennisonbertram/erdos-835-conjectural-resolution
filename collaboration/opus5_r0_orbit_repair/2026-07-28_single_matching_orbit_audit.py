#!/usr/bin/env python3
"""Independent audit of Opus 5's single-matching orbit reduction.

For each of the sixteen three-row Venn signatures, fix the first ten-vertex
support S_0.  The pointwise row stabilizer acts as a product of symmetric
groups on the four Venn cells contained in S_0.  This script computes its
orbits on the 945 perfect matchings of S_0 in three independent ways:

1. by the multiset of unordered endpoint-cell labels;
2. by connected components of the explicit generator action graph; and
3. by enumerating loop-multigraph incidence matrices with the prescribed
   four-cell degree vector.

Agreement proves the finite counts used in the proposed 50-case reduction.
It does not prove any of the resulting SAT instances UNSAT.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from itertools import combinations, permutations, product


VENN_SIGNATURES = (
    (0, 0, 0, 0, 0, 0, 3),
    (0, 0, 1, 0, 1, 1, 1),
    (0, 0, 1, 1, 0, 0, 2),
    (0, 0, 2, 1, 1, 1, 0),
    (0, 0, 2, 2, 0, 0, 1),
    (0, 0, 3, 3, 0, 0, 0),
    (0, 1, 1, 1, 1, 0, 1),
    (0, 1, 2, 2, 1, 0, 0),
    (1, 1, 0, 1, 0, 0, 2),
    (1, 1, 1, 1, 1, 1, 0),
    (1, 1, 1, 2, 0, 0, 1),
    (1, 1, 2, 3, 0, 0, 0),
    (1, 2, 1, 2, 1, 0, 0),
    (2, 2, 0, 2, 0, 0, 1),
    (2, 2, 1, 3, 0, 0, 0),
    (3, 3, 0, 3, 0, 0, 0),
)

OPUS_COUNTS = (1, 1, 1, 2, 2, 2, 2, 3, 2, 4, 3, 4, 6, 6, 7, 9)
ROW_INDICES = (0, 1, 2)
CELL_MASKS = tuple(range(1, 8))


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: int, right: int) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1


def transform_mask(mask: int, row_permutation: tuple[int, ...]) -> int:
    return sum(
        ((mask >> old_row) & 1) << row_permutation[old_row]
        for old_row in ROW_INDICES
    )


def transform_signature(
    signature: tuple[int, ...],
    row_permutation: tuple[int, ...],
) -> tuple[int, ...]:
    result = [0] * len(CELL_MASKS)
    for old_mask, count in zip(CELL_MASKS, signature):
        result[transform_mask(old_mask, row_permutation) - 1] = count
    return tuple(result)


def enumerate_venn_signatures() -> tuple[tuple[int, ...], ...]:
    """Derive all row-triple Venn signatures independently."""
    canonical = set()
    for candidate in product(range(4), repeat=len(CELL_MASKS)):
        if sum(candidate) > 13:
            continue
        if any(
            sum(
                candidate[mask - 1]
                for mask in CELL_MASKS
                if mask & (1 << row)
            )
            != 3
            for row in ROW_INDICES
        ):
            continue
        canonical.add(
            min(
                transform_signature(candidate, row_permutation)
                for row_permutation in permutations(ROW_INDICES)
            )
        )
    return tuple(sorted(canonical))


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            result.append(tuple(sorted(((first, second), *tail))))
    return tuple(result)


def cell_degree_vector(signature: tuple[int, ...]) -> tuple[int, int, int, int]:
    """Cell counts in S_0, for masks 0, 2, 4, and 6."""
    n_zero = 13 - sum(signature)
    result = (n_zero, signature[1], signature[3], signature[5])
    assert sum(result) == 10
    return result


def endpoint_cell_invariant(
    matching: tuple[tuple[int, int], ...],
    vertex_labels: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            tuple(sorted((vertex_labels[left], vertex_labels[right])))
            for left, right in matching
        )
    )


def transform_matching(
    matching: tuple[tuple[int, int], ...],
    transposition: tuple[int, int],
) -> tuple[tuple[int, int], ...]:
    left_swap, right_swap = transposition

    def image(vertex: int) -> int:
        if vertex == left_swap:
            return right_swap
        if vertex == right_swap:
            return left_swap
        return vertex

    return tuple(
        sorted(
            tuple(sorted((image(left), image(right))))
            for left, right in matching
        )
    )


def loop_multigraph_count(degrees: tuple[int, int, int, int]) -> int:
    """Count symmetric nonnegative incidence matrices with five edges."""
    edge_types = tuple(combinations(range(4), 2)) + tuple((index, index) for index in range(4))

    @lru_cache(maxsize=None)
    def visit(
        position: int,
        remaining_degrees: tuple[int, int, int, int],
        remaining_edges: int,
    ) -> int:
        if position == len(edge_types):
            return int(remaining_edges == 0 and not any(remaining_degrees))
        if remaining_edges < 0 or sum(remaining_degrees) != 2 * remaining_edges:
            return 0

        left, right = edge_types[position]
        use_left = 2 if left == right else 1
        use_right = 0 if left == right else 1
        maximum = remaining_edges
        maximum = min(maximum, remaining_degrees[left] // use_left)
        if use_right:
            maximum = min(maximum, remaining_degrees[right] // use_right)

        total = 0
        for multiplicity in range(maximum + 1):
            reduced = list(remaining_degrees)
            reduced[left] -= use_left * multiplicity
            if use_right:
                reduced[right] -= use_right * multiplicity
            total += visit(
                position + 1,
                tuple(reduced),
                remaining_edges - multiplicity,
            )
        return total

    return visit(0, degrees, 5)


def audit_orbit(orbit: int, signature: tuple[int, ...]) -> tuple[int, int, int]:
    degrees = cell_degree_vector(signature)
    labels = tuple(
        label
        for label, multiplicity in enumerate(degrees)
        for _ in range(multiplicity)
    )
    assert len(labels) == 10

    matchings = perfect_matchings(tuple(range(10)))
    assert len(matchings) == 945
    index = {matching: item for item, matching in enumerate(matchings)}
    assert len(index) == len(matchings)

    invariant_buckets: dict[tuple[tuple[int, int], ...], list[int]] = defaultdict(list)
    for item, matching in enumerate(matchings):
        invariant_buckets[endpoint_cell_invariant(matching, labels)].append(item)

    generators = []
    start = 0
    for multiplicity in degrees:
        generators.extend((vertex, vertex + 1) for vertex in range(start, start + multiplicity - 1))
        start += multiplicity

    action = DisjointSet(len(matchings))
    for item, matching in enumerate(matchings):
        for generator in generators:
            image = transform_matching(matching, generator)
            action.union(item, index[image])

    invariant_to_roots = {
        invariant: {action.find(item) for item in items}
        for invariant, items in invariant_buckets.items()
    }
    assert all(len(roots) == 1 for roots in invariant_to_roots.values())

    root_to_invariants: dict[int, set[tuple[tuple[int, int], ...]]] = defaultdict(set)
    for invariant, roots in invariant_to_roots.items():
        (root,) = roots
        root_to_invariants[root].add(invariant)
    assert all(len(invariants) == 1 for invariants in root_to_invariants.values())

    invariant_count = len(invariant_buckets)
    action_count = len({action.find(item) for item in range(len(matchings))})
    matrix_count = loop_multigraph_count(degrees)
    assert invariant_count == action_count == matrix_count
    assert invariant_count == OPUS_COUNTS[orbit]
    return invariant_count, action_count, matrix_count


def main() -> None:
    derived_signatures = enumerate_venn_signatures()
    assert len(derived_signatures) == 16
    assert derived_signatures == VENN_SIGNATURES

    totals = []
    print("orbit degrees invariant action loop-matrix")
    for orbit, signature in enumerate(VENN_SIGNATURES):
        counts = audit_orbit(orbit, signature)
        degrees = cell_degree_vector(signature)
        totals.append(counts[0])
        print(orbit, degrees, *counts)

    assert sum(totals[4:]) == 50
    assert sum(totals) == 55
    print(f"open_total={sum(totals[4:])}")
    print(f"all_total={sum(totals)}")
    print("PASS")


if __name__ == "__main__":
    main()

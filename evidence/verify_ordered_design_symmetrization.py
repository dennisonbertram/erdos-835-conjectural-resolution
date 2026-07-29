#!/usr/bin/env python3
"""Finite controls for the ordered-design-to-large-set bridge.

For k=2, an ``LOD(1,2,4)`` is a partition of the directed edges of K_4
into three derangements.  A genuine solution of Problem #835 at k=2 is a
partition of the *undirected* edges into three one-factors.  This exhaustive
four-point calculation checks two facts that are easy to blur together:

* some LODs are support-orbit closed and do yield the usual 3-colouring; and
* simply reading a canonical ordering of a block, or summing its ordered
  colours, does not turn every LOD into such a colouring.

The script is deliberately tiny and standard-library only.  It is a negative
control for proposed symmetrisation formulae; it makes no claim about general
LOD existence.
"""

from __future__ import annotations

from itertools import combinations, permutations


POINTS = tuple(range(4))
ARCS = frozenset((x, y) for x in POINTS for y in POINTS if x != y)
EDGES = tuple(combinations(POINTS, 2))
TRIANGLES = tuple(combinations(POINTS, 3))


def derangements():
    result = []
    for image in permutations(POINTS):
        if any(x == image[x] for x in POINTS):
            continue
        arcs = frozenset((x, image[x]) for x in POINTS)
        assert len(arcs) == 4
        result.append(arcs)
    return tuple(result)


def lods():
    """All unordered partitions of the twelve arcs into 3 derangements."""
    ds = derangements()
    answer = []
    for indices in combinations(range(len(ds)), 3):
        chosen = tuple(ds[index] for index in indices)
        if len(set().union(*chosen)) == 12:
            answer.append(chosen)
    return tuple(answer)


def star_rainbow(edge_colour):
    for triangle in TRIANGLES:
        colours = {
            edge_colour[tuple(sorted((triangle[i], triangle[j])))]
            for i, j in combinations(range(3), 2)
        }
        if len(colours) != 3:
            return False
    return True


def orbit_closed(parts):
    return all(
        any((x, y) in part and (y, x) in part for part in parts)
        for x, y in EDGES
    )


def colours(parts):
    return {
        arc: colour
        for colour, part in enumerate(parts)
        for arc in part
    }


def canonical_colouring(parts):
    directed = colours(parts)
    return {edge: directed[edge] for edge in EDGES}


def ordered_sum_colouring(parts, label):
    """The S_2-invariant colour sum, reduced mod 3, for every edge."""
    directed = colours(parts)
    return {
        edge: (label[directed[edge]] + label[directed[edge[::-1]]]) % 3
        for edge in EDGES
    }


def main():
    all_lods = lods()
    assert len(all_lods) == 4

    closed = [parts for parts in all_lods if orbit_closed(parts)]
    assert len(closed) == 1
    closed_parts = closed[0]
    assert star_rainbow(canonical_colouring(closed_parts))
    assert star_rainbow(ordered_sum_colouring(closed_parts, (0, 1, 2)))

    # A non-orbit-closed LOD for which the sorted-coordinate evaluation fails.
    bad_canonical = next(
        parts for parts in all_lods
        if not orbit_closed(parts) and not star_rainbow(canonical_colouring(parts))
    )
    bad_directed = colours(bad_canonical)
    bad_tri = next(
        triangle for triangle in TRIANGLES
        if len({bad_directed[tuple(sorted(edge))] for edge in combinations(triangle, 2)})
        != 3
    )

    # And, independently, a non-orbit-closed LOD whose colour sum fails for
    # every naming of the three arrays.  This disposes of the most natural
    # ``sum over S_k orderings'' formula already for S_2.
    labels = tuple(permutations((0, 1, 2)))
    bad_sum = next(
        parts for parts in all_lods
        if not orbit_closed(parts)
        and all(not star_rainbow(ordered_sum_colouring(parts, label)) for label in labels)
    )

    print("LOD(1,2,4) exact-cover enumeration: PASS")
    print("  total LODs:", len(all_lods))
    print("  support-orbit-closed LODs:", len(closed))
    print("  closed LOD canonical and ordered-sum colourings: rainbow PASS")
    print("  canonical counterexample parts:", tuple(sorted(part) for part in bad_canonical))
    print("  repeated-colour triangle:", bad_tri)
    print("  ordered-sum counterexample parts:", tuple(sorted(part) for part in bad_sum))
    print("  all 6 array labelings fail the ordered-sum rainbow test: PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independently verify the simultaneous 13-fan induced-shadow audit.

This script proves finite counts and incidence identities for the reduction.
It does not find an LS(3,4,20), a 13-fan, or a colouring of J(32,16).
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
sys.path.insert(0, str(REPO_ROOT / "evidence"))

from verify_defect_cross_link_lsts19 import (  # noqa: E402
    construct_lsts19,
    verify_large_set,
)


POINTS = tuple(range(19))
COLOURS = tuple(range(17))
FAN_LABELS = tuple(range(13))

Triple = tuple[int, int, int]
Quad = tuple[int, int, int, int]
Cell = tuple[Quad, int]
GroupKey = tuple[object, ...]


def require(condition: bool, message: str) -> None:
    """Raise a useful error even when Python assertions are disabled."""
    if not condition:
        raise RuntimeError(message)


def replaced_neighbours(block: tuple[int, ...]) -> set[tuple[int, ...]]:
    """Return all same-size blocks obtained by one point replacement."""
    outside = tuple(point for point in POINTS if point not in block)
    neighbours: set[tuple[int, ...]] = set()
    for dropped in block:
        base = tuple(point for point in block if point != dropped)
        for added in outside:
            neighbours.add(tuple(sorted(base + (added,))))
    return neighbours


def verify_induced_shadow_counts() -> dict[str, int]:
    """Check the two-layer vertex and edge census without constructing edges."""
    triples = tuple(combinations(POINTS, 3))
    quads = tuple(combinations(POINTS, 4))
    triple_set = set(triples)
    quad_set = set(quads)

    require(len(triples) == 969, "wrong number of link vertices")
    require(len(quads) == 3_876, "wrong number of free quadruples")

    for triple in triples:
        neighbours = replaced_neighbours(triple)
        require(len(neighbours) == 48, "wrong link-layer degree")
        require(neighbours <= triple_set, "bad link-layer neighbour")

        supersets = {
            tuple(sorted(triple + (point,))) for point in POINTS if point not in triple
        }
        require(len(supersets) == 16, "wrong link-to-fan incidence")
        require(supersets <= quad_set, "bad link-to-fan quadruple")

    for quad in quads:
        neighbours = replaced_neighbours(quad)
        require(len(neighbours) == 60, "wrong same-label fan degree")
        require(neighbours <= quad_set, "bad fan-layer neighbour")
        require(len(tuple(combinations(quad, 3))) == 4, "wrong face count")

    link_vertices = len(triples)
    fan_vertices = len(FAN_LABELS) * len(quads)
    vertices = link_vertices + fan_vertices

    link_link_edges = link_vertices * 48 // 2
    link_fan_edges = link_vertices * 16 * len(FAN_LABELS)
    same_label_edges = fan_vertices * 60 // 2
    cross_label_edges = len(quads) * comb(len(FAN_LABELS), 2)
    edges = link_link_edges + link_fan_edges + same_label_edges + cross_label_edges

    require(fan_vertices == 50_388, "wrong fan-layer vertex count")
    require(vertices == 51_357, "wrong induced-shadow vertex count")
    require(link_link_edges == 23_256, "wrong link-link edge count")
    require(link_fan_edges == 201_552, "wrong link-fan edge count")
    require(same_label_edges == 1_511_640, "wrong same-label edge count")
    require(cross_label_edges == 302_328, "wrong cross-label edge count")
    require(edges == 2_038_776, "wrong induced-shadow edge count")

    link_degree = 48 + 16 * len(FAN_LABELS)
    fan_degree = 60 + 4 + len(FAN_LABELS) - 1
    degree_sum = link_vertices * link_degree + fan_vertices * fan_degree
    require(link_degree == 256, "wrong total link-layer degree")
    require(fan_degree == 76, "wrong total fan-layer degree")
    require(degree_sum == 2 * edges, "induced-shadow handshake failed")
    require(comb(32, 16) == 601_080_390, "wrong full Johnson count")

    return {
        "vertices": vertices,
        "edges": edges,
        "link_vertices": link_vertices,
        "fan_vertices": fan_vertices,
        "link_degree": link_degree,
        "fan_degree": fan_degree,
    }


def build_fixed_link_groups(
    large_set: dict[Triple, int],
) -> tuple[
    tuple[Cell, ...],
    dict[GroupKey, tuple[int, ...]],
    tuple[tuple[GroupKey, ...], ...],
]:
    """Derive all allowed cells and all exact-cover constraint groups."""
    triples = tuple(combinations(POINTS, 3))
    quads = tuple(combinations(POINTS, 4))

    allowed_by_quad: dict[Quad, tuple[int, ...]] = {}
    cells_list: list[Cell] = []
    for quad in quads:
        face_colours = {large_set[face] for face in combinations(quad, 3)}
        require(len(face_colours) == 4, "quad faces are not rainbow")
        allowed = tuple(colour for colour in COLOURS if colour not in face_colours)
        require(len(allowed) == 13, "quad does not allow 13 colours")
        allowed_by_quad[quad] = allowed
        cells_list.extend((quad, colour) for colour in allowed)

    cells = tuple(cells_list)
    cell_index = {cell: index for index, cell in enumerate(cells)}
    require(len(cell_index) == len(cells), "duplicate allowed cell")
    require(len(cells) == 50_388, "wrong fixed-link vertex count")

    groups: dict[GroupKey, tuple[int, ...]] = {}
    for quad in quads:
        key: GroupKey = ("Q", quad)
        groups[key] = tuple(
            cell_index[(quad, colour)] for colour in allowed_by_quad[quad]
        )

    triple_colour_members: dict[tuple[Triple, int], list[int]] = {
        (triple, colour): []
        for triple in triples
        for colour in COLOURS
        if colour != large_set[triple]
    }
    for index, (quad, colour) in enumerate(cells):
        for triple in combinations(quad, 3):
            require(
                colour != large_set[triple],
                "forbidden face colour entered an allowed cell",
            )
            triple_colour_members[(triple, colour)].append(index)

    for (triple, colour), members in triple_colour_members.items():
        groups[("TC", triple, colour)] = tuple(members)

    q_group_count = len(quads)
    tc_group_count = len(triple_colour_members)
    require(q_group_count == 3_876, "wrong Q-group count")
    require(tc_group_count == 15_504, "wrong (T,c)-group count")
    require(len(groups) == 19_380, "wrong total group count")
    require(
        all(len(members) == 13 for members in groups.values()),
        "a constraint group is not a 13-clique",
    )

    incidence_lists: list[list[GroupKey]] = [[] for _ in range(len(cells))]
    for key, members in groups.items():
        for index in members:
            incidence_lists[index].append(key)

    incidences = tuple(tuple(keys) for keys in incidence_lists)
    require(
        all(len(keys) == 5 for keys in incidences),
        "an allowed cell does not belong to five groups",
    )
    require(
        sum(len(members) for members in groups.values()) == len(cells) * 5,
        "incidence double count failed",
    )
    return cells, groups, incidences


def verify_fixed_link_graph(
    large_set: dict[Triple, int],
) -> dict[str, int]:
    """Check the conflict graph, local Gram overlaps, and Hoffman bounds."""
    cells, groups, incidences = build_fixed_link_groups(large_set)
    group_sets = {key: frozenset(members) for key, members in groups.items()}
    incidence_sets = tuple(frozenset(keys) for keys in incidences)

    degree_sum = 0
    for index, keys in enumerate(incidences):
        for left_key, right_key in combinations(keys, 2):
            overlap = group_sets[left_key] & group_sets[right_key]
            require(
                overlap == {index},
                "two groups through a cell overlap elsewhere",
            )

        neighbours: set[int] = set()
        for key in keys:
            other_members = group_sets[key] - {index}
            require(
                neighbours.isdisjoint(other_members),
                "an edge belongs to two constraint groups",
            )
            neighbours.update(other_members)
        require(len(neighbours) == 60, "fixed-link degree is not 60")
        degree_sum += len(neighbours)

    # This exhausts every nonzero off-diagonal entry of B^T B: a shared
    # row is one of these group pairs, and every such pair shares only it.
    checked_group_pairs = 0
    for key, members in group_sets.items():
        for left, right in combinations(members, 2):
            common_rows = incidence_sets[left] & incidence_sets[right]
            require(
                common_rows == {key},
                "off-diagonal Gram entry is not the adjacency entry",
            )
            checked_group_pairs += 1

    vertices = len(cells)
    degree = 60
    edges_by_groups = sum(comb(len(members), 2) for members in groups.values())
    edges_by_degrees = degree_sum // 2
    require(vertices == 50_388, "wrong fixed-link graph order")
    require(checked_group_pairs == 1_511_640, "wrong pair audit count")
    require(edges_by_groups == 1_511_640, "wrong group edge count")
    require(edges_by_degrees == 1_511_640, "wrong degree edge count")

    row_count = len(groups)
    nullity_lower_bound = vertices - row_count
    least_eigenvalue = -5
    chromatic_bound = Fraction(1) - Fraction(degree, least_eigenvalue)
    independence_bound = Fraction(vertices * -least_eigenvalue) / Fraction(
        degree - least_eigenvalue
    )

    require(row_count == 19_380, "wrong incidence-matrix row count")
    require(nullity_lower_bound == 31_008, "wrong kernel lower bound")
    require(chromatic_bound == 13, "wrong Hoffman chromatic bound")
    require(independence_bound == 3_876, "wrong Hoffman alpha bound")

    return {
        "vertices": vertices,
        "edges": edges_by_groups,
        "degree": degree,
        "groups": row_count,
        "q_groups": comb(19, 4),
        "triple_colour_groups": comb(19, 3) * 16,
        "nullity_lower_bound": nullity_lower_bound,
        "least_eigenvalue": least_eigenvalue,
        "hoffman_chromatic_bound": int(chromatic_bound),
        "hoffman_independence_bound": int(independence_bound),
    }


def main() -> None:
    """Reconstruct the certificate and run every independent audit."""
    large_set = construct_lsts19()
    verify_large_set(large_set)
    require(len(large_set) == comb(19, 3), "cyclic certificate incomplete")
    require(set(large_set.values()) == set(COLOURS), "wrong palette")

    shadow = verify_induced_shadow_counts()
    fixed_link = verify_fixed_link_graph(large_set)

    print("PASS: reconstructed and verified the cyclic LS(2,3,19)")
    print(
        "PASS: induced shadow",
        f"{shadow['vertices']:,} vertices,",
        f"{shadow['edges']:,} edges,",
        f"layer degrees {shadow['link_degree']} and {shadow['fan_degree']}",
    )
    print(
        "PASS: fixed-link H_L",
        f"{fixed_link['vertices']:,} vertices,",
        f"{fixed_link['edges']:,} edges,",
        f"degree {fixed_link['degree']}",
    )
    print(
        "PASS: groups",
        f"{fixed_link['q_groups']:,} Q +",
        f"{fixed_link['triple_colour_groups']:,} (T,c) =",
        f"{fixed_link['groups']:,}",
    )
    print(
        "PASS: local overlaps certify A = B^T B - 5I;",
        "lambda_min = -5 and nullity >=",
        f"{fixed_link['nullity_lower_bound']:,}",
    )
    print(
        "PASS: exact Hoffman bounds",
        f"chi >= {fixed_link['hoffman_chromatic_bound']},",
        f"alpha <= {fixed_link['hoffman_independence_bound']:,}",
    )
    print(
        "SCOPE: no LS(3,4,20), 13-fan, or full J(32,16) colouring",
        "is constructed; existence and broader spectral obstructions remain open.",
    )


if __name__ == "__main__":
    main()

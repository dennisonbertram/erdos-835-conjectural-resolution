#!/usr/bin/env python3
"""Exact finite census of the non-simple branches for support orbit 2.

For an orbit-2 factor H, vertex 0 has degree one, vertex 3 has degree two,
and vertices 4,...,12 have degree three.  Delete vertex 0 and call its
neighbour x.

* If x=3, the ten-vertex core has degree sequence (1,3^9).
* If x!=3, the core has degree sequence (2,2,3^8), with distinguished
  degree-two vertices (3,x).  When they are adjacent, completing the core
  by a second 3x edge gives the doubled-root branch.

The graph6 lists below are the complete unlabeled outputs selected from

    nauty 2.8.9 geng -cq -d1D3 10 14:14

by those two degree tests.  The script independently checks every degree
condition, audits whether swapping the two roots is an automorphism, builds
all directed-root types, and tests prescribed colourability.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path


LEAF_AT_THREE = (
    "I?BFE_wL?",
    "I?BDf?[[?",
    "I?BDd`K[?",
    "I?BDeOkY?",
    "I?BEL_w[?",
    "I?BDM_w[?",
    "I?BDKpo[?",
    "I?`FBOsb?",
    "I?`FAqcJ?",
    "I?`DeOkX?",
    "I?`EV?sJ?",
    "I?`DU`SF?",
    "I?`DU_kX?",
    "I?`DUOsX?",
    "I?`DTPSX?",
    "I?bBDHWI_",
    "I?bBBIWI_",
    "I?aJEOsW_",
    "I?aJEOqX?",
)

DOUBLED_ROOT = (
    "I?B@t`ge?",
    "I?B@pr_e?",
    "I?`DeGwM?",
    "I?b@f@WJ?",
    "I?b@f@WF?",
    "I?b@b_wQ_",
    "I?b@ePoJ?",
    "I?b@eOwX?",
    "I?b@dHWU?",
    "I?b@bCwe?",
    "I?b@bCwU?",
    "I?b@`dgU?",
    "I?`bCqWT?",
    "I?`ad_wb?",
    "I?`adQoF?",
    "I?`adQWX?",
    "I?`adQWL?",
    "I?`adGwq?",
    "I?`adGwe?",
    "I?`a`jGK_",
    "I?`a`iI[?",
    "I?aJCpoT?",
    "ICOcePcJ?",
)


def load_switch_module():
    path = Path(__file__).with_name("2026-07-28_orbit2_switch_cegis.py")
    spec = importlib.util.spec_from_file_location("orbit2_switch", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load switch module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SWITCH = load_switch_module()


def decode_graph6(encoded: str) -> tuple[tuple[int, int], ...]:
    n = ord(encoded[0]) - 63
    assert n == 10
    bits = "".join(f"{ord(character) - 63:06b}" for character in encoded[1:])
    edges = []
    position = 0
    for right in range(1, n):
        for left in range(right):
            if bits[position] == "1":
                edges.append((left, right))
            position += 1
    return tuple(edges)


def degrees(edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    return tuple(sum(vertex in edge for edge in edges) for vertex in range(10))


def has_root_swap(
    edges: tuple[tuple[int, int], ...],
    left: int,
    right: int,
) -> bool:
    edge_set = frozenset(edges)
    cubic = tuple(vertex for vertex in range(10) if vertex not in (left, right))
    for images in itertools.permutations(cubic):
        permutation = {left: right, right: left}
        permutation.update(zip(cubic, images))
        image = frozenset(
            tuple(sorted((permutation[u], permutation[v]))) for u, v in edges
        )
        if image == edge_set:
            return True
    return False


def factor_from_core(
    encoded: str,
    role_three: int,
    role_leaf_neighbour: int,
) -> frozenset[tuple[int, int]]:
    edges = decode_graph6(encoded)
    other = [
        vertex
        for vertex in range(10)
        if vertex not in (role_three, role_leaf_neighbour)
    ]
    relabel = {role_three: 3, role_leaf_neighbour: 4}
    relabel.update({
        vertex: image for vertex, image in zip(other, range(5, 13))
    })
    core = {
        tuple(sorted((relabel[left], relabel[right])))
        for left, right in edges
    }
    return frozenset(core | {(0, 4)})


def census_records() -> tuple[dict[str, int], list[dict[str, object]]]:
    records = []
    for index, encoded in enumerate(LEAF_AT_THREE):
        edges = decode_graph6(encoded)
        degree = degrees(edges)
        assert sorted(degree) == [1] + [3] * 9
        role_three = degree.index(1)
        other = [vertex for vertex in range(10) if vertex != role_three]
        relabel = {role_three: 3}
        relabel.update({
            vertex: image for vertex, image in zip(other, range(4, 13))
        })
        factor = frozenset(
            {
                tuple(sorted((relabel[left], relabel[right])))
                for left, right in edges
            }
            | {(0, 3)}
        )
        assert not SWITCH.colourable(factor)
        records.append({
            "case": f"edge03_{index:02d}",
            "branch": "edge03",
            "graph6": encoded,
            "root": [role_three, role_three],
            "colourable": False,
            "factor": sorted(factor),
        })

    directed_count = 0
    uncolourable_count = 0
    for index, encoded in enumerate(DOUBLED_ROOT):
        edges = decode_graph6(encoded)
        degree = degrees(edges)
        assert sorted(degree) == [2, 2] + [3] * 8
        roots = tuple(vertex for vertex, value in enumerate(degree) if value == 2)
        assert len(roots) == 2 and tuple(sorted(roots)) in edges
        orientations = (roots,) if has_root_swap(edges, *roots) else (roots, roots[::-1])
        for orientation_index, (role_three, role_leaf_neighbour) in enumerate(
            orientations
        ):
            factor = factor_from_core(
                encoded,
                role_three,
                role_leaf_neighbour,
            )
            colourable = SWITCH.colourable(factor)
            directed_count += 1
            uncolourable_count += not colourable
            records.append({
                "case": f"double_{index:02d}_{orientation_index}",
                "branch": "double",
                "graph6": encoded,
                "root": [role_three, role_leaf_neighbour],
                "root_swap_automorphism": len(orientations) == 1,
                "colourable": colourable,
                "factor": sorted(factor),
            })

    summary = {
        "leaf_at_three_unlabeled": len(LEAF_AT_THREE),
        "double_unlabeled": len(DOUBLED_ROOT),
        "double_directed_root_types": directed_count,
        "double_uncolourable_directed_root_types": uncolourable_count,
    }
    return summary, records


def main() -> None:
    summary, records = census_records()
    print(json.dumps(summary, sort_keys=True))
    for record in records:
        print(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()

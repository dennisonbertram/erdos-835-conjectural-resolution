#!/usr/bin/env python3
"""Verify row-sum elimination of the 333, 55, and 37 r=0 cores.

This is an exact finite audit at the seven-prefix frontier.  It does not
prove that the four remaining Tutte-core types cannot block all seven
remaining size-ten supports.
"""

from __future__ import annotations

from itertools import combinations

import verify_r0_core_pairs as pairs


ALL_VERTICES = (1 << 13) - 1
CORE_DATA = {
    "37": (10, 21),
    "55": (10, 25),
    "333": (9, 27),
    "5111": (8, 18),
    "3311": (8, 22),
    "31111": (7, 18),
    "6": (6, 15),
}


def core_vertices(edges: int) -> int:
    return sum(
        1 << vertex
        for vertex in pairs.VERTICES
        if edges & pairs.INCIDENT[vertex]
    )


def sharp_reuse_ceiling(order: int, edges: int) -> int:
    outside = 13 - order
    extra_edges = 31 - edges
    forced_to_touch_core = max(
        0, extra_edges - outside * (outside - 1) // 2
    )
    capacity = (
        36 + 2 * order - 2 * edges - forced_to_touch_core
    )
    return max(0, capacity // 3)


def passes_prefix_screens(edges: int) -> bool:
    edge_count = edges.bit_count()
    if edge_count > 31:
        return False
    degrees = [
        (edges & pairs.INCIDENT[vertex]).bit_count()
        for vertex in pairs.VERTICES
    ]
    if max(degrees) > 7:
        return False
    deficit = sum(max(0, 2 - degree) for degree in degrees)
    if edge_count + (deficit + 1) // 2 > 31:
        return False
    if edge_count >= 29 and any(
        (edges & clique).bit_count() > 28
        for clique in pairs.NINE_CLIQUES
    ):
        return False
    return True


def verify_55_elimination(cores: dict[str, list[int]]) -> None:
    fixed = cores["55"][0]
    outside = ALL_VERTICES ^ core_vertices(fixed)
    assert outside.bit_count() == 3
    survivors = []
    for second in cores["5111"]:
        union = fixed | second
        if passes_prefix_screens(union):
            survivors.append(union)
    assert len(survivors) == 20
    for union in survivors:
        assert union.bit_count() == 28
        outside_degrees = [
            (union & pairs.INCIDENT[vertex]).bit_count()
            for vertex in pairs.VERTICES
            if outside >> vertex & 1
        ]
        assert outside_degrees == [0, 0, 0]
        # A support blocked by the 10-vertex 55 core has this exact outside
        # triple as its complement.  Thus d_F(v)-2 >= 1, or d_F(v) >= 3,
        # on all three vertices.  The remaining three F edges provide at
        # most six of the nine required degree endpoints.
        required_endpoints = sum(3 - degree for degree in outside_degrees)
        available_endpoints = 2 * (31 - union.bit_count())
        assert required_endpoints == 9 > available_endpoints == 6


def verify_37_elimination(cores: dict[str, list[int]]) -> None:
    fixed = cores["37"][0]
    allowed_kinds = ("37", "5111", "3311", "31111")
    survivors = {
        kind: [
            second
            for second in cores[kind]
            if second != fixed and passes_prefix_screens(fixed | second)
        ]
        for kind in allowed_kinds
    }
    assert {kind: len(values) for kind, values in survivors.items()} == {
        "37": 9,
        "5111": 105,
        "3311": 210,
        "31111": 35,
    }

    labelled = [
        (kind, core)
        for kind in allowed_kinds
        for core in survivors[kind]
    ]
    triple_types = []
    for index, (first_kind, first_core) in enumerate(labelled):
        for second_kind, second_core in labelled[index + 1 :]:
            if first_core == second_core:
                continue
            union = fixed | first_core | second_core
            if passes_prefix_screens(union):
                triple_types.append(
                    tuple(sorted(("37", first_kind, second_kind)))
                )
    assert len(triple_types) == 9
    assert set(triple_types) == {("37", "37", "37")}

    four_core_families = []
    for chosen in combinations(survivors["37"], 3):
        union = fixed
        for core in chosen:
            union |= core
        if passes_prefix_screens(union):
            four_core_families.append((fixed,) + chosen)
    assert len(four_core_families) == 3
    assert all(
        (first | second | third | fourth).bit_count() == 28
        for first, second, third, fourth in four_core_families
    )
    assert not any(
        passes_prefix_screens(
            fixed | first | second | third | fourth
        )
        for first, second, third, fourth in combinations(
            survivors["37"], 4
        )
    )

    graph_count = 0
    reuse_cases = 0
    residual_capacity_cases = 0
    for family in four_core_families:
        union = 0
        for core in family:
            union |= core
        nonedges = [
            index for index in range(78) if not (union >> index & 1)
        ]
        for additions in combinations(nonedges, 3):
            graph = union
            for index in additions:
                graph |= 1 << index
            degrees = [
                (graph & pairs.INCIDENT[vertex]).bit_count()
                for vertex in pairs.VERTICES
            ]
            if min(degrees) < 2 or max(degrees) > 7:
                continue
            graph_count += 1
            capacities = [degree - 2 for degree in degrees]
            outside_triples = [
                ALL_VERTICES ^ core_vertices(core) for core in family
            ]
            assert all(mask.bit_count() == 3 for mask in outside_triples)
            for reused_once in range(4):
                multiplicities = [2, 2, 2, 2]
                multiplicities[reused_once] = 1
                large_incidence = [
                    sum(
                        multiplicity
                        for mask, multiplicity in zip(
                            outside_triples, multiplicities
                        )
                        if mask >> vertex & 1
                    )
                    for vertex in pairs.VERTICES
                ]
                residual = [
                    capacity - used
                    for capacity, used in zip(
                        capacities, large_incidence
                    )
                ]
                reuse_cases += 1
                # The residual vector would have to be the column-degree
                # sequence of the three remaining five-set complements:
                # every entry in [0,3] and total 15.  No case even reaches
                # these necessary bounds.
                if (
                    min(residual) >= 0
                    and max(residual) <= 3
                    and sum(residual) == 15
                ):
                    residual_capacity_cases += 1

    assert graph_count == 147
    assert reuse_cases == 588
    assert residual_capacity_cases == 0


def main() -> None:
    ceilings = {
        kind: sharp_reuse_ceiling(order, edges)
        for kind, (order, edges) in CORE_DATA.items()
    }
    assert ceilings == {
        "37": 2,
        "55": 1,
        "333": 0,
        "5111": 4,
        "3311": 2,
        "31111": 4,
        "6": 6,
    }
    print("PASS edge-placement row-sum ceilings:", ceilings)
    print("PASS 333 cannot obstruct even one remaining size-10 support")

    cores = {kind: pairs.embeddings(kind) for kind in pairs.KINDS}
    verify_55_elimination(cores)
    print("PASS all 20 compatible 55+5111 embeddings fail outside row sums")

    verify_37_elimination(cores)
    print("PASS exact 37 pair/triple/four-core compatibility reduction")
    print("PASS 147 degree-valid F graphs and 588 reuse cases exhausted")
    print("PASS no 37-family case satisfies remaining complement row sums")
    print("SCOPE: eliminates 333, 55, and 37 cores only;")
    print("       the four surviving r=0 core types remain unresolved.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exhaust the r=0 obstruction-core pairs under exact necessary screens."""

from itertools import combinations


N = 13
VERTICES = tuple(range(N))
KINDS = ("37", "55", "333", "5111", "3311", "31111", "6")

try:
    popcount = int.bit_count
except AttributeError:

    def popcount(value: int) -> int:
        return bin(value).count("1")


EDGE_ID = {
    edge: index
    for index, edge in enumerate(combinations(VERTICES, 2))
}
INCIDENT = [0] * N
for edge, index in EDGE_ID.items():
    bit = 1 << index
    for vertex in edge:
        INCIDENT[vertex] |= bit

CLIQUE = [0] * (1 << N)
for mask in range(1 << N):
    edge_mask = 0
    vertices = [v for v in VERTICES if mask >> v & 1]
    for edge in combinations(vertices, 2):
        edge_mask |= 1 << EDGE_ID[edge]
    CLIQUE[mask] = edge_mask

NINE_CLIQUES = [
    CLIQUE[sum(1 << vertex for vertex in subset)]
    for subset in combinations(VERTICES, 9)
]


def vertex_mask(vertices: object) -> int:
    return sum(1 << vertex for vertex in vertices)


def core_mask(blocks: tuple[object, ...]) -> int:
    whole = 0
    inside = 0
    for block in blocks:
        mask = vertex_mask(block)
        whole |= mask
        inside |= CLIQUE[mask]
    return CLIQUE[whole] ^ inside


def embeddings(kind: str) -> list[int]:
    out = []
    if kind == "37":
        for whole in combinations(VERTICES, 10):
            for small_tuple in combinations(whole, 3):
                small = set(small_tuple)
                out.append(core_mask((small, set(whole) - small)))
    elif kind == "55":
        for whole in combinations(VERTICES, 10):
            anchor = whole[0]
            for rest in combinations(whole[1:], 4):
                first = {anchor, *rest}
                out.append(core_mask((first, set(whole) - first)))
    elif kind == "333":
        for whole in combinations(VERTICES, 9):
            anchor = whole[0]
            for rest in combinations(whole[1:], 2):
                first = {anchor, *rest}
                remaining = tuple(v for v in whole if v not in first)
                anchor_two = remaining[0]
                for rest_two in combinations(remaining[1:], 2):
                    second = {anchor_two, *rest_two}
                    out.append(
                        core_mask((first, second, set(remaining) - second))
                    )
    elif kind == "5111":
        for whole in combinations(VERTICES, 8):
            for large_tuple in combinations(whole, 5):
                large = set(large_tuple)
                singletons = tuple({v} for v in set(whole) - large)
                out.append(core_mask((large, *singletons)))
    elif kind == "3311":
        for whole in combinations(VERTICES, 8):
            for singles in combinations(whole, 2):
                remaining = tuple(v for v in whole if v not in singles)
                anchor = remaining[0]
                for rest in combinations(remaining[1:], 2):
                    first = {anchor, *rest}
                    second = set(remaining) - first
                    out.append(
                        core_mask(
                            (first, second, {singles[0]}, {singles[1]})
                        )
                    )
    elif kind == "31111":
        for whole in combinations(VERTICES, 7):
            for large_tuple in combinations(whole, 3):
                large = set(large_tuple)
                singletons = tuple({v} for v in set(whole) - large)
                out.append(core_mask((large, *singletons)))
    elif kind == "6":
        for whole in combinations(VERTICES, 6):
            out.append(CLIQUE[vertex_mask(whole)])
    else:
        raise ValueError(kind)

    assert len(out) == len(set(out))
    return out


def pair_table(cores: dict[str, list[int]]) -> dict[tuple[str, str], object]:
    table = {}
    for first_index, first_kind in enumerate(KINDS):
        first = cores[first_kind][0]
        for second_kind in KINDS[first_index:]:
            best = None
            witnesses = 0
            for second in cores[second_kind]:
                if first_kind == second_kind and first == second:
                    continue
                union = first | second
                union_edges = popcount(union)
                if union_edges > 31:
                    continue
                degrees = [
                    popcount(union & INCIDENT[vertex])
                    for vertex in VERTICES
                ]
                if max(degrees) > 7:
                    continue
                deficit = sum(max(0, 2 - degree) for degree in degrees)
                if union_edges + (deficit + 1) // 2 > 31:
                    continue

                new_edges = popcount(second & ~first)
                candidate = (new_edges, union_edges)
                if best is not None and candidate > best:
                    continue
                if union_edges >= 29 and any(
                    popcount(union & clique) > 28
                    for clique in NINE_CLIQUES
                ):
                    continue
                if best is None or candidate < best:
                    best = candidate
                    witnesses = 1
                elif candidate == best:
                    witnesses += 1
            table[(first_kind, second_kind)] = (
                None if best is None else (*best, witnesses)
            )
    return table


def main() -> None:
    cores = {kind: embeddings(kind) for kind in KINDS}
    assert {kind: len(values) for kind, values in cores.items()} == {
        "37": 34320,
        "55": 36036,
        "333": 200200,
        "5111": 72072,
        "3311": 360360,
        "31111": 60060,
        "6": 1716,
    }

    expected = {
        ("37", "37"): (7, 28, 9),
        ("37", "55"): None,
        ("37", "333"): None,
        ("37", "5111"): (9, 30, 105),
        ("37", "3311"): (7, 28, 210),
        ("37", "31111"): (6, 27, 35),
        ("37", "6"): None,
        ("55", "55"): None,
        ("55", "333"): None,
        ("55", "5111"): (3, 28, 20),
        ("55", "3311"): None,
        ("55", "31111"): None,
        ("55", "6"): None,
        ("333", "333"): None,
        ("333", "5111"): None,
        ("333", "3311"): None,
        ("333", "31111"): None,
        ("333", "6"): None,
        ("5111", "5111"): (4, 22, 15),
        ("5111", "3311"): (6, 24, 30),
        ("5111", "31111"): (3, 21, 20),
        ("5111", "6"): (3, 21, 10),
        ("3311", "3311"): (2, 24, 12),
        ("3311", "31111"): (1, 23, 6),
        ("3311", "6"): (2, 24, 9),
        ("31111", "31111"): (2, 20, 12),
        ("31111", "6"): (1, 19, 3),
        ("6", "6"): (5, 20, 42),
    }
    assert pair_table(cores) == expected

    # Structural sharpening of the only possible K55 partner.  The
    # canonical K55 uses vertices 0,...,9; every surviving K5111 partner
    # merely adds a triangle within one side and leaves 10,11,12 isolated.
    first_55 = cores["55"][0]
    outside = [
        vertex
        for vertex in VERTICES
        if popcount(first_55 & INCIDENT[vertex]) == 0
    ]
    assert outside == [10, 11, 12]
    survivors = []
    for second in cores["5111"]:
        union = first_55 | second
        union_edges = popcount(union)
        if union_edges > 31:
            continue
        degrees = [
            popcount(union & INCIDENT[vertex])
            for vertex in VERTICES
        ]
        if max(degrees) > 7:
            continue
        deficit = sum(max(0, 2 - degree) for degree in degrees)
        if union_edges + (deficit + 1) // 2 > 31:
            continue
        if union_edges >= 29 and any(
            popcount(union & clique) > 28
            for clique in NINE_CLIQUES
        ):
            continue
        survivors.append(union)
    assert len(survivors) == 20
    assert all(popcount(union) == 28 for union in survivors)
    assert all(
        all(popcount(union & INCIDENT[vertex]) == 0 for vertex in outside)
        for union in survivors
    )
    assert all(
        popcount(union & ~first_55) == 3
        and all(
            popcount((union & ~first_55) & INCIDENT[vertex]) in (0, 2)
            for vertex in VERTICES
        )
        for union in survivors
    )
    assert 2 * (31 - 28) < 3 * 3

    print("PASS generated all 764,764 labelled cores of the seven types")
    print("PASS exhausted every pair orbit after fixing the first core")
    print("PASS enforced |E|<=31, Delta<=7, delta-extension, and capacity")
    print("PASS exact minimum-new-edge table matches the note")
    print("PASS K5,5 partners are same-support triangles, so none can be used")
    print("SCOPE: necessary pair screen; eighth-colour packing remains open")


if __name__ == "__main__":
    main()

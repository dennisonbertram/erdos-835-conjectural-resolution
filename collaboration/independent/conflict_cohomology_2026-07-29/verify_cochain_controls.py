#!/usr/bin/env python3
"""Exact finite controls for the F_2 cochain reformulation of the tail test.

This script does not prove Erdős--Rosenfeld #835.  It checks:

1. A genuine positive control: after deleting five classes from an
   LS(2,3,9), the all-one vector on the deleted triples lies in the row space
   of the 4-set-versus-deleted-triple incidence matrix.
2. A genuine negative *fixed-partial* control: the authenticated
   Etzion--Hartman 15-system partial at (t,v,p)=(3,20,17) has a three-edge
   residual cycle.  Its coboundary is an explicit odd 45-block cocycle
   supported on the deleted systems, so the corresponding all-one vector is
   not in the row space.

Only Python's standard library and exact integer/F_2 operations are used.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path


EXPECTED_EH_SHA256 = (
    "06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78"
)
EXPECTED_COMPLETE_COLOURS = tuple(range(1, 13)) + (14, 15, 16)
EH_CYCLE_TSETS = (
    frozenset((0, 14, 17)),
    frozenset((5, 14, 17)),
    frozenset((2, 14, 17)),
)

CHECKS = 0


def check(condition: bool, label: str) -> None:
    global CHECKS
    if not condition:
        raise AssertionError(label)
    CHECKS += 1
    print(f"[ok] {label}")


def is_steiner(blocks, t: int, v: int) -> bool:
    blocks = tuple(blocks)
    counts = Counter(
        sub
        for block in blocks
        for sub in combinations(sorted(block), t)
    )
    return (
        len(blocks) == comb(v, t) // (t + 1)
        and len(counts) == comb(v, t)
        and set(counts.values()) == {1}
    )


def all_sts9():
    """Enumerate every labelled STS(9) by exact cover on pairs."""
    triples = tuple(frozenset(c) for c in combinations(range(9), 3))
    pairs = tuple(frozenset(c) for c in combinations(range(9), 2))
    by_pair = {pair: tuple(block for block in triples if pair <= block) for pair in pairs}
    output = []
    chosen = []

    def recurse(uncovered):
        if not uncovered:
            output.append(frozenset(chosen))
            return
        pair = min(uncovered, key=lambda item: tuple(sorted(item)))
        for block in by_pair[pair]:
            facets = tuple(
                frozenset(c) for c in combinations(sorted(block), 2)
            )
            if any(facet not in uncovered for facet in facets):
                continue
            chosen.append(block)
            recurse(uncovered.difference(facets))
            chosen.pop()

    recurse(frozenset(pairs))
    return tuple(output)


def first_large_set_sts9():
    systems = all_sts9()
    check(len(systems) == 840, "enumerated all 840 labelled STS(9)")
    chosen = []

    def recurse(start: int, used) -> bool:
        if len(chosen) == 7:
            return True
        for index in range(start, len(systems)):
            system = systems[index]
            if system & used:
                continue
            chosen.append(system)
            if recurse(index + 1, used | system):
                return True
            chosen.pop()
        return False

    check(recurse(0, frozenset()), "found seven pairwise block-disjoint STS(9)")
    return tuple(chosen)


def rowspace_witness(rows: tuple[int, ...], target: int):
    """Return (rank, selected-row mask) with XOR(selected rows)=target, or None."""
    basis = {}
    for row_index, original in enumerate(rows):
        value = original
        combination = 1 << row_index
        while value:
            pivot = value.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = (value, combination)
                break
            other, other_combination = basis[pivot]
            value ^= other
            combination ^= other_combination

    value = target
    combination = 0
    while value:
        pivot = value.bit_length() - 1
        if pivot not in basis:
            return len(basis), None
        other, other_combination = basis[pivot]
        value ^= other
        combination ^= other_combination
    return len(basis), combination


def positive_ls239_control() -> None:
    print("== Positive control: LS(2,3,9) ==")
    large_set = first_large_set_sts9()
    check(
        all(is_steiner(system, 2, 9) for system in large_set),
        "all seven classes are S(2,3,9)",
    )
    all_blocks = frozenset().union(*large_set)
    check(
        len(all_blocks) == comb(9, 3) == 84,
        "the seven classes partition all 84 triples",
    )

    deleted = frozenset().union(*large_set[:5])
    residual0, residual1 = large_set[5], large_set[6]
    residual = residual0 | residual1
    check(
        (len(deleted), len(residual)) == (60, 24),
        "deleting five systems leaves exactly two 12-block systems",
    )

    residual_blocks = tuple(
        sorted(residual, key=lambda block: tuple(sorted(block)))
    )
    residual_index = {block: index for index, block in enumerate(residual_blocks)}
    adjacency = [set() for _ in residual_blocks]
    all_edges_cross = True
    for pair in combinations(range(9), 2):
        pair_set = frozenset(pair)
        above = [block for block in residual if pair_set <= block]
        all_edges_cross &= (
            len(above) == 2
            and sum(block in residual1 for block in above) == 1
        )
        left, right = map(residual_index.__getitem__, above)
        adjacency[left].add(right)
        adjacency[right].add(left)
    check(
        all_edges_cross,
        "all 36 residual edges cross the two final systems",
    )
    seen = set()
    components = 0
    for start in range(len(residual_blocks)):
        if start in seen:
            continue
        components += 1
        stack = [start]
        while stack:
            vertex = stack.pop()
            if vertex in seen:
                continue
            seen.add(vertex)
            stack.extend(adjacency[vertex] - seen)
    check(components == 1, "the LS(2,3,9) residual graph is connected")

    columns = tuple(sorted(deleted, key=lambda block: tuple(sorted(block))))
    column_index = {block: index for index, block in enumerate(columns)}
    faces = tuple(frozenset(face) for face in combinations(range(9), 4))
    rows = tuple(
        sum(
            1 << column_index[block]
            for block in columns
            if block <= face
        )
        for face in faces
    )
    rank, witness = rowspace_witness(rows, (1 << len(columns)) - 1)
    check(witness is not None, "one-vector is in the 4-set/deleted-triple row space")
    selected_rows = tuple(
        index for index in range(len(rows)) if (witness >> index) & 1
    )
    reconstructed = 0
    for index in selected_rows:
        reconstructed ^= rows[index]
    check(
        reconstructed == (1 << len(columns)) - 1,
        "the explicit row combination covers every deleted triple oddly",
    )
    check(
        rank == comb(8, 3) - components == 55,
        "rank formula rank(M)=C(8,3)-components gives 55",
    )
    print(
        "positive-control census:"
        f" matrix={len(faces)}x{len(columns)}, rank={rank},"
        f" witness_rows={len(selected_rows)}"
    )


def load_eh_partial(path: Path):
    check(
        sha256(path.read_bytes()).hexdigest() == EXPECTED_EH_SHA256,
        "Etzion--Hartman partial has the authenticated SHA-256",
    )
    rows = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fields = tuple(map(int, raw.split()))
        if len(fields) != 5:
            raise AssertionError(f"EH line {line_number} does not have five integers")
        block = tuple(fields[:4])
        colour = fields[4]
        if tuple(sorted(block)) != block or len(set(block)) != 4:
            raise AssertionError(f"invalid EH block on line {line_number}")
        rows.append((frozenset(block), colour))
    check(len(rows) == comb(20, 4), "EH partial contains every 4-set exactly once")
    check(
        tuple(block for block, _ in rows)
        == tuple(frozenset(block) for block in combinations(range(20), 4)),
        "EH blocks are in exact lexicographic order",
    )
    counts = Counter(colour for _, colour in rows if colour >= 0)
    complete = tuple(sorted(colour for colour, count in counts.items() if count == 285))
    check(
        complete == EXPECTED_COMPLETE_COLOURS,
        "EH complete colours are exactly 1..12,14,15,16",
    )
    return rows, frozenset(complete)


def negative_eh_control(root: Path) -> None:
    print()
    print("== Negative fixed-partial control: EH residual triangle ==")
    path = root / "collaboration/ls3420_branch0_search/eh15_branch0_partial.txt"
    rows, complete_colours = load_eh_partial(path)
    deleted = frozenset(block for block, colour in rows if colour in complete_colours)
    residual = frozenset(block for block, colour in rows if colour not in complete_colours)
    check(
        (len(deleted), len(residual)) == (4_275, 570),
        "EH fifteen systems delete 4,275 blocks and leave 570",
    )
    check(
        all(
            is_steiner(
                (block for block, value in rows if value == colour),
                3,
                20,
            )
            for colour in complete_colours
        ),
        "all fifteen authenticated complete colours are S(3,4,20)",
    )

    z = frozenset(EH_CYCLE_TSETS)
    check(len(z) == 3, "the residual cycle cochain z has odd weight three")
    check(
        all(sum(triple <= block for triple in z) % 2 == 0 for block in residual),
        "H_E^T z=0 on every residual block",
    )

    all_four_sets = tuple(frozenset(block) for block in combinations(range(20), 4))
    y = frozenset(
        block
        for block in all_four_sets
        if sum(triple <= block for triple in z) % 2
    )
    check(len(y) == 45, "the coboundary y=delta z has odd weight 45")
    check(y <= deleted, "the 45-block coboundary is supported on deleted systems")
    check(
        all(
            sum(block <= face for block in y) % 2 == 0
            for face in map(frozenset, combinations(range(20), 5))
        ),
        "delta y=0 on every 5-set, so y is in the incidence-matrix kernel",
    )
    check(
        len(y) % 2 == len(z) % 2 == 1,
        "cochain parity identity |delta z|=|z| mod 2 holds",
    )
    print(
        "negative-control census:"
        " odd residual cycle=3 edges, odd deleted cocycle=45 blocks;"
        " therefore the deleted one-vector is not in the row space"
    )


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    positive_ls239_control()
    negative_eh_control(root)
    print()
    print(f"RESULT: PASS ({CHECKS} exact checks)")
    print("Scope: positive LS(2,3,9) and one negative EH fixed partial only.")
    print("No unrestricted LS(3,4,20) or Erdos--Rosenfeld #835 claim is made.")


if __name__ == "__main__":
    main()

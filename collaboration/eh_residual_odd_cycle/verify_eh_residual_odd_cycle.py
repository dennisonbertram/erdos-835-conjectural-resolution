#!/usr/bin/env python3
"""Verify the Etzion--Hartman last-two-system odd-cycle certificate.

The result concerns only the fifteen complete systems in the checked partial.
It is not an LS(3,4,20) nonexistence proof.
"""

from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Optional


EXPECTED_SHA256 = "06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78"
EXPECTED_COMPLETE_COLOURS = tuple(range(1, 13)) + (14, 15, 16)
EXPECTED_K5_POINT_SETS = {
    frozenset((0, 2, 5, 14, 17)),
    frozenset((1, 3, 4, 15, 16)),
    frozenset((6, 8, 11, 13, 18)),
    frozenset((7, 9, 10, 12, 19)),
}
CERTIFICATE = (
    (0, 2, 14, 17),
    (0, 5, 14, 17),
    (2, 5, 14, 17),
)
EXPECTED_CERTIFICATE_LINES = (277, 593, 2089)

CHECKS: list[str] = []


def check(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    CHECKS.append(label)
    print(f"[ok] {label}")


def load_rows(path: Path) -> list[tuple[tuple[int, ...], int, int]]:
    rows: list[tuple[tuple[int, ...], int, int]] = []
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        fields = tuple(map(int, raw_line.split()))
        if len(fields) != 5:
            raise AssertionError(f"line {line_number}: expected five integers")
        block = fields[:4]
        colour = fields[4]
        if tuple(sorted(block)) != block or len(set(block)) != 4:
            raise AssertionError(f"line {line_number}: invalid block {block}")
        if not all(0 <= point < 20 for point in block):
            raise AssertionError(f"line {line_number}: point outside [20]")
        if colour not in range(-1, 17):
            raise AssertionError(f"line {line_number}: invalid colour {colour}")
        rows.append((block, colour, line_number))
    return rows


def audit_input(
    path: Path,
) -> tuple[
    list[tuple[tuple[int, ...], int, int]],
    tuple[int, ...],
]:
    print("1. raw partial and fifteen complete systems")
    digest = sha256(path.read_bytes()).hexdigest()
    check("input SHA-256 matches the authenticated export", digest == EXPECTED_SHA256)

    rows = load_rows(path)
    expected_blocks = list(combinations(range(20), 4))
    check("the file has all C(20,4)=4,845 rows", len(rows) == comb(20, 4) == 4_845)
    check(
        "blocks occur exactly once in lexicographic order",
        [block for block, _, _ in rows] == expected_blocks,
    )
    assigned = sum(colour >= 0 for _, colour, _ in rows)
    holes = sum(colour < 0 for _, colour, _ in rows)
    check("assigned / holes = 4,773 / 72", (assigned, holes) == (4_773, 72))

    colour_counts = Counter(colour for _, colour, _ in rows if colour >= 0)
    complete_colours = tuple(
        sorted(colour for colour, count in colour_counts.items() if count == 285)
    )
    check(
        "the fifteen complete colours are exactly 1..12,14,15,16",
        complete_colours == EXPECTED_COMPLETE_COLOURS,
    )
    check(
        "the unfinished colours 0 and 13 each have 249 assigned blocks",
        colour_counts[0] == colour_counts[13] == 249,
    )

    for colour in complete_colours:
        triple_counts: Counter[tuple[int, ...]] = Counter()
        for block, value, _ in rows:
            if value == colour:
                triple_counts.update(combinations(block, 3))
        check(
            f"colour {colour:02d} is an S(3,4,20)",
            (len(triple_counts) == comb(20, 3) and set(triple_counts.values()) == {1}),
        )
    return rows, complete_colours


def build_residual_graph(
    rows: list[tuple[tuple[int, ...], int, int]],
    complete_colours: tuple[int, ...],
) -> tuple[
    list[tuple[int, ...]],
    list[dict[int, tuple[int, ...]]],
]:
    print()
    print("2. exact last-two-system residual graph")
    complete_set = set(complete_colours)
    residual = sorted(
        block for block, colour, _ in rows if colour < 0 or colour not in complete_set
    )
    check("the residual has 570 blocks", len(residual) == 570)
    residual_index = {block: index for index, block in enumerate(residual)}

    over_triple: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for block in residual:
        for triple in combinations(block, 3):
            over_triple[triple].append(block)
    check("all 1,140 triples occur in the residual", len(over_triple) == comb(20, 3))
    check(
        "every triple has exactly two residual extensions",
        set(map(len, over_triple.values())) == {2},
    )

    adjacency: list[dict[int, tuple[int, ...]]] = [{} for _ in range(len(residual))]
    for triple, blocks in over_triple.items():
        left, right = (residual_index[block] for block in blocks)
        if right in adjacency[left] or left in adjacency[right]:
            raise AssertionError("parallel residual edge")
        adjacency[left][right] = triple
        adjacency[right][left] = triple

    check("the residual graph is 4-regular", set(map(len, adjacency)) == {4})
    edge_count = sum(map(len, adjacency)) // 2
    check("the residual graph has 1,140 edges", edge_count == 1_140)
    return residual, adjacency


def audit_certificate(
    rows: list[tuple[tuple[int, ...], int, int]],
    residual: list[tuple[int, ...]],
    adjacency: list[dict[int, tuple[int, ...]]],
) -> None:
    print()
    print("3. the explicit shortest odd cycle")
    row_lookup = {block: (colour, line_number) for block, colour, line_number in rows}
    check(
        "certificate blocks are holes on lines 277,593,2089",
        tuple(row_lookup[block] for block in CERTIFICATE)
        == tuple(zip((-1, -1, -1), EXPECTED_CERTIFICATE_LINES)),
    )
    index = {block: position for position, block in enumerate(residual)}
    expected_edge_labels = (
        (0, 14, 17),
        (5, 14, 17),
        (2, 14, 17),
    )
    actual_edge_labels = tuple(
        adjacency[index[CERTIFICATE[position]]][index[CERTIFICATE[(position + 1) % 3]]]
        for position in range(3)
    )
    check(
        "the three certificate edges have the displayed shared triples",
        actual_edge_labels == expected_edge_labels,
    )
    check(
        "the certificate is a simple 3-cycle",
        len(set(CERTIFICATE)) == 3,
    )

    # Independent breadth-first two-colouring attempt.
    colours: list[Optional[int]] = [None] * len(residual)
    conflict: Optional[tuple[int, int]] = None
    for start in range(len(residual)):
        if colours[start] is not None:
            continue
        colours[start] = 0
        queue = deque([start])
        while queue and conflict is None:
            left = queue.popleft()
            for right in adjacency[left]:
                if colours[right] is None:
                    colours[right] = 1 - colours[left]
                    queue.append(right)
                elif colours[right] == colours[left]:
                    conflict = left, right
                    break
        if conflict is not None:
            break
    check("independent BFS detects non-bipartiteness", conflict is not None)
    check("length 3 is the minimum possible odd cycle in a simple graph", 3 >= 3)


def component_census(
    residual: list[tuple[int, ...]],
    adjacency: list[dict[int, tuple[int, ...]]],
) -> None:
    print()
    print("4. component and triangle census")
    seen: set[int] = set()
    components: list[set[int]] = []
    bipartite: list[bool] = []
    for start in range(len(residual)):
        if start in seen:
            continue
        part = {start: 0}
        queue = deque([start])
        component: set[int] = set()
        okay = True
        while queue:
            left = queue.popleft()
            if left in component:
                continue
            component.add(left)
            seen.add(left)
            for right in adjacency[left]:
                if right not in part:
                    part[right] = 1 - part[left]
                    queue.append(right)
                elif part[right] == part[left]:
                    okay = False
        components.append(component)
        bipartite.append(okay)

    census = Counter(
        (len(component), okay) for component, okay in zip(components, bipartite)
    )
    check(
        "component census is 4 nonbipartite K5, 12 nonbipartite 25, 1 bipartite 250",
        census == Counter({(5, False): 4, (25, False): 12, (250, True): 1}),
    )

    five_components = [component for component in components if len(component) == 5]
    check(
        "every 5-vertex component is K5",
        all(
            all(
                right in adjacency[left]
                for left, right in combinations(sorted(component), 2)
            )
            for component in five_components
        ),
    )
    k5_point_sets = {
        frozenset(point for vertex in component for point in residual[vertex])
        for component in five_components
    }
    check(
        "the four K5 components have the displayed five-point supports",
        k5_point_sets == EXPECTED_K5_POINT_SETS,
    )

    triangles = 0
    for left in range(len(residual)):
        for middle in adjacency[left]:
            if middle <= left:
                continue
            triangles += sum(
                right > middle
                for right in set(adjacency[left]) & set(adjacency[middle])
            )
    check("the residual graph has exactly 40 triangles", triangles == 40)


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    input_path = (
        root / "collaboration" / "ls3420_branch0_search" / "eh15_branch0_partial.txt"
    )
    rows, complete_colours = audit_input(input_path)
    residual, adjacency = build_residual_graph(rows, complete_colours)
    audit_certificate(rows, residual, adjacency)
    component_census(residual, adjacency)
    print()
    print(f"ALL {len(CHECKS)} EXACT CHECKS PASSED")
    print("The residual graph is non-bipartite; the fixed fifteen systems")
    print("cannot extend to an LS(3,4,20).")
    print("No general LS(3,4,20) or Erdos--Rosenfeld #835 conclusion is claimed.")


if __name__ == "__main__":
    main()

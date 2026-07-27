#!/usr/bin/env python3
"""Enumerate point/system automorphisms of the Etzion--Hartman 15-core.

This is a standard-library-only exhaustive verifier.  The input is the
authenticated branch-0 partial.  We discard the two unfinished colours and
recover the fifteen complete SQS(20)s in their original Etzion--Hartman
labels 0,...,14.

Completeness of the automorphism enumeration does not rely on a graph
isomorphism package.  The four intrinsic five-point groups are reconstructed
from the four K_5 components of the unused-block graph.  Every automorphism
must permute those components.  We then exhaust all group permutations and
all within-group point bijections, pruning only when a fully mapped block
would violate the induced partial system permutation.
"""

from __future__ import annotations

import hashlib
import itertools
from collections import Counter, defaultdict, deque
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
INPUT = REPO / "collaboration" / "ls3420_branch0_search" / "eh15_branch0_partial.txt"

EXPECTED_INPUT_SHA256 = (
    "06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78"
)

# The authenticated export's old-EH-colour -> branch-0-colour relabelling.
# Old colours 0,...,14 are precisely the fifteen complete SQSs.
BRANCH_COLOUR_BY_EH = (11, 14, 12, 2, 1, 4, 6, 7, 16, 9, 3, 5, 8, 15, 10)

V = 20
N_SYSTEMS = 15
POINTS = tuple(range(V))
BLOCKS = tuple(itertools.combinations(POINTS, 4))
TRIPLES = tuple(itertools.combinations(POINTS, 3))


def check(label: str, condition: bool) -> None:
    """Print and enforce one exact check."""

    if not condition:
        raise AssertionError(label)
    print(f"[ok] {label}")


def parse_core() -> tuple[dict[tuple[int, ...], int], list[set[tuple[int, ...]]]]:
    """Read the canonical partial and return EH-labelled block ownership."""

    raw = INPUT.read_bytes()
    check(
        "input SHA-256 matches the authenticated branch-0 partial",
        hashlib.sha256(raw).hexdigest() == EXPECTED_INPUT_SHA256,
    )
    lines = raw.decode("ascii").splitlines()
    check("input contains C(20,4)=4,845 rows", len(lines) == len(BLOCKS) == 4_845)

    branch_owner: dict[tuple[int, ...], int] = {}
    for expected_block, line in zip(BLOCKS, lines):
        fields = tuple(map(int, line.split()))
        if len(fields) != 5 or fields[:4] != expected_block:
            raise AssertionError(f"malformed row at block {expected_block}")
        branch_owner[expected_block] = fields[4]

    eh_by_branch = {
        branch_colour: eh_colour
        for eh_colour, branch_colour in enumerate(BRANCH_COLOUR_BY_EH)
    }
    owner = {
        block: eh_by_branch.get(branch_colour, -1)
        for block, branch_colour in branch_owner.items()
    }
    systems = [
        {block for block, colour in owner.items() if colour == system}
        for system in range(N_SYSTEMS)
    ]
    check(
        "the relabelling extracts fifteen 285-block systems",
        [len(system) for system in systems] == [285] * N_SYSTEMS,
    )
    for number, system in enumerate(systems):
        covered = Counter(
            triple for block in system for triple in itertools.combinations(block, 3)
        )
        check(
            f"EH system {number:02d} is an S(3,4,20)",
            len(covered) == 1_140 and set(covered.values()) == {1},
        )
    check(
        "the fifteen systems are pairwise block-disjoint",
        sum(map(len, systems)) == len(set().union(*systems)) == 4_275,
    )
    return owner, systems


def intrinsic_groups(owner: dict[tuple[int, ...], int]) -> tuple[tuple[int, ...], ...]:
    """Recover the four five-point groups from residual K_5 components."""

    residual = [block for block in BLOCKS if owner[block] < 0]
    check("the unowned residual has 570 blocks", len(residual) == 570)
    by_triple: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for index, block in enumerate(residual):
        for triple in itertools.combinations(block, 3):
            by_triple[triple].append(index)
    check(
        "each triple has exactly two unowned extensions",
        len(by_triple) == 1_140 and set(map(len, by_triple.values())) == {2},
    )

    adjacency = [set() for _ in residual]
    for left, right in by_triple.values():
        adjacency[left].add(right)
        adjacency[right].add(left)
    check("the residual graph is simple and 4-regular", set(map(len, adjacency)) == {4})

    unseen = set(range(len(residual)))
    components: list[set[int]] = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = deque([root])
        while queue:
            left = queue.popleft()
            for right in adjacency[left]:
                if right in unseen:
                    unseen.remove(right)
                    component.add(right)
                    queue.append(right)
        components.append(component)

    size_census = Counter(map(len, components))
    check(
        "residual component sizes are 250, twelve 25s, and four 5s",
        size_census == {250: 1, 25: 12, 5: 4},
    )
    five_components = [component for component in components if len(component) == 5]
    groups: list[tuple[int, ...]] = []
    for component in five_components:
        blocks = {residual[index] for index in component}
        point_set = tuple(sorted(set().union(*blocks)))
        check(
            f"size-five component is all four-subsets of {point_set}",
            len(point_set) == 5 and blocks == set(itertools.combinations(point_set, 4)),
        )
        groups.append(point_set)
    groups.sort()
    check(
        "the four intrinsic five-point groups partition all twenty points",
        sorted(itertools.chain.from_iterable(groups)) == list(POINTS),
    )
    return tuple(groups)


def enumerate_automorphisms(
    owner: dict[tuple[int, ...], int],
    groups: tuple[tuple[int, ...], ...],
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Exhaust all point maps and their induced system permutations."""

    # An order chosen only for pruning speed.  The first group is mapped
    # completely; each subsequent point immediately closes ten or more
    # four-subsets with already mapped points.
    source_order = tuple(
        itertools.chain.from_iterable(
            (
                groups[0],
                groups[1][:1],
                groups[2][:1],
                groups[3][:1],
                groups[1][1:],
                groups[2][1:],
                groups[3][1:],
            )
        )
    )
    check(
        "DFS source order contains each point exactly once",
        set(source_order) == set(POINTS),
    )

    automorphisms: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    search_nodes = 0
    leaves = 0

    for group_image in itertools.permutations(range(4)):
        target_group_for_point = {
            point: groups[group_image[source_group]]
            for source_group, group in enumerate(groups)
            for point in group
        }
        point_map = [-1] * V
        used_points = [False] * V
        system_map = [-1] * N_SYSTEMS
        inverse_system_map = [-1] * N_SYSTEMS
        mapped: list[int] = []

        def dfs(depth: int) -> None:
            nonlocal search_nodes, leaves
            search_nodes += 1
            if depth == V:
                leaves += 1
                if set(system_map) != set(range(N_SYSTEMS)):
                    raise AssertionError(
                        "complete point automorphism lacks system bijection"
                    )
                automorphisms.append((tuple(point_map), tuple(system_map)))
                return

            source = source_order[depth]
            for target in target_group_for_point[source]:
                if used_points[target]:
                    continue

                changes: list[tuple[int, int]] = []
                okay = True
                for old_triple in itertools.combinations(mapped, 3):
                    source_block = tuple(sorted(old_triple + (source,)))
                    target_block = tuple(
                        sorted(tuple(point_map[x] for x in old_triple) + (target,))
                    )
                    source_system = owner[source_block]
                    target_system = owner[target_block]
                    if (source_system < 0) != (target_system < 0):
                        okay = False
                        break
                    if source_system < 0:
                        continue
                    current = system_map[source_system]
                    inverse = inverse_system_map[target_system]
                    if current >= 0 and current != target_system:
                        okay = False
                        break
                    if inverse >= 0 and inverse != source_system:
                        okay = False
                        break
                    if current < 0:
                        system_map[source_system] = target_system
                        inverse_system_map[target_system] = source_system
                        changes.append((source_system, target_system))

                if okay:
                    point_map[source] = target
                    used_points[target] = True
                    mapped.append(source)
                    dfs(depth + 1)
                    mapped.pop()
                    used_points[target] = False
                    point_map[source] = -1

                for source_system, target_system in reversed(changes):
                    system_map[source_system] = -1
                    inverse_system_map[target_system] = -1

        dfs(0)

    print(f"[exact] exhaustive DFS nodes: {search_nodes}")
    print(f"[exact] complete DFS leaves: {leaves}")
    check("every complete DFS leaf is recorded", leaves == len(automorphisms))
    check(
        "the identity automorphism is present",
        (POINTS, tuple(range(15))) in automorphisms,
    )

    # Full direct semantic verification, independent of incremental pruning.
    for point_map, system_map in automorphisms:
        check_point = set(point_map) == set(POINTS)
        check_system = set(system_map) == set(range(N_SYSTEMS))
        if not check_point or not check_system:
            raise AssertionError("recorded maps are not permutations")
        for block in BLOCKS:
            image = tuple(sorted(point_map[point] for point in block))
            source_system = owner[block]
            target_system = owner[image]
            expected = -1 if source_system < 0 else system_map[source_system]
            if target_system != expected:
                raise AssertionError("recorded automorphism fails on a block")
    check("every recorded automorphism passes all 4,845 block checks", True)
    return sorted(set(automorphisms))


def compose(
    left: tuple[tuple[int, ...], tuple[int, ...]],
    right: tuple[tuple[int, ...], tuple[int, ...]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return left after right."""

    lp, ls = left
    rp, rs = right
    return (
        tuple(lp[rp[x]] for x in POINTS),
        tuple(ls[rs[c]] for c in range(N_SYSTEMS)),
    )


def audit_group(
    automorphisms: list[tuple[tuple[int, ...], tuple[int, ...]]],
) -> None:
    """Check identity, inverse, and closure for the enumerated set."""

    group = set(automorphisms)
    identity = (POINTS, tuple(range(N_SYSTEMS)))
    check("automorphism list has no duplicates", len(group) == len(automorphisms))
    check("automorphism set contains the identity", identity in group)
    for element in automorphisms:
        point_map, system_map = element
        inverse_point = tuple(point_map.index(x) for x in POINTS)
        inverse_system = tuple(system_map.index(c) for c in range(N_SYSTEMS))
        if (inverse_point, inverse_system) not in group:
            raise AssertionError("automorphism set is not inverse-closed")
    check("automorphism set is inverse-closed", True)
    for left in automorphisms:
        for right in automorphisms:
            if compose(left, right) not in group:
                raise AssertionError("automorphism set is not composition-closed")
    check("automorphism set is composition-closed", True)


def triple_orbits(
    automorphisms: list[tuple[tuple[int, ...], tuple[int, ...]]],
) -> list[tuple[tuple[int, int, int], ...]]:
    """Compute the induced automorphism orbits on dropped system triples."""

    triples = set(itertools.combinations(range(N_SYSTEMS), 3))
    orbits: list[tuple[tuple[int, int, int], ...]] = []
    while triples:
        representative = min(triples)
        orbit = {
            tuple(sorted(system_map[c] for c in representative))
            for _, system_map in automorphisms
        }
        # An orbit under a verified group can equally be generated from any
        # member, but checking stability catches an implementation mistake.
        closure = {
            tuple(sorted(system_map[c] for c in member))
            for member in orbit
            for _, system_map in automorphisms
        }
        if closure != orbit:
            raise AssertionError("computed triple orbit is not group-stable")
        triples -= orbit
        orbits.append(tuple(sorted(orbit)))

    check(
        "triple orbits partition all C(15,3)=455 dropped triples",
        sum(map(len, orbits)) == len(set().union(*orbits)) == 455,
    )
    return sorted(orbits, key=lambda orbit: orbit[0])


def full_top_sets(
    owner: dict[tuple[int, ...], int],
    dropped: tuple[int, int, int],
) -> tuple[tuple[int, ...], ...]:
    """Return five-sets all of whose four-subsets lie in the five-fold leave."""

    dropped_set = set(dropped)
    return tuple(
        five
        for five in itertools.combinations(POINTS, 5)
        if all(
            owner[block] < 0 or owner[block] in dropped_set
            for block in itertools.combinations(five, 4)
        )
    )


def five_set_occupancy_census(
    owner: dict[tuple[int, ...], int],
) -> dict[tuple[int, int, int], tuple[int, ...]]:
    """Count five-sets by the number of their blocks in each five-fold leave."""

    five_sets = tuple(itertools.combinations(POINTS, 5))
    blocks_in_five = tuple(tuple(itertools.combinations(five, 4)) for five in five_sets)
    census: dict[tuple[int, int, int], tuple[int, ...]] = {}
    for dropped in itertools.combinations(range(N_SYSTEMS), 3):
        dropped_set = set(dropped)
        counts = Counter(
            sum(owner[block] < 0 or owner[block] in dropped_set for block in blocks)
            for blocks in blocks_in_five
        )
        census[dropped] = tuple(counts[value] for value in range(6))
    return census


# The three five-packs are colours 0..4, 5..9, and 10..14.  Each is attached
# to one of the three partitions of the four intrinsic five-point groups.
PACK_GROUP_PAIRS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def restricted_leave_graph(
    owner: dict[tuple[int, ...], int],
    dropped: tuple[int, int, int],
    point_set: tuple[int, ...],
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, ...], ...],
    tuple[int, ...],
]:
    """Build the ten-point induced leave graph for one same-pack drop."""

    dropped_set = set(dropped)
    vertices = tuple(
        block
        for block in itertools.combinations(point_set, 4)
        if owner[block] < 0 or owner[block] in dropped_set
    )
    index = {block: row for row, block in enumerate(vertices)}
    by_triple: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for block, row in index.items():
        for triple in itertools.combinations(block, 3):
            by_triple[triple].append(row)

    if len(vertices) != 150:
        raise AssertionError("ten-point leave does not have 150 blocks")
    if set(by_triple) != set(itertools.combinations(point_set, 3)):
        raise AssertionError("ten-point leave misses a triple")
    if set(map(len, by_triple.values())) != {5}:
        raise AssertionError("ten-point leave is not five-fold")

    adjacency = [set() for _ in vertices]
    for rows in by_triple.values():
        for left, right in itertools.combinations(rows, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)
    if set(map(len, adjacency)) != {16}:
        raise AssertionError("ten-point leave graph is not 16-regular")
    if sum(map(len, adjacency)) // 2 != 1_200:
        raise AssertionError("ten-point leave graph does not have 1,200 edges")
    root = tuple(by_triple[min(by_triple)])
    return vertices, tuple(tuple(sorted(row)) for row in adjacency), root


def exact_five_colourability(
    adjacency: tuple[tuple[int, ...], ...],
    root_clique: tuple[int, ...],
) -> tuple[bool, int]:
    """Exhaustively decide five-colourability by deterministic DSATUR.

    The root K_5 is assigned colours 0,...,4 without loss of generality:
    every proper five-colouring uses all five colours there, and a global
    colour permutation puts them in this order.
    """

    number = len(adjacency)
    if len(root_clique) != 5:
        raise AssertionError("root is not a five-vertex clique")
    if any(
        right not in adjacency[left]
        for left, right in itertools.combinations(root_clique, 2)
    ):
        raise AssertionError("root vertices are not pairwise adjacent")

    colour = [-1] * number
    forbidden = [0] * number
    for value, vertex in enumerate(root_clique):
        colour[vertex] = value
        for neighbour in adjacency[vertex]:
            forbidden[neighbour] |= 1 << value

    nodes = 0

    def visit(uncoloured: int) -> bool:
        nonlocal nodes
        nodes += 1
        if uncoloured == 0:
            return True

        chosen = -1
        best_key = (-1, -1)
        for vertex in range(number):
            if colour[vertex] >= 0:
                continue
            if forbidden[vertex] == 0b11111:
                return False
            key = (
                forbidden[vertex].bit_count(),
                sum(colour[neighbour] < 0 for neighbour in adjacency[vertex]),
            )
            if key > best_key:
                chosen = vertex
                best_key = key

        available = (~forbidden[chosen]) & 0b11111
        while available:
            bit = available & -available
            available -= bit
            colour[chosen] = bit.bit_length() - 1
            changed: list[int] = []
            failed = False
            for neighbour in adjacency[chosen]:
                if colour[neighbour] < 0 and not (forbidden[neighbour] & bit):
                    forbidden[neighbour] |= bit
                    changed.append(neighbour)
                    if forbidden[neighbour] == 0b11111:
                        failed = True
                        break
            if not failed and visit(uncoloured - 1):
                return True
            for neighbour in changed:
                forbidden[neighbour] ^= bit
            colour[chosen] = -1
        return False

    return visit(number - len(root_clique)), nodes


def eliminate_same_pack_drops(
    owner: dict[tuple[int, ...], int],
    groups: tuple[tuple[int, ...], ...],
) -> tuple[int, int, int]:
    """Prove all thirty same-five-pack drop cases locally impossible."""

    cases = 0
    graphs = 0
    node_counts: list[int] = []
    for pack, group_pairs in enumerate(PACK_GROUP_PAIRS):
        for dropped in itertools.combinations(range(5 * pack, 5 * pack + 5), 3):
            cases += 1
            for left_group, right_group in group_pairs:
                point_set = tuple(sorted(groups[left_group] + groups[right_group]))
                _vertices, adjacency, root = restricted_leave_graph(
                    owner, dropped, point_set
                )
                colourable, nodes = exact_five_colourability(adjacency, root)
                if colourable:
                    raise AssertionError(
                        f"unexpected five-colouring for {dropped} on {point_set}"
                    )
                graphs += 1
                node_counts.append(nodes)

    check("all 30 same-five-pack cases were checked", cases == 30)
    check("both ten-point restrictions were checked in every case", graphs == 60)
    check("every restricted graph is exhaustively non-five-colourable", True)
    return sum(node_counts), min(node_counts), max(node_counts)


def audit_colour_search_controls() -> None:
    """Exercise both outcomes of the exact colouring routine."""

    k5 = tuple(tuple(right for right in range(5) if right != left) for left in range(5))
    colourable, nodes = exact_five_colourability(k5, tuple(range(5)))
    check("positive DSATUR control K5 is five-colourable", colourable and nodes == 1)

    k6 = tuple(tuple(right for right in range(6) if right != left) for left in range(6))
    colourable, nodes = exact_five_colourability(k6, tuple(range(5)))
    check(
        "negative DSATUR control K6 is not five-colourable",
        not colourable and nodes == 1,
    )


def main() -> None:
    owner, _systems = parse_core()
    groups = intrinsic_groups(owner)
    print(f"[exact] intrinsic groups: {groups}")
    automorphisms = enumerate_automorphisms(owner, groups)
    print(f"[exact] automorphism group order: {len(automorphisms)}")
    audit_group(automorphisms)

    induced_system_maps = sorted({system_map for _, system_map in automorphisms})
    print(f"[exact] faithful system-action order: {len(induced_system_maps)}")
    check(
        "point automorphisms act faithfully on the fifteen systems",
        len(induced_system_maps) == len(automorphisms),
    )

    orbits = triple_orbits(automorphisms)
    print(f"[exact] number of dropped-triple orbits: {len(orbits)}")
    check(
        "the trivial action gives 455 singleton dropped-triple orbits",
        len(orbits) == 455 and set(map(len, orbits)) == {1},
    )

    occupancy = five_set_occupancy_census(owner)
    signature_classes = Counter(occupancy.values())
    top_census = Counter(signature[5] for signature in occupancy.values())
    print(
        f"[exact] full-top K5 census across drop cases: {dict(sorted(top_census.items()))}"
    )
    print(f"[exact] five-set occupancy signature classes: {len(signature_classes)}")
    print(
        "[exact] signature class-size census: "
        f"{dict(sorted(Counter(signature_classes.values()).items()))}"
    )
    check(
        "full-top counts are 4 in 405 cases, 24 in 30, and 29 in 20",
        top_census == {4: 405, 24: 30, 29: 20},
    )
    same_pack = {
        dropped
        for pack in range(3)
        for dropped in itertools.combinations(range(5 * pack, 5 * pack + 5), 3)
    }
    check(
        "the 30 cases with 24 full top K5s are exactly the same-pack drops",
        {dropped for dropped, signature in occupancy.items() if signature[5] == 24}
        == same_pack,
    )
    check(
        "the occupancy invariant has exactly 130 signatures",
        len(signature_classes) == 130
        and Counter(signature_classes.values())
        == {1: 71, 2: 19, 3: 4, 4: 1, 5: 10, 10: 22, 20: 3},
    )

    audit_colour_search_controls()
    total_nodes, minimum_nodes, maximum_nodes = eliminate_same_pack_drops(owner, groups)
    print(
        "[exact] local DSATUR nodes: "
        f"total={total_nodes} min={minimum_nodes} max={maximum_nodes}"
    )
    check(
        "deterministic local search node census matches",
        (total_nodes, minimum_nodes, maximum_nodes) == (96_980, 1_094, 3_323),
    )
    print("[scope] 30 of 455 EH drop-three repair cases are excluded; 425 remain.")
    print("[scope] This does not decide LS(3,4,20) and does not address #835 directly.")
    print("status: PASS")


if __name__ == "__main__":
    main()

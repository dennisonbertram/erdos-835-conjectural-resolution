#!/usr/bin/env python3
"""Generate and verify the Etzion--Hartman 15-SQS(20) near-solution.

The construction is the p=v=5 specialization in Etzion--Hartman,
"Towards a large set of Steiner quadruple systems" (1991).  It gives
15 pairwise disjoint SQS(20)s, but that particular 15-set is maximal.
The 570 unused blocks are therefore only a seed for an unrestricted
17-colouring search, not an LS(3,4,20) certificate.

Output format is one sorted quadruple and a colour per line.  Colours
0,...,14 are exact SQSs.  Colours 15 and 16 are a locally optimized
cut of the residual graph.
"""

from __future__ import annotations

import argparse
import itertools
import random
from collections import Counter, deque
from pathlib import Path


BASE_SQS10 = (
    (0, 1, 2, 3), (0, 1, 4, 5), (0, 1, 6, 7), (0, 1, 8, 9),
    (0, 2, 4, 7), (0, 2, 5, 8), (0, 2, 6, 9), (0, 3, 4, 9),
    (0, 3, 5, 6), (0, 3, 7, 8), (0, 4, 6, 8), (0, 5, 7, 9),
    (1, 2, 4, 8), (1, 2, 5, 6), (1, 2, 7, 9), (1, 3, 4, 7),
    (1, 3, 5, 9), (1, 3, 6, 8), (1, 4, 6, 9), (1, 5, 7, 8),
    (2, 3, 4, 6), (2, 3, 5, 7), (2, 3, 8, 9), (2, 4, 5, 9),
    (2, 6, 7, 8), (3, 4, 5, 8), (3, 6, 7, 9), (4, 5, 6, 7),
    (4, 7, 8, 9), (5, 6, 8, 9),
)

# Relabel the known SQS(10) so that {0,...,4} and {5,...,9} are
# independent sets, then take five disjoint relabelled copies preserving
# that bipartition.
OLD_FIRST_HALF = (0, 1, 2, 4, 6)
SQS10_PERMUTATIONS = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 0, 2, 4, 3, 9, 6, 8, 7, 5),
    (4, 1, 0, 2, 3, 8, 5, 6, 7, 9),
    (7, 5, 9, 6, 8, 1, 0, 3, 2, 4),
    (1, 4, 0, 3, 2, 9, 5, 7, 6, 8),
)

# The three 1-factorizations (partitions into two unordered pairs) of K_4.
PARTITIONS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def relabelled_sqs10s() -> list[set[tuple[int, ...]]]:
    second = tuple(x for x in range(10) if x not in OLD_FIRST_HALF)
    relabel = {
        old: new
        for new, old in enumerate(OLD_FIRST_HALF + second)
    }
    base = {
        tuple(sorted(relabel[x] for x in block))
        for block in BASE_SQS10
    }
    systems = [
        {
            tuple(sorted(permutation[x] for x in block))
            for block in base
        }
        for permutation in SQS10_PERMUTATIONS
    ]

    used: set[tuple[int, ...]] = set()
    triples = set(itertools.combinations(range(10), 3))
    for system in systems:
        assert len(system) == 30
        assert not (used & system)
        used |= system
        cover = Counter(
            triple
            for block in system
            for triple in itertools.combinations(block, 3)
        )
        assert set(cover) == triples
        assert set(cover.values()) == {1}
        assert all(
            not (set(block) <= set(range(5)))
            and not (set(block) <= set(range(5, 10)))
            for block in system
        )
    return systems


def point(value: int, colour: int) -> int:
    return 4 * value + colour


def near_factor(isolate: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """The two edges of the standard near-one-factor F_isolate of K_5."""
    return (
        tuple(sorted(((isolate + 1) % 5, (isolate - 1) % 5))),
        tuple(sorted(((isolate + 2) % 5, (isolate - 2) % 5))),
    )


def orthogonal_array(shift: int) -> list[tuple[int, ...]]:
    """OA(3,5,5): quadratic evaluations, with one shifted coordinate."""
    rows = []
    for a in range(5):
        for b in range(5):
            for c in range(5):
                row = [
                    (a + b * x + c * x * x) % 5
                    for x in range(5)
                ]
                row[0] = (row[0] + shift) % 5
                rows.append(tuple(row))

    assert len(rows) == 125
    for coordinates in itertools.combinations(range(5), 3):
        projections = {
            tuple(row[i] for i in coordinates)
            for row in rows
        }
        assert len(projections) == 125
    return rows


def embed_sqs10(
    system: set[tuple[int, ...]], colours: tuple[int, int]
) -> set[tuple[int, ...]]:
    embedded = set()
    for block in system:
        image = []
        for x in block:
            if x < 5:
                image.append(point(x, colours[0]))
            else:
                image.append(point(x - 5, colours[1]))
        embedded.add(tuple(sorted(image)))
    return embedded


def etzion_hartman_systems() -> list[set[tuple[int, ...]]]:
    small = relabelled_sqs10s()
    systems: list[set[tuple[int, ...]]] = []

    for partition_index, ((i, j), (s, t)) in enumerate(PARTITIONS):
        rows = orthogonal_array(partition_index)
        for k in range(5):
            system = embed_sqs10(small[k], (i, j))
            system |= embed_sqs10(small[k], (s, t))

            for row in rows:
                if row[4] != k:
                    continue

                # Type C: one point in each of the four groups.
                system.add(tuple(sorted(point(row[c], c) for c in range(4))))

                # Type B: one point in two groups and one edge in a third.
                for doubled in (s, t):
                    for a, b in near_factor(row[doubled]):
                        system.add(tuple(sorted((
                            point(row[i], i), point(row[j], j),
                            point(a, doubled), point(b, doubled),
                        ))))
                for doubled in (i, j):
                    for a, b in near_factor(row[doubled]):
                        system.add(tuple(sorted((
                            point(row[s], s), point(row[t], t),
                            point(a, doubled), point(b, doubled),
                        ))))

            assert len(system) == 285
            systems.append(system)

    return systems


def verify_systems(
    systems: list[set[tuple[int, ...]]],
) -> tuple[list[tuple[int, ...]], list[list[int]]]:
    triples = list(itertools.combinations(range(20), 3))
    all_blocks = list(itertools.combinations(range(20), 4))
    owner: dict[tuple[int, ...], int] = {}
    for colour, system in enumerate(systems):
        cover = Counter(
            triple
            for block in system
            for triple in itertools.combinations(block, 3)
        )
        assert len(system) == 285
        assert len(cover) == len(triples)
        assert set(cover.values()) == {1}
        for block in system:
            assert block not in owner
            owner[block] = colour
    assert len(owner) == 15 * 285

    residual = [block for block in all_blocks if block not in owner]
    residual_index = {block: i for i, block in enumerate(residual)}
    by_triple: dict[tuple[int, ...], list[int]] = {
        triple: [] for triple in triples
    }
    for block in residual:
        r = residual_index[block]
        for triple in itertools.combinations(block, 3):
            by_triple[triple].append(r)

    adjacency = [[] for _ in residual]
    for extensions in by_triple.values():
        assert len(extensions) == 2
        a, b = extensions
        adjacency[a].append(b)
        adjacency[b].append(a)
    assert all(len(neighbours) == 4 for neighbours in adjacency)
    assert all(len(set(neighbours)) == 4 for neighbours in adjacency)
    return residual, adjacency


def connected_components(adjacency: list[list[int]]) -> list[list[int]]:
    unseen = set(range(len(adjacency)))
    components = []
    while unseen:
        root = next(iter(unseen))
        unseen.remove(root)
        component = []
        queue = deque([root])
        while queue:
            v = queue.popleft()
            component.append(v)
            for w in adjacency[v]:
                if w in unseen:
                    unseen.remove(w)
                    queue.append(w)
        components.append(component)
    return components


def verify_component_shapes(
    adjacency: list[list[int]], components: list[list[int]]
) -> None:
    """Check the claimed B_250 + 12(C5 square C5) + 4K5 decomposition."""
    import networkx as nx

    graph = nx.Graph()
    graph.add_nodes_from(range(len(adjacency)))
    graph.add_edges_from(
        (v, w)
        for v, neighbours in enumerate(adjacency)
        for w in neighbours
        if v < w
    )
    torus = nx.cartesian_product(nx.cycle_graph(5), nx.cycle_graph(5))
    counts = Counter()
    for component in components:
        induced = graph.subgraph(component)
        if len(component) == 250:
            assert nx.is_bipartite(induced)
            counts["bipartite_250"] += 1
        elif len(component) == 25:
            assert nx.is_isomorphic(induced, torus)
            counts["torus_25"] += 1
        elif len(component) == 5:
            assert induced.number_of_edges() == 10
            counts["K5"] += 1
        else:
            raise AssertionError(f"unexpected component size {len(component)}")
    assert counts == {
        "bipartite_250": 1,
        "torus_25": 12,
        "K5": 4,
    }


def cut_conflicts(adjacency: list[list[int]], side: list[int]) -> int:
    return sum(
        side[v] == side[w]
        for v, neighbours in enumerate(adjacency)
        for w in neighbours
        if v < w
    )


def local_max_cut(
    adjacency: list[list[int]], seed: int, restarts: int
) -> tuple[list[int], int]:
    """Repeated component-wise single-flip ascent for a near-solution."""
    rng = random.Random(seed)
    whole_side = [0] * len(adjacency)
    total_best = 0
    components = connected_components(adjacency)

    for component_number, component in enumerate(components):
        position = {v: i for i, v in enumerate(component)}
        graph = [
            [position[w] for w in adjacency[v]]
            for v in component
        ]
        best_side: list[int] | None = None
        best = 10**9

        for _ in range(restarts):
            side = [rng.randrange(2) for _ in graph]
            same = [
                sum(side[v] == side[w] for w in graph[v])
                for v in range(len(graph))
            ]

            # A flip changes the objective by degree - 2 * same[v].
            while True:
                improving = [
                    v for v in range(len(graph))
                    if len(graph[v]) - 2 * same[v] < 0
                ]
                if not improving:
                    break
                delta_min = min(
                    len(graph[v]) - 2 * same[v]
                    for v in improving
                )
                candidates = [
                    v for v in improving
                    if len(graph[v]) - 2 * same[v] == delta_min
                ]
                v = rng.choice(candidates)
                old = side[v]
                side[v] ^= 1
                same[v] = len(graph[v]) - same[v]
                for w in graph[v]:
                    if side[w] == old:
                        same[w] -= 1
                    else:
                        same[w] += 1

            score = sum(same) // 2
            if score < best:
                best = score
                best_side = side

        assert best_side is not None
        for local, original in enumerate(component):
            whole_side[original] = best_side[local]
        total_best += best
        print(
            f"component {component_number} size {len(component)} "
            f"cut conflicts {best}"
        )

    assert total_best == cut_conflicts(adjacency, whole_side)
    return whole_side, total_best


def exact_max_cut(
    adjacency: list[list[int]], seconds: float, seed: int
) -> tuple[list[int], int, bool]:
    """Optimize the residual cut with CP-SAT, component by component."""
    from ortools.sat.python import cp_model

    whole_side = [0] * len(adjacency)
    total_conflicts = 0
    all_optimal = True
    components = connected_components(adjacency)
    for component_number, component in enumerate(components):
        position = {v: i for i, v in enumerate(component)}
        edges = [
            (position[v], position[w])
            for v in component
            for w in adjacency[v]
            if v < w
        ]
        model = cp_model.CpModel()
        side = [model.new_bool_var(f"x_{v}") for v in range(len(component))]
        crossed = [
            model.new_bool_var(f"e_{edge_number}")
            for edge_number in range(len(edges))
        ]
        for edge_var, (v, w) in zip(crossed, edges):
            # Maximization forces edge_var=1 exactly when the endpoints differ.
            model.add(edge_var <= side[v] + side[w])
            model.add(edge_var <= 2 - side[v] - side[w])
        model.add(side[0] == 0)
        model.maximize(sum(crossed))

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = seconds
        solver.parameters.num_search_workers = 8
        solver.parameters.random_seed = seed + component_number
        status = solver.solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise RuntimeError(
                f"CP-SAT found no cut for component {component_number}"
            )
        optimal = status == cp_model.OPTIMAL
        all_optimal &= optimal
        component_side = [solver.value(x) for x in side]
        component_conflicts = len(edges) - round(solver.objective_value)
        for local, original in enumerate(component):
            whole_side[original] = component_side[local]
        total_conflicts += component_conflicts
        print(
            f"component {component_number} size {len(component)} "
            f"cut conflicts {component_conflicts} "
            f"({'optimal' if optimal else 'time-limited'})"
        )

    assert total_conflicts == cut_conflicts(adjacency, whole_side)
    return whole_side, total_conflicts, all_optimal


def exact_partial_bipartite(
    adjacency: list[list[int]], seconds: float, seed: int
) -> tuple[list[int], list[bool], int, bool]:
    """Maximum induced bipartite residual subgraph, component by component."""
    from ortools.sat.python import cp_model

    whole_side = [0] * len(adjacency)
    whole_kept = [False] * len(adjacency)
    total_removed = 0
    all_optimal = True
    components = connected_components(adjacency)
    for component_number, component in enumerate(components):
        position = {v: i for i, v in enumerate(component)}
        edges = [
            (position[v], position[w])
            for v in component
            for w in adjacency[v]
            if v < w
        ]
        model = cp_model.CpModel()
        kept = [model.new_bool_var(f"k_{v}") for v in range(len(component))]
        side = [model.new_bool_var(f"x_{v}") for v in range(len(component))]
        for v, w in edges:
            # If both endpoints are kept, their sides must differ.
            model.add_bool_or([
                kept[v].Not(), kept[w].Not(), side[v], side[w],
            ])
            model.add_bool_or([
                kept[v].Not(), kept[w].Not(),
                side[v].Not(), side[w].Not(),
            ])
        model.add(side[0] == 0)
        model.maximize(sum(kept))

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = seconds
        solver.parameters.num_search_workers = 8
        solver.parameters.random_seed = seed + component_number
        status = solver.solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise RuntimeError(
                f"CP-SAT found no partial cut for component {component_number}"
            )
        optimal = status == cp_model.OPTIMAL
        all_optimal &= optimal
        component_removed = len(component) - round(solver.objective_value)
        for local, original in enumerate(component):
            whole_side[original] = solver.value(side[local])
            whole_kept[original] = bool(solver.value(kept[local]))
        total_removed += component_removed
        print(
            f"component {component_number} size {len(component)} "
            f"partial removed {component_removed} "
            f"({'optimal' if optimal else 'time-limited'})"
        )

    for v, neighbours in enumerate(adjacency):
        for w in neighbours:
            assert (
                not whole_kept[v]
                or not whole_kept[w]
                or whole_side[v] != whole_side[w]
            )
    return whole_side, whole_kept, total_removed, all_optimal


def exact_balanced_max_cut(
    adjacency: list[list[int]], seconds: float, seed: int
) -> tuple[list[int], int, bool]:
    """Optimize the residual cut subject to 285 vertices on each side."""
    from ortools.sat.python import cp_model

    edges = [
        (v, w)
        for v, neighbours in enumerate(adjacency)
        for w in neighbours
        if v < w
    ]
    model = cp_model.CpModel()
    side = [model.new_bool_var(f"x_{v}") for v in range(len(adjacency))]
    crossed = [
        model.new_bool_var(f"e_{edge_number}")
        for edge_number in range(len(edges))
    ]
    for edge_var, (v, w) in zip(crossed, edges):
        model.add(edge_var <= side[v] + side[w])
        model.add(edge_var <= 2 - side[v] - side[w])
    model.add(sum(side) == len(adjacency) // 2)
    model.maximize(sum(crossed))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = seed
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError("CP-SAT found no balanced residual cut")
    answer = [solver.value(x) for x in side]
    conflicts = len(edges) - round(solver.objective_value)
    assert sum(answer) == len(adjacency) // 2
    assert conflicts == cut_conflicts(adjacency, answer)
    return answer, conflicts, status == cp_model.OPTIMAL


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evidence/ls_3_4_20_eh15_seed.txt"),
    )
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--restarts", type=int, default=1000)
    parser.add_argument(
        "--exact-cut-seconds",
        type=float,
        default=0.0,
        help="if positive, run CP-SAT for this many seconds per component",
    )
    parser.add_argument(
        "--balanced-cut",
        action="store_true",
        help="require the two residual seed colours to have size 285",
    )
    parser.add_argument(
        "--partial-output",
        type=Path,
        help="also write a proper partial colouring, using -1 for uncoloured",
    )
    parser.add_argument(
        "--exact-partial-seconds",
        type=float,
        default=20.0,
        help="CP-SAT seconds per component for --partial-output",
    )
    args = parser.parse_args()

    systems = etzion_hartman_systems()
    residual, adjacency = verify_systems(systems)
    components = connected_components(adjacency)
    verify_component_shapes(adjacency, components)
    print("verified 15 disjoint SQS(20)s")
    print("residual component sizes:",
          sorted((len(component) for component in components), reverse=True))

    if args.balanced_cut:
        side, conflicts, optimal = exact_balanced_max_cut(
            adjacency,
            args.exact_cut_seconds if args.exact_cut_seconds > 0 else 20.0,
            args.seed,
        )
        print(
            f"balanced residual cut proved optimal:"
            f" {'yes' if optimal else 'no'}"
        )
    elif args.exact_cut_seconds > 0:
        side, conflicts, optimal = exact_max_cut(
            adjacency, args.exact_cut_seconds, args.seed
        )
        print(
            "all residual component cuts proved optimal:"
            f" {'yes' if optimal else 'no'}"
        )
    else:
        side, conflicts = local_max_cut(
            adjacency, args.seed, args.restarts
        )
    owner = {
        block: colour
        for colour, system in enumerate(systems)
        for block in system
    }
    owner.update({
        block: 15 + side[r]
        for r, block in enumerate(residual)
    })

    all_blocks = list(itertools.combinations(range(20), 4))
    assert len(owner) == len(all_blocks) == 4845
    measured = 0
    for triple in itertools.combinations(range(20), 3):
        colours = [
            owner[tuple(sorted(triple + (x,)))]
            for x in range(20)
            if x not in triple
        ]
        measured += len(colours) - len(set(colours))
    assert measured == conflicts

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for block in all_blocks:
            handle.write("{} {} {} {} {}\n".format(*block, owner[block]))
    print(f"wrote {args.output} with {conflicts} conflicting triple-stars")

    if args.partial_output is not None:
        partial_side, kept, removed, partial_optimal = exact_partial_bipartite(
            adjacency, args.exact_partial_seconds, args.seed
        )
        partial_owner = {
            block: colour
            for colour, system in enumerate(systems)
            for block in system
        }
        partial_owner.update({
            block: (15 + partial_side[r] if kept[r] else -1)
            for r, block in enumerate(residual)
        })
        assert sum(value < 0 for value in partial_owner.values()) == removed
        for triple in itertools.combinations(range(20), 3):
            assigned = [
                partial_owner[tuple(sorted(triple + (x,)))]
                for x in range(20)
                if x not in triple
            ]
            assigned = [value for value in assigned if value >= 0]
            assert len(assigned) == len(set(assigned))
        args.partial_output.parent.mkdir(parents=True, exist_ok=True)
        with args.partial_output.open("w", encoding="utf-8") as handle:
            for block in all_blocks:
                handle.write(
                    "{} {} {} {} {}\n".format(*block, partial_owner[block])
                )
        print(
            f"wrote {args.partial_output} with {removed} uncoloured blocks; "
            f"all component optima proved: {'yes' if partial_optimal else 'no'}"
        )


if __name__ == "__main__":
    main()

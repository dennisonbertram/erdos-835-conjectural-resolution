#!/usr/bin/env python3
"""Extract a compatible fixed-row core from a best-effort matching hint.

A best-effort Q-transversal can repeat triple-colour groups.  This script
greedily removes high-conflict selected cells until the remainder is a
pairwise compatible exact-cover partial solution, optionally removes further
random rows to loosen the repair neighborhood, and writes the corresponding
sparse Algorithm-X matrix labels.  Failure to extend one such core has no
global mathematical status.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from convert_matching_hint_to_dlx import read_matrix
from search_cyclic_invariant_matching_local import QUAD_GROUPS
from verify_fan_kernel_reduction import (
    build_orbit_hypergraph,
    construct_large_set,
    verify_large_set,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hint", type=Path)
    parser.add_argument("matrix", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--loosen", type=int, default=0)
    args = parser.parse_args()

    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)
    _, matrix_rows = read_matrix(args.matrix)
    incidence: list[list[int]] = [[] for _ in cells]
    for group_index, group in enumerate(groups):
        for cell in group:
            incidence[cell].append(group_index)
    signatures = [tuple(sorted(columns)) for columns in incidence]
    if set(signatures) != set(matrix_rows):
        raise AssertionError("canonical and matrix incidence streams differ")

    hinted_cells = [
        int(line)
        for line in args.hint.read_text(encoding="ascii").splitlines()
        if line.strip()
    ]
    hinted = set(hinted_cells)
    if len(hinted_cells) != QUAD_GROUPS or len(hinted) != QUAD_GROUPS:
        raise ValueError(
            f"hint must contain {QUAD_GROUPS} distinct quotient-cell indices"
        )
    if any(
        len(hinted & set(group)) != 1 for group in groups[:QUAD_GROUPS]
    ):
        raise ValueError("hint is not a one-per-Q-group transversal")

    rng = random.Random(args.seed)
    active = set(hinted)
    conflict_removals = 0
    while True:
        counts = [
            len(active & set(group)) for group in groups[QUAD_GROUPS:]
        ]
        if max(counts, default=0) <= 1:
            break
        penalty: dict[int, int] = {}
        for group, count in zip(groups[QUAD_GROUPS:], counts):
            if count <= 1:
                continue
            for cell in active & set(group):
                penalty[cell] = penalty.get(cell, 0) + count - 1
        maximum = max(penalty.values())
        choices = [cell for cell, value in penalty.items() if value == maximum]
        active.remove(rng.choice(choices))
        conflict_removals += 1

    if args.loosen < 0 or args.loosen > len(active):
        raise ValueError("--loosen is outside the compatible-core size")
    for cell in rng.sample(sorted(active), args.loosen):
        active.remove(cell)
    if any(len(active & set(group)) > 1 for group in groups):
        raise AssertionError("fixed-row core is not pairwise compatible")

    liveness_removals = 0
    cell_groups = [set(columns) for columns in signatures]
    while True:
        covered = set().union(*(cell_groups[cell] for cell in active))
        dead_group = next(
            (
                group_index
                for group_index, group in enumerate(groups)
                if group_index not in covered
                and not any(
                    cell_groups[cell].isdisjoint(covered) for cell in group
                )
            ),
            None,
        )
        if dead_group is None:
            break
        blockers: dict[int, int] = {}
        for candidate in groups[dead_group]:
            for fixed in active:
                if not cell_groups[candidate].isdisjoint(cell_groups[fixed]):
                    blockers[fixed] = blockers.get(fixed, 0) + 1
        if not blockers:
            raise AssertionError("dead residual group has no fixed-row blocker")
        maximum = max(blockers.values())
        choices = [cell for cell, value in blockers.items() if value == maximum]
        active.remove(rng.choice(choices))
        liveness_removals += 1

    labels = sorted(matrix_rows[signatures[cell]] for cell in active)
    args.output.write_text(
        "".join(f"{label}\n" for label in labels),
        encoding="ascii",
    )
    print(f"hinted_rows={len(hinted)}")
    print(f"conflict_removals={conflict_removals}")
    print(f"loosened_rows={args.loosen}")
    print(f"liveness_removals={liveness_removals}")
    print(f"fixed_rows={len(labels)}")
    print("pairwise_compatibility=PASS")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()

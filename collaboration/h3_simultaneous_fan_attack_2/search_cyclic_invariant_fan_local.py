#!/usr/bin/env python3
"""Heuristic permutation-swap search for a C17-invariant 13-fan.

Every quadruple-orbit group is kept rainbow by representing its labels as a
permutation.  A move swaps two labels in one such group and scores only the
912 triple-colour orbit groups.  A found certificate is checked semantically
before it is written.  Failure or timeout has no mathematical status.
"""

from __future__ import annotations

import argparse
import math
import random
import time
from pathlib import Path

from verify_fan_kernel_reduction import (
    build_orbit_hypergraph,
    construct_large_set,
    verify_large_set,
)


LABELS = 13
QUAD_GROUPS = 228


def collision_score(counts: list[int]) -> int:
    return sum(count * (count - 1) // 2 for count in counts)


def verify_solution(
    labels: list[int],
    groups: tuple[tuple[int, ...], ...],
) -> None:
    target = set(range(LABELS))
    if any({labels[cell] for cell in group} != target for group in groups):
        raise AssertionError("local-search candidate has a non-rainbow group")


def search(
    groups: tuple[tuple[int, ...], ...],
    seconds: float,
    seed: int,
    progress: int,
) -> tuple[list[int] | None, int, int]:
    rng = random.Random(seed)
    qgroups = groups[:QUAD_GROUPS]
    tcgroups = groups[QUAD_GROUPS:]
    cell_count = sum(len(group) for group in qgroups)
    if cell_count != 2_964:
        raise AssertionError("quadruple groups do not partition the cells")

    qgroup_of = [-1] * cell_count
    cell_tc: list[list[int]] = [[] for _ in range(cell_count)]
    for qindex, group in enumerate(qgroups):
        for cell in group:
            if qgroup_of[cell] != -1:
                raise AssertionError("cell lies in two quadruple groups")
            qgroup_of[cell] = qindex
    for tindex, group in enumerate(tcgroups):
        for cell in group:
            cell_tc[cell].append(tindex)
    if -1 in qgroup_of or any(len(items) != 4 for items in cell_tc):
        raise AssertionError("unexpected quotient incidence degrees")

    started = time.monotonic()
    deadline = started + seconds
    moves = 0
    restarts = 0
    best_global = 10**9

    while time.monotonic() < deadline:
        restarts += 1
        labels = [-1] * cell_count
        for qindex, group in enumerate(qgroups):
            permutation = list(range(LABELS))
            if qindex:
                rng.shuffle(permutation)
            for position, cell in enumerate(group):
                labels[cell] = permutation[position]

        counts = [[0] * LABELS for _ in tcgroups]
        for tindex, group in enumerate(tcgroups):
            for cell in group:
                counts[tindex][labels[cell]] += 1
        group_scores = [collision_score(row) for row in counts]
        score = sum(group_scores)
        best_restart = score
        stagnant = 0
        temperature = 0.2

        while time.monotonic() < deadline:
            if score == 0:
                verify_solution(labels, groups)
                return labels, moves, restarts

            for _ in range(100):
                bad_group = rng.randrange(len(tcgroups))
                if group_scores[bad_group]:
                    break
            else:
                bad = [index for index, value in enumerate(group_scores) if value]
                bad_group = rng.choice(bad)

            movable_lefts = [
                cell
                for cell in tcgroups[bad_group]
                if counts[bad_group][labels[cell]] > 1 and qgroup_of[cell] != 0
            ]
            if not movable_lefts:
                stagnant += 1
                continue

            options: list[tuple[int, int, int]] = []
            for left in movable_lefts:
                qindex = qgroup_of[left]
                left_label = labels[left]
                for right in qgroups[qindex]:
                    if right == left:
                        continue
                    right_label = labels[right]
                    delta = 0
                    left_groups = set(cell_tc[left])
                    right_groups = set(cell_tc[right])
                    for tindex in left_groups | right_groups:
                        row = counts[tindex]
                        changes: dict[int, int] = {}
                        if tindex in left_groups:
                            changes[left_label] = changes.get(left_label, 0) - 1
                            changes[right_label] = changes.get(right_label, 0) + 1
                        if tindex in right_groups:
                            changes[right_label] = changes.get(right_label, 0) - 1
                            changes[left_label] = changes.get(left_label, 0) + 1
                        delta += sum(
                            (row[label] + change) * (row[label] + change - 1) // 2
                            - row[label] * (row[label] - 1) // 2
                            for label, change in changes.items()
                            if change
                        )
                    options.append((delta, left, right))

            minimum = min(delta for delta, _, _ in options)
            best = [item for item in options if item[0] == minimum]
            delta, left, right = rng.choice(best)
            left_label = labels[left]
            accept = delta <= 0
            if not accept:
                accept = rng.random() < math.exp(-delta / temperature)
            if not accept:
                stagnant += 1
                temperature = min(1.0, temperature * 1.00002)
                continue

            right_label = labels[right]
            left_groups = set(cell_tc[left])
            right_groups = set(cell_tc[right])
            for tindex in left_groups | right_groups:
                if tindex in left_groups:
                    counts[tindex][left_label] -= 1
                    counts[tindex][right_label] += 1
                if tindex in right_groups:
                    counts[tindex][right_label] -= 1
                    counts[tindex][left_label] += 1
                group_scores[tindex] = collision_score(counts[tindex])
            labels[left], labels[right] = right_label, left_label
            score += delta
            moves += 1

            if score < best_restart:
                best_restart = score
                stagnant = 0
                temperature = max(0.05, temperature * 0.98)
            else:
                stagnant += 1
            if score < best_global:
                best_global = score
            if progress and moves % progress == 0:
                if score != sum(group_scores):
                    raise AssertionError("incremental score drift")
                elapsed = time.monotonic() - started
                print(
                    f"moves={moves} restarts={restarts} "
                    f"score={score} best={best_global} elapsed={elapsed:.2f}",
                    flush=True,
                )
            if stagnant >= 100_000:
                break

    return None, moves, restarts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=300.0)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--progress", type=int, default=100_000)
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(__file__).with_name("cyclic_invariant_fan.txt"),
    )
    args = parser.parse_args()

    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)
    labels, moves, restarts = search(
        groups,
        args.seconds,
        args.seed,
        args.progress,
    )
    print(f"moves={moves}")
    print(f"restarts={restarts}")
    if labels is None:
        print("status=UNKNOWN")
        print("certificate=NONE")
        print("scope=timeout is not a nonexistence result")
        return
    verify_solution(labels, groups)
    args.certificate.write_text(
        "".join(f"{label}\n" for label in labels),
        encoding="ascii",
    )
    print("status=SAT")
    print(f"certificate={args.certificate}")
    print(f"orbit_cells={len(cells)}")
    print("semantic_verification=PASS")


if __name__ == "__main__":
    main()

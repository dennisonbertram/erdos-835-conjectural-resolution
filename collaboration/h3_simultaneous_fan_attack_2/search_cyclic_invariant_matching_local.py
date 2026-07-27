#!/usr/bin/env python3
"""Heuristically search for one C17-invariant perfect matching.

One cell is selected from each of the 228 Q-groups.  The collision score is
the sum of binomial(count, 2) over the 912 triple-colour groups.  Since the
selected cells have exactly 912 such incidences in total, score zero means
that every triple-colour group is hit exactly once.  A score-zero result is
verified semantically before the 228 selected orbit-cell indices are written.
Timeout or a nonzero score has no mathematical status.
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


QUAD_GROUPS = 228


def collision(count: int) -> int:
    return count * (count - 1) // 2


def verify_matching(
    selected: list[int],
    groups: tuple[tuple[int, ...], ...],
) -> None:
    chosen = set(selected)
    if len(chosen) != QUAD_GROUPS:
        raise AssertionError("matching repeats an orbit cell")
    if any(len(chosen & set(group)) != 1 for group in groups):
        raise AssertionError("candidate is not an exact transversal")


def search(
    groups: tuple[tuple[int, ...], ...],
    seconds: float,
    seed: int,
    progress: int,
) -> tuple[list[int] | None, list[int], int, int, int]:
    rng = random.Random(seed)
    qgroups = groups[:QUAD_GROUPS]
    tcgroups = groups[QUAD_GROUPS:]
    cell_count = sum(len(group) for group in qgroups)
    qgroup_of = [-1] * cell_count
    cell_tc: list[tuple[int, ...] | None] = [None] * cell_count
    for qindex, group in enumerate(qgroups):
        for cell in group:
            if qgroup_of[cell] != -1:
                raise AssertionError("Q-groups do not partition orbit cells")
            qgroup_of[cell] = qindex
    temporary_tc: list[list[int]] = [[] for _ in range(cell_count)]
    for tindex, group in enumerate(tcgroups):
        for cell in group:
            temporary_tc[cell].append(tindex)
    for cell, incidences in enumerate(temporary_tc):
        if len(incidences) != 4:
            raise AssertionError("orbit cell does not have four TC incidences")
        cell_tc[cell] = tuple(incidences)
    typed_cell_tc = [item for item in cell_tc if item is not None]
    if len(typed_cell_tc) != cell_count:
        raise AssertionError("incomplete cell incidence table")

    started = time.monotonic()
    deadline = started + seconds
    moves = 0
    restarts = 0
    best_global = 10**9
    best_selection: list[int] = []

    while time.monotonic() < deadline:
        restarts += 1
        selected = [rng.choice(group) for group in qgroups]
        counts = [0] * len(tcgroups)
        for cell in selected:
            for tindex in typed_cell_tc[cell]:
                counts[tindex] += 1
        score = sum(collision(count) for count in counts)
        if score < best_global:
            best_global = score
            best_selection = list(selected)
        stagnant = 0
        temperature = 0.3

        while time.monotonic() < deadline and stagnant < 40_000:
            if score == 0:
                verify_matching(selected, groups)
                return selected, list(selected), moves, restarts, 0
            bad = [index for index, count in enumerate(counts) if count > 1]
            if not bad:
                raise AssertionError("positive collision score without duplicates")
            bad_group = rng.choice(bad)
            selected_in_bad = [
                cell for cell in tcgroups[bad_group] if selected[qgroup_of[cell]] == cell
            ]
            if len(selected_in_bad) != counts[bad_group]:
                raise AssertionError("incremental matching state drift")

            options: list[tuple[int, int, int]] = []
            for old in selected_in_bad:
                qindex = qgroup_of[old]
                old_groups = set(typed_cell_tc[old])
                for new in qgroups[qindex]:
                    if new == old:
                        continue
                    new_groups = set(typed_cell_tc[new])
                    delta = 0
                    for tindex in old_groups | new_groups:
                        before = counts[tindex]
                        after = (
                            before
                            - int(tindex in old_groups)
                            + int(tindex in new_groups)
                        )
                        delta += collision(after) - collision(before)
                    options.append((delta, old, new))
            minimum = min(delta for delta, _, _ in options)
            best_options = [item for item in options if item[0] == minimum]
            delta, old, new = rng.choice(best_options)
            accept = delta <= 0 or rng.random() < math.exp(-delta / temperature)
            if not accept:
                stagnant += 1
                temperature = min(2.0, temperature * 1.0001)
                continue

            qindex = qgroup_of[old]
            for tindex in typed_cell_tc[old]:
                counts[tindex] -= 1
            for tindex in typed_cell_tc[new]:
                counts[tindex] += 1
            selected[qindex] = new
            score += delta
            moves += 1
            if score < best_global:
                best_global = score
                best_selection = list(selected)
                stagnant = 0
            else:
                stagnant += 1
            if delta < 0:
                temperature = max(0.05, temperature * 0.999)
            else:
                temperature = min(2.0, temperature * 1.00005)
            if progress and moves % progress == 0:
                exact_score = sum(collision(count) for count in counts)
                if score != exact_score:
                    raise AssertionError("incremental score drift")
                print(
                    f"moves={moves} restarts={restarts} score={score} "
                    f"best={best_global} elapsed={time.monotonic() - started:.2f}",
                    flush=True,
                )
    if not best_selection:
        raise AssertionError("search produced no best-effort assignment")
    return None, best_selection, moves, restarts, best_global


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--progress", type=int, default=100_000)
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(__file__).with_name("cyclic_invariant_matching.txt"),
    )
    parser.add_argument(
        "--best-effort",
        type=Path,
        help="optional 228-line Q-transversal hint; never a certificate",
    )
    args = parser.parse_args()

    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)
    selected, best_selection, moves, restarts, best = search(
        groups,
        args.seconds,
        args.seed,
        args.progress,
    )
    print(f"moves={moves}")
    print(f"restarts={restarts}")
    print(f"best_collision_score={best}")
    if selected is None:
        if args.best_effort is not None:
            args.best_effort.write_text(
                "".join(f"{cell}\n" for cell in best_selection),
                encoding="ascii",
            )
            print(f"best_effort={args.best_effort}")
        print("status=UNKNOWN")
        print("certificate=NONE")
        print("scope=timeout is not a nonexistence result")
        return
    verify_matching(selected, groups)
    args.certificate.write_text(
        "".join(f"{cell}\n" for cell in selected),
        encoding="ascii",
    )
    print("status=SAT")
    print(f"certificate={args.certificate}")
    print(f"selected_orbit_cells={len(selected)}")
    print(f"orbit_cell_universe={len(cells)}")
    print("semantic_verification=PASS")
    print("scope=one invariant matching only; not a 13-fan or #835 solution")


if __name__ == "__main__":
    main()

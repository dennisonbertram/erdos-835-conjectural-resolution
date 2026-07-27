#!/usr/bin/env python3
"""Screen a natural 272-member family of C17-invariant fan formulae.

For each quadruple, order its thirteen allowed link colours by a cyclic
coordinate based on a translation-covariant blend of the point barycentre and
the four face-colour barycentre.  The rank in that order is automatically
rainbow on every Q-group.  This script tests whether it is also rainbow on all
triple-colour groups.  Failure of the whole family is only an ansatz delimiter.
"""

from __future__ import annotations

from itertools import combinations

from verify_fan_kernel_reduction import (
    build_orbit_hypergraph,
    construct_large_set,
    verify_large_set,
)


MODULUS = 17
LABELS = 13
QUAD_GROUPS = 228


def inverse(value: int) -> int:
    return pow(value, -1, MODULUS)


def collision_score(labels: list[int], groups: tuple[tuple[int, ...], ...]) -> int:
    score = 0
    for group in groups:
        counts = [0] * LABELS
        for cell in group:
            counts[labels[cell]] += 1
        score += sum(count * (count - 1) // 2 for count in counts)
    return score


def labels_for_formula(
    colouring: dict[tuple[int, int, int], int],
    cells: tuple[tuple[tuple[int, int, int, int], int], ...],
    blend: int,
    multiplier: int,
) -> list[int]:
    labels = []
    for quad, colour in cells:
        finite = [point for point in quad if point < MODULUS]
        point_mean = sum(finite) * inverse(len(finite)) % MODULUS
        face_colours = {
            colouring[tuple(face)] for face in combinations(quad, 3)
        }
        if len(face_colours) != 4:
            raise AssertionError("quadruple does not have four face colours")
        face_mean = sum(face_colours) * inverse(4) % MODULUS
        anchor = (
            blend * point_mean + (1 - blend) * face_mean
        ) % MODULUS
        allowed = set(range(MODULUS)) - face_colours
        ordered = sorted(
            allowed,
            key=lambda value: multiplier * (value - anchor) % MODULUS,
        )
        labels.append(ordered.index(colour))
    return labels


def main() -> None:
    colouring = construct_large_set()
    verify_large_set(colouring)
    cells, groups = build_orbit_hypergraph(colouring)
    target = set(range(LABELS))
    best: tuple[int, int, int] | None = None
    for blend in range(MODULUS):
        for multiplier in range(1, MODULUS):
            labels = labels_for_formula(colouring, cells, blend, multiplier)
            if any(
                {labels[cell] for cell in group} != target
                for group in groups[:QUAD_GROUPS]
            ):
                raise AssertionError("formula is not rainbow on a Q-group")
            score = collision_score(labels, groups[QUAD_GROUPS:])
            candidate = score, blend, multiplier
            if best is None or candidate < best:
                best = candidate
                print(
                    f"best_score={score} blend={blend} multiplier={multiplier}",
                    flush=True,
                )
            if score == 0:
                if any(
                    {labels[cell] for cell in group} != target for group in groups
                ):
                    raise AssertionError("zero-score formula failed semantic check")
                print("status=SAT")
                print("semantic_verification=PASS")
                return
    if best is None:
        raise AssertionError("empty formula screen")
    print("status=NO_WITNESS_IN_FAMILY")
    print("formulae_checked=272")
    print(f"best_score={best[0]}")
    print(f"best_blend={best[1]}")
    print(f"best_multiplier={best[2]}")
    print("scope=finite ansatz exclusion only; not an UNSAT result")


if __name__ == "__main__":
    main()

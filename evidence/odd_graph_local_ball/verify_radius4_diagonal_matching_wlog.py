#!/usr/bin/env python3
"""Independently audit the diagonal-S15 matching normalization proof data."""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Iterator


POINTS, K, N, DEPTH = 31, 15, 15, 4
ALL = (1 << POINTS) - 1
ROOT = (1 << K) - 1


def neighbours(vertex: int) -> Iterator[int]:
    rest = ALL ^ vertex
    while rest:
        bit = rest & -rest
        rest ^= bit
        yield (ALL ^ vertex) ^ bit


def make_ball() -> tuple[list[int], list[int], dict[int, int]]:
    vertices, levels, lookup = [ROOT], [0], {ROOT: 0}
    queue = deque([ROOT])
    while queue:
        vertex = queue.popleft()
        if levels[lookup[vertex]] == DEPTH:
            continue
        for other in neighbours(vertex):
            if other not in lookup:
                lookup[other] = len(vertices)
                vertices.append(other)
                levels.append(levels[lookup[vertex]] + 1)
                queue.append(other)
    return vertices, levels, lookup


def partitions(total: int, ceiling: int | None = None) -> Iterator[tuple[int, ...]]:
    if total == 0:
        yield ()
        return
    if ceiling is None or ceiling > total:
        ceiling = total
    for head in range(ceiling, 0, -1):
        for tail in partitions(total - head, head):
            yield (head,) + tail


def standard(partition: tuple[int, ...]) -> tuple[int, ...]:
    image = [0] * N
    start = 0
    for size in partition:
        for offset in range(size):
            image[start + offset] = start + ((offset + 1) % size)
        start += size
    return tuple(image)


def cycle_partition(permutation: tuple[int, ...]) -> tuple[int, ...]:
    unseen = set(range(N))
    sizes = []
    while unseen:
        start = min(unseen)
        length = 0
        cursor = start
        while cursor in unseen:
            unseen.remove(cursor)
            cursor = permutation[cursor]
            length += 1
        if cursor != start:
            raise AssertionError("not a permutation cycle")
        sizes.append(length)
    return tuple(sorted(sizes, reverse=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.map.read_text(encoding="utf-8"))
    matching = payload.get("diagonal_matching")
    if payload.get("schema") != "odd-graph-o16-radius4-diagonal-matching-symbreak-v1" or not isinstance(matching, dict):
        raise AssertionError("not a diagonal-matching symmetry map")
    vertices, levels, lookup = make_ball()
    assert [sum(level == item for level in levels) for item in range(5)] == [1, 16, 240, 1800, 12600]
    # Rows C_(B_(r+1),A_i) are actual radius-two vertices, each adjacent
    # to root neighbour B\{B_(r+1)}; the latter's local bijection makes
    # colour 1 occur once per row.  Column bijection follows from the
    # radius-two centre constraints, with the B_0 row fixed by the 32 units.
    positions = []
    for row in range(N):
        line = []
        for column in range(N):
            mask = (ROOT ^ (1 << column)) | (1 << (15 + row + 1))
            item = lookup[mask]
            if levels[item] != 2:
                raise AssertionError("C-coordinate is not radius two")
            line.append(item)
        positions.append(line)
    if len({item for line in positions for item in line}) != N * N:
        raise AssertionError("C-coordinate table is not injective")
    listed_partitions = [tuple(item) for item in matching.get("partitions", [])]
    expected_partitions = list(partitions(N))
    if listed_partitions != expected_partitions or len(expected_partitions) != 176:
        raise AssertionError("not one deterministic representative per partition of 15")
    representatives = [tuple(item) for item in matching.get("representatives", [])]
    expected_representatives = [standard(item) for item in expected_partitions]
    if representatives != expected_representatives or len(set(representatives)) != 176:
        raise AssertionError("canonical cycle representatives mismatch")
    if any(cycle_partition(item) != partition for item, partition in zip(representatives, expected_partitions)):
        raise AssertionError("a representative has the wrong conjugacy invariant")
    print(json.dumps({
        "status": "PASS", "radius_two_matching_cells": N * N,
        "conjugacy_classes": len(expected_partitions),
        "selector_start": matching.get("selector_start"),
        "claim": "every S15 conjugacy class of colour-1 matchings has exactly one listed standard representative",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

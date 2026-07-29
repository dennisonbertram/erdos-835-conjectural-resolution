#!/usr/bin/env python3
"""Independent direct edge-colouring check of every EH pair link.

Unlike ``screen_pair_links.py``, this verifier never enumerates perfect
matchings.  It assigns one of five colours directly to each of the 45 edges,
propagates singleton colour domains, and branches on a minimum-domain edge.
The five incident edges at vertex zero are precoloured without loss of
generality by global colour permutation.  Every returned colouring is checked
from scratch.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path
from typing import Optional


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "evidence" / "ls_3_4_20_eh15_seed.txt"
SOURCE_SHA256 = "b1ea090d3e3b88366c87e95660c1c82a406d2c3b100cc1d39bcc2c7e8fde47f9"
POINTS = tuple(range(20))
BLOCKS = tuple(itertools.combinations(POINTS, 4))
PAIRS = tuple(itertools.combinations(POINTS, 2))
ALL_COLOURS = (1 << 5) - 1


def load_index() -> dict[
    tuple[int, int],
    list[tuple[tuple[int, ...], int]],
]:
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise AssertionError("authenticated EH source hash changed")
    lines = SOURCE.read_text(encoding="ascii").splitlines()
    if len(lines) != len(BLOCKS):
        raise AssertionError("EH source does not have 4,845 rows")
    answer = {pair: [] for pair in PAIRS}
    labels = Counter()
    for expected, raw in zip(BLOCKS, lines):
        fields = tuple(map(int, raw.split()))
        if len(fields) != 5 or fields[:4] != expected:
            raise AssertionError("EH source is malformed or out of order")
        label = fields[4]
        labels[label] += 1
        for pair in itertools.combinations(expected, 2):
            answer[pair].append((expected, label))
    if labels != Counter({label: 285 for label in range(17)}):
        raise AssertionError("EH source colour counts changed")
    return answer


def link_edges(
    indexed: dict[
        tuple[int, int],
        list[tuple[tuple[int, ...], int]],
    ],
    dropped: tuple[int, int, int],
    pair: tuple[int, int],
) -> tuple[tuple[int, int], ...]:
    vertices = [point for point in POINTS if point not in pair]
    position = {point: index for index, point in enumerate(vertices)}
    labels = set(dropped) | {15, 16}
    edges = []
    for block, label in indexed[pair]:
        if label in labels:
            outside = [point for point in block if point not in pair]
            edges.append(tuple(sorted(position[x] for x in outside)))
    edges = tuple(sorted(edges))
    degrees = Counter(vertex for edge in edges for vertex in edge)
    if (
        len(edges) != 45
        or len(set(edges)) != 45
        or degrees != Counter({vertex: 5 for vertex in range(18)})
    ):
        raise AssertionError("constructed link is not simple and 5-regular")
    return edges


def colour_link(
    edges: tuple[tuple[int, int], ...],
) -> tuple[Optional[tuple[int, ...]], int]:
    incidence: list[list[int]] = [[] for _ in range(18)]
    for edge_index, (left, right) in enumerate(edges):
        incidence[left].append(edge_index)
        incidence[right].append(edge_index)
    colours = [-1] * len(edges)
    used = [0] * 18
    nodes = 0

    def assign(edge_index: int, colour: int) -> bool:
        left, right = edges[edge_index]
        bit = 1 << colour
        if (used[left] | used[right]) & bit:
            return False
        colours[edge_index] = colour
        used[left] |= bit
        used[right] |= bit
        return True

    # Every proper edge-colouring differs by a global colour permutation from
    # one with these five assignments.
    for colour, edge_index in enumerate(sorted(incidence[0])):
        if not assign(edge_index, colour):
            raise AssertionError("initial colour normalization failed")

    def recurse() -> bool:
        nonlocal nodes
        nodes += 1
        forced: list[tuple[int, int]] = []
        while True:
            changed = False
            best_edge = -1
            best_domain = 0
            best_size = 6
            for edge_index, (left, right) in enumerate(edges):
                if colours[edge_index] >= 0:
                    continue
                domain = ALL_COLOURS & ~(used[left] | used[right])
                size = sum(bool(domain & (1 << colour)) for colour in range(5))
                if size == 0:
                    for undo_edge, undo_colour in reversed(forced):
                        a, b = edges[undo_edge]
                        colours[undo_edge] = -1
                        used[a] ^= 1 << undo_colour
                        used[b] ^= 1 << undo_colour
                    return False
                if size == 1:
                    colour = (domain & -domain).bit_length() - 1
                    if not assign(edge_index, colour):
                        raise AssertionError("singleton assignment failed")
                    forced.append((edge_index, colour))
                    changed = True
                    break
                if size < best_size:
                    best_edge = edge_index
                    best_domain = domain
                    best_size = size
            if not changed:
                break

        if best_edge < 0:
            return True
        left, right = edges[best_edge]
        for colour in range(5):
            if not (best_domain & (1 << colour)):
                continue
            colours[best_edge] = colour
            used[left] |= 1 << colour
            used[right] |= 1 << colour
            if recurse():
                return True
            colours[best_edge] = -1
            used[left] ^= 1 << colour
            used[right] ^= 1 << colour

        for undo_edge, undo_colour in reversed(forced):
            a, b = edges[undo_edge]
            colours[undo_edge] = -1
            used[a] ^= 1 << undo_colour
            used[b] ^= 1 << undo_colour
        return False

    found = recurse()
    return (tuple(colours) if found else None), nodes


def verify_colouring(
    edges: tuple[tuple[int, int], ...],
    colours: tuple[int, ...],
) -> None:
    if len(colours) != 45 or not set(colours) <= set(range(5)):
        raise AssertionError("edge colouring has the wrong shape")
    for vertex in range(18):
        incident = [
            colours[index] for index, edge in enumerate(edges) if vertex in edge
        ]
        if sorted(incident) != list(range(5)):
            raise AssertionError("edge colouring is not rainbow at a vertex")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--receipt",
        type=Path,
        default=HERE / "pair_link_screen_receipt.json",
    )
    args = parser.parse_args()
    receipt = json.loads(args.receipt.read_text(encoding="ascii"))
    if (
        receipt.get("source_sha256") != SOURCE_SHA256
        or receipt.get("cases") != 455
        or receipt.get("links_checked") != 86_450
    ):
        raise AssertionError("receipt is not the claimed complete 455-case run")

    indexed = load_index()
    digest = hashlib.sha256()
    maximum = (0, None, None)
    checked = 0
    started = time.time()
    for dropped in itertools.combinations(range(15), 3):
        for pair in PAIRS:
            edges = link_edges(indexed, dropped, pair)
            colours, nodes = colour_link(edges)
            if colours is None:
                raise AssertionError(
                    f"direct search rejected drop={dropped}, pair={pair}"
                )
            verify_colouring(edges, colours)
            checked += 1
            if nodes > maximum[0]:
                maximum = (nodes, dropped, pair)
            digest.update(
                json.dumps(
                    {
                        "drop": dropped,
                        "pair": pair,
                        "edges": edges,
                        "colours": colours,
                    },
                    separators=(",", ":"),
                ).encode("ascii")
            )
        if checked % (50 * len(PAIRS)) == 0:
            print(f"independently verified links={checked}", flush=True)

    if checked != 86_450:
        raise AssertionError("did not check all 455*190 links")
    print("PASS: direct edge-colouring verifier found and checked all 86,450 links")
    print(f"direct-colouring SHA-256: {digest.hexdigest()}")
    print(
        "maximum direct-search nodes: "
        f"{maximum[0]} at drop={maximum[1]}, pair={maximum[2]}"
    )
    print(f"elapsed seconds: {time.time() - started:.6f}")
    print(
        "SCOPE: every pair link passes this necessary condition; "
        "no global five-colouring or LS(3,4,20) is implied."
    )


if __name__ == "__main__":
    main()

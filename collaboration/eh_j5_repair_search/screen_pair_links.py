#!/usr/bin/env python3
"""Exact perfect-matching screen for every EH twelve-core pair link.

For a dropped triple of EH systems and a point pair W, the five-fold leave
induces a simple 5-regular graph on the other eighteen points.  A global
five-colouring would decompose this link into five perfect matchings.

This standard-library program searches exactly by anchoring one edge in the
first perfect matching, enumerating every possible completion of that
matching, and recursing on the residual regular graph.  It stops at the first
factorization when one exists; if none exists, the finite recursion has
exhausted every possible ordered factorization (the anchor loses no
generality because every edge belongs to one factor).
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path
from typing import Iterable, Optional


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "evidence" / "ls_3_4_20_eh15_seed.txt"
SOURCE_SHA256 = "b1ea090d3e3b88366c87e95660c1c82a406d2c3b100cc1d39bcc2c7e8fde47f9"
POINTS = tuple(range(20))
BLOCKS = tuple(itertools.combinations(POINTS, 4))
PAIRS = tuple(itertools.combinations(POINTS, 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_source() -> list[tuple[tuple[int, ...], int]]:
    if sha256(SOURCE) != SOURCE_SHA256:
        raise AssertionError("authenticated EH source hash changed")
    rows = []
    for expected, raw in zip(BLOCKS, SOURCE.read_text(encoding="ascii").splitlines()):
        fields = tuple(map(int, raw.split()))
        if len(fields) != 5 or fields[:4] != expected:
            raise AssertionError("EH source is malformed or out of order")
        rows.append((expected, fields[4]))
    if len(rows) != len(BLOCKS):
        raise AssertionError("EH source does not have 4,845 blocks")
    if Counter(label for _, label in rows) != Counter(
        {label: 285 for label in range(17)}
    ):
        raise AssertionError("EH source colour counts changed")
    return rows


def pair_index(
    rows: list[tuple[tuple[int, ...], int]],
) -> dict[tuple[int, int], list[tuple[tuple[int, ...], int]]]:
    answer = {pair: [] for pair in PAIRS}
    for block, label in rows:
        for pair in itertools.combinations(block, 2):
            answer[pair].append((block, label))
    if set(map(len, answer.values())) != {153}:
        raise AssertionError("a pair does not lie in exactly C(18,2) blocks")
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
    leave_labels = set(dropped) | {15, 16}
    edges = []
    for block, label in indexed[pair]:
        if label not in leave_labels:
            continue
        outside = [point for point in block if point not in pair]
        if len(outside) != 2:
            raise AssertionError("pair index contains a malformed block")
        edges.append(tuple(sorted(position[point] for point in outside)))
    edges = sorted(edges)
    if len(edges) != 45 or len(set(edges)) != 45:
        raise AssertionError("link is not a simple 45-edge graph")
    degrees = Counter(vertex for edge in edges for vertex in edge)
    if degrees != Counter({vertex: 5 for vertex in range(18)}):
        raise AssertionError("link is not 5-regular on eighteen vertices")
    return tuple(edges)


def factor_link(
    edges: tuple[tuple[int, int], ...],
) -> tuple[Optional[tuple[int, ...]], int, int]:
    """Return five factor masks, residual-state count, and PM branch count."""

    if len(edges) != 45:
        raise AssertionError("factor_link expects 45 edges")
    incidence = [0] * 18
    for index, (left, right) in enumerate(edges):
        incidence[left] |= 1 << index
        incidence[right] |= 1 << index
    all_vertices = (1 << 18) - 1
    states = 0
    matching_branches = 0

    def two_factor(mask: int) -> Optional[tuple[int, int]]:
        """Alternately split every even cycle of a 2-regular graph."""

        unseen = all_vertices
        factors = [0, 0]
        while unseen:
            start_bit = unseen & -unseen
            start = start_bit.bit_length() - 1
            vertex = start
            previous_edge = -1
            parity = 0
            length = 0
            while True:
                unseen &= ~(1 << vertex)
                available = incidence[vertex] & mask
                candidates = []
                while available:
                    edge_bit = available & -available
                    edge_index = edge_bit.bit_length() - 1
                    available -= edge_bit
                    if edge_index != previous_edge:
                        candidates.append(edge_index)
                if not candidates:
                    raise AssertionError("residual is not 2-regular")
                edge_index = min(candidates)
                factors[parity] |= 1 << edge_index
                parity ^= 1
                length += 1
                left, right = edges[edge_index]
                next_vertex = right if left == vertex else left
                previous_edge, vertex = edge_index, next_vertex
                if vertex == start:
                    break
            if length % 2:
                return None
        return factors[0], factors[1]

    @functools.lru_cache(maxsize=None)
    def recurse(mask: int, degree: int) -> Optional[tuple[int, ...]]:
        nonlocal states, matching_branches
        states += 1
        if degree == 1:
            return (mask,)
        if degree == 2:
            return two_factor(mask)

        # Any factorization has a unique factor containing this edge, so that
        # factor may be ordered first without loss of generality.
        anchor_bit = mask & -mask
        anchor_index = anchor_bit.bit_length() - 1
        left, right = edges[anchor_index]
        unmatched = all_vertices & ~(1 << left) & ~(1 << right)

        def extend_matching(
            remaining_vertices: int,
            matching: int,
        ) -> Optional[tuple[int, ...]]:
            nonlocal matching_branches
            if not remaining_vertices:
                matching_branches += 1
                tail = recurse(mask ^ matching, degree - 1)
                if tail is not None:
                    return (matching,) + tail
                return None

            # Minimum remaining induced degree is an exact fail-first choice.
            best_vertex = -1
            best_options: Optional[list[tuple[int, int]]] = None
            scan = remaining_vertices
            while scan:
                vertex_bit = scan & -scan
                vertex = vertex_bit.bit_length() - 1
                scan -= vertex_bit
                options = []
                candidates = incidence[vertex] & mask
                while candidates:
                    edge_bit = candidates & -candidates
                    edge_index = edge_bit.bit_length() - 1
                    candidates -= edge_bit
                    a, b = edges[edge_index]
                    neighbour = b if a == vertex else a
                    if remaining_vertices & (1 << neighbour):
                        options.append((neighbour, edge_bit))
                if not options:
                    return None
                if best_options is None or len(options) < len(best_options):
                    best_vertex = vertex
                    best_options = options

            if best_options is None:
                raise AssertionError("nonempty vertex set has no chosen vertex")
            for neighbour, edge_bit in best_options:
                result = extend_matching(
                    remaining_vertices & ~(1 << best_vertex) & ~(1 << neighbour),
                    matching | edge_bit,
                )
                if result is not None:
                    return result
            return None

        return extend_matching(unmatched, anchor_bit)

    factors = recurse((1 << len(edges)) - 1, 5)
    return factors, states, matching_branches


def verify_factors(
    edges: tuple[tuple[int, int], ...],
    factors: tuple[int, ...],
) -> None:
    if len(factors) != 5:
        raise AssertionError("factorization does not have five factors")
    union = 0
    for factor in factors:
        if union & factor:
            raise AssertionError("factors overlap")
        union |= factor
        degrees = Counter()
        for edge_index, (left, right) in enumerate(edges):
            if factor & (1 << edge_index):
                degrees[left] += 1
                degrees[right] += 1
        if degrees != Counter({vertex: 1 for vertex in range(18)}):
            raise AssertionError("a factor is not a perfect matching")
    if union != (1 << len(edges)) - 1:
        raise AssertionError("factors do not cover the link")


def parse_case(text: str) -> tuple[int, int, int]:
    try:
        case = tuple(sorted(map(int, text.split(","))))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("case must look like 1,3,8") from exc
    if len(case) != 3 or len(set(case)) != 3 or case[0] < 0 or case[-1] >= 15:
        raise argparse.ArgumentTypeError("case needs three distinct labels in 0,...,14")
    return case


def selected_cases(
    explicit: Iterable[tuple[int, int, int]],
) -> list[tuple[int, int, int]]:
    cases = list(dict.fromkeys(explicit))
    return cases or list(itertools.combinations(range(15), 3))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=parse_case, action="append", default=[])
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument(
        "--receipt",
        type=Path,
        default=HERE / "pair_link_screen_receipt.json",
    )
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("--limit must be nonnegative")

    rows = load_source()
    indexed = pair_index(rows)
    cases = selected_cases(args.case)
    if args.limit:
        cases = cases[: args.limit]

    started = time.time()
    factorization_hash = hashlib.sha256()
    state_histogram: Counter[int] = Counter()
    total_states = 0
    total_matching_branches = 0
    maximum = (0, None, None, 0)
    rejected: list[dict[str, object]] = []
    checked_links = 0

    for case_number, dropped in enumerate(cases, 1):
        for pair in PAIRS:
            edges = link_edges(indexed, dropped, pair)
            factors, states, matching_branches = factor_link(edges)
            checked_links += 1
            total_states += states
            total_matching_branches += matching_branches
            state_histogram[states] += 1
            if states > maximum[0]:
                maximum = (states, dropped, pair, matching_branches)
            if factors is None:
                rejected.append(
                    {
                        "drop": list(dropped),
                        "pair": list(pair),
                        "states": states,
                        "matching_branches": matching_branches,
                    }
                )
                break
            verify_factors(edges, factors)
            factorization_hash.update(
                json.dumps(
                    {
                        "drop": dropped,
                        "pair": pair,
                        "edges": edges,
                        "factors": factors,
                    },
                    separators=(",", ":"),
                ).encode("ascii")
            )
        if case_number % 50 == 0 or case_number == len(cases):
            print(
                f"cases={case_number}/{len(cases)} links={checked_links} "
                f"rejected={len(rejected)}",
                flush=True,
            )

    receipt = {
        "schema": 1,
        "source": str(SOURCE.relative_to(REPO)),
        "source_sha256": SOURCE_SHA256,
        "cases": len(cases),
        "links_checked": checked_links,
        "links_per_completed_case": len(PAIRS),
        "rejected_cases": rejected,
        "factorable_links": checked_links - len(rejected),
        "factorization_sha256": factorization_hash.hexdigest(),
        "total_residual_states": total_states,
        "total_perfect_matching_branches": total_matching_branches,
        "maximum_residual_states": {
            "states": maximum[0],
            "drop": list(maximum[1]) if maximum[1] is not None else None,
            "pair": list(maximum[2]) if maximum[2] is not None else None,
            "matching_branches": maximum[3],
        },
        "state_histogram": {
            str(states): count for states, count in sorted(state_histogram.items())
        },
        "elapsed_seconds": round(time.time() - started, 6),
        "scope": (
            "Exact necessary-condition screen only. A factorable pair link "
            "does not imply a global five-colouring or LS(3,4,20)."
        ),
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

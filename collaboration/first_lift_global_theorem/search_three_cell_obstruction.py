#!/usr/bin/env python3
"""Search a finite family of three-cell weighted obstructions for class B.

Exploratory only: a reported positive margin is a compact candidate
certificate and must be reconstructed as an actual support matrix and
independently verified before it is cited.  A nonpositive finite run is not a
universal theorem.  The dynamic program deliberately relaxes the five
missing-colours-per-vertex condition to its aggregate total in each cell, so a
positive result would still require realization and verification.
"""

from __future__ import annotations

import argparse
import functools
import itertools
import random


def profiles():
    # (n5,n3,n1), equivalently q=n_12 in the repository's notation.
    return [(7 + q, 10 - 2 * q, q) for q in range(6)]


def types_for(missing, cell_sizes):
    out = []
    for d0 in range(min(missing, cell_sizes[0]) + 1):
        for d1 in range(min(missing - d0, cell_sizes[1]) + 1):
            d2 = missing - d0 - d1
            if 0 <= d2 <= cell_sizes[2]:
                out.append((d0, d1, d2))
    return out


def min_matching_weight(attendance, weights):
    @functools.lru_cache(maxsize=None)
    def rec(state):
        if sum(state) == 0:
            return 0
        first = next(i for i, value in enumerate(state) if value)
        reduced = list(state)
        reduced[first] -= 1
        best = None
        for other in range(first, 3):
            if reduced[other] == 0:
                continue
            nxt = reduced[:]
            nxt[other] -= 1
            pair = (first, other)
            value = weights[pair] + rec(tuple(nxt))
            if best is None or value < best:
                best = value
        assert best is not None
        return best

    return rec(tuple(attendance))


def optimize(cell_sizes, profile, weights):
    target = tuple(5 * size for size in cell_sizes)
    order = [5] * profile[0] + [3] * profile[1] + [1] * profile[2]
    type_lists = {m: types_for(m, cell_sizes) for m in (1, 3, 5)}
    value = {}
    for m in (1, 3, 5):
        for d in type_lists[m]:
            attendance = tuple(cell_sizes[i] - d[i] for i in range(3))
            assert sum(attendance) % 2 == 0
            value[m, d] = min_matching_weight(attendance, weights)

    states = {(0, 0, 0): (0, ())}
    for m in order:
        nxt = {}
        for used, (base, history) in states.items():
            for d in type_lists[m]:
                total = tuple(used[i] + d[i] for i in range(3))
                if any(total[i] > target[i] for i in range(3)):
                    continue
                candidate = base + value[m, d]
                if total not in nxt or candidate > nxt[total][0]:
                    nxt[total] = (candidate, history + (d,))
        states = nxt
    return states.get(target)


def complete_graph_weight(cell_sizes, weights):
    total = 0
    for i in range(3):
        total += cell_sizes[i] * (cell_sizes[i] - 1) // 2 * weights[i, i]
        for j in range(i + 1, 3):
            total += cell_sizes[i] * cell_sizes[j] * weights[i, j]
    return total


def normalized_weights(values):
    pairs = ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2))
    return dict(zip(pairs, values))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--max-weight", type=int, default=8)
    args = parser.parse_args()
    rng = random.Random(args.seed)

    partitions = [
        cells
        for cells in itertools.combinations_with_replacement(range(1, 12), 3)
        if sum(cells) == 13
    ]
    fixed = [
        (0, 0, 0, 0, 0, 1),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 1, 0, 0, 0),
        (0, 1, 0, 0, 0, 0),
        (1, 0, 0, 0, 0, 0),
        (0, 1, 2, 0, 3, 0),
    ]
    random_values = [
        tuple(rng.randrange(args.max_weight + 1) for _ in range(6))
        for _ in range(args.samples)
    ]
    checked = 0
    best = None
    for cells in partitions:
        for profile in profiles():
            for values in fixed + random_values:
                if not any(values):
                    continue
                weights = normalized_weights(values)
                got = optimize(cells, profile, weights)
                assert got is not None
                demand, history = got
                supply = complete_graph_weight(cells, weights)
                margin = demand - supply
                checked += 1
                record = (margin, cells, profile, values, history)
                if best is None or record[0] > best[0]:
                    best = record
                if margin > 0:
                    print("CANDIDATE", record)
                    return 2
    print(f"checked={checked} best={best[:4]}")
    print("finite weighted three-cell search only; no universal conclusion")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

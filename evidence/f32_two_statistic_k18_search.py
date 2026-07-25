#!/usr/bin/env python3
"""Deterministic search for an actual-edge K18 in the (e1, lambda) quotient.

For a 16-set S in F_32 put

    a(S) = e_1(S),  lambda(S) = e_8(S) + a(S)^8.

Every sampled 17-set R gives 17 pairwise adjacent 16-sets R - {x}.  The
script inserts the corresponding quotient edges, searches the accumulated
1024-vertex graph for a clique of size 18, and prints one exact 17-set
witness for each of its 153 edges.

The search is only a certificate finder.  The separately generated verifier
must recompute every statistic and adjacency relation from the printed sets.
"""

from __future__ import annotations

import argparse
import random
from itertools import combinations


MODULUS = 0b100101  # X^5 + X^2 + 1


def multiply(left: int, right: int) -> int:
    answer = 0
    while right:
        if right & 1:
            answer ^= left
        right >>= 1
        left <<= 1
        if left & 32:
            left ^= MODULUS
    return answer & 31


PRODUCT = tuple(tuple(multiply(x, y) for y in range(32)) for x in range(32))


def power(value: int, exponent: int) -> int:
    answer = 1
    while exponent:
        if exponent & 1:
            answer = PRODUCT[answer][value]
        value = PRODUCT[value][value]
        exponent >>= 1
    return answer


POWER8 = tuple(power(x, 8) for x in range(32))


def trace(value: int) -> int:
    answer = 0
    current = value
    for _ in range(5):
        answer ^= current
        current = PRODUCT[current][current]
    assert answer in (0, 1)
    return answer


def prefix_for_points(points: list[int]) -> tuple[int, ...]:
    """Return elementary coefficients e_0,...,e_8."""

    result = [1] + [0] * 8
    for point in points:
        for degree in range(8, 0, -1):
            result[degree] ^= PRODUCT[point][result[degree - 1]]
    return tuple(result)


def deletion_states(points: list[int]) -> list[int]:
    """Return state ids 32*e1 + lambda for all 16-point deletions."""

    root = prefix_for_points(points)
    states = []
    for deleted in points:
        quotient = [1]
        for degree in range(1, 9):
            # E_R = E_(R-{x}) (1+x*t), hence q_j = r_j + x*q_(j-1).
            quotient.append(root[degree] ^ PRODUCT[deleted][quotient[-1]])
        first = quotient[1]
        lam = quotient[8] ^ POWER8[first]
        states.append(32 * first + lam)
    assert len(states) == len(set(states))
    return states


def greedy_clique(
    adjacency: list[int], target: int, rng: random.Random, restarts: int
) -> list[int] | None:
    """Randomized greedy search, exploiting the dense sampled graph."""

    vertices = [vertex for vertex, neighbors in enumerate(adjacency) if neighbors]
    for _ in range(restarts):
        first = rng.choice(vertices)
        clique = [first]
        candidates = adjacency[first]
        while candidates and len(clique) < target:
            choices = []
            bits = candidates
            while bits:
                bit = bits & -bits
                vertex = bit.bit_length() - 1
                choices.append(vertex)
                bits ^= bit
            # Prefer the vertex retaining the most current candidates.  Random
            # jitter breaks ties without changing deterministic reproducibility.
            rng.shuffle(choices)
            vertex = max(
                choices,
                key=lambda item: (adjacency[item] & candidates).bit_count(),
            )
            clique.append(vertex)
            candidates &= adjacency[vertex]
        if len(clique) >= target:
            return clique[:target]
    return None


def format_mask(mask: int) -> str:
    return "{" + ", ".join(str(x) for x in range(32) if mask >> x & 1) + "}"


def find_trace_clique_extension(args: argparse.Namespace) -> None:
    """Extend the known trace-hyperplane K17 by one quotient vertex."""

    lam = args.trace_extension
    if lam == 0:
        raise SystemExit("--trace-extension must be nonzero")
    b = power(lam, 27)  # lambda^(-4) in the order-31 group
    base_roots = sorted(
        {0}
        | {
            x
            for x in range(1, 32)
            if trace(PRODUCT[b][x]) == 1
        }
    )
    base_states = deletion_states(base_roots)
    assert base_states == [32 * a + lam for a in base_roots]
    base = set(base_states)

    connections = [set() for _ in range(1024)]
    witnesses: dict[tuple[int, int], int] = {}
    rng = random.Random(args.seed)
    extension = None

    for sample_number in range(1, args.samples + 1):
        points = sorted(rng.sample(range(32), 17))
        mask = sum(1 << point for point in points)
        states = deletion_states(points)
        for base_state in base.intersection(states):
            for state in states:
                if state != base_state:
                    connections[state].add(base_state)
                    witnesses.setdefault((base_state, state), mask)

        if sample_number % args.batch == 0:
            count, candidate = max(
                (len(connections[state]), state)
                for state in range(1024)
                if state not in base
            )
            print(
                f"samples={sample_number} best_extension_edges={count} "
                f"candidate=({candidate // 32}, {candidate % 32})"
            )
            if count == 17:
                extension = candidate
                break

    if extension is None:
        raise SystemExit("no extension of the trace K17 found")

    print("BASE_ROOTS =", base_roots)
    print("EXTERNAL_STATE =", (extension // 32, extension % 32))
    print("EXTENSION_WITNESS_MASKS = [")
    for base_state in base_states:
        mask = witnesses[(base_state, extension)]
        encoded = str(mask) if args.compact else format_mask(mask)
        print(f"    {encoded},")
    print("]")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=835)
    parser.add_argument("--samples", type=int, default=200_000)
    parser.add_argument("--batch", type=int, default=2_000)
    parser.add_argument("--restarts", type=int, default=10_000)
    parser.add_argument("--target", type=int, default=18)
    parser.add_argument(
        "--compact",
        action="store_true",
        help="print each 17-set witness as a 32-bit integer mask",
    )
    parser.add_argument(
        "--trace-extension",
        type=int,
        metavar="LAMBDA",
        help="search only for one vertex extending the trace K17 in this layer",
    )
    args = parser.parse_args()

    if args.trace_extension is not None:
        find_trace_clique_extension(args)
        return

    rng = random.Random(args.seed)
    adjacency = [0] * 1024
    witnesses: dict[tuple[int, int], int] = {}
    clique = None

    for sample_number in range(1, args.samples + 1):
        points = sorted(rng.sample(range(32), 17))
        mask = sum(1 << point for point in points)
        states = deletion_states(points)
        for left, right in combinations(states, 2):
            if left > right:
                left, right = right, left
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
            witnesses.setdefault((left, right), mask)

        if sample_number % args.batch == 0:
            clique = greedy_clique(
                adjacency, args.target, rng, args.restarts // 10
            )
            edge_count = sum(bits.bit_count() for bits in adjacency) // 2
            print(
                f"samples={sample_number} edges={edge_count} "
                f"density={edge_count / 507904:.6f} "
                f"clique={0 if clique is None else len(clique)}"
            )
            if clique is not None:
                break

    if clique is None:
        clique = greedy_clique(adjacency, args.target, rng, args.restarts)
    if clique is None:
        raise SystemExit(f"no K{args.target} found")

    clique.sort(key=lambda state: state // 32)
    print("CLIQUE_STATES = [")
    for state in clique:
        print(f"    ({state // 32}, {state % 32}),")
    print("]")
    print("EDGE_WITNESSES = [")
    for left_index, right_index in combinations(range(len(clique)), 2):
        left = clique[left_index]
        right = clique[right_index]
        key = tuple(sorted((left, right)))
        mask = witnesses[key]
        encoded = str(mask) if args.compact else format_mask(mask)
        print(
            f"    ({left_index}, {right_index}, "
            f"{encoded}),"
        )
    print("]")


if __name__ == "__main__":
    main()

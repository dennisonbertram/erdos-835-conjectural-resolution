#!/usr/bin/env python3
"""Exact cyclic search for the descended p=17 four-Pfaffian condition.

For n=p+3, let A be a skew-circulant n by n matrix over F_p:

    A[i,j] = f(j-i mod n),  f(-d)=-f(d),  f(n/2)=0.

The row sum is automatically zero.  The required condition is tested
directly, rather than through moments: for every triple T, the p values
Pf A[T union {u}], u not in T, must be pairwise distinct.

The p=5,7,11 runs exhaust the *projective* cyclic parameter space.  A
global nonzero scaling only scales all four-Pfaffians by its square, hence
preserves the predicate.  At p=17 the space has
(17^9-1)/16 = 7,411,742,281 projective points, so the default is a
deterministic sample.

This searches a structured subfamily only.  Failure is not an impossibility
result for arbitrary alternating matrices.
"""

from __future__ import annotations

import argparse
import itertools
import random
from collections.abc import Iterator


def cyclic_orbit_representatives(n: int) -> list[tuple[int, int, int]]:
    """One representative of each translation orbit of 3-subsets of Z/nZ."""
    unseen = set(itertools.combinations(range(n), 3))
    representatives = []
    while unseen:
        triple = min(unseen)
        orbit = {
            tuple(sorted((x + shift) % n for x in triple)) for shift in range(n)
        }
        representatives.append(triple)
        unseen.difference_update(orbit)
    return representatives


def projective_vectors(p: int, dimension: int) -> Iterator[tuple[int, ...]]:
    """Exactly one vector from every nonzero F_p line in F_p^dimension."""
    for first_nonzero in range(dimension):
        for tail in itertools.product(range(p), repeat=dimension - first_nonzero - 1):
            yield (0,) * first_nonzero + (1,) + tail


def make_entry(p: int, coefficients: tuple[int, ...]):
    n = p + 3
    half = n // 2

    def entry(i: int, j: int) -> int:
        d = (j - i) % n
        if d == 0 or d == half:
            return 0
        if d < half:
            return coefficients[d - 1]
        return (-coefficients[n - d - 1]) % p

    return entry


def pf4(entry, i: int, j: int, k: int, ell: int, p: int) -> int:
    return (
        entry(i, j) * entry(k, ell)
        - entry(i, k) * entry(j, ell)
        + entry(i, ell) * entry(j, k)
    ) % p


def triple_is_rainbow(entry, triple: tuple[int, int, int], p: int) -> bool:
    n = p + 3
    i, j, k = triple
    values = {
        pf4(entry, i, j, k, u, p)
        for u in range(n)
        if u not in triple
    }
    return len(values) == p


def cyclic_candidate_passes(coefficients: tuple[int, ...], p: int, stars) -> tuple[bool, int]:
    entry = make_entry(p, coefficients)
    for count, triple in enumerate(stars, start=1):
        if not triple_is_rainbow(entry, triple, p):
            return False, count
    return True, len(stars)


def exhaustive_controls(primes: list[int]) -> int:
    for p in primes:
        n = p + 3
        dimension = n // 2 - 1
        stars = cyclic_orbit_representatives(n)
        survivors = [0] * (len(stars) + 1)
        total = 0
        for coefficients in projective_vectors(p, dimension):
            total += 1
            ok, passed = cyclic_candidate_passes(coefficients, p, stars)
            survivors[passed] += 1
            if ok:
                print(f"p={p}: CYCLIC CANDIDATE {coefficients}")
                return 1
        # A compact, reproducible pruning profile, not a heuristic score.
        nonzero = [(index, value) for index, value in enumerate(survivors) if value]
        print(
            f"p={p}: exhausted {total} projective skew-circulants "
            f"({len(stars)} translation-orbit stars); rejection profile={nonzero}"
        )
    return 0


def sampled_17(samples: int, seed: int) -> int:
    p = 17
    n = p + 3
    dimension = n // 2 - 1
    stars = cyclic_orbit_representatives(n)
    rng = random.Random(seed)
    best = (-1, None)
    for trial in range(1, samples + 1):
        vector = [rng.randrange(p) for _ in range(dimension)]
        if not any(vector):
            continue
        # Normalize only for readable output; the predicate is scale invariant.
        first = next(x for x in vector if x)
        inverse = pow(first, -1, p)
        coefficients = tuple(x * inverse % p for x in vector)
        ok, passed = cyclic_candidate_passes(coefficients, p, stars)
        if passed > best[0]:
            best = (passed, coefficients)
        if ok:
            print(f"p=17: CYCLIC CANDIDATE after {trial} samples: {coefficients}")
            return 1
    space = (p**dimension - 1) // (p - 1)
    print(
        f"p=17: no candidate in {samples} deterministic projective samples "
        f"of {space} total; best passed {best[0]}/{len(stars)} orbit stars: {best[1]}"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", action="store_true", help="exhaust p=5,7,11")
    parser.add_argument("--sample-17", type=int, default=0)
    parser.add_argument("--seed", type=int, default=835)
    args = parser.parse_args()
    if not args.controls and not args.sample_17:
        parser.error("choose --controls and/or --sample-17")
    status = 0
    if args.controls:
        status |= exhaustive_controls([5, 7, 11])
    if args.sample_17:
        status |= sampled_17(args.sample_17, args.seed)
    return status


if __name__ == "__main__":
    raise SystemExit(main())

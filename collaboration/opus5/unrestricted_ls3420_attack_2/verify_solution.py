"""Deterministic semantic verifier for a claimed solution.

Takes a CaDiCaL witness file for the instance ``chi(J(n,s)) <= m`` produced by
``g1_cnf.py``, and

1. re-derives the variable map from scratch (the CNF is not consulted),
2. checks that every vertex has exactly one colour,
3. checks *semantically* that every star of ``J(n,s)`` is rainbow,
4. applies the Theorem G1 lift to the point ``n``,
5. checks *semantically* that the result is a genuine ``LS(s-1, s, n+1)``:
   every ``(s-1)``-subset of ``[n+1]`` is covered exactly once by every one of
   the ``m`` classes, and the classes partition all ``s``-subsets,
6. re-checks each class independently as a Steiner system,
7. writes the large set out in plain text.

Nothing here trusts the solver.  Standard library only.

    python3 -B verify_solution.py <n> <s> <m> <witness> [out.txt]
"""

from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations
from math import comb

from g1_cnf import (
    colouring_from_model,
    lift_to_large_set,
    read_model,
    verify_large_set,
    verify_proper,
    vertices,
)


def check_each_class_is_steiner(
    v: int, s: int, m: int, ls: dict[frozenset[int], int]
) -> None:
    for colour in range(m):
        blocks = [b for b, c in ls.items() if c == colour]
        assert len(blocks) == comb(v, s) // m, (colour, len(blocks))
        cover: Counter[frozenset[int]] = Counter()
        for b in blocks:
            for sub in combinations(sorted(b), s - 1):
                cover[frozenset(sub)] += 1
        assert len(cover) == comb(v, s - 1), (colour, len(cover))
        assert set(cover.values()) == {1}, (colour, Counter(cover.values()))


def main() -> None:
    if not __debug__:
        raise SystemExit("do not run this certificate checker with python -O")
    n, s, m = (int(a) for a in sys.argv[1:4])
    witness = sys.argv[4]
    assert m % 2 == 1 and n == m + s - 2, "not a Theorem G1 parameter triple"

    nvars = len(vertices(n, s)) * m
    true = read_model(witness, nvars)
    col = colouring_from_model(n, s, m, true)
    print(f"read {len(col)} coloured {s}-subsets of [{n}]")

    verify_proper(n, s, m, col)
    print(f"OK  every star of J({n},{s}) is rainbow")

    ls = lift_to_large_set(n, s, m, col)
    v = n + 1
    verify_large_set(v, s, m, ls)
    print(f"OK  Theorem G1 lift is a large set LS({s - 1},{s},{v})")

    check_each_class_is_steiner(v, s, m, ls)
    print(f"OK  each of the {m} classes is independently an S({s - 1},{s},{v})")

    if len(sys.argv) > 5:
        with open(sys.argv[5], "w") as f:
            f.write(
                f"# LS({s - 1},{s},{v}): {comb(v, s)} blocks, {m} classes of {comb(v, s) // m}\n"
            )
            for b in sorted(map(sorted, ls)):
                f.write(" ".join(map(str, b)) + f" {ls[frozenset(b)]}\n")
        print("wrote", sys.argv[5])

    print(f"VERIFIED  LS({s - 1},{s},{v}) exists")


if __name__ == "__main__":
    main()

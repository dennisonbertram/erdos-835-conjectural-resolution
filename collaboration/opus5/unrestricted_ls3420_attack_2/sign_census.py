"""Census of the star sign on 1-factorizations of K_n (n even).

Colours are labelled canonically: colour ``c`` is the 1-factor containing the
edge ``{0, c+1}``.  Because the star sign is invariant under colour relabelling
whenever ``n`` is even (see NOTE.md), this visits every isomorphism class of
1-factorization and every labelled one has the same sign as its canonical
representative.
"""

from __future__ import annotations

import sys
from collections import Counter

from star_sign import factorization_sign


def canonical_one_factorizations(n: int):
    """Yield each 1-factorization of ``K_n`` once, with colour ``c`` the factor
    through edge ``{0, c+1}``."""
    points = list(range(n))
    used: set[frozenset[int]] = set()
    col: dict[frozenset[int], int] = {}

    def matchings(remaining: list[int], acc: list[frozenset[int]]):
        if not remaining:
            yield list(acc)
            return
        a = remaining[0]
        for j in range(1, len(remaining)):
            b = remaining[j]
            e = frozenset((a, b))
            if e in used:
                continue
            acc.append(e)
            yield from matchings(remaining[1:j] + remaining[j + 1 :], acc)
            acc.pop()

    def rec(colour: int):
        if colour == n - 1:
            yield dict(col)
            return
        forced = frozenset((0, colour + 1))
        if forced in used:
            return
        rest = [x for x in points if x not in (0, colour + 1)]
        used.add(forced)
        col[forced] = colour
        for mat in matchings(rest, []):
            for e in mat:
                used.add(e)
                col[e] = colour
            yield from rec(colour + 1)
            for e in mat:
                used.discard(e)
                del col[e]
        used.discard(forced)
        del col[forced]

    yield from rec(0)


def main() -> None:
    for n in (4, 6, 8):
        census: Counter[int] = Counter()
        for f in canonical_one_factorizations(n):
            census[factorization_sign(f, n)] += 1
        print(f"K_{n}: {sum(census.values())} one-factorizations, signs {dict(census)}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()

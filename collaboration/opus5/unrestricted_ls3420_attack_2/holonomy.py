"""Holonomy of a large set: the non-abelian layer beyond the star sign.

For a large set ``LS(t,t+1,v)`` with colouring ``c``, every ``t``-set ``T``
gives a bijection ``chi_T : X\\T -> [m]``.  For ``R`` of size ``t-1`` and
``a != b`` in ``X\\R`` put

    sigma_R(a,b) = chi_{R u b} . chi_{R u a}^{-1}.

It is defined on ``[m]`` minus the colour ``c(R u {a,b})`` and permutes that
set; extended by fixing that colour it is an element of ``S_m``.  Its cycle
type is a conjugation invariant, strictly finer than its sign.

``N_kappa(c)`` counts the pairs ``(R, {a,b})`` whose holonomy has cycle type
``kappa``.  Theorem 7 of NOTE.md:

    sum over p in X of N_kappa(c^p)  =  (t-1) . N_kappa(c),

for every cycle type ``kappa``, because the holonomy of the derived object at
``p`` indexed by ``(R', {a,b})`` is the holonomy of ``c`` at
``(R' u {p}, {a,b})``.

Standard library only.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations


def cycle_type(perm: dict[int, int]) -> tuple[int, ...]:
    seen: set[int] = set()
    out: list[int] = []
    for start in sorted(perm):
        if start in seen:
            continue
        length, cur = 0, start
        while cur not in seen:
            seen.add(cur)
            cur = perm[cur]
            length += 1
        out.append(length)
    return tuple(sorted(out, reverse=True))


def star_map(
    colouring: dict[frozenset[int], int], T: frozenset[int], ground: list[int]
) -> dict[int, int]:
    return {x: colouring[T | {x}] for x in ground if x not in T}


def holonomy_census(
    colouring: dict[frozenset[int], int], ground: list[int], t: int, m: int
) -> Counter[tuple[int, ...]]:
    """Counter of cycle types of sigma_R(a,b) over all (R, {a,b})."""
    census: Counter[tuple[int, ...]] = Counter()
    gset = set(ground)
    for R in combinations(ground, t - 1):
        Rf = frozenset(R)
        rest = sorted(gset - Rf)
        chi = {y: star_map(colouring, Rf | {y}, ground) for y in rest}
        inv = {y: {col: x for x, col in chi[y].items()} for y in rest}
        for a, b in combinations(rest, 2):
            sig: dict[int, int] = {}
            for col in range(m):
                x = inv[a][col]
                sig[col] = chi[b][x] if x != b else col
            census[cycle_type(sig)] += 1
    return census


def derive(colouring: dict[frozenset[int], int], p: int) -> dict[frozenset[int], int]:
    return {B - {p}: i for B, i in colouring.items() if p in B}


def check_identity(
    colouring: dict[frozenset[int], int], ground: list[int], t: int, m: int
) -> tuple[bool, int]:
    """Return (identity holds, number of cycle types seen)."""
    top = holonomy_census(colouring, ground, t, m)
    total: Counter[tuple[int, ...]] = Counter()
    for p in ground:
        sub = [x for x in ground if x != p]
        total += holonomy_census(derive(colouring, p), sub, t - 1, m)
    scaled = Counter({k: (t - 1) * n for k, n in top.items()})
    return total == scaled, len(set(top) | set(total))

"""Star-sign invariant of a large set LS(t, t+1, t+m), and its tower identity.

Definitions
-----------
Let ``c`` be a large set ``LS(t, t+1, v)`` with ``v = t + m`` on the ordered
ground set ``X = range(v)``, presented as a colouring ``c`` of the
``(t+1)``-subsets of ``X`` by the ordered colour set ``range(m)`` such that for
every ``t``-subset ``T`` the star map

    chi_T : X \\ T -> [m],   chi_T(x) = c(T u {x})

is a bijection (equivalently, every ``t``-set is covered exactly once by every
colour class).

The *star sign* is

    E_t(c) = prod over t-subsets T of  sgn(chi_T),

where ``sgn`` of a bijection between two ordered sets of equal size is the sign
of the induced permutation.

This module provides exact computations only; no randomness, no solver,
standard library only.
"""

from __future__ import annotations

from itertools import combinations, permutations
from math import comb


# ---------------------------------------------------------------- signs


def perm_sign(seq: tuple[int, ...] | list[int]) -> int:
    """Sign of the permutation given by ``seq`` (a permutation of 0..n-1)."""
    seen = [False] * len(seq)
    sign = 1
    for i in range(len(seq)):
        if seen[i]:
            continue
        j, length = i, 0
        while not seen[j]:
            seen[j] = True
            j = seq[j]
            length += 1
        if length % 2 == 0:
            sign = -sign
    return sign


def bijection_sign(domain: list[int], images: list[int], codomain: list[int]) -> int:
    """Sign of the bijection ``domain[i] -> images[i]`` w.r.t. the given orders."""
    pos = {y: j for j, y in enumerate(codomain)}
    return perm_sign([pos[y] for y in images])


# ---------------------------------------------------------------- star sign


def star_sign(
    colouring: dict[frozenset[int], int],
    v: int,
    t: int,
    m: int,
    ground: list[int] | None = None,
) -> int:
    """Star sign ``E_t`` of a large set given as a colouring of (t+1)-sets.

    ``ground`` is the ordered ground set; it defaults to ``range(v)``.  Only the
    *order* matters, so an order-preserving relabelling leaves ``E_t``
    unchanged.
    """
    ground = list(range(v)) if ground is None else list(ground)
    assert len(ground) == v
    colours = list(range(m))
    total = 1
    for T in combinations(ground, t):
        Ts = set(T)
        dom = [x for x in ground if x not in Ts]
        img = [colouring[frozenset(Ts | {x})] for x in dom]
        assert sorted(img) == colours, ("star not rainbow", T)
        total *= bijection_sign(dom, img, colours)
    return total


def derive(colouring: dict[frozenset[int], int], p: int) -> dict[frozenset[int], int]:
    """Derived colouring at point ``p`` (blocks through ``p``, with ``p`` removed)."""
    return {B - {p}: i for B, i in colouring.items() if p in B}


def relabel_points(
    colouring: dict[frozenset[int], int], tau: dict[int, int]
) -> dict[frozenset[int], int]:
    return {frozenset(tau[x] for x in B): i for B, i in colouring.items()}


def relabel_colours(
    colouring: dict[frozenset[int], int], pi: dict[int, int]
) -> dict[frozenset[int], int]:
    return {B: pi[i] for B, i in colouring.items()}


# ---------------------------------------------------------------- invariance


def invariance_exponents(v: int, t: int) -> tuple[int, int]:
    """Return ``(a, b)`` such that a transposition multiplies ``E_t`` by

    ``(-1)**a * sgn(tau^(t))`` -- see NOTE.md.  Concretely the star sign is a
    genuine isomorphism invariant iff ``C(v,t)`` is even (colour relabelling)
    and ``(-1)**(C(v,t) + C(v-1,t-1)) * sgn(tau^(t)) == 1`` for a transposition
    ``tau`` (point relabelling).
    """
    colour_exp = comb(v, t) % 2
    # sgn(tau^(t)) for a transposition tau=(a b): the moved t-sets are those
    # containing exactly one of a, b, and they pair up into C(v-2, t-1)
    # transpositions.
    induced = comb(v - 2, t - 1) % 2
    point_exp = (comb(v, t) + comb(v - 1, t - 1) + induced) % 2
    return colour_exp, point_exp


# ---------------------------------------------------------------- 1-factorizations


def one_factorizations(n: int):
    """Yield every labelled 1-factorization of ``K_n`` (n even) as a dict

    ``frozenset({x,y}) -> colour`` with colours ``0..n-2``.  Colour ``i`` is
    built as the ``i``-th perfect matching; matchings are generated in
    lexicographic order and the search is exhaustive.
    """
    points = list(range(n))
    edges_used: set[frozenset[int]] = set()
    colouring: dict[frozenset[int], int] = {}

    def matchings(remaining: list[int], acc: list[frozenset[int]]):
        if not remaining:
            yield list(acc)
            return
        a = remaining[0]
        for j in range(1, len(remaining)):
            b = remaining[j]
            e = frozenset((a, b))
            if e in edges_used:
                continue
            acc.append(e)
            yield from matchings(remaining[1:j] + remaining[j + 1 :], acc)
            acc.pop()

    def rec(colour: int):
        if colour == n - 1:
            yield dict(colouring)
            return
        for mat in matchings(points, []):
            for e in mat:
                edges_used.add(e)
                colouring[e] = colour
            yield from rec(colour + 1)
            for e in mat:
                edges_used.discard(e)
                del colouring[e]

    yield from rec(0)


def factorization_sign(f: dict[frozenset[int], int], n: int) -> int:
    return star_sign(f, v=n, t=1, m=n - 1)


# ---------------------------------------------------------------- self-check


def _demo() -> None:
    # K_4: the unique 1-factorization class, 6 labelled colourings.
    signs4 = {factorization_sign(f, 4) for f in one_factorizations(4)}
    assert signs4 == {1}, signs4

    # K_6.
    signs6: dict[int, int] = {}
    count6 = 0
    for f in one_factorizations(6):
        count6 += 1
        s = factorization_sign(f, 6)
        signs6[s] = signs6.get(s, 0) + 1
    assert count6 == 6 * 5 * 4 * 3 * 2 * 1, (
        count6
    )  # 6 unordered * 5! colourings? checked below
    print("K_6 labelled 1-factorizations:", count6, "sign census:", signs6)

    # Colour relabelling really is a symmetry when C(v,1)=v is even.
    f0 = next(one_factorizations(6))
    for pi_t in permutations(range(5)):
        pi = dict(enumerate(pi_t))
        assert factorization_sign(relabel_colours(f0, pi), 6) == factorization_sign(
            f0, 6
        )

    # Point relabelling too.
    for tau_t in permutations(range(6)):
        tau = dict(enumerate(tau_t))
        assert factorization_sign(relabel_points(f0, tau), 6) == factorization_sign(
            f0, 6
        )

    print("K_4/K_6 relabelling invariance: OK")


if __name__ == "__main__":
    _demo()

"""Complete second-star symmetry break for the G1 instance chi(J(n,s)) <= m.

Setting.  After the root-star normalisation of ``g1_cnf.py`` -- WLOG
``c({0,...,s-2, x}) = x-(s-1)`` for ``x = s-1, ..., n-1`` -- the residual
symmetry group is

    S_{s-1}  x  S_{m-1},

where the second factor acts *diagonally*: ``g`` permutes the points
``{s-1, ..., n-1}`` and simultaneously the colours ``{0, ..., m-2}``, fixing
the leftover colour ``m-1``.

Now look at the second star, that of the ``(s-1)``-set

    T1 = {0, ..., s-3, s-1}       (root with its last point replaced by s-1),

and put, for ``x`` in ``{s, ..., n-1}``,

    phi(x) = c({0, ..., s-3, s-1, x}).

Two exclusions are already forced by clauses of the instance:

* ``phi(x) != 0``, because the star of ``T1`` also contains the block
  ``T1 u {s-2} = {0,...,s-2,s-1}``, whose colour the root normalisation fixed
  to ``0``, and a star is rainbow;
* ``phi(x) != x-(s-1)``, because ``T1 u {x} = {0,...,s-3,s-1,x}`` and the
  root-star block ``{0,...,s-2,x}`` share the ``(s-1)``-set ``{0,...,s-3,x}``,
  so they are adjacent in ``J(n,s)``.

Writing ``D = {1, ..., m-2}`` for the points ``{s, ..., n-1}`` re-indexed by
``x -> x-(s-1)`` and ``C = {1, ..., m-1}`` for the colours, ``phi`` is an
injective map ``D -> C`` with ``phi(i) != i``.  The full subgroup of the
residual group that fixes the second star setwise is
``S_{s-2} x S_{m-2}``.  The first factor is inert on ``phi``; the effective
``S_{m-2}`` factor acts diagonally on ``D`` (points and colours), fixes the
colour ``m-1``, and acts on ``phi`` by

    phi  |-->  g . phi . g^{-1}.

The orbits are classified by the functional digraph of ``phi`` on ``D``:

* if ``m-1`` is not in the image, ``phi`` is a fixed-point-free permutation of
  ``D`` and the invariant is its cycle type (all parts >= 2);
* otherwise exactly one ``i0`` has ``phi(i0) = m-1`` and exactly one ``j`` is
  missing from the image, and ``phi`` is a path ``j -> ... -> i0`` (possibly the
  single vertex ``j = i0``) together with fixed-point-free cycles; the
  invariant is (path length, cycle type).

``branch_representatives`` emits one representative per orbit; a solution
exists iff some branch is satisfiable.  Completeness of the classification is
checked by brute force at small sizes in ``_demo``.

Standard library only.
"""

from __future__ import annotations

import sys
from itertools import permutations
from pathlib import Path

from g1_cnf import build_cnf, vertices, write_dimacs


# ------------------------------------------------------- orbit representatives


def partitions_min2(n: int) -> list[tuple[int, ...]]:
    """Partitions of ``n`` into parts >= 2, as non-increasing tuples."""
    if n == 0:
        return [()]
    out: list[tuple[int, ...]] = []

    def rec(rem: int, cap: int, acc: list[int]) -> None:
        if rem == 0:
            out.append(tuple(acc))
            return
        for part in range(min(cap, rem), 1, -1):
            if rem - part == 1:
                continue
            acc.append(part)
            rec(rem - part, part, acc)
            acc.pop()

    rec(n, n, [])
    return out


def branch_representatives(d: int) -> list[dict[int, int]]:
    """One representative per orbit of {phi: [1..d] -> [1..d+1] injective,
    phi(i) != i} under diagonal S_d conjugation (with d+1 fixed)."""
    reps: list[dict[int, int]] = []

    def cycles_on(elems: list[int], parts: tuple[int, ...]) -> dict[int, int]:
        phi: dict[int, int] = {}
        pos = 0
        for p in parts:
            cyc = elems[pos : pos + p]
            for i in range(p):
                phi[cyc[i]] = cyc[(i + 1) % p]
            pos += p
        assert pos == len(elems)
        return phi

    # (a) phi is a fixed-point-free permutation of [1..d]
    for parts in partitions_min2(d):
        reps.append(cycles_on(list(range(1, d + 1)), parts))

    # (b) phi(i0) = d+1 for exactly one i0; path of length ell then cycles
    for ell in range(0, d):
        head = list(range(1, ell + 2))  # j = 1 -> 2 -> ... -> ell+1 = i0
        rest = list(range(ell + 2, d + 1))
        for parts in partitions_min2(len(rest)):
            phi = {head[i]: head[i + 1] for i in range(ell)}
            phi[head[ell]] = d + 1
            phi.update(cycles_on(rest, parts))
            reps.append(phi)

    for phi in reps:
        assert sorted(phi) == list(range(1, d + 1))
        assert len(set(phi.values())) == d
        assert all(phi[i] != i for i in phi)
        assert all(1 <= val <= d + 1 for val in phi.values())
    return reps


def _orbit_key(phi: dict[int, int], d: int) -> tuple:
    """Complete conjugation invariant: cycle type, plus path length when the
    extra symbol d+1 is used."""
    if d + 1 not in phi.values():
        seen: set[int] = set()
        cyc: list[int] = []
        for start in range(1, d + 1):
            if start in seen:
                continue
            length, cur = 0, start
            while cur not in seen:
                seen.add(cur)
                cur = phi[cur]
                length += 1
            cyc.append(length)
        return ("perm", tuple(sorted(cyc, reverse=True)))
    i0 = next(i for i in phi if phi[i] == d + 1)
    image = set(phi.values())
    j = next(x for x in range(1, d + 1) if x not in image)
    length, cur = 0, j
    onpath = {j}
    while cur != i0:
        cur = phi[cur]
        onpath.add(cur)
        length += 1
    seen = set(onpath)
    cyc = []
    for start in range(1, d + 1):
        if start in seen:
            continue
        clen, cur = 0, start
        while cur not in seen:
            seen.add(cur)
            cur = phi[cur]
            clen += 1
        cyc.append(clen)
    return ("path", length, tuple(sorted(cyc, reverse=True)))


# ------------------------------------------------------------------ branching


def branch_units(n: int, s: int, m: int, phi: dict[int, int]) -> list[list[int]]:
    """Unit clauses fixing the second star according to ``phi``."""
    verts = vertices(n, s)
    index = {v: i for i, v in enumerate(verts)}

    def var(v_idx: int, colour: int) -> int:
        return v_idx * m + colour + 1

    t1 = set(range(s - 2)) | {s - 1}  # {0,...,s-3, s-1}
    units = []
    for i, colour in sorted(phi.items()):
        x = i + (s - 1)
        blk = index[tuple(sorted(t1 | {x}))]
        units.append([var(blk, colour)])
    return units


def write_branches(n: int, s: int, m: int, outdir: str) -> int:
    clauses, nvars, meta = build_cnf(n, s, m)
    d = m - 2
    reps = branch_representatives(d)
    Path(outdir).mkdir(parents=True, exist_ok=True)
    for k, phi in enumerate(reps):
        write_dimacs(
            f"{outdir}/branch{k:03d}.cnf", clauses + branch_units(n, s, m, phi), nvars
        )
    print(f"{meta} -> {len(reps)} branches in {outdir}")
    return len(reps)


# ------------------------------------------------------------------ self-check


def _demo() -> None:
    # Brute-force completeness of the orbit classification at small sizes.
    for d in (2, 3, 4, 5):
        valid = []
        for img in permutations(range(1, d + 2), d):
            phi = {i + 1: img[i] for i in range(d)}
            if all(phi[i] != i for i in phi):
                valid.append(phi)
        # orbits under diagonal S_d
        keys = {}
        for phi in valid:
            keys.setdefault(_orbit_key(phi, d), []).append(phi)
        reps = branch_representatives(d)
        rep_keys = [_orbit_key(p, d) for p in reps]
        assert len(rep_keys) == len(set(rep_keys)), f"d={d}: duplicate representatives"
        assert set(rep_keys) == set(keys), f"d={d}: {set(keys) ^ set(rep_keys)}"
        # every orbit really is a single S_d orbit
        for key, members in keys.items():
            seed = members[0]
            orbit = set()
            for g_t in permutations(range(1, d + 1)):
                g = dict(zip(range(1, d + 1), g_t))
                gi = {b: a for a, b in g.items()}
                gh = dict(g)
                gh[d + 1] = d + 1
                orbit.add(tuple(sorted((i, gh[seed[gi[i]]]) for i in range(1, d + 1))))
            assert len(orbit) == len(members), (d, key, len(orbit), len(members))
        print(
            f"  d={d}: {len(valid)} maps, {len(keys)} orbits, representatives complete"
        )
    # sizes that matter here
    print("  d=11 (J(15,4), m=13):", len(branch_representatives(11)), "branches")
    print("  d=15 (J(19,4), m=17):", len(branch_representatives(15)), "branches")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("do not run this verifier with python -O")
    if len(sys.argv) == 1:
        _demo()
    else:
        n, s, m = (int(a) for a in sys.argv[1:4])
        write_branches(n, s, m, sys.argv[4])

"""Unrestricted CNF for  chi(J(n,s)) <= m  in the Theorem-G1 parameterisation.

With ``m`` odd and ``n = m + s - 2``, Theorem G1 (see
``collaboration/opus5/generic_radius4_certificate_attack/NOTE.md``) gives

    chi(J(n,s)) <= m   <=>   LS(s-1, s, n+1) exists,

by mutually inverse maps.  So a satisfying assignment here *is* a large set,
after applying the missing-colour map, and this file also contains the
deterministic semantic verifier that performs and checks that lift.

No symmetry ansatz is imposed.  The only assumption is the root-star
normalisation of section ``root_star_units`` below, which is a genuine WLOG:
``S_n`` is transitive on ``(s-1)``-sets, the stabiliser of ``{0,...,s-2}``
contains the full symmetric group on the remaining ``n-s+1`` points, and
colours may be relabelled freely.

Standard library only.
"""

from __future__ import annotations

import sys
from itertools import combinations
from math import comb


def vertices(n: int, s: int) -> list[tuple[int, ...]]:
    return list(combinations(range(n), s))


def build_cnf(n: int, s: int, m: int) -> tuple[list[list[int]], int, dict]:
    """Return (clauses, num_vars, meta) for a proper m-colouring of J(n,s)."""
    verts = vertices(n, s)
    index = {v: i for i, v in enumerate(verts)}
    nv = len(verts)

    def var(v_idx: int, colour: int) -> int:
        return v_idx * m + colour + 1

    clauses: list[list[int]] = []

    # exactly one colour per vertex
    for i in range(nv):
        clauses.append([var(i, c) for c in range(m)])
        for a in range(m):
            for b in range(a + 1, m):
                clauses.append([-var(i, a), -var(i, b)])

    # every star is rainbow: at most one block of each colour per (s-1)-set
    stars: dict[tuple[int, ...], list[int]] = {}
    for T in combinations(range(n), s - 1):
        Ts = set(T)
        star = [index[tuple(sorted(Ts | {x}))] for x in range(n) if x not in Ts]
        assert len(star) == n - s + 1
        stars[T] = star
        for c in range(m):
            for a in range(len(star)):
                for b in range(a + 1, len(star)):
                    clauses.append([-var(star[a], c), -var(star[b], c)])

    # root-star normalisation (WLOG, see module docstring)
    root = tuple(range(s - 1))
    units: list[list[int]] = []
    for j, x in enumerate(x for x in range(n) if x >= s - 1):
        blk = index[tuple(sorted(set(root) | {x}))]
        units.append([var(blk, j)])
    clauses.extend(units)

    meta = {
        "n": n,
        "s": s,
        "m": m,
        "vertices": nv,
        "stars": len(stars),
        "star_size": n - s + 1,
        "class_size": nv // m,
        "root_units": len(units),
        "clauses": len(clauses),
        "vars": nv * m,
    }
    return clauses, nv * m, meta


def write_dimacs(path: str, clauses: list[list[int]], nvars: int) -> None:
    with open(path, "w") as f:
        f.write(f"p cnf {nvars} {len(clauses)}\n")
        f.write("".join(" ".join(map(str, cl)) + " 0\n" for cl in clauses))


# ------------------------------------------------------------------ verifier


def read_model(path: str, nvars: int) -> set[int]:
    """Read a complete, consistent DIMACS solution; return its true variables."""
    true: set[int] = set()
    assignment: dict[int, bool] = {}
    sat = False
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("s "):
                sat = "SATISFIABLE" in line and "UNSATISFIABLE" not in line
            elif line.startswith("v "):
                for tok in line[2:].split():
                    lit = int(tok)
                    if lit == 0:
                        continue
                    var = abs(lit)
                    if not 1 <= var <= nvars:
                        raise AssertionError(
                            f"model literal {lit} is outside 1..{nvars}"
                        )
                    value = lit > 0
                    if var in assignment and assignment[var] != value:
                        raise AssertionError(f"model assigns variable {var} both ways")
                    assignment[var] = value
                    if value:
                        true.add(var)
    if not sat:
        raise SystemExit("model file does not report SATISFIABLE")
    if len(assignment) != nvars:
        missing = nvars - len(assignment)
        raise AssertionError(
            f"model is incomplete: {missing} of {nvars} variables unassigned"
        )
    return true


def colouring_from_model(
    n: int, s: int, m: int, true: set[int]
) -> dict[tuple[int, ...], int]:
    verts = vertices(n, s)
    col: dict[tuple[int, ...], int] = {}
    for i, v in enumerate(verts):
        got = [c for c in range(m) if i * m + c + 1 in true]
        if len(got) != 1:
            raise AssertionError(f"vertex {v} has colours {got}")
        col[v] = got[0]
    return col


def verify_proper(n: int, s: int, m: int, col: dict[tuple[int, ...], int]) -> None:
    """Semantic check: every star of J(n,s) is rainbow."""
    for T in combinations(range(n), s - 1):
        Ts = set(T)
        seen = [col[tuple(sorted(Ts | {x}))] for x in range(n) if x not in Ts]
        if len(set(seen)) != len(seen):
            raise AssertionError(f"star of {T} is not rainbow: {seen}")


def lift_to_large_set(
    n: int, s: int, m: int, col: dict[tuple[int, ...], int]
) -> dict[frozenset[int], int]:
    """Theorem G1 lift: adjoin the point ``n`` via the missing-colour map."""
    out: dict[frozenset[int], int] = {frozenset(v): c for v, c in col.items()}
    for T in combinations(range(n), s - 1):
        Ts = set(T)
        seen = {col[tuple(sorted(Ts | {x}))] for x in range(n) if x not in Ts}
        missing = set(range(m)) - seen
        if len(missing) != 1:
            raise AssertionError(f"star of {T} misses {missing}")
        out[frozenset(Ts | {n})] = missing.pop()
    return out


def verify_large_set(v: int, s: int, m: int, ls: dict[frozenset[int], int]) -> None:
    """Deterministic semantic check that ``ls`` is a genuine LS(s-1, s, v)."""
    assert len(ls) == comb(v, s), (len(ls), comb(v, s))
    assert set(ls) == {frozenset(b) for b in combinations(range(v), s)}
    counts = [0] * m
    for c in ls.values():
        assert 0 <= c < m
        counts[c] += 1
    assert all(x == comb(v, s) // m for x in counts), counts
    for T in combinations(range(v), s - 1):
        Ts = set(T)
        seen = sorted(ls[frozenset(Ts | {x})] for x in range(v) if x not in Ts)
        assert seen == list(range(m)), (T, seen)


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit("usage: g1_cnf.py <n> <s> <m> [out.cnf]")
    n, s, m = (int(a) for a in sys.argv[1:4])
    assert m % 2 == 1, "Theorem G1 needs m odd"
    assert n == m + s - 2, f"need n = m+s-2 = {m + s - 2}"
    clauses, nvars, meta = build_cnf(n, s, m)
    print(meta)
    if len(sys.argv) > 4:
        write_dimacs(sys.argv[4], clauses, nvars)
        print("wrote", sys.argv[4])


if __name__ == "__main__":
    main()

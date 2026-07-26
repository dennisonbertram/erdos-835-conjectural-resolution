#!/usr/bin/env python3
"""CNF proving a stored slice family is COMPLETE.

Encodes slice {i,j} exact cover directly: variables = allowed translates
(orbit-major, shift ascending); ExactlyOne per orbit; ExactlyOne per residual
edge over covering translates (pairwise AMO, ~11 covers/edge).  Then one
blocking clause per stored solution.  UNSAT == no unrecorded solution exists.

--omit N drops the blocking clause of stored solution N (SAT control).
"""

import argparse
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from global_latin_audit import construct_golf17  # noqa: E402

P = 17
POINTS = tuple(range(P))
MOVING_EDGES = tuple(combinations(POINTS, 2))


def translate(subset, amount):
    return tuple(sorted((v + amount) % P for v in subset))


def representatives():
    answer = []
    unseen = set(combinations(POINTS, 3))
    while unseen:
        seed = min(unseen)
        rep = min(translate(seed, s) for s in POINTS)
        answer.append(rep)
        for s in POINTS:
            unseen.discard(translate(rep, s))
    assert len(answer) == 40
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("i", type=int)
    parser.add_argument("j", type=int)
    parser.add_argument("family", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--omit", type=int, default=-1)
    args = parser.parse_args()

    golf = construct_golf17()
    forbidden = {
        e for e in MOVING_EDGES
        if golf[args.i][e[0]][e[1]] == 0 or golf[args.j][e[0]][e[1]] == 0
    }
    assert len(forbidden) == 16
    residual = [e for e in MOVING_EDGES if e not in forbidden]
    assert len(residual) == 120
    edge_index = {e: n for n, e in enumerate(residual)}

    reps = representatives()
    var = 0
    orbit_vars = []           # orbit -> [vars]
    var_key = {}              # (orbit, shift) -> var
    edge_covers = [[] for _ in residual]
    for orbit, rep in enumerate(reps):
        members = []
        for shift in range(P):
            triple = translate(rep, shift)
            edges = list(combinations(triple, 2))
            if any(e in forbidden for e in edges):
                continue
            var += 1
            members.append(var)
            var_key[(orbit, shift)] = var
            for e in edges:
                edge_covers[edge_index[e]].append(var)
        orbit_vars.append(members)
    n_rows = var

    clauses = []
    for members in orbit_vars:
        clauses.append(tuple(members))
        clauses.extend((-a, -b) for a, b in combinations(members, 2))
    for covers in edge_covers:
        assert covers
        clauses.append(tuple(covers))
        clauses.extend((-a, -b) for a, b in combinations(covers, 2))

    raw = args.family.read_bytes()
    assert len(raw) % 40 == 0
    solutions = [raw[k * 40:(k + 1) * 40] for k in range(len(raw) // 40)]
    for index, sol in enumerate(solutions):
        if index == args.omit:
            continue
        clause = []
        for orbit in range(40):
            shift = (P - sol[orbit]) % P
            clause.append(-var_key[(orbit, shift)])
        clauses.append(tuple(clause))

    with open(args.out, "w") as out:
        out.write(f"p cnf {n_rows} {len(clauses)}\n")
        for clause in clauses:
            out.write(" ".join(map(str, clause)) + " 0\n")
    print(f"pair={args.i},{args.j} rows={n_rows} clauses={len(clauses)} "
          f"blocked={len(solutions) - (1 if 0 <= args.omit < len(solutions) else 0)} "
          f"file={args.out}")


if __name__ == "__main__":
    main()

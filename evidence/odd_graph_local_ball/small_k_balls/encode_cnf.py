#!/usr/bin/env python3
"""CNF encoder for radius-4 / radius-5 local-ball existence at even k.

Faithful one-hot encoding of conditions 1-4 of radius4_reduction.md and,
for radius 5, of exact condition (1) of radius5_reduction.md via colour
variables P_ij(uvw).

Every structural condition is of the form "the colours on a d-set of
slots are exactly a d-element allowed set", which is encoded uniformly as
per-(context, colour) EXACTLY-ONE constraints over the slot literals plus
the indicator literals of the excluded colours.  Exactly-one = one ALO
clause + pairwise AMO clauses.

Usage:
  python3 encode_cnf.py K RADIUS out.cnf [--fix fixed.json]
where fixed.json optionally provides "L" and/or "M" (ball_defs JSON
format) to be pinned by unit clauses (used only for the k=16 control).

Also provides decode_model() to turn a cadical v-line model into
(L, M, N, P).
"""

import json
import os
import shutil
import sys
from itertools import combinations


class Enc:
    def __init__(self, k, radius):
        assert k % 2 == 0 and radius in (4, 5)
        self.k = k
        self.radius = radius
        self.V = tuple(range(k))
        self.A = tuple(range(k - 1))
        self.INF = k
        self.C = tuple(range(k + 1))
        self.VE = tuple(combinations(self.V, 2))
        self.AE = tuple(combinations(self.A, 2))
        self.VT = tuple(combinations(self.V, 3))

        self.nvars = 0
        self.lv = {}
        self.mv = {}
        self.nv = {}
        self.pv = {}
        for i in self.A:
            for u in self.V:
                for x in self.V:
                    self.lv[(i, u, x)] = self._new()
        for i in self.A:
            for e in self.VE:
                for c in self.C:
                    self.mv[(i, e, c)] = self._new()
        for e in self.VE:
            for f in self.AE:
                for c in self.C:
                    self.nv[(e, f, c)] = self._new()
        if radius == 5:
            for f in self.AE:
                for t in self.VT:
                    for c in self.C:
                        self.pv[(f, t, c)] = self._new()
        self.nclauses = 0
        self._body = None
        self._body_path = None

    def open_stream(self, path):
        self._body_path = path + ".body.tmp"
        self._body = open(self._body_path, "w")

    def _new(self):
        self.nvars += 1
        return self.nvars

    def add(self, cl):
        self.nclauses += 1
        self._body.write(" ".join(map(str, cl)) + " 0\n")

    def exactly_one(self, lits):
        self.add(list(lits))
        for a, b in combinations(lits, 2):
            self.add([-a, -b])

    def ve(self, u, v):
        return (min(u, v), max(u, v))

    def build(self):
        k, V, A, C, INF = self.k, self.V, self.A, self.C, self.INF
        lv, mv, nv, pv = self.lv, self.mv, self.nv, self.pv

        # --- L: value one-hot, derangement, row permutation, column cond 1.
        for i in A:
            for u in V:
                self.exactly_one([lv[(i, u, x)] for x in V])
                self.add([-lv[(i, u, u)]])
        for i in A:
            for x in V:
                self.exactly_one([lv[(i, u, x)] for u in V])
        for u in V:
            for x in V:
                if x != u:
                    self.exactly_one([lv[(i, u, x)] for i in A])

        # --- M: one colour per edge; vertex-endpoint exclusions.
        for i in A:
            for e in self.VE:
                self.exactly_one([mv[(i, e, c)] for c in C])
                u, v = e
                self.add([-mv[(i, e, u)]])
                self.add([-mv[(i, e, v)]])

        # Condition 2 colour lists: for each i, u, c in C\{u}, colour c
        # occurs at u exactly once among the k-1 incident M_i edges unless
        # c = L_i(u) (then zero); uniform exactly-one with the L indicator.
        for i in A:
            for u in V:
                for c in C:
                    if c == u:
                        continue  # excluded by the unit clauses above
                    lits = [
                        mv[(i, self.ve(u, v), c)] for v in V if v != u
                    ]
                    if c != INF:
                        lits.append(lv[(i, u, c)])
                    self.exactly_one(lits)

        # Condition 3: for each edge uv and c in C\{u,v}: exactly one i.
        for e in self.VE:
            u, v = e
            for c in C:
                if c in (u, v):
                    continue
                self.exactly_one([mv[(i, e, c)] for i in A])

        # --- N: one colour per (edge of K_V, edge of K_A).
        for e in self.VE:
            for f in self.AE:
                self.exactly_one([nv[(e, f, c)] for c in C])

        # Condition 4: for each uv, i, c: colour c occurs at index i in
        # N_uv exactly once among its k-2 incident K_A edges unless c is
        # one of {M_i(uv), L_i(u), L_i(v)} (then zero).
        for e in self.VE:
            u, v = e
            for i in A:
                for c in C:
                    lits = [
                        nv[(e, (min(i, j), max(i, j)), c)]
                        for j in A
                        if j != i
                    ]
                    lits.append(mv[(i, e, c)])
                    if c != INF:
                        lits.append(lv[(i, u, c)])
                        lits.append(lv[(i, v, c)])
                    self.exactly_one(lits)

        # --- radius 5: P_ij(uvw), exact condition (1).
        if self.radius == 5:
            for f in self.AE:
                for t in self.VT:
                    self.exactly_one([pv[(f, t, c)] for c in C])
            for f in self.AE:
                i, j = f
                for e in self.VE:
                    u, v = e
                    for c in C:
                        lits = [
                            pv[(f, tuple(sorted((u, v, w))), c)]
                            for w in V
                            if w not in e
                        ]
                        lits.append(nv[(e, f, c)])
                        lits.append(mv[(i, e, c)])
                        lits.append(mv[(j, e, c)])
                        self.exactly_one(lits)

    def fix(self, fixed):
        """Pin L and/or M from a ball_defs-style JSON dict via units."""
        if "L" in fixed:
            for i in self.A:
                for u in self.V:
                    x = fixed["L"][i][u]
                    self.add([self.lv[(i, u, x)]])
        if "M" in fixed:
            for key, c in fixed["M"].items():
                i, u, v = map(int, key.split(","))
                self.add([self.mv[(i, (u, v), c)]])

    def write(self, path):
        self._body.close()
        with open(path, "w") as fh:
            fh.write(f"p cnf {self.nvars} {self.nclauses}\n")
            with open(self._body_path) as body:
                shutil.copyfileobj(body, fh)
        os.remove(self._body_path)

    def decode_model(self, true_vars):
        s = set(true_vars)
        L = [[None] * self.k for _ in self.A]
        for (i, u, x), var in self.lv.items():
            if var in s:
                assert L[i][u] is None
                L[i][u] = x
        M = {}
        for (i, e, c), var in self.mv.items():
            if var in s:
                key = (i, e[0], e[1])
                assert key not in M
                M[key] = c
        N = {}
        for (e, f, c), var in self.nv.items():
            if var in s:
                assert (e, f) not in N
                N[(e, f)] = c
        P = None
        if self.radius == 5:
            P = {}
            for (f, t, c), var in self.pv.items():
                if var in s:
                    assert (f, t) not in P
                    P[(f, t)] = c
        return L, M, N, P


def parse_cadical_model(text):
    vals = []
    for line in text.splitlines():
        if line.startswith("v"):
            vals.extend(int(x) for x in line[1:].split())
    return [v for v in vals if v > 0]


def main():
    k = int(sys.argv[1])
    radius = int(sys.argv[2])
    out = sys.argv[3]
    enc = Enc(k, radius)
    enc.open_stream(out)
    enc.build()
    if "--fix" in sys.argv:
        with open(sys.argv[sys.argv.index("--fix") + 1]) as fh:
            enc.fix(json.load(fh))
    enc.write(out)
    print(
        f"k={k} radius={radius}: {enc.nvars} vars, "
        f"{enc.nclauses} clauses -> {out}"
    )


if __name__ == "__main__":
    main()

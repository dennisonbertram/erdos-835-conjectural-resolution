#!/usr/bin/env python3
"""Verifier for collaboration/opus5/common_odd_transversal_2026-07-29.

Standard library only.  Python 3.8+.

    python3 verify_common_odd_transversal.py

The Opus author could not execute this script. A later independent run found
and corrected the Part E colour-class parser, then passed every asserted
finite check. Lines marked OPEN report experiments on the unproved LLS
conjecture rather than asserted theorems.

Parts
-----
A  Admissibility  <=>  k+1 prime                                   (Cor 2.4)
B  Intersection distributions N_i, m_i on S(3,4,8) and S(5,6,12)   (Thm 2.1)
C  Max pairwise disjoint S(2,3,7) and S(3,4,8)                     (Thm 5.1)
D  Link theorem + LLS-span on the LS(2,3,9) control            (Thm 3.1-3.3)
E  Etzion-Hartman partial: link triangle + LLS-span            (Prop 3.6)

Part E is skipped with a clear message if the committed EH file is absent.
"""

from __future__ import annotations

import sys
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path

FAILURES = []


def check(cond: bool, msg: str) -> bool:
    print(("  PASS  " if cond else "  FAIL  ") + msg)
    if not cond:
        FAILURES.append(msg)
    return bool(cond)


def head(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


# --------------------------------------------------------------------------
# generic helpers
# --------------------------------------------------------------------------

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def all_steiner(n: int, t: int, kk: int):
    """All labelled S(t,kk,n) on points 0..n-1, by exact cover of the t-sets.

    Returns (blocks, designs) where blocks is the list of all kk-subsets and
    each design is a tuple of indices into blocks.
    """
    blocks = list(combinations(range(n), kk))
    tsets = list(combinations(range(n), t))
    tindex = {s: i for i, s in enumerate(tsets)}
    full = (1 << len(tsets)) - 1

    bmask = []
    for b in blocks:
        m = 0
        for s in combinations(b, t):
            m |= 1 << tindex[s]
        bmask.append(m)

    by_t = [[] for _ in tsets]
    for bi, b in enumerate(blocks):
        for s in combinations(b, t):
            by_t[tindex[s]].append(bi)

    out = []

    def rec(cov, chosen):
        if cov == full:
            out.append(tuple(chosen))
            return
        rem = ~cov & full
        i = (rem & -rem).bit_length() - 1  # lowest uncovered t-set: canonical
        for bi in by_t[i]:
            if bmask[bi] & cov:
                continue
            chosen.append(bi)
            rec(cov | bmask[bi], chosen)
            chosen.pop()

    rec(0, [])
    return blocks, out


def max_clique_size(nvert: int, adj):
    """Exact max clique by branch and bound.  adj[v] is a bitmask of neighbours."""
    best = 0

    def rec(size, cand):
        nonlocal best
        if size > best:
            best = size
        while cand:
            if size + bin(cand).count("1") <= best:
                return
            low = cand & -cand
            v = low.bit_length() - 1
            cand ^= low
            rec(size + 1, cand & adj[v])

    rec(0, (1 << nvert) - 1)
    return best


def f2_rank(vectors) -> int:
    """Rank over F_2 of a list of ints used as bit vectors."""
    basis = []
    for v in vectors:
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
            basis.sort(reverse=True)
    return len(basis)


# --------------------------------------------------------------------------
# residual conflict graph and links
# --------------------------------------------------------------------------

class Rung:
    """Residual conflict graph G for p-2 disjoint S(t,t+1,n)'s.

    `deleted` is the set of (t+1)-blocks used by the systems (as frozensets).
    """

    def __init__(self, n: int, t: int, deleted):
        self.n, self.t = n, t
        universe = [frozenset(b) for b in combinations(range(n), t + 1)]
        deleted = set(deleted)
        self.residual = sorted((b for b in universe if b not in deleted), key=sorted)
        self.rindex = {b: i for i, b in enumerate(self.residual)}
        self.edges = []          # list of (u, v) vertex-index pairs
        self.edge_label = []     # the t-set labelling each edge
        self.edge_of_label = {}
        for a in combinations(range(n), t):
            aset = frozenset(a)
            ext = [self.rindex[b] for b in self.residual if aset <= b]
            if len(ext) != 2:
                raise ValueError("t-set %s has %d residual extensions, expected 2"
                                 % (sorted(a), len(ext)))
            self.edge_of_label[aset] = len(self.edges)
            self.edge_label.append(aset)
            self.edges.append((ext[0], ext[1]))

    # -- basic invariants ---------------------------------------------------
    def components(self) -> int:
        parent = list(range(len(self.residual)))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for u, v in self.edges:
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
        return len({find(x) for x in range(len(self.residual))})

    def cycle_space_dim(self) -> int:
        return len(self.edges) - len(self.residual) + self.components()

    def is_bipartite(self) -> bool:
        colour = {}
        nbr = [[] for _ in self.residual]
        for ei, (u, v) in enumerate(self.edges):
            nbr[u].append(v)
            nbr[v].append(u)
        for s in range(len(self.residual)):
            if s in colour:
                continue
            colour[s] = 0
            stack = [s]
            while stack:
                x = stack.pop()
                for y in nbr[x]:
                    if y not in colour:
                        colour[y] = colour[x] ^ 1
                        stack.append(y)
                    elif colour[y] == colour[x]:
                        return False
        return True

    # -- links --------------------------------------------------------------
    def link_cycles(self):
        """Yield (A_0, cycle) where cycle is the list of Y-points of a cycle of R(A_0)."""
        for a0 in combinations(range(self.n), self.t - 1):
            a0set = frozenset(a0)
            ys = [y for y in range(self.n) if y not in a0set]
            radj = {y: [] for y in ys}
            for y, y2 in combinations(ys, 2):
                if a0set | {y, y2} in self.rindex:
                    radj[y].append(y2)
                    radj[y2].append(y)
            for y in ys:
                if len(radj[y]) != 2:
                    raise ValueError("link at %s is not 2-regular at %d (degree %d)"
                                     % (sorted(a0), y, len(radj[y])))
            seen = set()
            for start in ys:
                if start in seen:
                    continue
                cyc = [start]
                seen.add(start)
                prev, cur = None, start
                while True:
                    nxt = [z for z in radj[cur] if z != prev]
                    nxt = nxt[0] if len(nxt) == 1 else radj[cur][0]
                    if nxt == start:
                        break
                    cyc.append(nxt)
                    seen.add(nxt)
                    prev, cur = cur, nxt
                yield a0set, cyc

    def link_cycle_vector(self, a0set, cyc) -> int:
        """Bitmask over edge indices of the G-cycle induced by a link cycle."""
        vec = 0
        for y in cyc:
            vec ^= 1 << self.edge_of_label[a0set | {y}]
        return vec

    def in_cycle_space(self, vec: int) -> bool:
        deg = [0] * len(self.residual)
        for ei, (u, v) in enumerate(self.edges):
            if (vec >> ei) & 1:
                deg[u] += 1
                deg[v] += 1
        return all(d % 2 == 0 for d in deg)


def lls_report(rung: Rung, name: str) -> None:
    zdim = rung.cycle_space_dim()
    bip = rung.is_bipartite()
    vecs, odd_links = [], 0
    for a0set, cyc in rung.link_cycles():
        vec = rung.link_cycle_vector(a0set, cyc)
        if not rung.in_cycle_space(vec):
            check(False, "%s: link cycle at %s is not in the cycle space"
                  % (name, sorted(a0set)))
            return
        if len(cyc) % 2 == 1:
            odd_links += 1
        vecs.append(vec)
    ldim = f2_rank(vecs)
    print("  INFO  %s: |V|=%d |E|=%d components=%d dim Z_1=%d"
          % (name, len(rung.residual), len(rung.edges), rung.components(), zdim))
    print("  INFO  %s: link cycles=%d  odd link cycles=%d  dim L=%d"
          % (name, len(vecs), odd_links, ldim))
    print("  INFO  %s: G bipartite = %s" % (name, bip))
    # Corollary 3.4, proved: an odd link cycle forces non-bipartite.
    check(not (odd_links > 0 and bip),
          "%s: Cor 3.4 holds (odd link cycle => G not bipartite)" % name)
    # LLS-span was a proposed stronger condition; report its measured status.
    print("  OPEN  %s: LLS-span %s (dim L = %d vs dim Z_1 = %d)"
          % (name, "HOLDS" if ldim == zdim else "FAILS", ldim, zdim))
    if not bip and odd_links == 0:
        print("  OPEN  %s: *** LLS COUNTEREXAMPLE *** non-bipartite with all links even"
              % name)


# --------------------------------------------------------------------------
# Part A
# --------------------------------------------------------------------------

def part_a() -> None:
    head("Part A - admissibility <=> k+1 prime (Corollary 2.4)")
    bad = []
    for k in range(2, 81, 2):
        lam_ok = all(comb(k + m, m) % (k + 1) == 0 for m in range(1, k + 1))
        if lam_ok != is_prime(k + 1):
            bad.append(k)
    check(not bad, "lambda_j integrality == primality of k+1 for all even k <= 80")
    adm = [k for k in range(3, 40) if k % 2 == 0 and is_prime(k + 1)]
    check(adm == [4, 6, 10, 12, 16, 18, 22, 28, 30, 36],
          "admissible k in (2,40) are 4,6,10,12,16,18,22,28,30,36; got %s" % adm)


# --------------------------------------------------------------------------
# Part B
# --------------------------------------------------------------------------

def n_formula(k: int, i: int) -> int:
    num = comb(k, i) ** 2 + k * (-1) ** (k - i) * comb(k, i)
    assert num % (k + 1) == 0
    return num // (k + 1)


def m_formula(k: int, i: int) -> int:
    num = comb(k, i) ** 2 - (-1) ** (k - i) * comb(k, i)
    assert num % (k + 1) == 0
    return num // (k + 1)


def sqs8():
    """S(3,4,8): the 4-subsets of F_2^3 with zero XOR sum."""
    out = []
    for q in combinations(range(8), 4):
        x = 0
        for v in q:
            x ^= v
        if x == 0:
            out.append(frozenset(q))
    return out


def s_5_6_12():
    """S(5,6,12): orbit of {0,1,3,4,5,9} under PSL(2,11) on PG(1,11).

    Point 11 stands for infinity.
    """
    p = 11
    inv = {a: pow(a, p - 2, p) for a in range(1, p)}
    squares = {(a * a) % p for a in range(1, p)}

    def apply(mat, x):
        a, b, c, d = mat
        if x == 11:                       # infinity
            return 11 if c % p == 0 else (a * inv[c % p]) % p
        num, den = (a * x + b) % p, (c * x + d) % p
        return 11 if den == 0 else (num * inv[den]) % p

    base = frozenset({0, 1, 3, 4, 5, 9})
    orbit = set()
    for a in range(p):
        for b in range(p):
            for c in range(p):
                for d in range(p):
                    if (a * d - b * c) % p in squares:
                        orbit.add(frozenset(apply((a, b, c, d), x) for x in base))
    return sorted(orbit, key=sorted)


def profile(block, design):
    prof = {}
    for c in design:
        i = len(block & c)
        prof[i] = prof.get(i, 0) + 1
    return prof


def check_design(design, n, t, kk, label) -> bool:
    ok = all(len(b) == kk for b in design)
    for s in combinations(range(n), t):
        if sum(1 for b in design if frozenset(s) <= b) != 1:
            ok = False
            break
    return check(ok, "%s is a genuine S(%d,%d,%d) with %d blocks"
                 % (label, t, kk, n, len(design)))


def part_b() -> None:
    head("Part B - intersection distributions (Theorem 2.1)")
    for k, design, n, label in ((4, sqs8(), 8, "S(3,4,8)"),
                                (6, s_5_6_12(), 12, "S(5,6,12)")):
        if not check_design(design, n, k - 1, k, label):
            continue
        check(len(design) == comb(2 * k, k) // (k + 1),
              "%s has C_k = %d blocks" % (label, comb(2 * k, k) // (k + 1)))
        dset = set(design)
        okN = okM = True
        for b in combinations(range(n), k):
            bs = frozenset(b)
            prof = profile(bs, design)
            want = {i: (n_formula(k, i) if bs in dset else m_formula(k, i))
                    for i in range(k + 1)}
            want = {i: v for i, v in want.items() if v}
            if prof != want:
                if bs in dset:
                    okN = False
                else:
                    okM = False
        check(okN, "%s: N_i formula holds for every block" % label)
        check(okM, "%s: m_i formula holds for every non-block" % label)
        check(n_formula(k, 0) == 1 and m_formula(k, 0) == 0,
              "%s: complement closure (Cor 2.2) is the i=0 coefficient" % label)


# --------------------------------------------------------------------------
# Part C
# --------------------------------------------------------------------------

def part_c() -> None:
    head("Part C - maximum pairwise disjoint systems (Theorem 5.1)")
    for (n, t, kk, want_designs, want_max, label) in (
            (7, 2, 3, 30, 2, "S(2,3,7)"),
            (8, 3, 4, 30, 2, "S(3,4,8)")):
        blocks, designs = all_steiner(n, t, kk)
        check(len(designs) == want_designs,
              "%s: %d labelled systems (expected %d)" % (label, len(designs), want_designs))
        masks = []
        for d in designs:
            m = 0
            for bi in d:
                m |= 1 << bi
            masks.append(m)
        adj = []
        for i in range(len(masks)):
            a = 0
            for j in range(len(masks)):
                if i != j and not (masks[i] & masks[j]):
                    a |= 1 << j
            adj.append(a)
        got = max_clique_size(len(masks), adj)
        check(got == want_max,
              "%s: max pairwise disjoint = %d (expected %d)" % (label, got, want_max))
    print("  INFO  k=4 needs k-1 = 3 disjoint S(3,4,8); k=6 needs k-1 = 5 disjoint S(5,6,12).")


# --------------------------------------------------------------------------
# Part D
# --------------------------------------------------------------------------

def part_d() -> None:
    head("Part D - link theorem and LLS-span on the LS(2,3,9) control")
    blocks, designs = all_steiner(9, 2, 3)
    check(len(designs) == 840, "840 labelled STS(9); got %d" % len(designs))
    masks = []
    for d in designs:
        m = 0
        for bi in d:
            m |= 1 << bi
        masks.append(m)

    large = []

    def grow(cands, chosen):
        if len(chosen) == 7:
            large.extend(chosen)
            return True
        need = 7 - len(chosen)
        for idx, i in enumerate(cands):
            if len(cands) - idx < need:
                return False
            nxt = [j for j in cands[idx + 1:] if not (masks[j] & masks[i])]
            chosen.append(i)
            if grow(nxt, chosen):
                return True
            chosen.pop()
        return False

    if not check(grow(list(range(len(masks))), []),
                 "found a large set LS(2,3,9): 7 disjoint STS(9)"):
        return
    deleted = set()
    for i in large[:5]:
        for bi in designs[i]:
            deleted.add(frozenset(blocks[bi]))
    check(len(deleted) == 60, "5 of the 7 systems supply 60 deleted triples")
    rung = Rung(9, 2, deleted)
    check(rung.is_bipartite(), "LS(2,3,9) control: residual graph IS bipartite")
    lls_report(rung, "LS(2,3,9) 5-system")


# --------------------------------------------------------------------------
# Part E
# --------------------------------------------------------------------------

EH_REL = "collaboration/ls3420_branch0_search/eh15_branch0_partial.txt"


def part_e() -> None:
    head("Part E - Etzion-Hartman partial (3,20,17), 15 systems (Prop 3.6)")
    root = Path(__file__).resolve().parents[3]
    path = root / EH_REL
    if not path.exists():
        print("  SKIP  %s not found; Part E skipped." % EH_REL)
        return
    rows = []
    for line in path.read_text().split("\n"):
        parts = line.split()
        if len(parts) != 5:
            continue
        blk = frozenset(int(x) for x in parts[:4])
        rows.append((blk, int(parts[4])))
    counts = Counter(colour for _, colour in rows if colour >= 0)
    complete_colours = {
        colour for colour, count in counts.items() if count == 285
    }
    deleted = {block for block, colour in rows if colour in complete_colours}
    residual = {block for block, colour in rows if colour not in complete_colours}
    check(len(deleted) == 4275 and len(residual) == 570,
          "EH partial: 4275 deleted + 570 residual = %d + %d" % (len(deleted), len(residual)))
    # the link at A_0 = {14,17}: neighbours y,y' with {14,17,y,y'} residual
    a0 = frozenset({14, 17})
    ys = [y for y in range(20) if y not in a0]
    link = {y: [] for y in ys}
    for y, y2 in combinations(ys, 2):
        if a0 | {y, y2} in residual:
            link[y].append(y2)
            link[y2].append(y)
    check(all(len(link[y]) == 2 for y in ys),
          "EH: the link at {14,17} is a 2-factor on 18 points")
    check(sorted(link[0]) == [2, 5] and sorted(link[2]) == [0, 5]
          and sorted(link[5]) == [0, 2],
          "EH: {0,2,5} is a triangle of R({14,17})  (Prop 3.6)")
    rung = Rung(20, 3, deleted)
    check(not rung.is_bipartite(), "EH: residual graph is NOT bipartite")
    lls_report(rung, "EH 15-system")


# --------------------------------------------------------------------------

def main() -> int:
    part_a()
    part_b()
    part_c()
    part_d()
    part_e()
    head("Summary")
    if FAILURES:
        print("  %d FAILURE(S):" % len(FAILURES))
        for f in FAILURES:
            print("    - " + f)
        return 1
    print("  ALL CHECKS PASS")
    print("  Lines marked OPEN are reports on Lemma LLS, not assertions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

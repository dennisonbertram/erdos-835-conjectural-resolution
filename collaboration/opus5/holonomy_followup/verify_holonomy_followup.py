"""Verifier for collaboration/opus5/holonomy_followup/NOTE.md.

Standard library only.  Exact finite arithmetic and exhaustive enumeration.
No solver, no network.  The only randomness is used to build *controls*
(random chart families and random one-factorizations); every claim that the
note states as a theorem is also checked on exhaustively enumerated or
committed objects, and the random parts are labelled as samples both here and
in the note.

Run:

    python3 -B collaboration/opus5/holonomy_followup/verify_holonomy_followup.py
"""

from __future__ import annotations

import random
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from math import comb
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
K10_CATALOGUE = REPO / "evidence" / "k10_one_factorizations_396.txt"

PASSED = 0
FAILED = 0


def check(label: str, ok: bool) -> None:
    global PASSED, FAILED
    if ok:
        PASSED += 1
        print(f"  ok   {label}", flush=True)
    else:
        FAILED += 1
        print(f"  FAIL {label}", flush=True)


# --------------------------------------------------------------- utilities


def sgn_seq(seq):
    """Sign of a sequence of distinct comparable values, read as the
    permutation that carries the sorted order to the given order."""
    rank = {v: i for i, v in enumerate(sorted(seq))}
    perm = [rank[v] for v in seq]
    seen = [False] * len(perm)
    s = 1
    for i in range(len(perm)):
        if seen[i]:
            continue
        j, ln = i, 0
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            ln += 1
        if ln % 2 == 0:
            s = -s
    return s


def cycle_type(perm):
    """perm as a tuple with perm[i] the image of i.  Descending cycle type."""
    seen = [False] * len(perm)
    out = []
    for i in range(len(perm)):
        if seen[i]:
            continue
        ln, j = 0, i
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            ln += 1
        out.append(ln)
    return tuple(sorted(out, reverse=True))


def fpf_part(perm):
    """The fixed-point-free part of the cycle type."""
    return tuple(x for x in cycle_type(perm) if x > 1)


def derangement_types(k):
    """Partitions of k into parts >= 2, descending tuples."""
    out = []

    def rec(rem, mx, acc):
        if rem == 0:
            out.append(tuple(acc))
            return
        for p in range(min(rem, mx), 1, -1):
            if rem - p == 1:
                continue
            rec(rem - p, p, acc + [p])

    rec(k, k, [])
    return out


def partitions_count(n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            dp[total] += dp[total - part]
    return dp[n]


# ------------------------------------------------- charts and the holonomy
#
# A *chart family* of type (v, t, m) on an ordered ground set X with
# |X| = v and m = v - t is a family of bijections
#
#     g_T : X \ T -> [m],   T in binom(X, t).
#
# A large set LS(t,t+1,v) is exactly a chart family with the extra symmetry
# g_T(s) = g_{(T-r)+s}(r); the note calls that the *design* condition.


def charts_from_ls(ls, ground, t):
    out = {}
    for T in combinations(ground, t):
        fs = frozenset(T)
        out[fs] = {x: ls[frozenset(fs | {x})] for x in ground if x not in fs}
    return out


def random_charts(ground, t, m, rng):
    out = {}
    for T in combinations(ground, t):
        fs = frozenset(T)
        rest = [x for x in ground if x not in fs]
        cols = list(range(m))
        rng.shuffle(cols)
        out[fs] = dict(zip(rest, cols))
    return out


def holonomy(charts, R, a, b, m):
    """sigma_R(a,b) in Sym([m]) with the canonical completion:
    it agrees with g_{R+b} . g_{R+a}^{-1} where that is defined and sends
    g_{R+a}(b) to g_{R+b}(a).  On a large set those two colours coincide and
    the completion fixes it."""
    ga, gb = charts[R | {a}], charts[R | {b}]
    inv = {c: z for z, c in ga.items()}
    d_in, d_out = ga[b], gb[a]
    perm = [0] * m
    for e in range(m):
        z = inv[e]
        perm[e] = d_out if z == b else gb[z]
    return tuple(perm), d_in, d_out


def derive_charts(charts, ground, p, t):
    """The derived chart family at p: g^p_{T'} = g_{T' + p}."""
    g2 = [x for x in ground if x != p]
    return g2, {
        frozenset(T): charts[frozenset(T) | {p}] for T in combinations(g2, t - 1)
    }


def holonomy_sum(charts, ground, t, m):
    """H = sum over R in binom(X,t-1) and ORDERED (a,b) of [sigma_R(a,b)],
    as a Counter on Sym([m])."""
    acc = Counter()
    for R in combinations(ground, t - 1):
        Rs = frozenset(R)
        rest = [x for x in ground if x not in Rs]
        for a, b in permutations(rest, 2):
            perm, _di, _do = holonomy(charts, Rs, a, b, m)
            acc[perm] += 1
    return acc


def census(charts, ground, t, m):
    """Unordered-pair cycle-type census, and the refinement by fixed colour."""
    cen, ref = Counter(), Counter()
    for R in combinations(ground, t - 1):
        Rs = frozenset(R)
        rest = [x for x in ground if x not in Rs]
        for a, b in combinations(rest, 2):
            perm, d_in, d_out = holonomy(charts, Rs, a, b, m)
            cen[cycle_type(perm)] += 1
            if d_in == d_out:
                ref[(cycle_type(perm), d_in)] += 1
    return cen, ref


# --------------------------------------------------------- genuine objects


def build_ls239():
    """Exhaustive backtracking construction of an LS(2,3,9)."""
    pts = list(range(9))
    triples = [frozenset(t) for t in combinations(pts, 3)]
    pairs = list(combinations(pts, 2))
    idx = {frozenset(p): i for i, p in enumerate(pairs)}
    tp = {t: [idx[frozenset(p)] for p in combinations(sorted(t), 2)] for t in triples}
    order = sorted(triples, key=sorted)
    col = {}
    used = [[False] * 36 for _ in range(7)]

    def rec(i):
        if i == len(order):
            return True
        t = order[i]
        for c in range(7):
            if all(not used[c][p] for p in tp[t]):
                for p in tp[t]:
                    used[c][p] = True
                col[t] = c
                if rec(i + 1):
                    return True
                for p in tp[t]:
                    used[c][p] = False
                del col[t]
        return False

    if not rec(0):
        raise AssertionError("no LS(2,3,9) found")
    return dict(col)


def load_cyclic_lsts19():
    sys.path.insert(0, str(REPO))
    from evidence.verify_defect_cross_link_lsts19 import (  # noqa: PLC0415
        construct_lsts19,
        verify_large_set,
    )

    raw = construct_lsts19()
    verify_large_set(raw)
    return {frozenset(k): v for k, v in raw.items()}


def is_large_set(ls, ground, t, m):
    for T in combinations(ground, t):
        fs = frozenset(T)
        seen = {ls[frozenset(fs | {x})] for x in ground if x not in fs}
        if len(seen) != m:
            return False
    return True


# ----------------------------------------------------- one-factorizations


def _match(rem, used, acc, out):
    if not rem:
        out.append(tuple(acc))
        return
    a = rem[0]
    for i in range(1, len(rem)):
        b = rem[i]
        if (a, b) in used:
            continue
        _match(rem[1:i] + rem[i + 1 :], used, acc + [(a, b)], out)


def one_factorizations(n):
    """Every 1-factorization of K_n exactly once, colour i normalised to hold
    the edge {0, i+1}.  Yields dict[(x,y) with x<y] -> colour."""
    verts = list(range(n))

    def rec(colour, used, col):
        if colour == n - 1:
            yield dict(col)
            return
        rem = [v for v in verts if v not in (0, colour + 1)]
        cands = []
        _match(rem, used, [], cands)
        for mm in cands:
            edges = list(mm) + [(0, colour + 1)]
            for e in edges:
                col[e] = colour
            yield from rec(colour + 1, used | set(edges), col)
            for e in edges:
                del col[e]

    yield from rec(0, set(), {})


def load_k10():
    out = []
    with open(K10_CATALOGUE) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            _case, rest = line.strip().split("\t")
            col = {}
            for c, factor in enumerate(rest.split(";")):
                for e in factor.split(","):
                    x, y = int(e[0]), int(e[1])
                    col[(min(x, y), max(x, y))] = c
            if len(col) != 45:
                raise AssertionError("bad K10 record")
            out.append(col)
    return out


def round_robin(n):
    """The standard 1-factorization of K_n, n even."""
    m = n - 1
    col = {}
    for i in range(m):
        col[(min(i, m), max(i, m))] = i
        for k in range(1, (n - 2) // 2 + 1):
            a, b = (i + k) % m, (i - k) % m
            col[(min(a, b), max(a, b))] = i
    if len(col) != comb(n, 2):
        raise AssertionError("round robin failed")
    return col


def alt_cycles(col, n, e, f):
    """The alternating cycles of F_e u F_f, each as a list of edges."""
    pe, pf = {}, {}
    for (x, y), c in col.items():
        if c == e:
            pe[x], pe[y] = y, x
        elif c == f:
            pf[x], pf[y] = y, x
    seen, out = set(), []
    for v in range(n):
        if v in seen:
            continue
        edges, cur, use_e = [], v, True
        while True:
            seen.add(cur)
            nxt = pe[cur] if use_e else pf[cur]
            edges.append((min(cur, nxt), max(cur, nxt)))
            cur, use_e = nxt, not use_e
            if cur == v and use_e:
                break
        out.append(edges)
    return out


# Three one-factorizations of K_18 whose holonomy census realises, with ODD
# multiplicity, each of the three cycle types that the random sample misses.
# Each is 153 colours in the order list(combinations(range(18), 2)).  The
# (2,...,2) one was built by prescribing eight alternating 4-cycles through the
# vertex pair {0,1} and completing; the other two were found by search.  They
# are committed here so the n = 18 conclusion is deterministic.
WITNESSES_18 = {
    (4, 2, 2, 2, 2, 2, 2): (
        "10,5,16,3,6,2,13,4,9,14,8,12,15,7,1,11,0,7,3,11,9,15,12,13,6,1,5,16,"
        "0,8,14,4,2,12,15,14,13,1,2,4,9,16,6,8,3,11,0,10,6,1,4,11,8,7,5,10,15,"
        "9,13,0,2,14,2,0,16,12,14,13,4,1,7,10,5,8,9,8,15,7,5,3,0,10,4,11,13,"
        "12,16,3,1,16,11,14,7,10,9,6,5,12,9,0,4,2,5,14,6,7,10,8,3,0,11,14,16,"
        "15,10,6,5,10,12,8,11,2,15,13,1,7,2,12,16,8,15,6,13,6,1,9,3,15,3,0,4,"
        "9,11,5,2,1,13,12,14,4,16,3,7"
    ),
    (3, 3, 2, 2, 2, 2, 2): (
        "5,10,3,13,6,9,7,0,4,8,1,2,15,14,11,12,16,13,11,16,15,1,12,6,10,2,8,3,"
        "4,7,14,0,9,0,4,3,11,8,5,16,7,9,6,2,12,1,14,15,2,14,16,6,8,15,9,5,10,"
        "12,13,4,7,1,5,15,1,11,0,6,14,7,10,3,8,9,12,8,9,13,12,1,16,0,7,2,10,4,"
        "11,3,10,13,4,7,12,14,5,0,6,2,14,5,16,15,4,13,0,2,11,10,7,15,12,16,1,"
        "9,3,2,4,14,2,8,3,11,9,1,6,13,5,11,10,12,3,0,11,0,4,6,10,3,9,1,13,15,"
        "14,6,16,8,5,15,16,8,5,7,13"
    ),
    (2, 2, 2, 2, 2, 2, 2, 2): (
        "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,2,1,4,3,6,5,8,7,10,9,12,11,"
        "14,13,16,15,9,11,13,12,4,6,16,8,7,15,3,10,0,5,14,10,6,13,14,11,4,0,"
        "16,5,7,3,15,12,8,9,15,8,0,5,6,2,16,13,12,1,14,7,2,16,12,0,15,11,14,8,"
        "5,10,7,1,3,1,11,4,14,0,9,16,7,8,10,13,15,1,0,7,10,11,9,2,12,2,14,3,"
        "10,16,15,5,9,4,13,1,9,14,6,12,10,3,12,3,5,7,16,11,2,4,15,8,6,13,5,2,"
        "1,8,6,13,0,4,1,6,2,4,9,3,11,0"
    ),
}


def decode_witness(packed):
    vals = [int(x) for x in packed.split(",")]
    order = list(combinations(range(18), 2))
    if len(vals) != len(order):
        raise AssertionError("bad witness length")
    return dict(zip(order, vals))


def is_perfect(col, n):
    """True when every union of two factors is a single Hamiltonian cycle."""
    return all(
        len(alt_cycles(col, n, e, f)) == 1 for e, f in combinations(range(n - 1), 2)
    )


def random_one_factorization(n, rng, budget=200000):
    """One 1-factorization of K_n found by randomised backtracking over the
    factors.  Genuinely varied, unlike a cycle-switch walk started at the
    round-robin factorization (see is_perfect)."""
    verts = list(range(n))
    col = {}
    spent = [0]

    def matchings(rem, used, acc):
        if not rem:
            yield tuple(acc)
            return
        a = rem[0]
        idx = list(range(1, len(rem)))
        rng.shuffle(idx)
        for i in idx:
            b = rem[i]
            if (a, b) in used:
                continue
            yield from matchings(rem[1:i] + rem[i + 1 :], used, acc + [(a, b)])

    def rec(colour, used):
        if colour == n - 1:
            return True
        for mm in matchings(verts, used, []):
            spent[0] += 1
            if spent[0] > budget:
                return False
            for e in mm:
                col[e] = colour
            if rec(colour + 1, used | set(mm)):
                return True
            for e in mm:
                del col[e]
        return False

    return col if rec(0, set()) else None


def is_one_factorization(col, n):
    if len(col) != comb(n, 2):
        return False
    for a in range(n):
        seen = [col[(min(a, z), max(a, z))] for z in range(n) if z != a]
        if len(set(seen)) != n - 1:
            return False
    return True


def onefac_as_ls(col, n):
    """A 1-factorization is an LS(1,2,n): blocks are the edges."""
    return {frozenset(e): c for e, c in col.items()}


def star_sign(col, n):
    """E_1(F) = prod over vertices of sgn(rho_a), order-preserving reference."""
    p = 1
    for a in range(n):
        seq = [col[(min(a, z), max(a, z))] for z in range(n) if z != a]
        p *= sgn_seq(seq)
    return p


def alt_4cycles(col, n):
    """Total number of 4-cycles in F_e u F_f over all colour pairs e < f."""
    m = n - 1
    part = [{} for _ in range(m)]
    for (x, y), c in col.items():
        part[c][x] = y
        part[c][y] = x
    total = 0
    for e, f in combinations(range(m), 2):
        pe, pf = part[e], part[f]
        seen = set()
        for v in range(n):
            if v in seen:
                continue
            ln, cur, use_e = 0, v, True
            while True:
                seen.add(cur)
                cur = pe[cur] if use_e else pf[cur]
                use_e = not use_e
                ln += 1
                if cur == v and use_e:
                    break
            if ln == 4:
                total += 1
    return total


def onefac_stats(col, n):
    """Census (fixed-point-free part), sum of #2-cycles, product of holonomy
    signs, and the signs indexed by unordered vertex pairs."""
    m = n - 1
    charts = charts_from_ls(onefac_as_ls(col, n), list(range(n)), 1)
    cen = Counter()
    tot2 = 0
    signs = {}
    for a, b in combinations(range(n), 2):
        perm, d_in, d_out = holonomy(charts, frozenset(), a, b, m)
        if d_in != d_out:
            raise AssertionError("one-factorization must be symmetric")
        t = fpf_part(perm)
        cen[t] += 1
        tot2 += sum(1 for x in t if x == 2)
        signs[(a, b)] = sgn_seq(perm)
    return cen, tot2, signs


# ------------------------------------------------------------ linear algebra


def f2_nullspace(rows, k):
    """Basis of {a in F_2^k : <a, r> = 0 for every r in rows}, rows as ints.
    Reduced row echelon form, then the standard free-column basis."""
    pivots = []  # (pivot column, fully reduced row)
    for r in rows:
        cur = r
        for c, pr in pivots:
            if cur >> c & 1:
                cur ^= pr
        if cur == 0:
            continue
        c0 = cur.bit_length() - 1
        pivots = [(c, pr ^ cur if pr >> c0 & 1 else pr) for c, pr in pivots]
        pivots.append((c0, cur))
    pivcols = {c for c, _ in pivots}
    basis = []
    for f in range(k):
        if f in pivcols:
            continue
        a = 1 << f
        for c, pr in pivots:
            if pr >> f & 1:
                a |= 1 << c
        basis.append(a)
    return basis


def q_rank(vectors):
    """Rank over Q of a list of integer vectors."""
    rows = [[Fraction(x) for x in v] for v in vectors]
    rank, ncol = 0, len(rows[0]) if rows else 0
    for c in range(ncol):
        piv = None
        for r in range(rank, len(rows)):
            if rows[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        pr = rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][c] != 0:
                f = rows[r][c] / pr[c]
                rows[r] = [x - f * y for x, y in zip(rows[r], pr)]
        rank += 1
    return rank


def f2_reduce(vectors):
    """Canonical row-reduced echelon basis of the F_2 span, as a sorted list.
    Two subspaces are equal exactly when their reduced bases agree."""
    piv = []
    for v in vectors:
        cur = v
        for c, pr in piv:
            if cur >> c & 1:
                cur ^= pr
        if cur == 0:
            continue
        c0 = cur.bit_length() - 1
        piv = [(c, pr ^ cur if pr >> c0 & 1 else pr) for c, pr in piv]
        piv.append((c0, cur))
    return sorted(pr for _c, pr in piv)


def in_span(basis, x):
    red = f2_reduce(basis)
    cur = x
    for pr in sorted(red, reverse=True):
        if cur >> (pr.bit_length() - 1) & 1:
            cur ^= pr
    return cur == 0


def congruence_space(vectors, types):
    """Basis of the universal F_2 congruences a.N == const on `vectors`.
    The span itself is never materialised: it can have 2^40 elements."""
    k = len(types)
    base = vectors[0]
    rows = []
    for v in vectors[1:]:
        r = 0
        for i in range(k):
            if (v[i] - base[i]) & 1:
                r |= 1 << i
        if r:
            rows.append(r)
    return f2_nullspace(rows, k)


def d_mask(types):
    mask = 0
    for i, t in enumerate(types):
        if sum(1 for x in t if x == 2) % 2:
            mask |= 1 << i
    return mask


# ================================================================ sections


def section1_gauge_vacuity():
    print("\n[1] Theorem 1: the t >= 2 tower identity is gauge-vacuous")
    rng = random.Random(20260727)
    for v, t in ((9, 2), (8, 3), (10, 3), (11, 4)):
        m = v - t
        ground = list(range(v))
        charts = random_charts(ground, t, m, rng)
        top = holonomy_sum(charts, ground, t, m)
        acc = Counter()
        for p in ground:
            g2, ch2 = derive_charts(charts, ground, p, t)
            acc += holonomy_sum(ch2, g2, t - 1, m)
        want = Counter({k: (t - 1) * n for k, n in top.items()})
        check(
            f"random chart family v={v} t={t} m={m}: "
            f"sum_p H(g^p) = (t-1) H(g) in Z[S_{m}]",
            acc == want,
        )
        # the same families are demonstrably NOT large sets
        bad_sym = 0
        for R in combinations(ground, t - 1):
            Rs = frozenset(R)
            rest = [x for x in ground if x not in Rs]
            for a, b in combinations(rest, 2):
                _perm, d_in, d_out = holonomy(charts, Rs, a, b, m)
                if d_in != d_out:
                    bad_sym += 1
        check(
            f"control: that family violates the design symmetry "
            f"({bad_sym} asymmetric holonomies), so vacuity is not accidental",
            bad_sym > 0,
        )
    # and the identity holds on genuine objects too
    ls9 = {frozenset(k): v for k, v in build_ls239().items()}
    for name, ls, ground, t, m in (
        ("LS(2,3,9)", ls9, list(range(9)), 2, 7),
        ("cyclic LS(2,3,19)", load_cyclic_lsts19(), list(range(19)), 2, 17),
    ):
        charts = charts_from_ls(ls, ground, t)
        top = holonomy_sum(charts, ground, t, m)
        acc = Counter()
        for p in ground:
            g2, ch2 = derive_charts(charts, ground, p, t)
            acc += holonomy_sum(ch2, g2, t - 1, m)
        want = Counter({k: (t - 1) * n for k, n in top.items()})
        check(f"{name}: same identity holds (t-1 = {t - 1})", acc == want)
    return ls9


def section2_refinement_is_a_projection(ls9, ls19):
    print("\n[2] The colour refinement factors through the exact census")
    for name, ls, ground, t, m in (
        ("LS(2,3,9)", ls9, list(range(9)), 2, 7),
        ("cyclic LS(2,3,19)", ls19, list(range(19)), 2, 17),
    ):
        charts = charts_from_ls(ls, ground, t)
        n_unord = comb(len(ground), t - 1) * comb(len(ground) - t + 1, 2)
        cen, ref = census(charts, ground, t, m)
        check(
            f"{name}: every holonomy fixes exactly one colour "
            "(so the fixed colour is a function of the permutation)",
            all(k.count(1) == 1 for k in cen) and sum(ref.values()) == n_unord,
        )
        rows = Counter()
        for (_k, d), c in ref.items():
            rows[d] += c
        want = comb(len(ground), t - 1) * ((m + 1) // 2)
        check(
            f"{name}: refined row sum per colour is {want} for all {m} colours",
            set(rows.values()) == {want} and len(rows) == m,
        )
        # orientation: H is antipode invariant
        h = holonomy_sum(charts, ground, t, m)
        inv = Counter()
        for perm, c in h.items():
            back = [0] * m
            for i, j in enumerate(perm):
                back[j] = i
            inv[tuple(back)] += c
        check(f"{name}: H is invariant under g -> g^-1 (orientation is free)", h == inv)


def section3_sign_layer(ls9, ls19):
    print("\n[3] Theorem 3: for odd m, the holonomy sign layer is the epsilon layer")
    rng = random.Random(11)
    cases = [
        ("LS(2,3,9)", charts_from_ls(ls9, list(range(9)), 2), list(range(9)), 2, 7),
        (
            "cyclic LS(2,3,19)",
            charts_from_ls(ls19, list(range(19)), 2),
            list(range(19)),
            2,
            17,
        ),
        (
            "random v=10 t=3",
            random_charts(list(range(10)), 3, 7, rng),
            list(range(10)),
            3,
            7,
        ),
        (
            "random v=11 t=4",
            random_charts(list(range(11)), 4, 7, rng),
            list(range(11)),
            4,
            7,
        ),
    ]
    for name, charts, ground, t, m in cases:
        tri_ok = balanced_ok = prod_ok = True
        total = 1
        for R in combinations(ground, t - 1):
            Rs = frozenset(R)
            rest = [x for x in ground if x not in Rs]
            sg = {}
            for a, b in combinations(rest, 2):
                perm, _di, _do = holonomy(charts, Rs, a, b, m)
                sg[(a, b)] = sgn_seq(perm)

            def s(a, b, sg=sg):
                return sg[(a, b)] if a < b else sg[(b, a)]

            for a, b, e in combinations(rest, 3):
                if s(a, b) * s(b, e) * s(a, e) != -1:
                    tri_ok = False
            # balance: build eta from the first vertex and re-test every edge
            eta = {rest[0]: 1}
            for x in rest[1:]:
                eta[x] = -s(rest[0], x) * eta[rest[0]]
            for a, b in combinations(rest, 2):
                if s(a, b) != -eta[a] * eta[b]:
                    balanced_ok = False
            prod = 1
            for a, b in combinations(rest, 2):
                prod *= sg[(a, b)]
            # epsilon(R) = E_1(c^R) = product of the star signs of c^R
            eps = 1
            for x in rest:
                seq = [charts[Rs | {x}][z] for z in rest if z != x]
                eps *= sgn_seq(seq)
            if prod != eps:
                prod_ok = False
            total *= prod
        check(f"{name}: triangle sign law sgn.sgn.sgn = -1", tri_ok)
        check(
            f"{name}: the holonomy sign graph is balanced (a coboundary)", balanced_ok
        )
        check(
            f"{name}: prod over pairs of sgn sigma_R = epsilon(R) = E_1(g^R)", prod_ok
        )
        # E_t(c)^t
        et = 1
        for T in combinations(ground, t):
            fs = frozenset(T)
            seq = [charts[fs][z] for z in ground if z not in fs]
            et *= sgn_seq(seq)
        check(f"{name}: prod over all R and pairs of sgn sigma = E_t^t", total == et**t)


def section4_intercalate_congruence():
    print("\n[4] Theorem 4: the intercalate congruence (design-dependent)")
    exhaustive = {}
    for n, want in ((4, 1), (6, 6), (8, 6240)):
        cols = list(one_factorizations(n))
        check(f"K_{n}: {want} one-factorizations enumerated", len(cols) == want)
        exhaustive[n] = cols
    k10 = load_k10()
    check("K_10: 396 isomorphism-class representatives loaded", len(k10) == 396)

    families = [
        ("K_4 exhaustive", 4, exhaustive[4], True),
        ("K_6 exhaustive", 6, exhaustive[6], True),
        ("K_8 exhaustive", 8, exhaustive[8], True),
        ("K_10 all 396 classes", 10, k10, True),
    ]
    rng = random.Random(99)
    for n in (12, 18):
        check(
            f"the round-robin one-factorization of K_{n} is perfect, so a "
            "cycle-switch walk started there is inert (recorded: it silently "
            "produced a constant sample)",
            is_perfect(round_robin(n), n),
        )
    for n, cnt in ((12, 150), (18, 150)):
        cols = []
        while len(cols) < cnt:
            c = random_one_factorization(n, rng)
            if c is not None and is_one_factorization(c, n):
                cols.append(dict(c))
        check(
            f"K_{n}: {cnt} randomised-backtracking samples, all genuine "
            "one-factorizations",
            len(cols) == cnt,
        )
        families.append((f"K_{n} random sample", n, cols, False))

    # the 19 point-links of the committed cyclic LS(2,3,19)
    ls19 = load_cyclic_lsts19()
    links = []
    for x in range(19):
        rest = sorted(v for v in range(19) if v != x)
        ren = {v: i for i, v in enumerate(rest)}
        links.append(
            {
                (ren[a], ren[b]): ls19[frozenset((x, a, b))]
                for a, b in combinations(rest, 2)
            }
        )
    families.append(("K_18: the 19 links of the cyclic LS(2,3,19)", 18, links, True))

    census_store = {}
    for label, n, cols, exh in families:
        bad_id = bad_cong = bad_sign = 0
        vecs = []
        types = derangement_types(n - 2)
        ti = {t: i for i, t in enumerate(types)}
        for col in cols:
            cen, tot2, signs = onefac_stats(col, n)
            if tot2 != 2 * alt_4cycles(col, n):
                bad_id += 1
            if tot2 % 2:
                bad_cong += 1
            prod = 1
            for s in signs.values():
                prod *= s
            if prod != star_sign(col, n):
                bad_sign += 1
            v = [0] * len(types)
            for t, c in cen.items():
                v[ti[t]] = c
            vecs.append(v)
        tag = "exhaustive" if exh else f"sample of {len(cols)}"
        check(
            f"{label} ({tag}): sum #2-cycles = 2 * #alternating 4-cycles",
            bad_id == 0,
        )
        check(f"{label} ({tag}): the census congruence D holds", bad_cong == 0)
        check(
            f"{label} ({tag}): prod over pairs sgn sigma = E_1 (census fixes E_1)",
            bad_sign == 0,
        )
        census_store[label] = (n, types, vecs, exh)
    return census_store


def section5_mod2_content(census_store):
    print("\n[5] Theorem 5: the exact mod-2 content of the census")
    for label, (n, types, vecs, exh) in census_store.items():
        if n < 8 or len(vecs) < 2:
            continue
        if len(vecs) <= len(types):
            print(
                f"    {label}: {len(vecs)} objects for {len(types)} types - "
                "too few to bound the congruence space, skipped",
                flush=True,
            )
            continue
        basis = congruence_space(vecs, types)
        dm = d_mask(types)
        allm = (1 << len(types)) - 1
        expect = f2_reduce([dm, allm])
        red = f2_reduce(basis)
        tag = "exhaustive" if exh else f"sample of {len(vecs)}"
        print(f"    {label} ({tag}): {len(types)} types, dim = {len(basis)}")
        check(f"{label}: D is a universal congruence", in_span(basis, dm))
        check(
            f"{label}: the total count is a universal congruence", in_span(basis, allm)
        )
        if n == 8 and exh:
            check(
                "K_8 exhaustive: dim = 3, i.e. exactly ONE extra congruence "
                "beyond span{total, D}",
                len(basis) == 3 and red != expect,
            )
        if n == 10 and exh:
            check(
                "K_10 exhaustive over all 396 classes: dim = 2, the space is "
                "EXACTLY span{total, D} - the K_8 extra congruence does not "
                "generalise",
                len(basis) == 2 and red == expect,
            )
        if n == 12 and not exh:
            check(
                f"K_12 sample of {len(vecs)}: dim = 2 and the space is exactly "
                "span{total, D} - a sample can only overestimate the "
                "congruence space, so this bounds it above",
                len(basis) == 2 and red == expect,
            )
        if n == 18 and not exh:
            absent = [i for i in range(len(types)) if not any(v[i] for v in vecs)]
            gens = [dm, allm] + [1 << i for i in absent]
            print(
                f"      {len(absent)} of {len(types)} cycle types never occur "
                f"in this sample: {[types[i] for i in absent]}",
                flush=True,
            )
            check(
                f"K_18 ({tag}): the observed congruence space is EXACTLY "
                "span{total, D, coordinates of the cycle types absent from "
                "the sample} - the extra directions are absent-type "
                "artifacts, not laws",
                red == f2_reduce(gens),
            )
            # kill the artifacts with three committed witnesses
            wit = []
            for kappa, packed in WITNESSES_18.items():
                col = decode_witness(packed)
                cen, _tot2, _sg = onefac_stats(col, 18)
                check(
                    f"committed K_18 witness for {kappa}: a genuine "
                    f"one-factorization with N_kappa = {cen.get(kappa, 0)}, odd",
                    is_one_factorization(col, 18) and cen.get(kappa, 0) % 2 == 1,
                )
                w = [0] * len(types)
                for kk, cc in cen.items():
                    w[types.index(kk)] = cc
                wit.append(w)
            basis2 = congruence_space(vecs + wit, types)
            check(
                "K_18: with the three witnesses added, the universal F_2 "
                "congruence space is EXACTLY span{total, D}, dimension 2 - "
                "and since more objects can only shrink it while both "
                "functionals are proved universal, that is the exact value",
                len(basis2) == 2 and f2_reduce(basis2) == expect,
            )
    # rational affine dimension: no further real-linear constraint at n = 10
    n, types, vecs, exh = census_store["K_10 all 396 classes"]
    base = vecs[0]
    diffs = [[a - b for a, b in zip(v, base)] for v in vecs[1:]]
    r = q_rank(diffs)
    check(
        f"K_10 exhaustive: censuses affinely span the whole hyperplane "
        f"sum N = C(10,2) over Q (rank {r} = {len(types) - 1}), so D is a "
        "purely mod-2 phenomenon",
        r == len(types) - 1,
    )
    # the diagonal-swap pairing does NOT preserve the full cycle type
    k10 = load_k10()
    violated = False
    for col in k10:
        charts = charts_from_ls(onefac_as_ls(col, 10), list(range(10)), 1)
        for a, b in combinations(range(10), 2):
            pab, _, _ = holonomy(charts, frozenset(), a, b, 9)
            tab = fpf_part(pab)
            for z, w in combinations([x for x in range(10) if x not in (a, b)], 2):
                if (
                    col[(min(a, z), max(a, z))] == col[(min(b, w), max(b, w))]
                    and col[(min(a, w), max(a, w))] == col[(min(b, z), max(b, z))]
                ):
                    pzw, _, _ = holonomy(charts, frozenset(), z, w, 9)
                    if fpf_part(pzw) != tab:
                        violated = True
                        break
            if violated:
                break
        if violated:
            break
    check(
        "REFUTED: the diagonal-swap involution does not preserve the full "
        "cycle type at n = 10, so D admits no per-type refinement",
        violated,
    )


def section6_separating_power(census_store):
    print("\n[6] Theorem 6: how much the census separates")
    n, types, vecs, _ = census_store["K_8 exhaustive"]
    check(
        "K_8: the census takes exactly 6 values, matching the 6 isomorphism "
        "classes of one-factorizations of K_8",
        len({tuple(v) for v in vecs}) == 6,
    )
    n, types, vecs, _ = census_store["K_10 all 396 classes"]
    d = len({tuple(v) for v in vecs})
    check(
        f"K_10: the census separates {d} of the 396 isomorphism classes, "
        "so it is finer than the sign but not complete",
        d == 374,
    )


def section7_equivalence(ls9):
    print("\n[7] Theorem 2: the overlap system is exactly the problem")
    ground = list(range(9))
    # the 9 point-links of the LS(2,3,9), as LS(1,2,8) colourings
    links = {}
    for p in ground:
        rest = [x for x in ground if x != p]
        links[p] = {
            frozenset((a, b)): ls9[frozenset((p, a, b))]
            for a, b in combinations(rest, 2)
        }
    ok_match = all(
        links[p][frozenset((q, x))] == links[q][frozenset((p, x))]
        for p, q in combinations(ground, 2)
        for x in ground
        if x not in (p, q)
    )
    check("LS(2,3,9): the 9 point-links satisfy the matching condition", ok_match)
    rebuilt = {}
    for T in combinations(ground, 3):
        p, a, b = T
        rebuilt[frozenset(T)] = links[p][frozenset((a, b))]
    check(
        "LS(2,3,9): reconstruction from the links returns the same object",
        rebuilt == ls9,
    )
    check(
        "LS(2,3,9): every link is a one-factorization of K_8 = LS(1,2,8)",
        all(
            is_large_set(links[p], [x for x in ground if x != p], 1, 7) for p in ground
        ),
    )
    # negative control: perturb one link and the matching must fail
    import copy

    bad = copy.deepcopy(links)
    e0, e1 = sorted(bad[0])[0], sorted(bad[0])[1]
    bad[0][e0], bad[0][e1] = bad[0][e1], bad[0][e0]
    still = all(
        bad[p][frozenset((q, x))] == bad[q][frozenset((p, x))]
        for p, q in combinations(ground, 2)
        for x in ground
        if x not in (p, q)
    )
    check("negative control: perturbing one link breaks the matching", not still)
    # the only non-formal step in the general proof: S_3 plus one transposition
    # generates S_4
    gens = [(0, 2, 3, 1), (0, 3, 1, 2), (1, 0, 2, 3)]
    grp = {(0, 1, 2, 3)}
    frontier = list(grp)
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                p = tuple(h[g[i]] for i in range(4))
                if p not in grp:
                    grp.add(p)
                    nxt.append(p)
        frontier = nxt
    check(
        "the symmetric group of a triple together with one cross transposition "
        "generates S_4, which is the only non-formal step of Theorem 2",
        len(grp) == 24,
    )


def section8_constants(ls19):
    print("\n[8] Arithmetic constants quoted in the note")
    check("p(16) = 231 and p(15) = 176", partitions_count(16) == 231)
    check(
        "the number of fixed-point-free partitions of 16 is 231 - 176 = 55",
        len(derangement_types(16)) == partitions_count(16) - partitions_count(15) == 55,
    )
    check("55 * 17 = 935 refined (kappa, colour) coordinates", 55 * 17 == 935)
    charts = charts_from_ls(ls19, list(range(19)), 2)
    cen, _ref = census(charts, list(range(19)), 2, 17)
    check(
        "cyclic LS(2,3,19): 19 * C(18,2) = 2907 unordered holonomies",
        sum(cen.values()) == 2907,
    )
    check(
        "cyclic LS(2,3,19): 34 distinct cycle types of the 55 possible", len(cen) == 34
    )
    h = holonomy_sum(charts, list(range(19)), 2, 17)
    check(
        "cyclic LS(2,3,19): 5814 ordered summands, all coefficients 1",
        sum(h.values()) == 5814 and set(h.values()) == {1},
    )
    check(
        "LS(3,4,20) counts: 190 pairs, 153 pairs, 190*153 = C(20,4)*6",
        comb(20, 2) == 190 and comb(18, 2) == 153 and 190 * 153 == comb(20, 4) * 6,
    )
    check(
        "LS(3,4,20): 1710 = 6 * 285 holonomies per colour, 17 * 1710 = 29070",
        6 * 285 == 1710 and 17 * 1710 == 29070,
    )


def main():
    if not __debug__:
        raise SystemExit("do not run this verifier with python -O")
    ls9 = section1_gauge_vacuity()
    ls19 = load_cyclic_lsts19()
    section2_refinement_is_a_projection(ls9, ls19)
    section3_sign_layer(ls9, ls19)
    store = section4_intercalate_congruence()
    section5_mod2_content(store)
    section6_separating_power(store)
    section7_equivalence(ls9)
    section8_constants(ls19)
    print(f"\n{PASSED}/{PASSED + FAILED} checks passed")
    if FAILED:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

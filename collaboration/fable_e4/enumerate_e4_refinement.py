#!/usr/bin/env python3
"""Exact enumeration of the e4-refined moment-curve quotient graphs G_r.

SEARCH/ANALYSIS CODE -- not a certificate.  Certificates and independent
checkers live beside this file; see PROOF.md and JUDGMENT.md.

Setting (F = F_2[alpha]/(alpha^5+alpha^2+1), points of J(32,16) = 16-subsets
of F, adjacency = intersection 15):

  sigma5(S) = (e1, e2, e3, e4, e8 + e1^8)(S).

Refined moment-curve states over first coordinate a with parameter r:

  (a, a^2, a^3, a^4 + r, lambda).

Proved in PROOF.md (Theorem A/B):
  * every actual edge between two such states (any r values) forces the
    common value  e4(S) + a^4 = e4(T) + b^4 = e4(S cup T) = r,  and
    e1=e2=e3(S cup T) = 0;
  * conversely every 17-set R with e1=e2=e3=0, e4=r gives the labelled
    clique K17 on states (a, lambda_R(a)), a in R, where
       lambda_R(a) = r a^4 + e5(R) a^3 + e6(R) a^2 + e7(R) a + e8(R).

Hence G_r is exactly the union of those labelled K17s, and this script's
job is the exact enumeration of all such R and the clique analysis.
"""

from __future__ import annotations

import json
import sys
import time
from itertools import combinations
from pathlib import Path

sys.setrecursionlimit(100000)

MODULUS = 0b100101  # X^5 + X^2 + 1, same convention as the K32 verifier


def _mul(left: int, right: int) -> int:
    raw = 0
    for bit in range(5):
        if right >> bit & 1:
            raw ^= left << bit
    for degree in range(8, 4, -1):
        if raw >> degree & 1:
            raw ^= MODULUS << (degree - 5)
    return raw


MUL = tuple(tuple(_mul(a, b) for b in range(32)) for a in range(32))


def fpow(value: int, exponent: int) -> int:
    answer = 1
    while exponent:
        if exponent & 1:
            answer = MUL[answer][value]
        value = MUL[value][value]
        exponent >>= 1
    return answer


def trace(value: int) -> int:
    answer, current = 0, value
    for _ in range(5):
        answer ^= current
        current = MUL[current][current]
    return answer


def layer(value: int) -> int:
    return int(value == 0 or trace(value) == 1)


def stats_from_mask(mask: int) -> tuple:
    """(e1..e8) of the set of field elements in mask, computed from scratch."""
    e = [1] + [0] * 8
    for p in range(32):
        if mask >> p & 1:
            for d in range(8, 0, -1):
                e[d] ^= MUL[p][e[d - 1]]
    return tuple(e[1:9])


POPCOUNT = tuple(bin(m).count("1") for m in range(1 << 16))


def half_tables(elems):
    """stats[m] = (e1..e8) of {elems[i] : bit i of m}; full_of[m] = 32-bit mask."""
    n = len(elems)
    stats = [None] * (1 << n)
    full_of = [0] * (1 << n)
    stats[0] = (0,) * 8
    for m in range(1, 1 << n):
        lb = m & -m
        i = lb.bit_length() - 1
        x = elems[i]
        p = stats[m ^ lb]
        stats[m] = tuple(
            p[d - 1] ^ MUL[x][1 if d == 1 else p[d - 2]] for d in range(1, 9)
        )
        full_of[m] = full_of[m ^ lb] | (1 << x)
    return stats, full_of


def enumerate_r_sets(elems_a, elems_b):
    """All 17-subsets R of F with e1=e2=e3=0, keyed by r=e4(R).

    Returns records[r] = list of (mask, e5, e6, e7, e8).
    """
    sa, fa = half_tables(elems_a)
    sb, fb = half_tables(elems_b)
    buckets = {}
    for m in range(1 << 16):
        st = sb[m]
        key = (POPCOUNT[m], st[0], st[1], st[2])
        buckets.setdefault(key, []).append((m, st))
    records = [[] for _ in range(32)]
    for m in range(1, 1 << 16):
        sza = POPCOUNT[m]
        szb = 17 - sza
        if not 1 <= szb <= 16:
            continue
        a1, a2, a3, a4, a5, a6, a7, a8 = sa[m]
        b1 = a1
        b2 = a2 ^ MUL[a1][a1]
        b3 = a3 ^ MUL[a2][b1] ^ MUL[a1][b2]
        for mb, st in buckets.get((szb, b1, b2, b3), ()):
            b4, b5, b6, b7, b8 = st[3], st[4], st[5], st[6], st[7]
            e4 = a4 ^ MUL[a3][b1] ^ MUL[a2][b2] ^ MUL[a1][b3] ^ b4
            e5 = (a5 ^ MUL[a4][b1] ^ MUL[a3][b2] ^ MUL[a2][b3]
                  ^ MUL[a1][b4] ^ b5)
            e6 = (a6 ^ MUL[a5][b1] ^ MUL[a4][b2] ^ MUL[a3][b3]
                  ^ MUL[a2][b4] ^ MUL[a1][b5] ^ b6)
            e7 = (a7 ^ MUL[a6][b1] ^ MUL[a5][b2] ^ MUL[a4][b3]
                  ^ MUL[a3][b4] ^ MUL[a2][b5] ^ MUL[a1][b6] ^ b7)
            e8 = (a8 ^ MUL[a7][b1] ^ MUL[a6][b2] ^ MUL[a5][b3]
                  ^ MUL[a4][b4] ^ MUL[a3][b5] ^ MUL[a2][b6]
                  ^ MUL[a1][b7] ^ b8)
            records[e4].append((fa[m] | fb[mb], e5, e6, e7, e8))
    return records


def lambda_of(r: int, tail, a: int) -> int:
    """lambda_R(a) = r a^4 + e5 a^3 + e6 a^2 + e7 a + e8 (Horner)."""
    e5, e6, e7, e8 = tail
    t = MUL[r][a] ^ e5
    t = MUL[t][a] ^ e6
    t = MUL[t][a] ^ e7
    return MUL[t][a] ^ e8


def build_graph(records_r, r):
    """Vertices (a,lambda), adjacency bitmasks, and the R-clique member lists."""
    vid, verts = {}, []
    cliques = []
    for mask, e5, e6, e7, e8 in records_r:
        members = []
        for a in range(32):
            if mask >> a & 1:
                key = (a, lambda_of(r, (e5, e6, e7, e8), a))
                if key not in vid:
                    vid[key] = len(verts)
                    verts.append(key)
                members.append(vid[key])
        cliques.append(tuple(members))
    n = len(verts)
    neigh = [0] * n
    for mem in cliques:
        for i, j in combinations(mem, 2):
            neigh[i] |= 1 << j
            neigh[j] |= 1 << i
    return verts, neigh, cliques, vid


def edge_count(neigh):
    return sum(bin(m).count("1") for m in neigh) // 2


def class_span_core(verts, neigh, need):
    """Peel vertices whose surviving neighbours span < `need` distinct
    first coordinates.  Every vertex of a clique with `need`+1 distinct
    first coordinates survives, so an empty core certifies no such clique."""
    n = len(verts)
    alive = (1 << n) - 1
    changed = True
    while changed:
        changed = False
        m = alive
        while m:
            lb = m & -m
            v = lb.bit_length() - 1
            m ^= lb
            nb = neigh[v] & alive
            classes = set()
            while nb:
                l2 = nb & -nb
                classes.add(verts[l2.bit_length() - 1][0])
                nb ^= l2
            if len(classes) < need:
                alive ^= lb
                changed = True
    return alive


def max_clique(neigh, initial_best=0):
    """Exact maximum clique (Tomita-style branch and bound, bitsets)."""
    n = len(neigh)
    best = initial_best
    best_set = 0
    if n == 0:
        return best, best_set

    def expand(cand, cur, size):
        nonlocal best, best_set
        order, bound = [], []
        un = cand
        colour = 0
        while un:
            colour += 1
            avail = un
            while avail:
                lb = avail & -avail
                v = lb.bit_length() - 1
                order.append(v)
                bound.append(colour)
                un ^= lb
                avail &= ~(neigh[v] | lb)
        for idx in range(len(order) - 1, -1, -1):
            if size + bound[idx] <= best:
                return
            v = order[idx]
            newcand = cand & neigh[v]
            if newcand:
                expand(newcand, cur | (1 << v), size + 1)
            elif size + 1 > best:
                best = size + 1
                best_set = cur | (1 << v)
            cand &= ~(1 << v)

    expand((1 << n) - 1, 0, 0)
    return best, best_set


def induced(neigh, keep_ids):
    """Induced subgraph on the given vertex ids (order preserved)."""
    pos = {v: i for i, v in enumerate(keep_ids)}
    sub = [0] * len(keep_ids)
    for i, v in enumerate(keep_ids):
        nb = neigh[v]
        while nb:
            lb = nb & -nb
            u = lb.bit_length() - 1
            nb ^= lb
            if u in pos:
                sub[i] |= 1 << pos[u]
    return sub


def dsatur(neigh):
    n = len(neigh)
    colours = [-1] * n
    sat = [set() for _ in range(n)]
    degs = [bin(neigh[v]).count("1") for v in range(n)]
    for _ in range(n):
        v = max(
            (u for u in range(n) if colours[u] < 0),
            key=lambda u: (len(sat[u]), degs[u]),
        )
        c = 0
        while c in sat[v]:
            c += 1
        colours[v] = c
        nb = neigh[v]
        while nb:
            lb = nb & -nb
            sat[lb.bit_length() - 1].add(c)
            nb ^= lb
    return colours


def edge_pair_set(verts, neigh):
    pairs = set()
    for i in range(len(verts)):
        nb = neigh[i]
        while nb:
            lb = nb & -nb
            j = lb.bit_length() - 1
            nb ^= lb
            if j > i:
                pairs.add(frozenset((verts[i], verts[j])))
    return pairs


def main():
    t0 = time.time()
    out_dir = Path(__file__).resolve().parent
    root = out_dir.parents[1]

    # ---- Stage 1: enumerate all valid 17-sets R (two independent splits).
    records = enumerate_r_sets(list(range(16)), list(range(16, 32)))
    counts = [len(records[r]) for r in range(32)]
    total = sum(counts)
    print(f"[{time.time()-t0:6.1f}s] R-sets with e1=e2=e3=0: total={total}")
    print("per-r counts:", counts)

    records_alt = enumerate_r_sets(list(range(0, 32, 2)), list(range(1, 32, 2)))
    for r in range(32):
        assert sorted(records[r]) == sorted(records_alt[r]), r
    print(f"[{time.time()-t0:6.1f}s] alternate-split enumeration: IDENTICAL")

    # ---- Stage 2: from-scratch verification of every record.
    for r in range(32):
        for mask, e5, e6, e7, e8 in records[r]:
            assert bin(mask).count("1") == 17
            st = stats_from_mask(mask)
            assert st[0] == st[1] == st[2] == 0
            assert st[3] == r and st[4:] == (e5, e6, e7, e8)
    print(f"[{time.time()-t0:6.1f}s] every record re-verified from scratch")

    # scaling bijection sanity: all nonzero-r counts must agree
    assert len({counts[r] for r in range(1, 32)}) == 1

    # ---- Stage 3: cross-check against the K32 certificate masks.
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "k32", root / "evidence" / "f32_four_statistic_k32_verifier.py"
    )
    k32 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k32)
    mask_sets = [set(m for m, *_ in records[r]) for r in range(32)]
    k32_r_used = set()
    for a in range(32):
        row = k32.EDGE_WITNESS_MASK_ROWS[a]
        for off, mask in enumerate(row):
            b = a + off + 1
            st = stats_from_mask(mask)
            assert st[0] == st[1] == st[2] == 0
            r = st[3]
            k32_r_used.add(r)
            assert mask in mask_sets[r]
            tail = st[4:]
            assert lambda_of(r, tail, a) == layer(a)
            assert lambda_of(r, tail, b) == layer(b)
    print(
        f"[{time.time()-t0:6.1f}s] all 496 K32 witness masks found in "
        f"enumeration; lambda pattern matches layer(); r values used by K32: "
        f"{sorted(k32_r_used)}"
    )

    # ---- Stage 4: build G_0 and G_1, verify scaling isomorphism for all r.
    summary = {}
    graphs = {}
    for r in (0, 1):
        verts, neigh, cliques, vid = build_graph(records[r], r)
        graphs[r] = (verts, neigh, cliques, vid)
        print(
            f"[{time.time()-t0:6.1f}s] G_{r}: {len(verts)} vertices, "
            f"{edge_count(neigh)} edges, {len(cliques)} R-cliques"
        )

    verts1, neigh1, _, _ = graphs[1]
    base_pairs = edge_pair_set(verts1, neigh1)
    base_verts = set(verts1)
    for r in range(2, 32):
        c = fpow(r, 8)
        assert fpow(c, 4) == r
        c8 = fpow(c, 8)
        vr, nr, cl, _ = build_graph(records[r], r)
        mapped_verts = {(MUL[c][a], MUL[c8][lam]) for a, lam in verts1}
        assert mapped_verts == set(vr)
        mapped_pairs = {
            frozenset(((MUL[c][a1], MUL[c8][l1]), (MUL[c][a2], MUL[c8][l2])))
            for (a1, l1), (a2, l2) in base_pairs
        }
        assert mapped_pairs == edge_pair_set(vr, nr)
    print(
        f"[{time.time()-t0:6.1f}s] scaling isomorphism G_1 -> G_r verified "
        f"edge-by-edge for every r != 0"
    )

    # ---- Stage 5: exact clique analysis of G_0 and G_1.
    for r in (0, 1):
        verts, neigh, cliques, vid = graphs[r]
        core = class_span_core(verts, neigh, 17)
        core_size = bin(core).count("1")
        print(f"[{time.time()-t0:6.1f}s] G_{r}: 17-class-span core size = {core_size}")
        if core_size == 0:
            omega = 17 if cliques else 0
            witness_ids = list(cliques[0]) if cliques else []
            print(f"        => no K18 possible; omega(G_{r}) = {omega}")
        else:
            keep = []
            m = core
            while m:
                lb = m & -m
                keep.append(lb.bit_length() - 1)
                m ^= lb
            sub = induced(neigh, keep)
            omega_core, wset = max_clique(sub, initial_best=17)
            if omega_core > 17:
                omega = omega_core
                witness_ids = [
                    keep[i] for i in range(len(keep)) if wset >> i & 1
                ]
                print(f"        => omega(G_{r}) = {omega} (K{omega} FOUND)")
            else:
                omega = 17
                witness_ids = list(cliques[0])
                print(f"        => core has no K18; omega(G_{r}) = 17")
        summary[r] = {
            "n_rsets": len(records[r]),
            "n_verts": len(verts),
            "n_edges": edge_count(neigh),
            "omega": omega,
            "omega_witness": [list(verts[i]) for i in witness_ids],
        }

    # ---- Stage 6: task 4 -- does the K32 pattern retain any K18?
    print("layer pattern:", [layer(a) for a in range(32)])
    h_results = {}
    for r in range(32):
        verts, neigh, cliques, vid = (
            graphs[r] if r in graphs else build_graph(records[r], r)
        )
        keep = []
        for a in range(32):
            i = vid.get((a, layer(a)))
            if i is not None:
                keep.append(i)
        sub = induced(neigh, keep)
        om, wset = max_clique(sub)
        wit = [verts[keep[i]] for i in range(len(keep)) if wset >> i & 1]
        h_results[r] = {"n_verts": len(keep), "omega": om,
                        "witness": [list(w) for w in wit]}
    h_omegas = [h_results[r]["omega"] for r in range(32)]
    print(f"[{time.time()-t0:6.1f}s] K32-pattern subgraphs H_r: omegas =", h_omegas)
    print("max over r of omega(H_r):", max(h_omegas))

    # ---- Stage 7: DSATUR upper bound for chi(G_0), chi(G_1).
    for r in (0, 1):
        verts, neigh, cliques, vid = graphs[r]
        cols = dsatur(neigh)
        used = max(cols) + 1
        summary[r]["dsatur_colours"] = used
        print(f"[{time.time()-t0:6.1f}s] G_{r}: DSATUR uses {used} colours")

    # ---- Persist data for certificate extraction / downstream work.
    dump = {
        "counts": counts,
        "records": {str(r): [list(x) for x in records[r]] for r in range(32)},
        "summary": {str(r): summary[r] for r in summary},
        "h_results": {str(r): h_results[r] for r in h_results},
    }
    (out_dir / "e4_refinement_data.json").write_text(json.dumps(dump))
    print(f"[{time.time()-t0:6.1f}s] wrote e4_refinement_data.json")


if __name__ == "__main__":
    main()

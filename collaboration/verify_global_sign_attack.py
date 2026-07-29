#!/usr/bin/env python3
"""Exact verifier for collaboration/fable_global_sign_attack.md.

Stdlib only.  Deterministic (fixed seeds).  Sections:

  (1) binomial parities used in the gauge lemmas
  (2) row-sign invariant P of one-factorizations:
        - exhaustive on K_6 and K_8 (with OF counts as sanity anchors)
        - invariance under vertex/colour relabelling and cycle switches
        - sampled distribution on K_10 and K_18, with explicit K_18
          certificates
  (3) pfaffian-sign products: vertex-relabelling variance certificate
  (4) LS(2,3,9): pair-sign system, vertex products = derived-OF P,
        automatic even-negative-count law, gauge flips of the full product
  (5) k=2 sanity: the unique colouring family of J(4,2)
"""

import random
from itertools import combinations
from math import comb


def sgn_seq(seq):
    """Sign of a sequence of distinct comparables (parity of inversions)."""
    inv = sum(1 for i in range(len(seq)) for j in range(i + 1, len(seq))
              if seq[i] > seq[j])
    return -1 if inv & 1 else 1


# ---------------------------------------------------------------- matchings
def perfect_matchings(verts, edges):
    """All perfect matchings of vert-set using allowed edge set (frozensets)."""
    verts = sorted(verts)
    if not verts:
        yield frozenset()
        return
    v = verts[0]
    rest = verts[1:]
    for w in rest:
        e = frozenset((v, w))
        if e in edges:
            sub = [u for u in rest if u != w]
            for m in perfect_matchings(sub, edges):
                yield m | {e}


def enumerate_ofs(n2):
    """All one-factorizations of K_{n2}, canonically ordered:
    factor i-1 is the factor containing edge {0,i}.  Yields lists of
    matchings (each a frozenset of frozenset edges)."""
    all_edges = set(frozenset(e) for e in combinations(range(n2), 2))

    def rec(i, remaining):
        if i == n2:
            yield []
            return
        base = frozenset((0, i))
        if base not in remaining:
            return
        others = [v for v in range(1, n2) if v != i]
        usable = remaining - {base}
        for m in perfect_matchings(others, usable):
            fac = m | {base}
            for tail in rec(i + 1, remaining - fac):
                yield [fac] + tail

    yield from rec(1, all_edges)


def edge_colour_map(of):
    return {e: c for c, fac in enumerate(of) for e in fac}


def row_sign_product(of, verts=None):
    """P = product over vertices t of sgn(x -> colour(tx))."""
    col = edge_colour_map(of)
    if verts is None:
        verts = sorted({v for fac in of for e in fac for v in e})
    p = 1
    for t in verts:
        seq = [col[frozenset((t, x))] for x in verts if x != t]
        p *= sgn_seq(seq)
    return p


def pf_sign(matching, verts):
    """Pfaffian sign: parity of the vertex sequence i1 j1 i2 j2 ...
    (edges sorted by smaller endpoint, each edge written increasing)."""
    pos = {v: i for i, v in enumerate(sorted(verts))}
    seq = []
    for e in sorted(matching, key=lambda e: min(pos[v] for v in e)):
        a, b = sorted(e, key=lambda v: pos[v])
        seq += [pos[a], pos[b]]
    return sgn_seq(seq)


def random_of(n2, rng):
    """Random one-factorization of K_{n2} by sequential random matchings."""
    while True:
        remaining = set(frozenset(e) for e in combinations(range(n2), 2))
        of = []
        ok = True
        for _ in range(n2 - 1):
            m = random_matching(list(range(n2)), remaining, rng)
            if m is None:
                ok = False
                break
            of.append(m)
            remaining -= m
        if ok:
            return of


def random_matching(verts, edges, rng):
    if not verts:
        return frozenset()
    v = min(verts)
    partners = [w for w in verts if w != v and frozenset((v, w)) in edges]
    rng.shuffle(partners)
    for w in partners:
        sub = [u for u in verts if u not in (v, w)]
        m = random_matching(sub, edges, rng)
        if m is not None:
            return m | {frozenset((v, w))}
    return None


def relabel_of(of, vperm=None, cperm=None):
    out = of
    if vperm is not None:
        out = [frozenset(frozenset(vperm[v] for v in e) for e in fac)
               for fac in out]
    if cperm is not None:
        new = [None] * len(out)
        for c, fac in enumerate(out):
            new[cperm[c]] = fac
        out = new
    return out


def cycle_switch(of, rng):
    """Swap two colours along one cycle of their union; None if impossible."""
    n = len(of)
    c, d = rng.sample(range(n), 2)
    adj = {}
    for e in of[c] | of[d]:
        a, b = tuple(e)
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    start = min(adj)
    cyc_verts = {start}
    prev, cur = None, start
    while True:
        nxt = [w for w in adj[cur] if w != prev]
        w = nxt[0]
        if w == start:
            break
        cyc_verts.add(w)
        prev, cur = cur, w
    if len(cyc_verts) == len(adj):
        # single cycle: switching all of it = colour swap; still a valid test
        pass
    inc = lambda e: any(v in cyc_verts for v in e)
    new_c = frozenset(e for e in of[c] if not inc(e)) | \
        frozenset(e for e in of[d] if inc(e))
    new_d = frozenset(e for e in of[d] if not inc(e)) | \
        frozenset(e for e in of[c] if inc(e))
    out = list(of)
    out[c], out[d] = new_c, new_d
    return out


# ---------------------------------------------------------------- LS(2,3,9)
def sts_completions(pairs_left, triples_left, rng=None):
    """DFS: one STS(9) covering exactly the given pair set from allowed
    triples; yields frozensets of triples."""
    if not pairs_left:
        yield frozenset()
        return
    p = min(pairs_left)
    cand = [t for t in triples_left if p <= t]
    if rng is not None:
        rng.shuffle(cand)
    for t in cand:
        tp = {frozenset(c) for c in combinations(sorted(t), 2)}
        if not tp <= pairs_left:
            continue
        ok_triples = [u for u in triples_left
                      if not ({frozenset(c) for c in
                               combinations(sorted(u), 2)} & tp) or u == t]
        ok_triples = [u for u in ok_triples if u != t]
        for restm in sts_completions(pairs_left - tp, ok_triples, rng):
            yield restm | {t}
            if rng is not None:
                return  # randomized mode: first solution only


def random_large_set_9(rng):
    """One random LS(2,3,9): 7 pairwise disjoint STS(9) partitioning triples."""
    all_triples = [frozenset(t) for t in combinations(range(9), 3)]
    all_pairs = {frozenset(p) for p in combinations(range(9), 2)}
    while True:
        avail = set(all_triples)
        classes = []
        ok = True
        for _ in range(7):
            found = None
            for m in sts_completions(set(all_pairs), list(avail), rng):
                found = m
                break
            if found is None:
                ok = False
                break
            classes.append(found)
            avail -= found
        if ok:
            return classes


def ls9_pair_signs(classes):
    """eps for every pair: sign of x -> colour({a,b,x})."""
    colour = {t: c for c, cls in enumerate(classes) for t in cls}
    eps = {}
    for a, b in combinations(range(9), 2):
        seq = [colour[frozenset((a, b, x))] for x in range(9)
               if x not in (a, b)]
        assert sorted(seq) == list(range(7)), "pair star not rainbow"
        eps[frozenset((a, b))] = sgn_seq(seq)
    return eps


def main():
    rng = random.Random(835)

    print("== (1) binomial parities ==")
    for n, k in [(19, 2), (7, 2), (20, 3), (18, 3), (30, 15), (32, 15),
                 (32, 14), (17, 2), (9, 2)]:
        print(f"   C({n},{k}) = {comb(n, k)}  parity {comb(n, k) % 2}")

    print("== (2) row-sign invariant P ==")
    for n2, expected in [(4, 1), (6, 6), (8, 6240)]:
        vals = {}
        cnt = 0
        for of in enumerate_ofs(n2):
            cnt += 1
            p = row_sign_product(of)
            vals[p] = vals.get(p, 0) + 1
        print(f"   K_{n2}: {cnt} one-factorizations "
              f"(expected {expected}); P distribution {vals}")
        assert cnt == expected

    # invariance tests on K_8 samples
    sample = []
    for i, of in enumerate(enumerate_ofs(8)):
        if i % 977 == 0:
            sample.append(of)
        if len(sample) >= 6:
            break
    for of in sample:
        p = row_sign_product(of)
        vp = list(range(8))
        rng.shuffle(vp)
        cp = list(range(7))
        rng.shuffle(cp)
        assert row_sign_product(relabel_of(of, vperm=dict(enumerate(vp)))) == p
        assert row_sign_product(relabel_of(of, cperm=cp)) == p
        for _ in range(5):
            assert row_sign_product(cycle_switch(of, rng)) == p
    print("   K_8 invariance: vertex relabel / colour relabel / "
          "cycle switch all preserve P (6 OFs x tests)")

    for n2, tries in [(10, 300), (14, 100), (18, 60)]:
        vals = {}
        first = {}
        for _ in range(tries):
            of = random_of(n2, rng)
            p = row_sign_product(of)
            vals[p] = vals.get(p, 0) + 1
            if p not in first:
                first[p] = of
        print(f"   K_{n2}: sampled {tries} random OFs; P distribution {vals}")
        if n2 == 18:
            for p, of in sorted(first.items()):
                col = edge_colour_map(of)
                rows = []
                for t in range(18):
                    rows.append("".join(f"{col[frozenset((t, x))]:x}"
                                        if x != t else "." for x in range(18)))
                print(f"   K_18 certificate with P={p:+d} "
                      f"(row t = colours to 0..17, hex):")
                for r in rows:
                    print("      " + r)

    print("== (3) pfaffian products Q = prod_c pf-sign(M_c) ==")

    def q_of(of, verts):
        q = 1
        for fac in of:
            q *= pf_sign(fac, verts)
        return q

    varied = False
    for of in sample:
        q0 = q_of(of, range(8))
        for _ in range(10):
            vp = list(range(8))
            rng.shuffle(vp)
            if q_of(relabel_of(of, vperm=dict(enumerate(vp))), range(8)) != q0:
                varied = True
                break
        for _ in range(5):
            if q_of(cycle_switch(of, rng), range(8)) != q0:
                print("   Q changed under a cycle switch")
        if varied:
            break
    print(f"   Q vertex-relabelling variance found: {varied}")

    for n2 in (6, 8):
        joint = {}
        for of in enumerate_ofs(n2):
            key = (row_sign_product(of), q_of(of, range(n2)))
            joint[key] = joint.get(key, 0) + 1
        print(f"   K_{n2}: joint (P,Q) distribution {joint}")

    jq = {}
    for _ in range(60):
        of = random_of(18, rng)
        key = (row_sign_product(of), q_of(of, range(18)))
        jq[key] = jq.get(key, 0) + 1
    print(f"   K_18: sampled joint (P,Q) distribution {jq}")

    print("== (3b) per-Steiner-system pfaffian invariant Sigma ==")

    def derived_matching(design, y, verts):
        return frozenset(frozenset(b - {y}) for b in design if y in b)

    def sigma(design, pts):
        s = 1
        for y in pts:
            s *= pf_sign(derived_matching(design, y, pts),
                         [v for v in pts if v != y])
        return s

    # all 30 labelled Fano planes via exhaustive cover of pairs by triples
    fanos = []
    all_pairs7 = {frozenset(p) for p in combinations(range(7), 2)}
    all_triples7 = [frozenset(t) for t in combinations(range(7), 3)]

    def fano_rec(pairs_left, chosen, start):
        if not pairs_left:
            fanos.append(frozenset(chosen))
            return
        p = min(pairs_left, key=sorted)
        for t in all_triples7:
            if p <= t:
                tp = {frozenset(c) for c in combinations(sorted(t), 2)}
                if tp <= pairs_left:
                    fano_rec(pairs_left - tp, chosen + [t], 0)

    fano_rec(set(all_pairs7), [], 0)
    fanos = list(set(fanos))
    sig7 = {}
    for d in fanos:
        sig7[sigma(d, list(range(7)))] = sig7.get(sigma(d, list(range(7))), 0) + 1
    print(f"   {len(fanos)} labelled Fano planes; Sigma distribution {sig7}")

    # STS(9): random sample
    sig9 = {}
    all_pairs9 = {frozenset(p) for p in combinations(range(9), 2)}
    all_triples9 = [frozenset(t) for t in combinations(range(9), 3)]
    for _ in range(50):
        m = None
        for mm in sts_completions(set(all_pairs9), list(all_triples9), rng):
            m = mm
            break
        s = sigma(m, list(range(9)))
        sig9[s] = sig9.get(s, 0) + 1
        vp = list(range(9))
        rng.shuffle(vp)
        m2 = frozenset(frozenset(vp[v] for v in t) for t in m)
        if sigma(m2, list(range(9))) != s:
            print("   Sigma changed under vertex relabelling (STS(9))")
    print(f"   50 random STS(9): Sigma distribution {sig9}")

    # LS(2,3,9): verify prod_y Q_y = prod_c Sigma(D_c)
    classes = random_large_set_9(rng)
    lhs = 1
    for y in range(9):
        derived = [derived_matching(cls, y, range(9)) for cls in classes]
        lhs *= q_of(derived, [v for v in range(9) if v != y])
    rhs = 1
    for cls in classes:
        rhs *= sigma(cls, list(range(9)))
    assert lhs == rhs
    print(f"   LS(2,3,9): prod_y Q_y = prod_c Sigma(D_c) = {lhs:+d}  (verified)")

    print("== (3c) Sigma' on Steiner quadruple systems ==")

    def quad_systems(v, limit, rng_=None):
        """Yield SQS(v): 4-sets covering every 3-set exactly once."""
        triples = {frozenset(t) for t in combinations(range(v), 3)}
        quads = [frozenset(q) for q in combinations(range(v), 4)]
        out = []

        def rec(trip_left, avail, chosen):
            if len(out) >= limit:
                return
            if not trip_left:
                out.append(frozenset(chosen))
                return
            t0 = min(trip_left, key=sorted)
            cand = [q for q in avail if t0 <= q]
            if rng_ is not None:
                rng_.shuffle(cand)
            for q in cand:
                qt = {frozenset(c) for c in combinations(sorted(q), 3)}
                if qt <= trip_left:
                    rec(trip_left - qt,
                        [u for u in avail if u != q], chosen + [q])
                    if len(out) >= limit:
                        return

        rec(set(triples), quads, [])
        return out

    def sigma2(design, pts):
        """Sigma' = product over point pairs of pf-sign of the doubly
        derived perfect matching."""
        s = 1
        for y, z in combinations(pts, 2):
            m = frozenset(frozenset(b - {y, z}) for b in design
                          if y in b and z in b)
            s *= pf_sign(m, [v for v in pts if v not in (y, z)])
        return s

    sqs8 = quad_systems(8, 100)
    d8 = {}
    for d in sqs8:
        d8[sigma2(d, list(range(8)))] = d8.get(sigma2(d, list(range(8))), 0) + 1
    print(f"   {len(sqs8)} labelled SQS(8); Sigma' distribution {d8}")

    sqs10 = quad_systems(10, 1)
    assert sqs10, "no SQS(10) found"
    base10 = sqs10[0]
    print(f"   SQS(10) found; Sigma'(base) = {sigma2(base10, list(range(10))):+d}")

    def double_sqs(sq_a, sq_b, of_a, of_b, perm):
        """Classical doubling: SQS(2v) from two SQS(v) and two OFs of K_v."""
        blocks = [frozenset(b) for b in sq_a]
        blocks += [frozenset(x + 10 for x in b) for b in sq_b]
        for i, fac in enumerate(of_a):
            for e1 in fac:
                for e2 in of_b[perm[i]]:
                    blocks.append(frozenset(e1 | {x + 10 for x in e2}))
        return blocks

    d20 = {}
    for trial in range(20):
        vp = list(range(10))
        rng.shuffle(vp)
        sq_b = [frozenset(vp[x] for x in b) for b in base10]
        of_a = random_of(10, rng)
        of_b = random_of(10, rng)
        perm = list(range(9))
        rng.shuffle(perm)
        blocks = double_sqs(base10, sq_b, of_a, of_b, perm)
        # verify SQS(20)
        seen = set()
        for b in blocks:
            for t in combinations(sorted(b), 3):
                ft = frozenset(t)
                assert ft not in seen
                seen.add(ft)
        assert len(seen) == comb(20, 3)
        s = sigma2(blocks, list(range(20)))
        d20[s] = d20.get(s, 0) + 1
        if trial == 0:
            wp = list(range(20))
            rng.shuffle(wp)
            blocks2 = [frozenset(wp[x] for x in b) for b in blocks]
            print(f"   Sigma'(SQS(20)) relabelling check: "
                  f"{s:+d} -> {sigma2(blocks2, list(range(20))):+d}")
    print(f"   20 doubled SQS(20): Sigma' distribution {d20}")

    print("== (4) LS(2,3,9) pair-sign system ==")
    full_products = {}
    pt_products = {}
    for i in range(8):
        classes = random_large_set_9(rng)
        eps = ls9_pair_signs(classes)
        # vertex products and the automatic law
        pys = []
        for y in range(9):
            py = 1
            for pr, s in eps.items():
                if y in pr:
                    py *= s
            # cross-check against derived one-factorization row product
            derived = [frozenset(t - {y} for t in cls if y in t)
                       for cls in classes]
            assert row_sign_product(derived,
                                    verts=[v for v in range(9) if v != y]) == py
            pys.append(py)
        prod_all = 1
        for s in eps.values():
            prod_all *= s
        assert pys.count(-1) % 2 == 0, "even-negative law violated"
        p_tot = 1
        for v in pys:
            p_tot *= v
        assert p_tot == 1
        full_products[prod_all] = full_products.get(prod_all, 0) + 1
        pt_products[tuple(sorted(pys))] = \
            pt_products.get(tuple(sorted(pys)), 0) + 1
        if i == 0:
            # gauge flips of the full 36-pair product
            colour = {t: c for c, cls in enumerate(classes) for t in cls}
            # odd point transposition (0 1)
            classes_t = [frozenset(frozenset({0: 1, 1: 0}.get(v, v)
                                             for v in t) for t in cls)
                         for cls in classes]
            eps_t = ls9_pair_signs(classes_t)
            pa = 1
            for s in eps_t.values():
                pa *= s
            # odd colour transposition: swap classes 0,1
            classes_c = list(classes)
            classes_c[0], classes_c[1] = classes_c[1], classes_c[0]
            eps_c = ls9_pair_signs(classes_c)
            pc = 1
            for s in eps_c.values():
                pc *= s
            print(f"   large set #1: full product {prod_all:+d}; after odd "
                  f"point transposition {pa:+d}; after odd colour swap {pc:+d}")
    print(f"   8 random LS(2,3,9): full-product distribution {full_products}")
    print(f"   vertex-product (P_y) multiset distribution: {pt_products}")

    print("== (5) k=2 sanity: J(4,2) ==")
    ofs4 = list(enumerate_ofs(4))
    assert len(ofs4) == 1
    of = ofs4[0]
    colour = edge_colour_map(of)
    g = 1
    for t in range(4):
        seq = [colour[frozenset((t, x))] for x in range(4) if x != t]
        g *= sgn_seq(seq)
    print(f"   G(k=2) = {g:+d} = P(OF(K_4)) = {row_sign_product(of):+d}")
    assert g == row_sign_product(of) == 1

    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()

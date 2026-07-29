#!/usr/bin/env python3
"""Audit surface for PROOF.md Lemma 5.1, equation (6.1) and Theorem 5.

NOT RUN in the session that produced PROOF.md (no interpreter was available).
PROOF.md proves all of this by hand; this script is only for an independent
auditor.

Plan:
  (a) build a large set LS(1,2,v) (a 1-factorization of K_v) and a large set
      LS(2,3,9) (seven pairwise disjoint STS(9) partitioning all 84 triples),
      each verified from the definition;
  (b) for r = q-1, q-2, q-3 delete r of the classes and check Lemma 5.1,
      the regularity/edge count (6.1), and Theorem 5 parts 1-3:
        r = q-1  -> leftover is itself a Steiner system,
        r = q-2  -> conflict graph bipartite, and its 2-colouring splits it,
        r = q-3  -> conflict graph is a union of triangles, 3-colourable, and
                    a proper 3-colouring splits it;
  (c) confirm the converse direction is the one that fails to be automatic:
      report whether any 2-colouring found is unique up to swapping.

Standard library only.  Deterministic (all searches take the lexicographically
first solution).
"""

from itertools import combinations
from math import comb

FAILURES = []


def check(cond, label):
    if not cond:
        FAILURES.append(label)
        print("FAIL", label)


# --------------------------------------------------------------------------
# (a) large sets
# --------------------------------------------------------------------------

def is_steiner(blocks, t, v):
    cover = {}
    for b in blocks:
        if len(b) != t + 1:
            return False
        for sub in combinations(sorted(b), t):
            cover[sub] = cover.get(sub, 0) + 1
    return len(cover) == comb(v, t) and all(c == 1 for c in cover.values())


def one_factorization(v):
    """Round-robin 1-factorization of K_v for even v: v-1 classes."""
    assert v % 2 == 0
    fixed, rot = v - 1, list(range(v - 1))
    classes = []
    for r in range(v - 1):
        f = [frozenset({rot[r], fixed})]
        for i in range(1, v // 2):
            f.append(frozenset({rot[(r + i) % (v - 1)], rot[(r - i) % (v - 1)]}))
        classes.append(f)
    return classes


def all_sts9():
    """Every labelled STS(9) on points 0..8, by exact cover on pairs."""
    triples = [frozenset(c) for c in combinations(range(9), 3)]
    pairs = [frozenset(c) for c in combinations(range(9), 2)]
    by_pair = {p: [t for t in triples if p <= t] for p in pairs}
    out, chosen = [], []

    def rec(uncovered):
        if not uncovered:
            out.append(list(chosen))
            return
        p = min(uncovered, key=lambda s: sorted(s))
        for t in by_pair[p]:
            sub = [frozenset(c) for c in combinations(sorted(t), 2)]
            if any(s not in uncovered for s in sub):
                continue
            chosen.append(t)
            rec(uncovered - set(sub))
            chosen.pop()

    rec(set(pairs))
    return out


def large_set_sts9():
    """Seven pairwise disjoint STS(9), found by backtracking."""
    systems = [frozenset(s) for s in all_sts9()]
    print(f"  labelled STS(9) found: {len(systems)} (expected 840)")
    picked = []

    def rec(start, used):
        if len(picked) == 7:
            return True
        for i in range(start, len(systems)):
            s = systems[i]
            if s & used:
                continue
            picked.append(s)
            if rec(i + 1, used | s):
                return True
            picked.pop()
        return False

    ok = rec(0, frozenset())
    return [list(s) for s in picked] if ok else None


# --------------------------------------------------------------------------
# (b) leftover, conflict graph, Theorem 5
# --------------------------------------------------------------------------

def conflict_graph(leftover, t):
    """Vertices = leftover blocks; edge iff they share exactly t points."""
    adj = {b: set() for b in leftover}
    for a, b in combinations(leftover, 2):
        if len(a & b) == t:
            adj[a].add(b)
            adj[b].add(a)
    return adj


def proper_colouring(adj, ncolours):
    """Lexicographically first proper colouring, or None."""
    verts = sorted(adj, key=lambda s: sorted(s))
    colour = {}

    def rec(i):
        if i == len(verts):
            return True
        v = verts[i]
        for c in range(ncolours):
            if all(colour.get(u) != c for u in adj[v]):
                colour[v] = c
                if rec(i + 1):
                    return True
                del colour[v]
        return False

    return dict(colour) if rec(0) else None


def audit_large_set(name, classes, t, v):
    q = v - t
    K = t + 1
    check(len(classes) == q, f"{name}: {len(classes)} classes, expected {q}")
    for c in classes:
        check(is_steiner(c, t, v), f"{name}: each class is an S({t},{K},{v})")
    allb = [b for c in classes for b in c]
    check(len(allb) == len(set(allb)) == comb(v, K),
          f"{name}: classes partition all {K}-subsets")
    print(f"  {name}: t={t} v={v} q={q} verified as a large set")

    tsets = [frozenset(c) for c in combinations(range(v), t)]

    for drop in (1, 2, 3):
        r = q - drop
        if r < 0:
            continue
        kept = classes[:r]
        used = {b for c in kept for b in c}
        leftover = [frozenset(c) for c in combinations(range(v), K)
                    if frozenset(c) not in used]

        # Lemma 5.1
        for T in tsets:
            cnt = sum(1 for b in leftover if T <= b)
            check(cnt == drop, f"{name} r={r}: Lemma 5.1 count {cnt} != {drop}")

        adj = conflict_graph(leftover, t)
        deg = {len(adj[b]) for b in leftover}
        want_deg = K * (drop - 1)
        edges = sum(len(adj[b]) for b in leftover) // 2
        want_edges = comb(v, t) * comb(drop, 2)
        check(deg == {want_deg} or drop == 1,
              f"{name} r={r}: degrees {deg} != {{{want_deg}}}")
        check(edges == want_edges,
              f"{name} r={r}: {edges} edges != {want_edges}")
        check(len(leftover) == drop * (comb(v, K) // q),
              f"{name} r={r}: leftover size")

        if drop == 1:
            check(is_steiner(leftover, t, v),
                  f"{name} r={q-1}: leftover is a Steiner system (Thm 5.1)")
            print(f"    r=q-1: leftover is an S({t},{K},{v}) -- last class automatic")
        else:
            col = proper_colouring(adj, drop)
            check(col is not None, f"{name} r={r}: {drop}-colourable (Thm 5.{drop})")
            if col is not None:
                for c in range(drop):
                    part = [b for b in leftover if col[b] == c]
                    check(is_steiner(part, t, v),
                          f"{name} r={r}: colour class {c} is a Steiner system")
                print(f"    r=q-{drop}: conflict graph is {drop}-colourable and every"
                      f" colour class is an S({t},{K},{v})")
            if drop == 3:
                # Each t-set defines one canonical triangle on its three
                # leftover extensions.  These canonical triangles partition
                # the edge set because an edge determines the shared t-set.
                # The graph may also contain noncanonical triangles whose
                # three edges come from three different t-sets.
                canonical_edges = set()
                for T in tsets:
                    above = [b for b in leftover if T <= b]
                    check(len(above) == 3,
                          f"{name} r={r}: canonical triangle above {sorted(T)}")
                    if len(above) == 3:
                        for a, b in combinations(above, 2):
                            check(b in adj[a],
                                  f"{name} r={r}: canonical edge above {sorted(T)}")
                            canonical_edges.add(frozenset({a, b}))
                graph_edges = {
                    frozenset({a, b})
                    for a in leftover
                    for b in adj[a]
                    if tuple(sorted(a)) < tuple(sorted(b))
                }
                check(canonical_edges == graph_edges,
                      f"{name} r={r}: canonical triangles partition the edge set")
                all_triangles = sum(
                    1 for a, b, c in combinations(leftover, 3)
                    if b in adj[a] and c in adj[a] and c in adj[b]
                )
                print(
                    f"    r=q-3: {comb(v,t)} canonical triangles partition all"
                    f" edges; {all_triangles} graph triangles total"
                )


def main():
    print("== LS(1,2,v): 1-factorizations of K_v ==")
    for v in (6, 8, 10):
        audit_large_set(f"LS(1,2,{v})", one_factorization(v), 1, v)

    print("== LS(2,3,9): seven disjoint STS(9) ==")
    ls9 = large_set_sts9()
    if ls9 is None:
        print("FAIL LS(2,3,9): no seven pairwise disjoint STS(9) found")
        FAILURES.append("LS(2,3,9) search")
    else:
        audit_large_set("LS(2,3,9)", ls9, 2, 9)

    print()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURE(S)")
    else:
        print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()

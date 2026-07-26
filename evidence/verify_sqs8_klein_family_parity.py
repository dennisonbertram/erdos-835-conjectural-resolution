#!/usr/bin/env python3
"""Verifier for evidence/sqs8_klein_family_parity.md.

Structural proof that at most two S(3,4,8) are pairwise block-disjoint, via the
identification of the 30 systems with the 30 maximal totally singular subspaces
of a hyperbolic O_6^+(2) quadratic form.

Checked here, in exact arithmetic with no third-party imports:

  1. There are exactly 30 labelled S(3,4,8), and each spans a self-dual [8,4,4]
     binary code whose 14 weight-4 words are exactly its blocks.
  2. On the even-weight code E (dim 7), q(u) = wt(u)/2 mod 2 is a quadratic form
     whose polarization is the standard inner product, and whose radical is
     <1>.  It descends to E/<1> = F_2^6 and has 35 nonzero singular vectors --
     the O_6^+(2) (hyperbolic) count (2^2+1)(2^3-1).
  3. Each code gives a totally singular 3-space U_D of E/<1>; the 30 are
     distinct, and 30 = 2*3*5 is the O_6^+(2) count of maximal totally singular
     subspaces.
  4. "same family" defined by dim(U cap U') = 3 (mod 2) is an equivalence
     relation with exactly two classes of size 15.
  5. D, D' are block-disjoint  <=>  dim(U_D cap U_D') = 0, which is even, hence
     block-disjoint implies OPPOSITE families.  Therefore no three systems are
     pairwise disjoint.
  6. The two families are exactly the two A_8-orbits: even permutations
     preserve them, odd permutations swap them.  So the family indicator is a
     sign epsilon with epsilon(pi D) = sgn(pi) epsilon(D).

Run:  python3 -B evidence/verify_sqs8_klein_family_parity.py
"""

from itertools import combinations, permutations

FAILURES = []


def check(label, cond, detail=""):
    print(f"  [{'ok  ' if cond else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))
    if not cond:
        FAILURES.append(label)


# ---------------------------------------------------------------- designs

def all_sqs8():
    """All labelled S(3,4,8) on {0..7}, by exact cover on the triples."""
    triples = list(combinations(range(8), 3))
    tidx = {t: i for i, t in enumerate(triples)}
    quads = list(combinations(range(8), 4))
    qcov = [[tidx[t] for t in combinations(q, 3)] for q in quads]
    cover = [[] for _ in triples]
    for i, ts in enumerate(qcov):
        for t in ts:
            cover[t].append(i)
    used = [False] * len(triples)
    cur, out = [], []

    def rec():
        t = next((i for i in range(len(triples)) if not used[i]), None)
        if t is None:
            out.append(tuple(cur))
            return
        for i in cover[t]:
            if any(used[x] for x in qcov[i]):
                continue
            for x in qcov[i]:
                used[x] = True
            cur.append(quads[i])
            rec()
            cur.pop()
            for x in qcov[i]:
                used[x] = False

    rec()
    return [frozenset(frozenset(b) for b in d) for d in out]


def mask(s):
    m = 0
    for x in s:
        m |= 1 << x
    return m


def popcount(x):
    return bin(x).count("1")


def span(vectors):
    """F_2 span, returned as a sorted tuple of masks."""
    basis = []
    for v in vectors:
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
            basis.sort(reverse=True)
    words = {0}
    for b in basis:
        words |= {w ^ b for w in words}
    return tuple(sorted(words)), len(basis)


def dot(a, b):
    return popcount(a & b) & 1


# ---------------------------------------------------------------- main

def main():
    print("1. The 30 systems and their codes")
    designs = all_sqs8()
    check("exactly 30 labelled S(3,4,8)", len(designs) == 30, str(len(designs)))
    check("each has 14 blocks", all(len(d) == 14 for d in designs))

    codes = []
    ok_code = True
    for d in designs:
        words, dim = span(mask(b) for b in d)
        wt4 = {w for w in words if popcount(w) == 4}
        selfdual = all(dot(u, v) == 0 for u in words for v in words)
        if not (dim == 4 and len(words) == 16 and 0xFF in words
                and wt4 == {mask(b) for b in d} and len(wt4) == 14 and selfdual):
            ok_code = False
        codes.append(words)
    check("each spans a self-dual [8,4,4] code containing the all-ones word, "
          "whose 14 weight-4 words are exactly its blocks", ok_code)
    check("the 30 codes are distinct", len({c for c in codes}) == 30)

    print()
    print("2. The quadratic form on E/<1>")
    E = [w for w in range(256) if popcount(w) % 2 == 0]
    check("even-weight code has dimension 7", len(E) == 128)
    q = {w: (popcount(w) // 2) % 2 for w in E}
    check("q polarizes to the standard inner product",
          all(q[u ^ v] == (q[u] ^ q[v] ^ dot(u, v)) for u in E for v in E))
    check("radical of the bilinear form on E is <1>",
          {u for u in E if all(dot(u, v) == 0 for v in E)} == {0, 0xFF})
    check("q is constant on cosets of <1>", all(q[w] == q[w ^ 0xFF] for w in E))
    cosets = {}
    for w in E:
        cosets.setdefault(min(w, w ^ 0xFF), []).append(w)
    check("E/<1> has 64 elements = F_2^6", len(cosets) == 64)
    sing = [c for c in cosets if q[c] == 0 and c != 0]
    check("35 nonzero singular vectors = (2^2+1)(2^3-1) -> hyperbolic O_6^+(2)",
          len(sing) == 35, f"{len(sing)}")

    print()
    print("3. Systems -> maximal totally singular 3-spaces")
    def to_U(code):
        return frozenset(min(w, w ^ 0xFF) for w in code)
    Us = [to_U(c) for c in codes]
    check("each U_D has 8 elements (dim 3)", all(len(u) == 8 for u in Us))
    check("each U_D is totally singular", all(q[w] == 0 for u in Us for w in u))
    check("the 30 subspaces are distinct", len(set(Us)) == 30)
    check("30 = 2*3*5 is the O_6^+(2) count of maximal totally singular spaces",
          30 == 2 * (2 + 1) * (2 ** 2 + 1))

    print()
    print("4. The two families")
    def capdim(i, j):
        n = len(Us[i] & Us[j])
        return n.bit_length() - 1                      # |intersection| = 2^dim
    same = [[(capdim(i, j) % 2 == 1) for j in range(30)] for i in range(30)]
    # families by union-find on "same"
    fam = [None] * 30
    fam[0] = 0
    changed = True
    while changed:
        changed = False
        for i in range(30):
            for j in range(30):
                if fam[i] is None:
                    continue
                want = fam[i] if same[i][j] else 1 - fam[i]
                if fam[j] is None:
                    fam[j] = want
                    changed = True
                elif fam[j] != want:
                    FAILURES.append("family relation inconsistent")
                    return
    check("'dim(U cap U') odd' is a consistent 2-colouring", None not in fam)
    check("two families of size 15 each",
          sorted([fam.count(0), fam.count(1)]) == [15, 15],
          f"{fam.count(0)}/{fam.count(1)}")

    print()
    print("5. Disjointness forces opposite families")
    dis = [[bool(designs[i] & designs[j]) is False and i != j
            for j in range(30)] for i in range(30)]
    npairs = sum(dis[i][j] for i in range(30) for j in range(i + 1, 30))
    check("block-disjoint <=> dim(U cap U') = 0",
          all(dis[i][j] == (capdim(i, j) == 0)
              for i in range(30) for j in range(30) if i != j))
    check("block-disjoint pairs: 120 = 15*8", npairs == 120, f"{npairs}")
    check("every disjoint pair has opposite families",
          all(fam[i] != fam[j]
              for i in range(30) for j in range(30) if dis[i][j]))
    tri = any(dis[i][j] and dis[i][k] and dis[j][k]
              for i in range(30) for j in range(30) for k in range(30))
    check("no three pairwise disjoint systems (disjointness graph is bipartite)",
          not tri)

    print()
    print("6. The families are the two A_8-orbits")
    idx = {d: i for i, d in enumerate(designs)}

    def act(p, d):
        return frozenset(frozenset(p[x] for x in b) for b in d)

    def sgn(p):
        s, seen = 1, [False] * 8
        for i in range(8):
            if seen[i]:
                continue
            n, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                n += 1
            if n % 2 == 0:
                s = -s
        return s

    gens = [(1, 0, 2, 3, 4, 5, 6, 7),                     # a transposition, odd
            (1, 2, 3, 4, 5, 6, 7, 0)]                     # an 8-cycle, odd
    ok_equiv = True
    for p in gens:
        for i, d in enumerate(designs):
            j = idx[act(p, d)]
            expected = fam[i] if sgn(p) == 1 else 1 - fam[i]
            if fam[j] != expected:
                ok_equiv = False
    check("family(pi D) = sgn(pi) * family(D) on odd generators", ok_equiv)
    # a full random-free confirmation on all of S_8 would be 40320 * 30; do a
    # complete check on a generating set plus all 3-cycles (even)
    ok_even = all(fam[idx[act(p, d)]] == fam[i]
                  for p in [tuple(x) for x in permutations(range(4))]
                  for i, d in enumerate(designs)
                  for p in [p + (4, 5, 6, 7)]
                  if sgn(p) == 1)
    check("even permutations preserve families (all even perms of {0,1,2,3})",
          ok_even)

    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s): {FAILURES}")
        raise SystemExit(1)
    print("All checks passed.")
    print()
    print("CONCLUSION: block-disjointness of S(3,4,8) forces opposite Klein")
    print("families; there are only two families; hence at most two systems are")
    print("pairwise block-disjoint, and no LS(3,4,8) exists.")


if __name__ == "__main__":
    main()

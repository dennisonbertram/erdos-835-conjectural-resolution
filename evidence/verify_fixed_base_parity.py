#!/usr/bin/env python3
"""Exact computations for the fixed-base parity conjecture (2026-07-24).

Conjecture P.  Let A be an S(r-1, r, 2r+1) and let D(A) be the set of
S(r-1, r, 2r+1) systems block-disjoint from A.  Claim: for all
B, C in D(A),  |B intersect C| == b (mod 2),  b = C(2r+1, r)/(r+2).

Checks performed (all exact, stdlib only):
  1. r=3: complete.  All 30 Fano planes; fixed base A; all 8 mates;
     all 28 mate pairs.
  2. r=5: complete over a fixed base A (all mates enumerated by exhaustive
     exact cover; complete for every base by uniqueness of S(4,5,11)).
     Repeated for a second base (a mate of A).
  3. Local-bijection sign invariant E(B) (product over P in A of the sign
     of pi_P^B) for every mate; pairwise sign(tau) = E(B)E(C); the
     alternating-cycle count Gamma'; the fixed-slot count (r+1)|B cap C|.
  4. "Claim S": is x_A + x_B in the GF(2) row space of W_{r-1,r}?
     (Sufficient for Conjecture P: see judgment note.)  Tested for every
     disjoint pair available and for non-disjoint control pairs.
  5. r=3 relaxed kernel class: exhaustive search over all integer vectors z
     that are differences of two sphere-transversal choice maps (one +1 and
     one -1 in some spheres, 0 elsewhere) with Wz = 0 over Z; records the
     distribution of the number of active spheres.
"""

import random
import sys
from collections import Counter
from itertools import combinations
from math import comb

sys.setrecursionlimit(100000)


def popcount(x):
    return bin(x).count("1")


# ---------- permutations ----------

def perm_sign(perm):
    n = len(perm)
    seen = [False] * n
    sign = 1
    for i in range(n):
        if not seen[i]:
            j = i
            length = 0
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                length += 1
            if length % 2 == 0:
                sign = -sign
    return sign


def perm_cycles(perm):
    """Return (number of nontrivial cycles, number of fixed points)."""
    n = len(perm)
    seen = [False] * n
    nontrivial = 0
    fixed = 0
    for i in range(n):
        if not seen[i]:
            j = i
            length = 0
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                length += 1
            if length == 1:
                fixed += 1
            else:
                nontrivial += 1
    return nontrivial, fixed


# ---------- GF(2) linear algebra on bitmask vectors ----------

class GF2Space:
    """Row space with combination tracking (certificates)."""

    def __init__(self):
        self.pivots = {}  # pivot bit -> (vector, combo mask over original rows)

    def _reduce(self, v, combo=0):
        while v:
            p = v.bit_length() - 1
            if p in self.pivots:
                pv, pc = self.pivots[p]
                v ^= pv
                combo ^= pc
            else:
                return v, combo
        return 0, combo

    def add(self, v, tag):
        v2, c2 = self._reduce(v, tag)
        if v2:
            self.pivots[v2.bit_length() - 1] = (v2, c2)
            return True
        return False

    def contains(self, v):
        return self._reduce(v)[0] == 0

    def certificate(self, v):
        """If v in space, return combo mask of original rows; else None."""
        v2, c2 = self._reduce(v)
        return c2 if v2 == 0 else None

    @property
    def dim(self):
        return len(self.pivots)


def null_space(rows, ncols):
    work = list(rows)
    pivot_cols = []
    rank = 0
    for col in range(ncols):
        pr = next(
            (i for i in range(rank, len(work)) if (work[i] >> col) & 1), None
        )
        if pr is None:
            continue
        work[rank], work[pr] = work[pr], work[rank]
        for i in range(len(work)):
            if i != rank and ((work[i] >> col) & 1):
                work[i] ^= work[rank]
        pivot_cols.append(col)
        rank += 1
    pivot_set = set(pivot_cols)
    basis = []
    for f in range(ncols):
        if f in pivot_set:
            continue
        word = 1 << f
        for i, p in enumerate(pivot_cols):
            if (work[i] >> f) & 1:
                word |= 1 << p
        basis.append(word)
    return basis


# ---------- Algorithm X (exhaustive exact cover) ----------

def exact_cover(cols, rows, cap=None):
    solutions = []
    partial = []

    def select(r):
        removed = []
        for j in rows[r]:
            for i in cols[j]:
                for k in rows[i]:
                    if k != j:
                        cols[k].remove(i)
            removed.append(cols.pop(j))
        return removed

    def deselect(r, removed):
        for j in reversed(rows[r]):
            cols[j] = removed.pop()
            for i in cols[j]:
                for k in rows[i]:
                    if k != j:
                        cols[k].add(i)

    def solve():
        if cap is not None and len(solutions) >= cap:
            return
        if not cols:
            solutions.append(list(partial))
            return
        c = min(cols, key=lambda k: len(cols[k]))
        for r in sorted(cols[c]):
            partial.append(r)
            removed = select(r)
            solve()
            deselect(r, removed)
            partial.pop()
            if cap is not None and len(solutions) >= cap:
                return

    solve()
    return solutions


# ---------- Steiner utilities ----------

def is_steiner(blocks, n, r):
    cnt = Counter()
    for K in blocks:
        for x in K:
            cnt[K - {x}] += 1
    return len(cnt) == comb(n, r - 1) and all(v == 1 for v in cnt.values())


def check_encoding(A_list, n, r):
    """Every non-A r-set is uniquely X \\ (P u {p}), P in A, p outside P."""
    X = frozenset(range(n))
    Aset = set(A_list)
    seen = {}
    for P in A_list:
        for p in X - P:
            K = X - P - {p}
            assert K not in Aset, "complement of A-block contains an A-block"
            assert K not in seen, "encoding not unique"
            seen[K] = (P, p)
    all_blocks = {frozenset(c) for c in combinations(range(n), r)}
    assert set(seen) == all_blocks - Aset, "encoding not surjective"


def check_r2_sets(A_list, n, r, sample_cap=200):
    """Every (r+2)-set contains exactly (r+1)/2 blocks of A."""
    target = (r + 1) // 2
    rng = random.Random(1)
    all_y = combinations(range(n), r + 2)
    count = 0
    for Y in all_y:
        Ys = frozenset(Y)
        m = sum(1 for P in A_list if P <= Ys)
        assert m == target, (Y, m, target)
        count += 1
        if count >= sample_cap and n > 8:
            break
    return count


def system_perms(A_list, B_set, n):
    """Local bijections pi_P^B for P in A; returns (perms dict, E sign)."""
    X = frozenset(range(n))
    facet_to_block = {}
    for K in B_set:
        for x in K:
            facet_to_block[K - {x}] = K
    perms = {}
    E = 1
    for P in A_list:
        cod = sorted(X - P)
        pos = {y: i for i, y in enumerate(cod)}
        images = []
        for x in sorted(P):
            S = P - {x}
            K = facet_to_block[S]
            diff = K - S
            assert len(diff) == 1
            y = next(iter(diff))
            images.append(pos[y])
        K0 = next(K for K in B_set if not (K & P))
        rest = X - P - K0
        assert len(rest) == 1
        images.append(pos[next(iter(rest))])
        assert sorted(images) == list(range(len(cod)))
        perms[P] = images
        E *= perm_sign(images)
    return perms, E


def pair_stats(A_list, permsB, EB, permsC, EC, inter, b, r):
    sign_tau = EB * EC
    gamma = 0
    fixed_total = 0
    check_sign = 1
    for P in A_list:
        pb = permsB[P]
        pc = permsC[P]
        inv_c = [0] * len(pc)
        for i, v in enumerate(pc):
            inv_c[v] = i
        rho = [inv_c[v] for v in pb]
        check_sign *= perm_sign(rho)
        nt, fx = perm_cycles(rho)
        gamma += nt
        fixed_total += fx
    assert check_sign == sign_tau, "sign(tau) != E(B)E(C)"
    assert fixed_total == (r + 1) * inter, (
        "fixed slots != (r+1)|B cap C|", fixed_total, (r + 1) * inter
    )
    assert sign_tau == (-1) ** gamma, "sign(tau) != (-1)^Gamma'"
    q1_holds = sign_tau == (-1) ** ((b - inter) % 2)
    return sign_tau, gamma, q1_holds


def build_W_rows(n, r, blocks_list):
    rows = []
    facets = list(combinations(range(n), r - 1))
    for f in facets:
        fs = frozenset(f)
        m = 0
        for i, K in enumerate(blocks_list):
            if fs <= K:
                m |= 1 << i
        rows.append(m)
    return rows, facets


def block_vector(blocks, index):
    m = 0
    for K in blocks:
        m |= 1 << index[K]
    return m


# ---------- r=3 relaxed kernel search ----------

def relaxed_search_r3(A_list, n=7):
    X = frozenset(range(n))
    spheres = [sorted(X - P) for P in A_list]
    opts = [None] + [(i, j) for i in range(4) for j in range(4) if i != j]

    pair_pos = {}
    for a in range(7):
        for b_ in range(a + 1, 7):
            Pa, Pb = A_list[a], A_list[b_]
            qa = [spheres[a].index(q) for q in sorted(Pb - Pa)]
            qb = [spheres[b_].index(q) for q in sorted(Pa - Pb)]
            pair_pos[(a, b_)] = (qa, qb)

    def zsum(o, positions):
        if o is None:
            return 0
        t = 0
        for i in positions:
            if o[0] == i:
                t += 1
            if o[1] == i:
                t -= 1
        return t

    # precompute contributions: contrib[(a,b)][opt_index] for both sides
    opt_index = {o: k for k, o in enumerate(opts)}
    ca = {}
    cb = {}
    for key, (qa, qb) in pair_pos.items():
        ca[key] = [zsum(o, qa) for o in opts]
        cb[key] = [zsum(o, qb) for o in opts]

    counts = Counter()
    assignment = [0] * 7  # option indices
    nodes = [0]

    def dfs(s):
        if s == 7:
            act = sum(1 for k in assignment if opts[k] is not None)
            counts[act] += 1
            return
        for k in range(len(opts)):
            nodes[0] += 1
            ok = True
            for t in range(s):
                key = (t, s)
                if ca[key][assignment[t]] + cb[key][k] != 0:
                    ok = False
                    break
            if ok:
                assignment[s] = k
                dfs(s + 1)
        assignment[s] = 0

    dfs(0)
    return counts, nodes[0]


# ---------- r=3 section ----------

def run_r3():
    print("=" * 72)
    print("r=3 (Fano), complete verification")
    n, r = 7, 3
    b = comb(2 * r + 1, r) // (r + 2)
    blocks_list = [frozenset(c) for c in combinations(range(n), r)]
    index = {K: i for i, K in enumerate(blocks_list)}

    facets = list(combinations(range(n), r - 1))
    cols = {f: set() for f in facets}
    rowdefs = {}
    for i, K in enumerate(blocks_list):
        rowdefs[i] = [f for f in facets if frozenset(f) <= K]
        for f in rowdefs[i]:
            cols[f].add(i)
    systems = exact_cover({f: set(s) for f, s in cols.items()}, rowdefs)
    systems = [frozenset(blocks_list[i] for i in sol) for sol in systems]
    assert len(systems) == 30
    print("all 30 Fano planes generated")

    A = sorted(systems[0], key=sorted)
    A_list = list(A)
    Aset = frozenset(A_list)
    assert is_steiner(A_list, n, r)
    check_encoding(A_list, n, r)
    print("(P,p) encoding verified; every 5-set contains exactly",
          check_r2_sets(A_list, n, r) and 2, "A-blocks")

    mates = [S for S in systems if not (S & Aset)]
    assert len(mates) == 8
    inter_counter = Counter(
        len(Bm & Cm) for Bm, Cm in combinations(mates, 2)
    )
    print("mates of A: 8;  pairwise |B cap C| distribution:",
          dict(inter_counter))
    assert inter_counter == Counter({1: 28})

    # sphere transversality
    for Bm in mates:
        for P in A_list:
            assert sum(1 for K in Bm if not (K & P)) == 1
    print("sphere transversality verified for all 8 mates")

    # signs
    data = {}
    for Bm in mates:
        data[Bm] = system_perms(A_list, Bm, n)
    evals = [E for (_, E) in data.values()]
    print("E values over the 8 mates:", Counter(evals))
    q1_all = True
    econst_all = True
    gamma_parities = Counter()
    for Bm, Cm in combinations(mates, 2):
        inter = len(Bm & Cm)
        pB, EB = data[Bm]
        pC, EC = data[Cm]
        st, gamma, q1 = pair_stats(A_list, pB, EB, pC, EC, inter, b, r)
        gamma_parities[(gamma % 2, (b - inter) % 2)] += 1
        if not q1:
            q1_all = False
        if st != 1:
            econst_all = False
    print("all 28 pairs: sign(tau)=+1:", econst_all,
          "; sign(tau)==(-1)^(b-|BnC|):", q1_all,
          "; (Gamma' mod 2, delta mod 2) counts:", dict(gamma_parities))

    # Claim S
    W_rows, _ = build_W_rows(n, r, blocks_list)
    space = GF2Space()
    for i, row in enumerate(W_rows):
        space.add(row, 1 << i)
    print("rank_2 W_{2,3}(7) =", space.dim, "(Wilson: 15)")
    assert space.dim == 15
    ker = null_space(W_rows, len(blocks_list))
    print("dim ker_2 =", len(ker))
    ones = (1 << len(blocks_list)) - 1
    print("all-ones in rowspace:", space.contains(ones))

    kspace = GF2Space()
    for v in ker:
        kspace.add(v, 0)
    stacked = GF2Space()
    for _, (v, _c) in space.pivots.items():
        stacked.add(v, 0)
    for v in ker:
        stacked.add(v, 0)
    hull_dim = space.dim + kspace.dim - stacked.dim
    print("dim (rowspace cap kernel) =", hull_dim)

    xA = block_vector(A_list, index)
    memberships = Counter()
    cert_sizes = []
    for S in systems:
        if S == Aset:
            continue
        u = xA ^ block_vector(S, index)
        m = space.contains(u)
        memberships[(len(S & Aset), m)] += 1
        if m and not (S & Aset):
            cert = space.certificate(u)
            cert_sizes.append(popcount(cert))
    print("Claim S memberships by |A cap B'| over other 29 Fanos:",
          dict(sorted(memberships.items())))
    if cert_sizes:
        print("certificate (facet-subset) sizes for the disjoint pairs:",
              sorted(set(cert_sizes)))

    counts, nodes = relaxed_search_r3(A_list, n)
    print("relaxed kernel search: solutions by #active spheres:",
          dict(sorted(counts.items())), "; DFS nodes:", nodes)
    odd_active = {k: v for k, v in counts.items() if k % 2 == 1 and k > 0}
    print("odd-active relaxed solutions:", odd_active if odd_active else "NONE")
    return odd_active


# ---------- r=5 section ----------

def analyze_family(base_list, base_set, mates, n, r, b, label,
                   blocks_list, index, space):
    print("-" * 72)
    print(label)
    inter_counter = Counter(
        len(Bm & Cm) for Bm, Cm in combinations(mates, 2)
    )
    print("pairwise |B cap C| distribution over C({},2)={} pairs:".format(
        len(mates), comb(len(mates), 2)), dict(sorted(inter_counter.items())))
    odd_inters = {k: v for k, v in inter_counter.items() if (k - b) % 2 == 1}
    print("pairs violating |B cap C| == b (mod 2):",
          odd_inters if odd_inters else "NONE")

    for Bm in mates[:5]:
        for P in base_list:
            assert sum(1 for K in Bm if not (K & P)) == 1

    data = {}
    for Bm in mates:
        data[Bm] = system_perms(base_list, Bm, n)
    evals = [E for (_, E) in data.values()]
    print("E values over the {} mates:".format(len(mates)), Counter(evals))

    q1_viol = 0
    econst_viol = 0
    gamma_check = 0
    pairs = list(combinations(mates, 2))
    for k, (Bm, Cm) in enumerate(pairs):
        inter = len(Bm & Cm)
        pB, EB = data[Bm]
        pC, EC = data[Cm]
        if k < 400:
            st, gamma, q1 = pair_stats(
                base_list, pB, EB, pC, EC, inter, b, r)
            gamma_check += 1
        else:
            st = EB * EC
            q1 = st == (-1) ** ((b - inter) % 2)
        if not q1:
            q1_viol += 1
        if st != 1:
            econst_viol += 1
    print("pairs with sign(tau) != +1:", econst_viol,
          "; pairs violating sign(tau)==(-1)^(b-|BnC|):", q1_viol,
          "; full cycle/fixed-slot identities checked on", gamma_check,
          "pairs")

    xbase = block_vector(base_list, index)
    fail = 0
    for Bm in mates:
        u = xbase ^ block_vector(Bm, index)
        if not space.contains(u):
            fail += 1
    print("Claim S (x_base + x_mate in rowspace_2 W): failures:",
          fail, "of", len(mates))
    return inter_counter


def run_r5():
    print("=" * 72)
    print("r=5 (S(4,5,11)), complete over fixed bases")
    n, r = 11, 5
    b = comb(2 * r + 1, r) // (r + 2)
    blocks_list = [frozenset(c) for c in combinations(range(n), r)]
    index = {K: i for i, K in enumerate(blocks_list)}
    facets = list(combinations(range(n), r - 1))

    fac_of = {}
    for i, K in enumerate(blocks_list):
        fac_of[i] = [f for f in facets if frozenset(f) <= K]

    def cols_for(allowed):
        cols = {f: set() for f in facets}
        for i in allowed:
            for f in fac_of[i]:
                cols[f].add(i)
        return cols

    sol = exact_cover(cols_for(range(len(blocks_list))), fac_of, cap=1)
    A_list = sorted((blocks_list[i] for i in sol[0]), key=sorted)
    Aset = frozenset(A_list)
    assert is_steiner(A_list, n, r)
    check_encoding(A_list, n, r)
    ycount = check_r2_sets(A_list, n, r)
    print("base A built; (P,p) encoding verified;",
          "first {} 7-sets contain exactly 3 A-blocks".format(ycount))

    allowed = [i for i in range(len(blocks_list))
               if blocks_list[i] not in Aset]
    mate_sols = exact_cover(cols_for(allowed), fac_of)
    mates = [frozenset(blocks_list[i] for i in s) for s in mate_sols]
    print("number of systems disjoint from A:", len(mates))
    for Bm in mates[:3]:
        assert is_steiner(Bm, n, r)

    W_rows, _ = build_W_rows(n, r, blocks_list)
    space = GF2Space()
    for i, row in enumerate(W_rows):
        space.add(row, 1 << i)
    print("rank_2 W_{4,5}(11) =", space.dim, "(Wilson: 210)")
    assert space.dim == 210
    ones = (1 << len(blocks_list)) - 1
    print("all-ones in rowspace:", space.contains(ones))

    analyze_family(A_list, Aset, mates, n, r, b,
                   "family 1: base A and its mates",
                   blocks_list, index, space)

    B0 = mates[0]
    B0_list = sorted(B0, key=sorted)
    allowed2 = [i for i in range(len(blocks_list))
                if blocks_list[i] not in B0]
    mate2_sols = exact_cover(cols_for(allowed2), fac_of)
    mates2 = [frozenset(blocks_list[i] for i in s) for s in mate2_sols]
    print("number of systems disjoint from B0 (a mate of A):", len(mates2))
    assert Aset in mates2
    analyze_family(B0_list, B0, mates2, n, r, b,
                   "family 2: base B0 and its mates",
                   blocks_list, index, space)

    # non-disjoint controls
    rng = random.Random(20260724)
    control = Counter()
    for _ in range(300):
        perm = list(range(n))
        rng.shuffle(perm)
        D = frozenset(frozenset(perm[x] for x in K) for K in Aset)
        m = len(D & Aset)
        u = block_vector(Aset, index) ^ block_vector(D, index)
        control[(m, space.contains(u))] += 1
    print("controls: (|A cap pi(A)|, x_A + x_piA in rowspace) counts:",
          dict(sorted(control.items())))


def main():
    for r in (3, 5, 15):
        bb = comb(2 * r + 1, r) // (r + 2)
        print("r={}: b={} (parity {})".format(r, bb, bb % 2))
    odd_active = run_r3()
    run_r5()
    print("=" * 72)
    print("DONE")


if __name__ == "__main__":
    main()

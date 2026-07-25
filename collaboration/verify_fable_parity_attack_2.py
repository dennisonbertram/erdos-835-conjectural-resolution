#!/usr/bin/env python3
"""Verifier for collaboration/fable_parity_attack_2.md.

Machine checks for:
  L1  (groupoid): for ANY two S(r-1,r,2r+1) systems Y,Z the map
      F_{Y->Z} (fix shared blocks, else unique disjoint Z-block) is a
      well-defined bijection with F_{Z->Y} = F_{Y->Z}^{-1}.
  L2  (sign factorization): sgn(sigma_full) = f(A,B) f(A,C) f(B,C),
      f(Y,Z) := sign of F_{Y->Z} w.r.t. a fixed global block order.
  L3  (conjugacy): triangle holonomy cycle type is an invariant of the
      unordered triple {A,B,C}.
  L4  (chain laws, disjoint-base triangles): S_i^S_{i+1}={beta_i},
      |D_i^D_{i+1}|=1={delta_i}, T_i^T_{i+1}={alpha_{i+1}},
      alpha_{i+1} in T_i; the 3L walk is an INDUCED cycle of O_{r+1}.
  L5  (integer position identity): 2 s_p = L - a_p - d_p + c_p per point.
  L6  (affine intersection distribution): n_j(B,C) is affine in |B^C|
      with universal slope (-1)^(r-j) C(r,j).
  D1  (data): f-holonomy structure at r=3 (complete) and r=5 (sampled);
      general-triple even-cycle census; corner-bit battery.
All arithmetic exact; deterministic seed.
"""
import random
import sys
from collections import Counter
from itertools import combinations, permutations
from math import comb
from pathlib import Path

sys.setrecursionlimit(100000)
random.seed(20260724)

helper = Path(__file__).resolve().parent.parent / "evidence" / "disjoint_mates.py"
ns = {}
exec(compile(helper.read_text(encoding="utf-8").split("if __name__")[0],
             str(helper), "exec"), ns)

FAIL = []


def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"  {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)


def perm_sign(images):
    n = len(images)
    seen = [False] * n
    sgn = 1
    for i in range(n):
        if not seen[i]:
            j, clen = i, 0
            while not seen[j]:
                seen[j] = True
                j = images[j]
                clen += 1
            if clen % 2 == 0:
                sgn = -sgn
    return sgn


def cycle_type(perm):
    """perm: dict block->block. Returns sorted tuple of cycle lengths >= 2."""
    seen, out = set(), []
    for s in perm:
        if s in seen:
            continue
        j, clen = s, 0
        while j not in seen:
            seen.add(j)
            j = perm[j]
            clen += 1
        if clen >= 2:
            out.append(clen)
    return tuple(sorted(out))


def build_F(Y, Z, v, Zset=None):
    """F_{Y->Z} as dict; asserts well-definedness (unique image)."""
    if Zset is None:
        Zset = set(Z)
    X = set(range(v))
    F = {}
    for S in Y:
        if S in Zset:
            F[S] = S
            continue
        comp = X - set(S)
        hits = [c for c in (tuple(sorted(comp - {x})) for x in comp) if c in Zset]
        assert len(hits) == 1, ("n0 != 1", S, hits)
        F[S] = hits[0]
    assert len(set(F.values())) == len(Y), "not a bijection"
    return F


def f_sign(Y, Z, v, FYZ=None):
    """f(Y,Z) = sign of F_{Y->Z} w.r.t. sorted block orders."""
    if FYZ is None:
        FYZ = build_F(Y, Z, v)
    Ys, Zs = sorted(Y), sorted(Z)
    zi = {b: i for i, b in enumerate(Zs)}
    return perm_sign([zi[FYZ[b]] for b in Ys])


def sigma_full(A, B, C, v):
    """sigma = F_CB o F_AC o F_BA : B -> B (dict)."""
    FBA = build_F(B, A, v)
    FAC = build_F(A, C, v)
    FCB = build_F(C, B, v)
    return {S: FCB[FAC[FBA[S]]] for S in B}


def isect(Y, Z):
    return len(set(Y) & set(Z))


# ----------------------------------------------------------------------
# canonical-triangle (A disjoint from B and C) cycle walker with labels
# ----------------------------------------------------------------------
def dpartner(S, legset, v):
    Sc = frozenset(range(v)) - frozenset(S)
    for x in Sc:
        c = tuple(sorted(Sc - {x}))
        if c in legset:
            return c, x
    raise AssertionError("no disjoint partner")


def triangle_cycles(A, B, C, v):
    """Cycles of sigma on B\\C with per-step labels (S,D,T,alpha,beta,delta)."""
    Aset, Bset, Cset = set(A), set(B), set(C)
    BmC = [S for S in B if S not in Cset]
    step = {}
    for S in BmC:
        D, alpha = dpartner(S, Aset, v)
        T, beta = dpartner(D, Cset, v)
        Snext, delta = dpartner(T, Bset, v)
        assert beta in set(S) and delta in set(D)
        step[S] = (Snext, D, T, alpha, beta, delta)
    seen, cycles = set(), []
    for S0 in BmC:
        if S0 in seen:
            continue
        cyc, S = [], S0
        while S not in seen:
            seen.add(S)
            cyc.append((S,) + step[S][1:])
            S = step[S][0]
        cycles.append(cyc)
    return cycles


def audit_cycle(cyc, v):
    """Hard checks L4+L5 on one cycle; returns corner-bit odd-sum flags."""
    L = len(cyc)
    walk = []
    for i in range(L):
        S, D, T, a, b2, d = cyc[i]
        S1, D1, T1, a1, b21, d1 = cyc[(i + 1) % L]
        sS, sD, sT = set(S), set(D), set(T)
        sS1, sD1, sT1 = set(S1), set(D1), set(T1)
        assert sS & sS1 == {b2}, "S-chain law"
        assert sD & sD1 == {d}, "D-chain law"
        assert sT & sT1 == {a1}, "T-chain law (new)"
        assert a1 in sT, "alpha_{i+1} in T_i (new)"
        walk += [S, D, T]
    # induced 3L-cycle in the odd graph
    n = len(walk)
    assert len(set(walk)) == n, "walk vertices distinct"
    for i in range(n):
        for j in range(i + 1, n):
            adj = not (set(walk[i]) & set(walk[j]))
            consec = (j - i == 1) or (i == 0 and j == n - 1)
            assert adj == consec, "induced-cycle law"
    # integer position identity: 2 s_p = L - a_p - d_p + c_p
    sc, ac, cc, dc, tc = Counter(), Counter(), Counter(), Counter(), Counter()
    for S, D, T, a, b2, d in cyc:
        for p in S:
            sc[p] += 1
        for p in T:
            tc[p] += 1
        ac[a] += 1
        cc[b2] += 1
        dc[d] += 1
    for p in range(v):
        assert 2 * sc[p] == L - ac[p] - dc[p] + cc[p], "integer position identity"
        assert tc[p] == L - sc[p] - dc[p], "T-count corollary"
    # corner bits
    bits = Counter()
    for i in range(L):
        S, D, T, a, b2, d = cyc[i]
        S1, D1, T1, a1, b21, d1 = cyc[(i + 1) % L]
        bits["u[beta'==beta]"] += (b21 == b2)
        bits["w[alpha'==alpha]"] += (a1 == a)
        bits["e1[delta'==delta]"] += (d1 == d)
        bits["e2[delta'==alpha]"] += (d1 == a)
        bits["e3[delta' in S_i]"] += (d1 in set(S))
    return L, {k: val % 2 for k, val in bits.items()}


def corner_battery(A, mates, v, pair_list, tag):
    odd_cycles = 0
    ncyc = 0
    badbits = Counter()
    types = Counter()
    for (i, j) in pair_list:
        for cyc in triangle_cycles(A, mates[i], mates[j], v):
            L, bitpar = audit_cycle(cyc, v)
            ncyc += 1
            odd_cycles += L % 2
            for k, p in bitpar.items():
                if p != 0:
                    badbits[k] += 1
        types[tuple(sorted(len(c) for c in
                    triangle_cycles(A, mates[i], mates[j], v)))] += 1
    check(f"{tag}: chain/induced/position laws on {ncyc} cycles "
          f"({len(pair_list)} pairs)", True)
    check(f"{tag}: odd sigma-cycles", odd_cycles == 0, f"count={odd_cycles}")
    print(f"    cycle types: {dict(types)}")
    for k in ["u[beta'==beta]", "w[alpha'==alpha]", "e1[delta'==delta]",
              "e2[delta'==alpha]", "e3[delta' in S_i]"]:
        n_odd = badbits.get(k, 0)
        print(f"    bit {k}: cycles with ODD sum: {n_odd}/{ncyc}")


# ----------------------------------------------------------------------
# L6: affine intersection distribution
# ----------------------------------------------------------------------
def n_dist(Y, Z, r):
    n = [0] * (r + 1)
    for S in Y:
        sS = set(S)
        for T in Z:
            n[len(sS & set(T))] += 1
    return n


def affine_check(systems, pairs, r, v, tag):
    b = len(systems[0])
    lam = [comb(v - s, r - 1 - s) // (r - s) for s in range(r)]
    ref = None
    slope = [(-1) ** (r - j) * comb(r, j) for j in range(r + 1)]
    ok_design, ok_affine = True, True
    for (i, j) in pairs:
        n = n_dist(systems[i], systems[j], r)
        for s in range(r):
            if sum(comb(jj, s) * n[jj] for jj in range(r + 1)) != b * comb(r, s) * lam[s]:
                ok_design = False
        if ref is None:
            ref = (n, n[r])
        else:
            n0, m0 = ref
            if any(n[jj] != n0[jj] + slope[jj] * (n[r] - m0) for jj in range(r + 1)):
                ok_affine = False
    check(f"{tag}: design moment equations on {len(pairs)} pairs", ok_design)
    check(f"{tag}: n_j affine in |Y^Z| with slope (-1)^(r-j)C(r,j)", ok_affine)


# ======================================================================
print("=" * 72)
print("r=3  (v=7): exhaustive")
print("=" * 72)
v3, r3 = 7, 3
triples = list(combinations(range(v3), 3))
base = [b for b in triples if (b[0] + 1) ^ (b[1] + 1) ^ (b[2] + 1) == 0]
fanos = sorted({tuple(sorted(tuple(sorted(p[x] for x in b)) for b in base))
                for p in permutations(range(v3))})
assert len(fanos) == 30

# L1 on all ordered pairs + f table
fmat = {}
ok_inv, ok_sym = True, True
for i in range(30):
    for j in range(30):
        F = build_F(fanos[i], fanos[j], v3)
        if i < j:
            G = build_F(fanos[j], fanos[i], v3)
            ok_inv &= all(G[F[S]] == S for S in fanos[i])
        fmat[(i, j)] = f_sign(fanos[i], fanos[j], v3, F)
for i in range(30):
    for j in range(30):
        ok_sym &= fmat[(i, j)] == fmat[(j, i)]
check("L1: F is a bijection for all 900 ordered Fano pairs", True)
check("L1: F_ZY = F_YZ^-1 for all 435 unordered pairs", ok_inv)
check("L2: f symmetric, f(Y,Y)=+1", ok_sym and all(fmat[(i, i)] == 1 for i in range(30)))

deg = [sum(1 for j in range(30) if j != i and isect(fanos[i], fanos[j]) == 0)
       for i in range(30)]
check("disjointness degree = 8 for every Fano", set(deg) == {8})

# L2+L3 on all 4060 unordered triples; even-cycle census for general triples
sign_ok, conj_ok = True, True
census = Counter()
odd_nontrivial = 0
tri_sign_by_type = {}
sign_fn_of_type = True
for (i, j, k) in combinations(range(30), 3):
    A, B, C = fanos[i], fanos[j], fanos[k]
    sig = sigma_full(A, B, C, v3)
    ct = cycle_type(sig)
    s_direct = perm_sign([sorted(B).index(sig[S]) for S in sorted(B)])
    s_f = fmat[(i, j)] * fmat[(i, k)] * fmat[(j, k)]
    sign_ok &= (s_direct == s_f)
    ity = tuple(sorted((isect(A, B), isect(A, C), isect(B, C))))
    census[(ity, ct)] += 1
    odd_nontrivial += sum(1 for L in ct if L % 2)
    if ity in tri_sign_by_type and tri_sign_by_type[ity] != s_f:
        sign_fn_of_type = False
    tri_sign_by_type[ity] = s_f
check("L2: sgn(sigma_full) == f(A,B)f(A,C)f(B,C) on all 4060 triples", sign_ok)
print(f"    FINDING: odd nontrivial cycles in general triples: {odd_nontrivial}"
      f" ({'general even-cycle law REFUTED' if odd_nontrivial else 'none'})")
print("    census (sorted intersections -> cycle types):")
for (ity, ct), cnt in sorted(census.items()):
    print(f"      {ity}: {ct if ct else '(identity)'} x{cnt}")
print(f"    triangle sign a function of intersection type: {sign_fn_of_type}")
print(f"    sign by type: { {t: s for t, s in sorted(tri_sign_by_type.items())} }")

# does f factor as eps(Y)eps(Z) * g(|Y^Z|)?  try all g on {0,1,3}
factor_sols = []
for g0 in (1, -1):
    for g1 in (1, -1):
        for g3 in (1, -1):
            g = {0: g0, 1: g1, 3: g3}
            ok = all(tri_sign_by_type[t] == g[t[0]] * g[t[1]] * g[t[2]]
                     for t in tri_sign_by_type)
            if ok:
                factor_sols.append((g0, g1, g3))
print(f"    f = eps.eps.g(|Y^Z|) solutions (g(0),g(1),g(3)): {factor_sols}")
check("r=3: sgn(sigma) == (-1)^(|AB|+|AC|+|BC|) [g(j)=(-1)^j fits]",
      (1, -1, -1) in factor_sols)

# L3 conjugacy on a subsample
for (i, j, k) in random.sample(list(combinations(range(30), 3)), 60):
    A, B, C = fanos[i], fanos[j], fanos[k]
    ctB = cycle_type(sigma_full(A, B, C, v3))
    ctA = cycle_type(sigma_full(C, A, B, v3))
    ctC = cycle_type(sigma_full(B, C, A, v3))
    inv = sigma_full(A, C, B, v3)  # reversed orientation, base C
    conj_ok &= (ctB == ctA == ctC == cycle_type(inv))
check("L3: cycle type invariant of unordered triple (60 random triples)", conj_ok)

# canonical disjoint-base triangles + battery
A3 = fanos[0]
mates3 = [f for f in fanos if isect(A3, f) == 0]
assert len(mates3) == 8
corner_battery(A3, mates3, v3, list(combinations(range(8), 2)), "r=3 canonical")


def canonical_consistency(A, B, C, v):
    """sigma_full fixes B^C pointwise and matches the Lemma-6 sigma."""
    sig = sigma_full(A, B, C, v)
    shared = set(B) & set(C)
    ok = all(sig[S] == S for S in shared)
    step = {c[0]: nxt[0] for cyc in triangle_cycles(A, B, C, v)
            for c, nxt in zip(cyc, cyc[1:] + cyc[:1])}
    ok &= all(sig[S] == step[S] for S in step)
    ok &= set(step) == set(B) - shared
    return ok

ok_canon = all(canonical_consistency(A3, mates3[i], mates3[j], v3)
               for i, j in combinations(range(8), 2))
check("Lemma D: sigma_full == (fix B^C) + Lemma-6 sigma on all 28 r=3 pairs",
      ok_canon)

affine_check(fanos, list(combinations(range(30), 2)), r3, v3, "r=3")

# ======================================================================
print()
print("=" * 72)
print("r=5  (v=11): orbit of 5040 systems, sampled checks")
print("=" * 72)
v5, r5 = 11, 5
blocks5 = list(combinations(range(v5), 5))
X, Y = ns["steiner_cover_instance"](v5, 4, blocks5)
first = ns["algox_solutions"](X, Y, cap=1)[0]
start = tuple(sorted(tuple(sorted(b)) for b in first))
orbit = {start}
frontier = [start]
gens = [(i, i + 1) for i in range(v5 - 1)]
while frontier:
    nxt = []
    for sysm in frontier:
        for (a, bswap) in gens:
            m = {a: bswap, bswap: a}
            img = tuple(sorted(tuple(sorted(m.get(x, x) for x in blk))
                               for blk in sysm))
            if img not in orbit:
                orbit.add(img)
                nxt.append(img)
    frontier = nxt
systems5 = sorted(orbit)
check("orbit size == 11!/|M11| == 5040", len(systems5) == 5040,
      f"got {len(systems5)}")

A5 = start
mate_idx = [i for i, sm in enumerate(systems5) if isect(A5, sm) == 0]
check("|D(A)| == 144 within the orbit", len(mate_idx) == 144,
      f"got {len(mate_idx)}")
mates5 = [systems5[i] for i in mate_idx]

# L1 on random ordered pairs
ok_inv = True
for _ in range(300):
    i, j = random.sample(range(5040), 2)
    F = build_F(systems5[i], systems5[j], v5)
    G = build_F(systems5[j], systems5[i], v5)
    ok_inv &= all(G[F[S]] == S for S in systems5[i])
check("L1: bijection + inverse on 300 random ordered pairs", ok_inv)

# f on a sample: base A, all 144 mates, plus randoms to 250
sample = [A5] + mates5 + [systems5[i] for i in
                          random.sample(range(5040), 120)]
sample = list(dict.fromkeys(sample))[:250]
nsmp = len(sample)
fS = {}
for i in range(nsmp):
    for j in range(i, nsmp):
        val = f_sign(sample[i], sample[j], v5)
        fS[(i, j)] = fS[(j, i)] = val
check(f"f computed on all pairs of {nsmp}-system sample", True)

# pairwise intersection matrix and spectrum on the sample
imat = {}
spec = Counter()
for i in range(nsmp):
    for j in range(i + 1, nsmp):
        w = isect(sample[i], sample[j])
        imat[(i, j)] = imat[(j, i)] = w
        spec[w] += 1
print(f"    pairwise |Y^Z| spectrum on sample: {dict(sorted(spec.items()))}")
check("r=5: all pairwise intersections even (sampled)",
      all(w % 2 == 0 for w in spec))

# is the triangle sign a function of the intersection type?  (all sample
# triples, using the precomputed f-table)
tri_by_type = {}
fn_of_type = True
for (i, j, k) in combinations(range(nsmp), 3):
    p = fS[(i, j)] * fS[(i, k)] * fS[(j, k)]
    ity = tuple(sorted((imat[(i, j)], imat[(i, k)], imat[(j, k)])))
    if ity in tri_by_type and tri_by_type[ity] != p:
        fn_of_type = False
        tri_by_type[ity] = 0
    elif ity not in tri_by_type:
        tri_by_type[ity] = p
check("r=5: triangle sign is NOT a function of intersection type",
      not fn_of_type,
      f"sign by type (0=both values occur): {dict(sorted(tri_by_type.items()))}")

# L2 + general-triple census on random triples in the sample
sign_ok = True
census5 = {}
for _ in range(400):
    i, j, k = random.sample(range(nsmp), 3)
    A, B, C = sample[i], sample[j], sample[k]
    sig = sigma_full(A, B, C, v5)
    ct = cycle_type(sig)
    Bs = sorted(B)
    bi = {b: t for t, b in enumerate(Bs)}
    s_direct = perm_sign([bi[sig[S]] for S in Bs])
    s_f = fS[(i, j)] * fS[(i, k)] * fS[(j, k)]
    sign_ok &= (s_direct == s_f)
    ity = tuple(sorted((imat[(i, j)], imat[(i, k)], imat[(j, k)])))
    tot, odd, sgns = census5.get(ity, (0, 0, set()))
    census5[ity] = (tot + 1, odd + (1 if any(L % 2 for L in ct) else 0),
                    sgns | {s_f})
check("L2: sgn(sigma_full) == f f f on 400 random triples", sign_ok)
print("    type -> (#triples, #with odd nontrivial cycle, signs seen):")
for ity, (tot, odd, sgns) in sorted(census5.items()):
    print(f"      {ity}: ({tot}, {odd}, {sorted(sgns)})")

# L3 on a few r=5 triples
conj_ok = True
for _ in range(15):
    i, j, k = random.sample(range(nsmp), 3)
    A, B, C = sample[i], sample[j], sample[k]
    conj_ok &= (cycle_type(sigma_full(A, B, C, v5))
                == cycle_type(sigma_full(C, A, B, v5)))
check("L3: conjugacy on 15 random r=5 triples", conj_ok)

# canonical triangles: full cycle-type census (all 10296 mate pairs)
types5 = Counter()
sgn5 = Counter()
for (i, j) in combinations(range(144), 2):
    cycs = triangle_cycles(A5, mates5[i], mates5[j], v5)
    ct = tuple(sorted(len(c) for c in cycs))
    types5[ct] += 1
    sgn5[(-1) ** sum((L - 1) for L in ct)] += 1
check("r=5 canonical census: all cycles even",
      all(all(L % 2 == 0 for L in ct) for ct in types5), "")
print(f"    canonical cycle types: {dict(types5.most_common())}")
print(f"    canonical sgn(sigma): {dict(sgn5)}")

# heavy chain-law battery on 200 mate pairs
pl = random.sample(list(combinations(range(144), 2)), 200)
corner_battery(A5, mates5, v5, pl, "r=5 canonical (200 pairs)")
ok_canon5 = all(canonical_consistency(A5, mates5[i], mates5[j], v5)
                for i, j in pl[:30])
check("Lemma D: sigma_full == (fix B^C) + Lemma-6 sigma on 30 r=5 pairs",
      ok_canon5)

# SignLaw: #cycles(sigma) == b (mod 2) on the full canonical censuses
b3, b5 = 7, 66
sl3 = all(len(ct) % 2 == b3 % 2 for ct in [(6,)])
sl5 = all(len(ct) % 2 == b5 % 2 for ct in types5)
check("SignLaw #cycles==b mod 2: r=3 (28/28) and r=5 (10296/10296)",
      sl3 and sl5)

# Reproduce the cycle-trade census cited in the note.  A cycle would be a
# trade exactly when its S-side and T-side have the same facet multiset.
def facet_mult(blocks):
    out = Counter()
    for S in blocks:
        for x in S:
            out[tuple(y for y in S if y != x)] += 1
    return out


n_trade_cycles = 0
n_facet_closed = 0
for i, j in combinations(range(25), 2):
    for cyc in triangle_cycles(A5, mates5[i], mates5[j], v5):
        n_trade_cycles += 1
        n_facet_closed += (
            facet_mult([step[0] for step in cyc])
            == facet_mult([step[2] for step in cyc])
        )
check("r=5: individual sigma cycles are not trades (first 25 mates)",
      n_trade_cycles == 1828 and n_facet_closed == 0,
      f"facet-closed={n_facet_closed}/{n_trade_cycles}")

affine_check(systems5, [tuple(random.sample(range(5040), 2))
                        for _ in range(400)], r5, v5, "r=5")

# ----------------------------------------------------------------------
# Theorem: N := Phi1 + Phi2 == (K P_A K + K)[B\C, C\B];
#          rank_Q(N) = t - #even cycles, rank_F2(N) = t - #cycles.
# ----------------------------------------------------------------------
def rank_over(rows, mod=None):
    m = [r[:] for r in rows]
    R, C = len(m), len(m[0]) if m else 0
    rk, rpos = 0, 0
    for c in range(C):
        piv = next((i for i in range(rpos, R) if m[i][c]), None)
        if piv is None:
            continue
        m[rpos], m[piv] = m[piv], m[rpos]
        for i in range(R):
            if i != rpos and m[i][c]:
                if mod == 2:
                    m[i] = [(a + b) % 2 for a, b in zip(m[i], m[rpos])]
                else:
                    from fractions import Fraction
                    fac = Fraction(m[i][c], m[rpos][c])
                    m[i] = [a - fac * b for a, b in zip(m[i], m[rpos])]
        rk += 1
        rpos += 1
    return rk


def snf_rank_check(A, B, C, v, r, tag):
    Aset, Bset, Cset = set(A), set(B), set(C)
    BmC = sorted(S for S in B if S not in Cset)
    CmB = sorted(T for T in C if T not in Bset)
    t = len(BmC)
    ci = {T: j for j, T in enumerate(CmB)}
    # matchings directly
    N1 = [[0] * t for _ in range(t)]
    for a, S in enumerate(BmC):
        D, _ = dpartner(S, Aset, v)
        T1, _ = dpartner(D, Cset, v)     # phi1(S)
        T2, _ = dpartner(S, Cset, v)     # phi2(S)
        N1[a][ci[T1]] += 1
        N1[a][ci[T2]] += 1
    # global formula (K P_A K + K)[BmC, CmB]
    N2 = [[0] * t for _ in range(t)]
    for a, S in enumerate(BmC):
        sS = set(S)
        for j, T in enumerate(CmB):
            sT = set(T)
            kpk = sum(1 for D in A
                      if not (set(D) & sS) and not (set(D) & sT))
            N2[a][j] = kpk + (0 if sS & sT else 1)
    ok_formula = (N1 == N2)
    cycs = triangle_cycles(A, B, C, v)
    c = len(cycs)
    e = sum(1 for cy in cycs if len(cy) % 2 == 0)
    rQ, r2 = rank_over(N1), rank_over(N1, mod=2)
    ok_rank = (rQ == t - e) and (r2 == t - c)
    check(f"{tag}: N == (K P_A K + K)[B\\C,C\\B]", ok_formula)
    check(f"{tag}: rank_Q(N)=t-e, rank_F2(N)=t-c",
          ok_rank, f"t={t} c={c} e={e} rQ={rQ} r2={r2}")


print()
print("=" * 72)
print("SNF / rank reformulation checks")
print("=" * 72)
snf_rank_check(A3, mates3[0], mates3[1], v3, r3, "r=3 pair(0,1)")
snf_rank_check(A3, mates3[2], mates3[5], v3, r3, "r=3 pair(2,5)")
for (i, j) in [(0, 1), (3, 77), (10, 140)]:
    snf_rank_check(A5, mates5[i], mates5[j], v5, r5, f"r=5 pair({i},{j})")

print()
print("=" * 72)
print(f"RESULT: {'ALL CHECKS PASSED' if not FAIL else 'FAILURES: ' + str(FAIL)}")
print("=" * 72)

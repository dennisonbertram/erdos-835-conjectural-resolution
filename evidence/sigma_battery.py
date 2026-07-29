#!/usr/bin/env python3
"""Battery for the even-cycle identity of sigma = phi2^{-1} o phi1.

Per step S -> sigma(S): labels alpha (A-mate gap), beta (swap-out point),
delta (B-return gap), gamma (C-disjoint gap of S).
Tests, per mate pair and per cycle:
  - cycle length parity;
  - sums of candidate bits vs length parity (which bits satisfy
    sum == len mod 2 on EVERY cycle?);
  - |D_i cap D_{i+1}| census along cycles;
  - sgn(sigma).
Families: r=3 and r=5 (all ordered pairs of mates of one fixed base).
"""
import sys
sys.setrecursionlimit(100000)
from pathlib import Path
from itertools import combinations
from collections import Counter

helper = Path(__file__).with_name("disjoint_mates.py")
src = helper.read_text(encoding="utf-8").split('if __name__')[0]
ns = {}
exec(compile(src, str(helper), "exec"), ns)


def build_legs(v, ksz, t, nmates=None):
    blocks = list(combinations(range(v), ksz))
    X, Y = ns["steiner_cover_instance"](v, t, blocks)
    A = ns["algox_solutions"](X, Y, cap=1)[0]
    rest = [b for b in blocks if b not in set(A)]
    X2, Y2 = ns["steiner_cover_instance"](v, t, rest)
    mates = ns["algox_solutions"](X2, Y2, cap=nmates)
    return A, mates


def dpartner(S, legset, v):
    Sc = frozenset(range(v)) - frozenset(S)
    for x in Sc:
        c = tuple(sorted(Sc - {x}))
        if c in legset:
            return c, x
    raise AssertionError


def analyze_pair(A, B, C, v):
    Aset = set(map(tuple, A)); Bset = set(map(tuple, B))
    Cset = set(map(tuple, C))
    BmC = [S for S in Bset if S not in Cset]
    step = {}
    for S in BmC:
        D, alpha = dpartner(S, Aset, v)         # A-mate of S
        T, wc = dpartner(D, Cset, v)            # phi1(S); wc = w_C(D) = beta
        beta = set(S) - set(T)
        assert len(beta) == 1
        beta = beta.pop()
        assert beta == wc
        Snext, delta = dpartner(T, Bset, v)     # sigma(S); delta in D
        _, gamma = dpartner(S, Cset, v)         # phi2(S) = S^c minus gamma
        step[S] = (Snext, alpha, beta, delta, gamma, D)
    # cycles with per-step bits
    seen = set()
    cycles = []
    for S0 in BmC:
        if S0 in seen:
            continue
        cyc = []
        S = S0
        while S not in seen:
            seen.add(S)
            cyc.append(S)
            S = step[S][0]
        cycles.append(cyc)
    out = []
    for cyc in cycles:
        L = len(cyc)
        bits = Counter()
        dd_census = Counter()
        for idx, S in enumerate(cyc):
            Snext, a, b2, d, g, D = step[S]
            Dn = step[Snext][5]
            bits["c1[a==g]"] += (a == g)
            bits["c2[d==g]"] += (d == g)
            bits["c7[beta_next==delta]"] += (step[Snext][2] == d)
            bits["c8[alpha_next==alpha]"] += (step[Snext][1] == a)
            bits["c9[alpha_next==beta]"] += (step[Snext][1] == b2)
            bits["c10[gamma_next==gamma]"] += (step[Snext][4] == g)
            bits["c11[delta_next==delta]"] += (step[Snext][3] == d)
            inter = len(set(D) & set(Dn))
            dd_census[inter] += 1
            bits["c12[|DcapDn|odd]"] += (inter % 2)
        out.append((L, dict(bits), dict(dd_census)))
    return out


def run_family(v, ksz, t, tag, nmates=None, npairs=None):
    A, mates = build_legs(v, ksz, t, nmates)
    n = len(mates)
    # which candidate bits satisfy sum == L (mod 2) on EVERY cycle?
    good = None
    lenpar = Counter()
    dd_all = Counter()
    typec = Counter()
    cnt = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            res = analyze_pair(A, mates[i], mates[j], v)
            types = tuple(sorted(L for L, _, _ in res))
            typec[types] += 1
            for L, bits, dd in res:
                lenpar[L % 2] += 1
                for k2, s in bits.items():
                    okk = (s % 2) == (L % 2)
                    if good is None:
                        good = {}
                    if k2 not in good:
                        good[k2] = True
                    good[k2] = good[k2] and okk
                for a, c in dd.items():
                    dd_all[a] += c
            cnt += 1
            if npairs and cnt >= npairs:
                break
        if npairs and cnt >= npairs:
            break
    print(f"[{tag}] ordered pairs tested={cnt}")
    print(f"  cycle-length parities: {dict(lenpar)} (1 => odd cycle exists)")
    print(f"  |D_i ^ D_(i+1)| census: {dict(sorted(dd_all.items()))}")
    ok = [k2 for k2, g in (good or {}).items() if g]
    print(f"  bits with sum==L mod 2 on EVERY cycle: {ok if ok else 'NONE'}")
    for ty, c in typec.most_common(6):
        print(f"    cycle type {ty} x{c}")


run_family(7, 3, 2, "r=3")
run_family(11, 5, 4, "r=5")

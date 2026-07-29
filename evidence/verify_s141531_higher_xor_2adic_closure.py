#!/usr/bin/env python3
"""Deterministic verifier for s141531_higher_xor_2adic_closure.md.

Modes:
  (default)   Delta-lemma exact checks + r=9 end-to-end tail-reduction
              control (~1-2 min, pure stdlib).
  --window    The full r=15 finite-window computation: all 2-adic
              integrality conditions for 0 <= j <= 570344, all layers,
              external branch, mod 2^47 with exact NTT/CRT convolutions;
              prints SHA-256 certificates.  (numpy required; ~minutes.)

Exact moduli: conditions tested mod 2^31; all window arithmetic mod 2^47
(headroom); NTT primes 998244353, 754974721, 469762049, 167772161
(product ~ 2^115.5 > coefficient bound (mu+1)*2^94 < 2^113.2).
Exact counts: 9 distinct |F| cofactor products, 36 prime-convolutions,
108 transforms, NTT length 2^20 (mu+1 = 570286 <= 2^20).
A FAIL asserts (nonzero exit); the certificate hash covers the full
per-layer violation-count table and all full 64-hex U_F hashes.
"""
import sys
import hashlib
from math import comb

MODE_WINDOW = "--window" in sys.argv


def lam_of(r):
    v, t = 2 * r + 1, r - 1
    lam = []
    for s in range(r):
        num, den = comb(v - s, t - s), r - s
        assert num % den == 0
        lam.append(num // den)
    return lam


def phi_fn(r):
    v = 2 * r + 1
    lam = lam_of(r)

    def phi(w):
        if w <= r - 1:
            return sum((-2) ** s * comb(w, s) * lam[s] for s in range(w + 1))
        if w == r:
            return sum((-2) ** s * comb(r, s) * lam[s] for s in range(r))
        return -phi(v - w)
    return phi, lam[0]


def kraw_seq(F, b, J):
    K = [1, F]
    for j in range(1, J):
        num = F * K[j] - (b - j + 1) * K[j - 1]
        assert num % (j + 1) == 0
        K.append(num // (j + 1))
    return K


def v2(n):
    c = 0
    while n % 2 == 0:
        n //= 2
        c += 1
    return c


def delta_lemma():
    phi, b = phi_fn(15)
    F0, F1 = phi(15), phi(15) - 2 ** 15
    assert (F0, F1) == (1549, -31219)
    J = 1200
    K0, K1 = kraw_seq(F0, b, J), kraw_seq(F1, b, J)
    vals = [v2(K1[j] - K0[j]) for j in range(1, J + 1)]
    assert min(vals) == 15 and vals.count(15) == 64
    assert -(K1[3] - K0[3]) // 2 ** 15 == 145938438
    print("[ok] Delta-lemma: min v2 = 15 (sharp, 64 hits <= 1200); "
          "j=3 split 145938438 reproduced")


def r9_control():
    r = 9
    v, MOD = 2 * r + 1, 1 << (2 * r + 1)
    phi, b = phi_fn(r)
    F0, F1 = phi(r), phi(r) - 2 ** r
    M = max(max(abs(phi(w)) for w in range(1, v)), abs(F0), abs(F1))
    assert M == 454 and (b - M) % 2 == 0
    A = (b - M) // 2
    KW = [[sum((-1) ** h * comb(d, h) * comb(v - d, w - h)
               for h in range(min(d, w) + 1)) for w in range(v + 1)]
          for d in range(v + 1)]
    L = M + 400
    HEAD = 1 << (v + 16)

    def upow(F):
        aa, cc = (M + F) // 2, (M - F) // 2
        Av = [comb(aa, i) for i in range(aa + 1)]
        Bv = [comb(cc, i) * (-1) ** i for i in range(cc + 1)]
        Cv = [0] * (M + 1)
        for i, x in enumerate(Av):
            for jj, y in enumerate(Bv):
                Cv[i + jj] += x * y
        return Cv
    U = {F: upow(F) for F in sorted({phi(w) for w in range(1, v)}
                                    | {F0, F1})}
    S = [0] * (L + 1)
    Ar = [comb(M, i) for i in range(M + 1)] + [0] * (L - M)
    for rho in range(0, v + 15):
        cf = (pow(2, rho + 1, HEAD) * (comb(A, rho) % HEAD)) % HEAD
        for jj in range(rho, L + 1):
            S[jj] = (S[jj] + cf * Ar[jj - rho]) % HEAD
        for jj in range(1, L + 1):
            Ar[jj] = (Ar[jj] + Ar[jj - 1]) % HEAD
    DU = [U[F1][jj] - U[F0][jj] for jj in range(M + 1)]
    fails = off = checked = tail = 0
    for d in range(v + 1):
        P = [0] * (M + 1)
        for w in range(1, v):
            c = KW[d][w]
            Uw = U[phi(w)]
            for jj in range(M + 1):
                P[jj] += c * Uw[jj]
        corr = phi(d) if d not in (r, r + 1) else (F0 if d == r else -F0)
        for j in range(0, L + 1):
            pj = P[j] if j <= M else 0
            if (j + d) % 2 == 1:
                if pj % MOD:
                    off += 1
                continue
            checked += 1
            tot = (pj + 2 * corr * (DU[j] if j <= M else 0) + S[j]) % MOD
            if tot:
                fails += 1
            elif j >= M + v - 1:
                tail += 1
    assert fails == 0 and off == 0 and checked == 8550 and tail == 3830
    print(f"[ok] r=9 end-to-end control: {checked} on-parity conditions, "
          f"0 violations; off-parity clean; {tail} automatic-tail pairs")


# ---------------------------- r=15 window ------------------------------
NTT_PRIMES = [(998244353, 3), (754974721, 11), (469762049, 3),
              (167772161, 3)]


def window():
    import numpy as np
    r = 15
    v = 31
    phi, b = phi_fn(r)
    F0, F1 = phi(15), phi(15) - 2 ** 15
    mu = b // 31
    M = max(max(abs(phi(w)) for w in range(1, v)), abs(F0), abs(F1))
    assert M == mu == 570285, "spectrum bound M' = mu at r=15"
    A = (b - M) // 2
    MODC = 1 << 31
    HEAD = 1 << 47
    L = M + 59                       # window + collapse margin
    print(f"window: j <= {L}, threshold {M + 30} = 570315")

    def binom_vec(n):
        """C(n, i) mod 2^47 for i = 0..n, exact 2-adic stepping."""
        out = np.zeros(n + 1, dtype=np.int64)
        cur, e = 1, 0
        out[0] = 1
        for i in range(1, n + 1):
            x = n - i + 1
            while x % 2 == 0:
                x //= 2
                e += 1
            y = i
            while y % 2 == 0:
                y //= 2
                e -= 1
            cur = (cur * x * pow(y, -1, HEAD)) % HEAD
            out[i] = (cur << e) % HEAD if e < 47 else 0
        return out

    def ntt(a, p, g, inv=False):
        n = len(a)
        a = a.copy()
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j |= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
        ln = 2
        while ln <= n:
            wlen = pow(g, (p - 1) // ln, p)
            if inv:
                wlen = pow(wlen, p - 2, p)
            half = ln >> 1
            w = np.ones(half, dtype=np.int64)
            for i in range(1, half):
                w[i] = w[i - 1] * wlen % p
            for st in range(0, n, ln):
                u = a[st:st + half].copy()   # copy: the slice is mutated below
                t = (a[st + half:st + ln] * w % p).copy()
                a[st:st + half] = (u + t) % p
                a[st + half:st + ln] = (u - t) % p
            ln <<= 1
        if inv:
            ninv = pow(n, p - 2, p)
            a = a * ninv % p
        return a

    def conv47(x, y):
        n = 1
        while n < len(x) + len(y) - 1:
            n <<= 1
        res = []
        for p, g in NTT_PRIMES:
            fx = np.zeros(n, dtype=np.int64)
            fy = np.zeros(n, dtype=np.int64)
            fx[:len(x)] = x % p
            fy[:len(y)] = y % p
            fz = ntt(ntt(fx, p, g) * ntt(fy, p, g) % p, p, g, inv=True)
            res.append(fz)
        # CRT to mod 2^47
        P = [p for p, _ in NTT_PRIMES]
        out = np.zeros(n, dtype=object)
        Ptot = 1
        for p in P:
            Ptot *= p
        acc = np.zeros(n, dtype=object)
        for idx, p in enumerate(P):
            Np = Ptot // p
            wgt = (Np * pow(Np % p, p - 2, p))
            acc += res[idx].astype(object) * wgt
        acc %= Ptot
        return np.array([int(x) & (HEAD - 1) for x in acc[:len(x) +
                        len(y) - 1]], dtype=np.int64)

    args = sorted({phi(w) for w in range(1, v)} | {F0, F1})
    pos_args = sorted({abs(F) for F in args})
    print(f"distinct nontrivial arguments: {len(args)}; "
          f"distinct |F| convolutions: {len(pos_args)}")
    U = {}
    hashes = {}
    for F in pos_args:
        aa, cc = (M + F) // 2, (M - F) // 2
        Av = binom_vec(aa)
        Bv = binom_vec(cc)
        sg = np.ones(cc + 1, dtype=np.int64)
        sg[1::2] = -1
        UF = conv47(Av, (Bv * sg) % HEAD)
        U[F] = UF % HEAD
        U[-F] = (UF * np.where(np.arange(len(UF)) % 2 == 0, 1, -1)) % HEAD
        hashes[F] = hashlib.sha256(U[F].tobytes()).hexdigest()
    # R-series (prefix sums)
    S = np.zeros(L + 1, dtype=object)
    Ar = np.zeros(L + 1, dtype=object)
    bm = binom_vec(M)
    Ar[:M + 1] = bm.astype(object)
    for rho in range(0, 30):
        cf = (pow(2, rho + 1, HEAD) * (comb(A, rho) % HEAD)) % HEAD
        S[rho:] = (S[rho:] + cf * Ar[:L + 1 - rho]) % HEAD
        acc = 0
        for jj in range(L + 1):
            acc = (acc + Ar[jj]) % HEAD
            Ar[jj] = acc
    S = np.array([int(x) for x in S], dtype=np.int64)
    KW = [[sum((-1) ** h * comb(d, h) * comb(v - d, w - h)
               for h in range(min(d, w) + 1)) for w in range(v + 1)]
          for d in range(v + 1)]
    DU = (U[F1] - U[F0]) % HEAD
    bad = []
    layer_counts = []
    for d in range(v + 1):
        # radial part only; the Delta-correction is parity-gated at use time
        P = np.zeros(M + 1, dtype=object)
        for w in range(1, v):
            P += int(KW[d][w]) * U[phi(w)].astype(object)
        P %= HEAD
        corr = phi(d) if d not in (15, 16) else (F0 if d == 15 else -F0)
        Pj = np.zeros(L + 1, dtype=np.int64)
        Pj[:M + 1] = np.array([int(x) for x in P], dtype=np.int64)
        DUj = np.zeros(L + 1, dtype=np.int64)
        DUj[:M + 1] = DU.astype(np.int64)
        # reduce mod 2^31 BEFORE combining: keeps products within int64
        tot = (Pj % MODC
               + (2 * (corr % MODC) * (DUj % MODC)) % MODC
               + S % MODC) % MODC                 # on-parity total
        par = (np.arange(L + 1) + d) % 2
        on_bad = np.nonzero((par == 0) & (tot != 0))[0]
        off_bad = np.nonzero((par == 1) & (Pj % MODC != 0))[0]
        if len(on_bad):
            bad.append((d, "on", list(on_bad[:5])))
        if len(off_bad):
            bad.append((d, "off", list(off_bad[:5])))
        layer_counts.append((d, int(len(on_bad)), int(len(off_bad))))
        print(f"  layer d={d:2d}: on-parity violations "
              f"{len(on_bad)}, off-parity {len(off_bad)}")
    verdict = "PASS" if not bad else f"FAIL {bad[:4]}"
    cert = hashlib.sha256(
        (repr(sorted(hashes.items())) + repr(layer_counts)
         + verdict).encode()).hexdigest()
    print("U_F sha256 (full):")
    for F, h in sorted(hashes.items()):
        print(f"  |F|={F}: {h}")
    print(f"per-layer counts (d, on, off): {layer_counts}")
    print(f"WINDOW VERDICT: {verdict}; certificate {cert}")
    assert not bad, f"WINDOW FAIL: {bad[:4]}"

    # ---- cross-check 1: NTT cofactors vs exact bigints, j <= 400 ----
    JX = 400
    for F in pos_args:
        aa, cc = (M + F) // 2, (M - F) // 2
        for j in range(JX + 1):
            cj = sum(comb(aa, i) * (-1) ** (j - i) * comb(cc, j - i)
                     for i in range(max(0, j - cc), min(aa, j) + 1))
            assert int(U[F][j]) == cj % HEAD, ("U mismatch", F, j)
            assert int(U[-F][j]) == (cj if j % 2 == 0 else -cj) % HEAD
    print(f"[ok] cross-check 1: all 9 U_F (and negatives) match exact "
          f"bigint cofactor coefficients for j <= {JX}")
    # ---- cross-check 2: R/S series vs exact quotient expansion --------
    for j in range(JX + 1):
        sj = 2 * sum(comb(M + A, i) * comb(A - 1 + j - i, j - i)
                     for i in range(0, j + 1))
        assert int(S[j]) % MODC == sj % MODC, ("S mismatch", j)
    print(f"[ok] cross-check 2: S-series matches exact "
          f"2*(1+z)^(M+A)(1-z)^(-A) mod 2^31 for j <= {JX}")
    # ---- cross-check 3: design-level integrality, exact recurrence ----
    Kex = {F: kraw_seq(F, b, JX) for F in args}
    Kb = kraw_seq(b, b, JX)
    for j in range(0, JX + 1):
        for d in (0, 7, 15, 16, 31):
            if (j + d) % 2:
                continue
            N = (1 + (-1) ** (d + j)) * Kb[j]
            N += sum(KW[d][w] * Kex[phi(w)][j] for w in range(1, v))
            corr = phi(d) if d not in (15, 16) else (F0 if d == 15 else -F0)
            N += 2 * corr * (Kex[F1][j] - Kex[F0][j])
            assert N % (1 << 31) == 0, ("exact-int fail", j, d)
    print(f"[ok] cross-check 3: exact bigint conditions integral, j <= {JX}")
    return verdict


def main():
    delta_lemma()
    r9_control()
    if MODE_WINDOW:
        window()
    else:
        print("(pass --window for the full r=15 finite-window run)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Spot integrality tests (2-adic mod 2^45 + mod-b prime-power side) for the
Krawtchouk/Fourier conditions of a hypothetical S(14,15,31), per Theorem A of
evidence/s141531_higher_xor_hierarchy.md.

Pure integer arithmetic: python bigints + numpy int64/uint64. No floats.
All numpy modular work exploits uint64 wraparound (exact mod 2^64), masked to
the working modulus 2^tbits (tbits <= 64). Odd prime powers of b are tiny
(<= 31) and use Granville-style factorial-unit formulas.

Run normally to print the audit.  Pass
  --output evidence/s141531_spot_integrality_results.txt
to regenerate the preserved transcript.
"""
import sys, time
import numpy as np
from math import comb
from pathlib import Path

M64 = (1 << 64) - 1

def bc(x):
    """binary digit sum (popcount) of a nonnegative python int (py3.9-safe)."""
    return bin(x).count("1")
B = 17678835
F0 = 1549
F1 = -31219

OUT = []
def log(s=""):
    print(s, flush=True)
    OUT.append(str(s))

RESULTS = None
if "--output" in sys.argv:
    output_index = sys.argv.index("--output") + 1
    if output_index >= len(sys.argv):
        raise SystemExit("--output requires a path")
    RESULTS = Path(sys.argv[output_index])


def flush_results():
    if RESULTS is None:
        return
    with RESULTS.open("w") as f:
        f.write("\n".join(OUT) + "\n")

# ---------------------------------------------------------------- setup
lam = []
for s in range(15):
    num, den = comb(31 - s, 14 - s), 15 - s
    assert num % den == 0, (s, num, den)
    lam.append(num // den)
assert lam[0] == B

phi_ext = [0] * 32
for w in range(15):
    phi_ext[w] = sum((-2) ** s * comb(w, s) * lam[s] for s in range(w + 1))
phi_ext[15] = F0
phi_ext[16] = -F0
for w in range(17, 32):
    phi_ext[w] = -phi_ext[31 - w]
assert phi_ext[0] == B
assert all(abs(v) % 2 == 1 for v in phi_ext)

# cube Krawtchouks Kc[d][w] = sum_h (-1)^h C(d,h) C(31-d, w-h)  (exact ints)
Kc = [[sum((-1) ** h * comb(d, h) * comb(31 - d, w - h)
           for h in range(0, min(d, w) + 1))
       for w in range(32)] for d in range(32)]
assert Kc[0][5] == comb(31, 5) and Kc[31][4] == comb(31, 4)

def factorize(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

BFACT = factorize(B)
PPOWS = sorted(p ** e for p, e in BFACT.items())
assert np.prod  # numpy import used
_prod = 1
for q in PPOWS:
    _prod *= q
assert _prod == B

ABSF = sorted({abs(f) for f in phi_ext} | {abs(F1)})

# ------------------------------------------------- 2-adic machinery (mod 2^64 table)
def build_odd_fact(nmax):
    """tbl[x] = odd part of x!  (mod 2^64), x = 0..nmax."""
    tbl = np.empty(nmax + 1, dtype=np.uint64)
    tbl[0] = 1
    carry = 1
    CH = 1 << 22
    for lo in range(1, nmax + 1, CH):
        hi = min(nmax, lo + CH - 1)
        x = np.arange(lo, hi + 1, dtype=np.int64)
        while True:
            ev = (x & 1) == 0
            if not ev.any():
                break
            x = np.where(ev, x >> 1, x)
        u = x.astype(np.uint64)
        u = np.cumprod(u)                      # wraps mod 2^64: exact mod 2^64
        u *= np.uint64(carry)
        tbl[lo:hi + 1] = u
        carry = int(tbl[hi])
    return tbl

def inv_u64_arr(x):
    """batch Newton inverse mod 2^64 of odd uint64 array."""
    y = x.copy()
    two = np.uint64(2)
    for _ in range(5):                          # 3*2^5 = 96 >= 64 bits
        y = y * (two - x * y)
    return y

def inv_u64_int(x):
    y = x
    for _ in range(6):
        y = (y * (2 - x * y)) & M64
    return y & M64

def s2a(x):
    """binary digit sum of nonneg int64 array."""
    x = x.copy()
    s = np.zeros_like(x)
    while x.any():
        s += x & 1
        x >>= 1
    return s

def K2_window(j, F, tbits, tbl):
    """K_j(F) mod 2^tbits for F>0, via factorial-table gathers.
       K_j(F) = sum_i (-1)^i C(Q,i) C(F, j-2i), Q=(B-F)//2."""
    assert F > 0 and (B - F) % 2 == 0
    Q = (B - F) // 2
    ilo = max(0, -((F - j) // 2))               # ceil((j-F)/2)
    ihi = min(Q, j // 2)
    if ilo > ihi:
        return 0
    mask = (1 << tbits) - 1
    umask = np.uint64(mask)
    uM = np.uint64(mask + 1)
    scal = np.uint64((int(tbl[F]) * int(tbl[Q])) & M64)
    total = 0
    CH = 1 << 21
    s2F, s2Q = bc(int(F)), bc(Q)
    for lo in range(ilo, ihi + 1, CH):
        hi = min(ihi, lo + CH - 1)
        i = np.arange(lo, hi + 1, dtype=np.int64)
        m = j - 2 * i
        v = (s2a(m) + s2a(F - m) - s2F) + (s2a(i) + s2a(Q - i) - s2Q)
        assert (v >= 0).all()
        den = tbl[m] * tbl[F - m] * tbl[i] * tbl[Q - i]
        unit = inv_u64_arr(den) * scal
        ok = v < tbits
        sh = np.where(ok, v, 0).astype(np.uint64)
        term = (unit << sh) & umask
        term = np.where(ok, term, np.uint64(0))
        neg = (i & 1) == 1
        term = np.where(neg, (uM - term) & umask, term)
        total += int(term.sum())
    return total % (mask + 1)

def prod_odd_range(a, b):
    """product of odd parts of integers in [a,b], mod 2^64. Empty (a>b) -> 1."""
    r = 1
    CH = 1 << 22
    lo = a
    while lo <= b:
        hi = min(b, lo + CH - 1)
        x = np.arange(lo, hi + 1, dtype=np.int64)
        while True:
            ev = (x & 1) == 0
            if not ev.any():
                break
            x = np.where(ev, x >> 1, x)
        r = (r * int(np.multiply.reduce(x.astype(np.uint64)))) & M64
        lo = hi + 1
    return r

def v2a(x):
    """(valuation, odd part) of positive int64 array."""
    x = x.copy()
    v = np.zeros_like(x)
    while True:
        ev = (x & 1) == 0
        if not ev.any():
            break
        x = np.where(ev, x >> 1, x)
        v = np.where(ev, v + 1, v)
    return v, x

def K2_window_v2(j, F, tbits):
    """Independent 2-adic path: term-ratio cumulative products, base term from
       direct range products (no global table). K_j(F) mod 2^tbits, F>0."""
    assert F > 0
    Q = (B - F) // 2
    ilo = max(0, -((F - j) // 2))
    ihi = min(Q, j // 2)
    if ilo > ihi:
        return 0
    mask = (1 << tbits) - 1
    # base term t0 = C(Q, ilo) * C(F, j-2*ilo)   (magnitude; sign applied later)
    m0 = j - 2 * ilo
    u0 = (prod_odd_range(Q - ilo + 1, Q) * inv_u64_int(prod_odd_range(1, ilo))) & M64
    u0 = (u0 * prod_odd_range(F - m0 + 1, F)) & M64
    u0 = (u0 * inv_u64_int(prod_odd_range(1, m0))) & M64
    v0 = (bc(ilo) + bc(Q - ilo) - bc(Q)) + (bc(m0) + bc(F - m0) - bc(F))
    L = ihi - ilo + 1
    if L == 1:
        units = np.array([u0], dtype=np.uint64)
        vals = np.array([v0], dtype=np.int64)
        iarr = np.array([ilo], dtype=np.int64)
    else:
        i = np.arange(ilo, ihi, dtype=np.int64)          # transitions i -> i+1
        m = j - 2 * i
        # ratio = (Q-i)*m*(m-1) / ((i+1)*(F-m+1)*(F-m+2))   (times -1, via parity)
        vn1, on1 = v2a(Q - i)
        vn2, on2 = v2a(m)
        vn3, on3 = v2a(m - 1)
        vd1, od1 = v2a(i + 1)
        vd2, od2 = v2a(F - m + 1)
        vd3, od3 = v2a(F - m + 2)
        num = np.cumprod(on1.astype(np.uint64) * on2.astype(np.uint64)
                         * on3.astype(np.uint64))
        den = np.cumprod(od1.astype(np.uint64) * od2.astype(np.uint64)
                         * od3.astype(np.uint64))
        dv = np.cumsum((vn1 + vn2 + vn3) - (vd1 + vd2 + vd3))
        units = np.empty(L, dtype=np.uint64)
        units[0] = u0
        units[1:] = np.uint64(u0) * num * inv_u64_arr(den)
        vals = np.empty(L, dtype=np.int64)
        vals[0] = v0
        vals[1:] = v0 + dv
        iarr = np.arange(ilo, ihi + 1, dtype=np.int64)
    assert (vals >= 0).all()
    umask = np.uint64(mask)
    uM = np.uint64(mask + 1)
    ok = vals < tbits
    sh = np.where(ok, vals, 0).astype(np.uint64)
    term = (units << sh) & umask
    term = np.where(ok, term, np.uint64(0))
    neg = (iarr & 1) == 1
    term = np.where(neg, (uM - term) & umask, term)
    return int(term.sum()) % (mask + 1)

# ------------------------------------------------- odd prime-power machinery
class PPrime:
    def __init__(self, p, e):
        self.p, self.e, self.pe = p, e, p ** e
        pe = self.pe
        T = [1] * pe
        for r in range(1, pe):
            T[r] = T[r - 1] * (r if r % p else 1) % pe
        self.T = np.array(T, dtype=np.int64)
        # Wilson generalization: product of units over a full block == -1 mod pe
        blk = 1
        for i in range(1, pe + 1):
            if i % p:
                blk = blk * i % pe
        assert blk == pe - 1, (p, e, blk)
        self.INV = np.array([pow(x, -1, pe) if x % p else 0 for x in range(pe)],
                            dtype=np.int64)

    def sdig_arr(self, x):
        x = x.copy()
        s = np.zeros_like(x)
        while x.any():
            s += x % self.p
            x //= self.p
        return s

    def sdig_int(self, n):
        s = 0
        while n:
            s += n % self.p
            n //= self.p
        return s

    def fact_unit_arr(self, n):
        """unit_p(n!) mod pe, vectorized (Granville / generalized Wilson)."""
        x = n.copy()
        acc = np.ones_like(x)
        sgn = np.zeros_like(x)
        while x.any():
            acc = acc * self.T[x % self.pe] % self.pe
            sgn ^= (x // self.pe) & 1
            x //= self.p
        return np.where(sgn == 1, (self.pe - acc) % self.pe, acc)

    def fact_unit_int(self, n):
        acc, sgn, x = 1, 0, n
        while x:
            acc = acc * int(self.T[x % self.pe]) % self.pe
            sgn ^= (x // self.pe) & 1
            x //= self.p
        return (self.pe - acc) % self.pe if sgn else acc

    def binom_arr(self, n, k):
        """C(n,k) mod pe: n scalar int, k int64 array with 0<=k<=n."""
        v = (self.sdig_arr(k) + self.sdig_arr(n - k) - self.sdig_int(n)) \
            // (self.p - 1)
        un = self.fact_unit_int(n) * self.INV[self.fact_unit_arr(k)] % self.pe
        un = un * self.INV[self.fact_unit_arr(n - k)] % self.pe
        pw = np.power(self.p, np.minimum(v, self.e))
        return np.where(v >= self.e, 0, un * pw % self.pe)

PP = {}
for p, e in sorted(BFACT.items()):
    PP[p ** e] = PPrime(p, e)

def K_pp(j, F, pp, reverse=False):
    """K_j(F) mod pp.pe for F>0. reverse=True: independent m-parameterized path."""
    assert F > 0
    Q = (B - F) // 2
    ilo = max(0, -((F - j) // 2))
    ihi = min(Q, j // 2)
    if ilo > ihi:
        return 0
    pe = pp.pe
    total = 0
    CH = 1 << 21
    if not reverse:
        for lo in range(ilo, ihi + 1, CH):
            hi = min(ihi, lo + CH - 1)
            i = np.arange(lo, hi + 1, dtype=np.int64)
            m = j - 2 * i
            t = pp.binom_arr(F, m) * pp.binom_arr(Q, i) % pe
            t = np.where((i & 1) == 1, (pe - t) % pe, t)
            total += int(t.sum())
    else:
        mlo, mhi = j - 2 * ihi, j - 2 * ilo
        m = np.arange(mhi, mlo - 1, -2, dtype=np.int64)   # descending, ~= diff order
        i = (j - m) // 2
        t = pp.binom_arr(F, m) * pp.binom_arr(Q, i) % pe
        t = np.where((i & 1) == 1, (pe - t) % pe, t)
        total = int(t.sum())
    return total % pe

# ------------------------------------------------- exact bigint recurrence
def K_exact_dict(F, jmax):
    """exact K_j(F) for j=0..jmax via (j+1)K_{j+1} = F K_j - (B-j+1) K_{j-1}."""
    out = {0: 1, 1: F}
    K0, K1 = 1, F
    for jj in range(1, jmax):
        num = F * K1 - (B - jj + 1) * K0
        q, r = divmod(num, jj + 1)
        assert r == 0, ("recurrence non-integral", F, jj)
        K0, K1 = K1, q
        out[jj + 1] = q
    return out

def crt(res):
    """res: dict pe -> residue. Returns x mod B."""
    x, M = 0, 1
    for pe, r in res.items():
        g = pow(M, -1, pe)
        x = x + M * ((r - x) * g % pe)
        M *= pe
    return x % B

# ------------------------------------------------- per-j analysis
def K_signed(v, f, j, mod):
    """apply sign rule: K_j(f) = (-1)^j K_j(|f|) for f<0; v = K_j(|f|) mod `mod`."""
    if f < 0 and j % 2 == 1:
        return (mod - v) % mod
    return v

def analyze_j(j, tbl, tbits=45):
    t0 = time.time()
    mask = (1 << tbits) - 1
    Mmod = mask + 1
    K2 = {a: K2_window(j, a, tbits, tbl) for a in ABSF}
    Kp = {pe: {a: K_pp(j, a, PP[pe]) for a in ABSF} for pe in PPOWS}

    def k2(f):
        return K_signed(K2[abs(f)], f, j, Mmod)

    D2 = (k2(F1) - k2(F0)) % Mmod
    if D2 == 0:
        v2D = tbits          # >= tbits
    else:
        v2D = (D2 & -D2).bit_length() - 1
    c1 = {}
    for d in range(j % 2, 32, 2):
        N = sum(Kc[d][w] * k2(phi_ext[w]) for w in range(32)) % Mmod
        val = (N + 2 * D2 * phi_ext[d]) % Mmod
        c1[d] = (val % (1 << 31) == 0, val)
    dstar = 31 if j % 2 else 0
    A2 = (c1[dstar][1] >> 31) if c1[dstar][0] else None

    Ap, jAp = {}, {}
    for pe in PPOWS:
        def kp(f):
            return K_signed(Kp[pe][abs(f)], f, j, pe)
        Dp = (kp(F1) - kp(F0)) % pe
        Np = sum(Kc[dstar][w] * kp(phi_ext[w]) for w in range(32)) % pe
        Anum = (Np + 2 * Dp * phi_ext[dstar]) % pe
        Ap[pe] = Anum * pow(pow(2, 31, pe), -1, pe) % pe
        jAp[pe] = j * Ap[pe] % pe

    res = {
        "j": j, "tbits": tbits,
        "K2": K2, "Kp": Kp, "D2": D2, "v2D": v2D,
        "c1": c1, "dstar": dstar, "A2_mod": A2,
        "Ap": Ap, "jAp": jAp,
        "c1_pass": all(v[0] for v in c1.values()),
        "d15_pass": D2 % (1 << 15) == 0,
        "c2_pass": all(v == 0 for v in jAp.values()),
        "A_mod_b": crt(Ap),
        "wall": time.time() - t0,
    }
    res["all_pass"] = res["c1_pass"] and res["d15_pass"] and res["c2_pass"]
    return res

def analyze_j_independent(j, tbits=50):
    """recheck path: 2-adic via v2 window at higher modulus; primes via reversed window."""
    t0 = time.time()
    mask = (1 << tbits) - 1
    Mmod = mask + 1
    K2 = {a: K2_window_v2(j, a, tbits) for a in ABSF}
    Kp = {pe: {a: K_pp(j, a, PP[pe], reverse=True) for a in ABSF} for pe in PPOWS}

    def k2(f):
        return K_signed(K2[abs(f)], f, j, Mmod)

    D2 = (k2(F1) - k2(F0)) % Mmod
    c1 = {}
    for d in range(j % 2, 32, 2):
        N = sum(Kc[d][w] * k2(phi_ext[w]) for w in range(32)) % Mmod
        val = (N + 2 * D2 * phi_ext[d]) % Mmod
        c1[d] = (val % (1 << 31) == 0, val)
    dstar = 31 if j % 2 else 0
    Ap, jAp = {}, {}
    for pe in PPOWS:
        def kp(f):
            return K_signed(Kp[pe][abs(f)], f, j, pe)
        Dp = (kp(F1) - kp(F0)) % pe
        Np = sum(Kc[dstar][w] * kp(phi_ext[w]) for w in range(32)) % pe
        Anum = (Np + 2 * Dp * phi_ext[dstar]) % pe
        Ap[pe] = Anum * pow(pow(2, 31, pe), -1, pe) % pe
        jAp[pe] = j * Ap[pe] % pe
    return {
        "j": j, "tbits": tbits, "K2": K2, "D2": D2, "c1": c1,
        "Ap": Ap, "jAp": jAp,
        "c1_pass": all(v[0] for v in c1.values()),
        "d15_pass": D2 % (1 << 15) == 0,
        "c2_pass": all(v == 0 for v in jAp.values()),
        "wall": time.time() - t0,
    }

def report_j(r, label=""):
    j = r["j"]
    fails = [d for d, v in r["c1"].items() if not v[0]]
    log(f"j = {j}{label}   wall = {r['wall']:.1f}s")
    if fails:
        log(f"  (C1) FAIL at layers {fails}")
        for d in fails:
            log(f"    d={d}: (N_j(d) + 2*Delta_j*phi_ext(d)) mod 2^{r['tbits']} = {r['c1'][d][1]}")
    else:
        n = len(r["c1"])
        log(f"  (C1) PASS  {n}/{n} layers d = {sorted(r['c1'])}")
    v2s = f">= {r['tbits']}" if r["v2D"] >= r["tbits"] else str(r["v2D"])
    log(f"  v2(Delta_j) = {v2s}  (need >= 15): {'PASS' if r['d15_pass'] else 'FAIL'}"
        f"   Delta_j mod 2^{r['tbits']} = {r['D2']}")
    log(f"  (C2) d* = {r['dstar']}: A_j mod b = {r['A_mod_b']}, "
        f"A_j mod p^e = {r['Ap']}, j*A_j mod p^e = {r['jAp']}"
        f" -> b | j*A_j: {'PASS' if r['c2_pass'] else 'FAIL'}")
    if r.get("A2_mod") is not None:
        log(f"  A_j mod 2^{r['tbits']-31} = {r['A2_mod']}")
    log(f"  VERDICT: {'PASS' if r['all_pass'] else 'FAIL'}")

# ================================================================ main
def main():
    T0 = time.time()
    log("spot_integrality.py  --  S(14,15,31) Krawtchouk integrality spot tests")
    log(f"b = {B} = " + " * ".join(f"{p}^{e}" if e > 1 else str(p)
                                    for p, e in sorted(BFACT.items())))
    log(f"prime powers used for mod-b side: {PPOWS}")
    log(f"lambda_s (s=0..14): {lam}")
    log(f"phi_ext(w), w=0..31: {phi_ext}")
    log(f"distinct positive Krawtchouk arguments: {ABSF}")
    log("")

    log("building odd-factorial table mod 2^64, x = 0..b ...")
    tb = time.time()
    tbl = build_odd_fact(B)
    log(f"  built in {time.time()-tb:.1f}s")

    # table sanity: reconstruct binomials exactly for cases with v2+bits < 64
    for (n, k) in [(10, 3), (100, 37), (1000, 431), (8839417, 3), (17678835, 2)]:
        v = bc(k) + bc(n - k) - bc(n)
        unit = (int(tbl[n]) * inv_u64_int((int(tbl[k]) * int(tbl[n - k])) & M64)) & M64
        c = comb(n, k)
        assert v == (c & -c).bit_length() - 1, (n, k)
        assert unit & ((1 << 45) - 1) == (c >> v) % (1 << 45), (n, k)
    log("  table sanity (5 exact binomial reconstructions mod 2^45): OK")

    # prime machinery sanity vs math.comb
    for pe, pp in PP.items():
        ks = np.array([0, 1, 2, 17, 100, 999, 1500], dtype=np.int64)
        got = pp.binom_arr(2000, ks)
        want = [comb(2000, int(k)) % pe for k in ks]
        assert list(got) == want, (pe, list(got), want)
    log("  prime-power binomial sanity vs math.comb (n=2000): OK")
    log("")

    # ---------------- CONTROL 1: exact recurrence vs modular machinery
    log("CONTROL 1: exact Krawtchouk recurrence j<=1000 vs window machinery")
    ctrl_F = [1549, -31219, phi_ext[2], phi_ext[7]]
    ok1 = True
    for F in ctrl_F:
        ex = K_exact_dict(F, 1000)
        for j in (700, 997):
            e45 = ex[j] % (1 << 45)
            e50 = ex[j] % (1 << 50)
            m45 = K_signed(K2_window(j, abs(F), 45, tbl), F, j, 1 << 45)
            m50 = K_signed(K2_window_v2(j, abs(F), 50), F, j, 1 << 50)
            pok = all(K_signed(K_pp(j, abs(F), PP[pe]), F, j, pe) == ex[j] % pe
                      for pe in PPOWS)
            prok = all(K_signed(K_pp(j, abs(F), PP[pe], reverse=True), F, j, pe)
                       == ex[j] % pe for pe in PPOWS)
            line = (f"  F={F:>8} j={j}: mod2^45 {'OK' if m45 == e45 else 'MISMATCH'}"
                    f", v2-path mod2^50 {'OK' if m50 == e50 else 'MISMATCH'}"
                    f", primes {'OK' if pok else 'MISMATCH'}"
                    f", primes-rev {'OK' if prok else 'MISMATCH'}")
            log(line)
            if not (m45 == e45 and m50 == e50 and pok and prok):
                ok1 = False
                log(f"    exact K_j(F) mod 2^45 = {e45}, machinery = {m45}")
                log(f"    exact K_j(F) mod 2^50 = {e50}, v2-path  = {m50}")
    if not ok1:
        log("CONTROL 1 FAILED -- STOPPING.")
        flush_results()
        sys.exit(1)
    log("CONTROL 1: PASS")
    log("")

    # cross-path agreement at large j (exercises ilo>0 branches of both paths)
    log("CONTROL 1b: cross-path agreement at j=1000000 (ilo>0 windows)")
    ok1b = True
    for F in (1549, 31219, 570285):
        a = K2_window(1000000, F, 45, tbl)
        bb = K2_window_v2(1000000, F, 50) % (1 << 45)
        pok = all(K_pp(1000000, F, PP[pe]) == K_pp(1000000, F, PP[pe], reverse=True)
                  for pe in PPOWS)
        log(f"  F={F:>7}: table-path vs ratio-path mod 2^45 "
            f"{'OK' if a == bb else 'MISMATCH'} ; primes fwd vs rev {'OK' if pok else 'MISMATCH'}")
        if a != bb or not pok:
            ok1b = False
    if not ok1b:
        log("CONTROL 1b FAILED -- STOPPING.")
        flush_results()
        sys.exit(1)
    log("CONTROL 1b: PASS")
    log("")

    # ---------------- CONTROL 2: j=3 exact
    log("CONTROL 2: j=3 exact values")
    K3 = {a: K_exact_dict(a, 3)[3] for a in ABSF}
    def k3(f):
        return K3[abs(f)] if f > 0 else -K3[abs(f)]     # j=3 odd
    D3 = k3(F1) - k3(F0)
    tgt_D3 = -(1 << 15) * 145938438
    log(f"  Delta_3 exact = {D3}  target -2^15*145938438 = {tgt_D3}: "
        f"{'OK' if D3 == tgt_D3 else 'MISMATCH'}")
    N331 = sum(Kc[31][w] * k3(phi_ext[w]) for w in range(32))
    A3num = N331 + 2 * D3 * phi_ext[31]
    assert A3num % (1 << 31) == 0, "A_3 not integral?!"
    A3 = A3num >> 31
    log(f"  A_3 exact = {A3}  target 927696866625: {'OK' if A3 == 927696866625 else 'MISMATCH'}")
    r3 = analyze_j(3, tbl, tbits=45)
    m_ok = (r3["D2"] == D3 % (1 << 45))
    a2_ok = (r3["A2_mod"] == A3 % (1 << 14))
    ap_ok = all(r3["Ap"][pe] == A3 % pe for pe in PPOWS)
    ab_ok = (r3["A_mod_b"] == A3 % B)
    log(f"  machinery Delta_3 mod 2^45 {'OK' if m_ok else 'MISMATCH'}"
        f" ; A_3 mod 2^14 {'OK' if a2_ok else 'MISMATCH'}"
        f" ; A_3 mod p^e all {'OK' if ap_ok else 'MISMATCH'}"
        f" ; A_3 mod b = {r3['A_mod_b']} vs {A3 % B} {'OK' if ab_ok else 'MISMATCH'}")
    log(f"  j*A_3 mod b = {3 * A3 % B}  (b | 3*A_3: {'yes' if 3 * A3 % B == 0 else 'no'})")
    if not (D3 == tgt_D3 and A3 == 927696866625 and m_ok and a2_ok and ap_ok and ab_ok):
        log("CONTROL 2 FAILED -- STOPPING.")
        flush_results()
        sys.exit(1)
    log("CONTROL 2: PASS")
    log("")

    # ---------------- CONTROL 3: j = 19999, 20000 must fully pass
    log("CONTROL 3: j = 19999, 20000 (inside committed verified sweep) must PASS")
    ok3 = True
    for j in (19999, 20000):
        r = analyze_j(j, tbl)
        report_j(r, "  [control]")
        if not r["all_pass"]:
            ok3 = False
    if not ok3:
        log("CONTROL 3 FAILED -- STOPPING (machinery or committed range in question).")
        flush_results()
        sys.exit(1)
    log("CONTROL 3: PASS")
    log("")
    flush_results()

    # ---------------- MAIN SWEEP
    sweep = [50000, 262144, 1000000, 4194304, 8839417, 8839418,
             12000000, 16777216, 17600000]
    log("MAIN SWEEP: spot j values in untested range 20000 < j < b-20000")
    table = []
    for j in sweep:
        r = analyze_j(j, tbl)
        report_j(r)
        verdict = "PASS" if r["all_pass"] else "FAIL"
        if not r["all_pass"]:
            log(f"  *** FAILURE at j={j} -- rerunning with independent code path "
                f"(mod 2^50, ratio-derived window, reversed prime windows) ***")
            ri = analyze_j_independent(j)
            log(f"  independent path: C1 {'PASS' if ri['c1_pass'] else 'FAIL'}, "
                f"v2(Delta)>=15 {'PASS' if ri['d15_pass'] else 'FAIL'}, "
                f"C2 {'PASS' if ri['c2_pass'] else 'FAIL'}  (wall {ri['wall']:.1f}s)")
            agree2 = all(ri["K2"][a] % (1 << 45) == r["K2"][a] for a in ABSF)
            log(f"  K-value agreement between paths (mod 2^45): "
                f"{'AGREE' if agree2 else 'DISAGREE'}")
            log(f"  independent-path residues: Delta mod 2^50 = {ri['D2']}")
            for d, v in sorted(ri["c1"].items()):
                if not v[0]:
                    log(f"    d={d}: residue mod 2^50 = {v[1]}, mod 2^31 = {v[1] % (1<<31)}")
            log(f"    Ap = {ri['Ap']}  jAp = {ri['jAp']}")
            confirmed = (ri["c1_pass"] == r["c1_pass"]
                         and ri["d15_pass"] == r["d15_pass"]
                         and ri["c2_pass"] == r["c2_pass"] and agree2)
            verdict = ("FAIL-CONFIRMED" if confirmed else "FAIL-UNCONFIRMED(paths disagree!)")
            log(f"  ==> {verdict}")
        table.append((j, r, verdict))
        log("")
        flush_results()

    log("=" * 78)
    log("SUMMARY TABLE")
    log(f"{'j':>10}  {'C1':>6}  {'v2(D)>=15':>10}  {'C2 b|jA':>8}  {'verdict':>16}  {'wall(s)':>8}")
    for j, r, verdict in table:
        n = len(r["c1"])
        c1s = f"{sum(1 for v in r['c1'].values() if v[0])}/{n}"
        log(f"{j:>10}  {c1s:>6}  {('yes' if r['d15_pass'] else 'NO'):>10}  "
            f"{('yes' if r['c2_pass'] else 'NO'):>8}  {verdict:>16}  {r['wall']:>8.1f}")
    log("")
    log(f"total wall time: {time.time()-T0:.1f}s")
    flush_results()

if __name__ == "__main__":
    main()

/* exh.c -- EXHAUSTIVE enumeration of the whole class Pi(n, r), for parameters
 * small enough to allow it, plus a completion decision for every instance.
 *
 *   Pi(n, r): |A| = n, q = n+r-1 colours, |S_a| = r for every a,
 *             m_c = #{a : c in S_a} <= r and n - m_c even.
 *
 * An instance IS the n x q incidence matrix (rows = vertices, columns =
 * colours), with row sums r and column sums in {r, r-2, ...}.  We enumerate
 * those matrices up to S_n x S_q by the lex-maximal representative scheme of
 * NOTE.md section 6:
 *   (C) column vectors non-increasing (row 0 the most significant bit);
 *   (R) inside every maximal block of rows agreeing on columns 1..j-1, the
 *       rows with a 1 in column j precede those with a 0.
 * Lemma G of NOTE.md proves this generates a representative of every orbit.
 *
 * build: cc -O3 -DN=9 -DR=3 -o exh_9_3 exh.c
 * run:   ./exh_9_3 [count|solve] [PART NPARTS]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#ifndef N
#define N 9
#endif
#ifndef R
#define R 3
#endif
#define Q (N + R - 1)
#define FULLC ((1u << Q) - 1u)
#define FULLV ((1u << N) - 1u)

static inline int pc(uint32_t x) { return __builtin_popcount(x); }

/* ---------------- completion solver (same algorithm as cbsearch.c) -------- */
static uint32_t avail[N], openv[N];
static long nodes;

static int rec(void)
{
    nodes++;
    int uA[256], uB[256], uC[256], nu = 0, rv = 0;
    for (;;) {
        int fa = -1, fb = -1, fc = -1;
        int bestcnt = 1000, bkind = -1, bx = -1, by = -1;
        uint32_t bmask = 0;
        for (int a = 0; a < N && fa < 0; a++) {
            uint32_t om = openv[a] & ~((1u << (a + 1)) - 1u);
            while (om) {
                int b = __builtin_ctz(om); om &= om - 1;
                uint32_t m = avail[a] & avail[b];
                if (!m) { rv = 0; goto done; }
                int c = pc(m);
                if (c == 1) { fa = a; fb = b; fc = __builtin_ctz(m); break; }
                if (c < bestcnt) { bestcnt = c; bkind = 0; bx = a; by = b; bmask = m; }
            }
        }
        if (fa < 0) {
            for (int a = 0; a < N && fa < 0; a++) {
                uint32_t m = avail[a];
                while (m) {
                    int c = __builtin_ctz(m); m &= m - 1;
                    uint32_t cand = 0, om = openv[a];
                    while (om) { int b = __builtin_ctz(om); om &= om - 1;
                                 if ((avail[b] >> c) & 1u) cand |= 1u << b; }
                    if (!cand) { rv = 0; goto done; }
                    int k = pc(cand);
                    if (k == 1) { fa = a; fb = __builtin_ctz(cand); fc = c; break; }
                    if (k < bestcnt) { bestcnt = k; bkind = 1; bx = a; by = c; bmask = cand; }
                }
            }
        }
        if (fa < 0) {
            int allclosed = 1;
            for (int a = 0; a < N; a++) if (openv[a]) { allclosed = 0; break; }
            if (allclosed) { rv = 1; goto done; }
            if (bkind == 0) {
                int a = bx, b = by; uint32_t m = bmask;
                while (m) {
                    int c = __builtin_ctz(m); m &= m - 1;
                    avail[a] ^= 1u << c; avail[b] ^= 1u << c;
                    openv[a] &= ~(1u << b); openv[b] &= ~(1u << a);
                    int r = rec();
                    avail[a] ^= 1u << c; avail[b] ^= 1u << c;
                    openv[a] |= 1u << b; openv[b] |= 1u << a;
                    if (r) { rv = r; goto done; }
                }
            } else {
                int a = bx, c = by; uint32_t m = bmask;
                while (m) {
                    int b = __builtin_ctz(m); m &= m - 1;
                    avail[a] ^= 1u << c; avail[b] ^= 1u << c;
                    openv[a] &= ~(1u << b); openv[b] &= ~(1u << a);
                    int r = rec();
                    avail[a] ^= 1u << c; avail[b] ^= 1u << c;
                    openv[a] |= 1u << b; openv[b] |= 1u << a;
                    if (r) { rv = r; goto done; }
                }
            }
            rv = 0; goto done;
        }
        avail[fa] ^= 1u << fc; avail[fb] ^= 1u << fc;
        openv[fa] &= ~(1u << fb); openv[fb] &= ~(1u << fa);
        uA[nu] = fa; uB[nu] = fb; uC[nu] = fc; nu++;
    }
done:
    for (int i = nu - 1; i >= 0; i--) {
        avail[uA[i]] ^= 1u << uC[i]; avail[uB[i]] ^= 1u << uC[i];
        openv[uA[i]] |= 1u << uB[i]; openv[uB[i]] |= 1u << uA[i];
    }
    return rv;
}

static int solve(const uint32_t *forb)
{
    for (int a = 0; a < N; a++) {
        avail[a] = FULLC & ~forb[a];
        openv[a] = FULLV & ~(1u << a);
    }
    nodes = 0;
    return rec();
}

/* ---------------- enumeration ---------------- */
static int VALS[16], NVALS = 0, MINV = 0, MAXV = 0;
static uint32_t MASKS[1 << 20];
static uint32_t MVAL[1 << 20];
static int NMASK = 0;
static long long counted = 0, sat = 0, unsat = 0;
static int dosolve = 0, PART = 0, NPARTS = 1;
static long long topidx = 0;
static uint32_t colmask[Q];
static int cap[N], blockid[N];

static int reach[64][512];             /* reach[left][T] = 1 if T is a sum of
                                          `left` values from VALS */
static void build_reach(void)
{
    memset(reach, 0, sizeof(reach));
    reach[0][0] = 1;
    for (int l = 1; l < 64 && l <= Q; l++)
        for (int T = 0; T <= N * R; T++)
            for (int i = 0; i < NVALS; i++)
                if (T >= VALS[i] && reach[l - 1][T - VALS[i]]) { reach[l][T] = 1; break; }
}

static int feasible(int left)
{
    int T = 0, mx = 0;
    for (int i = 0; i < N; i++) { T += cap[i]; if (cap[i] > mx) mx = cap[i]; }
    if (mx > left) return 0;
    if (T > N * R) return 0;
    return reach[left][T];
}

static void emit_instance(void)
{
    uint32_t forb[N];
    for (int i = 0; i < N; i++) {
        uint32_t f = 0;
        for (int j = 0; j < Q; j++) if ((colmask[j] >> i) & 1u) f |= 1u << j;
        forb[i] = f;
    }
    counted++;
    if (dosolve) {
        if (solve(forb)) sat++;
        else {
            unsat++;
            printf("EXH_UNSAT N=%d R=%d [", N, R);
            for (int a = 0; a < N; a++) printf("%u%s", forb[a], a + 1 < N ? "," : "");
            printf("]\n"); fflush(stdout);
        }
    }
    if ((counted % 1000000) == 0)
        fprintf(stderr, "  ... %lld enumerated (SAT %lld UNSAT %lld)\n", counted, sat, unsat);
}

static void go(int j, uint32_t prev)
{
    if (j == Q) {
        for (int i = 0; i < N; i++) if (cap[i]) return;
        emit_instance();
        return;
    }
    if (!feasible(Q - j)) return;
    for (int t = 0; t < NMASK; t++) {
        uint32_t m = MASKS[t], val = MVAL[t];
        if (val > prev) continue;
        int ok = 1;
        for (int i = 0; i < N && ok; i++) if (((m >> i) & 1u) && cap[i] == 0) ok = 0;
        if (!ok) continue;
        for (int i = 0; i + 1 < N && ok; i++)
            if (blockid[i] == blockid[i + 1] && !((m >> i) & 1u) && ((m >> (i + 1)) & 1u))
                ok = 0;
        if (!ok) continue;
        if (j == 2) { if ((topidx++ % NPARTS) != PART) continue; }
        int oldblock[N];
        memcpy(oldblock, blockid, sizeof(blockid));
        colmask[j] = m;
        for (int i = 0; i < N; i++) if ((m >> i) & 1u) cap[i]--;
        int nb = 0, cur = -1, curbit = -1;
        for (int i = 0; i < N; i++) {
            int bit = (m >> i) & 1u;
            if (oldblock[i] != cur || bit != curbit) { nb++; cur = oldblock[i]; curbit = bit; }
            blockid[i] = nb;
        }
        go(j + 1, val);
        memcpy(blockid, oldblock, sizeof(blockid));
        for (int i = 0; i < N; i++) if ((m >> i) & 1u) cap[i]++;
    }
}

int main(int argc, char **argv)
{
    dosolve = (argc > 1 && !strcmp(argv[1], "solve"));
    if (argc > 3) { PART = atoi(argv[2]); NPARTS = atoi(argv[3]); }
    int top = ((R - N) % 2 == 0) ? R : R - 1;
    if (top < 0) top = 0;
    for (int v = top; v >= 0; v -= 2) VALS[NVALS++] = v;
    MINV = VALS[NVALS - 1]; MAXV = VALS[0];
    build_reach();
    for (uint32_t m = 0; m < (1u << N); m++) {
        int k = pc(m), good = 0;
        for (int i = 0; i < NVALS; i++) if (VALS[i] == k) good = 1;
        if (!good) continue;
        uint32_t val = 0;
        for (int i = 0; i < N; i++) if ((m >> i) & 1u) val |= 1u << (N - 1 - i);
        MASKS[NMASK] = m; MVAL[NMASK] = val; NMASK++;
    }
    /* sort masks by value descending so that (C) prunes early */
    for (int i = 0; i < NMASK; i++)
        for (int j = i + 1; j < NMASK; j++)
            if (MVAL[j] > MVAL[i]) {
                uint32_t t = MVAL[i]; MVAL[i] = MVAL[j]; MVAL[j] = t;
                t = MASKS[i]; MASKS[i] = MASKS[j]; MASKS[j] = t;
            }
    for (int i = 0; i < N; i++) { cap[i] = R; blockid[i] = 0; }
    fprintf(stderr, "N=%d R=%d Q=%d column sizes:", N, R, Q);
    for (int i = 0; i < NVALS; i++) fprintf(stderr, " %d", VALS[i]);
    fprintf(stderr, "  (%d masks)\n", NMASK);
    go(0, 0xFFFFFFFFu);
    printf("exh N=%d R=%d part %d/%d: enumerated %lld  SAT %lld  UNSAT %lld  (solve=%d)\n",
           N, R, PART, NPARTS, counted, sat, unsat, dosolve);
    return 0;
}

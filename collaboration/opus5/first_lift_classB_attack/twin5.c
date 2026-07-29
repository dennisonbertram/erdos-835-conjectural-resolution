/* twin5.c -- EXHAUSTIVE search of the "size-5 twin class" family at n = 13.
 *
 * A class-B instance at n = 13, q = 17 has a twin class of size 5 (five
 * vertices with the same S_a) if and only if five colours share one support
 * of size 8; these are the extremal configurations of the k=12 and k=14
 * counterexample families of results/first_lift_k13_hole/NOTE.md.
 *
 * Writing Y for the five twins and R = S_a (a in Y), every c in R has m_c = 5
 * and V_c = X := A \ Y, |X| = 8.  The instance is then completely described by
 * the 8 x 12 incidence matrix of the OTHER twelve colours against X:
 *      row sums 5, column sums in {1,3,5}.
 *
 * We enumerate those matrices up to S_8 x S_12 with the "lex-maximal
 * representative" scheme, which is complete:
 *
 *   (C) the column vectors v_1 >= v_2 >= ... >= v_12  (v_j read top to bottom
 *       as a binary number, row 0 the most significant bit);
 *   (R) inside every maximal block of rows that agree on columns 1..j-1, the
 *       rows with a 1 in column j precede the rows with a 0.
 *
 * Completeness proof (self-contained; see NOTE.md): take the member of the
 * S_8 x S_12 orbit whose column-by-column reading is lexicographically
 * maximal.  Swapping two adjacent columns with v_j < v_{j+1} increases that
 * string, so (C) holds; transposing two rows of a block that violate (R)
 * increases it as well, so (R) holds.
 *
 * build: cc -O3 -o twin5 twin5.c
 * run:   ./twin5 count            (enumerate only)
 *        ./twin5 solve            (enumerate and decide every instance)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define NR 8            /* rows    = X            */
#define NC 12           /* columns = other colours */
#define N 13
#define Q 17
#define FULLC ((1u << Q) - 1u)
#define FULLV ((1u << N) - 1u)

static inline int pc(uint32_t x) { return __builtin_popcount(x); }

/* ------------------------------------------------------------------ */
/* the completion solver (same algorithm as cbsearch.c)               */
/* ------------------------------------------------------------------ */
static uint32_t avail[N], openv[N];
static long nodes;

static int rec(void)
{
    nodes++;
    int undoA[128], undoB[128], undoC[128], nundo = 0;
    int rv = 0;
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
        undoA[nundo] = fa; undoB[nundo] = fb; undoC[nundo] = fc; nundo++;
    }
done:
    for (int i = nundo - 1; i >= 0; i--) {
        int a = undoA[i], b = undoB[i], c = undoC[i];
        avail[a] ^= 1u << c; avail[b] ^= 1u << c;
        openv[a] |= 1u << b; openv[b] |= 1u << a;
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

/* ------------------------------------------------------------------ */
static long long counted = 0, sat = 0, unsat = 0;
static int dosolve = 0;
static uint32_t colmask[NC];              /* bit i (i = row) set */
static int cap[NR];
static int blockid[NR];                   /* current row-block labels */

/* feasibility of the remaining capacities with `left` columns to go */
static int feasible(int left)
{
    int T = 0, mx = 0;
    for (int i = 0; i < NR; i++) { T += cap[i]; if (cap[i] > mx) mx = cap[i]; }
    if (T > 5 * left || T < left) return 0;
    if ((T - left) & 1) return 0;
    if (mx > left) return 0;
    return 1;
}

static long long SLICE = 0;

static void emit_instance(void)
{
    if (SLICE) {
        if (counted < SLICE) {
            printf("[");
            for (int j = 0; j < NC; j++) printf("%u%s", colmask[j], j + 1 < NC ? "," : "");
            printf("]\n");
        }
        counted++;
        if (counted >= SLICE) exit(0);
        return;
    }
    /* rows 0..7 of X are vertices 0..7; twins Y are vertices 8..12
       colours: 0..11 are the "other" colours, 12..16 are R            */
    uint32_t forb[N];
    for (int i = 0; i < NR; i++) {
        uint32_t f = 0;
        for (int j = 0; j < NC; j++) if ((colmask[j] >> i) & 1u) f |= 1u << j;
        forb[i] = f;
    }
    for (int i = NR; i < N; i++) forb[i] = 0x1F000u;      /* colours 12..16 */
    counted++;
    if (dosolve) {
        int r = solve(forb);
        if (r) sat++;
        else {
            unsat++;
            printf("TWIN5_UNSAT [");
            for (int a = 0; a < N; a++) printf("%u%s", forb[a], a + 1 < N ? "," : "");
            printf("]\n"); fflush(stdout);
        }
    }
    if ((counted % 1000000) == 0) {
        fprintf(stderr, "  ... %lld enumerated (SAT %lld UNSAT %lld)\n", counted, sat, unsat);
    }
}

static int PART = 0, NPARTS = 1, topidx = 0;

static void go(int j, uint32_t prev)
{
    if (j == NC) {
        int ok = 1;
        for (int i = 0; i < NR; i++) if (cap[i]) ok = 0;
        if (ok) emit_instance();
        return;
    }
    if (!feasible(NC - j)) return;
    /* candidate masks: popcount in {1,3,5}, value <= prev (row 0 = MSB),
       respecting capacities and the block prefix rule                      */
    for (uint32_t m = 0; m < (1u << NR); m++) {
        int k = pc(m);
        if (k != 1 && k != 3 && k != 5) continue;
        /* column value with row 0 as most significant bit */
        uint32_t val = 0;
        for (int i = 0; i < NR; i++) if ((m >> i) & 1u) val |= 1u << (NR - 1 - i);
        if (val > prev) continue;
        int ok = 1;
        for (int i = 0; i < NR && ok; i++) if (((m >> i) & 1u) && cap[i] == 0) ok = 0;
        if (!ok) continue;
        /* prefix rule: inside each block, the chosen rows come first */
        for (int i = 0; i + 1 < NR && ok; i++)
            if (blockid[i] == blockid[i + 1] && !((m >> i) & 1u) && ((m >> (i + 1)) & 1u))
                ok = 0;
        if (!ok) continue;
        if (j == 3) { if ((topidx++ % NPARTS) != PART) continue; }
        int oldblock[NR];
        memcpy(oldblock, blockid, sizeof(blockid));
        colmask[j] = m;
        for (int i = 0; i < NR; i++) if ((m >> i) & 1u) cap[i]--;
        /* refine blocks */
        int nb = 0, cur = -1, curbit = -1;
        for (int i = 0; i < NR; i++) {
            int bit = (m >> i) & 1u;
            if (oldblock[i] != cur || bit != curbit) { nb++; cur = oldblock[i]; curbit = bit; }
            blockid[i] = nb;
        }
        go(j + 1, val);
        memcpy(blockid, oldblock, sizeof(blockid));
        for (int i = 0; i < NR; i++) if ((m >> i) & 1u) cap[i]++;
    }
}

int main(int argc, char **argv)
{
    dosolve = (argc > 1 && !strcmp(argv[1], "solve"));
    if (argc > 3) { PART = atoi(argv[2]); NPARTS = atoi(argv[3]); }
    if (argc > 1 && !strcmp(argv[1], "slice")) SLICE = atoll(argv[2]);
    for (int i = 0; i < NR; i++) { cap[i] = 5; blockid[i] = 0; }
    go(0, 0xFFFFFFFFu);
    printf("twin5 exhaustive part %d/%d: enumerated %lld  SAT %lld  UNSAT %lld  (solve=%d)\n",
           PART, NPARTS, counted, sat, unsat, dosolve);
    return 0;
}

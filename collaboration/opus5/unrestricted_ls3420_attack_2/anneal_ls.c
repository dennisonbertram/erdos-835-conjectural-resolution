/* Stochastic search for a large set LS(t, t+1, v) with m = v - t classes.
 *
 * Formulation used (exactly the unrestricted problem, no ansatz):
 *   colour every (t+1)-subset of [v] with one of m = v-t colours so that for
 *   every t-subset T the m blocks containing T carry m distinct colours.
 *   That is precisely a partition of all (t+1)-subsets into m disjoint
 *   S(t,t+1,v).
 *
 * Cost = sum over t-sets T of (m - #distinct colours in the star of T).
 * Cost 0  <=>  a large set.
 *
 * Search = min-conflicts on a randomly chosen violated star, plus a
 * Metropolis acceptance rule and periodic random restarts.  This program only
 * ever *proposes* objects; a separate deterministic Python verifier decides
 * whether an emitted object is genuine.  A non-zero final cost is NOT evidence
 * of non-existence.
 *
 * Usage: anneal_ls <v> <t> <seed> <seconds> [outfile]
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
#include <math.h>

static int V, T_SIZE, M;      /* ground size, t, number of colours = V - t */
static int NB, NT;            /* number of (t+1)-sets (blocks), number of t-sets */

static int *blockOfT;         /* NT * M : the blocks of each star */
static int *tOfBlock;         /* NB * (T_SIZE+1) : the t-subsets of each block */
static int *posInStar;        /* NB * (T_SIZE+1) : index of that block inside that star */
static int *colour;           /* NB */
static int *cnt;              /* NT * M */
static long cost;

/* ---------------- combinatorial indexing ---------------- */

static long *binom;           /* binom[n*(V+2)+k] */
static long C(int n, int k) {
    if (k < 0 || k > n) return 0;
    return binom[n * (V + 2) + k];
}

static void initBinom(void) {
    binom = calloc((size_t)(V + 2) * (V + 2), sizeof(long));
    for (int n = 0; n <= V + 1; n++) {
        binom[n * (V + 2) + 0] = 1;
        for (int k = 1; k <= n; k++)
            binom[n * (V + 2) + k] =
                binom[(n - 1) * (V + 2) + k - 1] + binom[(n - 1) * (V + 2) + k];
    }
}

/* colex rank of a strictly increasing k-subset */
static long rankSet(const int *s, int k) {
    long r = 0;
    for (int i = 0; i < k; i++) r += C(s[i], i + 1);
    return r;
}

static void unrankSet(long r, int k, int *out) {
    for (int i = k; i >= 1; i--) {
        int x = i - 1;
        while (C(x + 1, i) <= r) x++;
        out[i - 1] = x;
        r -= C(x, i);
    }
}

/* ---------------- rng ---------------- */

static uint64_t rngState;
static inline uint64_t rnd64(void) {
    rngState ^= rngState << 13;
    rngState ^= rngState >> 7;
    rngState ^= rngState << 17;
    return rngState;
}
static inline int rndInt(int n) { return (int)(rnd64() % (uint64_t)n); }
static inline double rndUnit(void) { return (double)(rnd64() >> 11) / 9007199254740992.0; }

/* ---------------- setup ---------------- */

static void build(void) {
    NB = (int)C(V, T_SIZE + 1);
    NT = (int)C(V, T_SIZE);
    blockOfT = malloc((size_t)NT * M * sizeof(int));
    tOfBlock = malloc((size_t)NB * (T_SIZE + 1) * sizeof(int));
    posInStar = malloc((size_t)NB * (T_SIZE + 1) * sizeof(int));
    colour = malloc((size_t)NB * sizeof(int));
    cnt = malloc((size_t)NT * M * sizeof(int));

    int *fill = calloc((size_t)NT, sizeof(int));
    int blk[16], sub[16];
    for (int b = 0; b < NB; b++) {
        unrankSet(b, T_SIZE + 1, blk);
        for (int d = 0; d <= T_SIZE; d++) {          /* drop position d */
            int j = 0;
            for (int i = 0; i <= T_SIZE; i++) if (i != d) sub[j++] = blk[i];
            long tr = rankSet(sub, T_SIZE);
            tOfBlock[b * (T_SIZE + 1) + d] = (int)tr;
            posInStar[b * (T_SIZE + 1) + d] = fill[tr];
            blockOfT[tr * M + fill[tr]] = b;
            fill[tr]++;
        }
    }
    for (int t = 0; t < NT; t++)
        if (fill[t] != M) { fprintf(stderr, "star size %d != %d\n", fill[t], M); exit(1); }
    free(fill);
}

static void randomise(void) {
    memset(cnt, 0, (size_t)NT * M * sizeof(int));
    for (int b = 0; b < NB; b++) {
        colour[b] = rndInt(M);
        for (int d = 0; d <= T_SIZE; d++)
            cnt[tOfBlock[b * (T_SIZE + 1) + d] * M + colour[b]]++;
    }
    cost = 0;
    for (int t = 0; t < NT; t++) {
        int miss = 0;
        for (int c = 0; c < M; c++) if (cnt[t * M + c] == 0) miss++;
        cost += miss;
    }
}

/* recolour block b to nc; maintains cnt and cost */
static void recolour(int b, int nc) {
    int oc = colour[b];
    if (oc == nc) return;
    for (int d = 0; d <= T_SIZE; d++) {
        int t = tOfBlock[b * (T_SIZE + 1) + d];
        int *row = cnt + (size_t)t * M;
        if (--row[oc] == 0) cost++;
        if (row[nc]++ == 0) cost--;
    }
    colour[b] = nc;
}

static long deltaOf(int b, int nc) {
    int oc = colour[b];
    if (oc == nc) return 0;
    long d = 0;
    for (int k = 0; k <= T_SIZE; k++) {
        int t = tOfBlock[b * (T_SIZE + 1) + k];
        int *row = cnt + (size_t)t * M;
        if (row[oc] == 1) d++;
        if (row[nc] == 0) d--;
    }
    return d;
}

/* ---------------- search ---------------- */

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: %s v t seed seconds [out]\n", argv[0]); return 2; }
    V = atoi(argv[1]);
    T_SIZE = atoi(argv[2]);
    rngState = strtoull(argv[3], NULL, 10) * 6364136223846793005ULL + 1442695040888963407ULL;
    double seconds = atof(argv[4]);
    const char *out = argc > 5 ? argv[5] : NULL;
    double T0 = argc > 6 ? atof(argv[6]) : 0.55;
    double cool = argc > 7 ? atof(argv[7]) : 0.999999;
    M = V - T_SIZE;

    initBinom();
    build();
    printf("LS(%d,%d,%d): %d blocks, %d stars, %d colours, %d blocks/class\n",
           T_SIZE, T_SIZE + 1, V, NB, NT, M, NB / M);
    fflush(stdout);

    long best = -1;
    clock_t t0 = clock();
    double elapsed = 0.0;
    long long iters = 0;
    double temp = T0;

    /* deficient stars kept in a simple list, rebuilt lazily */
    int *deficient = malloc((size_t)NT * sizeof(int));

    while (elapsed < seconds) {
        randomise();
        long stall = 0;
        long localBest = cost;
        temp = T0;
        while (elapsed < seconds && cost > 0 && stall < 30000000L) {
            /* collect a random deficient star cheaply: sample until hit */
            int t = -1;
            for (int tries = 0; tries < 200; tries++) {
                int cand = rndInt(NT);
                int miss = 0;
                for (int c = 0; c < M; c++) if (cnt[cand * M + c] == 0) { miss = 1; break; }
                if (miss) { t = cand; break; }
            }
            if (t < 0) {
                int nd = 0;
                for (int i = 0; i < NT; i++) {
                    for (int c = 0; c < M; c++) if (cnt[i * M + c] == 0) { deficient[nd++] = i; break; }
                }
                if (nd == 0) break;
                t = deficient[rndInt(nd)];
            }
            /* pick a missing colour and a duplicated colour in this star */
            int missing[64], nmiss = 0, dup[64], ndup = 0;
            for (int c = 0; c < M; c++) {
                if (cnt[t * M + c] == 0) missing[nmiss++] = c;
                else if (cnt[t * M + c] >= 2) dup[ndup++] = c;
            }
            if (nmiss == 0 || ndup == 0) { stall++; continue; }
            int nc = missing[rndInt(nmiss)];
            int dc = dup[rndInt(ndup)];
            /* choose one of the blocks in the star carrying dc */
            int chosen = -1, seen = 0;
            for (int i = 0; i < M; i++) {
                int b = blockOfT[t * M + i];
                if (colour[b] == dc) { seen++; if (rndInt(seen) == 0) chosen = b; }
            }
            long d = deltaOf(chosen, nc);
            if (d <= 0 || rndUnit() < exp(-(double)d / temp)) recolour(chosen, nc);
            iters++;
            if (cost < localBest) { localBest = cost; stall = 0; } else stall++;
            temp *= cool;
            if (temp < 0.05) temp = T0;               /* reheat */
            if ((iters & 0xFFFFF) == 0) elapsed = (double)(clock() - t0) / CLOCKS_PER_SEC;
        }
        if (best < 0 || cost < best) {
            best = cost;
            printf("  best cost %ld (iters %lld, %.1fs)\n", best, iters, elapsed);
            fflush(stdout);
        }
        if (cost == 0) break;
        elapsed = (double)(clock() - t0) / CLOCKS_PER_SEC;
    }

    printf("RESULT v=%d t=%d best_cost=%ld iters=%lld secs=%.1f\n", V, T_SIZE, best, iters, elapsed);
    if (cost == 0 && out) {
        FILE *f = fopen(out, "w");
        fprintf(f, "# LS(%d,%d,%d) colouring: one line per block, colex order\n", T_SIZE, T_SIZE + 1, V);
        int blk[16];
        for (int b = 0; b < NB; b++) {
            unrankSet(b, T_SIZE + 1, blk);
            for (int i = 0; i <= T_SIZE; i++) fprintf(f, "%d ", blk[i]);
            fprintf(f, "%d\n", colour[b]);
        }
        fclose(f);
        printf("WROTE %s\n", out);
    }
    return cost == 0 ? 0 : 1;
}

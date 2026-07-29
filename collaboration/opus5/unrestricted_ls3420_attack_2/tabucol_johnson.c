/* TabuCol / PartialCol search for a proper m-colouring of the Johnson graph
 * J(n, s)  (vertices = s-subsets of [n], adjacent iff they meet in s-1 points).
 *
 * With n = m + s - 2 and m odd, Theorem G1 of
 * collaboration/opus5/generic_radius4_certificate_attack/NOTE.md says
 *
 *     chi(J(n,s)) <= m   <=>   LS(s-1, s, n+1) exists,
 *
 * and the missing-colour map rebuilds the large set.  So this program searches
 * for the unrestricted object: no symmetry, no ansatz.
 *
 * This program only proposes colourings.  A separate deterministic Python
 * verifier decides whether an emitted colouring is genuine and lifts it.
 * A non-zero final cost is NOT evidence of non-existence.
 *
 * Usage: tabucol_johnson <n> <s> <m> <seed> <seconds> [outfile]
 */

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int N, S, M;
static int NV, DEG;
static int *adj;        /* NV * DEG */
static int *colour;     /* NV */
static int *gamma_;     /* NV * M */
static long conflicts;

static long *binom;
static long C(int n, int k) { return (k < 0 || k > n) ? 0 : binom[n * (N + 2) + k]; }

static void initBinom(void) {
    binom = calloc((size_t)(N + 2) * (N + 2), sizeof(long));
    for (int n = 0; n <= N + 1; n++) {
        binom[n * (N + 2)] = 1;
        for (int k = 1; k <= n; k++)
            binom[n * (N + 2) + k] = binom[(n - 1) * (N + 2) + k - 1] + binom[(n - 1) * (N + 2) + k];
    }
}
static long rankSet(const int *a, int k) {
    long r = 0;
    for (int i = 0; i < k; i++) r += C(a[i], i + 1);
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

static uint64_t st;
static inline uint64_t rnd64(void) { st ^= st << 13; st ^= st >> 7; st ^= st << 17; return st; }
static inline int ri(int n) { return (int)(rnd64() % (uint64_t)n); }

static void build(void) {
    NV = (int)C(N, S);
    DEG = S * (N - S);
    adj = malloc((size_t)NV * DEG * sizeof(int));
    int a[16], b[16];
    for (int v = 0; v < NV; v++) {
        unrankSet(v, S, a);
        int k = 0;
        for (int d = 0; d < S; d++) {
            for (int x = 0; x < N; x++) {
                int in = 0;
                for (int i = 0; i < S; i++) if (a[i] == x) in = 1;
                if (in) continue;
                int j = 0;
                for (int i = 0; i < S; i++) if (i != d) b[j++] = a[i];
                b[S - 1] = x;
                /* sort b (S elements) */
                for (int p = 1; p < S; p++) {
                    int t = b[p], q = p - 1;
                    while (q >= 0 && b[q] > t) { b[q + 1] = b[q]; q--; }
                    b[q + 1] = t;
                }
                adj[(size_t)v * DEG + k++] = (int)rankSet(b, S);
            }
        }
        if (k != DEG) { fprintf(stderr, "degree %d != %d\n", k, DEG); exit(1); }
    }
}

static void randomise(void) {
    memset(gamma_, 0, (size_t)NV * M * sizeof(int));
    for (int v = 0; v < NV; v++) colour[v] = ri(M);
    for (int v = 0; v < NV; v++)
        for (int i = 0; i < DEG; i++) gamma_[(size_t)adj[(size_t)v * DEG + i] * M + colour[v]]++;
    conflicts = 0;
    for (int v = 0; v < NV; v++) conflicts += gamma_[(size_t)v * M + colour[v]];
    conflicts /= 2;
}

static void setColour(int v, int c) {
    int o = colour[v];
    if (o == c) return;
    for (int i = 0; i < DEG; i++) {
        int u = adj[(size_t)v * DEG + i];
        gamma_[(size_t)u * M + o]--;
        gamma_[(size_t)u * M + c]++;
    }
    conflicts += gamma_[(size_t)v * M + c] - gamma_[(size_t)v * M + o];
    colour[v] = c;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: %s n s m seed seconds [out]\n", argv[0]); return 2; }
    N = atoi(argv[1]); S = atoi(argv[2]); M = atoi(argv[3]);
    st = strtoull(argv[4], NULL, 10) * 6364136223846793005ULL + 1442695040888963407ULL;
    double seconds = atof(argv[5]);
    const char *out = argc > 6 ? argv[6] : NULL;

    initBinom();
    build();
    colour = malloc((size_t)NV * sizeof(int));
    gamma_ = malloc((size_t)NV * M * sizeof(int));
    int *tabu = malloc((size_t)NV * M * sizeof(int));
    int *conf = malloc((size_t)NV * sizeof(int));

    printf("J(%d,%d) with %d colours: %d vertices, degree %d, class size %g\n",
           N, S, M, NV, DEG, (double)NV / M);
    fflush(stdout);

    clock_t t0 = clock();
    long best = -1;
    long long it = 0;
    double elapsed = 0;

    while (elapsed < seconds && best != 0) {
        randomise();
        memset(tabu, 0, (size_t)NV * M * sizeof(int));
        long localBest = conflicts;
        long long lastImp = 0, iter = 0;
        while (elapsed < seconds && conflicts > 0 && iter - lastImp < 400000) {
            int nc = 0;
            for (int v = 0; v < NV; v++) if (gamma_[(size_t)v * M + colour[v]] > 0) conf[nc++] = v;
            if (nc == 0) break;
            long bestDelta = 1L << 40;
            int bv = -1, bcCol = -1, ties = 0;
            for (int i = 0; i < nc; i++) {
                int v = conf[i];
                int cv = colour[v];
                int g0 = gamma_[(size_t)v * M + cv];
                for (int c = 0; c < M; c++) {
                    if (c == cv) continue;
                    long d = gamma_[(size_t)v * M + c] - g0;
                    int isTabu = tabu[(size_t)v * M + c] > iter;
                    if (isTabu && !(conflicts + d < localBest)) continue;
                    if (d < bestDelta) { bestDelta = d; bv = v; bcCol = c; ties = 1; }
                    else if (d == bestDelta && ri(++ties) == 0) { bv = v; bcCol = c; }
                }
            }
            if (bv < 0) { iter++; continue; }
            int oldc = colour[bv];
            setColour(bv, bcCol);
            tabu[(size_t)bv * M + oldc] = (int)(iter + 10 + ri(10) + (int)(0.6 * nc));
            iter++; it++;
            if (conflicts < localBest) { localBest = conflicts; lastImp = iter; }
            if ((it & 0x3FFF) == 0) elapsed = (double)(clock() - t0) / CLOCKS_PER_SEC;
        }
        if (best < 0 || conflicts < best) {
            best = conflicts;
            printf("  best conflicts %ld (%.1fs, %lld moves)\n", best, elapsed, it);
            fflush(stdout);
        }
        elapsed = (double)(clock() - t0) / CLOCKS_PER_SEC;
    }

    printf("RESULT J(%d,%d) m=%d best_conflicts=%ld moves=%lld secs=%.1f\n",
           N, S, M, best, it, elapsed);
    if (conflicts == 0 && out) {
        FILE *f = fopen(out, "w");
        fprintf(f, "# proper %d-colouring of J(%d,%d); one line per s-set in colex order\n", M, N, S);
        int a[16];
        for (int v = 0; v < NV; v++) {
            unrankSet(v, S, a);
            for (int i = 0; i < S; i++) fprintf(f, "%d ", a[i]);
            fprintf(f, "%d\n", colour[v]);
        }
        fclose(f);
        printf("WROTE %s\n", out);
    }
    return conflicts == 0 ? 0 : 1;
}

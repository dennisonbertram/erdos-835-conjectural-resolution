/* cbsearch.c -- class-B first-lift completion at n = 13, q = 17.
 *
 * Search driver only.  Nothing this program prints is evidence by itself:
 * every instance it reports is re-decided independently in Python by
 * verify_classB.py (a second complete DFS and a CDCL SAT solver), and every
 * completion is re-checked from the definition there.
 *
 * The DFS below is complete: "UNSAT" means the whole tree was searched.  The
 * node budget is only used to steer the search; a budget hit is reported as
 * BUDGET and is never treated as infeasibility.
 *
 * build: cc -O2 -o cbsearch cbsearch.c
 * run:   ./cbsearch random  SEED COUNT
 *        ./cbsearch anneal  SEED RESTARTS STEPS
 *        ./cbsearch profile SEED COUNT P      (P = index of m-profile 0..5)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

#ifndef N
#define N 13
#endif
#ifndef Q
#define Q 17
#endif
#define ROWR 5
#define FULLC ((1u << Q) - 1u)
#define FULLV ((1u << N) - 1u)

static inline int pc(uint32_t x) { return __builtin_popcount(x); }

/* ---------------- xoshiro-ish rng ---------------- */
static uint64_t rs;
static inline uint64_t rnd64(void) {
    rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs;
}
static inline int rndint(int n) { return (int)(rnd64() % (uint64_t)n); }
static inline double rnd01(void) { return (double)(rnd64() >> 11) / 9007199254740992.0; }

/* ---------------- complete DFS ---------------- */
static uint32_t avail[N];
static uint32_t openv[N];
static int8_t   asg[N][N];
static long     nodes, budget;
static int      nsol, capsol;
static int8_t   bestsol[N][N];

static int rec(void)
{
    if (++nodes > budget) return -2;               /* budget */
    /* ---- unit propagation ---- */
    int undoA[200], undoB[200], undoC[200], nundo = 0;
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
                    while (om) {
                        int b = __builtin_ctz(om); om &= om - 1;
                        if ((avail[b] >> c) & 1u) cand |= 1u << b;
                    }
                    if (!cand) { rv = 0; goto done; }
                    int k = pc(cand);
                    if (k == 1) { fa = a; fb = __builtin_ctz(cand); fc = c; break; }
                    if (k < bestcnt) { bestcnt = k; bkind = 1; bx = a; by = c; bmask = cand; }
                }
            }
        }
        if (fa < 0) {
            /* nothing forced */
            int allclosed = 1;
            for (int a = 0; a < N; a++) if (openv[a]) { allclosed = 0; break; }
            if (allclosed) {
                if (nsol == 0) memcpy(bestsol, asg, sizeof(asg));
                nsol++;
                rv = (nsol >= capsol);
                goto done;
            }
            if (bkind == 0) {
                int a = bx, b = by; uint32_t m = bmask;
                while (m) {
                    int c = __builtin_ctz(m); m &= m - 1;
                    avail[a] ^= 1u << c; avail[b] ^= 1u << c;
                    openv[a] &= ~(1u << b); openv[b] &= ~(1u << a);
                    asg[a][b] = asg[b][a] = (int8_t)c;
                    int r = rec();
                    avail[a] ^= 1u << c; avail[b] ^= 1u << c;
                    openv[a] |= 1u << b; openv[b] |= 1u << a;
                    asg[a][b] = asg[b][a] = -1;
                    if (r) { rv = r; goto done; }
                }
                rv = 0; goto done;
            } else {
                int a = bx, c = by; uint32_t m = bmask;
                while (m) {
                    int b = __builtin_ctz(m); m &= m - 1;
                    avail[a] ^= 1u << c; avail[b] ^= 1u << c;
                    openv[a] &= ~(1u << b); openv[b] &= ~(1u << a);
                    asg[a][b] = asg[b][a] = (int8_t)c;
                    int r = rec();
                    avail[a] ^= 1u << c; avail[b] ^= 1u << c;
                    openv[a] |= 1u << b; openv[b] |= 1u << a;
                    asg[a][b] = asg[b][a] = -1;
                    if (r) { rv = r; goto done; }
                }
                rv = 0; goto done;
            }
        }
        /* apply the forced assignment */
        avail[fa] ^= 1u << fc; avail[fb] ^= 1u << fc;
        openv[fa] &= ~(1u << fb); openv[fb] &= ~(1u << fa);
        asg[fa][fb] = asg[fb][fa] = (int8_t)fc;
        undoA[nundo] = fa; undoB[nundo] = fb; undoC[nundo] = fc; nundo++;
    }
done:
    for (int i = nundo - 1; i >= 0; i--) {
        int a = undoA[i], b = undoB[i], c = undoC[i];
        avail[a] ^= 1u << c; avail[b] ^= 1u << c;
        openv[a] |= 1u << b; openv[b] |= 1u << a;
        asg[a][b] = asg[b][a] = -1;
    }
    return rv;
}

/* returns 1 SAT, 0 UNSAT, -2 BUDGET */
static int solve(const uint32_t *forb, long bud, int cap)
{
    for (int a = 0; a < N; a++) {
        avail[a] = FULLC & ~forb[a];
        openv[a] = FULLV & ~(1u << a);
        for (int b = 0; b < N; b++) asg[a][b] = -1;
    }
    nodes = 0; budget = bud; nsol = 0; capsol = cap;
    int r = rec();
    if (r == -2) return -2;
    return nsol > 0 ? 1 : 0;
}

/* ---------------- randomised greedy (hardness proxy) ---------------- */
static int greedy_once(const uint32_t *forb)
{
    uint32_t av[N], op[N];
    for (int a = 0; a < N; a++) { av[a] = FULLC & ~forb[a]; op[a] = FULLV & ~(1u << a); }
    int left = N * (N - 1) / 2;
    while (left) {
        int fa = -1, fb = -1, fc = -1;
        int bestcnt = 1000, bkind = -1, bx = -1, by = -1; uint32_t bmask = 0;
        for (int a = 0; a < N && fa < 0; a++) {
            uint32_t om = op[a] & ~((1u << (a + 1)) - 1u);
            while (om) {
                int b = __builtin_ctz(om); om &= om - 1;
                uint32_t m = av[a] & av[b];
                if (!m) return 0;
                int c = pc(m);
                if (c == 1) { fa = a; fb = b; fc = __builtin_ctz(m); break; }
                if (c < bestcnt) { bestcnt = c; bkind = 0; bx = a; by = b; bmask = m; }
            }
        }
        if (fa < 0) {
            for (int a = 0; a < N && fa < 0; a++) {
                uint32_t m = av[a];
                while (m) {
                    int c = __builtin_ctz(m); m &= m - 1;
                    uint32_t cand = 0, om = op[a];
                    while (om) { int b = __builtin_ctz(om); om &= om - 1;
                                 if ((av[b] >> c) & 1u) cand |= 1u << b; }
                    if (!cand) return 0;
                    int k = pc(cand);
                    if (k == 1) { fa = a; fb = __builtin_ctz(cand); fc = c; break; }
                    if (k < bestcnt) { bestcnt = k; bkind = 1; bx = a; by = c; bmask = cand; }
                }
            }
        }
        if (fa < 0) {
            if (bkind < 0) return left == 0;
            if (bkind == 0) {
                int k = rndint(pc(bmask));
                uint32_t m = bmask; while (k--) m &= m - 1;
                fa = bx; fb = by; fc = __builtin_ctz(m);
            } else {
                int k = rndint(pc(bmask));
                uint32_t m = bmask; while (k--) m &= m - 1;
                fa = bx; fc = by; fb = __builtin_ctz(m);
            }
        }
        av[fa] ^= 1u << fc; av[fb] ^= 1u << fc;
        op[fa] &= ~(1u << fb); op[fb] &= ~(1u << fa);
        left--;
    }
    return 1;
}

static int hardness(const uint32_t *forb, int trials)
{
    int bad = 0;
    for (int i = 0; i < trials; i++) if (!greedy_once(forb)) bad++;
    return bad;
}

/* ---------------- class-B instances ---------------- */
static int PROFS[64][3];
static int NPROF = 0;
static void build_profiles(void)
{
    NPROF = 0;
    for (int n5 = 0; n5 <= Q; n5++) {
        int n3 = 2 * N - 2 - 2 * n5;
        int n1 = Q - n5 - n3;
        if (n3 < 0 || n1 < 0) continue;
        if (5 * n5 + 3 * n3 + n1 != 5 * N) continue;
        PROFS[NPROF][0] = n5; PROFS[NPROF][1] = n3; PROFS[NPROF][2] = n1; NPROF++;
    }
}

static int mcount(const uint32_t *forb, int c)
{
    int t = 0; for (int a = 0; a < N; a++) t += (forb[a] >> c) & 1u; return t;
}

static int gen_instance(uint32_t *forb, int p)
{
    int ms[Q], k = 0;
    for (int i = 0; i < PROFS[p][0]; i++) ms[k++] = 5;
    for (int i = 0; i < PROFS[p][1]; i++) ms[k++] = 3;
    for (int i = 0; i < PROFS[p][2]; i++) ms[k++] = 1;
    for (int i = Q - 1; i > 0; i--) { int j = rndint(i + 1); int t = ms[i]; ms[i] = ms[j]; ms[j] = t; }
    for (int att = 0; att < 200; att++) {
        int rowrem[N]; for (int a = 0; a < N; a++) rowrem[a] = 5;
        for (int a = 0; a < N; a++) forb[a] = 0;
        int order[Q]; for (int c = 0; c < Q; c++) order[c] = c;
        /* fill largest column first */
        for (int i = 0; i < Q; i++) for (int j = i + 1; j < Q; j++)
            if (ms[order[j]] > ms[order[i]]) { int t = order[i]; order[i] = order[j]; order[j] = t; }
        int ok = 1;
        for (int i = 0; i < Q; i++) {
            int c = order[i], need = ms[c];
            int cand[N], nc = 0;
            for (int a = 0; a < N; a++) if (rowrem[a] > 0) cand[nc++] = a;
            if (nc < need) { ok = 0; break; }
            for (int x = nc - 1; x > 0; x--) { int y = rndint(x + 1); int t = cand[x]; cand[x] = cand[y]; cand[y] = t; }
            for (int x = 0; x < nc; x++) for (int y = x + 1; y < nc; y++)
                if (rowrem[cand[y]] > rowrem[cand[x]]) { int t = cand[x]; cand[x] = cand[y]; cand[y] = t; }
            for (int x = 0; x < need; x++) { forb[cand[x]] |= 1u << c; rowrem[cand[x]]--; }
        }
        if (!ok) continue;
        int good = 1;
        for (int a = 0; a < N; a++) if (rowrem[a] != 0) good = 0;
        if (good) return 1;
    }
    return 0;
}

static int classB_ok(const uint32_t *forb)
{
    for (int a = 0; a < N; a++) if (pc(forb[a]) != 5) return 0;
    for (int c = 0; c < Q; c++) { int m = mcount(forb, c); if (m > 5 || m < 1 || (m & 1) == 0) return 0; }
    return 1;
}


/* ---- (BC): |X|*|W| <= sum_c rho_c^max, for disjoint X,W ---- */
static int bc_clean(const uint32_t *forb)
{
    uint32_t V[Q];
    for (int c = 0; c < Q; c++) {
        uint32_t m = 0;
        for (int a = 0; a < N; a++) if (!((forb[a] >> c) & 1u)) m |= 1u << a;
        V[c] = m;
    }
    for (uint32_t xm = 1; xm < (1u << N); xm++) {
        uint32_t rest = FULLV & ~xm;
        int x = pc(xm);
        for (uint32_t sub = rest; sub; sub = (sub - 1) & rest) {
            uint32_t wm = sub;
            int w = pc(wm), tot = 0;
            for (int c = 0; c < Q; c++) {
                int sX = pc(V[c] & xm), sW = pc(V[c] & wm);
                int z = pc(V[c]) - sX - sW;
                int hi = sX < sW ? sX : sW;
                if (z == 0 && ((sX - hi) & 1)) hi--;
                if (hi > 0) tot += hi;
            }
            if (tot < x * w) return 0;
        }
    }
    return 1;
}

/* one class-B preserving move */
static int move(uint32_t *forb)
{
    for (int att = 0; att < 80; att++) {
        int a = rndint(N), b = rndint(N);
        if (a == b) continue;
        if (rnd64() % 100 < 35) {           /* profile move: m_c += 2, m_c' -= 2 */
            uint32_t both_in = forb[a] & forb[b];
            uint32_t both_out = FULLC & ~(forb[a] | forb[b]);
            if (!both_in || !both_out) continue;
            int i = rndint(pc(both_in)); uint32_t m = both_in; while (i--) m &= m - 1;
            int cp = __builtin_ctz(m);
            i = rndint(pc(both_out)); m = both_out; while (i--) m &= m - 1;
            int c = __builtin_ctz(m);
            if (mcount(forb, c) + 2 > 5 || mcount(forb, cp) - 2 < 1) continue;
            forb[a] = (forb[a] & ~(1u << cp)) | (1u << c);
            forb[b] = (forb[b] & ~(1u << cp)) | (1u << c);
            return 1;
        }
        uint32_t ca = forb[a] & ~forb[b], cb = forb[b] & ~forb[a];
        if (!ca || !cb) continue;
        int i = rndint(pc(ca)); uint32_t m = ca; while (i--) m &= m - 1;
        int c = __builtin_ctz(m);
        i = rndint(pc(cb)); m = cb; while (i--) m &= m - 1;
        int cp = __builtin_ctz(m);
        forb[a] = (forb[a] & ~(1u << c)) | (1u << cp);
        forb[b] = (forb[b] & ~(1u << cp)) | (1u << c);
        return 1;
    }
    return 0;
}

static void emit(const char *tag, const uint32_t *forb)
{
    printf("CANDIDATE %s [", tag);
    for (int a = 0; a < N; a++) printf("%u%s", forb[a], a + 1 < N ? "," : "");
    printf("]\n"); fflush(stdout);
}

int main(int argc, char **argv)
{
    if (argc < 3) { fprintf(stderr, "usage: cbsearch mode seed ...\n"); return 1; }
    const char *mode = argv[1];
    build_profiles();
    rs = strtoull(argv[2], NULL, 10) * 2862933555777941757ull + 3037000493ull;
    for (int i = 0; i < 50; i++) rnd64();

    if (!strcmp(mode, "check")) {
        /* ./cbsearch check SEED cap m0,m1,...  -- decide one instance */
        int cap = atoi(argv[3]);
        uint32_t forb[N];
        char *tok = strtok(argv[4], ",");
        for (int a = 0; a < N; a++) { forb[a] = (uint32_t)strtoul(tok, NULL, 10); tok = strtok(NULL, ","); }
        int r = solve(forb, 100000000000L, cap);
        printf("verdict %s nsol %d nodes %ld\n", r == 1 ? "SAT" : (r == 0 ? "UNSAT" : "BUDGET"), nsol, nodes);
        if (nsol > 0) { printf("sol"); for (int a = 0; a < N; a++) for (int b = a+1; b < N; b++) printf(" %d", bestsol[a][b]); printf("\n"); }
        return 0;
    }
    if (!strcmp(mode, "hunt")) {
        /* find UNSAT class-B instances and report whether they are (BC)-clean */
        long count = atol(argv[3]);
        long sat = 0, unsat = 0, bud = 0, clean = 0;
        uint32_t forb[N];
        for (long it = 0; it < count; it++) {
            int p = rndint(NPROF);
            if (!gen_instance(forb, p)) { it--; continue; }
            int nm = rndint(800);
            for (int i = 0; i < nm; i++) move(forb);
            if (!classB_ok(forb)) { it--; continue; }
            int r = solve(forb, 200000000L, 1);
            if (r == 1) sat++;
            else if (r == -2) { bud++; emit("budget", forb); }
            else {
                unsat++;
                if (bc_clean(forb)) { clean++; emit("BCclean_UNSAT", forb); }
            }
        }
        printf("hunt N=%d seed=%s count=%ld SAT=%ld UNSAT=%ld BCcleanUNSAT=%ld BUDGET=%ld\n",
               N, argv[2], count, sat, unsat, clean, bud);
        return 0;
    }
    if (!strcmp(mode, "random") || !strcmp(mode, "profile")) {
        long count = atol(argv[3]);
        int fixed = !strcmp(mode, "profile") ? atoi(argv[4]) : -1;
        long sat = 0, unsat = 0, bud = 0;
        uint32_t forb[N];
        for (long it = 0; it < count; it++) {
            int p = fixed >= 0 ? fixed : rndint(NPROF);
            if (!gen_instance(forb, p)) { it--; continue; }
            int nm = rndint(800);
            for (int i = 0; i < nm; i++) move(forb);
            if (!classB_ok(forb)) { it--; continue; }
            int r = solve(forb, 20000000L, 1);
            if (r == 1) sat++;
            else if (r == 0) { unsat++; emit("random", forb); }
            else { bud++; emit("budget", forb); }
        }
        printf("random seed=%s count=%ld SAT=%ld UNSAT=%ld BUDGET=%ld\n",
               argv[2], count, sat, unsat, bud);
        return 0;
    }
    if (!strcmp(mode, "anneal2") || !strcmp(mode, "bchunt")) {
        /* anneal2: lexicographic objective (greedy-failure count, then DFS
           nodes to the first solution).  bchunt: same, but every move that
           leaves the (BC)-clean region is rejected, so any UNSAT instance
           found is automatically (BC)-clean.                              */
        int bcmode = !strcmp(mode, "bchunt");
        long restarts = atol(argv[3]);
        long steps = atol(argv[4]);
        const int TR = 40;
        const long NODECAP = 300000L;
        double bestscore = -1; long sat = 0, unsat = 0, bud = 0, tested = 0;
        uint32_t forb[N], cand[N], bestf[N];
        for (long r = 0; r < restarts; r++) {
            int p = rndint(NPROF);
            if (!gen_instance(forb, p)) { r--; continue; }
            if (bcmode && !bc_clean(forb)) { r--; continue; }
            double cur = hardness(forb, TR);
            for (long s = 0; s < steps; s++) {
                double T = 3.0 * pow(0.02 / 3.0, (double)s / (double)(steps > 1 ? steps - 1 : 1));
                memcpy(cand, forb, sizeof(forb));
                if (!move(cand)) continue;
                if (!classB_ok(cand)) continue;
                if (bcmode && !bc_clean(cand)) continue;
                double h = hardness(cand, TR);
                if (h >= TR) {
                    solve(cand, NODECAP, 1);
                    h = TR + (double)nodes / (double)NODECAP;
                }
                if (h >= cur || rnd01() < exp((h - cur) / T)) { memcpy(forb, cand, sizeof(forb)); cur = h; }
                if (cur > bestscore) { bestscore = cur; memcpy(bestf, forb, sizeof(forb)); }
                if (cur >= TR) {
                    tested++;
                    int v = solve(forb, 3000000000L, 1);
                    if (v == 1) sat++;
                    else if (v == 0) { unsat++; emit(bc_clean(forb) ? "BCclean_UNSAT" : "UNSAT", forb); }
                    else { bud++; emit("budget", forb); }
                }
            }
        }
        printf("%s N=%d seed=%s restarts=%ld steps=%ld bestscore=%.4f tested=%ld SAT=%ld UNSAT=%ld BUDGET=%ld\n",
               mode, N, argv[2], restarts, steps, bestscore, tested, sat, unsat, bud);
        if (bestscore >= 0) emit("hardest", bestf);
        return 0;
    }
    if (!strcmp(mode, "anneal")) {
        long restarts = atol(argv[3]);
        long steps = atol(argv[4]);
        int TR = 40;
        int globalbest = -1;
        long sat = 0, unsat = 0, bud = 0, tested = 0;
        uint32_t forb[N], cand[N], bestf[N];
        for (long r = 0; r < restarts; r++) {
            int p = rndint(NPROF);
            if (!gen_instance(forb, p)) { r--; continue; }
            int cur = hardness(forb, TR);
            for (long s = 0; s < steps; s++) {
                double T = 6.0 * pow(0.03 / 6.0, (double)s / (double)(steps > 1 ? steps - 1 : 1));
                memcpy(cand, forb, sizeof(forb));
                if (!move(cand)) continue;
                if (!classB_ok(cand)) continue;
                int h = hardness(cand, TR);
                if (h >= cur || rnd01() < exp((h - cur) / T)) { memcpy(forb, cand, sizeof(forb)); cur = h; }
                if (cur > globalbest) { globalbest = cur; memcpy(bestf, forb, sizeof(forb)); }
                if (cur >= TR) {
                    tested++;
                    int v = solve(forb, 200000000L, 1);
                    if (v == 1) sat++;
                    else if (v == 0) { unsat++; emit(bc_clean(forb) ? "BCclean_UNSAT" : "anneal", forb); }
                    else { bud++; emit("budget", forb); }
                }
            }
        }
        printf("anneal seed=%s restarts=%ld steps=%ld besthardness=%d/%d tested=%ld SAT=%ld UNSAT=%ld BUDGET=%ld\n",
               argv[2], restarts, steps, globalbest, TR, tested, sat, unsat, bud);
        if (globalbest >= 0) emit("hardest", bestf);
        return 0;
    }
    fprintf(stderr, "unknown mode\n");
    return 1;
}

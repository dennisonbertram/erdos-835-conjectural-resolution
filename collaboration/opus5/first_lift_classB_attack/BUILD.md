# Building the C engines

    cc -O2 -o cbsearch cbsearch.c -lm                  # (n,r) = (13,5)
    cc -O2 -DN=5  -DQ=9  -o cbsearch5  cbsearch.c -lm
    cc -O2 -DN=7  -DQ=11 -o cbsearch7  cbsearch.c -lm
    cc -O2 -DN=9  -DQ=13 -o cbsearch9  cbsearch.c -lm
    cc -O2 -DN=11 -DQ=15 -o cbsearch11 cbsearch.c -lm  # used by verify_classB.py
    cc -O2 -DN=13 -DQ=17 -o cbsearch13 cbsearch.c -lm

    cc -O2 -DN=<n> -DR=<r> -o g_<n>_<r> grid.c -lm     # general Pi(n,r) search
    cc -O3 -DN=<n> -DR=<r> -o exh_<n>_<r> exh.c        # general Pi(n,r) exhaustive
    cc -O3 -o twin5 twin5.c                            # size-5 twin family at n=13

`verify_classB.py` uses `cbsearch11` as an independent second complete solver
for the n = 11 certificate; if it is not built the verifier falls back to the
CDCL SAT solver and says so.

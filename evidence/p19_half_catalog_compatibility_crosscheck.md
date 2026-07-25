# Independent compatibility-mask cross-check

This is a second implementation check for the exact \(p=19\) paired
half-link search.  It does not replace the primary 210-anchor sweep and does
not enlarge that sweep's mathematical scope.

The primary implementation assigns the six outside-vertex states in a fixed
order and checks each newly exposed Schur entry directly.  The cross-check
source
[`p19_unrestricted_rank4_half_catalog_search_compatibility_crosscheck.cpp`](p19_unrestricted_rank4_half_catalog_search_compatibility_crosscheck.cpp)
instead:

1. represents every outside vertex's remaining states by an eight-bit mask;
2. chooses the unassigned vertex with the smallest remaining domain;
3. lazily computes a compatibility mask against each other vertex; and
4. propagates those masks before recursing.

The two programs share the field arithmetic, catalogue parser, Schur
reduction, and final witness verifier.  Thus this is an independent CSP
branching/propagation check, not a wholly independent reimplementation of
every layer.

The cross-check exhausts all \(396\cdot8!=15{,}966{,}720\)
factorization/magnitude jobs on four widely separated anchors:

```text
anchor 000 = [0,1,2,3]   wall_seconds=40.9336
anchor 084 = [1,2,3,4]   wall_seconds=240.997
anchor 137 = [1,6,7,9]   wall_seconds=106.546
anchor 209 = [6,7,8,9]   wall_seconds=110.677
```

Every log has both exact counters equal to \(15{,}966{,}720\) and ends

```text
NO WITNESS FOR THIS ANCHOR (complete)
```

The verifier
[`verify_p19_half_catalog_compatibility_crosscheck.py`](verify_p19_half_catalog_compatibility_crosscheck.py)
checks the source and catalogue hashes, anchor indices and vertices, all
counters, and all terminal markers.  Its output is:

```text
crosscheck_source_sha256=PASS
catalogue_sha256=PASS
completed_sample_anchors=4
total_crosscheck_jobs=63866880
compatibility_mask_crosscheck=PASS
```

The pinned SHA-256 values are:

```text
0cd7a6bf5fda3fb202810a3384ddd31c80709d798e1cf9f4403961bba777ec8a  p19_unrestricted_rank4_half_catalog_search_compatibility_crosscheck.cpp
226c5addbf5915c7a68023302c2eefc80cbe7cf243441f2fea68b8f263f7bc46  k10_one_factorizations_396.txt
```

Run the sample set with:

```bash
bash evidence/run_p19_half_catalog_compatibility_samples.sh \
  6 7200 0 84 137 209
python3 -B evidence/verify_p19_half_catalog_compatibility_crosscheck.py
```

An earlier eager-table prototype stopped at its wall guard after
\(7{,}839{,}151\) jobs and printed `NO WITNESS (heuristic only)`.  That log
is retained as `compat-anchor-000.txt` for transparency but is not read by
the verifier and is not evidence for a negative result.

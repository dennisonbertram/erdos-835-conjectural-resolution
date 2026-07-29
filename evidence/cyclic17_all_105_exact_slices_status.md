# All 105 cyclic prescribed-link slices are independently feasible

This is an exact partial result for the fixed Wallis-golf,
\(\mathbb Z_{17}\)-equivariant radius-five ansatz.  It is **not** a joint
radius-five layer and is **not** a solution of Erdős--Rosenfeld Problem
#835.

For every one of the \(\binom{15}{2}=105\) pairs of Wallis golf squares, a
bit-parallel Algorithm-X search found one translate from each of the forty
moving-triple orbits which decomposes exactly the 120 edges of
\[
K_{17}-(S_i^{-1}(0)\cup S_j^{-1}(0)).
\]
Thus all 105 prescribed-link cyclic \(LS(2,3,19)\) slices exist separately.
The complete batch took 352.7 aggregate solver-seconds, about 44 seconds of
wall time with eight workers.

The independent Python verifier checks directly, for every slice:

* forty selected moving triples, one from every cyclic orbit;
* no selected edge in either prescribed zero one-factor;
* every one of the 120 residual edges covered exactly once; and
* moving-point degree vector \((8,7,\ldots,7)\).

It then reconstructs all seventeen translated colour classes for every
slice and verifies directly that each is an \(STS(19)\), that the classes
are pairwise disjoint, and that they partition all triples.  This checks
all \(105\cdot17=1{,}785\) Steiner systems without trusting the search
program or a phase-sign convention.

## Certificates and scope

The first complete independently exact seed is
`cyclic17_all_105_exact_slices_certificate.json`, with SHA-256

```text
7ddb20ec2ab02cd2dd029276c6df75dd425d5c1588c7b58c659299311dc8cdc5
```

It has 3,802 shared-\(N\) collision pairs, 5,474 distinct phase slots out
of the required 8,400, and zero fully conflict-free cross groups.

Weighted exact-row coordinate descent preserves every slice exactly while
reducing cross collisions.  The checked-in search seed
`cyclic17_all_105_exact_slices_cross_seed.json`, with SHA-256

```text
640ad301772b3224b7466e43bec5c659455b08af58d3178260efbff7b1bbcabb
```

has 2,935 collision pairs and 5,928 distinct phase slots, but still zero of
600 fully conflict-free groups.  It is a heuristic gluing seed only.

The joint layer requires zero collision pairs, equivalently 8,400 distinct
phase slots.  Neither certificate reaches that condition.  In particular,
105 independent slice completions do not by themselves define the shared
\(N_{uv}\) table.

## Reproducible commands

```sh
c++ -std=c++17 -O3 -Wall -Wextra -pedantic \
  evidence/odd_graph_local_ball/search_radius5_golf_cyclic_slice_exact_cover.cpp \
  -o /tmp/search_radius5_golf_cyclic_slice_exact_cover

python3 -B \
  evidence/odd_graph_local_ball/generate_radius5_golf_cyclic_exact_slice_seed.py \
  /tmp/search_radius5_golf_cyclic_slice_exact_cover \
  /tmp/cyclic17-row-exact-seed.json \
  --workers 8 --seconds 30 --retries 8 --seed 857

python3 -B \
  evidence/odd_graph_local_ball/verify_radius5_golf_cyclic_exact_slice_seed.py \
  evidence/cyclic17_all_105_exact_slices_certificate.json

python3 -B \
  evidence/odd_graph_local_ball/verify_radius5_golf_cyclic_exact_slice_seed.py \
  evidence/cyclic17_all_105_exact_slices_cross_seed.json

python3 -B \
  evidence/odd_graph_local_ball/improve_radius5_golf_cyclic_exact_slices_dlx.py \
  /tmp/search_radius5_golf_cyclic_slice_exact_cover \
  evidence/cyclic17_all_105_exact_slices_certificate.json \
  /tmp/cyclic17-row-exact-cross-seed.json \
  --sweeps 1 --seconds-per-pair 2
```

The C++ solver's `UNKNOWN` status is only a resource-limited search result.
No infeasibility claim is made without a portable proof.

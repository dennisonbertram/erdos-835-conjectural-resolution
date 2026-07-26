# Fixed-Wallis centre-0 certificate bundle

This directory supports the narrow result stated in
[`../cyclic17_star_centre0_infeasibility.md`](../cyclic17_star_centre0_infeasibility.md):
the fixed-Wallis, translation-equivariant cyclic-17 ansatz has no completion.
It does **not** exclude other cyclic starters, non-equivariant constructions, or
solve Erdős–Rosenfeld Problem #835.

The load-bearing incompatible core uses only the six complete slice families
`sols_0_2.bin` through `sols_0_7.bin`. Each binary is a concatenation of
40-byte rows; byte `r` is the selected phase in moving-triple orbit `r`.

## Fast checks

From the repository root:

```sh
python3 evidence/cyclic17_star_centre0/verify_star_five_witnesses.py \
  evidence/cyclic17_star_centre0/families \
  evidence/cyclic17_star_centre0/erdos835-star-all-five-witnesses.jsonl

python3 evidence/cyclic17_star_centre0/verify_dual_enumerations.py
```

The first command semantically checks all 6,314 rows in the thirteen families
with outer labels 2 through 14 and checks all 1,287 explicit five-family
witnesses. The second compares the canonical files to an exhaustive traversal
with reversed column and row tie-breaking.

Regenerate the six-core CNF:

```sh
python3 evidence/cyclic17_star_centre0/emit_star_support_cnf.py \
  /tmp/erdos835-star-core.cnf \
  evidence/cyclic17_star_centre0/families/sols_0_2.bin \
  evidence/cyclic17_star_centre0/families/sols_0_3.bin \
  evidence/cyclic17_star_centre0/families/sols_0_4.bin \
  evidence/cyclic17_star_centre0/families/sols_0_5.bin \
  evidence/cyclic17_star_centre0/families/sols_0_6.bin \
  evidence/cyclic17_star_centre0/families/sols_0_7.bin

shasum -a 256 /tmp/erdos835-star-core.cnf
```

The expected SHA-256 is
`4cd5a9b81e06b5401a7f828c5801a431f95db1067c6cc20545a2aac3d5bb5cc3`.

To verify the portable UNSAT proof, decompress
`erdos835-star-core-2-7-support.drat.gz` and run a DRAT checker:

```sh
drat-trim \
  evidence/cyclic17_star_centre0/erdos835-star-core-2-7-support.cnf \
  /tmp/erdos835-star-core-2-7-support.drat
```

The uncompressed proof SHA-256 is
`0c3086e155fde25d3780b9acc3130cb31148e078537997a68ae31d29f1357e2f`.

## Rebuild the enumerations and census

Compile the exhaustive slice enumerator and run one core family:

```sh
c++ -O3 -std=c++17 \
  evidence/cyclic17_star_centre0/count_slice_solutions.cpp \
  -o /tmp/count_slice_solutions

/tmp/count_slice_solutions --pair 0,2 --cap 20000000 \
  --store /tmp/sols_0_2.bin --store-limit 500000
```

The corresponding reversed traversal adds `--alt`. Full runs take tens of
minutes per family on the reference machine. Recorded machine outputs are in
`enumeration_results/`.

Compile and rerun the subset census:

```sh
c++ -O3 -std=c++17 \
  evidence/cyclic17_star_centre0/erdos835-star-subset-census.cpp \
  -o /tmp/erdos835-star-subset-census

/tmp/erdos835-star-subset-census \
  evidence/cyclic17_star_centre0/families 6 \
  /tmp/five-family-witnesses.jsonl
```

The census checks all subsets through size six. It reports no incompatible
subset of size at most five, 1,712 incompatible six-subsets, and four compatible
six-subsets.

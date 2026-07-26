# Independent audit of the small-\(k\) certificate package

Audit date: 2026-07-26.

This audit checked the package independently of the archived solver summaries.
It does not establish a new value of \(k\) for Erdős–Rosenfeld Problem #835.

## Source and encoding review

`ball_defs.py`, `encode_cnf.py`, `solve_cpsat.py`, `solve_k4.py`,
`decode_and_verify.py`, and `control_k16.py` were read in full. The one-hot
CNF constraints in `encode_cnf.py` implement conditions 1--4 of
`../radius4_reduction.md` and the exact radius-5 extension condition in
`../radius5_reduction.md`. In particular, the combined exactly-one clauses
also force each set of three excluded colours to be distinct.

The three proof-bearing CNFs were regenerated and compared byte-for-byte:

```sh
python3 -B encode_cnf.py 4 4 /tmp/k4_r4.cnf
python3 -B encode_cnf.py 4 5 /tmp/k4_r5.cnf
python3 -B encode_cnf.py 6 5 /tmp/k6_r5.cnf
cmp /tmp/k4_r4.cnf k4_r4.cnf
cmp /tmp/k4_r5.cnf k4_r5.cnf
cmp /tmp/k6_r5.cnf k6_r5.cnf
```

All three comparisons returned zero. A full DIMACS scan gave:

| instance | variables | header clauses | scanned clauses | maximum variable |
|---|---:|---:|---:|---:|
| `k4_r4` | 228 | 1,896 | 1,896 | 228 |
| `k4_r5` | 288 | 3,018 | 3,018 | 288 |
| `k6_r5` | 3,155 | 48,200 | 48,200 | 3,155 |
| `k16_r4_wallisfix` | 248,640 | 6,850,440 | 6,850,440 | 248,640 |

Every clause ended in zero and no literal exceeded its declared variable
range.

## Proof rechecks

The checker was built from `marijnheule/drat-trim` source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; the audited binary had SHA-256
`42a69f9a17bcd58001676abf02d58992bd0ede58410a467dda07a350fec498c9`.
Fresh checks returned:

| proof | independent result | core data |
|---|---|---|
| `k4_r4.drat` | `s VERIFIED` | 32/242 lemmas, 395 resolution steps, 0 RAT |
| `k4_r5.drat` | `s VERIFIED` | 35/344 lemmas, 518 resolution steps, 0 RAT |
| decompressed `k6_r5.drat.gz` | `s VERIFIED` | 207,528/340,311 lemmas, 13,633,410 resolution steps, 0 RAT |

The decompressed \(k=6\) proof hash was
`df7b8b9d236472285c75bfed1a04236667d269c22148b0397ae7885560fcefc5`,
matching `SHA256SUMS`. As a rejection control, running the checker on
`k4_r4.cnf` with `/dev/null` as the proof returned `s NOT VERIFIED` and a
nonzero exit status.

## \(k=16\) positive control

The initially exported `k16_r4_wallisfix.cnf.gz` was truncated. Its
102,105,088-byte decompressed prefix agreed exactly with a fresh deterministic
generation, but the gzip stream had no valid end. The archive in this package
was replaced by the complete regenerated stream:

```sh
python3 -B encode_cnf.py 16 4 /tmp/k16_r4_wallisfix.cnf \
  --fix wallis_k16_LM_fix.json
gzip -n -9 -c /tmp/k16_r4_wallisfix.cnf \
  > k16_r4_wallisfix.cnf.gz
gzip -t k16_r4_wallisfix.cnf.gz
```

The repaired gzip is 21,387,535 bytes and has SHA-256
`7748a12204c1a6390d804c405101cbd50f4102cac6c49e6684e5134f7cdc2334`.
The archived CaDiCaL model assigns all 248,640 variables and directly
satisfies all 6,850,440 clauses in the regenerated fixed CNF. Decoding that
model produced a byte-identical copy of
`k16_r4_encoder_control_witness.json`, and the independent semantic checker
reported PASS.

`control_k16.py` was then rerun. It solved all 120 \(N\)-slices and its
independent radius-4 semantic check reported PASS. Its regenerated
`wallis_k16_radius4_witness.json` and `wallis_k16_LM_fix.json` were
byte-identical to the packaged files.

## Other checks and scope

The pure-Python exhaustive \(k=4\) solver independently returned 24 candidate
\(L\)-tables, zero \((L,M)\) pairs passing conditions 1--3, and UNSAT at both
radii 4 and 5. A targeted count also confirmed that no candidate \(L\)-table
admits condition 2 simultaneously in all three rows.

All six Python sources pass an AST parse. A case-insensitive scan for common
credential patterns found no secrets. The only absolute user path was removed
from `control_k16.py`; it now finds the repository evidence directory
relative to its own location.

After replacing the truncated control archive, `shasum -a 256 -c
SHA256SUMS` reports OK for every archived file listed there.

The certified conclusions are limited to the local exclusions at \(k=4\) and
\(k=6\), plus the positive radius-4 encoding control at \(k=16\). They do not
decide the full \(k=16\) problem or Erdős–Rosenfeld Problem #835.

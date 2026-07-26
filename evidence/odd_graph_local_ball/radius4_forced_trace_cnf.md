# Complete generic radius-4 CNF with forced radius-5 traces

`materialize_radius4_forced_trace_cnf.py` authenticates and augments the exact
canonical CNF from `generate_radius4_generic_sinz_cnf.py`.  The result contains
the complete unrestricted \(k=16\), radius-four \(O_{16}=KG(31,15)\) ball and
the 1,680 `AllDifferent(15)` constraints proved necessary by
`radius5_minimal_trace_forced.md`.

This is not a Wallis, cyclic, finite-field, Latin-square, algebraic, or other
construction ansatz.  It uses the existing canonical BFS vertex positions,
one-hot primary variables, and 32 symmetry-normalizing units.  The new
constraints are invariant under those normalizations.

## Trace coordinates

For each unordered pair of root points \(\{i,j\}\) and each moving point \(u\),
the trace consists of the fifteen sphere-four vertices

\[
  (R\setminus\{i,j\})\cup\{15+u,15+v\},
  \qquad v\in\{0,\ldots,15\}\setminus\{u\}.
\]

Their colours are the fifteen values \(N_{uv}(ij)\).  There are
\(\binom{15}{2}\cdot16=1{,}680\) such traces.  The materializer emits their
canonical positions in a separate trace map.  The independent verifier checks
that every listed vertex is in sphere four, every trace has 15 distinct
vertices, all 1,680 traces are distinct, and every one of the 12,600
sphere-four vertices occurs in exactly two traces.

## CNF encoding and exact dimensions

For each trace and each of the 17 colours, the parent one-hot primaries satisfy
at-most-one.  This is exactly the pairwise-disequality meaning of
`AllDifferent(15)`.

A direct encoding would add

\[
  1{,}680\cdot17\cdot\binom{15}{2}=2{,}998{,}800
\]

binary clauses.  The materialized certificate instead uses a standard
14-state Sinz sequential AMO for each of the \(1{,}680\cdot17=28{,}560\)
trace/colour instances.  Each instance has 14 auxiliary variables and 41
binary clauses.  The independent verifier exhaustively checks the projection
of this template against direct pairwise AMO for all \(2^{15}=32{,}768\)
primary assignments.

| item | count |
|---|---:|
| parent variables | 483,681 |
| parent clauses | 738,537 |
| forced traces | 1,680 |
| trace/colour AMO instances | 28,560 |
| added Sinz auxiliary variables | 399,840 |
| added Sinz binary clauses | 1,170,960 |
| **total variables** | **883,521** |
| **total clauses** | **1,909,497** |

The final clause-length distribution is 32 unit clauses, 1,859,839 binary
clauses, and 49,626 clauses of length 17.

## Pinned artifacts

The exact 37,303,238-byte CNF, 260,860-byte trace map, and manifest are checked
in under `radius4_forced_trace_cnf/`.  The live proof-logging run uses a
byte-identical copy under `/private/tmp`.

| artifact | SHA-256 |
|---|---|
| parent CNF | `0e66e3d7f4e15bd155db737092b8387b10540fd0e5bbcb56127c650baf6c54dc` |
| parent map | `ba4c9455a31907d3af5d58a143eaf2ce0a48517e2a26122f320cb71fcc3393e6` |
| parent manifest | `9c5fd2e89ea69d9dc607e2e7793962c35b9e7b45597977eb3c3e93445c88b4f2` |
| augmented CNF | `2eb2e0efba279655021e4c709b03148e3cea73d98e32c745637864ba177327d4` |
| trace map | `a99d8f0f55308260956e9008cb5f1e15b15fadaa5df1924baacba092ea5acfb2` |
| augmented manifest | `b0127a4f79faeab9227283d9b9bd11c1155f4f8b91b86ca08f929e2fe24e5b65` |

The materializer refuses any parent artifact whose bytes do not match all
three pinned parent hashes.  `verify_radius4_forced_trace_cnf.py` imports
neither generator: it independently reconstructs and byte-compares the parent
CNF, parent map, parent manifest, trace map, and complete augmented CNF stream,
then parses all 1,909,497 clauses and performs the semantic trace checks.

## Reproduce and verify

First reproduce the canonical parent:

```bash
python3 -B evidence/odd_graph_local_ball/generate_radius4_generic_sinz_cnf.py \
  --cnf /private/tmp/o16-r4-generic.cnf \
  --map /private/tmp/o16-r4-generic.map.json \
  --manifest /private/tmp/o16-r4-generic.manifest.json
```

Materialize the forced-trace instance:

```bash
python3 -B evidence/odd_graph_local_ball/materialize_radius4_forced_trace_cnf.py \
  --parent-cnf /private/tmp/o16-r4-generic.cnf \
  --parent-map /private/tmp/o16-r4-generic.map.json \
  --parent-manifest /private/tmp/o16-r4-generic.manifest.json \
  --cnf /private/tmp/o16-r4-forced-trace-sinz-v1.cnf \
  --trace-map /private/tmp/o16-r4-forced-trace-sinz-v1.trace-map.json \
  --manifest /private/tmp/o16-r4-forced-trace-sinz-v1.manifest.json
```

Run the independent audit:

```bash
python3 -B evidence/odd_graph_local_ball/verify_radius4_forced_trace_cnf.py \
  --parent-cnf /private/tmp/o16-r4-generic.cnf \
  --parent-map /private/tmp/o16-r4-generic.map.json \
  --parent-manifest /private/tmp/o16-r4-generic.manifest.json \
  --cnf evidence/odd_graph_local_ball/radius4_forced_trace_cnf/instance.cnf \
  --trace-map evidence/odd_graph_local_ball/radius4_forced_trace_cnf/trace_map.json \
  --manifest evidence/odd_graph_local_ball/radius4_forced_trace_cnf/manifest.json
```

That audit returned `PASS` for the hashes and counts above.  After verification,
a deliberately bounded five-second CaDiCaL 3.0.1 probe returned `UNKNOWN`:

```bash
cadical -t 5 -q /private/tmp/o16-r4-forced-trace-sinz-v1.cnf
```

No satisfiability conclusion is drawn from that probe.

## Exact scope

An independently checked **UNSAT proof would exclude \(k=16\) only**: it would
rule out a radius-five extension at this \(k\), and hence a global \(k=16\)
cover.  An UNSAT claim requires retaining the exact CNF, solver/version/command,
complete proof, and an independent proof-checker result.

A **SAT result is only a necessary local witness** for radius four plus the
forced-trace consequence.  It is not a complete radius-five ball and not a
global colouring.  A SAT claim requires a complete model decoded back to the
canonical vertex colours and independently checked against every CNF clause and
all 1,680 semantic traces.

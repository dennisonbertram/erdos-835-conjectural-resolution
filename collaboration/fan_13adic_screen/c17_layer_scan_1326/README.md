# Bounded layer scan of all 1,326 mixed branches

## Status and exact scope

This directory records **bounded solver telemetry**, not an
unsatisfiability proof.

Every one of the 1,326 type-\((L,\infty)\) mixed branches was tested on
both 40-row fixed-point layers.  The 2,652 layer-instance outcomes are:

- 167 `SAT` witnesses;
- 2,485 `UNKNOWN` outcomes;
- 0 certified layer-level `UNSAT` outcomes.

Here `UNKNOWN` includes every timeout.  It must not be read as
unsatisfiable.

The SAT witnesses occur on 142 branches.  A 60-second compatibility pass
on those branches found 19 explicit compatible 88-row prefixes in total
(including seven prefixes found before the uniform pass).  CaDiCaL
returned `UNSATISFIABLE` on the induced finite stage for all 19.  These
nineteen outcomes are recorded as `UNSATISFIABLE_TELEMETRY`; only the first
branch-0 prefix has a separately checked proof, in
`../branch0_prefix1_refutation/`.

No 228-row exact cover was found.  Nothing here excludes a different
prefix, the fixed-link \(C_{17}\)-equivariant ansatz, \(LS(3,4,20)\), a
simultaneous thirteen-fan, or Erdős--Rosenfeld Problem #835.

## Configuration

Solver: CaDiCaL 3.0.1, exact pairwise exact-one CNFs.

- Branches 2--41: 30 seconds per layer instance.
- Branches 42--1325: 10 seconds per layer instance.
- Branches 0--1: retained prior layer runs, identified by `source` in the
  manifest.
- Compatible partner search: 60 seconds per hit branch, with the anchor
  layer's 40 finite demands forbidden by unit clauses.
- Finite-only completion: 300 seconds, although every recorded instance
  terminated with solver status 20 before the limit.
- Parallel scan/compatibility workers: 24 for the uniform passes.

`scan_manifest.csv` has one row for every branch/fixed-point pair, including
the exact status, wall limit, source, and SHA-256 of the solver result file.
`compatible_prefixes.json` records all 19 exact row sets and the dimensions
and SHA-256 of each reconstructed finite CNF. `RUN_RECEIPT.json` authenticates
both manifests and gives the aggregate census.

## Verification and replay

Verify the manifests, the \(8+40+40+140\) decomposition, all 19 compatible
prefixes, and every finite CNF hash:

```text
python3 -B verify_scan_telemetry.py
```

To reconstruct the 19 finite CNFs for independent bounded reruns:

```text
python3 -B verify_scan_telemetry.py --emit-finite-cnfs /tmp/c17-finite
cadical -q -t 300 -w /tmp/result.witness \
  /tmp/c17-finite/branch-0000-prefix-01.cnf
```

The proof-bearing version of that first prefix is intentionally kept in
the separate `../branch0_prefix1_refutation/` package.

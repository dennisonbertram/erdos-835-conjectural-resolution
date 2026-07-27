# Finite-first packing witness of size 132

This package records an exact collision-free packing of 132 finite
quadruple-orbit rows in the `C17` fixed-link quotient used by the search for
Erdos-Rosenfeld problem 835.

The semantic checker reconstructs the quotient exact-cover matrix from the
audited fixed cyclic `LS(2,3,19)`.  It verifies that:

- there are 140 finite quadruple orbits and 640 finite triple-colour demands;
- every recorded row belongs to a different finite quadruple orbit;
- every recorded row uses four finite triple-colour demands;
- all `132 + 4*132 = 660` covered columns are distinct.

Therefore this package proves only

`alpha_finite >= 132`.

The trivial upper bound is `alpha_finite <= 140`.  Neither the equality
`alpha_finite = 140` nor a full `C17`-equivariant extension is proved.

## Omit-one telemetry

`omit_one_manifest.csv` records a bounded SAT search for a packing of size
139, once for each possible omitted finite quadruple orbit.  Each of the 140
runs used CaDiCaL's SAT-oriented mode, seed `13001 + omitted_q`, and a
30-second wall-clock limit.  Every run returned `UNKNOWN`.

The checker deterministically reconstructs all 140 CNFs and checks their
SHA-256 digests.  The recorded timeout outcomes are telemetry, not proof:
`UNKNOWN` cannot be used to infer `alpha_finite < 139`.

## Exact 302,743-neighborhood search

`near_assignment_score10.json` records a complete 140-orbit assignment with
10 finite-demand collisions.  Its conflict graph has 10 edges on 18 bad rows,
leaving 122 conflict-free rows.

`verify_neighborhood_302743.py` performs two exact local searches:

- It enumerates all 64 minimum vertex covers of size 8 in the conflict graph,
  then exactly tries to refill each resulting 132-row packing.
- It removes all 18 bad rows, additionally removes every subset of one, two,
  or three of the 122 good rows, and exactly reassigns every removed
  quadruple orbit.  This comprises
  `C(122,1) + C(122,2) + C(122,3) = 302,743` neighborhoods.

No completion exists in either local family.  This excludes only the
precisely defined neighborhood of the recorded assignment.  It does not prove
`alpha_finite < 140`, exclude the complete `C17` ansatz, or solve problem 835.

## Verify

From the repository root:

```sh
/opt/homebrew/bin/python3 \
  collaboration/fan_13adic_screen/finite_first_packing_132/verify_finite_packing_132.py
```

Replay the exact neighborhood exhaustion:

```sh
/opt/homebrew/bin/python3 \
  collaboration/fan_13adic_screen/finite_first_packing_132/verify_neighborhood_302743.py
```

Expected final scope line:

```text
scope: alpha_finite >= 132 only; upper bound remains the trivial 140
```

## Files

- `packing.json`: exact 132-row witness and its deliberately narrow claim.
- `omit_one_manifest.csv`: reproducible CNF digests and bounded-run outcomes.
- `near_assignment_score10.json`: exact starting assignment for the local
  search.
- `RUN_RECEIPT.json`: package hashes and aggregate counts.
- `RUN_LOG.txt`: commands, exact counters, and scope delimiters.
- `verify_finite_packing_132.py`: independent semantic and reconstruction
  checker.
- `verify_neighborhood_302743.py`: deterministic exact neighborhood search.

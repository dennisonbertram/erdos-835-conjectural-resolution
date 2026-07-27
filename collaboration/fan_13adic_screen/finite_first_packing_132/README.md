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

## Verify

From the repository root:

```sh
/opt/homebrew/bin/python3 \
  collaboration/fan_13adic_screen/finite_first_packing_132/verify_finite_packing_132.py
```

Expected final scope line:

```text
scope: alpha_finite >= 132 only; upper bound remains the trivial 140
```

## Files

- `packing.json`: exact 132-row witness and its deliberately narrow claim.
- `omit_one_manifest.csv`: reproducible CNF digests and bounded-run outcomes.
- `RUN_RECEIPT.json`: package hashes and aggregate counts.
- `verify_finite_packing_132.py`: independent semantic and reconstruction
  checker.


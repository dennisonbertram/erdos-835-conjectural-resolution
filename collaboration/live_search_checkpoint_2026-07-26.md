# Live search checkpoint — 26 July 2026

Recorded at approximately 15:15 EDT.  This is an operational checkpoint, not
a mathematical result.  None of the searches below had reported SAT,
UNSAT, FEASIBLE, or INFEASIBLE at the checkpoint.

## Active searches

- Complete \(LS(3,4,20)\) parent CNF under CaDiCaL with proof logging,
  seed 836.  Its incomplete DRAT stream was about 6.9 GB.
- Authenticated even branch 0 of the \(LS(3,4,20)\) second-star split under
  Kissat.
- The same branch 0 under CP-SAT, seeded with the exact 4,773-assignment
  Etzion--Hartman partial.
- Complete unrestricted radius-four ball with all forced radius-five traces
  under integer CP-SAT.
- Complete generic radius-five CNF under CaDiCaL, without proof logging.
- Wallis shared-\(N\), forced-trace CP-SAT search with the audited
  congruence hint.

## Stopped proof stream

The complete radius-four-plus-forced-trace CaDiCaL proof logger (seed 840)
was interrupted with `SIGINT` after about 2 hours 43 minutes of wall time.
Its incomplete DRAT stream was about 8.1 GB and its solver log ended with
`exit 0` followed by `raising signal 2 (SIGINT)`.  It produced no verdict.

The local stream was preserved, but it is intentionally not checked into
Git: an interrupted DRAT prefix is not a certificate, and committing more
than 8 GB of non-verifying data would impair the public research repository.
The logger was stopped when free disk reached 52 GB; the independent
radius-four CP-SAT search remained active.

## Lossless preservation update

At approximately 15:42 EDT, the stopped radius-four DRAT prefix was
losslessly compressed to
`/private/tmp/o16-r4-forced-trace-sinz-v1-seed840.drat.gz`.  The compressed
file is about 1.2 GB.  `gzip -t` passed, and hashing the decompressed byte
stream reproduced the pre-compression SHA-256

```text
7afe544065dbb93d6871a03ba0c7e573be819e28e586ebb094a82ea9ec5823fb
```

Thus the incomplete stream remains exactly recoverable while releasing
roughly 7 GB for the surviving proof-producing search.  It remains
non-certificate evidence and is not suitable for GitHub because of its size.
At this update the live \(LS(3,4,20)\) DRAT prefix was about 7.9 GB and had
still produced no verdict.

The same preservation procedure was then applied to the stopped
`cyclic17-vertex-degree-reduced-seed835.drat` prefix.  Its compressed
3.1 GB stream passed `gzip -t`, and the decompressed bytes reproduced the
pre-compression SHA-256

```text
ec45f8ec696597a458a59bbe489263fed84e7ae4970d4421cf7902c6741f48d9
```

That stopped run had no SAT/UNSAT line and is likewise not a certificate.
After this second lossless compression, free disk was 61 GB.  The live
\(LS(3,4,20)\) prefix had reached about 8.8 GB without a verdict.

## Interpretation

An eventual SAT witness from the complete \(LS(3,4,20)\) parent would solve
that necessary derived-design problem, not Erdős--Rosenfeld #835.  An UNSAT
certificate would exclude \(k=16\), not every other possible prime
parameter.  A fully verified global Odd-graph colouring or an unrestricted
all-parameter theorem is still required to resolve Problem #835.

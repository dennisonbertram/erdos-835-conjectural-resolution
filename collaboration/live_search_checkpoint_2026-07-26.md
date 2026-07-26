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

## Interpretation

An eventual SAT witness from the complete \(LS(3,4,20)\) parent would solve
that necessary derived-design problem, not Erdős--Rosenfeld #835.  An UNSAT
certificate would exclude \(k=16\), not every other possible prime
parameter.  A fully verified global Odd-graph colouring or an unrestricted
all-parameter theorem is still required to resolve Problem #835.

# Live search checkpoint — 26 July 2026

Recorded at approximately 15:15 EDT.  This is an operational checkpoint, not
a mathematical result.  None of the searches below had reported SAT,
UNSAT, FEASIBLE, or INFEASIBLE at the checkpoint.

## Active searches

- Complete \(LS(3,4,20)\) parent CNF under CaDiCaL with proof logging,
  seed 836.  Its incomplete DRAT stream was about 6.9 GB at the initial
  checkpoint; this logger was later stopped for disk safety as recorded
  below.
- Authenticated even branch 0 of the \(LS(3,4,20)\) second-star split under
  Kissat.
- The same branch 0 under CP-SAT, seeded with the exact 4,773-assignment
  Etzion--Hartman partial.
- Complete unrestricted radius-four ball with all forced radius-five traces
  under integer CP-SAT (this later reached its limit with `UNKNOWN`; see
  below).
- Complete generic radius-five CNF under CaDiCaL, without proof logging.
- Wallis shared-\(N\), forced-trace CP-SAT search with the audited
  congruence hint.

## Six-hour unrestricted radius-four result

The complete unrestricted radius-four integer model with all 1,680 forced
radius-five traces reached its configured six-hour limit and returned
`UNKNOWN`, not `FEASIBLE` or `INFEASIBLE`.  The exact log records:

```text
vertices: 14,657
constrained centres: 2,057
radius-five trace constraints: 1,680
branches: 8,204,609
conflicts: 693
wall time: 21,602.762527 seconds
status: UNKNOWN
```

No witness/certificate file was written.  This run therefore changes no
mathematical status: it neither constructs the required local cover nor
excludes \(k=16\).

## Unrestricted radius-four Kissat reconnaissance

After the CP-SAT run released a CPU, the same complete radius-four ball with
all 1,680 forced traces was encoded as a deterministic Sinz CNF and launched
under Kissat with seed 844 and a six-hour time limit.  The DIMACS header is

```text
p cnf 883521 1909497
```

and the exact CNF SHA-256 is

```text
2eb2e0efba279655021e4c709b03148e3cea73d98e32c745637864ba177327d4
```

At the approximately 18:09 EDT update the solver was still running and had
printed no `SATISFIABLE` or `UNSATISFIABLE` verdict.  This reconnaissance run
does not log a proof: a SAT result would provide a local witness, while an
UNSAT line by itself would require a separate proof-producing rerun before it
could serve as a publication certificate.

## Stopped \(LS(3,4,20)\) proof stream

At approximately 17:56 EDT, free disk had fallen to 40 GB while the complete
\(LS(3,4,20)\) parent proof logger was still growing.  It was interrupted
with `SIGINT` after 24,284.77 seconds of real time and 3,489.70 seconds of
process time.  Its log ends with `exit 0` followed by
`raising signal 2 (SIGINT)` and contains no solver verdict.

The approximately 14 GB incomplete DRAT stream had SHA-256

```text
2dccb6fd267680004a172855a0d674523c541781a4588b5151a73f5d1914575a
```

It was losslessly compressed to the 2.8 GB local file
`/private/tmp/ls-3-4-20-seed836.drat.gz`.  `gzip -t` passed, and hashing the
decompressed byte stream reproduced the same SHA-256.  Free disk returned
to 61 GB.  The stream is preserved locally but is not a proof certificate
and is intentionally excluded from GitHub.  The independent
\(LS(3,4,20)\) branch-0 Kissat and CP-SAT searches, generic radius-five
CaDiCaL search, Wallis CP-SAT search, and radius-four Kissat search remained
active without a verdict.

## Stopped radius-four proof stream

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

## Later terminal and live updates

The Wallis shared-\(N\), forced-trace CP-SAT run reached its configured
six-hour limit and returned `UNKNOWN`.  Its exact terminal JSON was:

```json
{
  "branches": 1262701750,
  "conflicts": 45686786,
  "forced_trace_stars": 1680,
  "golf_sha256": "e419aad73c4275a29702db282ea2378357435b330312bde8fed0c7829be3f857",
  "hint_audited_n": true,
  "hinted_values": 12600,
  "schema": "odd-graph-o16-radius5-fixed-golf-n-forced-trace-v2",
  "status": "UNKNOWN",
  "triangle_congruence_literals": 0,
  "wall_time_seconds": 21601.932101000002
}
```

The authenticated \(LS(3,4,20)\) branch-0 Kissat run also terminated
`UNKNOWN`, after 6,323.95 seconds of process time, 59,996,510 conflicts,
422,486,886 decisions, and 30,551,090,317 propagations.  It emitted no
witness or proof.

The parallel branch-0 CP-SAT log contains only its startup and presolve
header.  Its session ended without a durable terminal response in that log,
so it has no recordable solver verdict and no mathematical status.

At 21:10 EDT two independent searches were still live:

- the complete radius-four-plus-forced-traces Kissat run, at about
  8,438 seconds of process time and with no terminal verdict; and
- the complete generic radius-five CaDiCaL run, at about 11,523 seconds of
  process time and with no terminal verdict.

These are operational facts only.  Every terminal result in this section is
either `UNKNOWN` or absent; none changes the mathematical status.

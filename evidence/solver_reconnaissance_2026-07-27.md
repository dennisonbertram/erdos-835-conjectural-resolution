# Solver reconnaissance checkpoint

Date: 2026-07-27 (America/New_York).

This file records operational solver evidence only.  An `UNKNOWN` result, an
unfinished search, a node count, a proof-file size, or a solver's internal
"variables remaining" statistic is **not** mathematical evidence for
existence or nonexistence.

## Completed unrestricted radius-four-plus-forced-trace CP-SAT run

The model was the unrestricted Boolean formulation implemented by
`evidence/odd_graph_local_ball/search_local_cover.py` with:

- radius \(4\);
- the lossless `--radius5-trace-only` necessary constraints enabled;
- \(14{,}657\) ball vertices;
- \(2{,}057\) constrained closed-neighbourhood centres; and
- \(28{,}560\) Boolean trace constraints (the \(1{,}680\) forced traces,
  expanded over \(17\) colours).

After a one-hour limit it returned:

```text
status: UNKNOWN
wall_time_seconds: 3600.932224
branches: 51,950,141
conflicts: 14,464,614
```

This is inconclusive.  CP-SAT emitted neither a colouring nor a portable
infeasibility certificate.

## Concurrent exact searches at this checkpoint

The following independent searches were still running:

| track | latest observable state |
|---|---|
| proof-producing CaDiCaL, unrestricted radius-four-plus-forced-trace CNF | no verdict; raw DRAT stream `/private/tmp/erdos835-r4-forcedtrace.drat` was 6.3 GiB |
| proof-producing CaDiCaL, \(C_{17}\)-equivariant cover CNF | no verdict; raw DRAT stream `/private/tmp/erdos835-c17-cover.drat` was 6.8 GiB |
| proof-producing CaDiCaL, fixed full cyclic-link \(LS(3,4,20)\) instance | no verdict |
| SAT-tuned CaDiCaL, unrestricted radius-four-plus-forced-trace CNF | no verdict; solver reported 33% of variables remaining |
| SAT-tuned CaDiCaL, \(C_{17}\)-equivariant cover CNF | no verdict; solver reported 76% of variables remaining |
| independent C++ Algorithm X/DLX, \(C_{17}\)-equivariant exact cover | no verdict after more than 585 million nodes |

The two raw DRAT files are live temporary streams, not repository artifacts.
They cannot be checked, compressed, hashed, or interpreted until their
respective solvers terminate.  At the snapshot above, the data volume had
99 GiB of free space.

## Verdict discipline

- A satisfying result must be extracted and checked by the independent
  semantic verifier before it counts as a construction.
- An unsatisfying CaDiCaL result must finish its proof stream and pass an
  independent proof checker before it counts as a restricted or unrestricted
  nonexistence theorem.
- Even a certified negative answer for the \(k=16\) instance would not by
  itself settle the existential quantifier in Erdős–Rosenfeld #835.

At this checkpoint every listed exact search remains undecided.

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

## Other exact-search status at the final checkpoint

No live solver session survived to the final snapshot.  The following
independent tracks terminated, were stopped for disk safety, or disappeared
with the tmux server without leaving a verdict:

| track | latest observable state |
|---|---|
| proof-producing CaDiCaL, unrestricted radius-four-plus-forced-trace CNF | manually interrupted without verdict when its partial DRAT reached 27,201,167,360 bytes and free disk space fell to 39 GiB |
| proof-producing CaDiCaL, \(C_{17}\)-equivariant cover CNF | manually interrupted without verdict when its partial DRAT reached 19,750,801,980 bytes, to preserve space for the unrestricted run |
| Kissat, fixed full cyclic-link \(LS(3,4,20)\) instance | no verdict retained; its tmux session later disappeared |
| SAT-tuned Kissat, unrestricted radius-four-plus-forced-trace CNF | no verdict retained; its last visible progress statistic reported 33% of variables remaining |
| SAT-tuned Kissat, \(C_{17}\)-equivariant cover CNF | no verdict retained; its last visible progress statistic reported 76% of variables remaining |
| independent C++ Algorithm X/DLX, \(C_{17}\)-equivariant exact cover | terminated at its time limit with `UNKNOWN` after 656,759,808 nodes |
| complete 56-way second-star sweep for \(J(15,4)\) with 900 seconds per branch | all 56 branches returned `UNKNOWN(exit 0)`; complete structured ledger retained |
| unbranched \(J(19,4)\) CaDiCaL attempt | retained only `c UNKNOWN`; no model or verdict |

An interrupted DRAT stream is not a proof and cannot be repaired into one by
hashing or preserving a prefix.  Both temporary DRAT files subsequently
disappeared together with the tmux server; at the final inspection
`/private/tmp` had 407 GiB free.  No conclusion is drawn from that external
cleanup or restart.

## Verdict discipline

- A satisfying result must be extracted and checked by the independent
  semantic verifier before it counts as a construction.
- An unsatisfying CaDiCaL result must finish its proof stream and pass an
  independent proof checker before it counts as a restricted or unrestricted
  nonexistence theorem.
- Even a certified negative answer for the \(k=16\) instance would not by
  itself settle the existential quantifier in Erdős–Rosenfeld #835.

At this checkpoint every listed track remains undecided.  The completed DLX
and 56-branch sweeps are still `UNKNOWN`: their node counts, full branch
coverage, and timeouts carry no mathematical verdict.

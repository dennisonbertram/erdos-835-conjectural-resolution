# Exhaustive \(k=4\) top-rung premise control

Date: 2026-07-29

## Question tested

The \(k=16\) conflict-cohomology reduction starts from \(k-1\) pairwise
disjoint \(S(k-1,k,2k)\)'s and asks whether their union supports an odd
unitrade. The unique weight-\(2k+1=9\) unitrade at \(k=4\) is the
\(3\)-by-\(3\) product \(W_2\times W_2\). This control asked whether every
three-system \(S(3,4,8)\) partial already contains that pattern.

## Result

The premise is empty at \(k=4\). There are 30 labelled \(S(3,4,8)\)'s,
forming 120 disjoint pairs, but there is no triple of pairwise block-disjoint
systems. Thus no \(k-1=3\) top partial exists on which to test the
common-odd-transversal theorem.

The verifier independently:

1. constructs the affine \(S(3,4,8)\);
2. generates all 30 labelled copies under \(S_8\);
3. verifies every triple occurs once and complement closure holds;
4. exhausts all \(\binom{30}{3}\) candidate system triples;
5. constructs and parity-checks all 280 labelled
   \(W_2\times W_2\) nine-block unitrades.

Run:

```sh
/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3 -B \
  collaboration/independent/top_rung_k4_control_2026-07-29/\
verify_top_k4.py

ruff check \
  collaboration/independent/top_rung_k4_control_2026-07-29/\
verify_top_k4.py
```

The output is:

```text
labelled S(3,4,8) systems: 30
disjoint system pairs: 120
pairwise-disjoint three-system partials: 0
partials with a common odd transversal: 0
classified 9-block product unitrades: 280
RESULT: PASS
```

## Scope

This is a negative strategy control, not progress on the unrestricted first
open case. It explains why the \(k=4\) product unitrade cannot be used as
evidence for a universal \(k=16\) top-rung pattern: the required \(k=4\)
partial family does not exist. Erdős--Rosenfeld #835 remains open.

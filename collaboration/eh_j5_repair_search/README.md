# Five-colour repair search above twelve Etzion--Hartman systems

## Exact reduction and scope

The authenticated Etzion--Hartman construction in
`evidence/ls_3_4_20_eh15_seed.txt` contains fifteen pairwise disjoint
SQS(20)s, labelled `0,...,14`.  Retain twelve and drop a triple \(D\) of
systems.  The unused blocks are the three dropped systems plus the original
570-block leave, hence there are

\[
3\cdot285+570=1425=5\cdot285
\]

leave blocks.  Above each of the \(\binom{20}{3}=1140\) triples there are
exactly five leave extensions.  Thus completing the retained twelve systems
to an \(LS(3,4,20)\) is exactly the problem of properly five-colouring this
leave graph.  Each colour class of such a colouring is automatically an
SQS(20).

This is a shadow construction related to Erdős--Rosenfeld Problem #835.  Even
an \(LS(3,4,20)\) witness would not settle #835, whose first open case is the
different large set \(LS(14,15,31)\).  Conversely, a failed search for these
455 particular retained twelve-system cores proves no general
nonexistence theorem.

## Programs

`search_eh_j5_repair.py`:

* authenticates the full seed and the 72-hole proper partial by SHA-256;
* independently checks all fifteen source SQS(20)s;
* constructs the 1,425-vertex five-fold leave for each dropped triple;
* adds the 1,140 exact five-colour constraints;
* fixes only global colour-label symmetry at the `(0,1,2)` triple;
* uses the proper 1,353-block part of the 72-hole seed as an advisory hint;
* limits each CP-SAT run to at most two workers;
* records solver reconnaissance as JSON Lines; and
* writes a complete witness if CP-SAT reports `FEASIBLE` or `OPTIMAL`.

`verify_eh_j5_witness.py` is deliberately independent of OR-Tools and of the
search program.  It authenticates the source, checks the twelve retained
systems, all 1,140 rainbow triple stars, every class size, and all seventeen
SQS properties.

CP-SAT `INFEASIBLE` is not a portable certificate here.  `UNKNOWN` proves
nothing.  Only a witness accepted by the independent verifier is an exact
positive result.

The source-label convention is exact.  Labels `0,...,14` in the authenticated
full seed are the fifteen complete EH systems.  Labels `15,16` are only the
two sides of a balanced cut of the original 570-block leave; they are not
SQSs.  For a dropped triple \(D\), the search leave has labels
\(D\cup\{15,16\}\).  The twelve retained systems keep their source labels.
Solver colours `0,...,4` are mapped back to these five output labels by their
order above the reference triple `(0,1,2)`; each JSONL row records this as
`solver_to_output_label`.

## Completed reconnaissance

The requested formerly unresolved cases were rerun for 45 seconds per case
with two workers:

| dropped systems | CP-SAT status | wall seconds |
|---|---:|---:|
| `(1,3,8)` | `INFEASIBLE` | 2.523483 |
| `(1,3,12)` | `INFEASIBLE` | 3.262838 |
| `(1,4,9)` | `INFEASIBLE` | 6.899413 |

The exact records are in `requested_cases_default_search.jsonl`.

The deterministic one-second interleaved pass in `sweep_1s.jsonl` contains
all 455 distinct dropped triples exactly once.  It returned 17
`INFEASIBLE`, 438 `UNKNOWN`, and no witness.  Its total CP-SAT wall time was
451.792889 seconds.  The 17 negative statuses are solver reconnaissance only.

`prioritized_repair.jsonl` contains eleven longer runs using the
change-minimization objective: nine `INFEASIBLE`, two `UNKNOWN`, and no
witness.  In particular, the anomalous one-second case `(8,10,13)` was
resolved as `INFEASIBLE` after 17.405159 seconds.  None of these CP-SAT
statuses is presented as a portable proof.

## Exact pair-link screen

There is a cheaper necessary condition.  Fix a point pair \(W\).  The
five-fold leave induces a simple 5-regular graph on the other eighteen
points: a leave block \(W\cup\{x,y\}\) becomes the edge \(xy\).  A global
five-colouring would decompose this graph into five perfect matchings.

`screen_pair_links.py` checked all

\[
\binom{15}{3}\binom{20}{2}=455\cdot190=86{,}450
\]

links by deterministic perfect-matching recursion.  Every link was
factorable, so the exact list of pair-link-infeasible dropped triples is
empty.  The primary run used 425,175 memoized residual states and 342,602
complete perfect-matching branches.  Its largest search used 1,074 residual
states at drop `(1,5,11)`, pair `(2,8)`.  The aggregate factorization digest
is

```text
691d8ecfd9bfa61438f0d82f88acb04de83c370ca9d11cebe27ee7350e21c71f
```

The complete machine-readable summary is
`pair_link_screen_receipt.json`.

`verify_pair_links_direct.py` independently repeated all 86,450 positive
checks by assigning colours directly to the 45 edges, without enumerating
perfect matchings.  It verified every returned colouring from scratch.  Its
independent colouring digest is

```text
b2f69ba3fc5aebfb0538daa7bf35b88fa3795307095c35ca9fe66c86f6c9209a
```

Thus pair links close as a local obstruction route for these 455 cores: all
of them pass.  This exact positive screen does not imply that any whole leave
is five-colourable.

## Commands

Search the three cases that survived the earlier five-second screen:

```sh
/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B \
  collaboration/eh_j5_repair_search/search_eh_j5_repair.py \
  --case 1,3,8 --case 1,3,12 --case 1,4,9 \
  --seconds 45 --workers 2 --seed 835 \
  --results collaboration/eh_j5_repair_search/requested_cases.jsonl
```

Sample the full set of 455 dropped triples in a deterministic interleaved
order, with a small first-pass budget:

```sh
/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B \
  collaboration/eh_j5_repair_search/search_eh_j5_repair.py \
  --sweep --seconds 2 --workers 2 --seed 835 \
  --results collaboration/eh_j5_repair_search/sweep_2s.jsonl
```

The `--minimize-changes` option makes the number of deviations from the
authenticated proper partial an objective.  It can be useful for constructive
search, but objective runs and feasibility runs should both be regarded as
reconnaissance unless they produce a witness.

Verify a found witness:

```sh
/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B \
  collaboration/eh_j5_repair_search/verify_eh_j5_witness.py \
  collaboration/eh_j5_repair_search/witnesses/ls3420_drop_1_3_8.txt \
  --drop 1 3 8
```

Reproduce the complete exact pair-link screen and its independent check:

```sh
/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B \
  collaboration/eh_j5_repair_search/screen_pair_links.py \
  --receipt \
    collaboration/eh_j5_repair_search/pair_link_screen_receipt.json

/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -B \
  collaboration/eh_j5_repair_search/verify_pair_links_direct.py \
  --receipt \
    collaboration/eh_j5_repair_search/pair_link_screen_receipt.json
```

# Exact branch-0 search handoff for \(LS(3,4,20)\)

## Scope and result

This directory turns the verified even-flag theorem into a deterministic
branch-0 search input.  It does **not** establish SAT or UNSAT for branch 0,
does not resolve \(LS(3,4,20)\), and does not resolve Erdős--Rosenfeld
Problem #835.

The checked Etzion--Hartman 4,773-block partial has been point- and
colour-relabelled from its fully assigned flag

\[
 B=\{0,4,5,9\},\quad T=\{0,4,5\},\quad e=\{0,5\},\quad r=4,\quad q=9
\]

to the canonical branch-0 flag \((012,01,3)\).  The resulting row has cycle
type \(2^8\).

Artifacts:

* `export_verify_eh_branch0_hint.py` derives both relabellings from the
  authenticated source, transforms all 4,845 rows, checks every partial
  triple star, checks all sixteen branch-0 units, and checks the inverse
  round trip.  It uses only the Python standard library and launches no
  solver.
* `eh15_branch0_partial.txt` is the deterministic CP-SAT hint: 4,773
  assigned blocks and 72 holes.
* `eh15_branch0_receipt.json` records the exact maps, hashes, counts, and
  scope.

The exact output hash is

```text
06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78
```

The derived maps, written in old-label order, are:

```text
point  = 0,4,6,7,2,1,8,10,5,3,11,12,14,16,18,9,17,15,13,19
colour = 11,14,12,2,1,4,6,7,16,9,3,5,8,15,10,13,0
```

## Reproduce and verify

Export:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/ls3420_branch0_search/export_verify_eh_branch0_hint.py \
  --output collaboration/ls3420_branch0_search/eh15_branch0_partial.txt \
  --receipt collaboration/ls3420_branch0_search/eh15_branch0_receipt.json
```

Verify an existing export without rewriting it:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/ls3420_branch0_search/export_verify_eh_branch0_hint.py \
  --verify collaboration/ls3420_branch0_search/eh15_branch0_partial.txt
```

Exact output of the independent semantic checks:

```text
status: PASS
blocks: 4845
assigned / holes: 4773 / 72
target branch / cycle type: 0 / 2,2,2,2,2,2,2,2
inverse round trip: PASS
partial semantics: PASS
output SHA-256: 06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78
```

The one-second model-loading smoke was:

```sh
/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3 \
  -B evidence/search_ls_3_4_20_full_cpsat.py \
  --seconds 1 --workers 1 --seed 842 \
  --hint collaboration/ls3420_branch0_search/eh15_branch0_partial.txt \
  --second-star-manifest \
    evidence/ls_3_4_20_second_star_branches/manifest.json \
  --second-star-branch-id 0
```

It reported exactly:

```text
status: UNKNOWN
hint_assigned_blocks: 4773
hint_conjugated_to_second_star: false
second_star_branch_id: 0
second_star_cycle_type: 2,2,2,2,2,2,2,2
triple_stars: 1140
```

`UNKNOWN` is expected from this bounded smoke and proves nothing.  The
important fact is that the already-relabeled hint loads without
`--conjugate-hint-to-second-star` and agrees with all branch-0 constraints.

## Authenticated branch-0 CNF path

The propagation-enhanced branch-0 CNF can be reproduced as:

```sh
/opt/homebrew/bin/python3 -B \
  evidence/materialize_ls_3_4_20_second_star_branch.py \
  --parent-cnf evidence/ls_3_4_20_generic_cnf/instance.cnf \
  --manifest evidence/ls_3_4_20_second_star_branches/manifest.json \
  --branch-id 0 --star-pairwise-amo \
  --output /private/tmp/ls3420-second-star-branch-0-amo.cnf
```

Authenticate it independently:

```sh
/opt/homebrew/bin/python3 -B \
  evidence/verify_ls_3_4_20_second_star_branches.py \
  --parent-cnf evidence/ls_3_4_20_generic_cnf/instance.cnf \
  --parent-manifest evidence/ls_3_4_20_generic_cnf/manifest.json \
  --manifest evidence/ls_3_4_20_second_star_branches/manifest.json \
  --cubes evidence/ls_3_4_20_second_star_branches/branches.cubes \
  --branch-cnf /private/tmp/ls3420-second-star-branch-0-amo.cnf \
  --branch-id 0 --star-pairwise-amo
```

The independent verifier returned:

```text
status: PASS
variables: 159885
clauses: 2887653
cycle type: 2,2,2,2,2,2,2,2
SHA-256: 5a8b07ca44a0697935c46690412e35275650c45e8432542098748b0a667b3d49
```

At 2026-07-26 14:11 EDT, that exact CNF was already running under Kissat
4.0.4 in tmux session `erdos835-ls3420-b0-amo-kissat`.  No second Kissat
or CaDiCaL copy should be started merely to duplicate that search.

## Safest hinted CP-SAT command

To redirect the existing hinted CP-SAT budget from redundant labelled
branch 54 to lossless branch 0, preserve its eight-worker ceiling and use:

```sh
/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3 \
  -B evidence/search_ls_3_4_20_full_cpsat.py \
  --seconds 21600 --workers 8 --seed 842 \
  --hint collaboration/ls3420_branch0_search/eh15_branch0_partial.txt \
  --second-star-manifest \
    evidence/ls_3_4_20_second_star_branches/manifest.json \
  --second-star-branch-id 0 \
  --certificate /private/tmp/ls-3-4-20-witness-b0-hinted.txt \
  --log
```

Do **not** pass `--conjugate-hint-to-second-star`: this artifact is already
in the canonical branch-0 labels.  A `FEASIBLE`/`OPTIMAL` result must be
checked by

```sh
/opt/homebrew/bin/python3 -B \
  evidence/verify_ls_3_4_20_certificate.py \
  /private/tmp/ls-3-4-20-witness-b0-hinted.txt
```

An `INFEASIBLE` CP-SAT result is not a portable proof.  A checked branch-0
UNSAT theorem would still require a proof-producing SAT run against the
authenticated CNF.  Because two existing decisive proof logs are already
growing and only about 57 GiB was free at this handoff, starting another
unbounded DRAT stream is not currently the safest path.

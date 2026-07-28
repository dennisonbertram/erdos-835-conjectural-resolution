# Independent audit of the wave-2 cut-feasible repair campaign

Date: 2026-07-28.

## Audited command and terminal result

The live process was inspected read-only:

```text
PID 94797
python collaboration/coordinated_nine_r0_repair_cegis/search_cut_feasible_repair.py
  --max-rounds 0
  --cuts-per-model 990
  --time-limit-seconds 900
  --replay-witness-log
    /private/tmp/erdos835-cut-minimal-wave1-20260728.jsonl
  --witness-log
    /private/tmp/erdos835-cut-minimal-wave2-20260728.jsonl
  --unsat-cnf-dir
    /private/tmp/erdos835-cut-minimal-wave2-unsat-20260728
```

The confirmed terminal JSON was:

```json
{
  "clauses_after_replay": 61067,
  "cuts": 99960,
  "elapsed_seconds": 900.056,
  "final_clauses": 144437,
  "initial_clauses": 44477,
  "new_cuts": 83370,
  "replay_sha256": "13a708a59b184027ec63db8402a7a88cb8f4b913b45646437e044a4a9a6e5046",
  "replayed_cuts": 16590,
  "rounds": 398,
  "status": "time_limit",
  "variables": 10992,
  "witness_sha256": "2c9c04247cb3dc478900639ee7b474b0706950796360037b368f44e98fd7354f"
}
```

No UNSAT CNF directory was created.  The process stopped at its configured
900-second limit.

## Whole-log replay and hash audit

The finalized wave-2 log has:

```text
83,370 records
21,437,047 bytes
```

Every record was streamed through the implementation's strict
`replay_witnesses` path.  To keep the independent audit memory-bounded, the
reconstructed clause was removed from the temporary in-memory CNF after each
record had passed:

1. duplicate-key JSON parsing;
2. typed witness decoding;
3. static witness validation;
4. capacity-cut validation;
5. clause reconstruction;
6. clause SHA-256 comparison; and
7. canonical compact-JSON comparison.

Results:

```json
{
  "records": 83370,
  "schema_counts": {"CutWitness": 83370},
  "duplicate_records": 0,
  "duplicate_clause_hashes": 0,
  "wave2_sha256": "25fc157ab609cc391cd6f3329915775a9b33af829da5ed3c89dac68fa1543e63"
}
```

The ordinary file hash agrees:

```sh
shasum -a 256 /private/tmp/erdos835-cut-minimal-wave2-20260728.jsonl
```

```text
25fc157ab609cc391cd6f3329915775a9b33af829da5ed3c89dac68fa1543e63
```

The replay-input hash also agrees with the terminal JSON:

```sh
shasum -a 256 /private/tmp/erdos835-cut-minimal-wave1-20260728.jsonl
```

```text
13a708a59b184027ec63db8402a7a88cb8f4b913b45646437e044a4a9a6e5046
```

Hashing the wave-1 and wave-2 bytes in replay order gives:

```text
2c9c04247cb3dc478900639ee7b474b0706950796360037b368f44e98fd7354f
```

This exactly equals the terminal `witness_sha256`.

There are no duplicates across the wave boundary:

```json
{
  "wave1_records": 16590,
  "wave2_records": 83370,
  "cross_duplicate_records": 0,
  "cross_duplicate_clause_hashes": 0,
  "combined_unique_records": 99960,
  "combined_unique_clause_hashes": 99960
}
```

All 83,370 generated replacement lists were sorted, distinct, and in edge
range.  All colour lists contained exactly three distinct indices in
\(\{0,\ldots,6\}\), and all complement arrays contained exactly three
canonical triples.

## Deterministic independent sample

Five interior records, chosen independently of the earlier audit sample,
were reconstructed again:

| line | signature \((i;r_0,r_1,r_2)\) | clause literals | hash check |
|---:|:---:|---:|:---:|
| 50,021 | \((1;0,2,3)\) | 69 | exact |
| 60,013 | \((4;1,4,5)\) | 71 | exact |
| 70,001 | \((2;0,1,2)\) | 72 | exact |
| 80,021 | \((0;0,3,5)\) | 70 | exact |
| 83,359 | \((5;1,4,6)\) | 72 | exact |

For every sampled record:

* the recorded and independently recomputed clause hashes were equal; and
* reserializing the typed witness and reconstructed clause reproduced the
  canonical JSON line exactly.

## Clause semantics

A `CutWitness` fixes:

1. one prefix layer's original support;
2. a replacement perfect matching \(P\) on that support;
3. three of the seven remaining size-ten complement rows; and
4. explicit edges which remain free of the other five prefix layers.

The replacement edges are included among the edges required to avoid the
other five layers.  The capacity certificate excludes \(P\) itself and
counts only edges which remain residual after the repair.

For a selected ten-support \(S\), a perfect matching uses at least
\[
\max(0,|S\cap X|-5)
\]
edges internal to \(X\).  Three mutually edge-disjoint perfect matchings
therefore require at least
\[
\sum_{j=1}^3\max(0,|S_j\cap X|-5) \tag{1}
\]
distinct residual edges in \(X\).

Only \(|X|=6,7,8\) can make (1) stronger than the universal internal-edge
lower bound coming from maximum deleted degree five.  Sets of order at most
five have zero demand, while for sets of order at least nine the universal
edge lower bound already exceeds the maximum demand.  Thus the implemented
finite cut list is the complete list of this particular internal-edge
capacity relaxation.

The learned clause is exactly the negation of the sufficient conditions for
the recorded **cut-feasible** repaired route.  Hence any base assignment
having no such route must satisfy every learned clause.

## Exact meaning of each terminal status

### `time_limit`

This is the actual wave-2 result.  It proves no universal theorem and gives
no counterexample.  It means only that 398 solver rounds were attempted and
the valid accumulated clause database was not resolved within 900 seconds.

The 83,370 new cuts equal
\[
397\cdot(6\binom73)=397\cdot210.
\]
Thus 397 completed models supplied a cut-feasible witness for every one of
the 210 repair-layer/three-triple signatures.  This is substantial search
evidence, but it is not a proof about unvisited models.

### `counterexample`

The script would independently replay the raw model and prove:

> For that particular packed complement-cover six-prefix, no replacement of
> one prefix layer on its fixed support makes any three of the seven
> remaining size-ten rows satisfy all internal-edge capacity cuts.

Because actual edge-disjoint perfect matchings necessarily satisfy those
cuts, this would also refute an actual three-size-ten continuation after one
repacked layer for that prefix.

It would **not** refute:

* a continuation using one or more of the four remaining size-eight rows;
* repair of two or more prefix layers;
* choosing a different complement-cover six-prefix from the same support
  family;
* coordinated nine in unrestricted scope; or
* Erdős--Rosenfeld Problem #835.

### `unsat_uncertified`

The incremental solver result alone would not be a proof.  After freezing
the final CNF, generating a fresh DRAT proof, replaying it with DRAT-trim,
and independently auditing every semantic witness cut, UNSAT would prove:

> Every exact \(r=0\) packed complement-cover six-prefix has a one-layer
> support-preserving repacking and three remaining size-ten rows satisfying
> all the encoded internal-edge capacity cuts.

That remains only a **cut-feasibility theorem**.  The capacity cuts are
necessary, not sufficient, for three pairwise edge-disjoint perfect
matchings.  Even a fully certified UNSAT result would therefore not prove
coordinated nine or #835 without a separate theorem upgrading cut
feasibility to actual matching coordination.

## Replay hardening caveat

The generated wave-1 and wave-2 logs are canonical and pass stronger shape
checks.  The generic replay validator itself should nevertheless be hardened
before accepting untrusted external logs:

* it tests that the set of colour indices has order three, but does not
  separately require the colour tuple itself to have length three; and
* it does not explicitly require the replacement edge tuple to be sorted,
  although generated replacements are sorted.

Neither issue affects this campaign: all 99,960 records have exactly three
canonical colours and canonical replacements.  The first issue could become
proof-relevant for a maliciously constructed external replay log, so a
future certificate auditor should enforce both conditions explicitly.

## Static code check

```sh
/Users/dennison/Library/Python/3.9/bin/ruff check \
  collaboration/coordinated_nine_r0_repair_cegis/search_cut_feasible_repair.py
```

Result:

```text
All checks passed!
```

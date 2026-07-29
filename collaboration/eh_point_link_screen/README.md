# Complete exclusion of EH retain-twelve repairs

## Exact result

Let \(\mathcal C_0,\ldots,\mathcal C_{14}\) be the fifteen authenticated
Etzion--Hartman SQS(20)s. Every twelve-member subfamily of this fixed EH
15-core is excluded from an \(LS(3,4,20)\). Consequently:

> Any \(LS(3,4,20)\), if one exists, shares at most eleven of these fifteen
> EH systems.

The \(\binom{15}{3}=455\) drop-three cases are covered without overlap:

| exclusion route | cases | evidence |
|---|---:|---|
| ten-point obstruction | 30 | exhaustive deterministic DSATUR |
| legacy point-0 obstruction | 2 | independently replayed DRAT |
| batch point-0 obstruction | 423 | independently replayed trimmed DRAT |
| total | 455 | complete |

The aggregate gate checks that these three sets are pairwise disjoint and
their union is all 455 cases. It also runs every underlying verifier.

This is a theorem about overlap with one fixed EH core. It does **not** prove
that \(LS(3,4,20)\) is nonexistent, and it does not resolve
Erdős--Rosenfeld Problem #835.

## Why a derived-point obstruction is decisive

Discard three EH systems, retain the other twelve, and fix point \(0\).
Delete \(0\) from every leave block containing it. The resulting point-link
is a \(2\text{-}(19,3,5)\) design:

- 285 triples on nineteen points;
- 171 point pairs;
- exactly five triples over each pair;
- a 12-regular graph when triples sharing a pair are adjacent.

If the five-fold SQS(20) leave could be partitioned into five replacement
SQS(20)s, deriving those five systems at point \(0\) would partition the
285 triples into five STS(19)s. Therefore an UNSAT point-link certificate is
a rigorous obstruction to the global repair. The converse is not claimed:
a colourable link at one point alone need not construct a global repair.

`point_link_cnf.py` encodes the point-link partition transparently. Variable
\(x_{B,c}\) assigns one of five colours to derived triple \(B\).

1. Every triple has exactly one colour.
2. For every pair and every colour, exactly one of the five triples over that
   pair has that colour.
3. The first five-triple pair-star is fixed to colours \(0,\ldots,4\), which
   is without loss under a global colour relabelling.

Every instance has 1,425 variables and 12,545 clauses. Satisfying
assignments are exactly partitions of that point-link into five STS(19)s.

## Exact STS packing number in the certified links

The three discarded EH systems derive to three pairwise disjoint STS(19)s
inside every one of the 455 point-0 leaves. This gives a canonical
three-pack.

There is also an elementary complement lemma. If a five-fold leave contained
four disjoint STS(19)s, those systems would use four of the five available
triples over every point pair. The 57 unused triples would therefore cover
every pair exactly once and form a forced fifth STS(19).

It follows that an UNSAT five-colouring certificate rules out even a
four-pack. Hence the STS(19) packing number is exactly three in the 425
point-link-certified cases: the two legacy cases plus the 423-case batch.
The separate ten-point theorem excludes the other 30 global repairs, but
does not by itself determine the packing number of their point-0 links.

The all-455 canonical three-pack audit has digest:

```text
c27934a1d370abad000b1bc83bcd5a83e479603e25545416e49e394133dee9e7
```

## Portable certificate bundle

The authenticated EH seed is
`evidence/ls_3_4_20_eh15_seed.txt`, SHA-256:

```text
b1ea090d3e3b88366c87e95660c1c82a406d2c3b100cc1d39bcc2c7e8fde47f9
```

The new batch contains 423 deterministic gzip files in `certificates/`.
Each stores a trimmed binary DRAT proof. The manifest records the exact CNF
hash, compressed and uncompressed proof hashes, dimensions, tool versions,
and provenance timings.

```text
batch proof files:                 423
batch compressed proof bytes:     608,518,572
largest compressed proof:           3,618,195 bytes
batch manifest SHA-256:
0ae9a6a7b840cd2927e1b150d9a5ff5cd89d7b0c50d4b0b77b543c42d5c2d4f9
batch certificate bundle digest:
1698fc1e5e14814ac37b5a6a9d8a8375420fdb8f304eb1e237040ce9a2d48c67
```

CaDiCaL 3.0.1 produced the proofs. `drat-trim` at upstream commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` checked and trimmed them.
The portable gate:

- authenticates and reconstructs all fifteen source SQS(20)s;
- independently reconstructs every design-to-CNF serialization without
  importing the CNF generator;
- validates every manifest field and compressed/uncompressed hash;
- detects missing or orphan proof files;
- streams all 423 proofs through `drat-trim`;
- separately replays the two legacy proofs;
- reruns the exact 30-case ten-point theorem;
- checks the complete \(30+2+423=455\) coverage partition.

The raw-proof and first-check fields in the manifest are generation
provenance: raw proofs are not committed. Portable verification uses the
committed trimmed gzip files and fresh `drat-trim` replay.

## Verify the committed theorem

Python 3.10 or newer is required because the existing ten-point verifier uses
`int.bit_count()`.

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/eh_point_link_screen/verify_all_455_coverage.py \
  --batch-recon \
    collaboration/eh_point_link_screen/remaining_423_point0_recon.jsonl \
  --batch-manifest \
    collaboration/eh_point_link_screen/remaining_423_point0_certificate_manifest.jsonl \
  --batch-base-dir collaboration/eh_point_link_screen \
  --drat-trim /path/to/drat-trim \
  --receipt \
    collaboration/eh_point_link_screen/all_455_point0_theorem_receipt.json
```

Expected final output:

```text
[theorem] every twelve-system subfamily of the EH 15-core is excluded
[theorem] any LS(3,4,20) shares at most 11 of the EH 15-core
[theorem] the 425 point-link-certified leaves have STS(19) packing number exactly 3
[scope] The separate ten-point theorem does not determine the point-0 packing number in its other 30 cases.
[scope] This does not decide LS(3,4,20) or #835.
[exact] aggregate receipt SHA-256: 312096aa9e489156778094e7ab7dc4fd3e3fe34c11d9a2d82531489684c4b085
status: PASS
```

The aggregate receipt also binds the coverage digest, source hash, legacy
evidence hashes, recon receipt, manifest, bundle digest, tool identifiers,
proof byte total, and packing scope.

## Recorded reconnaissance and regeneration

Before certification, all 423 new point-0 cases returned CaDiCaL's UNSAT
competition code:

```text
census:                       423 UNSAT_RECONNAISSANCE
total solver seconds:         928.751818
minimum / maximum seconds:    0.652791 / 7.108775
recon JSONL SHA-256:
cf3d33428cfdb62781afa2ef0015bd1b1da76a9898523e0e921f0009e82503a9
recon receipt SHA-256:
563a52d46c4f242e0ba0856e09b0940e05bcd4bfaa1f3caa58a9363c9ce599d2
```

Those solver statuses became theorems only after the DRAT certificates were
generated and replayed. To regenerate fresh evidence, use
`screen_point_links.py`, `finalize_recon_receipt.py`, and
`certify_point_links.py`. Timings are stored in the JSONL and manifest, so a
fresh run is not expected to reproduce those whole-file hashes byte-for-byte.
The committed evidence is verified by semantic reconstruction and proof
replay, not by expecting a rerun to have identical timings.

## Separate retain-eleven frontier

Dropping four EH systems and retaining eleven gives a point-link
\(2\text{-}(19,3,6)\) design with 342 triples. A packing of five disjoint
STS(19)s forces the sixth by the same complement argument, so a six-colouring
is equivalent to a five-pack. The four discarded EH systems give a canonical
four-pack, making the point-link packing number either four or six.

`drop_four_point_link_cnf.py` emits the direct six-colour encoding:

```text
variables: 2,052
clauses:  21,894
```

`screen_drop_four_samples.py` tested nine point-0 cases, one in every cell of
the construction-pack-multiplicity/full-top structural census. These are
diverse reconnaissance cases, not automorphism-orbit representatives; the EH
core has trivial automorphism group.

All nine reached the 30-second bound:

```text
census:               9 UNKNOWN
total solver seconds: 270.321988
results SHA-256:
e29ba7363bc1ad67d30586161a089d1c4e82eb33c198ceece5bb3055d093a3b7
```

`verify_drop_four_sample.py` regenerates all nine CNFs, checks the intended
structural cells, validates the receipt, and would independently check any
stored SAT colour vector as six STS(19)s. Here there are no SAT or UNSAT
claims:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/eh_point_link_screen/verify_drop_four_sample.py \
  --results \
    collaboration/eh_point_link_screen/drop_four_point0_sample_recon.jsonl \
  --receipt \
    collaboration/eh_point_link_screen/drop_four_point0_sample_receipt.json
```

This bounded sample identifies the next frontier as materially harder. It
does not exclude or construct a retain-eleven completion.

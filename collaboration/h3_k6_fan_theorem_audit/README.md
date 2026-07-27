# Independent audit: universal k=6 fan theorem and cyclic CNF

## Scope and verdict

This directory audits:

- commit `7aec3f3` (`Prove the universal k6 fan obstruction`), especially
  `ALL_K6_THEOREM.md`, `k6_large_sets.py`, and `verify_all_k6_links.py`;
- the then-uncommitted cyclic invariant-fan CNF generator and model decoder in
  `collaboration/h3_simultaneous_fan_attack_2/`.

The universal **k=6** theorem passes an independent reconstruction. I found no
gap in the 840/15,360/two-orbit classification, either 18-cell contradiction,
or the deduction that no `LS(2,3,9)` supports a simultaneous 3-fan.

The cyclic CNF also passes an independent byte-level and semantic audit. The
audit initially found one small decoder-hardening issue: its status parser
accepted the nonstandard string `s NOTSATISFIABLE` because it searched for the
substring `SATISFIABLE`. The decoder now requires exact equality with
`s SATISFIABLE`; the audit verifies that regression fix as well as the
independent one-hot and rainbow checks.

Nothing here proves the unresolved k=16 case or Erdős--Rosenfeld Problem #835.
The cyclic CNF has been encoded and audited, but no satisfying model or
unsatisfiability certificate is supplied.

## 1. Independent k=6 classification

`verify_k6_fan_theorem_audit.py` imports none of the committed k=6
implementation. It independently:

1. reconstructs the type A and type B array large sets;
2. checks every constituent is an `STS(9)`, the seven systems are disjoint,
   all 84 triples are covered, and every pair-star has all seven colours;
3. enumerates exact triangle decompositions of `K_9`, finding 840 labelled
   `STS(9)`s;
4. counts unordered exact covers of the 84 triples by seven systems, finding
   15,360 large sets on the fixed labelled point set;
5. scans all `9!` point permutations and obtains automorphism orders 42 and
   54.

The two representatives cannot be point-isomorphic because isomorphic
structures have conjugate automorphism groups and hence the same order. Thus
their point-action orbits are disjoint. Orbit--stabilizer gives

```text
type A: 9! / 42 = 8,640
type B: 9! / 54 = 6,720
sum                  15,360
```

Each orbit consists of valid large sets and the disjoint orbit sizes sum to
the independently enumerated total. This validates the classification logic:
there are exactly two point-isomorphism types.

Minor wording note: the docstring of `count_large_sets` says “seven labelled
STS masks,” but its canonical first-uncovered-triple branching counts the
seven systems as an unordered exact cover. The theorem text and reported
15,360 count use the correct unordered interpretation.

## 2. Every cell, clique, and written contradiction

For each representative, the independent verifier builds the full conflict
hypergraph from its link:

```text
378 allowed cells
630 three-cell groups = 126 Q-groups + 504 (T,c)-groups
every cell lies in 5 groups
the conflict graph is 10-regular with 1,890 edges
```

All 36 displayed cells are allowed. All 22 displayed triangles are exact
constraint groups, with these independently recovered identities:

```text
type A
ABC=Q:0278   KLM=Q:0258   OPQ=Q:0245
ADE=TC:027;4 AGI=TC:028;4 BJK=TC:028;1 CHL=TC:028;5
DGO=TC:024;4 JNR=TC:026;1 KPR=TC:025;1 FLQ=TC:025;5

type B
BCD=Q:0134   PQR=Q:0378
ABE=TC:013;0 CFG=TC:013;1 AHI=TC:023;0 DKL=TC:034;4
EIP=TC:037;0 FJQ=TC:037;1 KNR=TC:037;4
GOQ=TC:038;1 LMR=TC:038;4
```

The prose contradictions were checked more narrowly than a generic
non-3-colourability search:

- Type A, with `A=0,B=1,C=2` and only `JNR` removed, has 18 colourings.
  Every one satisfies all advertised intermediate set equalities and ends
  with `J=R`; both cases `K=0` and `K=2` occur. Restoring the clique `JNR`
  leaves zero colourings.
- Type B, with `B=0,C=1,D=2` and only `PQR` removed, has 8 colourings. Every
  one forces `I=0`, `P=A`, `Q=1`, and `R=2`, so `PQR` cannot be rainbow.
  Restoring `PQR` leaves zero colourings.

This directly validates both human-readable contradiction chains rather than
only checking the final graphs with another DSATUR implementation.

## 3. Cyclic invariant-fan CNF

`verify_cyclic_cnf_audit.py` independently reconstructs the cyclic
`LS(2,3,19)`, validates all pair-stars, and builds the `C17` quotient:

```text
2,964 quotient cells
1,140 quotient groups, each of size 13
every quotient cell lies in 5 groups
88,591 distinct conflict edges
```

### Base encoding

For every cell, the generator emits one 13-literal at-least-one clause and a
12-auxiliary Sinz sequential at-most-one encoding with 35 binary clauses.
For every group and label it emits one 13-literal coverage clause. Finally it
fixes the first rainbow group's member labels with 13 unit clauses.

```text
variables = 2,964 * (13 primary + 12 auxiliary) = 74,100
clauses   = 2,964 * 36 + 1,140 * 13 + 13     = 121,537

clause lengths
1:       13
2:  103,740
13:  17,784
```

The independent verifier exhausts all `2^13 = 8,192` primary assignments for
one sequential counter. An assignment has some satisfying auxiliary extension
if and only if at most one primary is true. Together with the cell
at-least-one clause, every cell is exactly one-hot.

Every quotient group has exactly 13 cells. Requiring each of 13 labels to
occur at least once among 13 one-hot cells therefore makes the group rainbow;
no separate group at-most-one clauses are logically needed. The first group
is rainbow, so a global permutation of the 13 fan labels can map its member in
position `i` to label `i`. The 13 normalization units are lossless.

The generated base file was reproduced clause-for-clause and byte-for-byte:

```text
sha256 b247b458dfeb3daff7c37046bd2def635601e26737761f5450541722dccb85a5
```

### Optional redundant group AMO

The optional mode adds 13 negative binary clauses for every distinct conflict
edge:

```text
extra clauses = 88,591 * 13 = 1,151,683
total clauses                   1,273,220
sha256 896d975b3246202daa0b1d6fd101e60d3f53814dc4f50ea1ada859f5715d2591
```

This file also matches the independent clause stream byte-for-byte.

### Direct pairwise encoding

The third solver variant replaces each cell's twelve auxiliary variables and
35-clause sequential AMO with the 78 primary-variable pairwise clauses, and
also retains the redundant conflict-edge clauses:

```text
variables = 38,532
clauses   = 1,400,672
sha256 74ac2417ffdc1410075faabb5d2292969f2247566583980ed46f777f98bc9249
```

The extended independent verifier reconstructs this clause stream without
importing the generator and matches it byte-for-byte. The direct encoding is
logically equivalent to the base encoding; it is only a different
propagation experiment.

### Decoder

Synthetic unit tests against the hardened decoder confirm:

- an ordinary `s SATISFIABLE` model is parsed;
- `s UNSATISFIABLE`, `s NOTSATISFIABLE`, and a missing status are rejected;
- a valid one-hot rainbow synthetic model is accepted;
- a two-hot cell is rejected;
- a one-hot but non-rainbow group is rejected.

Ignoring auxiliary literals is intentional and sound for the output
certificate: the decoder verifies the stronger, direct combinatorial object
(one label per cell and every group rainbow), rather than trusting that the
solver's auxiliary assignment satisfies the DIMACS.

## Reproduction

```sh
python3 -B collaboration/fan_small_controls/verify_all_k6_links.py
python3 -B collaboration/h3_k6_fan_theorem_audit/verify_k6_fan_theorem_audit.py

python3 -B \
  collaboration/h3_simultaneous_fan_attack_2/write_cyclic_invariant_fan_cnf.py \
  /tmp/cyclic_invariant_fan_audit.cnf
python3 -B \
  collaboration/h3_k6_fan_theorem_audit/verify_cyclic_cnf_audit.py \
  /tmp/cyclic_invariant_fan_audit.cnf

python3 -B \
  collaboration/h3_simultaneous_fan_attack_2/write_cyclic_invariant_fan_cnf.py \
  /tmp/cyclic_invariant_fan_audit_redundant.cnf \
  --redundant-group-amo
python3 -B \
  collaboration/h3_k6_fan_theorem_audit/verify_cyclic_cnf_audit.py \
  /tmp/cyclic_invariant_fan_audit_redundant.cnf \
  --redundant-group-amo

python3 -B \
  collaboration/h3_simultaneous_fan_attack_2/write_cyclic_invariant_fan_cnf.py \
  /tmp/cyclic_invariant_fan_audit_direct.cnf \
  --redundant-group-amo --pairwise-cell-amo
python3 -B \
  collaboration/h3_k6_fan_theorem_audit/verify_cyclic_cnf_audit.py \
  /tmp/cyclic_invariant_fan_audit_direct.cnf \
  --redundant-group-amo --pairwise-cell-amo

ruff check collaboration/h3_k6_fan_theorem_audit
```

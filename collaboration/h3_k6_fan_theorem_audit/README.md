# Independent audit: universal k=6 fan theorem and cyclic CNF

## Scope and verdict

This directory audits:

- commit `7aec3f3` (`Prove the universal k6 fan obstruction`), especially
  `ALL_K6_THEOREM.md`, `k6_large_sets.py`, and `verify_all_k6_links.py`;
- the then-uncommitted cyclic invariant-fan CNF generator and model decoder in
  `collaboration/h3_simultaneous_fan_attack_2/`; and
- the later \(C_{17}\)-invariant single-matching models, exact-cover matrix,
  formula screen, and direct CNF.

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

## 4. Cyclic invariant single-matching audit

`verify_invariant_matching_attack.py` independently proves that the newer
single-matching model is exactly the pre-existing \(C_{17}\)-equivariant
\(LS(3,4,20)\) exact-cover instance:

```text
matrix: 2,964 rows x 1,140 columns
row degree: 5
column size: 13
matrix sha256 059c4f30f2355100ce5589acaac1e8ddc337ee8e3fe55294103d68379d078186
```

It checks the full quotient-cell-index to sparse-matrix-row bijection.  The
compact cover CNF has 3,876 phase variables, of which 912 are forbidden by
unit clauses; it has no auxiliaries:

```text
clause census  1:912, 2:31,008, 16:912, 17:228
total clauses  33,060
sha256 860aba8e26b2ec8c0fdbe268e5a19cac63647ef3593b123d7a12c5dec63eccf2
map sha256 2908c7b90fc14a5229600b359fddf7e874f8665418b7e85ed94215143abab358
```

`write_matching_direct_exact_cover_cnf.py` emits a propagation-strong
equivalent encoding with one coverage clause and all 78 pairwise clauses for
each of the 1,140 exact-cover groups.  The audit reconstructs all 90,060
clauses independently:

```text
sha256 bfd7e07ffbdeb1c4a2a2f74f6a2af38c62845f3a114b5294848288ebfb0a6252
```

The same audit independently reproduces all 272 fan formulae, all 3,536
individual matching classes, their optima 4,098 and 237, and the strong odd
cycle and induced \(C_5\).  It also checks the local/CP-SAT/DLX certificate
gates and hint bridge.  None of these audits supplies a matching, fan, or
Problem #835 solution.

## 5. Audit-only exact-cover search ordering

`solve_c17_exact_cover_order_bench.cpp` retains the exact matrix and DLX
cover/uncover semantics while benchmarking randomized, least-constraining,
most-constraining, exact-damage, near-hint, and randomized-column-tie orders.
No heuristic filters or fixes a row.

On seed 1701, the existing randomized value order was better than every
least-constraining or damage score tested: it reached depth 103 in two seconds,
versus 98 for the cheap LCV proxy and 94 for the exact damage score.  A
ten-second randomized run processed 1,236,992 nodes and reached depth 103.
Ten one-second random restarts processed 1,458,176 nodes in 10.21 aggregate
seconds and reached depth 104.

That is only a diversification signal, not evidence of a solution or a
universal speedup.  Restarted traversals can revisit common prefixes, node
counts from different search trees are not proof-work measures, and every run
returned `UNKNOWN`.  The safe operational recommendation is to retain the
current randomized row order and, for witness hunting, run independent short
seeds in parallel or a geometrically increasing restart schedule.  Any
`SAT_CANDIDATE` remains provisional until
`verify_c17_equivariant_cnf.py --model ...` passes.

## 6. OR-Tools MIP audit

The exact MIP script was independently checked against the quotient incidence:
it has exactly 2,964 binary cell variables and all 1,140 size-13 exact-cover
equalities.  Every cell occurs in one Q group and four triple-colour groups, so
this is precisely the same binary exact-cover problem as the sparse matrix.

The soft MIP keeps the 228 Q equalities hard and uses, for each of the 912
triple-colour groups,
\[
  \operatorname{count}+u-v=1,\qquad u,v\geq0,
\]
minimizing \(u+v\).  For a fixed integer count its minimum is exactly
\(\lvert\operatorname{count}-1\rvert\).  More importantly, the script does not
trust the floating-point objective: it reconstructs the selected cells,
checks the Q transversal, recomputes the integer L1 defect, and calls the
independent combinatorial verifier before writing a zero-defect certificate.
Warm starts are validated one-per-Q hints and remain advisory.

With OR-Tools 9.15.6755 and SCIP 10.0, a three-second exact run returned
`NOT_SOLVED`; a three-second hinted soft run returned a feasible incumbent
with both reported and semantic defect 108.  Neither wrote a certificate.
HiGHS returned unmapped status code 99 in one-second smokes, and CBC did not
respect the nominal one-second wall time tightly; both paths still fail
closed.  No backend-local `INFEASIBLE`, timeout, unknown code, or positive
defect is treated as a proof.

## 7. C++ one- and two-move witness hunter

`search_c17_matching_two_opt.cpp` was audited against full recomputation.  Its
collision score is
\(\sum_g\binom{\operatorname{count}_g}{2}\).  A Q-transversal has exactly 912
triple-colour incidences over 912 groups, so score zero is equivalent to every
triple-colour count being one.  Every zero is then checked against all 1,140
loaded-matrix columns before an exclusive SAT-candidate write, and the output
still states that independent semantic verification is required.

For two moves with changed incidences \(a_g,b_g\), the exact interaction is
\[
  \Delta(a+b)=\Delta(a)+\Delta(b)+\sum_g a_gb_g.
\]
After all single moves are nonnegative, any improving pair must therefore
share at least one group with opposite signs.  The sparse positive/negative
index is exhaustive: at a sampled single-move local optimum, a brute-force
comparison found 20 improving pairs, all 20 indexed, with best delta \(-1\)
in both searches.  A further 12,500 randomized one- and two-move checks agreed
with complete count and score recomputation.

The parser unconditionally validates positive unique row labels, five distinct
columns per row, one Q plus four triple-colour incidences, and thirteen rows
per Q group.  Hint, model, and best-effort paths must be distinct; both output
formats use exclusive creation.  A five-second hinted smoke compiled cleanly,
performed 523,952 moves, and ended `UNKNOWN` at score 54.  Its 228-row
best-effort file independently recomputed to score 54; no candidate model was
emitted.

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

python3 -B \
  collaboration/cyclic_lsts19_extension/generate_c17_equivariant_cnf.py \
  --cnf /tmp/c17_matching_cover.cnf \
  --map /tmp/c17_matching_cover-map.json \
  --encoding cover
python3 -B \
  collaboration/h3_k6_fan_theorem_audit/write_matching_direct_exact_cover_cnf.py \
  --matrix collaboration/cyclic_lsts19_extension/c17_exact_cover.matrix \
  --cnf /tmp/c17_matching_direct.cnf
python3 -B \
  collaboration/h3_k6_fan_theorem_audit/verify_invariant_matching_attack.py \
  --matrix collaboration/cyclic_lsts19_extension/c17_exact_cover.matrix \
  --cover-cnf /tmp/c17_matching_cover.cnf \
  --cover-map /tmp/c17_matching_cover-map.json \
  --direct-cnf /tmp/c17_matching_direct.cnf

c++ -std=c++17 -O3 -Wall -Wextra -pedantic \
  collaboration/h3_k6_fan_theorem_audit/solve_c17_exact_cover_order_bench.cpp \
  -o /tmp/c17_order_bench
/tmp/c17_order_bench \
  collaboration/cyclic_lsts19_extension/c17_exact_cover.matrix \
  /tmp/c17_order_candidate.model 2 1701 random -

ruff check collaboration/h3_k6_fan_theorem_audit
```

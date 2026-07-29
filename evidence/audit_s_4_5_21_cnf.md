# Independent audit: `s_4_5_21_cnf.py`

Run:

```sh
python3 -B evidence/audit_s_4_5_21_cnf.py
```

The audit generates and parses all seven DIMACS instances and compares them
with the CP-SAT model in `search_s_4_5_21_extension.py`.  It passed on 2026-07-24:
every case has 20,269 variables and 814,322 clauses, with exactly the same
variables, all 5,985 exact-one rows, and all 17 normalization units as the
CP-SAT model.

## Direct count check

After fixing `01234`, every other block containing four anchor points is
impossible, so the candidate count is

\[
\binom{21}{5}-\binom54\binom{16}{1}=20{,}269.
\]

The rows indexed by 4-sets have lengths (17) (5,820 times), (15) (160
times), and (1) (five times).  Hence their pairwise exact-one CNF encoding,
together with 17 units, has

\[
17+5985+5820\binom{17}{2}+160\binom{15}{2}=814{,}322
\]

clauses.  The audit checks every DIMACS clause in sequence, not only this
count.

## Why the seven cases are exhaustive

With `01234` fixed, blocks through `012` make a perfect matching on the other
18 points, containing `34`.  A permutation of the other 16 points makes the
remaining eight edges `56,78,...,19,20`.  Blocks through `013` give a second
perfect matching, containing `24`; on those 16 points it is disjoint from the
first matching (otherwise a 4-set would occur twice).  The union of two
disjoint perfect matchings is a disjoint union of alternating cycles of even
length at least four.  Under the stabilizer of the first matching, its orbit
is determined by the unordered half-cycle lengths, namely the partitions of
eight with all parts at least two:

\[
(8),(6,2),(5,3),(4,4),(4,2,2),(3,3,2),(2,2,2,2).
\]

Thus these are lossless label normalizations for an arbitrary
(S(4,5,21)), not an automorphism restriction.

## Decoder scope

For a SAT output, `decode()` maps positive literals to five-sets and calls the
independent `verify()` routine, which requires exactly 1,197 blocks and checks
every one of the 5,985 four-sets has multiplicity one.  No SAT witness existed
at audit time, so acceptance of an actual solver-produced witness remains to
be executed.  For UNSAT, the DIMACS audit does **not** validate a DRAT proof;
an independent proof checker is still required before treating any UNSAT case
as certified.

# Exact row-type partition after the five-core reductions

This directory provides deterministic tooling for partitioning the strongest
current exceptional-\(r=0\) CNF by the row counts of the four surviving
Tutte-core types
\[
(A,B,C,D)=(5111,3311,31111,6).
\]

These are counts of the seven support rows, not counts of distinct core
descriptors. The 120 weak compositions of seven into four row-type counts
partition every
possible assignment of obstruction types to the seven remaining size-ten
supports. The all-\(D\) branch is already excluded by the verified four-\(K_6\)
theorem, leaving exactly 119 SAT branches.

Every generated branch includes the proved prerequisite cuts:

- only \(A,B,C,D\) survive the row-sum elimination;
- at least five distinct core descriptors are required;
- the all-\(K_6\) branch is excluded; and
- any \(B\)-row forces at least six distinct core descriptors.

The resulting partition has 35 \(B\)-free branches requiring at least five
distinct cores and 84 \(B\)-present branches requiring at least six. This is
distinct from the exactly-five-core type screen: after the \(B\)-exclusion,
that screen has 21 unresolved multisets over \(A,C,D\).

List the complete partition without writing CNFs:

```bash
python3 -B branch_runner.py --list
```

Generate one branch:

```bash
python3 -B branch_runner.py \
  --output-dir /private/tmp/erdos835-r0-type-branches \
  --branch a2_b1_c3_d1
```

Run a bounded search only when no other CaDiCaL process is active:

```bash
python3 -B branch_runner.py \
  --output-dir /private/tmp/erdos835-r0-type-branches \
  --branch a2_b1_c3_d1 \
  --solve-seconds 300 \
  --drat-trim /private/tmp/drat-trim-erdos835/drat-trim
```

The runner refuses concurrent solving by default. `--allow-concurrent` is an
explicit override and should not be used while the monolithic exact run needs
the CPU.

For SAT, the witness is checked directly as a seven-prefix blocking all seven
remaining size-ten supports. For UNSAT, the binary DRAT trace is replayed with
`drat-trim -i` when `--drat-trim` is supplied. `UNKNOWN`,
`UNSAT_AWAITING_REPLAY`, and partial proof streams are always labeled
nonterminal.

The 119 branches become a proof only when every branch has a directly checked
SAT witness or an independently replayed UNSAT certificate. This partition
addresses only the exceptional-\(r=0\) eighth-matching frontier. It does not
constrain the three remaining size-eight supports and does not resolve
Erdős--Rosenfeld problem 835.

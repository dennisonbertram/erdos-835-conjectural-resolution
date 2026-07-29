# Exact refutation of every two-core r=0 obstruction

Date: 2026-07-27.

## Result

The row-sum elimination in
`../R0_ROW_SUM_CORE_ELIMINATION.md` leaves four possible size-ten Tutte
cores:
\[
5111,\qquad3311,\qquad31111,\qquad6.
\]
The sharper solver-free reuse ceilings are respectively \(3,1,3,5\).
Consequently, two distinct cores can block all seven remaining size-ten
supports only in one of these type pairs:
\[
(5111,6),\qquad(31111,6),\qquad(6,6).
\]

This package exhausts every \(S_{13}\)-orbit and every possible split of
the seven blocked supports between those two cores. Twenty-two CNFs are
UNSAT, each with an independently replayed DRAT certificate. The remaining
orbit consists of two disjoint \(K_6\)'s: their thirty edges omit a
thirteenth vertex, and the one remaining prefix edge cannot raise its
degree from zero to the required minimum two.

Therefore:

> If all seven remaining size-ten supports are blocked after an \(r=0\)
> seven-prefix, at least three distinct Tutte cores are required.

This is not an eighth-colour theorem. Configurations with three or more
distinct surviving cores remain open.

## Exact model

Each CNF contains:

- seven edge-disjoint selected matchings, three of size five and four of
  size four;
- all edges of the specified pair of cores;
- seven size-three complements, assigned to the outside set of one of the
  two cores;
- three size-five complements;
- the exact row identity
  \[
  \#\{\text{remaining complements containing }v\}=d_F(v)-2.
  \]

There are 845 variables and between 47,723 and 47,795 clauses per branch.
`generate_and_search.py` constructs the instances from first principles.
`manifest.json` records every orbit, reuse split, CNF digest, and compressed
and raw proof digest.

## Verification

Digest and deterministic-CNF reconstruction:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/first_lift_global_theorem/r0_two_core_refutations/verify_two_core_refutations.py
```

Full proof replay with official `drat-trim`:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/first_lift_global_theorem/r0_two_core_refutations/verify_two_core_refutations.py \
  --drat-trim /path/to/drat-trim
```

All 22 proofs must report `s VERIFIED`. Solver timeouts or silence are not
used anywhere in the conclusion.

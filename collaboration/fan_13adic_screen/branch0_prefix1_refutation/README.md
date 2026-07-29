# One exact prefix-local refutation in the fixed-link \(C_{17}\) ansatz

## Exact scope

This package proves only the following finite statement:

> The explicit 88-row prefix in `prefix.json` has no completion to a
> 228-row exact cover of the fixed cyclic-link \(C_{17}\)-quotient matrix.

It does **not** exclude another 88-row prefix, the full fixed-link
\(C_{17}\)-equivariant ansatz, \(LS(3,4,20)\), a simultaneous
thirteen-fan, or Erdős--Rosenfeld Problem #835.

## The \(8+40+40+140\) decomposition

The 228 quadruple orbits split according to their intersections with the
two fixed points \(L=17\) and \(\infty=18\):

\[
8\ (\text{both})+40\ (L\text{-only})+40\ (\infty\text{-only})
+140\ (\text{finite-only}).
\]

The 57 triple orbits split as \(1+8+8+40\) in the analogous way.
After choosing the eight both-fixed rows, the two 40-row layers separately
cover their own quadruple columns and fixed-point triple-colour demands.
Each selected row in either layer also consumes one finite
triple-colour demand.  The two layers are compatible exactly when those
80 consumed finite demands are distinct.

For the explicit compatible prefix recorded here, 80 of the 640 finite
demands are already covered.  The remaining finite-only problem therefore
has

\[
140+(640-80)=700
\]

exact-one target columns.  Removing finite candidates that collide with
the prefix leaves 1,016 variables.  Pairwise exact-one encoding gives the
17,046-clause `finite_completion.cnf`.

## Verification

Reconstruct the decomposition, prefix, candidates, and CNF byte for byte:

```text
python3 -B verify_prefix_refutation.py
```

Then independently replay the proof with `drat-trim`:

```text
./verify_drat.sh /path/to/drat-trim
```

The accepted official-checker transcript is in
`DRAT_TRIM_RECEIPT.txt`; `prefix.json` records the SHA-256 digests of
the CNF and both forms of the proof.

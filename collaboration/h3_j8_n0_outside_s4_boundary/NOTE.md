# Boundary search with one fixed exterior point and exterior \(S_4\)

## Result and strict scope

Normalize a \(\Delta=60\) four-cube on vertices \(0,\ldots,7\).  Fix exterior
vertex \(8\), and require invariance under every permutation of exterior
vertices \(9,\ldots,12\).  In the \(N=0\) branch, exact integer searches
independently replayed by CP-SAT and Gurobi eliminate these six subcases:

\[
\begin{array}{c|c}
\text{maximum positive cube value }m&
\text{maximum weight-two positive value }w\\ \hline
9&9\\
10&\text{unrestricted}\\
11&10\\
12&\text{unrestricted}\\
13&10\\
13&12.
\end{array}
\]

These are exact finite subcase eliminations, not a complete elimination of
the exterior-\(S_4\) model.  Thirteen branches remain unresolved:
\[
\begin{split}
&(8,8);\\
&(9,7),(9,8);\\
&(11,7),(11,8),(11,9),(11,11);\\
&(13,6),(13,7),(13,8),(13,9),(13,11),(13,13).
\end{split}
\]
Most importantly, fixing one exterior point and imposing \(S_4\) symmetry on
the other four is an additional ansatz, not a without-loss-of-generality
reduction.  This work does **not** eliminate unrestricted \(N=0\), prove the
\(j=8\to9\) lift, or solve Erdős--Rosenfeld Problem #835.

## Full orbit model

For a four-set \(Q\), retain its exact cube part, whether it contains vertex
\(8\), and only the number of points it contains from
\(\{9,10,11,12\}\).  The 715 four-sets give 256 variable orbits.  There are
130 triple-load orbits.  Expanding actual four-sets, with orbit
multiplicities retained, gives
\[
\sum_{Q\supset T}d_Q\le13
\]
for each representative triple \(T\).

For every representative \(S\) of sizes \(5,\ldots,11\), put
\(D_S=\sum_{Q\in\binom S4}d_Q\) and introduce a nonnegative integer \(N_S\).
The full exact equations are
\[
\begin{array}{c|c|c}
|S|&\text{number of orbits}&\text{equation}\\ \hline
5&381&2N_S+D_S=13\\
6&456&3N_S-D_S=39\\
7&456&4N_S+D_S=195\\
8&381&5N_S-D_S=325\\
9&256&6N_S+D_S=702\\
10&130&7N_S-D_S=546\\
11&46&8N_S+D_S=858.
\end{array}
\]
The CP-SAT script uses all 2,106 equations.

## Exact row reduction used by Gurobi

The Gurobi script stays within the restricted-license size limit without
weakening the integer model:

- The 381 size-five coefficient rows have rank 163 over
  \(\mathbb F_2\).  A rank basis enforces the parity equations.  The other
  rows retain \(D_S\le13\), which together with \(d_Q\ge0\) is exactly
  equivalent to \(2N_S+D_S=13\).  The affine right sides follow from the
  coefficient relations because every size-five row has odd row sum.
- The size-six, size-eight, and size-ten coefficient rows have ranks
  \(135,126,84\) over \(\mathbb F_3,\mathbb F_5,\mathbb F_7\),
  respectively.  Their recurrence conditions are homogeneous
  congruences, so rank bases are exact.
- The size-nine congruence modulo six follows from the size-five
  congruences modulo two and the size-six congruences modulo three.
  Nonnegativity of its count is automatic: summing the 84 triple-load
  bounds inside a nine-set gives \(4D_S\le13\binom93\), hence
  \(D_S\le273<702\).
- Every size-seven and size-eleven equation is retained.

Before cube symmetry breakers, the reduced model has 1,266 integer variables
and 1,360 constraints.

## Cube symmetry and exhaustive branch labels

Permuting the four matched cube pairs and swapping an even number of pairs
preserves the positive and negative cube cells.  This 192-element group is
transitive on the eight positive cells.  After moving a maximal positive
cell to \((0,2,4,6)\), its \(S_4\) stabilizer is transitive on the six
weight-two cells.  After moving their maximum to \((0,2,5,7)\), the remaining
\(S_2\times S_2\) stabilizer is transitive on the four crossing cells; the
scripts use \((0,3,4,7)\) as their maximum.  These breakers are therefore
without loss **inside the exterior-\(S_4\) ansatz**.

Eight nonnegative positive cells, each at most 13, sum to 60, so
\(8\le m\le13\).  If \(w\) is the maximum of the six weight-two cells, then
\[
60\le2m+6w,\qquad w\le m.
\]
This gives the complete finite \((m,w)\) partition checked by
`verify_model.py`.  The searches for \(m=10\) and \(m=12\) eliminate all
allowed \(w\) simultaneously.

## Reproduction

Audit the translation and reductions without solver dependencies:

```text
python3 -B verify_model.py
```

Replay a completed branch with the full-equation CP-SAT model:

```text
python3 -B search_cp_sat.py --seconds 60 --workers 1 \
  --reference-positive 13 --reference-weight-two 10
```

For hard branches, the independently audited exact row reduction is also
available to CP-SAT:

```text
python3 -B search_cp_sat_reduced.py --seconds 1800 --workers 8 \
  --reference-positive 8 --reference-weight-two 8
```

The \(m=8,w=8\) branch has only 71 symmetry-normalized assignments of its
eight positive cube values.  They may instead be checked one at a time, with
`--seconds` interpreted as the limit for each assignment:

```text
python3 -B search_cp_sat_reduced.py --seconds 300 --workers 8 \
  --enumerate-m8-cube-cases
```

Replay it with the independently implemented rank-reduced Gurobi model:

```text
python3 -B search_gurobi.py --seconds 60 --threads 1 \
  --reference-positive 13 --reference-weight-two 10
```

The completed outputs are in [`RUN_LOG.txt`](RUN_LOG.txt).  The solvers are
independent implementations, while the repository does not yet contain a
proof-checker-consumable UNSAT certificate.  Accordingly, the defensible
claim is an independently replayed exact finite subcase elimination with a
separately audited translation.

Time-limited, unknown, and deliberately interrupted searches are retained
separately in
[`NONTERMINAL_RUN_LOG.txt`](NONTERMINAL_RUN_LOG.txt).  They are telemetry only
and support no mathematical claim.

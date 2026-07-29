# Five-point star gluing for the first open case of ER #835

This note concerns only the first open case

\[
O_{16}=K(31,15),\qquad 17\text{ colors}.
\]

It studies a necessary color-moment relaxation.  Feasibility of the
relaxation is **not** a coloring of \(O_{16}\) and does not solve
Erdős--Rosenfeld Problem #835.

## 1. The tensor being glued

Start with the exact triple tensor \(q(x,y,z)\) and let

\[
F(x,y,z,w),\qquad w\sim z,
\]

be a free one-edge four-point tensor.  It is important that \(F\) remain a
variable: fixing the deterministic max-flow completion from the earlier
four-point witness would test only that one completion.

The next tensor is

\[
G(x,y,z,w_1,w_2),\qquad
w_1,w_2\in N(z),\quad w_1\ne w_2.
\]

It must forbid \(c(w_1)=c(w_2)\), have both one-neighbor marginals equal to
the same \(F\), and have re-based marginals such as
\(G(x,w_1,z,w_2)\) equal to that same global \(F\).

The orbit enumeration has

- 13,736 directed four-point geometric orbits and 133,005 allowed
  four-color partition variables;
- 48,015 five-point geometric orbits and 795,882 allowed five-color
  partition variables.

There are 928,887 raw variables.

### Why this is universal

If a \(17\)-color perfect-code partition of \(O_{16}\) existed, choose each
labelled geometric tuple uniformly and independently apply a uniform
permutation of the 17 color names.  The resulting orbit probabilities are
nonnegative and satisfy every equation below.  The triple equations force the
already certified tensor \(q\); \(F\) and \(G\) are left completely free.
Position reorders are identities of the same actual tuple moment, and re-based
equations are ordinary marginals of that moment.

Thus this is a necessary relaxation for every unrestricted \(k=16\) coloring,
not an ansatz about a special coloring.  Exact infeasibility would rule out
every coloring.  Exact feasibility has only the weaker, one-sided meaning
proved below.

## 2. An exact theorem: the ordinary star lift is automatic

Fix a geometric/color source triple \((x,y,z)\).  Expand a one-edge tensor
\(F\) from equality-pattern probabilities to probabilities of actual colors.
Index the resulting matrix by the 16 actual neighbors of \(z\) and the 16
colors different from \(c(z)\).

Every row sum is the mass of the fixed source pattern.  The one-edge
local-bijection equations say that every column sum is the same mass.
After scaling, the matrix is doubly stochastic.  By the
Birkhoff--von Neumann theorem it is a convex combination of permutation
matrices.  Sampling a permutation assigns all 16 neighbor colors
simultaneously and distinctly while preserving every one-slot marginal.
Average the decomposition over the geometric and color stabilizers to retain
orbit symmetry.

Therefore the following adds no obstruction, for **every** admissible free
\(F\):

1. two or all 16 neighbor slots at once;
2. distinct neighbor colors; and
3. only the original one-slot \(F\) marginals.

The genuinely new equations are the re-based four-point marginals.

## 3. All conditional position reorders

A generic four-point orbit has four admissible position permutations and a
generic five-point orbit has four.  Rare geometries contain another Odd-graph
edge or an alternate two-neighbor star, so they have additional conditional
reorders:

\[
\begin{array}{c|rrrr}
\text{four admissible permutations} &4&8&12&16\\
\text{number of orbits} &13328&386&16&6
\end{array}
\]

\[
\begin{array}{c|rrrrrr}
\text{five admissible permutations} &4&8&12&16&24&36\\
\text{number of orbits} &47024&416&430&120&18&7.
\end{array}
\]

Quotienting by every such permutation identifies 538,636 four-variable
links and 3,212,476 five-variable links, leaving 250,294 variable classes.
This closes a gap in a model that imposes only the generic
\(x\leftrightarrow y\), edge-reversal, and
\(w_1\leftrightarrow w_2\) symmetries.

In the full quotient, one re-based projection implies the other three:
\(x\leftrightarrow y\) exchanges drop-\(x\) and drop-\(y\), while
\(w_1\leftrightarrow w_2\) exchanges the two neighbor orders.

## 4. Exact feasibility certificate

The strongest full-reorder, free-\(F\), re-based LP has

\[
250294\text{ variables},\quad
441260\text{ equalities},\quad
2961055\text{ nonzero coefficients}.
\]

HiGHS IPM followed by crossover produced a valid floating basis.  SoPlex then
read the exact numerator/denominator LP, used that basis, and was run with
zero rational feasibility and optimality tolerances, exact checking, and
forced rational factorization.  It reported

```text
Max/sum bound violation: 0 / 0
Max/sum row violation:   0 / 0
```

The resulting rational point has 93,581 positive entries and SHA-256

```text
8949df7fdb457e250b7426e7e7660e4efa59e37ba102e5bd2fee4e1607c9aec9
```

The independent standard-library verifier regenerated the geometry and
checked, over `Fraction`,

- nonnegativity of every listed rational entry;
- all four re-based projections explicitly, not just one symmetry
  representative;
- 441,905 exact equalities; and
- 5,118,391 combined nonzero rational coefficients.

Its terminal result was

```text
{'status': 'PASS',
 'scope': 'exact five-point necessary relaxation only; not a coloring and not a solution of ER #835',
 'variables': 250294,
 'positive_certificate_variables': 93581,
 'checked_equalities': 441905,
 'checked_nonzero_coefficients': 5118391,
 'solution_sha256': '8949df7fdb457e250b7426e7e7660e4efa59e37ba102e5bd2fee4e1607c9aec9'}
```

The normalized exact LP used for basis transfer has SHA-256

```text
7aca37136e936f23583fea41ae0a71066f7c6f31f6baea34e480edcd4a9401b7
```

The equivalent gcd row-scaled exact LP has SHA-256

```text
99ef295f4657e1670fbce6f295b8d93fbb5c3b1352a9b080c6385fcb6d21fead
```

Therefore the full free-\(F\), full-special-reorder, re-based five-point
necessary relaxation is **exactly feasible**.  This rigorously rules out this
five-point LP as an obstruction.  It does not construct a coloring, does not
settle the existence of a coloring, and does not solve ER #835.

## 5. Reproduction

Verify the supplied rational certificate:

```bash
python3 evidence/verify_five_point_full_reorder_exact.py
```

To regenerate the normalized exact LP used by SoPlex:

```bash
python3 evidence/solve_five_point_star_gluing_lp.py \
  --stage drop-y-one \
  --normalized-rebase-rows \
  --write-exact-lp evidence/five_point_full_reorder_exact.lp \
  --no-solve
```

Generate a current HiGHS crossover basis and convert it to MPS BAS:

```bash
python3 evidence/export_five_point_highs_basis.py \
  --basis evidence/five_point_full_reorder_highs.bas \
  --solution evidence/five_point_full_reorder_highs.sol

python3 evidence/convert_highs_basis_to_soplex.py \
  evidence/five_point_full_reorder_highs.bas \
  evidence/five_point_full_reorder_soplex.bas
```

Run strict exact rational factorization:

```bash
soplex --readmode=1 --solvemode=2 -s0 \
  --readbas=evidence/five_point_full_reorder_soplex.bas \
  -f0 -o0 -l0 --int:checkmode=2 \
  --bool:forcebasic=true --bool:ratfac=true --bool:ratfacjump=true \
  -c -X=evidence/five_point_full_reorder_exact_seeded_strict.sol \
  evidence/five_point_full_reorder_exact.lp
```

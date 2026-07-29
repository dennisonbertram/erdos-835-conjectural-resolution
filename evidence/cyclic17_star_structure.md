# Exact structure of the centre-0 cyclic Wallis star

This note concerns only one necessary fourteen-row star in the fixed-Wallis,
\(\mathbb Z_{17}\)-equivariant radius-five ansatz.  It is not a star witness,
not an infeasibility proof, and not a result for the unrestricted
Erdős--Rosenfeld problem 835.

## 1. Permutation form

Fix Wallis square \(0\).  For moving-triple orbit \(k\), let \(A_k\) be the
phases \(s\in\mathbb Z_{17}\) for which the translated triple \(T_k+s\)
avoids the colour-zero matching \(M_0\).  Exactly three phases are forbidden,
so \(|A_k|=14\).

The outer rows are \(j=1,\ldots,14\).  A primary choice \(x_{jks}\) exists
exactly when \(s\in A_k\) and \(T_k+s\) also avoids \(M_j\).  The cell
equations choose one phase for each \((j,k)\), while the cross equations
choose one row for each \((k,s)\), \(s\in A_k\).  Consequently, for every
orbit \(k\), a star is exactly a permutation

\[
  j\longmapsto s_{j,k}
  \quad\text{from }\{1,\ldots,14\}\text{ onto }A_k,
\]

subject to the fourteen independent residual-triangle-decomposition
conditions on the rows.

Among the \(40\cdot14=560\) centre-allowed phase slots, 112 translated
triples have one forbidden outer row and 448 have three.  Hence the number
of primary choices is

\[
  112(14-1)+448(14-3)=6384.
\]

The exact-cover matrix has 560 cell rows, 1,680 residual-edge rows, and 560
cross-phase rows, for 2,800 equations in all.

## 2. Pairwise collision matrices

Let \(\mathcal R_j\) be the family of all exact residual decompositions for
row \(\{0,j\}\).  Represent \(R\in\mathcal R_j\) by its forty-slot set

\[
  S(R)=\{(k,s_{j,k}):0\leq k<40\}\subseteq
  \{(k,s):s\in A_k\}.
\]

For candidates \(R\in\mathcal R_j\) and \(R'\in\mathcal R_\ell\), define

\[
  C^{j\ell}_{R,R'}=|S(R)\cap S(R')|.
\]

Then a centre-0 star exists if and only if one can choose
\(R_j\in\mathcal R_j\) for all fourteen outer rows with every pairwise
collision equal to zero.  Since the fourteen chosen sets have total size
\(14\cdot40=560\), pairwise disjointness is equivalent to partitioning all
560 centre-allowed slots.

For any fourteen exact rows, let \(n_{k,s}\) be the multiplicity of slot
\((k,s)\).  The exact total collision count and occupied-slot count are

\[
  Q=\sum_{j<\ell}C^{j\ell}_{R_j,R_\ell}
    =\sum_{k,s}\binom{n_{k,s}}2,\qquad
  D=\sum_{k,s}\mathbf 1_{n_{k,s}>0}.
\]

Thus \(Q\geq560-D\), with equality precisely when every multiplicity is at
most two.  The star condition is \(Q=0\), equivalently \(D=560\).

A finite row pool therefore gives an exact finite 14-partite clique or
quadratic-assignment master.  A positive optimum in such a finite pool is
only pool-relative and is not an obstruction for the full row families.

Every one of the \(\binom{14}{2}=91\) two-row subsystems is feasible.  The
standalone certificate
`cyclic17_star_pairwise_compatibility_certificate.json` contains, for each
outer pair, two exact residual decompositions with zero common phase slots.
The independent verifier checks 182 exact rows and all 91 zero-collision
conditions.  Its SHA-256 is

```text
8716e8f53cb0438cf18c6a00d324241af606e48b32dd68821cca60e2c9b30389
```

Thus there is no obstruction supported on only two outer rows.  This does
not imply that the 91 pairwise choices can be made consistently from one
common set of fourteen rows.

The same conclusion holds for every three-row subsystem.  The standalone
certificate `cyclic17_star_triple_compatibility_certificate.json` contains
one collision-free triple of exact residual decompositions for each of the
\(\binom{14}{3}=364\) outer triples.  The independent verifier reconstructs
and checks all 1,092 rows and every within-record collision count.  Its
SHA-256 is

```text
1f52a75c7eeae8050f293a9f52e54e9aea63eb33e93dfe0c13ad06748ac03fd5
```

Thus there is no obstruction supported on at most three outer rows.  Again,
the rows may differ between triple records, so this is not a compatible
fourteen-row selection.  The pairwise certificate rows can be deduplicated
by outer index and used directly as a retained-row seed for the finite
fourteen-partite master; the triple certificate supplies a much richer
verified seed pool.  A failure to find a fourteen-row clique in either
finite pool would remain pool-relative.

## 3. A proof-safe global master and dual

There is also a proof-safe column-generation formulation.  Give every exact
row \(R\in\mathcal R_j\) a variable \(\lambda_{j,R}\).  The maximum number of
pairwise-disjoint row solutions is the set-packing program

\[
\begin{aligned}
 \max\;&\sum_{j,R}\lambda_{j,R}\\
 \text{s.t. }&
 \sum_{R\in\mathcal R_j}\lambda_{j,R}\leq1 &&(j=1,\ldots,14),\\
 &\sum_{j,R:(k,s)\in S(R)}\lambda_{j,R}\leq1 &&((k,s)\text{ a slot}),\\
 &\lambda_{j,R}\geq0.
\end{aligned}
\]

An integral value 14 is exactly a star.  Its LP dual assigns nonnegative
weights \(a_j\) to row families and \(b_{k,s}\) to slots, with

\[
 a_j+\sum_{(k,s)\in S(R)}b_{k,s}\geq1
 \quad\text{for every }R\in\mathcal R_j.
\]

Therefore a rational dual solution with
\(\sum_j a_j+\sum_{k,s}b_{k,s}<14\) would rigorously exclude the star.
All infinitely stated dual inequalities reduce to fourteen independent
weighted exact-row pricing problems.  For a portable certificate, each
pricing lower bound must itself be proved exactly; heuristic or timed-out
pricing is not enough.

## 4. Complete linear counting kernel

There are three transparent families of integer dependencies among the
2,800 exact-one equations.

1. For each outer row \(j\) and cyclic edge difference \(d=1,\ldots,8\),
   summing the fifteen residual-edge equations of difference \(d\) equals
   the orbit-cell sum weighted by the number of difference-\(d\) edges in
   the representative triple.  This gives \(14\cdot8=112\) balances.
2. For each orbit, the sum of its fourteen cross-phase equations equals the
   sum of its fourteen outer-row cell equations.  This gives 40 balances.
3. For each of the 128 moving edges outside \(M_0\), summing all cross slots
   whose triple contains that edge equals the sum of that residual-edge
   equation over every eligible outer row.  This gives 128 balances.

These 280 explicit dependencies have rank 272 over each of
\(\mathbb F_3,\mathbb F_5,\mathbb F_{17}\); there are eight relations among
them.  Independently, the \(2800\times6384\) incidence matrix has rank 2528,
so its left nullity is exactly 272.  Thus these elementary balances span the
entire linear counting kernel in each tested odd characteristic.  They
produce no augmented contradiction and no positive collision lower bound.
Any successful obstruction must therefore use integrality or genuinely
nonlinear compatibility, not another linear recombination of the exact-one
rows over those fields.

## Reproduction

```sh
/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python \
  -B evidence/audit_cyclic17_star_structure.py
```

The audit reconstructs all choices and equations, verifies every displayed
dependency over the integers, and independently checks the stated modular
ranks.

Verify the complete two-row certificate with:

```sh
/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python \
  -B evidence/verify_cyclic17_star_pairwise_compatibility.py \
  evidence/cyclic17_star_pairwise_compatibility_certificate.json
```

Verify the complete three-row certificate with:

```sh
/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python \
  -B evidence/verify_cyclic17_star_triple_compatibility.py \
  evidence/cyclic17_star_triple_compatibility_certificate.json
```

# A row-sum obstruction for a representable (LS(3,4,20))

This note concerns the (p=17) descendant of the principal-Pfaffian
ansatz: an alternating (20\times20) matrix (A=(a_{ij})) over
(mathbb F_{17}) whose principal 4-Pfaffians

\[
 P_{ijkl}=a_{ij}a_{kl}-a_{ik}a_{jl}+a_{il}a_{jk}
\tag{1}
\]

are required to be all of (mathbb F_{17}) on every 3-star.  Its zero
fibre would be an (S(3,4,20)), and its full fibres would be an
(LS(3,4,20)).  The argument below applies more generally with
(20=p+3).

It is a necessary-condition result, not a classification or a proof that
such a matrix cannot exist.

## The first star moment forces zero row sums

Write

\[
 s_i=\sum_{u=1}^{p+3}a_{iu}.
\tag{2}
\]

For distinct (i,j,k), use (1) with the fourth index (u), including
the three repeated-index terms (which are zero).  Direct summation gives

\[
 \sum_uP_{ijku}
  =a_{ij}s_k-a_{ik}s_j+a_{jk}s_i.
\tag{3}
\]

If the 3-star is rainbow, its non-repeated (p) values are exactly
(mathbb F_p), whose sum is zero.  Hence the right-hand side of (3)
vanishes for every triple, equivalently

\[
 A\wedge s=0.
\tag{4}
\]

If (s\ne0), choose (t) with (s_t\ne0).  Applying (3) to
(i,j,t) gives

\[
 a_{ij}=\frac{a_{it}s_j-a_{jt}s_i}{s_t}.
\tag{5}
\]

Thus (A) is a decomposable 2-form, so it has rank at most two and every
4-Pfaffian in (1) is zero.  That contradicts a rainbow 3-star.  Therefore
every representable (LS(3,4,p+3)), in particular a putative one at
(p=17), must satisfy the strict linear constraint

\[
 \boxed{A\mathbf1=0.}
\tag{6}
\]

For (p=17), this reduces the genuine algebraic search from arbitrary
alternating (20\times20) matrices to alternating forms on the
19-dimensional quotient by the all-ones vector.  It does not cause a
contradiction by itself: such forms can have rank 18 and nonzero
4-Pfaffians.

## Second moment

The next rainbow identity is also exact.  Put

\[
 G_{rs}=\sum_u a_{ru}a_{su}=(AA^T)_{rs},
 \qquad w_{ijk}=(a_{jk},-a_{ik},a_{ij}).
\tag{7}
\]

Since the sum of squares of (mathbb F_p) is zero for odd (p>3), every
rainbow star must obey

\[
 w_{ijk}^{T}G[\{i,j,k\}]w_{ijk}=0.
\tag{8}
\]

Equations (6) and (8), together with the requirement that the seventeen
values (P_{ijku}) be pairwise distinct, are a smaller exact polynomial
system for the (p=17) search.  This is the useful surviving formulation;
the zero-fibre equations alone are insufficient, because every rank-two
alternating form makes *all* 4-Pfaffians zero and hence vanishes on any
chosen (S(3,4,20)) without yielding a large set.

## Exact checks

The companion verifier checks both (3) and (8) on independently seeded
random alternating matrices for (p=5,7,11,17):

```bash
python3 evidence/verify_pfaffian_four_star_moments.py
```

The proof of (3) is the displayed expansion.  Equation (8) follows by
writing (P_{ijku}=w_{ijk}\cdot(a_{iu},a_{ju},a_{ku})) and summing its
square over (u).

## Full star polynomial, and the limit of low moments

For a genuine \(p=17\) solution, the entire length-20 vector

\[
 b_{ijk}=(P_{ijku})_{u=1}^{20}=w_{ijk}^{T}A
\tag{9}
\]

has three forced zero coordinates (at \(i,j,k\)) and its other seventeen
coordinates are exactly \(\mathbb F_{17}\).  Equivalently,

\[
 \prod_{u=1}^{20}(z-P_{ijku})=z^3(z^{17}-z)=z^{20}-z^4.
\tag{10}
\]

Thus every elementary symmetric function of this row is zero except

\[
 e_{16}(b_{ijk})=-1,
\tag{11}
\]

and the power sums are zero through degree fifteen, while

\[
 \sum_u P_{ijku}^{16}=-1.
\tag{12}
\]

The first and second of these equations are (3) and (8).  They do not
by themselves force either \(A^2=0\) or rank at most two.  The companion
countermodel checker constructs two exact \(20\times20\) examples over
\(\mathbb F_{17}\), both with \(A\mathbf1=0\) and satisfying the degree-1
and degree-2 star equations for every triple:

1. A rank-two form with \(A^2\ne0\) and all 4-Pfaffians zero.
2. A rank-four form \(A=UCU^T\), where the four columns of \(U\) are
   pairwise orthogonal isotropic sum-zero vectors.  It has \(A^2=0\) but
   256 nonzero principal 4-Pfaffians.

```bash
python3 evidence/verify_pfaffian_moment_countermodels.py
```

Consequently any contradiction must use at least the high-degree
condition (11)/(12), or the pairwise-distinct requirement itself, together
with the fact that the vectors in (9) arise from the same alternating
form.  These countermodels do **not** satisfy (10), so they are not
counterexamples to the principal-Pfaffian colouring problem.

## Scope

No representable (S(3,4,20)), no representable (LS(3,4,20)), and no
general impossibility theorem has been obtained here.  The result rules out
only the nonzero-row-sum portion of the arbitrary principal-Pfaffian
family and supplies exact constraints for a targeted (p=17) solver.

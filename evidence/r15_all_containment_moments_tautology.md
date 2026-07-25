# Every containment moment at \(r=15\) gives the same parity tautology

## Result and scope

Let \(B,C\) be two mates of a fixed \(S(14,15,31)\), represented by
their two tilings of 16-sets.  For \(0\le i\le15\), let \(a_i\) count
ordered cross-pairs of tiling sets whose intersection has size
\(16-i\).  Thus
\[
a_0=h=|B\cap C|,\qquad h= b-t,
\]
where \(b=17\,678\,835\) and
\(t=\#\{P:w_B(P)\ne w_C(P)\}\).

The full family of constant-containment identities, at every level
from 17-sets through the whole 31-set, implies
\[
a_i\equiv 1+h\equiv t\pmod2
\qquad(1\le i\le15). \tag{1}
\]

Consequently no higher containment moment in this family improves on
the second moment: each nontrivial cross-distance count has exactly
the parity one is trying to prove.  Equation (1) is a rigorous closure
of this moment route only.  It does not exclude an integral
involution, a nonlinear identity, or another global argument that
independently proves one of these counts even.

## Inclusion matrices

The ground set has size
\[
v=2r+1,
\]
and a tiling is an incidence vector \(x\) on the
\((r+1)\)-subsets \(H\).  For \(1\le s\le r\), let \(N_s\) be the
inclusion matrix from \((r+1)\)-sets to \((r+1+s)\)-sets:
\[
(N_s)_{Y,H}=[H\subseteq Y].
\]

Every \((r+2)\)-set contains exactly one selected \(H\).  Counting
these \((r+2)\)-sets inside a fixed \((r+1+s)\)-set \(Y\), every
selected \(H\subseteq Y\) is counted \(s\) times.  Hence every row of
\(N_sx\) has the constant value
\[
c_s=\frac1s\binom{r+1+s}{r+2}
    =\frac1{r+2}\binom{r+1+s}{r+1}. \tag{2}
\]

Let \(A_i\) be the relation matrix on \((r+1)\)-sets defined by
\[
(A_i)_{H,K}=[\,|H\cap K|=r+1-i\,].
\]
If \(|H\cap K|=r+1-i\), their union has size \(r+1+i\), so the number
of \((r+1+s)\)-sets containing both is
\(\binom{r-i}{s-i}\).  Therefore, over the integers,
\[
N_s^{\mathsf T}N_s
=\sum_{i=0}^{s}\binom{r-i}{s-i}A_i. \tag{3}
\]

For two tilings \(x,y\), put \(a_i=x^{\mathsf T}A_i y\).  Equations
(2)--(3) give the complete triangular moment system
\[
\sum_{i=0}^{s}\binom{r-i}{s-i}a_i
=c_s^2\binom{2r+1}{r+1+s},
\qquad 1\le s\le r. \tag{4}
\]

No approximation or relaxation is used in (4).

## Solving the parity system at \(r=15\)

Now \(r=15\), so \(r+1=16=2^4\) and
\(v=31=2^5-1\).

First, every right side of (4) is odd.  By (2),
\[
c_s=\frac1{17}\binom{16+s}{16}.
\]
The divisor 17 is odd, and Lucas's theorem shows
\(\binom{16+s}{16}\) is odd for \(1\le s\le15\).  Lucas also shows
that every \(\binom{31}{j}\) is odd.  Thus (4) reduces modulo 2 to
\[
\sum_{i=0}^{s}\binom{15-i}{s-i}a_i=1. \tag{5}
\]

We solve (5) inductively.  For \(s=1\), it gives
\(a_1=1+a_0\).  Suppose \(a_i=1+a_0\) for
\(1\le i<s\).  The interior coefficient sum is
\[
\sum_{i=1}^{s-1}\binom{15-i}{s-i}
=\binom{16}{s}-\binom{15}{s}-1. \tag{6}
\]
For \(1\le s\le15\), Lucas gives
\[
\binom{16}{s}\equiv0,\qquad
\binom{15}{s}\equiv1\pmod2,
\]
so (6) is even.  The coefficient
\(\binom{15}{s}\) of \(a_0\) is odd, while the coefficient of \(a_s\)
is one.  Equation (5) therefore gives
\[
a_s=1+a_0.
\]
This proves (1) for every \(s\).

Finally,
\[
b=\frac1{15}\binom{31}{14}
\]
is odd: its numerator is odd by Lucas and its divisor is odd.  Hence
\[
1+a_0=1+h=1+(b-t)=t\pmod2.
\]

## Interpretation in the original block systems

Taking complements turns a tiling 16-set into its corresponding
15-block.  If two tiling sets meet in \(16-i\) points, their
complementary blocks meet in \(15-i\) points.  Consequently
\[
a_i
=\#\{(Q,R)\in B\times C:|Q\cap R|=15-i\}.
\]
The theorem says that every non-common block-intersection class,
including the disjoint class \(i=15\), has parity \(t\).

In particular:

- \(i=1\) is the first containment moment;
- \(i=2\) is the second-moment count whose exceptional part was
  denoted \(E_3+X_3\);
- \(i=3,\dots,15\) cannot rescue the method, because their parities
  are the same unknown \(t\).

The same calculation also works at the finite control \(r=3\).
It should not be stated for every Mersenne \(r\) without checking the
existence divisibilities in (2): for example, at \(r=7,s=3\), (2)
would give \(c_3=\binom{11}{9}/3=55/3\), so the required tiling
parameters are already impossible.  The theorem asserted here is the
\(r=15\) statement, with \(r=3\) only as a valid small control.

Validator: `verify_r15_all_containment_moments.py`.

# No nontrivial tensor solution at \(p=17\)

This note rules out a precise separable construction for the modular
power-kernel formulation of the \(k=16\) case.  It does not rule out a
genuinely entangled function.

## Setup

Partition a 32-point set as
\[
X=X_1\sqcup\cdots\sqcup X_s,
\]
choose positive integers \(r_i\) with
\[
\sum_i r_i=16,
\]
and let
\[
f_i:\binom{X_i}{r_i}\longrightarrow\mathbb F_{17}.
\]
Define \(f:\binom X{16}\to\mathbb F_{17}\) by
\[
f(S)=
\begin{cases}
\prod_i f_i(S\cap X_i),&
 |S\cap X_i|=r_i\text{ for every }i,\\
0,&\text{otherwise}.
\end{cases}
\tag{1}
\]
Empty or unused factors can be removed; allowing them does not change the
argument below.

Write \(D_{n,r}=W_{r-1,r}(n)\) for the down-incidence map.

## Theorem

If \(f\ne0\) and
\[
D_{32,16}(f^a)=0
\qquad(1\le a\le15),
\tag{2}
\]
then \(s=1\), \(|X_1|=32\), and \(r_1=16\).  Thus (1) gives no genuine
tensor decomposition of a solution.

## Proof

Put \(n_i=|X_i|\).  Since \(f\ne0\), every factor \(f_i\) has a nonzero
coordinate.

Fix \(i\), a set \(T\in\binom{X_i}{r_i-1}\), and, for every \(j\ne i\),
choose \(A_j\in\binom{X_j}{r_j}\) with \(f_j(A_j)\ne0\).  Apply (2) to
the 15-set
\[
R=T\cup\bigcup_{j\ne i}A_j.
\]
Only extensions of \(R\) by a point of \(X_i\) can enter the support in
(1).  Consequently
\[
0=D_{32,16}(f^a)(R)
 =\left(\prod_{j\ne i}f_j(A_j)^a\right)
   D_{n_i,r_i}(f_i^a)(T).
\]
The prefactor is nonzero, so
\[
D_{n_i,r_i}(f_i^a)=0
\qquad(1\le a\le15)
\tag{3}
\]
for every factor.

We next show \(n_i\ge2r_i\).  If \(n_i<2r_i\), complementing row and
column indices identifies the transpose of \(D_{n_i,r_i}\) with
\[
W_{n_i-r_i,n_i-r_i+1}(n_i).
\]
Wilson's diagonal factors for this matrix are
\[
n_i-r_i+1-j,\qquad 0\le j\le n_i-r_i.
\]
They lie between \(1\) and \(r_i\le16\), so none vanishes modulo 17.
The transpose therefore has full row rank over \(\mathbb F_{17}\), and
\(D_{n_i,r_i}\) has zero kernel.  This contradicts (3) for \(a=1\).
Hence \(n_i\ge2r_i\).

Summing gives
\[
32=\sum_i n_i\ge2\sum_i r_i=32.
\]
Equality holds throughout:
\[
n_i=2r_i\qquad\text{for every }i.
\tag{4}
\]

Now fix an \((r_i-1)\)-set in \(X_i\).  Its \(r_i+1\) extensions have
values \(x_1,\ldots,x_{r_i+1}\).  By (3),
\[
\sum_\ell x_\ell^a=0\qquad(1\le a\le15). \tag{5}
\]
For \(z\in\mathbb F_{17}\), let \(m_z\) be the multiplicity of \(z\).
The \(15\times16\) matrix
\[
\bigl(z^a\bigr)_{\substack{1\le a\le15\\z\in\mathbb F_{17}^{\times}}}
\]
has rank 15; its nullspace is spanned by the all-one vector.  Equation
(5) therefore says that the sixteen multiplicities \(m_z\), for
\(z\ne0\), are all congruent modulo 17.

Because
\[
0\le m_z\le r_i+1\le17,
\]
a star with a nonzero value has at least sixteen nonzero entries, unless
all seventeen entries have one repeated nonzero value.  In particular,
if \(r_i\le14\), every entry of every star is zero.  Then \(f_i=0\), a
contradiction.  Thus every nonzero factor has
\[
r_i\ge15.
\]

Since every positive \(r_i\) is at least 15 and the \(r_i\) sum to 16,
there can be only one factor.  For completeness, the apparent borderline
attempt to use a size-15 factor and leave one selected point for a second
factor also fails directly: (4) would make the latter a function on the
two singleton subsets of a two-point set.  If its values are \(u,v\),
equations (3) for powers one and two give
\[
u+v=0,\qquad u^2+v^2=0.
\]
As \(2\ne0\) in \(\mathbb F_{17}\), these force \(u=v=0\), making
\(f=0\).

Only the single factor \(r_1=16,n_1=32\) remains.  This is the original,
undecomposed problem. \(\square\)

## Scope

The proof covers fixed-multidegree product constructions, including
ordinary tensor products of local inclusion-kernel codewords.  It does not
cover sums of many tensor terms, nonlinear couplings between factors, or
other genuinely nonseparable constructions.

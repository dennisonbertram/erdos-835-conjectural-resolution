# The saturated support lattice: exact 2-adic status

Date: 2026-07-24.

This note separates three objects that must not be conflated in the
fixed-base parity attack:

\[
\ker_{\mathbf F_2}N,\qquad
\overline{\ker_{\mathbf Z}N},\qquad
\ker_{\mathbf Z}(H+I).
\]

Here \(A\) is an \(S(r-1,r,2r+1)\), \(\mathcal O\) is the set of
\(r\)-sets outside \(A\), \(N=W_{r-1,r}[* ,\mathcal O]\), and \(H\) is
the subgraph of \(O_{r+1}=KG(2r+1,r)\) induced by \(\mathcal O\).
All assertions below are checked by
`verify_saturated_support_lattice.py`.

## 1. The exact integral object

Extend \(z\in\mathbf Z^{\mathcal O}\) by zero on \(A\).  If \(Nz=0\),
then every lower inclusion sum also vanishes: for \(J\) of size
\(j\le r-1\),
\[
 (r-j)\sum_{K\supseteq J}z_K
 =\sum_{\substack{F\supseteq J\\|F|=r-1}}
   \sum_{K\supseteq F}z_K=0.
\]
For \(P\in A\), inclusion-exclusion therefore gives
\[
 \sum_{K\cap P=\varnothing}z_K
 =\sum_{J\subseteq P}(-1)^{|J|}
   \sum_{K\supseteq J}z_K
 =(-1)^r z_P=0.
\]
Thus the sphere-sum equations follow over the integers from \(Nz=0\).
The support-restricted lattice is exactly
\[
 \Lambda(A)=\ker_{\mathbf Z}N.
\tag{1}
\]

Let \(B\) be the \(A\)-by-\(\mathcal O\) matrix whose row at \(P\)
indicates the outside blocks disjoint from \(P\).  The Odd-graph equations
give
\[
\boxed{\Lambda(A)=\ker_{\mathbf Z}(H+I)\cap\ker_{\mathbf Z}B.}
\tag{2}
\]
For completeness, let \(D\) be the full Odd-graph adjacency matrix and
let \(J\) be the Johnson adjacency matrix on all \(r\)-sets.  Direct
common-neighbour counting and facet counting give
\[
 D^2=(r+1)I+J,\qquad W^{\mathsf T}W=rI+J,
\]
so \(W^{\mathsf T}W=D^2-I\).  If \(Wz=0\), the preceding
inclusion-exclusion identity gives \(Dz=(-1)^rz=-z\).  Conversely,
\(Dz=-z\) gives \(W^{\mathsf T}Wz=0\), hence \(Wz=0\).  Extending an
outside vector by zero on \(A\), its \(D+I\) equations are exactly
\((Bz,(H+I)z)=0\), which proves (2).

The \(Bz=0\) clause cannot be dropped.  At \(r=5\),
\[
\dim\ker_{\mathbf Z}(H+I)=88,\qquad
\dim\Lambda(A)=77,
\]
and the sphere map has rank \(11\) on the former kernel.  The equality
\(\ker(H+I)=\Lambda(A)\) at \(r=3\) is an exceptional small-case
coincidence.

## 2. Saturation and the stable binary kernel

For an arbitrary integer matrix \(N\) with \(n\) columns and rational
rank \(\rho\), put
\[
 L=\ker_{\mathbf Z}N,\qquad
 R^{\rm sat}=(\operatorname{row}_{\mathbf Q}N)\cap\mathbf Z^n.
\]
Both \(L\) and \(R^{\rm sat}\) are primitive sublattices.  Reduction
modulo two is injective on \(L/2L\) and on
\(R^{\rm sat}/2R^{\rm sat}\): for example, if
\(z\in L\cap2\mathbf Z^n\), then \(z=2y\) and \(Ny=0\), so \(z\in2L\).
Consequently
\[
 \boxed{\bar L
 =\bigl(\overline{R^{\rm sat}}\bigr)^\perp
 \subseteq\ker_{\mathbf F_2}N.}
\tag{3}
\]
Indeed one inclusion follows from integral orthogonality, and both sides
have dimension \(n-\rho\).

Equivalently, \(\bar L\) is the **stable 2-adic kernel**: it consists of
the binary words \(u_0\) for which there are binary digits
\(u_1,u_2,\ldots\) satisfying, for every \(s\ge1\),
\[
 N\left(\widetilde u_0+2\widetilde u_1+\cdots+
 2^{s-1}\widetilde u_{s-1}\right)\equiv0\pmod {2^s}.
\tag{4}
\]
Smith normal form makes the loss from the ordinary binary kernel exact:
\[
\boxed{
\dim\bigl(\ker_{\mathbf F_2}N/\bar L\bigr)
=\rho-\operatorname{rank}_{\mathbf F_2}N,
}
\tag{5}
\]
the number of nonzero even Smith factors.  Therefore a word in the broad
binary facet/sphere kernel is not evidence about the integral parity
conjecture unless its full 2-adic liftability is established.

There is a concrete first lifting obstruction.  Write
\[
K=\ker_{\mathbf F_2}\bar N,\qquad
K^\ell=\ker_{\mathbf F_2}\bar N^{\mathsf T}.
\]
For \(u\in K\), choose its \(0/1\) lift \(\widetilde u\) and define
\[
\beta(\lambda,u)
=\lambda^{\mathsf T}\frac{N\widetilde u}{2}\pmod2
\qquad(\lambda\in K^\ell).
\tag{6}
\]
Changing an integral lift by \(2y\) changes the half-image by \(Ny\), so
the pairing with \(K^\ell\) is unchanged.  The equation
\(N(\widetilde u+2y)=0\pmod4\) is soluble exactly when
\(\beta(\lambda,u)=0\) for every \(\lambda\).

In both exact cases, the first obstruction already removes every
nonstable word:
\[
\begin{array}{c|c|c|c}
r&\dim K&\operatorname{rank}\beta&\dim\ker\beta=\dim\bar\Lambda\\ \hline
3&13&6&7\\
5&186&109&77.
\end{array}
\]
Equivalently, all nonzero even Smith factors have 2-adic valuation exactly
one; none is divisible by four.  Thus in these cases
\[
\boxed{\bar\Lambda=\ker\beta,}
\tag{7}
\]
an exact mod-four characterization rather than an infinite lifting test.
Whether the same one-step collapse follows at \(r=15\) from the design
axioms is an open, sharply formulated intermediate question.

## 3. The quadratic form

Every \(z\in\Lambda(A)\) has even norm, since summing the facet equations
counts each coordinate \(r\) times and \(r\) is odd.  Hence
\[
 q(\bar z)=\frac{z\cdot z}{2}\pmod2
\tag{8}
\]
is well-defined on \(\bar\Lambda=\Lambda/2\Lambda\), with polar form
\[
 q(u+v)-q(u)-q(v)=u\cdot v\pmod2.
\tag{9}
\]
The claim that \(\Lambda\) is 4-even is precisely \(q=0\), not merely a
claim about \(\ker_{\mathbf F_2}N\).

The exact small cases are:

| \(r\) | \(\operatorname{rank}_{\mathbf Q}N\) | \(\operatorname{rank}_2N\) | \(\dim\bar\Lambda\) | binary/stable loss | polar rank | radical | \(q\) |
|---:|---:|---:|---:|---:|---:|---:|:---|
| 3 | 21 | 15 | 7 | 6 | 0 | 7 | identically zero |
| 5 | 319 | 210 | 77 | 109 | 32 | 45 | nonzero |

At \(r=5\), \(q\) vanishes on the 45-dimensional radical and descends to
a nondegenerate 32-dimensional quadratic space of Arf invariant \(0\).
Thus the failure is a genuine hyperbolic quotient, not a lone anomalous
vector.  It also explains how the nonlinear family of actual mate
differences can lie in a totally singular slice while the full saturated
lattice fails to be 4-even.

There is a sharper representation-theoretic compression.  Let \(C\) be
the reduction of the **full** integral trade lattice
\(\ker_{\mathbf Z}W_{r-1,r}\), let \(\operatorname{rad}C\) be the radical
of its dot product, and let
\[
S=C/\operatorname{rad}C.
\]
The exact small cases give:

| \(r\) | \(\dim C\) | \(\dim\operatorname{rad}C\) | \(\dim S\) | Arf \(S\) | \(\dim\operatorname{im}(\bar\Lambda\to S)\) |
|---:|---:|---:|---:|---:|---:|
| 3 | 14 | 6 | 8 | 0 | 4 |
| 5 | 132 | 100 | 32 | 0 | 32 |

At \(r=3\), the four-dimensional image of \(\bar\Lambda\) is a maximal
totally singular subspace of the hyperbolic eight-space \(S\).  At
\(r=5\), the image is all of the hyperbolic 32-space, so its polar form
has rank 32 and 4-evenness is impossible.  The dimensions \(8=2^3\) and
\(32=2^5\) agree with the expected basic-spin quotient of the two-row
Specht/trade module.  This last general identification is a
representation-theoretic route, not proved by the present finite
certificate.

Accordingly, the clean \(r=15\) target is: identify the corresponding
\(2^{15}\)-dimensional nondegenerate quotient and prove that the image of
the support kernel is totally singular (plausibly a \(2^{14}\)-dimensional
Lagrangian).  This formulation precisely distinguishes the \(r=3\)
mechanism from the \(r=5\) counterexample.

There is an important distinction between the whole support lattice and
the actual nonlinear family of mate differences.  Exhaustive exact-cover
enumeration gives:

| \(r\) | mates disjoint from fixed \(A\) | unordered mate pairs | differences in \(\operatorname{rad}C\) | rank of their span |
|---:|---:|---:|---:|---:|
| 3 | 8 | 28 | 0 | 6 |
| 5 | 144 | 10,296 | 10,296 | 44 |

Thus the \(r=3\) mate differences are radical only for the restricted
support lattice (whose polar form is zero), not for the full stable trade
code.  At \(r=5\), all mate differences do lie in the full radical, and
their 44-dimensional span lies in
\(\bar\Lambda\cap\operatorname{rad}C\), which has dimension 45.

For a full stable trade word \(u\in C\), full radicality has the exact
saturated-rowspace formulation
\[
 u\in\operatorname{rad}C
 \quad\Longleftrightarrow\quad
 u\in C^\perp
 =\overline{\bigl(\operatorname{row}_{\mathbf Q}W
                  \cap\mathbf Z^{\binom{2r+1}r}\bigr)}.
\tag{10}
\]
The table proves that a common block-disjoint base does **not** imply
(10): every \(r=3\) mate pair is a counterexample.  Consequently the
\(r=5\) phenomenon cannot be promoted to a universal nonlinear-design
identity; it is consistent with a special Witt/\(M_{11}\) symmetry.

### The Mersenne parity that actually separates \(r=3,15\) from \(r=5\)

The positive cases have a stronger common feature than
\(r\equiv3\pmod4\).  If \(r=2^m-1\), then every parameter
\(\lambda_i\) of a hypothetical \(S(r-1,r,2r+1)\) is odd.  Put
\(j=r-i\).  Then
\[
\lambda_{r-j}
=\frac1j\binom{2^m+j}{j-1}
=\frac1{2^m+1}\binom{2^m+j}{j}.
\]
The denominator is odd, and Lucas' theorem makes the last binomial
coefficient odd: the binary digits of \(j<2^m\) occur unchanged below
the new leading digit of \(2^m+j\).

This forces a clean parity split in the block-intersection distribution.
For a fixed \(r\)-set \(K\), let \(n_\ell(K)\) count \(A\)-blocks meeting
\(K\) in \(\ell\) points.  The design moment equations are
\[
\sum_{\ell\ge i}\binom{\ell}{i}n_\ell(K)
=\binom ri\lambda_i.
\tag{11}
\]
Because all binary digits of \(r=2^m-1\) are one,
\(\binom ri\) is odd for every \(i\).  If \(K\in A\), then
\(n_r=1\); descending through (10) shows that every off-diagonal
\(n_i\), \(i<r\), is even.  If \(K\notin A\), then \(n_r=0\);
descending induction and
\(\sum_{\ell=i}^{r-1}\binom\ell i=\binom r{i+1}\) show that every
\(n_i\), \(i<r\), is odd.

Thus \(r=3\) and the target \(r=15\) have an all-odd parameter system and
even internal intersection valencies off the diagonal.  At \(r=5\), only
\(\lambda_4\) is odd and the internal intersection-one valency is
\(15\), odd.  This does not by itself prove total singularity, but it is
a rigorously stronger discriminator than the earlier blanket condition
\(r\equiv3\pmod4\).  A surviving lattice conjecture should be stated for
the Mersenne/all-odd case unless an independent argument covers the other
congruence cases.

## 4. Why the unrestricted trade lattice does not help

The full lattice \(\ker_{\mathbf Z}W_{r-1,r}\) is not 4-even even at
\(r=3\).  On points \(0,\ldots,6\), take the disjoint Fano planes
\[
\begin{aligned}
A_0&=\{012,034,056,135,146,236,245\},\\
A_1&=\{013,025,046,126,145,234,356\}.
\end{aligned}
\]
The vector \(z=1_{A_0}-1_{A_1}\) has every pair-sum zero, because each
pair occurs once in each plane, but
\[
 z\cdot z=7+7=14\equiv2\pmod4.
\]
So any successful lattice theorem must use the zero coordinates on the
fixed base \(A\); it cannot be a theorem about the full Specht/trade
lattice.

## 5. Verdict

The 4-even property at \(r=3\) is exact, but its only known higher test
(\(r=5\)) fails after full saturation.  No argument based on the ordinary
binary kernel or on \(\ker(H+I)\) alone can establish the \(r=15\) target.
The surviving statement is specifically about the stable 2-adic kernel
in (3)--(4), with the sphere condition in (2), and presently has only one
positive data point.

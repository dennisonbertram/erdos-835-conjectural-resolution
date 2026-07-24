# The \(\mathbb F_{17}S_{32}\)-module audit

Let
\[
W=W_{15,16}(32),\qquad
K=\ker_{\mathbb F_{17}}W.
\]
This note records why the first modular-representation obstruction is
exactly saturated by a prospective colouring.

## Structure of \(K\)

Wilson's diagonal factors for \(W_{k-1,k}(2k)\) are
\[
k-j,\qquad 0\le j\le k-1.
\]
For \(k=16\), these are \(16,15,\ldots,1\), all nonzero modulo 17.
Therefore \(W\) has full row rank over \(\mathbb F_{17}\), and
\[
\dim K
=\binom{32}{16}-\binom{32}{15}
=\frac1{17}\binom{32}{16}
=35{,}357{,}670.
\tag{1}
\]

The usual polytabloids of shape \((16,16)\) lie in \(K\) and have the
dimension in (1).  Hence
\[
K\cong S^{(16,16)}
\]
as an \(\mathbb F_{17}S_{32}\)-module.

The standard coordinate dot product on \(K\) has radical
\[
\operatorname{rad}K=K\cap K^\perp
=\ker W\cap\operatorname{row}(W).
\]
Because \(W\) has full row rank, this radical is isomorphic to
\(\ker(WW^{\mathsf T})\).

Over characteristic zero, the nonzero eigenvalues of \(WW^{\mathsf T}\)
are
\[
(16-j)(17-j),\qquad 0\le j\le15,
\]
with the standard Johnson multiplicities.  Exactly one factor of 17 occurs
in their determinant: it comes from \(j=0\), whose multiplicity is one.
Thus the determinant has 17-adic valuation one, and reduction modulo 17
has nullity exactly one.  Moreover,
\[
W^{\mathsf T}\mathbf1=16\mathbf1=-\mathbf1,
\]
so this radical line is the constant line:
\[
\operatorname{rad}K=\langle\mathbf1\rangle.
\tag{2}
\]

The partition \((16,16)\) is 17-regular.  The quotient of its Specht module
by the radical of the invariant form is therefore the simple module
\(D^{(16,16)}\).  Consequently \(K\) has precisely the two layers
\[
0\subset\langle\mathbf1\rangle\subset K,
\qquad
K/\langle\mathbf1\rangle\cong D^{(16,16)}.
\tag{3}
\]
There is no additional Jantzen/radical layer on which to base an immediate
contradiction.

## The prospective power space fits

Suppose a colouring exists, label its colours by \(\mathbb F_{17}\), and
write \(c\) for the resulting coordinate function.  Put
\[
L=\langle 1,c,c^2,\ldots,c^{15}\rangle.
\]
The seventeen colours occur equally often, with common multiplicity
\[
d=\frac1{17}\binom{32}{16}=35{,}357{,}670.
\]
The functions \(1,c,\ldots,c^{15}\) are linearly independent, so
\[
\dim L=16.
\]

The Catalan congruence \(d\equiv-1\pmod {17}\) follows, for example, from
\[
\binom{33}{16}=33d\equiv1\pmod {17}.
\]
For \(1\le a,b\le15\),
\[
\langle c^a,c^b\rangle
=d\sum_{z\in\mathbb F_{17}}z^{a+b}
=
\begin{cases}
1,&a+b=16,\\
0,&a+b\ne16.
\end{cases}
\tag{4}
\]
Also, the constant vector is orthogonal to all of \(L\), including itself.
Thus
\[
\operatorname{rad}L=\langle\mathbf1\rangle,
\]
and \(L/\langle\mathbf1\rangle\) is a nondegenerate 15-dimensional space
with the anti-diagonal Gram matrix in (4).

This is fully compatible with (2)--(3): the required power space consumes
the one radical direction but otherwise embeds as an ordinary
nondegenerate subspace of the enormous simple quotient.  Module structure
and the invariant bilinear form alone do not force \(c\) to be constant.

## Consequence for further attacks

Any decisive modular argument must use more than composition factors,
radical dimension, or the Gram matrix of the powers.  It must exploit the
coordinatewise multiplicative relations among the vectors
\(c,c^2,\ldots,c^{15}\), or equally the fact that they arise from a single
17-cell partition.

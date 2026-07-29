# Every tight prime colouring has full slice degree

This note proves a general necessary condition for every surviving prime
case of Erdős--Rosenfeld Problem #835.  It is not a nonexistence proof.

Let \(p\) be an odd prime, put
\[
 k=p-1,\qquad n=2k,
\]
and identify the \(p\) colours with \(\mathbb F_p\).  A function on the
\(k\)-slice \(\binom{[n]}k\) has **slice degree at most \(d\)** if it is the
restriction of a multilinear polynomial of degree at most \(d\) in the
point-incidence variables.

## Theorem

If
\[
 c:\binom{[2k]}k\longrightarrow\mathbb F_p
\]
is a tight \(p\)-colouring, then \(c\) has slice degree exactly \(k\).
More generally, if \(h:\mathbb F_p\to\mathbb F_p\) is nonconstant and
\[
 \sum_{z\in\mathbb F_p}h(z)=0,
\tag{1}
\]
then \(h\circ c\) has slice degree exactly \(k\).

In particular, every difference of two colour-class indicators has full
slice degree.  At the first open case, no relabelling of a hypothetical
17-colouring can have degree at most \(15\).

## Proof

Let \(W=W_{k-1,k}(2k)\) be the inclusion matrix whose rows are indexed by
\((k-1)\)-sets and whose columns are indexed by \(k\)-sets.  The \(p\)
extensions of every \((k-1)\)-set receive all \(p\) colours.  Indeed, any
two such extensions are facets of their common \((k+1)\)-set and hence
have different colours.  Therefore (1) gives
\[
 W(h\circ c)=0.                                           \tag{2}
\]

We now identify the low-degree part of this kernel.  For
\(A\subseteq[n]\), let
\[
 m_A(S)=\mathbf 1_{A\subseteq S}\qquad
 (S\in\textstyle\binom{[n]}k).
\]
If \(|A|=a\le k-1\), then
\[
 \sum_{\substack{T\supseteq A\\|T|=k-1}}m_T
   =(k-a)m_A.                                             \tag{3}
\]
The scalar \(k-a\) lies in \(\{1,\ldots,k\}\) and is nonzero in
\(\mathbb F_p\).  Hence every monomial of degree at most \(k-1\) lies in
\(\operatorname{row}W\).  The reverse inclusion is immediate, so
\[
 \{\text{slice-degree-at-most-}k-1\text{ functions}\}
   =\operatorname{row}_{\mathbb F_p}W.                   \tag{4}
\]

Wilson's diagonal factors for \(W_{k-1,k}(2k)\) are
\[
 k-j,\qquad 0\le j\le k-1.
\]
None is zero modulo \(p=k+1\), so \(W\) has full row rank over
\(\mathbb F_p\).

It remains to compute the radical of its row space.  Over the rationals,
the eigenvalues of \(WW^{\mathsf T}\) are
\[
 (k-j)(k+1-j),\qquad 0\le j\le k-1,
\tag{5}
\]
with the usual Johnson multiplicities.  Exactly one factor of \(p\)
occurs in the determinant: it is \(k+1=p\) in the \(j=0\) eigenvalue,
whose multiplicity is one.  Thus reduction modulo \(p\) has nullity
exactly one.  Consequently the radical of the row space is
one-dimensional.  The constant function belongs to that radical because
\[
 W\mathbf 1=p\mathbf 1=0,\qquad
 W^{\mathsf T}\mathbf 1=k\mathbf 1=-\mathbf 1.
\]
Consequently
\[
 \ker W\cap\operatorname{row}W=\langle\mathbf1\rangle.
\tag{6}
\]

If \(h\circ c\) had degree at most \(k-1\), equations (2), (4), and (6)
would make it constant.  Since every colour occurs and \(h\) is
nonconstant, \(h\circ c\) is nonconstant.  This contradiction proves that
its degree is \(k\), the maximum possible degree on the middle slice.
\(\square\)

## Consequences and scope

Taking \(h(z)=z\) proves the assertion for the raw colour function because
\(\sum_z z=0\).  Taking
\[
 h(z)=\mathbf1_{z=a}-\mathbf1_{z=b}
\]
proves the full-degree assertion for every difference of two fibres.
More generally, the space of zero-sum colour statistics modulo constants is
15-dimensional, and every nonzero class in it has a full-degree
representative after composition with the colouring.

This strictly contains the linear part of the additive and quadratic
ansatz obstructions: a successful colouring cannot be represented by any
polynomial of degree \(0,\ldots,15\), irrespective of its coefficients.
It does not control degree-16 functions; the full kernel in (2) is enormous,
and a genuine colouring would live there.

Run

```bash
python3 -B evidence/verify_full_slice_degree_necessity.py
```

for direct matrix checks at \(p=3,5\) and exact factor audits at
\(p=7,17\).

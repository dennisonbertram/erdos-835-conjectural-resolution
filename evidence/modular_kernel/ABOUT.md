# Modular-kernel audit

This directory records two exact checks relevant to the finite-field
formulation of Erdős Problem #835.

Let \(p=k+1\) be prime and let
\[
W=W_{k-1,k}(2k)
\]
be the inclusion matrix from \((k-1)\)-sets to \(k\)-sets.  A prospective
colouring gives a nonconstant \(c\) such that
\[
c,c^2,\ldots,c^{p-2}\in\ker_{\mathbb F_p}W.
\]

The script verifies:

1. Wilson's diagonal factors imply that \(W\) has full row rank modulo
   \(p\), so
   \[
   \dim\ker W=\binom{2p-2}{p-1}/p=C_{p-1}.
   \]
2. Complementation acts as \(+1\) on this kernel because \(k=p-1\) is
   even.
3. For \(p=3,5,7\), the coordinatewise Schur square of the kernel is the
   entire complement-symmetric space.  Thus a bare Schur-square dimension
   argument supplies no obstruction.
4. The tempting stronger claim
   \[
   c,c^2\in\ker W\Longrightarrow c\text{ is constant}
   \]
   is false.  An explicit counterexample is constructed for \(p=7\).

For the last check, partition twelve points into three groups of four.
On the two-subsets of each four-set, use the standard one-factorization
of \(K_4\), labelled by \(1,2,4\in\mathbb F_7^\times\).  A six-set gets
value zero unless it meets every group in two points; in the latter case,
its value is the product of its three local labels.  At every five-star,
either every extension has value zero, or its three potentially nonzero
extensions differ by the factors \(1,2,4\).  Since
\[
1+2+4=1^2+2^2+4^2=0\pmod 7,
\]
both \(c\) and \(c^2\) lie in the inclusion kernel.  The function is
nonconstant, with 708 zero values and 72 occurrences of each of
\(1,2,4\).

This does **not** solve Problem #835.  It shows that all powers through
\(p-2\), rather than merely the quadratic condition, are essential.

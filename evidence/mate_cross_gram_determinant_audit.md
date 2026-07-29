# Direct cross-Gram invariants are not fixed by the mate equations

Status: **proved formulation; exact negative controls for direct fixed-value
tests.**  This note tests a natural determinant/Pfaffian and matrix-tree
route which really does use the two endpoint exact covers.  It does not
prove the fixed-base parity conjecture, and it does not exclude every
possible parity criterion derived from the full cross-Gram matrix.

Let \(r\) be odd, let \(A\) be an \(S(r-1,r,2r+1)\), and let \(B,C\)
be mates of \(A\).  Use the sphere bijections to label the blocks of each
mate by \(P\in A\):

\[
 K_B(P)=X\setminus(P\cup\{\varphi_B(P)\}),\qquad
 K_C(P)=X\setminus(P\cup\{\varphi_C(P)\}).
\]

Let \(E_B\) be the facet--block incidence matrix of \(B\), with its columns
in this order, and define the integral cross-Gram matrix

\[
 G_{B,C}=E_B^{\mathsf T}E_C.
\tag{1}
\]

Both endpoint Steiner conditions are used here: every row of either incidence
matrix has exactly one \(1\), and every column has exactly \(r\) ones.

## 1. Exact form of the matrix

For two \(r\)-blocks \(K,L\), their number of common \((r-1)\)-facets is

\[
 G_{K,L}=
 \begin{cases}
 r,&K=L,\\
 1,&|K\cap L|=r-1,\\
 0,&\text{otherwise}.
 \end{cases}
\tag{2}
\]

Hence \(G\mathbf 1=G^{\mathsf T}\mathbf 1=r\mathbf 1\).  More
particularly, \(K_B(P)\) and \(K_C(P)\) are both \(r\)-subsets of the same
\((r+1)\)-set \(X\setminus P\).  They are equal exactly when the two mate
maps agree at \(P\); otherwise they meet in \(r-1\) points.  If
\(i=|B\cap C|\), then

\[
 \operatorname{tr}G=b+(r-1)i.
\tag{3}
\]

Thus, for odd \(r\), the diagonal of \(G\bmod2\) is always \(1\), whether
or not the mate maps agree.  A test that uses only those diagonal entries
has lost the target.  Equation (3) recovers the parity only tautologically
from a mod-\(4\) trace when \(r\equiv3\pmod4\); it supplies no fixed value
for that trace.  This observation does not rule out a subtler invariant
using the full off-diagonal matrix.

The standard skew lift
\(\begin{psmallmatrix}0&G\\-G^{\mathsf T}&0\end{psmallmatrix}\) has
Pfaffian \(\pm\det G\), so it cannot add information beyond the same
cross-Gram determinant.

## 2. Exact controls

The accompanying verifier builds a deterministic base and then enumerates
all its mates by Algorithm X.

* At \(r=3\), all \(28\) unordered pairs of the eight Fano mates have
  \(i=1\), \(\operatorname{tr}G=9\), and
  \(\det G=27\).  The Laplacian (3I-G) has zero rooted matrix-tree
  cofactor.
* At \(r=5\), the deterministic Witt base has \(144\) mates.  Two valid
  pairs have respectively \(i=18\) and \(i=6\); their determinants are
  \(934696197509765625\equiv9\pmod {16}\) and \(0\).  Both rooted
  cofactors of \(5I-G\) are zero.

Therefore determinant invertibility, a single fixed \(2\)-adic determinant
value, and a nonzero first matrix-tree cofactor are not forced even by the
full simultaneous endpoint exact-cover conditions.  The two \(r=5\)
controls have the same agreement parity, so they do **not** show that no
function of the determinant can recover agreement parity.  They close only
the direct fixed-value/invertibility/cofactor candidates tested here.

Run:

```sh
python3 -B evidence/verify_mate_cross_gram_audit.py
```

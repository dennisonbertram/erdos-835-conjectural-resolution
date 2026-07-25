# Oriented disjointness and the triangle-Pfaffian audit

This note tests whether the sign of the canonical triangle permutation can
be forced solely from the oriented disjointness operator.  The answer is
negative: the complete skew/Pfaffian determinant calculation is compatible
with an arbitrary signed triangle permutation, including permutations with
odd cycles.

The calculation does not disprove the desired even-cycle theorem.  It
shows exactly which extra input a proof must use: the global Steiner
incidence identities, rather than skew-symmetry or positivity of Pfaffian
squares alone.

## 1. The signed disjointness operator

Let \(r\) be odd, \(n=2r+1\), and orient the real vector space
\(\mathbb R^n\).  Put \(u=e_1+\cdots+e_n\), let \(*\) be the Hodge star,
and define
\[
 {\cal T}=\iota_u *:\bigwedge^r\mathbb R^n
 \longrightarrow\bigwedge^r\mathbb R^n.           \tag{1}
\]
In the basis indexed by \(r\)-subsets, the entry
\({\cal T}_{S,T}\) is zero unless \(S\cap T=\varnothing\), in which case
it is \(+1\) or \(-1\).  Swapping the two \(r\)-fold wedges changes the
orientation by \((-1)^{r^2}=-1\), so
\[
 {\cal T}^{\mathsf T}=-{\cal T}.                  \tag{2}
\]
This is the canonical signed version of the adjacency matrix of the odd
graph.

If \(A\) and \(B\) are block-disjoint
\(S(r-1,r,2r+1)\) systems, every block of \(A\) has exactly one disjoint
block of \(B\), and conversely.  Therefore the rectangular block
\({\cal T}[A,B]\) is a signed permutation matrix.  Also
\({\cal T}[A,A]=0\), because two blocks in one such Steiner system are
never disjoint.

Now suppose \(A,B,C\) are pairwise block-disjoint systems, each with \(b\)
blocks.  On their labelled direct sum, the principal block of
\({\cal T}\) has the form
\[
 {\cal T}_{ABC}=
 \begin{pmatrix}
 0&P&Q\\
 -P^{\mathsf T}&0&R\\
 -Q^{\mathsf T}&-R^{\mathsf T}&0
 \end{pmatrix},                                  \tag{3}
\]
where \(P,Q,R\) are signed permutation matrices.  Independent signed
permutation changes of basis in the three fibres put (3) into the normal
form
\[
 {\cal S}(H)=
 \begin{pmatrix}
 0&I&I\\
 -I&0&H\\
 -I&-H^{\mathsf T}&0
 \end{pmatrix},                                  \tag{4}
\]
where \(H\) is a signed permutation matrix.  Up to inversion and
conjugacy, its underlying permutation is
\[
 F_{CB}F_{AC}F_{BA},
\]
the canonical triangle monodromy.  Thus its cycle lengths are exactly the
cycle lengths relevant to the proposed even-cycle obstruction.

## 2. Exact determinant formula

For an indeterminate \(t\), Schur complementation of the first diagonal
block in \(I+t{\cal S}(H)\) gives
\[
\begin{aligned}
\det(I+t{\cal S}(H))
&=\det\begin{pmatrix}
(1+t^2)I&tH+t^2I\\
-tH^{\mathsf T}+t^2I&(1+t^2)I
\end{pmatrix}\\
&=\boxed{\det\left(
(1+3t^2)I-t^3(H-H^{\mathsf T})\right).}           \tag{5}
\end{aligned}
\]
The blocks in the last calculation commute because
\(H^{\mathsf T}=H^{-1}\).

If \(\lambda\) runs through the complex eigenvalues of \(H\), equation
(5) is
\[
 \det(I+t{\cal S}(H))
 =
 \prod_\lambda
 \left(1+3t^2-t^3(\lambda-\lambda^{-1})\right).
 \tag{6}
\]
Every eigenvalue lies on the unit circle.  A real eigenvalue
\(\lambda=\pm1\) contributes the positive factor \(1+3t^2\).  A
nonreal conjugate pair \(e^{\pm i\theta}\) contributes
\[
 (1+3t^2)^2+4t^6\sin^2\theta>0                  \tag{7}
\]
for real \(t\).  Hence the usual fact that
\(\det(I+tK)>0\) for real skew-symmetric \(K\) gives no restriction at
all on the cycle structure of \(H\).

This remains true when the signed product around every monodromy cycle is
\(+1\), as supplied by the cofactor-orientation identity.  Take \(H\) to
be the ordinary permutation matrix of any prescribed permutation.  Then
every signed cycle product is \(+1\), while (5)--(7) still hold.  In
particular, a single odd cycle is fully compatible with the oriented
disjointness and all Pfaffian-square positivity constraints.

## 3. Cross-minor signs do not factor

A stronger possible use of (1) would be to hope that the determinant of
the signed matching between two disjoint systems factors as
\[
 \det{\cal T}[A,B]=\eta(A)\eta(B)                 \tag{8}
\]
for signs attached separately to the two systems, after fixing a total
order on the systems and writing (8) only for \(A<B\).  (The order
convention is necessary because, when \(b\) is odd,
\(\det{\cal T}[B,A]=-\det{\cal T}[A,B]\).)  Such a factorization would
make every canonically oriented cycle product positive and, in
particular, would fix every triangle product.  It is already false for
the complete set of 30 labelled Fano planes.

With the ground points and blocks in lexicographic order, consider the
four Fano planes
\[
\begin{aligned}
A_0={}&(012,034,056,135,146,236,245),\\
A_1={}&(013,025,046,126,145,234,356),\\
A_2={}&(014,023,056,125,136,246,345),\\
A_3={}&(015,024,036,126,134,235,456).
\end{aligned}
\]
Consecutive systems, including \(A_3,A_0\), are block-disjoint.  Exact
evaluation of the four signed permutation minors, always in increasing
system order (so the closing edge is evaluated as \(A_0,A_3\)), gives
signs
\[
 (+1,-1,+1,+1),
\]
whose product is \(-1\).  Changing the ordering or orientation attached
to any one system changes the two incident edge signs and leaves this
cycle product unchanged.  Thus (8) cannot hold under any gauge.

This four-cycle is not a counterexample to the desired triangle theorem:
the disjointness graph of the Fano planes is triangle-free.  It is an
exact counterexample to the proposed *pairwise minor-factorization
mechanism* for proving that theorem.

## 4. Consequence for the proof search

The following route is therefore rigorously closed:

> infer that the triangle monodromy is even, or has only even cycles,
> merely because it is obtained from three signed disjointness matchings
> inside a skew-symmetric Hodge/boundary operator.

At this level the normal form retains an arbitrary signed permutation
\(H\).  Neither its determinant, the positivity of
\(\det(I+t{\cal T}_{ABC})\), nor the Pfaffian squares in that determinant
distinguish even from odd monodromy cycles.

A successful oriented-incidence proof would have to invoke an identity
not used above, such as the full operator relation
\[
 {\cal T}^2=(\partial^{\mathsf T}\partial)-nI
\]
together with the exact Steiner grouping of all columns, or a genuinely
mod-\(4\) constraint on the relevant cross-minors.  Skew-symmetry and the
pairwise perfect matchings themselves are insufficient.

Run

```bash
python3 evidence/verify_triangle_pfaffian_audit.py
```

for exact-integer checks of (5) on signed permutations containing both
odd and even cycles, and for independent reproduction of the negative
Fano four-cycle.

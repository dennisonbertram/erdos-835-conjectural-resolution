# Two high-dimensional incidence-code boundaries

Status: **exact audits of two frozen shortening subspaces; not a
nonexistence proof, not a design, and not a solution of Problem #835.**

The verifier
`verify_s141531_high_dimension_boundaries.py` uses only Python's standard
library.  The two subspaces below were found heuristically, but the script
exhausts every coset of each frozen subspace and checks all displayed
arithmetic exactly.

## Setup

Let \(C_0\) be the forced \(30\)-dimensional even point-incidence code of a
hypothetical \(S(14,15,31)\); the full-point-rank prerequisite is proved in
`mersenne_spin_functional_audit.md`.  For an even subspace \(H\) supported
on a fixed set of fifteen points, retain the block coordinates on which
every word of \(H\) vanishes.  If \(q=|H|\), the retained length and a
restricted word weight are
\[
 n_H={1\over q}\sum_{h\in H}F(h),\qquad
 w_H(c)={\sum_{h\in H}F(h)-\sum_{h\in H}F(c+h)\over2q}.
\]
Only point-weight \(16\) is unresolved: the external Fourier value is
\(-1549\), and it increases by \(2^{15}\) when the set is the complement
of a design block.

## A dimension-ten divisible near-boundary

For the hexadecimal basis
\[
(5,35,5c,e4,1fd,21c,4e0,a5c,1015,5341),
\]
the shortened image has length \(16\,359\).  Even if every possible
weight-\(16\) translate is treated as a block complement, every nonzero
image word has weight at least \(1\,640\).  This positivity proves that the
kernel is exactly \(H\), so the image dimension is \(20\).

Every middle-layer correction changes a restricted weight by \(16\).
All external-base weights are divisible by \(4\).  Hence the actual image
is necessarily a projective doubly-even, and therefore self-orthogonal,
binary code.  There are \(3\,670\) quotient words whose translates avoid
the unresolved middle layer; their exact enumerator is
\[
\begin{array}{c|rrrrrr}
w&8024&8056&8212&8596&8628&10868\\ \hline
A_w&513&57&2907&171&19&3.
\end{array}
\]
In particular its true minimum satisfies
\[
1640\le d\le8024.
\]
The upper endpoint is close to, but still on the feasible side of,
Griesmer:
\[
g_2(8024,20)=16056,\qquad 16359-16056=303.
\]
Thus divisibility, self-orthogonality, and this exact partial enumerator do
not by themselves supply a contradiction.

Projectivity follows because two retained block columns define the same
functional on the even point space only if their symmetric difference lies
in its one-dimensional orthogonal complement.  That complement is spanned
by the odd all-one vector, whereas a symmetric difference is even; hence
the two blocks would have to be equal.  A retained column is also nonzero:
a \(15\)-block incidence vector is neither zero nor the all-one vector, so
it does not lie in the orthogonal complement of the even point space.

## A dimension-twelve crossing that joint occupancy does not reach

For the hexadecimal basis
\[
(3,1b,36,7e,a9,1d0,291,7cb,80e,1e11,2844,4b47),
\]
the retained length is \(4291\).  The weight-two words of \(H\) partition
the fifteen supported coordinates into classes of sizes
\[
(3,4,4,4).
\]

Within one translated coset, possible weight-\(16\) block complements are
adjacent when their difference has point-weight two.  They cannot both
occur: the corresponding \(15\)-blocks would share a \(14\)-set, contrary
to the Steiner property.  After fixing the number of selected coordinates
in each class, a connected component of this adjacency graph is
\[
\mathop{\square}_i J(n_i,r_i).
\]
It has
\[
v=\prod_i {n_i\choose r_i},\quad
\delta=\sum_i r_i(n_i-r_i),\quad
\lambda_{\min}=-\sum_i\min(r_i,n_i-r_i).
\]
Hoffman's bound therefore gives the exact-arithmetic occupancy upper bound
\[
\alpha\le
\left\lfloor {v(-\lambda_{\min})\over
                    \delta-\lambda_{\min}}\right\rfloor.
\]
The verifier applies this separately to every component in every coset.
The resulting lower bound is only
\[
d\ge556.
\]
It is positive, so again the kernel is exactly \(H\) and the image
dimension is \(18\).

There is also an actual no-middle word of weight \(2188\).  At that
optimistic endpoint,
\[
g_2(2188,18)=4387>4291
\]
by \(96\).  This is a genuine boundary crossing, but **not a
contradiction**: Griesmer would require a lower bound near \(2188\), while
the rigorous joint-occupancy lower bound is \(556\), for which
\[
g_2(556,18)=1123<4291.
\]

## Exact scope

This audit establishes:

1. the two frozen subspaces have ranks \(10\) and \(12\);
2. all retained lengths and every no-middle restricted word are exact;
3. the dimension-ten image is necessarily \(4\)-divisible;
4. the dimension-twelve weight-two exclusion plus Hoffman bounds prove
   \(d\ge556\), hence image dimension \(18\); and
5. neither frozen subspace currently contradicts a hypothetical
   \(S(14,15,31)\).

The remaining gap is a substantially stronger joint constraint on the
weight-\(16\) block-complement indicators, or a stronger structural bound
for the resulting projective divisible code.  The negative \(96\)
no-middle slack must not be reported as a solution.

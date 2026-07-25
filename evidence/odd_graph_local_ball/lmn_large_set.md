# The \(L/M\) layer as a large set of symmetric idempotent Latin squares

Let \(\mathcal C=V\sqcup\{\infty\}\), with \(|\mathcal C|=17\).
A symmetric idempotent Latin square on \(\mathcal C\) is a map
\[
S:\mathcal C^2\longrightarrow\mathcal C
\]
such that \(S(x,y)=S(y,x)\), \(S(x,x)=x\), and every row is a
permutation of \(\mathcal C\).

## Equivalence theorem

Conditions 1--3 of `radius4_reduction.md` are equivalent to a family
\[
S_i\qquad(i=1,\ldots,15)
\]
of symmetric idempotent Latin squares of order 17 that are pairwise
disjoint in every off-diagonal cell.  In fact, for every \(x\ne y\),
\[
\{S_i(x,y):1\le i\le15\}
=\mathcal C\setminus\{x,y\}.
\tag{1}
\]
Thus the family is maximum possible: an off-diagonal cell of an
idempotent symmetric Latin square cannot contain either of its row or
column labels, leaving exactly fifteen possible entries.

### Proof

Given \(L_i,M_i\), define
\[
\begin{aligned}
S_i(u,u)&=u &&(u\in V),\\
S_i(\infty,\infty)&=\infty,\\
S_i(u,\infty)=S_i(\infty,u)&=L_i(u),\\
S_i(u,v)=S_i(v,u)&=M_i(uv) &&(u\ne v\in V).
\end{aligned}
\]
For a finite row \(u\), the diagonal contributes \(u\), the
\(\infty\)-cell contributes \(L_i(u)\), and the fifteen \(M_i\)-cells
contribute exactly the other fifteen symbols.  The \(\infty\)-row is
Latin because \(L_i\) is a permutation.  Hence \(S_i\) is symmetric,
idempotent, and Latin.

For the cells \(u\infty\), equation (1) is condition 1 of the
radius-4 reduction.  For the cells \(uv\) with \(u,v\in V\), it is
condition 3.  This proves off-diagonal disjointness and saturation.

Conversely, start with a family satisfying (1), and set
\[
L_i(u)=S_i(u,\infty),\qquad M_i(uv)=S_i(u,v).
\]
The \(\infty\)-row makes each \(L_i\) a permutation.  Idempotence and
the Latin property give \(L_i(u)\ne u\), so it is a derangement.
Equation (1) at \(u\infty\) gives condition 1.  In finite row \(u\),
the entries on the other finite columns are precisely
\(\mathcal C\setminus\{u,L_i(u)\}\), giving condition 2.  Equation (1)
at \(uv\) gives condition 3. \(\square\)

## One-factorization form

A single \(S_i\) gives a canonically labelled one-factorization of
\(K_{18}\) on vertices \(\mathcal C\sqcup\{\alpha\}\): the factor
labelled \(c\) contains \(\alpha c\) and every edge \(xy\) with
\(S_i(x,y)=c\).  Conversely, any one-factorization normalized by
labelling the factor containing \(\alpha c\) as \(c\) gives such a
square.

For a large family, all normalized factorizations share the canonical
edge \(\alpha c\) in their \(c\)-factors, while no two share any other
edge with the same factor label.  This precise statement is safer than
calling the factorizations merely “orthogonal,” which is a different
and potentially stronger convention in the design literature.

## Audited construction attacks

Claude Fable suggested three especially natural ways to build the
large set.  Each exposes useful structure, but none currently supplies
a witness.

### One multiplicatively free square on \(\operatorname{PG}(1,16)\)

Write the point set as
\(\operatorname{GF}(16)\sqcup\{\infty\}\).  If a symmetric idempotent
Latin square \(S\) satisfies
\[
 S(\rho a,\rho b)\ne \rho S(a,b)
 \tag{2}
\]
for every \(\rho\in\operatorname{GF}(16)^*\setminus\{1\}\) and every
off-diagonal cell, then its fifteen multiplicative twists
\[
 S^\lambda(a,b)=\lambda
 S(\lambda^{-1}a,\lambda^{-1}b)
 \qquad(\lambda\in\operatorname{GF}(16)^*)
\]
are a large set of the required kind.  The equivalence follows by
conjugating the equality \(S^\lambda(a,b)=S^\mu(a,b)\) by
\(\mu^{-1}\).

`search_multiplicative_twist.py` encodes (2) in two equivalent ways:
direct forbidden pairs and all-different constraints on each of the
nine free cell orbits.  A 600-second direct search of the unrestricted
ansatz returned `UNKNOWN`, so this appealing construction remains
open.  Adding Frobenius equivariance
\[
S(a^2,b^2)=S(a,b)^2
\tag{3}
\]
returned `INFEASIBLE` in presolve in both encodings.  This is an exact
finite-model refutation of the Frobenius-equivariant subfamily as
encoded, not an infeasibility certificate for the unrestricted
multiplicative ansatz.

### Why the hyperoval pencil construction cannot work

Let \(H\) be a hyperoval in \(\operatorname{PG}(2,16)\).  Every point
\(Q\notin H\) determines the perfect matching \(M(Q)\) of \(H\) whose
pairs lie with \(Q\) on a secant.  The seventeen points on any external
line \(\ell\) give a one-factorization of \(K_H\).

Fix \(\alpha\in H\) and normalize each factor by labelling \(M(Q)\)
with the unique \(c\in H\setminus\{\alpha\}\) for which
\(\alpha,c,Q\) are collinear.  Two external lines meet at a point
\(Q\notin H\), so their normalized factorizations contain the same
whole matching \(M(Q)\) with the same label.  Besides the allowed
canonical edge \(\alpha c\), they consequently share eight further
same-labelled edges.  Thus no two factorizations from this pencil
family can occur in the required large set.

### Two cyclic no-go lemmas

First suppose a square on \(\mathbb Z_{17}\) is translation-equivariant.
It then has the form
\[
S(x,x+d)=x+\tau(d)\qquad(d\ne0).
\]
Put \(q(d)=\tau(d)/d\).  Since an off-diagonal cell cannot contain
either endpoint, \(q\) maps the sixteen nonzero differences into the
fifteen values
\(\mathbb Z_{17}\setminus\{0,1\}\).  If fifteen multiplicative
conjugates indexed by \(A\subset\mathbb Z_{17}^*\) formed a large set,
then, for every \(d\ne0\), \(q\) would be injective on the
fifteen-element set \(A^{-1}d\).  Any two nonzero differences lie
together in one such set: its complement has one point, and as \(d\)
varies that missing point varies over all sixteen choices.  Hence
\(q\) would be injective from a sixteen-element set to a
fifteen-element set, a contradiction.

Second, take the seventeen cyclic rotations of one normalized
one-factorization.  If a set \(T\subset\mathbb Z_{17}\) of fifteen
rotations were pairwise compatible, then
\(T-T=\mathbb Z_{17}\): for every \(d\), the two fifteen-element sets
\(T\) and \(T+d\) intersect.  Compatibility depends only on the
rotation difference, so all seventeen rotations would then be
pairwise compatible.  That is impossible because an off-diagonal cell
has only fifteen permissible labels.  Therefore a required family
cannot be obtained by selecting fifteen rotations of one
factorization.

## What this does and does not decide

This theorem identifies the exact \(L/M\) object and reduces its search
to 15 coupled order-17 Latin squares.  It does not settle existence.
Even a large-set witness must still pass the independent \(N_{uv}\)
list-edge-colouring layer before it yields a radius-4 ball colouring.

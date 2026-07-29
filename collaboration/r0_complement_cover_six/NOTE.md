# A complement-covering six-prefix for the profile \(r=0\)

Date: 2026-07-28.

## Result and scope

Let \(V_1,\ldots,V_{17}\subseteq V(K_{13})\) be a class-B support
family with profile
\[
 (n_8,n_{10},n_{12})=(7,10,0),
\]
where every vertex belongs to twelve supports.  There is a subfamily of
three size-eight supports and three size-ten supports such that

1. their six complements cover all thirteen vertices; and
2. the six prescribed perfect matchings can be chosen pairwise
   edge-disjoint.

Consequently, if \(D\) is the union of the six matchings, then
\[
 \Delta(D)\le 5,\qquad \delta(K_{13}-D)\ge7. \tag{1}
\]

This is a better invariant than the earlier arbitrary six-packing, but it
is still only a **six-prefix theorem**.  In particular, it does not pack
three further colours, prove a coordinated nine-packing, or solve
Erdős--Rosenfeld Problem #835.

## Why the tempting \(4+2\) cover is false

Take complements inside \(V(K_{13})\).  The profile consists of seven
five-sets and ten triples, and every vertex occurs in exactly five of
these seventeen complements.

The claim that four five-sets and two triples must cover the vertex set is
false.  Here is a counterexample with all ten triples distinct.

Partition the vertex set as
\[
 X=\mathbb Z_7,\qquad Y=\mathbb Z_6.
\]
For \(i\in\mathbb Z_7\), take the seven five-sets
\[
 A_i=X\setminus\{i,i+1\}. \tag{2}
\]
Every vertex of \(X\) lies in exactly five of them, while no vertex of
\(Y\) lies in one.

On \(Y\), take the six cyclic triples
\[
 C_i=\{i,i+1,i+3\}\qquad(i\in\mathbb Z_6) \tag{3}
\]
and the four additional triples
\[
 012,\qquad045,\qquad135,\qquad234. \tag{4}
\]
Every vertex of \(Y\) occurs three times in (3) and twice in (4), hence
five times in total.  None of the ten triples is the complement in \(Y\)
of another one.  Two triples on a six-set are disjoint exactly when they
are complementary, so these ten triples are pairwise intersecting.
Therefore two of them cover at most five vertices of \(Y\).  Four sets
from (2) contain no vertex of \(Y\), so no choice of four five-sets and
two triples covers \(X\cup Y\).

Thus a universal complement-cover of support type \(8^4 10^2\) cannot be
the route to a degree-five six-prefix.

## A universal \(3+3\) complement cover

We now prove the replacement.

> **Covering lemma.**  Some three of the seven five-sets and some three of
> the ten triples cover all thirteen vertices.

Choose three five-sets and three triples uniformly and independently.
For a vertex \(v\), let \(a_v\) be its multiplicity among the seven
five-sets.  Its triple multiplicity is \(5-a_v\).  The probability that
the six chosen complements miss \(v\) is
\[
 p(a_v)=
 \frac{\binom{7-a_v}{3}}{\binom73}
 \frac{\binom{5+a_v}{3}}{\binom{10}3}. \tag{5}
\]
For \(a=0,\ldots,5\), the exact values are
\[
 \frac1{12},\quad
 \frac2{21},\quad
 \frac1{12},\quad
 \frac4{75},\quad
 \frac1{50},\quad
 0. \tag{6}
\]
They satisfy the pointwise linear bound
\[
 p(a)\le \frac{5-a}{36}. \tag{7}
\]

The total incidence among the seven five-sets is
\[
 \sum_v a_v=7\cdot5=35. \tag{8}
\]
By linearity of expectation, (7) and (8),
\[
 \mathbb E[\text{uncovered vertices}]
 \le\sum_v\frac{5-a_v}{36}
 =\frac{13\cdot5-35}{36}
 =\frac56<1. \tag{9}
\]
The number of uncovered vertices is a nonnegative integer, so some
selection leaves none.

The bound \(5/6\) is the exact maximum of the left side over the relaxed
integer data \(a_v\in\{0,\ldots,5\}\), \(\sum a_v=35\): equality in (7)
is possible only at \(a=2,5\), and the unique equality multiplicities are
ten occurrences of \(a=2\) and three of \(a=5\).

## Three prescribed ten-supports in an ambient dense graph

The selected six supports have sizes \(8,8,8,10,10,10\), so the last
three cannot be justified by the elementary greedy degree threshold.  We
use the following coordination lemma.

> **Three-support lemma.**  Let \(H\) be a graph on thirteen vertices with
> \(\delta(H)\ge9\).  For arbitrary ten-subsets
> \(S_1,S_2,S_3\subseteq V(H)\), there are pairwise edge-disjoint perfect
> matchings
> \[
> M_i\subseteq H[S_i]\qquad(i=1,2,3).
> \]

Each \(H[S_i]\) has minimum degree at least six.  Apply the two-support
lemma from
`../first_lift_global_theorem/SIX_PACKING_NOTE.md` to choose disjoint
perfect matchings \(M_1\subseteq H[S_1]\) and
\(M_2\subseteq H[S_2]\).
Put
\[
 G=H[S_3]-(M_1\cup M_2).
\]
Then \(\delta(G)\ge4\).  If \(G\) has a perfect matching, we are done.

Suppose it does not.  Tutte's theorem gives a set \(Q\), \(|Q|=q\), for
which \(G-Q\) has at least \(q+2\) odd components.  If one such component
has odd order \(c\), then
\[
 c-1+q\ge4. \tag{10}
\]
The finite possibilities in ten vertices leave only:

1. \(q=0\), with two components of order five; or
2. \(q=4\), with six singleton components.

Indeed, for \(q=1,2,3\), the least possible totals of the odd components
are respectively \(3\cdot5\), \(4\cdot3\), and \(5\cdot3\), all larger
than \(10-q\); and \(q\ge5\) violates \(q+2\le10-q\).

### Two \(K_5\) components

Write \(S_3=A\mathbin{\dot\cup}B\), with \(|A|=|B|=5\).  Minimum degree
four forces
\[
 G=K_5\mathbin{\dot\cup}K_5. \tag{11}
\]
Every vertex has degree at least six in \(H[S_3]\), so it has at least
two neighbours across the cut \(A,B\).  All such cross-edges lie in
\(M_1\cup M_2\).  The cut therefore has at least ten edges, while each
matching contributes at most five.  Equality is forced throughout:
each of \(M_1,M_2\) is a perfect matching across \(A,B\).
In particular, both matchings saturate \(S_3\), so
\[
 S_1=S_2=S_3. \tag{12}
\]

Choose two edges \(a_1b_1,a_2b_2\in M_1\), and replace them in \(M_1\)
by \(a_1a_2,b_1b_2\).  These new edges lie in the two untouched cliques.
Now use the freed edge \(a_1b_1\), a perfect matching of
\(A\setminus\{a_1\}\), and a perfect matching of
\(B\setminus\{b_1\}\).  Their union is the required third perfect
matching, disjoint from the modified \(M_1\) and from \(M_2\).

### A four-vertex separator and six singletons

Write \(S_3=Q\mathbin{\dot\cup}U\), with \(|Q|=4\), \(|U|=6\).
Minimum degree four forces
\[
 G[Q,U]=K_{4,6},\qquad G[U]=\varnothing. \tag{13}
\]
Every \(u\in U\) already has its four neighbours in \(Q\), but has degree
at least six in \(H[S_3]\).  Thus it is incident with two edges of
\(H[U]\), and both lie in \(M_1\cup M_2\).  Since each matching supplies
at most one incident edge, each \(M_i\) pairs all six vertices of \(U\)
internally.  Hence \(H[U]\) is the union of two disjoint perfect
matchings, so every \(u\in U\) has exactly two neighbours in \(U\).

Each \(u\) consequently has exactly three nonneighbours among the other
five vertices of \(U\).  But \(\delta(H)\ge9\), so a vertex has at most
three nonneighbours in all of \(H\).  Therefore
\[
 H[U,V(H)\setminus U]=K_{6,7}. \tag{14}
\]

Choose an edge \(uv\in M_1[U]\) and either of the two remaining edges
\(pq\in M_1[S_1\setminus U]\).  Replace \(uv,pq\) by \(up,vq\), which
exist by (14).  The other matching \(M_2\) has no edge between \(U\) and
its complement, so the modified \(M_1\) remains disjoint from \(M_2\).
Finally, use the freed edge \(uv\) and match the four vertices of
\(U\setminus\{u,v\}\) bijectively to the four vertices of \(Q\), using
(13).  This is a perfect matching on \(S_3\), and it is edge-disjoint
from the first two.

The two cases prove the three-support lemma.

## Packing the covering six-prefix

Choose the three size-eight and three size-ten supports supplied by the
covering lemma.  Pack the three size-eight supports greedily.  If \(D_0\)
is the union of these three matchings, then
\[
 H=K_{13}-D_0
\quad\text{satisfies}\quad
\delta(H)\ge9. \tag{15}
\]
The three-support lemma packs the selected size-ten supports inside
\(H\).

Let \(D\) be the union of all six matchings and let \(\sigma(v)\) count
the selected complements containing \(v\).  Because the selected
complements cover every vertex,
\[
 d_D(v)=6-\sigma(v)\le5. \tag{16}
\]
This proves (1) and the claimed six-prefix theorem.

## Verification and remaining frontier

Run:

```sh
python3 collaboration/r0_complement_cover_six/verify_arithmetic.py
```

The verifier uses only the standard library.  It checks the explicit
\(4+2\) counterexample, the exact probability table and integer maximum,
the finite Tutte catalogue, and representative switches for both terminal
forms of the three-support lemma.

After this six-prefix, four size-eight and seven size-ten colours remain.
Reaching coordinated nine still requires packing three of those remaining
supports in a common residual graph of minimum degree seven.  The result
above neither assumes nor proves that extension.

# Coordinated eight-packings for the profile \(r=1\)

Date: 2026-07-28.

## Result

Let \(V_1,\ldots,V_{17}\subseteq V(K_{13})\) be a target class-B support
family with profile
\[
 (n_8,n_{10},n_{12})=(8,8,1),
\]
where every vertex belongs to twelve supports.  Then some eight support
matchings can be chosen pairwise edge-disjoint.

This is an existential, coordinated packing theorem.  It does not say
that an arbitrary seven-prefix extends; the exact certificate in
`../first_lift_global_theorem/R1_DEAD_SEVEN_PREFIX.md` disproves that
stronger statement.

## A complement-covering six-subfamily

Take complements inside the thirteen-vertex set.  There are eight
five-sets, eight triples, and one singleton \(\{x\}\), and every vertex
occurs in exactly five complements.

> **Covering lemma.**  Some four of the five-sets and two of the triples
> cover all thirteen vertices.

Choose four of the eight five-sets and two of the eight triples uniformly
and independently.  For \(v\ne x\), let \(a\) be its five-set multiplicity.
Its triple multiplicity is \(5-a\), and its probability of being missed is
\[
 p_0(a)=
 \frac{\binom{8-a}{4}}{\binom84}
 \cdot
 \frac{\binom{3+a}{2}}{\binom82}.
\tag{1}
\]
For \(a=0,\ldots,5\), these values are
\[
 \frac3{28},\quad
 \frac3{28},\quad
 \frac{15}{196},\quad
 \frac{15}{392},\quad
 \frac3{280},\quad
 0.
\tag{2}
\]
They obey the convenient linear bound
\[
 p_0(a)\le\frac{3(5-a)}{112}. \tag{3}
\]

For the singleton vertex \(x\), if its five-set multiplicity is \(a\),
then its triple multiplicity is \(4-a\).  Its miss probability, for
\(a=0,\ldots,4\), is
\[
 p_1(a)=
 \frac3{14},\quad
 \frac5{28},\quad
 \frac{45}{392},\quad
 \frac3{56},\quad
 \frac1{70}.
\tag{4}
\]

The total five-set incidence is \(8\cdot5=40\).  Writing \(a_x\) for the
five-set multiplicity of \(x\), linearity of expectation and (3) give
\[
\begin{aligned}
\mathbb E[\text{uncovered vertices}]
&\le
 \frac3{112}\sum_{v\ne x}(5-a_v)+p_1(a_x)\\
&=
 \frac{3(20+a_x)}{112}+p_1(a_x)
\le\frac34<1.
\end{aligned}
\tag{5}
\]
The last inequality is the five-case check \(a_x=0,\ldots,4\).
The number of uncovered vertices is a nonnegative integer, so some choice
has none.  This proves the covering lemma.

Select the corresponding four support-eight colours and two support-ten
colours.  Greedily pack the four size-eight supports.  After those four
matchings, the residual graph on either selected size-ten support has
minimum degree at least five.  The two-support lemma in
`../first_lift_global_theorem/SIX_PACKING_NOTE.md` coordinates disjoint
perfect matchings on those two supports.  Let \(D\) be the union of these
six matchings.  Then
\[
 |E(D)|=4\cdot4+2\cdot5=26. \tag{6}
\]

For a vertex \(v\), let \(\sigma(v)\) count its occurrences in the six
selected complements, and let \(\rho(v)\) count its occurrences in the
eleven remaining complements.  Since each selected matching saturates its
support,
\[
 d_D(v)=6-\sigma(v),\qquad
 \rho(v)=5-\sigma(v)=d_D(v)-1.
\tag{7}
\]
The selected complements cover every vertex, so
\[
 \Delta(D)\le5,\qquad
 \delta(H)\ge7,\qquad H=K_{13}-D.
\tag{8}
\]

## One of the six remaining size-ten supports extends

Suppose a remaining size-ten support \(Y\) has no perfect matching in
\(H[Y]\).  Coarsening a Tutte barrier into exactly \(s+2\) odd blocks
forces \(D[Y]\) to contain a complete multipartite core.  Under
\(\Delta(D)\le5\), the only possible block patterns are
\[
 K_{5,5}\quad\text{or}\quad K_6. \tag{9}
\]
Indeed, the odd block partitions for \(s=0,\ldots,4\) are the familiar
size-ten catalogue; every other core has maximum degree at least six.

Assume for contradiction that all six unselected size-ten supports are
blocked.

### A \(K_{5,5}\) core

If \(D\) contains a \(K_{5,5}\) on \(Y\), all ten core vertices already
have \(D\)-degree five.  They have no other incident \(D\)-edge, and the
one edge of \(D\) outside the 25-edge core lies among the three vertices
outside \(Y\).  No other connected obstruction core can occur: the
\(K_{5,5}\) component contains no \(K_6\), and any ten-vertex
\(K_{5,5}\) core in it is the same core.

Thus every blocked size-ten support must equal \(Y\), so all six remaining
triple complements are the same outside triple.  On each \(v\in Y\),
(7) gives
\[
 \rho(v)=d_D(v)-1=4.
\]
Those six triples contribute no incidence on \(Y\).  The other remaining
complements—four five-sets and the singleton—have total capacity
\[
 4\cdot5+1=21,
\]
but would have to supply \(10\cdot4=40\) incidences on \(Y\), a
contradiction.

### A \(K_6\) core

If \(D\) contains a \(K_6\) on \(C\), its six vertices likewise have
\(D\)-degree five and no \(D\)-edge to the other seven vertices.  The
remaining graph \(D-C\) has only \(26-15=11\) edges.  Hence no different
connected obstruction core occurs: a second \(K_6\) outside \(C\) would
need fifteen edges, and a \(K_{5,5}\) needs ten vertices.

Every blocked size-ten support must therefore contain \(C\), so all six
remaining triple complements avoid \(C\).  Equation (7) again gives
\(\rho(v)=4\) for every \(v\in C\).  The four remaining five-sets and the
singleton would have to supply \(6\cdot4=24\) incidences on \(C\), more
than their total capacity 21.  This is also impossible.

Consequently at least one remaining size-ten support \(Y\) has a perfect
matching
\[
 M\subseteq H[Y]. \tag{10}
\]

## The size-twelve support also extends

We use a matching-resilience lemma that is independent of the support
arithmetic.

> **Lemma.**  If \(G\) is a graph on twelve vertices with
> \(\delta(G)\ge6\), then \(G-P\) has a perfect matching for every matching
> \(P\subseteq E(G)\).

Suppose \(G-P\) has no perfect matching.  Tutte's theorem gives
\(S\subseteq V(G)\), \(|S|=s\), such that \((G-P)-S\) has at least
\(s+2\) odd components.  If one has order \(c\), a vertex in it has at
most \(c-1\) neighbours inside the component, at most \(s\) in \(S\), and
at most one \(G\)-edge in the other components, because every such edge
must lie in the matching \(P\).  Thus
\[
 6\le d_G(v)\le c+s,\qquad c\ge6-s. \tag{11}
\]
For \(s=0,1,2,3,4\), the least possible total orders of the \(s+2\) odd
components are respectively
\[
 2\cdot7,\quad3\cdot5,\quad4\cdot5,\quad
 5\cdot3,\quad6\cdot3,
\]
all larger than \(12-s\).  If \(s\ge6\), already
\(s+2>12-s\).  The sole remaining case is \(s=5\), with seven singleton
components.

Every one of those seven vertices has at most five neighbours in \(S\)
but degree at least six in \(G\), so it is incident with an edge of
\(G\) inside the seven-set.  Every such edge belongs to \(P\), since the
vertices are separate components of \(G-P\).  The matching \(P\) would
therefore saturate an odd set of seven vertices, impossible.  This proves
the lemma.

Let \(X\) be the unique size-twelve support.  From (8),
\[
 \delta(H[X])\ge6.
\]
Apply the lemma to \(G=H[X]\) and
\[
 P=M\cap E(H[X]).
\]
It supplies a perfect matching \(N\) on \(X\) disjoint from \(M\) and
from \(D\).  The six matchings in \(D\), followed by \(M\) and \(N\), are
the required coordinated eight-packing.

## Verification and exact scope

Run:

```sh
python3 collaboration/coordinated_eight_r1/verify_arithmetic.py
```

The verifier uses only the standard library.  It checks the exact
hypergeometric tables and expectation bound, enumerates every odd-block
partition in the maximum-degree-five size-ten barrier, verifies the core
edge and complement-capacity counts, and checks every finite case in the
twelve-vertex matching-resilience lemma.

Together with
`../first_lift_global_theorem/R0_EIGHTH_MATCHING_THEOREM.md` and
`../coordinated_eight_r2_r5/NOTE.md`, this proves that every target
class-B profile \(r=0,\ldots,5\) has some coordinated eight-packing.  It
therefore applies to the class-B-prime and fan-realizable subfamilies.

The theorem does not pack the final nine colours, prove universal
class-B or fan completion, or solve Erdős--Rosenfeld Problem #835.

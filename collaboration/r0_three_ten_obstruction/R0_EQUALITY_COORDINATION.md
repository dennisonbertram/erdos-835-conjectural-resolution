# Coordinating three size-ten colours at the r0 forced-edge equality boundary

Date: 2026-07-28.

## The theorem

Let an \(r=0\) class-B instance on \(K_{13}\) have a packed
complement-cover six-prefix of profile \(10^3\,8^3\), and let \(D\) be
the union of its six selected matchings.  Thus
\[
 |E(D)|=27,\qquad \Delta(D)\le5. \tag{1}
\]
Suppose \(D\) is \(K_6\)-free and contains
\[
 D[U]=K_6-e \tag{2}
\]
on a six-set \(U\), where \(e\) is the sole missing edge.  Put
\[
 W=V(K_{13})\setminus U,\qquad |W|=7.
\]
Suppose six of the seven remaining triple complements
\[
 T_1,\ldots,T_6
\]
are contained in \(W\).  Their complementary size-ten supports contain
all of \(U\), so every residual perfect matching on any of them uses the
same edge \(e\).

> **Equality-coordination theorem.**  There is a support-preserving
> two-edge trade in one selected layer after which, for any distinct
> \(i,j\in\{1,\ldots,6\}\), the two supports complementary to
> \(T_i,T_j\) and the support complementary to the seventh triple have
> pairwise edge-disjoint perfect matchings.

The proof is solver-free.  Repeated complements are allowed; no
distinctness assumption is used.

## Why there are exactly three equality cases

Let \(x,y\) be the endpoints of \(e\), and let
\[
 a=|E_D(U,W)|.
\]
The four vertices of \(U\setminus\{x,y\}\) already have \(D\)-degree
five in (2), so every selected cross-edge is incident to \(x\) or \(y\).
Each endpoint has degree four inside \(U\), hence initially \(a\le2\).

For a vertex \(v\), its multiplicity \(\rho(v)\) among the eleven
remaining complements satisfies
\[
 \rho(v)=d_D(v)-1. \tag{3}
\]
The four non-endpoints of \(e\) therefore contribute \(4\cdot4\)
remaining-complement incidences on \(U\), while \(x,y\) contribute
\(6+a\).  The total is
\[
 22+a. \tag{4}
\]

Let \(T_*\) be the seventh triple and put
\[
 r=|T_*\cap U|.
\]
The six triples \(T_1,\ldots,T_6\) contribute nothing on \(U\).
The four remaining five-set complements have total capacity twenty, so
(4) gives
\[
 22+a-r\le20,\qquad r\ge2+a. \tag{5}
\]
Since \(1\le r\le3\), the only possibilities are
\[
 (a,r)=(0,2),\qquad(0,3),\qquad(1,3). \tag{6}
\]
In particular,
\[
 a\le1. \tag{7}
\]

## A legal trade

The fourteen core edges in (2) meet at least five selected layers,
because a matching contains at most three edges inside \(U\).  The
number of selected edges inside \(W\) is
\[
 27-14-a=13-a\ge12, \tag{8}
\]
so they meet at least four selected layers.  Hence some selected layer
contains both
\[
 uv\in E(D[U]),\qquad pq\in E(D[W]). \tag{9}
\]

For the case \((a,r)=(0,2)\), write
\[
 T_*\cap W=\{w_*\}.
\]
We choose \(pq\) away from \(w_*\).  At most five of the thirteen
selected \(W\)-edges meet \(w_*\), so at least eight avoid it.  Those
eight edges meet at least three layers; the core edges meet at least
five.  Thus a layer satisfying (9) with
\[
 p,q\ne w_* \tag{10}
\]
exists.

Replace the two edges in (9) by one of
\[
 \{up,vq\},\qquad\{uq,vp\}. \tag{11}
\]
There is at most one old selected cross-edge by (7), while the two
candidate pairs in (11) are disjoint.  At least one pair therefore
consists of unused edges.  Use that pair.

This is a perfect matching trade on the same four endpoints, so it
preserves the selected support, all layer disjointness, and every vertex
degree.  Write \(D'\) for the new union and
\[
 H=K_{13}-D'.
\]
Then
\[
\begin{aligned}
H[U]&=\{e,uv\},\\
F:=E_{D'}(U,W)&\text{ has }|F|=a+2\le3
                 \text{ and }\Delta(F)\le2,\\
H[U,W]&=K_{6,7}-F.
\end{aligned} \tag{12}
\]
The trade also leaves \(D'\) \(K_6\)-free.  Its graph on \(U\) misses
two edges, its graph on \(W\) has only \(12-a<15\) edges, and a mixed
\(K_6\) would require at least five cross-edges, while \(D'\) has at
most three.

## Two forced supports coordinate

Fix any distinct \(T_i,T_j\) among the six triples inside \(W\), and put
\[
 Q_i=W\setminus T_i,\qquad Q_j=W\setminus T_j.
\]
Both have order four.  We will use \(e\) in the first perfect matching
and \(uv\) in the second.  Their remaining cross-matchings must join
\[
\begin{array}{c|c}
A_1=U\setminus V(e)&Q_i\\
A_2=U\setminus\{u,v\}&Q_j.
\end{array} \tag{13}
\]

First choose a perfect matching \(C_1\) between \(A_1\) and \(Q_i\) in
\(H\).  This is possible because a Hall obstruction in \(K_{4,4}\)
deletes at least four edges, while \(F\) has at most three.

Now delete \(C_1\) and consider \(A_2,Q_j\).  If Hall fails on a set
\(S\subseteq A_2\), \(|S|=s\), then all edges in a rectangle of size at
least
\[
 s(5-s) \tag{14}
\]
are deleted.  For \(s=1,2,3,4\), these thresholds are
\[
 4,\ 6,\ 6,\ 4. \tag{15}
\]
The matching \(C_1\) contributes at most
\[
 1,\ 2,\ 2,\ 1 \tag{16}
\]
edges to the corresponding rectangles.  For \(s=1,4\), the degree bound
\(\Delta(F)\le2\) contributes at most two more; for \(s=2,3\), the
total-size bound \(|F|\le3\) contributes at most three.  Thus the total
possible deletions are at most
\[
 3,\ 5,\ 5,\ 3, \tag{17}
\]
strictly below (15).  Hall supplies a second cross-matching \(C_2\).

Consequently
\[
 M_1=\{e\}\cup C_1,\qquad
 M_2=\{uv\}\cup C_2 \tag{18}
\]
are edge-disjoint perfect matchings on the two chosen forced supports.

## The case (a,r)=(0,2)

The seventh support has four vertices
\[
 A_3=U\setminus T_*
\]
and the six-set \(W\setminus\{w_*\}\).  By (10), the newly residual edge
\(pq\) lies in that six-set.  Reserve \(pq\) for the seventh matching
and put
\[
 B_3=W\setminus\{w_*,p,q\}.
\]
Both sets \(A_3,B_3\) have order four.  The two new selected
cross-edges in (11) end at \(p,q\), and \(a=0\), so
\[
 H[A_3,B_3]=K_{4,4}. \tag{19}
\]

Deleting the restrictions of \(C_1,C_2\) leaves minimum degree at least
two in (19).  Every balanced bipartite graph on \(4+4\) vertices with
minimum degree at least two has a perfect matching.  Indeed, Hall is
immediate for sets of order one or two.  If a three-set had at most two
neighbours, either right vertex outside its neighbourhood would have
degree at most one; and the full left set sees every right vertex.

Let \(C_3\) be the resulting matching.  Then
\[
 M_3=\{pq\}\cup C_3 \tag{20}
\]
is a perfect matching on the seventh support, disjoint from (18).  This
settles \((a,r)=(0,2)\).

## A two-edge matching inside W for r=3

It remains to treat \((a,r)=(0,3),(1,3)\), where \(T_*\subseteq U\).
Before the trade, the residual graph on \(W\) has
\[
 21-(13-a)=8+a \tag{21}
\]
edges.  The trade adds \(pq\), so \(H[W]\) has \(9+a\) edges.

We claim that \(H[W]\) contains a two-edge matching \(N\) whose endpoints
include \(p,q\), and, when \(a=1\), also include the \(W\)-endpoint
\(w_0\) of the old selected cross-edge.

For \(a=0\), if the old residual graph has an edge disjoint from \(pq\),
use it together with \(pq\).  Otherwise all eight old residual edges
meet \(\{p,q\}\).  A seven-vertex graph with matching number at most one
has at most six edges: its pairwise-intersecting edge family is a star or
a triangle.  Hence two old residual edges are disjoint.  Since both meet
\(\{p,q\}\), together they cover \(p,q\).

Now let \(a=1\).  The old selected cross-edge at \(w_0\) leaves
\[
 d_{H[W]}(w_0)\ge2, \tag{22}
\]
because its selected degree inside \(W\) was at most four.  If
\(w_0\in\{p,q\}\), the preceding argument already works.  Otherwise,
if \(w_0\) has a neighbour \(s\notin\{p,q\}\), use \(w_0s\) and \(pq\).
If not, (22) gives both \(w_0p,w_0q\).  An edge from \(q\) to one of the
other four vertices pairs with \(w_0p\), and symmetrically an edge from
\(p\) pairs with \(w_0q\).  If neither exists, all ten edges of \(H[W]\)
would lie in a triangle on \(\{p,q,w_0\}\) and a \(K_4\) on the other
vertices, which together have at most
\[
 3+6=9
\]
edges.  This contradiction proves the claim.

Reserve \(N\) for the seventh support, and put
\[
 A_3=U\setminus T_*,\qquad B_3=W\setminus V(N).
\]
Both have order three.  The set \(B_3\) omits \(p,q\), so it avoids both
new selected cross-edges.  When \(a=1\), it also omits \(w_0\), so it
avoids the old selected cross-edge.  Therefore
\[
 H[A_3,B_3]=K_{3,3}. \tag{23}
\]

## The final K2,2 switch

Delete the restrictions of \(C_1,C_2\) from (23).  If a perfect matching
\(C_3\) remains, then
\[
 M_3=N\cup C_3
\]
finishes the proof.

Suppose no perfect matching remains.  The deleted edges form the union
of two matchings, hence have maximum degree at most two.  A Hall failure
on one vertex or on all three vertices would require deletion degree
three at a left or right vertex.  The only remaining possibility is a
two-set with at most one neighbour.  Exact equality forces an alternating
\(K_{2,2}\).  To avoid reusing the earlier names \(p,q\) for the
trade-edge endpoints, relabel the right vertices of this \(K_{2,2}\) as
\(\ell,m\):
\[
\begin{array}{c|cc}
&\ell&m\\ \hline
C_1&x\ell&ym\\
C_2&xm&y\ell.
\end{array} \tag{24}
\]
Let \(z\) be the third vertex of \(A_3\) and \(n\) the third vertex of
\(B_3\).

Besides \(x\ell,ym\), the four-edge matching \(C_1\) has two edges
\[
 a_1b_1,\qquad a_2b_2, \tag{25}
\]
where \(a_i\notin\{x,y\}\) and \(b_i\notin\{\ell,m\}\).  For each
\(i=1,2\), consider the two support-preserving switches
\[
\begin{aligned}
 x\ell,\ a_ib_i&\longmapsto xb_i,\ a_i\ell,\\
 ym,\ a_ib_i&\longmapsto yb_i,\ a_im.
\end{aligned} \tag{26}
\]
Every candidate new edge is automatically outside \(C_2\): \(C_2\)
matches \(x\) to \(m\) and \(y\) to \(\ell\).  The four pairs of
candidate new edges in (26) are pairwise
disjoint.  If every switch used an edge of \(F\), then \(|F|\ge4\),
contrary to (12).  Hence one switch is legal in \(H\) and keeps the two
forced matchings disjoint.

If the legal switch frees \(x\ell\), then
\[
 x\ell,\qquad yn,\qquad zm \tag{27}
\]
is a perfect matching of the good \(K_{3,3}\).  The first edge was freed;
the other two were unused because \(C_1,C_2\) already use the other two
edges at \(y\) and at \(m\).  The new edges in the first line of (26)
meet neither \(yn\) nor \(zm\).  If the switch frees \(ym\), use instead
\[
 ym,\qquad xn,\qquad z\ell. \tag{28}
\]
Adjoining the reserved two-edge matching \(N\) proves the theorem in
both \(r=3\) cases.

## Scope

This theorem closes the entire **six-fold common-forced-edge equality
boundary** after a \(K_6\)-free complement-cover six-prefix.  In
particular, the K6-free dead prefix in
`K6_FREE_MIXED_DEAD_PREFIX.md` is not an isolated accident: every
configuration with six size-ten matching families forced through the
same edge is repaired by one selected-layer trade and then yields three
size-ten colours.

It does **not** by itself prove coordinated nine for all \(r=0\)
instances.  A full theorem still needs to show that any failure to
coordinate three of the seven size-ten families reduces to this common
forced-edge boundary, or handle the other cross-family obstruction
patterns directly.  That cross-family reduction is not proved here.

## Verification

Run:

```sh
python3 collaboration/r0_three_ten_obstruction/verify_r0_equality_coordination.py
```

The standard-library verifier checks the three incidence cases, layer
counts, Hall rectangle inequalities, the \(K_{4,4}\) terminal bound, and
the four-choice \(K_{2,2}\) switch.  It also exhaustively checks the two
small \(W\)-matching claims over every labelled nine- and ten-edge graph
on seven vertices satisfying their hypotheses.

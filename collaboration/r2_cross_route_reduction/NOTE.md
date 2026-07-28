# A cross-route reduction for the \(r=2\) coordinated-nine frontier

Date: 2026-07-28.

## Result and scope

Let \(D\) be the edge union of a complement-cover six-prefix of type
\(8^4\,10^2\) in a target class-B \(r=2\) instance, and put
\[
G=K_{13}-D.
\]
Write \(A_1,\ldots,A_5\) for the five remaining size-five complements,
\(T_1,\ldots,T_4\) for the four remaining triples, and \(x,y\) for the
two singleton complements.

This note proves the following conditional reduction.

> **Cross-route theorem.** Suppose that, for every \(j=1,\ldots,4\), a
> perfect matching on the size-ten support \(V\setminus T_j\), followed
> by a near-factor missing \(x\), reaches a hard terminal \(K_7\) branch
> whose \(D\)-core has seventeen edges. Then:
>
> 1. all four terminal seven-sets are the same set \(U\);
> 2. \(D[U]\) has six internally \(D\)-saturated vertices \(Z\) and one
>    vertex of internal \(D\)-degree four;
> 3. at least three of the five size-eight supports \(V\setminus A_i\)
>    already have perfect matchings in \(G\); and
> 4. none of those three supports can reach a hard seventeen-edge
>    \(K_7\) branch after a size-eight matching.
> 5. the fixed six-prefix has a coordinated nine-extension.

Thus a counterexample cannot put all four size-ten routes and all
available size-eight routes into the same dense terminal obstruction.
The remaining mixed cases must coordinate an initially blocked
size-eight core \(K_{3,5}\), \(K_{3,1^3}\), or \(K_5\) with at most two
rigid size-ten rows and the remaining five-saturated or ordinary
size-ten terminal routes.

This is a conditional branch theorem, not a universal coordinated-nine
theorem: it closes the case in which all four size-ten choices reach
hard seventeen-edge cores.  Other mixtures of size-ten terminal types
remain open, so \(r=2\) is not resolved.

To prove item 5, first observe that every size-eight \(K_7\) terminal
branch with \(|A_i\cap U|\ge3\) is switchable.  If the first
near-factor is in an ordinary \(a_P\ge2,d_P\ge1\) row, the ordinary
near-factor switch applies outside the all-bad column, while that
column has its own \(K_{4,4}\) repair.  If the size-eight matching is
ordinary but the near-factor is not, the endpoint equations with
\(|A_i\cap U|\ge3\) leave only the \(P_4\) row; the eleven-row \(P_4\)
switch applies.  If neither row is ordinary, the hard seventeen-edge
catalogue has \(|A_i\cap U|\le2\), while its sixteen-edge rows are again
\(P_4\) rows.  These exhaust the \(K_7\) catalogue.

Now, if some \(A_i\) contains all five of its vertices in \(Z\), its
size-eight support is matchable by the construction below.  A
\(K_{5,7}\) or \(K_{3,1^5}\) terminal failure would require five
saturated vertices outside \(A_i\), impossible because there are at
most nine saturated vertices and \(A_i\) already contains five.  A hard
terminal \(K_7\) branch is switchable by the preceding paragraph.

If no \(A_i\) contains five vertices of \(Z\), then (8) and
\(|A_i\cap Z|\le4\) force every \(A_i\) to contain at least three
vertices of \(Z\).  All five size-eight supports are therefore
matchable.  If all five failed, after the same three switching
reductions every failure would be of type \(K_{5,7}\) or
\(K_{3,1^5}\).  Each consumes five saturated row-exclusions, requiring
twenty-five in total.  The exact class-B row identity gives at most
\[
\sum_{i=1}^5|W\setminus A_i|
=|W|+\sum_{w\in W}(t(w)+h(w))
\le9+14=23,
\]
where \(W=\{v:d_D(v)=5\}\).  This contradiction proves the branch
closure.

## Exact size-ten endpoint catalogue

Fix a size-ten matching \(M\), a first near-factor \(P\) missing \(x\),
and a terminal \(K_7\) barrier for the second near-factor missing \(y\).
Let \(U\) be the seven singleton components and \(S\) the five-vertex
separator.  For either selected matching record
\[
(a,b,c,d,e)=(UU,US,Uy,SS,Sy).
\]
For \(M\), let \((r_U,r_S,r_y)\) count its three omitted vertices in
\(U,S,\{y\}\).  The endpoint equations are
\[
2a+b+c=7-r_U,\qquad
b+2d+e=5-r_S,\qquad
c+e=1-r_y. \tag{1}
\]
The first matching has five edges and three omissions; the near-factor
has six edges and one omission.

As in the size-eight reduction, remove the ordinary rows in which
either selected matching has \(a\ge2\) and \(d\ge1\).  Exhausting (1),
and imposing \(a_M+a_P\ge4\), leaves eight hard pairs.  Seven have
\[
|E(D[U])|=21-a_M-a_P=17, \tag{2}
\]
and one has sixteen edges.  In every seventeen-edge row,
\[
r_U\le1. \tag{3}
\]
The verifier lists all eight pairs explicitly.

Four of those eight pairs have \(P=P_4=(2,3,0,0,1)\).  The
support-preserving \(P_4\) switch from the companion size-eight note
applies verbatim to a size-ten \(M\): the switch changes only \(P\), and
the three \(P\)-cross vertices are internally covered by \(M\) because
the selected internal incidences cover \(U\).  In fact the size-ten
endpoint equations give fourteen compatible \(M\)-rows with
\(a_M\ge2\), and the same proof switches all fourteen.

After deleting the four \(P_4\) pairs, the hard size-ten catalogue has
exactly four rows.  They share the \(M\)-type
\[
(r_U,r_S,r_y)=(0,3,0),\qquad
(a,b,c,d,e)_M=(3,1,0,0,1), \tag{13}
\]
and pair it with \(P_1,P_2,P_3\), or \(P_5\).  Call these the
**rigid hard rows**.  Each has a seventeen-edge core, and crucially its
triple complement avoids \(U\).

Equation (2) also forces the internal \(D\)-degree sequence
\[
(5,5,5,5,5,5,4). \tag{4}
\]
Let \(Z\subset U\) be the saturated six-set.  Every \(z\in Z\) has all
five of its \(D\)-edges inside \(U\), so no \(D\)-edge joins \(Z\) to
\(V\setminus U\).

## Uniqueness of the dense seven-core

Two distinct seven-sets cannot both span seventeen edges of \(D\).
Indeed, since \(|E(D)|=26\), their intersection contains at least eight
common edges and hence at least five vertices.

If the intersection has five vertices, a vertex saturated internally
in both cores would need five common neighbours among only four
vertices.  Thus all five common vertices would have to be exceptional
in one core or the other, although there are only two exceptional
vertices in total.

If the intersection has six vertices, at least four are saturated in
both cores.  They force fourteen edges inside the common six-set, and
the exclusive vertex has at least four further internal edges.  This
would give at least eighteen edges in one core.  Therefore the two
seven-sets coincide.

Under the hypothesis of the theorem, all four size-ten terminal
seven-sets are consequently the same \(U\), and their saturated six-set
is the same \(Z\).

There is also no initially blocked size-ten support once any
seventeen-edge terminal core exists.  An initially blocked size-ten
support forces a saturated \(K_6\) in \(D\) (the alternative
\(K_{5,5}\) core violates the degree sum).  A saturated \(K_6\) has no
\(D\)-edge to its seven-vertex complement.  The seventeen-edge
seven-core has minimum internal \(D\)-degree four and is connected, so
it would have to lie wholly in one of those two components.  It cannot
fit in the six-set; in the complementary seven-set it would use
seventeen edges disjoint from the fifteen clique edges, exceeding
\(|E(D)|=26\).  Therefore:

> The presence of one rigid hard size-ten row implies that all four
> remaining size-ten supports are initially matchable.

## The class-B rows force mass onto \(Z\)

For a vertex \(v\), let \(a(v),t(v),h(v)\) count its incidences in the
five remaining \(A_i\), the four remaining \(T_j\), and the two
singleton complements.  The exact row identity is
\[
a(v)+t(v)+h(v)=d_D(v)-1. \tag{5}
\]

By (3), every \(T_j\) meets \(U\), and hence \(Z\), in at most one
vertex.  Therefore
\[
\sum_{z\in Z}t(z)\le4. \tag{6}
\]
The terminal hole \(y\) lies outside \(U\).  Only the other singleton
can meet \(Z\), so
\[
\sum_{z\in Z}h(z)\le1. \tag{7}
\]
Every \(z\in Z\) has \(d_D(z)=5\).  Summing (5) on \(Z\) and using
(6)--(7) gives
\[
\sum_{i=1}^5|A_i\cap Z|
=24-\sum_{z\in Z}(t(z)+h(z))
\ge19. \tag{8}
\]
If two of the five intersections had order at most one, the left side
of (8) would be at most
\[
1+1+5+5+5=17.
\]
In particular, at least three of the \(A_i\) meet \(Z\) in at least
three vertices.  Otherwise the left side of (8) would be at most
\[
5+5+2+2+2=16.
\]
(The stronger but less useful statement that at least four intersections
have order at least two follows similarly.)

## Those three size-eight supports are matchable

Put
\[
H=G[V\setminus Z].
\]
The exceptional vertex of \(U\) has four \(D\)-edges to \(Z\).
The six vertices of \(Z\) have total internal degree thirty, so
\[
|E(D[Z])|=(30-4)/2=13.
\]
Consequently exactly
\[
26-13-4=9 \tag{9}
\]
edges of \(D\) lie wholly in the seven-set \(V\setminus Z\).  Thus
\[
H=K_7-F,\qquad |E(F)|=9. \tag{10}
\]
Also every edge between \(Z\) and \(V\setminus U\) belongs to \(G\).
Write \(q=U\setminus Z\).  The four internal \(D\)-edges at \(q\) join
it to \(Z\), while \(d_D(q)\le5\).  Thus \(q\) has at most one missing
edge inside \(V\setminus Z\), and every other vertex of
\(V\setminus Z\) is complete in \(G\) to \(Z\).

Fix \(A=A_i\), let \(k=|A\cap Z|\ge3\), and put
\[
Y=V\setminus A.
\]

* If \(k=3\), then \(Y\setminus Z\) has five vertices.  Its induced
  graph in \(H\) has at least
  \(\binom52-9=1\) edge.  If \(q\) is present, choose instead an edge
  of \(H\) incident with \(q\): it has at least three neighbours in
  this five-set.  Use the chosen edge and match the remaining three
  outside vertices across to the three vertices of \(Y\cap Z\).
* If \(k=4\), then \(Y\setminus Z\) has six vertices and spans at least
  \(\binom62-9=6\) edges of \(H\).  A graph on six vertices with
  matching number at most one has at most five edges.  Hence it has two
  disjoint edges.  If \(q\) is present, the six-edge lower bound gives
  a non-\(q\) edge, and \(q\), which has at least four neighbours in
  this six-set, can be paired to a vertex outside that edge.  Thus the
  two-edge matching can be chosen to cover \(q\).  Use it and match the
  two remaining outside vertices across to \(Y\cap Z\).
* If \(k=5\), then \(Y\setminus Z=V\setminus Z\), and (10) gives twelve
  edges.  The six-set \(H-q\) has at least six edges and hence a
  two-edge matching.  Of the two vertices it leaves uncovered, at least
  one is adjacent to \(q\), because \(q\) has at most one missing
  \(H\)-edge.  Add that \(q\)-edge.  The resulting three-edge matching
  leaves a vertex other than \(q\), which can be matched to the one
  vertex of \(Y\cap Z\).

Therefore every \(A_i\) counted above has a perfect matching on its
size-eight support.

## The same dense terminal core cannot recur

In the hard seventeen-edge size-eight endpoint catalogue, the five
omitted vertices of the size-eight matching satisfy
\[
|A_i\cap U|=r_U\le2. \tag{11}
\]
But each of the three matchable complements above has
\[
|A_i\cap U|\ge|A_i\cap Z|\ge3. \tag{12}
\]
It cannot produce a hard seventeen-edge terminal branch on the common
set \(U\).  By uniqueness, no different seventeen-edge terminal
seven-set exists.  This proves the theorem.

## Three rigid size-ten failures already suffice

The same argument closes a broader branch.

> **Three-rigid theorem.** If at least three of the four size-ten
> candidates reach rigid hard rows, the fixed six-prefix has a
> coordinated nine-extension.

The three rigid triples avoid their common \(U\), hence avoid \(Z\).
The fourth remaining triple contributes at most three incidences to
\(Z\), and \(y\notin Z\) leaves at most one singleton incidence there.
The saturated row identity therefore gives
\[
\sum_{i=1}^5|A_i\cap Z|\ge24-3-1=20. \tag{14}
\]
If one intersection has order five, its support is matchable and a
five-saturated terminal type is impossible, exactly as in the proof of
item 5.  If no intersection has order five, (14) and the upper bound
four force
\[
|A_i\cap Z|=4\qquad(i=1,\ldots,5). \tag{15}
\]
All five size-eight supports are matchable.  Their \(K_7\) terminal
branches are switchable: the all-bad column has its own \(K_{4,4}\)
switch; an ordinary first near-factor switches; and
the exact endpoint catalogue with \(r_U\ge4\) otherwise leaves only a
\(P_4\) row.  Thus five failures would again have to be the two
five-saturated terminal types, contradicting \(25>23\).

This leaves only global mixtures with at most two rigid size-ten rows
and ordinary or five-saturated size-ten terminal routes.
Initially blocked size-ten supports can occur only in the zero-rigid
branch.

## Verification

Run:

```sh
python3 collaboration/r2_cross_route_reduction/verify_reduction.py
```

The verifier uses only the Python standard library.  It exhausts the
size-ten endpoint equations, checks the seven/one split between
seventeen- and sixteen-edge hard pairs, independently enumerates the
size-eight hard seventeen-edge rows and verifies (11), replays the dense-core
uniqueness arithmetic, verifies the class-B incidence bound, checks
the extremal matching bounds used above, and exhaustively validates
the small matching bounds used in the three cross-cut constructions.

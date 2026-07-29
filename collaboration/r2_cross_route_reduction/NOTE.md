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

This note records the cross-route reductions culminating in the
coordinated \(r=2\) theorem.  The first theorem below was the key
intermediate branch closure.

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
The later seventeen-core gate removes the all-four hypothesis, and
the switches in the companion terminal-flexibility note close the two
remaining terminal types.  Their combination below proves the
unconditional coordinated \(r=2\) theorem.  It still does not solve the
unrestricted Erdős--Rosenfeld problem.

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

In fact the same core excludes every initially blocked size-eight
support.  Write \(U=Z\cup\{q\}\), where \(Z\) is the saturated six-set.
There is no \(D\)-edge from \(Z\) to \(V\setminus U\), and \(q\) already
has four internal \(D\)-edges.  Hence
\[
|E_D(U,V\setminus U)|\le1,\qquad
|E(D[V\setminus U])|\le26-17=9. \tag{16}
\]
Also
\[
G[U]\cong P_3\mathbin{\dot\cup}K_2\mathbin{\dot\cup}K_2. \tag{17}
\]

An initially blocked size-eight support has one of the three connected
cores
\[
K_{3,5},\qquad K_{3,1,1,1},\qquad K_5. \tag{18}
\]
Every nontrivial cut in these graphs has respectively at least
\(3,3,4\) edges, so (16) prevents a core from spanning the
\(U{:}(V\setminus U)\) cut.  None can lie wholly outside \(U\):
\(K_{3,5}\) has too many vertices, while the other two have twelve and
ten edges, both exceeding nine.

Nor can a core lie wholly in \(U\).  The \(K_{3,5}\) again has too many
vertices.  A \(K_5\) in \(D[U]\) would be an independent five-set in
(17), but
\[
\alpha(P_3\mathbin{\dot\cup}2K_2)=2+1+1=4.
\]
Finally, a \(K_{3,1,1,1}\) on six vertices would require all edges of
(17) induced on those six vertices to lie inside its three-vertex
part.  Deleting a vertex from \(P_3\dot\cup2K_2\) always leaves edges
whose endpoints use at least four vertices, so this is impossible.

Thus one seventeen-edge terminal core makes all five size-eight
supports initially matchable.  The five-eight theorem in the companion
note then gives:

> **Seventeen-core gate theorem.** The presence of any seventeen-edge
> terminal \(K_7\) core after a size-eight or size-ten candidate
> guarantees a coordinated nine-extension of the fixed six-prefix.

Consequently no counterexample to coordinated \(r=2\) can contain a
rigid seventeen-edge terminal row at all.

## The zero-rigid reduction

The endpoint catalogues now give a complete global description of every
terminal \(K_7\) branch, for either a size-eight or size-ten first
matching.

* If the first near-factor has \(a_P\ge2,d_P\ge1\), its ordinary switch
  applies outside the all-bad column.
* The all-bad column has the \(K_{4,4}\) switch.
* If \(P=P_4\), the support-preserving \(P_4\) switch applies (to all
  eleven compatible size-eight rows and all fourteen compatible
  size-ten rows).
* In every remaining compatible endpoint pair,
  \[
  a_M+a_P=4,
  \]
  so \(|E(D[U])|=17\), and the seventeen-core gate theorem supplies a
  different candidate extension.

This is an exact exhaustion, checked independently for both first
support sizes by the verifier.  Therefore:

> **Five-saturated reduction.** In a global counterexample to the fixed
> \(r=2\) six-prefix, every remaining support is either initially
> blocked or, after an initial perfect matching, fails only through the
> \(K_{5,7}\) or \(K_{3,1^5}\) terminal type.  Every candidate of the
> latter kind consumes at least five saturated exclusions from its
> complement row.

For size-ten supports, an initial block is necessarily the unique
saturated \(K_6\) type; the \(K_{5,5}\) type violates the degree sum.
For size-eight supports, the initial cores are exactly
\(K_{3,5}\), \(K_{3,1,1,1}\), and \(K_5\).  The first two contain three
saturated vertices outside the corresponding five-set complement; the
\(K_5\) type is the only initial obstruction without an automatic
three-saturated charge.

This isolates the remaining \(r=2\) theorem as a global
initial-core/row-incidence problem.  No terminal \(K_7\) switching case
remains.

### At most one blocked size-eight support is impossible

Let \(W=\{v:d_D(v)=5\}\), \(w=|W|\le9\).  The exact exclusion budgets
are
\[
\sum_{i=1}^5|W\setminus A_i|=w+t(W)+h(W)\le w+14, \tag{19}
\]
and, over all five \(A_i\) and four \(T_j\),
\[
\sum_i|W\setminus A_i|+\sum_j|W\setminus T_j|
=5w+h(W)\le5w+2. \tag{20}
\]

If no size-eight support is initially blocked, the five-eight theorem
already gives an extension.  Suppose exactly one is blocked.

If its core is \(K_{3,5}\) or \(K_{3,1,1,1}\), its complement excludes
three saturated vertices.  The other four failed size-eight candidates
exclude five each.  For \(w\le8\), the required \(3+4\cdot5=23\)
exclusions exceed (19).  For \(w=9\), every five-set automatically
excludes at least four vertices of \(W\), so the requirement is at
least \(4+4\cdot5=24>23\).

It remains to consider one blocked \(K_5\) row.  The other four
size-eight candidates and all four size-ten candidates each consume at
least five saturated exclusions: a matchable candidate does so by the
five-saturated reduction, while a blocked size-ten candidate contains
a saturated \(K_6\).  Thus (20) must supply at least forty exclusions.
This is impossible for \(w\le7\).

For \(w=8\), each of the four matchable \(A_i\) contains at most three
saturated vertices, so
\[
a(W)\le5+4\cdot3=17.
\]
But the row identity and \(t(W)+h(W)\le14\) give
\[
a(W)=4w-t(W)-h(W)\ge32-14=18.
\]
For \(w=9\), the four non-saturated vertices have total \(D\)-degree
seven.  At most one vertex of the blocking \(K_5\) can be
non-saturated, so at least four clique vertices lie in \(W\).  The
blocking complement avoids that clique and therefore contains at most
five saturated vertices.  The other four \(A_i\) contain at most four
each, giving
\[
a(W)\le5+4\cdot4=21<36-14=22.
\]
This proves:

> **Two-block threshold.** Every global counterexample to the fixed
> \(r=2\) six-prefix must have at least two initially blocked
> size-eight supports.

The cases with two or more blocked size-eight supports, especially
multiple \(K_5\) cores, are the remaining zero-rigid frontier.

### A saturated \(K_6\) always supplies an escape route

Suppose one of the four size-ten supports is initially blocked.  Its
only possible core is a saturated \(K_6\), say on \(B\); every blocked
size-ten support has the same core.  Put \(R=V\setminus B\).  Then
\[
D=K_6[B]\mathbin{\dot\cup}J[R],\qquad |E(J)|=11, \tag{21}
\]
so every \(B{:}R\) edge belongs to \(G\), and \(G[R]\) has ten edges.

First suppose some remaining triple \(T\) meets \(B\).  Put
\(b=|T\cap B|\ge1\).  Its size-ten support contains \(6-b\) vertices
of \(B\) and \(4+b\) vertices of \(R\).  Choose \(b-1\) disjoint edges
in \(G[R]\), then match the remaining \(6-b\) vertices on each side
across the complete cut.  This gives the candidate matching.  The only
nontrivial case is \(b=3\), requiring a two-edge matching in \(G[R]\);
a seven-vertex graph with ten edges has matching number at least two.

For a near-factor missing a vertex of \(R\), all six covered vertices
of \(B\) can be matched across to the six covered vertices of \(R\).
For a near-factor missing a vertex of \(B\), choose one unused edge in
\(G[R]\), then match the other five \(R\)-vertices across to the five
covered \(B\)-vertices.  There are always unused internal edges:
the candidate used at most two, and the two near-factors use at most
one each.

Choose the cross matchings sequentially.  For the first near-factor,
the balanced cross graph has order five or six and has lost at most one
edge at each vertex.  For the second, it has lost at most two.  Thus its
minimum degree is at least \(m-2\ge m/2\), where \(m\in\{5,6\}\), and
Hall's theorem gives the required cross matching.

It remains to suppose all four triples avoid \(B\), so all four
size-ten supports are blocked.  The initial-support dichotomy gives a
matchable size-eight support \(V\setminus A\).  Let
\(k=|A\cap B|\).  Any perfect matching on this support uses all
\(6-k\) covered vertices of \(B\) across the cut and uses \(k-2\)
internal edges of \(G[R]\).  Fix such a matching.  It uses at most
three internal \(R\)-edges, leaving enough for the two near-factors.
The identical sequential cross-matching argument completes both of
them.

Therefore:

> **Saturated-\(K_6\) escape theorem.** If any remaining size-ten
> support is initially blocked, the fixed six-prefix has a coordinated
> nine-extension.

Every global counterexample must consequently have all four size-ten
supports initially matchable.  By the five-saturated reduction, each
of their failures consumes five saturated exclusions.

## Coordinated nine for the \(r=2\) profile

The companion terminal-flexibility note now switches both
five-saturated terminal types as well.  Combine the results:

1. the initial-support dichotomy guarantees an initial perfect matching
   on at least one of the five size-eight or four size-ten supports;
2. after that matching, the first prescribed near-factor always exists;
3. the two five-saturated terminal types are switchable;
4. every terminal \(K_7\) row is ordinary-\(P\), \(P_4\), all-bad, or
   has a seventeen-edge core;
5. the first three \(K_7\) cases are switchable, and the
   seventeen-core gate theorem supplies an extension through another
   support.

Therefore:

> **Coordinated \(r=2\) theorem.** Every target class-B \(r=2\)
> instance, after any legal complement-cover six-prefix of type
> \(8^4\,10^2\), has three further pairwise edge-disjoint
> support-respecting perfect matchings.  Equivalently, the prefix
> extends to a coordinated nine-packing.

This closes the \(r=2\) coordinated-nine profile.  It does not complete
the remaining eight colours, prove fan-realizability, or resolve
Erdős--Rosenfeld Problem #835.  The coordinated-nine profiles \(r=0\)
and \(r=1\) also remain open.

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

The stronger seventeen-core gate theorem supersedes this delimiter:
no rigid size-ten row can occur in a counterexample.  By the
five-saturated reduction, the remaining global work lies entirely in
initially blocked supports and the two five-saturated terminal types.

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

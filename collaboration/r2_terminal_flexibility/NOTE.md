# The \(r=2\) terminal-flexibility frontier

Date: 2026-07-28.

## Scope and result

Stop after a complement-cover six-packing of types \(8^4\,10^2\) in a
target class-B \(r=2\) instance.  Let \(D\) be its edge union and put
\[
G=K_{13}-D.
\]
Then
\[
|E(D)|=26,\qquad 1\le d_D(v)\le5,\qquad \delta(G)\ge7. \tag{1}
\]
Write \(A_1,\ldots,A_5\) for the five remaining size-five complements,
and \(x,y\) for the two remaining singleton complements.

This note proves the terminal part of the coordinated \(r=2\) theorem:

1. after any perfect matching on a remaining size-eight or size-ten
   support, the first prescribed near-perfect matching always exists;
2. failure of the second near-perfect matching has exactly three
   coarsened Tutte types;
3. the \(K_{5,7}\) and \(K_{3,1^5}\) types are locally switchable;
4. every \(K_7\) type is locally switchable except a rigid
   seventeen-edge core, and the companion seventeen-core gate excludes
   that core globally by supplying another support.

Together with the initial-support dichotomy in the companion note,
these statements prove that every target class-B \(r=2\) instance
extends the complement-cover six-prefix to a coordinated nine-packing.
This is only the coordinated-nine \(r=2\) subproblem: it does not pack
the remaining eight colours, address fan realizability, or solve
Erdős--Rosenfeld Problem #835.

## Exact row identity

For a vertex \(v\), let \(a(v)\) count the sets \(A_i\) containing \(v\),
and let \(b(v)\) count its incidences in the four remaining triples and
the two singleton complements.  Every vertex occurs in five complements
in total, while its degree in \(D\) is the number of selected supports
containing it.  Therefore
\[
\boxed{a(v)+b(v)=d_D(v)-1.} \tag{2}
\]
The total \(b\)-mass is
\[
\sum_v b(v)=4\cdot3+2\cdot1=14. \tag{3}
\]

## The first near-factor cannot fail

Fix one \(A=A_i\), put \(Y=V(K_{13})\setminus A\), and suppose \(M\) is
a perfect matching of \(G[Y]\).  Let
\[
Q=G-M.
\]
The graph \(Q-x\) has order twelve and minimum degree at least five.
Indeed, a vertex can lose its edge of \(M\) and its edge to \(x\), and
no more.

A graph of order twelve and minimum degree at least five without a
perfect matching has an independent set of order seven.  This follows
immediately from Tutte's theorem: if a Tutte set has order \(s\), then
each odd component has order at least the least odd integer not smaller
than \(6-s\), and at least \(s+2\) odd components are required.  The
only possible case is \(s=5\), with seven singleton components.

If \(U\) were such an independent seven-set in \(Q-x\), every edge of
\(G[U]\) would belong to \(M\).  But every \(u\in U\) has at most six
vertices outside \(U\), so \(d_G(u)\ge7\) forces an edge of \(G[U]\) at
every vertex.  Thus \(M[U]\) would be 1-regular on seven vertices, an
impossibility.  Hence \(Q-x\) has a perfect matching \(P\), missing the
prescribed vertex \(x\).

Nothing in this argument uses that \(M\) has four rather than five
edges: it uses only that \(M\) is a matching.  The same conclusion
therefore holds when \(M\) is a perfect matching on a remaining
size-ten support.

## Complete terminal Tutte catalogue

Delete \(P\) and the second prescribed omission:
\[
R=G-M-P-y.
\]
This graph has order twelve and minimum degree at least four.  If it has
no perfect matching, let \(S\) be a Tutte set of order \(s\).  Each odd
component of \(R-S\) has order at least the least odd integer not smaller
than \(5-s\), and at least \(s+2\) odd components are required.  The
only surviving possibilities are
\[
\begin{array}{c|c|c}
s&\text{odd component orders}&
\text{core in }D\cup M\cup P\\ \hline
0&5+7&K_{5,7}\\
4&3+1+1+1+1+1&K_{3,1,1,1,1,1}\\
5&1+1+1+1+1+1+1&K_7.
\end{array} \tag{4}
\]
For \(s=4\), there are two literal component partitions:
\(3+1^5\) and \(1^8\).  The row in (4) coarsens both: in the second
case, group any three singleton components into the displayed
three-vertex block.  Thus the block \(C\) used below is connected, and
so \(R[C]\ne\varnothing\), in the literal \(3+1^5\) case; the branch
\(R[C]=\varnothing\) is exactly the coarsened \(1^8\) case.  With this
convention, (4) is the complete coarsened terminal catalogue.

## Row resources consumed by the first two types

Let
\[
W=\{v:d_D(v)=5\}
\]
be the saturated vertices.

In the \(5+7\) case, let \(Z\) be the component of order five.  Each
\(z\in Z\) has seven potential cross-edges in \(K_{13}-y\), none
surviving in \(R\).
The graph \(D\) can supply at most five of them, while \(M\) and \(P\)
can supply at most one each.  Equality is forced throughout.  Hence
\[
Z\subseteq W,\qquad Z\cap A=\varnothing. \tag{5}
\]

In the separator-four case, let \(T\) be the five singleton components
and \(C\) the remaining three-vertex component.  Each \(t\in T\) has
seven potential edges in \(K_{13}\) to
\((T\cup C)\setminus\{t\}\), none surviving in \(R\).
The same \(5+1+1\) equality gives
\[
T\subseteq W,\qquad T\cap A=\varnothing. \tag{6}
\]

Thus either of the first two terminal types consumes five incidences of
the form
\[
(v,A)\quad\text{with}\quad v\in W\setminus A. \tag{7}
\]

There are at most nine saturated vertices.  Indeed, ten degree-five
vertices and the lower bound \(d_D(v)\ge1\) at the other three vertices
would give degree sum at least \(53>2|E(D)|=52\).

Using (2), the total number of saturated row-exclusions across the five
candidate complements is
\[
\begin{aligned}
\sum_{i=1}^5|W\setminus A_i|
 &=5|W|-\sum_{v\in W}a(v)\\
 &=|W|+\sum_{v\in W}b(v)\\
 &\le |W|+14\\
 &\le23. \tag{8}
\end{aligned}
\]
Five terminal obstructions of the first two types would require
twenty-five such exclusions, contradicting (8).  Therefore:

> If all five candidate terminal constructions fail, at least one
> failure has the \(K_7\) type.

## Resource forced by the \(K_7\) type

Let \(U\) be the seven singleton components and \(S\) the five-vertex
Tutte separator.  For \(u\in U\), define
\[
\alpha(u)=
\mathbf1_{\{M(u)\in U\}}+
\mathbf1_{\{P(u)\in U\}}.
\]
All six edges from \(u\) to \(U\setminus\{u\}\) are absent from \(R\).
Consequently
\[
d_{D[U]}(u)+\alpha(u)\ge6. \tag{9}
\]
Since \(d_D(u)\le5\), every \(\alpha(u)\ge1\).

Put \(m=|E(M[U])|\) and \(p=|E(P[U])|\).  Summing \(\alpha\) gives
\[
2(m+p)\ge7,\qquad m+p\ge4. \tag{10}
\]
Because a matching has at most three edges in a seven-set, \(p\le3\),
so \(m\ge1\): the candidate size-eight matching itself must use an edge
inside the terminal seven-set.

Moreover, the endpoints of the internal \(M\)-edges and internal
\(P\)-edges together cover \(U\).  Hence the number of internal
\(M\)-endpoints not used internally by \(P\) is
\[
7-2p\ge1. \tag{11}
\]
At each such endpoint, (9) forces \(d_{D[U]}(u)\ge5\), so \(u\in W\);
it also lies outside \(A\), because it is covered by \(M\).
Thus every \(K_7\) branch consumes both:

* an internal edge of the candidate matching \(M[U]\); and
* at least one saturated row-exclusion \(u\in W\setminus A\).

The next sections use this internal-edge resource to perform
support-preserving switches.  The sole rigid residue is the
seventeen-edge core, handled globally by the companion gate theorem.

### Exact hard endpoint types

For either selected matching, record
\[
(a,b,c,d,e)=(UU,US,Uy,SS,Sy). \tag{12}
\]
For the size-eight matching \(M\), also record the numbers
\((r_U,r_S,r_y)\) of omitted vertices in \(U,S,\{y\}\).  The endpoint
equations are
\[
2a+b+c=7-r_U,\quad
b+2d+e=5-r_S,\quad
c+e=1-r_y. \tag{13}
\]
For \(P\), the same equations have exactly one omitted vertex, namely
its prescribed hole \(x\).

The ordinary \(K_7\) freeing branch looks for a selected matching with
at least two \(UU\)-edges and at least one \(SS\)-edge.  Exhausting the
nonnegative integer solutions of (13), imposing \(a_M+a_P\ge4\) from
(10), and removing every pair in which either matching has
\(a\ge2,d\ge1\), leaves exactly the following six \(M\)-rows:
\[
\begin{array}{c|c|c}
& (r_U,r_S,r_y)&(a,b,c,d,e)\\ \hline
M_1&(2,3,0)&(2,1,0,0,1)\\
M_2&(1,4,0)&(2,1,1,0,0)\\
M_3&(1,3,1)&(2,2,0,0,0)\\
M_4&(1,4,0)&(3,0,0,0,1)\\
M_5&(0,5,0)&(3,0,1,0,0)\\
M_6&(0,4,1)&(3,1,0,0,0),
\end{array} \tag{14}
\]
and the following five \(P\)-rows:
\[
\begin{array}{c|c|c}
&\text{hole location}&(a,b,c,d,e)\\ \hline
P_1&U&(1,3,1,1,0)\\
P_2&U&(1,4,0,0,1)\\
P_3&S&(1,4,1,0,0)\\
P_4&S&(2,3,0,0,1)\\
P_5&y&(1,5,0,0,0).
\end{array} \tag{15}
\]
The compatibility list has only eighteen pairs:
\[
\{M_1P_4,M_2P_4,M_3P_4\}
\ \cup\
\{M_iP_j: i\in\{4,5,6\},\ 1\le j\le5\}. \tag{16}
\]

The ordinary-\(P\) switch used here is the one proved in
`collaboration/k7_terminal_switching/NOTE.md`, equations (9)--(14).
Only \(P\) is switched.  That local proof uses the other selected
matching solely through the facts that it is edge-disjoint from \(P\),
has at most one incidence at each vertex, and, together with \(P\),
covers \(U\) internally as forced by (9).  It therefore applies
unchanged when the other matching \(M\) is perfect on a size-eight or
size-ten support.

There is an additional exact edge invariant in these rows.  Since
\(R[U]\) is empty,
\[
E(K_7[U])=E(D[U])\mathbin{\dot\cup}E(M[U])
          \mathbin{\dot\cup}E(P[U]),
\]
and hence
\[
|E(D[U])|=21-a_M-a_P. \tag{17}
\]
Fifteen of the eighteen pairs have \(a_M+a_P=4\).  They force
\[
|E(D[U])|=17,\qquad
(d_{D[U]}(u):u\in U)=(5,5,5,5,5,5,4). \tag{18}
\]
Equivalently, \(G[U]\) is a four-edge graph with degree sequence
\((2,1,1,1,1,1,1)\), necessarily a three-vertex path plus two
independent edges.  The six degree-five vertices in (18) have no
\(D\)-edge leaving \(U\).

The other three pairs are \(M_4P_4,M_5P_4,M_6P_4\).  They have
\(a_M+a_P=5\), so
\[
|E(D[U])|=16,\qquad
(d_{D[U]}(u):u\in U)=(5,5,5,5,4,4,4). \tag{19}
\]
Thus the eighteen endpoint rows reduce further to fifteen maximally
dense \(17\)-edge cores and three \(16\)-edge cores.

### Uniqueness of the \(17\)-edge core

There cannot be two distinct seven-sets \(U,U'\) with
\[
|E(D[U])|=|E(D[U'])|=17. \tag{20}
\]
Indeed, putting \(T=U\cap U'\), inclusion-exclusion and \(|E(D)|=26\)
give
\[
|E(D[T])|\ge17+17-26=8,
\]
so \(|T|\ge5\).

Each 17-edge core has six vertices of internal \(D\)-degree five and one
of internal degree four.  If \(|T|=5\), every common vertex saturated in
both cores would need five neighbours in the four other vertices of
\(T\), which is impossible.  Thus every vertex of \(T\) would have to
be the exceptional vertex in at least one core, but the two cores have
only two exceptional vertices between them.

If \(|T|=6\), at least four vertices of \(T\) are saturated in both
cores.  Each is adjacent in \(D\) to all other five vertices of \(T\).
Those four vertices force at least
\[
\binom42+4\cdot2=14
\]
edges inside \(T\).  The vertex of \(U\setminus T\) has internal
\(D\)-degree at least four, giving at least eighteen edges in \(D[U]\),
again a contradiction.  The only remaining case is \(|T|=7\), namely
\(U=U'\).

The exact endpoint distribution sharpens this.  In a 17-edge hard row,
\(a_M+a_P=4\), so the seven vertices receive eight internal matching
incidences.  Exactly one vertex is covered internally by both matchings;
it is the unique internal-degree-four vertex of \(D[U]\).  The other six
vertices are \(D\)-saturated.  Consequently:

* in rows \(M_1P_4,M_2P_4,M_3P_4\), exactly three saturated vertices
  are internal \(M\)-only endpoints outside \(A\);
* in the other twelve 17-edge rows, exactly five saturated vertices are
  internal \(M\)-only endpoints outside \(A\).

Finally, all five candidate complements cannot produce 17-edge hard
cores.  By uniqueness they would share one set \(U\), hence one
six-set \(Z\subset U\) of saturated vertices.  Every hard \(M\)-row in
(14) has \(|A_i\cap U|\le2\), so
\[
\sum_{i=1}^5|Z\setminus A_i|\ge5\cdot4=20. \tag{21}
\]
On the other hand, applying (2) to the six vertices of \(Z\) gives
\[
\sum_{i=1}^5|Z\setminus A_i|
=6+\sum_{z\in Z}b(z). \tag{22}
\]
The second prescribed hole \(y\) is not in \(U\), hence not in \(Z\).
At least its singleton incidence lies outside \(Z\), so (3) makes the
right side of (22) at most \(6+13=19\), contradicting (21).

Therefore an all-five collection of hard \(K_7\) branches must include
one of the three 16-edge rows
\[
M_4P_4,\qquad M_5P_4,\qquad M_6P_4. \tag{23}
\]

### All eleven \(P_4\) rows are switchable

Let
\[
B=R[U,S],\qquad
D_s=\{u\in U:us\notin E(B)\}.
\]
Every row of \(B\) has degree at least four, so the missing classes
\(D_s\) are pairwise disjoint.  As in the three-near-factor argument, a
pair \(uv\in\binom U2\) is *bad* precisely when
\[
U\setminus\{u,v\}\subseteq D_s
\quad\text{for some }s\in S. \tag{24}
\]
Outside the case \(D_s=U\), the bad-pair graph has matching number at
most one.

The switch below applies more broadly than the eighteen hard rows in
(16).  Solving the size-eight endpoint equations with \(a_M\ge2\)
gives exactly eleven \(M\)-rows compatible with \(P_4\): seven have
\(a_M=2\) and a seventeen-edge \(D[U]\)-core, while four have
\(a_M=3\) and a sixteen-edge core.  These include the six \(P_4\)
pairs in (16) and five rows previously removed by the ordinary
\(a_M\ge2,d_M\ge1\) filter.

In any of these eleven rows, write the \(P_4\) matching as
\[
uv,\quad wz,\quad
a_1s_1,\ a_2s_2,\ a_3s_3,\quad s_0y, \tag{25}
\]
where the first two edges are \(UU\), the next three are \(US\), and
the last is \(Sy\).  The two \(UU\)-edges are disjoint, so one of them,
say \(uv\), is Hall-good unless \(D_s=U\).

The all-bad case cannot occur here.  If \(D_{s^\ast}=U\), then
\(B=K_{7,4}\) with right side \(S\setminus\{s^\ast\}\).  A selected
\(US\)-edge is absent from \(B\), so each of the three selected
\(US\)-edges in (25) would have to end at the single vertex
\(s^\ast\), impossible in a matching.

Each \(a_i\) is internal to \(M\).  Indeed, it is not internal to \(P\),
while (9) requires at least one internal selected incidence at every
vertex of \(U\).  It is therefore one of the four internally
single-covered vertices, has \(d_{D[U]}(a_i)=5\), and has no \(D\)-edge
leaving \(U\).  Consequently
\[
a_i y,\quad a_i s_0
\]
are available and unused.

If \(\{u,v\}\not\subseteq D_{s_0}\), orient \(uv\) so that
\(vs_0\in B\), and choose \(s_i\) not missed by \(u\).  Switch
\[
uv,\ a_i s_i,\ s_0y
\quad\longrightarrow\quad
u s_i,\ v s_0,\ a_i y. \tag{26}
\]
This frees \(uv\).  The two new \(B\)-edges touch the deleted vertices
\(u,v\), so the original perfect matching of
\(B[U\setminus\{u,v\},S]\) remains available.  Together with \(uv\), it
is the required second near-factor missing \(y\).

It remains to suppose \(\{u,v\}\subseteq D_{s_0}\).  A vertex of
\(D_{s_0}\) that is internally double-covered has
\(d_{D[U]}(v)=4\).  Since both selected incidences are internal,
\(vs_0\in D\), and degree seven forces \(vy\) to be present and unused.
A \(P\)-internal vertex that is not \(M\)-internal has
\(d_{D[U]}(v)=5\).  It cannot be omitted by \(M\), or paired by \(M\)
to \(y\): in either case its missing edge to \(s_0\) would require a
sixth \(D\)-edge or would survive in \(B\).  Thus it must be paired by
\(M\) to \(s_0\), and again its edge to \(y\) is available.  Hence
\(vy\) is available for either orientation, and one may switch
\[
uv,\ a_i s_i,\ s_0y
\quad\longrightarrow\quad
u s_i,\ v y,\ a_i s_0. \tag{27}
\]

There is no label-mutation exception in (27).  In the 16-edge rows, at
most the three double-covered vertices and the one possible \(M_6\)
external endpoint can lie in \(D_{s_0}\), so
\(|D_{s_0}|\le4\).  In the 17-edge rows there is only one
double-covered vertex and at most one \(M\)-edge to \(s_0\), so
\(|D_{s_0}|\le2\).  Deleting \(u,v\) and moving \(a_i\)'s unique
missing label from \(s_i\) to \(s_0\) therefore leaves the new
\(D_{s_0}\) of order at most three.  Every other missing class has order
at most four because \(uv\) was Hall-good.  Hall's theorem still gives
the five cross-edges for the second near-factor.

This proves that all eleven \(P_4\) rows are locally switchable.  Within
the hard endpoint frontier (16), the six \(P_4\) pairs are removed and
the frontier is reduced to the twelve pairs
\[
\{M_iP_j:i\in\{4,5,6\},\ j\in\{1,2,3,5\}\}. \tag{28}
\]
Every row in (28) has the unique 17-edge core, and
\(|A_i\cap U|\le1\).  It therefore consumes at least five exclusions
from the common saturated six-set \(Z\).  Five such rows would require
twenty-five exclusions, while (22) allows at most nineteen.

### The all-bad column is switchable

There is one further useful exact fact about the Hall graph.  Suppose
\[
D_{s_0}=U
\]
for some \(s_0\in S\).  Then
\[
B=K_{U,S\setminus\{s_0\}}.
\]
No selected edge can join \(U\) to \(S\setminus\{s_0\}\), because all
those edges survive in \(B\).  Every \(G\)-edge from \(U\) to \(s_0\)
must be selected, because otherwise it too would survive in the
terminal residual graph.

Fix \(u\in U\).  It has the four displayed neighbours in
\(S\setminus\{s_0\}\), at most one neighbour \(y\), and at most two
further neighbours supplied by its incident edges in the two selected
matchings.  The degree-seven hypothesis forces equality throughout.
In particular, both selected matchings cover \(u\), neither uses
\(uy\), and both selected incidences lie in \(U\cup\{s_0\}\).
This holds for every \(u\in U\).  The size-eight matching therefore
covers all seven vertices of \(U\), so
\[
\boxed{A\cap U=\varnothing.} \tag{29}
\]
Consequently, any candidate with \(A\cap U\ne\varnothing\) automatically
lies outside the all-bad-column exception.

More strongly, the configuration can always be repaired.  Put
\[
L'=(S\setminus\{s_0\})\cup\{y\}.
\]
Each selected matching has exactly three \(UU\)-edges and one
\(Us_0\)-edge.  The size-eight matching ends there; the near-factor
\(P\) additionally has two edges on \(L'\), leaving its prescribed
hole \(x\in L'\).

The vertex \(s_0\) has the two selected neighbours in \(U\), one from
each matching.  Its only other five possible neighbours are the
vertices of \(L'\), so degree seven forces it to be complete to \(L'\).
Those five edges are unused.  The same degree equality above forces
every edge \(uy\), \(u\in U\), to be present and unused.

Choose a \(UU\)-edge \(uv\) and the \(Us_0\)-edge \(ws_0\) of \(P\).
Delete those two edges and the two \(P\)-edges on \(L'\).  The exposed
left vertices
\[
\{u,v,w,s_0\}
\]
and the four exposed, non-omitted vertices of \(L'\) span an unused
\(K_{4,4}\): the \(U\)-to-\(S\setminus\{s_0\}\) edges survive in \(B\),
the \(U\)-to-\(y\) edges were forced above, and \(s_0\) is complete to
\(L'\).  Rematch these eight vertices through that \(K_{4,4}\).

For the second near-factor, use the freed edges \(uv,ws_0\), then match
the four remaining vertices of \(U\) bijectively to
\(S\setminus\{s_0\}\).  The new \(P\)-edges touch only \(u,v,w,s_0\),
whereas the last four edges use the other four vertices of \(U\).
Thus the matchings are edge-disjoint and the terminal obstruction is
repaired.

The same proof applies when the first selected matching has size ten:
it merely has one additional edge inside \(L'\), which is disjoint from
the cross edges used in the switch.

### The remaining ordinary size-eight rows are switchable

Outside the all-bad column, the only ordinary-\(M\), nonordinary-\(P\)
rows not covered by the eleven-row \(P_4\) switch have
\[
(r_U,r_S,r_y)_M=(1,3,1),\qquad
(a,b,c,d,e)_M=(3,0,0,1,0), \tag{30}
\]
with \(P\in\{P_1,P_2,P_3,P_5\}\).  Thus \(M\) consists of three
\(UU\)-edges and one \(SS\)-edge \(st\).

The three \(UU\)-edges form a matching, while the bad-pair graph has
matching number at most one.  Hence at least two of them are Hall-good.
Fix a good edge \(uv\).  The two-edge switch on \(uv,st\) fails exactly
when
\[
\{u,v\}\subseteq D_s
\quad\text{or}\quad
\{u,v\}\subseteq D_t. \tag{31}
\]

Here \(|E(D[U])|=17\).  The six internal \(M\)-endpoints and two
internal \(P\)-endpoints cover \(U\), with one double-covered vertex.
The double-covered vertex has internal \(D\)-degree four; the other six
vertices are saturated.

For any separator label \(q\), its missing class \(D_q\) contains:

* at most the one double-covered vertex; and
* at most one saturated \(M\)-only vertex, namely the endpoint of a
  possible selected \(P\)-edge to \(q\).

The saturated \(P\)-only vertex is omitted by \(M\) and internally
covered by \(P\), so its edge to \(q\) survives in \(B\).  Also the
double-covered vertex belongs to at most one missing class.  Therefore,
for the two distinct labels \(s,t\), at most one of \(D_s,D_t\) can
contain two vertices.  At most one \(UU\)-edge can satisfy (31).

Since at least two \(UU\)-edges are Hall-good, choose one for which
(31) fails.  The bipartite graph
\[
B[\{u,v\},\{s,t\}]
\]
has a perfect matching.  Replace \(uv,st\) by those two cross edges.
They touch only \(u,v\), so the perfect matching of
\(B[U\setminus\{u,v\},S]\), together with the freed edge \(uv\), is the
required second near-factor.  This closes all ordinary size-eight
terminal rows.

### Consequence when all five size-eight supports are matchable

Suppose every one of the five remaining size-eight supports has an
initial perfect matching.  If a candidate cannot be extended through
the two prescribed near-factors, its terminal obstruction is either:

* \(K_{5,7}\) or \(K_{3,1^5}\), consuming five saturated exclusions
  \(W\setminus A_i\); or
* one of the twelve rigid rows in (28), likewise consuming at least
  five saturated exclusions.

All other \(K_7\) rows have now been switched.  Five failed candidates
would therefore require twenty-five saturated row-exclusions, while
(8) supplies at most twenty-three.  Hence:

> **Five-eight theorem.** If all five remaining size-eight supports are
> initially matchable after the complement-cover six-prefix, then the
> prefix has a coordinated nine-extension.

### The two five-saturated terminal types are switchable

The preceding exclusion charges can be sharpened to local repairs.  The
switch is always performed in the near-factor \(P\), so it works when
the first selected matching has either size eight or size ten.

For the \(K_{5,7}\) type, let the two residual components be
\(C_5,C_7\).  Every vertex of \(C_5\) has at least two \(G\)-edges to
\(C_7\).  All such edges lie in \(D\cup M\cup P\); the five \(D\)-edges
and one edge from each selected matching are forced at every vertex.
Thus \(P\) has five cross edges saturating \(C_5\), the residual graph
on \(C_5\) is \(K_5\), and the residual graph on \(C_7\) has minimum
degree four.

Among the five \(P\)-endpoints in \(C_7\), choose adjacent vertices
\(b_1,b_2\), with partners \(a_1,a_2\in C_5\).  Replace
\[
a_1b_1,\ a_2b_2
\quad\longrightarrow\quad
a_1a_2,\ b_1b_2. \tag{32}
\]
For the second near-factor use the freed edge \(a_1b_1\), a perfect
matching of \(C_5-a_1\cong K_4\), and a perfect matching of
\(C_7-b_1\).  The last graph has order six and minimum degree at least
three, so Dirac's theorem applies.

For the \(K_{3,1^5}\) coarsened type, let \(S\) be the four-vertex
separator, let \(T\) be five singleton components, and let \(C\) be
the remaining three-vertex block.  As explained after (4), \(C\) is
either a genuine connected component or a group of three further
singleton components.  Put \(L=S\cup\{y\}\).  Every vertex of \(T\) is
adjacent residually to all four vertices of \(S\).  Degree seven then
forces its other three distinct neighbours to be its unused edge to
\(y\) and its two selected incidences, one in \(M\) and one in \(P\),
both going into \(T\cup C\).  In particular, both selected matchings
cover all five vertices of \(T\).

The near-factor \(P\) has a \(TT\)-edge and an \(LL\)-edge.  Indeed, if
\(a,b\) count its \(TT,TC\) edges, then
\[
2a+b=5,\qquad b\le3,
\]
so \(a\ge1\); after covering \(T\), too few vertices of \(C\) remain to
pair all non-omitted vertices of \(L\).

In the literal \(3+1^5\) case, connectedness of \(C\) guarantees the
following first branch.  If the residual graph on \(C\) contains an
edge \(c_1c_2\), write
\(C=\{c_1,c_2,c_3\}\), choose \(t_1t_2\in E(P[T])\) and
\(uv\in E(P[L])\), and switch
\[
t_1t_2,\ uv
\quad\longrightarrow\quad
t_1u,\ t_2v. \tag{33}
\]
The new edges are available because \(T\) is complete residually to
\(S\) and every \(ty\) is forced unused.  For the second near-factor
use the freed \(t_1t_2\), the edge \(c_1c_2\), an edge \(c_3s_0\) with
\(s_0\in S\), and match the other three vertices of \(T\) bijectively
to \(S\setminus\{s_0\}\).

In the literal \(1^8\) case, the coarsened block \(C\) has empty
residual graph.  Degree four then makes every edge from
\(W=T\cup C\) to \(S\) residual.  The same degree-seven equality
forces every \(wy\), \(w\in W\), to be present and unused, and forces
both selected matchings to pair all eight vertices of \(W\) internally.
The near-factor \(P\) therefore has four \(W\)-edges and two \(L\)-edges.
Delete two of each.  The four exposed \(W\)-vertices and four exposed,
non-omitted \(L\)-vertices span an unused \(K_{4,4}\); rematch \(P\)
through it.  The second near-factor uses the two freed \(W\)-edges and
matches the other four vertices of \(W\) bijectively to \(S\).

These switches preserve the prescribed hole of \(P\) and do not alter
the first selected matching.  Together with the \(K_7\) analysis:

> **Mixed terminal theorem.** In a target class-B \(r=2\) instance,
> after any initial perfect matching on a remaining size-eight or
> size-ten support, the two prescribed near-factors can be packed,
> unless a seventeen-edge \(K_7\) core is reached.  In that last case
> the companion seventeen-core gate theorem gives a coordinated
> nine-extension through another support.

Combined with the initial-support dichotomy in the companion note, this
proves the coordinated \(r=2\) theorem stated there.  The result is
global over the nine remaining support choices; it does not assert that
an arbitrary fixed candidate matching must extend.

## Why a fixed candidate matching is not enough

The quantifier over all five candidate supports is essential even before
the class-B row identity is imposed.  Here is an ambient counterexample.
Let \(D\) have edges
\[
\begin{split}
&02,03,04,05,06,\quad12,13,14,15,16,\\
&24,25,26,\quad34,35,36,\quad46,\quad57,\\
&78,79,7\,10,7\,11,\quad89,8\,10,8\,11,\quad11\,12.
\end{split} \tag{34}
\]
Then \(|E(D)|=26\) and \(\Delta(D)=5\).  In \(G=K_{13}-D\), take
\[
Y=\{0,\ldots,7\},\qquad
M=\{01,23,45,67\},\qquad x=8,\ y=9. \tag{35}
\]
Put \(Q=G-M\) and \(U=\{0,\ldots,6\}\).  Directly from (32)--(33),
\[
E(Q[U])=\{56\}. \tag{36}
\]
After deleting either \(8\) or \(9\), only five vertices remain outside
the seven-set \(U\).  Every perfect matching must therefore use an edge
inside \(U\), and (34) says that edge must be \(56\).  Thus every
near-perfect matching missing \(8\), and every one missing \(9\), uses
the same edge \(56\); no two can be edge-disjoint.

This counterexample satisfies the raw six-prefix edge and degree bounds,
but the displayed \(Y,M,x,y\) data are not asserted to extend to the
five-candidate class-B row inventory.  It refutes only a universal lemma
for one arbitrary candidate matching.

## Verification

Run:

```sh
python3 collaboration/r2_terminal_flexibility/verify_terminal.py
```

The standard-library verifier exhausts the Tutte arithmetic in (4),
checks the row-resource bounds (8)--(11), enumerates the hard endpoint
types (14)--(31), audits the switches (32)--(33), reconstructs the
counterexample (34)--(36), and
independently enumerates its two families of near-perfect matchings to
confirm that no edge-disjoint pair exists.

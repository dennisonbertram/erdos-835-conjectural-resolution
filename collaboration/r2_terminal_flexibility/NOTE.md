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

This note proves:

1. after any perfect matching on a candidate size-eight support, the
   first prescribed near-perfect matching always exists;
2. failure of the second near-perfect matching has exactly three
   coarsened Tutte types;
3. two types each consume five saturated row-exclusions, so the exact
   class-B row identity prevents those two types from blocking all five
   candidate supports;
4. therefore an all-five failure must contain at least one \(K_7\)
   terminal branch.

This is a solver-free finite reduction, not a coordinated-nine theorem
for \(r=2\).  The remaining problem is to switch a candidate
size-eight matching or the first near-factor through the forced \(K_7\)
branch while preserving its support.

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
Thus (4) is the complete coarsened terminal catalogue.

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

The unresolved step is to use this internal-edge resource to perform a
support-preserving switch that frees a Hall-good pair in \(U\), uniformly
over all five choices of \(A_i\).

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

### All six \(P_4\) rows are switchable

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

In each of the six rows \(M_iP_4\), \(1\le i\le6\), write the \(P_4\)
matching as
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

This proves that all six \(P_4\) rows are locally switchable.  The hard
endpoint frontier (16) is reduced to the twelve pairs
\[
\{M_iP_j:i\in\{4,5,6\},\ j\in\{1,2,3,5\}\}. \tag{28}
\]
Every row in (28) has the unique 17-edge core, and
\(|A_i\cap U|\le1\).  It therefore consumes at least five exclusions
from the common saturated six-set \(Z\).  Five such rows would require
twenty-five exclusions, while (22) allows at most nineteen.

This still does not prove coordinated nine for \(r=2\): a global failure
may mix the first two terminal types in (4), ordinary labelled \(K_7\)
rows whose switches require a separate audit, and fewer than five of the
twelve rows in (28).

Thus a full switch proof need not treat arbitrary endpoint patterns.
After the ordinary branch is audited, its genuinely hard local work is
the eighteen labelled rows in (16), together with the all-bad-column
case in the Hall graph \(R[U,S]\).  Enumeration (14)--(16) is only a
finite reduction; it does not itself assert that the omitted ordinary
rows are switchable.

## Why a fixed candidate matching is not enough

The quantifier over all five candidate supports is essential even before
the class-B row identity is imposed.  Here is an ambient counterexample.
Let \(D\) have edges
\[
\begin{split}
&02,03,04,05,06,\quad12,13,14,15,16,\\
&24,25,26,\quad34,35,36,\quad46,\quad57,\\
&78,79,7\,10,7\,11,\quad89,8\,10,8\,11,\quad11\,12.
\end{split} \tag{29}
\]
Then \(|E(D)|=26\) and \(\Delta(D)=5\).  In \(G=K_{13}-D\), take
\[
Y=\{0,\ldots,7\},\qquad
M=\{01,23,45,67\},\qquad x=8,\ y=9. \tag{30}
\]
Put \(Q=G-M\) and \(U=\{0,\ldots,6\}\).  Directly from (29)--(30),
\[
E(Q[U])=\{56\}. \tag{31}
\]
After deleting either \(8\) or \(9\), only five vertices remain outside
the seven-set \(U\).  Every perfect matching must therefore use an edge
inside \(U\), and (19) says that edge must be \(56\).  Thus every
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
types (14)--(28), reconstructs the counterexample (29)--(31), and
independently enumerates its two families of near-perfect matchings to
confirm that no edge-disjoint pair exists.

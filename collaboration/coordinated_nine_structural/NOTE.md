# Structural reduction for a coordinated ninth matching

Date: 2026-07-28.

## Scope and result

Let \(F\) be the union of eight pairwise edge-disjoint support-perfect
matchings in a target class-B instance on \(K_{13}\), and put
\[
 H=K_{13}-F.
\]
This note gives:

1. the exact coarsened Tutte obstruction catalogues for an unused support
   of size \(8,10\), or \(12\);
2. the sharper catalogues for the coordinated \(r=1,\ldots,5\)
   eight-packings already constructed in this repository;
3. an exact complement-row reuse bound for every fixed obstruction core;
4. the resulting finite overlap frontier for a ninth matching.

This is a solver-free finite reduction, not yet a universal
ninth-matching theorem.

## Exact eight-prefix identities

Every vertex belongs to twelve of all seventeen supports.  If
\(\sigma(v)\) is the number of selected complements containing \(v\), then
\[
 d_F(v)=8-\sigma(v).
\]
If \(\rho(v)\) counts the remaining nine complements containing \(v\),
then
\[
 \boxed{\rho(v)=5-\sigma(v)=d_F(v)-3.} \tag{1}
\]
In particular,
\[
 3\le d_F(v)\le8,\qquad \delta(F)\ge3. \tag{2}
\]

The coordinated constructions have the following exact selected profiles,
edge totals, and remaining support inventories:
\[
\begin{array}{c|c|c|c}
r&\text{selected supports}&|E(F)|&
(\text{remaining }n_8,n_{10},n_{12})\\ \hline
0&8^4\,10^4&36&(3,6,0)\\
1&8^4\,10^3\,12&37&(4,5,0)\\
2&8^4\,10^2\,12^2&38&(5,4,0)\\
3&8^4\,10^2\,12^2&38&(6,2,1)\\
4&8^4\,10^2\,12^2&38&(7,0,2)\\
5&8^4\,12^4&40&(8,0,1).
\end{array} \tag{3}
\]
For \(r=1,\ldots,5\), the first six matchings were chosen from a
complement cover and have union of maximum degree at most five.  Adding
the last two matchings gives the stronger bound
\[
 \Delta(F)\le7. \tag{4}
\]
The \(r=0\) theorem starts with an arbitrary seven-prefix, so only the
general bound \(\Delta(F)\le8\) is available there.

## Tutte coarsening

Let \(V\) be an unused support of even order \(n\in\{8,10,12\}\), and
suppose \(H[V]\) has no perfect matching.  Tutte's theorem supplies
\(S\subseteq V\), \(|S|=s\), such that \(H[V]-S\) has more than \(s\)
odd components.  Parity gives at least \(s+2\).

Absorb every even component into an odd component and repeatedly merge
three odd blocks until exactly \(s+2\) odd blocks remain.  Their odd orders
\[
 a_1\le\cdots\le a_{s+2},\qquad
 \sum_i a_i=n-s, \tag{5}
\]
partition \(V\setminus S\).  No \(H\)-edge joins distinct blocks, so
\(F\) contains the complete multipartite core
\[
 K_{a_1,\ldots,a_{s+2}}. \tag{6}
\]

The tables below list every odd partition in (5) surviving the applicable
maximum-degree and edge-budget constraints.  The columns give the core
order \(c\), edge count \(e\), and maximum degree \(\Delta\).
Here and below, "exact catalogue" means exact exhaustion of the
coarsened Tutte possibilities under the stated necessary screens.  It
does not assert that every listed core is realizable in a valid coloured
prefix.

## Size-eight catalogue

All six possible types survive even under (4):
\[
\begin{array}{c|c|c|c|c}
s&\text{blocks}&\text{core}&e&\Delta\\ \hline
0&1+7&K_{1,7}&7&7\\
0&3+5&K_{3,5}&15&5\\
1&1+1+5&K_{5,1,1}&11&6\\
1&1+3+3&K_{3,3,1}&15&6\\
2&1+1+1+3&K_{3,1,1,1}&12&5\\
3&1+1+1+1+1&K_5&10&4.
\end{array} \tag{7}
\]

## Size-ten catalogue

For a general eight-prefix with \(\Delta(F)\le8\), the exact list is
\[
\begin{array}{c|c|c|c|c}
s&\text{blocks}&\text{core}&e&\Delta\\ \hline
0&3+7&K_{3,7}&21&7\\
0&5+5&K_{5,5}&25&5\\
1&1+1+7&K_{7,1,1}&15&8\\
1&1+3+5&K_{5,3,1}&23&8\\
1&3+3+3&K_{3,3,3}&27&6\\
2&1+1+1+5&K_{5,1,1,1}&18&7\\
2&1+1+3+3&K_{3,3,1,1}&22&7\\
3&1+1+1+1+3&K_{3,1,1,1,1}&18&6\\
4&1+1+1+1+1+1&K_6&15&5.
\end{array} \tag{8}
\]
The omitted \(1+9\) type has maximum degree nine.  In the coordinated
nonzero profiles, (4) also removes the two degree-eight rows, leaving the
seven familiar types
\[
 37,\ 55,\ 333,\ 5111,\ 3311,\ 31111,\ 6. \tag{9}
\]

## Size-twelve catalogue

The minimum-degree condition (2) adds a useful global screen.  For a core
\(J\), define the degree-three deficits on all thirteen vertices by
\[
 q_v=\max\{0,3-d_J(v)\}.
\]
Any completion of \(J\) to \(F\) needs at least
\[
 \tau_3(J)=
 \max\left\{\max_vq_v,\,
 \left\lceil\frac{\sum_vq_v}{2}\right\rceil\right\}
\tag{10}
\]
additional edges.  Thus \(e(J)+\tau_3(J)\le |E(F)|\) is necessary.

After the maximum-degree and (10) screens, a general eight-prefix has four
base types:
\[
\begin{array}{c|c|c|c|c|c}
s&\text{blocks}&\text{core}&e&\Delta&e+\tau_3\\ \hline
3&1+1+1+1+5&K_{5,1,1,1,1}&26&8&32\\
3&1+1+1+3+3&K_{3,3,1,1,1}&30&8&36\\
4&1+1+1+1+1+3&K_{3,1,1,1,1,1}&25&7&33\\
5&1+1+1+1+1+1+1&K_7&21&6&30.
\end{array} \tag{11}
\]
When \(|E(F)|\ge38\), one additional type is possible:
\[
 K_{5,7},\qquad e=35,\quad\Delta=7,\quad e+\tau_3=38.
\tag{12}
\]
The only other degree-at-most-eight candidate is \(K_{5,3,3}\).  It has
39 edges on eleven vertices, while its two outside vertices require at
least three more edges to reach degree three.  Hence it would require at
least 42 edges and is impossible in every profile.

For the coordinated nonzero packings, (4) removes the two degree-eight
types in (11).  Thus an unused size-twelve support can be blocked only by
\[
 K_{3,1,1,1,1,1},\quad K_7,
\quad\text{and, when allowed by the exact row count, }K_{5,7}.
\tag{13}
\]

## Exact fixed-core reuse bound

Let \(J\subseteq F\) be a fixed core on a vertex set \(C\), with
\[
 c=|C|,\qquad e=|E(J)|,\qquad \Delta_J=\Delta(J).
\]
Suppose \(t\) remaining supports of size \(n\) contain \(C\).  Their
complements, of size \(k=13-n\), lie in \(O=V(K_{13})\setminus C\).
Equation (1) gives the exact capacity
\[
\begin{aligned}
kt
&\le\sum_{v\in O}(d_F(v)-3)\\
&=2|E(F)|-\sum_{v\in C}d_F(v)-3(13-c).
\end{aligned}
\tag{14}
\]

There is also a simple-graph correction.  At most
\(\binom{13-c}{2}\) noncore edges of \(F\) avoid \(C\), so at least
\[
 r_J=\max\left\{0,\,
 |E(F)|-e-\binom{13-c}{2}\right\} \tag{15}
\]
additional edges touch \(C\).  Therefore
\[
 \sum_{v\in C}d_F(v)\ge2e+r_J,
\]
and
\[
 t\le
 \left\lfloor
 \frac{2|E(F)|-39+3c-2e-r_J}{k}
 \right\rfloor.
\tag{16}
\]
A maximum-degree core vertex also gives \(t\le12-\Delta_J\).  Intersecting
these bounds with the number \(N_n\) of remaining size-\(n\) supports gives
the exact fixed-core screen
\[
 R(J,n)=\min\left\{
 N_n,\ 12-\Delta_J,\
 \left\lfloor
 \frac{2|E(F)|-39+3c-2e-r_J}{13-n}
 \right\rfloor
 \right\}.
\tag{17}
\]
Here “exact” means that (17) uses the exact complement-row identity; it is
an upper bound, not an assertion that every value is attainable.

## Profile-specific reuse tables

For size eight, use the order
\[
 17,\ 35,\ 511,\ 331,\ 3111,\ 5
\tag{18}
\]
for the six rows of (7).  Formula (17) gives:
\[
\begin{array}{c|c}
r&\text{fixed-core reuse ceilings}\\ \hline
0&(3,3,3,3,3,3)\\
1&(4,3,4,3,4,4)\\
2&(5,3,4,4,5,5)\\
3&(5,3,4,4,5,6)\\
4&(5,3,4,4,5,6)\\
5&(5,4,5,4,5,6).
\end{array} \tag{19}
\]

For the seven nonzero-profile size-ten types in the order (9), the
ceilings are
\[
\begin{array}{c|c}
r&\text{fixed-core reuse ceilings}\\ \hline
1&(3,2,1,4,3,5,5)\\
2&(3,2,1,4,3,4,4)\\
3&(2,2,1,2,2,2,2).
\end{array} \tag{20}
\]
The \(r=0\) row must also include the two degree-eight types.  In the order
\[
 37,\ 55,\ 711,\ 531,\ 333,\ 5111,\ 3311,\ 31111,\ 6,
\]
its ceilings are
\[
 (3,1,4,2,1,4,3,5,6). \tag{21}
\]

For the coordinated unused size-twelve supports, in the order
\[
 57,\ 311111,\ 7,
\]
the rows are
\[
\begin{array}{c|c}
r&\text{fixed-core reuse ceilings}\\ \hline
3&(0,1,1)\\
4&(0,2,2)\\
5&(1,1,1).
\end{array} \tag{22}
\]
In particular, the exact row identity rules out \(K_{5,7}\) entirely for
the \(r=3,4\) remaining size-twelve supports, even though its raw edge
budget is 38.

## A three-near-factor route

There is a potentially stronger route for \(r=3,4,5\).  Stop after the
coordinated complement-cover six-prefix and let \(D\) be its union.  Then
\(\Delta(D)\le5\), so
\[
 G=K_{13}-D\qquad\text{satisfies}\qquad\delta(G)\ge7. \tag{23}
\]
In each of these three profiles, at least three unused size-twelve
supports remain: exactly three for \(r=3,5\), and four for \(r=4\).
Choose any three.  If their omitted vertices are \(x,y,z\), a packing
of three edge-disjoint near-perfect matchings of \(G\), missing
respectively \(x,y,z\), would immediately give a coordinated ninth
matching.

We prove the following assertion.

> every graph on thirteen vertices of minimum degree at least seven
> contains three edge-disjoint prescribed near-perfect matchings, with
> repeated prescribed omissions allowed,

The proof is solver-free and proceeds through the three exact terminal
Tutte types below.

### Two prescribed near-perfect matchings always exist

First use Dirac's theorem in \(G-x\), whose order is twelve and whose
minimum degree is at least six, to obtain a perfect matching \(M_x\).
Now put
\[
 Q=G-M_x-y.
\]
This graph has order twelve and minimum degree at least five.  A useful
sharp special case of Tutte's theorem is:

> If a graph \(Q\) of order twelve has \(\delta(Q)\ge5\) and no perfect
> matching, then \(Q\) has an independent set of order seven.

Indeed, for a Tutte set \(S\) of order \(s\), every odd component of
\(Q-S\) has order at least the least odd integer not smaller than
\(6-s\).  The requirement of at least \(s+2\) odd components is
numerically impossible unless \(s=5\); then there are exactly seven
singleton components.

If the displayed \(Q\) had no perfect matching, let \(A\) be that
independent seven-set.  Every edge of \(G[A]\) then belongs to \(M_x\),
so \(\Delta(G[A])\le1\).  But each vertex of \(A\) has only six vertices
outside \(A\), while its degree in \(G\) is at least seven.  Thus
\(\delta(G[A])\ge1\), which would make \(G[A]\) a 1-regular graph of odd
order.  This is impossible.  Hence \(Q\) has a perfect matching \(M_y\),
and \(M_x,M_y\) are edge-disjoint with their prescribed omissions.  The
argument also covers \(x=y\).

### Exact terminal catalogue after two matchings

Delete any such \(M_x,M_y\), then delete the third prescribed omission
\(z\).  The resulting graph \(R\) has order twelve and minimum degree at
least four.  If \(R\) has no perfect matching, the same Tutte count,
coarsened as in (5), leaves exactly
\[
 K_{5,7},\qquad K_{3,1,1,1,1,1},\qquad K_7 \tag{24}
\]
in the nonedge graph of \(R\).  Equivalently, its only possible Tutte
separator sizes are \(0,4,5\).  This is the same three-type
size-twelve catalogue that appears in (13), now obtained without an
edge-budget hypothesis.

The first type in (24) is always switch-repairable.  Suppose
\(R\) has components \(A,B\) of orders five and seven.  Every vertex of
\(A\) needs at least two \(G\)-edges to \(B\), because it has at most
four neighbours in \(A\) and at most the neighbour \(z\).  All such
edges lie in \(M_x\cup M_y\).  The two matchings contain at most five
edges each across this cut, so equality holds: each contains five and
saturates \(A\).  It follows also that \(R[A]=K_5\), while
\(\delta(R[B])\ge4\).

Choose one of the two matchings.  Among its five endpoints in \(B\),
two, say \(b_1,b_2\), are adjacent in \(R[B]\), since every one of those
five vertices has at least two neighbours within the five.  If their
matching partners are \(a_1,a_2\in A\), replace
\[
 a_1b_1,\ a_2b_2
 \quad\text{by}\quad
 a_1a_2,\ b_1b_2. \tag{25}
\]
This preserves the matching and its prescribed omission.  In the new
residual graph, use \(a_1b_1\), a perfect matching of
\(R[A]-a_1\cong K_4\), and a perfect matching of \(R[B]-b_1\).
The latter exists by Dirac, because it has order six and minimum degree
at least three.  These six edges form the required matching missing
\(z\).

The separator-four type in (24) is also always switch-repairable.  Let
\(S\) be the separator, \(|S|=4\).  The coarsening can be chosen so that
five vertices \(T\) are actual singleton components of \(R-S\), while
the other three vertices form a block \(C\).  Hence
\[
 |T|=5,\quad |C|=3,\quad
 E_R(T,T\cup C)=\varnothing. \tag{26}
\]
Every \(t\in T\) has degree at least four in \(R\), so it is adjacent in
\(R\) to all four vertices of \(S\).

Put \(L=S\cup\{z\}\).  Since \(\delta(G)\ge7\), each \(t\in T\) must use
all three possible additional, distinct incidences: \(tz\), its edge in
\(M_x\), and its edge in \(M_y\).  Neither selected edge can go to
\(S\) or to \(z\), because all four \(T\)-to-\(S\) edges survive in
\(R\), and using \(tz\) would merge two of the three additional
incidences.  Thus \(x,y\notin T\), and in each selected matching all five
vertices of \(T\) are paired into \(T\cup C\).

For one selected matching, let \(a\) be its number of \(T\)-to-\(T\)
edges and \(b\) its number of \(T\)-to-\(C\) edges.  Then
\[
 2a+b=5,\qquad b\le3,
\]
so \(b\in\{1,3\}\) and \(a\ge1\).  The matching also has an edge wholly
inside \(L\): after the \(T\)-vertices are covered, at most \(3-b\)
unused \(C\)-vertices are available to partner the at least four
non-omitted vertices of \(L\).

First suppose \(R[C]\) contains an edge \(c_1c_2\), and write
\(C=\{c_1,c_2,c_3\}\).  Choose a \(T\)-to-\(T\) edge \(t_1t_2\) and an
\(L\)-to-\(L\) edge \(uv\) in the same selected matching, and switch
\[
 t_1t_2,\ uv
 \quad\text{to}\quad
 t_1u,\ t_2v. \tag{27}
\]
All required new edges exist: every \(T\)-to-\(S\) edge survives in
\(R\), and every \(tz\) was forced above.  They are unused by the other
selected matching.  Now use the freed \(t_1t_2\) in the third matching.
The vertex \(c_3\) has an \(R\)-neighbour \(s_0\in S\), since
\(d_R(c_3)\ge4\) and it has only two possible neighbours in \(C\).
Use \(c_1c_2,c_3s_0\), and match the three vertices of
\(T-\{t_1,t_2\}\) bijectively to \(S-\{s_0\}\).  Together with
\(t_1t_2\), these are six pairwise disjoint edges forming the matching
missing \(z\); none is an edge introduced in (27).

It remains to treat \(R[C]\) empty.  Then the degree-four condition makes
every edge between
\[
 W=T\cup C\quad\text{and}\quad S
\]
present in \(R\).  Applying the same three-additional-incidences argument
to each \(c\in C\) shows that \(cz\) is present and unused, and that each
of \(M_x,M_y\) pairs every vertex of \(W\) inside \(W\).  In particular,
\(x,y\in L\); each selected matching consists locally of a perfect
matching of the eight vertices \(W\) and two edges on the four vertices
of \(L\) other than its omission.

In \(M_x\), choose two \(W\)-edges and its two \(L\)-edges.  Delete those
four edges and match the four exposed \(W\)-vertices bijectively to the
four exposed \(L\)-vertices.  Every such edge is available by the
complete \(W\)-to-\(S\) residual graph and the forced \(W\)-to-\(z\)
edges, and none is used by \(M_y\).  For the third matching, use the two
freed \(W\)-edges and match the other four vertices of \(W\)
bijectively to \(S\).  The new first-matching edges and the third
matching can share \(W\)-endpoints, but not edges: the former are
\(W_{\rm exposed}\)-to-\(L\) edges, while the latter are the freed
internal \(W\)-edges together with
\(W_{\rm remaining}\)-to-\(S\) edges.  All of the cross edges were
residual before the switch, so the three matchings are edge-disjoint and
have the required omissions.

It remains to eliminate the separator-five core in (24).  Let \(S\) be
the separator, \(|S|=5\), and let \(U\) be the seven singleton
components of \(R-S\).  Put
\[
 B=R[U,S].
\]
Then \(R[U]\) is empty and every row of \(B\) has degree at least four.
For \(s\in S\), define its missing-row class
\[
 D_s=\{u\in U:us\notin E(B)\}. \tag{28}
\]
The sets \(D_s\) are pairwise disjoint, because a row of \(B\) misses at
most one of its five possible edges.

Call a pair \(uv\in\binom U2\) **bad** if
\(B[U-\{u,v\},S]\) has no perfect matching.  A five-by-five subgraph of
\(B\) can fail Hall only on its entire five-vertex left side: every
smaller nonempty left set has at least four neighbours.  Consequently,
\[
 uv\text{ is bad}
 \quad\Longleftrightarrow\quad
 U-\{u,v\}\subseteq D_s
 \text{ for some }s\in S. \tag{29}
\]
There is at most one \(D_s\) of order at least five.  If its order is
five, six, or seven, the bad-pair graph is respectively one edge, a
six-edge star, or \(K_7\).

Every vertex \(u\in U\) has a \(G\)-neighbour in \(U\), since it has
only six vertices outside \(U\) and \(d_G(u)\ge7\).  All such edges
belong to \(M_x\cup M_y\).  Hence
\[
 \delta((M_x\cup M_y)[U])\ge1. \tag{30}
\]
In particular, outside the \(K_7\) bad-pair case, some selected
\(U\)-edge is good.

We first dispose of the \(K_7\) bad-pair case.  Here
\(D_{s_0}=U\) for some \(s_0\), so \(B=K_{7,4}\) with right side
\(S-\{s_0\}\).  For every \(u\in U\), its four \(B\)-edges, its two
selected incidences, and \(uz\) are the only possible seven distinct
incidences.  Thus \(uz\) is present and unused, and each selected
matching pairs \(U\) as
\[
 3\,UU+1\,U s_0. \tag{31}
\]
The other two matching edges lie on
\[
 L'=(S-\{s_0\})\cup\{z\},
\]
apart from the matching's prescribed omission in \(L'\).

In one selected matching choose a \(UU\)-edge \(uv\), its edge
\(as_0\), and its two edges covering the four non-omitted vertices of
\(L'\).  Delete these four edges.  Pair \(s_0\) to one of the at least
three exposed vertices of \(S-\{s_0\}\), and pair \(u,v,a\)
bijectively to the other three exposed vertices of \(L'\).  All these
edges are available: the \(U\)-to-\(S-\{s_0\}\) edges are in \(B\),
the \(U\)-to-\(z\) edges were forced above, and
\(s_0\) sees all of \(S-\{s_0\}\) in \(R\) because \(d_R(s_0)\ge4\).
The third matching uses the freed edges \(uv,as_0\) and a perfect
matching between
\[
 U-\{u,v,a\}\quad\text{and}\quad S-\{s_0\}.
\]
This repairs the common-missing-column case.

For the remaining cases, record the exact type of one selected matching
by
\[
 (a,b,c,d,e)=
 (\#UU,\#US,\#Uz,\#SS,\#Sz).
\]
Counting its covered vertices gives the following exhaustive table:
\[
\begin{array}{c|l}
\text{omission}&(a,b,c,d,e)\\ \hline
U&(0,5,1,0,0),(1,3,1,1,0),(1,4,0,0,1),\\
 &(2,1,1,2,0),(2,2,0,1,1),(3,0,0,2,1)\\
S&(1,4,1,0,0),(2,2,1,1,0),(2,3,0,0,1),\\
 &(3,0,1,2,0),(3,1,0,1,1)\\
z&(1,5,0,0,0),(2,3,0,1,0),(3,1,0,2,0).
\end{array} \tag{32}
\]

Suppose a selected matching \(P\) has \(a\ge2\) and \(d\ge1\).
Its \(UU\)-edges form a matching of order at least two, while the bad
graph outside the case already handled has matching number at most one.
Thus \(P\) has a good edge \(uv\).

If \(P\) has an \(SS\)-edge \(st\) such that
\(\{u,v\}\not\subseteq D_s,D_t\), the bipartite graph between
\(\{u,v\}\) and \(\{s,t\}\) has a perfect matching.  Replace
\(uv,st\) by that perfect matching.  This frees \(uv\), and a perfect
matching of \(B[U-\{u,v\},S]\) completes the third matching.

Otherwise \(u,v\) share a missing label, say
\(\{u,v\}\subseteq D_s\), where \(s\) is an endpoint of every
\(SS\)-edge of \(P\).  Since the \(SS\)-edges are disjoint, this forces
\(d=1\); write the unique edge as \(st\).  The table (32) shows that
every type with \(a\ge2,d=1\) has a \(US\)-edge, say \(aq\), where
\(q\notin\{s,t\}\).

The degree condition gives an important label check.  For
\(w\in D_s\), \(d_B(w)=4\).  Degree seven therefore forces \(w\) not
to be either prescribed omission, forces \(wz\) to be present and
unused, and forces both selected matchings to cover \(w\) with distinct
edges other than \(wz\).  In \(P\), the vertex \(s\) is already used by
\(st\), while every other \(S\)-neighbour of \(w\) is a residual
\(B\)-edge.  Thus \(P(w)\in U\).  Consequently \(P\) pairs \(D_s\)
internally and \(|D_s|\) is even.  If \(|D_s|\le4\), switch
\[
 uv,\ st,\ aq
 \quad\text{to}\quad
 a s,\ u t,\ v q. \tag{33}
\]
The three new edges lie in \(B\): \(u,v\) miss only \(s\), while
the selected edge \(aq\) makes \(q\) the unique missing label of \(a\).
On \(U-\{u,v\}\), the switch changes only the missing label of \(a\)
from \(q\) to \(s\).  The new \(D_s\) has order at most three, and
every other missing class still has order at most four: otherwise such
a class of order at least five would contain
\(U-\{u,v\}\), contradicting that \(uv\) is good.  Hall therefore still
supplies the five cross edges for the third matching.

If instead \(|D_s|=6\), the six vertices of \(D_s\) force
\(a=3,d=1\).  The table leaves only
\[
 (a,b,c,d,e)=(3,1,0,1,1)
\]
with its omission in \(S\).  Let its \(Sz\)-edge be \(rz\);
necessarily \(r\ne s\).  Replace
\[
 uv,\ rz\quad\text{by}\quad ur,\ vz. \tag{34}
\]
Here \(ur\in B\), because \(u\) misses only \(s\), and \(vz\) is forced
present and unused by the degree-seven equality at the labelled vertex
\(v\).  Both new edges are incident to the deleted pair
\(\{u,v\}\), so the original perfect matching of
\(B[U-\{u,v\},S]\) remains available for the third matching.

It remains only to consider the situation in which neither selected
matching has \(a\ge2,d\ge1\).  Equation (30) gives
\[
 a_x+a_y\ge4.
\]
Inspection of (32) then forces both selected matchings to have type
\[
 (2,3,0,0,1), \tag{35}
\]
and both prescribed omissions lie in \(S\).

Fix one of these matchings.  Write its \(Sz\)-edge as \(s_0z\), and
its three \(US\)-edges as \(a_i s_i\), \(i=1,2,3\).  Its two
\(UU\)-edges are disjoint, so at least one, say \(uv\), is good.
If \(\{u,v\}\not\subseteq D_{s_0}\), then for some \(i\) it is also
not contained in \(D_{s_i}\), since the missing classes are disjoint.
Orient the two available cross edges and switch
\[
 uv,\ a_i s_i,\ s_0z
 \quad\text{to}\quad
 u s_i,\ v s_0,\ a_i z. \tag{36}
\]
The edge \(a_i z\) is forced present and unused: the selected
\(a_i s_i\) leaves exactly four \(B\)-edges at \(a_i\), so degree seven
requires the other selected incidence and a distinct edge to \(z\).
The two new \(B\)-edges are incident to \(u,v\), which are absent from
the third matching's Hall problem.

Finally, if \(\{u,v\}\subseteq D_{s_0}\), use
\[
 uv,\ a_i s_i,\ s_0z
 \quad\text{to}\quad
 u s_i,\ v z,\ a_i s_0. \tag{37}
\]
The three \(US\)-endpoints \(a_i\) have missing labels \(s_i\), so
\(D_{s_0}\) is contained in the four \(UU\)-endpoints.  After deleting
\(u,v\) and changing \(a_i\)'s missing label from \(s_i\) to \(s_0\),
the new \(D_{s_0}\) has order at most three; all other classes have
order at most four because \(uv\) was good.  Thus Hall again supplies
the third matching.  The edges \(us_i,a_is_0\) lie in \(B\), and
\(vz\) is forced present and unused exactly as above.

This eliminates the last type in (24), proving:

> **Three-near-factor theorem.**  Every graph on thirteen vertices with
> minimum degree at least seven contains three pairwise edge-disjoint
> near-perfect matchings missing any three prescribed vertices, with
> repetitions allowed.

## Finite ninth-matching frontier

The catalogues and reuse tables give several immediate structural
reductions.

* For \(r=4\), total blockage of the seven remaining size-eight supports
  needs at least two distinct size-eight core embeddings, and each of the
  two size-twelve supports must contain a
  \(K_{3,1,1,1,1,1}\) or \(K_7\) core.
* For \(r=5\), total blockage of the eight remaining size-eight supports
  needs at least two distinct size-eight core embeddings; the one
  size-twelve support has only the three core types in (13).
* For \(r=0,1,2,3\), the displayed vectors identify exactly which single
  core types can saturate an entire remaining support-size family and
  which branches necessarily require distinct cores.
* For \(r=3,4,5\), the six-prefix route and the three-near-factor theorem
  prove a coordinated ninth matching: append three chosen unused
  size-twelve support matchings directly to the complement-cover
  six-prefix.

Thus the coordinated ninth step is proved for \(r=3,4,5\).  For
\(r=0,1,2\), it remains reduced to coexistence and switching among
finitely many labelled core embeddings inside graphs with 36, 37, or 38
edges satisfying (1)--(4).  No ninth theorem for those three profiles,
and no complete solution of Erdős--Rosenfeld Problem #835, is claimed.

## Verification

Run:

```sh
python3 collaboration/coordinated_nine_structural/verify_catalogue.py
```

The standard-library verifier exhausts all odd block partitions, checks
every edge count, maximum degree, degree-three completion bound, selected
profile, remaining inventory, correction term, every entry of
(19)--(22), the minimum-degree-five and minimum-degree-four catalogues,
the exact bad-pair classification, the matching-type table, and the
integer reductions used in the three-near-factor theorem.  No optimizer
is used.

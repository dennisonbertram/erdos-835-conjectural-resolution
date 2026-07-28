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
In each of these three profiles, exactly three unused size-twelve
supports remain.  If their omitted vertices are \(x,y,z\), a packing of
three edge-disjoint near-perfect matchings of \(G\), missing respectively
\(x,y,z\), would immediately give a coordinated ninth matching.

The full assertion

> every graph on thirteen vertices of minimum degree at least seven
> contains three edge-disjoint prescribed near-perfect matchings, with
> repeated prescribed omissions allowed,

is not proved here.  The following solver-free results reduce it sharply.

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

Consequently, any genuine counterexample to the three-near-factor
assertion must survive all choices of the first two matchings and must
end in one of only the two separator-core families
\[
 K_{3,1,1,1,1,1}\quad\text{or}\quad K_7. \tag{26}
\]
No proof eliminating (26), and no counterexample realizing it against
every possible first-two-matching choice, is presently claimed.

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
* For \(r=3,4,5\), the six-prefix route (23)--(26) says that a ninth
  matching follows unless every admissible choice of two of the three
  size-twelve matchings leaves a separator-four or separator-five
  obstruction for the third.

Thus the ninth step is reduced to coexistence and switching among finitely
many labelled core embeddings inside graphs with 36, 37, 38, or 40 edges
satisfying (1)--(4).  The reuse identities alone do not rule out every
multi-core configuration, so no universal ninth matching is claimed.

## Verification

Run:

```sh
python3 collaboration/coordinated_nine_structural/verify_catalogue.py
```

The standard-library verifier exhausts all odd block partitions, checks
every edge count, maximum degree, degree-three completion bound, selected
profile, remaining inventory, correction term, every entry of
(19)--(22), and the minimum-degree-five and minimum-degree-four
catalogues used in the near-factor reduction.  No optimizer is used.

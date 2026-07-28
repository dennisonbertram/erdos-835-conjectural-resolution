# Switching away the terminal \(K_7\) obstruction

Date: 2026-07-28.

## Result

Let \(G\) be a graph on thirteen vertices with
\[
\delta(G)\ge 7.
\]
Let \(M_1,M_2\) be edge-disjoint near-perfect matchings with prescribed
omitted vertices \(x,y\), and let \(z\) be a third prescribed omission.
Put
\[
R=G-M_1-M_2-z.
\]
Suppose a Tutte barrier for \(R\) has separator \(S\) of order five and
seven singleton components \(U\).  Equivalently,
\[
|U|=7,\qquad |S|=5,\qquad R[U]\text{ is empty}. \tag{1}
\]
Then \(M_1,M_2\) can be switched, preserving their prescribed omissions,
so that the new residual graph has a perfect matching on
\(V(G)\setminus\{z\}\).

Thus the terminal \(K_7\) obstruction in the prescribed
three-near-factor argument is always repairable.  This proof is
solver-free.

## The residual bipartite graph

Let
\[
B=R[U,S].
\]
Deleting \(z\) and the two selected matchings removes at most three
incident edges at a vertex of \(U\), so
\[
d_B(u)=d_R(u)\ge4\qquad(u\in U). \tag{2}
\]
For \(s\in S\), put
\[
D_s=\{u\in U:us\notin B\}. \tag{3}
\]
Every \(u\) belongs to at most one \(D_s\).  In particular, the five
sets \(D_s\) are pairwise disjoint.

Call a pair \(uv\subset U\) **good** if
\[
B[U\setminus\{u,v\},S]
\]
has a perfect matching.  Hall's theorem gives an exact description:
\[
uv\text{ is bad}
\quad\Longleftrightarrow\quad
U\setminus\{u,v\}\subseteq D_s
\text{ for some }s\in S. \tag{4}
\]
Indeed, in a bipartite graph with five left and five right vertices and
left minimum degree at least four, Hall can fail only for the full
five-vertex left side.

There is at most one \(D_s\) of order at least five.  If its order is
five, the bad pairs form one edge; if its order is six, they form a
six-edge star; and if its order is seven, every pair is bad.  Hence,
unless some \(D_s=U\), every matching of two or more disjoint pairs in
\(U\) contains a good pair. \(\tag{5}\)

## Edge-type bookkeeping

For \(i=1,2\), let
\[
(a_i,b_i,c_i,d_i,e_i)
\]
count the \(M_i\)-edges of types
\[
UU,\quad US,\quad Uz,\quad SS,\quad Sz,
\]
respectively.  If the omitted vertex of \(M_i\) lies in
\(U,S,\{z\}\), write the corresponding indicators as
\(\epsilon_U,\epsilon_S,\epsilon_z\).  The exact endpoint equations are
\[
\begin{aligned}
2a_i+b_i+c_i&=7-\epsilon_U,\\
b_i+2d_i+e_i&=5-\epsilon_S,\\
c_i+e_i&=1-\epsilon_z. \tag{6}
\end{aligned}
\]

Every \(G\)-edge inside \(U\) belongs to \(M_1\cup M_2\), by (1).
Every vertex of \(U\) has a \(G\)-neighbour in \(U\), because it has
only six possible neighbours outside \(U\) and degree at least seven.
Consequently the \(UU\)-edges of the two matchings cover \(U\), and
\[
a_1+a_2\ge4. \tag{7}
\]

If \(d_i=0\), equations (6) give \(a_i\le2\), with equality only for
\[
(a_i,b_i,c_i,d_i,e_i)=(2,3,0,0,1)
\quad\text{and}\quad \epsilon_S=1. \tag{8}
\]
It follows from (7) that either

1. some selected matching \(P\) has \(a\ge2\) and \(d\ge1\); or
2. both omitted vertices lie in \(S\), and both selected matchings have
   the exceptional type (8).

We treat these alternatives, followed by the common-missing-neighbour
case \(D_s=U\).

## The ordinary case

Assume no \(D_s\) equals \(U\), and choose \(P\) with \(a\ge2,d\ge1\).
By (5), its \(UU\)-matching contains a good edge \(uv\).

If \(P\) has an \(SS\)-edge \(st\) such that
\[
B[\{u,v\},\{s,t\}]
\]
has a perfect matching, replace
\[
uv,\ st
\quad\text{by those two bipartite edges}. \tag{9}
\]
This preserves \(P\) and its omission.  The only newly consumed
\(B\)-edges touch \(u,v\).  Therefore \(uv\), followed by a perfect
matching of \(B[U\setminus\{u,v\},S]\), is the required third matching.

Suppose no \(SS\)-edge permits (9).  The two endpoints of \(uv\) then
miss a common separator vertex contained in every \(SS\)-edge of \(P\).
Since the \(SS\)-edges are themselves a matching, there is exactly one:
write it as \(st\), with
\[
u,v\in D_s. \tag{10}
\]

Solving (6) under \(a\ge2,d=1\) gives only
\[
\begin{array}{c|c}
\text{location of the omission}&(a,b,c,d,e)\\ \hline
U&(2,2,0,1,1)\\
S&(2,2,1,1,0)\text{ or }(3,1,0,1,1)\\
z&(2,3,0,1,0).
\end{array} \tag{11}
\]
In particular, \(P\) has a cross edge \(aq\), where
\[
q\notin\{s,t\}.
\]
The selected edge \(aq\) means that \(a\) misses \(q\) in \(B\), and
therefore \(a\) is adjacent in \(B\) to \(s,t\).  Also \(u,v\), which
miss \(s\), are adjacent in \(B\) to \(t,q\).  Hence the switch
\[
uv,\ st,\ aq
\quad\longmapsto\quad
as,\ ut,\ vq \tag{12}
\]
is valid.

On the five vertices \(U\setminus\{u,v\}\), switch (12) merely changes
the unique missing neighbour of \(a\) from \(q\) to \(s\).  If the new
bipartite graph had no perfect matching, all five of those vertices
would now miss \(s\).  Since \(u,v\in D_s\) and \(a\notin D_s\), this
can happen only when
\[
|D_s|=6,\qquad U\setminus D_s=\{a\}. \tag{13}
\]
If (13) does not hold, (12) followed by Hall gives the third matching.

It remains to repair (13), without making switch (12).  Every \(P\)-cross
vertex lies outside \(D_s\), since \(s\) is already used by the
\(SS\)-edge.  Thus (13) forces \(b=1\), and (11) forces
\[
(a,b,c,d,e)=(3,1,0,1,1)
\]
with the omission in \(S\).  Let \(rz\) be the \(Sz\)-edge of \(P\).
Here \(r\ne s\).

For every \(w\in D_s\), the four \(B\)-edges at \(w\), its \(P\)-edge
inside \(U\), and its at-most-one edge in the other selected matching
give at most six neighbours unless \(wz\) is present and unused.
Thus all six edges from \(D_s\) to \(z\) are present and unused.  Replace
\[
uv,\ rz
\quad\longmapsto\quad
ur,\ vz. \tag{14}
\]
The edge \(ur\) lies in \(B\), and \(vz\) is forced unused as just shown.
Only a \(B\)-edge at the already covered vertex \(u\) is consumed.
Therefore the original perfect matching of
\(B[U\setminus\{u,v\},S]\), together with the freed edge \(uv\), is the
third prescribed near-factor.

## The exceptional edge type

Now suppose both selected matchings have type
\[
(2,3,0,0,1)
\]
and both omissions lie in \(S\).

Let \(X_i\subset U\) be the three vertices that \(M_i\) matches into
\(S\).  The four \(UU\)-edges in \(M_1\cup M_2\) cover \(U\), so
\[
X_1\cap X_2=\varnothing. \tag{15}
\]
Each vertex of \(X_i\) has as its unique missing \(B\)-neighbour the
distinct separator vertex to which \(M_i\) matches it.  The sole vertex
outside \(X_1\cup X_2\) can miss at most one further separator vertex.
Thus
\[
|D_s|\le3\qquad(s\in S). \tag{16}
\]
Every \(UU\)-edge is good.

Fix one selected matching \(P\).  Its four \(UU\)-endpoints are the
three vertices of the other cross set and the sole remaining vertex.
The first three have distinct missing-neighbour labels.  Consequently,
among the two \(UU\)-edges of \(P\), some edge \(uv\) has endpoints with
different missing-neighbour labels.

Let \(aq\) be any \(US\)-edge of \(P\), and let \(s_0z\) be its
\(Sz\)-edge.  Since \(q\ne s_0\), the distinct-label choice of \(uv\)
guarantees a perfect matching in
\[
B[\{u,v\},\{q,s_0\}]. \tag{17}
\]
Moreover \(a\) is cross-matched in \(P\) and internally matched in the
other selected matching.  Its four \(B\)-neighbours, those two selected
incidences, and the degree-seven hypothesis force \(az\) to be present;
neither selected matching uses it.  Replace
\[
uv,\ aq,\ s_0z
\]
by \(az\) and the two edges in (17).  This preserves \(P\), frees \(uv\),
and consumes no \(B\)-edge at a vertex of \(U\setminus\{u,v\}\).
By (16) and Hall, \(uv\) plus a perfect matching of
\(B[U\setminus\{u,v\},S]\) is the required matching missing \(z\).

This argument allows the two prescribed omissions in \(S\) to be equal.

## The common missing neighbour

Finally suppose
\[
D_{s_0}=U
\]
for some \(s_0\in S\), and put \(S'=S\setminus\{s_0\}\).  Then
\[
B=K_{U,S'}. \tag{18}
\]

Every \(G\)-edge from \(U\) to \(s_0\) is selected.  There are at most
two such edges, one in each selected matching.  Since \(s_0\) has only
the five possible neighbours in \(S'\cup\{z\}\), its degree is at least
seven only if there are exactly two selected \(U s_0\)-edges and
\(s_0\) is adjacent to every vertex of \(S'\cup\{z\}\).

At \(u\in U\), the four edges to \(S'\) survive in \(B\).  All present
edges from \(u\) to \(U\cup\{s_0\}\) are selected and account for at
most the two selected incidences at \(u\).  Degree at least seven
therefore forces \(uz\) to be present and unused, and forces both
selected incidences at \(u\) to lie in \(U\cup\{s_0\}\).  In particular,
\[
x,y\notin U. \tag{19}
\]

Put \(L'=S'\cup\{z\}\).  Each selected matching \(P\) now consists of

* three \(UU\)-edges;
* one edge \(ws_0\);
* two edges covering four vertices of \(L'\), with its prescribed
  omission as the fifth vertex.

Choose any \(UU\)-edge \(uv\) of \(P\).  Delete that edge, \(ws_0\), and
the two displayed \(L'\)-edges.  The four exposed vertices
\[
\{u,v,w,s_0\}
\]
and the four exposed, non-omitted vertices of \(L'\) span an unused
\(K_{4,4}\): the \(U\)-to-\(S'\) edges come from (18), the \(U\)-to-\(z\)
edges were forced above, and \(s_0\) is complete to \(L'\).  Rematch
these eight vertices through that \(K_{4,4}\).

The switched \(P\) has the same omission.  For the third matching, use
the two freed edges
\[
uv,\ ws_0,
\]
then match the four remaining vertices of \(U\) bijectively to \(S'\).
The new \(P\)-edges touch only \(u,v,w,s_0\), whereas these last four
third-matching edges use the other four vertices of \(U\).  Hence all
three matchings are pairwise edge-disjoint.

This also covers every repeated-omission pattern.

## Class-B corollary

Combine this \(K_7\) repair with the two-near-factor argument and the
separator-zero and separator-four repairs in
`../coordinated_nine_structural/NOTE.md`.  The result is the following
prescribed theorem.

> **Three-near-factor lemma.** Every graph on thirteen vertices with
> minimum degree at least seven contains three pairwise edge-disjoint
> near-perfect matchings with any three prescribed omitted vertices.
> The prescribed vertices need not be distinct.

This immediately advances three class-B profiles.  In the coordinated
six-prefix construction, the union \(D\) has
\[
\Delta(D)\le5,
\]
so \(G=K_{13}-D\) has minimum degree at least seven.  The exact
size-twelve inventory after the six-prefix is:
\[
\begin{array}{c|c|c|c}
r&\text{total size-12 colours}&
\text{used in the six-prefix}&\text{available}\\ \hline
3&3&0&3\\
4&4&0&4\\
5&5&2&3.
\end{array}
\]
For \(r=3\), apply the lemma to all three available colours.  For \(r=4\),
choose any three of the four.  For \(r=5\), apply it to the three colours
left after the two size-twelve colours used in the complement-cover
six-prefix.  Their singleton complements are the prescribed omitted
vertices, with repetitions allowed.

Adding these three matchings to the six-prefix proves:

> Every target class-B instance in profiles \(r=3,4,5\) has nine
> pairwise edge-disjoint prescribed-support perfect matchings.

The same argument does not by itself cover \(r=0,1,2\).  After the
six-prefix those profiles have respectively zero, one, and two available
size-twelve colours.  Replacing the missing near-factors by size-ten or
size-eight support matchings would require three or five prescribed
omissions, and the minimum-degree calculation underlying (2) no longer
gives the five-by-five Hall graph used here.  A separate mixed-support
switching lemma is needed; no ninth-matching result for \(r=0,1,2\) is
claimed in this note.

## Scope and verification

The main proof eliminates the separator-five \(K_7\) terminal
obstruction.  Its class-B corollary depends on the companion
separator-zero and separator-four repairs cited above.

Run

```sh
python3 collaboration/k7_terminal_switching/verify_arithmetic.py
```

for a dependency-free audit of the endpoint-type table, the Hall bad-pair
classification, and the exceptional distinct-label claim.  The verifier
is an audit aid; the proof above does not use a solver or depend on the
finite computation.

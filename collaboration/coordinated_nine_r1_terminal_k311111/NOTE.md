# Eliminating the \(K_{3,1,1,1,1,1}\) terminal in profile \(r=1\)

Date: 2026-07-28.

## Result and scope

Start with the complement-cover six-prefix in the class-B \(r=1\)
profile, after the switch which removes its possible \(K_6\).  Let
\(D\) be the prefix union, let \(M_0,M_1\) be edge-disjoint perfect
matchings on two remaining size-ten supports, and let
\[
X=V\setminus\{z\}
\]
be the unique size-twelve support.  Put
\[
R=K_X-(D\cup M_0\cup M_1).
\]

This note proves:

> **Separator-four repair lemma.** If a Tutte barrier for \(R\) has a
> three-vertex component and five singleton components after a
> four-vertex separator, then \(M_0,M_1\) can be reselected on the same
> two supports so that the new pair and a perfect matching on \(X\) are
> mutually edge-disjoint.

Together with the certified size-ten pair gate and the row-sum
elimination of \(K_{5,7}\), this leaves only the \(K_7\) terminal family
in the \(r=1\) coordinated-nine route.  No full \(r=1\) theorem is
claimed here.

## Equality forced by the barrier

Write
\[
X=C\mathbin{\dot\cup}T\mathbin{\dot\cup}S,
\qquad |C|=3,\quad |T|=5,\quad |S|=4,
\]
where \(C\) is the three-vertex component, \(T\) is the set of singleton
components, and \(S\) is the separator.  Put
\[
B=S\cup\{z\}.
\]

All 25 edges between distinct components of \(R-S\) belong to
\(D\cup M_0\cup M_1\).  Thus, for every \(t\in T\), the seven edges from
\(t\) to \((C\cup T)\setminus\{t\}\) are selected.  Since
\(d_D(t)\le5\) and each \(M_i\) contributes at most one edge at \(t\),
equality is forced:
\[
d_D(t)=5,\qquad d_{M_0}(t)=d_{M_1}(t)=1. \tag{1}
\]
All five \(D\)-edges at \(t\) lie inside \(C\cup T\).  Consequently:

* both selected triples avoid \(T\), so both \(M_i\) saturate \(T\);
* each \(M_i\)-edge at a vertex of \(T\) lies inside \(C\cup T\); and
* every edge between \(T\) and \(B\) belongs to \(R\), except that edges
  incident with \(z\) lie outside \(X\) but still avoid all three
  selected edge sets.

Also \(R[C]\) is connected, because \(C\) is a component of \(R-S\).
Every \(c\in C\) has \(R\)-degree at least four.

## A near-factor meeting the old pair once

Fix \(i\in\{0,1\}\).  Let \(a\) and \(b\) be the numbers of \(TT\)- and
\(TC\)-edges in \(M_i\).  Since \(M_i\) saturates the odd set \(T\),
\[
2a+b=5,\qquad b\le3. \tag{2}
\]
Hence \(b\in\{1,3\}\) and \(a\ge1\).  In particular, \(M_i\) has a
\(TT\)-edge
\[
e=t_1t_2. \tag{3}
\]

There is a perfect matching \(N\) on \(X\) which meets
\(D\cup M_0\cup M_1\) only in \(e\).  Indeed, choose an edge \(c_1c_2\)
of the connected graph \(R[C]\), and write \(C=\{c,c_1,c_2\}\).  The
vertex \(c\) has at most two neighbours in \(C\), so its \(R\)-degree
bound gives a neighbour \(s\in S\).  Use
\[
e,\quad c_1c_2,\quad cs,
\]
and match the three vertices of \(T\setminus\{t_1,t_2\}\) bijectively to
the three vertices of \(S\setminus\{s\}\).  The last three edges exist by
(1).

It remains to repair the owner \(M_i\) of \(e\) while leaving \(N\) and
the other selected matching untouched.

## The ordinary two-switch

The five vertices of the support of \(M_i\) outside \(T\) lie in
\(C\cup B\).  If \(M_i\) has an edge \(b_1b_2\) with
\(b_1,b_2\in B\), replace
\[
e,\ b_1b_2
\quad\longmapsto\quad
t_1b_1,\ t_2b_2. \tag{4}
\]
The new edges are in the same support.  By (1), they belong to neither
\(D\) nor either old matching.  They also avoid \(N\), because \(N\)
uses \(e\) and therefore has no other edge at \(t_1\) or \(t_2\).
Thus (4) produces the required new \(M_i\).

## The exact exceptional pattern

Suppose \(M_i\) has no \(BB\)-edge.  Let \(c\) be the number of vertices
of \(C\) in its support.  After its \(b\) \(TC\)-edges, its outside-only
matching contains
\[
c-b\text{ vertices of }C,\qquad 5-c\text{ vertices of }B.
\]
With no \(BB\)-edge, every remaining \(B\)-vertex must be paired to a
\(C\)-vertex, so
\[
5-c\le c-b. \tag{5}
\]
Together with \(c\le3\) and (2), this forces
\[
b=1,\qquad c=3. \tag{6}
\]
Thus the only exceptional pattern is
\[
M_i=
e+f+t c_0+c_1b_1+c_2b_2, \tag{7}
\]
where \(e,f\) are \(TT\)-edges,
\(C=\{c_0,c_1,c_2\}\), and \(b_1,b_2\in B\).

If \(c_1c_2\in R\), choose the matching \(N\) above using a different
edge of the connected graph \(R[C]\).  Then augment \(M_i-e\) along
\[
t_1-b_1-c_1-c_2-b_2-t_2. \tag{8}
\]
Equivalently, replace
\[
e,\ c_1b_1,\ c_2b_2
\quad\longmapsto\quad
t_1b_1,\ c_1c_2,\ t_2b_2. \tag{9}
\]
As in (4), all three new edges avoid \(D\), the other old matching, and
\(N\).

Finally, some owner always permits (4) or (9).  If the other matching
has a \(BB\)-edge, use it in (4).  Otherwise it also has the rigid form
(7).  Each rigid matching has one central \(C\)-vertex used by its sole
\(TC\)-edge; its candidate edge in (9) joins the other two vertices of
\(C\).

* If the two central vertices agree, neither old matching has a
  \(TC\)-edge at either endpoint of the common candidate.  All five core
  edges at each endpoint therefore lie in \(D\), saturating its
  \(D\)-degree.  The candidate \(C\)-edge cannot lie in \(D\), and it
  lies in neither old matching, so it is in \(R\).
* If the central vertices differ, let \(q\) be the third vertex of
  \(C\).  It is central in neither matching.  Its five core edges again
  saturate its \(D\)-degree.  Both rigid candidates are incident with
  \(q\), hence both lie in \(R\).

Therefore one of the repairs (4) or (9) always applies.  The repaired
matching, the untouched old matching, and \(N\) give the promised
coordinated \(10,10,12\) extension.

## Verification

Run:

```sh
python3 collaboration/coordinated_nine_r1_terminal_k311111/verify_terminal.py
```

The dependency-free verifier exhausts all perfect matchings on
\(T\) together with five vertices of \(C\cup B\), checks (2), and proves
by enumeration that absence of a \(BB\)-edge has exactly the form
(6)--(7).  It also audits the easy and exceptional augmenting paths and
the two-centre saturation split.

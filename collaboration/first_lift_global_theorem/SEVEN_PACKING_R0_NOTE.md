# The exceptional profile also has a seven-colour packing

Date: 2026-07-27.

## Result and scope

This note closes the \(r=0\) case left open in
`SEVEN_PACKING_NONZERO_R_NOTE.md`.  Together the two notes prove:

> **Seven-prefix theorem.**  Every \(n=13,q=17\) class-B support instance
> contains seven colours whose prescribed perfect matchings can be chosen
> pairwise edge-disjoint.

The result automatically applies to the smaller class-B-prime and
fan-realizable families.  It remains a prefix theorem: it does not complete
the other ten colours and therefore does not solve the full first-lift
problem or Erdős--Rosenfeld Problem #835.

## Setup for \(r=0\)

The profile is
\[
 (n_8,n_{10},n_{12})=(7,10,0).
\]
By `SIX_PACKING_NOTE.md`, choose edge-disjoint perfect matchings on four
size-eight supports and two size-ten supports.  Let \(F\) be their union.
Then
\[
 |E(F)|=4\cdot4+2\cdot5=26, \tag{1}
\]
and \(F\) is the union of six matchings.  Consequently
\[
 \Delta(F)\le6,\qquad
 |E(F[X])|\le6\left\lfloor |X|/2\right\rfloor
 \quad\text{for every }X. \tag{2}
\]

Eight size-ten colours remain.  The corrected Tutte audit in
`SEVEN_PACKING_NONZERO_R_NOTE.md` says that a remaining size-ten support
can fail to have an \(F\)-avoiding perfect matching only if \(F\) contains
one of the following cores:

* a **C-core**, a copy of \(K_6\);
* a **B-core**, a copy of \(K_7-E(K_3)\).

The letters only name the two barrier shapes; they are unrelated to the
class-B/class-B-prime terminology.

## Core uniqueness

We prove that \(F\) contains at most one obstruction core in total.

### Two C-cores

Suppose two \(K_6\)'s have vertex sets with intersection \(t\).

* If \(t=0\), their thirty edges contradict (1).
* If \(1\le t\le4\), a shared vertex has at least
  \(5+(6-t)=11-t\ge7\) neighbours in their union, contradicting
  \(\Delta(F)\le6\).
* If \(t=5\), their union is \(K_7\) minus one edge, with twenty edges on
  seven vertices, contradicting the bound \(6\lfloor7/2\rfloor=18\) in
  (2).

Thus two C-cores coincide.

### Two B-cores

Write a B-core as \(J(U,C)=K_7-E(K_3)\), where \(|U|=7\), \(C\subset U\)
has size three, and \(Q=U\setminus C\) has size four.  Every \(q\in Q\)
has all six of its \(F\)-neighbours inside \(U\); it has no \(F\)-edge to a
vertex outside \(U\).

Consider \(J(U,C)\) and \(J(U',C')\), and put \(t=|U\cap U'|\).

* If \(t\le4\), the two eighteen-edge cores share at most
  \(\binom t2\le6\) edges, so their union has at least thirty edges,
  contradicting (1).
* If \(t=5\), their union has at least \(36-\binom52=26\) edges on nine
  vertices, contradicting \(6\lfloor9/2\rfloor=24\).
* If \(t=6\), let \(b\) be the vertex of \(U'\setminus U\).  At least three
  vertices of \(Q\) lie in \(U\cap U'\).  None can be adjacent to \(b\),
  but the second core omits \(qb\) only when both \(q\) and \(b\) belong to
  its three-set \(C'\).  This would put \(b\) and at least three such
  \(q\)'s in \(C'\), impossible.
* If \(t=7\), both cores lie on the same seven vertices.  Each already has
  eighteen edges, the maximum allowed by (2), so their edge sets must be
  equal and hence their omitted triangles coincide.

Thus two B-cores coincide.

### A B-core and a C-core

Let \(J(U,C)\) have degree-six set \(Q=U\setminus C\), and suppose a
\(K_6\) has vertex set \(W\).

If \(W\cap Q\ne\varnothing\), take \(q\) in the intersection.  Since all
six neighbours of \(q\) lie in \(U\), the clique \(W\) must be contained in
\(U\).  But every six-subset of \(U=Q\mathbin{\dot\cup}C\), with
\((|Q|,|C|)=(4,3)\), contains at least two vertices of \(C\), whose edge is
absent from the already saturated graph \(F[U]=J(U,C)\).  This is a
contradiction.

If \(W\cap Q=\varnothing\), the two cores share no edge: their common
vertices, if any, lie in \(C\), and the B-core has no edge inside \(C\).
They would contribute \(15+18=33>26\) edges to \(F\).  Hence the two core
types cannot coexist.

This proves core uniqueness.

## Choosing the seventh colour

If \(F\) contains no obstruction core, any of the eight remaining
size-ten colours extends the prefix.

Suppose first that the unique core is a C-core \(K_6\) on \(W\).  Every
vertex \(w\in W\) is incident with five differently coloured edges of the
six-matchings union \(F\), so it belongs to at least five of the six
selected supports.  It is therefore forbidden in at most one selected
colour.  Every vertex is forbidden in exactly five of all seventeen
colours, so \(w\) must be forbidden in at least four of the eleven remaining
colours.  Only three remaining colours have support size eight.  Hence some
remaining size-ten colour forbids \(w\).  Its support does not contain the
unique C-core, and no B-core exists, so its residual graph has a perfect
matching.

Suppose instead that the unique core is a B-core \(J(U,C)\).  Any
\(q\in Q=U\setminus C\) has degree six in the core.  Its six incident edges
have different colours, so \(q\) belongs to all six selected supports.
All five colours forbidden at \(q\) are therefore among the eleven
remaining colours.  Again only three of those have size-eight support, so
at least two remaining size-ten colours forbid \(q\).  Choose either one.
Its support omits \(q\), hence cannot contain the unique B-core; no C-core
coexists.  The corrected Tutte classification supplies its perfect
matching.

In both cases the six-prefix extends to seven colours.  This completes the
\(r=0\) proof and, together with the nonzero-\(r\) note, proves the
seven-prefix theorem for every target class-B profile.

## Remaining frontier

The new invariant is existential and stops at seven.  After choosing the
seventh matching, the residual union has seven matching colours and the
core-capacity bounds change.  A proof of the full seventeen-colour
completion still needs a propagated switching/capacity invariant or a
different global argument.

`verify_seven_packing_r0.py` exhausts all labelled pairs of the two core
types relative to canonical representatives using the necessary bounds
(1)--(2), and checks the final row-sum arithmetic.  It is an audit of the
finite core analysis; the universal conclusion rests on the proof above.

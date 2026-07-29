# A narrowed Tutte--Lovász gate for full-row cut sufficiency

Date: 2026-07-28.

## Scope and verdict

This note does not prove full-row cut sufficiency.  It gives an exact
normalization of the \(b\)-factor criterion and eliminates every
Tutte--Lovász witness whose first separator side has at most four vertices.
The first case not settled below is an extremal \(5+5+3\) partition.

Let
\[
t(v)=|\{i:v\in R_i\}|,\qquad b(v)=3-t(v),
\]
and let \(u(v)\) be the incidence of \(v\) in the other eight remaining
rows.  Thus
\[
\rho(v)=t(v)+u(v),\qquad b(V)=30,\qquad 0\le u(v)\le4.
\]

## 1. Exact factor criterion and ledger cancellation

For disjoint \(A,B\subseteq V\), let \(q(A,B)\) be the number of components
\(C\) of \(G-(A\cup B)\) for which
\[
b(C)+e_G(C,B)\quad\hbox{is odd}.
\]
The Tutte--Lovász \(b\)-factor theorem says that \(G\) has a simple
\(b\)-factor if and only if
\[
\Delta(A,B):=
b(A)+\sum_{v\in B}d_{G-A}(v)-b(B)-q(A,B)\ge0             \tag{1}
\]
for every disjoint \(A,B\).

The full eleven-row equation makes (1) unusually concrete.  Since
\[
d_G(v)=12-d_D(v)=11-\rho(v),
\]
one has
\[
d_G(v)-b(v)=8-u(v).
\]
Consequently
\[
\boxed{\quad
\Delta(A,B)=b(A)+8|B|-u(B)-e_G(A,B)-q(A,B).
\quad}                                                   \tag{2}
\]
Also \(\Delta(A,B)\) is even.  Indeed, modulo two, the definition of
\(q(A,B)\) gives
\[
q(A,B)\equiv b(V\setminus(A\cup B))
                  +e_G(V\setminus(A\cup B),B),
\]
and substitution in (1) gives
\(\Delta(A,B)\equiv b(V)=0\pmod2\).

Every component \(C\) of \(G-(A\cup B)\) obeys
\[
|C|\ge 8-|A|-|B|                                      \tag{3}
\]
whenever the right side is positive, because \(\delta(G)\ge7\).

## 2. The empty-\(B\) inequalities

All inequalities with \(B=\varnothing\) hold.

Put \(a=|A|\).  Since the three selected rows have total incidence nine,
\[
b(A)=3a-t(A)\ge3a-9.                                  \tag{4}
\]
For \(a=0,1,2\), (3), connectedness, and the parity of the total \(b\)-sum
give \(q(A,\varnothing)\le b(A)\).

For \(a=3\), there are at most two components.  If \(b(A)>0\), parity gives
\(q(A,\varnothing)\le b(A)\).  If \(b(A)=0\), all three selected rows equal
\(A\).  The only possible failure would make \(G-A\) the union of two
five-vertex odd components, contradicting the already audited individual
matchability of \(G[S_i]=G-A\).

For \(a=4,5,6,7\), the component bounds from (3) are respectively
\[
2,\ 2,\ 3,\ 6,
\]
whereas (4) gives \(b(A)\ge3,6,9,12\).  For \(a\ge8\), the trivial bound
\(q\le13-a\) is smaller than \(3a-9\).  Hence (1) holds whenever
\(B=\varnothing\).

## 3. Every witness with \(|A|\le4\) is impossible

Assume \(B\ne\varnothing\), write \(a=|A|\), \(k=|B|\), and put
\[
p(v)=8-u(v)-e_G(v,A).
\]
Equation (2) becomes
\[
\Delta(A,B)=b(A)+\sum_{v\in B}p(v)-q(A,B),             \tag{5}
\]
and
\[
p(v)\ge4-a.                                            \tag{6}
\]

### The cases \(a\le2\)

For \(a=0\), (6) gives \(\Delta\ge4k-q\).  For \(k=1,2\), (3) gives
\(q\le1\); for \(k\ge3\), \(q\le13-k\le4k\).

For \(a=1\), one has \(\Delta\ge b(A)+3k-q\).  The component bounds for
\(k=1,2\) are \(q\le1,2\), and for \(k\ge3\),
\(q\le12-k\le3k\).

For \(a=2\), one has \(\Delta\ge b(A)+2k-q\).  For \(k=1,2,3\), (3) gives
\(q\le2,2,2\), and for \(k\ge4\),
\(q\le11-k\le2k\).

Thus no negative witness has \(a\le2\).

### The case \(a=3\)

Here \(p(v)\ge1\), so
\[
\Delta\ge b(A)+k-q.                                    \tag{7}
\]
For \(k=1,2,3\), (3) gives \(q\le2,2,3\).  The only apparent slack is
\(k=1,b(A)=0,q=2\), where the lower bound is \(-1\); the evenness of
\(\Delta\) closes it.  For \(k\ge5\), \(q\le10-k\le k\).

For \(k=4\), one has \(q\le6\).  If \(b(A)>0\), (7) is at least \(-1\), so
parity again closes the case.  If \(b(A)=0\), all three selected rows equal
\(A\).  The only lower-bound failure has \(q=6\), which makes the six
vertices of \(V\setminus(A\cup B)\) independent in \(G\).  Each selected
support contains all six, so the cut condition demands three internal
edges there, a contradiction.

### The case \(a=4\)

Now \(p(v)\ge0\) and \(b(A)\ge3\).  The cases \(k=1,2\) have \(q\le2,3\);
for \(k\ge5\), \(q\le9-k\), and parity closes the sole lower bound \(-1\).
It remains to check \(k=3,4\).

If \(k=3\), put \(C=V\setminus(A\cup B)\), so \(|C|=6\).  A negative
witness needs \(b(A)\le4\) and at least five counted components.  Hence
\(e(G[C])\le1\).  But \(b(A)=3\) means that all nine selected-row
incidences lie in \(A\), so (C) demands three edges in \(G[C]\).
If \(b(A)=4\), only one selected-row incidence lies outside \(A\), so at
least two of the selected supports contain all of \(C\), and (C) demands
at least two edges.  Both contradict \(e(G[C])\le1\).

If \(k=4\), then \(|C|=5\).  A negative witness can only have
\[
b(A)=3,\qquad q=5,\qquad p(v)=0\quad(v\in B).           \tag{8}
\]
The first equality puts all selected rows inside \(A\), so \(b(c)=3\) for
\(c\in C\).  The second makes \(C\) five counted singleton components,
and therefore \(G[C]\) is edgeless.  The last equality, together with
\(u(v)\le4\) and \(e_G(v,A)\le4\), gives
\[
u(v)=4,\quad e_G(v,A)=4,\quad d_D(v)=5
\qquad(v\in B).                                        \tag{9}
\]
Thus there are no \(D\)-edges from \(A\) to \(B\).

Every \(c\in C\) already has its four \(D\)-neighbours in \(C\), so it has
at most one further \(D\)-neighbour.  Since its singleton is counted,
\[
3+e_G(c,B)\quad\hbox{is odd}.
\]
As \(|B|=4\), this forces \(e_G(c,B)=4\), hence there are no \(D\)-edges
from \(B\) to \(C\).  Equations (9) would then force every \(v\in B\) to
have five \(D\)-neighbours among the other three vertices of \(B\), an
impossibility.

This proves:

> **Small first-side factor lemma.** Under the full row equations and (C),
> every Tutte--Lovász inequality (1) with \(B=\varnothing\) or
> \(|A|\le4\) holds.

## 4. Earliest exact factor gap

For completeness, the same calculation settles the first four nonempty
\(B\)-sizes when \(|A|=5\).  Now \(p(v)\ge-1\), \(b(A)\ge6\), and
\(|C|=8-k\).  For \(k=1\), (3) gives \(q\le3\), so
\(\Delta\ge6-1-3>0\).

For \(k\ge2\), the crude lower bound is \(-2\).  If \(b(A)\ge7\), it
improves to \(-1\), and parity closes the inequality.  Thus a negative
witness must have equality everywhere:
\[
b(A)=6,\qquad \sum_{v\in B}p(v)=-k,\qquad q=8-k.       \tag{10}
\]
The first equality says that all nine selected-row incidences lie in \(A\).
The second says \(p(v)=-1\) for every \(v\in B\).  The third says that all
\(8-k\) vertices of \(C\) are counted singleton components, so \(G[C]\)
is edgeless.

For \(k=2\), the six-set \(C\) lies in all three selected supports, so (C)
demands three edges in the edgeless graph \(G[C]\).

For \(k=3\), every \(v\in B\) has \(u(v)=4\), \(d_D(v)=5\), and no
\(D\)-neighbour in \(A\).  Every \(c\in C\) already has its four
\(D\)-neighbours inside the independent five-set \(C\).  Counted-singleton
parity, now with \(|B|=3\), forces its possible fifth \(D\)-edge to enter
\(B\).  Hence \(e_D(B,C)=5\), while the deleted-degree sum on \(B\) would
give
\[
15=2e_D(B)+5,
\]
or \(e_D(B)=5>\binom32\), a contradiction.

For \(k=4\), the deleted-degree sum on \(B\) and
\(e_D(B)\le\binom42=6\) force \(e_D(B,C)\ge8\).  Since
\(D[C]=K_4\),
\[
e_D(B\cup C)
=e_D(B)+e_D(B,C)+6
=16+\frac12e_D(B,C)\ge20.
\]
But all three selected supports contain the eight-set \(B\cup C\), so (C)
requires nine residual edges there, equivalently
\(e_D(B\cup C)\le19\), a contradiction.

The first size pair not settled is therefore
\[
|A|=5,\qquad |B|=5,\qquad |C|=3.                       \tag{11}
\]
In this first surviving extremal case every inequality used above must be
tight:

\[
\begin{gathered}
b(A)=6,\qquad R_1,R_2,R_3\subseteq A,\\
p(v)=-1,\quad u(v)=4,\quad d_D(v)=5,\quad
e_G(v,A)=5 \qquad(v\in B),\\
q(A,B)=3,\qquad G[C]\ \hbox{edgeless}.
\end{gathered}                                         \tag{12}
\]

For each \(c\in C\), counted-singleton parity forces
\[
d_D(c,B)\in\{1,3\}.
\]
Writing \(m=e_D(B,C)\), the cut on \(B\cup C\) and the degree sum on \(B\)
leave
\[
m\in\{5,7\}.                                           \tag{13}
\]
No argument here excludes (12)--(13) using the four unselected triples,
four five-sets, and the six prefix layers.  This is the earliest exact
unproved universal step in the factor route.  Even eliminating it would
still leave the cases \(|A|\ge6\).

## 5. Exact colouring interface

Factor existence is not yet the target.  For a fixed \(b\)-factor \(H\),
identify the three colours with the nonzero elements of
\(\mathbb F_2^2\), and let
\[
\sigma(v)=\sum_{i:v\in S_i} i.
\]
Then \(H\) has the prescribed proper three-edge-colouring if and only if
there is a map
\[
x:E(H)\longrightarrow\mathbb F_2^2\setminus\{0\}
\]
such that
\[
\sum_{e\ni v}x(e)=\sigma(v)\qquad(v\in V).             \tag{14}
\]
For degrees one and two, (14) forces exactly the prescribed incident
colours; at degree three, three nonzero elements summing to zero must be
the three distinct colours.

If zero edge labels are allowed, (14) is a linear system whose exact
component condition is
\[
\sum_{v\in K}\sigma(v)=0
\]
for every component \(K\) of \(H\).  In terms of the three support
cardinalities, this says that their three parities are equal; it also allows
the all-odd case.  A nonzero solution is stronger: because every colour
class is a matching internal to \(K\), it forces
\(|K\cap S_i|\) even for every \(i\).  Excluding zero on every edge is the
remaining nonlinear obstruction; it includes ordinary cubic
three-edge-colourability and is not supplied by either parity condition.

Likewise, the direct packing formulation has variables \(x_{e,i}\) with
\[
\sum_{e\ni v}x_{e,i}=1\quad(v\in S_i),\qquad
\sum_i x_{e,i}\le1\quad(e\in G).
\]
Each variable consumes two colour-vertex demands and one shared
edge-resource.  This is a three-uniform exact-matching interface (with
unused-resource fillers), not an ordinary graph matching until an explicit
resource gadget is proved correct.  Condition (C) supplies necessary
internal-capacity inequalities for this system; no proof here shows that
they are its complete obstruction family.

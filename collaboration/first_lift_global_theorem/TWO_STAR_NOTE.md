# A coordinated two-star lemma at the target order

Date: 2026-07-27.

## Scope

This note proves a local coordination theorem for the \(n=13\) class-B
support problem underlying the first lift of Erdős--Rosenfeld Problem #835.
It closes the orientation gap left by the ordinary degree-constrained
bipartite-factor argument.

It does **not** prove that all seventeen support matchings can be chosen
simultaneously.  In particular, it is not yet a completion theorem for
class B, class B-prime, or the fan-realizable subclass.

## Abstract compatibility lemma

Let \(A,B,W\) be sets of size eleven.  Some elements of \(A\) and \(B\) may
carry the same label; write \(A\cap B\) for these identified labels.  Let
\(G_A\subseteq A\times W\) and \(G_B\subseteq B\times W\) be bipartite
graphs, each with minimum degree at least six on both sides.

> **Two-matching lemma.**  There are perfect matchings \(F\) of \(G_A\) and
> \(H\) of \(G_B\) such that no common label \(c\in A\cap B\) is matched to
> the same \(w\in W\) by both \(F\) and \(H\).

No equality of the two neighbourhoods of a common label is needed.

### Preliminary 1: perfect matchings exist

Any balanced \(11\)-by-\(11\) bipartite graph \(G=(X,W)\) of minimum degree
six has a perfect matching.  Indeed, if a nonempty \(S\subseteq X\) violated
Hall, then:

* for \(|S|\le6\), any vertex in \(S\) already has at least six neighbours,
  so \(|N(S)|\ge6\ge|S|\);
* for \(|S|\ge7\), a vertex outside \(N(S)\) would have all its neighbours
  in \(X\setminus S\), a set of size at most four, contrary to minimum
  degree six.

### Preliminary 2: no edge is unavoidable

For every edge \(e\) of such a graph \(G\), the graph \(G-e\) still has a
perfect matching.

Suppose instead that \(S\subseteq X\) violates Hall in \(G-e\).  Since \(G\)
itself satisfies Hall, deleting \(e=xy\) must have removed exactly one
neighbour from \(S\).  Thus, with \(s=|S|\), the neighbourhood in \(G-e\)
has size \(s-1\), \(x\in S\), and \(y\) is the only vertex outside that
neighbourhood adjacent to \(S\), through the sole edge \(xy\).

If \(2\le s\le10\), a vertex of \(S\setminus\{x\}\) has degree at most
\(s-1\), forcing \(s\ge7\).  But there is also a vertex on the right outside
the \(s\)-element neighbourhood of \(S\) in \(G\) and different from \(y\);
it has degree at most \(11-s\), forcing \(s\le5\), a contradiction.  The
cases \(s=1\) and \(s=11\) give a vertex of degree at most one directly.

### The only way deletion of a matching can fail

Let \(D\) be any matching in a balanced \(11\)-by-\(11\) bipartite graph
\(G=(B,W)\) of minimum degree six.  Suppose \(G-D\) has no perfect matching.
Take a Hall-deficient \(S\subseteq B\), put
\[
 T=N_{G-D}(S),\quad s=|S|,\quad t=|T|,\quad
 R=B\setminus S,\quad U=W\setminus T.
\]
Every vertex of \(S\) has at most \(t+1\) neighbours in \(G\), because \(D\)
is a matching.  Hence \(t\ge5\).  Every vertex of \(U\) has at most
\(|R|+1=12-s\) neighbours, so \(s\le6\).  Hall deficiency gives
\(t\le s-1\).  Therefore necessarily
\[
 s=6,\qquad t=5. \tag{1}
\]
All inequalities are equalities.  The edges of \(G\) between \(S\) and \(U\)
are exactly a perfect matching \(P\), all of which lies in \(D\);
furthermore \(G[S,T]=K_{6,5}\) and \(G[R,U]=K_{5,6}\).

In the bipartite complement \(\overline G\), the vertices \(S\cup U\)
therefore induce
\[
 K_{6,6}-P. \tag{2}
\]
Every one of these twelve vertices has complement-degree five, so (2) is an
isolated connected component of \(\overline G\).  The remaining part of the
complement has only ten vertices.  Consequently \(G\) has at most one such
critical six-edge matching \(P\): any Hall failure after deleting any
matching must delete this same \(P\).

### Proof of the lemma

Choose any perfect matching \(F\) of \(G_A\).  For each common label
\(c\in A\cap B\), mark the edge \(cF(c)\) in \(G_B\) if that edge belongs to
\(G_B\).  The marked set \(D_F\) is a matching.

If \(G_B-D_F\) has a perfect matching \(H\), it is compatible with \(F\) and
we are done.  Otherwise the preceding analysis produces the unique critical
matching \(P\subseteq D_F\).  Pick \(e\in P\).  Because \(e\in D_F\), it is
also an edge of \(F\), hence of \(G_A\).  Preliminary 2 gives a perfect
matching \(F'\) of \(G_A-e\).

If \(G_B-D_{F'}\) had no perfect matching, its Hall failure would have to
delete the same unique critical matching \(P\).  That is impossible because
\(e\notin D_{F'}\).  Thus \(G_B-D_{F'}\) has a perfect matching \(H'\), and
\((F',H')\) is the required compatible pair.  This proves the lemma.

## Application to a class-B target instance

Let the thirteen vertices be the hole \(V\), and let \(L(x)\) be the twelve
colours allowed at \(x\).  Fix distinct vertices \(u,v\) and a colour
\(\gamma\in L(u)\cap L(v)\).  Put
\[
 W=V\setminus\{u,v\},\quad
 A=L(u)\setminus\{\gamma\},\quad
 B=L(v)\setminus\{\gamma\}.
\]
All three sets have size eleven.  Join \(c\in A\) (respectively \(c\in B\))
to \(w\in W\) exactly when \(c\in L(w)\).

On the colour side, every support has size at least eight.  A colour common
to \(u,v\) therefore has at least six neighbours in \(W\), and a colour
allowed at only one of them has at least seven.  On the \(W\) side,
\[
 |L(w)\cap A|,\ |L(w)\cap B|\ \ge\ 12+11-17=6. \tag{3}
\]
Both incidence graphs satisfy the two-matching lemma.

Colour \(uv\) by \(\gamma\), colour the eleven edges from \(u\) according to
the first matching, and the eleven edges from \(v\) according to the second.
The compatibility condition says the two colours seen at each \(w\) are
different.  Hence all twenty-three edges incident with \(u\) or \(v\) receive
a proper support-respecting colouring.

Equivalently, two entire adjacent stars can always be coordinated at the
exact target order.  This is stronger than independently applying Hall to
each star: the latter does not prevent a common colour from colliding at a
vertex.

## Remaining frontier

Deleting the two coloured vertices leaves eleven vertices, but the residual
support parameters are not simply another copy of the same class-B problem.
The lemma therefore supplies a rigorous local reduction primitive, not an
induction by itself.  A global proof still needs to coordinate successive
two-star choices, prove a suitable residual invariant, or establish the
full seventeen-matching packing theorem directly.

`verify_two_star_arithmetic.py` checks the finite inequality skeleton and
the connected critical-complement claim used above.  The universal content
rests on the displayed proof, not on random search.

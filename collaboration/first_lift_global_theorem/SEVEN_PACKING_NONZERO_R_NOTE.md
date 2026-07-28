# Seven support matchings pack when a size-twelve support exists

Date: 2026-07-27.

## Scope

Write the target class-B support profile as
\[
 (n_8,n_{10},n_{12})=(7+r,\,10-2r,\,r),\qquad0\le r\le5.
\]
This note proves a seven-colour packing theorem for every \(r\ge1\).  It also
reduces the exceptional \(r=0\) case to two explicit Tutte-barrier shapes.

Thus it is not yet a universal seven-prefix theorem, and it is not a
seventeen-colour completion theorem for class B, class B-prime, or the
fan-realizable subclass.

## A six-matching resilience lemma on twelve vertices

> **Lemma.**  If \(D\) is the union of six matchings in \(K_{12}\), then
> \(K_{12}-D\) has a perfect matching.

Suppose not.  By Tutte's theorem there is \(S\subseteq V(K_{12})\), with
\(s=|S|\), such that \(G-S\), where \(G=K_{12}-D\), has \(k>s\) odd
components.  Parity gives \(k\ge s+2\).

Every vertex loses at most one edge to each of the six matchings, so
\(\Delta(D)\le6\).  If an odd component \(C\) of \(G-S\) has order \(c\),
then all edges from \(C\) to the other components belong to \(D\).  Hence
\[
 12-s-c\le6,\qquad\text{or}\qquad c\ge6-s. \tag{1}
\]
Taking the least odd integer permitted by (1), the cases \(s=0,\ldots,4\)
would require respectively at least
\[
 2\cdot7,\quad3\cdot5,\quad4\cdot5,\quad5\cdot3,\quad6\cdot3
\]
vertices outside \(S\), more than \(12-s\).  If \(s\ge6\), already
\(s+2>12-s\).  The only remaining case is \(s=5\): seven singleton odd
components.

But then every edge of the \(K_7\) on those seven vertices belongs to \(D\).
Each matching contains at most three edges of a \(K_7\), so the six
matchings cover at most eighteen of its twenty-one edges, a contradiction.
This proves the lemma.

## Seven colours for every nonzero \(r\)

The six-colour theorem in `SIX_PACKING_NOTE.md` can be chosen so that a
size-twelve support remains unused:

* if \(r=1\), pack supports \(8,8,8,8,10,10\), using the coordinated
  ten-vertex lemma for the last two;
* if \(2\le r\le4\), greedily pack \(8,8,8,8,10,12\);
* if \(r=5\), greedily pack \(8,8,8,8,12,12\).

The stated support counts are available in each profile.  On any unused
size-twelve support, the six already chosen colour classes restrict to a
union of six matchings.  The resilience lemma supplies a perfect matching
avoiding all of them.  Therefore seven prescribed support matchings pack for
every \(r\ge1\).

## The exact remaining \(r=0\) barriers

Now let \(r=0\), so the profile is \((7,10,0)\).  Pack four size-eight
supports and then coordinate two size-ten supports as in
`SIX_PACKING_NOTE.md`.  Let \(V\) be a third size-ten support, and suppose
its residual graph has no perfect matching.

Apply Tutte to \(K[V]\) after deleting the six existing matchings.  The
deleted graph has maximum degree at most six.  The same component-size
calculation leaves five numerical shapes.  Two are impossible by edge
capacity:

* \(S\) of size one with three components of order three requires all
  \(27\) intercomponent edges, but six matchings on nine vertices cover at
  most \(6\cdot4=24\);
* \(S\) of size three with seven singleton components requires \(K_7\),
  whose \(21\) edges exceed \(6\cdot3=18\).

The three numerical survivors are:

1. \(S=\varnothing\), two components of order five, requiring all \(25\)
   edges of a \(K_{5,5}\);
2. \(|S|=3\), component orders \(3,1,1,1,1\), requiring the \(18\) edges
   of \(K_7-E(K_3)\);
3. \(|S|=4\), six singleton components, requiring the \(15\) edges of
   \(K_6\).

The first survivor is incompatible with the class-B row sums.  The four
size-eight matchings have four edges each and the two size-ten matchings
have five each, for a total crossing capacity
\[
 4+4+4+4+5+5=26.
\]
To cover the \(25\) distinct edges of \(K_{5,5}\), exactly one of the six
matchings has crossing deficit one and all others attain their maximum.

If the deficient matching has size eight, the other three size-eight
supports and both size-ten supports lie entirely in \(V\).  Every one of
the three vertices outside \(V\) already forbids those five colours, so it
must belong to the deficient support.  That support then has only five
vertices in \(V\), too few to supply its required three crossing edges.

If the deficient matching has size ten, all four size-eight supports and
the other size-ten support lie in \(V\).  Again the five-forbidden-colours
condition forces all three outside vertices into the deficient support.
It then has only seven vertices in \(V\), too few to supply four crossing
edges.  Thus the \(5+5\) barrier is impossible.

Consequently a failure of the seventh matching in the exceptional profile
must have one of exactly two forms:
\[
 K_7-E(K_3)\quad\text{or}\quad K_6
\]
fully covered by the six previously selected matchings, on the vertices
outside the respective Tutte set.

## Remaining frontier

The two surviving saturation patterns are equality cases, not
counterexamples.  The six-prefix can still be re-chosen, and no class-B
instance is known in which every eligible third size-ten support produces
one of them.  Closing \(r=0\) requires a switching argument that breaks both
patterns, or a checkable instance proving that no seven-prefix exists.

`verify_seven_packing_boundary.py` checks the finite component arithmetic,
profile choices, capacity eliminations, and the row-sum contradiction for
the \(5+5\) barrier.

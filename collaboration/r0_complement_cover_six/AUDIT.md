# Independent claim audit

Date: 2026-07-28.

This audit checks the solver-free theorem in `NOTE.md`; the accompanying
script checks its finite arithmetic and displayed switches.

## Dependency check

The only imported matching result is the two-support lemma in
`../first_lift_global_theorem/SIX_PACKING_NOTE.md`: two arbitrary graphs on
ten vertices, each of minimum degree at least five, have edge-disjoint
perfect matchings.  Its proof classifies every matching-deletion obstruction
as either \(K_5\dot\cup K_5\) plus its unique crossing matching or
\(K_{4,6}\) plus its unique matching on the six-side.  The critical matching
is determined by the complement of the ambient graph, so avoiding one of its
edges repairs the first choice.  This is sufficient for the invocation in
the three-support lemma, where each prescribed ten-support has minimum
degree at least six before either matching is deleted.

## Covering check

For a vertex of five-set multiplicity \(a\), its triple multiplicity is
\(5-a\), giving exactly
\[
 p(a)=\frac{\binom{7-a}{3}}{\binom73}
      \frac{\binom{5+a}{3}}{\binom{10}3}.
\]
The pointwise bound \(p(a)\le(5-a)/36\), together with
\(\sum a=35\), makes the expected number of uncovered vertices at most
\(5/6\).  Since that number is integral, a zero-uncovered selection exists.
The verifier checks every value and the exact relaxed integer maximum.

## Tutte catalogue check

After two selected ten-support matchings are removed, the target graph has
ten vertices and minimum degree at least four.  For a Tutte separator of
size \(q\), every odd component of order \(c\) satisfies
\(c-1+q\ge4\).  Parity and the ten-vertex budget leave only:

1. \(q=0\), two components of order five; and
2. \(q=4\), six singleton components.

There are no omitted even-component cases: in both surviving patterns the
odd components already use all \(10-q\) available vertices.

## Edge-availability check

In the two-\(K_5\) case, minimum degree six in the pre-deletion graph forces
ten crossing edges.  The two deleted matchings can supply at most ten, so
both are crossing perfect matchings and both supports equal the target
support.  The replacement edges lie in the two untouched \(K_5\) components;
the third matching uses one freed crossing edge and untouched internal
edges.

In the separator-four case, every one of the six singleton-side vertices
has four residual neighbours in the separator and needs two more neighbours
inside the six-side.  Those two edges must be one from each deleted matching.
Thus both matchings pair the six-side internally.  Each six-side vertex
already has its maximum possible three nonneighbours inside that side, so
the ambient minimum-degree-nine hypothesis forces adjacency to all seven
outside vertices.  The displayed two-edge switch is therefore available,
does not meet the second deleted matching, and frees exactly the edge needed
by the third matching.

## Scope

The audit accepts the claimed complement-covering six-prefix theorem for
profile \(r=0\).  It does not prove the remaining three-match extension,
coordinated nine for \(r=0\), full class-B completion, or Problem #835.

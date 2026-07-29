# Four-\(K_6\) obstruction families in the exceptional profile

Date: 2026-07-27.

## Result and scope

In the exceptional \(r=0\) profile, four distinct \(K_6\) obstruction
cores cannot collectively account for all seven blocked size-ten
supports.

This is not a non-coexistence statement.  Many four-\(K_6\) families fit
inside a graph satisfying the necessary seven-prefix screens.  The exact
classification below shows that every family with enough simultaneous
complement capacity has a common high-degree vertex, and the full
complement-row identity then rules out assigning all seven supports to
those cores.

## Exact two-shape classification

Fix one \(K_6\) under the action of \(S_{13}\), and enumerate every
unordered choice of three further distinct \(K_6\)'s.  Retain only unions
\(J\) satisfying
\[
 |E(J)|\le31,\quad \Delta(J)\le7,\quad
 |E(J)|+\left\lceil\frac{\sum_v(2-d_J(v))_+}{2}\right\rceil\le31,
\]
the nine-vertex induced-capacity inequalities, and all fifteen
subfamily-capacity inequalities from `R0_THREE_CORE_CAPACITY.md`.

Of the \(7{,}971{,}964\) candidate families, \(18{,}410\) pass the graph
screens and \(15{,}260\) admit a positive multiplicity assignment
\[
 t_1+t_2+t_3+t_4=7,\qquad1\le t_i\le4
\]
through every subfamily-capacity inequality.  Every one has one of exactly
two forms:

1. \(J=K_7\).  All four \(K_6\)'s lie in the same seven-vertex set.  Their
   four supports have a three-vertex intersection, and every vertex in
   that intersection has \(d_J(v)=6\).
2. \(J\) has 26 edges on one eight-vertex set.  The four supports have an
   intersection of order two or three, and every vertex in it has
   \(d_J(v)=7\).

With the first core fixed, the first shape contributes 140 labelled
families and seven distinct union graphs.  The second contributes 15,120
labelled families and 1,008 distinct union graphs: 10,080 families have
common intersection order three and 5,040 have common intersection order
two.

## Row-identity exclusion

Assign each of the seven allegedly blocked supports to one of the four
cores certifying it.  Let \(v\) be any vertex in the common intersection
of the four core supports.  The complement triple of a support assigned
to a core lies outside that core support.  Therefore none of the seven
remaining complement triples contains \(v\).

Only the three complement five-sets of the remaining size-eight supports
can contain \(v\), and each is a set, so \(v\) occurs in at most three of
them.  But the exact complement-row identity says that \(v\) occurs in
exactly
\[
 d_F(v)-2
\]
of all ten remaining complement sets.  Since \(J\subseteq F\), either
classified shape gives
\[
 d_F(v)-2\ge d_J(v)-2\ge4,
\]
a contradiction.

Thus neither shape can be a total obstruction, and four distinct
\(K_6\) cores cannot account for all seven remaining size-ten supports.

## Reproduction and frontier

`verify_r0_four_k6.py` reproduces the complete classification
deterministically and checks the common-intersection degree contradiction.

Mixed families of four distinct cores are now excluded in
`R0_FOUR_CORE_WITH_3311.md` and `R0_ALL_FOUR_CORE_FAMILIES.md`.
Therefore a hypothetical total obstruction needs at least five distinct
cores.  Families of five or more distinct cores remain open.

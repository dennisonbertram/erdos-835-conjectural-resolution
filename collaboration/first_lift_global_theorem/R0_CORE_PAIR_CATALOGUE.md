# Exact core-pair screen for the exceptional profile

Date: 2026-07-27.

## Result and scope

In the exceptional \(r=0\) profile, a seven-matching prefix has four
size-eight and three size-ten colours.  Its union \(F\) satisfies
\[
 |E(F)|=31,\qquad 2\le d_F(v)\le7, \qquad
 |E(F[X])|\le7\lfloor |X|/2\rfloor. \tag{1}
\]
`EIGHTH_MATCHING_CORE_CATALOGUE.md` lists the seven core types that can
obstruct a remaining size-ten support.  This note exhausts every labelled
embedding of every pair of those core types, up to fixing the first core
under \(S_{13}\), and retains only pairs that pass all necessary conditions
in (1).

The screen is exact for those necessary conditions.  A surviving entry does
not assert that the pair extends to an actual seven-coloured \(F\), and the
table by itself is not yet an eighth-colour theorem.

## The additional minimum-degree screen

For a candidate union \(J=J_1\cup J_2\), put
\[
 \partial(J)=\sum_{v=0}^{12}\max\{0,2-d_J(v)\}. \tag{2}
\]
Every completion of \(J\) to an \(F\) satisfying \(\delta(F)\ge2\) needs at
least \(\lceil\partial(J)/2\rceil\) additional edges.  Therefore
\[
 |E(J)|+\left\lceil\frac{\partial(J)}2\right\rceil\le31 \tag{3}
\]
is necessary.

Under \(|E(J)|\le31\) and \(\Delta(J)\le7\), the induced-capacity condition
in (1) needs a separate check only on nine-vertex subsets.  For even sets it
follows from the degree bound; odd sets of order at most seven satisfy it
even for a clique; and the capacities on eleven and thirteen vertices
exceed the global 31-edge budget.

## Exact pair table

Write the core types by their multipartite block sizes:
\[
 37,\ 55,\ 333,\ 5111,\ 3311,\ 31111,\ 6.
\]
An integer in the table is the minimum number
\(|E(J_2)\setminus E(J_1)|\) of new edges contributed by a **distinct**
second core among all surviving embeddings.  A dash means no distinct pair
of those types can occur in any \(F\) satisfying (1).

\[
\begin{array}{c|rrrrrrr}
 &37&55&333&5111&3311&31111&6\\ \hline
37    &7&-&-&9&7&6&-\\
55    & &-&-&3&-&-&-\\
333   & & &-&-&-&-&-\\
5111  & & & &4&6&3&3\\
3311  & & & & &2&1&2\\
31111 & & & & & &2&1\\
6     & & & & & & &5
\end{array} \tag{4}
\]

Several consequences are immediate.

* A \(K_{3,3,3}\) core cannot coexist with any other obstruction core,
  including a distinct \(K_{3,3,3}\).
* A \(K_{5,5}\) core can coexist only with a core of type
  \(K_{5,1,1,1}\), and two distinct \(K_{5,5}\)'s cannot coexist.
* A \(K_{3,7}\) cannot coexist with a \(K_{5,5}\), \(K_{3,3,3}\), or
  \(K_6\).
* The sparsest compatible overlaps occur among the final three types.  For
  example, a \(K_{3,1,1,1,1}\) and a \(K_6\) can differ by only one edge.

The \(r=0\) reuse inequality proves that no fixed core obstructs all seven
remaining size-ten supports.  Thus a hypothetical total obstruction needs
at least two distinct cores, and (4) is now the complete pair-type search
space for the next overlap or switching argument.

## Exhaustiveness

The verifier fixes a canonical first core and generates every distinct
labelled second core on thirteen vertices.  The exact embedding counts are
\[
\begin{array}{c|rrrrrrr}
\text{type}&37&55&333&5111&3311&31111&6\\ \hline
\text{embeddings}
&34320&36036&200200&72072&360360&60060&1716.
\end{array}
\]
It then checks the 31-edge budget, maximum degree seven, (3), and every
nine-vertex induced capacity before recording the minimum in (4).

`verify_r0_core_pairs.py` reproduces the complete table deterministically.

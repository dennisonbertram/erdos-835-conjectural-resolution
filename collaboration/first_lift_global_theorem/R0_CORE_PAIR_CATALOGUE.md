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

## The \(K_{5,5}\) branch is impossible

The exact complement-degree argument in
`EIGHTH_MATCHING_CORE_CATALOGUE.md` shows that a fixed \(K_{5,5}\) can
obstruct at most one of the seven size-ten supports in a hypothetical total
obstruction.  If a \(K_{5,5}\) were actually used, some distinct core would
therefore also be needed.  Table (4) says that the only possible partner
type is \(K_{5,1,1,1}\).

The exhaustive pair calculation gives a stronger structural fact.  Fix the
\(K_{5,5}\) on sides \(A,B\), and let \(O\) be the three outside vertices.
All twenty surviving partner embeddings have the same form up to the
stabilizer of the first core:
\[
 J_1\cup J_2=K_{5,5}[A,B]\ \cup\ K_3[T],
 \qquad T\in\binom A3\ \text{or}\ T\in\binom B3. \tag{5}
\]
Thus their union has twenty-eight edges, all on \(A\cup B\), and no edge
incident with \(O\).

Only three further edges remain in the 31-edge graph \(F\), so
\[
 \sum_{v\in O}d_F(v)\le6. \tag{6}
\]
But a size-ten support blocked by the \(K_{5,5}\) is exactly \(A\cup B\);
its complement triple is \(O\).  By the exact complement identity, every
\(v\in O\) then has \(d_F(v)-2\ge1\), or \(d_F(v)\ge3\).  This gives
\[
 \sum_{v\in O}d_F(v)\ge9,
\]
contradicting (6).

Therefore a \(K_{5,5}\) cannot be an obstruction core used by any of the
seven blocked supports in a total-obstruction argument.

## A \(K_6\) cannot be reused five times

Let \(C\) be the vertex set of a \(K_6\) core, and let \(O\) be the other
seven vertices.  Suppose five blocked supports reused this core.  The
sixfold exclusion in `EIGHTH_MATCHING_CORE_CATALOGUE.md` shows that the
other two supports do not reuse it.  Since the clique fills every pair
inside \(C\), write the other sixteen edges of \(F\) as
\[
 a=|E_F(C,O)|,\qquad c=|E_F(O)|,\qquad a+c=16.
\]
The complement capacity in \(O\) is
\[
 \sum_{v\in O}(d_F(v)-2)=2c+a-14=18-a.
\]
Five complement triples inside \(O\) require fifteen incidences, so
\[
 a\le3. \tag{7}
\]

The other two blocked supports require a distinct obstruction core \(J\).
It cannot lie wholly in \(C\), where the only core is the original \(K_6\).
If it lies wholly in \(O\), it needs at least fifteen edges.  For
\(a\ge2\), however, \(c=16-a<15\).  For \(a=0\) or \(1\), the only possible
type is a \(K_6\); its fifteen edges leave the seventh vertex of \(O\)
incident with at most the one remaining edge inside \(O\) and the at most
one cross edge, giving degree at most one when \(a=0\) or \(1\).  This
contradicts \(\delta(F)\ge2\).

Finally, \(J\) cannot meet both \(C\) and \(O\).  The exact pair enumeration
has the following structural refinement:

> Every distinct obstruction core compatible with a fixed \(K_6\) and
> meeting both sides of the cut \((C,O)\) uses at least four
> \(C\)-to-\(O\) edges.

The minimum four is attained by a core of type \(K_{3,1,1,1,1}\);
\(K_{5,1,1,1}\) needs at least six.  This contradicts (7).  Hence no
distinct core exists, and the two remaining blocked supports cannot be
explained.

Therefore a fixed \(K_6\) can be reused at most four times in a total
seven-support obstruction.

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
nine-vertex induced capacity before recording the minimum in (4).  It also
checks all twenty surviving \(K_{5,5}+K_{5,1,1,1}\) embeddings and verifies
the structural form (5), and checks the four-edge cross-cut lower bound for
every surviving partner of a fixed \(K_6\).

`verify_r0_core_pairs.py` reproduces the complete table deterministically.

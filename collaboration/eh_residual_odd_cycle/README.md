# Odd-cycle certificate in the Etzion--Hartman residual

## Result and scope

The checked file

```text
collaboration/ls3420_branch0_search/eh15_branch0_partial.txt
```

contains \(4\,845=\binom{20}{4}\) rows: \(4\,773\) assigned quadruples and
72 holes.  Fifteen colour classes are complete \(S(3,4,20)\) systems.
Colours \(0\) and \(13\) each have 249 assigned blocks and are the two
unfinished classes.

Delete the fifteen complete systems and retain all 570 remaining
quadruples, including the 72 holes.  Their residual graph is **not
bipartite**.  A shortest odd cycle is the triangle

\[
\begin{aligned}
A&=\{0,2,14,17\},\\
B&=\{0,5,14,17\},\\
C&=\{2,5,14,17\}.
\end{aligned}
\tag{1}
\]

All three are holes in the checked input, at lines 277, 593, and 2089.
Their pairwise intersections are the triples

\[
A\cap B=\{0,14,17\},\qquad
B\cap C=\{5,14,17\},\qquad
C\cap A=\{2,14,17\}.
\tag{2}
\]

Consequently the particular fifteen complete systems in this
Etzion--Hartman partial cannot be extended to an \(LS(3,4,20)\).  This says
nothing about a different family of fifteen systems and does **not** prove
that \(LS(3,4,20)\) is impossible.  It also does not resolve
Erdős--Rosenfeld problem #835.

The branch-0 CP-SAT process received this file only through its advisory
`--hint` mechanism.  It is allowed to change any hinted value.  Therefore
this certificate does **not** make the branch-0 CP-SAT instance infeasible
and does not prevent that search from finding a different completion.

## 1. Why the last-two-system problem is bipartiteness

Let \({\cal S}_1,\ldots,{\cal S}_{15}\) be the fifteen complete
\(S(3,4,20)\) systems in the file, and let \(R\) be the set of quadruples
outside their union.  Every triple \(T\subset[20]\) has seventeen
extensions \(T\cup\{x\}\).  Each complete Steiner system uses exactly one,
so exactly two extensions remain in \(R\).

Define a graph \(G\) with vertex set \(R\).  For every triple \(T\), join
the two residual blocks containing \(T\).  There are no loops or parallel
edges: distinct quadruples share at most one triple.

If the fifteen systems extended to a large set, the two final systems would
give a two-colouring of \(G\), because the two residual extensions of every
triple must receive different final colours.  Conversely, a bipartition of
\(G\) puts exactly one extension of every triple in each side, so each side
is an \(S(3,4,20)\).  Therefore

\[
\boxed{\text{the fixed fifteen systems extend}\iff G\text{ is bipartite}.}
\tag{3}
\]

The tentative \(0/13\) labels on 498 residual blocks are not needed for
this equivalence.  We retain those blocks as unlabelled vertices of \(G\).
Thus the obstruction below remains valid even if those two partial colour
classes are completely recoloured.

## 2. The three-line certificate

The raw input contains:

```text
277:  0 2 14 17 -1
593:  0 5 14 17 -1
2089: 2 5 14 17 -1
```

Thus \(A,B,C\) are all residual vertices.  By (2), each pair shares a
triple and hence is an edge of \(G\).  The three vertices form a
\(3\)-cycle.

In any proposed last-two-system completion, the shared triple
\(\{0,14,17\}\) forces \(A\) and \(B\) to opposite sides.  The triple
\(\{5,14,17\}\) forces \(B\) and \(C\) to opposite sides, so \(A\) and
\(C\) must lie on the same side.  But the triple \(\{2,14,17\}\) forces
\(C\) and \(A\) to opposite sides, a contradiction.

A triangle is the shortest possible odd cycle in a simple graph, so (1) is
a smallest odd-cycle certificate.

## 3. Exact residual census

The verifier independently reconstructs the graph from the raw rows.  It
finds:

\[
|V(G)|=570,\qquad |E(G)|=1140,\qquad \deg_G(v)=4
\quad\text{for every }v.
\tag{4}
\]

The \(4\)-regularity is also immediate: every residual quadruple contains
four triples, and each triple supplies one residual mate.

The connected-component census is:

| component size | number | bipartite? |
|---:|---:|:---|
| 5 | 4 | no |
| 25 | 12 | no |
| 250 | 1 | yes |

Each 5-vertex component is \(4\)-regular and therefore is a \(K_5\).  The
four underlying five-point sets are

\[
\begin{gathered}
\{0,2,5,14,17\},\quad
\{1,3,4,15,16\},\\
\{6,8,11,13,18\},\quad
\{7,9,10,12,19\}.
\end{gathered}
\tag{5}
\]

For example, all five four-subsets of \(\{0,2,5,14,17\}\) are residual.
The triangle in (1) consists of three of them.  The graph contains 40
triangles in total, ten in each \(K_5\).

These census facts are useful independent controls, but the three rows in
Section 2 are already a complete nonextendibility proof.

## 4. Verification

Run:

```sh
python3 -B \
  collaboration/eh_residual_odd_cycle/verify_eh_residual_odd_cycle.py
```

The verifier uses only Python's standard library and exact set/integer
operations.  It checks the input SHA-256

```text
06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78
```

and then independently checks:

* all \(\binom{20}{4}=4\,845\) rows in lexicographic block order;
* 4,773 assignments and 72 holes;
* the fifteen complete \(S(3,4,20)\) systems;
* exactly two residual extensions over each of the 1,140 triples;
* the 570-vertex, 1,140-edge, 4-regular residual graph;
* the explicit triangle and a breadth-first bipartiteness failure;
* the full component and triangle census in Section 3.

**Scope:** this is an exact certificate against freezing and extending this
particular Etzion--Hartman fifteen-system partial.  It does not constrain a
solver that may revise the hint, is not a general \(LS(3,4,20)\)
nonexistence proof, and leaves #835 open.

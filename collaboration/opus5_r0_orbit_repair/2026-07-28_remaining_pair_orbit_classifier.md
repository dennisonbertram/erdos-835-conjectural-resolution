# Exact compatible-pair catalogue for support orbits 4--15

Date: 2026-07-28

## Result

The compatible-pair reduction for each remaining prescribed-colour support
orbit now has an exact, generic symmetry classifier.

For every orbit, choose lexicographically a pair \(R_i,R_j\) having maximum
intersection, put \(S_a=V(K_{13})\setminus R_a\), and enumerate every ordered
pair

\[
(P_i,P_j),
\qquad
P_i\text{ a perfect matching on }S_i,\quad
P_j\text{ a perfect matching on }S_j,\quad
P_i\cap P_j=\varnothing.
\]

The classifier quotients these pairs by the full automorphism group of the
three-support system that stabilizes the selected unordered pair
\(\{S_i,S_j\}\).  When such an automorphism interchanges \(S_i,S_j\), the
matching colours are swapped as well.

The exact counts are:

| orbit | Venn signature | representative rows \(R_0;R_1;R_2\) | chosen pair | \(r=|R_i\cap R_j|\) | pair swap? | labelled disjoint pairs | canonical pair orbits |
|---:|---|---|---|---:|---|---:|---:|
| 4 | \((0,0,2,2,0,0,1)\) | \(012;012;234\) | \(0,1\) | 3 | yes | 514,080 | **11** |
| 5 | \((0,0,3,3,0,0,0)\) | \(012;012;345\) | \(0,1\) | 3 | yes | 514,080 | **17** |
| 6 | \((0,1,1,1,1,0,1)\) | \(012;023;124\) | \(0,1\) | 2 | no | 570,780 | **23** |
| 7 | \((0,1,2,2,1,0,0)\) | \(012;013;245\) | \(0,1\) | 2 | no | 570,780 | **76** |
| 8 | \((1,1,0,1,0,0,2)\) | \(012;123;124\) | \(0,1\) | 2 | yes | 570,780 | **16** |
| 9 | \((1,1,1,1,1,1,0)\) | \(012;135;245\) | \(0,1\) | 1 | yes | 627,900 | **87** |
| 10 | \((1,1,1,2,0,0,1)\) | \(012;123;245\) | \(0,1\) | 2 | yes | 570,780 | **47** |
| 11 | \((1,1,2,3,0,0,0)\) | \(012;123;456\) | \(0,1\) | 2 | yes | 570,780 | **93** |
| 12 | \((1,2,1,2,1,0,0)\) | \(012;134;256\) | \(0,1\) | 1 | no | 627,900 | **300** |
| 13 | \((2,2,0,2,0,0,1)\) | \(012;234;256\) | \(0,1\) | 1 | yes | 627,900 | **109** |
| 14 | \((2,2,1,3,0,0,0)\) | \(012;234;567\) | \(0,1\) | 1 | yes | 627,900 | **181** |
| 15 | \((3,3,0,3,0,0,0)\) | \(012;345;678\) | \(0,1\) | 0 | yes | 684,180 | **166** |

In total, 7,077,840 labelled compatible pairs reduce to 1,126 canonical
types.

## Why paths and cycles suffice

Let \(r=|R_i\cap R_j|\).  The common part of the two supports has size
\(7+r\).  Each vertex there has one incident \(P_i\)-edge and one incident
\(P_j\)-edge.  Each of the \(3-r\) vertices in \(S_i\setminus S_j\) has
degree one and colour \(i\), each of the \(3-r\) vertices in
\(S_j\setminus S_i\) has degree one and colour \(j\), and the \(r\) vertices
outside both supports are isolated.

Therefore \(P_i\cup P_j\) is a disjoint union of:

- \(3-r\) alternating paths whose endpoints are the degree-one vertices;
  and
- alternating even cycles on the unused common vertices.

Paths between unlike endpoint colours have even length.  Paths whose
endpoints have the same colour have odd length.  This completely describes
the possible unlabelled component shapes, but the third support can
distinguish vertices at different positions.  The component-word invariant
retains exactly that information.

## Canonical component-sequence invariant

Label each vertex by its full Venn mask

\[
\mu(v)=\sum_{a=0}^2 2^a\,1_{\{v\in R_a\}}\in\{0,\ldots,7\}.
\]

For an oriented path, record

\[
\bigl(P;\ \mu(v_0),\ldots,\mu(v_\ell);\
       c(v_0v_1),\ldots,c(v_{\ell-1}v_\ell)\bigr),
\]

where every edge colour is \(i\) or \(j\).  Minimize this word over the two
path orientations.

For an oriented cycle, record the cyclic vertex-mask word and the colour of
the outgoing edge at every position.  Minimize over every starting vertex
and both directions.  Including outgoing-edge colours retains the
alternating phase; the dihedral minimization removes it exactly when a
colour-preserving component isomorphism does.

Sort all canonical component words to form a multiset.  Finally minimize
that multiset over every row permutation \(\sigma\) satisfying:

1. \(\sigma\) preserves the seven-cell Venn signature; and
2. \(\sigma(\{i,j\})=\{i,j\}\).

The second condition is necessary because the classified state space uses
the fixed chosen pair.  A symmetry sending it to a different maximum-
intersection pair does not act on this state space.  If \(\sigma(i)=j\),
the two edge colours are swapped.  This is the optional pair swap shown in
the table.

## Proof that the invariant is complete

Let

\[
C_m=\{v:\mu(v)=m\}.
\]

Every automorphism fixing all three rows pointwise is an arbitrary
permutation inside each \(C_m\).  A row permutation preserving the Venn
signature is realized by bijections

\[
C_m\longrightarrow C_{\sigma(m)}.
\]

Thus the full group acting on the chosen pair is

\[
\left(\prod_{m=0}^7\operatorname{Sym}(C_m)\right)\rtimes H,
\]

where \(H\) is the allowed row-permutation group above.

Suppose two coloured matching pairs have the same canonical invariant.
Choose row symmetries attaining the same minimized component multiset.
Equal path words give mask- and colour-preserving component isomorphisms,
possibly after path reversal.  Equal cycle words give the same after a
rotation or reflection.  Match equal components and combine these
isomorphisms.  They map every used vertex to a vertex in the required Venn
cell and preserve every coloured edge.

The two component multisets use the same number of vertices in every cell.
Extend the component bijection arbitrarily over the unused vertices of each
cell.  The result is a permutation of all 13 vertices realizing an allowed
support automorphism and carrying one matching pair to the other.

Conversely, any allowed automorphism preserves the path/cycle decomposition,
the Venn masks up to its single global row permutation, and the edge colours
up to the corresponding optional pair swap.  Hence it preserves the
canonical invariant.  Equality of invariants is therefore equivalent to
membership in the same group orbit.

## Independent exhaustive action-graph audit

The script does not rely only on the preceding completeness proof.  For
each support orbit it constructs a second, independent partition of all
labelled compatible pairs.

The pointwise cell group is generated by adjacent transpositions within
each nontrivial \(C_m\).  For every nonidentity allowed row symmetry, the
script constructs a canonical cell-to-cell vertex bijection.  These actions
generate the full semidirect product above.

The audit:

1. enumerates all \(945^2\) ordered perfect-matching pairs and keeps exactly
   the edge-disjoint ones;
2. computes the image of every retained pair under every action generator;
3. forms the connected components of this finite action graph with a
   disjoint-set data structure;
4. checks exhaustively that each generator preserves the component-word
   invariant; and
5. checks both directions of partition equality: every invariant bucket has
   one action-graph root and every root has one invariant.

For every orbit 4--15, the action-graph orbit count equals the bold count in
the table.  No collision or split was found.

Run the complete audit:

```sh
TMPDIR=/private/tmp /usr/bin/python3 -B \
  collaboration/opus5_r0_orbit_repair/2026-07-28_remaining_pair_orbit_classifier.py
```

Use `--skip-generator-audit` only for a faster enumeration of the primary
component invariant; it is not the full independent audit.

## Scope

This is an exact symmetry reduction, not a prescribed-colour packing proof.
It gives the complete compatible-pair starting catalogue for orbit-specific
finite reductions on support orbits 4--15.  It does not prove those 12
cut-sufficiency cases, the coordinated-nine theorem, or
Erdős--Rosenfeld Problem #835.

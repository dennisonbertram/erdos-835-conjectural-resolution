# Exact symmetries and a ten-point obstruction in the EH 15-core

## Result and scope

Let \(\mathcal C_0,\ldots,\mathcal C_{14}\) be the fifteen complete
SQS(20)s in the authenticated Etzion--Hartman partial.  This directory
establishes two exact facts.

1. The point/system automorphism group of this particular fifteen-system
   core is trivial.  Consequently its action on the
   \(\binom{15}{3}=455\) choices of three systems to drop has 455 singleton
   orbits: there is no honest automorphism quotient of those cases.
2. Thirty of the 455 cases are nevertheless impossible for a separate,
   local reason.  If all three dropped systems lie in one of the construction
   five-packs

   \[
   \{0,1,2,3,4\},\quad
   \{5,6,7,8,9\},\quad
   \{10,11,12,13,14\},
   \]

   then a ten-point induced subgraph of the five-fold leave is not
   five-colourable.  A small standard-library exhaustive search checks all
   \(3\binom53=30\) cases.  Thus only 425 drop-three repairs remain.

This is a theorem about repair attempts retaining twelve members of one
specific EH core.  It does **not** decide \(LS(3,4,20)\), and it does not
resolve Erdős--Rosenfeld Problem #835.

## Authenticated input and labels

The verifier reads
`collaboration/ls3420_branch0_search/eh15_branch0_partial.txt`, whose SHA-256
is

```text
06ad9c5d8377183aa13e7acb070a0b9b9efbd3f528989701f5688d9b72ff1d78
```

That file is a point- and colour-relabelling of the EH seed.  The branch-0
colours of the original EH systems \(0,\ldots,14\) are, in order,

```text
11,14,12,2,1,4,6,7,16,9,3,5,8,15,10
```

The script extracts those fifteen 285-block classes, and independently checks
that each covers every triple exactly once and that the classes are pairwise
block-disjoint.

## The five-fold leave

For a dropped triple \(D\subset\{0,\ldots,14\}\), retain the other twelve
systems and let

\[
L_D=\binom{[20]}4\setminus
 \bigcup_{c\notin D}\mathcal C_c.
\]

Every triple has exactly five extensions in \(L_D\).  Form \(G_D\) with
vertex set \(L_D\), joining two blocks when they share a triple.  A
five-colouring of \(G_D\) partitions \(L_D\) into five SQS(20)s, and together
with the retained twelve systems gives an \(LS(3,4,20)\).  Conversely any
such completion gives a five-colouring.  Hence the selected twelve-system
subcore extends exactly when \(G_D\) is five-colourable.

## Why the full automorphism group is exhausted

First delete all blocks owned by the fifteen systems.  The graph on the 570
remaining blocks, adjacent when they share a triple, has components

\[
250,\quad 12\times25,\quad 4\times5.
\]

The four five-vertex components are complete graphs and are exactly all
four-subsets of the following intrinsic five-point groups:

```text
Q0 = 0,2,5,14,17
Q1 = 1,3,4,15,16
Q2 = 6,8,11,13,18
Q3 = 7,9,10,12,19
```

They partition the twenty points.  Every point/system automorphism preserves
unowned blocks and shared triples, so it must permute these four components
and therefore the four point groups.

The verifier consequently exhausts all \(4!\) group correspondences and all
within-group point bijections.  Whenever a fourth point is assigned, every
newly completed four-set is checked.  Unowned blocks must map to unowned
blocks, while owned blocks incrementally force a bijection of the fifteen
systems.  This visits 11,837 search nodes and has one complete leaf, the
identity.  The leaf is then checked directly on all 4,845 four-sets.  This
establishes completeness without nauty, NetworkX, or another isomorphism
package.

The induced system action therefore also has order one, and all 455
drop-three orbits are singletons.

## The thirty locally impossible repairs

The three construction five-packs are attached to these partitions of the
four intrinsic point groups:

| dropped-system pack | paired point groups |
|---|---|
| \(0,\ldots,4\) | \((Q_0,Q_1)\), \((Q_2,Q_3)\) |
| \(5,\ldots,9\) | \((Q_0,Q_2)\), \((Q_1,Q_3)\) |
| \(10,\ldots,14\) | \((Q_0,Q_3)\), \((Q_1,Q_2)\) |

Fix three dropped systems \(D\) within one row, choose either paired union
\(S=Q_i\cup Q_j\), and restrict \(G_D\) to the blocks contained in \(S\).
The verifier reconstructs, rather than assumes, the following exact data:

- \(|S|=10\);
- 150 of its four-subsets lie in \(L_D\);
- every one of the \(\binom{10}{3}=120\) triples has exactly five extensions
  among those 150 blocks;
- the induced graph is 16-regular and has 1,200 edges.

For every triple \(T\subset S\), its five extensions are a \(K_5\).  In a
proper five-colouring that \(K_5\) uses all five colours, so one selected
triple-star may be assigned colours \(0,1,2,3,4\) without loss of generality.

The verifier then performs deterministic DSATUR backtracking.  At each node
it selects an uncoloured vertex of maximum saturation (breaking ties by
remaining degree and then row order), and tries **every** colour not already
used by a coloured neighbour.  Failed branches restore every changed
forbidden-colour mask.  Induction on the number of uncoloured vertices shows
that this enumerates every proper colouring extending the fixed root
\(K_5\); the root normalization covers every colouring up to a global colour
permutation.

All sixty checks (thirty drops times two paired ten-point sets) return
uncolourable.  Their deterministic search census is:

```text
total nodes: 96,980
minimum for one graph: 1,094
maximum for one graph: 3,323
```

If \(G_D\) had a five-colouring, its restriction to either induced
ten-point graph would be a five-colouring, contradicting this exhaustive
check.  Thus all thirty same-pack repairs are impossible.

## A useful invariant, not a symmetry quotient

For each five-set \(X\subset[20]\), count how many of its five four-subsets
belong to \(L_D\).  The resulting six-entry occupancy census is invariant
under point isomorphism.  Across the 455 drop triples it gives 130 distinct
signatures, with class-size census

```text
size 1: 71 signatures
size 2: 19
size 3: 4
size 4: 1
size 5: 10
size 10: 22
size 20: 3
```

Counting only full top \(K_5\)s (five-sets with all five blocks in the leave)
gives:

```text
4 tops: 405 cases
24 tops: 30 cases
29 tops: 20 cases
```

The thirty 24-top cases are exactly the same-pack cases eliminated above.
These occupancy signatures are search-prioritization invariants only.
Equal signatures do not prove two subcores isomorphic, and they must not be
used to discard a case.

## Reproduce

The verifier uses only the Python standard library:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/eh_core_symmetry_orbits/verify_eh_core_symmetry_orbits.py
```

Expected final lines:

```text
[exact] local DSATUR nodes: total=96980 min=1094 max=3323
[ok] deterministic local search node census matches
[scope] 30 of 455 EH drop-three repair cases are excluded; 425 remain.
[scope] This does not decide LS(3,4,20) and does not address #835 directly.
status: PASS
```

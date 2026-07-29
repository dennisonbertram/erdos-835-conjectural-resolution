# The exact local lemma for \(C(10,4,2)\)

Throughout, blocks are distinct \(4\)-subsets.  For a point \(x\), write
\(r_x\) for the number of blocks containing \(x\), and for two points
\(x,y\), write \(\lambda_{xy}\) for the number of blocks containing both.

## Theorem

1. \(C(10,4,2)=9\).
2. In every nine-block \(C(10,4,2)\), every point has degree \(3\) or \(4\).
   Consequently, exactly six points have degree \(4\) and four have degree
   \(3\).

Only one finite step below is computer-assisted: the exclusion of degree
\(5\) in a nine-block cover.  The source, search space, recursion, and complete
output are given explicitly.

## Eight blocks are impossible

Suppose first that eight blocks cover every pair.  Since one block through a
point covers only three of the nine pairs incident with that point,
\(r_x\geq 3\) for every \(x\).  On the other hand,

\[
\sum_x r_x=8\cdot 4=32.
\]

Thus the degree sequence is of one of the following two forms:

- one point has degree \(5\), and the other nine have degree \(3\); or
- two points have degree \(4\), and the other eight have degree \(3\).

If \(r_x=3\), then

\[
\sum_{y\ne x}\lambda_{xy}=3r_x=9.
\]

There are nine terms and every term is at least one, so
\(\lambda_{xy}=1\) for every \(y\ne x\).

In the first degree pattern, let \(a\) be the point of degree \(5\).  Every
other point has degree \(3\), hence \(\lambda_{ay}=1\) for all nine choices of
\(y\).  This gives

\[
\sum_{y\ne a}\lambda_{ay}=9,
\]

contrary to the same sum being \(3r_a=15\).

In the second pattern, let \(a,b\) be the two points of degree \(4\), and let
\(L\) be the other eight points.  Every pair incident with a point of \(L\)
has multiplicity one.  Therefore

\[
12=3r_a=\lambda_{ab}+\sum_{y\in L}\lambda_{ay}
          =\lambda_{ab}+8,
\]

so \(\lambda_{ab}=4\).  All four blocks through \(a\) consequently also
contain \(b\).  Write them as

\[
\{a,b\}\cup P_1,\ldots,\{a,b\}\cup P_4,
\]

where the \(P_i\) are pairs in \(L\).  Since every \(\lambda_{ay}=1\), the
four pairs \(P_i\) partition \(L\).

The remaining four blocks lie wholly in \(L\).  Every point of \(L\) occurs
once with \(a,b\), so it occurs exactly twice in these remaining blocks.
The four pairs \(P_i\) are already covered, while the other
\(\binom82-4=24\) pairs in \(L\) still have to be covered.  Four \(4\)-sets
have exactly \(4\binom42=24\) pair slots.  Hence all these slots must be used
without repetition, and two of the remaining blocks can intersect in at
most one point.

But, counting intersections of the four remaining blocks by points,

\[
\sum_{1\leq i<j\leq4}|B_i\cap B_j|
  =\sum_{y\in L}\binom{2}{2}=8,
\]

whereas pairwise intersections of size at most one make the left side at
most \(\binom42=6\).  This contradiction rules out eight blocks.  Any cover
with fewer than eight blocks could be enlarged to eight distinct blocks, so
it is ruled out as well.

For completeness, the following nine blocks do cover every pair:

```text
0 1 5 6
2 3 4 6
6 7 8 9
1 2 3 7
0 4 5 7
0 2 5 8
0 3 5 9
1 2 4 9
1 3 4 8
```

Its pair-multiplicity histogram is \(38\) pairs of multiplicity \(1\), six
of multiplicity \(2\), and one of multiplicity \(4\).  Thus all
\(\binom{10}{2}=45\) pairs occur.

Thus \(C(10,4,2)=9\).

## Degrees at least seven are impossible with nine blocks

Now let there be exactly nine blocks, and suppose a distinguished point
\(x\) has degree \(r\).  Delete \(x\).  The \(r\) blocks through \(x\) become
triples

\[
T_1,\ldots,T_r
\]

on the remaining nine-point set \(Y\), and their vertex-union is \(Y\).  The
other \(9-r\) blocks remain quadruples on \(Y\).

Let \(E_0\) be the set of pairs in \(Y\) that occur in none of the triples.
The triples cover at most \(3r\) distinct pairs, so

\[
|E_0|\geq \binom92-3r=36-3r.
\]

Every pair in \(E_0\) must be covered by the remaining \(9-r\) quadruples,
whose total pair capacity is \(6(9-r)\).  For \(r=7,8,9\), respectively, this
would require

\[
15\leq12,\qquad 12\leq6,\qquad 9\leq0.
\]

All are impossible.

## Degree six is impossible

Let \(r=6\).  The preceding lower bound and capacity bound are both \(18\).
Equality is therefore forced everywhere:

- the six triples have pairwise disjoint edge sets;
- \(|E_0|=18\); and
- the three remaining quadruples partition \(E_0\) into their edge sets.

For \(y\in Y\), let \(n_y\) be the number of triples containing \(y\), and
let \(m_y\) be the number of the three quadruples containing \(y\).  Because
the triples cover \(Y\), \(n_y\geq1\).  Pair-disjointness of the triples gives
\(2n_y\) triple-covered neighbors of \(y\), while edge-disjointness of the
quadruples gives \(3m_y\) uncovered neighbors.  Hence

\[
8-2n_y=3m_y.
\]

The only nonnegative integral solutions with \(n_y\geq1\) are

\[
(n_y,m_y)=(1,2)\quad\text{or}\quad(4,0).
\]

Since \(\sum_y n_y=6\cdot3=18\), exactly three points have \(n_y=4\) and the
other six have \(n_y=1\).  Call the former three points heavy.

For \(i=1,\ldots,6\), put \(k_i=|T_i\cap H|\), where \(H\) is the heavy
three-set.  Then

\[
\sum_i k_i=3\cdot4=12.
\]

The triple edge sets are disjoint, so a pair of heavy points occurs in at
most one triple.  Consequently,

\[
\sum_i\binom{k_i}{2}\leq\binom32=3.
\]

On the other hand, \(\binom{k}{2}\geq k-1\) for
\(k=0,1,2,3\), and hence

\[
\sum_i\binom{k_i}{2}
 \geq \sum_i(k_i-1)=12-6=6.
\]

This contradiction excludes degree \(6\).

## Degree five: complete finite certificate

It remains to exclude \(r=5\).  After deleting \(x\), its five incident
blocks are five distinct triples on \(Y\), their union is \(Y\), and the
other four blocks are quadruples.  Together those five triples and four
quadruples must cover all \(36\) edges of \(K_9\).

The verifier
[`check_c1042_degree5.cpp`](check_c1042_degree5.cpp) performs exactly the
following finite search.

1. It generates all \(\binom93=84\) triples and all
   \(\binom94=126\) quadruples on \(Y=\{0,\ldots,8\}\).
2. By \(S_9\)-symmetry it fixes one triple as \(\{0,1,2\}\).
3. It enumerates every unordered four-subset of the other \(83\) triples:

   \[
   \binom{83}{4}=1,837,620
   \]

   families.
4. It discards a family unless its five triples cover all nine vertices.
5. For each surviving family, it computes the exact set \(U\) of edges not
   covered by its triples and calls `cover_by_quads(U,4)`.

The recursive predicate is exhaustive by induction on its second argument.
If \(U\) is empty it succeeds.  If no quadruple remains, or
\(|U|>6s\), it fails.  Otherwise it chooses an edge \(e\in U\).  Every
quadruple cover of \(U\) must contain one of the \(126\) quadruples through
\(e\); the verifier tries every such quadruple \(Q\) and recurses on
\(U\setminus\binom Q2\) with \(s-1\).  Memoization stores only states already
proved impossible and therefore does not remove any possible cover.

The recursion even permits a quadruple to be used repeatedly and accepts a
cover using fewer than four quadruples.  It thus searches a superset of the
valid distinct-block completions.  Failure in this enlarged search is a
fortiori sufficient.

Reproduce with:

```bash
clang++ -std=c++20 -O3 -DNDEBUG \
  candidate_c12/check_c1042_degree5.cpp \
  -o /tmp/c12_degree5_verify
/tmp/c12_degree5_verify
```

The expected complete output is:

```text
VERIFIED UNSAT degree-5 case
triple_families 1837620
vertex_covering_families 411300
false_cache_1 2441
false_cache_2 594031
false_cache_3 2474296
false_cache_4 408420
```

The SHA-256 of the source used for these figures is
`16dfb23f2f215e020ed184d1ca96ada65d4cdb944dbc2ffad63b397060d4bf7c`.
On Apple clang 17.0.0, the full verification takes about seven seconds.

Therefore degree \(5\) is impossible.

## Degree distribution

Every point in a pair cover has degree at least \(3\), and the preceding
arguments show that every point in a nine-block cover has degree at most
\(4\).  If \(n_4\) points have degree \(4\), then

\[
36=\sum_x r_x=4n_4+3(10-n_4)=30+n_4.
\]

Thus \(n_4=6\), completing the theorem.

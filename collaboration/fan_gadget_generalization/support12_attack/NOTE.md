# Cyclic quotient support-12 attack

## Scope and current result

This directory studies squarefree trades in the cyclic \(C_{17}\) quotient.
It does not decide an exact cover, a fan, or Erdős--Rosenfeld Problem #835.

Q-balance gives the eleven partitions of six:
\[
6,\ 5+1,\ 4+2,\ 4+1+1,\ 3+3,\ 3+2+1,\ 3+1+1+1,\ 2+2+2,
\ 2+2+1+1,\ 2+1+1+1+1,\ 1^6.
\]
The verifier excludes all eleven complete partitions:
\[
\boxed{6,\quad5+1,\quad4+2,\quad3+3,\quad4+1+1,\quad
2+2+2,\quad3+1+1+1,\quad3+2+1,\quad2+2+1+1,\quad
2+1+1+1+1,\quad1^6.}
\]
Therefore every nonzero squarefree trade in this cyclic quotient has support
at least 14.

Each forcing verifier also checks explicitly that every single, double, or
triple/four target from which it selects a signed coordinate is nonzero.
The \(3+1+1+1\) verifier additionally checks the complete single-swap table
for cross-Q opposite pairs before using the fact that a zero two-move
residual cannot occur.  Thus these programs do not silently depend on a
separate smaller-support certificate to avoid an empty-vector branch.

## Direct signature and difference cases

- Case \(6\) compares all \(228\binom{13}{6}=391,248\) six-subsets
  within their Q-groups.  There are no equal TC-multiset signatures.
- Case \(5+1\) checks all
  \(228\binom{13}{5}\binom{8}{5}=16,432,416\) disjoint
  five-versus-five differences against the required single swap in another
  Q-group.  Exactly 14,211,626 satisfy the necessary unit coefficient
  bound, and none completes.
- Case \(4+2\) checks all 20,540,520 disjoint four-versus-four
  differences against the dictionary of 978,120 double swaps in another
  Q-group.  None completes.
- Case \(3+3\) checks all 7,824,960 disjoint triple-versus-triple
  differences against their opposites in another Q-group.  None completes.

## Exact \(4+1+1\) forcing

For each four-swap target \(t\), two single swaps \(u,v\), in distinct
Q-groups from each other and the four group, would satisfy \(u+v=t\).
At any nonzero target coordinate, at least one of \(u,v\) has the target
sign.  A signed-row index enumerates that move without loss; the other is
uniquely determined.

The final lookup uses a deterministic additive 64-bit fingerprint preceded
by a 24-bit membership table.  This is exact, not probabilistic: equal
vectors necessarily have equal fingerprints, while every full-fingerprint
collision is checked by exact sparse equality.  The twelve fixed ranges
exhaust 20,540,520 configurations, 2,893,266,152 forced-move probes, and
6,128,590 low-table hits.  There are no full-fingerprint hits.

`verify_partial.py` independently reconstructs the quotient columns,
checks their committed SHA-256 digest through the support-eight builder,
compiles the standard-library C++17 sources, checks every fixed range and
counter, and rejects any output drift.

## Exact \(2+2+2\) forcing

Fix the least of the three Q-groups and one of its 978,120 double swaps.
At a nonzero coordinate, at least one of the other two double swaps has the
opposite sign.  The signed-row index enumerates it; the third vector is
uniquely determined and is filtered by the same exact fingerprint method.
All three Q-groups are required to be distinct, and every full-hash hit
would be checked by exact sparse summation.

The twelve fixed ranges exhaust 978,120 outer double swaps,
1,823,898,120 forced probes, and 103,316,764 low-table hits.  There are no
full-hash hits.  Thus partition \(2+2+2\) is impossible.

## Exact \(3+1+1+1\) forcing

For every disjoint triple-versus-triple target, three single swaps must sum
to its negative.  Two signed-row forcing steps select the first two moves;
the final move is fingerprint-filtered and exact-checked, with all four
Q-groups required distinct.  The twelve ranges exhaust 7,824,960 triple
configurations, 1,102,759,494 first moves, 146,898,268,636 final probes,
and 311,205,246 low-table hits.  No full fingerprint hits occur.  Hence
partition \(3+1+1+1\) is impossible.

## Exact \(3+2+1\) forcing

At a nonzero coordinate of the triple target, either the double swap or
the single swap must carry the target sign.  Two signed posting lists
exhaust these alternatives.  In each branch the other vector is uniquely
fingerprinted and exact-checked, with all three Q-groups distinct.
The twelve ranges exhaust 7,824,960 triple configurations,
1,103,664,772 single probes, 59,641,423,270 double probes, 126,352,944
single low-table hits, and 62,515,800 double low-table hits.  There are no
full-hash hits.  Thus partition \(3+2+1\) is impossible.

## Exact \(2+2+1+1\) overlap forcing

Order the two double-swap Q-groups and fix the move \(a\) in the smaller
group.  If a second double swap \(b\) can be completed by two single swaps,
then \(a+b\) has support at most 16.  If \(I\) is the number of common
nonzero coordinates of \(a\) and \(b\), then
\[
 |\operatorname{supp}(a+b)|
 \geq |\operatorname{supp}(a)|+|\operatorname{supp}(b)|-2I.
\]
Consequently only posting-list pairs with
\[
 I\geq
 \left\lceil
 \frac{|\operatorname{supp}(a)|+|\operatorname{supp}(b)|-16}{2}
 \right\rceil
\]
can complete.  The verifier counts intersections exactly, then rejects
targets with support above 16 or coefficients outside \([-2,2]\).

For each remaining nonzero target, a signed coordinate forces at least one
of the two single swaps.  The other is uniquely fingerprinted; every
fingerprint match is checked by exact sparse equality and all four Q-groups
must be distinct.  The twelve ranges exhaust 978,120 outer double swaps,
120,799,660,300 posting hits, 410,224 overlap candidates, 12,432 bounded
targets, and 1,670,964 single probes.  There are no fingerprint hits.
Thus partition \(2+2+1+1\) is impossible.

## Exact \(2+1+1+1+1\) support-bounded forcing

Fix a double-swap target.  Four single swaps in distinct other Q-groups
would have to equal it.  At each nonzero residual coordinate at least one
remaining single has the residual sign.  After forcing the first single,
the residual must be a sum of three single swaps, so its coefficients have
magnitude at most three and its support is at most 24.  After forcing the
second, the corresponding bounds are two and 16.  These necessary bounds
reduce the final pair targets sharply.  A signed posting list then forces
one member of the last pair, and the other is fingerprinted and
exact-checked.

The twelve ranges exhaust 978,120 double targets, 138,202,888 first moves,
18,498,726,888 second moves, 62,550 support-bounded pair targets, and
8,446,888 final pair probes.  There are no full-fingerprint hits.  Thus
partition \(2+1+1+1+1\) is impossible.

## Exact \(1^6\) canonical forcing

Choose the unique least Q-group among the six and fix its oriented single
swap.  For a partial sum with \(r\) single swaps still unchosen, any
completion has coefficient magnitudes at most \(r\) and support at most
\(8r\).  At a nonzero coordinate, at least one remaining move has the
cancelling sign.  The verifier repeatedly uses that signed posting,
enforces the coefficient and support bounds for four, three, and two
remaining moves, and resolves the final pair by deterministic fingerprint
plus exact sparse equality.  All later Q-groups must be distinct and
strictly larger than the canonical least group where appropriate; all
representatives in a fingerprint bucket are retained.

The twelve ranges exhaust 35,568 canonical outer moves, 2,150,540 second
moves, 184,653,052 third moves, 708,486 support-bounded fourth moves, and
61,299,516 final pair probes.  There are no full-fingerprint hits.  Thus
partition \(1^6\) is impossible, completing the support-12 exclusion.

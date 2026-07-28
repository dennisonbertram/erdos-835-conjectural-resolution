# Exact three-layer full repair of the \(r=1\) dead prefix

Date: 2026-07-28.

## Result and scope

For the dead seven-prefix in `R1_DEAD_SEVEN_PREFIX.md`, define the
**full-completion repair distance** to be the least number of its seven
selected matching layers that must be replaced, on their same prescribed
supports, so that all seventeen prescribed supports have pairwise
edge-disjoint perfect matchings partitioning \(E(K_{13})\).

The exact distance is
\[
 \boxed{3}. \tag{1}
\]

This is different from the eighth-extension distance proved in
`R1_MINIMUM_LAYER_REPAIR.md`: one changed layer is enough to admit one
eighth matching, but three are necessary and sufficient to reach a full
seventeen-matching completion.

The result is exact for this one support instance and this one dead prefix.
It is not a universal three-layer switching theorem, a class-B completion
theorem, or a solution of Problem #835.

## The \(6:7\) cut lower bound

Let
\[
 C=\{0,\ldots,5\},\qquad O=\{6,\ldots,12\}.
\]
All seven original prefix matchings lie entirely inside
\(K_C\mathbin{\dot\cup}K_O\), so none uses an edge of the 42-edge cut
\(E(C,O)\).

For a support \(V\), every perfect matching on \(V\) uses at most
\[
 \min(|V\cap C|,|V\cap O|) \tag{2}
\]
cut edges.  The ten originally unselected supports have total upper
capacity
\[
 6\cdot4+(1+1+2+2)=30. \tag{3}
\]
Indeed, the six size-ten supports have split \(6:4\), two size-eight
supports have split \(1:7\), and two have split \(2:6\).

Among the seven selected supports, the unique size-twelve support has cut
capacity six and each other support has cut capacity four.  Consequently,
after changing at most two selected layers, all non-fixed layers together
can cover at most
\[
 30+6+4=40<42 \tag{4}
\]
cut edges.  The retained original layers cover none.  A full completion
would have to cover every edge of \(E(C,O)\), so (4) is impossible.
Therefore the full-completion repair distance is at least three.

## A three-layer completion

Change selected colours \(0,1,2\), retain selected colours \(3,4,5,6\)
verbatim, and use the following seventeen matchings in support order:

\[
\begin{array}{c|l}
0&0\,12,\ 1\,11,\ 2\,10,\ 3\,9,\ 4\,8,\ 5\,7\\
1&2\,12,\ 3\,11,\ 4\,10,\ 5\,9\\
2&0\,11,\ 2\,9,\ 4\,7,\ 5\,12\\
3&0\,4,\ 1\,3,\ 6\,12,\ 7\,11,\ 8\,10\\
4&1\,5,\ 2\,4,\ 8\,12,\ 9\,11\\
5&0\,1,\ 3\,5,\ 7\,8,\ 10\,12\\
6&0\,3,\ 1\,2,\ 6\,11,\ 7\,10,\ 8\,9\\
7&0\,10,\ 1\,12,\ 2\,11,\ 3\,6,\ 4\,5\\
8&0\,9,\ 1\,8,\ 2\,5,\ 3\,12,\ 4\,6\\
9&0\,7,\ 1\,9,\ 2\,6,\ 3\,4,\ 5\,11\\
10&0\,6,\ 1\,4,\ 2\,8,\ 3\,7,\ 5\,10\\
11&0\,5,\ 1\,6,\ 2\,3,\ 4\,11,\ 9\,10\\
12&0\,2,\ 1\,7,\ 3\,8,\ 4\,12,\ 5\,6\\
13&0\,8,\ 6\,10,\ 7\,9,\ 11\,12\\
14&1\,10,\ 6\,9,\ 7\,12,\ 8\,11\\
15&2\,7,\ 3\,10,\ 6\,8,\ 9\,12\\
16&4\,9,\ 5\,8,\ 6\,7,\ 10\,11
\end{array} \tag{5}
\]

Every row of (5) is a perfect matching on its prescribed support, colours
\(3,4,5,6\) equal their original selected matchings, and the 78 displayed
edges partition \(E(K_{13})\).  Hence the distance is at most three.
Together with (4), this proves (1).

## Verification

`verify_r1_minimum_full_repair.py` is a standard-library replay.  It
reconstructs the exact support instance and prefix, checks the \(6:7\) cut
and all capacity values in (3)--(4), and verifies every endpoint and edge
of the literal completion (5).

`search_r1_minimum_full_repair.py` records the CP-SAT discovery search.  It
is not needed for the proof.

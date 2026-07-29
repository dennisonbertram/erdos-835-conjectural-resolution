# A dead but fully completable \(r=5\) seven-prefix

Date: 2026-07-28.

## Result and scope

There is a class-B-prime support instance on thirteen target vertices with
profile
\[
(n_8,n_{10},n_{12})=(12,0,5)
\]
and a pairwise edge-disjoint seven-prefix of type
\[
8^4\,12^3
\]
such that none of the ten remaining prescribed supports has a perfect
matching avoiding the prefix.  In particular, all eight remaining
size-eight supports and both remaining size-twelve supports are blocked.

The same support matrix has a different full 17-matching edge partition of
\(K_{13}\).  It also comes from a proper saturated 17-colouring of
\(K_{18}-E(K_{13})\), so it is class B-prime rather than merely abstract
class B.

Thus “every valid seven-prefix extends to an eighth matching” is false at
\(r=5\), even in a completable class-B-prime instance.  This is not a
noncompletable support instance, does not test fan realizability, and does
not resolve Erdős--Rosenfeld Problem #835.  Any universal proof must
coordinate or switch the earlier matching choices.

## The dead seven-prefix

On \(V=\{0,\ldots,12\}\), take
\[
\begin{array}{c|l}
0&02,\ 36,\ 47,\ 8\,10\\
1&07,\ 13,\ 26,\ 8\,11\\
2&06,\ 14,\ 27,\ 89\\
3&04,\ 16,\ 23,\ 9\,12\\
4&01,\ 24,\ 37,\ 56,\ 8\,12,\ 10\,11\\
5&03,\ 17,\ 25,\ 46,\ 9\,11,\ 10\,12\\
6&12,\ 34,\ 58,\ 67,\ 9\,10,\ 11\,12 .
\end{array} \tag{1}
\]
These are matchings of sizes \(4,4,4,4,6,6,6\); their 34 edges are
distinct.

The selected complements, obtained directly from their endpoints, are
\[
\begin{array}{c|l}
0&1,5,9,11,12\\
1&4,5,9,10,12\\
2&3,5,10,11,12\\
3&5,7,8,10,11\\
4&9\\
5&8\\
6&0 .
\end{array} \tag{2}
\]
Use the following ten complements for the remaining supports:
\[
\begin{array}{c|l}
7&0,1,2,3,4\\
8&0,2,3,4,6\\
9&1,2,3,4,6\\
10&0,2,3,5,7\\
11&0,1,4,6,7\\
12&6,7,8,9,11\\
13&1,7,8,10,11\\
14&2,6,9,10,12\\
15&8\\
16&12 .
\end{array} \tag{3}
\]

There are twelve complement five-sets and five singleton complements.
Every vertex occurs in exactly five of the seventeen complements, hence
belongs to exactly twelve supports.  Equivalently, if \(F\) is the union
of (1), the ten rows in (3) satisfy the exact identity
\[
\#\{\text{remaining complements containing }v\}=d_F(v)-2. \tag{4}
\]
Thus (2)--(3) are a target-order class-B support matrix of the claimed
profile.

## Ten explicit Tutte barriers

Let \(H=K_{13}-F\).  For each remaining support \(S_i\), the table gives a
separator \(Z_i\).  Every vertex of \(S_i-Z_i\) is an isolated component
of \(H[S_i-Z_i]\).

\[
\begin{array}{c|c|c|c}
i&V\setminus S_i&Z_i&S_i\setminus Z_i\\ \hline
7&01234&567&8,9,10,11,12\\
8&02346&1,5,7&8,9,10,11,12\\
9&12346&0,5,7&8,9,10,11,12\\
10&02357&1,4,6&8,9,10,11,12\\
11&01467&2,3,5&8,9,10,11,12\\
12&6,7,8,9,11&5,10,12&0,1,2,3,4\\
13&1,7,8,10,11&5,9,12&0,2,3,4,6\\
14&2,6,9,10,12&5,8,11&0,1,3,4,7\\
15&8&5,9,10,11,12&0,1,2,3,4,6,7\\
16&12&5,8,9,10,11&0,1,2,3,4,6,7 .
\end{array} \tag{5}
\]

For rows \(7\)--\(14\), deleting three vertices leaves five odd
components; for rows \(15\)--\(16\), deleting five vertices leaves seven
odd components.  In every case
\[
o\bigl(H[S_i]-Z_i\bigr)>|Z_i|.
\]
Tutte's theorem therefore blocks a perfect matching on every one of the
ten remaining supports.  This proves that (1) is a dead seven-prefix.

## Why the support instance is nevertheless complete

`verify_r5_dead_seven_prefix.py` contains a literal different family of
seventeen support-perfect matchings.  Their endpoints equal the ordered
supports (2)--(3), their edge sets are pairwise disjoint, and their
\[
4\cdot4+8\cdot4+5\cdot6=78
\]
edges are exactly \(E(K_{13})\).  Hence the support instance is fully
completable; only the particular prefix (1) is dead.

The same verifier contains a literal partial-factorization certificate:
a \(13\times5\) array colouring every target-to-outside edge and colours
for all ten edges of the outside \(K_5\).  At each target vertex the five
cross-edge colours are exactly the five colours missing from its support.
At each outside vertex the thirteen cross edges and four internal edges
use all seventeen colours once.  This is a proper saturated colouring of
\(K_{18}-E(K_{13})\), proving class-B-prime realizability.

No simultaneous thirteen-fan certificate is asserted.

## Discovery and independent verification

`search_r5_dead_seven_prefix.py` is the CP-SAT/CEGAR discovery helper.  In
the recorded feasibility-first run it rejected 229 candidates and added
50,363 literal perfect-matching cuts before finding (1)--(3) on round
230.  Separate exact models found the full completion in 0.026 seconds
and the partial-factorization realization in under one second.  These
search timings and statuses are discovery telemetry, not the proof.

`verify_r5_dead_seven_prefix.py` is dependency-free and uses only the
Python standard library.  It reconstructs the class-B arithmetic,
replays all ten explicit Tutte barriers, independently exhausts the
perfect-matching recursion, checks the literal full edge partition, and
checks the saturated partial \(K_{18}\) factorization.  Its complete run
takes approximately 0.05 seconds on the discovery machine.

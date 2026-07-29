# An exact \(r=2\) obstruction to the fixed six-prefix route

Date: 2026-07-28.

## Result and exact scope

There is a target class-B support instance of profile
\[
(n_8,n_{10},n_{12})=(9,6,2)
\]
with a legitimate complement-cover six-packing of types
\[
8^4\,10^2
\]
whose residual graph has no perfect matching on **any** of the four
remaining size-ten supports.

Consequently, a proof of coordinated nine for \(r=2\) cannot take an
arbitrary complement-cover six-prefix and always append the two unused
size-twelve colours and one unused size-ten colour.  The certificate does
not disprove coordinated nine: one may choose a different six-prefix, or
append one of the five remaining size-eight colours instead.

## The six-prefix

Use vertex set \(\{0,\ldots,12\}\), and put
\[
A=\{0,\ldots,6\},\qquad
C=\{2,\ldots,6\},\qquad
B=\{7,\ldots,12\}.
\]
Take the following six pairwise edge-disjoint matchings.  The complement
listed after each matching is the set of vertices it misses.

\[
\begin{array}{c|l|l}
&\text{matching}&\text{support complement}\\ \hline
M_0&7\,11,\ 9\,12,\ 2\,6,\ 4\,5&\{0,1,3,8,10\}\\
M_1&8\,9,\ 10\,12,\ 3\,5,\ 4\,6&\{0,1,2,7,11\}\\
M_2&7\,8,\ 10\,11,\ 2\,4,\ 5\,6&\{0,1,3,9,12\}\\
M_3&7\,9,\ 8\,10,\ 11\,12,\ 3\,4&\{0,1,2,5,6\}\\
M_4&7\,10,\ 8\,12,\ 9\,11,\ 2\,3,\ 0\,1&\{4,5,6\}\\
M_5&7\,12,\ 8\,11,\ 9\,10,\ 2\,5,\ 3\,6&\{0,1,4\}.
\end{array} \tag{1}
\]

Their complements cover all thirteen vertices.  Their union is exactly
\[
D=K_6[B]\ \mathbin{\dot\cup}\ K_5[C]\ \mathbin{\dot\cup}\ K_2[\{0,1\}].
\tag{2}
\]
Thus
\[
|E(D)|=15+10+1=26,\qquad
(d_D(v):v=0,\ldots,12)=(1,1,4,4,4,4,4,5,5,5,5,5,5),
\tag{3}
\]
and in particular \(\Delta(D)=5\), exactly as required by the
complement-cover construction.

## Completing the class-B support inventory

Add the following five size-five complements:
\[
\begin{split}
&\{8,9,10,11,12\},\quad
\{7,9,10,11,12\},\quad
\{7,8,10,11,12\},\\
&\{7,8,9,11,12\},\quad
\{6,7,8,9,10\},
\end{split} \tag{4}
\]
the following four size-three complements:
\[
\{3,5,6\},\quad
\{2,4,6\},\quad
\{2,3,5\},\quad
\{2,3,4\},
\tag{5}
\]
and the two singleton complements
\[
\{4\},\qquad\{5\}. \tag{6}
\]

Together with the six complements in (1), these are nine five-sets, six
triples, and two singletons.  Every vertex occurs in exactly five of the
seventeen complements.  Equivalently, every vertex belongs to exactly
twelve supports, so this is a target class-B \(r=2\) instance.

The residual complement-incidence identity is visible directly from
(3): after the six-prefix, the remaining complement multiplicities are
\[
\rho(v)=d_D(v)-1=(0,0,3,3,3,3,3,4,4,4,4,4,4). \tag{7}
\]
The sets in (4)--(6) realize exactly these row sums.

## Why all four remaining size-ten colours are blocked

Let
\[
H=K_{13}-D.
\]
By (2), \(B\) is an independent six-set in \(H\).  Each triple \(T\) in
(5) is contained in \(C\subset A\).  Hence its size-ten support
\[
Y=V(K_{13})\setminus T
\]
contains every vertex of \(B\), but only \(7-3=4\) vertices of \(A\).

In any matching of \(H[Y]\), every vertex of \(B\) must be paired with a
different vertex of \(A\cap Y\), because \(H[B]\) has no edges.  Six
vertices of \(B\) cannot be injected into the four vertices of
\(A\cap Y\).  Thus \(H[Y]\) has no perfect matching for every one of the
four triples in (5).

This failure occurs before either size-twelve matching is selected.
Therefore no choice of the two prescribed near-perfect matchings can
repair this particular route.

## An instance-specific nine-packing

The same six-prefix does extend to nine if one uses a remaining
size-eight colour instead of a size-ten colour.  Take the size-eight
support with complement
\[
\{6,7,8,9,10\}
\]
and the following perfect matching on it:
\[
N_8=\{0\,5,\ 1\,4,\ 2\,11,\ 3\,12\}. \tag{8}
\]
For the size-twelve supports missing \(4\) and \(5\), respectively, take
\[
\begin{split}
N_{12}^{(4)}
 &=\{0\,12,\ 1\,10,\ 2\,9,\ 3\,7,\ 5\,8,\ 6\,11\},\\
N_{12}^{(5)}
 &=\{0\,8,\ 1\,11,\ 2\,7,\ 3\,9,\ 4\,10,\ 6\,12\}.
\end{split} \tag{9}
\]
The three matchings in (8)--(9) are pairwise edge-disjoint and avoid
every edge in \(D\).  Appending them to (1) therefore gives a literal
nine-packing of support-size pattern
\[
8^5\,10^2\,12^2. \tag{10}
\]

This is an exact repair of the displayed instance, not a universal
\(r=2\) theorem.  Its structural lesson is only that a prospective
universal argument must retain the five unused size-eight supports as a
terminal choice; the four size-ten supports alone can all be dead.

## Verification

Run:

```sh
python3 collaboration/coordinated_nine_r2_obstruction/verify_obstruction.py
```

The verifier uses only the Python standard library.  It checks the six
matchings and their supports, reconstructs (2), verifies the exact
class-B column and row data, and exhaustively confirms the absence of a
perfect matching on each of the four residual size-ten supports.  It
also verifies every support and edge-disjointness condition in the
explicit nine-packing (8)--(10).

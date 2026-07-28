# An exact \(r=2\) obstruction to an arbitrary size-ten terminal choice

Date: 2026-07-28.

## Result and exact scope

There is a target class-B \(r=2\) instance with a legitimate
complement-cover six-prefix, a remaining size-ten support, and a perfect
matching \(M\) on that support such that the residual graph after \(M\)
does not contain two edge-disjoint near-perfect matchings with the two
prescribed singleton omissions.

This refutes an arbitrary-first-matching lemma on the size-ten side.  It
does not refute coordinated nine: one may choose another remaining
support or another matching on the displayed support.

## Literal class-B certificate

Take the six prefix matchings
\[
\begin{array}{c|l|l}
&\text{matching}&\text{support complement}\\ \hline
D_0&7\,10,\ 0\,3,\ 1\,4,\ 2\,6&\{5,8,9,11,12\}\\
D_1&3\,4,\ 0\,5,\ 1\,6,\ 8\,10&\{2,7,9,11,12\}\\
D_2&1\,2,\ 3\,5,\ 11\,12,\ 7\,8&\{0,4,6,9,10\}\\
D_3&0\,4,\ 7\,9,\ 2\,5,\ 3\,6&\{1,8,10,11,12\}\\
D_4&2\,4,\ 1\,5,\ 8\,12,\ 0\,6,\ 7\,11&\{3,9,10\}\\
D_5&4\,6,\ 5\,7,\ 0\,2,\ 1\,3,\ 8\,11&\{9,10,12\}.
\end{array} \tag{1}
\]
Their complements cover all thirteen vertices.  Their edge union \(D\)
has 26 edges and degree sequence
\[
(5,5,5,5,5,5,5,5,4,1,2,3,2),\qquad \Delta(D)=5. \tag{2}
\]

Use the remaining five-set complements
\[
\begin{split}
&\{4,5,6,7,8\},\quad
\{3,5,6,7,8\},\quad
\{3,4,5,6,7\},\\
&\{2,3,4,5,6\},\quad
\{0,1,2,3,4\},
\end{split} \tag{3}
\]
the four triples
\[
\{10,11,12\},\quad
\{0,1,11\},\quad
\{0,1,2\},\quad
\{0,1,2\}, \tag{4}
\]
and singleton complements
\[
\{7\},\qquad\{8\}. \tag{5}
\]
Together with (1), these have the class-B \(r=2\) profile
\(5^9\,3^6\,1^2\), and every vertex occurs in exactly five complements.

## The forced common edge

Put \(G=K_{13}-D\).  On the size-ten support complementary to
\(\{10,11,12\}\), take
\[
M=\{0\,1,\ 2\,3,\ 4\,5,\ 6\,7,\ 8\,9\}. \tag{6}
\]
These five edges belong to \(G\).  Let
\[
Q=G-M,\qquad U=\{0,\ldots,6\}.
\]
A direct inspection of (1) and (6) gives
\[
E(Q[U])=\{5\,6\}. \tag{7}
\]

After deleting either prescribed hole \(7\) or \(8\), only five vertices
remain outside the seven-set \(U\).  Any perfect matching must therefore
use an edge within \(U\); by (7), it must use \(5\,6\).  Thus every
near-perfect matching missing \(7\), and every one missing \(8\), uses
the same edge \(5\,6\).  No two such matchings are edge-disjoint.

The obstruction is attached to the particular matching (6), not merely
to its support.

## Verification

Run:

```sh
python3 collaboration/r2_size10_terminal_obstruction/verify_obstruction.py
```

The standard-library verifier reconstructs the six-prefix and class-B
rows, verifies (6)--(7), enumerates all near-perfect matchings with each
prescribed omission, and confirms that every cross-pair shares an edge.

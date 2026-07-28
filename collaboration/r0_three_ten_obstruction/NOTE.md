# A sharp obstruction to three further size-ten colours in \(r=0\)

Date: 2026-07-28.

## Result

Consider an \(r=0\) class-B support family on \(K_{13}\).  Suppose a
packed six-prefix has support profile
\[
 8^3\,10^3
\]
and its six support complements cover all thirteen vertices.  If \(D\)
is the union of the six matchings, then \(\Delta(D)\le5\).

Exactly the following statement is universally true:

> **Sharp extension theorem.**  At least two of the seven remaining
> size-ten supports have a perfect matching in \(K_{13}-D\).

The number two is best possible.  An explicit valid class-B instance and
packed complement-cover six-prefix below have five blocked remaining
size-ten supports and only two individually extendible ones.

Consequently, the six-prefix theorem in
`../r0_complement_cover_six/NOTE.md` cannot by itself reach coordinated
nine by appending three size-ten colours.  This does **not** disprove
coordinated nine: one may choose a different six-prefix or use one of the
four remaining size-eight colours.

## Why at least two size-ten supports extend

There remain four five-set complements and seven triple complements.
For a vertex \(v\), let \(\rho(v)\) be its multiplicity in these eleven
remaining complements.  Since every vertex has total complement
multiplicity five and the selected matching union has degree
\(d_D(v)\),
\[
 \rho(v)=d_D(v)-1. \tag{1}
\]
In particular, the remaining complements have total size
\[
 4\cdot5+7\cdot3=41. \tag{2}
\]

Let \(Y\) be a remaining size-ten support and suppose
\((K_{13}-D)[Y]\) has no perfect matching.  Coarsening a Tutte barrier
into exactly \(s+2\) odd blocks gives a complete multipartite core in
\(D[Y]\).  Under \(\Delta(D)\le5\), the order-ten odd-partition catalogue
leaves only
\[
 K_{5,5}\quad\text{or}\quad K_6. \tag{3}
\]
Indeed, the other coarsened cores have maximum degree at least six.

A \(K_{5,5}\) core is impossible here.  All ten core vertices have
\(D\)-degree five, so (1) requires forty remaining-complement incidences
on \(Y\).  But the triple \(V(K_{13})\setminus Y\) contributes none
there, and all other remaining complements have total size
\[
 41-3=38<40. \tag{4}
\]

Thus every blocked support contains a \(K_6\) in \(D\).  The six vertices
of such a clique already have degree five, so the clique is a connected
component of \(D\).  Since \(|E(D)|=27<30\), there is at most one such
component; call it \(C\).  Hence every blocked support contains the same
six-set \(C\), and its complementary triple avoids \(C\).

If \(t\) of the seven size-ten supports are blocked, then every
\(v\in C\) has \(\rho(v)=4\), requiring twenty-four remaining-complement
incidences on \(C\).  The \(t\) blocked triples contribute zero, while
all other remaining complements have total capacity
\[
 4\cdot5+(7-t)\cdot3=41-3t. \tag{5}
\]
Thus \(41-3t\ge24\), so \(t\le5\).  At least two supports extend.

## A sharp thirteen-vertex example

Write
\[
 C=\{c_0,\ldots,c_5\},\qquad O=\{o_0,\ldots,o_6\}.
\]
The following six rows are pairwise edge-disjoint matchings.  The first
three have five edges and hence support size ten; the last three have
four edges and hence support size eight.

\[
\begin{array}{c|c|c}
&\text{edges in }C&\text{edges in }O\\ \hline
M_0&05,\ 14,\ 23&25,\ 34\\
M_1&04,\ 35,\ 12&36,\ 45\\
M_2&03,\ 24,\ 15&04,\ 56\\
M_3&13,\ 45&15,\ 06\\
M_4&01,\ 25&26,\ 01\\
M_5&02,\ 34&03,\ 12
\end{array} \tag{6}
\]
Here \(ij\) in the middle column means \(c_ic_j\), while \(ij\) in the
last column means \(o_io_j\).  The \(C\)-edges in (6) partition
\(E(K_C)\).  Let \(D=\bigcup_{i=0}^5M_i\).

The three selected triple complements, computed from the endpoints of
\(M_0,M_1,M_2\), are
\[
 016,\qquad012,\qquad123 \quad\text{inside }O. \tag{7}
\]
The three selected five-set complements are
\[
\begin{aligned}
 &\{c_0,c_2,o_2,o_3,o_4\},\\
 &\{c_3,c_4,o_3,o_4,o_5\},\\
 &\{c_1,c_5,o_4,o_5,o_6\}.
\end{aligned} \tag{8}
\]
These six complements cover all thirteen vertices.

Complete the seven five-set complements by adding
\[
 C\setminus\{c_0\},\quad
 C\setminus\{c_1\},\quad
 C\setminus\{c_2\},\quad
 C\setminus\{c_3\}. \tag{9}
\]
Complete the ten triple complements by adding the five triples
\[
 013,\quad124,\quad256,\quad356,\quad456
 \quad\text{inside }O, \tag{10}
\]
and the two triples
\[
 \{c_0,c_1,o_0\},\qquad
 \{c_2,c_3,o_0\}. \tag{11}
\]
All seven five-sets and all ten triples are distinct.  Direct incidence
counting gives complement multiplicity five at every vertex, so this is
a valid \(r=0\) class-B support family.

Since (6) contains every edge of \(K_C\), the residual graph has no edge
inside \(C\).  Each of the five triples in (10) is contained in \(O\);
its complementary size-ten support therefore contains all six vertices
of \(C\) but only four vertices of \(O\).  A perfect matching would have
to match all six vertices of \(C\) to those four outside vertices, which
is impossible.  Thus all five supports are blocked.

The two supports complementary to (11) do extend.  For example, the
following residual perfect matchings certify this:
\[
\begin{aligned}
V\setminus\{c_0,c_1,o_0\}:&
\quad c_2o_1,\ c_3o_2,\ c_4o_3,\ c_5o_5,\ o_4o_6,\\
V\setminus\{c_2,c_3,o_0\}:&
\quad c_0o_1,\ c_1o_2,\ c_4o_3,\ c_5o_5,\ o_4o_6.
\end{aligned} \tag{12}
\]
Hence exactly five of the seven remaining size-ten supports are blocked,
attaining the universal upper bound.

## A forced-edge near-factor shortcut is also false

One might try to convert a perfect matching on
\(V\setminus T\) into a near-perfect matching by adjoining an edge inside
the omitted triple \(T\), then invoke the prescribed three-near-factor
theorem.  The sharp example already rules out the required ambient
forced-edge strengthening.

Take the blocked triple
\[
 T=\{o_0,o_1,o_3\}.
\]
The edge \(o_1o_3\) does not occur in (6), so it belongs to the residual
graph \(K_{13}-D\).  If that graph had a near-perfect matching missing
\(o_0\) and containing \(o_1o_3\), deleting \(o_1o_3\) would leave a
perfect matching on \(V\setminus T\).  The latter support is blocked.
Thus even one forced internal edge need not extend at minimum degree seven.

This does not preclude using the same conversion after first selecting an
individually extendible triple.  It does show that the existing arbitrary-hole
three-near-factor theorem cannot be strengthened by adding arbitrary forced
edges without additional hypotheses.

## Verification and strict frontier

Run:

```sh
python3 collaboration/r0_three_ten_obstruction/verify_obstruction.py
```

The standard-library verifier reconstructs all seventeen complements and
six matchings, checks the class-B row and column data, verifies the cover
and edge-disjointness, exhaustively confirms the five matching
obstructions, checks the two witnesses in (12), and verifies the
forced-edge delimiter.

This note refutes only the strategy “take an arbitrary complement-cover
\(8^3 10^3\) six-prefix and append three size-ten colours.”  A coordinated
ninth theorem for \(r=0\), a full class-B completion theorem, and
Erdős--Rosenfeld Problem #835 all remain open.

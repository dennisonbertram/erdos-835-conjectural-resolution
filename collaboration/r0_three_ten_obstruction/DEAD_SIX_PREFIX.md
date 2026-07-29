# A complement-cover six-prefix with only two extendible colours

Date: 2026-07-28.

## Exact result

There is an \(r=0\) class-B support instance and a packed
complement-cover six-prefix of type
\[
 8^3\,10^3
\]
for which exactly two of the eleven remaining colours have an
individually available perfect matching.  The other four size-eight and
five size-ten colours are all blocked.

Thus the complement-cover six-prefix theorem cannot be promoted to
coordinated nine by extending an arbitrary prefix, even if the four
remaining size-eight colours are retained as choices.  Any universal
\(r=0\) ninth-matching argument must backtrack or switch the six-prefix
itself.

This is a dead-prefix certificate, not a counterexample to coordinated
nine for the full support instance.

## The six selected matchings

Partition the vertices as
\[
 C=\{c_0,\ldots,c_5\},\qquad O=\{o_0,\ldots,o_6\}.
\]
Take the following six pairwise edge-disjoint matchings:
\[
\begin{array}{c|c|c}
&\text{edges in }C&\text{edges in }O\\ \hline
M_0&05,\ 14,\ 23&03,\ 15\\
M_1&04,\ 35,\ 12&04,\ 26\\
M_2&03,\ 24,\ 15&05,\ 36\\
M_3&13,\ 45&06,\ 45\\
M_4&01,\ 25&34,\ 56\\
M_5&02,\ 34&35,\ 46
\end{array} \tag{1}
\]
As before, the middle column uses \(c\)-labels and the last column uses
\(o\)-labels.  The first three rows have five edges and support size ten;
the last three have four edges and support size eight.

The edges in the middle column partition \(E(K_C)\).  On \(O\), the
twelve selected edges form a graph \(J\).  Its residual complement
\[
 R=K_O-J \tag{2}
\]
has edge set
\[
\begin{aligned}
E(R)=\{&
01,02,12,13,14,16,\\
&23,24,25\}.
\end{aligned} \tag{3}
\]
Every edge in (3) is incident to \(o_1\) or \(o_2\), while
\(o_1o_6,o_2o_5\in E(R)\).  Hence
\[
 \nu(R)=2. \tag{4}
\]

The three selected triple complements are
\[
 246,\qquad135,\qquad124
 \quad\text{inside }O, \tag{5}
\]
and the three selected five-set complements are
\[
\begin{aligned}
 &\{c_0,c_2,o_1,o_2,o_3\},\\
 &\{c_3,c_4,o_0,o_1,o_2\},\\
 &\{c_1,c_5,o_0,o_1,o_2\}.
\end{aligned} \tag{6}
\]
These six complements cover all thirteen vertices, equivalently the
matching union in (1) has maximum degree five.

## Completing the class-B support family

Add the four five-set complements
\[
 C\setminus\{c_0\},\quad
 C\setminus\{c_1\},\quad
 C\setminus\{c_2\},\quad
 C\setminus\{c_3\}. \tag{7}
\]
Add the five triples
\[
 056,\qquad345,\qquad346,\qquad356,\qquad456
 \quad\text{inside }O, \tag{8}
\]
and the two triples
\[
 \{c_0,c_1,o_0\},\qquad
 \{c_2,c_3,o_0\}. \tag{9}
\]

The seven five-sets and ten triples are all distinct.  Every vertex
occurs in exactly five of the seventeen complements:

* every \(c_i\) has selected-complement multiplicity one and
  remaining-complement multiplicity four;
* the degrees of \(o_0,\ldots,o_6\) in \(J\) are
  \[
  4,1,1,4,4,5,5,
  \]
  so their selected-complement multiplicities are
  \(2,5,5,2,2,1,1\), while (8)--(9) give the complementary remaining
  multiplicities \(3,0,0,3,3,4,4\).

This is therefore a valid \(r=0\) class-B support instance.

## Nine of the eleven remaining colours are blocked

The four size-eight supports complementary to (7) are
\[
 O\cup\{c_0\},\quad O\cup\{c_1\},\quad
 O\cup\{c_2\},\quad O\cup\{c_3\}. \tag{10}
\]
The residual graph has no edge inside \(C\).  A perfect matching on any
support in (10) would use one edge from its sole \(C\)-vertex to \(O\)
and then require a three-edge matching in \(R\) on the remaining six
vertices of \(O\).  This contradicts (4).  Hence all four size-eight
colours are blocked.

Every triple in (8) lies inside \(O\), so its complementary size-ten
support contains all six vertices of \(C\) but only four vertices of
\(O\).  Since the residual graph has no edge inside \(C\), all five of
these size-ten colours are blocked.

The two size-ten supports complementary to (9) do extend.  Explicit
residual perfect matchings are
\[
\begin{aligned}
V\setminus\{c_0,c_1,o_0\}:&
\quad o_1o_6,\ c_2o_2,\ c_3o_3,\ c_4o_4,\ c_5o_5,\\
V\setminus\{c_2,c_3,o_0\}:&
\quad o_2o_5,\ c_0o_1,\ c_1o_3,\ c_4o_4,\ c_5o_6.
\end{aligned} \tag{11}
\]
Thus exactly two remaining colours are individually extendible.

## Verification and scope

Run:

```sh
python3 collaboration/r0_three_ten_obstruction/verify_dead_six_prefix.py
```

The verifier reconstructs the six matchings and all seventeen
complements, checks every row and column sum, confirms the complement
cover, computes \(\nu(R)=2\), exhaustively tests all eleven residual
supports, and verifies (11).

The earlier `NOTE.md` proves the sharp universal statement that at least
two remaining size-ten colours always extend individually.  The present
example simultaneously attains that lower bound and blocks all four
remaining size-eight colours.  In fact,
`FULL_COMPLETION_WITNESS.md` gives a different matching choice for the
same supports that completes all seventeen colours.  The obstruction is
therefore exactly a dead-prefix phenomenon.

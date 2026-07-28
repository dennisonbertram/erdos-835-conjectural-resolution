# A K6-free obstruction to coordinating three remaining size-ten colours

Date: 2026-07-28.

## Exact result

The individual-extension theorem in `K6_PREFIX_SWITCH.md` cannot be
upgraded to a three-colour coordination theorem from the same invariant.
There is a valid \(r=0\) class-B support instance and a packed
complement-cover six-prefix of profile
\[
 10^3\,8^3
\]
whose edge union \(D\)

1. has \(\Delta(D)=5\);
2. contains no \(K_6\);
3. leaves every one of the seven remaining size-ten supports individually
   matchable; but
4. leaves no three of those seven supports with pairwise edge-disjoint
   perfect matchings.

Thus eliminating the saturated-\(K_6\) blocker is not enough to append
three size-ten colours.  This is a delimiter for that particular route,
not a counterexample to coordinated nine: a different six-prefix, a
larger support-preserving trade, or some of the four remaining size-eight
colours may still work.

## The six-prefix

Write
\[
 C=\{c_0,\ldots,c_5\},\qquad O=\{o_0,\ldots,o_6\}.
\]
The following rows are pairwise edge-disjoint matchings.  An entry \(ij\)
in the middle column denotes \(c_ic_j\), and one in the last column
denotes \(o_io_j\).

\[
\begin{array}{c|c|c}
 &E(C)&E(O)\\ \hline
M_0&14,\ 23&02,\ 13,\ 45\\
M_1&04,\ 35,\ 12&05,\ 12\\
M_2&03,\ 24,\ 15&06,\ 23\\
M_3&02,\ 45&16,\ 24\\
M_4&25,\ 34&34,\ 56\\
M_5&05,\ 13&35,\ 46
\end{array} \tag{1}
\]

The first three rows have five edges and the last three have four.  Their
six support complements are
\[
\begin{aligned}
&\{c_0,c_5,o_6\},\quad
  \{o_3,o_4,o_6\},\quad
  \{o_1,o_4,o_5\},\\
&\{c_1,c_3,o_0,o_3,o_5\},\\
&\{c_0,c_1,o_0,o_1,o_2\},\\
&\{c_2,c_4,o_0,o_1,o_2\}.
\end{aligned} \tag{2}
\]
They cover all thirteen vertices.

Inside \(C\), the rows in (1) partition
\[
 E(K_C)\setminus\{c_0c_1\}. \tag{3}
\]
There is no \(C\)-to-\(O\) edge in \(D\).  Inside \(O\), they give the
thirteen-edge graph
\[
\begin{split}
J=\{&02,05,06,12,13,16,23,24,\\
    &34,35,45,46,56\}.
\end{split} \tag{4}
\]
Consequently
\[
 D=(K_C-c_0c_1)\mathbin{\dot\cup}J. \tag{5}
\]
Its degree sequence on \(C\) is \(4,4,5,5,5,5\), and on \(O\) is
\(3,3,4,4,4,4,4\).  In particular, \(\Delta(D)=5\).  Equation (3)
also shows that \(C\) is not a \(K_6\), while the disconnected
seven-vertex component \(J\) has only thirteen edges, fewer than the
fifteen needed by a \(K_6\).  Hence \(D\) is \(K_6\)-free.

## Completing the class-B support data

Take the following six remaining triple complements, all inside \(O\):
\[
 012,\quad123,\quad246,\quad345,\quad356,\quad456. \tag{6}
\]
Take one further triple complement
\[
 \{c_2,c_3,o_0\}, \tag{7}
\]
and the four remaining five-set complements
\[
 C\setminus\{c_0\},\quad C\setminus\{c_1\},\quad
 C\setminus\{c_2\},\quad C\setminus\{c_3\}. \tag{8}
\]
Together with (2), these are seven distinct five-sets and ten distinct
triples.  Every vertex occurs in exactly five complements.  Equivalently,
the seventeen complementary supports have sizes \(8^7\,10^{10}\), and
every vertex occurs in exactly twelve supports.  This is a valid \(r=0\)
class-B instance.

For a short incidence check, the six triples in (6) have multiplicities
\[
 (1,2,3,3,3,3,3) \tag{9}
\]
on \(o_0,\ldots,o_6\).  Adding (7) gives
\((2,2,3,3,3,3,3)\), exactly \(d_D(o_i)-1\).  On \(C\), the four
five-sets in (8) plus (7) have multiplicities
\[
 (3,3,4,4,4,4), \tag{10}
\]
again exactly \(d_D(c_i)-1\).  Since a vertex occurs in
\(6-d_D(v)\) selected complements, its total complement multiplicity is
five.

## The common forced edge

Let
\[
 H=K_{13}-D,\qquad e=c_0c_1.
\]
For any triple \(T\) in (6), its complementary size-ten support is
\[
 S_T=C\cup(O\setminus T). \tag{11}
\]
The residual graph has
\[
 H[C]=\{e\},\qquad H[C,O]=K_{6,7}. \tag{12}
\]
Any perfect matching of \(H[S_T]\) must match six vertices of \(C\)
against only four vertices of \(O\setminus T\), so it must use an edge
inside \(C\).  By (12), that edge can only be \(e\).  Conversely, after
using \(e\), any bijection from
\(C\setminus\{c_0,c_1\}\) to \(O\setminus T\) completes the matching.
Thus every one of these six supports has exactly
\[
 4!=24 \tag{13}
\]
perfect matchings, and all twenty-four contain the same edge \(e\).

The seventh remaining size-ten support, complementary to (7), is also
live.  One residual perfect matching on it is
\[
 c_0o_2,\quad c_1o_3,\quad c_4o_5,\quad c_5o_6,\quad o_1o_4. \tag{14}
\]
(The verifier finds exactly \(132\) such matchings.)

Any choice of three among the seven remaining size-ten supports includes
at least two of the six supports from (6).  Perfect matchings for those
two supports would both contain \(e\), so they cannot be edge-disjoint.
This proves the obstruction.

The scope separation is concrete: this same prefix *does* extend to nine
colours if one uses a remaining size-eight support.  Take the supports
complementary to \(012\) in (6), to (7), and to
\(C\setminus\{c_0\}\) in (8).  Three pairwise edge-disjoint residual
perfect matchings on them are respectively
\[
\begin{aligned}
&c_0c_1,\ c_2o_3,\ c_3o_4,\ c_4o_5,\ c_5o_6,\\
&c_0o_1,\ c_1o_2,\ c_4o_4,\ c_5o_5,\ o_3o_6,\\
&c_0o_3,\ o_0o_4,\ o_1o_5,\ o_2o_6.
\end{aligned} \tag{15}
\]
So the example rules out exactly the three-size-ten continuation, not
the desired coordinated-nine conclusion.

## Verification

Run:

```sh
python3 collaboration/r0_three_ten_obstruction/verify_k6_free_three_ten_obstruction.py
```

The verifier uses only the Python standard library.  It reconstructs all
seventeen complements and the six selected matchings, checks the class-B
row and column data, the complement cover, edge-disjointness, degrees,
the exact decomposition (5), and absence of a \(K_6\).  It independently
enumerates every residual perfect matching on the seven size-ten
supports, obtains counts
\[
 24,24,24,24,24,24,132,
\]
checks the common forced edge in the first six families, checks (14), and
exhaustively confirms that none of the \(\binom73=35\) triples packs.
It also checks the mixed-size nine-colour extension (15).

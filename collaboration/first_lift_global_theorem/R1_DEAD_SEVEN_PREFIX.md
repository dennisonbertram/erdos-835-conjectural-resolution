# A dead seven-prefix in the \(r=1\) profile

Date: 2026-07-28.

## Result and scope

There is an exact \(n=13,q=17\) class-B support instance with profile
\[
(n_8,n_{10},n_{12})=(8,8,1)
\]
and seven pairwise edge-disjoint prescribed support matchings of type
\[
8^4\,10^2\,12
\]
such that **none of the ten remaining supports has a perfect matching
avoiding the seven selected matchings**.

Consequently, the exceptional-\(r=0\) theorem

> every seven-prefix of the prescribed type extends to eight

does not generalize to \(r=1\).  Any universal eight-matching theorem for
all class-B instances must coordinate the choice of the first seven
matchings, switch an earlier matching, or use additional structure.

This is a dead prefix, not a noncompletable support instance.  In fact, the
same seventeen supports have an explicit different full decomposition of
all \(78\) edges of \(K_{13}\) into their prescribed matchings.  The
construction does not address class-B-prime or fan realizability, and does
not resolve the full first-lift theorem or Erdős--Rosenfeld Problem #835.

## Construction

Split the thirteen vertices as
\[
C=\{c_1,\ldots,c_6\},\qquad
O=\{o_0,\ldots,o_6\}.
\]
Let
\[
R=\{o_0o_1,o_0o_2,o_0o_3,o_0o_4\}
\]
be a four-edge star, and put
\[
F=K_C\mathbin{\dot\cup}(K_O-R). \tag{1}
\]
Thus \(|E(F)|=15+17=32\).

To decompose \(F\), use the standard seven-colouring of \(K_7\) on
\(\mathbb Z_7\), in which the edge \(i j\) has colour
\[
4(i+j)\pmod7. \tag{2}
\]
For \(K_C\), delete the vertex \(0\): colour \(0\) retains three edges and
each other colour retains two.  For \(K_O\), identify \(o_i\) with \(i\)
and delete the four star edges in \(R\).  Their colours are
\(\{1,2,4,5\}\).  The combined colour-class sizes are therefore
\[
6,\ 4,\ 4,\ 5,\ 4,\ 4,\ 5,
\]
which is exactly one size-twelve, four size-eight, and two size-ten
support matchings.

The six remaining size-ten support complements are the triples
\[
\begin{gathered}
123,\quad145,\quad246,\quad356,\quad126,\quad345
\end{gathered} \tag{3}
\]
on \(\{o_1,\ldots,o_6\}\).  Each of these six outside vertices occurs
three times and \(o_0\) occurs zero times.

The four remaining size-eight support complements are
\[
\begin{aligned}
P_1&=C\setminus\{c_1\},&
P_2&=C\setminus\{c_2\},\\
P_3&=(C\setminus\{c_3,c_4\})\cup\{o_5\},&
P_4&=(C\setminus\{c_5,c_6\})\cup\{o_6\}.
\end{aligned} \tag{4}
\]
Every \(c_i\) occurs in three of these four five-sets.

The degrees in \(F\) are
\[
d_F(c_i)=5,\quad d_F(o_0)=2,\quad
d_F(o_i)=5\ (1\le i\le4),\quad
d_F(o_5)=d_F(o_6)=6. \tag{5}
\]
Equations (3)--(5) give the exact remaining-complement identity
\[
\#\{\text{remaining complements containing }v\}=d_F(v)-2.
\]
Together with the selected supports, every vertex is therefore omitted
from exactly five of the seventeen supports and belongs to exactly twelve.
This proves that the displayed supports form a class-B instance of the
claimed profile.

## Why the prefix is dead

Let \(H=K_{13}-F\).  Every remaining size-ten support contains all six
vertices of \(C\), because its complement triple lies in \(O\).  But
\(H[C]\) has no edges, and the support contains only four vertices of
\(O\).  A perfect matching could match at most four of the six \(C\)
vertices across to \(O\), so no such matching exists.

For \(P_1,P_2\), the remaining size-eight support consists of one vertex
of \(C\) and all seven vertices of \(O\).  After matching the \(C\)-vertex
across, a perfect matching would require three disjoint edges of
\(H[O]=R\), whose matching number is one.

For \(P_3,P_4\), the support consists of two vertices of \(C\) and six
vertices of \(O\).  The two \(C\)-vertices must be matched across, after
which two disjoint edges of \(H[O]\) would be required.  Again
\(\nu(R)=1\).

Hence all ten unselected supports are blocked.

## The support instance itself completes

The verifier contains a second family of seventeen matchings, one for each
support in the exact order constructed above.  It checks directly that
each matching saturates its prescribed support, that the matchings are
pairwise edge-disjoint, and that their \(78\) edges are all of \(K_{13}\).

Thus the failure is entirely path-dependent: this support instance has a
full completion, but the displayed seven-prefix cannot be continued even
one more colour.  This rules out arbitrary-prefix induction while leaving
coordinated choice and switching as viable routes.

## Reproduction

`verify_r1_dead_seven_prefix.py` reconstructs the two round-robin
edge-colourings, the deleted star, all seventeen supports, and the exact
row sums.  It independently exhausts perfect matchings of every remaining
support and confirms that all ten are blocked, then checks the separate
explicit full-completion certificate edge by edge.

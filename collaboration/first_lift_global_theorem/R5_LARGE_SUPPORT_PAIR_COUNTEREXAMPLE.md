# The two large \(r=5\) supports can both be blocked

Date: 2026-07-28.

## Result and scope

In the \(r=5\) profile, a seven-prefix of type
\[
 8^4\,12^3
\]
can leave both remaining size-twelve supports without a perfect matching.
Moreover, the prefix can simultaneously contain distinct cores of both
possible types
\[
 E=K_8-E(K_3),\qquad G=K_7.
\]
Consequently every pair type \(EE,EG,GG\) can coexist, with both selected
cores lying in their respective size-twelve supports.  The exact
complement-row identity does not contradict any of the three pair types.

This is an abstract class-B prefix certificate.  It refutes a proof step
that tries to extend the prefix using only one of the two remaining
size-twelve supports.  It is not a counterexample to eighth-colour
extension: in this certificate every remaining size-eight support does
have a perfect matching.  No class-B-prime, fan, or full-factorization
realization is asserted.

## The seven-prefix

Let
\[
 C=\{0,\ldots,7\},\qquad O=\{8,\ldots,12\}.
\]
Use the explicit one-factorization
\[
 R_r=\{r\,7\}\cup
 \bigl\{\{r+j,r-j\}:j=1,2,3\bigr\},
 \qquad r\in\mathbb Z/7\mathbb Z, \tag{1}
\]
of \(K_C\), where the arithmetic in the second coordinates is modulo
seven.  Keep \(R_3,R_4,R_5,R_6\) as four size-eight support matchings.
Enlarge the first three factors by
\[
\begin{aligned}
P_0&=\{9\,10,11\,12\},\\
P_1&=\{8\,11,10\,12\},\\
P_2&=\{8\,12,9\,11\}.
\end{aligned} \tag{2}
\]
Thus \(R_i\cup P_i\), for \(i=0,1,2\), are three size-twelve support
matchings, omitting \(8,9,10\), respectively.

The seven matchings are edge-disjoint and their union is
\[
 F=K_C\mathbin{\dot\cup}(P_0\cup P_1\cup P_2). \tag{3}
\]
In particular,
\[
 |E(F)|=28+6=34,
\]
and its degree sequence on \(C;O\) is
\[
 7^8;\ 2,2,2,3,3. \tag{4}
\]

## Completing the class-B support matrix

The selected complements are four copies of \(O\), followed by the three
singletons \(8,9,10\).

For \(i\in\mathbb Z/8\mathbb Z\), put
\[
 T_i=\{i,i+1,i+3\},\qquad Q_i=C\setminus T_i. \tag{5}
\]
Use \(Q_0,\ldots,Q_7\) as the complement five-sets of the eight remaining
size-eight supports, and use \(\{11\},\{12\}\) as the complements of the
two remaining size-twelve supports.

Every point of \(C\) occurs in exactly five of the \(Q_i\).  Each of
\(8,9,10\) occurs in the four selected copies of \(O\) and in its selected
singleton.  Each of \(11,12\) occurs in those four copies of \(O\) and in
its remaining singleton.  Hence every vertex occurs in exactly five of
the seventeen complements.  Equivalently, every vertex belongs to exactly
twelve supports, so this is a class-B support family with profile
\[
 (n_8,n_{10},n_{12})=(12,0,5). \tag{6}
\]

The remaining complement multiplicities are
\[
 5^8;\ 0,0,0,1,1,
\]
which equal \(d_F(v)-2\) from (3).  Thus the complement-row identity is
satisfied exactly.

## Simultaneous \(EE,EG,GG\) cores

Because \(F\) contains all of \(K_C\), it contains, for example, the
distinct cores
\[
\begin{aligned}
E_0&=K_C-E(K_{\{0,1,2\}}),&
E_1&=K_C-E(K_{\{0,1,3\}}),\\
G_0&=K_{C\setminus\{0\}},&
G_1&=K_{C\setminus\{1\}}.
\end{aligned} \tag{7}
\]
Both remaining size-twelve supports are
\[
 V\setminus\{11\},\qquad V\setminus\{12\}, \tag{8}
\]
so both contain \(C\).  Assigning \((E_0,E_1)\), \((E_0,G_0)\), or
\((G_0,G_1)\) to the two supports realizes distinct-core versions of
\(EE,EG,GG\), respectively.  Same-core reuse is possible as well.

In the residual graph \(H=K_{13}-F\), the eight vertices of \(C\) are
independent.  Each support in (7) contains only four vertices outside
\(C\).  A matching can therefore cover at most four vertices of \(C\)
using cross edges, so neither twelve-vertex residual graph has a perfect
matching.

## Why the prefix still extends

Every remaining size-eight support is \(O\cup T_i\).  The graph \(H\)
contains all \(T_i\)-to-\(O\) edges, and
\[
 H[O]=\{8\,9,8\,10,9\,12,10\,11\}. \tag{9}
\]
Choose any edge of \(H[O]\), then match the three vertices of \(T_i\) to
the other three vertices of \(O\).  This gives a perfect matching for
every \(O\cup T_i\).

Thus the certificate is a sharp warning about the large-support-only
route, not an obstruction to the eighth matching itself.

## Verification

`verify_r5_large_support_pair_counterexample.py` reconstructs the
one-factorization, all seventeen complements, the seven prefix matchings,
the residual graph, the four distinct cores, and exhaustive
perfect-matching decisions for all ten remaining supports.

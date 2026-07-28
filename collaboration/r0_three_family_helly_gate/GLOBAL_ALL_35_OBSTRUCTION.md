# A full-row r=0 obstruction to all 35 three-size-ten routes

Date: 2026-07-28.

## Exact result

There is a valid \(r=0\) class-B instance and a packed
complement-cover six-prefix of profile \(8^3\,10^3\) such that

1. all seven remaining size-ten families are individually live;
2. every pair of them admits edge-disjoint perfect matchings; but
3. every one of the \(\binom73=35\) choices of three size-ten
   occurrences fails to admit three pairwise edge-disjoint perfect
   matchings.

Thus neither an arbitrary-three Helly lemma nor a seven-family selection
theorem can finish \(r=0\) using only the remaining size-ten colours.
This is not a coordinated-nine counterexample: the same prefix has an
explicit continuation using two size-ten colours and one size-eight
colour.

## The disconnected extremal

Put

\[
U=\{3,4,5,6,7,8\},\qquad
W=\{0,1,2,9,10,11,12\}.
\]

Take the prefix matchings

\[
\begin{array}{c|l}
C_0&0\,12,\ 12,\ 35,\ 9\,10\\
C_1&0\,10,\ 1\,11,\ 46,\ 78\\
C_2&02,\ 1\,12,\ 38,\ 67\\
C_3&2\,10,\ 36,\ 47,\ 58,\ 11\,12\\
C_4&0\,11,\ 1\,10,\ 48,\ 57,\ 9\,12\\
C_5&01,\ 2\,11,\ 37,\ 45,\ 68 .
\end{array}
\]

They are pairwise edge-disjoint matchings of sizes \(4,4,4,5,5,5\).
Their union \(D\) has no \(U\)-to-\(W\) edges and satisfies

\[
D[U]=K_U-\{34,56\},\qquad |D[W]|=14.
\]

Its degree sequence on \(0,\ldots,12\) is

\[
(5,5,4,4,4,4,4,5,5,2,4,4,4).
\]

## Completing the class-B rows

Use the seven remaining triple complements

\[
012,\quad 1\,10\,11,\quad 1\,10\,11,\quad 1\,9\,10,\quad
0\,11\,12,\quad 0\,2\,12,\quad 0\,2\,12,
\]

all contained in \(W\).  Use the four remaining five-set complements

\[
U-\{3\},\quad U-\{4\},\quad U-\{5\},\quad U-\{6\}.
\]

Together with the six prefix complements, these are ten triples and
seven five-sets.  Every vertex has complement multiplicity five.
Equivalently, the eleven remaining rows satisfy

\[
\rho(v)=d_D(v)-1.
\]

This realizes exactly the extremal incidence calculation.  If \(t=7\)
triple rows avoid a six-set spanning \(K_6-2K_2\), then the number of
deleted cross edges must be zero and all four remaining five-sets must
lie inside the six-set.

## Why all 35 choices fail

Every remaining size-ten support contains all six vertices of \(U\) and
four vertices of \(W\).  Let a perfect matching on such a support use
\(a\) edges inside \(U\), \(b\) edges inside \(W\), and \(c\) cross
edges.  Counting its endpoints in the two parts gives

\[
2a+c=6,\qquad 2b+c=4,
\]

and hence \(a=b+1\ge1\).

But the residual graph has only two edges inside \(U\), namely \(34\)
and \(56\).  Every perfect matching therefore uses at least one of
these two edges.  Three pairwise edge-disjoint perfect matchings would
need three distinct residual \(U\)-edges, which is impossible.  The
argument applies to every choice of three among the seven occurrences.

The verifier also enumerates the residual perfect matchings.  Their
counts for the seven size-ten occurrences are

\[
54,\ 54,\ 54,\ 50,\ 52,\ 54,\ 54.
\]

Every pair of occurrences coordinates, so the obstruction is genuinely
three-way rather than an individual or pair failure.

## The mixed escape

The obstruction is specific to using three size-ten colours.  The
remaining supports complementary to \(012\), \(1\,10\,11\), and
\(U-\{3\}\) admit the following pairwise edge-disjoint perfect
matchings:

\[
\begin{aligned}
&\{34,59,6\,10,7\,11,8\,12\},\\
&\{03,24,56,7\,12,89\},\\
&\{09,13,2\,12,10\,11\}.
\end{aligned}
\]

In fact, exact enumeration finds that all 84 choices consisting of two
of the seven size-ten occurrences and one of the four size-eight
occurrences pack, while no other three-colour type does for this fixed
prefix.

## A universal repair of the \(t=7\) extremal

The disconnected obstruction has a support-preserving two-edge repair.
This works for every \(t=7\) extremal of the displayed structural form,
not only for the certificate above.

Write the two residual \(U\)-edges as

\[
e=u_0v_0,\qquad f=u_1v_1,
\]

and let \(g=u_2v_2\) join the two remaining vertices of \(U\).  Thus
\(\{e,f,g\}\) is a perfect matching of \(K_U\), while \(g\in D\).  The
prefix colour containing \(g\) also contains an edge \(ab\) inside
\(W\): a matching contains at most three \(U\)-edges, whereas every
prefix colour has four or five edges and there are no cross edges.
Make the support-preserving switch

\[
g,ab\longmapsto u_2a,v_2b.
\]

The two new cross edges were not previously in \(D\), so the six prefix
matchings remain edge-disjoint.  The residual graph now contains the
perfect matching \(\{e,f,g\}\) on \(U\), and its only deleted cross edges
are \(u_2a,v_2b\).

Take any three remaining size-ten supports and assign their internal
\(U\)-edges to be \(e,f,g\).  Complete the first matching across
\((U-\{u_0,v_0\})\times A_0\), where \(A_0\) is its four-vertex part in
\(W\).  Only the two switched edges can be absent, so Hall's condition
holds.  For the second matching, the two vertices of the first core pair
have all four cross choices, while \(u_2,v_2\) each lose at most one
switched edge and one edge used by the first matching.  Hall's condition
again holds.  For the third matching, each of its four \(U\)-vertices
has lost only the one cross edge used by the earlier matching that
contains it.  Those lost edges come from two matchings on disjoint
two-vertex sets, so no right vertex loses all four incident edges; Hall's
condition holds a third time.

Hence the repaired prefix packs every choice of three size-ten
occurrences.

For the displayed certificate, \(g=78\) lies in \(C_1\) together with
\(0\,10\).  Apply

\[
78,\ 0\,10\longmapsto 07,\ 8\,10.
\]

After the switch all 35 size-ten triples pack.  One explicit packing on
the first three occurrences is

\[
\begin{aligned}
&\{34,59,6\,10,7\,11,8\,12\},\\
&\{03,24,56,7\,12,89\},\\
&\{04,23,5\,12,69,78\}.
\end{aligned}
\]

The complete before/after audit over all 165 triples of remaining
occurrences is:

\[
\begin{array}{c|c|c}
&\text{before}&\text{after}\\ \hline
\text{three size-ten}&0&35\\
\text{two size-ten plus one size-eight}&84&84\\
\text{all other types}&0&0\\
\text{total}&84&119.
\end{array}
\]

## Verification

Run:

```sh
python3 collaboration/r0_three_family_helly_gate/verify_global_counterexample.py
```

The verifier uses only the Python standard library.  It checks the
prefix, the disconnected \(13+14\)-edge decomposition, the exact
class-B row data, all perfect matchings on the eleven remaining
supports, all 35 size-ten failures, all 21 pair compatibilities, the
84 mixed continuations, the support-preserving repair, all 165 routes
before and after the switch, and the displayed witnesses.

# Coordinated eight-packings for the profiles \(r=2,3,4,5\)

Date: 2026-07-28.

## Result

Let \(V_1,\ldots,V_{17}\subseteq V(K_{13})\) be a target class-B support
family: every vertex belongs to twelve supports, and
\[
 (n_8,n_{10},n_{12})=(7+r,\,10-2r,\,r).
\]
For each
\[
 r\in\{2,3,4,5\},
\]
there are eight colours whose support-perfect matchings can be chosen
pairwise edge-disjoint.

This is an existential, coordinated eight-packing theorem.  It is not a
claim that an arbitrary seven-prefix extends.  The committed dead-prefix
certificates show that the latter statement is false.

## A six-complement covering lemma

Take complements inside the thirteen-vertex set.  The family consists of
\[
 m=7+r\ \text{five-sets},\qquad
 t=10-2r\ \text{triples},\qquad
 r\ \text{singletons}, \tag{1}
\]
and every vertex occurs in exactly five complement sets.

> **Covering lemma.**
>
> * If \(r=2,3,4\), some four of the five-sets and some two of the triples
>   cover all thirteen vertices.
> * If \(r=5\), some four of the five-sets and some two of the singleton
>   sets cover all thirteen vertices.

### The cases \(r=2,3\)

Choose four five-sets and two triples independently and uniformly within
their two labelled families.  For a vertex \(v\), let \(a_v,b_v,s_v\) be
its multiplicities among the five-sets, triples, and singletons.  Thus
\[
 a_v+b_v+s_v=5,\qquad \sum_v s_v=r. \tag{2}
\]
The probability that \(v\) is uncovered is
\[
 p_r(a_v,b_v)=
 \frac{\binom{m-a_v}{4}}{\binom m4}
 \cdot
 \frac{\binom{t-b_v}{2}}{\binom t2}, \tag{3}
\]
where a binomial coefficient is zero when its lower argument is too large.

For \(r=2\), direct substitution under \(a+b+s=5\) gives
\[
 p_2\le
 \begin{cases}
 1/18,&s=0,\\
 1/9,&s=1,\\
 2/9,&s=2.
 \end{cases} \tag{4}
\]
The two singleton incidences are either on one vertex or on two vertices.
The corresponding upper bounds for the expected number of uncovered
vertices are
\[
 \frac29+\frac{12}{18}=\frac89<1,\qquad
 \frac29+\frac{11}{18}=\frac56<1. \tag{5}
\]

For \(r=3\), the analogous maxima are
\[
 p_3\le
 \begin{cases}
 1/28,&s=0,\\
 1/12,&s=1,\\
 1/6,&s=2,\\
 1/3,&s=3.
 \end{cases} \tag{6}
\]
The three partitions of the singleton incidences give, respectively,
\[
 \frac13+\frac{12}{28}=\frac{16}{21},\qquad
 \frac16+\frac1{12}+\frac{11}{28}=\frac9{14},\qquad
 \frac3{12}+\frac{10}{28}=\frac{17}{28}. \tag{7}
\]
All are less than one.  Since the number of uncovered vertices is a
nonnegative integer, an expectation below one proves that some selection
covers every vertex.

### The case \(r=4\)

Here \(m=11,t=2\), so both triples are selected.  A vertex appearing in a
triple is automatically covered.  For a vertex with no triple incidence
and singleton multiplicity \(s\), its five-set multiplicity is \(5-s\),
and the probability that four random five-sets miss it is at most
\[
\begin{array}{c|ccccc}
s&0&1&2&3&4\\ \hline
p&1/22&7/66&7/33&21/55&7/11.
\end{array} \tag{8}
\]
Unless all four singleton sets are the same vertex, the worst partition is
\(3+1\), and (8) bounds the expectation by
\[
 \frac{21}{55}+\frac7{66}+\frac{11}{22}
 =\frac{163}{165}<1. \tag{9}
\]

It remains to handle four repeated singleton sets \(\{x\}\).  If \(x\)
lies in a triple, the other twelve vertices contribute at most
\(12/22<1\).  Otherwise (2) says that \(x\) belongs to a unique five-set
\(A^\ast\).  Select \(A^\ast\), both triples, and three random five-sets
from the other ten.  Only the eight vertices outside \(A^\ast\) can remain
uncovered.  Any such vertex that is also outside both triples has
singleton multiplicity zero, triple multiplicity zero, and hence lies in
five of those ten five-sets.  Its miss probability is
\[
 \frac{\binom53}{\binom{10}3}=\frac1{12}.
\]
The expected number left uncovered is at most \(8/12<1\).  This completes
the \(r=4\) case.

### The case \(r=5\)

There are twelve five-sets, no triples, and five singleton sets.  Select
four five-sets and two singleton sets independently and uniformly.  If a
vertex has singleton multiplicity \(s\), then its five-set multiplicity is
\(5-s\), and its miss probability is
\[
 \frac{\binom{7+s}{4}}{\binom{12}{4}}
 \cdot
 \frac{\binom{5-s}{2}}{\binom52}.
 \tag{10}
\]
For \(s=0,\ldots,5\), these probabilities are
\[
 \frac7{99},\quad
 \frac{14}{165},\quad
 \frac{21}{275},\quad
 \frac7{165},\quad
 0,\quad0. \tag{11}
\]
The singleton multiplicities sum to five.  Checking the seven integer
partitions of five, the largest resulting expectation occurs for
\(1+1+1+1+1\), where it is
\[
 5\cdot\frac{14}{165}+8\cdot\frac7{99}
 =\frac{98}{99}<1. \tag{12}
\]
This proves the covering lemma in the final profile.

## Packing the selected six colours

For \(r=2,3,4\), use the covering lemma to select four support-eight
colours and two support-ten colours.  Choose perfect matchings on the four
size-eight supports greedily.  At step \(i\le4\), the current residual
graph on that support has minimum degree at least \(8-i\ge4\), so the
standard dense-support argument applies.

After those four matchings, each of the two selected size-ten supports has
residual minimum degree at least \(9-4=5\).  The two-matching lemma proved
in `collaboration/first_lift_global_theorem/SIX_PACKING_NOTE.md` supplies
perfect matchings on the two supports that are disjoint from each other
and from the first four.

For \(r=5\), the covering lemma instead selects four support-eight colours
and two support-twelve colours.  The support sizes
\[
 8,8,8,8,12,12
\]
satisfy \(s_i\ge2i\), so the dense-support lemma packs all six greedily.

In either construction, let \(D\) be the union of the six matchings.

Every selected matching contributes degree one precisely at the vertices
of its support.  Since the six selected complements cover every vertex,
each vertex lies in at most five selected supports.  Therefore
\[
 \Delta(D)\le5,\qquad
 \delta(K_{13}-D)\ge12-5=7. \tag{13}
\]

## Adding two size-twelve colours

For \(r=2,3,4\), no size-twelve colour was used among the first six.  For
\(r=5\), two of the five size-twelve colours were used, leaving three.
Thus at least two unused size-twelve colours remain in every case.  Choose
two, write their singleton complements as \(\{x\}\) and \(\{y\}\), and put
\[
 H=K_{13}-D.
\]

If \(x\ne y\), Ore's Hamilton-connectedness criterion applies: a graph of
order \(n\) in which every nonadjacent pair has degree sum at least \(n+1\)
is Hamilton-connected.  By (13), every such sum in \(H\) is at least
\(14=13+1\).  Hence \(H\) has a Hamilton path from \(x\) to \(y\).
Its twelve edges split alternately into two disjoint six-edge matchings.
One misses \(x\), and the other misses \(y\), so they are perfect matchings
on the two prescribed size-twelve supports.

If \(x=y\), the graph \(H-x\) has twelve vertices and minimum degree at
least six.  Dirac's theorem gives a Hamilton cycle.  Its alternating edge
sets are two disjoint perfect matchings on the common support
\(V(K_{13})\setminus\{x\}\).

In both cases these two matchings avoid \(D\).  Together with the first six
they give the claimed coordinated eight-packing.

For completeness, Ore's criterion can be obtained from the standard
Hamilton-connected closure rule: adding a nonedge \(uv\) with
\(d(u)+d(v)\ge n+1\) preserves Hamilton-connectedness.  Repeatedly adding
all nonedges closes the graph to \(K_n\).

## Verification and exact scope

Run:

```sh
python3 collaboration/coordinated_eight_r2_r5/verify_arithmetic.py
```

The standard-library verifier checks every probability maximum in
(4), (6), (8), and (11), every singleton-incidence partition, the
exceptional \(r=4\) estimate, all profile counts, and the degree and
Hamiltonian threshold arithmetic.

The proof covers every abstract class-B instance for \(r=2,3,4,5\), and
therefore also their class-B-prime and fan-realizable subfamilies.  The
\(r=1\) coordinated-eight case remains open: there is only one
size-twelve colour, so the final Hamilton-path construction cannot be
used twice.  No full seventeen-colour completion or solution of
Erdős--Rosenfeld Problem #835 is claimed.

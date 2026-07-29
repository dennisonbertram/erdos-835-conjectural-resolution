# The \(r=2\) initial-support dichotomy

Date: 2026-07-28.

## Theorem

Let \(D\) be the union of a complement-cover six-packing of types
\(8^4\,10^2\) in a target class-B \(r=2\) instance, and put
\[
G=K_{13}-D.
\]
Among the five remaining size-eight supports and four remaining
size-ten supports, at least one induces a graph with a perfect matching
in \(G\).

Equivalently, it is impossible for all nine non-singleton terminal
supports to be blocked immediately after the six-prefix.

This is a solver-free initial-choice theorem.  It is not yet a
coordinated-nine theorem: after choosing the guaranteed matching, two
prescribed near-perfect matchings still have to be packed disjointly.

## Six-prefix identities

The selected matchings have sizes \(4,4,4,4,5,5\), so
\[
|E(D)|=26.
\]
Because the six selected complements cover all thirteen vertices,
\[
1\le d_D(v)\le5,\qquad \delta(G)\ge7. \tag{1}
\]

Write \(A_1,\ldots,A_5\) for the remaining five-set complements,
\(T_1,\ldots,T_4\) for the remaining triples, and \(x,y\) for the
singleton complements.  If \(a(v),t(v),h(v)\) count the corresponding
incidences, the exact class-B row identity is
\[
\boxed{a(v)+t(v)+h(v)=d_D(v)-1.} \tag{2}
\]
The total triple-plus-singleton mass is
\[
\sum_v(t(v)+h(v))=4\cdot3+2=14. \tag{3}
\]

## If all four size-ten supports are blocked

Suppose for contradiction that all four size-ten supports are blocked.
Each induced graph has minimum degree at least
\[
7-(13-10)=4.
\]
Tutte's theorem leaves only two coarsened obstruction cores in \(D\):
\[
K_{5,5}\qquad\text{or}\qquad K_6. \tag{4}
\]
Indeed, a Tutte set of order \(s\) requires at least \(s+2\) odd
components, and every component has order at least the least odd integer
not smaller than \(5-s\).  The only surviving partitions are \(5+5\)
for \(s=0\) and \(1^6\) for \(s=4\).

The \(K_{5,5}\) type is impossible.  Its ten vertices all have
\(D\)-degree at least five and hence exactly five.  Together with the
lower bound one at the other three vertices, this would give degree sum
at least
\[
10\cdot5+3=53>2|E(D)|=52. \tag{5}
\]
Thus every blocked size-ten support contains a \(K_6\) in \(D\).

All four \(K_6\) cores are the same.  If two such cliques share a vertex
\(v\), the five clique-neighbours already saturate \(d_D(v)\), so the
two neighbour sets—and hence the cliques—coincide.  If they are
disjoint, they use \(2\binom62=30>26\) edges.  Call the common clique
\(B\), \(|B|=6\).

Every vertex of \(B\) is saturated by its five clique edges.  Therefore
no \(D\)-edge joins \(B\) to
\[
R=V(K_{13})\setminus B,\qquad |R|=7,
\]
and
\[
D=K_6[B]\mathbin{\dot\cup}J,\qquad
J=D[R],\qquad |E(J)|=26-15=11. \tag{6}
\]
Every triple \(T_j\) avoids \(B\), because its complementary support
contains the common core \(B\).

Apply (2) on \(B\).  There \(d_D=5\) and \(t=0\), so
\[
\sum_{b\in B}a(b)+\sum_{b\in B}h(b)=24.
\]
The two singletons contribute at most two incidences, giving
\[
\sum_{b\in B}a(b)\ge22. \tag{7}
\]

## The five size-eight supports cannot also be blocked

A blocked size-eight support has one of the three possible cores
\[
K_{3,5},\qquad K_{3,1,1,1},\qquad K_5 \tag{8}
\]
inside \(D\).  These are exactly the size-eight Tutte types compatible
with \(\Delta(D)\le5\).

No size-eight support can contain five vertices of \(B\).  If its
five-set complement \(A_i\) met \(B\) in at most one vertex, then (even
putting all five vertices of \(B\) into every other \(A_j\))
\[
\sum_{b\in B}a(b)\le1+4\cdot5=21,
\]
contradicting (7).

Every core in (8) is connected, while (6) has no edge between \(B\) and
\(R\).  A size-eight obstruction core must therefore lie wholly in
\(B\) or wholly in \(R\).  The preceding paragraph rules out a core in
\(B\): every type in (8) has at least five vertices.

Inside \(R\), the graph \(J\) has only eleven edges.  Hence it cannot
contain \(K_{3,5}\), which has fifteen edges, or
\(K_{3,1,1,1}\), which has twelve.  Every blocked size-eight support
must therefore contain a \(K_5\) in \(J\).

There is at most one such \(K_5\).  Two distinct five-cliques on the
seven-set \(R\) have union of at least
\[
2\binom52-\binom42=14>11 \tag{9}
\]
edges.  Thus if all five size-eight supports were blocked, they would
all contain one common clique \(C\subset R\), \(|C|=5\).  Equivalently,
all five complements \(A_i\) would avoid \(C\), so
\[
\sum_{c\in C}a(c)=0. \tag{10}
\]

Every \(c\in C\) has \(d_D(c)\ge4\).  Summing (2) over \(C\), and using
(10), gives
\[
\sum_{c\in C}(t(c)+h(c))
=\sum_{c\in C}(d_D(c)-1)\ge5\cdot3=15. \tag{11}
\]
But (3) says that the total triple-plus-singleton mass over all thirteen
vertices is only fourteen.  This contradiction proves the theorem.

## Verification

Run:

```sh
python3 collaboration/r2_initial_support_dichotomy/verify_dichotomy.py
```

The verifier uses only the Python standard library.  It exhausts the
coarsened Tutte arithmetic for support sizes ten and eight, checks every
edge, degree-sum, overlap, and row-incidence bound in (3)--(11), and
confirms the exact surviving core lists.

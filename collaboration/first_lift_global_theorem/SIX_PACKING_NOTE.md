# Six support matchings always pack at the target order

Date: 2026-07-27.

## Scope

This note proves that every \(n=13,q=17\) class-B support instance contains a
six-colour subfamily whose prescribed perfect matchings can be chosen
edge-disjointly.  In particular, some dense five-colour prefix always extends
through a sixth colour.

This is a genuine coordinated-prefix theorem, but it is not a completion of
all seventeen colours.  It applies to the abstract class B and hence also to
class B-prime and fan-realizable instances; it does not prove the universal
completion claim for any of those classes.

## A two-matching lemma on ten vertices

We first isolate the repair step needed in the profile with no support of
size twelve.

> **Lemma.**  Let \(G_1,G_2\) be graphs, each on a set of ten vertices and
> each of minimum degree at least five.  Their vertex sets need not be the
> same.  There are perfect matchings \(M_1\subseteq E(G_1)\) and
> \(M_2\subseteq E(G_2)\) with no common edge.

### Matching-deletion classification

Let \(G\) be a graph on ten vertices with \(\delta(G)\ge5\), let \(D\) be a
matching, and suppose \(H=G-D\) has no perfect matching.  By Tutte's theorem
there is an \(S\subseteq V(G)\), with \(s=|S|\), such that the number \(k\)
of odd components of \(H-S\) is greater than \(s\).

Parity gives \(k-s\) even, hence \(k\ge s+2\).  Since \(H\) has minimum
degree at least four, every odd component \(C\) of \(H-S\) has
\[
 |C|-1+s\ge4,\qquad\text{so}\qquad |C|\ge5-s. \tag{1}
\]
Also \(k\le10-s\), so \(s\le4\).  The integer cases in (1) leave only:

1. \(s=0\): there are exactly two components of order five;
2. \(s=4\): there are exactly six singleton components.

For \(s=1,2,3\), the least possible total sizes of the odd components are,
respectively, \(3\cdot5=15\), \(4\cdot3=12\), and \(5\cdot3=15\), all
larger than \(10-s\).

In case 1, every vertex has at most four neighbours inside its component and
at most one edge of \(D\) to the other component.  Minimum degree five forces
\[
 G=K_5\mathbin{\dot\cup}K_5+P, \tag{2}
\]
where \(P\subseteq D\) is a perfect matching between the two cliques.

In case 2, write \(U=V(G)\setminus S\), so \(|U|=6\).  Every \(u\in U\) has
at most four neighbours in \(S\) and at most one edge of \(D\) in \(U\).
Again equality is forced:
\[
 G[S,U]=K_{4,6},\qquad G[U]=P\subseteq D, \tag{3}
\]
where \(P\) is a perfect matching on \(U\).

The critical matching \(P\) is unique for a fixed \(G\).  In case (2), the
complement is the connected bipartite graph \(K_{5,5}-P\), whose bipartition
is unique up to exchange.  In case (3), \(K_6-P\) is an isolated connected
six-vertex component of the complement, while only four vertices remain.
The two cases cannot coexist because the complement in (2) is connected and
the complement in (3) is not.

The classification also shows that every edge of \(G\) is avoidable by a
perfect matching.  Indeed, if \(G-e\) had no perfect matching, the one-edge
matching \(D=\{e\}\) would have to contain a critical \(P\) of size five in
case (2) or size three in case (3), which is impossible.  Taking \(D\) empty
likewise proves directly that \(G\) has a perfect matching.

### Repair proof

Choose any perfect matching \(M_1\) of \(G_1\), and put
\[
 D=M_1\cap E(G_2).
\]
If \(G_2-D\) has a perfect matching, we are done.  Otherwise its unique
critical matching \(P\) is contained in \(D\).  Choose \(e\in P\).  The edge
\(e\) also belongs to \(G_1\), and the avoidability result gives a perfect
matching \(M_1'\) of \(G_1-e\).

If \(G_2-(M_1'\cap E(G_2))\) had no perfect matching, its failure would have
to delete the same unique \(P\), contradicting \(e\notin M_1'\).  Thus the
repaired first matching admits a disjoint second matching.  This proves the
lemma.

## The target support profiles

Let \(n_8,n_{10},n_{12}\) count colours whose supports have the indicated
sizes.  The class-B row and column sums force
\[
 (n_8,n_{10},n_{12})=(7+r,\,10-2r,\,r),
 \qquad 0\le r\le5. \tag{4}
\]

Recall the elementary dense-support rule: after \(i-1\) matchings have been
chosen, a support of even size \(s\) sees a residual graph of minimum degree
at least \(s-i\).  If \(s\ge2i\), this is at least \(s/2\), so the residual
graph has a perfect matching.  Thus supports ordered as
\(s_i\ge2i\) can be packed greedily.

If \(1\le r\le4\), choose supports of sizes
\[
 8,8,8,8,10,12.
\]
If \(r=5\), choose
\[
 8,8,8,8,12,12.
\]
In both cases \(s_i\ge2i\) for \(1\le i\le6\), so the six matchings pack
greedily.

It remains to treat \(r=0\), where (4) is \((7,10,0)\).  Choose four
size-eight supports and pack them greedily.  For each of two size-ten
supports \(V_1,V_2\), delete the edges used by those four matchings.  The
resulting graphs \(G_i\) on \(V_i\) have
\[
 \delta(G_i)\ge9-4=5.
\]
The ten-vertex lemma supplies edge-disjoint perfect matchings in \(G_1\) and
\(G_2\).  Together with the first four matchings these give the required
six-colour packing.

Therefore every target class-B instance has an edge-disjoint six-matching
prefix, and its first five supports can be ordered to satisfy the dense
criterion.

## What remains

The dead-prefix certificate in `NOTE.md` shows why an arbitrary dense
five-prefix need not extend.  The present theorem repairs exactly that
failure of quantifiers: **some** dense five-prefix always extends.

The residual eleven colours still have interacting prescribed supports, and
the six-prefix theorem does not by itself furnish an invariant that permits
all eleven remaining matchings to be added.  The unresolved step is now to
propagate a coordinated-prefix property beyond six or to prove a global
switching theorem.

`verify_six_packing_arithmetic.py` checks all finite Tutte-size cases,
critical-complement connectivity, profile counts, and dense inequalities.
The universal theorem rests on the proof above rather than on random search.

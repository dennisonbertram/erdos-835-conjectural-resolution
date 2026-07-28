# A support-preserving switch removes every size-ten blocker

Date: 2026-07-28.

## Result

Consider any of the profiles \(r=0,1,2\) after a packed
complement-cover six-prefix:

\[
\begin{array}{c|c|c|c}
r&\text{selected supports}&
\text{remaining complements }(5,3,1)&|E(D)|\\ \hline
0&8^3\,10^3&(4,7,0)&27\\
1&8^4\,10^2&(4,6,1)&26\\
2&8^4\,10^2&(5,4,2)&26.
\end{array} \tag{1}
\]

The \(r=0\) row uses the \(3+3\) covering theorem in
`../r0_complement_cover_six/NOTE.md`; the \(r=1,2\) rows use the
covering constructions in `../coordinated_eight_r1/NOTE.md` and
`../coordinated_eight_r2_r5/NOTE.md`.

> **Prefix-switch theorem.**  After at most one two-edge switch inside
> one selected colour, every remaining size-ten support has a perfect
> matching in \(K_{13}-D\).

The switch preserves the six exact supports, all edge-disjointness,
every vertex degree in \(D\), and hence the complement-cover invariant
\(\Delta(D)\le5\).

This is an individual-extension theorem.  It does not assert that three
of the remaining perfect matchings can be chosen simultaneously.

## The only possible blockers

Let \(Y\) be a remaining size-ten support.  If
\((K_{13}-D)[Y]\) has no perfect matching, coarsening a Tutte barrier
gives a complete multipartite core in \(D[Y]\).  Since
\(\Delta(D)\le5\), the order-ten odd-partition catalogue leaves only
\[
 K_{5,5}\quad\text{or}\quad K_6. \tag{2}
\]

For every vertex,
\[
 \rho(v)=d_D(v)-1, \tag{3}
\]
where \(\rho(v)\) is its multiplicity among the remaining complements.
A \(K_{5,5}\) core would give \(d_D(v)=5\), hence \(\rho(v)=4\), at
each of its ten vertices.  It would require forty remaining-complement
incidences on \(Y\).  The complementary triple of \(Y\) contributes
zero there.  The total capacities of all the other remaining
complements in the three rows of (1) are respectively
\[
\begin{array}{c|c|c}
r&\text{total remaining complement size}&
\text{after deleting the blocked triple}\\ \hline
0&4\cdot5+7\cdot3=41&38\\
1&4\cdot5+6\cdot3+1=39&36\\
2&5\cdot5+4\cdot3+2=39&36.
\end{array} \tag{4}
\]
All are smaller than forty.  Thus \(K_{5,5}\) is impossible in every
profile.

It remains only to remove a possible \(K_6\).

## The two-edge switch

Suppose \(D\) contains a \(K_6\) on \(C\), and put
\[
 O=V(K_{13})\setminus C,\qquad |O|=7.
\]
Every vertex of \(C\) already has \(D\)-degree five, so \(C\) is a
connected component of \(D\); in particular, \(D\) has no
\(C\)-to-\(O\) edge.

Every selected colour layer is a matching of size four or five.  Within
\(C\) or within \(O\), a matching has at most three edges.  Since the
layer has no cross-edge, it therefore contains both
\[
 uv\in E(K_C)
 \quad\text{and}\quad
 pq\in E(K_O). \tag{5}
\]
Replace these two edges in that one layer by
\[
 up,\qquad vq. \tag{6}
\]
The four endpoints in (5) are distinct and all lie in the same support,
so (6) is again a perfect matching on exactly that support.  Both new
edges were unused because \(D\) had no cross-edge.  All other selected
layers remain disjoint from the switched one.  The switch preserves the
degree of every vertex, so it also preserves the complement cover and
\(\Delta(D)\le5\).

## No new \(K_6\) is created

Before the switch, the \(K_6\) on \(C\) is unique.  A second one sharing
a vertex of \(C\) would have to lie in the same saturated component, and
a disjoint one would need fifteen of the at most
\[
 |E(D)|-15\le12 \tag{7}
\]
edges outside \(C\).

Let \(D'\) be the switched union.  A \(K_6\) in \(D'\) that uses neither
new edge in (6) would already have been a \(K_6\) in \(D\); the unique
candidate \(C\) has lost \(uv\).

Suppose instead that a new \(K_6\) uses \(up\).  The five neighbours of
\(u\) in \(D'\) are exactly
\[
 (C\setminus\{u,v\})\cup\{p\}. \tag{8}
\]
Hence the putative clique would have to be
\[
 \{u,p\}\cup(C\setminus\{u,v\}).
\]
But \(p\) has no edge to any vertex of
\(C\setminus\{u,v\}\): there were no old cross-edges, and the switch
added only \(up\) and \(vq\).  This is impossible.  The same argument
rules out a clique using \(vq\).  Therefore \(D'\) contains no \(K_6\).

Together with (2)--(4), this proves that every remaining size-ten
support has a residual perfect matching.

## Sharp meaning of the theorem

`DEAD_SIX_PREFIX.md` shows why the switch is genuinely necessary: its
displayed \(r=0\) six-prefix has a saturated \(K_6\) and only two live
remaining colours.  Applying (5)--(6) to \(c_0c_5,o_0o_3\) in its first
layer replaces them by \(c_0o_0,c_5o_3\).  After this switch, all seven
remaining size-ten supports have perfect matchings.

Run:

```sh
python3 collaboration/r0_three_ten_obstruction/verify_k6_prefix_switch.py
```

The standard-library verifier checks the three capacity rows, the exact
Tutte catalogue, the abstract post-switch \(K_6\) classification, and
concrete switches in both the \(r=0\) dead-prefix certificate and the
four-blocked-support \(r=2\) certificate in
`../coordinated_nine_r2_obstruction/NOTE.md`.  On the \(r=0\) instance
the seven residual perfect-matching counts become
\[
 24,24,24,24,24,138,152.
\]
On the \(r=2\) instance all four formerly blocked size-ten supports have
exactly twenty-four residual perfect matchings after the switch.

The remaining \(r=0\) frontier is now purely simultaneous: coordinate
three of seven individually extendible size-ten supports, or make a
larger support-preserving trade in the six-prefix.  No coordinated ninth
or solution of Erdős--Rosenfeld Problem #835 is claimed here.

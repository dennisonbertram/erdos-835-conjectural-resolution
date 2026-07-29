# The r0 size-ten incompatibility graph

Date: 2026-07-28.

## Setup

Let an \(r=0\) class-B instance on \(K_{13}\) have a packed
complement-cover six-prefix of profile \(10^3\,8^3\).  Let \(D\) be the
union of its six selected matchings and put
\[
 H=K_{13}-D.
\]
After the support-preserving saturated-\(K_6\) switch from
`K6_PREFIX_SWITCH.md`, we may assume
\[
 |E(D)|=27,\qquad 1\le d_D(v)\le5,\qquad D\text{ is }K_6\text{-free},
 \tag{1}
\]
and all seven remaining size-ten supports are individually matchable.
Their complements are seven triples, with repetitions allowed.

Define the **incompatibility graph** \(I\) on these seven colour
occurrences.  Two colours are adjacent when no perfect matching on one
support is edge-disjoint from a perfect matching on the other.

The certified pair gate in
`../coordinated_nine_r0_pair_gate_sat/NOTE.md` says that every edge of
\(I\) has a common forced edge: some graph edge belongs to every perfect
matching on both supports.  The forced-edge catalogue has two possible
deletion cores:
\[
 K_6-e,\qquad K_{5,5}-e. \tag{2}
\]

## Exact classification

> **Incompatibility-graph theorem.**
>
> 1. No edge of \(I\) arises from a \(K_{5,5}-e\) core.
> 2. If \(D\) has no \(K_6-e\) core, then \(I\) is empty.
> 3. Otherwise there is a unique six-set \(U\) and a unique edge \(e\)
>    such that
>    \[
>    D[U]=K_6-e.
>    \]
>    If \(t\) of the seven triple complements avoid \(U\), then
>    \[
>    I=K_t\mathbin{\dot\cup}(7-t)K_1,\qquad 0\le t\le6. \tag{3}
>    \]
>
> Consequently, if \(I\) has no independent three-set, then \(t=6\).
> This is exactly the six-fold common-forced-edge boundary proved
> coordinateable in `R0_EQUALITY_COORDINATION.md`.

The first assertion means that the \(K_{5,5}-e\) equality type may occur
for one support, but it cannot certify an incompatible pair.

## The remaining-complement identity

Let \(\rho(v)\) be the multiplicity of \(v\) among the eleven remaining
complements: four five-sets and seven triples.  Since every class-B row
has complement multiplicity five and the selected matchings saturate
exactly the vertices outside their complements,
\[
 \rho(v)=d_D(v)-1. \tag{4}
\]
The total remaining-complement capacity is
\[
 4\cdot5+7\cdot3=41. \tag{5}
\]

## A K5,5-e core is globally rigid

Suppose a residual perfect-matching family on a ten-set \(Y\) has forced
edge \(e=ab\) through a \(K_{5,5}-e\) deletion core.  Write
\[
 Y=A\mathbin{\dot\cup}B,\qquad |A|=|B|=5,
\]
where \(a\in A,b\in B\), and \(D[Y]\) contains every \(A\)-to-\(B\)
edge except \(e\).

The eight vertices other than \(a,b\) already have \(D\)-degree five and
are saturated.  The endpoints have core degree four.  Any additional
selected edge at an endpoint must go to
\[
 X=V(K_{13})\setminus Y,
\]
because the other core vertices are saturated and \(e\notin D\).  Let
\(c\) be the number of such endpoint-to-\(X\) edges.

Equation (4) requires at least
\[
 8\cdot4+(3+c_a)+(3+c_b)=38+c \tag{6}
\]
remaining-complement incidences on \(Y\).  The triple \(X\) itself
contributes zero there, while all ten other remaining complements have
total capacity
\[
 41-3=38. \tag{7}
\]
Thus
\[
 c=0, \tag{8}
\]
and equality holds throughout.

The core uses twenty-four edges.  No core vertex can have another
selected edge, so the other three edges of \(D\) lie inside the
three-set \(X\).  Therefore
\[
 D=(K_{5,5}-e)\mathbin{\dot\cup}K_3. \tag{9}
\]

This has three consequences.

1. It contains no \(K_6-e'\): such a graph is connected and
   non-bipartite, while the only components in (9) have orders ten and
   three and the order-ten component is bipartite.
2. It contains no second \(K_{5,5}-e'\) core.  Such a core is connected
   on ten vertices, so it must use \(Y\); the connected bipartite graph
   \(K_{5,5}-e\) has a unique bipartition, and its unique missing cross
   edge is \(e\).
3. Every \(x\in X\) has \(d_D(x)=2\), hence \(\rho(x)=1\).  The one
   triple \(X\) already uses that incidence.  A second remaining colour
   cannot have the same triple complement.

Hence at most one of the seven colours has this forced edge, and no
incompatibility edge can be certified by the \(K_{5,5}-e\) branch.
Mixed \(K_{5,5}-e/K_6-e'\) certification is impossible as well.

## A K6-e core is unique

Suppose \(D\) contains \(K_6-e\) on \(U\) and \(K_6-e'\) on a distinct
six-set \(U'\).  Put \(k=|U\cap U'|\).

If \(k\le1\), the two cores use at least twenty-eight edges, contradicting
\(|E(D)|=27\).  If \(k=2\) and the two common vertices are both endpoints
of the first missing edge, the cores share no selected edge and again
use at least twenty-eight.  Otherwise one common vertex is a non-endpoint
of the first missing edge.  It already has five neighbours inside \(U\),
so it has no selected neighbour in \(U'\setminus U\), whereas the second
core can omit only one of those four required edges.  This is impossible.

For \(3\le k\le5\), at least \(k-2\) common vertices are non-endpoints of
the first missing edge and hence saturated inside \(U\).  The second core
would have to omit at least
\[
 (k-2)(6-k) \tag{10}
\]
edges from these vertices to \(U'\setminus U\).  The values for
\(k=3,4,5\) are \(3,4,3\), but a \(K_6-e'\) core omits only one edge.
This is again impossible.

Thus \(U'=U\).  If \(e'\ne e\), the union of the two cores is a full
\(K_6\), contrary to (1).  Therefore the six-set and missing edge are
both unique.

Let
\[
 {\cal S}=\{i:T_i\cap U=\varnothing\},\qquad t=|{\cal S}|.
\]
For every \(i\in{\cal S}\), its support contains \(U\), and its perfect
matchings all use \(e\).  Hence every two vertices of \({\cal S}\) are
adjacent in \(I\).

Conversely, an incompatibility edge must have a common forced edge by the
certified pair gate.  The \(K_{5,5}-e\) branch is unavailable, and the
\(K_6-e\) core is unique.  Both endpoint supports must therefore contain
\(U\), so both colour vertices lie in \({\cal S}\).  This proves (3).

## The clique has order at most six

Let
\[
 a=|E_D(U,V\setminus U)|.
\]
The four non-endpoints of \(e\) have \(D\)-degree five, while its two
endpoints have total degree \(4+a_x,4+a_y\).  By (4), the remaining
complements require
\[
 22+a \tag{11}
\]
incidences on \(U\), where \(a=a_x+a_y\).

The \(t\) triples in \({\cal S}\) contribute zero there.  The four
five-sets and the other \(7-t\) triples have capacity at most
\[
 20+3(7-t)=41-3t. \tag{12}
\]
Thus
\[
 22+a\le41-3t,\qquad
 t\le\left\lfloor\frac{19-a}{3}\right\rfloor\le6. \tag{13}
\]

For \(t\ge1\), the independence number of (3) is
\[
 \alpha(I)=1+(7-t)=8-t. \tag{14}
\]
Together with \(t\le6\), the absence of an independent three-set is
equivalent to \(t=6\).  The incidence arithmetic in that equality case
is precisely the three-case reduction
\[
 (a,r)=(0,2),(0,3),(1,3)
\]
handled in `R0_EQUALITY_COORDINATION.md`.

## Independent audit of the certified gate

The semantic auditor was run with the \(r=0\) prefix shape:

```sh
python3 collaboration/coordinated_nine_r1_gate_sat/audit_certificates.py \
  --certificate-dir collaboration/coordinated_nine_r0_pair_gate_sat/certificates \
  --prefix-sizes 4 4 4 5 5 5 \
  --label r=0
```

It independently recovered the six support-pair orbits
\[
(k,x)=(0,0),(0,1),(1,0),(1,1),(2,0),(3,0),
\]
reconstructed every CNF clause semantically, and matched all six
manifests, clause counts, pair counts, and hashes.  It reported
`PASS all six exact r=0 cross-family certificates`.

A second independent pass supplied the local DRAT-trim binary through the
auditor's `--drat-trim` option.  All six compressed proofs replayed to
`s VERIFIED`, in addition to the original CaDiCaL internal checks and
generation-time DRAT-trim verification recorded in the certificate note.

The SAT theorem applies to arbitrary ten-sets, including coincident
supports, and uses only six disjoint matchings of sizes
\(4,4,4,5,5,5\) and the degree interval \(1\le d_D\le5\).  The
class-B complement rows enter only in the structural deductions
(4)--(13).

## Scope: the remaining three-way gate

This theorem proves the requested collapse:

> If the pair-incompatibility graph has no independent triple, the
> instance lies in the six-fold \(K_6-e\) boundary and is repaired by
> `R0_EQUALITY_COORDINATION.md`.

It does **not** yet prove coordinated nine for \(r=0\).  An independent
three-set in \(I\) says that each of its three support pairs admits some
edge-disjoint choice.  Those three pairwise witnesses need not be
consistent choices of three simultaneous perfect matchings.  A final
argument must prove a three-family Helly/coordination gate for an
independent triple, or directly switch any three-way-only obstruction.

## Verification

Run:

```sh
python3 collaboration/r0_three_ten_obstruction/verify_r0_incompatibility_graph.py
```

The standard-library verifier checks the \(K_{5,5}-e\) equality
arithmetic and canonical global graph, exhaustively confirms uniqueness
of both forced-core types under the stated edge and degree bounds, and
checks every clique-plus-isolates incompatibility graph and its
independence number.

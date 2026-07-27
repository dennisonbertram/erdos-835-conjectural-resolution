# Independent audit: the simultaneous 13-fan shadow

This note records an independently checked reduction associated with
Erdős--Rosenfeld problem #835.  It is a necessary induced shadow of a
17-colouring of \(J(32,16)\), not a colouring of the full Johnson graph and
not a solution of the open problem.

## 1. The 51,357-vertex induced shadow

Let

- \(V=U\mathbin{\dot\cup}A\), with \(|U|=19\) and \(|A|=13\);
- \(C\) be a labelled palette of 17 colours; and
- \(G_U\) be the subgraph of \(J(32,16)\) induced by
  \[
  X=\{S\in {V\choose16}: |S\cap U|\in\{15,16\}\}.
  \]

A labelled \(LS(2,3,19)\) is a map
\(L:{U\choose3}\to C\) for which the 17 triples through each pair receive
all 17 colours.  A labelled \(LS(3,4,20)\) on a 20-set \(W\) is a map
\(F:{W\choose4}\to C\) for which the 17 quadruples through each triple
receive all 17 colours.

### Induced-shadow theorem

A proper labelled 17-colouring of \(G_U\) is equivalent to the following
data:

1. for every \(a\in A\), a labelled \(LS(3,4,20)\)
   \(F_a\) on \(U\cup\{a\}\);
2. a common labelled \(LS(2,3,19)\) link \(L\), with
   \[
   F_a(\{a\}\cup T)=L(T)
   \quad
   (a\in A,\ T\in {U\choose3});
   \]
3. for every \(Q\in {U\choose4}\), the 13 values
   \[
   \{F_a(Q):a\in A\}
   \]
   are pairwise distinct.

The explicit assertion that \(L\) is an \(LS(2,3,19)\) is redundant once
the \(F_a\)'s are known to be large sets with the displayed common-link
condition, but it makes the reduction transparent.

#### Necessity

Let \(c\) be a proper 17-colouring of \(G_U\).  Define
\[
L(T)=c(U\setminus T)
\]
and, on \(W_a=U\cup\{a\}\), define
\[
F_a(R)=c(W_a\setminus R).
\]
Every 16-subset of \(W_a\) lies in \(X\), so this defines \(F_a\) on every
quadruple.  The 17 triples through a fixed pair of \(U\), after taking
complements in \(U\), form a 17-clique.  They are therefore rainbow and
give the \(LS(2,3,19)\) condition.  Similarly, the complements in \(W_a\)
of the 17 quadruples through any fixed triple form a 17-clique, so \(F_a\)
is an \(LS(3,4,20)\).  The common-link identity is literal:
\[
F_a(\{a\}\cup T)=c(U\setminus T)=L(T).
\]

For a fixed \(Q\in{U\choose4}\), all 17 extensions of the 15-set
\(U\setminus Q\) form another 17-clique.  Four of them are
\(U\setminus(Q\setminus\{x\})\), \(x\in Q\), and the remaining 13 are
\((U\setminus Q)\cup\{a\}\), \(a\in A\).  Hence their colours are all
different, proving condition 3 as well as the stronger fact
\[
\{F_a(Q):a\in A\}
=
C\setminus\{L(Q\setminus\{x\}):x\in Q\}.
\]

#### Sufficiency

Given the three kinds of data, colour \(X\) by
\[
c(U\setminus T)=L(T),\qquad
c((U\setminus Q)\cup\{a\})=F_a(Q).
\]
All possible adjacent pairs fall into exactly four cases:

1. \(U\setminus T\) and \(U\setminus T'\) are adjacent exactly when
   \(|T\cap T'|=2\), and \(L\) separates them.
2. Two vertices carrying the same \(a\) are adjacent exactly when their
   quadruples share a triple, and \(F_a\) separates them.
3. \(U\setminus T\) and \((U\setminus Q)\cup\{a\}\) are adjacent exactly
   when \(T\subset Q\).  These are the two quadruples
   \(\{a\}\cup T\) and \(Q\) in \(F_a\), so their colours differ.
4. Vertices carrying different \(a,b\in A\) are adjacent exactly when
   they carry the same \(Q\), and condition 3 separates them.

Thus the displayed construction is a proper colouring of all of \(G_U\).

### Exact induced-subgraph counts

There are
\[
{19\choose3}=969
\quad\text{and}\quad
13{19\choose4}=50,388
\]
vertices in the two layers, hence **51,357 vertices** in total.

The four edge classes are:

| class | count |
|---|---:|
| link--link | \(969\cdot48/2=23,256\) |
| link--fan | \(969\cdot(16\cdot13)=201,552\) |
| same-\(a\) fan--fan | \(50,388\cdot60/2=1,511,640\) |
| different-\(a\) fan--fan | \(3,876{13\choose2}=302,328\) |
| **total** | **2,038,776** |

A link vertex has degree \(48+208=256\).  A fan vertex has degree
\(60+4+12=76\).  Accordingly,
\[
969\cdot256+50,388\cdot76
=4,077,552
=2\cdot2,038,776.
\]

The full graph \(J(32,16)\) has
\({32\choose16}=601,080,390\) vertices.  The theorem therefore concerns
only the specified 51,357-vertex induced subgraph.

## 2. A fixed-link conflict graph

Fix a labelled \(LS(2,3,19)\), \(L\).  For
\(Q\in{U\choose4}\), its four face colours
\[
\{L(T):T\in{Q\choose3}\}
\]
are distinct because any two faces share a pair.  Define the allowed
cells
\[
\mathcal V_L=
\{(Q,c):Q\in{U\choose4},\
  c\notin\{L(T):T\in{Q\choose3}\}\}.
\]
Every \(Q\) allows 13 colours, so
\[
|\mathcal V_L|={19\choose4}\cdot13=\mathbf{50,388}.
\]

Define \(H_L\) on these cells by joining two distinct cells when either

- they have the same \(Q\), or
- they have the same \(c\) and their quadruples share a triple.

There are two types of 13-cliques:

- one \(Q\)-group for each of the 3,876 quadruples; and
- one \((T,c)\)-group for each
  \(T\in{U\choose3}\) and \(c\ne L(T)\), giving
  \(969\cdot16=15,504\) groups.

To see that a \((T,c)\)-group has size 13, write its possible quadruples
as \(T\cup\{x\}\), for the 16 choices \(x\in U\setminus T\).  For each of
the three pairs \(R\subset T\), the large-set condition supplies exactly
one \(x_R\) for which \(L(R\cup\{x_R\})=c\).  The three forbidden points
\(x_R\) are distinct: equality for two pairs would give the same colour
to two triples sharing a pair.  Exactly \(16-3=13\) cells remain.

Each cell belongs to five groups: its \(Q\)-group and its four
\((T,c)\)-groups.  The five groups through a cell intersect pairwise only
in that cell, and every edge belongs to exactly one group.  Consequently
\[
d(H_L)=5(13-1)=\mathbf{60}
\]
and
\[
|E(H_L)|
=\frac{50,388\cdot60}{2}
=\mathbf{1,511,640}.
\]

### Resolution equivalence

A simultaneous 13-fan over this fixed \(L\) is equivalent to a proper
labelled 13-colouring of \(H_L\), where graph-colour \(a\) denotes the
extension \(F_a\).

In the forward direction, put graph colour \(a\) on \((Q,c)\) when
\(F_a(Q)=c\).  Same-\(Q\) conflicts encode the cross-extension
all-different condition, while same-\(c\), shared-triple conflicts encode
the \(LS(3,4,20)\) condition within one extension.

Conversely, every 13-clique uses every graph colour.  A \(Q\)-group
therefore gives one value \(F_a(Q)\) for every \(a\).  For a fixed
\(T\subset U\), every \((T,c)\)-group, \(c\ne L(T)\), contains graph
colour \(a\) once.  Thus the 16 free quadruples through \(T\) use every
colour other than \(L(T)\) exactly once; adjoining
\(\{a\}\cup T\), coloured \(L(T)\), makes that triple star rainbow.
Triple stars containing \(a\) are rainbow directly from the
\(LS(2,3,19)\) property of \(L\).  This constructs every \(F_a\) and
recovers all three fan conditions.

Equivalently, \(H_L\) is the conflict (line) graph of the unrestricted
fixed-link exact-cover incidence system.  One fixed-link extension is a
maximum independent transversal; a 13-fan is a resolution of all allowed
cells into 13 such transversals.

## 3. The local Gram identity and what it does not prove

Let \(B\) be the \(19,380\times50,388\) zero--one matrix whose rows are
the constraint groups and whose columns are allowed cells.  Every column
has five ones.  Distinct columns have inner product one exactly when the
corresponding cells are adjacent, and otherwise have inner product zero.
Therefore, exactly,
\[
\boxed{A(H_L)=B^{\mathsf T}B-5I}.
\]

Positive semidefiniteness gives
\(\lambda_{\min}(H_L)\ge-5\).  Moreover,
\[
\dim\ker B\ge50,388-19,380=31,008>0,
\]
so \(-5\) is an eigenvalue and
\(\lambda_{\min}(H_L)=-5\), with multiplicity at least 31,008.

Since \(H_L\) is 60-regular, the Hoffman bounds give exactly
\[
\chi(H_L)\ge1-\frac{60}{-5}=13
\]
and
\[
\alpha(H_L)
\le
50,388\frac{5}{60+5}
=3,876.
\]
If a fixed-link \(LS(3,4,20)\) exists, its 3,876 chosen cells meet the
independence bound with equality.  A 13-fan would partition all 50,388
cells into 13 such equality cases.

This calculation exhausts only the least-eigenvalue Hoffman ratio bound.
It does **not** show \(\chi(H_L)=13\), construct an independent set, or
construct a fan.  A fuller spectral or eigenspace obstruction, Hoffman
equality structure, inertia, or a non-group clique larger than 13 could
still obstruct a 13-colouring.  Those broader spectral questions and the
existence of the required extensions remain open.

## 4. Reproducible check and provenance

Run:

```bash
python3 collaboration/h3_simultaneous_fan_audit/verify_simultaneous_fan_audit.py
```

The verifier is standard-library-only.  It reconstructs and verifies the
committed cyclic \(LS(2,3,19)\) certificate in
[`evidence/verify_defect_cross_link_lsts19.py`](../../evidence/verify_defect_cross_link_lsts19.py),
then independently derives every allowed cell, constraint group,
incidence overlap, graph count, Hoffman calculation, and induced-shadow
count used above.

The individual link facts were already implicit in
[`evidence/defect_cross_link_lsts19.md`](../../evidence/defect_cross_link_lsts19.md),
and the fact that a fixed free quadruple forbids its four face colours was
already used in
[`collaboration/opus5/cyclic_lsts19_extension_attack/NOTE.md`](../opus5/cyclic_lsts19_extension_attack/NOTE.md).
The simultaneous-common-link formulation, the 3,876 cross-copy
all-different constraints, the induced-subgraph converse, and the
13-colouring/resolution packaging are the new synthesis audited here.
This graph is not the residual graph of unused quadruples discussed in
[`evidence/ls_3_4_20_residual_graph.md`](../../evidence/ls_3_4_20_residual_graph.md).

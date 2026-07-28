# Claude Opus 5 max: the \(r=0\) cut-feasible selection and repair lemma

Work tool-free and independently.  Give a complete proof, a concrete
counterexample, or the earliest exact gap.  Do not assume a plausible switch
works globally without checking every cut it can damage.

## Exact setting

Let \(V\) have 13 vertices.  Six pairwise edge-disjoint prefix matchings have
sizes \(4,4,4,5,5,5\), union \(D\), and
\[
1\le d_D(v)\le5.
\]
Put \(G=K_{13}-D\).  The eleven remaining complement rows are seven triples
and four five-sets satisfying
\[
\rho(v)=d_D(v)-1.
\]
The support of row \(R\) is \(S_R=V\setminus R\).

A legal repair replaces one prefix matching by another perfect matching on
exactly the same support, avoiding the other five prefix layers.  It therefore
preserves every \(d_D(v)\) and every remaining row.

## Conditional input theorem

For this prompt, assume the following cut-sufficiency statement has been
proved separately:

> Three selected size-ten supports \(S_i=V\setminus R_i\) admit pairwise
> edge-disjoint perfect matchings in \(G\) whenever, for every \(U\subseteq V\),
> \[
> \sum_i\max(0,|S_i\cap U|-5)\le e(G[U]). \tag{C}
> \]

Do not spend the response reproving cut sufficiency.  Attack the selection
lemma needed to use it.

## Target

Prove or refute:

> **Cut-feasible repair-selection lemma.**  After at most one legal repair,
> some three of the seven remaining triple occurrences satisfy (C).

A proof would close coordinated-nine \(r=0\), conditional only on cut
sufficiency.  A counterexample must give all six prefix layers, all eleven
rows, and verify that every legal one-layer repair leaves every triple of the
seven size-ten occurrences violating some cut.

## Reductions already available

1. A support-preserving switch first removes every individual size-ten
   blocker.  The incompatibility graph on the seven triple occurrences is
   then
   \[
   K_t\mathbin{\dot\cup}(7-t)K_1,\qquad t\le6.
   \]
2. If \(t=6\), an existing solver-free equality theorem gives a legal
   two-edge trade after which any two clique occurrences coordinate with the
   seventh occurrence.  You may use this theorem, but must still verify (C)
   for the resulting selected triple or replace it with a direct argument.
3. If \(t\le5\), there is an independent three-set in the incompatibility
   graph, so each selected pair coordinates.  Pairwise coordination alone is
   not enough.
4. Every known pairwise-compatible bad triple in the nine regenerated
   support orbits violates (C).  One legal two-edge switch repairs each known
   full-row example.  This is evidence only.

## Small-cut reduction to exploit

For a triple complement \(R_i\),
\[
\phi_i(U)=|S_i\cap U|-5=|U|-5-|U\cap R_i|.
\]
Since \(\delta(G)\ge7\),
\[
e(G[U])\ge \left\lceil\frac{|U|(|U|-6)}2\right\rceil.
\]
Therefore every positive inequality (C) is automatic for \(|U|\ge9\), and
trivial for \(|U|\le5\).  Only \(|U|=6,7,8\) can matter.  Equivalently, every
six-set \(U\) must satisfy both
\[
\#\{i:R_i\cap U=\varnothing\}\le e(G[U]), \tag{6+}
\]
\[
\sum_i\max(0,|R_i\cap U|-1)\le e(G[V\setminus U]), \tag{6-}
\]
plus the possible size-eight equality case.  Audit this reduction before
using it.

A two-edge trade
\[
uv,ab\longmapsto ua,vb
\]
with \(u,v\in U\) and \(a,b\notin U\) increases both
\(e(G[U])\) and \(e(G[V\setminus U])\) by one.  The key difficulty is to prove
that repairing one tight cut does not create a violation on another cut.

## Required return

1. exact verdict on the cut-feasible repair-selection lemma;
2. complete proof or explicit counterexample if obtained;
3. a classification of minimal violating six/seven/eight-set cuts if useful;
4. earliest remaining gap, stated without optimism inflation.

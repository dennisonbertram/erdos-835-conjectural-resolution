# Claude Opus 5 max: full-row cut theorem via factor and colouring

Work tool-free and independently.  Return at most 20,000 tokens.  Give a
complete proof, a completely explicit counterexample, or the earliest exact
gap.  Do not repeat the weaker-ambient counterexample below as a target
refutation.

## Target setting

Let \(V\) have 13 vertices.  Six pairwise edge-disjoint prefix matchings have
sizes \(4,4,4,5,5,5\), union \(D\), and
\[
1\le d_D(v)\le5.
\]
Put \(G=K_{13}-D\).  There are seven remaining triple rows and four remaining
five-set rows satisfying
\[
\rho(v)=d_D(v)-1.
\]
Select three triple occurrences \(R_1,R_2,R_3\), with
\(S_i=V\setminus R_i\).  Assume for every \(U\subseteq V\)
\[
\sum_i\max(0,|S_i\cap U|-5)\le e(G[U]). \tag{C}
\]
The complementary inequality is already included by replacing \(U\) with
\(V\setminus U\).

Prove or refute:

> There are pairwise edge-disjoint perfect matchings
> \(M_i\subseteq G[S_i]\).

## Audited facts you may use

1. Only \(|U|=6,7,8\) can bind in (C).
2. Under the full row equation and (C), every \(G[S_i]\) is individually
   matchable.  The only ten-vertex Tutte survivors at minimum degree four
   are \(K_5\dot\cup K_5\), excluded by the row-incidence equation, and an
   independent six-set, excluded by (C).
3. The ambient statement without the eleven-row equation is false:
   \(D=K_{5,5}\cup P_3\), with the three omitted rows all the three vertices
   of \(P_3\), passes every cut but has
   \(G[S]=K_5\dot\cup K_5\).  The row equation excludes this because those
   three omitted vertices have total remaining incidence one.
4. A valid packing is equivalent to a subgraph \(H\subseteq G\) with
   \[
   d_H(v)=3-\#\{i:v\in R_i\}
   \]
   that has a proper three-edge-colouring in which colour \(i\) is missing
   exactly at the vertices of \(R_i\).

## Corrections to the previous run

Do not assume that (C), individual matchability, and a nonbinding parity cut
already produce the degree-constrained union \(H\).  That is a separate
\(b\)-factor or packing obligation.

Do not use
\[
e_D(U,V\setminus U)\le3
\]
as a lower bound.  A previous “deficit five” claim made that direction error
and is withdrawn.

## Required attack

Treat the following separately.

### F: factor existence

Does (C) plus the class-B row equation imply some simple
\(H\subseteq G\) with the displayed degrees?  Apply the exact
Tutte--Lovasz \(b\)-factor criterion if useful.  Translate every surviving
obstruction back to the three rows and the six prefix layers.

### E: prescribed three-edge-colouring

If such an \(H\) exists, can it always be chosen class 1 with the exact
missing-colour sets?  A generic subcubic graph need not be 3-edge-colourable,
so density or switching in the ambient \(G\) must be used.  State precisely
where.

If the theorem is false, a target counterexample must include:

1. all six prefix layers;
2. all eleven remaining rows satisfying every column equation;
3. the three selected rows;
4. verification of all cuts; and
5. a proof of nonpackability.

Return:

1. verdict on F;
2. verdict on E;
3. full target theorem or explicit counterexample if obtained;
4. earliest exact gap without optimism inflation.

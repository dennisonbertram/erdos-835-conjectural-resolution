# Claude Opus 5 max: prove or refute cut sufficiency for the \(r=0\) triple gate

Work tool-free and independently.  We need a rigorous proof, a concrete
counterexample, or the earliest exact gap.  Do not report a plausible sketch
as a theorem.

## Setting

Let \(V\) have 13 vertices.  Six pairwise edge-disjoint matchings have sizes
\(4,4,4,5,5,5\), union \(D\), and
\(1\le d_D(v)\le5\).  Put \(G=K_{13}-D\), so \(|E(G)|=51\) and
\(\delta(G)\ge7\).

There are seven triple rows and four five-set rows satisfying
\[
\rho(v)=d_D(v)-1.
\]
For a triple row \(R_i\), its size-ten support is \(S_i=V\setminus R_i\).

For three selected triple occurrences \(R_1,R_2,R_3\), define for every
\(U\subseteq V\)
\[
\phi_i(U)=|S_i\cap U|-5.
\]
Three edge-disjoint perfect matchings on \(S_1,S_2,S_3\) necessarily satisfy
\[
\sum_{i=1}^3\max(0,\phi_i(U))\le e(G[U]),\qquad
\sum_{i=1}^3\max(0,-\phi_i(U))\le e(G[V\setminus U]). \tag{C}
\]

## New exact observation

A previously cited orbit-4 obstruction has complements
\[
012,\quad012,\quad034
\]
and prefix
\[
\begin{array}{c|l}
C_0&06,24,9\,12,10\,11\\
C_1&01,37,58,10\,12\\
C_2&3\,12,5\,10,7\,11,89\\
C_3&03,15,7\,12,8\,10,9\,11\\
C_4&04,26,59,78,11\,12\\
C_5&02,16,57,8\,11,9\,10.
\end{array}
\]
It has no simultaneous triple.  The obvious dense six-set makes (C) tight,
but a complete independent audit found a different cut
\[
U=\{0,1,2,3,4,6\}
\]
with \((\phi_1,\phi_2,\phi_3)=(-2,-2,-2)\) and
\[
6>e(G[V\setminus U])=5.
\]
Thus the full cut family does detect this obstruction.  The earlier claim
that orbit 4 demonstrates insufficiency of (C) was wrong.

The disconnected all-35 obstruction is also detected by (C): a six-set
\(U\) has only two residual internal edges while all three selected rows
have \(\phi_i(U)=1\).

## Primary question

Prove or refute:

> **Cut-sufficiency conjecture.**  In the setting above, three selected
> size-ten supports admit pairwise edge-disjoint perfect matchings in \(G\)
> if and only if (C) holds for every \(U\subseteq V\).

You may use the special facts that \(D\) is the union of the six specified
matching layers and that the full eleven-row class-B equations hold.  State
clearly which hypotheses are actually used.

Promising proof forms include:

1. a Tutte/factor reformulation of the union of the three matchings;
2. a minimal-counterexample switching proof;
3. matching-polytope duality showing that every obstruction has a cut
   witness in this dense 13-vertex regime; or
4. a reduction to the already certified two-family gate.

If false, provide a completely explicit prefix \(D\), full eleven-row
inventory, the three rows, verification that all \(2^{13}\) cut inequalities
hold, and a proof that no matching triple exists.  If you cannot produce the
full class-B counterexample, distinguish weaker-ambient failures from target
failures.

## Secondary question

Assuming cut sufficiency, find the sharpest route to the coordinated-nine
\(r=0\) theorem:

> one prefix layer can be repacked on exactly the same support so that some
> three of the eleven remaining supports admit edge-disjoint perfect
> matchings.

In particular, can the row identity
\[
\sum_{\text{all 11 rows}}\phi_U(R)=e(G[U])-e(G[V\setminus U])
\]
force some triple of rows to satisfy (C), possibly after one
support-preserving alternating-cycle repair?

Return:

1. exact verdict on cut sufficiency;
2. complete proof or explicit counterexample if obtained;
3. exact lemma toward choosing a cut-feasible triple after repair;
4. earliest remaining gap.

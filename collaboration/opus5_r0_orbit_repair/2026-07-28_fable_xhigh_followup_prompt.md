# Claude Fable 5 xhigh follow-up: audit the \(r=0\) proof route

Independently audit the following finite theorem strategy.  Do not assume the
conclusion.  Return either a proof, a concrete counterexample, or the earliest
precise gap.

## Target

Let \(V\) have 13 vertices.  Six pairwise edge-disjoint prefix matchings have
sizes \(4,4,4,5,5,5\), union \(D\), and \(1\le d_D(v)\le5\).  The eleven
remaining complement rows comprise seven triples and four five-sets and obey

\[
\rho(v)=d_D(v)-1.
\]

The support of a row \(R\) is \(V\setminus R\).  We want to prove that one
prefix layer can be repacked on the same support so that some three of the
eleven remaining supports have edge-disjoint perfect matchings avoiding the
repaired prefix.

## Proposed exact CEGIS theorem

The base CNF \(B\) encodes every such prefix and all eleven rows exactly.  For
each repair layer \(i\), let \(o_{i,e}\) mean that edge \(e\) is used by one of
the other five prefix layers.  A semantic witness \(W\) contains:

1. a replacement perfect matching \(P\) on exactly the old support of layer
   \(i\);
2. three distinct remaining rows with their exact complements; and
3. three mutually edge-disjoint perfect matchings \(N_0,N_1,N_2\) on those
   supports, also edge-disjoint from \(P\).

Put \(E^*=P\cup N_0\cup N_1\cup N_2\).  The witness works for every base
assignment having the same support for layer \(i\), the same three complement
rows, and \(o_{i,e}=0\) for every \(e\in E^*\).  Add the single clause negating
that conjunction.  Repeatedly solve \(B\), find witnesses for each model, and
add their clauses.  If the accumulated ordinary CNF becomes UNSAT and a
freshly generated DRAT proof independently replays, the proposed conclusion
is that every valid prefix has a one-layer repair and three-colour extension.

Audit the quantifier order very carefully.  Is this finite witness-cut
procedure sound as a proof of

\[
\forall P_{\rm input}\ \exists(P_{\rm repair},N_0,N_1,N_2)?
\]

If sound, state a short formal proof.  If not, give a literal failure mode.

## Opus cut invariant

Let \(G=K_{13}-D\).  For \(U\subseteq V\), \(W=V\setminus U\), and a remaining
row \(R\) with support \(S\), define

\[
\phi_U(R)=|S\cap U|-|S|/2.
\]

If a matching realizing \(R\) has \(k\) edges in \(U\), \(m\) edges in \(W\),
and \(c\) crossing edges, then

\[
\phi_U(R)=k-m.
\]

For edge-disjoint realizations of selected rows,

\[
\sum_R\max(0,\phi_U(R))\le e(G[U]),\qquad
\sum_R\max(0,-\phi_U(R))\le e(G[W]).
\]

Across all eleven remaining rows,

\[
\sum_R\phi_U(R)=e(G[U])-e(G[W]).
\]

Therefore the support inventory alone gives

\[
e(G[U])\le
\min\left\{\binom{|U|}{2},\frac{51+\sum_R\phi_U(R)}2\right\}
\]

and the analogous bound for \(W\).  Audit every identity and tell us whether
it can be strengthened to a sufficient condition for three matchings in this
special \(13\)-vertex profile.  We already know a bad triple with a
12-edge six-core for which the basic cut bound is tight but no simultaneous
triple exists, so any claimed sufficiency must address cross-edge
system-of-distinct-representatives obstructions.

## Known evidence

An exact CEGIS implementation currently has 10,992 variables and 44,477 base
clauses.  A 120-second discovery run added 1,752,064 valid witness cuts and
found neither an UNSAT result nor a no-repair counterexample.  This is search
evidence only.

End with:

1. verdict on witness-cut soundness;
2. verdict on the cut invariant;
3. strongest new lemma you can prove;
4. exact remaining gap.

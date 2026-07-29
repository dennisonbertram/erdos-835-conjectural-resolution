# Claude Opus 5 max: settle the full-row \(r=0\) cut-sufficiency theorem

Work tool-free and independently. Return at most 20,000 tokens. Give a
complete proof, a complete explicit counterexample, or the earliest exact
gap. Do not restate general matching theory unless you instantiate every
condition in this thirteen-vertex setting.

## Exact setting

Let \(V\) have thirteen vertices. Six pairwise edge-disjoint prefix
matchings have sizes
\[
4,4,4,5,5,5,
\]
union \(D\), and
\[
|D|=27,\qquad 1\le d_D(v)\le5.
\]
Put \(G=K_{13}-D\).

The eleven remaining complement-row occurrences are seven triples and four
five-sets satisfying the exact column equations
\[
\rho(v)=d_D(v)-1.
\]
Select three of the triple rows \(R_1,R_2,R_3\), put
\[
S_i=V\setminus R_i,\qquad |S_i|=10,
\]
and assume every internal-edge capacity cut
\[
\boxed{\quad
\sum_{i=1}^3\max(0,|S_i\cap U|-5)\le e(G[U])
\quad(U\subseteq V).\quad} \tag{C}
\]

## Target

Prove or refute:

> **Full-row cut sufficiency.** Under all hypotheses above, \(G[S_1]\),
> \(G[S_2]\), and \(G[S_3]\) have pairwise edge-disjoint perfect
> matchings.

A proof closes coordinated nine at \(r=0\), because a separate
solver-free theorem now proves that after at most one legal prefix repair
some three of the seven triple rows satisfy (C).

## Audited facts you may use

1. Only cuts of sizes \(6,7,8\) can bind. Cuts of sizes at most five are
   trivial and sizes at least nine are automatic from \(d_D\le5\).
2. Under the full row equations and (C), each \(G[S_i]\) is individually
   matchable.
3. A certified pair theorem says that two live size-ten families fail to
   coordinate only if they share a forced edge arising from a \(K_6-e\)
   or \(K_{5,5}-e\) deletion core. In the full row setting,
   \(K_{5,5}-e\) cannot certify an incompatible pair. Condition (C)
   excludes the shared \(K_6-e\) pair obstruction. Thus every selected
   pair coordinates.
4. For
   \[
   t(v)=|\{i:v\in R_i\}|,\qquad b(v)=3-t(v),
   \]
   any desired union \(H=M_1\cup M_2\cup M_3\) has
   \(d_H(v)=b(v)\) and \(b(V)=30\). The elementary degree-capacity
   inequality
   \[
   b(X)\le b(V\setminus X)+2e(G[X])
   \]
   is implied by (C). This elementary slice is not the full
   Tutte--Lovász \(b\)-factor criterion.
5. If such an \(H\) is properly edge-coloured with the prescribed three
   colours, every component \(C\) obeys
   \[
   |C\cap S_i|\equiv0\pmod2\quad(i=1,2,3).
   \]
   This is necessary, not already sufficient.

## Known failed routes to avoid

- The claim \(\alpha(G)\le5\) is false: valid saturated \(K_6\) prefix
  certificates exist.
- Individual matchability plus pairwise coordination does not imply the
  simultaneous triple in general.
- The elementary \(b\)-Hall inequality is not the complete
  Tutte--Lovász criterion.
- A weaker-ambient counterexample exists:
  \(D=K_{5,5}\mathbin{\dot\cup}P_3\), with all three selected rows equal
  to the \(P_3\) vertex set. It satisfies all cuts but cannot even match
  one support. It cannot be completed to the exact full row inventory,
  so it does not refute the target.
- Do not assume every obstruction is \(K_6-2K_2\), that rows are
  distinct, or that a plausible alternating switch preserves all three
  supports.

## Suggested proof interfaces

You may choose any route, but make it checkable:

1. apply the full Tutte--Lovász \(b\)-factor theorem and eliminate every
   disjoint-set/odd-component obstruction using (C), the exact eleven-row
   ledger, and \(d_D\le5\); then prove the prescribed 3-edge-colouring;
2. take a maximal pairwise-disjoint choice of three near-matchings and use
   alternating paths/cycles to derive a violated cut (C);
3. reduce the prescribed-colour problem to a single ordinary matching or
   flow instance with an explicit gadget and prove that (C) is the complete
   Tutte/Hall family for that gadget; or
4. construct a full exact counterexample: list all six prefix layers, all
   eleven rows, verify the column equations and every one of the
   \(2^{13}\) cuts, and prove no simultaneous triple exists.

The three selected triples have only sixteen Venn types modulo row and
vertex permutation. A valid proof may use a finite case lemma, but every
case and reduction must be explicit enough for an independent verifier.

## Required return

1. exact verdict on full-row cut sufficiency;
2. complete derivation or explicit counterexample;
3. if using a factor theorem, write its precise instantiated hypotheses and
   show every one is met;
4. if using edge-colouring, prove the prescribed missing-colour condition,
   not merely ordinary 3-edge-colourability;
5. earliest remaining gap without optimism inflation.

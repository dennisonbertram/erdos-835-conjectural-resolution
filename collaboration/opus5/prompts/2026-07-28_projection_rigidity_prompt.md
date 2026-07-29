# Opus 5 maximum-effort attack: two-valued top-module projections for #835

Date: 2026-07-28

You are Claude Opus 5 at maximum reasoning effort. Invoke
`/efficient-frontier` first if available. Cost is not a stopping condition.

## Full objective

Resolve Erdős--Rosenfeld Problem #835:

> Does there exist any \(k>2\) with
> \(\chi(J(2k,k))=k+1\), equivalently an
> \(LS(k-1,k,2k)\)?

A positive answer needs one complete construction. A negative answer must
cover every \(k>2\), not merely \(k=16\).

## Exact attack surface

After the prime sieve, put \(q=k+1=p\), with \(p\) an odd prime and \(k\)
even. A hypothetical colouring is equivalently a covering projection

\[
O_k=KG(2k-1,k-1)\longrightarrow K_q.
\]

Let \(N=\binom{2k-1}{k-1}\), let \(x_a\) be the indicator of colour fibre
\(a\), and put \(y_a=x_a-q^{-1}{\bf1}\). The \(y_a\) form a regular simplex
inside the \(-1\) eigenspace \(E_{k-1}\) of \(O_k\). If \(W\) is their
\(k\)-dimensional span and \(P_W\) its orthogonal projector, then

\[
P_W(u,v)=
\begin{cases}
k/N,&c(u)=c(v),\\
-1/N,&c(u)\ne c(v).
\end{cases}
\]

Thus \(P_W\) is a rank-\(k\), two-valued orthogonal projection contained in
the top Specht/Johnson module, with \(AP_W=-P_W\). Conversely such a
projection, if its \(k/N\) relation has exactly \(q\) equivalence classes,
recovers the colouring.

Personally determine whether this projection formulation yields:

1. a uniform nonexistence theorem for all even \(k>2\);
2. a construction for one prime-form \(k\); or
3. a genuinely new, rigorously proved rigidity lemma that sharply reduces
   the full problem.

Do not stop at the elementary spectral identities above. Push Schur closure,
integral lattices, modular reduction at \(p\), primitive idempotents,
Terwilliger constraints, and the equivalence-relation condition. In
particular investigate the entrywise identity forced by two values,

\[
P_W\circ P_W
=\frac{k-1}{N}P_W+\frac{k}{N^2}J,
\]

and all consequences of simultaneously having \(P_W^2=P_W\),
\(P_W\in E_{k-1}\operatorname{Mat}E_{k-1}\), and the \(0/1\) equivalence
relation matrix \((N P_W+J)/q\).

## Avoid duplicating known dead ends

Read the relevant current record before deciding what is new:

- `README.md`;
- `erdos_835_conjectural_resolution.md`;
- `collaboration/opus5/joint_schreier_krein_attack/NOTE.md`;
- `collaboration/opus5/staircase_support_frontier/NOTE.md`;
- `collaboration/general_h1_rigidity/README.md`;
- `collaboration/general_h2_rigidity/README.md`;
- `collaboration/schreier_h3_support/README.md`;
- `collaboration/schreier_h4_support/README.md`;
- `collaboration/fable_e4_v2/JUDGMENT.md`;
- `collaboration/fable_e4_v2/PROOF.md`.

A recent general source that may or may not add anything is Bailey--Cameron--Zhou,
“Equitable partitions of regular graphs, and perfect sets in normal Cayley
graphs,” arXiv:2605.17376. Its general Theorem 2.3/Corollary 2.4 compares two
equitable partitions. Check whether applying it to the colour partition and
the Odd-graph distance/Johnson orbit partitions is strictly stronger than the
already committed design quadrature; do not claim novelty if it is the same
linear condition.

## Proof standard

- A solver status, bounded search, or restricted ansatz is not a solution.
- Prove every equivalence and quantifier.
- If computation supports a finite claim, produce a complete standard-library
  verifier or a replayable certificate and identify its exact scope.
- Explicitly test any proposed theorem against the \(k=6\) Witt-design
  constituent control and explain why the distinction between one perfect
  code and a partition into \(k+1\) perfect codes matters.
- Label conjectures and failed routes as such.

## Deliverable

Work only inside:

`collaboration/opus5/projection_rigidity_attack_2026-07-28/`

Create:

- `STATUS.md` -- verdict, strongest new result, and exact remaining gap;
- `PROOF.md` -- complete arguments only;
- `IDEAS.md` -- unproved ideas and exact failure boundaries;
- any verifier scripts needed.

Include the headings:

- `Independent audit surface`
- `Scope relative to the full #835`
- `Why this does or does not prove the full problem`

Do not edit existing files, do not include secrets or account data, and do
not expose raw internal reasoning.

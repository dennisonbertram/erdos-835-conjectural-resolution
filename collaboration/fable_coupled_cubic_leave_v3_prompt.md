# Claude Fable xhigh assignment: coupled cubic-leave obstruction or witness

Invoke `/efficient-fable` first and apply it to this self-contained reasoning
task. Use maximum reasoning effort, but keep the context concentrated on the
equations below. Cost is not a stopping condition.

This is a self-contained one-shot reasoning assignment. You have no file or
shell tools in this run. Do not announce a plan to inspect repository files,
attempt tool calls, or ask for more context: all facts you may rely on are
stated below. Spend the turn doing the mathematics and return a substantive
final answer.

The full objective is Erdős–Rosenfeld Problem #835: determine whether any
\(k>2\) has an \(LS(k-1,k,2k)\). A construction for one \(k\) resolves the
existential problem. A nonexistence result only at \(k=16\) closes the first
open case but is not the full general theorem.

Your core assignment is an exact two-layer necessary object for the
\(k=16\) case.

## Coupled cubic-leave target

Let \(D\) be the \(120\times560\) edge-versus-triple incidence matrix of a
16-set. Seek zero-one matrices
\[
G_2\in\{0,1\}^{120\times120},\qquad
G_3\in\{0,1\}^{560\times560}
\]
such that:

1. every row of \(G_2\) is a perfect matching of \(K_{16}\), and every
   column is a perfect matching;
2. the 15 row matchings indexed by edges through any fixed point form a
   one-factorization, and dually for columns;
3. with independent copies \(D_B,D_C\),
   \[
   D_BG_3+G_2D_C=J,\qquad
   D_CG_3^{\mathsf T}+G_2^{\mathsf T}D_B=J. \tag{1}
   \]

For every column triple \(F\), its three \(G_2\) matchings form a cubic
graph \(H_F\), and the corresponding column of \(G_3\) is a
32-triangle decomposition of \(K_{16}-H_F\). The same must hold in the row
direction using one common \(G_3\). Individually every cubic leave on 16
vertices can occur, so only the simultaneous coupling has leverage.

A proof that no \((G_2,G_3)\) satisfies (1) rules out even this truncation
and therefore rules out \(S(15,16,32)\). A witness proves only two-layer
feasibility, not a global colouring.

## Equivalent constructive boundary

In the fixed cyclic radius-five ansatz, 105 prescribed-link
\(LS(2,3,19)\) slices are separately feasible. They become one radius-five
witness only if their shared trace values satisfy, for every
\(uv\in\binom{16}{2}\) and every index \(i\),
\[
\{Q_{ij}(u,v,\infty):j\ne i\}
=\mathcal C\setminus\{M_i(uv),L_i(u),L_i(v)\}. \tag{2}
\]
Independent slice completions do not imply (2). Even a valid radius-five
witness remains local and is not a global Odd-graph cover.

## Closed or unsafe shortcuts

- The generic radius-four ball is exactly feasible.
- Separately feasible cubic leaves, 105 separate prescribed-link slices,
  bounded solver `UNKNOWN`, or failure of a cyclic seed prove nothing about
  (1).
- Rank and ordinary row/column sums are consistent:
  \(G_2\) is degree eight and \(\operatorname{rank}_{\mathbb Q}G_2\le105\).
- The average overlap of disjoint \(G_2\) rows is \(8/13\), so a
  constant-Gram or association-scheme assumption is false at this
  parameter.
- Any parity/moment identity must be checked for whether it is merely a
  linear combination of (1).

## Required work

Try both directions:

1. derive a genuine obstruction from (1), preferably via integral
   divisibility, Smith form, mod-2/mod-3 rank, triangle-space homology,
   determinant/Pfaffian orientation, or a double count that uses both
   equations simultaneously;
2. or construct a full \((G_2,G_3)\), or a simultaneous cyclic trace
   satisfying (2), with a compact exact certificate and semantic verifier.

Use \(k=4\) and \(k=6\) controls. Prove that any proposed invariant is not
already forced tautologically by (1). Solver output counts only with a
complete model and replayable certificate.

Return a complete proof/witness if found. Otherwise return the strongest
new unconditional lemma with proof, the exact failure boundary, and the next
finite certificate-producing computation. Label every conjecture.

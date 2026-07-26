# Decisive sign head: independently constrain the partial-fiber product

Formula (F) and the exact completion equations (8)--(10) are now certified.
Use:

- `evidence/odd_graph_local_ball/flag_at_exact_formula.md`
- `evidence/odd_graph_local_ball/radius4_dual_trace_forced.md`
- the three independent audit scripts already on disk.

Fix the induced orders from those notes and set
\[
 H(L,M,N)=\prod_{i,u}\prod_{x\ne L_i(u)}
              \operatorname{sgn}\Phi_{i,u,x},
\]
where each partial bijection has its induced domain/codomain order.  Let
\[
 E(L,M)=\prod_{i,u}\prod_{x\ {\rm generic}}
          \varepsilon(v_M(i,u,x),v_L(i,u,x))
\]
be the computable generic hole-orientation product in equation (10).
Because the fixed per-flag completion factor is repeated over the even number
\(k(k-1)\) of flags, equations (1), (7), and (10) already imply the rigorous
necessary identity
\[
 \boxed{H(L,M,N)=
 E(L,M)\,(-1)^{k(k-1)/2}\operatorname{AT}(T)
 \prod_i\delta(S_i).}\tag{H}
\]
(Division by \(E=\pm1\) is multiplication.)  Thus it is imprecise to call the
global value of \(H\) unevaluated: conditionally, (H) determines it from
\(L,M\).  What is genuinely missing is an **independent** theorem from one or
both forced fiberings.

Wallis control with the current finite order gives \(E=+1\) (1,680 negative
generic hole pairs out of 3,360), RHS(F)=+1, hence required \(H=+1\).
Independently recheck this.

## Heavy-lifting task

1. Prove (H) carefully and compute \(E\), RHS(F), and required \(H\) on:
   - every labelled \(k=6\) radius-3 family and every choice of distinguished
     root colour;
   - the Wallis \(k=16\) family.
   Keep radius-3 controls explicitly separate from actual radius-5 witnesses.

2. Re-express \(H\) in each fibering:
   - per \(ij\): signs of the partner maps at vertices \(u\) across the
     perfect/near-perfect \(D_x^{ij}\) matchings;
   - per \(uv\): signs of partner maps at indices \(i\) across the forced
     matchings of \(N_{uv}\).
   Track all hole cofactors.  Look for a parity theorem forced by either
   one-factorization family, their union cycles, or their shared \(N\)-table.

3. Falsify aggressively.  Build exact one-sided synthetic tables satisfying
   only the per-\(ij\) constraints, and separately only the per-\(uv\)
   constraints, at the smallest feasible even orders.  If both signs of the
   proposed invariant occur, record a concrete counterexample and prove that
   fibering alone cannot decide \(H\).  Then test the strongest jointly
   feasible relaxation available.

4. A result excludes unrestricted \(k=16\) only if the independent theorem
   forces a value incompatible with (H) for **every** admissible \(L,M\).
   Failure on Wallis alone excludes only that chart.  Do not call a universal
   Latin identity an independent evaluation.

Export a theorem or exact no-go note and a stdlib verifier.  Label PROVED,
COMPUTATION, CONJECTURE, OPEN.  No claim that #835 is solved unless the
unrestricted contradiction or a global construction is complete.

# Opus 5 second pass: turn the layer signal into a theorem

Your first-pass verifier is soundly scoped, but it leaves the decisive head
open. Continue at xhigh effort and export a mathematical note as well as code.

Priority:

1. Prove or refute a general formula for the infinity-layer product
   \(H_\infty\), for arbitrary even \(k\), arbitrary one-factorization
   \(\Psi\) of \(K_k\), and every two-sided compatible family
   \(D^{ij}\). Do not infer a theorem from the \(k=4,6\) census. Factor the
   global corner permutation through the coloured cells, or use Pfaffian
   orientations, and track induced-order cofactors exactly.
2. Enumerate more than the standard \(\Psi\) at the smallest feasible
   parameter, especially both parity classes of one-factorizations at \(k=8\),
   and determine whether \(H_\infty\) depends on \(D\), on \(\Psi\), or only
   on \(k\).
3. Generalize the corner-regrouping formula to the finite layers with their
   genuine one- and three-index holes and zero- or two-vertex holes. Seek an
   exact product over all \(k+1\) colours. State every residual term.
4. Revisit root-colour coupling structurally. A negative result needs an
   explicit transformation law showing that the independently evaluated
   layer product changes consistently; variation of `H_required` alone is not
   proof that no coupling exists.
5. Cross-check the concurrently developing exact-trace work under
   `collaboration/global_h_parity/` once stable.

Export:

- `collaboration/opus5/full_n_sign/NOTE.md`
- any updated assertion-enabled standard-library verifier(s)

Keep synthetic layers, full shared \(N\), a radius-five ball, and a global
colouring sharply separated. Do not claim a solution of #835 without an
unrestricted construction or contradiction.

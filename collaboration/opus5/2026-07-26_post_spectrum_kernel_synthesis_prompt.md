# Opus 5 xhigh: unrestricted post-spectrum/kernel synthesis

Continue the attempt to resolve Erdős--Rosenfeld Problem #835.  Work only on
the exact unrestricted \(k=16\) problem; do not substitute a symmetric,
cyclic, determinantal, Plücker, or finite-radius ansatz.

Read these current verified artifacts first:

1. `collaboration/schreier_spectrum_obstruction/README.md`
2. `collaboration/schreier_spectrum_obstruction/verify_schreier_spectrum_obstruction.py`
3. `collaboration/hadamard_kernel_attack/README.md`
4. `collaboration/opus5/hadamard_kernel_followup/NOTE.md`
5. `collaboration/fable_hadamard_kernel/2026-07-26_fable_note.md`
6. Sections 7.3--7.4 of `erdos_835_conjectural_resolution.md`

The two exact frontiers are:

- For the one-fibre intersection-one graph,
  \[
  \operatorname{Spec}(R)
  =\{120^1,(-97)^{30},77^{434}\}\uplus\Lambda,\qquad
  \Lambda\subseteq[-83,82],
  \]
  and
  \[
  R^2=120I+5A_{13}+Q,
  \]
  with \(Q\) supported on intersection twelve, entries \(0,1,2,3\), and
  row sum \(10080\).

- Deleting one colour class forces a \(15\)-dimensional nondegenerate
  constant-Hadamard-product subspace, equivalently a coherent system of
  \(I+J\) simplex frames.  Linear rank is far too weak after derivation.

Try to close the unrestricted case.  In particular, investigate both of
these concrete possibilities before choosing the stronger one:

1. Use the Johnson/association-scheme intersection algebra, integrality,
   Krein positivity, Schur products of the forced \(-97\) and \(77\)
   modules, or higher compressed Odd moments to prove that no residual
   module \(\Lambda\) and no \(Q\) can satisfy all constraints.
2. Use the nondegenerate frame formulation to prove a universal quadratic
   capacity bound below \(15\), preferably already for every member of a
   derived \(LS(4,5,21)\) or \(LS(3,4,20)\).  The gluing across shared
   evaluations, not raw kernel dimension, is the target.

You may use agents and exact computations to discover identities, but a
resolution must end in a self-contained proof or a fully checkable finite
certificate.  Audit every normalization and test \(k=2,4,6\) controls.
Explicitly distinguish PROVED, EXACT COMPUTATION, HEURISTIC, and OPEN.
Do not revive the vacuous complement/clique corollary or the refuted
\(\dim\ker M_D=|D|/2\) guess.

Export all work to
`collaboration/opus5/post_spectrum_kernel_synthesis/`, including a note and
dependency-light verifier(s).  If no contradiction or construction is
obtained, give the strongest new exact theorem and identify the single
missing implication.  State unambiguously whether \(k=16\) and #835 are
settled.

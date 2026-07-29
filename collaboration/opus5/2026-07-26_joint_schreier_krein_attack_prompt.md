# Opus 5 prompt: joint \(Q\)-leakage attack after the \(H_2\) support theorem

Work as the principal mathematical researcher on Erdős--Rosenfeld Problem
#835.  We still need a genuine unrestricted proof or construction.  Do not
restate old reductions and do not treat a negative result for \(k=16\) as a
solution of the full existential problem.

Assume for contradiction that a cover
\[
O_{16}=KG(31,15)\longrightarrow K_{17}
\]
exists.  Fix one fibre \(C\), of size \(17\,678\,835\).  The committed notes
`collaboration/schreier_spectrum_obstruction/README.md` and
`collaboration/schreier_krein_followup/README.md` prove the following exact
facts.

* \(R\) is the \(120\)-regular graph joining fibre blocks with intersection
  one.
* \(P_2\) is the orthogonal projector onto the forced
  \(434\)-dimensional pair-harmonic module, and
  \(RP_2=P_2R=77P_2\).
* \(A_{13}\) and \(A_{12}\) join fibre blocks with the indicated
  intersections.
* There is a symmetric matrix \(Q\) such that
  \[
  R^2=120I+5A_{13}+Q,
  \]
  with \(Q\) supported on \(A_{12}\), entries in
  \(\{0,1,2,3\}\), and row sum \(10080\).
* The exact compressions are
  \[
  P_2A_{13}P_2=449P_2,\quad
  P_2A_{12}P_2=5148P_2,\quad
  P_2QP_2=3564P_2.
  \]
* For every unit \(x\in\mathcal H_2\), its zero extension has global Odd
  spectral measure
  \[
  \frac1{17}\delta_{14}
  +\frac{29}{85}\delta_{-3}
  +\frac4{15}\delta_2
  +\frac13\delta_{-1},
  \]
  equivalently the exact quartic annihilator stated in the follow-up note.

The next concrete target is joint information about \(R,Q,A_{13}\), not
another scalar Krein calculation.  In particular,
\[
 (I-P_2)QP_2=-5(I-P_2)A_{13}P_2.
\]

Do the heavy mathematical lifting on this target:

1. Independently rederive every identity you use; flag any hidden invariance
   assumption.
2. Compute the exact Frobenius/operator leakage information that the
   Steiner \(14\)-design and the known Johnson kernels force for
   \[
   L=(I-P_2)A_{13}P_2.
   \]
   Determine whether \(\operatorname{tr}(P_2A_{13}^2P_2)\), or a sharp bound
   on it, is obtainable from the forced intersection data.
3. Combine the leakage identity with the entry constraints on \(Q\).  Push
   through \(P_2Q^2P_2\), mixed products such as
   \(P_2A_{13}QP_2\), rowwise Cauchy/variance inequalities, and the smallest
   useful positive-semidefinite block moment matrix.  Seek an exact
   contradiction at \(k=16\), not a numerical suggestion.
4. Use the known \(k=6\) derived-Witt cover as a normalization control
   wherever the same formula applies.
5. Do not infer Loewner order from entrywise inequalities.  Do not assume
   that \(A_{13}\) or \(Q\) preserves \(\mathcal H_2\); prove invariance if
   needed.
6. If this attack cannot contradict the cover, prove the strongest precise
   no-go theorem for the whole quadratic-leakage class and identify the
   first genuinely unforced mixed statistic.  A rigorous closure of a dead
   end is valuable, but “the bounds overlap” is not enough without a proof
   of exactly what was exhausted.
7. If a contradiction emerges, continue all the way to a publication-ready
   proof and independently check each finite calculation.  Remember that
   excluding \(k=16\) alone still would not settle existential Problem #835.

Write a self-contained research note to
`collaboration/opus5/joint_schreier_krein_attack/NOTE.md` and put any exact,
deterministic verifier beside it.  State the final scope in unmistakable
language.  Erdős--Rosenfeld #835 remains open unless you have supplied a
complete all-parameter proof or a valid construction.

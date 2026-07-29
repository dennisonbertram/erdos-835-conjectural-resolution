# Opus 5 xhigh follow-up: unrestricted attack after four route closures

We are still solving Erdős–Rosenfeld Problem #835:

> Does some \(k>2\) satisfy
> \[
> \chi(J(2k,k))=k+1?
> \]

Equivalently, does an \(LS(k-1,k,2k)\) exist?  Ma--Tang forces
\(p=k+1\) prime, and \(k=16\) is the first open case.

The answer must concern the unrestricted problem.  A restricted ansatz
refutation is not a solution, and a local relaxation witness is not a
coloring.

## New exact closures you must take as the current checkpoint

1. **Total two-sided layer sign is redundant.**  The exact finite and
   infinity layer formulas combine to
   \[
   H=(-1)^{\binom{k}{2}}\Sigma(T)\prod_x P(\Psi^x),
   \]
   and Pfaffian reduction gives
   \[
   \prod_xP(\Psi^x)=(-1)^{\binom{k}{2}}\prod_i\delta(S_i).
   \]
   Hence the total sign is identically the already-known
   \(F(L,M)\).  It gives no new obstruction.

2. **The individual layer XOR cuts appear logically redundant.**  Each
   \(P(\Psi^x)\) can be written as an explicit quadratic XOR in the
   \(N\)-variables, but no-hole augmentation appears to force the target
   already.  An independent package is still being audited.

3. **Single maximal-minor colorings are closed for every admissible
   \(k>2\).**  The \(p\equiv1\pmod4\), \(p\equiv3\pmod8\), and now
   \(p\equiv7\pmod8\) cases are all impossible.  This does not touch
   ratios or tuples of Plücker coordinates.

4. **The unrestricted free-\(F\), full-reorder, re-based five-point
   linear relaxation at \(k=16\) is exactly feasible.**  A rational
   certificate passes 441,905 equalities and 5,118,391 coefficients.
   Thus that LP obstruction is dead; the certificate is not a coloring.

5. Exact full searches remain live with no verdict: generic radius 4
   plus forced trace, generic radius 5, Wallis shared \(N\), and
   \(LS(3,4,20)\) searches.

## Heavy-lifting request

Choose one genuinely unrestricted route and push it to a concrete theorem
or construction.  Highest-value choices:

- a coloring formula using a ratio or small tuple of Plücker coordinates,
  with a complete collision analysis;
- an exact root-change/monodromy invariant for a genuine global
  \(O_{16}\to K_{17}\) covering that does not collapse to the total sign;
- a finite complete reduction materially smaller than the current generic
  radius-4 CNF, with a proof that every global cover is represented;
- or an explicit \(LS(15,16,32)\) construction with an independently
  checkable certificate.

Do not spend the response recapping the checkpoint.  Work the mathematics.
Try to falsify your own candidate at small \(k\) and on the Wallis chart.
If a conjecture fails, record the smallest exact counterexample and pivot.

Export a self-contained note and verifier under
`collaboration/opus5/unrestricted_post_closure/`.  State the exact logical
scope at the top and bottom: whether it solves #835, proves only a
restricted theorem, or closes only an obstruction route.  Do not commit.

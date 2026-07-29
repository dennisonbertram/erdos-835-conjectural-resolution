# Claude Opus 5 maximum-effort assignment: solve Erdős–Rosenfeld #835

You are the principal mathematical investigator. Work at maximum reasoning
effort and use the efficient-frontier skill. Cost is not a stopping
condition. Work on the full existential problem:

> Does any \(k>2\) admit a tight \((k+1)\)-colouring of \(J(2k,k)\)?

Equivalently, does any \(LS(k-1,k,2k)\) exist? A positive construction for
one \(k\) solves the problem. A negative solution must cover every \(k>2\),
not merely the first open case \(k=16\).

Read `README.md` first and preserve its honest scope. Then inspect only the
frontier artifacts relevant to your chosen attack. Current exact state:

1. Divisibility forces \(k=p-1\) with \(p\) prime. Known results exclude
   \(k\le14\); \(k=16\) is first open and \(k=18\) is next.
2. At \(k=16\), the complete generic radius-four ball of
   \(O_{16}\to K_{17}\) is SAT, with an independently checked assignment to
   all 738,537 clauses. Radius five is the first possible local obstruction.
3. The full free-\(F\), all-position-reorder, re-based five-point necessary
   LP is exactly feasible. An independent rational checker passed 441,905
   equalities and 5,118,391 nonzero coefficients. This closes that LP route.
4. The quotient by
   \((e_1,e_2,e_3,e_4,e_8+e_1^8)\) contains an explicit actual-edge
   \(K_{18}\), so every arbitrary postprocessing of these five statistics
   still needs at least 18 colours. The witness uses only three 15-set masks
   and is being independently packaged. Do not mistake this restricted
   no-go for a theorem about arbitrary colourings.
5. The matching-cube projected cubic, triple-polytabloid support, first
   overlap-sensitive 2-adic lift, scalar sign, proposed Norton \(1/3\) gap,
   and projected fourth-moment shortcuts all close consistently. The
   unprojected fourth-moment residual is PSD, but equality is equivalent to
   recovering the original colouring.
6. For each fixed pair \(ij\), the radius-five boundary equations are
   exactly a boundary-prescribed large set of 17 disjoint \(STS(19)\)s.
   The missing issue is compatibility across all 105 pairs.
7. Solver silence, bounded UNKNOWN, and failure inside an ansatz are not
   evidence for the unrestricted problem.

Do genuinely new heavy lifting. Pursue mathematically different avenues in
parallel in your own reasoning:

- Try a positive construction for \(k=18\) or a later prime case, not only
  \(k=16\). Algebraic formulas must be proved proper on every Johnson edge
  and accompanied by a complete certificate or concise symbolic proof.
- Try a uniform negative invariant over all primes \(p=k+1\), using the
  simultaneous matching-cube cubic, an integral/2-adic obstruction, or a
  covering-monodromy theorem that does not collapse to the original
  colouring condition.
- For \(k=16\), exploit the exact radius-five
  boundary-prescribed \(LS(2,3,19)\) formulation only if you can prove the
  simultaneous compatibility or impossibility, rather than just one slice.

Check every finite claim independently and use the true \(k=2\) and false
\(k=4\) controls. Do not return a literature summary or only a list of
ideas. If an avenue fails, prove the failure boundary and move to a
mathematically different attack.

Write only under `collaboration/opus5_v2/`:

- `STATUS.md`: strongest proved result and exact remaining gap;
- `PROOF.md`: complete arguments only;
- `IDEAS.md`: explicitly unproved directions and failed attempts;
- independent validators for finite claims.

If you find a full resolution, include a section titled
`Why this proves the full problem` and distinguish a construction, a
restricted no-go, and a universal theorem with complete precision.

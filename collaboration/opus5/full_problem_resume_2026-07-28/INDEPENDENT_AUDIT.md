# Independent audit of the 2026-07-28 Opus full-problem note

Date: 2026-07-28
Auditor: Codex, independently of the authoring Opus session

## Verdict

The note does **not** solve Erdős–Rosenfeld Problem #835, as it correctly
states. Its principal exact identities and tail-colouring equivalences survive
audit, subject to the corrections below.

## Checks executed

Using Python 3.14.6:

```sh
python3 -B collaboration/opus5/full_problem_resume_2026-07-28/verify_intersection_distribution.py
python3 -B collaboration/opus5/full_problem_resume_2026-07-28/verify_tail_dichotomy.py
```

The intersection-distribution verifier passed every check. It independently
constructed and validated the listed Steiner systems, checked Theorems 1–2,
checked the completeness identity, and checked the arithmetic assertions of
Theorem 3 for every prime from 5 through 61 and every rung.

The original tail verifier reported four failures. These did **not** refute
Theorem 5's splitting/colouring equivalences. The verifier had incorrectly
expected the canonical triangles to be every triangle of the conflict graph.
For example, it found 50 graph triangles in the `LS(2,3,9)` test where there
are 36 canonical triangles, one for each pair. The theorem needs only the
edge-disjoint decomposition into canonical triangles. The verifier was
corrected to check that exact edge decomposition while allowing additional
noncanonical triangles. The corrected verifier was then rerun and ended with
`ALL CHECKS PASS`.

## Hand audit

1. The fixed-block moment equations in Theorem 1 determine the entire
   intersection distribution because `K=t+1`; the displayed binomial
   inversion, including its boundary correction at `i=K`, is sound.
2. The cross-class calculation in Theorem 2 follows from the same moment
   system with the fixed block absent. The completeness identity follows
   algebraically.
3. For prime `p`, the congruence
   `binom(p-1,i) = (-1)^i (mod p)` proves the asserted integrality. The
   shell-packing calculation cancels to `r <= p` whenever its coefficient is
   nonzero.
4. The former monotonicity assertion for `D_t` was false. At `p=11`, for
   example, the even-index binomial contribution rises and then falls; the
   sequence cannot be strictly increasing across the stated range. The
   monotonicity clause has been removed. The separately proved uniqueness
   statements `D_t=1` only at `t=p-2` and `D_t=0` only at `t=p-3` do not use
   that clause and remain valid.
5. Theorem 5 parts 1–3 are exact. A proper colouring gives exactly one block
   of each colour above every `t`-set, and conversely a splitting is a proper
   colouring. In part 3 the canonical triangles partition the **edges**;
   additional graph triangles may exist.
6. The original broad claims that no one- or two-class statistic, or no
   degree/cut/LP-type invariant, can help were not proved. The established
   route closure is narrower: the single-base-block shell inequalities
   explicitly calculated in the note yield only `r <= p`, and the elementary
   degree/vertex/edge counts do not decide bipartiteness or 3-colourability.
   The proof and status files have been narrowed accordingly.
7. The Latin-rectangle equivalence in Theorem 6 follows directly from the
   rainbow up-stars and is sound.

## Remaining mathematical gap

Neither the audited identities nor the exact conflict-graph reformulation
provides an unrestricted construction or obstruction. A complete solution
still requires either an actual `LS(k-1,k,2k)` for some `k>2`, or a uniform
nonexistence argument covering every admissible `k`.

You are Claude Opus 5 at maximum reasoning effort, doing core novel
combinatorics research on Erdős--Rosenfeld Problem #835. Cost is not a
constraint. Do not stop at a survey or a reformulation: attempt a complete
proof or a genuine counterexample.

Repository root:
  /Users/dennison/Documents/Math Problem

Read these files first:

1. collaboration/opus5/common_odd_transversal_2026-07-29/PROOF.md
2. collaboration/opus5/common_odd_transversal_2026-07-29/INDEPENDENT_AUDIT.md
3. collaboration/opus5/common_odd_transversal_2026-07-29/IDEAS.md
4. collaboration/independent/conflict_cohomology_2026-07-29/PROOF.md
5. collaboration/independent/conflict_cohomology_2026-07-29/INDEPENDENT_AUDIT.md
6. collaboration/ls3420_branch0_search/README.md
7. collaboration/independent/conflict_cohomology_2026-07-29/verify_cochain_controls.py

Important corrections already established:

- The stronger LLS-span claim is false on both controls:
  dim L=11<13 on LS(2,3,9), and dim L=467<587 on the authenticated
  Etzion--Hartman 15-system SQS(20) partial. Do not reuse L=Z_1.
- Theorem 6.1 is only a counting upper bound, not unconditional attainment.
- “k+1 prime” is divisibility-admissibility, not design existence.
- Every nonzero deleted-support unitrade at the top has weight at least
  2k+1, hence at least 33 at k=16.

Primary target:

Let D_1,...,D_15 be pairwise block-disjoint S(3,4,20) systems. For every
pair A of points, their links are 15 disjoint one-factors of K_18; let R(A)
be the residual 2-factor.

Prove or refute the following universal statement:

  (LOL20) For every such 15-system partial, some R(A) contains an odd cycle.

A proof of LOL20 would show that no LS(3,4,20) exists, hence no
LS(15,16,32) exists, resolving the first open k=16 case negatively. A
counterexample must be an actual family of 15 disjoint SQS(20), not an
abstract collection of one-factors.

Attack LOL20 through exact parity identities coupling the 190 link
2-factors. Each residual 4-block appears in six pair-links and each residual
triple labels one conflict edge. Potential handles include:

- parity or sign of the 15 fixed one-factors and the two missing factors;
- compatibility of even-cycle two-colourings across overlapping pairs;
- a cohomological obstruction on the quotient Z_1(G)/L, since L itself
  need not span;
- triple/quadruple incidence identities unavailable to isolated links;
- complement or switching structure induced by a hypothetical global
  completion.

Requirements:

1. Clearly state whether LOL20 is proved, refuted, or still open.
2. Check every quantifier. A fixed Etzion--Hartman example is not universal.
3. If you derive a parity identity, prove it symbolically and test it on the
   authenticated EH partial and the LS(2,3,9) control when applicable.
4. If LOL20 fails, construct or locate an authenticated 15-system partial
   with every link even but a globally non-bipartite residual graph, or
   explain exactly why no such object was obtained.
5. Do not claim #835 solved unless the implication to LS(15,16,32) is fully
   rigorous and independently auditable.
6. Write all work under:
   collaboration/opus5/local_odd_link_k16_2026-07-29/
   with PROOF.md, IDEAS.md, STATUS.md, and exact standard-library verifiers.
7. Do not edit existing files, commit, or push.

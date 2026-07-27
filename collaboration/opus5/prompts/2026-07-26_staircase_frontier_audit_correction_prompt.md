# Audit correction request: staircase-support frontier

Your new `collaboration/opus5/staircase_support_frontier/NOTE.md` contains a
useful exact staircase-support calculation, but the central "Theorem T" and
several downstream exhaustion claims do not yet survive audit.  Please stop,
repair the note and verifier rigorously, and distinguish proved upper bounds
from exact image dimensions.

## Mandatory corrections

1. The claimed image dimension `a` under `Z -> Z P_a` is already false at
   `a=2`: the committed companion note proves
   `R P_2 = 77 P_2` and indeed `A_s P_2 = a_s P_2` for every relation.
   Thus the image at level 2 has dimension 1, not 2.  Your current verifier
   checks only the dimension of the subspace of Johnson polynomials that
   vanish on the *global support*.  That proves `dim image <= a`; it does not
   prove equality, because compression can create additional cancellations.
   Rewrite Theorem T as the valid support-derived upper bound unless you can
   separately prove exact rank for each level.  The sentence saying the
   `a=2` case reproduces scalarity is internally inconsistent with dimension
   2.

2. Recompute every downstream triple-profile equality system after adding
   all already-proved compression relations, especially the extra level-2
   scalar relation `R P_2 = 77 P_2` (and the complete committed H1/H2 scalar
   tables).  Report the actual equation rank.  Rational consistency and the
   fact that no coordinate is uniquely determined do **not** prove existence
   of a nonnegative integral profile, so do not say that the linear theory
   "cannot obstruct" profiles.  State only exactly what the calculation
   establishes, and leave LP/nonnegative-integral feasibility open unless
   you certify it.

3. Remove the literal placeholder
   `||(I-P_3)A_13P_3||_F^2 = Y - ?/`.
   The exact identity is
   `Y - ||P_3 A_13 P_3||_F^2`; if the second term is not determined, say so.

4. Scope the phrase "no upper bound": the `3 x 3` Gram PSD condition by
   itself may give no upper bound, but the adjacency operator has trivial
   finite norm bounds.  Likewise do not say the free statistics are subject
   *only* to Gram PSD unless you have proved that no other combinatorial,
   integrality, or operator constraint applies.

5. The Steiner-side quantity `d(B)` is not free.  First, two distinct
   15-subsets of the 16-point complement of `B` intersect in 14 points, so
   `d(B) <= 1`.  More decisively, the complete design-moment/binomial-inversion
   formula
   `n_s = C(15,s)/17 * (C(16,s+1) + (-1)^(s+1) 16)`
   uses only the `S(14,15,31)` property and `n_15=1`; at `s=0` it gives
   `n_0=d(B)=0`.  Audit this carefully, but if confirmed, delete the claim
   that intersectingness is an extra condition and delete `d(B)` from the
   free frontier.  Explain instead that every `S(14,15,31)` is automatically
   intersecting and therefore a large set of these systems is already
   equivalent to the desired cover.

6. Audit the symmetric-square and Krein "route exhausted" language.  Equality
   of source and ambient dimensions does not on its own prove the pointwise
   product map is injective or that a bound is saturated.  Similarly, closure
   of the Johnson Schur span does not prove that every possible coupling
   argument is exhausted.  Replace broad no-go claims by the narrow theorem
   actually verified.

7. Audit the claim that integrality at levels 3--7 "gives nothing."  Failure
   of scalarity merely removes the simple rational-algebraic-integer
   argument; it does not prove that characteristic-polynomial, lattice, rank,
   or congruence constraints are absent.

## Preserve and strengthen what is valid

- Keep the exact staircase support calculation if it remains correct.
- Keep the support-derived relation spaces, but label them as a certified
  family of relations / an image-dimension upper bound.
- Add verifier assertions that explicitly catch the level-2 counterexample:
  the support-derived upper bound is 2, while the known scalar compression
  makes the actual image dimension 1.
- Run Ruff and the full exact verifier.
- End with a precise inventory of what is proved and what remains open.  Do
  not claim a solution to Erdős--Rosenfeld #835.

Please edit the existing note and verifier in place, then report the exact
changed claims and verification output.

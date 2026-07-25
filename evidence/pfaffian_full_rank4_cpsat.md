# CP-SAT search for the normalized rank-four Pfaffian problem

The solver in search_pfaffian_full_rank4_cpsat.py encodes the proved rank-four
normal form from pfaffian_full_rank4.md. In coordinate \(c\), the sixteen
non-basis entries are a permutation of
\(\mathbb F_{17}\setminus\{(-1)^{3-c}\}\). Coordinate 0 is fixed in that
order by vertex relabelling. No unproved coordinate-order symmetry breaker
is used.

The first exact CP layer includes all 96 stars consisting of two basis
points and one non-basis point. Every one of the 17 fourth-point
determinants is explicitly reduced modulo 17 and constrained AllDifferent.
Before solving, the program independently compares its reduced determinant
formula with direct \(4\times4\) determinant evaluation on 20 seeded random
point systems. The checker also reconstructs returned points and recomputes
all determinants independently, then evaluates the complete 1,140-star
predicate.

Run: python3 evidence/search_pfaffian_full_rank4_cpsat.py --seconds 60 --workers 8

The --core mode replaces each star AllDifferent by its equivalent 136
pairwise inequalities, gates those inequalities by an assumption literal,
and prints OR-Tools' sufficient set of enabled stars if the layer is
infeasible. This is useful localization evidence, but still not a portable
proof trace.

An INFEASIBLE status would settle this 96-star necessary layer in the
specified finite model. OR-Tools does not emit a solver-independent proof
trace, so that status is reproducible machine evidence rather than a
portable rank-four impossibility certificate. A feasible point still must
pass the full independent check; it is not automatically a rank-four
candidate.

Neither layer, nor any rank-four candidate, resolves arbitrary-rank
Pfaffian matrices or provides the required 32-point lift.

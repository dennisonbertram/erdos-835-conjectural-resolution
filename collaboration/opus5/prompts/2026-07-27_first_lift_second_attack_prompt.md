# Opus 5 second attack: close the class-B first lift

Work on Erdős--Rosenfeld Problem #835 at maximum mathematical reasoning effort.
Cost is not a constraint. The full problem is open; do not overclaim.

Your concrete target is the class-B first-lift theorem at \(\Pi(13,5)\):
there are 13 vertices, 17 colours, each vertex forbids exactly 5 colours,
each colour is forbidden at an odd number at most 5 of vertices, and hence
each colour support has size 8, 10, or 12. Prove that \(E(K_{13})\) always
partitions into one perfect matching on each colour support, or produce a
fully checked counterexample.

Read these current artifacts first:

- `collaboration/opus5/first_lift_classB_attack/NOTE.md`
- `collaboration/first_lift_global_theorem/SEVEN_PACKING_NONZERO_R_NOTE.md`
- `collaboration/first_lift_global_theorem/SEVEN_PACKING_R0_NOTE.md`
- `collaboration/first_lift_global_theorem/PROPAGATION_COUNTEREXAMPLE.md`
- `collaboration/first_lift_global_theorem/EIGHTH_MATCHING_CORE_CATALOGUE.md`

Known frontier:

1. Every target class-B palette has a simultaneously matchable seven-colour
   prefix.
2. An arbitrary prefix need not propagate; the exact residual-degree invariant
   alone is insufficient.
3. After a seven-prefix, a blocked size-10 support forces one of seven explicit
   complete multipartite cores in the selected union. A blocked size-12
   support forces \(K_7\) or \(K_8-E(K_3)\).
4. The stronger bipartite-capacity condition (BC), parity condition (BP), and
   the tested fractional LP cannot obstruct the target.

Push past this frontier. A successful output must be one of:

- a complete solver-free proof of the class-B theorem;
- a finite reduction with a sound, independently replayable SAT/SMT/ILP
  certificate that covers every target instance; or
- an explicit class-B counterexample plus a complete UNSAT certificate for
  its matching decomposition.

Do not settle for random evidence, another necessary condition that vanishes,
or an unverified solver status. If one route fails, record the exact delimiter
and move to the next strongest route. Pay special attention to:

- switching selected matchings to destroy the eighth-matching cores;
- simultaneous overlap bounds for all cores required by the remaining
  supports;
- augmenting-path or matroid-parity formulations that use the special row
  sum 12 and the six exact support profiles;
- whether the universal seven-prefix can be chosen with an additional
  resilience invariant, rather than trying to extend an arbitrary prefix.

Write all new work under
`results/first_lift_classB_second_attack/`, including `NOTE.md`, source,
certificates, and a deterministic verifier. State scope precisely. Do not
modify existing result directories. Continue until you have exhausted serious
proof and exact-certificate routes.

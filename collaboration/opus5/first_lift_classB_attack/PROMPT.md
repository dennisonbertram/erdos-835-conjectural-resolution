You are Claude Opus 5, working as the core mathematical reasoner on
Erdos-Rosenfeld Problem #835. Use maximum reasoning effort. Cost is not a
constraint. Continue until you have either a rigorous decisive theorem or a
precisely delimited frontier with all artifacts saved.

Read these public-repository files first:

- collaboration/unrestricted_lift_tower/NOTE.md
- results/first_lift_k13_hole/NOTE.md
- results/first_lift_k13_hole/first_lift.py
- results/first_lift_k13_hole/verify_first_lift_obstruction.py
- collaboration/first_lift_support_completion/NOTE.md
- collaboration/first_lift_sufficiency_search/NOTE.md

Important correction to the older results note:

1. Class B includes the parity condition: every forbidden-set column
   multiplicity is odd and at most 5.
2. Universal class-B completion is stronger than the partial-edge-colouring
   extension question. Only class B-prime is equivalent to extending a
   proper 17-edge-colouring of K18-E(K13) saturated on the five vertices
   outside the hole. Class C, the fan-realizable instances, is smaller still.
3. Do not identify these three questions or claim an equivalence between
   class B and class B-prime.

Primary target:

Let A have 13 vertices and C have 17 colours. For each a in A, let S_a be a
5-subset of C. Suppose every colour occurs in an odd number, at most 5, of
the S_a. Prove or refute that E(K_A) partitions into perfect matchings M_c on
V_c={a:c not in S_a}.

If the strong class-B statement is false, determine whether the
counterexample is class B-prime. If it is not, attack the universal
class-B-prime extension theorem directly. A constructive theorem, a finite
minimal-counterexample reduction, a known theorem with fully checked
hypotheses, or a machine-checkable counterexample are all acceptable, but
the final claim must be rigorous.

Explore the most promising mathematical routes, including:

- partial one-factorization and symmetric Latin rectangle completion;
- alternating-cycle or switching proofs;
- matching preclusion, list edge-colouring, and matroid-intersection
  formulations;
- exact exhaustive search over the six multiplicity profiles, with symmetry
  reduction and independently checkable certificates;
- whether the support sizes 8, 10, and 12 on K13 force completion;
- known extension theorems, but quote no theorem until you have obtained and
  checked its actual statement.

Write every artifact under:

  results/first_lift_classB_attack/

At minimum leave:

- NOTE.md with a complete proof/counterexample or exact frontier;
- verifier code and any certificates;
- RUN_LOG.txt with exact commands and outputs;
- any literature references actually used.

Independently recheck computational witnesses from definitions. Never use a
timeout or node-budget exhaustion as evidence of unsatisfiability. Do not
claim a simultaneous fan, LS(3,4,20), J(32,16) colouring, or solution of #835
unless you have actually constructed and verified it.

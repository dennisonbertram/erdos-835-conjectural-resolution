# Claude Opus 5 task: attack the exact simultaneous 13-fan frontier

You are the core mathematical reasoner on Erdős--Rosenfeld Problem #835.
Cost is not a constraint.  Work autonomously and deeply.  Use cheaper
background agents for repository inventory, literature search, and mechanical
experiments; reserve Opus 5 reasoning for the core combinatorics and proof.

## Non-negotiable scope

The full target remains a rigorous construction or nonexistence proof for
Problem #835.  Do not relabel a restricted ansatz, a timeout, an `UNKNOWN`
solver result, a sampled pattern, or a necessary condition as a solution.
The first surviving parameter is \(k=16\).

The just-completed holonomy audit proves that the aggregate tower identity and
all of its linear projections are pure gauge.  Do not spend time trying to
revive that route.  Read and use:

- `collaboration/opus5/holonomy_followup/NOTE.md`
- `collaboration/h3_holonomy_audit/README.md`
- `evidence/holonomy_group_algebra_tower.md`

The unaffected live frontier is:

- `collaboration/simultaneous_ls3420_fan/README.md`
- `collaboration/simultaneous_ls3420_fan/verify_simultaneous_ls3420_fan.py`
- `collaboration/h3_simultaneous_fan_audit/README.md`
- `collaboration/h3_simultaneous_fan_audit/verify_simultaneous_fan_audit.py`

Read any related fixed-link, exact-cover, cyclic-link, residual-graph, and
star-sign artifacts needed from the repository.  Treat the current worktree as
authoritative.

## Exact target

For a labelled \(LS(2,3,19)\) link \(L\), the \(50,388\)-vertex,
\(60\)-regular conflict graph \(H_L\) is the line graph of a
\(5\)-uniform incidence system with
\[
  A(H_L)=B^\mathsf{T}B-5I.
\]
A simultaneous 13-fan is exactly a proper 13-colouring of \(H_L\), or
equivalently a resolution of its 50,388 cells into thirteen
Hoffman-tight independent transversals of size 3,876.

Find one of the following, in descending value:

1. a parameter-independent contradiction showing \(H_L\) is not
   13-colourable for every possible \(LS(2,3,19)\) link \(L\), which would
   exclude \(k=16\);
2. an explicit, independently verifiable 13-colouring for some \(L\), which
   constructs the full simultaneous fan and advances the unrestricted local
   shadow;
3. a rigorous new structural theorem that materially reduces either of those
   tasks, with a precise next finite decision problem.

Promising mechanisms to assess rather than assume:

- Hoffman-equality structure inside \(\ker B\), including integrality and
  simultaneous orthogonality of thirteen centred indicators;
- exact-cover resolvability, trades, parity, Smith normal form, modular rank,
  and incidence-lattice obstructions;
- clique or inertia obstructions beyond the ordinary ratio bound;
- compatibility of the 19,380 \(K_{13}\) constraint groups as an orthogonal
  array / Latin trade / resolvable transversal system;
- cyclic-link constructions, but with restricted scope stated exactly;
- small-parameter controls that distinguish universal identities from
  accidents;
- a certificate-producing SAT/CSP formulation if computation is genuinely
  decisive.  Any UNSAT claim needs a checkable proof; any SAT claim needs a
  semantic verifier.

Do not merely rephrase the fan equivalence.  Try to break or construct it.
Explicitly test every attractive lemma against small controls before building
on it.

## Deliverables

Work only under:

`collaboration/opus5/simultaneous_fan_attack_2/`

The prompt is already there.  Add:

- `NOTE.md`: definitions, proved theorems, proof details, exact scope, failed
  routes, and honest status of #835;
- one or more standard-library verifiers or compact certificate checkers;
- any small deterministic certificates needed for reproducibility;
- `RUN_LOG.txt` only for finite computations whose output matters.

Run every verifier, lint Python, inspect your final diff, and report exact
check counts.  If no decisive proof is obtained, identify the strongest proved
reduction and the next exact target.  Do not commit or push; the parent agent
will independently audit and integrate.

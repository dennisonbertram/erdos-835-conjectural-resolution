# Discovery campaign: Erdős–Rosenfeld Problem #835

## Role

You are the root researcher for a sustained, multi-agent mathematical
discovery campaign. Your job is not to produce persuasive prose. Your job is
to discover, falsify, prove, and independently audit mathematical claims.

Use all concurrency that is actually available, dynamically. Preserve several
independent approaches during early rounds. The root agent owns the research
registry, proof standard, synthesis, redirection, and final judgment.

## Primary target

For every integer \(k>2\), determine whether the \(k\)-subsets of a
\(2k\)-element set can be coloured with \(k+1\) colours so that the \(k+1\)
\(k\)-subsets of every \((k+1)\)-set receive pairwise distinct colours.

Equivalently, determine whether

\[
\chi(J(2k,k))=k+1
\]

can hold for any \(k>2\).

The current negative-resolution conjecture is

\[
\chi(J(2k,k))\geq k+2\qquad(k>2).
\]

Treat its truth as unknown. Do not assume either that the conjecture is true
or that a proof must exist. A valid construction or counterexample is as
valuable as a nonexistence proof.

The full target is a theorem for every \(k>2\). The first unresolved case is
\(k=16\). Resolving \(k=16\) is a major discovery, but is not by itself a
resolution for all \(k\).

## Exact equivalent formulations

Use an equivalence only after auditing both directions.

The established working formulations include:

- a \((k+1)\)-colouring of \(J(2k,k)\);
- a large set \(LS(k-1,k,2k)\);
- for even \(k\), a locally bijective covering projection
  \(O_k\to K_{k+1}\);
- a partition of \(O_k\) into \(k+1\) perfect one-error-correcting codes;
- for \(k=16\), a compatible tower of derived large sets, including
  \(LS(4,5,21)\), \(LS(3,4,20)\), and \(LS(2,3,19)\).

The divisibility obstruction already forces \(k+1\) to be prime. Audit this
and every other imported reduction before relying on it.

## Required orientation

Read the repository's current research record before proposing new work:

- `README.md`
- `erdos_835_conjectural_resolution.md`
- `evidence/`
- `collaboration/`

Build a claim ledger with four statuses:

- **PROVED**: a human-checkable derivation with all dependencies discharged;
- **CERTIFIED**: an exhaustive computation with a complete, independently
  replayed certificate and a proved encoding-to-theorem bridge;
- **OBSERVED**: reproducible data or a bounded computation;
- **CONJECTURED**: an unproved statement or mechanism.

Never promote an OBSERVED or CONJECTURED item to PROVED. A solver timeout,
`UNKNOWN`, an unreplayed proof trace, a floating-point residual, or a search
through a fixed bound is not evidence of nonexistence.

## Current frontier and known boundaries

Re-audit these facts from the local record; do not merely repeat them.

- \(k=16\) is the first unresolved case after the prime and small-case
  obstructions.
- A complete one-star compatibility layer exists at \(k=16\): it is a golf
  design \(G(17)\).
- An explicit locally bijective colouring extends through the radius-four
  Odd-graph ball. Therefore, attacks that see only one star, one adjacent
  pair of Latin squares, or radius at most four cannot decide the case.
- The next local extension layer is a coupled radius-five
  triangle-decomposition problem.
- Several natural affine, XOR-syndrome, pair-local, projective, and highly
  symmetric constructions have exact no-go results.
- Scalar Latin signs, bare graph-topological lifting, ordinary spectral or
  association-scheme feasibility, and several unrestricted lattice
  relaxations have survived or collapsed to tautologies.
- Pair-trade and matching-cell formulations expose nonlinear and integral
  constraints, but attractive universal parity strengthenings have failed in
  smaller parameters.

Do not reopen a blocked family by changing notation. Reopen it only with a
new invariant, a stronger input, a new coupling across layers, or a concrete
counterexample to the recorded no-go boundary.

## Scope-drift rule

The repository may contain valuable side problems, including the
\(C(12,6,4)\) covering-number campaign. A side theorem is a legitimate
discovery and should be recorded as such. It does not count as progress on
the primary target unless an explicit proved implication connects it to
Erdős–Rosenfeld #835.

Never substitute a tractable neighboring theorem for the stated target.

## Research portfolio

Begin with a genuinely diverse portfolio. Organize agents by mathematical
mechanism rather than wording. Keep at least several incompatible families
alive until evidence justifies pruning. Candidate families include, but are
not limited to:

1. radius-five and deeper Odd-graph compatibility, including coupled
   triangle decompositions and labelled closed walks;
2. simultaneous constraints across the entire derived-large-set tower,
   rather than existence of one constituent design;
3. nonlinear exact-slice, trade-code, and integral-lattice invariants that
   distinguish \(0\)-\(1\) partitions from feasible linear relaxations;
4. monodromy, permutation groupoids, critical groups, and global holonomy
   that genuinely use the subset-labelled graph;
5. modular and representation-theoretic arguments, especially where the
   prime \(17\) interacts with integrality or support disjointness;
6. automorphism-free and asymmetric arguments, not only equivariant
   constructions;
7. direct constructive attacks, because the conjectured direction may be
   false;
8. exact computation on a carefully chosen quotient or local extension whose
   outcome would discriminate between proof families.

Do not tell most early agents which family is currently favoured. After
independent development, cross-pollinate only concrete lemmas, equations,
counterexamples, and certificates.

## Approach registry

Maintain a live table with one row per genuine approach family:

| Family | Precise target lemma | Why it would matter | Status | Strongest result | Exact gap | Decisive next test | Reopen condition |
|---|---|---|---|---|---|---|---|

Mark a route **BLOCKED** when its missing lemma is equivalent in strength to
the original problem, contradicted by a smaller case, or unsupported by any
mechanism. Do not keep assigning agents to a BLOCKED route unless its reopen
condition is met.

Rank new work by expected information gain:

- Does either outcome eliminate a family or prove a reusable lemma?
- Is the statement strictly stronger than an already feasible relaxation?
- Can a small exact case falsify it?
- Does it couple structures that previous no-go results treated separately?
- Is there a path from computation to an independently checkable theorem?

## Agent return contract

Reject vague status reports. Every agent must return:

1. a precise claim or target lemma;
2. its status: PROVED, CERTIFIED, OBSERVED, CONJECTURED, REFUTED, or BLOCKED;
3. a derivation, construction, explicit counterexample, equation, or
   certificate;
4. all dependencies and any direction of an equivalence used;
5. the smallest adversarial test performed;
6. the exact remaining gap;
7. a proposed next action whose possible outcomes are informative.

If an agent proposes a theorem-strength lemma, immediately assign:

- one independent prover who is not shown the proposed proof;
- one adversarial checker looking for a smallest counterexample;
- one implication auditor checking that the lemma really advances the primary
  target and is not equivalent to it in disguise.

## Computation standard

Use computation to discover structure and to certify finite cases, not to
hide gaps.

For every decisive computation:

1. state the finite mathematical proposition being decided;
2. prove that the encoding is sound and complete;
3. remove unjustified symmetry assumptions or prove orbit exhaustion;
4. use exact arithmetic where possible;
5. emit the witness for SAT or a replayable proof certificate for UNSAT;
6. write an independent verifier that does not import the generator;
7. pin inputs, source hashes, tool versions, commands, and outputs;
8. replay the certificate with a small trusted checker when practical;
9. distinguish `SAT`, `UNSAT`, timeout, resource exhaustion, and `UNKNOWN`.

Searches in small parameters should be designed to kill false lemmas early.
They do not prove the general case unless accompanied by a theorem lifting
them.

## Adversarial audit checklist

Every candidate proof must be checked for:

- a one-way reduction presented as an equivalence;
- a theorem about one Steiner system silently applied to a compatible large
  set, or conversely;
- local feasibility confused with global extendability;
- fractional, modular, or spectral feasibility confused with a
  disjoint-support \(0\)-\(1\) partition;
- symmetry imposed without proving that every solution has a representative;
- complement closure used outside its valid parity range;
- a statement verified for \(k=4\), \(6\), or another small case extrapolated
  to \(k=16\);
- circular use of the desired colouring, cover, or large set;
- hidden repeated blocks or loss of multiplicity information;
- an unproved appeal to a classification theorem;
- a computation whose negative result lacks an exhaustive certificate;
- a side result presented as resolving the primary target.

## Round protocol

### Round 0: audit and map

Reconstruct the exact target, claim ledger, approach registry, and known
counterexamples. Identify the narrowest live frontier in each family.

### Round 1: independent divergence

Launch independent attacks across underexplored families. Prefer falsifiable
lemmas and calculations over broad essays.

### Round 2 and later: select, cross-check, redirect

Promote only routes that produced a concrete mechanism. Assign adversarial
audits before expanding them. Redirect agents away from crowded or blocked
families. Use discoveries from one family as inputs to another only after
their status is clear.

### Proof gate

A claimed resolution may pass only after:

1. line-by-line dependency audit;
2. an independent reconstruction of the proof;
3. adversarial small-case and boundary-case checks;
4. independent replay of every computational certificate;
5. verification that the conclusion has exactly the quantified scope stated
   in the primary target.

## Return conditions

Return immediately if a complete resolution survives the proof gate.

Otherwise continue until the allotted research budget is exhausted or an
external dependency genuinely blocks all informative work. Do not claim
completion because the first portfolio failed.

If the campaign ends without a full resolution, return a discovery dossier,
not a motivational summary:

1. the strongest new PROVED or CERTIFIED result;
2. its exact implication for the primary target;
3. every new counterexample or killed proof family;
4. the updated approach registry;
5. the narrowest exact remaining gaps;
6. the single highest-information next experiment or lemma;
7. reproducible artifact paths and commands;
8. a clear statement that the full problem remains unresolved.

Partial progress is valuable only when its status and implication are stated
exactly.

## Literature and novelty

Use primary literature and standard references to verify background, theorem
hypotheses, and novelty. Do not search for text to imitate or treat an
unrefereed claim as proof. Before calling a lemma new, run a targeted novelty
check. Keep a source ledger distinguishing established literature from this
campaign's derivations.

## Initial output

Begin by returning:

1. the audited problem card;
2. the current claim ledger;
3. the approach registry;
4. the first diverse batch of concrete assignments;
5. the proof and computation standards that will govern promotion.

Then begin the research rounds.

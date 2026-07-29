# Unproved directions and their explicit failure points

Status labels: everything here is UNPROVED unless it cites PROOF.md.

## 1. Exact decision of the cubic embedding at k=4 (follow-up to the selected attack)

- If `decide_cubic_embedding_k4.py` finds a numerically feasible point:
  certify it exactly.  Two routes: (a) rational reconstruction of the
  subspace \(V\) from the saved configuration; (b) interval
  Newton/Krawczyk on the polynomial system around the point.  Failure
  point: the solution set may be positive-dimensional (an orbit of the
  stabilizer), so Newton needs a gauge fix — e.g. quotient by the
  \(O(p-1)\)-freedom already removed and by \(S_8\).
- If a residual floor: prove infeasibility exactly.  Plan: decompose
  \(\operatorname{Sym}^2 K\to K\) as an \(S_8\)-map
  (\(K=S^{(4,4)}\), \(\dim14\)); the multiplicity space of \(S^{(4,4)}\)
  in \(\operatorname{Sym}^2S^{(4,4)}\) pins \(\beta\) up to few
  parameters, and the embedding equations become a small parameterized
  system that Gröbner/resultant methods can kill.  Failure point: the
  multiplicity may be large enough that the reduced system is still ugly;
  not attempted, sizes not computed.
- Only after the k=4 outcome: formulate the p-uniform statement.  Nothing
  is known about \(p=17\) feasibility either way; PROOF.md Theorem 1 only
  says no polarization argument decides it.

## 2. Richer finite-field statistic families (positive direction)

Structural facts to respect (both directions proved or audited):

- Any statistic-rule colouring is a proper colouring of the actual-edge
  quotient, and conversely; a quotient with chromatic number exactly 17
  would resolve #835 positively.  So the positive route through statistics
  is: find a statistic map whose actual-edge quotient is both small enough
  to colour and provably 17-chromatic.
- The two-statistic \(K_{18}\) does not automatically survive refinement:
  its extension vertex \((29,27)\) splits into up to 17 refined vertices
  (one per witness row) once the added statistic separates the rows.
  Expected but UNVERIFIED: the 17 rows' \(e_2\)-values at the
  \(y\)-deletions are not all equal, so the specific certificate dies
  under \((e_1,e_2,e_8+e_1^8)\); a new search is required per family.

Concrete next experiments (adapt `evidence/f32_two_statistic_k18_search.py`):

- \(K_{18}\) search in the \((e_1,e_2,e_8+e_1^8)\) quotient (three
  statistics).  If found: closes a strictly larger family than both
  existing no-gos.  Failure point: fibers shrink as statistics are added,
  so actual-edge collapses get rarer and the search may simply stall
  without deciding anything.
- Bounded 17-colourability of sampled realized subgraphs of the same
  quotient via SAT/CP.  An UNSAT core on a finite realized subgraph would
  be a new exact no-go; a satisfying assignment is only a partial rule.
- Heuristic caution for the full eight-coefficient family: the average
  fiber size of \(S\mapsto(e_1,\dots,e_8)\) is
  \(\binom{32}{16}/2^{40}\approx5.5\times10^{-4}\) (601,080,390 sets over
  \(2^{40}\) states), so most realized states are singleton fibers and
  that quotient is essentially the Johnson graph itself — neither easier
  to colour nor a promising place to hunt a \(K_{18}\).  This is a
  heuristic average, not a theorem; structured states (e.g. the
  moment-curve slices) have larger fibers.

## 3. Beyond the cubic: what new identities would actually add power

PROOF.md Theorem 1's boundary lists the data the cubic does not
determine.  Candidate strengthenings, all unproved:

- Projected triple products \(P_K(q_aq_bq_c)\): for a true colouring these
  are again explicit (\(q_a^3=(p-2)^2q_a+\dots\)); deriving the analogous
  closed quartic/cubic family and checking whether the weighted
  \(p\)-point model still satisfies it would either extend the no-go or
  produce the first genuinely stronger system.  Failure point: each new
  layer may again be model-consistent, an infinite regress; the regress
  stops only if some layer sees the ambient multiplication tensor of
  \(K\).
- Unprojected fourth moments \(\langle q_aq_b,q_cq_d\rangle\): for true
  colourings these count intersections of colour classes and are known
  (\(=\) explicit in \(p,d\)); adding them to the cubic system gives a
  strictly stronger finite system whose k=4 feasibility is again
  decidable by the same script pattern.  Not implemented.

## 4. Housekeeping gaps (cheap, do first in an unblocked session)

- Run the five newest repo verifiers and the two new validators; append
  outputs to `evidence/verification.txt`, which currently records none of
  them.
- The `--trace-extension` search command in
  `evidence/f32_two_statistic_k18_obstruction.md` was not replayed here;
  it is not part of the proof, but reproducing it once would close the
  provenance loop for the witness masks.

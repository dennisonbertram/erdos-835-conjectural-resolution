# Fixed cyclic \(LS(2,3,19)\) extension search

This is a constructive search inside the complete \(LS(3,4,20)\) problem.
It fixes the independently audited cyclic \(LS(2,3,19)\) from
`evidence/verify_defect_cross_link_lsts19.py` as the derived large set at
point \(0\), then asks whether the remaining quadruples can be coloured to
form \(LS(3,4,20)\).

The fixed-link CNF is the canonical unrestricted parent plus 952 new unit
clauses.  The other 17 link assignments are already the parent's
colour-symmetry units.

Canonical dimensions and hashes:

- variables: `159885`;
- clauses: `252909`;
- fixed point-link assignments: `969`;
- appended units: `952`;
- fixed-link unit SHA-256:
  `fdf715ea0f53b1afa2c893381946e7361b08e7f92e575828d183e176d5981846`;
- augmented CNF SHA-256:
  `a187094af93645080977a5f2fffcf40cdf2ca40086852390307269e263a3c65c`.

Reproduce:

```sh
python3 -B \
  collaboration/cyclic_lsts19_extension/generate_fixed_link_cnf.py \
  --cnf /tmp/ls3420-cyclic-lsts19-fixed.cnf

python3 -B \
  collaboration/cyclic_lsts19_extension/verify_fixed_link_cnf.py \
  --cnf /tmp/ls3420-cyclic-lsts19-fixed.cnf
```

If a solver returns SAT, pass its DIMACS witness to the verifier with
`--model`.  The verifier then ignores the CNF encoding and directly checks
that every quadruple has one colour and every triple star has all seventeen
colours.

Scope:

- SAT would construct a complete \(LS(3,4,20)\), an important necessary
  shadow of the \(k=16\) problem, but would not solve Erdős–Rosenfeld #835.
- Checked UNSAT would exclude the entire point/colour isomorphism class of
  this cyclic link from occurring at any point of an \(LS(3,4,20)\).  It
  would not exclude large sets whose point links belong to other isomorphism
  classes, \(k=16\), or #835.

The current CaDiCaL run is reconnaissance and has no recorded verdict yet.

## \(C_{17}\)-equivariant subproblem

The fixed point link is covariant under simultaneous translation of its
seventeen finite points and colours.  Requiring the unknown quadruple
colouring to have the same covariance gives a much smaller, but restricted,
construction search.  Its 3,876 Boolean variables encode one of seventeen
base phases on each of the 228 free quadruple orbits.  The 57 triple orbits
enforce that their sixteen non-root extensions receive exactly the sixteen
colours other than the fixed root colour.

Generate and independently reconstruct every clause:

```sh
python3 -B \
  collaboration/cyclic_lsts19_extension/generate_c17_equivariant_cnf.py \
  --cnf /tmp/ls3420-c17-equivariant.cnf \
  --map /tmp/ls3420-c17-equivariant-map.json \
  --encoding cover

python3 -B \
  collaboration/cyclic_lsts19_extension/verify_c17_equivariant_cnf.py \
  --cnf /tmp/ls3420-c17-equivariant.cnf \
  --map /tmp/ls3420-c17-equivariant-map.json
```

This symmetry is an ansatz, not a without-loss reduction.  SAT gives a
complete \(LS(3,4,20)\); checked UNSAT excludes only this equivariant
extension of this fixed cyclic point link.

More precisely, equivariant UNSAT excludes the pair consisting of this link
and this distinguished order-17 action: the action has point-cycle type
\(17+1+1\), is regular on the seventeen classes, and fixes the new parent
point.  It does not exclude nonsymmetric extensions of the same link or a
potentially nonconjugate order-17 action.

The `cover` encoding uses the fact that sixteen extension slots must contain
all sixteen allowed colours; coverage alone therefore forces a bijection.
The alternative `--encoding pairwise` writes the equivalent pairwise
inequalities.  The independent verifier reconstructs the selected encoding
clause-for-clause.

`search_c17_equivariant_min_conflicts.py` is a heuristic witness search on the
same 228-phase CSP.  It has no negative evidentiary value.  Any model it emits
must pass `verify_c17_equivariant_cnf.py --model ...` before it is treated as a
construction.

`search_c17_equivariant_exact_cover.py` expresses the same problem as 2,964
five-entry rows covering 1,140 columns and runs a bounded Algorithm-X witness
search.  A timeout has no mathematical status, and even process-local
exhaustion is not treated as portable UNSAT evidence without an independently
checkable certificate.

`search_c17_equivariant_cpsat.py` supplies two additional witness-search
encodings of the same quotient: one preserves the 57 native all-different
constraints on 228 phase variables, and the other uses the 1,140 exact-one
rows directly.  It can accept fixed or hinted row sets for scoped extension
searches.  Only a SAT candidate that passes the independent semantic verifier
has positive mathematical status; `UNKNOWN` and uncertified `INFEASIBLE`
statuses are telemetry only.

For a faster independent search implementation, the Python script can dump
that matrix and `solve_c17_exact_cover.cpp` runs bounded dancing links on it.
Its SAT output is still only a candidate until the semantic verifier passes.
Optional row labels after the seed fix a compatible partial branch; they do
not constitute symmetry breaking unless justified separately.  The optional
`--hint ROW_LABEL_FILE` form merely searches the listed active rows first and
does not fix them; it changes search order only.

`enumerate_c17_type_i_branches.py` independently lists all 1,326 feasible
type-(i) branches.  `batch_search_c17_type_i.py` can distribute bounded
compiled witness searches across that list.  Its timeout and local-exhaustion
records are telemetry, not UNSAT evidence.

`finalize_c17_type_i_sweep.py` requires an exact disjoint census of all branch
indices, validates every recorded row tuple and solver status, and emits a
merged JSONL plus a scope-explicit receipt.

The recorded 0.5-second-per-branch sweep covered all 1,326 branches with
207,040,512 dancing-links nodes and found no model; every branch timed out.
This is telemetry only and proves no branch UNSAT.  Exact artifacts:

- branch census SHA-256:
  `f5281dc2cafaad77e15a3194dfd83342785ba37507758e2c9eb2469a61eabaaf`;
- exact-cover matrix SHA-256:
  `059c4f30f2355100ce5589acaac1e8ddc337ee8e3fe55294103d68379d078186`;
- merged sweep SHA-256:
  `71a5b2203a4b76e6adbf4539604147b2fa4acfe3dc5dbba6d2df348c116844eb`;
- receipt SHA-256:
  `f498da37290ab9b6285df44d4898b73d4dd05549f62f1e6908e615b764f88582`.

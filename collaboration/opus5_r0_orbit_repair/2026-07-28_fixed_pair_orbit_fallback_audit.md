# Orbit-parameterized fixed-pair fallback audit

## Scope

`2026-07-28_fixed_pair_orbit_fallback.py` generalizes the audited orbit-4
fixed-pair support-relaxation driver to support orbits 5 through 15.  It does
not modify or replace either the orbit-4 driver or the separate
single-matching driver.

The driver intentionally launches no full campaign in this audit.  Only case
0 of orbit 5 was run for one CEGIS round.

## Separate 50-case count review

The proposed canonical-first-matching reduction was rerun independently:

```text
python3 collaboration/opus5_r0_orbit_repair/2026-07-28_single_matching_orbit_audit.py
```

For orbits 4 through 15 its counts are

```text
2, 2, 2, 3, 2, 4, 3, 4, 6, 6, 7, 9
```

and sum to 50.  For every orbit, three independently computed counts agree:
endpoint-cell invariants, connected components of the explicit stabilizer
action, and loop-multigraph incidence matrices.  This validates the count; it
does not prove those 50 SAT instances UNSAT.

The fallback developed here deliberately uses the finer exact compatible-pair
catalogue rather than relying on the 50-case reduction.

## Exact-pair catalogue audit

The existing independent classifier audit was run for orbit 5:

```text
python3 collaboration/opus5_r0_orbit_repair/2026-07-28_remaining_pair_orbit_classifier.py --orbits 5
```

It enumerated 514,080 compatible labelled pairs.  Both the component-word
invariant and the explicit nine-generator action graph give exactly 17
orbits.  The fallback independently rebuilt the same 17 deterministic
representatives before its smoke case.

## Encoding audit

For each fixed-pair case:

1. The deletion variables satisfy exactly 27 deleted edges and the vertex
   bounds `selected multiplicity + 1 <= d_D(v) <= 5`.
2. Every positive three-support capacity cut is generated.  A cut is omitted
   from the CNF only when its upper bound follows from the explicit size and
   degree constraints; every cut, including omitted automatic cuts, is checked
   directly against each SAT model.
3. The ten fixed-pair edges are forced available.
4. The unique third family is computed as the complement of the selected
   maximum-intersection pair.  Every third matching edge-disjoint from the
   fixed pair receives its five-positive-deletion blocking clause.
5. Global CEGIS enumerates actual edge-disjoint triples and adds the positive
   15-edge union clause.  Exhaustion is confirmed by a second exact oracle
   query before any relaxed counterexample can be returned.
6. No vertex-symmetry constraints are emitted after fixing a labelled pair.

Thus an UNSAT result for every exact pair type soundly closes this support
relaxation.  A SAT result is only a relaxed obstruction candidate.

## Orbit-5 one-round smoke

Command:

```text
python3 collaboration/opus5_r0_orbit_repair/2026-07-28_fixed_pair_orbit_fallback.py \
  --orbit 5 --cases 0 --cut-batch 1000 --max-rounds 1 --progress-every 0 \
  --jsonl collaboration/opus5_r0_orbit_repair/2026-07-28_fixed_pair_orbit5_smoke.jsonl
```

Result: `round-limit`, as expected for a bounded smoke.  The model passed the
full semantic verifier.  The instance had 56,820 variables, 227,888 initial
clauses, 4,040 positive capacity cuts of which 435 were nonautomatic and
encoded, 453 fixed-pair third extensions, and 228 new exact triple-union
clauses in the first round.  No proof is claimed.

## Checksums

```text
1aa4dfe8d17fb090bf30bc1d3ac50f36fb61c4cdd796411381893fa37e190df0  2026-07-28_fixed_pair_orbit_fallback.py
cfb706c2a059abd22e547b04774a1aae68b019cc90c98980b2b4850231669af5  2026-07-28_fixed_pair_orbit5_smoke.jsonl
```

The driver also passes Python AST compilation and Ruff.

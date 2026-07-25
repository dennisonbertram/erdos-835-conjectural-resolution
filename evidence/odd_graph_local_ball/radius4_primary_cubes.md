# Deterministic proof-preserving cubes for the complete radius-4 CNF

`generate_radius4_primary_cubes.py` partitions a specified exact parent
CNF into deterministic cubes on the first unnormalized primary rows:
positions 32, 33, and 34.  A depth-\(d\) manifest has \(17^d\) leaves
and retains every colour at every split.  Therefore it is neither a
heuristic pruning rule nor an extra symmetry assumption.

For a parent formula \(F\), one-hot vertex clauses imply
\[
 F\models \bigvee_{c=0}^{16}x_{v,c}.
\]
Repeatedly splitting on this tautological cover makes the generated
leaves disjoint and exhaustive for every model of \(F\).  The manifest
records the parent CNF SHA-256; its verifier rederives the graph,
normalization, variables, leaves, and self-hash independently.

```bash
python3 evidence/odd_graph_local_ball/generate_radius4_primary_cubes.py \
  --parent-cnf-sha256 c6733572a4d62a1b6736e8332ae6ccebe63780969fed88957e78463240697a42 \
  --depth 1 --output /private/tmp/o16-r4-pairwise-cubes.json

python3 evidence/odd_graph_local_ball/verify_radius4_primary_cubes.py \
  --parent-cnf /private/tmp/o16-r4-pairwise.cnf \
  --manifest /private/tmp/o16-r4-pairwise-cubes.json

python3 evidence/odd_graph_local_ball/materialize_radius4_cube_cnf.py \
  --parent-cnf /private/tmp/o16-r4-pairwise.cnf \
  --cubes /private/tmp/o16-r4-pairwise-cubes.json --cube-id 0 \
  --output /private/tmp/o16-r4-pairwise-cube-000.cnf
```

## Certificate protocol

For a SAT leaf, its model is already a model of the parent CNF (the
cube only adds units).  Decode it with
`verify_radius4_generic_sinz_model.py`, which independently checks the
actual graph colouring and ignores solver status.

For an UNSAT conclusion, every materialized leaf must have a complete
proof checked against that leaf's exact CNF by an independent
DRAT/FRAT/LRAT checker.  Then the independently checked manifest proves
the leaves cover all parent models, so the conjunction of all leaf
UNSAT results proves the parent UNSAT.  A partial proof, failed check,
or `UNKNOWN` leaf leaves the parent status `UNKNOWN`; it cannot be
combined into an obstruction.

This is a tree certificate rather than an implicit solver assumption:
retain the parent CNF, audited cube manifest, every leaf CNF/hash,
every proof, and every external checker transcript.

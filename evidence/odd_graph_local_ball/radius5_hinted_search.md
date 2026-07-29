# Audited-radius-four hint repair for the complete joint radius-five model

`search_radius5_golf_joint_hinted.py` uses precisely the joint model in
`search_radius5_golf_joint.py`; it adds no assumption and removes no
constraint.  Its only change is a CP-SAT solution hint: the 120 independently
verified radius-four list edge-colourings are supplied as initial values for
the 12,600 `N` variables.

That hint is *not* a radius-five witness: its first fixed `P_(0,1)` extension
is known to be infeasible.  CP-SAT is therefore asked to repair it jointly
with all 58,800 `P` variables.  A timeout or `UNKNOWN` has no mathematical
meaning.  Any `SAT` result is passed to `verify_radius5_golf_joint.py`, which
reconstructs every closed neighbourhood in the full radius-five ball.

```bash
python3 -B evidence/odd_graph_local_ball/search_radius5_golf_joint_hinted.py \
  --seconds 300 --workers 8 --seed 0 \
  --certificate /private/tmp/o16-r5-golf-hinted.json
python3 -B evidence/odd_graph_local_ball/verify_radius5_golf_joint.py \
  --certificate /private/tmp/o16-r5-golf-hinted.json
```

## N-only congruence seed

`search_radius5_golf_n_congruence.py` has one deliberately limited purpose:
find a full collection of 120 list edge-colourings that also satisfies all
edge-count and degree-parity consequences of a triangle decomposition at all
105 `ij` slices.  It has no `P` variables, so its output is never evidence of
a radius-five ball.  Instead, its self-hashed N vector can seed the complete
model's repair search:

```bash
python3 -B evidence/odd_graph_local_ball/search_radius5_golf_n_congruence.py \
  --seconds 120 --workers 8 --seed 0 --output /private/tmp/o16-n-congruence.json
python3 -B evidence/odd_graph_local_ball/search_radius5_golf_joint_hinted.py \
  --seconds 300 --workers 8 --n-hint /private/tmp/o16-n-congruence.json
```

## Redundant triangle-decomposition propagation

`search_radius5_golf_joint_tight.py` also preserves the complete joint
model, but exposes two necessary conditions that are already logically
implied by its `P` constraints.  For every `ij` and colour `x`, it requires
the candidate x-graph to have an edge count divisible by three and every
residual graph degree even.  The implementation recomputes the fixed
`M_i/M_j` matching incidences directly rather than relying on a simplified
formula.  Thus it is a sound search strengthening, not a relaxation or a
new hypothesis.

```bash
python3 -B evidence/odd_graph_local_ball/search_radius5_golf_joint_tight.py \
  --seconds 300 --workers 8 --seed 0 --hint-audited-n \
  --certificate /private/tmp/o16-r5-golf-tight.json
```

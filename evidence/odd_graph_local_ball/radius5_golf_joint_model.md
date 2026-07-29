# Complete joint radius-5 model above the fixed cyclic golf L/M witness

This conditional extension model fixes the cyclic golf-design L/M
layers, while every N_uv(ij) and every P_ij(uvw) remains variable. SAT
supplies a radius-5 local witness extending this particular radius-4
witness. UNSAT would exclude only this golf L/M extension, not all
radius-4 colourings.

For all 120 uv pairs and 105 ij pairs, the model has N_uv(ij). Its
domain is the intersection of the two endpoint lists from Condition 4
of `radius4_reduction.md`; the incident `AllDifferent` constraints
force each N_uv to be an exact list-edge-colouring of K_15.

For all 105 ij pairs and 560 uvw triples, it has P_ij(uvw). A sound
static domain removes every fixed M_i and M_j value on the triple's
three pairs. For every ij,uv, the fourteen triples containing uv are
`AllDifferent` and each differs from N_uv(ij). Thus they are exactly
the fourteen values in Equation (1) of `radius5_reduction.md`.

## Independently re-derived dimensions

| object | count |
|---|---:|
| N variables | 12,600 |
| P variables | 58,800 |
| total integer variables | 71,400 |
| N incident `AllDifferent` constraints | 1,800 |
| P pair-extension `AllDifferent` constraints | 12,600 |
| dynamic P != N constraints | 176,400 |

No extra symmetry assumption is made. The verifier checks every N list
edge-colouring and all 12,600 extension equations, then reconstructs
the 73,457-vertex radius-5 ball and checks all 14,657 closed
neighbourhoods.

```bash
python3 evidence/odd_graph_local_ball/search_radius5_golf_joint.py --audit-only

python3 evidence/odd_graph_local_ball/verify_radius5_golf_joint.py --audit-only

python3 evidence/odd_graph_local_ball/search_radius5_golf_joint.py \
  --seconds 120 --workers 8 --seed 0 \
  --certificate /private/tmp/o16-r5-golf.json

python3 evidence/odd_graph_local_ball/verify_radius5_golf_joint.py \
  --certificate /private/tmp/o16-r5-golf.json
```

`UNKNOWN` produces no certificate and is not evidence either way.

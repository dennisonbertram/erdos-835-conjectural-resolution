# Finite-ball cover search in \(O_{16}\)

`search_local_cover.py` generates the exact radius-\(R\) ball around a
fixed vertex of
\[
O_{16}=KG(31,15)
\]
and searches for a 17-colouring that is bijective on every closed
neighbourhood whose centre has distance at most \(R-1\).

The root is fixed to colour 0 and its sixteen neighbours are fixed to
colours 1 through 16.  The fifteen non-root neighbours of the
colour-1 neighbour are then fixed to colours 2 through 16.  These
assignments remove only symmetry: the first family uses global colour
permutations, and the second uses the free permutation of the root's
fifteen underlying points.

Run, for example:

```bash
python3 evidence/odd_graph_local_ball/search_local_cover.py \
  --radius 4 --seconds 300
```

The default Boolean encoding has one indicator for each vertex-colour
pair and imposes exact-one constraints both at each vertex and for each
colour in every constrained closed neighbourhood.  `--encoding integer`
retains an independent `AllDifferent` formulation for cross-checking.

Interpretation:

- `INFEASIBLE` is an exact finite-radius obstruction and would rule out a
  global covering \(O_{16}\to K_{17}\).
- `OPTIMAL` or `FEASIBLE` says only that this finite ball is consistent.
- `UNKNOWN` is inconclusive.

When `--certificate PATH` is supplied and a solution is found, the script
writes all vertex masks and colours to JSON after independently checking
every constrained closed neighbourhood.

`construct_radius3.py` uses the field labels to split the radius-3
instance into fifteen independent edge-colouring problems on \(K_{16}\).
It is both a faster construction and an independently structured check
of the generic ball model.

## Verified radius-3 result

On 2026-07-24,

```bash
python3 evidence/odd_graph_local_ball/construct_radius3.py \
  --seconds-per-column 60 --workers 8 \
  --certificate evidence/odd_graph_local_ball/radius_3_certificate.json
```

returned `FEASIBLE`.  All fifteen column solvers returned `OPTIMAL`, each
in less than 0.12 seconds, and the assembled 2,057-vertex assignment
passed `verify_assignment`.  The committed certificate has SHA-256

```text
1392a94b45ab4f5c013200495ab8ac65c37f3d8f81ed5443bba3d5442a1d69ce
```

Thus radius 3 is rigorously consistent and cannot supply a finite local
obstruction.

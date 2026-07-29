# Complete generic radius-4 CNF certificate instance

`generate_radius4_generic_sinz_cnf.py` emits a deterministic DIMACS
encoding of the full radius-4 ball of
\(O_{16}=KG(31,15)\).  It is **not** a finite-field, one-factorization,
or Latin-square ansatz.

For every ball vertex \(v\) and colour \(c\in\{0,\ldots,16\}\), the
primary variable \(x_{v,c}\) means that \(v\) has colour \(c\).  Each
vertex gets an at-least-one clause and a standard 16-state Sinz
sequential at-most-one encoding.  For each of the 2,057 centres at
distance at most three and each colour, the CNF contains exactly one
at-least-one clause over the 17 vertices in that closed neighbourhood.
No neighbourhood at-most-one clauses are needed: 17 vertices each
receive one colour, while all 17 colours are required to appear, so
each appears exactly once.

The 32 unit clauses only choose a representative of a symmetry orbit:
the root and its 16 neighbours consume global colour relabelling; the
fifteen non-root neighbours of the first root neighbour consume the
residual permutation of the root's fifteen underlying points.  Every
colouring has a representative satisfying these units.

Consequently, this CNF is satisfiable exactly when the complete
generic radius-4 local-cover instance is satisfiable.  A checked UNSAT
proof would therefore exclude a global \(O_{16}\to K_{17}\) cover.
A SAT result is only a radius-4 local witness.

The status is now **SAT**: [`global_latin_radius4_bridge.md`](global_latin_radius4_bridge.md)
constructs a deterministic complete model.  Its independent semantic and
clause-by-clause verifier checks all 14,657 vertices and all 738,537 clauses
against the canonical CNF hash below.  This does not extend to radius five.

## Fixed dimensions

| item | count |
|---|---:|
| ball vertices | 14,657 |
| constrained closed neighbourhoods | 2,057 |
| primary variables | 249,169 |
| Sinz auxiliary variables | 234,512 |
| total variables | 483,681 |
| clauses | 738,537 |

The clauses comprise 14,657 vertex ALO clauses, 688,879 vertex Sinz
AMO clauses, 34,969 closed-neighbourhood colour ALO clauses, and 32
symmetry units.  Their length distribution is 32 unit clauses, 688,879
binary clauses, and 49,626 length-17 clauses.

## Reproducible commands

```bash
python3 evidence/odd_graph_local_ball/generate_radius4_generic_sinz_cnf.py \
  --cnf /private/tmp/o16-r4-generic.cnf \
  --map /private/tmp/o16-r4-generic.map.json \
  --manifest /private/tmp/o16-r4-generic.manifest.json

python3 evidence/odd_graph_local_ball/verify_radius4_generic_sinz_cnf.py \
  --cnf /private/tmp/o16-r4-generic.cnf \
  --map /private/tmp/o16-r4-generic.map.json \
  --manifest /private/tmp/o16-r4-generic.manifest.json
```

For an UNSAT claim, retain the exact CNF, the solver's complete proof,
the solver version and command, and an independent proof-checker
result.  The audit script validates the instance but deliberately does
not substitute for DRAT/FRAT/LRAT proof checking.  For SAT, write a
SAT-competition model and check it independently:

```bash
python3 evidence/odd_graph_local_ball/verify_radius4_generic_sinz_model.py \
  --model /private/tmp/o16-r4-generic.model
```

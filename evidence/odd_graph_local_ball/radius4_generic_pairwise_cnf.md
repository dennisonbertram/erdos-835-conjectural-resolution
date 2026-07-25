# Certificate-preserving propagation strengthening for the generic radius-4 ball

This is an acceleration of the complete generic radius-4 CNF, not a
restricted construction family.  The variable map and its 32 symmetry
units are unchanged.  `generate_radius4_generic_pairwise_cnf.py` emits
the base Sinz CNF followed by all pairwise clauses
\[
  \neg x_{u,c}\ \lor\ \neg x_{v,c}
\]
for distinct \(u,v\) in every constrained closed neighbourhood and
every colour \(c\).

## Why the new clauses are WLOG / equisatisfiable

Fix a closed neighbourhood \(Q\) of size 17 and a colour \(c\).  In
the base CNF, each member of \(Q\) has exactly one colour, and every
one of the 17 colours occurs at least once in \(Q\).  If two different
vertices of \(Q\) had colour \(c\), the remaining 15 vertices could
realize at most 15 distinct colours.  At least one of the remaining 16
colours would be absent, contradicting its local at-least-one clause.
Thus every added binary clause is entailed by the base formula.

Conversely the pairwise CNF contains all base clauses, so it has exactly
the same satisfying primary-colour assignments.  This addition is often
useful to CDCL because setting \(x_{u,c}\) immediately falsifies all
other \(x_{v,c}\) in its closed neighbourhood, instead of relying on a
global pigeonhole consequence.

The 32 units do not justify any *additional literal* by themselves.
They leave a diagonal \(S_{15}\) action: simultaneously relabel the
fifteen root points, the fifteen complement points other than the one
indexing the selected root neighbour, and the corresponding fifteen
finite colours.  This preserves the normalized root and selected
second-layer branch as a set of labelled constraints.  Exploiting that
residual symmetry safely requires a canonical-labelling or full
lex-leader construction over a solution-dependent 15-point structure;
it is not sound to arbitrarily fix another vertex-colour literal.
Accordingly this CNF adds no symmetry constraint at all: every added
clause is an explicit logical consequence proved above.

## Exact dimensions and audit

The stronger instance has the same 483,681 variables and adds
\[
2057\cdot17\cdot\binom{17}{2}=4,755,784
\]
binary clauses, for 5,494,321 clauses total.  Its clause-length
distribution is 32 unit clauses, 5,444,663 binary clauses, and 49,626
length-17 clauses.

```bash
python3 evidence/odd_graph_local_ball/generate_radius4_generic_pairwise_cnf.py \
  --cnf /private/tmp/o16-r4-pairwise.cnf \
  --map /private/tmp/o16-r4-pairwise.map.json \
  --manifest /private/tmp/o16-r4-pairwise.manifest.json

python3 evidence/odd_graph_local_ball/verify_radius4_generic_pairwise_cnf.py \
  --cnf /private/tmp/o16-r4-pairwise.cnf \
  --map /private/tmp/o16-r4-pairwise.map.json \
  --manifest /private/tmp/o16-r4-pairwise.manifest.json
```

Any terminal SAT model may be checked using the already separate
`verify_radius4_generic_sinz_model.py`: it verifies the primary colour
assignment directly against the graph and does not rely on the new
redundant clauses.  Any UNSAT proof must be checked against this exact
pairwise CNF; a solver's status, timeout, or partial trace is not a
certificate.

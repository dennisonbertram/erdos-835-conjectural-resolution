# Complete generic \(LS(3,4,20)\) CNF

This directory contains a deterministic, unrestricted encoding of the
derived-design obstruction

\[
LS(3,4,20).
\]

Every hypothetical \(LS(15,16,32)\), hence every \(17\)-colouring sought in
the \(k=16\) case of Erdős--Rosenfeld Problem #835, derives to an
\(LS(3,4,20)\). Therefore a checked UNSAT proof for this instance would
exclude \(k=16\). A satisfying assignment would construct the first known
nontrivial large set of Steiner quadruple systems, but would still be only a
necessary shadow of #835.

## Exact encoding

There is one primary Boolean \(x_{B,c}\) for every
\(B\in\binom{[20]}4\) and \(c\in[17]\). A Sinz sequential counter forces
each block to have exactly one colour. For every triple
\(T\in\binom{[20]}3\) and every colour \(c\), one at-least-one clause says
that some one of the seventeen extensions \(T\cup\{x\}\) has colour \(c\).
Because those seventeen blocks each have one colour, these clauses force
each triple star to use every colour exactly once.

The seventeen blocks extending \(\{0,1,2\}\) are assigned the colours in
point order. This removes only the free global colour permutation.

The canonical dimensions are:

- 82,365 primary variables;
- 77,520 Sinz auxiliaries;
- 159,885 variables total;
- 251,957 clauses.

The canonical CNF SHA-256 is

```text
f855ff1dcd09c420d8d086a9bd759c7906b7685b0e40eb0149eb42768424625f
```

## Reproduce and audit

```sh
python3 -B evidence/generate_ls_3_4_20_sinz_cnf.py \
  --cnf evidence/ls_3_4_20_generic_cnf/instance.cnf \
  --map evidence/ls_3_4_20_generic_cnf/variable_map.json \
  --manifest evidence/ls_3_4_20_generic_cnf/manifest.json

python3 -B evidence/verify_ls_3_4_20_sinz_cnf.py \
  --cnf evidence/ls_3_4_20_generic_cnf/instance.cnf \
  --map evidence/ls_3_4_20_generic_cnf/variable_map.json \
  --manifest evidence/ls_3_4_20_generic_cnf/manifest.json
```

The verifier does not import the generator. It reconstructs the complete
DIMACS byte stream, parses the supplied file, checks every dimension and
clause-length count, and checks both recorded hashes.

As of this commit, the complete CaDiCaL and CP-SAT runs are still in
progress. There is no SAT or UNSAT claim here.

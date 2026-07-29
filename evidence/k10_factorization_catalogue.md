# Machine-readable catalogue of the 396 one-factorizations of \(K_{10}\)

The half-link search must not assume that the standard round-robin
one-factorization is the only possibility.  Gelling proved that there are 396
isomorphism classes and printed representative schedules in his 1973 thesis:

<https://dspace.library.uvic.ca/items/97c7e4b6-8b9a-4f65-b747-fa48878b4d6f>

For a machine-readable and independently regenerated version, this directory
uses the open-source MathCheck2 data:

<https://bitbucket.org/cbright/mathcheck2>

The imported files are from MathCheck2 commit
`62db4780684028102da50b1fedab2501d3d47fb2`:

- `mathcheck_k10_initial_matrix.txt` is
  `lams_problem/ovals/initial_matrix`;
- `mathcheck_k10_factorizations_sat_literals.txt` is
  `lams_problem/ovals/k10_1-factorizations`.

The exact upstream assumptions file at that revision is:

<https://bitbucket.org/cbright/mathcheck2/raw/62db4780684028102da50b1fedab2501d3d47fb2/lams_problem/ovals/k10_1-factorizations>

Their SHA-256 hashes are, respectively,

```text
a272e9741feecec760a418cd02d202aa91e56715191a8a92d5cc735b1fbed81d
809ef98da1c5b7d70a9e47b7eaebead0719c1eb3521fdb6bdbd6125938fbe164
```

The second file has exactly 396 lines.  Each line records one representative
as the positive SAT literals of a partially fixed incidence matrix.
`decode_mathcheck_k10_factorizations.py` combines those literals with the
fixed matrix and writes `k10_one_factorizations_396.txt` in a transparent
edge-list format.

Run:

```bash
python3 evidence/decode_mathcheck_k10_factorizations.py \
  evidence/mathcheck_k10_initial_matrix.txt \
  evidence/mathcheck_k10_factorizations_sat_literals.txt \
  evidence/k10_one_factorizations_396.txt
```

The decoder checks, independently for every line, that:

1. there are nine factors;
2. each factor is a perfect matching of the ten vertices;
3. the factors partition all 45 edges of \(K_{10}\);
4. all 396 decoded representatives are distinct;
5. the fixed first factor is
   \(\{01,23,45,67,89\}\).

Expected output:

```text
decoded_factorizations=396
distinct_factorizations=396
edge_partition_checks=PASS
fixed_first_factor_checks=PASS
```

The decoded catalogue has SHA-256
`226c5addbf5915c7a68023302c2eefc80cbe7cf243441f2fea68b8f263f7bc46`.
These checks establish that the file is a valid collection of 396 distinct
one-factorizations.  The completeness up to isomorphism is inherited from the
published Gelling classification and the independent MathCheck2 generation;
the small decoder does not itself perform graph-isomorphism classification.

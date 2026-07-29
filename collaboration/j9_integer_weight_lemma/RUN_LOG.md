# Independent audit log

The proof in `NOTE.md` was checked line by line against the stated lemma.

Checks performed:

- recomputed every edge/triangle incidence coefficient;
- checked both endpoint cases in the exclusion of a weight-\(-2\) edge;
- checked the boundary cases \(n_v=0,1\) separately from the use of an edge
  inside \(N(v)\);
- verified that the two clique arguments use only already-proved facts;
- ran the standard-library arithmetic audit with assertions enabled;
- ran Python bytecode compilation.

Commands:

```sh
python3 collaboration/j9_integer_weight_lemma/verify_arithmetic.py
PYTHONPYCACHEPREFIX=/private/tmp/erdos835-j9-pycache \
  python3 -m py_compile collaboration/j9_integer_weight_lemma/verify_arithmetic.py
/Users/dennison/Library/Python/3.9/bin/ruff check \
  collaboration/j9_integer_weight_lemma/verify_arithmetic.py
```

Result: all commands pass.

Scope: this establishes the stated \(K_{13}\) integer edge-weight lemma. It is
one component of the proposed lift analysis and is not a complete resolution
of Erdős--Rosenfeld problem #835.

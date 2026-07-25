# Sound residual-diagonal \(S_{15}\) normalization

After the existing 32 units, the remaining combined graph-colour
symmetry is the diagonal \(S_{15}\).  Index the root points by
\(i\in\{0,\ldots,14\}\), and the non-special complement points by
\(u_a\), \(a\in\{0,\ldots,14\}\).  The already-normalized special
complement point is \(u_\star\), with colour 1.  Consider the matrix
\[
 Q_{a,i}=\operatorname{col}(C_{u_a,i}).
\]
Each row contains colour 1 exactly once, from local bijectivity at the
root-neighbour indexed by \(u_a\).  For a fixed column \(i\), the
sixteen values \(\operatorname{col}(C_{u,i})\), as \(u\) ranges over
the complement points, form the derangement permutation \(L_i\) from
Condition 2 of `radius4_reduction.md`.  The normalized
\(u_\star\) entry is colour \(i+2\), not colour 1; therefore colour 1
occurs in exactly one of the fifteen displayed rows.  Hence the
positions of colour 1 define a permutation
\[
 f:a\longmapsto i\quad\text{where }Q_{a,i}=1.
\]

Concretely, \(h\) maps root point \(i\) to \(h(i)\), complement point
\(u_a\) to \(u_{h(a)}\), and colour \(a+2\) to \(h(a)+2\), while
fixing \(u_\star\), colour 0, and colour 1.  It preserves every one of
the original 32 units: the root-neighbour labels move with their
colours, and the selected branch relation
\(C_{u_\star,i}\mapsto i+2\) moves to
\(C_{u_\star,h(i)}\mapsto h(i)+2\).  Thus this is an actual action on
the normalized model, not an informal relabelling.  It maps rows,
columns, and non-special finite colours by \(h\), hence maps \(f\) to
\(hfh^{-1}\).  Permutations are conjugate exactly when they have the
same cycle partition.  There are \(p(15)=176\) partitions.  For each
partition, this encoding selects the standard representative whose
cycles use contiguous labels in non-increasing cycle-length order.
Every solution can be relabelled into exactly one such cycle type, so
the condition is WLOG; it does not assume a value observed in a
search.

The CNF adds 176 selector variables, one selector ALO, and 2,640 binary
implications from a selected cycle representative to its fifteen
colour-1 matching entries.  Two different representatives force two
colour-1 vertices in some common root-neighbour closed neighbourhood,
which is immediately inconsistent in the pairwise parent CNF.  Thus
no selector AMO is needed.  The instance has 483,857 variables and
5,496,962 clauses.

```bash
python3 evidence/odd_graph_local_ball/generate_radius4_diagonal_matching_symbreak_cnf.py \
  --cnf /private/tmp/o16-r4-diagonal.cnf \
  --map /private/tmp/o16-r4-diagonal.map.json \
  --manifest /private/tmp/o16-r4-diagonal.manifest.json

python3 evidence/odd_graph_local_ball/verify_radius4_diagonal_matching_wlog.py \
  --map /private/tmp/o16-r4-diagonal.map.json

# First audit the supplied parent with verify_radius4_generic_pairwise_cnf.py.
python3 evidence/odd_graph_local_ball/verify_radius4_diagonal_matching_cnf.py \
  --parent-cnf /private/tmp/o16-r4-pairwise.cnf \
  --cnf /private/tmp/o16-r4-diagonal.cnf \
  --map /private/tmp/o16-r4-diagonal.map.json \
  --manifest /private/tmp/o16-r4-diagonal.manifest.json
```

For a SAT result, use the existing semantic primary-colour verifier.
For UNSAT, check a complete proof against this exact symmetry-broken
CNF; the conjugacy argument transfers UNSAT back to the unrestricted
pairwise and base instances.

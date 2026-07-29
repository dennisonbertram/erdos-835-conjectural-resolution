# Finite three-cell obstruction search

Date: 2026-07-27.

This directory's proved result is in `NOTE.md` and is checked by
`verify_dead_prefix.py`.  The separate
`search_three_cell_obstruction.py` program records a bounded exploratory
search that did **not** find another obstruction.  Its negative output is
included for reproducibility; it is not a proof of completion.

## Question tested

Partition the thirteen target vertices into three nonempty cells.  Give the
six cell-pair edge types nonnegative integral weights.  For each colour,
compute exactly the minimum weight of a perfect matching on its support from
the three cell-attendance counts.  If the sum of these colourwise minima
exceeded the total weight of \(K_{13}\), the support family could not have
edge-disjoint perfect matchings.

The outer dynamic program ranges over all six target support profiles and all
cell-level missing-count types while enforcing the correct aggregate missing
budget \(5|C_i|\) in each cell.  This is a relaxation: it does not require the
cell totals to be realizable by a \(13\times17\) zero-one matrix with every
individual row sum five.  Therefore even a positive output would only be a
candidate requiring reconstruction as an actual class-B instance and an
independent exact verifier.

## Exact bounded run

From the repository root:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/first_lift_global_theorem/search_three_cell_obstruction.py \
  --samples 10 --seed 835 --max-weight 6
```

Output:

```text
checked=1344 best=(0, (1, 1, 11), (7, 10, 0), (1, 0, 0, 0, 0, 0))
finite weighted three-cell search only; no universal conclusion
```

The 1,344 cases are:

- every unordered partition of thirteen into three positive cell sizes;
- all six class-B support profiles;
- six fixed weight vectors plus ten pseudorandom vectors generated once from
  seed 835, with entries in \(\{0,\ldots,6\}\).

The best margin was zero.  Thus this particular finite family supplied no
strict weighted obstruction.  This does not exclude other weight vectors,
more cells, non-cellular certificates, genuine incomplete class-B instances,
or incomplete class-B-prime/fan-realizable instances.

## Status of the actual problem

The universal completion question at \(n=13\) remains open in this repository.
The three nested scopes must not be conflated:

1. class B: abstract support matrices with row sums five and odd column
   complements of size at most five;
2. class B-prime: those supports induced by a proper saturated colouring of
   \(K_{18}-E(K_{13})\);
3. fan-realizable: the still smaller family arising from one simultaneous
   thirteen-fan.

No counterexample to any of these three scopes is claimed here.

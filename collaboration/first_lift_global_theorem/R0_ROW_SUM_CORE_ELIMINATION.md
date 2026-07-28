# Row-sum elimination of three exceptional-profile cores

Date: 2026-07-27.

## Result and scope

Let \(F\) be an \(r=0\) seven-matching prefix: four matchings on
size-eight supports and three on size-ten supports. Then
\[
 |E(F)|=31,\qquad 2\le d_F(v)\le7.
\]
There remain seven size-ten and three size-eight supports.

This note combines the exact pair catalogue with the complement-row
identity to eliminate three obstruction-core types from a hypothetical
situation in which all seven remaining size-ten supports are blocked:
\[
 K_{3,3,3},\qquad K_{5,5},\qquad K_{3,7}.
\]

This is not yet an eighth-colour theorem. The types
\[
 K_{5,1,1,1},\quad K_{3,3,1,1},\quad
 K_{3,1,1,1,1},\quad K_6
\]
remain unresolved.

## Edge-placement reuse bound

Suppose a fixed core \(J\), with \(C\) vertices and \(e\) edges, is used
to block \(t\) remaining size-ten supports. Every such support complement
is a triple contained in \(O=V(K_{13})\setminus V(J)\).

There are \(31-e\) edges of \(F\) outside the core, and at most
\(\binom{13-C}{2}\) can lie wholly in \(O\). Therefore at least
\[
 r=\max\{0,31-e-\tbinom{13-C}{2}\}
\]
of them touch the core. Since
\(\sum_v(d_F(v)-2)=36\), the complement incidences available in \(O\)
satisfy
\[
 3t\le\sum_{v\in O}(d_F(v)-2)
 \le36+2C-2e-r. \tag{1}
\]

For the seven catalogue types \(37,55,333,5111,3311,31111,6\), (1)
gives the ceilings
\[
 2,\ 1,\ 0,\ 4,\ 2,\ 4,\ 6.
\]
In particular, a \(K_{3,3,3}\) core cannot occur at all.

## Eliminating \(K_{5,5}\)

A \(K_{5,5}\) can coexist only with a \(K_{5,1,1,1}\). Fixing a canonical
\(K_{5,5}\), the pair verifier finds exactly twenty compatible labelled
second cores. Every union has 28 edges and gives degree zero to all three
vertices outside the \(K_{5,5}\).

Even one support blocked by this ten-vertex core has that exact outside
triple as its complement. Hence all three outside vertices require
\(d_F(v)\ge3\), or nine degree endpoints in total. Only three edges remain
outside the 28-edge union, providing at most six endpoints. This is
impossible.

## Eliminating \(K_{3,7}\)

Equation (1) says a fixed \(K_{3,7}\) blocks at most two supports, so seven
blocked supports require at least four distinct cores.

After fixing one \(K_{3,7}\), the exact pair screen leaves respectively
\[
9,\ 105,\ 210,\ 35
\]
compatible labelled cores of types \(37,5111,3311,31111\). Exhausting all
pairs of these candidates shows that every surviving three-core union has
type \(37+37+37\); there are nine labelled cases. Exactly three
four-distinct-\(37\) families survive, each with 28 union edges. No fifth
core can coexist.

The verifier then adds every possible three-edge completion to 31 edges.
Exactly 147 completed graphs satisfy \(2\le d_F(v)\le7\). Four fixed cores
with reuse ceiling two must have multiplicities \(2,2,2,1\), giving 588
graph/reuse cases.

For a \(K_{3,7}\), the outside set is already a triple, so every associated
support complement is forced. Subtracting those seven triple incidences
from the row capacities \(d_F(v)-2\) leaves the degree sequence that the
three five-set complements would need. In none of the 588 cases does this
residual vector even have all entries in \(\{0,1,2,3\}\) and total 15.
Thus no all-seven obstruction can contain a \(K_{3,7}\).

## Verification

From the repository root:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/first_lift_global_theorem/verify_r0_row_sum_core_elimination.py
```

The verifier uses only the Python standard library and the independently
checked core generator in `verify_r0_core_pairs.py`. It reconstructs every
counter above. Its final scope line explicitly leaves the four surviving
core types open.

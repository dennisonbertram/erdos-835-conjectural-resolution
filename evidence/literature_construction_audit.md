# Construction-literature audit for Erdős–Rosenfeld #835

Date checked: 2026-07-25.

## Target, and the distinction that matters

The requested coloring is exactly a large set
\[\operatorname{LS}(k-1,k,2k),\]
i.e. a partition of all `k`-subsets of a `2k`-set into `k+1` Steiner systems
`S(k-1,k,2k)`.  A constituent by itself is already a very strong object: after
derivation it is the standard perfect-1-code/odd-graph Steiner-system problem.
The 2025 survey chapter of Krotov and Potapov states the equivalent forms
`S(w-1,w,2w+1)` and `S(w,w+1,2w+2)`, and identifies the first open odd-graph
case as `O_16`.

Sources:

* D. Krotov and V. Potapov, *Completely Regular Codes and Equitable
  Partitions* (2025), section on perfect codes in odd graphs:
  <https://www.researchgate.net/publication/388978477_Completely_Regular_Codes_and_Equitable_Partitions>.
* The current problem discussion gives the direct equivalence between a
  `(k+1)`-coloring and an `LS(k-1,k,2k)`:
  <https://www.erdosproblems.com/forum/thread/835?embed=1>.

Thus an individual Steiner system, an odd-graph perfect code, a derived
design, a local ball coloring, or a lower-strength shadow is **not** a solution
of #835.  A full construction must additionally partition all `k`-sets.

## Ordered designs give a sharp but insufficient relaxation

An ordered design `OD(t,n,v)` is an `n x binom(v,t)t!` array of injective
columns such that every ordered `t`-tuple occurs once in every selection of
`t` rows.  An `LOD` partitions all ordered `n`-tuples among such arrays.  This
is the definition used in Jin--Zhu--Gu--Sun (2022), which also records
Teirlinck's 1988 theorem:

> if `m=prod p_i^{alpha_i}` and `alpha_i(p_i-1)>t` for every `i`, then
> `LOD(t,t+1,t+m)` exists.

Set `t=k-1` and `m=k+1`.  If `k+1` is prime, its sole condition is
`k>k-1`; hence the theorem gives
\[
  \operatorname{LOD}(k-1,k,2k) \qquad (k+1\text{ prime}).
\]
This includes the principal unresolved candidate `k=16`.

Sources:

* L. Teirlinck, *On large sets of disjoint ordered designs*, Ars
  Combinatoria **25** (1988), 31--37.  Bibliographic record:
  <https://combinatorialpress.com/ars/vol25/>.
* K. Jin, T. Zhu, Z. Gu, X. Sun, *Latin Matchings and Ordered Designs
  OD(n-1,n,2n-1)*, Mathematics **10** (2022), 4703, especially the definition
  of `OD`/`LOD` and its summary of Teirlinck's theorem:
  <https://doi.org/10.3390/math10244703>.

This does **not** settle #835.  Here is the precise missing condition.  From a
Steiner system `D=S(k-1,k,2k)`, put all `k!` orderings of each block of `D` as
columns of an array `A_D`.  The Steiner property proves directly that `A_D` is
an `OD(k-1,k,2k)`.  From an `LS(k-1,k,2k)`, these arrays form the corresponding
`LOD(k-1,k,2k)`.

For the converse, an `LOD` would need the following additional *support-orbit
closure*:

1. Every array is a union of complete `S_k`-orbits of columns under coordinate
   permutation (so it contains either all or none of the `k!` orderings of each
   underlying `k`-set).
2. The `k!` orderings of a given `k`-set lie in one, rather than several,
   arrays.

Under this condition, forgetting order converts each array into one
`S(k-1,k,2k)`, and the `LOD` becomes the desired large set.  The ordinary `LOD`
axioms only constrain ordered projections; they do not impose this orbit
closure.

This is a genuine gap, not a terminology issue.  At `k=6`, Teirlinck's theorem
does give `LOD(5,6,12)` (take `m=7`), whereas the current #835 discussion
records the constant-weight-code obstruction to the required 7-coloring for
all `3 <= k <= 14`.  Therefore an implication `LOD(k-1,k,2k) =>
LS(k-1,k,2k)` is false.

Equivalently, perpendicular-array constructions must be strengthened from an
ordered partition to an orbit-closed partition.  The usual correspondence is
`OD(t,n,v) = PA_{t!}(t,n,v)` with all orderings prescribed; the needed extra
symmetry is not part of a general perpendicular array.

## Exact necessary odd-graph consequence

Fix a point `infinity`.  In a hypothetical large set, the blocks in each
component design that contain `infinity`, with `infinity` removed, form a
perfect 1-code in the odd graph on `(k-1)`-subsets of the remaining `(2k-1)`
points.  Across the `k+1` component designs these codes partition that odd
graph.  Thus #835 entails not merely one odd-graph perfect code, but a
partition into `k+1` of them.

Fiol proves spectrally that an odd graph `O_l` with `l` odd has no perfect
1-code.  Consequently this whole odd-`k` family is excluded already at the
constituent level.  This does not touch the live prime-plus-one candidates,
where `k` is even.

Source: M. A. Fiol, *A new class of polynomials from the spectrum of a graph,
and its application to bound the k-independence number*, Linear Algebra and
its Applications **605** (2020), 1--19; preprint and the stated corollary:
<https://arxiv.org/abs/1907.08626>.

## What was and was not obtained

No full `LS(k-1,k,2k)` construction, no verifier witness, and no broad
impossibility theorem for even `k` were found in this literature pass.

The actionable construction problem is now sharply stated: start from an
available `LOD(k-1,k,2k)` (in particular at `k=16`) and enforce complete
coordinate-permutation orbits of every support.  This is exactly the global
constraint that existing ordered-design/perpendicular-array theorems leave
uncontrolled.

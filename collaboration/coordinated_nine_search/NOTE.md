# Exact-search attack on the coordinated ninth frontier

Date: 2026-07-28.

## Result

No class-B support instance with packing number eight was found.  In fact,
every one of the 3,726 fixed instances tested by exact optimization had
packing number
\[
\boxed{17}.
\]
Thus every tested instance admits not merely a ninth matching but a full
partition of all 78 edges of \(K_{13}\) into the seventeen prescribed
support-perfect matchings.

This is a finite computational survey.  It is exact for each tested
instance but is **not** an exhaustive proof over all class-B support
matrices and does not prove a universal ninth-matching theorem.

## Model

For profile \(r\in\{0,\ldots,5\}\), write \(C_i\) for the seventeen
support complements.  Their sizes are
\[
 5^{\,7+r},\qquad 3^{\,10-2r},\qquad 1^r, \tag{1}
\]
and every vertex occurs in exactly five \(C_i\)'s.  The support of colour
\(i\) is \(V(K_{13})\setminus C_i\).

For a fixed instance, the exact CP-SAT model has a Boolean variable
\(z_i\) saying whether colour \(i\) is packed and a Boolean variable
\(x_{i,e}\) for every edge \(e\) inside its support.  It imposes
\[
 \sum_{e\ni v}x_{i,e}=z_i
 \quad(v\text{ in support }i), \tag{2}
\]
and
\[
 \sum_i x_{i,e}\le1
 \quad(e\in E(K_{13})), \tag{3}
\]
then maximizes \(\sum_i z_i\).  An `OPTIMAL` result is therefore the exact
packing number of that fixed matrix.  The program independently checks
every returned matching and all edge-disjointness conditions.

There is a useful tightness invariant.  The total edge demand of all
seventeen colours is
\[
4(7+r)+5(10-2r)+6r=78=|E(K_{13})|. \tag{4}
\]
Consequently an optimum of seventeen automatically uses every edge
exactly once.  At each vertex the same fact is local: the vertex lies in
twelve supports, so a full completion uses its twelve incident edges
exactly once.

## Campaigns

### Two-switch survey

For each profile, CP-SAT first constructs one complement-incidence matrix
with the prescribed column sizes and row sum five.  A Markov walk then
uses 2-switches between two columns, preserving both conditions exactly.
Every sampled fixed matrix is solved to optimality with one solver worker.

Two deterministic-seed runs gave:

| run | samples per profile | profiles | exact outcomes |
|---|---:|---:|---:|
| pilot, seed 8359, 500 switches/sample | 100 | 6 | \(600/600\) optimum 17 |
| expanded, seed 9361, 1000 switches/sample | 500 | 6 | \(3000/3000\) optimum 17 |

The expanded run took 81.600 seconds.  Its largest per-instance solver
wall time was 0.042 seconds.  These are Markov-chain samples; no claim of
uniformity or independence is made.

The expanded run is reproduced by:

```sh
python3 collaboration/coordinated_nine_search/search_exact_packing_survey.py \
  --campaign random \
  --samples 500 \
  --switches 1000 \
  --seconds 10 \
  --seed 9361
```

### Maximally duplicated supports

Random switching tends to produce few identical columns, so a separate
campaign attacked the opposite extreme.  For each complement size, its
number of labelled colours was partitioned into multiplicities at most
five.  A master CP model sought a row-regular realization with those
duplicate groups.  Shapes were tried in increasing order of the total
number of distinct generating groups, and the first twenty feasible
instances per profile were passed to the exact packing solver.

All \(120/120\) instances had optimum seventeen.  The smallest attainable
numbers of generating groups seen were:

\[
\begin{array}{c|rrrrrr}
r&0&1&2&3&4&5\\ \hline
\text{groups}&7&7&6&6&7&7.
\end{array}
\]

The campaign included matrices with eleven duplicate columns, complement
overlap five, and as few as five distinct vertex-incidence rows.  Hence
the full completions were not an artifact of generic-looking supports.
The search takes only the first CP realization for each tested
multiplicity shape and is not exhaustive over all realizations.

Reproduce it with:

```sh
python3 collaboration/coordinated_nine_search/search_exact_packing_survey.py \
  --campaign duplicates \
  --duplicates-limit 20 \
  --seconds 10
```

### Previously adversarial dead-prefix instances

The six committed dead-prefix support instances for
\[
r=1,\ r=2,\ r=3\ (C\subset G),\ r=3\ (D\subset G),\ r=4,\ r=5
\]
were also sent through the same exact packing-number model.  Each has an
arbitrary seven-prefix that blocks all ten unused supports, so they are
adversarial to blind prefix extension.  Nevertheless all \(6/6\) fixed
support instances had exact optimum seventeen.

Reproduce this cross-check with:

```sh
python3 collaboration/coordinated_nine_search/search_exact_packing_survey.py \
  --campaign certificates \
  --seconds 10
```

## What the search says—and what it does not

Across generic, maximally symmetric/duplicated, and known dead-prefix
instances, the observed packing number never landed at any value from
nine through sixteen: every exact result jumped all the way to seventeen.
This strongly motivates the following conjecture.

> **Class-B completion conjecture.** Every target class-B support instance
> on \(K_{13}\) has a full prescribed-support decomposition of \(K_{13}\).

The conjecture is stronger than the already proved coordinated-eight
theorem.  If true, it would close every subsequent matching step at once.
The present evidence does not prove it.  A counterexample returned with
optimum at most eight would also need an independently replayable
proof-logging SAT certificate for the no-nine upper bound before being
treated as publication-grade.

The exact structural obstruction catalogues and fixed-core reuse bounds
for the ninth step are in
`../coordinated_nine_structural/NOTE.md`.  The empirical all-or-full
phenomenon here suggests that switching among complete decompositions,
rather than extending an arbitrary eight-prefix, is the more promising
next theoretical target.

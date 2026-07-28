# The r=0 three-family Helly gate is false

Date: 2026-07-28.

## Exact counterexample

The following plausible strengthening of the certified two-family gate is
false, even after imposing the complete class-B row equations:

> If three remaining size-ten families are pairwise compatible, then they
> admit one simultaneous triple of pairwise edge-disjoint perfect matchings.

Take the six edge-disjoint prefix matchings

\[
\begin{array}{c|l}
C_0&01,\ 2\,11,\ 46,\ 5\,12\\
C_1&02,\ 36,\ 4\,10,\ 79\\
C_2&0\,12,\ 37,\ 6\,10,\ 89\\
C_3&03,\ 12,\ 49,\ 7\,10,\ 8\,12\\
C_4&15,\ 28,\ 3\,10,\ 69,\ 7\,12\\
C_5&1\,12,\ 34,\ 58,\ 67,\ 9\,10 .
\end{array}
\]

Their sizes are \(4,4,4,5,5,5\), their edges are pairwise disjoint, and
their union \(D\) has degree sequence

\[
(4,4,4,5,4,3,5,5,4,5,5,1,5).
\]

Use the seven remaining triple complements

\[
012,\ 012,\ 012,\ 379,\ 7\,9\,12,\ 6\,7\,12,\ 468
\]

and the four remaining five-set complements

\[
6\,7\,8\,10\,12,\quad
3\,5\,6\,9\,10,\quad
3\,4\,5\,8\,10,\quad
3\,4\,9\,10\,12 .
\]

Together with the six complements left unmatched by the prefix, these
are exactly seven five-sets and ten triples, and every vertex has total
complement multiplicity five.  Equivalently, the eleven displayed
remaining rows satisfy

\[
\rho(v)=d_D(v)-1.
\]

## Pairwise compatibility but no simultaneous triple

Put \(Y=V\setminus\{0,1,2\}\).  The graph \(K_Y-D[Y]\) has exactly 42
perfect matchings.  In particular it contains the two edge-disjoint
perfect matchings

\[
\begin{aligned}
P&=\{35,47,68,9\,11,10\,12\},\\
Q&=\{39,45,6\,12,78,10\,11\}.
\end{aligned}
\]

Thus any two of the three repeated colour occurrences can use \(P,Q\).

There is nevertheless no edge-disjoint triple.  The exact enumeration
has 190 unordered disjoint pairs among the 42 perfect matchings, and
every such pair contains the edge \(39\) in exactly one member.  If
three perfect matchings were pairwise edge-disjoint, at most one could
contain \(39\), leaving a disjoint pair in which neither contains it.
That contradicts the enumerated bipartition certificate.

This is a finite exact certificate, not a general structural proof.  The
verifier independently generates all 42 perfect matchings and checks all
\(\binom{42}{2}\) pairs.

## Exact scope: the seven families still coordinate

This counterexample kills the arbitrary-three Helly lemma, not the
coordinated-\(r=0\) goal.  Of the 35 choices of three occurrences among
all seven remaining size-ten families, exactly 34 admit a simultaneous
triple.  The only failure is the three repeated \(012\) occurrences.

For example, occurrences \(012,012,379\) use

\[
\begin{aligned}
&\{35,47,68,9\,11,10\,12\},\\
&\{39,45,6\,12,78,10\,11\},\\
&\{04,16,25,8\,10,11\,12\}.
\end{aligned}
\]

The correct remaining target is therefore a seven-family selection
theorem, not a Helly theorem for every pairwise-compatible subtriple.

## Reproduction

Run the independent exact verifier:

```sh
python3 collaboration/r0_three_family_helly_gate/verify_counterexample.py
```

The CEGIS search is separate from the certificate:

```sh
python3 collaboration/r0_three_family_helly_gate/search_counterexamples.py \
  --orbits 0 --cut-batch 10000
```

There are 39 ordered Venn types for three triple complements and exactly
16 types modulo permuting the three family occurrences.  The search
enumerates all 16, including repeated supports.  It uses the certified
two-family gate to express pairwise compatibility and lazily adds exact
clauses excluding each discovered simultaneous matching triple.  Search
output is evidence only; `verify_counterexample.py` checks the displayed
certificate without a SAT dependency.

## Global seven-family campaign

The separate global CEGIS model asks whether all 35 choices of three among
the seven remaining size-ten occurrences can fail simultaneously.  A first
10,000-round campaign over the stricter \(K_6-e\)-free subspace generated
6,992,960 valid coordination cuts and 10 dense-core cuts, ending with
7,033,625 clauses after 270.168 seconds.  It found no counterexample, but it
also did not prove unsatisfiability.  This is search evidence only, and is
not the full remaining search because \(K_6-e\) occurrences belonging to at
most five triple rows must remain in scope.

`search_global_counterexamples.py` now uses the correct boundary clause:
it always excludes \(K_6\), while a \(K_6-e\) is excluded only when six
specified triple rows all avoid that core.  The row-avoidance literals are
part of the learned clause.

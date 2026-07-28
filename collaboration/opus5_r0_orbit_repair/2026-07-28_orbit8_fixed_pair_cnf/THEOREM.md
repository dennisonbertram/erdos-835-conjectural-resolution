# Orbit 8: certified prescribed-colour cut sufficiency

Date: 2026-07-28

## Result

Let \(V=\{0,\ldots,12\}\), let

\[
R_0=012,\qquad R_1=123,\qquad R_2=124,
\]

and put \(S_i=V\setminus R_i\).  Let \(D\subseteq E(K_{13})\), put
\(G=K_{13}-D\), and define

\[
t(v)=|\{i:v\in R_i\}|.
\]

Suppose:

1. \(|D|=27\);
2. \(t(v)+1\le d_D(v)\le5\) for every \(v\in V\);
3. every support-capacity cut holds:
   \[
   \sum_{i=0}^2\max(0,|S_i\cap U|-5)\le e_G(U)
   \qquad(U\subseteq V);
   \tag{C}
   \]
4. \(G\) contains edge-disjoint perfect matchings \(P_0\) on \(S_0\)
   and \(P_1\) on \(S_1\).

Then \(G\) contains pairwise edge-disjoint perfect matchings \(M_i\) on
\(S_i\), for \(i=0,1,2\).

This is exactly the orbit-8 prescribed-colour cut-sufficiency statement
used by the campaign.  The exact eleven-row equations imply the lower
degree bounds because \(\rho(v)=d_D(v)-1\) and \(\rho(v)\ge t(v)\).
Pairwise compatibility supplies premise 4.  The certificate does not
assume that \(D\) decomposes into six prefix matching layers, does not
encode the compatible-pair premises for the other two support pairs, and
does not encode the remaining-row realization.

The lower degree vector is

\[
(2,4,4,2,2,1,1,1,1,1,1,1,1).
\]

## Complete compatible-pair catalogue

The Venn signature in masks \(1,\ldots,7\) is

\[
(1,1,0,1,0,0,2).
\]

All three row intersections have size two; the deterministic convention
selects the pair \((0,1)\).  Each support has ten vertices and therefore
945 perfect matchings.  Exhaustive enumeration finds exactly
\(570{,}780\) ordered edge-disjoint pairs \((P_0,P_1)\).

For every pair, the classifier decomposes \(P_0\cup P_1\) into alternating
paths and cycles.  Along each component it records the full three-row Venn
mask of every vertex and the matching colour of every edge.  It minimizes
the component words under path reversal, coloured-cycle dihedral symmetry,
within-cell vertex permutations, and the two row symmetries that stabilize
the selected unordered support pair.  The resulting invariant has exactly
sixteen values.

This invariant calculation was checked independently by building the
explicit action graph on all \(570{,}780\) labelled pairs.  Its eight
distinct generators consist of adjacent transpositions within Venn cells
and a canonical vertex realization of the nonidentity selected-pair row
symmetry.  The action graph has exactly sixteen connected components, and
each component is exactly one invariant bucket.  Thus the sixteen
deterministic representatives in
`2026-07-28_orbit8_fixed_pair_results.jsonl` are exhaustive, not a sampled
catalogue.

## Quantifier and symmetry audit

Assume for contradiction that the result fails.  Choose the compatible
pair \(P_0,P_1\) from premise 4.  A row-and-vertex relabeling preserving the
displayed support system maps this pair to one of the sixteen fixed
representatives.  Apply the same relabeling to \(D\).  It preserves
\(|D|\), the vertex degree bounds, every capacity cut, pair availability,
and the assertion that no simultaneous prescribed triple exists.

After this fixed-pair reduction there are **no additional solver symmetry
clauses**.  This point is essential: canonicalizing \(D\) independently
after a labelled pair has been fixed would be unsound.  Instead, every
compatible-pair action orbit gets its own formula, and the relabeled \(D\)
is accepted without any post-fixed-pair normalization.

For each representative, the frozen formula contains:

1. the exact condition \(|D|=27\);
2. the displayed lower degree bounds and \(d_D(v)\le5\);
3. every capacity cut not already implied by the base bounds;
4. a negative unit clause for every fixed-pair edge, so that the chosen
   pair is present in \(G\);
5. one clause forcing \(D\) to meet every perfect matching on \(S_2\)
   edge-disjoint from the fixed pair; and
6. learned clauses
   \[
   \bigvee_{e\in M_0\cup M_1\cup M_2}[e\in D]
   \tag{T}
   \]
   for simultaneous triples of pairwise edge-disjoint support matchings.

Every clause of type (T) is a logically necessary condition for a
counterexample: if all fifteen union edges were outside \(D\), those three
matchings would be the desired conclusion.  Under the same counterexample
assumption, every direct fixed-pair extension clause is also necessary.
Consequently, UNSAT for all sixteen formulas rules out every possible
counterexample.  The CEGIS search only discovers valid clauses of type
(T); soundness does not require the discovered clauses to be
symmetry-closed.

## All capacity cuts

There are \(3{,}872\) positive instances of (C).  The formulas explicitly
encode the 499 that are not already implied by the base bounds:

| \(|U|\) | encoded cuts |
|---:|---:|
| 6 | 406 |
| 7 | 92 |
| 8 | 1 |

The other \(3{,}373\) cuts are automatic.  To check this independently,
let \(W=V\setminus U\), put

\[
L=\sum_{v\in W}(t(v)+1),
\]

and let \(q\) be the number of deleted edges not internal to \(U\).  The
degree lower bounds outside \(U\) imply both

\[
q\ge\left\lceil\frac L2\right\rceil
\quad\text{and}\quad
q\ge L-\binom{|W|}{2}.
\]

Therefore

\[
e_D(U)\le
27-\max\left(
\left\lceil\frac L2\right\rceil,
L-\binom{|W|}{2},
0
\right).
\]

Combining this with simplicity and \(d_D(v)\le5\) gives

\[
e_D(U)\le\min\left\{
\binom{|U|}{2},
\left\lfloor\frac{5|U|}{2}\right\rfloor,
27,\,
27-\max\left(
\left\lceil\frac L2\right\rceil,
L-\binom{|W|}{2},
0
\right)
\right\}.
\]

The verifier enumerates all \(2^{13}\) vertex sets and confirms that every
omitted cut follows from this bound.

## Finite results

Every case has 71,757 variables.  The terminal results are:

| case | third extensions | base clauses | learned clauses | final clauses | status |
|---|---:|---:|---:|---:|---|
| `000` | 365 | 287,612 | 82,578 | 370,190 | UNSAT |
| `001` | 370 | 287,617 | 100,887 | 388,504 | UNSAT |
| `002` | 371 | 287,618 | 92,515 | 380,133 | UNSAT |
| `003` | 371 | 287,618 | 96,670 | 384,288 | UNSAT |
| `004` | 371 | 287,618 | 88,044 | 375,662 | UNSAT |
| `005` | 372 | 287,619 | 82,246 | 369,865 | UNSAT |
| `006` | 366 | 287,613 | 68,447 | 356,060 | UNSAT |
| `007` | 372 | 287,619 | 100,022 | 387,641 | UNSAT |
| `008` | 370 | 287,617 | 96,887 | 384,504 | UNSAT |
| `009` | 371 | 287,618 | 92,796 | 380,414 | UNSAT |
| `010` | 364 | 287,611 | 91,579 | 379,190 | UNSAT |
| `011` | 371 | 287,618 | 103,755 | 391,373 | UNSAT |
| `012` | 371 | 287,618 | 91,415 | 379,033 | UNSAT |
| `013` | 368 | 287,615 | 109,182 | 396,797 | UNSAT |
| `014` | 361 | 287,608 | 88,407 | 376,015 | UNSAT |
| `015` | 359 | 287,606 | 117,044 | 404,650 | UNSAT |

In total, the formulas contain \(1{,}502{,}474\) learned simultaneous-
triple clauses.

## Independent certificate audit

The semantic verifier does not import the fixed-pair CEGIS generator.  It:

1. rederives the orbit-8 signature, rows, supports, degree bounds, and all
   \(3{,}872\) positive capacity cuts;
2. independently derives the 499/3,373 encoded/automatic cut split;
3. enumerates all \(570{,}780\) labelled compatible pairs, derives the
   sixteen invariant representatives, and checks those buckets against the
   sixteen connected components of the explicit action graph;
4. reconstructs every fixed pair and every possible third extension;
5. confirms that no post-fixed-pair vertex-symmetry encoding exists;
6. compares every base clause to the deterministically reconstructed CNF;
7. reads each preserved learned record in exact CNF order; and
8. checks, for all \(1{,}502{,}474\) learned records, the three matching
   indices, pairwise edge-disjointness, exact fifteen-edge union, and
   corresponding positive deleted-edge clause.

CaDiCaL 3.0.1 generated sixteen binary DRAT traces with
`--checkproof=1`, and all sixteen internal proof checks passed.  Upstream
`drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` independently reports
`VERIFIED` for all sixteen traces.  The executable SHA-256 hashes and exact
commands are recorded in `TOOLCHAIN.json`.

The deterministic compressed package includes every frozen CNF,
learned-clause log, DRAT trace, CaDiCaL log, and `drat-trim` log.  Its
`MANIFEST.sha256` authenticates every compressed artifact and every
packaged verifier, script, metadata file, and theorem note;
`RAW_SHA256.txt` independently authenticates all eighty decompressed
artifacts.  A fresh package replay checks both manifests, gzip integrity,
the full semantic audit, the sixteen stored internal-check logs, and all
sixteen external DRAT traces.

Replay with the audited upstream checker:

```sh
DRAT_TRIM=/path/to/drat-trim \
  collaboration/opus5_r0_orbit_repair/\
2026-07-28_orbit8_fixed_pair_cnf/verify_certificates.sh
```

## Scope

This proves only the orbit-8 prescribed-colour cut-sufficiency theorem
stated above.  It closes orbit 8 under the campaign's stronger full-row,
prefix-decomposition, and pairwise-compatibility hypotheses.  It does not
prove the other unresolved local support orbits, the coordinated-nine to
seventeen lift, the six-instance global coupling, or Erdős--Rosenfeld
Problem #835.

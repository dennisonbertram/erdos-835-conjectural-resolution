# Orbit 10: certified prescribed-colour cut sufficiency

Date: 2026-07-28

## Result

Let \(V=\{0,\ldots,12\}\), let

\[
R_0=012,\qquad R_1=123,\qquad R_2=245,
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

This is the orbit-10 prescribed-colour cut-sufficiency statement used by
the campaign.  The exact eleven-row equations imply the lower degree
bounds because \(\rho(v)=d_D(v)-1\) and \(\rho(v)\ge t(v)\).  Pairwise
compatibility supplies premise 4.  The certificate does not assume that
\(D\) decomposes into six prefix matching layers, does not encode the
compatible-pair premises for the other two support pairs, and does not
encode the remaining-row realization.

The lower degree vector is

\[
(2,3,4,2,2,2,1,1,1,1,1,1,1).
\]

## Complete compatible-pair catalogue

The Venn signature in masks \(1,\ldots,7\) is

\[
(1,1,1,2,0,0,1).
\]

The three row-intersection sizes are \(2,1,1\), so the unique
maximum-intersection pair is \((0,1)\).  Each support has ten vertices and
therefore 945 perfect matchings.  Exhaustive enumeration finds exactly
\(570{,}780\) ordered edge-disjoint pairs \((P_0,P_1)\).

For every pair, the classifier decomposes \(P_0\cup P_1\) into alternating
paths and cycles.  Along each component it records the full three-row Venn
mask of every vertex and the matching colour of every edge.  It minimizes
the component words under path reversal, coloured-cycle dihedral symmetry,
within-cell vertex permutations, and the two row symmetries stabilizing
the selected unordered support pair.  This invariant has exactly
forty-seven values.

The invariant calculation was checked independently by constructing the
explicit action graph on all \(570{,}780\) labelled pairs.  Its eight
distinct generators consist of adjacent transpositions within Venn cells
and a canonical vertex realization of the nonidentity selected-pair row
symmetry.  The action graph has exactly forty-seven connected components,
each equal to one invariant bucket.  Thus the forty-seven deterministic
representatives in `2026-07-28_orbit10_fixed_pair_results.jsonl` are
exhaustive.

## Quantifier and symmetry audit

Assume for contradiction that the result fails.  Choose the compatible
pair \(P_0,P_1\) from premise 4.  A support-system automorphism maps this
pair to one of the forty-seven fixed representatives.  Apply the same
automorphism to \(D\).  It preserves \(|D|\), the degree bounds, every
capacity cut, the selected-pair availability, and the assertion that no
simultaneous prescribed triple exists.

There are **no additional solver symmetry clauses after the pair is
fixed**.  Canonicalizing \(D\) independently after fixing a labelled pair
would be unsound.  Instead, every compatible-pair action orbit receives
its own formula, and the relabelled \(D\) is admitted without further
normalization.

For each representative, the frozen formula contains:

1. the exact condition \(|D|=27\);
2. the displayed lower degree bounds and \(d_D(v)\le5\);
3. every capacity cut not already implied by the base bounds;
4. a negative unit clause for every fixed-pair edge;
5. one clause forcing \(D\) to meet every perfect matching on \(S_2\)
   edge-disjoint from the fixed pair; and
6. learned clauses
   \[
   \bigvee_{e\in M_0\cup M_1\cup M_2}[e\in D]
   \tag{T}
   \]
   for simultaneous triples of pairwise edge-disjoint support matchings.

Every clause of type (T) is necessary for a counterexample: if all fifteen
union edges were outside \(D\), the three matchings would prove the
conclusion.  The direct fixed-pair extension clauses are necessary for the
same reason.  Hence UNSAT for all forty-seven formulas rules out every
counterexample.  CEGIS is used only to discover valid clauses of type (T);
soundness does not depend on their being symmetry-closed.

## All capacity cuts

There are \(4{,}124\) positive instances of (C).  The formulas explicitly
encode the 526 that are not already implied by the base bounds:

| \(|U|\) | encoded cuts |
|---:|---:|
| 6 | 497 |
| 7 | 29 |

The other \(3{,}598\) cuts are automatic.  To check this independently,
let \(W=V\setminus U\), put

\[
L=\sum_{v\in W}(t(v)+1),
\]

and let \(q\) count deleted edges not internal to \(U\).  The lower degree
bounds outside \(U\) imply

\[
q\ge\left\lceil\frac L2\right\rceil
\quad\text{and}\quad
q\ge L-\binom{|W|}{2}.
\]

Therefore

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

Every case has 68,531 variables.  The terminal results are:

| case | third extensions | base clauses | learned clauses | final clauses | status |
|---|---:|---:|---:|---:|---|
| `000` | 406 | 274,776 | 72,883 | 347,659 | UNSAT |
| `001` | 453 | 274,823 | 118,699 | 393,522 | UNSAT |
| `002` | 412 | 274,782 | 86,874 | 361,656 | UNSAT |
| `003` | 412 | 274,782 | 80,486 | 355,268 | UNSAT |
| `004` | 453 | 274,823 | 164,216 | 439,039 | UNSAT |
| `005` | 460 | 274,830 | 114,105 | 388,935 | UNSAT |
| `006` | 460 | 274,830 | 171,045 | 445,875 | UNSAT |
| `007` | 413 | 274,783 | 75,871 | 350,654 | UNSAT |
| `008` | 462 | 274,832 | 99,037 | 373,869 | UNSAT |
| `009` | 468 | 274,838 | 186,519 | 461,357 | UNSAT |
| `010` | 462 | 274,832 | 191,469 | 466,301 | UNSAT |
| `011` | 462 | 274,832 | 129,829 | 404,661 | UNSAT |
| `012` | 414 | 274,784 | 86,571 | 361,355 | UNSAT |
| `013` | 414 | 274,784 | 95,650 | 370,434 | UNSAT |
| `014` | 462 | 274,832 | 143,240 | 418,072 | UNSAT |
| `015` | 468 | 274,838 | 172,389 | 447,227 | UNSAT |
| `016` | 463 | 274,833 | 127,131 | 401,964 | UNSAT |
| `017` | 470 | 274,840 | 143,878 | 418,718 | UNSAT |
| `018` | 470 | 274,840 | 184,582 | 459,422 | UNSAT |
| `019` | 470 | 274,840 | 149,105 | 423,945 | UNSAT |
| `020` | 463 | 274,833 | 138,548 | 413,381 | UNSAT |
| `021` | 407 | 274,777 | 75,300 | 350,077 | UNSAT |
| `022` | 462 | 274,832 | 112,744 | 387,576 | UNSAT |
| `023` | 470 | 274,840 | 157,602 | 432,442 | UNSAT |
| `024` | 471 | 274,841 | 138,969 | 413,810 | UNSAT |
| `025` | 471 | 274,841 | 127,683 | 402,524 | UNSAT |
| `026` | 453 | 274,823 | 100,794 | 375,617 | UNSAT |
| `027` | 462 | 274,832 | 164,651 | 439,483 | UNSAT |
| `028` | 412 | 274,782 | 83,282 | 358,064 | UNSAT |
| `029` | 412 | 274,782 | 86,698 | 361,480 | UNSAT |
| `030` | 453 | 274,823 | 173,506 | 448,329 | UNSAT |
| `031` | 413 | 274,783 | 103,876 | 378,659 | UNSAT |
| `032` | 462 | 274,832 | 160,717 | 435,549 | UNSAT |
| `033` | 470 | 274,840 | 174,739 | 449,579 | UNSAT |
| `034` | 471 | 274,841 | 167,414 | 442,255 | UNSAT |
| `035` | 471 | 274,841 | 150,426 | 425,267 | UNSAT |
| `036` | 460 | 274,830 | 102,609 | 377,439 | UNSAT |
| `037` | 468 | 274,838 | 148,593 | 423,431 | UNSAT |
| `038` | 458 | 274,828 | 122,713 | 397,541 | UNSAT |
| `039` | 468 | 274,838 | 171,214 | 446,052 | UNSAT |
| `040` | 458 | 274,828 | 172,320 | 447,148 | UNSAT |
| `041` | 404 | 274,774 | 64,016 | 338,790 | UNSAT |
| `042` | 453 | 274,823 | 106,211 | 381,034 | UNSAT |
| `043` | 453 | 274,823 | 94,725 | 369,548 | UNSAT |
| `044` | 444 | 274,814 | 146,278 | 421,092 | UNSAT |
| `045` | 453 | 274,823 | 135,377 | 410,200 | UNSAT |
| `046` | 453 | 274,823 | 99,382 | 374,205 | UNSAT |

In total, the formulas contain \(6{,}073{,}966\) learned simultaneous-
triple clauses.

## Independent certificate audit

The semantic verifier does not import the fixed-pair CEGIS generator.  It:

1. rederives the signature, rows, supports, degree bounds, and all
   \(4{,}124\) positive cuts;
2. independently derives the 526/3,598 encoded/automatic cut split;
3. enumerates all \(570{,}780\) labelled compatible pairs, derives the
   forty-seven invariant representatives, and checks them against the
   forty-seven connected components of the explicit action graph;
4. reconstructs every fixed pair and all possible third extensions;
5. confirms that no post-fixed-pair symmetry encoding exists;
6. compares every base clause with the reconstructed formula; and
7. checks all \(6{,}073{,}966\) learned records for their matching indices,
   pairwise edge-disjointness, exact fifteen-edge union, and corresponding
   positive deleted-edge clause in exact CNF order.

CaDiCaL 3.0.1 generated forty-seven binary DRAT traces with
`--checkproof=1`; all forty-seven internal proof checks passed.  Upstream
`drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` independently reports
`VERIFIED` for all forty-seven traces.  Executable hashes and exact
commands are recorded in `TOOLCHAIN.json`.

The deterministic compressed package contains every frozen CNF,
learned-clause log, DRAT trace, CaDiCaL log, and `drat-trim` log.
`MANIFEST.sha256` authenticates all compressed artifacts and packaged
source, metadata, scripts, and theorem note.  `RAW_SHA256.txt`
independently authenticates all decompressed artifacts.  A fresh temporary-
directory replay checks both manifests, gzip integrity, the full semantic
audit, all stored internal-check logs, and every external proof.

Replay with the audited upstream checker:

```sh
DRAT_TRIM=/path/to/drat-trim \
  collaboration/opus5_r0_orbit_repair/\
2026-07-28_orbit10_fixed_pair_cnf/verify_certificates.sh
```

## Scope

This proves only the orbit-10 prescribed-colour cut-sufficiency theorem
stated above.  It closes orbit 10 under the campaign's stronger full-row,
prefix-decomposition, and pairwise-compatibility hypotheses.  It does not
prove the other unresolved local support orbits, the coordinated-nine to
seventeen lift, the six-instance global coupling, or Erdős--Rosenfeld
Problem #835.

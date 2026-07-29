# Independent audit: conflict cohomology and the common odd transversal

Date: 2026-07-29

## Verdict

The equivalences and rank formula in `PROOF.md` are correct. They give a
lossless certificate translation for the residual bipartiteness question:

\[
G_{\cal E}\text{ bipartite}
\iff
H_{\cal E}x={\bf1}\text{ is soluble}
\iff
{\bf1}_{\cal D}\in\operatorname{row}M_{\cal D}.
\]

At the top rung this is exactly the existence of a binary point set meeting
every cell of every complemented Steiner partition oddly. This is an exact
reformulation, not a proof that the point set exists or fails to exist.
Erdős--Rosenfeld Problem #835 therefore remains open.

## Proof audit

I checked the following steps independently.

1. Every row of \(H_{\cal E}\) is the incidence vector of one residual-graph
   edge, so \(H_{\cal E}x={\bf1}\) is precisely a proper binary colouring.
   The left-kernel criterion is ordinary finite-dimensional duality.
2. The displayed contraction at a fixed point proves exactness of the full
   simplex cochain complex over \(\mathbf F_2\). No topological black box is
   being assumed.
3. For \(z\) on the \(t\)-sets, \(\delta_tz\) vanishes on the residual
   blocks exactly when \(z\in\ker H_{\cal E}^{\mathsf T}\). Extending a
   deleted-block cocycle by zero and applying simplex exactness proves
   surjectivity onto \(\ker M_{\cal D}\).
4. Summing \(\delta_tz\) counts each \(t\)-set \(n-t=p\) times. Since \(p\)
   is odd, the map preserves weight parity. This is the load-bearing fact
   converting odd residual cycles into odd deleted cocycles.
5. Dimension counting in the resulting short exact sequence gives
   \[
   \operatorname{rank}_2 M_{\cal D}
   =\binom{n-1}{t+1}-c(G_{\cal E}).
   \]
   I rederived the formula from
   \(\operatorname{rank}\delta_s=\binom{n-1}{s}\) and the binary graph
   incidence rank \(|{\cal E}|-c(G_{\cal E})\).
6. The complement-closure lemma at the top rung follows from the stated
   intersection equations and binomial inversion. The alternating
   coefficient calculation is
   \([x^k]x^k(1+x)^k=1\), and even \(k\) gives exactly one disjoint block,
   necessarily the complement.
7. Complementing a row \(F\in\binom X{k+1}\) and a deleted block
   \(B\in\binom Xk\) changes \(B\subset F\) into
   \(X\setminus F\subset X\setminus B\). Thus the matrix really is the
   point-versus-cell incidence matrix of the \(k-1\) Steiner partitions.
   Its row-space equation is exactly the common odd-transversal system.
8. I independently checked the unitrade-gap count added as Theorem 7.1.
   Two blocks meeting in at most \(k-3\) require disjoint sets of facet
   partners. If they meet in \(k-2\), the four possible common partners form
   a \(2\)-by-\(2\) grid; counting its selected entries plus the rows and
   columns needing separate parity partners gives the sharp \(2k\) lower
   bound outside the \(k+1\)-facet simplex. Lemma 6.1 excludes that simplex
   from the deleted support, so an odd obstruction has at least \(2k+1\)
   blocks.
9. Potapov's equality classification at weight \(2k\) gives the symmetric
   difference of two complete facet families. Such a word contains \(k\)
   facets of one \((k+1)\)-set, while Lemma 6.1 permits only \(k-1\) deleted
   facets there. Corollary 7.2 therefore correctly strengthens the minimum
   weight of every nonzero deleted-support kernel vector to \(2k+1\).

The warning separating upward cochain coboundaries from downward chain
boundaries is necessary and correct. In particular, the facets of one
\((t+2)\)-set are parity checks, not automatic kernel witnesses.

## Independent executable checks

I ran:

```sh
/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3 -B \
  collaboration/independent/conflict_cohomology_2026-07-29/\
verify_cochain_controls.py

ruff check \
  collaboration/independent/conflict_cohomology_2026-07-29/\
verify_cochain_controls.py
```

The verifier printed `RESULT: PASS (22 exact checks)`, and Ruff printed
`All checks passed!`.

The positive control independently enumerates all 840 labelled
\(STS(9)\)'s, constructs an \(LS(2,3,9)\), checks its connected bipartite
residual graph, and exhibits a 48-row witness for the deleted all-one
vector. The negative control authenticates the fixed Etzion--Hartman partial,
checks all fifteen complete \(S(3,4,20)\)'s, and constructs the odd
45-block cocycle from its residual triangle.

## Exact remaining lemma

For even \(k\), suppose \(k-1\) pairwise disjoint
\(S(k-1,k,2k)\)'s are given. After complementing their blocks, must their
\(k-1\) partitions of \(\binom X{k-1}\) have a common binary point set
meeting every cell oddly?

A positive answer would extend every such partial family by the final two
systems. A negative answer for one partial family is not enough for a
negative solution of #835, and this formulation does not prove that the
initial \(k-1\) systems exist. This is the precise boundary of the result.

For \(k=16\), the strengthened support bound means that a negative
row-space certificate must contain at least 33 complemented deleted blocks;
indeed every nonzero vector in that restricted kernel has at least 33.
It remains an existence lower bound, not an obstruction theorem.

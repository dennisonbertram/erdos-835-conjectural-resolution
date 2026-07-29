# Orbit 7: certified prescribed-colour cut sufficiency

Date: 2026-07-28

## Result

Let \(V=\{0,\ldots,12\}\), let

\[
R_0=012,\qquad R_1=013,\qquad R_2=245,
\]

and put \(S_i=V\setminus R_i\). Let
\(D\subseteq E(K_{13})\), put \(G=K_{13}-D\), and define

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
4. there are edge-disjoint perfect matchings \(P_0\) on \(S_0\) and
   \(P_1\) on \(S_1\).

Then \(G\) contains pairwise edge-disjoint perfect matchings \(M_i\) on
\(S_i\), for \(i=0,1,2\).

This is stronger than the orbit-7 instance used by the larger campaign.
The certificate does not assume that \(D\) decomposes into the six prefix
matching layers, does not encode the other two pairwise-compatibility
premises, and does not encode the remaining-row realization. The exact
eleven-row equations imply premise 2 in the campaign because
\(\rho(v)=d_D(v)-1\) and \(\rho(v)\ge t(v)\).

The degree lower vector here is

\[
(3,3,3,2,2,2,1,1,1,1,1,1,1).
\]

## Complete compatible-pair catalogue

Each support has \(945\) perfect matchings. Exact enumeration gives
\(570{,}780\) labelled edge-disjoint ordered pairs
\((P_0,P_1)\).

For every pair, the classifier decomposes \(P_0\cup P_1\) into alternating
paths and cycles and records, in order, the full three-row Venn-cell mask
of every vertex and the matching colour of every edge. It minimizes these
component words under path reversal, coloured-cycle dihedral symmetry,
within-cell vertex permutations, and every row-system symmetry stabilizing
the selected pair. For this row system the row-symmetry group in question
is trivial.

This primary invariant gives exactly \(76\) buckets. An independent action
audit constructs the graph on all \(570{,}780\) labelled pairs generated
by the seven within-cell transpositions and obtains exactly \(76\)
connected components, with each component equal to one invariant bucket.
Thus the catalogue is complete, not merely a list of observed shapes.

The representatives, invariants, and matching edges are stored in
`2026-07-28_orbit7_fixed_pair_results.jsonl`. Cases 048 and 049 are
distinct coloured-pair orbits but have the same ten-edge union, so the
uncoloured fixed-edge CNF and learned log coincide. Both indexed cases are
retained and certified.

## Sound quantifiers

Assume for contradiction that the theorem fails. Choose the compatible
pair \(P_0,P_1\) supplied by premise 4. Catalogue completeness gives a
vertex relabeling \(g\) preserving all three rows and taking this pair to
one of the \(76\) fixed representatives. Apply the same \(g\) to \(D\).
The cardinality and degree bounds, every cut (C), and the absence of a
simultaneous prescribed-colour triple are invariant under this relabeling.

No solver-level vertex-symmetry clauses remain after the pair is fixed.
This avoids the invalid quantifier swap that would arise from
canonicalizing \(D\) independently of the chosen pair. Instead, every
compatible-pair orbit has its own formula, and the transported \(D\) is
accepted without further canonicalization.

For a fixed representative, the frozen formula contains:

1. \(|D|=27\);
2. \(t(v)+1\le d_D(v)\le5\);
3. every nonautomatic capacity cut;
4. a negative unit clause for every edge of \(P_0\cup P_1\), making the
   fixed pair available;
5. for every perfect matching \(N\) on \(S_2\) edge-disjoint from the
   fixed pair, a clause requiring \(D\cap N\ne\varnothing\); and
6. learned clauses
   \[
   \bigvee_{e\in M_0\cup M_1\cup M_2}[e\in D]
   \tag{T}
   \]
   for simultaneous triples of pairwise edge-disjoint perfect matchings.

Every clause in items 5 and 6 is necessary for a counterexample. If it
failed, its displayed available matchings would already be the theorem's
conclusion. Therefore every counterexample transported to a representative
would satisfy that representative's final CNF. Proving all \(76\) final
CNFs UNSAT rules out the counterexample.

The CEGIS loop is only a way to discover valid clauses of type (T).
Soundness does not require the discovered clause set to be
symmetry-closed.

## Capacity cuts

There are \(4{,}215\) positive instances of (C). Exactly \(540\) are not
already implied by the base bounds and are explicitly encoded:

| \(|U|\) | encoded cuts |
|---:|---:|
| 6 | 518 |
| 7 | 22 |

The remaining \(3{,}675\) are automatic. For an independent check, put
\(W=V\setminus U\) and

\[
L=\sum_{v\in W}(t(v)+1).
\]

If \(q\) is the number of deleted edges not internal to \(U\), the degree
lower bounds outside \(U\) give

\[
q\ge\left\lceil\frac L2\right\rceil
\quad\text{and}\quad
q\ge L-\binom{|W|}{2}.
\]

Consequently

\[
e_D(U)\le
\min\left\{
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

The independent verifier enumerates all \(2^{13}\) sets \(U\) and confirms
that this bound implies every omitted cut.

## Finite formulas

Every case has \(69{,}525\) variables. Across the \(76\) indexed cases:

- the base clause counts range from \(278{,}764\) to \(278{,}888\), with
  \(21{,}192{,}342\) base clauses in total;
- the fixed pair has from \(404\) to \(528\) possible third extensions;
- the learned clause counts range from \(60{,}209\) to \(209{,}771\), with
  \(9{,}386{,}110\) learned clauses in total; and
- the final clause counts range from \(339{,}013\) to \(488{,}657\), with
  \(30{,}578{,}452\) clauses in total.

All \(76\) terminal formulas are UNSAT.

## Independent certificate audit

The semantic verifier does not import the fixed-pair fallback driver. It:

1. rederives the rows, supports, degree vector, and all capacity cuts;
2. independently enumerates all \(570{,}780\) compatible labelled pairs;
3. checks the \(76\) invariant classes against the explicit action graph;
4. reconstructs every fixed pair and all possible third extensions;
5. verifies that no post-fix vertex-symmetry clauses occur;
6. compares every static CNF clause with an independent reconstruction;
7. checks the frozen CNF and learned-log hashes; and
8. checks all \(9{,}386{,}110\) learned records: three matching indices,
   pairwise edge-disjointness, exact sorted fifteen-edge union, and the
   corresponding positive deleted-edge clause in the CNF.

CaDiCaL 3.0.1 generated \(76\) binary DRAT traces with
`--checkproof=1`; all \(76\) internal proof checks passed. Upstream
`drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` independently reports
`VERIFIED` for all \(76\) traces.

The deterministic package
`2026-07-28_orbit7_fixed_pair_cnf/` contains \(399\) files and is
\(570{,}514{,}010\) bytes. It includes \(380\) `gzip -9 -n` artifacts:
the CNF, learned log, DRAT trace, CaDiCaL log, and `drat-trim` log for
every case. It also contains the self-contained verifier dependencies,
worker logs, deterministic merge script, exact generation/packaging/replay
scripts, toolchain hashes, and two hash manifests.

The package manifest has \(398\) entries and SHA-256

```text
d1266fe1dd2c73bd5444b3fe0e85b7b819ba338a04e92b93240d6455400bd816
```

The raw manifest has \(380\) entries and SHA-256

```text
2afefebda4d0b966f40234986dcdd88898c16bd8ea6caa9e0e31e2bf54b9590d
```

A full replay from a fresh temporary directory passed:

- all \(398\) package-manifest hashes;
- all \(380\) gzip integrity checks;
- all \(380\) decompressed raw hashes;
- deterministic regeneration of the merged \(76\)-case result;
- the complete classifier, cut, static-CNF, and learned-clause semantic
  audits; and
- all \(76\) fresh external `drat-trim` replays.

Run the same replay with:

```sh
DRAT_TRIM=/path/to/upstream/drat-trim \
  collaboration/opus5_r0_orbit_repair/\
2026-07-28_orbit7_fixed_pair_cnf/verify_certificates.sh
```

## Scope

This proves the orbit-7 prescribed-colour cut-sufficiency theorem stated
above. Under the larger campaign's degree, cut, and pairwise-compatibility
hypotheses, it closes that local support orbit.

It does not prove any other unresolved support orbit, the global
coordinated-nine theorem, the seventeen-matching first lift, the
six-instance shared-colour coupling, the fan-realizability step, or
Erdős--Rosenfeld Problem #835.

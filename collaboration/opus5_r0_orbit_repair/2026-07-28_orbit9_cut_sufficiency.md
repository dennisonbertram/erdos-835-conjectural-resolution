# Orbit 9: certified prescribed-colour cut sufficiency

Date: 2026-07-28

## Result

Let \(V=\{0,\ldots,12\}\), let

\[
R_0=012,\qquad R_1=135,\qquad R_2=245,
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
4. there are edge-disjoint perfect matchings \(P_0\) on \(S_0\) and
   \(P_1\) on \(S_1\).

Then \(G\) contains pairwise edge-disjoint perfect matchings \(M_i\) on
\(S_i\), for \(i=0,1,2\).

This is stronger than the orbit-9 instance needed by the campaign.  The
exact eleven-row equations imply the lower degree bounds because
\(\rho(v)=d_D(v)-1\) and \(\rho(v)\ge t(v)\).  Pairwise compatibility
supplies the pair in premise 4.  The certificate does not assume that
\(D\) decomposes into the six prefix matching layers, does not encode the
other two compatible-pair premises, and does not encode the remaining-row
realization.

The lower degree vector used in the formulas is

\[
(2,3,3,2,2,3,1,1,1,1,1,1,1).
\]

## Complete compatible-pair quotient

Each selected support has 945 perfect matchings.  Exact enumeration gives
627,900 ordered edge-disjoint pairs on \(S_0,S_1\).

The primary quotient records, along every alternating path and cycle of a
pair, each vertex's full three-row Venn mask and each edge's matching
colour.  It minimizes over path reversal, coloured-cycle dihedral
presentations, the selected-support row stabilizer, and the induced
matching-colour swap.  Sorting these invariants gives exactly 87 classes
and fixes the deterministic case order `orbit9_pair_000` through
`orbit9_pair_086`.

Exhaustiveness is also checked by an explicit action calculation.  The
within-cell adjacent transpositions generate the symmetric group of every
Venn cell.  Together with the nonidentity row-stabilizer action they give
seven distinct generators on the 627,900 labelled compatible pairs.
The verifier constructs the entire generated action graph.  It has
exactly 87 connected components, and every component agrees exactly with
one primary-invariant bucket.  Hence the 87 formulas cover the full
compatible-pair space; the catalogue is not sampled solver output.

## Sound relaxation and quantifiers

Assume for contradiction that the theorem fails and choose the pair
\(P_0,P_1\) supplied by premise 4.  A support-stabilizing relabeling maps
this labelled pair to one of the 87 fixed representatives.  Apply the same
relabeling to \(D\).  It preserves the degree constraints, all cuts, and
the nonexistence of a prescribed simultaneous triple.

After fixing a representative, the formula applies no further vertex
symmetry to \(D\).  Independently canonicalizing \(D\) after fixing a pair
would be unsound; exhaustive enumeration of pair orbits is what makes this
reduction valid.

For each fixed pair, the frozen CNF contains:

1. \(|D|=27\);
2. the displayed lower degree bounds and \(d_D(v)\le5\);
3. every nonautomatic capacity cut;
4. a negative unit clause for every edge of the fixed pair, so those
   edges remain in \(G\);
5. one clause requiring \(D\) to meet every perfect matching on \(S_2\)
   that is edge-disjoint from the fixed pair; and
6. learned clauses
   \[
   \bigvee_{e\in M_0\cup M_1\cup M_2}[e\in D]
   \tag{T}
   \]
   for pairwise edge-disjoint prescribed triples.

Every clause of type (T) is necessary for a counterexample: if all
15 edges were outside \(D\), those three matchings would prove the
conclusion.  The fixed-pair extension blockers are necessary for the same
reason.  Thus UNSAT for all 87 formulas rules out the assumed
counterexample.  CEGIS is used only to discover valid clauses of type
(T); soundness does not require that its learned set be complete or
symmetry-closed.

## All capacity cuts

There are 4,250 positive instances of (C).  The formulas encode the 575
not already implied by the base bounds:

| \(|U|\) | encoded cuts |
|---:|---:|
| 6 | 553 |
| 7 | 22 |

The other 3,675 cuts are automatic.  For the independent check, put
\(W=V\setminus U\) and

\[
L=\sum_{v\in W}(t(v)+1).
\]

If \(q\) is the number of deleted edges not internal to \(U\), the degree
lower bounds outside \(U\) give

\[
q\ge\left\lceil\frac L2\right\rceil
\quad\hbox{and}\quad
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

The verifier enumerates all \(2^{13}\) subsets and checks that this bound
implies every omitted capacity cut.

## Finite results and independent semantic audit

All 87 formulas are solver-UNSAT.  Every case has 73,760 variables.
Across the campaign there are 13,734,283 learned simultaneous-triple
clauses, discovered in 3,423 CEGIS rounds.  The per-case terminal record,
fixed representative, extension count, base and learned clause counts,
round count, elapsed time, and raw hashes are preserved in
`2026-07-28_orbit9_fixed_pair_results.jsonl`.

The independent verifier does not import the fixed-pair CEGIS driver.  It:

1. reconstructs the signature, rows, supports, degree bounds, and all
   4,250 positive cuts;
2. independently derives the 575/3,675 encoded/automatic split;
3. enumerates every one of the 627,900 labelled compatible pairs and
   checks the 87 invariant buckets against all 87 components of the full
   seven-generator action graph;
4. reconstructs every fixed pair and every possible third extension;
5. checks that no post-fixed-pair vertex-symmetry clauses occur;
6. compares every static clause, in order, with an independently rebuilt
   formula; and
7. checks all 13,734,283 learned records for matching indices, pairwise
   edge-disjointness, the exact 15-edge union, within-case uniqueness,
   and the corresponding CNF clause.

CaDiCaL 3.0.1, binary SHA-256
`52daad7dcbb97d3d68a7494fb415ba54a509c49d30f5dfcd157e1bcbe138e6ee`,
generated 87 binary DRAT traces using
`cadical --checkproof=1 CASE.cnf CASE.drat`.  Every internal proof check
passed.

Upstream `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA-256
`42a69f9a17bcd58001676abf02d58992bd0ede58410a467dda07a350fec498c9`,
independently reported `VERIFIED` for all 87 traces.  The source and
Makefile used to build the checker were checked byte-for-byte against that
upstream commit.

The deterministic package contains, for every case, the frozen CNF,
learned record, DRAT trace, CaDiCaL log, and `drat-trim` log.  Its raw and
compressed manifests authenticate every artifact and all self-contained
support files.  `verify_certificates.sh` checks both manifests, all gzip
streams, deterministic worker-result merging, the complete semantic
audit, stored proof-log conditions, and fresh upstream `drat-trim` replay
of all 87 traces.

Replay with the specified checker:

```sh
DRAT_TRIM=/path/to/drat-trim \
  collaboration/opus5_r0_orbit_repair/\
2026-07-28_orbit9_fixed_pair_cnf/verify_certificates.sh
```

## Scope

This proves the orbit-9 prescribed-colour cut-sufficiency theorem stated
above.  It does not by itself prove the analogous statement for any other
support orbit, the global coordinated-nine theorem, the later selection
and fan-realizability steps, or Erdős--Rosenfeld Problem #835.

# Orbit 6: certified prescribed-colour cut sufficiency

Date: 2026-07-28

## Result

Let \(V=\{0,\ldots,12\}\), let the three omitted rows be

\[
R_0=012,\qquad R_1=023,\qquad R_2=124,
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

This theorem is stronger than the orbit-6 instance needed by the campaign.
The exact eleven-row equations imply the lower degree bounds because
\(\rho(v)=d_D(v)-1\) and \(\rho(v)\ge t(v)\).  Pairwise compatibility
supplies the pair in premise 4.  The certificate does not assume that
\(D\) decomposes into the six prefix matching layers, does not encode the
other two compatible-pair premises, and does not encode the remaining-row
realization.

The relevant lower degree vector is

\[
(3,3,4,2,2,1,1,1,1,1,1,1,1).
\]

## Complete twenty-three-case compatible-pair catalogue

The selected supports are \(S_0=V\setminus\{0,1,2\}\) and
\(S_1=V\setminus\{0,2,3\}\).  Independently enumerating every ordered pair
of edge-disjoint perfect matchings on these supports gives \(570{,}780\)
labelled pairs.  Canonicalization under the full support stabilizer gives
the following twenty-three representatives.  An entry \(a\!-\!b\) denotes
the edge \(\{a,b\}\).

| case | \(P_0\) | \(P_1\) |
|---|---|---|
| `000` | `3-5 4-6 7-8 9-10 11-12` | `1-4 5-7 6-9 8-11 10-12` |
| `001` | `3-5 4-6 7-8 9-10 11-12` | `1-6 4-7 5-9 8-11 10-12` |
| `002` | `3-5 4-6 7-8 9-10 11-12` | `1-7 4-8 5-9 6-11 10-12` |
| `003` | `3-5 4-6 7-8 9-10 11-12` | `1-7 4-9 5-11 6-8 10-12` |
| `004` | `3-5 4-6 7-8 9-10 11-12` | `1-7 4-9 5-11 6-10 8-12` |
| `005` | `3-5 4-6 7-8 9-10 11-12` | `1-7 4-9 5-11 6-12 8-10` |
| `006` | `3-5 4-6 7-8 9-10 11-12` | `1-4 5-7 6-8 9-11 10-12` |
| `007` | `3-5 4-6 7-8 9-10 11-12` | `1-7 4-9 5-10 6-11 8-12` |
| `008` | `3-5 4-6 7-8 9-10 11-12` | `1-6 4-7 5-8 9-11 10-12` |
| `009` | `3-5 4-6 7-8 9-10 11-12` | `1-7 4-9 5-8 6-11 10-12` |
| `010` | `3-5 4-6 7-8 9-10 11-12` | `1-7 4-9 5-6 8-11 10-12` |
| `011` | `3-5 4-6 7-8 9-10 11-12` | `1-7 4-8 5-6 9-11 10-12` |
| `012` | `3-5 4-6 7-8 9-10 11-12` | `1-4 5-6 7-9 8-11 10-12` |
| `013` | `3-5 4-6 7-8 9-10 11-12` | `1-7 4-5 6-9 8-11 10-12` |
| `014` | `3-5 4-6 7-8 9-10 11-12` | `1-7 4-5 6-8 9-11 10-12` |
| `015` | `3-5 4-6 7-8 9-10 11-12` | `1-6 4-5 7-9 8-11 10-12` |
| `016` | `3-5 4-6 7-8 9-10 11-12` | `1-5 4-7 6-8 9-11 10-12` |
| `017` | `3-5 4-6 7-8 9-10 11-12` | `1-5 4-7 6-9 8-11 10-12` |
| `018` | `3-4 5-6 7-8 9-10 11-12` | `1-5 4-7 6-9 8-11 10-12` |
| `019` | `3-4 5-6 7-8 9-10 11-12` | `1-5 4-7 6-8 9-11 10-12` |
| `020` | `3-4 5-6 7-8 9-10 11-12` | `1-5 4-6 7-9 8-11 10-12` |
| `021` | `3-4 5-6 7-8 9-10 11-12` | `1-4 5-7 6-8 9-11 10-12` |
| `022` | `3-4 5-6 7-8 9-10 11-12` | `1-4 5-7 6-9 8-11 10-12` |

The generic invariant records the Venn-cell mask and matching colour along
each alternating path or cycle, minimizes over its presentations and the
selected-support stabilizer, and produces exactly these twenty-three
classes.  As a separate exhaustiveness check, the classifier constructs
the full labelled-pair graph under seven explicit stabilizer generators.
Its connected components also number twenty-three and agree exactly with
the invariant classes.  Thus the catalogue is not merely a list of
observed SAT cases.

## Sound relaxation and quantifiers

Assume for contradiction that the theorem fails.  Choose the compatible
pair \(P_0,P_1\) supplied by premise 4.  A support-stabilizing vertex
relabeling maps this labelled pair to one of the twenty-three fixed
representatives above.  Apply the same relabeling to \(D\).  It preserves
the degree bounds, all cuts, and the assertion that no prescribed
simultaneous triple exists.

No solver-level vertex-symmetry clauses are retained after a pair is fixed.
This is important: independently canonicalizing \(D\) after fixing a
labelled pair would not be sound.  Instead, every possible pair orbit gets
its own formula, and the relabelled \(D\) is accepted without further
canonicalization.

For each fixed representative, the frozen formula contains:

1. \(|D|=27\);
2. the displayed lower degree bounds and \(d_D(v)\le5\);
3. every nonautomatic capacity cut;
4. a negative unit clause for every fixed-pair edge, making that edge
   available in \(G\);
5. one clause requiring \(D\) to meet every perfect matching on \(S_2\)
   that is edge-disjoint from the fixed pair; and
6. learned clauses
   \[
   \bigvee_{e\in M_0\cup M_1\cup M_2} [e\in D]
   \tag{T}
   \]
   for prescribed simultaneous triples.

Every clause of type (T) is a necessary condition for a counterexample:
if all fifteen edges were outside \(D\), the three matchings would be the
required conclusion.  Likewise, under the assumed absence of every
simultaneous triple, the direct fixed-pair extension clauses are necessary.
Therefore an UNSAT result for all twenty-three formulas rules out the
original counterexample.

The CEGIS process uses a SAT model only to discover additional valid
clauses of type (T).  Its correctness does not depend on the discovered
set being complete or symmetry-closed.

## All capacity cuts

There are \(3{,}984\) positive instances of (C).  The formulas explicitly
encode the 527 that are not already implied by the base bounds:

| \(|U|\) | encoded cuts |
|---:|---:|
| 6 | 462 |
| 7 | 64 |
| 8 | 1 |

The other \(3{,}457\) cuts are automatic.  To verify this without trusting
the generator, let \(W=V\setminus U\), put

\[
L=\sum_{v\in W}(t(v)+1),
\]

and let \(q\) be the number of deleted edges not internal to \(U\).  The
degree lower bounds outside \(U\) give both

\[
q\ge\left\lceil\frac L2\right\rceil
\quad\text{and}\quad
q\ge L-\binom{|W|}{2}.
\]

Consequently

\[
e_D(U)\le
27-\max\left(
\left\lceil\frac L2\right\rceil,
L-\binom{|W|}{2},
0
\right).
\]

Together with simplicity and \(d_D(v)\le5\), this gives the independently
audited automatic upper bound

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
omitted cut is implied by this bound.

## Finite results

Every case has 72,345 variables.  The terminal results are:

| case | third extensions | base clauses | learned clauses | final clauses | rounds | status |
|---|---:|---:|---:|---:|---:|---|
| `000` | 365 | 289,992 | 46,400 | 336,392 | 51 | UNSAT |
| `001` | 406 | 290,033 | 139,421 | 429,454 | 104 | UNSAT |
| `002` | 412 | 290,039 | 140,175 | 430,214 | 119 | UNSAT |
| `003` | 413 | 290,040 | 132,876 | 422,916 | 99 | UNSAT |
| `004` | 413 | 290,040 | 147,183 | 437,223 | 111 | UNSAT |
| `005` | 414 | 290,041 | 133,988 | 424,029 | 97 | UNSAT |
| `006` | 366 | 289,993 | 59,006 | 348,999 | 49 | UNSAT |
| `007` | 414 | 290,041 | 120,577 | 410,618 | 151 | UNSAT |
| `008` | 407 | 290,034 | 128,725 | 418,759 | 99 | UNSAT |
| `009` | 414 | 290,041 | 137,018 | 427,059 | 114 | UNSAT |
| `010` | 413 | 290,040 | 115,122 | 405,162 | 104 | UNSAT |
| `011` | 412 | 290,039 | 139,632 | 429,671 | 128 | UNSAT |
| `012` | 364 | 289,991 | 51,002 | 340,993 | 53 | UNSAT |
| `013` | 412 | 290,039 | 143,313 | 433,352 | 135 | UNSAT |
| `014` | 412 | 290,039 | 143,539 | 433,578 | 131 | UNSAT |
| `015` | 404 | 290,031 | 144,615 | 434,646 | 76 | UNSAT |
| `016` | 412 | 290,039 | 143,711 | 433,750 | 109 | UNSAT |
| `017` | 412 | 290,039 | 131,824 | 421,863 | 130 | UNSAT |
| `018` | 406 | 290,033 | 102,376 | 392,409 | 70 | UNSAT |
| `019` | 407 | 290,034 | 101,011 | 391,045 | 62 | UNSAT |
| `020` | 404 | 290,031 | 98,848 | 388,879 | 81 | UNSAT |
| `021` | 361 | 289,988 | 51,089 | 341,077 | 25 | UNSAT |
| `022` | 359 | 289,986 | 53,536 | 343,522 | 24 | UNSAT |

In total, the formulas contain \(2{,}604{,}987\) learned
simultaneous-triple clauses, discovered in 2,122 CEGIS rounds.

## Independent certificate audit

The orbit-6 semantic verifier does not import the orbit-fallback generator.
It:

1. reconstructs the orbit-6 signature, rows, supports, degree lower bounds,
   and all \(3{,}984\) positive cuts;
2. independently rederives the 527/3,457 encoded/automatic cut split;
3. enumerates all \(570{,}780\) labelled compatible pairs and independently
   checks the twenty-three invariant classes against the connected
   components of the seven-generator action graph;
4. reconstructs each fixed pair and every possible third extension;
5. checks that no vertex-symmetry encoding is present;
6. compares every base clause, in order, with the independently
   reconstructed formula;
7. reads the preserved learned-clause records in exact CNF order; and
8. for every one of the \(2{,}604{,}987\) learned records, checks the three
   matching indices, pairwise edge-disjointness, the exact fifteen-edge
   union, uniqueness within its case, and the corresponding positive
   deleted-edge clause.

CaDiCaL 3.0.1, binary SHA-256
`52daad7dcbb97d3d68a7494fb415ba54a509c49d30f5dfcd157e1bcbe138e6ee`,
generated twenty-three binary DRAT traces with
`cadical --checkproof=1 CASE.cnf CASE.drat`.  Every internal proof check
passed.

Upstream `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, binary SHA-256
`42a69f9a17bcd58001676abf02d58992bd0ede58410a467dda07a350fec498c9`,
independently reported `VERIFIED` for all twenty-three raw traces.  The
source and Makefile used to build it were also checked byte-for-byte
against that upstream commit.

The deterministic compressed package contains 169,250,435 bytes
(169 MB decimal, 161.4 MiB).  For every case it contains the frozen CNF,
learned-clause log, DRAT trace, CaDiCaL log, and `drat-trim` log: 115
compressed artifacts in total.  `RAW_SHA256.txt` authenticates all 115
decompressed contents, while `MANIFEST.sha256` authenticates those
compressed files plus thirteen self-contained support files (128 entries
total).

The packaged replay was run twice, including once by a separate central
process.  Both runs passed all manifest hashes, gzip checks, all raw hashes,
the complete semantic audit, the stored-log assertions, and fresh upstream
`drat-trim` replay of all twenty-three proofs.

Replay with an upstream `drat-trim` executable:

```sh
DRAT_TRIM=/path/to/drat-trim \
  collaboration/opus5_r0_orbit_repair/\
2026-07-28_orbit6_fixed_pair_cnf/verify_certificates.sh
```

The independent verifier, terminal search log, certificate metadata, and
certificate package are:

- `2026-07-28_orbit6_fixed_pair_verify.py`;
- `2026-07-28_orbit6_fixed_pair_results.jsonl`;
- `2026-07-28_orbit6_fixed_pair_classifier_audit.json`;
- `2026-07-28_orbit6_fixed_pair_raw_audit.json`;
- `2026-07-28_orbit6_certificate_results.json`;
- `2026-07-28_orbit6_toolchain.json`; and
- `2026-07-28_orbit6_fixed_pair_cnf/`.

The proof-generation, raw-replay, package-generation, and packaged-replay
scripts preserve the complete reconstruction path.

## Scope

This proves the orbit-6 prescribed-colour cut-sufficiency theorem stated
above and closes orbit 6 under the campaign's stronger full-row,
prefix-decomposition, and pairwise-compatibility hypotheses.

Together with the certified results for orbits 0 through 5, seven of the
sixteen selected-support Venn types are now closed.  The nine types
numbered 7 through 15 remain open.  This does not prove the global
coordinated-nine theorem, the later selection and fan-realizability steps,
or Erdős--Rosenfeld Problem #835.

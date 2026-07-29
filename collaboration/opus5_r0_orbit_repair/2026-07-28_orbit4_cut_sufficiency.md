# Orbit 4: certified prescribed-colour cut sufficiency

Date: 2026-07-28

## Result

Let \(V=\{0,\ldots,12\}\), let the three omitted rows be

\[
R_0=012,\qquad R_1=012,\qquad R_2=234,
\]

and put \(S_i=V\setminus R_i\).  Thus \(S_0=S_1\).  Let
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
4. \(G[S_0]\) contains two edge-disjoint perfect matchings.

Then \(G\) contains pairwise edge-disjoint perfect matchings \(M_i\) on
\(S_i\), for \(i=0,1,2\).

This theorem is stronger than the orbit-4 instance needed by the campaign.
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

## Complete eleven-case compatible-pair catalogue

Fix edge-disjoint perfect matchings \(P_0,P_1\) on the common ten-vertex
support \(S_0=S_1\).  Their union is a two-regular graph whose components
are alternating even cycles of length at least four.  Hence its uncoloured
shape is either

\[
C_{10}\qquad\text{or}\qquad C_4\mathbin{\dot\cup}C_6.
\]

Vertices \(3,4\) form the distinguished Venn cell \(R_2\setminus R_0\);
the other eight support vertices \(5,\ldots,12\) are interchangeable.
The stabilizer may also interchange rows 0 and 1, simultaneously swapping
the two matching colours.

For \(C_{10}\), the cyclic distance between the two distinguished vertices
is one of \(1,\ldots,5\), giving five types.  For
\(C_4\mathbin{\dot\cup}C_6\), the distinguished vertices are:

- both on \(C_4\), at distance one or two;
- both on \(C_6\), at distance one, two, or three; or
- one on each component.

This gives another \(2+3+1=6\) types, hence eleven in total.

The generic classifier independently checks this elementary description.
It records the full Venn mask and matching colour along each alternating
component, minimizes under path/cycle presentation and the selected-pair
support stabilizer, and then compares all invariant buckets with the
connected components of the explicit generator action graph.  For orbit 4,
all \(514{,}080\) labelled edge-disjoint matching pairs fall into exactly
these eleven orbits.

The certificate case order is:

| case | pair-union type |
|---|---|
| `orbit4_pair_00` | \(C_4+C_6\), both marked vertices on \(C_6\), distance 1 |
| `orbit4_pair_01` | \(C_4+C_6\), both on \(C_6\), distance 2 |
| `orbit4_pair_02` | \(C_4+C_6\), both on \(C_6\), distance 3 |
| `orbit4_pair_03` | \(C_4+C_6\), both on \(C_4\), distance 1 |
| `orbit4_pair_04` | \(C_4+C_6\), both on \(C_4\), distance 2 |
| `orbit4_pair_05` | \(C_{10}\), distance 1 |
| `orbit4_pair_06` | \(C_{10}\), distance 2 |
| `orbit4_pair_07` | \(C_{10}\), distance 3 |
| `orbit4_pair_08` | \(C_4+C_6\), one marked vertex on each component |
| `orbit4_pair_09` | \(C_{10}\), distance 4 |
| `orbit4_pair_10` | \(C_{10}\), distance 5 |

## Sound relaxation and quantifiers

Assume for contradiction that the theorem fails.  Choose the compatible
pair \(P_0,P_1\) supplied by premise 4.  A support-stabilizing vertex
relabeling maps this labelled pair to one of the eleven fixed
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
   available;
5. one clause requiring \(D\) to meet every third matching on \(S_2\)
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
Therefore an UNSAT result for every one of the eleven formulas rules out
the original counterexample.

The CEGIS process uses a SAT model only to discover additional valid
clauses of type (T).  Its correctness does not depend on the discovered
set being symmetry-closed.

## All capacity cuts

There are \(3{,}844\) positive instances of (C).  The formulas explicitly
encode the 457 that are not already implied by the base bounds:

| \(|U|\) | encoded cuts |
|---:|---:|
| 6 | 392 |
| 7 | 64 |
| 8 | 1 |

The other \(3{,}387\) cuts are automatic.  To verify this without trusting
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

Every case has 63,875 variables.  The terminal results are:

| case | fixed-pair third extensions | base clauses | learned triple clauses | final clauses | status |
|---|---:|---:|---:|---:|---|
| `00` | 407 | 256,084 | 134,694 | 390,778 | UNSAT |
| `01` | 453 | 256,130 | 130,764 | 386,894 | UNSAT |
| `02` | 458 | 256,135 | 170,476 | 426,611 | UNSAT |
| `03` | 404 | 256,081 | 45,159 | 301,240 | UNSAT |
| `04` | 444 | 256,121 | 154,297 | 410,418 | UNSAT |
| `05` | 406 | 256,083 | 55,536 | 311,619 | UNSAT |
| `06` | 453 | 256,130 | 89,208 | 345,338 | UNSAT |
| `07` | 460 | 256,137 | 132,580 | 388,717 | UNSAT |
| `08` | 462 | 256,139 | 128,016 | 384,155 | UNSAT |
| `09` | 462 | 256,139 | 123,469 | 379,608 | UNSAT |
| `10` | 463 | 256,140 | 232,787 | 488,927 | UNSAT |

In total, the formulas contain \(1{,}396{,}986\) learned simultaneous-triple
clauses.

## Independent certificate audit

The semantic verifier:

1. reconstructs the orbit-4 rows, supports, degree lower bounds, and all
   3,844 positive cuts;
2. rederives the 457/3,387 encoded/automatic cut split;
3. reconstructs every fixed pair and all of its possible third extensions;
4. checks that no vertex-symmetry encoding is present;
5. compares every base clause with the deterministically reconstructed
   formula;
6. reads the preserved learned-clause log in exact CNF order; and
7. for each of all \(1{,}396{,}986\) learned clauses, checks the three
   matching indices, pairwise edge-disjointness, the exact fifteen-edge
   union, and the corresponding positive deleted-edge clause.

CaDiCaL 3.0.1 generated eleven binary DRAT traces with
`--checkproof=1`; all eleven internal proof checks passed.  Upstream
`drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` independently reports
`VERIFIED` for all eleven traces.

The complete compressed package is about 91 MB.  It includes:

- every frozen CNF, learned-clause log, and DRAT trace;
- `MANIFEST.sha256` for the compressed files;
- `RAW_SHA256.txt` for their decompressed contents;
- `CERTIFICATE_RESULTS.json`; and
- `verify_certificates.sh`.

The packaged replay was run from the compressed artifacts.  It passed all
33 compressed hashes, all gzip integrity checks, all 33 raw hashes, the
complete semantic audit, and all eleven external `drat-trim` replays.

Replay with an upstream `drat-trim` executable:

```sh
DRAT_TRIM=/path/to/drat-trim \
  collaboration/opus5_r0_orbit_repair/\
2026-07-28_orbit4_fixed_pair_cnf/verify_certificates.sh
```

The generator, semantic verifier, terminal search log, and certificate
package are:

- `2026-07-28_orbit4_fixed_pair_cegis.py`;
- `2026-07-28_orbit4_fixed_pair_verify.py`;
- `2026-07-28_orbit4_fixed_pair_certificate_results.jsonl`; and
- `2026-07-28_orbit4_fixed_pair_cnf/`.

## Scope

This proves the orbit-4 prescribed-colour cut-sufficiency theorem stated
above and closes orbit 4 under the campaign's stronger full-row,
prefix-decomposition, and pairwise-compatibility hypotheses.

Together with the certified results for orbits 0, 1, 2, and 3, five of the
sixteen selected-support Venn types are now closed.  The eleven types
numbered 5 through 15 remain open.  This does not prove the global
coordinated-nine theorem, the later selection and fan-realizability steps,
or Erdős--Rosenfeld Problem #835.

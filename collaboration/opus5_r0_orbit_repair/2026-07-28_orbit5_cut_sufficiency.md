# Orbit 5: certified prescribed-colour cut sufficiency

Date: 2026-07-28

## Result

Let \(V=\{0,\ldots,12\}\), let the three omitted rows be

\[
R_0=012,\qquad R_1=012,\qquad R_2=345,
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

This theorem is stronger than the orbit-5 instance needed by the campaign.
The exact eleven-row equations imply the lower degree bounds because
\(\rho(v)=d_D(v)-1\) and \(\rho(v)\ge t(v)\).  Pairwise compatibility
supplies the pair in premise 4.  The certificate does not assume that
\(D\) decomposes into the six prefix matching layers, does not encode the
other two compatible-pair premises, and does not encode the remaining-row
realization.

The relevant lower degree vector is

\[
(3,3,3,2,2,2,1,1,1,1,1,1,1).
\]

## Complete seventeen-case compatible-pair catalogue

Fix edge-disjoint perfect matchings \(P_0,P_1\) on the common ten-vertex
support \(S_0=S_1\).  Their union is a two-regular graph whose components
are alternating even cycles of length at least four.  Hence its uncoloured
shape is either

\[
C_{10}\qquad\text{or}\qquad C_4\mathbin{\dot\cup}C_6.
\]

Vertices \(3,4,5\) form the distinguished Venn cell
\(R_2\setminus R_0\); the other seven support vertices \(6,\ldots,12\)
are interchangeable.  The stabilizer may also interchange rows 0 and 1,
simultaneously swapping the two matching colours.

For \(C_{10}\), record the three positive cyclic gaps between consecutive
distinguished vertices.  Up to rotation and reflection, the eight
possibilities are

\[
\begin{split}
&(1,1,8),\ (1,2,7),\ (1,3,6),\ (2,2,6),\\
&(1,4,5),\ (2,3,5),\ (2,4,4),\ (3,3,4).
\end{split}
\]

For \(C_4\mathbin{\dot\cup}C_6\), the distinguished vertices have one of
the following distributions:

- all three on \(C_6\), with gap type \((1,1,4)\), \((1,2,3)\), or
  \((2,2,2)\);
- all three on \(C_4\), giving one type;
- two on \(C_4\), at distance one or two, and one on \(C_6\); or
- one on \(C_4\) and two on \(C_6\), at distance one, two, or three.

This gives \(8+(3+1+2+3)=17\) types.

The generic classifier independently checks this elementary description.
It records the full Venn mask and matching colour along each alternating
component, minimizes under path/cycle presentation and the selected-pair
support stabilizer, and then compares all invariant buckets with the
connected components of the explicit generator action graph.  For orbit 5,
all \(514{,}080\) labelled edge-disjoint matching pairs fall into exactly
these seventeen orbits.

The deterministic certificate order is:

| case | pair-union type |
|---|---|
| `orbit5_pair_000` | \(C_4+C_6\), all three marked vertices on \(C_6\), gaps \((1,1,4)\) |
| `orbit5_pair_001` | \(C_4+C_6\), all three on \(C_6\), gaps \((1,2,3)\) |
| `orbit5_pair_002` | \(C_4+C_6\), all three on \(C_6\), gaps \((2,2,2)\) |
| `orbit5_pair_003` | \(C_4+C_6\), all three on \(C_4\) |
| `orbit5_pair_004` | \(C_{10}\), gaps \((1,1,8)\) |
| `orbit5_pair_005` | \(C_{10}\), gaps \((1,2,7)\) |
| `orbit5_pair_006` | \(C_4+C_6\), two on \(C_4\) at distance 1 and one on \(C_6\) |
| `orbit5_pair_007` | \(C_4+C_6\), two on \(C_4\) at distance 2 and one on \(C_6\) |
| `orbit5_pair_008` | \(C_{10}\), gaps \((1,3,6)\) |
| `orbit5_pair_009` | \(C_{10}\), gaps \((2,2,6)\) |
| `orbit5_pair_010` | \(C_{10}\), gaps \((1,4,5)\) |
| `orbit5_pair_011` | \(C_{10}\), gaps \((2,3,5)\) |
| `orbit5_pair_012` | \(C_4+C_6\), one on \(C_4\) and two on \(C_6\) at distance 1 |
| `orbit5_pair_013` | \(C_4+C_6\), one on \(C_4\) and two on \(C_6\) at distance 2 |
| `orbit5_pair_014` | \(C_4+C_6\), one on \(C_4\) and two on \(C_6\) at distance 3 |
| `orbit5_pair_015` | \(C_{10}\), gaps \((2,4,4)\) |
| `orbit5_pair_016` | \(C_{10}\), gaps \((3,3,4)\) |

## Sound relaxation and quantifiers

Assume for contradiction that the theorem fails.  Choose the compatible
pair \(P_0,P_1\) supplied by premise 4.  A support-stabilizing vertex
relabeling maps this labelled pair to one of the seventeen fixed
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
Therefore an UNSAT result for every one of the seventeen formulas rules
out the original counterexample.

The CEGIS process uses a SAT model only to discover additional valid
clauses of type (T).  Its correctness does not depend on the discovered
set being symmetry-closed.

## All capacity cuts

There are \(4{,}040\) positive instances of (C).  The formulas explicitly
encode the 435 that are not already implied by the base bounds:

| \(|U|\) | encoded cuts |
|---:|---:|
| 6 | 413 |
| 7 | 22 |

The other \(3{,}605\) cuts are automatic.  To verify this without trusting
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

Every case has 56,820 variables.  The terminal results are:

| case | fixed-pair third extensions | base clauses | learned triple clauses | final clauses | status |
|---|---:|---:|---:|---:|---|
| `000` | 453 | 227,888 | 86,569 | 314,457 | UNSAT |
| `001` | 504 | 227,939 | 81,947 | 309,886 | UNSAT |
| `002` | 555 | 227,990 | 92,718 | 320,708 | UNSAT |
| `003` | 444 | 227,879 | 88,178 | 316,057 | UNSAT |
| `004` | 453 | 227,888 | 82,412 | 310,300 | UNSAT |
| `005` | 507 | 227,942 | 58,604 | 286,546 | UNSAT |
| `006` | 516 | 227,951 | 90,847 | 318,798 | UNSAT |
| `007` | 570 | 228,005 | 84,088 | 312,093 | UNSAT |
| `008` | 516 | 227,951 | 74,382 | 302,333 | UNSAT |
| `009` | 570 | 228,005 | 115,406 | 343,411 | UNSAT |
| `010` | 519 | 227,954 | 85,824 | 313,778 | UNSAT |
| `011` | 582 | 228,017 | 124,118 | 352,135 | UNSAT |
| `012` | 519 | 227,954 | 79,241 | 307,195 | UNSAT |
| `013` | 585 | 228,020 | 145,937 | 373,957 | UNSAT |
| `014` | 594 | 228,029 | 104,959 | 332,988 | UNSAT |
| `015` | 585 | 228,020 | 133,388 | 361,408 | UNSAT |
| `016` | 594 | 228,029 | 125,338 | 353,367 | UNSAT |

In total, the formulas contain \(1{,}653{,}956\) learned
simultaneous-triple clauses.

## Independent certificate audit

The semantic verifier does not import the orbit-fallback generator.  It:

1. reconstructs the orbit-5 rows, supports, degree lower bounds, and all
   4,040 positive cuts from the generic search and classifier modules;
2. rederives the 435/3,605 encoded/automatic cut split;
3. independently enumerates all 514,080 labelled compatible pairs and
   obtains exactly seventeen canonical representatives;
4. reconstructs every fixed pair and all of its possible third extensions;
5. checks that no vertex-symmetry encoding is present;
6. compares every base clause with the deterministically reconstructed
   formula;
7. reads the preserved learned-clause log in exact CNF order; and
8. for each of all \(1{,}653{,}956\) learned clauses, checks the three
   matching indices, pairwise edge-disjointness, the exact fifteen-edge
   union, and the corresponding positive deleted-edge clause.

CaDiCaL 3.0.1 generated seventeen binary DRAT traces with
`--checkproof=1`; all seventeen internal proof checks passed.  Upstream
`drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` independently reports
`VERIFIED` for all seventeen traces.

The complete compressed package is about 118 MB.  It includes:

- every frozen CNF, learned-clause log, and DRAT trace;
- `MANIFEST.sha256` for the 51 compressed files;
- `RAW_SHA256.txt` for their 51 decompressed contents;
- `CERTIFICATE_RESULTS.json`; and
- `verify_certificates.sh`.

The packaged replay was run from the compressed artifacts.  It passed all
51 compressed hashes, all gzip integrity checks, all 51 raw hashes, the
complete semantic audit, and all seventeen external `drat-trim` replays.

Replay with an upstream `drat-trim` executable:

```sh
DRAT_TRIM=/path/to/drat-trim \
  collaboration/opus5_r0_orbit_repair/\
2026-07-28_fixed_pair_orbit5_work/verify_certificates.sh
```

The generator, independent semantic verifier, terminal search log, and
certificate package are:

- `2026-07-28_fixed_pair_orbit_fallback.py`;
- `2026-07-28_orbit5_fixed_pair_verify.py`;
- `2026-07-28_fixed_pair_orbit5_results.jsonl`; and
- `2026-07-28_fixed_pair_orbit5_work/`.

## Scope

This proves the orbit-5 prescribed-colour cut-sufficiency theorem stated
above and closes orbit 5 under the campaign's stronger full-row,
prefix-decomposition, and pairwise-compatibility hypotheses.

Together with the certified results for orbits 0 through 4, six of the
sixteen selected-support Venn types are now closed.  The ten types numbered
6 through 15 remain open.  This does not prove the global coordinated-nine
theorem, the later selection and fan-realizability steps, or
Erdős--Rosenfeld Problem #835.

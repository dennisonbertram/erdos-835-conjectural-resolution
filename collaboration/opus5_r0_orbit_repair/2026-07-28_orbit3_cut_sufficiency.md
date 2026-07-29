# Orbit 3: certified prescribed-colour cut sufficiency

Date: 2026-07-28

## Result

Orbit 3, with Venn signature

\[
(0,0,2,1,1,1,0),
\]

of the prescribed three-family gate is closed by a computer-assisted proof.
Take the representative omitted triples

\[
R_1=012,\qquad R_2=014,\qquad R_3=234
\]

on \(V=V(K_{13})\), and put \(S_i=V\setminus R_i\).  Let \(D\) be the
union of the six prefix matchings of sizes

\[
4,4,4,5,5,5,
\]

so \(|D|=27\), put \(G=K_{13}-D\), and impose the campaign's hard-case
hypothesis \(\Delta(D)\le5\).  Assume the exact full-row column equations,
the capacity cuts

\[
\sum_{i=1}^3\max(0,|S_i\cap U|-5)\le e_G(U)
\qquad(U\subseteq V),                                      \tag{C}
\]

and that the first two supports have edge-disjoint perfect matchings in
\(G\).  Then \(G\) contains pairwise edge-disjoint perfect matchings
\(M_i\) on \(S_i\), for \(i=1,2,3\).

The full campaign's pairwise-compatibility hypothesis is stronger than the
single compatible-pair premise used here.

The result is certified at three distinct levels:

1. an explicit 16-case support-stabilizer catalogue;
2. a separate semantic verifier for every frozen CNF clause; and
3. a DRAT proof for every case, independently accepted by `drat-trim`.

## Boundary inventory

Let

\[
t(v)=|\{i:v\in R_i\}|,\qquad b(v)=3-t(v).
\]

The prescribed union \(M_1\cup M_2\cup M_3\) has degree \(b(v)\) at \(v\).
For the displayed rows:

- vertices \(0,1\) belong only to \(S_3\), so \(b=1\);
- vertex \(2\) belongs only to \(S_2\), so \(b=1\);
- vertex \(4\) belongs only to \(S_1\), so \(b=1\);
- vertex \(3\) belongs to \(S_1,S_2\), so \(b=2\);
- vertices \(5,\ldots,12\) belong to all three supports, so \(b=3\).

Thus the boundary has eight cubic vertices, one degree-two vertex, and four
forced-colour leaves.  Its degree sum is \(30\), hence a simultaneous triple
uses exactly 15 edges.

The separately proved factor theorem guarantees an uncoloured simple
\(b\)-factor under the full-row cuts.  The issue closed here is the stronger
one: the factor can be selected as three matchings with their prescribed
colours.

## Complete compatible-pair catalogue

Fix edge-disjoint perfect matchings \(P_1\) on \(S_1\) and \(P_2\) on
\(S_2\).  Their union has degree one at vertices \(4,2\) and degree two at
the nine common vertices

\[
W=\{3,5,6,\ldots,12\}.
\]

It is therefore an alternating path from \(4\) to \(2\), together with
vertex-disjoint alternating even cycles.  The path-and-cycle shapes are
exactly

\[
P_{10},\quad
P_6\mathbin{\dot\cup}C_4,\quad
P_4\mathbin{\dot\cup}C_6,\quad
P_2\mathbin{\dot\cup}C_8,\quad
P_2\mathbin{\dot\cup}C_4\mathbin{\dot\cup}C_4.            \tag{1}
\]

Vertex \(3\) is distinguished because it is absent from \(S_3\); the other
eight vertices of \(W\) are interchangeable.  The vertex permutation
\((2\ 4)\) interchanges \(R_1,R_2\) and fixes \(R_3\) setwise.  Hence it
interchanges the first two supports and matchings and reflects the terminal
path.  On every cycle, a colour-preserving isomorphism is obtained by
choosing the image of one \(P_1\)-edge and then following the alternating
cycle, so the apparent alternating phase creates no additional orbit.
Rotations, reflections, interchange of equal \(C_4\) components, and
permutations of the eight ordinary core vertices are absorbed in this way.
Consequently the possible locations of vertex \(3\) are:

| shape | inequivalent locations of vertex \(3\) | count |
|---|---|---:|
| \(P_{10}\) | path distances \((1,9),(2,8),(3,7),(4,6),(5,5)\) | 5 |
| \(P_6+C_4\) | path distances \((1,5),(2,4),(3,3)\), or on \(C_4\) | 4 |
| \(P_4+C_6\) | path distances \((1,3),(2,2)\), or on \(C_6\) | 3 |
| \(P_2+C_8\) | on the path or on \(C_8\) | 2 |
| \(P_2+C_4+C_4\) | on the path or on a \(C_4\) | 2 |

This gives exactly \(5+4+3+2+2=16\) orbits.  The generator derives the
invariant

\[
(\text{path length},\ \text{cycle-length multiset},\
  \text{location of vertex }3)
\]

for all \(5\cdot9=45\) raw placements and asserts that its 16 selected
representatives cover all of them.  It also checks directly that each
representative consists of two disjoint perfect matchings on the required
supports.  There is no solver-level symmetry breaker.

If a counterexample to the theorem existed, fix the compatible pair supplied
by the premise.  It would be unextendable and, after a support-preserving
relabeling, would be one of these 16 representatives.  It therefore suffices
to rule out all 16.

## Sound strengthened relaxation

For each representative the frozen formula searches for a deletion graph
\(D\subseteq K_{13}\) subject only to:

1. \(|D|=27\);
2. \(t(v)+1\le d_D(v)\le5\) for every vertex;
3. 555 selected capacity cuts on sets of sizes six, seven, and eight;
4. availability of the ten fixed-pair edges; and
5. deletion of at least one edge from every simultaneous prescribed triple.

The 555 cuts are precisely those not already automatic from
\(\Delta(D)\le5\), \(|D|=27\), and the complete-graph bound within the
enumerated sizes: 518 have size six, 36 have size seven, and one has size
eight.

For completeness, no other cut size is missing.  If \(|U|\le5\), every term
in the left side of (C) is zero.  If \(m=|U|\ge9\), put
\(W'=V\setminus U\) and \(k=|W'|=13-m\le4\).  All three terms in (C) are
then positive, and since \(\sum_v t(v)=9\),

\[
r(U):=\sum_i(|S_i\cap U|-5)=3m-15-t(U).
\]

The row-derived lower degree bound and simplicity give

\[
\begin{aligned}
e_D(U)
 &=27-\sum_{v\in W'}d_D(v)+e_D(W')\\
 &\le27-(t(W')+k)+{k\choose2}\\
 &=18+t(U)-k+{k\choose2}.                                \tag{2}
\end{aligned}
\]

The deletion upper bound equivalent to (C) is

\[
{m\choose2}-r(U)
=54+t(U)-\frac{19k}{2}+\frac{k^2}{2}.                    \tag{3}
\]

The right side of (3) exceeds the right side of (2) by \(36-8k\ge4\).
Thus every cut with at least nine vertices is automatic.  The finite
enumeration of sizes six through eight is therefore complete, not a
weakening at the cut level.

Every full source instance lies in this searched class.  Indeed, the exact
row equation

\[
\rho(v)=d_D(v)-1
\]

and \(\rho(v)\ge t(v)\) imply the lower degree bound.  Condition (C) implies
every encoded cut, while the calculation above derives all other cut sizes
from retained base constraints.  The prefix decomposition into six
matchings, the other eight remaining rows, and their completion constraints
are discarded.  These omissions enlarge the candidate class, so UNSAT in
this relaxation is stronger than required.

The last condition is implemented without a quantifier error.  Initially,
the formula blocks every third matching disjoint from the fixed pair.  For
each SAT model, exact CEGIS enumerates all available matchings in all three
families and every pairwise edge-disjoint triple.  For each union \(Q\) it
adds the logically necessary counterexample clause

\[
\bigvee_{e\in Q} d_e.                                      \tag{4}
\]

Every such \(Q\) has 15 edges.  Once the accumulated formula is UNSAT, no
deletion graph in the relaxation can block all simultaneous triples.

## Finite results

Every case has 72,933 variables and 555 encoded capacity cuts.  All 16
accumulated formulas are UNSAT.

| type | rounds | clauses | fixed-pair thirds | global triple clauses |
|---|---:|---:|---:|---:|
| `P10_X0` | 33 | 368,627 | 406 | 76,214 |
| `P10_X1` | 66 | 468,642 | 453 | 176,182 |
| `P10_X2` | 109 | 490,998 | 460 | 198,531 |
| `P10_X3` | 78 | 483,369 | 462 | 190,900 |
| `P10_X4` | 95 | 462,154 | 463 | 169,684 |
| `P6_C4_X0` | 37 | 393,935 | 407 | 101,521 |
| `P6_C4_X1` | 79 | 429,983 | 453 | 137,523 |
| `P6_C4_X2` | 117 | 533,236 | 458 | 240,771 |
| `P6_C4_X5` | 105 | 499,873 | 462 | 207,404 |
| `P4_C6_X0` | 44 | 359,648 | 404 | 67,237 |
| `P4_C6_X1` | 66 | 437,415 | 444 | 144,964 |
| `P4_C6_X3` | 79 | 482,181 | 462 | 189,712 |
| `P2_C8_X0` | 27 | 356,206 | 359 | 63,840 |
| `P2_C8_X1` | 56 | 453,799 | 453 | 161,339 |
| `P2_C4_C4_X0` | 29 | 371,884 | 361 | 79,516 |
| `P2_C4_C4_X1` | 77 | 439,731 | 453 | 147,271 |

## Independent semantic audit

The separate verifier
`2026-07-28_orbit3_support_closure_verify.py` does not trust the CEGIS
routine's claim about its learned clauses.  For every frozen formula it:

1. regenerates the complete static formula and checks it clause-for-clause
   against the frozen prefix;
2. requires every later clause to consist of 15 distinct positive deletion
   variables; and
3. independently backtracks a prescribed three-edge-colouring of those 15
   edges, checking the exact boundary degrees and allowed colours.

It accepted all 16 formulas and all 2,352,609 semantic triple clauses.  It
also rederives the 16 pair orbits, the 555 selected cuts, and all 945 perfect
matchings on each support.

Run:

```sh
TMPDIR=/private/tmp /usr/bin/python3 -B \
  collaboration/opus5_r0_orbit_repair/2026-07-28_orbit3_support_closure_verify.py
```

## DRAT certification

CaDiCaL 3.0.1 re-solved every frozen CNF as UNSAT while emitting an ASCII
DRAT trace with `--check=true`.  Its internal checker and LRAT checker both
accepted every generated derivation.

The independent upstream `drat-trim` checker then replayed the actual traces:

| type | original clauses in core | proof lemmas in core | resolution steps | result |
|---|---:|---:|---:|---|
| `P10_X0` | 7,864 | 88,936 | 1,759,658 | VERIFIED |
| `P10_X1` | 8,513 | 63,800 | 1,204,682 | VERIFIED |
| `P10_X2` | 7,697 | 63,561 | 1,230,610 | VERIFIED |
| `P10_X3` | 8,419 | 73,150 | 1,415,722 | VERIFIED |
| `P10_X4` | 8,031 | 63,689 | 1,224,557 | VERIFIED |
| `P6_C4_X0` | 7,383 | 68,323 | 1,358,493 | VERIFIED |
| `P6_C4_X1` | 8,140 | 66,959 | 1,233,185 | VERIFIED |
| `P6_C4_X2` | 6,746 | 54,013 | 1,041,036 | VERIFIED |
| `P6_C4_X5` | 8,357 | 72,548 | 1,363,653 | VERIFIED |
| `P4_C6_X0` | 6,842 | 80,670 | 1,625,517 | VERIFIED |
| `P4_C6_X1` | 8,394 | 73,503 | 1,394,922 | VERIFIED |
| `P4_C6_X3` | 7,730 | 63,226 | 1,205,986 | VERIFIED |
| `P2_C8_X0` | 10,203 | 118,348 | 2,581,775 | VERIFIED |
| `P2_C8_X1` | 7,720 | 70,015 | 1,367,986 | VERIFIED |
| `P2_C4_C4_X0` | 9,831 | 85,875 | 1,745,291 | VERIFIED |
| `P2_C4_C4_X1` | 8,338 | 76,107 | 1,468,811 | VERIFIED |

Every checked trace has zero RAT lemmas in its core.

The checker came from the official
[`marijnheule/drat-trim`](https://github.com/marijnheule/drat-trim)
repository at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  The checked source file has
SHA-256
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`;
the local checker executable used for all 16 replays has SHA-256
`42a69f9a17bcd58001676abf02d58992bd0ede58410a467dda07a350fec498c9`.

## Compressed artifacts and replay

The CNFs and DRAT traces are stored with deterministic `gzip -9 -n`
compression in `2026-07-28_orbit3_support_closure_cnf/`.  The manifest
records compressed hashes, while `RAW_SHA256.txt` records the expected
hashes after decompression.  No stored certificate file is larger than
7.2 MB.

Verify the archives:

```sh
cd collaboration/opus5_r0_orbit_repair/2026-07-28_orbit3_support_closure_cnf
shasum -a 256 -c MANIFEST.sha256
gzip -t ./*.gz
```

Replay one case without changing the repository:

```sh
certificate_dir=collaboration/opus5_r0_orbit_repair/2026-07-28_orbit3_support_closure_cnf
replay_dir="$(mktemp -d /private/tmp/orbit3-P10_X0.XXXXXX)"
gzip -dc "$certificate_dir/P10_X0.cnf.gz" > "$replay_dir/P10_X0.cnf"
gzip -dc "$certificate_dir/P10_X0.drat.gz" > "$replay_dir/P10_X0.drat"
drat-trim "$replay_dir/P10_X0.cnf" "$replay_dir/P10_X0.drat" -w
```

The expected terminal line is `s VERIFIED`.

## Scope

This closes only orbit 3 of the local prescribed three-family
cut-sufficiency gate under the explicit \(\Delta(D)\le5\) hard-case
hypothesis.  It is a genuine theorem needed by the coordinated-nine attack,
but it does **not** by itself prove the global seven-family selection step,
the size-eight route, the coordinated-nine theorem, or
Erdős--Rosenfeld Problem #835.

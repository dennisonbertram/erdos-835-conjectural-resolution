# Orbit 2: certified cut sufficiency

Date: 2026-07-28

## Result

Orbit 2 of the prescribed three-family gate is closed by a
computer-assisted proof.

Take the representative omitted triples

\[
T_0=012,\qquad T_1=012,\qquad T_2=123
\]

and supports \(S_i=V(K_{13})\setminus T_i\).  Let \(D\) be the union of the
six prefix matchings of sizes \(4,4,4,5,5,5\), put \(G=K_{13}-D\), and impose
the campaign's hard-case hypothesis \(\Delta(D)\le5\).  If the selected
families are pairwise compatible and every capacity cut

\[
\sum_{i=0}^2\max(0,|U\cap S_i|-5)\le e_G(U)
\qquad(U\subseteq V(K_{13}))
\]

holds, then the three families have a simultaneous triple of pairwise
edge-disjoint perfect matchings.

The finite proof uses only compatibility of the two families with the
identical support.  Compatibility involving the third family is dropped.
Thus the checked statement is stronger than the one needed by the full
campaign.

## Exact full-row reduction

Vertices \(1,2\) lie in all three selected omitted triples and hence outside
all three selected supports.  Delete those vertices and relabel

\[
3\mapsto A,\qquad 0\mapsto B,\qquad
\{4,\ldots,12\}\mapsto W=\{2,\ldots,10\}.
\]

On the active vertex set

\[
R=\{A,B\}\cup W
\]

the supports become

\[
S_0=S_1=\{A\}\cup W,\qquad S_2=\{B\}\cup W.
\]

The exact class-B column equation is

\[
\rho(v)=d_D(v)-1.
\]

Because vertices \(1,2\) occur in the three displayed remaining rows,
\(\rho(1),\rho(2)\ge3\), so

\[
d_D(1),d_D(2)\ge4.
\]

Since \(|D|=27\),

\[
\begin{aligned}
e_D(R)
&=27-d_D(1)-d_D(2)+\mathbf 1_{\{12\in D\}}\\
&\le 27-4-4+1=20.
\end{aligned}
\]

The finite proof deliberately relaxes this exact bound to

\[
e_D(R)\le23.
\]

It also drops the remaining row structure, the six-colour prefix
decomposition, all edges incident with the two removed vertices, cuts not
contained in \(R\), and two of the three pair-compatibility assumptions.
Every exact full-row instance therefore maps into the larger searched class,
so UNSAT there proves the stated result.

The bound \(\Delta(D)\le5\) remains an explicit hard-case hypothesis.

## Complete marked compatible-pair catalogue

Compatibility of the two identical-support families supplies edge-disjoint
perfect matchings \(P_0,P_1\) on the ten-vertex set \(\{A\}\cup W\).  Their
union is 2-regular.  Every component alternates between \(P_0\) and \(P_1\),
so it is an even cycle of length at least four.

The only partitions of ten into such cycle lengths are

\[
10,\qquad 4+6.
\]

The terminal \(A\) is distinguished because it is absent from \(S_2\).
Consequently the complete marked list is

\[
C_{10},\qquad
C_4(A)+C_6,\qquad
C_4+C_6(A).
\]

These are the script cases `C10`, `C4_marked`, and `C6_marked`.

This is an orbit-complete mathematical reduction.  Fix \(A,B\).  On the
component containing \(A\), begin at the \(P_0\)-neighbour of \(A\) and walk
in the forced alternating order.  On every unmarked component, begin with
any \(P_0\)-edge and walk alternately.  Relabel the nine core vertices in
these orders.  This maps the labelled pair to exactly the canonical pair in
`2026-07-28_orbit2_support_cut_closure.py`.  Rotations and reflections of
the unmarked cycle are absorbed by the core relabelling; neither terminal is
moved and the matching labels are preserved.

An independent exhaustive audit enumerated all 514,080 ordered disjoint
pairs of perfect matchings on the common support:

| marked type | ordered pairs |
|---|---:|
| \(C_{10}\) | 362,880 |
| \(C_4(A)+C_6\) | 60,480 |
| \(C_4+C_6(A)\) | 90,720 |

No fourth type occurs.  No solver-level vertex-symmetry clauses are used.

## Capacity-cut audit

The generator enumerates every one of the \(2^{11}\) subsets \(U\subseteq R\).
There are 898 subsets with positive required capacity.  Writing

\[
r(U)=\sum_i\max(0,|U\cap S_i|-5),
\]

the deletion form of the cut is

\[
e_{D[R]}(U)\le {|U|\choose2}-r(U).
\]

The relaxed base conditions imply

\[
e_{D[R]}(U)
\le
\min\left\{
{|U|\choose2},\,
23,\,
\left\lfloor\frac{5|U|}{2}\right\rfloor
\right\}.
\]

A cut is omitted only when this automatic upper bound is no larger than the
cut upper bound.  Exactly 465 nonautomatic cuts are encoded:

- 336 on six vertices;
- 120 on seven vertices;
- 9 on eight vertices.

The other 433 positive cuts follow directly from the explicit degree and
total-edge bounds.

## Exact CNF and CEGIS closure

Each case uses 55 semantic edge-deletion variables on \(K_{11}\), plus the
auxiliary variables of exact unary counters.  It encodes:

1. the ten edges of the fixed compatible pair as available;
2. \(\deg_{D[R]}(v)\le5\) for every active vertex;
3. the relaxed bound \(e_D(R)\le23\);
4. all 465 nonautomatic support cuts;
5. every third-support perfect matching disjoint from the fixed pair as
   blocked.

For every SAT model, the generator independently enumerates all simultaneous
triples.  Each available triple \(M_0,M_1,M_2\) adds the valid
counterexample-exclusion clause

\[
\bigvee_{e\in M_0\cup M_1\cup M_2} d_e.
\]

The three cases terminate UNSAT:

| marked type | rounds | variables | clauses | fixed-pair thirds | global triple clauses | SHA-256 |
|---|---:|---:|---:|---:|---:|---|
| \(C_{10}\) | 196 | 71,208 | 349,373 | 365 | 63,915 | `3b871e59ee88cb62dfbb1adaf8506de83e13b7faeae1d5d8dff2d8c49e3ce74c` |
| \(C_4(A)+C_6\) | 160 | 71,208 | 668,713 | 364 | 383,256 | `63362bebb238e9de6f7712740379e5face5000aea437cf0fdb070c1d111603cf` |
| \(C_4+C_6(A)\) | 170 | 71,208 | 351,402 | 366 | 65,943 | `84d403a7e4a7da0d27750b9f0bb5d166696ca0d3ec1bdfb534ae2601b45326e6` |

The semantic auditor reconstructs the complete base formula, checks it
clause-for-clause against each frozen CNF, and verifies that every later
15-literal clause is the edge union of a prescribed simultaneous triple.
Thus the accumulated formulas contain only the advertised constraints and
logically valid no-counterexample clauses.

## Independent certification

CaDiCaL 3.0.1 re-solved every frozen CNF as UNSAT while emitting a binary
DRAT trace with `--check=true`.  Its internal checker and LRAT checker both
accepted every derived clause.

PySAT's independent Glucose 4 backend also returned UNSAT:

| marked type | Glucose 4 solve time |
|---|---:|
| \(C_{10}\) | 40.724 s |
| \(C_4(A)+C_6\) | 43.040 s |
| \(C_4+C_6(A)\) | 39.576 s |

Finally, the upstream `drat-trim` checker independently replayed the actual
proof traces:

| marked type | original clauses in core | proof lemmas in core | resolution steps | result |
|---|---:|---:|---:|---|
| \(C_{10}\) | 11,006 | 57,423 | 765,774 | VERIFIED |
| \(C_4(A)+C_6\) | 10,737 | 55,467 | 752,113 | VERIFIED |
| \(C_4+C_6(A)\) | 10,586 | 53,993 | 729,766 | VERIFIED |

Every trace had zero RAT lemmas in its core.  The checker was compiled from
the official `marijnheule/drat-trim` source at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; the `drat-trim.c` source file
had SHA-256
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.

## Compressed artifacts and replay

The CNFs and proofs are stored with deterministic `gzip -9 -n` compression
under `2026-07-28_orbit2_support_cut_closure_cnf/`.  `MANIFEST.sha256`
checks the compressed files, `RAW_SHA256.txt` checks their decompressed
contents, and `CERTIFICATE_RESULTS.json` records all solver and checker
statistics.

The standalone replay performs both the semantic CNF audit and all three
independent DRAT checks:

```sh
DRAT_TRIM=/path/to/drat-trim \
  collaboration/r0_three_family_helly_gate/\
2026-07-28_orbit2_support_cut_closure_cnf/verify_certificates.sh
```

It decompresses only into a fresh temporary directory and removes that
directory on exit.

Regenerate the three accumulated raw CNFs with:

```sh
TMPDIR=/private/tmp /usr/bin/python3 -B \
  collaboration/r0_three_family_helly_gate/\
2026-07-28_orbit2_support_cut_closure.py \
  --output-dir /private/tmp/orbit2-regenerated
```

The generator asserts the expected rounds, variable counts, clause counts,
and raw CNF hashes before reporting a completed UNSAT case.

## Scope

This closes exactly support orbit 2, signature

\[
(0,0,1,1,0,0,2),
\]

of the local prescribed three-family cut-sufficiency gate under the
campaign's explicit \(\Delta(D)\le5\) hard-case hypothesis.

It does not close the other support orbits, the global seven-family
selection step, any size-eight route, or Erdős--Rosenfeld Problem #835.

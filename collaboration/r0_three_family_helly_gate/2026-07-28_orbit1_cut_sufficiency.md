# Orbit 1: certified cut sufficiency

Date: 2026-07-28

## Result

Orbit 1 of the prescribed three-family gate is closed by a
computer-assisted proof.

Take the representative omitted triples

\[
T_0=012,\qquad T_1=023,\qquad T_2=123
\]

and supports \(S_i=V(K_{13})\setminus T_i\).  Let \(D\) be the union of the
six prefix matchings of sizes

\[
4,4,4,5,5,5,
\]

so \(|D|=27\), and impose the campaign's hard-case hypothesis
\(\Delta(D)\le5\).  Put \(G=K_{13}-D\).  If one pair of the three matching
families is compatible and every capacity cut

\[
\sum_{i=0}^2\max(0,|U\cap S_i|-5)\le e_G(U)
\qquad(U\subseteq V(K_{13}))
\]

holds, then the three families have a simultaneous triple of pairwise
edge-disjoint perfect matchings.

Pairwise compatibility, as imposed by the full campaign, is stronger than
the single compatible-pair hypothesis used here.

This is not merely solver evidence.  The five frozen UNSAT formulas have
binary DRAT proofs independently verified by the upstream `drat-trim`
checker.  CaDiCaL's internal DRAT/LRAT checking and independent Glucose 4
UNSAT solves give two additional checks.

## Exact full-row reduction

Let

\[
W=\{4,5,\ldots,12\}.
\]

The three supports are

\[
S_0=W\cup\{3\},\qquad
S_1=W\cup\{1\},\qquad
S_2=W\cup\{0\}.
\]

Thus they share a nine-vertex core and have three distinct terminals.
Vertex \(2\) lies outside all three supports.

The exact class-B column equation is

\[
\rho(v)=d_D(v)-1.
\]

Since vertex \(2\) is in all three displayed remaining triple rows,
\(\rho(2)\ge3\), and hence \(d_D(2)\ge4\).  With \(|D|=27\), the deletion
graph induced on

\[
R=V(K_{13})\setminus\{2\}
\]

therefore satisfies

\[
e_D(R)=27-d_D(2)\le23.
\]

Every full-row instance consequently maps to a graph on \(R\) satisfying

\[
\Delta(D[R])\le5,\qquad e_D(R)\le23.
\]

The finite proof deliberately drops the remaining row structure, prefix
edge-colouring, edges incident with vertex \(2\), cuts containing vertex
\(2\), and compatibility of the other two pairs.  Dropping these restrictions
enlarges the searched class.  UNSAT in this larger class therefore proves the
stated exact-full-row result.

The bound \(\Delta(D)\le5\) is preserved explicitly; it is the existing
hard-case hypothesis, not a consequence of the six prefix sizes alone.

## Complete compatible-pair catalogue

Choose edge-disjoint perfect matchings \(P_0\) on \(S_0\) and \(P_1\) on
\(S_1\).  Their union has degree one at terminals \(3,1\) and degree two at
every vertex of \(W\).  It is therefore one alternating path between the
terminals, together with alternating even cycles.

The path begins with a \(P_0\)-edge and ends with a \(P_1\)-edge, so its
length \(L\) is even.  It uses \(L-1\) core vertices, leaving \(10-L\) core
vertices for cycles.  Every cycle is even and has length at least four.
Consequently the complete list is

\[
\begin{array}{c|c}
L&\text{remaining cycles}\\ \hline
10&\varnothing\\
6&C_4\\
4&C_6\\
2&C_8\\
2&C_4\mathbin{\dot\cup}C_4.
\end{array}
\]

The nominal case \(L=8\) leaves two vertices and is impossible.  These are
the five script labels

\[
P10,\quad P6+C4,\quad P4+C6,\quad P2+C8,\quad P2+C4+C4.
\]

For each type, relabel the nine common-core vertices along the path and
cycles.  The alternating colours on the terminal path are forced; rotations,
reflections, phase choices on cycles, and interchange of equal \(C_4\)
components are absorbed by the core relabelling.  This puts the pair into
exactly the canonical form displayed in
`2026-07-28_orbit1_support_cut_closure.py`.

No lexicographic or other solver-level symmetry breaker is used.  The only
symmetry reduction is this explicit five-case mathematical catalogue, so it
cannot discard a labelled obstruction.

## Capacity-cut audit

The generator enumerates every one of the \(2^{12}\) subsets \(U\subseteq R\).
There are 1,922 subsets with a positive required capacity.  Writing

\[
r(U)=\sum_i\max(0,|U\cap S_i|-5),
\]

the corresponding deletion inequality is

\[
e_{D[R]}(U)\le { |U| \choose 2}-r(U).
\]

The degree and total-edge bounds already imply

\[
e_{D[R]}(U)
\le
\min\left\{
{|U|\choose2},\,
23,\,
\left\lfloor\frac{5|U|}{2}\right\rfloor
\right\}.
\]

The generator omits a cut only when this automatic upper bound is no larger
than the cut's upper bound.  Exactly 507 nonautomatic cuts are encoded:

- 462 on six vertices;
- 36 on seven vertices;
- 9 on eight vertices.

Thus every support cut is either explicitly encoded or a direct consequence
of two explicitly encoded base bounds.

## Exact CNF and CEGIS closure

Each case uses 66 semantic edge-deletion variables on \(K_{12}\), plus exact
unary-counter variables.  It encodes:

1. the ten edges of the fixed compatible pair as available;
2. \(\deg_{D[R]}(v)\le5\) for every vertex;
3. \(e_D(R)\le23\);
4. all 507 nonautomatic support cuts;
5. every possible third matching disjoint from the fixed pair as blocked.

The generator independently enumerates all 945 perfect matchings of each
ten-vertex support.  For every SAT model, it enumerates all simultaneous
triples.  Each available triple \(M_0,M_1,M_2\) adds the valid
counterexample-exclusion clause

\[
\bigvee_{e\in M_0\cup M_1\cup M_2} d_e.
\]

All five cases terminate UNSAT:

| pair type | rounds | variables | clauses | fixed-pair thirds | global triple clauses |
|---|---:|---:|---:|---:|---:|
| \(P10\) | 170 | 68,282 | 632,259 | 365 | 358,506 |
| \(P6+C4\) | 183 | 68,282 | 576,234 | 366 | 302,480 |
| \(P4+C6\) | 167 | 68,282 | 1,078,041 | 364 | 804,289 |
| \(P2+C8\) | 129 | 68,282 | 563,398 | 359 | 289,651 |
| \(P2+C4+C4\) | 140 | 68,282 | 630,594 | 361 | 356,845 |

The final CNF contains only original exact constraints and clauses logically
required by the assumption that no simultaneous triple exists.  Therefore
UNSAT of the accumulated CNF closes the finite case.

## Independent certification

CaDiCaL 3.0.1 re-solved every frozen CNF as UNSAT while emitting a binary
DRAT trace with `--check=true`.  Its internal output reported both checker
and LRAT-checker statistics.

PySAT's Glucose 4 backend independently returned UNSAT:

| pair type | Glucose 4 total time |
|---|---:|
| \(P10\) | 46.715 s |
| \(P6+C4\) | 41.639 s |
| \(P4+C6\) | 44.721 s |
| \(P2+C8\) | 57.594 s |
| \(P2+C4+C4\) | 36.171 s |

Finally, `drat-trim` independently checked the actual proof traces:

| pair type | original clauses in core | proof lemmas in core | resolution steps | result |
|---|---:|---:|---:|---|
| \(P10\) | 11,247 | 59,332 | 889,386 | VERIFIED |
| \(P6+C4\) | 10,736 | 56,214 | 865,467 | VERIFIED |
| \(P4+C6\) | 12,481 | 59,528 | 861,527 | VERIFIED |
| \(P2+C8\) | 12,401 | 73,627 | 1,111,829 | VERIFIED |
| \(P2+C4+C4\) | 11,121 | 54,081 | 845,609 | VERIFIED |

Every trace had zero RAT lemmas in its core.

The checker was compiled with

```sh
cc -O2 -DNDEBUG drat-trim.c -o drat-trim
```

from the official
[`marijnheule/drat-trim`](https://github.com/marijnheule/drat-trim)
repository at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
The source file used had SHA-256
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.

## Compressed artifacts and replay

All CNFs and traces are stored with deterministic `gzip -9 -n` compression
under `2026-07-28_orbit1_support_cut_closure_cnf/`.  The uncompressed copies
were removed after recording and verifying their hashes.  No compressed file
is larger than 17.5 MB.

Verify the compressed manifest:

```sh
cd collaboration/r0_three_family_helly_gate/2026-07-28_orbit1_support_cut_closure_cnf
shasum -a 256 -c MANIFEST.sha256
gzip -t ./*.gz
```

Replay one certificate without changing the repository:

```sh
certificate_dir=collaboration/r0_three_family_helly_gate/2026-07-28_orbit1_support_cut_closure_cnf
replay_dir="$(mktemp -d /private/tmp/orbit1-P10.XXXXXX)"
gzip -dc "$certificate_dir/P10.cnf.gz" > "$replay_dir/P10.cnf"
gzip -dc "$certificate_dir/P10.drat.gz" > "$replay_dir/P10.drat"
drat-trim "$replay_dir/P10.cnf" "$replay_dir/P10.drat" -i -w
```

The expected terminal line is `s VERIFIED`.  Replace `P10` with any other
case basename for the other four replays.  `RAW_SHA256.txt` records the
expected hashes after decompression.

Regenerate the raw CNFs:

```sh
TMPDIR=/private/tmp /usr/bin/python3 -B \
  collaboration/r0_three_family_helly_gate/2026-07-28_orbit1_support_cut_closure.py
```

For each raw CNF, regenerate the checked binary proof and deterministic
archives:

```sh
cadical --check=true P10.cnf P10.drat
gzip -9 -n P10.cnf P10.drat
```

## Scope

This closes only orbit 1, signature

\[
(0,0,1,0,1,1,1),
\]

of the local prescribed three-family cut-sufficiency gate, under the
campaign's explicit \(\Delta(D)\le5\) hard-case hypothesis.  Together with
the separate orbit-0 certificate it closes two of the 16 support orbits.

It does not close the other 14 support orbits, the global seven-family
selection step, any size-eight route, or Erdős-Rosenfeld Problem #835.

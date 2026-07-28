# Orbit 0: computer-assisted cut sufficiency

Date: 2026-07-28

## Result

The orbit-0 graph gate is true under the exact prefix bounds used by the
full-row campaign.

Let \(V=S\mathbin{\dot\cup}T\), where \(|S|=10\) and \(|T|=3\).  Let
\(D\) be the union of the six prefix matchings, with

\[
|D|=4+4+4+5+5+5=27,\qquad \Delta(D)\le 5,
\]

and put \(G=K_{13}-D\) and \(H=G[S]\).  Suppose the three selected remaining
triple complements are all \(T\).  If

1. \(H\) has two edge-disjoint perfect matchings, and
2. for every \(U\subseteq V\),

   \[
   3\max(0,|U\cap S|-5)\le e_G(U),
   \]

then \(H\) has three pairwise edge-disjoint perfect matchings.

This is a computer-assisted finite proof, not yet a short handwritten proof.
It is stronger than the required exact-full-row claim: after deriving the two
numeric prefix bounds below, the finite closure does not use the other eight
remaining rows.

## Human reduction

The complete class-B column equation is

\[
\rho(v)=d_D(v)-1.
\]

The three repeated \(T\)-rows give \(\rho(t)\ge3\), hence \(d_D(t)\ge4\),
for all \(t\in T\).  Therefore

\[
\begin{aligned}
12
&\le \sum_{t\in T}d_D(t)\\
&=e_D(S,T)+2e_D(T)\\
&=27-e_D(S)+e_D(T)\\
&\le30-e_D(S),
\end{aligned}
\]

so

\[
e_D(S)\le18.
\]

Only the cuts with \(U\subseteq S\) are needed in the finite check.  They say

\[
e_H(U)\ge3(|U|-5)\qquad(6\le |U|\le10).
\]

Now assume for contradiction that \(H\) has no three disjoint perfect
matchings.  Choose a compatible pair \(P,Q\).  Their union is an alternating
2-factor on ten vertices.  Since its cycles are even and have length at least
four, it has exactly one of two types:

\[
C_{10}\quad\text{or}\quad C_4\mathbin{\dot\cup}C_6.
\]

Relabeling \(S\) puts \(P,Q\) into one of the two canonical forms in
`2026-07-28_orbit0_pair_extension.py`.  Thus a hypothetical counterexample
must occur in one of only two finite cases.

## Exact finite closure

There are 945 perfect matchings of \(K_{10}\).  After fixing \(P,Q\), there
are:

- 293 possible third matchings for the \(C_{10}\) case;
- 292 possible third matchings for the \(C_4\dot\cup C_6\) case.

For each case the CNF has one Boolean variable \(d_e\) for every edge
\(e\in E(K_{10})\), with \(d_e=1\) meaning \(e\in D[S]\).  Exact unary
cardinality constraints encode:

- every edge of \(P\cup Q\) is available;
- \(\deg_{D[S]}(v)\le5\) for every vertex;
- \(e_D(S)\le18\);
- every displayed internal-edge capacity cut;
- every possible third matching disjoint from \(P\cup Q\) meets \(D[S]\).

The CEGIS loop independently enumerates all currently available perfect
matchings.  Whenever it finds three pairwise disjoint ones, it adds the valid
counterexample-exclusion clause

\[
\bigvee_{e\in M_1\cup M_2\cup M_3}d_e.
\]

Both cases terminate UNSAT:

| pair type | rounds | variables | clauses | third-matchings | global triple clauses |
|---|---:|---:|---:|---:|---:|
| \(C_{10}\) | 446 | 75,191 | 329,203 | 293 | 27,925 |
| \(C_4\dot\cup C_6\) | 534 | 75,191 | 329,725 | 292 | 28,448 |

The frozen CNFs were then solved again by CaDiCaL 3.0.1 with
`--check=true --no-binary`.  CaDiCaL returned UNSAT for both, emitted textual
DRAT traces, and reported successful internal DRAT and LRAT checking.
As a solver-diversity check, PySAT's Glucose 4 backend independently returned
UNSAT on the same frozen formulas in 29.485 and 30.595 seconds, respectively.
Finally, the separate `drat-trim` binary replayed both committed traces and
reported `s VERIFIED` (6.077 and 5.933 seconds).

## Frozen artifacts

| artifact | SHA-256 |
|---|---|
| `C10.cnf` | `72ac8e83c76f3c69355324c218b5f715aace5828386996e09edaa30fdbde2e0d` |
| `C10.drat` | `0d4d33ab617efd6861bf4a4c23647b7a4a699e5c2b703e49f58e9b526604ca2b` |
| `C4_C6.cnf` | `b865284e17ce08803a7dd9a38ba80a0ef5aaa829f85355a4ae3e8126a8cc2aa6` |
| `C4_C6.drat` | `eb29c91bbb52395940ae76fe250ff3e1da832860b6306ee0ff322d076c265792` |

They are under
`2026-07-28_orbit0_pair_extension_cnf/`.

Regenerate the finite closure:

```sh
TMPDIR=/private/tmp /usr/bin/python3 -B \
  collaboration/r0_three_family_helly_gate/2026-07-28_orbit0_pair_extension.py
```

Regenerate and internally check the proof traces:

```sh
cadical --check=true --no-binary \
  collaboration/r0_three_family_helly_gate/2026-07-28_orbit0_pair_extension_cnf/C10.cnf \
  collaboration/r0_three_family_helly_gate/2026-07-28_orbit0_pair_extension_cnf/C10.drat

cadical --check=true --no-binary \
  collaboration/r0_three_family_helly_gate/2026-07-28_orbit0_pair_extension_cnf/C4_C6.cnf \
  collaboration/r0_three_family_helly_gate/2026-07-28_orbit0_pair_extension_cnf/C4_C6.drat
```

The external `drat-trim` replay separates proof checking from CaDiCaL's
internal checker.  Glucose 4 supplies an additional solver-diversity UNSAT
solve, though it does not check the DRAT traces.

## Why the earlier obstruction does not contradict this

The repeated-\(012\) full-row obstruction in `NOTE.md` has a common residual
support with 42 perfect matchings, pairwise compatibility, and no disjoint
triple.  It fails exactly one required cut:

\[
U=\{3,4,6,7,9,10\},\qquad e_G(U)=2<3.
\]

The only available edges inside that six-set are \(39\) and \(47\).  Every
perfect matching of the ten-vertex support needs at least one internal edge
of \(U\), so two matchings can use those two edges but three cannot.  The cut
condition removes precisely this obstruction.

## Scope

This closes only orbit 0 of the local three-family gate: three identical
remaining size-ten supports.  It does not close the other 15 support orbits,
the seven-family coordinated selection step, any size-eight route, or
Erdős-Rosenfeld Problem #835 itself.

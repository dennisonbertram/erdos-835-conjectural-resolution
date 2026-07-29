# SUPERSEDED: the centre-0 star threshold note

> **Audit warning (2026-07-26).** Theorem D below omitted the complementation
> factor in \(\operatorname{Aut}(J(32,16))\), and the stated structural reason
> for the Hall claim did not cover row sets of sizes 13 and 14. The numerical
> heuristic in §3 is retained, but the corrected theorem and a stronger,
> chart-independent Hall proof are in
> `cyclic17_star_scope_rev2_and_pointwise_exhaustion.md`. Do not cite the
> unrepaired arguments below.

# The centre-0 star: what the obstruction is, and what refuting it would buy

**Scope, stated first.** Erdős–Rosenfeld #835 remains **open**. This note does
not construct or refute a tight 17-colouring of \(J(32,16)\). It does three
things: it upgrades the *scope* of the cyclic-17 star programme (Theorem D,
proved), it proves that no single-orbit Hall argument can ever explain the star
UNSAT (proved), and it gives a quantitative model that locates the minimum
obstruction size at exactly six rows (**heuristic, not a proof**).

Verifier: `evidence/verify_cyclic17_star_threshold.py` — stdlib only, no solver,
no family enumeration. It prints which of its three parts are proofs.

---

## 0. An audit finding about the enumeration tool

`search_radius5_golf_cyclic_slice_exact_cover.cpp` accepts `--enumerate n`, and
its search halts when `enumerated_solutions.size() >= solution_limit`, when
`nodes >= node_limit`, or when the deadline passes. On the last two it sets
`timed_out`, **but `timed_out` is not printed when any solution was found** —
the JSON says `"status":"SAT"` either way. So a truncated family is
indistinguishable from a complete one in the output. Measured on pair \((0,1)\):

| `--enumerate` | `--seconds` | nodes | status | solutions |
|---|---|---|---|---|
| 100,000 | 20 | 9,469,952 | SAT | 4 |
| 100,000 | 200 | 88,473,600 | SAT | 35 |
| 100,000,000 | 20 | 8,945,664 | SAT | 4 |
| 100,000,000 | 200 | 94,863,360 | SAT | 40 |

Row \((0,1)\) was still yielding new solutions at 95 M nodes. Replacing it with
an unconstrained 40-slot row is therefore the right move, and it makes the
result *stronger*: relaxing a row and still getting UNSAT implies UNSAT with the
true family, whatever it is. A reliable completeness signal from this tool is
`seconds` reported strictly below the requested budget.

---

## 1. Theorem D — the cyclic ansatz is the *weakest* colour-transitive one

> **Theorem D.** Suppose a tight 17-colouring of \(J(32,16)\) admits an
> automorphism group \(G\) that is transitive on the seventeen colour classes.
> Then it admits an automorphism \(\sigma\) of order 17 whose cycle type on the
> 32 points is \(17+1^{15}\) and which permutes the colours in a 17-cycle —
> that is, it satisfies the cyclic ansatz of
> `cyclic17_equivariant_reduction.md`.

*Proof.* Let \(K=\ker(G\to\operatorname{Sym}(\text{colours}))\). The image
\(G/K\) is transitive on 17 points, so \(17\mid |G/K|\) and hence \(17\mid|G|\).
Let \(S\) be a Sylow 17-subgroup of \(G\). The image of a Sylow subgroup is
Sylow in the quotient, and the 17-part of \(|G/K|\) is nontrivial, so \(S\) has
nontrivial image; pick \(\sigma\in S\) with nontrivial image. Exactly one
multiple of 17 is at most 32, so \(17^1\) exactly divides \(32!\); hence every
17-subgroup of \(\operatorname{Sym}(32)\) has order 17 and \(\sigma\) has order
17. Its image is an element of order 17 in \(\operatorname{Sym}(17)\), i.e. a
17-cycle, so \(\sigma\) is already colour-transitive. On the 32 points
\(\sigma\) has cycles of length 1 or 17, and \(2\cdot17=34>32\) forces exactly
one 17-cycle \(A\) and \(|F|=15\) fixed points. Relabelling the colours by
\(\mathbb Z_{17}\) so that \(\sigma\) sends \(q\) to \(q+1\) is the ansatz.
\(\square\)

**What this buys, exactly.**

* A no-go for the cyclic-17 ansatz **over all golf designs of \(\mathbb Z_{17}\)**
  would refute **every colour-transitive** tight 17-colouring of \(J(32,16)\).
* It would **not** refute tight colourings whose automorphism group is trivial
  or merely not colour-transitive. So it would still not settle #835.
* A no-go for **one** chart (Wallis) excludes only that chart. The reported
  centre-0 UNSAT is a Wallis-only statement.

Theorem D is the reason the "all golf designs" quantifier is worth chasing:
it is the difference between a chart-specific curiosity and a theorem about all
symmetric colourings.

---

## 2. Proved: no single-orbit Hall obstruction can exist

At a fixed orbit \(q\), the 14 rows of a star must take pairwise distinct
phases, row \((i,j)\) restricted to its domain \(D_{ij}(q)\). One might hope the
UNSAT is a failure of Hall's condition at some single orbit. It is not, and it
cannot be.

> **Lemma.** In every star of either chart, Hall's condition holds at every
> orbit: for all \(T\) of rows, \(\bigl|\bigcup_{j\in T}D_{ij}(q)\bigr|\ge|T|\).

Verified exhaustively over **all** subsets of the 14 rows, for all 15 centres
and all 40 orbits, in both charts: **0 failures out of 600 (centre, orbit)
pairs each.** The structural reason is immediate: every phase domain contains at
least **11** of the 14 available values, and a star has only 14 rows, so a
violation would require at least 12 rows whose domains all lie inside one common
11-set. None occurs.

**Consequence.** The star infeasibility is not a single-orbit phenomenon. No
Hall/SDR argument at one orbit can prove it, and none should be sought. Any
proof must couple the 40 orbits — which is exactly what the DFS/DRAT
certificate does.

---

## 3. Heuristic: why the minimum obstruction size is exactly six

This section is a **model**, not a proof. It is stated separately for that
reason.

Model each row's chosen slice as drawing, independently at each of the 40
orbits, a uniform phase from that cell's domain. For a set \(S\) of \(m\) rows,

\[
 E(S)=\prod_{j\in S}|F_j|\ \cdot\ \prod_{q=0}^{39}P_q(S),
\]

where \(P_q(S)\) is the probability that the \(m\) draws at orbit \(q\) are
pairwise distinct — computed *exactly* as a weighted permanent by subset DP, not
simulated. Define the **break-even family size** \(F^*(m)\) by \(E=1\) when every
\(|F_j|=F^*\):

\[
 \log_{10}F^*(m)=-\tfrac1m\sum_q\log_{10}P_q(S).
\]

Measured (Wallis, centre 0; the \((-1)\)-symmetric chart agrees to three
significant figures):

| \(m\) | \(\sum_q\log_{10}P_q\) | break-even \(F^*\) | actual \(\approx486\) |
|---|---|---|---|
| 2 | −1.27 | 4 | tuples expected |
| 3 | −3.92 | 20 | tuples expected |
| 4 | −8.06 | 103 | tuples expected |
| 5 | −13.84 | **586** | **not expected** |
| 6 | −21.43 | **3,731** | **not expected** |
| 7 | −31.06 | 27,348 | not expected |

The exhaustively enumerated centre-0 families have sizes 449–526, mean **486**.

**Reading.** \(F^*\) crosses the actual family size between \(m=5\) and
\(m=6\): at \(m=5\) you would need families of about 586 and you have 486 — a
shortfall of 1.2×; at \(m=6\) you would need about 3,731 and you have 486 — a
shortfall of 7.7×. *That* is why the minimum obstruction is six rows. With the
true sizes, the reported core \((0,2)\dots(0,7)\) gives \(\log_{10}E=-5.33\),
which is the generic value for a 6-subset — the core is **not special**, which
is consistent with 1,712 of the 1,716 6-subsets being UNSAT.

**Limits of the model, stated plainly.** \(E<1\) does not prove non-existence:
the families are fixed sets, not random ones. The model is systematically
optimistic for UNSAT — it gives \(E\approx10^{-0.4}<1\) at \(m=5\) although every
5-subset is reported SAT, and predicts \(1716\times10^{-5.3}\approx0.008\) SAT
6-subsets although 4 are reported. It locates the transition; it does not count.
The rigorous statement remains the DFS/DRAT certificate.

---

## 4. The \((-1)\)-symmetric chart is not expected to escape

The break-even table is **the same to three significant figures** on the
\((-1)\)-symmetric chart (\(F^*(6)=3{,}732\) versus 3,731). This is not a
coincidence: §5.1 of `cyclic_layer_recursion_prime_census.md` shows that the
aggregate invariants — 456 allowed translates per fixed pair, the
\(2\)-\((15,3,16)\) hole multidesign, 47,880 phase literals — are **forced by the
golf-design axioms and are design-independent**. The break-even count is driven
by those aggregates.

So the constructive pivot to the symmetric chart is predicted to hit the same
wall, and I do not recommend spending enumeration budget on its star. This is a
prediction from the model in §3, not a proof; the cheap decisive test is to
enumerate one symmetric-chart star family and compare its size against
\(F^*(6)=3{,}732\).

---

## 5. Where this leaves the constructive route

Combining Theorem D with §3–§4: within colour-transitive ansätze at \(k=16\)
there is **no intermediate rung to retreat to**. Because 17 is prime, any
colour-transitive group contains a colour-transitive \(\mathbb Z_{17}\)
(Theorem D), so \(\mathbb Z_{17}\) is the *weakest* such hypothesis — imposing
more symmetry only shrinks the families further, and there is no proper subgroup
to impose less. The cyclic ansatz is all-or-nothing, and the counting model says
it fails by a factor of about 7.7 in family size.

The honest constructive conclusion is therefore that a genuinely different
starter or chart within the cyclic-17 framework is **not** where an advance on
#835 will come from, and that any advance must abandon colour-transitivity
altogether. I am not proposing a replacement ansatz here; I have not found one
that is grounded rather than speculative.

---

## 6. Reproduce

```sh
python3 -B evidence/verify_cyclic17_star_threshold.py
```

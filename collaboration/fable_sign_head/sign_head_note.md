# The radius-5 sign head: exact evaluation (H), the E-lemma, fiber re-expressions, and one-sided no-gos

Date: 2026-07-26.  Labels used exactly: **PROVED / COMPUTATION /
CONJECTURE / OPEN**.  Companion verifier (pure stdlib, deterministic):
`verify_sign_head.py`; synthetic-table generator (OR-Tools CP-SAT +
cadical): `gen_tables.py`; raw data: the JSON files listed in §10.

Scope, stated at the top: everything below is structure theory and
computation about local balls of \(O_k\).  Nothing is a construction of a
radius-5 ball at \(k=16\), and nothing here excludes one.
**Erdős–Rosenfeld #835 is not solved.**

> **Subsequent independent result.**  This Fable note is preserved as a
> time-stamped research record.  The later proof in
> [`../global_h_parity/README.md`](../global_h_parity/README.md) resolves the
> full shared-\(N\) sign question left open in §§7–8: each layer has a closed
> one-factorization formula, and the total product is identically \(F(L,M)\).
> The one-sided counterexamples and the theorem \(H=F(L,M)\) below remain
> valid; the older “OPEN” status for the total two-sided sign is superseded.

Sources relied on (certified elsewhere in the repo):

- `evidence/odd_graph_local_ball/flag_at_exact_formula.md` — equations
  (1)–(10) and the induced-order conventions (all positions zero-based;
  \(V=0..k-1\), \(A=0..k-2\), \(\infty:=k\) last).
- `evidence/odd_graph_local_ball/radius4_dual_trace_forced.md` — Lemmas
  1–4, the flag Latin-square theorem, and the exact global AT product
  (its equation (5) = formula (F) = equation (1) of
  `flag_at_exact_formula.md`).
- `evidence/odd_graph_local_ball/radius4_reduction.md`,
  `radius5_minimal_trace_forced.md` — conditions 1–4 and the forced trace.
- `collaboration/claude/flag_sign_reference_independence.md`,
  `audit_formula_F.py` — certified (F) and the audit conventions reused
  verbatim here.

Objects.  \(H(L,M,N)=\prod_{i,u}\prod_{x\ne L_i(u)}
\operatorname{sgn}\Phi_{i,u,x}\) (partial fibers with their induced
domain/codomain orders);
\(E(L,M)=\prod_{i,u}\prod_{x\ \mathrm{generic}}
\varepsilon(v_M(i,u,x),v_L(i,u,x))\) with
\(v_M\) the \(M_i\)-\(x\)-partner of \(u\), \(v_L=L_i^{-1}(x)\), and
\(\varepsilon=+1\) iff \(v_M\) precedes \(v_L\);
\(T\), \(S_i\), \(\delta\), \(\operatorname{AT}\) as in the sources.
Write throughout
\[
 \mathrm{RHS}(F)\;=\;(-1)^{k(k-1)/2}\operatorname{AT}(T)\prod_i\delta(S_i).
\]

---

## 1. Theorem (H) — PROVED

**Theorem (H).**  Let \(k\) be even and let \((L,M,N)\) satisfy the
unrestricted radius-5 conditions — in fact only this much is used:
conditions 1–3, condition 4 for every edge \(uv\), and the forced trace
for every index pair \(ij\) (equivalently: every flag square \(Q^{i,u}\)
is Latin).  Then
\[
 \boxed{\;H(L,M,N)\;=\;E(L,M)\cdot(-1)^{k(k-1)/2}
 \operatorname{AT}(T)\prod_{i\in A}\delta(S_i)\;=\;E(L,M)\cdot
 \mathrm{RHS}(F).\;}
\]

*Proof.*  Every step is either certified in the sources or elementary;
each is cited.

1. **Per flag, equation (10)** of `flag_at_exact_formula.md`:
   \[
    \Sigma(Q^{i,u})=(-1)^{\binom{k-2}{2}+1}
    \Bigl(\prod_{x\ \mathrm{generic}}\varepsilon(v_M,v_L)\Bigr)
    \Bigl(\prod_{x}\operatorname{sgn}\Phi_{i,u,x}\Bigr),
   \]
   where \(\Sigma(Q)\) is the product of the completed symbol-permutation
   signs.  (10) is assembled in the source from the exact cofactor
   expansions (8)–(9) and the three sweep facts of Lemma 4
   (`radius4_dual_trace_forced.md`): the generic omitted rows sweep
   \(A\setminus\{i\}\) once, the \(M\)-holes sweep the finite columns
   except \(w_\infty\), the \(L\)-holes sweep them except \(v_0\), so the
   ordinary position exponents of (8)–(9) sum to
   \((k-2)+(k-1)+\binom{k-2}{2}+2\binom{k-1}{2}-2p_u(w_\infty)-2p_u(v_0)
   \equiv\binom{k-2}{2}+1\pmod 2\).
   Independent machine check: part A2 of `verify_sign_head.py` verifies
   (8), (9), (10) — and (6) below — symbol by symbol on random Latin
   squares of orders 4, 6, 8 with designated dummy lines \(m,l,*\);
   the identities are *shape-level* (any Latin square of the augmented
   shape satisfies them), so this check is non-degenerate even though no
   radius-5 structure exists at those orders.

2. **Multiply over the \(k(k-1)\) flags.**  \(k(k-1)\) is even for every
   \(k\), so the constant \((-1)^{\binom{k-2}{2}+1}\) cancels and, by the
   definitions of \(E\) and \(H\),
   \[
    \prod_{i,u}\Sigma(Q^{i,u})\;=\;E(L,M)\cdot H(L,M,N).
   \]

3. **Equation (7)** of `flag_at_exact_formula.md` (from the universal
   Latin parity identity (6), \(\operatorname{AT}(Q)\Sigma(Q)
   =(-1)^{k(k-1)/2}\), again over the even number of flags):
   \[
    \prod_{i,u}\Sigma(Q^{i,u})=\prod_{i,u}\operatorname{AT}(Q^{i,u}).
   \]

4. **Equation (1) = certified formula (F)**
   (`flag_at_exact_formula.md`; `radius4_dual_trace_forced.md`;
   `collaboration/claude/flag_sign_reference_independence.md` and
   `audit_formula_F.py`):
   \(\prod_{i,u}\operatorname{AT}(Q^{i,u})=\mathrm{RHS}(F)\).

5. Chaining 2–4: \(E\cdot H=\mathrm{RHS}(F)\).  Since \(E\in\{\pm1\}\),
   division by \(E\) is multiplication by \(E\), giving (H). \(\square\)

End-to-end control on the **only decided parameter with a genuine
radius-5 structure**, \(k=2\): part A3 of the verifier builds the unique
\(k=2\) structure from the definitions and checks \(H=1\), \(E=1\)
(both empty products), \(\Sigma(Q^{0,u})=-1\) at both flags,
\(\operatorname{AT}(Q^{0,u})=+1\), \(\operatorname{AT}(T)=+1\),
\(\delta(S_0)=-1\), \(\mathrm{RHS}(F)=+1\), and identities (6), (7),
(1), (10), (H) all hold exactly.

Scope note: (H) is a **structural evaluation**, not an obstruction.  It
determines the global partial-fiber sign product from \(L,M\) alone in
any structure where the flag squares are Latin.  It says nothing about
whether such a structure exists at \(k=16\).

## 2. The E-lemma — PROVED (coordinator-audited): \(E(L,M)=+1\) always

**Lemma E.**  For every even \(k\) and every \((L,M)\) satisfying
radius-4 conditions 1–2 (only these are used), \(E(L,M)=+1\).

*Proof.*  Fix \(i\) and a finite colour \(x\), and put
\(v=L_i^{-1}(x)\).  The colour \(x\) is generic at \((i,u)\) exactly for
\(u\in V\setminus\{x,v\}\), which is precisely the support of the
\(x\)-class matching of \(M_i\) (condition 2), and then
\(v_M=\mathrm{mate}_x(u)\), \(v_L=v\).  The mate map is a fixed-point-free
involution of that support, so as \(u\) sweeps the support, so does
\(v_M\), each vertex once:
\[
 \prod_{u\in V\setminus\{x,v\}}\varepsilon(\mathrm{mate}_x(u),v)
 =\prod_{z\in V\setminus\{x,v\}}\varepsilon(z,v)
 =(-1)^{\,k-1-\mathrm{pos}(v)}\,\varepsilon(x,v),
\]
since the full product \(\prod_{z\ne v}\varepsilon(z,v)\) has exactly
\(k-1-\mathrm{pos}(v)\) negative factors and removing the factor
\(z=x\) multiplies by \(\varepsilon(x,v)\).  Multiplying over
\(x\in V\) (so \(v=L_i^{-1}(x)\) sweeps \(V\)):
\[
 \prod_{x}(-1)^{k-1-\mathrm{pos}(v)}=(-1)^{k(k-1)/2},
 \qquad
 \prod_{x}\varepsilon(x,L_i^{-1}(x))=\prod_{v}\varepsilon(L_i(v),v),
\]
so the per-\(i\) product is
\((-1)^{k(k-1)/2}\prod_v\varepsilon(L_i(v),v)\).  Finally, by condition
1, for fixed \(v\) the values \(L_i(v)\) sweep \(V\setminus\{v\}\) over
\(i\in A\), so
\(\prod_{i,v}\varepsilon(L_i(v),v)=\prod_v(-1)^{k-1-\mathrm{pos}(v)}
=(-1)^{k(k-1)/2}\).  Hence
\[
 E=(-1)^{k(k-1)/2\,(k-1)}\cdot(-1)^{k(k-1)/2}
 =(-1)^{k(k-1)/2\cdot k}=+1
\]
because \(k\cdot k(k-1)/2=(k/2)\,k(k-1)\) is even for even \(k\).
\(\square\)

Machine check (parts B2 and C of the verifier): all three proof steps
are verified numerically on the Wallis \(k=16\) chart and on 35 sampled
\(k=6\) charts; and every one of the 11,760 census charts of §4 has an
even number of negative generic pairs (in fact exactly 60 — see §4),
consistent with \(E=+1\).

**Corollary (H′).**  In every structure covered by Theorem (H),
\[
 H \;=\; \mathrm{RHS}(F)\;=\;(-1)^{k(k-1)/2}\operatorname{AT}(T)
 \prod_i\delta(S_i)\;=:\;H_{\mathrm{required}}(L,M).
\]
The name \(H_{\mathrm{required}}\) is used below for this
\((L,M)\)-computable value; it is never conflated with any observed
partial-fiber product on a synthetic table.

## 3. Wallis \(k=16\) recomputation — COMPUTATION

Independent code path (part B of the verifier; Wallis array embedded,
conditions 1–3 re-checked):

- generic hole pairs: **3,360** total (240 flags × 14 generic colours),
  of which **1,680** are negative — both exactly as expected; hence
  \(E=+1\) (and the E-lemma forces the parity).
- \(R(T)=+1\), \(C(T)=+1\), \(\operatorname{AT}(T)=+1\);
  \(\delta(S_i)\) over the 15 squares:
  \([1,-1,1,1,-1,1,1,1,-1,-1,-1,-1,-1,-1,1]\) — eight \(-1\)s, product
  \(+1\); \(\mathrm{RHS}(F)=+1\).
- **\(H_{\mathrm{required}}(\text{Wallis})=+1\)**: any radius-5
  structure on the Wallis chart (none is known) would have
  \(H=+1\).

## 4. Complete labelled \(k=6\) census — COMPUTATION (radius-3 controls; NOT radius-5 witnesses)

Part C of the verifier enumerates from scratch: 6,240 SILS(7); 1,680
labelled discordant 5-families (matching the certified census); every
family × every distinguished root colour = **11,760 charts**, each
re-checked against conditions 1–3.  Results:

- \(E=+1\) on **all 11,760** charts; the negative-generic-pair count is
  the constant **60** (of 120) on every chart.
- \(\mathrm{RHS}(F)=H_{\mathrm{required}}\) distribution:
  **\(-1\) on 6,720 charts, \(+1\) on 5,040 charts.**
- The per-uv layer (condition 4, all 15 edges) is feasible for **0** of
  the 11,760 charts — consistent with the certified k=6 radius-4
  obstruction; so none of these charts carries any actual \(N\)-table,
  and no actual \(H\) exists on them.
- \(k=4\) recheck: 6 SILS(5), max discordant set 1 < 3 — no radius-3
  chart at all.

**What this does and does not show.**  \(H_{\mathrm{required}}\) takes
both signs across radius-3 charts.  Therefore a hypothetical independent
theorem of the form "every genuine radius-5 structure has \(H=C\)" (a
universal constant) **would have exclusion power**: combined with (H′)
it would exclude every chart whose \(H_{\mathrm{required}}\ne C\) —
at \(k=6\), depending on \(C\), either 6,720 or 5,040 of the 11,760
charts (all of which are in fact already dead at radius 4).  The census
does **not** and cannot refute the existence of such a theorem: none of
these charts extends to radius 4/5, so no genuine \(H\) is realised on
them, and a theorem quantified over genuine radius-5 structures is not
constrained by them.  (This paragraph replaces an earlier invalid
inference; the correction is due to the coordinator.)

## 5. Fiber re-expressions of \(H\) — PROVED

Throughout, "cells" of the fiber \(\Phi_{i,u,x}\) are the pairs
\((j,v)\in(A\setminus\{i\})\times(V\setminus\{u\})\) with
\(N_{uv}(ij)=x\); rows and columns carry the induced (natural) orders.
For an arbitrary table \(N\) (no constraints at all) define
\[
 T(N)=\sum_{i,u,x}\#\{\text{misordered cell pairs of }\Phi_{i,u,x}\},
 \qquad
 \widehat H(N)=(-1)^{T(N)},
\]
where a pair of cells \((j,v),(j',v')\) is misordered iff
\((j-j')(v-v')<0\).

**Lemma R1 (inversion form).**  If every fiber is a partial matching
(true whenever condition 4 and the forced trace hold), then
\(\operatorname{sgn}\Phi_{i,u,x}=(-1)^{\#\text{misordered pairs}}\) and
hence \(H=\widehat H\).
*Proof.*  The sign of a bijection between ordered sets equals the parity
of the inversions of its cell set; part A0 of the verifier exhausts this
on all partial injections of rectangles up to \(4\times4\) (474
instances). \(\square\)

**Lemma R2 (per-uv regrouping).**  For any table,
\[
 T(N)=\sum_{u}\ \sum_{i}\ \sum_{\{v<v'\}\not\ni u}
 \#\{(j,j'):j\ne j',\ N_{uv}(ij)=N_{uv'}(ij'),\ j>j'\},
\]
i.e. \(T\) counts, for each vertex \(u\), index \(i\), and ordered column
pair \(v<v'\), the descents of the partial composition
\(\sigma_{i,u,v,v'} = (\text{colour-to-index match of }N_{uv'}\text{ at }i)
\circ(\text{index-to-colour map of }N_{uv}\text{ at }i)\).
*Proof.*  Every misordered cell pair lies in one fiber \((i,u,x)\) and
has distinct columns \(v\ne v'\) and distinct rows; group the pairs by
\((u,i,\{v,v'\})\); the common colour \(x\) is determined by the cells;
with \(v<v'\) fixed, misordered means the row at \(v\) exceeds the row
at \(v'\).  Part D of the verifier recomputes both sides independently
on random tables. \(\square\)

**Lemma R3 (per-ij regrouping).**  For any table satisfying the per-ij
trace (so that each colour class of each slice is a matching with
partner maps \(p^{ij}_x\)),
\[
 T(N)=\sum_{i}\ \sum_{x}\ \sum_{\{j<j'\}\subseteq A\setminus\{i\}}
 \#\{u: u\in\mathrm{supp}\,D_x^{ij}\cap\mathrm{supp}\,D_x^{ij'},\
 p^{ij}_x(u)>p^{ij'}_x(u)\},
\]
(the general-table version replaces partners by all incident
\(x\)-edges).  *Proof.*  Group the misordered pairs by the flag index
\(i\), the colour \(x\), and the two rows \(\{j,j'\}\); the flag vertex
\(u\) ranges over the common support; the cells are
\((j,p^{ij}_x(u))\) and \((j',p^{ij'}_x(u))\); with \(j<j'\) fixed,
misordered means \(p^{ij}_x(u)>p^{ij'}_x(u)\).  Machine check: part D.
\(\square\)

**Structural reading.**  R2 writes \(H\) as a second-order statistic of
the per-uv family — it couples *pairs of stars* \(N_{uv},N_{uv'}\)
sharing a vertex; R3 writes it as a second-order statistic of the
per-ij family — it couples *pairs of slices* \(D^{ij},D^{ij'}\) sharing
an index, colour by colour, along the union cycles of the two matchings.
Neither expression is a product of single-slice or single-star terms.
A single-fibering parity theorem would have to make these cross terms
cancel; §6 shows by exhibit that no such theorem exists.

On the union-cycle route specifically: for two matchings
\(D_x^{ij},D_x^{ij'}\), the R3 count
\(\#\{u:p^{ij}_x(u)>p^{ij'}_x(u)\}\) is **not** an invariant of the
union-cycle structure alone — explicit relabellings of a single
alternating 6-cycle realise both parities (count 3 for the natural
labelling \(12,34,56\ \cup\ 23,45,61\); count 2 for
\(13,26,45\ \cup\ 32,64,51\)), so no label-free per-cycle lemma can
evaluate it.  Only order-dependent global cancellations (of the
R\(_\tau\)-lemma kind, certified in
`flag_sign_reference_independence.md`) survive relabelling.  Beyond
R1–R3 no candidate lemma survived with a complete proof, and per
instructions none is stated without one.

## 6. One-sided falsification — COMPUTATION with PROVED-by-exhibit no-gos

One-sided tables *exist* as combinatorial objects (unlike the
nonexistent \(k=6\) radius-5 extensions), so the following inferences
are valid.  All tables below are stored in the JSONs and independently
re-verified by part E of the verifier (constraints + recomputation of
\(\widehat H\)).

**Per-ij-only tables** (each pair's slice satisfies the forced-trace
matching conditions; no cross condition):

| order | chart | \(H_{\mathrm{required}}\) | sampled | \(\widehat H=+1\) | \(\widehat H=-1\) | one-slice-swap counterexample |
|---|---|---|---|---|---|---|
| \(k=4\) | all 4 condition-1 charts | n/a (no \(M\)) | — | — | — | vacuous: 0 charts have feasible slices; every feasible finite class would be a forced single edge |
| \(k=6\) | census family 0, root 6 | \(-1\) | 300 | 157 | 143 | yes (`cex_base`/`cex_flip`, differ only in the \(\{0,1\}\) slice) |
| \(k=8\) | cyclic chart, root 8 | \(+1\) | 200 | 96 | 104 | yes |
| \(k=16\) | Wallis | \(+1\) | 12 | see JSON | see JSON | yes — found at the FIRST resampling of the \(\{0,1\}\) slice (base \(\widehat H=+1\), flip \(-1\)) |

**Per-uv-only tables** (every \(N_{uv}\) satisfies condition 4; no cross
condition):

| order | chart | \(H_{\mathrm{required}}\) | sampled | \(\widehat H=+1\) | \(\widehat H=-1\) | one-edge-recolour counterexample |
|---|---|---|---|---|---|---|
| \(k=6\) | any census chart | — | — | — | — | infeasible: 0 of 11,760 charts have a per-uv layer (§4) |
| \(k=8\) | cyclic chart, root 8 | \(+1\) | 200 | 84 | 116 | yes |
| \(k=16\) | Wallis | \(+1\) | 12 | see JSON | see JSON | yes — found at the FIRST recolouring of \(N_{01}\) (base \(\widehat H=-1\), flip \(+1\)) |

**No-go theorem N1 (per-ij; PROVED by exhibit).**  There is no theorem
of the form "for every table satisfying the per-ij trace constraints for
a chart \((L,M)\), \(\widehat H=f(L,M)\)": the two stored \(k=6\) tables
`cex_base`, `cex_flip` satisfy all per-ij constraints for the same
chart, differ in a single slice, and have opposite \(\widehat H\).
Hence the per-ij fibering alone cannot decide \(H\); any forced-value
proof must use cross-slice (per-uv) information.

**No-go theorem N2 (per-uv; PROVED by exhibit).**  Likewise with the
stored \(k=8\) (and \(k=16\)) per-uv counterexample pairs: condition 4
alone cannot decide \(H\); any forced-value proof must use cross-star
(per-ij) information.

Scope of N1/N2, stated precisely: they refute theorems whose hypotheses
are the one-sided axioms alone.  They do **not** refute a theorem whose
hypotheses include joint consistency (genuine two-sided tables); that
class is addressed in §7–§8 and remains the live question.

## 7. The joint layer at \(k=8\): a new solver-certified exclusion — COMPUTATION

A \(k=8\) radius-3 chart exists.  The starter construction behind the
Wallis \(G(17)\) works verbatim in \(\mathbb Z_9\): a translation-
invariant SILS(9) is exactly a starter (a partition of
\(\mathbb Z_9\setminus\{0\}\) into 4 pairs with distinct difference
classes), and two starter-developed squares are discordant iff the
starters are edge-disjoint.  \(\mathbb Z_9\) has exactly **9 starters**,
and exactly **one** 7-subset is pairwise disjoint: the cyclic chart
\(\{\{1,t{+}1\},\dots\}\) stored in `k8_charts.json`.  It passes
conditions 1–3; by the E-lemma and direct computation \(E=+1\), and
\(\mathrm{RHS}(F)=+1\) for **all 9 roots** (the translation
automorphism makes the roots equivalent), so
\(H_{\mathrm{required}}=+1\).

Findings for this chart (root 8; all roots equivalent):

- **per-uv layer feasible**: all 28 edges admit condition-4 colourings
  (200 full per-uv tables generated);
- **per-ij layer feasible**: all 21 slices admit trace decompositions
  (200 full per-ij tables generated);
- **the joint layer is INFEASIBLE**: condition 4 on all edges plus the
  forced trace on all pairs has no solution.  CP-SAT proves
  INFEASIBLE in under a second; an independent direct CNF encoding
  (2,268 vars, 17,922 clauses, `k8_joint_c0_r8.cnf`) is UNSAT by
  cadical (exit 20) with a DRAT proof emitted
  (`k8_joint_c0_r8.drat`; no DRAT checker is installed locally, so the
  proof file is stored unchecked — flagged, not certified).
- **Localisation** (`k8_scan.json`, `k8_subset_scan.json`): with
  condition 4 on all edges, the forced trace is satisfiable for any
  0, 1 or 2 index pairs tested (both 2-pair isomorphism types: sharing
  an index, and disjoint), and INFEASIBLE for **every 3-pair subset
  tested — all five isomorphism types**: star \((0,1),(0,2),(0,3)\),
  triangle \((0,1),(0,2),(1,2)\), path \((0,1),(1,2),(2,3)\),
  cherry + edge \((0,1),(0,2),(3,4)\), and even three disjoint pairs
  \((0,1),(2,3),(4,5)\).  Any two slices coexist with the full
  radius-4 layer; no tested three do.  (Solver results, 60 s caps,
  each INFEASIBLE returned in seconds; not an exhaustive run over all
  1,330 3-subsets.)

**Consequences, stated with exact scope.**

1. On this chart there are **no genuine two-sided tables at all**, so
   the hoped-for non-degenerate end-to-end control of (H) at \(k=8\)
   is vacuous; \(k=2\) remains the only genuine end-to-end control.
2. NEW structural fact: the trace × condition-4 **interaction** can
   kill a chart whose radius-4 per-edge layer is entirely feasible —
   at \(k=6\) death already occurs at condition 4, and at \(k=8\) it
   occurs strictly later, at the shared-\(N\) level.  This is exactly
   the shape of question that is open at \(k=16\) for the Wallis chart
   (radius-4 gate SAT; shared trace unresolved).
3. Caveat: this excludes only the **unique cyclic (starter-developed)**
   \(k=8\) chart (all roots; the joint UNSAT was re-run at root 0 and
   with a single-threaded solver, both INFEASIBLE).  Whether non-cyclic
   \(k=8\) charts exist is OPEN (two CP-SAT chart searches — square 0
   fixed to the cyclic SILS, 120 s, and a symmetry-broken search
   requiring at least one non-translation-invariant square, 900 s —
   both returned UNKNOWN);
   nothing at \(k=8\) transfers to \(k=16\) by itself — indeed §8 shows
   the same 3-slice configuration is FEASIBLE on the Wallis chart.

## 8. Strongest jointly-feasible relaxation at \(k=16\) — COMPUTATION

`gen_tables.py k16joint` imposes full condition 4 on all 120 Wallis
edges plus the forced trace on a prefix of index pairs, and samples
solutions.  Tables of this family satisfy strictly more than either
one-sided family; on them \(\widehat H\) is compared against
\(H_{\mathrm{required}}=+1\).  Results:

- trace on **1 pair** \((0,1)\): FEASIBLE; 2 sampled tables, both with
  \(\widehat H=+1\) (`joint_k16_pairs1.json`).
- trace on **3 pairs** \((0,1),(0,2),(0,3)\) — the exact configuration
  size and shape that kills the \(k=8\) cyclic chart: **FEASIBLE** at
  \(k=16\) Wallis; the \(k=8\) 3-slice death does not transfer.  Six
  sampled tables under this one constraint set have
  \(\widehat H=[-1,-1,+1,-1,-1,-1]\): **both signs occur inside the
  same partial-joint family** (`joint_k16_partial.json`; the earlier
  2-solution run is kept as `joint_k16_pairs3.json`), while
  \(H_{\mathrm{required}}=+1\).  **No contradiction with (H)**: (H)
  forces \(H=H_{\mathrm{required}}\) only when the trace holds for ALL
  pairs (all flag squares Latin); with 3 of 105 pairs constrained,
  \(\widehat H\) is not the (H)-governed quantity.  Conclusion of this
  escalation: even the strongest jointly-feasible relaxation we could
  construct and sample — full condition 4 plus a feasible trace
  fragment — still does not pin \(\widehat H\); the sign only becomes
  rigid at the full joint level, exactly where (H) already evaluates
  it.

## 9. Verdict, per the strict exclusion criteria

1. **(H) with the E-lemma is PROVED**: in every structure whose flag
   squares are Latin (in particular every unrestricted radius-5 ball),
   \(H=H_{\mathrm{required}}(L,M)=(-1)^{k(k-1)/2}\operatorname{AT}(T)
   \prod_i\delta(S_i)\).  It is a conditional structural evaluation,
   not an obstruction.
2. **No second evaluation from a single fibering exists**: PROVED by
   exhibit (N1, N2).  The sign head cannot be decided from the per-ij
   slices alone nor from the per-uv stars alone.
3. **A second evaluation from the joint structure remains OPEN.**  The
   only new leverage found is negative-existential: at \(k=8\) the
   joint layer itself is empty for the one existing cyclic chart
   (solver-certified), so there the question is vacuous.  At \(k=16\)
   nothing here forces any value of \(H\) beyond (H).
4. **Exclusion criteria**: a \(k=16\) exclusion would need an
   independent theorem forcing a value incompatible with (H) for
   EVERY admissible \((L,M)\); nothing above does this.  A failure on
   the Wallis chart alone would exclude only that chart; nothing above
   does this either.  The universal Latin identity is not an
   independent evaluation (it reproduces (1)); no claim of that kind is
   made.
5. **#835 remains open.**  No radius-5 ball at \(k=16\) is constructed
   or excluded here.

## 10. Reproduce

```sh
# everything stdlib + deterministic; ~2 min with the census
python3 -B verify_sign_head.py            # parts A-E
# generators (OR-Tools CP-SAT; cadical for the k=8 UNSAT):
python3 -B gen_tables.py k4check | k6perij | k8chart | k8joint | k8scan \
                        | k8peruv | k8perij | k8cnf | k16perij | k16peruv \
                        | k16joint
/opt/homebrew/bin/cadical k8_joint_c0_r8.cnf k8_joint_c0_r8.drat  # exit 20
```

Raw results: `k6_census.json`, `k8_charts.json`, `k8_scan.json`,
`k8_subset_scan.json`, `falsify_k6_perij.json`, `falsify_k8_perij.json`,
`falsify_k8_peruv.json`, `falsify_k16_perij.json`,
`falsify_k16_peruv.json`, `joint_k8_trace_cond4.json`,
`joint_k16_pairs1.json`, `joint_k16_pairs3.json`,
`joint_k16_partial.json`, `k8_joint_c0_r8.cnf`, `k8_joint_c0_r8.drat`
(DRAT emitted by cadical, no checker installed locally — stored
unchecked), plus `k8_noncyclic_search.py`/`.log` (UNKNOWN) and
`hunt_cex_k16.py`.  Every stored table is independently re-verified by
part E of the stdlib verifier.

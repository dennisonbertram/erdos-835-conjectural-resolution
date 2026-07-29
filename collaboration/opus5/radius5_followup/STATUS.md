# Unrestricted radius-5 follow-up: census, a k=6 obstruction, and a lemma audit

**Scope, stated first.** Erdős–Rosenfeld #835 remains **open**. Nothing here is
a global construction or an unrestricted theorem at \(k=16\). Everything below
is about the *unrestricted* local ball model of \(O_k\) — no cyclic, GF(16) or
Wallis ansatz — except §3, which audits a lemma using Wallis only as a witness.

Verifier (stdlib only, no solver, self-contained — the Wallis array is
embedded, nothing under `evidence/` is imported or modified):

```sh
python3 -B collaboration/opus5/radius5_followup/verify_radius3_census_and_k6_obstruction.py
python3 -B collaboration/opus5/radius5_followup/verify_radius3_census_and_k6_obstruction.py --quick
```

Every non-existence claim below is an exhaustive enumeration that terminates.
No unbounded solver was launched.

---

## 0. Prior art, credited

Two statements I re-derived turn out to be already recorded, so they are **not**
claimed as new:

* The radius-3 ball data \((L,M)\) is exactly a family of 15 symmetric
  idempotent Latin squares of order 17, pairwise disagreeing in every
  off-diagonal cell — `evidence/odd_graph_local_ball/lmn_large_set.md`
  (lines 1, 13–26, and the \(K_{18}\) one-factorization form at 60–73).
* Given \(L\) and \(M\), the 120 radius-4 subproblems (one per edge \(uv\) of
  \(K_V\)) are **mutually independent** —
  `evidence/global_latin_compatibility.md:211`.

What is new here: the small-order **census** of those families (§1), the
**complete finite obstruction at \(k=6\)** with its mechanism (§2), and the
independent **audit** of the minimal-trace lemma (§3). The hole-profile
statement in §2 is recorded in the repo only for the cyclic case
(`cyclic17_vertex_degree_structure.md`), not unrestrictedly.

---

## 1. The unrestricted radius-3 census (new)

For general \(k\), write \(|A|=k-1\), \(|V|=k\), \(\mathcal C=V\sqcup\{\infty\}\)
so \(|\mathcal C|=k+1\). The radius-3 ball needs \(k-1\) symmetric idempotent
Latin squares of order \(n=k+1\), pairwise discordant off the diagonal.

| \(k\) | \(n=k+1\) | symmetric idempotent LS of order \(n\) | max discordant family | need \(k-1\) | radius-3 ball |
|---|---|---|---|---|---|
| 2 | 3 | 1 | 1 | 1 | **exists** |
| 4 | 5 | 6 | **1** | 3 | **impossible** |
| 6 | 7 | 6,240 | 5 | 5 | exists |

> **Proposition 1.** The unrestricted radius-3 ball of \(O_4\) does not exist.
> Of the six symmetric idempotent Latin squares of order 5, no two are
> discordant, so a discordant family has size 1, while 3 are required.

**Controls.** \(k=2\), where a tight colouring genuinely exists, is *not*
obstructed — the test correctly does not fire. \(k=4\), where no tight colouring
exists, is killed outright, with **no ansatz of any kind**. This is a stronger
statement than the cyclic layer-1 census: that one assumed \(\mathbb Z_p\)
translation equivariance, this one assumes nothing.

---

## 2. \(k=6\): a complete finite obstruction at radius 4 (new)

At \(k=6\) the radius-3 ball exists, so the control must fire later. It does,
at radius 4, and completely.

Given \(L,M\), the radius-4 subproblem at a pair \(uv\) asks for a proper edge
colouring of \(K_{A}\) (\(k-1\) vertices) with the \(k+1\) colours of
\(\mathcal C\), in which vertex \(i\) misses exactly
\(H_i=\{M_i(uv),L_i(u),L_i(v)\}\).

**Hole profile (unrestricted).** Put \(B_c=\{i: c\in H_i\}\). The three index
sets \(\{i:M_i(uv)=c\}\), \(\{i:L_i(u)=c\}\), \(\{i:L_i(v)=c\}\) are pairwise
disjoint (an index in two of them would force \(M_i(uv)=L_i(u)\) or
\(L_i(u)=L_i(v)\), both excluded), and each is a singleton or empty by
conditions 1 and 3 of `radius4_reduction.md`. Hence
\[
 |B_c|=1 \text{ for } c\in\{\infty,u,v\},\qquad |B_c|=3 \text{ otherwise},
\]
so \(\sum_c|B_c|=3+3(k-2)=3(k-1)\) ✓. The verifier asserts this profile on
every subproblem it builds.

> **Proposition 2.** At \(k=6\) there are exactly **1,680** discordant radius-3
> families, and **none** of them extends to radius 4 — for any of the 7 choices
> of which colour is the root colour \(\infty\). Zero survivors.

> **Proposition 3 (mechanism).** Every infeasible radius-4 subproblem at
> \(k=6\) is infeasible for one reason: a colour \(c\) with \(|B_c|=3\) has its
> class equal to a perfect matching of \(A\setminus B_c\), which has
> \(|A|-3=k-4\) vertices. At \(k=6\) that is **exactly 2 vertices, i.e. one
> forced edge**. Two distinct triple-hole colours with the same \(B_c\) force
> the same edge twice, and colour classes must be edge-disjoint.

Over all 1,680 families and all root-colour choices — 176,400 subproblems —
45,360 are infeasible and **every single one** is a forced-edge collision;
**zero** are infeasible for any other reason.

**Scope, explicitly.** At \(k=16\), \(|A|-3=12\), so a triple-hole class is a
perfect matching on 12 vertices and nothing is forced. **This mechanism does
not transfer to \(k=16\).** Proposition 3 validates the pipeline and explains
\(k=6\); it is not progress on \(k=16\).

---

## 3. Audit of the "minimal trace is forced" lemma — **CONFIRMED**

The coordinator's lemma is **correct**. I re-derived it independently and
checked every ingredient at \(k=16\) against the Wallis family.

*Derivation.* For fixed \(ij\) and colour \(x\), the three events
\(N_{uv}(ij)=x\), \(M_i(uv)=x\), \(M_j(uv)=x\) are mutually exclusive
(condition 4 gives \(N_{uv}(ij)\notin\{M_i(uv),M_j(uv)\}\); condition 3 gives
\(M_i(uv)\ne M_j(uv)\)). So
\(\deg_{H}(u)=\deg_{D_x}(u)+a_{i,x}(u)+a_{j,x}(u)\), and evenness of
\(\deg_{G_{ij,x}}(u)=k-1-\deg_H(u)\) gives condition (3).

Verified ingredients (all `ok`):

* \(a_{i,\infty}(u)=1\) for every \(u\) — the \(\infty\)-class of \(M_i\) is a
  perfect matching of \(V\);
* \(a_{i,x}(u)=0\) exactly on \(\{x,L_i^{-1}(x)\}\) for finite \(x\);
* \(L_i^{-1}(x)\ne x\) (each \(L_i\) is a derangement) and
  \(L_i^{-1}(x)\ne L_j^{-1}(x)\) for \(i\ne j\) (condition 1 makes
  \(i\mapsto L_i(u)\) injective) — so the two exceptional vertices are distinct;
* odd-degree vertex counts in \(D_x\): **16** for \(x=\infty\), **14** for each
  finite \(x\), exactly as claimed;
* \(8+16\cdot7=120=|E(K_{16})|\), so the lower bounds are tight and **equality
  is forced**: \(D_\infty\) is a perfect matching of \(V\), and \(D_x\) is a
  perfect matching of \(V\setminus\{L_i^{-1}(x),L_j^{-1}(x)\}\).

Two consequences I add:

* **The mod-3 filter (2) of `radius5_reduction.md` becomes redundant.** It reads
  \(t_\infty\equiv2\), \(t_x\equiv1 \pmod 3\); the forced values are \(8\) and
  \(7\), and \(8\equiv2\), \(7\equiv1\). So (2) is implied by the equality and
  adds nothing once the lemma is known.
* **Triple-count cross-check.** \(|E(G_{ij,\infty})|=120-3\cdot8=96\) (32
  triangles) and \(|E(G_{ij,x})|=120-3\cdot7=99\) (33 triangles), giving
  \(32+16\cdot33=560=\binom{16}{3}\) ✓.

### The one gap, reported as required

The parity input comes from "\(G_{ij,x}\) is triangle-decomposable", which
**presupposes that a radius-5 extension exists**. So the correct statement is:

> the minimal trace is forced for any radius-4 colouring **that extends to
> radius 5** — it is *not* forced by the radius-4 data alone.

That is still enough for the intended use: it upgrades the "minimal-trace
ansatz" of `radius5_large_set_equivalence.md` §1 to a theorem *within the
radius-5 problem*, so the prescribed-link \(LS(2,3,19)\) equivalence in §2 of
that note holds unconditionally for any radius-5 ball. Any wording that says
the trace is forced by radius-4 data, or that drops the extension hypothesis,
would be an overclaim.

---

## 4. What this does and does not give

* **Does**: an unrestricted, ansatz-free obstruction that kills \(k=4\) at
  radius 3 and \(k=6\) at radius 4, with the \(k=2\) control correctly silent.
  A validated pipeline, and a confirmed lemma with its scope pinned.
* **Does not**: shrink the \(k=16\) model, supply a new \(k=16\) invariant, or
  give a construction. The \(k=6\) mechanism provably does not transfer. I did
  **not** find a lossless reduction beyond the two already-recorded ones, nor a
  construction mechanism.

**Erdős–Rosenfeld #835 remains open.**

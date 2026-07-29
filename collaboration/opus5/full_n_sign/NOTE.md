# The infinity-layer sign: a theorem, and what is still open

**Scope, first.** Nothing here constructs or refutes anything about
Erdős–Rosenfeld #835, which remains **open**. Four levels are kept sharply
separate throughout and are never conflated:

| level | what it is | do we have one? |
|---|---|---|
| synthetic layer | a two-sided model of the ∞-layer constraints alone | yes, at k = 4, 6, 16 |
| full shared \(N\) | all \(k+1\) layers, jointly compatible | **no**, at any \(k>2\) |
| radius-five ball | a genuine \((L,M,N)\) | **no**, at any \(k>2\) |
| global colouring | a tight \((k+1)\)-colouring of \(J(2k,k)\) | **no**, at \(k>2\) |

`H_observed` (the actual partial-fiber sign product, existing only on a genuine
radius-5 structure) and `H_required` (what identity (H) forces if a chart
extends) are never used interchangeably.

> **Subsequent independent result.**  This Opus 5 report is retained as an
> external audit record.  The same-day proof in
> [`../../global_h_parity/README.md`](../../global_h_parity/README.md) settles
> the subquestions left open below: it proves
> \(H_\infty=\rho(\Psi)=P(\Psi)\), evaluates every finite layer, and proves
> that the product of all layer equations is identically the already-known
> flag formula \(F(L,M)\).  Thus the statements below calling \(\rho\)
> conjectural or the finite layers untouched are historical, not the current
> repository status.  The unrestricted construction problem remains open.

Verifier: `collaboration/opus5/full_n_sign/verify_full_n_sign.py`
(stdlib only, assertion-enabled, no solver).

---

## 1. PROVED — a closed formula for \(H_\infty\)

Fix even \(k\), a one-factorization \(\Psi\) of \(K_V\) indexed by \(A\), and a
two-sided compatible family \(\{D^{ij}\}\). Write \(P(i,j,u)\) for the
\(D^{ij}\)-partner of \(u\), so \(\Phi_{i,u}(j)=P(i,j,u)\).

**Step 1 (the completion).** For fixed \(i\) the array
\(\Theta_i(j,u)=P(i,j,u)\), rows \(A\setminus\{i\}\) and columns \(V\), has
every row a fixed-point-free involution of \(V\), and every column \(u\)
containing exactly \(V\setminus\{u,\Psi_i(u)\}\). Adjoining the two rows
\(e=\mathrm{id}\) and \(f=\Psi_i\) therefore completes it to a genuine
\(k\times k\) **Latin square** \(L^{(i)}\).

**Step 2 (cofactors).** Deleting row \(f\) (image \(\Psi_i(u)\)) and then row
\(e\) (image \(u\)) from column \(u\) gives
\[
 \operatorname{sgn}\Phi_{i,u}
 =(-1)^{1+\operatorname{pos}(u)+\operatorname{pos}(\Psi_i(u))+[\Psi_i(u)<u]}
   \operatorname{sgn}(\text{col }u).
\]
Summing the exponent over \(u\): \(\sum_u 1=k\equiv0\);
\(\sum_u\operatorname{pos}(u)=\sum_u\operatorname{pos}(\Psi_i(u))=k(k-1)/2\);
and \(\sum_u[\Psi_i(u)<u]=k/2\) because \(\Psi_i\) is a fixed-point-free
involution. Hence
\(\prod_u\operatorname{sgn}\Phi_{i,u}=(-1)^{k/2}\,C(L^{(i)})\).

**Step 3 (row signs).** Every row of \(L^{(i)}\) except \(e\) is a
fixed-point-free involution, of sign \((-1)^{k/2}\), so
\(R(L^{(i)})=(-1)^{(k/2)(k-1)}\) and \(C=\operatorname{AT}\cdot R\).

**Step 4.** Multiplying over \(i\), the accumulated constant is
\((-1)^{k^2(k-1)/2}\), and \(k^2(k-1)/2=(k/2)k(k-1)\) is even. Therefore

\[
\boxed{\;H_\infty=\prod_{i\in A}\operatorname{AT}\bigl(L^{(i)}\bigr).\;}
\]

Since \(k\) is even, each \(\operatorname{AT}(L^{(i)})\) is
reference-independent, so \(H_\infty\) is **intrinsic** — no induced-order
convention survives. Verified against the direct definition on every model
found at \(k=4\) and \(k=6\).

This answers Priority 1 in the affirmative: the general formula exists and is
proved, for arbitrary even \(k\), arbitrary \(\Psi\), and every two-sided
compatible \(D\). It was **not** inferred from the \(k=4,6\) census; the census
is used only as a check.

---

## 2. RETRACTION, and the corrected statement

### 2.1 The conjecture \(H_\infty=(-1)^{k/2}\) is FALSE — withdrawn

The second pass conjectured \(H_\infty=(-1)^{k/2}\) from \(k=4,6\) plus a
capped \(k=8\) sample. **That conjecture is false and is withdrawn**, together
with the \(k=8\) evidence, which was worthless for two independent reasons
(both mine): the parity classifier was the product of factor signs, and every
factor of \(K_8\) is four transpositions, hence even — so it separated
nothing; and the model search was capped at 6 per \(\Psi\).

Independently reproduced refutation at \(k=16\). Both examples are the same
construction: take any Steiner triple system \(m\) on \(A\) and set
\(D^{ij}=\Psi_{m(ij)}\). This is automatically two-sided compatible, because
\(\{ij:uv\in D^{ij}\}\) is the link of \(\Psi(uv)\) in \(m\), and the link of a
point of an STS is a perfect matching of the remaining points. Both STS(15)
links were verified directly.

| \(\Psi\) | STS(15) | \(H_\infty\) |
|---|---|---|
| XOR, \(\Psi(uv)=u+v\) on \(\mathbb F_2^4\) | projective | \(+1\) |
| XOR | Bose | \(+1\) |
| round-robin | projective | \(-1\) |
| round-robin | Bose | \(-1\) |

Since \((-1)^{16/2}=+1\), the round-robin rows refute the conjecture.

### 2.2 What the data supports instead

* **\(H_\infty\) does not depend on \(D\).** Two non-isomorphic STS(15) give
  the same value for each \(\Psi\); and at \(k=6\) all seven two-sided
  families agree, for every one of the 720 labelled \(\Psi\).
* **\(H_\infty\) does depend on \(\Psi\).** \(+1\) versus \(-1\) above.
* So \(H_\infty=\rho(\Psi)\) for some one-factorization invariant \(\rho\).
  **CONJECTURE, not proved here**, and \(\rho\) is not identified.

### 2.3 Reconciliation with the proved formula

There is no conflict. \(H_\infty=\prod_i\operatorname{AT}(L^{(i)})\) is proved
and stands; §2.2 refines it by asserting that this product is constant in
\(D\). The earlier \(k=4,6\) census is also consistent with \(\rho(\Psi)\)
rather than with \((-1)^{k/2}\): \(K_4\) and \(K_6\) each have a **unique**
one-factorization up to isomorphism, so those parameters cannot exhibit any
\(\Psi\)-dependence at all. The apparent fit was a two-point coincidence on
parameters that were structurally incapable of refuting it. \(K_{16}\) has many
non-isomorphic one-factorizations, which is exactly why the refutation appears
there.

## 3. OPEN — Priorities 3, 4, 5

* **Priority 3 (finite layers).** Not done. The corner-regrouping of §1 uses
  the ∞-layer's degeneracy: its per-\(ij\) holes vanish and its per-\(uv\) hole
  is a single point, which is exactly what makes the two adjoined rows
  \(e,f\) canonical. A finite colour \(x\) has one- or three-index holes on one
  side and zero- or two-vertex holes on the other, so \(\Theta_i\) is no longer
  a Latin rectangle with a canonical two-row completion, and the argument does
  not transfer unchanged. No exact product over all \(k+1\) colours is claimed.
* **Priority 4 (root-colour coupling).** The previous pass reported the
  *negative* observation that \(H_{\rm required}\) varies with the root colour
  at \(k=6\) (in all 1680 charts, 4 of 7 roots give \(-1\)) while Wallis at
  \(k=16\) is constant \(+1\). As requested, that is **not** accepted as proof
  that no coupling exists: an explicit transformation law for the
  independently evaluated layer product under change of root is still missing,
  and is not supplied here.
* **Priority 5.** `collaboration/global_h_parity/` was not cross-checked; it
  was not present at the time of this pass.

---

## 4. What would follow, and what does not

If \(\rho(\Psi)\) were identified and proved, and if the analogous finite-layer
products were also forced, then \(H_{\rm observed}=\prod_x H_x\) would be an
**independent** evaluation. Combined with the already-proved
\[
 H_{\rm observed}=(-1)^{k(k-1)/2}\operatorname{AT}(T)\prod_i\delta(S_i),
\]
that would become a necessary condition on the radius-3 chart, and any chart
failing it could not extend. At \(k=16\) Wallis has
\(\operatorname{AT}(T)\prod_i\delta(S_i)=+1\), so only a forced value of
\(-1\) would exclude it. Note that \(\rho\) now genuinely varies with
\(\Psi\) at \(k=16\), so any such condition would be a constraint coupling
\(\Psi\) to the rest of the chart, not a single global sign.

**None of that is established.** One layer of \(k+1\) has a proved closed
form; its value is a conjectural function of \(\Psi\), unidentified; the
finite layers are untouched. No \(k=16\) chart is excluded, Wallis or
otherwise, and excluding \(k=16\) would in any case leave the other prime
cases open.

**Erdős–Rosenfeld #835 remains open** — no unrestricted construction, no
unrestricted contradiction.

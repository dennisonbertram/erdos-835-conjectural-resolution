# Post-spectrum / kernel synthesis: what was and was not obtained

## Answer up front

**\(k=16\) is NOT settled. Erdős–Rosenfeld #835 is NOT settled.** No
contradiction and no construction. The deliverables are one proved implication
(§4), one rederivation (§1), exact moment data that tests only coarse necessary
bounds (§3), and one standalone derived-layer computation (§4).

Verifiers (stdlib, exact integer arithmetic, no solver):

| file | content |
|---|---|
| `verify_spectrum_moments.py` | §1–§3 |
| `verify_derived_capacity_control.py` | §4 |

---

## 1. REDERIVATION (not new) — \(R\) is triangle-free for even \(k\ge6\)

**This is not a new result.** The triangle-monodromy note already records that
\(R\) has odd girth at least 11 at \(k=16\), which gives triangle-freeness
immediately, and that odd-girth bound is itself automatic from the fibre's
set-intersection geometry rather than a cover-specific obstruction.

The second derivation, recorded only because it is what makes
\(\operatorname{tr}(R^3)=0\) usable in §3: from
\(R^2=\binom k2I+5A_{k-3}+Q\) with \(\operatorname{supp}Q\subseteq A_{k-4}\),
\((R^2)_{BC}=0\) unless \(|B\cap C|\in\{k,k-3,k-4\}\); a triangle needs
\((R^2)_{BC}>0\) together with \(|B\cap C|=1\), and \(k-4\ge2>1\). The \(k=4\)
boundary is respected: there \(k-3=1\) and the argument does not apply.

## 2. EXACT COMPUTATION — the \(k=6\) control

With \(n=66\), \(\deg=15\), spectrum \(15^1,(-7)^{10},2^{44},(-3)^{11}\):
\(\operatorname{tr}R=0\), \(\operatorname{tr}R^2=990=n\deg\),
\(\operatorname{tr}R^3=0\). All three hold exactly, validating the
normalisations and the triangle-free statement of §1.

## 3. EXACT COMPUTATION — forced moments, and precisely what they do not show

From \(\operatorname{Spec}(R)=\{120^1,(-97)^{30},77^{434}\}\uplus\Lambda\) with
\(\operatorname{tr}R=0\), \(\operatorname{tr}R^2=120n\),
\(\operatorname{tr}R^3=0\), the residual moments are forced:

| quantity | value |
|---|---|
| \(|\Lambda|\) | 17,678,370 |
| \(\sum_\Lambda\lambda\) | \(-30{,}628\) |
| \(\sum_\Lambda\lambda^2\) | 2,118,590,344 |
| \(\sum_\Lambda\lambda^3\) | \(-172{,}483{,}132\) |

Tested against \(\Lambda\subseteq[-83,82]\): \(|\sum\lambda^3|\le83\sum\lambda^2\)
holds with slack factor 1019; and
\(\operatorname{tr}R^4=n\deg^2+25n|A_{13}|+\sum_Bs_B\) with
\(s_B=\sum_CQ_{BC}^2\in[10{,}080,\,30{,}240]\) puts
\(\sum_\Lambda\lambda^4\in[7.859\times10^{11},\,1.142\times10^{12}]\), inside the
power-mean floor \(2.539\times10^{11}\) and the cap \(8.390\times10^{14}\).

> **What this is.** A few **coarse necessary inequalities whose feasible ranges
> overlap.** That is the whole content.
>
> **What this is not.** No residual spectrum \(\Lambda\) is constructed; no
> \(Q\) with entries in \(\{0,1,2,3\}\) realising these values is exhibited; no
> algebraic-integer, multiplicity, or Krein condition is imposed. Overlap of
> coarse bounds is **not** consistency of the frontier, and **nothing here is
> exhausted.** Earlier phrasing to that effect is withdrawn.

## 4. Derived layer: one exact computation, and one proved implication

**EXACT COMPUTATION.** The derived layer of a \(k=6\) colouring is an
\(LS(2,3,9)\). Built from the 840 labelled \(STS(9)\): seven pairwise disjoint
systems partitioning all 84 triples, every 2-star verified rainbow. Deleting one
system gives \(M_{D'}\) of size \(36\times72\), rank\(_{\mathbb F_7}=36\); and
\(U'=\langle g,\dots,g^{\circ5}\rangle\) is verified to have dimension
\(5=p-2\), to lie in \(\ker M_{D'}\), and to satisfy
\(M_{D'}(u_r\circ u_s)=-\mathbf1\) iff \(r+s=p-1\), else \(0\) — the
nondegenerate anti-diagonal Gram.

> **Scope of that computation.** It shows only that the **degree-two capacity
> bound cannot exclude this one standalone derived large set.** It does **not**
> show that the descent cannot close \(k=6\), and it does **not** show that no
> higher-degree or cross-layer compatibility obstruction is visible at that
> layer — neither was tested.

**PROVED implication.** A uniform degree-two capacity bound below \(p-2\) at a
derived layer implies, by the deleted-colour theorem, that **no large set
exists at that layer** (a member of one would extend, and the theorem would
produce the \((p-2)\)-space).

At \(k=16\): a uniform degree-two capacity bound below 15 at the
\(LS(4,5,21)\) layer **would prove that no \(LS(4,5,21)\) exists.** Whether
\(LS(4,5,21)\) exists is itself **open**. No comparison of difficulty between
the two is claimed.

Direction matters: capacity \(\ge15\) does **not** imply the large set exists,
since degree two is only a relaxation of the full degree-\((p-1)\) hierarchy.

## 5. The two frontiers have **distinct** missing steps

They do not reduce to one another, and were wrongly merged in an earlier draft.

* **Frontier 1 (spectrum).** Missing: a condition beyond the low moments —
  Krein/Schur positivity on the forced \(-97\) and \(77\) modules, integrality
  or multiplicity constraints on \(\Lambda\), or control of the *fine
  distribution* of \(Q\) rather than its row sum. §3 shows the coarse moment
  layer does not supply it.
* **Frontier 2 (kernel/frames).** Missing: a uniform degree-two capacity bound,
  which by §4 is entangled with the existence question for \(LS(4,5,21)\). The
  target here is a statement about *gluing* the \(I+J\) simplex frames across
  shared evaluations.

## 6. Two open implications, not one

The \(k=4\) collapse has a specific mechanism: the only isotropic lines in
\(\ker M_D\) are the design indicators \(h_C=\mathbf1+\mathbf1_C\), **and** no
two are compatible, since
\(M_D(h_C\circ h_E)=\mathbf1+M_D\mathbf1_{C\cap E}\) is nonconstant. Reaching a
capacity cap at \(k=16\) needs **both** of the following, and **both are open**:

1. **(open)** every isotropic vector at \(k=16\) is a design indicator;
2. **(open)** the resulting design indicators are **pairwise incompatible,
   uniformly** over all \(k=16\) zero classes.

Implication 1 alone does **not** cap the capacity at 1. An earlier draft
asserted that it would; that is withdrawn.

## 7. Scope

* **PROVED:** the derived-layer implication (§4).
* **REDERIVED, not new:** triangle-freeness (§1).
* **EXACT COMPUTATION:** the \(k=6\) spectral control (§2); the forced moments
  and the overlap of coarse bounds (§3); the \(LS(2,3,9)\) realization (§4).
* **OPEN:** everything at \(k=16\), including both implications in §6.
* Not used, per instruction: the vacuous complement/clique corollary and the
  refuted \(\dim\ker M_D=|D|/2\) guess.

**\(k=16\) is not settled. Erdős–Rosenfeld #835 is not settled.**

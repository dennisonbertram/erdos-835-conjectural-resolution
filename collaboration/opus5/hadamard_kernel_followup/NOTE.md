# Deleted-colour Hadamard kernel: audit, frame reformulation, and the exact gap

## Outcome, stated first

The deleted-colour theorem **is sound**, including its higher-degree converse;
I found no error. I did **not** obtain the preferred outcome (an unrestricted
contradiction at \(k=16\)). What is delivered: a full independent audit, **one**
new proved corollary (the frame reformulation, §2), one corollary that turned
out to be **vacuous** (§3), one **refuted** guess (§4), and a precise statement
of the remaining gap. **Erdős–Rosenfeld #835 remains open.**

Verifier: `verify_frame_and_clique.py` (stdlib only, no solver, assertion-enabled).

---

## 1. PROVED — audit of the deleted-colour theorem: SOUND

Re-derived independently, not read off the source note.

* **(1)** For a tight colouring every \((k-1)\)-star carries each field value
  once, so \(\sum_{S\supset B}g(S)^m=\sum_{z\in\mathbb F_p}z^m\), which is \(0\)
  for \(1\le m\le p-2\) and \(-1\) for \(m=p-1\). ✓
* **Converse.** Newton gives \(e_1=\dots=e_{p-2}=0\) (each step divides by
  \(m\not\equiv0\)) and \(e_{p-1}=-1\), so the star polynomial is
  \(T^p-T-e_p\). Since \(T^p-T\) vanishes identically on \(\mathbb F_p\), that
  polynomial has a root in \(\mathbb F_p\) **iff** \(e_p=0\); the roots are the
  \(g(S)\in\mathbb F_p\), so \(e_p=0\) and the star is a permutation. ✓
* **Independence of \(u_r=g^{\circ r}\).** \(g(X\setminus D)=\mathbb F_p^\ast\),
  so \(\sum c_rz^r\) vanishing there and at \(0\) is a degree-\(\le p-2\)
  polynomial with \(p\) roots, hence zero. \(\dim U=p-2\). ✓
* **\(U\le\ker M_D\)**: \(M_Du_r=W(g^{\circ r})=0\), the \(D\)-columns
  contributing \(0\) since \(g\) vanishes there and \(r\ge1\). ✓
* **(6)**: \(M_D(u_r\circ u_s)=\sum_{z}z^{r+s}\), which is \(-1\) exactly when
  \((p-1)\mid(r+s)\). With \(2\le r+s\le 2p-4\) the only multiple in range is
  \(p-1\), so \(b\) is the anti-diagonal \(-1\) matrix: **nondegenerate**. ✓
* **Higher-degree converse (8)**: taking \(x\in U\) with \(\rho_B(x)\) equal to
  \(\mathbb F_p^\ast\) forces every deleted star to have power sums
  \(0,\dots,0,-1\) over \(p-1\) values, so by Newton \(e_1=\dots=e_{p-2}=0\),
  \(e_{p-1}=-1\) and the star polynomial is \(T^{p-1}-1=\prod_{z\ne0}(T-z)\).
  Adding the unique \(D\)-block of value \(0\) gives a tight colouring. ✓

**Counts, all verified.** \(|D|=\binom{2k}{k}/p\);
\(|X\setminus D|=\binom{2k}{k}\frac{p-1}{p}=\binom{2k}{k-1}=|Y|\), so
**\(M_D\) is square**; and Wilson's rank formula gives
\(\operatorname{rank}_pW_{k-1,k}(2k)=\sum_{i\le k-1}\bigl[\binom{2k}{i}-\binom{2k}{i-1}\bigr]=\binom{2k}{k-1}\)
— **full row rank** — because the divisibility condition is
\(p\nmid\binom{k-i}{k-1-i}=k-i\) and \(1\le k-i\le k<p\) always.

**One wording imprecision** (not an error): the converse says "one (hence
every) \(\rho_B\) injective". The "hence every" is true *a posteriori* but is
not needed as a hypothesis — the argument only uses surjectivity of a single
\(\rho_B\).

## 2. PROVED — frame reformulation

Since \(b\) is nondegenerate, define \(v_S\in U\) by \(b(v_S,x)=x(S)\). Then
condition (5) says exactly that each \(\rho_B\) is an **isometry onto**
\(H_0=\mathbf1^\perp\subset\mathbb F_p^{p-1}\); transporting \(e_i\mapsto e_i+\mathbf1\)
gives the equivalent system

* \(b(v_S,v_S)=2\);
* \(b(v_S,v_{S'})=1\) whenever \(|S\cap S'|=k-1\), i.e. whenever \(S,S'\) are
  **adjacent in the Johnson graph** \(J(2k,k)\);
* \(\sum_{S\supset B,\,S\notin D}v_S=0\) for every \(B\in Y\).

(The Gram \(I+J\) of a deleted star, eq. (7) of the source note, is exactly
\((e_i+\mathbf1)\cdot(e_j+\mathbf1)=\delta_{ij}+1\), and its kernel \(\mathbf1\)
gives the star-sum relation.) Nothing is prescribed on non-adjacent pairs.

## 3. Clique corollary — PROVED but **VACUOUS** (corrected)

\(\operatorname{rank}_p(I+J_m)=m\) unless \(m\equiv-1\pmod p\), when it is
\(m-1\). A clique \(T\subseteq X\setminus D\) has Gram \(I+J_{|T|}\) inside
\(U\), so \(|T|=p\) is forbidden and \(|T|=p-1\) exactly saturates. Maximal
cliques of \(J(2k,k)\) have size \(p\) and are stars of \((k-1)\)-sets or
\(k\)-subsets of \((k+1)\)-sets; stars meet \(D\) by the Steiner property, so
every \((k+1)\)-set must contain a \(D\)-block, and the count
\(|D|(2k-k)=\binom{2k}{k+1}\) makes it exactly one — i.e. \(D^{c}\) is an
\(S(k-1,k,2k)\).

> **This conclusion is automatic and therefore imposes no constraint.** The
> complement of a \(t\)-design is always a \(t\)-design, and here the constant
> is 1: the number of blocks of an \(S(k-1,k,2k)\) disjoint from a
> \((k-1)\)-set is
> \(N=\sum_j(-1)^j\binom{k-1}{j}\lambda_j\) with
> \(\lambda_j=\binom{2k-j}{k-1-j}/(k-j)\), and \(N=1\) for every \(k\)
> (verified for \(k=2,4,6,10,16,22\)).

So \(D^c\) is a Steiner system for **every** such \(D\), with no reference to a
colouring. The clique argument is weaker even than complement closure
\(D=D^c\), which is the genuine fact (Hoffman / \(E_k\) eigenspace). **It is
not a new or stronger bi-Steiner constraint and must not be cited as one.**
The earlier draft claimed otherwise; that claim is withdrawn.

## 4. COMPUTATION — kernel dimensions, and a REFUTED guess

\(\dim\ker M_D\) = **1** (\(k=2\)), **7** (\(k=4\)), **77** (\(k=6\); rank
715 of the \(792\times792\) matrix over \(\mathbb F_7\)).

The \(k=6\) figure is reproduced by the checked-in exact script

```bash
python3 -B collaboration/opus5/hadamard_kernel_followup/verify_k6_kernel.py
```

which uses exact integer arithmetic mod 7 (numpy as an array container only;
no floating point).

The pattern \(\dim\ker M_D=|D|/2\) predicts \(1,7,66\); it matches at
\(k=2,4\) and is **FALSE at \(k=6\)** (77, not 66). Recorded so it is not
re-tried. **\(\dim\ker M_D\) at \(k=16\) is not determined by this work, and
no estimate of it is claimed.**

## 5. PROVED — the descent is legitimate; nothing more is claimed

For \(LS(4,5,21)\): a 4-set lies in \(21-4=17=p\) five-sets, so every row
carries exactly \(p\) blocks, the theorem applies **verbatim**, and it yields
\(U'\) of dimension \(p-2=15\) inside \(\ker M_{D'}\). The descent therefore
**preserves the required 15-dimensional structure**.

\(|X'\setminus D'|=19152\) while \(|Y'|=5985\), so \(M_{D'}\) is wide and
\(\dim\ker M_{D'}\ge13167\). **Corrected:** that does *not* show the descent
is harder. All that follows is that **linear nullity alone gives no bound**
in the derived layer. The quadratic conditions — in particular gluing the
simplex frames across overlapping 4-set stars — may still make the derived
layer the better place to work. Nothing here settles that either way.

## 6. FAILED ATTACK — the exact remaining gap

No uniform capacity bound below 15 was obtained at \(k=16\).

The clique route is not merely weaker than needed, it is empty (§3). The
mechanism at \(k=4\) is that the only isotropic lines are the design
indicators \(h_C=\mathbf1+\mathbf1_C\) — one checks \(M_Dh_C=0\) and
\(M_D(h_C\circ h_C)=2\cdot\mathbf1\) — **and** that no two combine, since
\(M_D(h_C\circ h_E)=\mathbf1+M_D\mathbf1_{C\cap E}\) is nonconstant.

Reaching a capacity cap at \(k=16\) therefore needs **two** implications, and
**both are open**:

1. **(open)** every isotropic vector at \(k=16\) is a design indicator;
2. **(open)** the resulting design indicators are **pairwise incompatible,
   uniformly** over all \(k=16\) zero classes.

Implication 1 alone does **not** cap the capacity at 1 — without implication 2
a large family of mutually compatible design indicators is not excluded. An
earlier draft of this note treated implication 1 as "the crux" whose proof
would reach \(k=16\); that is withdrawn.

No counting or dimension heuristic is offered in support of a \(k=16\)
collapse; the kernel dimension there is unknown (§4).

## 7. Scope

Solves #835: **no**. Proves a capacity bound at \(k=16\): **no**.

* **Proved and non-trivial:** the audit (§1), the frame reformulation (§2),
  and the legitimacy of the descent (§5).
* **Proved but vacuous:** the clique/bi-Steiner corollary (§3) — it holds for
  every \(S(k-1,k,2k)\) regardless of any colouring, so it constrains nothing
  and is not a contribution.
* **Refuted:** the \(\dim\ker M_D=|D|/2\) guess (§4).
* **Open — TWO separate implications (§6):** (i) whether isotropy forces
  design-ness at \(k=16\), and (ii) whether the resulting design indicators
  are pairwise incompatible uniformly. Both are needed; neither is proved,
  and (i) alone caps nothing.

No estimate of \(\dim\ker M_D\) at \(k=16\) is claimed, and no heuristic is
offered for a collapse there. **Erdős–Rosenfeld #835 remains open.**

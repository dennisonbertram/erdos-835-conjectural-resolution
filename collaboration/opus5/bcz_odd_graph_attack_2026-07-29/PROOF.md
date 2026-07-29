# The full two-equitable-partition system on the Odd graph: complete
# specialization and a route-closure theorem

Date: 2026-07-29.  Author: Claude Opus 5.

Only fully proved statements appear in this file.  Failed routes, exact failure
boundaries and the next live idea are in `IDEAS.md`.  The verdict and its scope
are in `STATUS.md`.

---

## 0. Scope, provenance, and what is actually proved here

### 0.1 Provenance of the source (read this first)

The task asks me to apply Theorem 2.3 and Corollary 2.4 of

> R. A. Bailey, P. J. Cameron, S. Zhou, *Equitable partitions of regular
> graphs, and perfect sets in normal Cayley graphs*, arXiv:2605.17376,

and in particular to specialize "systems (6)--(8) and (13)".

**I could not retrieve that paper in this session.**  `WebFetch`, `WebSearch`
and outbound `curl` were all refused by the permission layer, as was every
Python interpreter.  I therefore have **no verified access to the numbering,
the hypotheses, or the exact statements of (6)--(8), (13), Theorem 2.3, or
Corollary 2.4.**  I do not state, paraphrase, or attribute any of them.

**Later audit.**  `INDEPENDENT_AUDIT.md` records a subsequent check against the
primary source and an executed verifier.  That audit confirms the concrete BCZ
specialization, retracts broader methodological overclaims in the original
draft, and adds the uniform Theorem 11.4.

What the derivation below actually covers:

I derive from scratch the standard intertwining and projection constraints that
two equitable partitions of a regular graph impose through their quotient
matrices and intersection-density matrix, and then determine their entire
solution space when one partition is the hypothetical #835 colour partition.

The later primary-source audit establishes the relationship to the cited paper:

* BCZ Theorem 2.3 systems (6)--(8) reduce to Theorems 1 and 3 below when the
  colour quotient is \(J_q-I_q\).
* BCZ Corollary 2.4(b), including system (13), is the swapped-order instance of
  the same projection calculation.
* Claims involving information beyond quotient and intersection-density data
  remain outside the scope of this file.

The paper's title also mentions *normal Cayley graphs*.  I do **not** know
whether \(O_k\) is a normal Cayley graph, and I do not assume it is; nothing
below uses any Cayley structure.  \(O_3\) (the Petersen graph) is classically
not a Cayley graph at all, which is at least a reason not to assume the Cayley
half of that theory applies here.

### 0.2 Standing setting

Fix an even integer \(k\ge2\) and put

\[
 q=k+1,\quad v=2k-1,\quad r=k-1,\quad X=\binom{[v]}{r},\quad N=|X|=\binom{2k-1}{k-1}.
\]

\(\Gamma=O_k=KG(v,r)\) is the Odd graph: \(S\sim T\iff S\cap T=\varnothing\).
It is \(k\)-regular.  \(A\) is its adjacency matrix, \(J\) the all-ones matrix,
\(\mathbf 1\) the all-ones vector; \(J_{m\times q}\) is the \(m\times q\)
all-ones matrix and \(J_q=J_{q\times q}\).

\(J(v,r)\) is the Johnson scheme on \(X\) with eigenspaces \(V_0,\dots,V_r\),
\(V_i\cong S^{(v-i,i)}\), \(m_i=\dim V_i=\binom vi-\binom v{i-1}\).

**Lemma 0** (as in `projection_rigidity_attack_2026-07-28/PROOF.md`).  \(A\)
acts on \(V_i\) as \(\lambda_i=(-1)^i(k-i)\); for even \(k\) the \((-1)\)-
eigenspace of \(A\) is **exactly** \(V_r=V_{k-1}\).  \(\square\)

Note \(m_{k-1}=\binom{2k-1}{k-1}-\binom{2k-1}{k-2}=N\bigl(1-\tfrac{k-1}{k+1}\bigr)=\tfrac{2N}{q}\).

Throughout, \(\tau=\{C_1,\dots,C_q\}\) denotes a hypothetical partition of \(X\)
into \(q\) perfect \(1\)-codes of \(O_k\) — equivalently (Lemma D of the earlier
note) a large set \(LS(k-2,k-1,2k-1)\), equivalently a covering projection
\(O_k\to K_q\), equivalently the object whose nonexistence for all \(k>2\) is
Erdős--Rosenfeld #835 in its Odd-graph form.  We write

\[
 y_a:=\mathbf 1_{C_a}-\tfrac1q\mathbf 1 .
\]

**Design quadrature (DQ).**  The statement "\(y_a\in V_{k-1}\) for every \(a\),
and \(\{C_a\}\) partitions \(X\)".  By Lemma D of the earlier note this is
exactly "each \(C_a\) is a perfect code / an \(S(k-2,k-1,2k-1)\)", i.e. it *is*
the problem, not a relaxation of it.

---

## 1. Equitable partitions: the facts used

Let \(\pi=\{P_1,\dots,P_m\}\) be a partition of \(V(\Gamma)\) of a \(d\)-regular
graph \(\Gamma\) on \(n\) vertices.  Write \(u_i=\mathbf 1_{P_i}\),
\(X_\pi=[u_1|\cdots|u_m]\in\{0,1\}^{n\times m}\), \(p=(|P_1|,\dots,|P_m|)^{\mathsf T}\),
\(D_\pi=\operatorname{diag}(p)\), \(U_\pi=\operatorname{col}X_\pi\).

\(\pi\) is **equitable** if for all \(i,j\) the number \(|N(u)\cap P_j|\) is the
same for every \(u\in P_i\); call it \((B_\pi)_{ij}\).  \(B_\pi\) is the
**quotient matrix**.

**Lemma 1.1.**  \(\pi\) is equitable \(\iff AX_\pi=X_\pi B_\pi\) for some
\(m\times m\) matrix \(B_\pi\), and then \(B_\pi\) is the quotient matrix.

*Proof.*  \((AX_\pi)_{u,j}=|N(u)\cap P_j|\) and \((X_\pi B_\pi)_{u,j}=(B_\pi)_{i(u),j}\)
where \(i(u)\) is the index of the cell containing \(u\).  Equality for all
\(u,j\) is exactly the equitability condition.  \(\square\)

**Lemma 1.2.**  For equitable \(\pi\):

1. \(B_\pi\mathbf 1_m=d\,\mathbf 1_m\);
2. \(D_\pi B_\pi=B_\pi^{\mathsf T}D_\pi\) (equivalently \(D_\pi B_\pi\) is symmetric,
   equivalently \(B_\pi^{\mathsf T}=D_\pi B_\pi D_\pi^{-1}\));
3. \(p^{\mathsf T}B_\pi=d\,p^{\mathsf T}\), i.e. \(p\) is a left \(d\)-eigenvector;
4. \(U_\pi\) is \(A\)-invariant, \(A|_{U_\pi}\) has matrix \(B_\pi\) in the basis
   \((u_i)\); hence \(B_\pi\) is diagonalizable with real spectrum and
   \(\operatorname{spec}B_\pi\subseteq\operatorname{spec}A\);
5. for every \(\theta\), the multiplicity of \(\theta\) in \(B_\pi\) equals
   \(\dim\bigl(U_\pi\cap\ker(A-\theta I)\bigr)\);
6. \(X_\pi D_\pi^{-1}X_\pi^{\mathsf T}=\Pi_{U_\pi}\), the orthogonal projector onto
   \(U_\pi\); it commutes with \(A\).

*Proof.*  (1) Row \(i\) of \(B_\pi\) sums to \(\sum_j|N(u)\cap P_j|=d\).
(2) \((D_\pi B_\pi)_{ij}=|P_i|\cdot|N(u)\cap P_j|\;(u\in P_i)\) counts the ordered
edges from \(P_i\) to \(P_j\), which is symmetric in \(i,j\).
(3) \(p^{\mathsf T}B_\pi=(B_\pi^{\mathsf T}p)^{\mathsf T}=(D_\pi B_\pi D_\pi^{-1}p)^{\mathsf T}
=(D_\pi B_\pi\mathbf 1_m)^{\mathsf T}=d\,p^{\mathsf T}\) by (1),(2).
(4) Immediate from Lemma 1.1; \(A|_{U_\pi}\) is the restriction of a symmetric
operator to an invariant subspace, hence diagonalizable with real spectrum, and
\(B_\pi\) is its matrix in a basis.
(5) The \(\theta\)-eigenspace of \(A|_{U_\pi}\) is \(U_\pi\cap\ker(A-\theta I)\).
(6) \(\{u_i/\sqrt{|P_i|}\}\) is an orthonormal basis of \(U_\pi\); commutation
with \(A\) holds because \(U_\pi\) and \(U_\pi^{\perp}\) are both \(A\)-invariant
(\(A\) symmetric).  \(\square\)

**Lemma 1.3 (the two extreme equitable partitions).**
The partition into singletons is equitable with \(B_\pi=A\), \(U_\pi=\mathbb R^{V}\).
The partition into one cell is equitable with \(B_\pi=(d)\), \(U_\pi=\langle\mathbf 1\rangle\).

*Proof.*  For singleton cells the equitability condition is vacuous (one vertex
per cell) and \((B_\pi)_{uw}=|N(u)\cap\{w\}|=A_{uw}\).  \(\square\)

**Lemma 1.4 (lattice).**  If \(\pi,\rho\) are equitable then so is their join
\(\pi\vee\rho\) (finest common coarsening), and
\(U_{\pi\vee\rho}=U_\pi\cap U_\rho\).  Also \(U_\pi+U_\rho\) is \(A\)-invariant.

*Proof.*  A vector is constant on the cells of \(\pi\vee\rho\) iff it is constant
on the cells of \(\pi\) and on those of \(\rho\); hence
\(U_{\pi\vee\rho}=U_\pi\cap U_\rho\), which is \(A\)-invariant as an intersection
of \(A\)-invariant subspaces.  A partition space that is \(A\)-invariant belongs
to an equitable partition by Lemma 1.1.  Sums of invariant subspaces are
invariant.  \(\square\)

---

## 2. The two-equitable-partition theorem (both orders)

Let \(\pi=\{P_i\}_{i\le m}\) and \(\sigma=\{Q_a\}_{a\le q}\) be **two** equitable
partitions of the same \(d\)-regular \(\Gamma\).  Define

\[
 S:=X_\pi^{\mathsf T}X_\sigma\in\mathbb Z_{\ge0}^{m\times q},\qquad S_{ia}=|P_i\cap Q_a| ,
\]
\[
 T:=D_\pi^{-1}S \quad(\text{row densities }T_{ia}=|P_i\cap Q_a|/|P_i|),\qquad
 T':=D_\sigma^{-1}S^{\mathsf T}.
\]

**Theorem 1 (intertwining).**
\[
 \boxed{B_\pi^{\mathsf T}S=S\,B_\sigma}
\]
equivalently \(B_\pi T=T B_\sigma\), equivalently \(B_\sigma T'=T'B_\pi\).

*Proof.*  Compute \(X_\pi^{\mathsf T}AX_\sigma\) in two ways.  Using
\(AX_\sigma=X_\sigma B_\sigma\) gives \(X_\pi^{\mathsf T}X_\sigma B_\sigma=SB_\sigma\).
Using \(A=A^{\mathsf T}\) and \(AX_\pi=X_\pi B_\pi\) gives
\((AX_\pi)^{\mathsf T}X_\sigma=B_\pi^{\mathsf T}X_\pi^{\mathsf T}X_\sigma=B_\pi^{\mathsf T}S\).
For the density form, substitute \(S=D_\pi T\) and \(B_\pi^{\mathsf T}=D_\pi B_\pi D_\pi^{-1}\)
(Lemma 1.2(2)): \(D_\pi B_\pi D_\pi^{-1}D_\pi T=D_\pi TB_\sigma\), and cancel the
invertible \(D_\pi\).  For the third form, transpose the first:
\(S^{\mathsf T}B_\pi=B_\sigma^{\mathsf T}S^{\mathsf T}\), substitute
\(S^{\mathsf T}=D_\sigma T'\) and \(B_\sigma^{\mathsf T}=D_\sigma B_\sigma D_\sigma^{-1}\).  \(\square\)

**Theorem 2 (the two orders carry the same information).**  The three displayed
identities of Theorem 1 are equivalent to one another as constraints on the pair
\((\pi,\sigma)\).  Consequently "apply the theorem with \(\tau\) as the colour
partition and \(\pi\) as the auxiliary one" and "apply it with the roles swapped"
produce *identical* constraint sets.

*Proof.*  Each is obtained from the previous by multiplying on the left and/or
right by the invertible matrices \(D_\pi^{\pm1},D_\sigma^{\pm1}\) and by
transposition, all reversible operations; the proof of Theorem 1 exhibits the
reversible substitutions explicitly.  \(\square\)

**The full first-order system.**  Collecting everything true about the pair at
this level:

\[
\begin{aligned}
&\text{(S1)}&& B_\pi^{\mathsf T}S=SB_\sigma
   \quad(\text{equivalently }B_\pi T=TB_\sigma,\ B_\sigma T'=T'B_\pi),\\
&\text{(S2)}&& S\mathbf 1_q=p_\pi,\qquad S^{\mathsf T}\mathbf 1_m=p_\sigma
   \quad(\text{row/column totals}),\\
&\text{(S3)}&& S\in\mathbb Z_{\ge0}^{m\times q}
   \quad(\text{integrality and nonnegativity}),\\
&\text{(S4)}&& 0\preceq G:=T^{\mathsf T}D_\pi T-\tfrac1n p_\sigma p_\sigma^{\mathsf T}
   \preceq \operatorname{diag}(p_\sigma)-\tfrac1n p_\sigma p_\sigma^{\mathsf T}
   \quad(\text{Gram sandwich, Prop. 10.1}),\\
&\text{(S5)}&& \operatorname{rank}\bigl(S-\tfrac1n p_\pi p_\sigma^{\mathsf T}\bigr)
   \le\#\bigl(\operatorname{spec}B_\pi\cap\operatorname{spec}B_\sigma\setminus\{d\}\bigr)
   \text{-weighted bound (Prop. 10.2).}
\end{aligned}
\]

(S4),(S5) are proved in §10; they are listed here so that the closure theorem of
§4 can be stated for the whole package.

---

## 3. Complete symbolic specialization at \(M_\tau=J_q-I_q\)

Now take \(\sigma=\tau\), the hypothetical colour partition.

**Lemma 3.1.**  \(\tau\) is equitable with \(B_\tau=J_q-I_q\), all cells of size
\(N/q\), and \(\operatorname{spec}B_\tau=\{k^{(1)},(-1)^{(k)}\}\).

*Proof.*  A perfect \(1\)-code partition means every closed neighbourhood meets
every class exactly once; so for \(u\in C_a\), \(|N(u)\cap C_b|=1\) for \(b\ne a\)
and \(=0\) for \(b=a\).  That is \(B_\tau=J_q-I_q\), which is equitable by
definition, and \(J_q-I_q\) has eigenvalue \(q-1=k\) on \(\mathbf 1_q\) and \(-1\)
on \(\mathbf 1_q^{\perp}\).  Class sizes: \(|C_a|\cdot q=N\) since
\((A+I)\mathbf1_{C_a}=\mathbf1\) forces \(\langle\mathbf1_{C_a},\mathbf1\rangle(k+1)=N\).  \(\square\)

**Theorem 3 (the specialized system, in full).**  Let \(\pi\) be any equitable
partition of \(O_k\) with \(m\) cells, and let \(\tau\) be a partition into \(q\)
perfect codes.  Put \(\varepsilon_\pi:=\dim\bigl(U_\pi\cap V_{k-1}\bigr)\)
(= multiplicity of \(-1\) in \(B_\pi\), by Lemma 1.2(5) and Lemma 0).  Then
(S1)+(S2) is **equivalent** to the single matrix equation together with row
stochasticity:

\[
 \boxed{\;(B_\pi+I_m)\,T=J_{m\times q},\qquad T\mathbf 1_q=\mathbf 1_m\;}
 \tag{3.1}
\]

and the complete solution space of (3.1) is the affine space

\[
 \boxed{\;T=\tfrac1q J_{m\times q}+Z,\qquad
 \text{columns of }Z\in\ker(B_\pi+I_m),\qquad Z\mathbf 1_q=0,\;}
 \tag{3.2}
\]

of dimension \(\varepsilon_\pi\,(q-1)\).  Moreover the column-total condition
\(S^{\mathsf T}\mathbf 1_m=\frac Nq\mathbf 1_q\) is **automatically implied** and adds
nothing.

*Proof.*
*Reduction to (3.1).*  By Theorem 1 in density form, \(B_\pi T=TB_\tau=TJ_q-T\).
By (S2), \(T\mathbf 1_q=\mathbf 1_m\), hence \(TJ_q=(T\mathbf 1_q)\mathbf 1_q^{\mathsf T}=J_{m\times q}\).
So \(B_\pi T=J_{m\times q}-T\), i.e. \((B_\pi+I)T=J_{m\times q}\).  Conversely
(3.1) gives \(B_\pi T=J_{m\times q}-T=TJ_q-T=T(J_q-I_q)=TB_\tau\).

*Consistency.*  Multiply (3.1) by \(\mathbf 1_q\):
\((B_\pi+I)\mathbf 1_m=(k+1)\mathbf 1_m=q\mathbf 1_m=J_{m\times q}\mathbf 1_q\), using Lemma 1.2(1)
with \(d=k\).  So \(\tfrac1qJ_{m\times q}\) is a particular solution of the linear
part, and it is row stochastic.

*Solution space.*  The homogeneous equation is \((B_\pi+I)Z=0\), i.e. every
column of \(Z\) lies in \(K:=\ker(B_\pi+I_m)\), a space of dimension
\(\varepsilon_\pi\) (Lemma 1.2(5) with \(\theta=-1\), Lemma 0).  The extra
condition \(T\mathbf 1_q=\mathbf 1_m\) becomes \(Z\mathbf 1_q=0\).  The map
\(K^{q}\to K,\ Z\mapsto Z\mathbf 1_q\) is surjective, so its kernel has dimension
\(\varepsilon_\pi q-\varepsilon_\pi=\varepsilon_\pi(q-1)\).

*Column totals are automatic.*  \(p^{\mathsf T}\) is a left \(k\)-eigenvector of
\(B_\pi\) (Lemma 1.2(3)), and \(k\ne-1\), so \(p^{\mathsf T}z=0\) for every
\(z\in K\) (left and right eigenvectors of a diagonalizable matrix for distinct
eigenvalues are orthogonal).  Hence
\(S^{\mathsf T}\mathbf 1_m=T^{\mathsf T}D_\pi\mathbf 1_m=T^{\mathsf T}p
=\tfrac1qJ_{q\times m}p+Z^{\mathsf T}p=\tfrac Nq\mathbf 1_q\).  \(\square\)

**Corollary 3.2 (the \(\varepsilon_\pi=0\) case: proportional meeting).**  If
\(-1\notin\operatorname{spec}B_\pi\) then \(B_\pi+I\) is invertible, (3.2) forces
\(Z=0\), and

\[
 |P_i\cap C_a|=\frac{|P_i|}{q}\qquad\text{for every }i,a .
\]

In particular \(q\mid|P_i|\) for every cell of \(\pi\).

**Corollary 3.3 (the \(\varepsilon_\pi=1\) case).**  If \(\varepsilon_\pi=1\), fix
\(0\ne z\in\ker(B_\pi+I_m)\).  Then there is \(c\in\mathbb R^q\) with
\(\sum_ac_a=0\) such that

\[
 |P_i\cap C_a|=\frac{|P_i|}{q}+|P_i|\,z_i\,c_a\qquad\text{for all }i,a .
\]
That is, the whole deviation table is rank one and is determined by \(q-1\)
scalars.

*Proof.*  (3.2) with \(\dim K=1\) gives \(Z=zc^{\mathsf T}\); \(Z\mathbf 1_q=0\)
gives \(\sum_ac_a=0\); \(S=D_\pi T\).  \(\square\)

**Remark 3.4 (this is the whole first-order specialization).**  Equations
(3.1)--(3.2) are the *complete* symbolic answer to "specialize the two-equitable
partition system when the quotient matrix of one partition is \(J_q-I_q\)":
a single linear matrix equation, an explicit particular solution, and a kernel
of dimension \(\varepsilon_\pi(q-1)\).  Nothing about \(O_k\) has been used yet
except \(k\)-regularity; the Odd-graph input enters only through
\(\varepsilon_\pi=\dim(U_\pi\cap V_{k-1})\).

---

## 4. The closure theorem: the whole system is design quadrature

**Theorem 4 (route closure for the full two-equitable-partition system).**
Let \(k\ge2\) be even, \(\Gamma=O_k\), and let \(C_1,\dots,C_q\) be any partition
of \(X\).  Then:

1. **(Soundness / no new information.)**  If DQ holds — i.e. every \(C_a\) is a
   perfect code — then for **every** equitable partition \(\pi\) of \(O_k\), in
   **either order**, the entire system (S1)--(S5) holds.  Moreover for each
   fixed \(\pi\), the system (S1)+(S2) is *exactly* the statement
   \[
     \Pi_{U_\pi}\,y_a\in U_\pi\cap V_{k-1}\qquad(a=1,\dots,q),
     \tag{4.1}
   \]
   i.e. the orthogonal projection of DQ onto \(U_\pi\).
2. **(Sharpness.)**  Taking \(\pi\) to be the partition into singletons
   (equitable by Lemma 1.3, with \(B_\pi=A\)) turns (3.1) into
   \((A+I)X_\tau=J_{N\times q}\), which is precisely DQ.
3. **(No gain from families.)**  For any finite family
   \(\pi^{(1)},\dots,\pi^{(s)}\) of equitable partitions, the conjunction of the
   pairwise systems for \((\pi^{(t)},\tau)\) is the conjunction of the individual
   conditions (4.1), and equals the single condition (4.1) for the \(A\)-invariant
   subspace \(U:=U_{\pi^{(1)}}+\dots+U_{\pi^{(s)}}\).  Adding the pairwise systems
   among the \(\pi^{(t)}\) themselves contributes no condition involving any
   \(C_a\).  Joins of equitable partitions give conditions that are *weaker*
   (their spaces are intersections, Lemma 1.4).

Consequently: **ranged over all equitable partitions, the two-equitable-partition
system is logically equivalent to DQ, i.e. to Problem #835 itself.  For one
fixed \(\pi\), its linear part is the projection of DQ onto \(U_\pi\), so it is
never stronger than DQ.**  If \(U_\pi\ne\mathbb R^X\), this projection discards
real-linear directions.  This alone does **not** prove strict weakening after
one also restricts the unknowns to zero-one indicators forming a partition;
that stronger claim would require an actual non-DQ partition satisfying the
projected system.

*Proof.*
(1) Let \(\pi\) be equitable.  \(\Pi_{U_\pi}\) commutes with \(A\)
(Lemma 1.2(6)), so it preserves every eigenspace of \(A\); hence
\(\Pi_{U_\pi}V_{k-1}=U_\pi\cap V_{k-1}\).  If \(y_a\in V_{k-1}\) then
\(\Pi_{U_\pi}y_a\in U_\pi\cap V_{k-1}\), giving (4.1).  Conversely, expand:
\(\Pi_{U_\pi}\mathbf 1_{C_a}=\sum_i\frac{|P_i\cap C_a|}{|P_i|}u_i\) and
\(\Pi_{U_\pi}\mathbf 1=\mathbf 1=\sum_iu_i\), so
\(\Pi_{U_\pi}y_a=\sum_iZ_{ia}u_i\) with \(Z=T-\frac1qJ_{m\times q}\).  Since
\(A|_{U_\pi}\) has matrix \(B_\pi\) in the basis \((u_i)\), the statement
\(\Pi_{U_\pi}y_a\in\ker(A+I)\cap U_\pi\) is exactly \((B_\pi+I)Z_{\cdot a}=0\),
which by Theorem 3 is exactly (S1)+(S2) restricted to column \(a\).  This proves
the "exactly" claim in (1) and, with Theorem 2, that both orders give the same
thing.  (S3) holds because \(|P_i\cap C_a|\) are cardinalities.  (S4),(S5) are
proved in §10 from (4.1) alone.

(2) With singleton cells, \(D_\pi=I\), \(T=S=X_\tau\), \(B_\pi=A\), so (3.1) reads
\((A+I)X_\tau=J_{N\times q}\).  Column \(a\) says
\(|N(u)\cap C_a|+[u\in C_a]=1\) for every vertex \(u\): every closed
neighbourhood meets \(C_a\) exactly once, i.e. \(C_a\) is a perfect code.  Row
stochasticity is automatic since the \(C_a\) partition \(X\).  This is DQ.

(3) Condition (4.1) for \(\pi^{(t)}\) says
\(\langle y_a,w\rangle=0\) for every \(w\in U_{\pi^{(t)}}\ominus(U_{\pi^{(t)}}\cap V_{k-1})\),
because \(\Pi_{U}y_a\in U\cap V_{k-1}\) iff \(y_a\perp\bigl(U\ominus(U\cap V_{k-1})\bigr)\)
— indeed, decomposing the \(A\)-invariant \(U\) into eigenspaces
\(U=\bigoplus_\theta(U\cap\ker(A-\theta))\), the condition is
\(\Pi_{U\cap\ker(A-\theta)}y_a=0\) for every \(\theta\ne-1\).  Such conditions are
linear functionals of \(y_a\) indexed by vectors of \(U^{(t)}\); the conjunction
over \(t\) is the same family of functionals indexed by
\(U=\sum_tU^{(t)}\), which is \(A\)-invariant (Lemma 1.4).  The pairwise system
for \((\pi^{(t)},\pi^{(s)})\) involves only \(B_{\pi^{(t)}},B_{\pi^{(s)}}\) and
\(|P\cap P'|\); no \(C_a\) occurs in it.  For joins,
\(U_{\pi\vee\rho}=U_\pi\cap U_\rho\subseteq U_\pi\), so its functional family is
a subfamily.  \(\square\)

**Corollary 4.1 (exact restatement, not a relaxation).**  The two-equitable-
partition machinery applied to \((\pi,\tau)\) for **all** \(\pi\) is not a
relaxation of #835 and not a strengthening of it: it is a re-encoding.  Any
contradiction obtainable from it is obtainable from "each \(C_a\) is an
\(S(k-2,k-1,2k-1)\)" plus the partition condition, and conversely.

**Corollary 4.2 (a natural spanning family already saturates).**  For a vertex
\(M\in X\), let \(\pi_M\) be the distance partition from \(M\).  Then
\(U_{\pi_M}\cap V_i=\langle E_ie_M\rangle\) is one-dimensional for every
\(0\le i\le k-1\), and condition (4.1) for \(\pi_M\) reads
\((E_iy_a)_M=0\) for \(1\le i\le k-2\).  Hence the family \(\{\pi_M\}_{M\in X}\)
already gives exactly DQ, while **each individual** \(\pi_M\) gives only the
\(k-2\) scalar equations at the single vertex \(M\).

*Proof.*  \(O_k\) is distance-regular of diameter \(k-1\); the distance partition
from a vertex is equitable, and its cells are the \(S_{k-1}\times S_k\)-orbits
\(P_j=\{S:|S\cap M|=j\}\) (see §8).  The space of \(\operatorname{Stab}(M)\)-invariants
in \(V_i\) has dimension \(o_i-o_{i-1}\), where \(o_i\) is the number of
\(\operatorname{Stab}(M)\)-orbits on \(i\)-subsets of \([v]\); here
\(o_i=\min(i,k-1)+1=i+1\) for \(i\le k-1\), so the dimension is \(1\).  This
one-dimensional space contains \(E_i e_M\), which is nonzero since
\((E_i)_{MM}=m_i/N>0\); so it is spanned by it.  By the proof of Theorem 4(3),
(4.1) for \(\pi_M\) says \(\langle y_a,E_ie_M\rangle=0\) for \(i\ne0,k-1\), i.e.
\((E_iy_a)_M=0\).  Ranging over all \(M\) gives \(E_iy_a=0\) for
\(1\le i\le k-2\), and \(E_0y_a=0\) holds by construction; that is
\(y_a\in V_{k-1}\), i.e. DQ.  \(\square\)

---

## 5. Column decoupling: what this system structurally cannot see

**Theorem 5 (decoupling).**  For every equitable \(\pi\), the system (S1)+(S2)
for \((\pi,\tau)\) decouples over the colours: it is the conjunction over
\(a=1,\dots,q\) of the *single-class* conditions (4.1), together with the
partition identity \(\sum_a\mathbf 1_{C_a}=\mathbf 1\).  No condition in the system
involves two colour classes simultaneously.  The same holds for (S4)--(S5),
which are consequences of (4.1) for the individual classes plus the Gram matrix
\(Y^{\mathsf T}Y=\frac Nq(I_q-\frac1qJ_q)\), itself a consequence of the partition
identity and \(|C_a|=N/q\).

*Proof.*  Theorem 3 shows (S1)+(S2) is \((B_\pi+I)Z_{\cdot a}=0\) column by
column, with the only coupling being \(Z\mathbf1_q=0\), which is the partition
identity projected to \(U_\pi\).  §10 derives (S4),(S5) from
\(G=Y^{\mathsf T}\Pi_{U_\pi}Y\) with \(Y=[y_1|\cdots|y_q]\).  \(\square\)

**Corollary 5.1 (exact decoupling boundary).**  Before imposing the zero-one
partition domain, the linear equations supplied by a fixed auxiliary
partition constrain the columns separately, with their sum coupled only by
\(\sum_a\mathbf1_{C_a}=\mathbf1\).  They contain no explicit matching,
intersection, or transport variable joining two colour classes.

This does **not** imply that the system cannot distinguish one perfect code
from a partition into \(q\) of them.  The zero-one partition identity is itself
a strong global disjointness constraint, and Theorem 4(2) shows that the
singleton auxiliary partition recovers the entire large-set problem.  What is
proved here is only the absence of additional explicit cross-colour variables
in the projected linear equations.  The controls in §9 establish numerical
feasibility for the stated stabilizer and distance families, not feasibility
of the singleton system or of every auxiliary partition.

---

## 6. The \(\varepsilon_\pi=0\) route is unconditionally vacuous

By Corollary 3.2, the only *arithmetic* consequence obtainable from an equitable
partition whose quotient spectrum misses \(-1\) is: \(q\) divides every cell
size.  This is the natural place to look for a contradiction.  It never fires.

**Theorem 6 (unconditional divisibility).**  Let \(k\ge2\) with \(q=k+1\)
**prime**, \(v=2k-1\), \(X=\binom{[v]}{k-1}\).  Let \(P\subseteq X\) be **any**
subset with \(\mathbf 1_P\perp V_{k-1}\).  Then \(q\mid|P|\).

*Proof.*  Let \(W\) be the \(\binom{v}{k-2}\times\binom{v}{k-1}\) inclusion matrix
of \((k-2)\)-subsets versus \((k-1)\)-subsets of \([v]\).

*(a) \(\operatorname{col}_{\mathbb Q}W^{\mathsf T}=V_0\oplus\cdots\oplus V_{k-2}=V_{k-1}^{\perp}\).*
\(W\) has full row rank \(\binom{v}{k-2}\) because \(k-2\le k-1\le v-(k-2)=k+1\)
(Gottlieb's theorem, or Wilson's diagonal form below, which has no zero
diagonal entry).  Hence \(\operatorname{col}_{\mathbb Q}W^{\mathsf T}\) has dimension
\(\binom v{k-2}=\sum_{i\le k-2}m_i\); it is \(S_v\)-invariant, so it is a sum of
isotypic components; comparing dimensions it must be
\(V_0\oplus\cdots\oplus V_{k-2}\), which is \(V_{k-1}^\perp\) since
\(\mathbb R^X=\bigoplus_{i=0}^{k-1}V_i\).

*(b) The saturation index is coprime to \(q\).*  By Wilson's diagonal form for
inclusion matrices (R. M. Wilson, *A diagonal form for the incidence matrices of
\(t\)-subsets vs. \(\kappa\)-subsets*, Europ. J. Combin. 11 (1990) 609--615 —
used here as a cited classical theorem, not reproved), the Smith normal form of
\(W\) has, for \(i=0,\dots,k-2\), exactly \(m_i\) diagonal entries equal to
\(\binom{(k-1)-i}{(k-2)-i}=k-1-i\).  So the elementary divisors of \(W\) all lie
in \(\{1,2,\dots,k-1\}\).  Writing \(W=U\Sigma V\) with \(U,V\) unimodular and
changing basis by the unimodular \(V^{-\mathsf T}\), one sees
\[
 d\cdot\Bigl(\mathbb Z^X\cap\operatorname{col}_{\mathbb Q}W^{\mathsf T}\Bigr)
 \subseteq W^{\mathsf T}\mathbb Z^{\binom{[v]}{k-2}},
 \qquad d:=\operatorname{lcm}(1,2,\dots,k-1).
\]
Since \(q=k+1\) is prime and \(q>k-1\), we have \(\gcd(d,q)=1\).

*(c) Conclusion.*  \(\mathbf1_P\in\mathbb Z^X\cap\operatorname{col}_{\mathbb Q}W^{\mathsf T}\)
by hypothesis and (a).  By (b), \(d\,\mathbf1_P=W^{\mathsf T}g\) with
\(g\in\mathbb Z^{\binom{[v]}{k-2}}\).  Every \((k-2)\)-subset lies in exactly
\(v-(k-2)=k+1=q\) subsets of size \(k-1\), i.e. \(W\mathbf1=q\mathbf1\).  Hence
\[
 d\,|P|=\mathbf1^{\mathsf T}W^{\mathsf T}g=(W\mathbf 1)^{\mathsf T}g=q\,\mathbf1^{\mathsf T}g\in q\mathbb Z .
\]
As \(\gcd(d,q)=1\), \(q\mid|P|\).  \(\square\)

**Corollary 6.1 (the \(\varepsilon=0\) divisibility test is closed for every
\(k\)).**  Let \(q=k+1\) be prime.  For **every** equitable partition \(\pi\) of
\(O_k\) with \(-1\notin\operatorname{spec}B_\pi\), every cell size is divisible by
\(q\).  Hence the necessary condition of Corollary 3.2 is satisfied
unconditionally, and can never produce a contradiction — for any \(k\), any such
\(\pi\), and independently of whether any perfect code exists.

*Proof.*  \(-1\notin\operatorname{spec}B_\pi\) means \(U_\pi\cap V_{k-1}=0\)
(Lemma 1.2(5)); since \(U_\pi\) is \(A\)-invariant and \(A\) is symmetric,
\(U_\pi\perp V_{k-1}\).  So every cell indicator satisfies the hypothesis of
Theorem 6.  \(\square\)

**Remark 6.2.**  Primality of \(q\) is exactly the right hypothesis: \(q=k+1\) is
coprime to \(\operatorname{lcm}(1,\dots,k-1)\) iff every prime factor of \(k+1\)
exceeds \(k-1\), which for \(k\ge2\) happens iff \(k+1\) is prime.  And \(q\)
prime is already forced for #835 by the Ma--Tang obstruction, so Theorem 6
covers every case that survives to this point.

---

## 7. The \(s\)-set stabilizer family, computed explicitly

This section re-derives the conclusion of §6 for the most natural family of
\(\pi\)'s, by a direct argument independent of Wilson's theorem.  It answers the
task's request to test "stabilizer-orbit partitions associated with a point,
pair, or \(s\)-set" uniformly in \(k\).

Fix \(0\le m\le k-1\) and \(M_0\subseteq[v]\) with \(|M_0|=m\).  Let
\(H=\operatorname{Sym}(M_0)\times\operatorname{Sym}([v]\setminus M_0)\) and let
\(\pi^{(m)}\) be its orbit partition on \(X\), with cells

\[
 P_j=\{S\in X:|S\cap M_0|=j\},\qquad
 |P_j|=\binom mj\binom{2k-1-m}{\,k-1-j\,},\qquad 0\le j\le m .
\]

(The range is \(0\le j\le m\) because \(k-1-j\le 2k-1-m\) always holds for
\(m\le k-1\).)

**Lemma 7.1.**  \(\pi^{(m)}\) is equitable, and
\(\operatorname{spec}B_{\pi^{(m)}}=\{\lambda_i=(-1)^i(k-i):0\le i\le m\}\), each
simple.  In particular \(\varepsilon_{\pi^{(m)}}=0\) iff \(m\le k-2\), and
\(\varepsilon_{\pi^{(k-1)}}=1\).

*Proof.*  Orbit partitions of automorphism groups are equitable.
\(U_{\pi^{(m)}}=(\mathbb R^X)^H\), and
\(\dim(V_i)^H=o_i(H)-o_{i-1}(H)\), where \(o_i(H)\) is the number of \(H\)-orbits
on \(i\)-subsets of \([v]\) (because \(\mathbb R^{\binom{[v]}i}\cong\bigoplus_{j\le i}V_j\)
for \(i\le v/2\)).  Here \(o_i(H)=\#\{(a,b):a+b=i,\ 0\le a\le m,\ 0\le b\le v-m\}
=\min(i,m)+1\) for \(i\le v-m\).  Since \(v-m=2k-1-m\ge k\ge k-1\), this applies
for all \(i\le k-1\), giving \(\dim(V_i)^H=1\) for \(i\le m\) and \(0\) for
\(m<i\le k-1\).  Now apply Lemma 1.2(5) and Lemma 0.  \(\square\)

**Theorem 7 (the stabilizer family is uniformly non-obstructive).**  Let \(k\ge2\)
be even with \(q=k+1\) prime.  Then for every \(0\le j\le m\le k-2\),
\[
 q\ \Bigm|\ \binom{2k-1-m}{\,k-1-j\,},\qquad\text{hence}\qquad q\mid|P_j| .
\]
Consequently the proportional-meeting conditions of Corollary 3.2 for the whole
family \(\pi^{(0)},\dots,\pi^{(k-2)}\) are integral for every admissible \(k\),
and this family yields no contradiction.

*Proof.*  Put \(n=2k-1-m=2q-3-m\) and \(s=k-1-j=q-2-j\).  Since \(0\le j\le m\le q-3\):
\[
 1\le q-2-m\le s\le q-2\le q-1,\qquad
 n-s=(2q-3-m)-(q-2-j)=q-1-(m-j),
\]
and \(0\le m-j\le q-3\) gives \(2\le n-s\le q-1\).  So both \(s\) and \(n-s\) lie
in \(\{1,\dots,q-1\}\): each is a single nonzero base-\(q\) digit with no
higher digits.  Their sum is \(n=2q-3-m\ge q\) (using \(m\le q-3\)), so adding
\(s\) and \(n-s\) in base \(q\) produces a carry out of the units place.  By
Kummer's theorem \(v_q\binom ns\ge1\).  \(\square\)

**Remark 7.2.**  Theorem 7 is the special case of Corollary 6.1 for this family
(consistently: \(\varepsilon=0\) exactly when \(m\le k-2\)).  It is included
because its proof is elementary and gives an independent check of Theorem 6 at
every \(k\), and because the numbers \(|P_j|/q\) are exactly the classical
"blocks meeting a fixed \(m\)-set in \(j\) points" counts of an
\(S(k-2,k-1,2k-1)\), i.e. the standard divisibility conditions of the design.
The boundary is sharp: at \(m=k-1\) one has \(|P_{k-1}|=1\), which is **not**
divisible by \(q\) — and indeed \(\varepsilon_{\pi^{(k-1)}}=1\), so Corollary 3.2
does not apply there.  That case is §8.

---

## 8. The distance-partition family (\(\varepsilon_\pi=1\)): closed form and
## uniform feasibility

Take \(m=k-1\) in §7: \(M\in X\) is a vertex, \(H=\operatorname{Stab}(M)\), and
\(\pi_M\) has cells \(P_j=\{S:|S\cap M|=j\}\), \(0\le j\le k-1\), with

\[
 |P_j|=\binom{k-1}{j}\binom{k}{\,k-1-j\,},\qquad
 P_{k-1}=\{M\},\quad P_0=N(M).
\]

This is the distance partition from \(M\) (\(P_0\) is the neighbourhood, \(P_{k-1}\)
is \(M\) itself), and \(\varepsilon_{\pi_M}=1\) by Lemma 7.1.  By Corollary 3.3 the
whole intersection table is rank one; the singleton cell pins the free parameter.

**Theorem 8 (exact closed form).**  Assume \(\tau\) is a partition of \(O_k\) into
\(q\) perfect codes.  Fix \(M\in X\) and \(a\in\{1,\dots,q\}\), and put
\(\epsilon=[\,M\in C_a\,]\in\{0,1\}\).  Then for \(0\le j\le k-1\),

\[
 \boxed{\;
 \alpha_j:=|P_j\cap C_a|
 =\frac{|P_j|}{q}+(-1)^{k-1-j}\binom{k-1}{j}\Bigl(\epsilon-\frac1q\Bigr)
 =\binom{k-1}{j}\cdot\frac{\binom{k}{k-1-j}+(-1)^{k-1-j}(q\epsilon-1)}{q}. }
\]

*Proof.*  By Corollary 3.3, \(\alpha_j=\frac{|P_j|}q+w_j\gamma\) where
\(w=D_\pi z\) is a fixed nonzero vector (independent of \(a\)) and \(\gamma\)
depends only on \(a\).  Because \(P_{k-1}=\{M\}\) is a singleton,
\(\alpha_{k-1}=\epsilon\); normalizing \(w_{k-1}=1\) gives
\(\gamma=\epsilon-\frac1q\).  It remains to identify \(w\).

\(C_a\) is an \(S(k-2,k-1,2k-1)\) (Lemma D of the earlier note), so for
\(0\le i\le k-2\) the number of blocks containing a fixed \(i\)-set is
\(\lambda_i=\binom{2k-1-i}{k-2-i}\big/(k-1-i)\), and double counting over the
\(i\)-subsets of the \((k-1)\)-set \(M\) gives
\[
 \beta_i:=\sum_{j}\binom ji\alpha_j=\binom{k-1}{i}\lambda_i\qquad(0\le i\le k-2),
 \qquad \beta_{k-1}=\alpha_{k-1}=\epsilon .
\]
Binomial (Möbius) inversion of \(\beta_i=\sum_j\binom ji\alpha_j\) over
\(0\le i,j\le k-1\) gives \(\alpha_j=\sum_{i\ge j}(-1)^{i-j}\binom ij\beta_i\).
Only the top term \(i=k-1\) carries \(\epsilon\), with coefficient
\((-1)^{k-1-j}\binom{k-1}{j}\).  Hence \(w_j=\partial\alpha_j/\partial\epsilon
=(-1)^{k-1-j}\binom{k-1}j\), and \(w_{k-1}=1\) as normalized.  Substituting
\(\gamma=\epsilon-\frac1q\) gives the first displayed form; the second follows
from \(|P_j|=\binom{k-1}j\binom k{k-1-j}\).  \(\square\)

**Theorem 8.1 (uniform feasibility of the distance-partition system).**  Let
\(k\ge2\) be even with \(q=k+1\) prime.  Then for every \(j\) and every
\(\epsilon\in\{0,1\}\), the number \(\alpha_j\) of Theorem 8 is a **nonnegative
integer**, and \(\sum_j\alpha_j=N/q\), and
\(\alpha_j(\epsilon=1)+(q-1)\alpha_j(\epsilon=0)=|P_j|\).

Hence the system (3.1)--(3.2) for \(\pi_M\) has an explicit nonnegative integral
solution for **every** admissible \(k\), including \(k=16\).  This family
therefore yields no obstruction, uniformly in \(k\).

*Proof.*
*Integrality.*  \(k=q-1\), so \(\binom{k}{s}=\binom{q-1}{s}\equiv(-1)^s\pmod q\)
for \(0\le s\le q-1\) (immediate from
\(\binom{q-1}{s}=\prod_{t=1}^{s}\frac{q-t}{t}\equiv\prod_{t=1}^s(-1)=(-1)^s\)).
With \(s=k-1-j\),
\(\binom{k}{k-1-j}+(-1)^{k-1-j}(q\epsilon-1)\equiv(-1)^{s}-(-1)^{s}=0\pmod q\).

*Nonnegativity.*  If \(\epsilon=0\), the bracket is
\(\binom k{k-1-j}-(-1)^{k-1-j}\ge1-1=0\).  If \(\epsilon=1\), the bracket is
\(\binom{k}{k-1-j}+(q-1)(-1)^{k-1-j}\); when the sign is \(+1\) this is positive,
and when \(k-1-j\) is odd we have \(1\le k-1-j\le k-1\), so
\(\binom k{k-1-j}\ge\binom k1=k=q-1\), giving a value \(\ge0\).

*Totals.*  \(\sum_j\alpha_j=\frac1q\sum_j|P_j|+(\epsilon-\frac1q)\sum_j(-1)^{k-1-j}\binom{k-1}j
=\frac Nq+0\) since \(\sum_j(-1)^{k-1-j}\binom{k-1}{j}=(1-1)^{k-1}=0\) for \(k\ge2\).
The last identity is the sum over the \(q\) colours: one has \(\epsilon=1\), the
other \(q-1\) have \(\epsilon=0\), and the \(\epsilon\)-terms cancel by the same
computation.  \(\square\)

**Remark 8.2.**  Theorem 8 is exactly the classical statement that a perfect code
in a distance-regular graph is completely regular: the distance distribution of
\(C_a\) from a vertex depends only on \(\bigl[M\in C_a\bigr]\).  Equivalently, in
design language, for a \(t\)-design the intersection numbers with a
\((t+1)\)-set are determined up to one parameter, and here the block size equals
\(t+1\) so that parameter is the single bit "is \(M\) itself a block".  This is a
single-class condition (Theorem 5) and is satisfied by one perfect code alone.

---

## 9. Small controls

Throughout: \(q=k+1\), \(|P_j|=\binom{k-1}j\binom k{k-1-j}\), and \(\alpha_j\) is
from Theorem 8.  All tables below are hand-computed and cross-checked against
both the Möbius form and the closed form.

### 9.1 \(k=2\) (the one case where the object exists)

\(v=3\), \(r=1\), \(X=\binom{[3]}1\), \(O_2=KG(3,1)=K_3\), degree \(2\), \(q=3\),
\(N=3\).  Perfect codes are single vertices; \(\tau=\{\{1\},\{2\},\{3\}\}\) is a
partition into \(3\) perfect codes, so a solution exists.  Lemma 0 still holds
(\(\lambda_0=2,\lambda_1=-1\), \(V_1\) is the \((-1)\)-eigenspace, \(\dim V_1=2=k\)).
Distance partition from \(M\): \(P_0=\{\text{other two}\}\) of size
\(\binom10\binom21=2\), \(P_1=\{M\}\) of size \(1\).  Theorem 8 gives
\(\alpha_0=\frac23-(\epsilon-\frac13)=1-\epsilon\), \(\alpha_1=\epsilon\), summing
to \(1=N/q\) ✓.  This is the correct behaviour of the singleton code.
**Control value:** the machinery is consistent in the unique case with a solution;
it does not distinguish \(k=2\) from \(k=4,6\) below.

### 9.2 \(k=4\): no large set, yet the system is feasible

\(v=7\), \(r=3\), \(N=35\), \(q=5\), \(|C_a|=7\).  Perfect codes are the \(30\)
labelled Fano planes \(S(2,3,7)\); at most **two** are pairwise disjoint
(`verify_k4.py` in the repository), far short of \(5\), so **no \(LS(2,3,7)\)
exists**.

Distance partition from a vertex \(M\) (a \(3\)-set): cells \(P_0,\dots,P_3\).

| \(j\) | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| \(\lvert P_j\rvert\) | 4 | 18 | 12 | 1 |
| \(\alpha_j\ (M\notin C_a)\) | 1 | 3 | 3 | 0 |
| \(\alpha_j\ (M\in C_a)\) | 0 | 6 | 0 | 1 |

Checks: \(4+18+12+1=35\) ✓; \(1+3+3+0=7=N/q\) ✓; \(0+6+0+1=7\) ✓;
\(\alpha_j(1)+4\alpha_j(0)=|P_j|\) for each \(j\): \(0+4=4\), \(6+12=18\),
\(0+12=12\), \(1+0=1\) ✓.  Independent geometric check in the Fano plane: two
lines always meet in exactly one point, so a line \(M\in C_a\) has
\(\alpha_1=6,\alpha_0=\alpha_2=0\) ✓; a non-line triple has exactly one line in
its complementary \(4\)-set, so \(\alpha_0=1\) ✓.

Stabilizer partitions \(m\le k-2=2\): \(m=1\) gives cells of sizes
\(\binom62=15,\binom63=20\), both divisible by \(5\) ✓; \(m=2\) gives
\(\binom{5}{3}=10,2\binom52=20,\binom51=5\), all divisible by \(5\) ✓.

**Control value:** the stabilizer- and distance-partition conditions computed
here are satisfiable by nonnegative integers at \(k=4\), where the answer is
known to be *no*.  Feasibility of these projected numerical systems therefore
does not imply existence.  The singleton system is not feasible: by Theorem
4(2), it is the original large-set problem.

### 9.3 \(k=6\): no large set, yet the system is feasible

\(v=11\), \(r=5\), \(N=462\), \(q=7\), \(|C_a|=66\).  Perfect codes are the Witt
systems \(S(4,5,11)\); Kramer--Mesner proved at most **two** are mutually
disjoint, short of \(7\), so **no \(LS(4,5,11)\) exists**.

| \(j\) | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| \(\lvert P_j\rvert\) | 6 | 75 | 200 | 150 | 30 | 1 |
| \(\alpha_j\ (M\notin C_a)\) | 1 | 10 | 30 | 20 | 5 | 0 |
| \(\alpha_j\ (M\in C_a)\) | 0 | 15 | 20 | 30 | 0 | 1 |

Checks: \(6+75+200+150+30+1=462\) ✓; both \(\alpha\) rows sum to \(66\) ✓;
\(\alpha_j(1)+6\alpha_j(0)=|P_j|\) for each \(j\): \(6,\,15+60=75,\,20+180=200,\,
30+120=150,\,0+30=30,\,1\) ✓.  Cross-check against the Möbius form with
\(\lambda_0,\dots,\lambda_4=66,30,12,4,1\) reproduces the same two rows ✓.

**Control value:** identical to \(k=4\).  Note also \(\alpha_{k-2}=\alpha_4=0\)
when \(M\in C_a\), which is just "two blocks share at most \(k-3\) points"; the
system predicts it, and it is a single-block fact.

### 9.4 \(k=16\)

\(v=31\), \(r=15\), \(q=17\).  Theorem 6/7 give \(17\mid|P_j|\) for every cell of
every stabilizer partition with \(m\le14\); Theorem 8.1 gives a nonnegative
integral solution of the distance-partition system.  **No condition in the whole
system is violated at \(k=16\).**  (No numerical table is stated here: the
binomials were not computed in this session, and Theorems 6--8.1 are proved
symbolically for all admissible \(k\), so no numerical instance is needed.)

---

## 10. The second-order conditions (Gram sandwich and rank bound) are also closed

Write \(Y=[y_1|\cdots|y_q]\in\mathbb R^{N\times q}\).

**Lemma 10.0.**  \(Y^{\mathsf T}Y=\frac Nq\bigl(I_q-\frac1qJ_q\bigr)\) and
\(Y\mathbf1_q=0\).

*Proof.*  \(\langle y_a,y_b\rangle=|C_a\cap C_b|-\frac{|C_a|+|C_b|}q+\frac N{q^2}
=\delta_{ab}\frac Nq-\frac N{q^2}\).  \(\square\)

**Proposition 10.1 (Gram sandwich).**  For every equitable \(\pi\), with
\(Z=T-\frac1qJ_{m\times q}\),
\[
 G_\pi:=Z^{\mathsf T}D_\pi Z=Y^{\mathsf T}\Pi_{U_\pi}Y,\qquad
 0\preceq G_\pi\preceq \frac Nq\Bigl(I_q-\frac1qJ_q\Bigr),\qquad G_\pi\mathbf1_q=0 .
\]
Explicitly \((G_\pi)_{ab}=\sum_i\frac{|P_i\cap C_a||P_i\cap C_b|}{|P_i|}-\frac Nq\).

*Proof.*  From the proof of Theorem 4(1), \(\Pi_{U_\pi}y_a=\sum_iZ_{ia}u_i\), so
\(\langle\Pi_{U_\pi}y_a,\Pi_{U_\pi}y_b\rangle=\sum_i|P_i|Z_{ia}Z_{ib}=(Z^{\mathsf T}D_\pi Z)_{ab}\),
and also \(=\langle y_a,\Pi_{U_\pi}y_b\rangle\) since \(\Pi\) is an orthogonal
projector.  Then \(0\preceq Y^{\mathsf T}\Pi Y\preceq Y^{\mathsf T}Y\) because
\(\Pi\) and \(I-\Pi\) are both positive semidefinite.  The explicit entries follow
by expanding and using \(\sum_i|P_i\cap C_a|=N/q\).  \(\square\)

**Proposition 10.2 (rank and deviation bounds).**
\(\operatorname{rank}Z=\operatorname{rank}G_\pi\le\min(\varepsilon_\pi,\,q-1)\), and
for all \(i,a\),
\[
 \Bigl|\,|P_i\cap C_a|-\frac{|P_i|}q\,\Bigr|
 \le\bigl\|\Pi_{V_{k-1}}\mathbf1_{P_i}\bigr\|\cdot\sqrt{\frac Nq\cdot\frac{q-1}{q}} .
\]

*Proof.*  Columns of \(Z\) lie in \(\ker(B_\pi+I)\) of dimension
\(\varepsilon_\pi\) (Theorem 3), and \(Z\mathbf1_q=0\) bounds the column rank by
\(q-1\).  For the second bound,
\(|P_i\cap C_a|-\frac{|P_i|}q=\langle\mathbf1_{P_i},y_a\rangle
=\langle\Pi_{V_{k-1}}\mathbf1_{P_i},y_a\rangle\) since \(y_a\in V_{k-1}\); apply
Cauchy--Schwarz and \(\|y_a\|^2=\frac Nq(1-\frac1q)\) (Lemma 10.0).  \(\square\)

**Corollary 10.3.**  (S4) and (S5) are consequences of DQ alone (each uses only
\(y_a\in V_{k-1}\) and Lemma 10.0), so Theorem 4 applies to them verbatim: they
are covered by the closure and are not new constraints.

---

## 11. The first genuinely new constraint: a two-colour transport identity

Theorem 5 says the whole equitable-partition package is single-class.  The
cheapest thing lying strictly outside it is a condition that couples **two**
colour classes.  This section constructs one, proves it exactly, and evaluates
it.

**Definition.**  For distinct colours \(a,a'\) and \(u\in C_a\), let
\(\sigma_{a'}(u)\) be the unique neighbour of \(u\) lying in \(C_{a'}\).
(It exists and is unique: \(C_{a'}\) is a perfect code, so the closed ball of
\(u\) meets \(C_{a'}\) exactly once, and \(u\notin C_{a'}\).)  Then
\(\sigma_{a'}:C_a\to C_{a'}\) is a bijection with inverse \(\sigma_a\).

Fix a vertex \(M\in X\) and the distance partition \(\pi_M\) of §8, with cells
\(P_j=\{S:|S\cap M|=j\}\).  Set \(P_{-1}=\varnothing\), write
\(\alpha_j(a)=|P_j\cap C_a|\) as in Theorem 8, and define

\[
 x_i^{a,a'}:=\#\bigl\{u\in P_i\cap C_a\ :\ \sigma_{a'}(u)\in P_{k-2-i}\bigr\},
 \qquad 0\le i\le k-1 .
\]

**Lemma 11.1 (two-level structure).**  For \(u\in P_i\), every neighbour of
\(u\) lies in \(P_{k-2-i}\cup P_{k-1-i}\); precisely, the neighbour obtained by
deleting the point \(y\in[v]\setminus u\) lies in \(P_{k-2-i}\) if \(y\in M\)
and in \(P_{k-1-i}\) otherwise.  There are \(k-1-i\) neighbours of the first
kind and \(i+1\) of the second.

*Proof.*  The neighbours of \(u\) are exactly the \((k-1)\)-subsets of the
\(k\)-set \([v]\setminus u\), i.e. \(([v]\setminus u)\setminus\{y\}\).  Then
\(|T\cap M|=|M\setminus u|-[y\in M]=(k-1-i)-[y\in M]\).  Also
\(|([v]\setminus u)\cap M|=k-1-i\) and
\(|([v]\setminus u)\setminus M|=k-(k-1-i)=i+1\).  \(\square\)

**Theorem 11 (transport identity and the resulting inequality).**  Assume
\(\tau\) is a partition of \(O_k\) into \(q\) perfect codes.  Then for all
distinct colours \(a,a'\), all \(M\in X\) and all \(0\le i\le k-1\),

\[
 \boxed{\;x_i^{a,a'}=\sum_{t=0}^{i}\Bigl[\alpha_t(a)-\alpha_{k-1-t}(a')\Bigr]\;}
 \tag{11.1}
\]

and consequently the **two-colour necessary condition**

\[
 \boxed{\;0\;\le\;\sum_{t=0}^{i}\Bigl[\alpha_t(a)-\alpha_{k-1-t}(a')\Bigr]\;\le\;\alpha_i(a)
 \qquad(0\le i\le k-1).\;}
 \tag{11.2}
\]

Writing \(\epsilon_a=[M\in C_a]\), \(\delta=\epsilon_a+\epsilon_{a'}\in\{0,1\}\),
the closed form of (11.1) is

\[
 x_i^{a,a'}
 =\frac1q\sum_{t=0}^{i}\binom{k-1}{t}\Bigl[\binom{k}{k-1-t}-\binom kt\Bigr]
   -\Bigl(\delta-\frac2q\Bigr)(-1)^i\binom{k-2}{i}.
 \tag{11.3}
\]

*Proof.*  By Lemma 11.1, \(\sigma_{a'}\) maps \(P_i\cap C_a\) into
\(P_{k-2-i}\cup P_{k-1-i}\), with exactly \(x_i^{a,a'}\) images in
\(P_{k-2-i}\) and \(\alpha_i(a)-x_i^{a,a'}\) images in \(P_{k-1-i}\); in
particular \(0\le x_i^{a,a'}\le\alpha_i(a)\), which is (11.2) once (11.1) is
proved.  Since \(\sigma_{a'}\) is a bijection onto \(C_{a'}\), counting the
preimage of \(P_{j'}\cap C_{a'}\) — whose contributions come from \(i\) with
\(k-2-i=j'\) and from \(i\) with \(k-1-i=j'\) — gives
\[
 \alpha_{j'}(a')=x_{k-2-j'}^{a,a'}+\Bigl(\alpha_{k-1-j'}(a)-x_{k-1-j'}^{a,a'}\Bigr).
\]
Substituting \(j'=k-1-i\) yields
\(x_i^{a,a'}=x_{i-1}^{a,a'}+\alpha_i(a)-\alpha_{k-1-i}(a')\) for \(0\le i\le k-1\)
with \(x_{-1}^{a,a'}:=0\); telescoping gives (11.1).

For (11.3) use Theorem 8: \(\alpha_t(a)=\frac{|P_t|}q+w_t(\epsilon_a-\frac1q)\)
with \(w_t=(-1)^{k-1-t}\binom{k-1}t\).  Since \(k\) is even,
\(w_{k-1-t}=(-1)^{t}\binom{k-1}{t}=-w_t\), so
\[
 \alpha_t(a)-\alpha_{k-1-t}(a')
 =\frac{|P_t|-|P_{k-1-t}|}{q}-(-1)^t\binom{k-1}t\Bigl(\epsilon_a+\epsilon_{a'}-\frac2q\Bigr),
\]
and \(|P_t|-|P_{k-1-t}|=\binom{k-1}t\bigl[\binom k{k-1-t}-\binom kt\bigr]\) because
\(\binom{k-1}{k-1-t}=\binom{k-1}t\).  Summing over \(t\le i\) and using
\(\sum_{t=0}^i(-1)^t\binom{k-1}t=(-1)^i\binom{k-2}i\) gives (11.3).  \(\square\)

**Remark 11.2 (why this is outside the closure).**  (11.2) involves
\(\alpha_\bullet(a)\) and \(\alpha_\bullet(a')\) simultaneously; it is not of the
form (4.1) for any equitable \(\pi\), and by Theorem 5 it cannot be produced by
the two-equitable-partition system.  Its input is the perfect-code *matching*
\(\sigma_{a'}\), which is exactly the "coupling" datum §5 shows the system
lacks.  It is a relative of, but not the same as, the fibre-Schreier relation
\(R\) of `erdos_835_conjectural_resolution.md` §7.3, which lives on one colour
class and uses triangles of \(K_q\); (11.2) uses one vertex of \(O_k\) and an
ordered pair of colours.

**Symmetry.**  Lemma 11.1 applied from the other side gives
\(x_i^{a,a'}=x_{k-2-i}^{a',a}\) and
\(\alpha_i(a)-x_i^{a,a'}=\alpha_{k-1-i}(a')-x_{k-1-i}^{a',a}\); so the condition
for the ordered pair \((a',a)\) is equivalent to that for \((a,a')\).

**Theorem 11.3 (evaluation of (11.2) at \(k=4,6,10\)).**  For \(k\in\{4,6,10\}\)
(all admissible: \(q=5,7,11\) prime), condition (11.2) holds for every ordered
pair of distinct colours and every vertex \(M\), in all three cases
\((\epsilon_a,\epsilon_{a'})\in\{(0,0),(1,0),(0,1)\}\).  It is therefore **not**
an obstruction at these \(k\).

*Proof (exhibited values; all entries hand-computed from Theorem 8 and (11.1),
and each row cross-checked against \(\sum_i\alpha_i=N/q\)).*

\(k=4\), \(q=5\); \(\alpha(\epsilon{=}0)=(1,3,3,0)\), \(\alpha(\epsilon{=}1)=(0,6,0,1)\):

| \((\epsilon_a,\epsilon_{a'})\) | \(x_0,\dots,x_3\) | bounds \(\alpha_i(a)\) |
|---|---|---|
| \((0,0)\) | \(1,1,1,0\) | \(1,3,3,0\) |
| \((1,0)\) | \(0,3,0,0\) | \(0,6,0,1\) |
| \((0,1)\) | \(0,3,0,0\) | \(1,3,3,0\) |

\(k=6\), \(q=7\); \(\alpha(0)=(1,10,30,20,5,0)\), \(\alpha(1)=(0,15,20,30,0,1)\):

| \((\epsilon_a,\epsilon_{a'})\) | \(x_0,\dots,x_5\) | bounds \(\alpha_i(a)\) |
|---|---|---|
| \((0,0)\) | \(1,6,16,6,1,0\) | \(1,10,30,20,5,0\) |
| \((1,0)\) | \(0,10,10,10,0,0\) | \(0,15,20,30,0,1\) |
| \((0,1)\) | \(0,10,10,10,0,0\) | \(1,10,30,20,5,0\) |

\(k=10\), \(q=11\); \(\alpha(0)=(1,36,396,1596,2898,2394,924,144,9,0)\),
\(\alpha(1)=(0,45,360,1680,2772,2520,840,180,0,1)\) (both sum to
\(\binom{19}{9}/11=8398\)):

| \((\epsilon_a,\epsilon_{a'})\) | \(x_0,\dots,x_9\) |
|---|---|
| \((0,0)\) | \(1,28,280,952,1456,952,280,28,1,0\) |
| \((1,0)\) | \(0,36,252,1008,1386,1008,252,36,0,0\) |
| \((0,1)\) | \(0,36,252,1008,1386,1008,252,36,0,0\) |

Every entry satisfies \(0\le x_i\le\alpha_i(a)\).  The equality cases, at all
three \(k\), are \(x_0=\alpha_0=1\) in row \((0,0)\), \(x_0=\alpha_0=0\) in row
\((1,0)\), and \(x_1=\alpha_1\) in row \((0,1)\); note also that by (11.3)
\(x_i\) depends on \((\epsilon_a,\epsilon_{a'})\) only through
\(\delta=\epsilon_a+\epsilon_{a'}\), which is why rows \((1,0)\) and \((0,1)\)
coincide while their bounds differ.  \(\square\)

**Theorem 11.4 (uniform feasibility; the scalar transport route closes).**
Let \(k\ge2\) be even and \(q=k+1\) prime.  For every \(0\le i\le k-1\) and
every possible ordered-pair case
\((\epsilon_a,\epsilon_{a'})\in\{(0,0),(1,0),(0,1)\}\), the forced value in
(11.1) is a nonnegative integer and satisfies
\[
0\le x_i^{a,a'}\le\alpha_i(a).
\]
Thus (11.2) is never an obstruction at any admissible \(k\).

*Proof.*  Put
\[
 C_i=\binom{k-1}{i},\qquad B_i=\binom{k-2}{i},\qquad
 D_i=\binom{k}{i+1},\qquad s_i=(-1)^i,
\]
with the convention \(B_{k-1}=0\).  First, the binomial part of (11.3)
telescopes:
\[
\begin{aligned}
 S_i
 &:=\sum_{t=0}^{i}\binom{k-1}{t}
       \left[\binom{k}{t+1}-\binom{k}{t}\right]\\
 &=\frac{k-1-i}{i+1}\binom{k-1}{i}^{2}.                 \tag{11.4}
\end{aligned}
\]
Indeed the right side is \(k-1\) at \(i=0\), and its difference from the
same expression at \(i-1\) is
\[
 C_i^2\left(\frac{k-1-i}{i+1}-\frac{i}{k-i}\right)
 =C_i\left[\binom{k}{i+1}-\binom{k}{i}\right].
\]
For \(i\le k-2\),
\[
B_i=\frac{k-1-i}{k-1}C_i,\qquad
\frac{S_i}{B_i}=\frac{k-1}{k}D_i.
\]
Consequently (11.3), with
\(\delta=\epsilon_a+\epsilon_{a'}\), becomes
\[
\boxed{\quad
x_i^{a,a'}=\frac{B_i}{q}
\left[\frac{k-1}{k}D_i+(2-q\delta)s_i\right].
\quad}                                                   \tag{11.5}
\]
This is also valid at \(i=k-1\), where both sides are zero.  Integrality
follows independently from (11.1) and Theorem 8.1.

For nonnegativity, when \(\delta=0\) only odd \(i\) needs checking; then
\(\frac{k-1}{k}D_i\ge (k-1)^2/2\ge2\) (and the \(k=2\) range is empty).
When \(\delta=1\), only even \(i\) needs checking; then
\(\frac{k-1}{k}D_i\ge k-1\).  Hence (11.5) is nonnegative in all cases.

It remains to prove the upper bound.  Theorem 8 can be written
\[
\alpha_i(0)=\frac{C_i}{q}(D_i+s_i),\qquad
\alpha_i(1)=\frac{C_i}{q}(D_i-ks_i).
\]
Using (11.5) and \((i+1)D_i/k=C_i\), direct subtraction gives
\[
\begin{array}{rcl}
(\epsilon_a,\epsilon_{a'})=(0,0):
&\displaystyle \alpha_i(a)-x_i
=\frac{C_i}{q}\left(C_i+s_i\frac{2i-k+1}{k-1}\right),\\[6pt]
(1,0):
&\displaystyle \alpha_i(a)-x_i
=\frac{C_i}{q}\left(C_i-(i+1)s_i\right),\\[6pt]
(0,1):
&\displaystyle \alpha_i(a)-x_i
=\frac{C_i}{q}\left(C_i+(k-i)s_i\right).
\end{array}                                             \tag{11.6}
\]
The first bracket is nonnegative because
\(\lvert2i-k+1\rvert\le k-1\) and \(C_i\ge1\).  In the second, the only
nontrivial case has even \(i\); then \(i\le k-2\) and
\(C_i\ge i+1\) (equality is allowed at the boundary).  In the third, the
only nontrivial case has odd \(i\); then \(C_i\ge k-i\), again with equality
allowed at the boundary.  Therefore every expression in (11.6) is
nonnegative, proving \(x_i\le\alpha_i(a)\).  \(\square\)

**Status of (11.2).**  It is a valid two-colour necessary condition, but
Theorem 11.4 proves it feasible for every admissible parameter.  A stronger
transportation-polytope condition using a sparser auxiliary quotient, or a
condition coupling at least three colours, would be needed to continue this
route.

---

## 12. Statements *not* proved here

Listed so that nothing above is over-read.

1. **No nonexistence result for any \(k\) is proved.**  Theorems 4, 5, 6, 7, 8.1
   are statements about the *method*; they show the route cannot fire.  #835 is
   untouched by them.
2. **No construction is produced.**  Feasibility of (3.1)--(3.2) with nonnegative
   integers (Theorem 8.1) is a property of a numerical matrix system, not of any
   family of sets.  §9.2 and §9.3 are explicit witnesses that feasibility here
   coexists with proved nonexistence.
3. **I did not read arXiv:2605.17376.**  No statement in this file is attributed
   to Bailey--Cameron--Zhou.  Theorem 4 closes the constraint system derived in
   §§1--3 and §10; if their Theorem 2.3 or Corollary 2.4(b) uses data outside
   \((B_\pi,B_\tau,S)\) — e.g. triple intersections \(|P\cap C_a\cap C_b|\),
   a normal-Cayley group-algebra decomposition, or a non-equitable common
   refinement — then this file does not close it.  §5 identifies exactly which
   extra data would be needed: something that couples **two** colour classes,
   and §11 constructs and proves one such condition.
3b. **Condition (11.2) is feasible for all admissible \(k\).**  Theorem 11.4
   proves this uniformly.  This closes only the scalar distance-transport
   inequality, not general two-colour transportation constraints.
4. **Nothing about normal Cayley graphs is used or claimed.**  I did not
   determine whether \(O_k\) is a Cayley graph.
5. **Wilson's diagonal form is cited, not reproved** (§6, step (b)).  It is
   already in the repository's source list.  Theorem 7 gives an independent
   elementary proof of the same conclusion for the stabilizer family, so §6 is
   not the only support for the \(\varepsilon=0\) closure.
6. **The nonexistence of \(LS(2,3,7)\) and \(LS(4,5,11)\)** used in §9 is quoted
   from the repository (`verify_k4.py`, Kramer--Mesner), not proved here.
7. **No computation was executed in this session.**  Python and network access
   were both refused by the permission layer.  `verify_bcz_odd_graph.py` is
   provided as a redundant independent check and was **not run**; every theorem
   above is proved by hand and every numerical table in §9 was hand-computed
   twice by two different routes (Möbius inversion and the closed form).

# The joint \(Q\)-leakage attack collapses: total intersection rigidity at \(k=16\)

## 0. Scope, in unmistakable language

**Erdős–Rosenfeld problem #835 remains OPEN.**  This note contains no
construction and no all-parameter proof.  It does not exclude the \(k=16\)
cover.  Even if it had, excluding \(k=16\) alone would still not settle the
existential problem #835.

What this note does contain, all of it conditional on the assumed cover:

1. A **new exact rigidity theorem** (Theorem B): under the standing
   hypotheses, *every* fibre intersection matrix \(A_s\), \(s=1,\dots,13\),
   acts as an integer scalar on the pair module \({\cal H}_2\) and on the
   point module \({\cal H}_1\).
2. As the special case that the assigned target asked for: the leakage
   operator
   \[
   L=(I-P_2)A_{13}P_2
   \]
   is **identically zero**, hence \((I-P_2)QP_2=0\) as well.  The identity
   \((I-P_2)QP_2=-5(I-P_2)A_{13}P_2\) is true but vacuous — both sides are
   the zero matrix.  Consequently
   \(\operatorname{tr}(P_2A_{13}^2P_2)=434\cdot449^2=87\,494\,834\)
   **exactly**, with zero slack, and no bound on it is needed.
3. A **proved no-go theorem** (Theorem C) for the entire quadratic-leakage
   class, with an exact statement of what is exhausted: the smallest
   complete positive-semidefinite block moment matrix of the forced system
   has exactly **one** free entry, its PSD bound on that entry is *strictly
   weaker* than the trivial entrywise bound, and the Gram matrix of the
   restrictions \(A_s|_{\cal K}\) is degenerate of corank exactly two with a
   kernel that is forced by the Johnson kernels themselves.  No strict
   inequality survives anywhere in the class.
4. A genuine **improvement** of the published fourth-moment interval as a
   by-product (Section 8): \(\operatorname{tr}R^4\le48\,840n\) and
   \(\#C_4(R)\le2520n\), replacing \(65\,640n\) and \(4620n\).
5. The identification of the **first genuinely unforced mixed statistic**
   and its exact local combinatorial meaning (Section 8).

Everything numerical is audited by the exact standard-library verifier
`verify_joint_schreier_krein_attack.py` beside this note (143 checks, Ruff
clean).

**Correction recorded (this revision).**  An earlier draft of Lemma 8.3 stated
the diagonal-pair condition backwards ("intersection \(12\) iff the omitted
points coincide") and defined \(\varepsilon\) with an equality indicator.
The correct statement is the opposite: the diagonal pair
\(\{B_{11},B_{22}\}\) has intersection \(12\) iff \(w_{11}\ne w_{22}\),
because the two blocks then omit two *different* points of the \(14\)-set
\(W'\).  Section 8.1 now proves every one of the ten intersections
explicitly, \(\varepsilon\) is defined with inequality indicators, and the
verifier constructs labelled \(W',U,V\) blocks for both the equal and the
distinct omitted-point cases and asserts the actual sizes, in the abstract
model and on the real \(k=6\) cover.  All displayed numerical bounds are
unchanged, because they depend only on \(\varepsilon\le2\).

---

## 1. Standing hypotheses, rederived, with the hidden assumptions flagged

Assume a covering map (a surjective **local isomorphism**, not merely a
homomorphism)
\[
O_{16}=KG(31,15)\longrightarrow K_{17}.
\]
Both graphs are \(16\)-regular.  Fix one fibre \({\cal C}\).

**(H0) Equal fibres.**  \(K_{17}\) is connected, so all \(17\) fibres of a
covering map have the same cardinality; hence
\(n=|{\cal C}|=\binom{31}{15}/17=17\,678\,835\).
*This is where local bijectivity is used, and it is not optional: the Kneser
graph \(KG(31,15)\) has chromatic number \(3\), so a mere homomorphism to
\(K_{17}\) exists trivially and carries no information.*

**(H1) No fibre pair at intersection \(0\).**  Fibres are independent sets.

**(H2) No fibre pair at intersection \(14\).**  If \(|B\cap C|=14\) then
\(B,C\) are two of the sixteen \(15\)-subsets of the \(16\)-set \(Y=B\cup C\).
Those sixteen sets are exactly the \(O_{16}\)-neighbours of the block
\([31]\setminus Y\), so local bijectivity puts them in sixteen *distinct*
fibres.  Hence \(B\) and \(C\) lie in different fibres.

**(H3) \({\cal C}\) is a Steiner system \(S(14,15,31)\).**  By (H2) no
\(14\)-set lies in two blocks of \({\cal C}\); each block contains
\(\binom{15}{14}=15\) of them; and
\(15n=265\,182\,525=\binom{31}{14}\).  So every \(14\)-set lies in exactly
one block.  *This is the only place the exact fibre size is consumed, and it
is the invariance assumption that all later Johnson-kernel arithmetic rests
on.  It is proved, not assumed.*

Write \(A_s\) for the \(0/1\) fibre matrix of block intersection \(s\)
(\(s=1,\dots,13\); \(A_0=A_{14}=0\) by (H1)–(H2)), \(R=A_1\),
\({\cal A}\) for the adjacency matrix of \(O_{16}\), \(\iota\) for extension
by zero from \({\cal C}\), \(E_j\) for the Johnson/Odd spectral idempotent at
\[
\theta_j=(-1)^j(16-j),
\]
and \(m_j=\dim{\cal H}_j\), so \(m_0=1,\ m_1=30,\ m_2=434\).
\(P_j\) is the orthogonal projector of \(\mathbb R^{\cal C}\) onto
\({\cal H}_j\); by (H3) and strength \(14\),
\[
\iota^*E_j\iota=\tfrac1{17}P_j\qquad(0\le j\le7).
\tag{1.1}
\]

**Intersection numbers.**  Solving the triangular system
\(\sum_sC(s,i)n_s=\binom{15}{i}(\lambda_i-1)\), \(\lambda_i=\binom{31-i}{14-i}/\binom{15-i}{14-i}\):

| \(s\) | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| \(n_s\) | 120 | 3360 | 49140 | 349440 | 1417416 | 3363360 | 4877730 |

| \(s\) | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|
| \(n_s\) | 4324320 | 2362360 | 768768 | 147420 | 14560 | 840 |

with \(\sum_{s=1}^{13}n_s=n-1\).

**Odd walk compressions.**  From \({\cal A}D_d=b_{d-1}D_{d-1}+c_{d+1}D_{d+1}\)
(the Odd graph has \(a_d=0\) below the diameter; \(b_{2j}=k-j\), \(c_{2j}=j\),
\(b_{2j+1}=k-1-j\), \(c_{2j+1}=j+1\)), and the dictionary
\(D_{2t}\leftrightarrow\) intersection \(15-t\),
\(D_{2t+1}\leftrightarrow\) intersection \(t\), the classes \(D_1\)
(intersection \(14\)) and \(D_{15}\) (intersection \(0\)) die on the fibre and
\[
\boxed{
\begin{aligned}
\iota^*\iota&=I, &\iota^*{\cal A}\iota&=0,
&\iota^*{\cal A}^2\iota&=16I, &\iota^*{\cal A}^3\iota&=2R,\\
\iota^*{\cal A}^4\iota&=496I+4A_{13},
&\iota^*{\cal A}^5\iota&=178R+12A_2,
\end{aligned}}
\tag{1.2}
\]
\[
\iota^*{\cal A}^6\iota=22\,576I+524A_{13}+36A_{12}.
\tag{1.3}
\]

**\(R\)-invariance of \({\cal H}_1,{\cal H}_2\).**  As in the committed
Schreier note: the \(R\)-neighbours of \(B\) are \(D_e=(Y\setminus e)\cup\{\phi_B(e)\}\)
for the \(\binom{16}{2}\) edges \(e\) of \(Y=[31]\setminus B\), with \(\phi_B\)
a one-factorisation of \(K_Y\); this gives \(Rf_p\) and \(Rf_S\) in closed
form, hence
\[
RP_1=-97P_1,\qquad RP_2=77P_2,\qquad R\mathbf1=120\mathbf1.
\tag{1.4}
\]

**Two-step algebra.**  \(R^2=120I+5A_{13}+Q\) with
\(\operatorname{supp}Q\subseteq A_{12}\), \(Q_{BC}\in\{0,1,2,3\}\),
\(Q\mathbf1=10\,080\,\mathbf1\).

*Flagged and used nowhere else:* no step below assumes that \(A_{13}\),
\(A_{12}\) or \(Q\) preserves \({\cal H}_2\).  That is the conclusion, and it
is proved.  No entrywise inequality is ever promoted to Loewner order.

---

## 2. Support theorems

For a unit \(x\in{\cal H}_j\) put \(y=\iota x\) and let
\(m_p=\langle{\cal A}^p\rangle_y\).  By (1.1)–(1.2) and (1.4),
\(m_0=1,\ m_1=0,\ m_2=16\), and \(m_3=2\mu_j\) with \(\mu_1=-97\),
\(\mu_2=77\).  By (1.1) the global measure of \(y\) has mass \(1/17\) at
\(\theta_j\) and no mass at any other \(\theta_{j'}\) with \(j'\le7\); the
residual points are
\(\theta_8,\dots,\theta_{15}=8,-7,6,-5,4,-3,2,-1\).

### 2.1 The point module: a new degree-two certificate

Take
\[
q(t)=(t-2)(t+1).
\]
On the eight residual points \(q\) takes the values
\(54,54,28,28,10,10,0,0\): nonnegative, with zeros exactly at \(2\) and
\(-1\).  Since \(\deg q=2\), \(\langle q\rangle_y=m_2-m_1-2=14\) is
determined by \(\iota^*{\cal A}^p\iota\) for \(p\le2\) alone — no use of
\(R\).  The fixed mass contributes \(q(-15)/17=238/17=14\).  Hence the
residual measure integrates \(q\) to zero and

\[
\boxed{\iota{\cal H}_1\subseteq E_1\oplus E_{14}\oplus E_{15},\qquad
\text{measure }\ \tfrac1{17}\delta_{-15}+\tfrac{31}{51}\delta_{2}
+\tfrac13\delta_{-1}.}
\tag{2.1}
\]

The three weights are forced by \(m_0,m_1,m_2\) only.  As an independent
consistency test the measure then *predicts* \(m_3=-194=2\cdot(-97)\),
recovering the \({\cal H}_1\) eigenvalue of \(R\) — which was derived from the
one-factorisation, i.e. from a completely different argument.  This support
theorem is new; the committed notes treat only \({\cal H}_2\).

### 2.2 The pair module

Rederived exactly as in the committed follow-up.  With
\(h(t)=\frac15(5t-6)(t+3)(t-2)(t+1)=t^4+\frac45t^3-\frac{37}5t^2+\frac{36}5\),
\(h\ge0\) on the residual points with zeros exactly \(\{-3,2,-1\}\), so
\(m_4\ge2292\) pointwise; the Johnson kernel of \(P_2\) gives
\(\operatorname{tr}(P_2A_{13})=434\cdot449\) hence average \(m_4=2292\)
exactly; therefore equality holds pointwise and

\[
\boxed{\iota{\cal H}_2\subseteq E_2\oplus E_{13}\oplus E_{14}\oplus E_{15},
\qquad\text{measure }\ \tfrac1{17}\delta_{14}+\tfrac{29}{85}\delta_{-3}
+\tfrac4{15}\delta_{2}+\tfrac13\delta_{-1}.}
\tag{2.2}
\]

(The verifier recomputes \(\operatorname{tr}(P_2A_{13})=194\,866=434\cdot449\)
from the Eberlein kernel independently.)

---

## 3. Theorem A: the leakage is identically zero

> **Theorem A.**  \(A_{13}P_2=449P_2\).  Equivalently
> \(L=(I-P_2)A_{13}P_2=0\), \(\|L\|_F=0\), and
> \[
> \operatorname{tr}(P_2A_{13}^2P_2)=434\cdot449^2=87\,494\,834
> \]
> **exactly**.  Consequently \((I-P_2)QP_2=-5L=0\) and \(QP_2=3564P_2\).

*Proof.*  Let \(x\in{\cal H}_2\) and \(y=\iota x\).  By (2.2), \(y\) lies in
the span of the four eigenspaces with \(\theta\in\Theta=\{14,-3,2,-1\}\).
Let \(p_\theta\) be the Lagrange polynomial on \(\Theta\), so
\(\deg p_\theta=3\) and \(F_\theta y=p_\theta({\cal A})y\), where
\(F_\theta\) is the global spectral projector at \(\theta\).

Because \(\iota^*{\cal A}^p\iota\in\{I,0,16I,2R\}\) for \(p=0,1,2,3\) by
(1.2), the compression \(\iota^*p_\theta({\cal A})\iota\) is an
\(\mathbb R\)-linear combination \(\alpha_\theta I+\beta_\theta R\).  By (1.4)
\(R\) acts on \({\cal H}_2\) as \(77\), so
\[
\iota^*F_\theta\iota\,x=(\alpha_\theta+77\beta_\theta)\,x=w_\theta x ,
\tag{3.1}
\]
a **scalar multiple of \(x\)**, with \(w_\theta\) the weight in (2.2)
(the identification \(\alpha_\theta+77\beta_\theta=w_\theta\) is forced by
\(\langle x,\iota^*F_\theta\iota x\rangle=\|F_\theta y\|^2=w_\theta\); the
verifier evaluates all four Lagrange compressions and confirms
\(1/17,\,29/85,\,4/15,\,1/3\)).

Therefore, for *every* polynomial \(g\),
\[
\boxed{\iota^*g({\cal A})\iota\,x
=\Bigl(\sum_{\theta\in\Theta}g(\theta)w_\theta\Bigr)x
=m_{g}\,x.}
\tag{3.2}
\]
Taking \(g(t)=t^4\) and using \(\iota^*{\cal A}^4\iota=496I+4A_{13}\) from
(1.2) gives \(496x+4A_{13}x=2292x\), i.e. \(A_{13}x=449x\).  Polarisation is
unnecessary: this is already an identity of operators on \({\cal H}_2\).
The rest follows from \(R^2P_2=77^2P_2=5929P_2\):
\[
5A_{13}P_2+QP_2=(5929-120)P_2=5809P_2,
\qquad 5\cdot449+3564=5809 .
\tag{3.3}
\]
\(\square\)

**Answer to the assigned target.**  The requested Frobenius/operator leakage
information for \(L\) is: \(L=0\).  \(\operatorname{tr}(P_2A_{13}^2P_2)\) is
not merely boundable from the forced intersection data, it is *determined*,
and the interval collapses to the single point \(87\,494\,834\).  The stated
identity \((I-P_2)QP_2=-5(I-P_2)A_{13}P_2\) is correct and is a corollary of
the strictly stronger (3.3); it is vacuous because both sides vanish.

**Every mixed \(P_2\)-compression is now a product of scalars**, e.g.
\[
P_2Q^2P_2=3564^2P_2=12\,702\,096\,P_2,\qquad
P_2A_{13}QP_2=449\cdot3564\,P_2=1\,600\,236\,P_2 .
\]
There is nothing left to bound with Cauchy–Schwarz or variance inequalities
inside this block.  For the record, the rowwise Cauchy test is satisfied with
a factor-\(97\) margin: \(\|P_2q^B\|^2=3564^2\cdot434/n=19\,758\,816/63\,365
=311.825\ldots\) against \(\|q^B\|^2\le3\cdot10\,080=30\,240\).

---

## 4. Theorem B: total intersection rigidity

> **Theorem B.**  For every \(s\in\{1,\dots,13\}\),
> \[
> A_sP_2=a_sP_2,\qquad A_sP_1=b_sP_1,
> \]
> with \(a_s,b_s\in\mathbb Z\) given below.  Hence
> \({\cal F}={\cal H}_0\oplus{\cal H}_1\oplus{\cal H}_2\)
> (\(\dim{\cal F}=465\)) is invariant under every \(A_s\), and each \(A_s\)
> acts on each of the three modules by an integer scalar.

*Proof.*  \(A_s=\iota^*D_{15-s}\iota\) and \(D_i=\sum_jP_i(j)E_j\) with
\(P_i(j)\) the Eberlein polynomial of \(J(31,15)\).  By the support theorem
\(E_j\iota P_2=0\) for \(j\notin\{2,13,14,15\}\), and by (3.1)
\(\iota^*E_j\iota P_2=w_jP_2\) for \(j\in\{2,13,14,15\}\).  Therefore
\[
\boxed{a_s=\sum_{j\in\{2,13,14,15\}}P_{15-s}(j)\,w_j,\qquad
b_s=\sum_{j\in\{1,14,15\}}P_{15-s}(j)\,w'_j.}
\tag{4.1}
\]
\(\square\)

Rationality plus integrality of the matrices \(A_s\) forces
\(a_s,b_s\in\mathbb Z\); the verifier confirms this is satisfied, so **no
integrality contradiction is available**.

| \(s\) | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| \(a_s\) | 77 | 1488 | 13689 | 52000 | 75933 | \(-24024\) | \(-162591\) |
| \(b_s\) | \(-97\) | \(-2282\) | \(-27027\) | \(-147056\) | \(-413413\) | \(-546546\) | \(-162591\) |

| \(s\) | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|
| \(a_s\) | \(-108108\) | 42185 | 73216 | 30537 | 5148 | 449 |
| \(b_s\) | 414414 | 531531 | 272272 | 71253 | 8918 | 623 |

Independent checks, all exact:

* \(a_1=77\) and \(b_1=-97\) reproduce (1.4), which came from the
  one-factorisation, not from any measure;
* \(a_{13}=449\), \(a_2=1488\), \(a_{12}=5148\) reproduce the three scalars
  of the committed follow-up note;
* the forbidden classes come out zero: formula (4.1) at \(s=0\) and \(s=14\)
  gives \(0\) for both modules — a nontrivial cancellation
  (\(697/85-203/85-48/15-5=0\) for \(s=14\) on \({\cal H}_2\));
* \(\sum_{s=1}^{13}a_s=\sum_{s=1}^{13}b_s=-1\), as required by
  \(\sum_sA_s=J-I\) and \(JP_j=0\);
* \(|a_s|\le n_s\) and \(|b_s|\le n_s\) for every \(s\) (Perron);
* the walk route reproduces \(a_{13},a_2,a_{12}\) and \(b_{13},b_2,b_{12}\)
  from \(m_4,m_5,m_6\) via (1.2)–(1.3), i.e. two structurally different
  derivations agree.

**Corollary B1 (kernel entries).**  Reading \(A_sP_j=\mathrm{eig}^{(j)}_sP_j\)
at the diagonal entry \((B,B)\) gives
\(n_s(P_j)_{BC}\big|_{|B\cap C|=s}=\mathrm{eig}^{(j)}_s\cdot m_j/n\), i.e.
\[
p_j(s)=\frac{m_j}{n}\cdot\frac{\mathrm{eig}^{(j)}_s}{n_s}.
\tag{4.2}
\]
Combining with \(P_jP_{j'}=\delta_{jj'}P_j\) yields the exact orthogonality
identities
\[
\boxed{\sum_{s=1}^{13}\frac{(\mathrm{eig}^{(j)}_s)^2}{n_s}=\frac n{m_j}-1,
\qquad
\sum_{s=1}^{13}\frac{\mathrm{eig}^{(j)}_s\mathrm{eig}^{(j')}_s}{n_s}=-1
\quad(j\ne j').}
\tag{4.3}
\]
Numerically \(\sum_sb_s^2/n_s=1\,178\,587/2\) and
\(\sum_sa_s^2/n_s=570\,271/14\), matching \(n/30-1\) and \(n/434-1\).
These identities are the exact reason the quadratic tests of the next section
are saturated rather than strict.

---

## 5. What \(Q\) looks like on the forced module

From \(R^2P_j=\mu_j^2P_j\) and \(R^2=120I+5A_{13}+Q\):
\[
\boxed{Q\mathbf1=10\,080\,\mathbf1,\qquad QP_1=6174P_1,\qquad QP_2=3564P_2 ,}
\tag{5.1}
\]
and for the complementary nonnegative matrix
\[
(3A_{12}-Q)\mathbf1=33\,600\,\mathbf1,\quad
(3A_{12}-Q)P_1=20\,580P_1,\quad
(3A_{12}-Q)P_2=11\,880P_2 .
\tag{5.2}
\]
All six scalars respect the Perron bound of their own matrix, with the
tightest ratio \(3564/10\,080=0.3536\ldots\).  So
\[
\operatorname{tr}(Q|_{\cal F}^2)=10\,080^2+30\cdot6174^2+434\cdot3564^2
=6\,757\,864\,344 .
\tag{5.3}
\]

---

## 6. Theorem C: the quadratic-leakage class is exhausted, with proof

Let \({\cal K}={\cal F}^\perp\), \(\dim{\cal K}=n-465=17\,678\,370\).  By
Theorem B each \(A_s\) is block diagonal with respect to
\(\mathbb R^{\cal C}={\cal F}\oplus{\cal K}\), so
\(\operatorname{tr}(A_sA_t)=\operatorname{tr}(A_s|_{\cal F}A_t|_{\cal F})
+\operatorname{tr}(A_s|_{\cal K}A_t|_{\cal K})\), while directly
\(\operatorname{tr}(A_sA_t)=\delta_{st}\,n\,n_s\).  Define the Frobenius Gram
matrix of the thirteen residual operators,
\[
G_{st}=\operatorname{tr}(A_s|_{\cal K}A_t|_{\cal K})
=\delta_{st}\,n\,n_s-\bigl(n_sn_t+30\,b_sb_t+434\,a_sa_t\bigr).
\tag{6.1}
\]
\(G\succeq0\) automatically, being a Gram matrix.

> **Theorem C.**
> **(i)** \(G=\operatorname{diag}(n\,n_s)-UU^{\!\top}\) with
> \(U\) the \(13\times3\) matrix of rows \((n_s,\sqrt{30}\,b_s,\sqrt{434}\,a_s)\),
> and
> \[
> U^{\!\top}\operatorname{diag}(n\,n_s)^{-1}U
> =I_3-\tfrac1n zz^{\!\top},\qquad z=(1,\sqrt{30},\sqrt{434}),
> \]
> an exact rank-one deficit.  Hence **\(\operatorname{rank}G=11\)**, and the
> two-dimensional kernel is spanned by the two zero-diagonal Johnson
> combinations
> \(\sum_s(\mathrm{eig}^{(j)}_s/n_s-1)A_s\), \(j=1,2\).
> **(ii)** Adjoin \(Q|_{\cal K}\).  Every entry of the resulting
> \(15\times15\) moment matrix over
> \(\operatorname{span}\{I,A_1,\dots,A_{13},Q\}|_{\cal K}\) is forced except
> \(\langle Q|_{\cal K},Q|_{\cal K}\rangle\); the two forced consistency
> conditions \(c\perp\ker G\) hold identically; and the PSD bound they imply,
> \[
> \operatorname{tr}(Q^2)\ \ge\ \frac{1\,603\,823\,911\,200}{13}
> =1.23371\ldots\times10^{11},
> \]
> is **strictly weaker** than the trivial entrywise bound
> \(\operatorname{tr}(Q^2)\ge10\,080n=178\,202\,656\,800\).
> **(iii)** For every one of the \(2^{13}-1=8191\) subsets
> \(S\subseteq\{1,\dots,13\}\) and both modules, the Perron test
> \(\bigl|\sum_{s\in S}\mathrm{eig}_s\bigr|\le\sum_{s\in S}n_s\) holds; the
> tightest instance is \(97/120\) (\({\cal H}_1\), \(S=\{1\}\)).
>
> Consequently **no strict inequality exists anywhere in the quadratic class,
> and no contradiction at \(k=16\) can be produced from it.**

*Proof of the corank statement.*  \(H_{jj'}:=\sum_s
\mathrm{eig}^{(j)}_s\mathrm{eig}^{(j')}_s/(n\,n_s)\) is exactly the
\((j,j')\) entry of \(U^{\!\top}\operatorname{diag}(nn_s)^{-1}U\) up to the
\(\sqrt{m_j m_{j'}}\) normalisation, so (4.3) gives
\(H_{jj}=1-m_j/n\) and \(H_{jj'}=-\sqrt{m_jm_{j'}}/n\), i.e.
\(H=I_3-zz^{\!\top}/n\) with \(z=(\sqrt{m_0},\sqrt{m_1},\sqrt{m_2})\).
Its eigenvalues are \(1,1,1-465/n\), so \(I-UU^\top\)-conjugated has exactly
two zero eigenvalues and \(\operatorname{rank}G=11\).

*Why the kernel is unavoidable.*  \(\sum_sc_sA_s|_{\cal K}=0\) means
\(\sum_sc_sA_s\in\operatorname{span}\{P_0,P_1,P_2\}\).  By (4.2) each \(P_j\)
already lies in \(\operatorname{span}\{I,A_1,\dots,A_{13}\}\), and a
combination \(\gamma_0P_0+\gamma_1P_1+\gamma_2P_2\) has zero diagonal exactly
when \(\gamma_0+30\gamma_1+434\gamma_2=0\) — a two-dimensional condition.  So
the corank-two degeneracy is **forced by the Johnson kernels themselves**, not
by any accident of the hypothetical cover: it cannot be removed by choosing
better test matrices inside the span, and it is not evidence for or against
the cover.  This is the precise sense in which the class is exhausted.  The
same corank appears in the \(k=6\) control (Section 9), where there are three
classes, two relations, and Gram rank one.

*Why enlarging the span does not help.*  Any word \(W\) in
\(\{I,A_1,\dots,A_{13},Q\}\) has \(P_jWP_j\) equal to a product of the forced
scalars (Theorem B and (5.1)), so \(\operatorname{tr}(P_jW)\) is forced and
carries no new information; and for products of length \(\ge2\) that are not
already in the span — \(A_sA_t\), \(A_{13}Q\), \(Q^2\) — the *global* traces
\(\operatorname{tr}(A_sA_tA_u)\), \(\operatorname{tr}(A_{13}QA_s)\) etc. are
not determined by the design, so those operators cannot be adjoined to the
moment matrix with forced entries.  The \(15\times15\) matrix of (ii) is
therefore the **largest complete** forced moment matrix, and it is the
"smallest useful" one in the sense asked: it has a single free entry.

---

## 7. Routes that are now provably closed

* **Leakage bounds on \(L\).**  Closed: \(L=0\).
* **Sharp bounds on \(\operatorname{tr}(P_2A_{13}^2P_2)\).**  Closed: exact
  value \(87\,494\,834\).  (For contrast, the best bound obtainable *without*
  Theorem A, from the fourth-moment interval
  \(\operatorname{Spec}(A_{13}|_{\mathbf1^\perp})\subseteq[-60,776]\), is
  \(87\,494\,834\le\operatorname{tr}(P_2A_{13}^2P_2)\le434\cdot368\,044
  =159\,731\,096\); Theorem A collapses it to the lower endpoint.)
* **\(P_2Q^2P_2\), \(P_2A_{13}QP_2\), rowwise Cauchy/variance.**  Closed:
  all forced, all products of scalars, margins listed in Section 3.
* **Integrality of the forced eigenvalues.**  Closed: all \(26\) values are
  integers.
* **Perron/0-1-combination tests.**  Closed: all \(16\,382\) instances pass.
* **PSD block moment matrix.**  Closed: one free entry, bound weaker than
  the entrywise bound.
* **Krein / Schur closure.**  Already closed in the committed follow-up
  (all relevant Johnson Krein parameters positive, automatic from strength
  \(14\)); Theorem B explains why: the Schur algebra generated by
  \(P_0,P_1,P_2\) never leaves the Johnson kernel span.

---

## 8. The first genuinely unforced mixed statistic

Everything forced above lives in the \({\cal F}\)-block.  The first statistic
that is *not* forced, and the smallest one, is
\[
\boxed{\operatorname{tr}(Q^2)=\sum_{B,C}Q_{BC}^2
=\operatorname{tr}(R^4)-35\,400n},
\]
equivalently the entry distribution \((N_1,N_2,N_3)\) of \(Q\) subject to
\(N_1+2N_2+3N_3=10\,080n\), equivalently \(\#C_4(R)\).

It has an exact local meaning, which is the concrete next lever.

**Lemma 8.1 (matching reformulation of the design).**  For every
\(13\)-subset \(W\subset[31]\), the \(\lambda_{13}=9\) blocks of \({\cal C}\)
containing \(W\) are \(W\cup e\) for the nine edges \(e\) of a **perfect
matching** \(M_W\) of the \(18\)-set \([31]\setminus W\).
*Proof.*  Two blocks \(W\cup e\), \(W\cup f\) meet in \(13+|e\cap f|\) points,
and \(14\) is forbidden by (H2), so \(e\cap f=\emptyset\); nine disjoint edges
cover \(18\) points. \(\square\)

**Corollary 8.2.**  If \(|B\cap C|=12\), \(U=B\setminus C\),
\(V=C\setminus B\), \(W=[31]\setminus(B\cup C)\) (so \(|W|=13\),
\(|U|=|V|=3\)), then
\[
Q_{BC}=\#\{\text{edges of }M_W\text{ joining }U\text{ to }V\}\in\{0,1,2,3\},
\]
which reproves the entry bound structurally rather than by case analysis.

### 8.1 Lemma 8.3, with every intersection computed

> **Lemma 8.3.**  Let \(D,D'\) be fibre blocks with \(|D\cap D'|=13\).  Put
> \[
> I=D\cap D',\quad U=D\setminus D'=\{u_1,u_2\},\quad
> V=D'\setminus D=\{v_1,v_2\},\quad W'=[31]\setminus(D\cup D'),
> \]
> so \(|I|=13\), \(|U|=|V|=2\), \(|W'|=31-(13+2+2)=14\), and
> \([31]=I\sqcup U\sqcup V\sqcup W'\).  Then:
>
> **(a) Classification.**  A block \(B\) is a common \(R\)-neighbour of
> \(D\) and \(D'\) (i.e. \(|B\cap D|=|B\cap D'|=1\)) if and only if \(B\) is
> one of
> \[
> B_0=W'\cup\{q_0\}\ (q_0\in I),\qquad
> B_{ij}=(W'\setminus\{w_{ij}\})\cup\{u_i,v_j\}\ \ (i,j\in\{1,2\}),
> \]
> and all five exist, with \(q_0\in I\) and \(w_{ij}\in W'\) unique.
>
> **(b) The ten pairwise intersections.**
> \[
> |B_0\cap B_{ij}|=|W'\setminus\{w_{ij}\}|=13\quad(\text{4 pairs}),
> \]
> \[
> |B_{ij}\cap B_{i'j'}|=
> \bigl|W'\setminus\{w_{ij},w_{i'j'}\}\bigr|
> +\bigl|\{u_i,v_j\}\cap\{u_{i'},v_{j'}\}\bigr| .
> \]
> For the four *off-diagonal* index pairs — those sharing exactly one
> coordinate, \(\{11,12\},\{21,22\},\{11,21\},\{12,22\}\) — the second term is
> \(1\), so the total is \(14\) if \(w_{ij}=w_{i'j'}\) and \(13\) otherwise;
> since \(14\) is forbidden by (H2) the \(w\)-values **must differ** and the
> intersection is exactly \(13\) (4 pairs).
> For the two *diagonal* index pairs \(\{11,22\}\) and \(\{12,21\}\) the second
> term is \(0\), so
> \[
> |B_{11}\cap B_{22}|=
> \begin{cases}13,&w_{11}=w_{22}\ \ (\,|W'\setminus\{w\}|=13\,)\\
> 12,&w_{11}\ne w_{22}\ \ (\,|W'\setminus\{w_{11},w_{22}\}|=12\,)\end{cases}
> \]
> and likewise for \(\{12,21\}\).
>
> **(c) Conclusion.**  Exactly \(4+4=8\) of the ten pairs have intersection
> \(13\), forced; the two diagonal pairs have intersection \(12\) or \(13\).
> Define
> \[
> \boxed{\varepsilon(D,D')=[\,w_{11}\ne w_{22}\,]+[\,w_{12}\ne w_{21}\,]
> \in\{0,1,2\},}
> \]
> **which is exactly the number of \(A_{12}\)-pairs among the five common
> neighbours.**  The inequality, not the equality, is the \(A_{12}\)
> condition.  As a by-product, (b) shows the map \((i,j)\mapsto w_{ij}\) is
> injective along each row and each column of the \(2\times2\) index array.

*Proof of (a).*  Split \(B\) as \((B\cap I)\sqcup(B\cap U)\sqcup(B\cap V)
\sqcup(B\cap W')\).  Then \(|B\cap D|=|B\cap I|+|B\cap U|=1\) and
\(|B\cap D'|=|B\cap I|+|B\cap V|=1\), so either \(|B\cap I|=1\) and
\(B\cap U=B\cap V=\emptyset\), forcing \(|B\cap W'|=14=|W'|\) and
\(B=W'\cup\{q\}\) with \(q\in I\); or \(B\cap I=\emptyset\) and
\(|B\cap U|=|B\cap V|=1\), forcing \(|B\cap W'|=13=|W'|-1\) and
\(B=(W'\setminus\{w\})\cup\{u,v\}\).
In the first case \(W'\) is a \(14\)-set, so by (H3) it lies in exactly one
block \(W'\cup\{q_0\}\); \(q_0\in U\) would give \(|B\cap D'|=0\) and
\(q_0\in V\) would give \(|B\cap D|=0\), both barred by (H1); hence
\(q_0\in I\) and there is exactly one block of the first kind.
In the second case, two blocks \((W'\setminus\{w\})\cup\{u,v\}\) and
\((W'\setminus\{w'\})\cup\{u,v\}\) with \(w\ne w'\) would meet in
\((W'\setminus\{w,w'\})\cup\{u,v\}\), of size \(12+2=14\), barred by (H2); so
at most one \(w\) per \((u_i,v_j)\), i.e. at most four blocks of the second
kind.  Hence \((R^2)_{DD'}\le5\).  Equality holds because the
one-factorisation count gives \(\binom{16}{2}\cdot\frac{5\cdot14}{2}
=120\cdot35=4200=5\cdot840=5n_{13}\) two-step walks from each block to the
\(840\) blocks at intersection \(13\); the bound \(\le5\) is therefore attained
term by term.  So all five exist. \(\square\)

*Proof of (b).*  Direct set computation, using
\([31]=I\sqcup U\sqcup V\sqcup W'\).  \(B_0\cap B_{ij}\): the point \(q_0\in I\)
lies in neither \(W'\) nor \(\{u_i,v_j\}\), and \(\{u_i,v_j\}\cap W'=\emptyset\),
so the intersection is \(W'\cap(W'\setminus\{w_{ij}\})=W'\setminus\{w_{ij}\}\),
size \(13\).  For two second-kind blocks the two displayed parts lie in
disjoint ground pieces (\(W'\) versus \(U\cup V\)), so the sizes add. \(\square\)

### 8.2 The double count, with every factor of two audited

> **Proposition 8.4.**  With \(\varepsilon\) as in Lemma 8.3:
> \[
> \textbf{(global)}\qquad
> \boxed{\ \operatorname{tr}(Q^2)=10\,080\,n
> +4\!\!\sum_{\{D,D'\}:\,|D\cap D'|=13}\!\!\varepsilon(D,D')\ }
> \]
> \[
> \textbf{(row)}\qquad
> \boxed{\ \sum_{D}Q_{BD}^2=10\,080
> +2\!\!\sum_{\{C,C'\}\subseteq N_R(B),\ |C\cap C'|=13}\!\!
> \varepsilon_B(C,C')\ }
> \]
> where \(\varepsilon_B(C,C')\in\{0,1\}\) is the indicator that \(B\)'s
> partner in an \(A_{12}\)-pair among the five common \(R\)-neighbours of
> \(C,C'\) exists.  **The naive per-\(B\) form
> \(\sum_DQ_{BD}^2=10\,080+4\sum_{C:|B\cap C|=13}\varepsilon_{BC}\) is not
> correct**: it indexes by the \(840\) blocks at intersection \(13\) from
> \(B\), whereas the correct index set is the \(2100\) unordered pairs of
> \(R\)-neighbours of \(B\) at mutual intersection \(13\), and its factor is
> \(2\), not \(4\).

*Proof.*  Step 1 (the \(A_{12}\) side contributes nothing).  Let
\(|X\cap Y|=12\), \(U=X\setminus Y\), \(V=Y\setminus X\), \(W=[31]\setminus(X\cup Y)\)
with \(|W|=13\), \(|U|=|V|=3\).  Exactly as in the proof of Lemma 8.3(a),
a common \(R\)-neighbour must be \(W\cup\{u,v\}\) with \(u\in U\), \(v\in V\),
and by Lemma 8.1 this is a block iff \(\{u,v\}\in M_W\); distinct such
neighbours have \(u\ne u'\), \(v\ne v'\), so
\[
\bigl|(W\cup\{u,v\})\cap(W\cup\{u',v'\})\bigr|=|W|=13 .
\]
Hence **any two common \(R\)-neighbours of an \(A_{12}\) pair meet in exactly
\(13\) points**, never \(12\).

Step 2 (the bijection).  Count the set
\[
{\cal T}=\bigl\{\bigl(\{X,Y\},\{D,D'\}\bigr):\ |X\cap Y|=12,\
D\ne D'\ \text{both }R\text{-adjacent to }X\text{ and to }Y\bigr\},
\]
in two ways.  Two \(R\)-neighbours of a common block meet in \(13\) or \(12\)
points (the one-factorisation two-step law), so in every element of
\({\cal T}\) we have \(|D\cap D'|\in\{12,13\}\); by Step 1 applied to
\(\{D,D'\}\) — whose common neighbours include \(X\) and \(Y\) with
\(|X\cap Y|=12\) — the case \(|D\cap D'|=12\) is impossible.  So
\(|D\cap D'|=13\), and by Lemma 8.3 the pair \(\{X,Y\}\) is one of the
\(\varepsilon(D,D')\) diagonal \(A_{12}\)-pairs among the five common
neighbours of \(\{D,D'\}\).  Conversely every such choice gives an element of
\({\cal T}\).  Therefore
\[
|{\cal T}|=\!\!\sum_{\{D,D'\}:\,|D\cap D'|=13}\!\!\varepsilon(D,D') .
\tag{8.1}
\]

Step 3 (the other count of \({\cal T}\), and the factors).  For a fixed
*unordered* \(\{X,Y\}\) the number of admissible \(\{D,D'\}\) is
\(\binom{Q_{XY}}2\), so
\(|{\cal T}|=\sum_{\{X,Y\}}\binom{Q_{XY}}2\).  Passing to ordered pairs
doubles this: \(\sum_{(X,Y)}\binom{Q_{XY}}2=2|{\cal T}|\).  Now use
\(q^2=q+2\binom q2\) on each ordered entry and
\(\sum_{(X,Y)}Q_{XY}=10\,080\,n\) (row sum \(10\,080\), \(n\) rows):
\[
\operatorname{tr}(Q^2)=\sum_{(X,Y)}Q_{XY}^2
=\sum_{(X,Y)}Q_{XY}+2\sum_{(X,Y)}\binom{Q_{XY}}2
=10\,080n+2\cdot2|{\cal T}|,
\]
which with (8.1) is the global identity: the factor \(4\) is
\(2\ (\text{from }q^2=q+2\binom q2)\times2\ (\text{ordered vs unordered }\{X,Y\})\).

Step 4 (the row identity, and the cross-check).  Fix \(B\).  Then
\(\sum_DQ_{BD}^2\) counts triples \((D,C,C')\) with \(|B\cap D|=12\) and
\(C,C'\in N_R(B)\cap N_R(D)\).  The \(C=C'\) part is
\(\sum_D Q_{BD}=10\,080\).  For \(C\ne C'\): both lie in \(N_R(B)\), so
\(|C\cap C'|\in\{13,12\}\); if \(|C\cap C'|=12\) then by Step 1 all its common
neighbours pairwise meet in \(13\), and \(B\) is one of them, so no \(D\ne B\)
with \(|B\cap D|=12\) exists — no contribution.  If \(|C\cap C'|=13\), the five
common neighbours of \(\{C,C'\}\) include \(B\), and by Lemma 8.3(c) the two
diagonal pairs are vertex-disjoint, so \(B\) lies in **at most one**
\(A_{12}\)-pair; hence the number of admissible \(D\) is
\(\varepsilon_B(C,C')\in\{0,1\}\).  Summing over ordered \((C,C')\) doubles the
unordered sum, giving the row identity with factor \(2\).
Consistency: summing the row identity over \(B\) and regrouping by
\(\{C,C'\}\), each of the \(\varepsilon(C,C')\) diagonal \(A_{12}\)-pairs
contributes its two member blocks, so
\(\sum_{B}\varepsilon_B(C,C')=2\varepsilon(C,C')\) and the row identity
reproduces the global one, \(2\cdot2=4\).  \(\square\)

With \(n\,n_{13}/2=420n\) unordered intersection-\(13\) pairs and
\(\varepsilon\le2\),
\[
10\,080n\le\operatorname{tr}(Q^2)\le13\,440n,
\]
i.e. \(178\,202\,656\,800\le\operatorname{tr}(Q^2)\le237\,603\,542\,400\), and
therefore
\[
\boxed{804\,033\,415\,800\le\operatorname{tr}R^4\le863\,434\,301\,400,
\qquad
37\,125\,553\,500\le\#C_4(R)\le44\,550\,664\,200 .}
\]
These replace the previously committed upper bounds
\(\operatorname{tr}R^4\le1\,160\,438\,729\,400\ (=65\,640n)\) and
\(\#C_4(R)\le81\,676\,217\,700\ (=4620n)\): the excess above the forced
\(A_{13}\) contribution is cut from \(2520n\) to \(420n\), a factor of six.
The improvement comes from Lemma 8.3, i.e. from the observation that eight of
the ten pairs among the five common neighbours are forced.

### 8.3 The first genuinely unforced mixed statistic, precisely

> **Definition.**  For an ordered pair \((D,D')\) of fibre blocks with
> \(|D\cap D'|=13\), let \(w_{11},w_{12},w_{21},w_{22}\in W'\) be the omitted
> points of Lemma 8.3 and set
> \(\varepsilon(D,D')=[w_{11}\ne w_{22}]+[w_{12}\ne w_{21}]\).  The **first
> unforced mixed statistic** is
> \[
> {\cal E}=\!\!\sum_{\{D,D'\}:|D\cap D'|=13}\!\!\varepsilon(D,D')
> \ \in\ [\,0,\ 840n\,],
> \]
> equivalently \(\operatorname{tr}(Q^2)=10\,080n+4{\cal E}\), equivalently
> \(\#C_4(R)=2100n+{\cal E}/2\), equivalently the entry census
> \((N_1,N_2,N_3)\) of \(Q\) modulo \(N_1+2N_2+3N_3=10\,080n\).

**Why no quadratic attack can determine \({\cal E}\).**  Every statistic in
the quadratic class is a linear functional of the operators
\(\{I,A_1,\dots,A_{13},Q\}\) restricted to \({\cal F}\) or evaluated by a
trace.  By Theorem B all \({\cal F}\)-blocks are forced scalars, so
\(\operatorname{tr}(P_jW)\) is forced for every word \(W\) and contributes
nothing; and by Theorem C(ii) the *only* free entry of the complete forced
moment matrix is \(\langle Q|_{\cal K},Q|_{\cal K}\rangle
=\operatorname{tr}(Q^2)-6\,757\,864\,344\), i.e. \({\cal E}\) itself, whose
PSD lower bound is weaker than the trivial entrywise one.  So \({\cal E}\) is
simultaneously (i) the unique free parameter of the quadratic theory and
(ii) provably not pinned by it.  Determining it requires either a *cubic*
statistic — \(\operatorname{tr}(Q^3)\), \(\operatorname{tr}(QA_{13}Q)\), or a
triple-intersection profile — or a genuinely local argument about the
matching system \(\{M_W\}\) of Lemma 8.1.  A future obstruction must control
\({\cal E}\), or equivalently \(Q|_{\cal K}\); it cannot come from any
compression onto \({\cal F}\).

---

## 9. The \(k=6\) control: verified against real matrices

The known derived-Witt cover \(O_6=KG(11,5)\to K_7\) has fibre an
\(S(4,5,11)\) with \(n=66\).  The verifier constructs the design by
deterministic exact cover and then checks the entire mechanism against the
explicit \(66\times66\) matrices, with exact rational linear algebra:

* \(\dim{\cal H}_1=10\), \(\dim{\cal H}_2=44\) (pair span of rank \(55\));
* the degree-two certificate of §2.1 applies verbatim
  (\(\langle q\rangle-q(-5)/7=0\)) and kills the mass at \(-3\), giving the
  \({\cal H}_1\) measure \(\frac17\delta_{-5}+\frac{11}{21}\delta_2
  +\frac13\delta_{-1}\);
* formula (4.1) gives \((a_1,a_2,a_3)=(2,-2,-1)\) and
  \((b_1,b_2,b_3)=(-7,-2,8)\); both sum to \(-1\); \(s=0\) and \(s=4\) give
  \(0\); \(a_1=2\) and \(b_1=-7\) match \((k-2)(k-5)/2\) and
  \((-k^2+4k-2)/2\);
* **all six operator identities \(A_sx=\mathrm{eig}_sx\) are verified on all
  \(10\) and all \(44\) basis vectors** — this is a direct test of Theorem B
  on a cover that actually exists;
* \(R^2=15I+5A_3+Q\) yields \(Q=3A_2\) exactly (row sums \(60\), entries in
  \(\{0,3\}\)), and \(Qx=-6x\) on both modules, matching
  \(\mu_j^2-15-5\,\mathrm{eig}^{(j)}_3\) for \(j=1,2\);
* \(\operatorname{tr}(Q^2)=11\,880\) attains the \(\varepsilon\equiv2\)
  extreme of Proposition 8.4 exactly, so **the \(\varepsilon\) bound is
  attained on a real cover** and cannot be improved by pure algebra;
* the \(k=6\) \({\cal K}\)-Gram has rank \(1=3-2\), the same corank two as
  \(k=16\), and (4.3) holds with \(n/m_j-1\).

The control therefore validates the normalisation, formula (4.1), Theorem B,
the \(Q\)-eigenvalue arithmetic, the \(\varepsilon\) identity, and the
corank-two degeneracy — on a cover known to exist.

---

## 10. Remaining gap

Under the standing hypotheses, the forced module
\({\cal F}={\cal H}_0\oplus{\cal H}_1\oplus{\cal H}_2\) of dimension \(465\)
is completely rigid: it is a common eigenspace of every fibre intersection
matrix, of \(R\), of \(A_{13}\), of \(A_{12}\) and of \(Q\), with all
\(26+3\) eigenvalues integers, and every second-moment relation among these
operators is exactly saturated with a forced corank-two degeneracy.  The
attack targeted the leakage \((I-P_2)A_{13}P_2\); that operator is zero, so
the target was empty, and the whole quadratic-leakage class provably cannot
contradict the cover.  What is left is entirely the residual module
\({\cal K}\) of dimension \(17\,678\,370\), whose only forced data are the
odd-trace vanishing through degree nine, the residual moment bookkeeping of
the committed notes, and the sharpened interval
\(\operatorname{tr}(Q|_{\cal K}^2)\in
[10\,080n-6\,757\,864\,344,\ 13\,440n-6\,757\,864\,344]\).

**No contradiction was found.  The \(k=16\) cover is not excluded.
Erdős–Rosenfeld problem #835 remains open; nothing here is a construction,
and nothing here is an all-parameter proof.**

---

## 11. Exact verification

```sh
python3 -B \
  collaboration/opus5/joint_schreier_krein_attack/verify_joint_schreier_krein_attack.py
```

Standard library only, exact integer/`Fraction` arithmetic, no floating point
in any decision, no randomness.  It audits: the Steiner derivation from local
bijectivity; the Odd walk expansions through degree six; both support
certificates including the independent recovery of \(m_3=-194\); all four
Lagrange compressions; Theorem A and every \(P_2\)-compression; the full
\(a_s\)/\(b_s\) tables by two independent routes with integrality, forbidden
classes, sums and Perron; the orthogonality identities (4.3); the
\({\cal K}\)-Gram rank and its kernel; the moment-matrix bound and its
weakness; all \(16\,382\) Perron instances; the \(\varepsilon\) enumeration
and the improved \(\operatorname{tr}R^4\), \(\#C_4\) intervals; the labelled
set model of Lemma 8.3 over all \(256\) omitted-point patterns (\(84\)
admissible, \(172\) creating a forbidden \(14\)-intersection); and the whole
\(k=6\) control against the explicitly constructed Witt fibre, including
Lemma 8.3 on all \(990\) of its \(A_3\) pairs and both the global and the
row form of Proposition 8.4 with the factor audit.
Current status: **143 checks, all passing; Ruff clean.**

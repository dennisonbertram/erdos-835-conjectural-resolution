# The staircase support theorem, a certified relation family, and the corrected \(k=16\) frontier

Companion to `collaboration/opus5/joint_schreier_krein_attack/NOTE.md`.
Same hypotheses and notation: an assumed covering map
\(O_{16}=KG(31,15)\to K_{17}\), one fibre \({\cal C}\) which is an
\(S(14,15,31)\) with \(n=17\,678\,835\) blocks, \(A_s\) the fibre
intersection matrices, \(R=A_1\), \(P_a\) the projector onto the restricted
degree-\(a\) harmonic module \({\cal H}_a\), \(m_a=\dim{\cal H}_a\),
\(N_j:=\iota^*E_j\iota\), \(\theta_j=(-1)^j(16-j)\),
\({\cal J}=\operatorname{span}\{I,A_1,\dots,A_{13}\}\) (\(\dim=14\)).

## 0. Scope

**Erdős–Rosenfeld problem #835 remains OPEN.**  No contradiction is derived
here; no construction is given; \(k=16\) is not excluded; and excluding
\(k=16\) would not settle #835.

**Audit correction (this revision).**  An earlier draft of this note asserted
a "Theorem T" claiming that the image of \({\cal J}\) under \(Z\mapsto ZP_a\)
has dimension **exactly** \(a\).  That is false, and already false at
\(a=2\): the companion note proves \(A_sP_2=a_sP_2\), so the level-2 image
has dimension \(1\), not \(2\).  The error was methodological — the
computation exhibited the subspace of Johnson polynomials vanishing on the
global support, which certifies an **upper** bound
\(\dim\operatorname{im}\le a\) and nothing more, because compression can
create further cancellation.  It does.  The missing relation is the
strength-\(14\) identity \(N_aP_a=\frac1{17}P_a\), i.e.
\[
Z_a:=17\,\iota^*E_a\iota-I\in{\cal J},\qquad Z_aP_a=0 ,
\]
which at \(a=3\) reduces the level-3 span \(\{I,R,A_{13}\}\) to \(\{I,R\}\)
via
\[
\boxed{A_{13}P_3=(R+372I)P_3 .}
\]
That identity, and the resulting two-operator level-3 theory, is the
committed result of `collaboration/schreier_h3_support/README.md` (its
equations (7)–(10)); the level-4 analogue is
`collaboration/schreier_h4_support/README.md`, and the triple-containment
profiles are `collaboration/schreier_h3_triple_profiles/README.md`.  This
note now **defers** to those for levels 3 and 4 and keeps only what is
independently new: the uniform staircase computation, the certified relation
family with honest upper bounds, and the corrected Steiner-side identity of
Section 4.  Downstream claims that depended on the false exact rank
(a "free" \(\operatorname{tr}(P_3A_{13}^2)\), a "vacuous closure" no-go, and
a "linear theory cannot obstruct profiles" statement) are retracted below and
replaced by what the calculation actually establishes.

## 1. The staircase support theorem (unchanged, and still correct)

For \(0\le a\le7\) and \(0\le j\le15\) put
\[
T(a,j)=\operatorname{tr}\bigl(P_aN_j\bigr)=\|E_j\iota P_a\|_F^2\ \ge0 .
\]
Both \(P_a\) and \(N_j\) have entries depending only on \(s=|B\cap C|\):
\((P_a)_{BC}=17f_a(s)\), \((N_j)_{BC}=f_j(s)\), with
\[
f_a(s)=\frac{m_a}{\binom{31}{15}}\cdot\frac{P_{15-s}(a)}{n^{J}_{15-s}},
\qquad f_a(15)=\frac{m_a}{\binom{31}{15}},
\]
\(P_i(\cdot)\) the Eberlein polynomial of \(J(31,15)\) and
\(n^J_i=\binom{15}{i}\binom{16}{i}\).  Hence \(T(a,j)\) is a closed-form
function of the design's inner distribution alone:
\[
\boxed{\;T(a,j)=\frac{17\,n\,m_am_j}{\binom{31}{15}^2}
\sum_{i=0}^{15}\alpha_i\,\frac{P_i(a)P_i(j)}{(n^J_i)^2},\qquad
\alpha_0=1,\ \alpha_1=\alpha_{15}=0,\ \alpha_i=n_{15-i}. }
\tag{1.1}
\]

> **Theorem S (staircase).**  For \(0\le a\le7\),
> \(T(a,j)=0\) unless \(j=a\) or \(15-a\le j\le15\).  Since
> \(T(a,j)=\|E_j\iota P_a\|_F^2\), this is the exact subspace statement
> \[
> \boxed{\ \iota{\cal H}_a\subseteq
> E_a\oplus E_{15-a}\oplus\cdots\oplus E_{15},\qquad
> \#\{\text{support}\}=a+2 .\ }
> \]
> Moreover \(T(a,a)=m_a/17\) and \(\sum_jT(a,j)=m_a\).

*Proof.*  Evaluate (1.1): a finite exact rational computation with the forced
\(\alpha_i\).  The verifier does all \(8\times16\) pairs.  The vanishing for
\(1\le j\le7\), \(j\ne a\), is the strength-\(14\) statement
\(N_j=\frac1{17}P_j\); the content is the vanishing for \(8\le j\le14-a\).
No positivity certificate is needed: the norm is literally zero. \(\square\)

The resulting global measures (weights \(T(a,j)/m_a\) at \(\theta_j\)) are

| \(a\) | measure |
|---|---|
| 0 | \(\frac1{17}\delta_{16}+\frac{16}{17}\delta_{-1}\) |
| 1 | \(\frac1{17}\delta_{-15}+\frac{31}{51}\delta_{2}+\frac13\delta_{-1}\) |
| 2 | \(\frac1{17}\delta_{14}+\frac{29}{85}\delta_{-3}+\frac4{15}\delta_{2}+\frac13\delta_{-1}\) |
| 3 | \(\frac1{17}\delta_{-13}+\frac{522}{2975}\delta_{4}+\frac{29}{175}\delta_{-3}+\frac{29}{75}\delta_{2}+\frac{16}{75}\delta_{-1}\) |
| 4 | \(\frac1{17}\delta_{12}+\frac{10}{119}\delta_{-5}+\frac{16}{175}\delta_{4}+\frac{54}{175}\delta_{-3}+\frac{128}{525}\delta_{2}+\frac{16}{75}\delta_{-1}\) |
| 5 | \(\frac1{17}\delta_{-11}+\frac{345}{9163}\delta_{6}+\frac{25}{539}\delta_{-5}+\frac{10}{49}\delta_{4}+\frac{48}{245}\delta_{-3}+\frac{72}{245}\delta_{2}+\frac{8}{49}\delta_{-1}\) |

The \(a=0\) row is the Delsarte characterisation of a \(14\)-design; \(a=1,2\)
reproduce the two measures of the companion note; \(a=3,4\) agree with the
committed `schreier_h3_support` and `schreier_h4_support` supports.  Every row
satisfies \(m_0=1,\ m_1=0,\ m_2=16\), and for \(a=3,4,5\)
\[
m_3=-\tfrac{598}5,\ \tfrac{452}5,\ -66,\qquad
m_4=\tfrac{8724}5,\ \tfrac{6624}5,\ 1012,
\]
matching \(m_3=2\operatorname{tr}(P_aR)/m_a\) and
\(m_4=496+4\operatorname{tr}(P_aA_{13})/m_a\) computed independently from the
Johnson kernels, and reproducing
\(\operatorname{tr}(P_3R)=-240\,994\),
\(\operatorname{tr}(P_3R^2)=14\,417\,914\) of the committed Schreier–Krein
trace table.

**Independent certificate at \(a=3\).**  \(h_3(t)=(t-4)(t+3)(t-2)(t+1)\) is
\(\ge0\) on the eight residual points with zeros exactly \(\{4,-3,2,-1\}\),
and \(\langle h_3\rangle_y=496+4\langle x,A_{13}x\rangle-4\langle x,Rx\rangle-184\)
averages to \(1800=h_3(-13)/17\) — the exact lower bound — so equality holds
pointwise.  This re-proves the \(a=3\) row by positivity.

## 2. Theorem T, corrected: a certified relation family and an upper bound

> **Theorem T (certified relations; upper bound on the image).**
> For \(1\le a\le7\) the following two families lie in
> \(\{Z\in{\cal J}:ZP_a=0\}\):
> 1. every \(Z=\sum_iz_iD_i\) with \(\widehat Z(j)=\sum_iz_iP_i(j)=0\) for all
>    \(j\) in the \((a+2)\)-element support of Theorem S (a \((14-a)\)-dimensional
>    family of fibre matrices);
> 2. the single extra relation \(Z_a=17\,\iota^*E_a\iota-I\), which satisfies
>    \(Z_aP_a=0\) because \(N_a=\frac1{17}P_a\) by strength \(14\).
>
> Their span has dimension \(13,13,12,11,10,9,8\) for \(a=1,\dots,7\)
> (family 2 is contained in family 1 only at \(a=1\)).  Consequently
> \[
> \boxed{\ \dim\{ZP_a:Z\in{\cal J}\}\ \le\ \max(1,\,a-1)\ }
> \]
> — **an upper bound only.**

*Proof.*  Family 1: \(ZP_a=\sum_j\widehat Z(j)N_jP_a\), and the terms with
\(j\) outside the support vanish by Theorem S.  Family 2: immediate from
\(N_a=\frac1{17}P_a\).  Dimensions and containments are computed exactly by
the verifier. \(\square\)

**Where the exact rank is known.**  Only at three levels, and each needs an
extra input beyond Theorem T:

* \(a=1,2\): rank \(=1\).  Proved in the companion note
  (\(A_sP_1=b_sP_1\), \(A_sP_2=a_sP_2\)).  **This is the counterexample to
  the earlier draft's "exactly \(a\)".**  The verifier asserts both numbers
  side by side: support-derived upper bound \(2\) at \(a=2\) versus actual
  rank \(1\).
* \(a=3\): rank \(=2\) exactly.  The upper bound gives \(\le2\); the lower
  bound is \(\ge2\) because \(RP_3\notin\operatorname{span}\{P_3\}\), which
  follows from the strictly positive slack
  \[
  \operatorname{tr}(P_3R^2)-\frac{\operatorname{tr}(P_3R)^2}{m_3}
  =\frac{32\,364}5>0 .
  \]
* \(a\ge4\): **only the upper bound \(\le a-1\) is proved here.**  Whether it
  is attained is open in this note.

**Level-3 reduced form.**  Combining Theorem T with the level-3 walk basis
gives, for every \(s\),
\[
A_sP_3=(\alpha_sI+\beta_sR)P_3 ,
\]
the two-operator statement of `schreier_h3_support` (its (9)).  This note's
independently derived three-operator table
\(A_sP_3=(\alpha'_sI+\beta'_sR+\gamma'_sA_{13})P_3\) reduces to it under
\(A_{13}P_3=(R+372I)P_3\); the verifier checks the reduction for all thirteen
\(s\), e.g. \(s=2\): \(-274-\frac{11}3\cdot372=-1638\) and
\(-\frac{25}3-\frac{11}3=-12\), and \(s=12\):
\(\frac{2470}3+\frac{29}9\cdot372=2022\) and
\(-\frac{137}9+\frac{29}9=-12\).  The three-operator column sums are exactly
\((-1,0,0)\), as forced by \(\sum_sA_s=J-I\) and \(JP_3=0\) — a consistency
check, not an obstruction.

## 3. Retractions, and what the level-3 Gram actually says

**Retracted.**  The earlier draft claimed that
\(X=\operatorname{tr}(P_3RA_{13})\) and \(Y=\operatorname{tr}(P_3A_{13}^2)\)
are unforced, on the strength of a "vacuous \(J\)-closure".  Both are in fact
**forced**, because \(A_{13}P_3=(R+372I)P_3\):
\[
\boxed{
\begin{aligned}
X&=\operatorname{tr}(P_3R^2)+372\operatorname{tr}(P_3R)=-75\,231\,854,\\
Y&=\operatorname{tr}(P_3R^2)+744\operatorname{tr}(P_3R)+372^2m_3
   =392\,805\,898 .
\end{aligned}}
\]
The \(3\times3\) Gram matrix of \(\{IP_3,RP_3,A_{13}P_3\}\) is therefore
completely determined and singular of rank \(2\), which is exactly the
statement that the level-3 image is two-dimensional.  The
"\(\sigma+e_1=0\)" observation is a valid identity but was the wrong frame:
in the reduced two-operator basis the Gram matrix
\(\bigl(\begin{smallmatrix}4030&-240994\\-240994&14417914\end{smallmatrix}\bigr)\)
is forced with determinant \(4030\cdot14\,417\,914-240\,994^2>0\), so nothing
is left free at the level of second-order traces.

**The placeholder is removed.**  The exact level-3 leakage identity is
\[
\bigl\|(I-P_3)A_{13}P_3\bigr\|_F^2
=\bigl\|A_{13}P_3\bigr\|_F^2-\bigl\|P_3A_{13}P_3\bigr\|_F^2
=\operatorname{tr}(P_3R^2)-\bigl\|P_3RP_3\bigr\|_F^2
=\bigl\|(I-P_3)RP_3\bigr\|_F^2 ,
\]
using \(A_{13}P_3=RP_3+372P_3\) so that the \(372\)-terms cancel between the
two norms.  The first term is forced; the second,
\(\|P_3RP_3\|_F^2=\operatorname{tr}\bigl((P_3RP_3)^2\bigr)\), is **not
determined by anything in this note**, and it is the single genuinely free
level-3 second-order statistic.  It is bounded below by
\(\operatorname{tr}(P_3R)^2/m_3\) and above by \(\operatorname{tr}(P_3R^2)\);
the committed `schreier_h3_support` and `h3_state_refinement` notes give
sharper windows and a rank bound, and this note does not improve them.

**Scope of "no upper bound".**  Where the earlier draft said a free statistic
had "no upper bound" and was "subject only to Gram positivity", both claims
were too broad.  Gram positivity alone gives no upper bound, but \(R\) and
\(A_{13}\) are nonnegative integer matrices with row sums \(120\) and \(840\),
so \(\|RP_3\|_F^2\le120^2m_3\) and \(\|A_{13}P_3\|_F^2\le840^2m_3\) hold
trivially, and further combinatorial, integrality and rank constraints are not
ruled out — this note simply does not use any.

## 4. The Steiner side: \(d(B)=0\) is forced, and the exact reformulation

Fix a block \(B\) in a fibre \({\cal C}\), put \(Y=[31]\setminus B\)
(\(|Y|=16\)), and let \(d(B)\) be the number of blocks of \({\cal C}\)
disjoint from \(B\), i.e. contained in \(Y\).

**(i) \(d(B)\le1\).**  Two distinct \(15\)-subsets of the \(16\)-set \(Y\)
meet in \(14\) points, so they cannot both be blocks of an \(S(14,15,31)\).
Hence the disjointness graph inside a fibre has maximum degree \(1\): it is a
matching.  It is in fact an involution — if \(B'=Y\setminus\{y\}\) is disjoint
from \(B\) then \(B\) is a \(15\)-subset of \([31]\setminus B'=B\cup\{y\}\),
so \(d(B')=1\) with partner \(B\) — whence \(\#\{B:d(B)=1\}\) is even.

**(ii) The counting identity.**  Each of the \(\binom{16}{14}=120\)
\(14\)-subsets of \(Y\) lies in exactly one block of \({\cal C}\).  A block
meeting \(B\) in exactly one point contains exactly one of them; a block
disjoint from \(B\) is \(Y\setminus\{y\}\) and contains
\(\binom{15}{14}=15\) of them; a block meeting \(B\) in \(\ge2\) points
contains none.  Hence
\[
\boxed{\;n_1(B)+15\,d(B)=120\;}
\]
so \(n_1(B)\in\{120,105\}\) and \(n_1(B)\equiv0\pmod{15}\).

**(iii) \(d(B)=0\) is forced, so every \(S(14,15,31)\) is intersecting.**
Two independent proofs.  *Closed form:* the general-\(k\) intersection formula
of `collaboration/general_h2_rigidity/README.md` (6.1),
\[
n_s=\frac{\binom{k-1}{s}}{k+1}\Bigl(\binom{k}{s+1}+(-1)^{s+1}k\Bigr),
\]
uses only the design moments and \(n_{k-1}=1\), and gives
\(n_0=(16-16)/17=0\) at \(k=16\) (and \(n_{14}=0\), \(n_{15}=1\)); the verifier
checks that it reproduces all thirteen \(n_s\) at \(k=16\) and all of
\(0,15,20,30,0,1\) at \(k=6\) against the explicitly constructed
\(S(4,5,11)\).  *Triangular system:*  The
binomial-moment system \(\sum_{s}\binom si\,n_s(B)=\binom{15}{i}(\lambda_i-1)\)
for \(i=13,12,\dots,1\) is triangular and determines
\(n_{13},\dots,n_1\) with no reference to \(n_0=d(B)\) (because
\(\binom0i=0\) for \(i\ge1\)); the \(i=0\) equation then reads
\(\sum_{s\ge0}n_s(B)=n-1\).  The verifier confirms
\(\sum_{s=1}^{13}n_s=n-1\) exactly, so \(d(B)=n_0(B)=0\) and
\(n_1(B)=120\) for **every** block of **every** \(S(14,15,31)\).

**Consequence (corrected reformulation).**  An earlier draft said the
intersecting condition is an extra requirement beyond the large set.  It is
not — it is automatic.  Therefore
\[
\boxed{
\begin{aligned}
&\text{a covering map }O_{16}\to K_{17}\ \text{exists}\\
&\iff\ \text{a large set of }17\ \text{pairwise disjoint }S(14,15,31)
\text{ partitioning }\tbinom{[31]}{15}\text{ exists.}
\end{aligned}}
\]
(\(\Leftarrow\): each block's \(16\) Odd-neighbours are the \(15\)-subsets of
its complement, which pairwise meet in \(14\) points and so lie in \(16\)
distinct fibres, none of them its own by (iii); \(\Rightarrow\) is (H0)–(H3)
of the companion note.)  Since \(d\equiv0\), the parity observation in (i) is
vacuous and yields no additional constraint — recorded here as a checked dead
end rather than a lever.

## 5. What the profile computation does and does not establish

For an ordered pair \((B,C)\) with \(|B\cap C|=u\) define the triple profile
\[
\nu_{s,t}(B,C)=\#\{D\in{\cal C}\setminus\{B,C\}:|B\cap D|=s,\ |C\cap D|=t\},
\qquad 1\le s,t\le13 ,
\]
\(169\) unknowns.  Exact linear equations, coefficients depending only on
\(u\): \(13\) row sums, \(13\) column sums, the \(28\) entrywise identities
\((N_jP_a)_{BC}=0\) from Theorem S (\(a\le7\), \(8\le j\le14-a\)) in two
orientations, and the \(76=13+13+12+11+10+9+8\) certified relations
\((ZP_a)_{BC}=0\) of Theorem T in two orientations — **\(234\) equations**.

> Exact rational elimination gives, for **every** \(u=1,\dots,13\):
> \[
> \text{rank}=114,\qquad\text{free dimensions}=55,\qquad
> \text{inconsistent rows}=0,
> \]
> and no coordinate \(\nu_{s,t}\) is uniquely determined by the system.

(For the record, the earlier weaker system that omitted the \(Z_a\) relations
gave \(222\) equations, rank \(108\), \(61\) free.)

**What this establishes and what it does not.**  It establishes exactly two
things: the \(234\) equations are mutually consistent over \(\mathbb Q\) for
every \(u\), and no single profile coordinate is pinned, hence none can be
exhibited as forced-negative or forced-non-integral by this system alone.
It does **not** establish that a nonnegative integral profile exists, and it
does **not** show that "the linear theory cannot obstruct profiles": rational
consistency of an equality system says nothing about the intersection of its
solution set with \(\mathbb Z_{\ge0}^{169}\).  **LP and integer feasibility
are left open here**; no certificate either way is claimed.  The committed
`schreier_h3_triple_profiles/README.md` carries this further and should be
read for the state-refined version.

## 6. Routes examined, with the narrow statement each supports

* **Staircase support (Theorem S).**  Proved, exact, for \(a\le7\).
* **Certified relations (Theorem T).**  Proved as an upper bound
  \(\dim\operatorname{im}\le\max(1,a-1)\); exact rank known only at
  \(a=1,2\) (\(=1\)) and \(a=3\) (\(=2\)).  Open for \(a\ge4\).
* **Level-3 second-order traces.**  All of \(\operatorname{tr}(P_3R)\),
  \(\operatorname{tr}(P_3R^2)\), \(\operatorname{tr}(P_3RA_{13})\),
  \(\operatorname{tr}(P_3A_{13}^2)\) are forced.  The free level-3 statistic
  is \(\|P_3RP_3\|_F^2\).  No contradiction found; no exhaustion claimed
  beyond these four values.
* **Triple profiles.**  See Section 5: consistency and non-determinacy only.
* **Symmetric square of \({\cal H}_1\).**  Pointwise products of two elements
  of \(\iota{\cal H}_1\) are \(\chi_{\cal C}\cdot(\text{global degree}\le2)\),
  hence lie in \(\iota({\cal H}_0\oplus{\cal H}_1\oplus{\cal H}_2)\), of
  dimension \(465=\binom{31}2=\dim\operatorname{Sym}^2{\cal H}_1\).  The
  correct narrow statement is that source and ambient dimensions **coincide**;
  this does *not* prove the product map is injective, and no absolute bound is
  thereby shown to be violated or saturated.  Earlier "exactly saturated"
  language is withdrawn.  For \({\cal H}_2\),
  \(\dim\operatorname{Sym}^2=94\,395\) exceeds the ambient
  \(1+30+434+4030+26\,970=31\,465\), so the map has a kernel of dimension at
  least \(62\,930\) and gives no bound.
* **Krein/Schur coupling of \(P_1,\dots,P_4\).**  What is verified is that the
  relevant Johnson Krein parameters are positive and that Schur products of
  \(P_1,\dots,P_4\) close inside \(P_0,\dots,P_8\), both forced by strength
  \(14\).  This closes the specific Krein-nonnegativity and Schur-rank tests
  performed in the committed follow-up.  It does **not** prove that every
  coupling argument involving these modules is exhausted; that broader claim
  is withdrawn.
* **Integrality at levels \(3\)–\(7\).**  Because the \(A_s\) do not act by
  scalars there, the simple "rational eigenvalue of an integer matrix is an
  integer" argument is unavailable.  That is all that is shown.  Whether
  characteristic-polynomial, lattice, Smith-normal-form, rank or congruence
  constraints bite at these levels is **not** settled here; the earlier claim
  that integrality "gives nothing" is withdrawn.

## 7. Inventory: proved here, versus open

**Proved (conditional on the assumed cover), and exactly verified:**
1. Theorem S, the staircase support \(\iota{\cal H}_a\subseteq
   E_a\oplus E_{15-a}\oplus\cdots\oplus E_{15}\) for \(0\le a\le7\), with all
   six measures and their moments.
2. Theorem T as an upper bound, with the certified relation counts
   \(13,13,12,11,10,9,8\), and the exact ranks at \(a=1,2,3\).
3. The forced level-3 values \(\operatorname{tr}(P_3RA_{13})=-75\,231\,854\)
   and \(\operatorname{tr}(P_3A_{13}^2)=392\,805\,898\), and the leakage
   identity \(\|(I-P_3)A_{13}P_3\|_F=\|(I-P_3)RP_3\|_F\).
4. \(d(B)=0\) and \(n_1(B)=120\) for every block of every \(S(14,15,31)\),
   hence the exact equivalence between the \(k=16\) cover and a large set of
   \(17\) disjoint \(S(14,15,31)\).
5. Rational consistency and non-determinacy of the \(234\)-equation triple
   profile system for all thirteen intersection classes.

**Open (not settled here):**
- the exact image ranks at levels \(a\ge4\);
- \(\|P_3RP_3\|_F^2\), and its level-\(a\) analogues;
- \({\cal E}\) (the level-2 \(\varepsilon\) statistic of the companion note);
- nonnegative-integral feasibility of the triple profiles;
- whether integrality/lattice constraints bite at levels \(\ge3\);
- **existence of the large set of \(17\) disjoint \(S(14,15,31)\), i.e. the
  \(k=16\) case itself;**
- **Erdős–Rosenfeld problem #835, which this note does not solve and does not
  claim to solve.**

## 8. Verification

```sh
python3 -B \
  collaboration/opus5/staircase_support_frontier/verify_staircase_support_frontier.py
```

Standard library only, exact integer/`Fraction` arithmetic, no floating point
in any decision, no randomness.  Runtime is dominated by the exact rational
elimination of the thirteen \(234\times169\) profile systems (a few minutes);
`--fast` skips that block.  The verifier asserts, among other things, the
level-2 counterexample explicitly: the support-derived upper bound is \(2\)
while the proved rank is \(1\).

# DRAFT — REJECTED closure attempt: the j-fold XOR arithmetic is NOT closed

Date: 2026-07-26.  Verifier:
`verify_s141531_higher_xor_integrality_closure_draft.py`.
Status: **audit record of a REJECTED argument.**  Standalone; modifies nothing
else.

> **Verdict.**  A first version of this draft claimed that Theorem C closes the
> all-\(j\) arithmetic of `s141531_higher_xor_hierarchy.md`.  **That claim is
> withdrawn as circular.**  Theorem C itself is valid and is retained below,
> but its hypothesis (H) is *precisely* full Fourier self-consistency of the
> unknown block indicator.  Lemma D below proves that, under the forced
> shape, (H) is equivalent to \(A\) being an \(S(14,15,31)\) — so invoking
> (H) invokes the missing design.
>
> **Historical status at this rejection point.**  Conditions (1)
> \(2^{31}\mid a_j(D)\) numerator, (2) \(2^{30}\mid A_j\) numerator, and
> (3) \(b\mid jA_j\) were then verified only for \(0\le j\le20\,000\) and its
> mirror.  The rejected Theorem-C argument does not settle them.
>
> **Subsequent status.**  A different, noncircular argument now closes the
> route: `s141531_higher_xor_2adic_closure.md` proves (1) by a Δ-lemma,
> tail theorem, and two independent finite-window certificates, while
> `s141531_xor_divisibility_reduction.md` proves (1) \(\Rightarrow\) (2),(3)
> from explicit binomial identities.  This audit is retained because its
> circularity diagnosis remains valid.  Nothing here or in those later route
> closures settles #835.

## 0. Notation

\(G=\mathbb F_2^{31}\) under symmetric difference; \(\mathbf 1\) the all-ones
vector; \(\chi_u(x^g)=(-1)^{u\cdot g}\).  For \(x\equiv b\pmod2\),
\(K_j(x)=[z^j](1+z)^{(b+x)/2}(1-z)^{(b-x)/2}\).  \(\varphi\), \(F_0=1549\),
\(F_1=-31219\), \(b=17\,678\,835\) are the constants of the hierarchy note.

## 1. Theorem C — valid, general, unconditional (RETAINED)

**Theorem C.**  Let \(n\ge1\), \(G=\mathbb F_2^n\), and \(F:G\to\mathbb Z\) any
function with \(F(u)\equiv F(0)\pmod2\) for all \(u\).  Put \(b=F(0)\) and
\(a_j(D):=2^{-n}\sum_u(-1)^{u\cdot D}K_j(F(u))\).  Assume

\[
 \textbf{(H)}\qquad a_1(D)\in\{0,1\}\ \text{for every }D\in G .
\]

Then \(a_j(D)\in\mathbb Z_{\ge0}\) for every \(j\ge0\) and \(D\); \(a_j\equiv0\)
for \(j>b\); \(\sum_Da_j(D)=\binom bj\).

*Proof.*  \(K_1(x)=x\), so \(a_1\) is the inverse transform of \(F\).  By (H)
it is the indicator of \(S:=\operatorname{supp}(a_1)\), and inversion gives
\(F(u)=\sum_{B\in S}(-1)^{u\cdot B}\) with \(|S|=\sum_Da_1(D)=F(0)=b\).  In
\(\mathbb Z[G][z]\),
\(\prod_{B\in S}(1+zx^B)=\sum_je_jz^j\) with
\(e_j=\sum_{|Y|=j,\,Y\subseteq S}x^{\operatorname{XOR}(Y)}\), so each \(e_j\)
has non-negative integer coefficients.  Applying \(\chi_u\) turns \(P(u)\) of
the factors into \(1+z\) and \(b-P(u)\) into \(1-z\), and
\(P(u)-(b-P(u))=F(u)\), so \(\chi_u(e_j)=K_j(F(u))\).  Inversion recovers
\([x^D]e_j=a_j(D)\). ∎

Theorem C is unconditional: no design, no Steiner property, no scheme.  Its
hypothesis (H) is the whole content.

## 2. The circular step (why the closure claim fails)

**(H) is Fourier self-consistency, not a scalar condition.**  \(a_1\) is the
inverse transform of \(F\); (H) says that transform is \(\{0,1\}\)-valued, i.e.
that \(F=\widehat{\mathbf 1_S}\) for **some** set \(S\subseteq G\).  A priori
\(S\) need be neither \(A\) nor constant-weight.  The following lemma closes
that gap, so the equivalence below is proved rather than asserted.

**Lemma D.**  Assume the forced shape: \(F(u)=\varphi(|u|)\) for \(|u|\le14\);
\(F(u^c)=-F(u)\) for all \(u\); and (S2), that on \(|u|=15\) \(F\) takes only
the values \(F_0\) and \(F_1=F_0-2^{15}\), the latter exactly \(b\) times, on a
set \(A\).  Assume (H), and put \(S=\operatorname{supp}(a_1)\), so
\(F=\widehat{\mathbf 1_S}\) and \(|S|=F(0)=b\).  Then every member of \(S\) has
size exactly \(15\), \(S\) is an \(S(14,15,31)\), and \(S=A\).

*Proof.*
**(a) Odd sizes.**  \(\widehat{\mathbf 1_S}(u^c)=\sum_{B\in S}(-1)^{|B|}
(-1)^{u\cdot B}\), so \(F(u^c)=-F(u)\) for all \(u\) gives
\(\sum_{B\in S}\bigl[(-1)^{|B|}+1\bigr](-1)^{u\cdot B}=0\) identically.  The
bracket is \(2\) on even-size members and \(0\) on odd ones, so the group-ring
element \(\sum_{|B|\ \mathrm{even}}x^{B}\) has vanishing transform, hence is
zero: **no member of \(S\) has even size.**

**(b) Low incidence numbers.**  Writing \(\lambda'_T=\#\{B\in S:T\subseteq B\}\)
and using \((-1)^{|u\cap B|}=\sum_{T\subseteq u\cap B}(-2)^{|T|}\),
\(F(u)=\sum_{T\subseteq u}(-2)^{|T|}\lambda'_T\).  Since \(\varphi(w)=
\sum_{i\le w}\binom wi(-2)^i\lambda_i\) for \(w\le14\), Möbius inversion on the
Boolean lattice gives \(\lambda'_T=\lambda_{|T|}\) for every \(|T|\le14\).

**(c) Constant weight 15.**  Let \(n_s=\#\{B\in S:|B|=s\}\).  Counting
incidences with 14-sets, \(\sum_sn_s\binom s{14}=\lambda_{14}\binom{31}{14}
=\binom{31}{14}=15b=15\sum_sn_s\).  For \(|u|=15\), (b) gives
\(F(u)=F_0+(-2)^{15}\lambda'_u\), so (S2) forces \(\lambda'_u\in\{0,1\}\) with
value \(1\) exactly \(b\) times; counting incidences with 15-sets,
\(\sum_sn_s\binom s{15}=b=\sum_sn_s\).  Subtracting \(15\times\) the second
relation from the first and using the identity

\[
 \binom s{14}-15\binom s{15}=\binom s{14}\,(15-s),
\]

we get \(\sum_sn_s\binom s{14}(15-s)=0\).  By (a) only odd \(s\) occur.  For
odd \(s\le13\) and for \(s=15\) the term vanishes; for odd \(s\ge17\) it is
strictly negative.  Hence \(n_s=0\) for \(s\ge17\), and then
\(\sum_sn_s[\binom s{15}-1]=0\) reduces to \(-\sum_{s\le13}n_s=0\), so
\(n_s=0\) there too.  Thus \(n_s=0\) unless \(s=15\).  (Step (a) is
load-bearing: \(s=14\) would contribute \(\binom{14}{14}(15-14)=+1\) and break
the sign argument.)

**(d) Design, and \(S=A\).**  By (b) with \(|T|=14\), every 14-set lies in
exactly \(\lambda_{14}=1\) member of \(S\), and by (c) all members have size
15, so \(S\) is an \(S(14,15,31)\).  Finally, for \(|u|=15\), \(\lambda'_u=1\)
iff \(u\in S\), so \(F(u)=F_1\iff u\in S\); by (S2) \(F(u)=F_1\iff u\in A\);
hence \(S=A\). ∎

Conversely, if \(A\) is an \(S(14,15,31)\) then \(F=\widehat{\mathbf 1_A}\) and
(H) holds.  Therefore, **under the forced shape**,

\[
 \textbf{(H)}\ \Longleftrightarrow\ A\ \text{is an }S(14,15,31).
\]

Assuming (H) to prove the arithmetic is therefore assuming the design.  (The
weaker statement suffices for the rejection: applying Theorem C via
\(F=\widehat{\mathbf 1_A}\) assumes exactly the global self-consistency that is
missing.  Lemma D upgrades that to a genuine equivalence.)

**Where the substitution enters.**  Theorem A of the hierarchy note computes
the middle-layer correction as

\[
 \frac{1}{2^{31}}\sum_u(-1)^{u\cdot D}\varepsilon_j(u)
 =\frac{\Delta_j}{2^{31}}\bigl[1+(-1)^{j+|D|}\bigr]\cdot\widehat{\mathbf 1_A}(D),
\]

and then **replaces \(\widehat{\mathbf 1_A}(D)\) by \(F(D)\)** to obtain the
layer/branch formula \(a_j(D)=g_j(|D|)+\Delta_jF(D)/2^{30}\).  That replacement
is exactly \(F=\widehat{\mathbf 1_A}\).  Consequently the "parametric" formula
already presupposes self-consistency, and any integrality argument built on it
inherits the assumption.

**Why the conditional implication is not enough.**  "A design exists \(\Rightarrow\)
\(a_j(D)\) is a subset count \(\Rightarrow\) integral" is true but inert.  It is
entirely compatible with the *fixed numeric formula* being non-integral at some
\(j\) — which would prove **non**existence.  Ruling that out requires an
arithmetic proof that does not route through the design; §1 does not provide
one.

## 3. Finite countermodel: layer-multiset/branch-count data does not determine (H)

Take \(n=3\), \(G=\mathbb F_2^3\), and the genuine set
\(S=\{000,011,101\}\), \(b=3\).  Then

\[
 F=\widehat{\mathbf 1_S}=(3,-1,1,1,1,1,-1,3)\quad(u=0,\dots,7),
\]

whose inverse transform is \(\mathbf 1_S\): (H) holds.  Now **swap the two
values inside weight layer 1**, at \(u=001\) and \(u=010\):

\[
 F'=(3,\,1,\,-1,\,1,\,1,\,1,\,-1,\,3).
\]

\(F'\) has **exactly the same weight-layer multisets** as \(F\) — layer 0:
\(\{3\}\); layer 1: \(\{-1,1,1\}\); layer 2: \(\{-1,1,1\}\); layer 3:
\(\{3\}\) — and exactly the same branch counts.  Only the assignment differs.
Yet its inverse transform is

\[
 a_1'=\bigl(1,\,-\tfrac12,\,\tfrac12,\,1,\,0,\,\tfrac12,\,\tfrac12,\,0\bigr),
\]

so (H) **fails**, and downstream \(a_3'\) is non-integral as well
(\(\pm\tfrac12\) at four points).

**Moral.**  The layer-multiset and branch-count data — which values occur on
each weight layer and how many \(u\) carry each — are *identical* in the two
cases, while (H) holds in one and fails in the other.  So **that data alone
does not determine whether (H) holds**; establishing (H) requires the full
assignment, i.e. global Fourier self-consistency.  In particular the layer-15
identity \(\sum_w\varphi(w)K_w(15)-2^{16}F_1=2^{31}\), offered in the withdrawn
version as the "one genuinely parametric residue", does not establish (H) for
an unknown block subset: it is a consequence of the substitution of §2, not an
independent check on an arbitrary \(A\).

Note the countermodel is a statement about what layer/branch data can
*determine*; it is not a counterexample to Lemma D, whose hypotheses include
the full forced shape (S1)–(S3), not merely the layer multisets.

## 4. Withdrawals

1. **Withdrawn:** "the all-\(j\) arithmetic is closed" and "conditions (1)–(3)
   can never fire".  They remain open for \(j>20\,000\).
2. **Withdrawn:** "Theorem C subsumes Theorem B."  It does not.  Theorem B of
   the hierarchy note is **non-circular**: its proof uses only the *value*
   bound \(|F(u)|\le b/31\) for nontrivial \(u\) — valid for every branch
   assignment — together with \(F(0)=b\), \(F(\mathbf 1)=-b\) and a Cauchy
   estimate.  It never uses \(F=\widehat{\mathbf 1_A}\).  Hence **positivity
   for all \(j\) stands**, and Theorem B remains the only unconditional all-\(j\)
   result here.
3. **Withdrawn:** "the \(j=1\) identity is the entire non-vacuous arithmetic
   content."  §3 refutes this.

## 5. What stood at the time of the rejection

| statement | status |
|---|---|
| Theorem C (general, unconditional) | **proved** |
| (H) \(\Leftrightarrow\) design, under the forced shape (Lemma D) | **proved** (§2) |
| layer-multiset/branch-count data does not determine (H) | **proved** by countermodel (§3) |
| non-negativity \(a_j(D)\ge0\), all \(j\) | **proved** (Theorem B, non-circular) |
| (1) \(2^{31}\mid a_j(D)\) numerator | **not proved here**; later closed by the 2-adic companion |
| (2) \(2^{30}\mid A_j\) numerator | **not proved here**; later derived from (1) |
| (3) \(b\mid jA_j\) | **not proved here**; later derived from (1) |

The finite sweep remains a legitimate test: it evaluates explicit rational
numbers built from \(\varphi,F_0,F_1,b\) and Krawtchouk values and checks
divisibility.  What is conditional is only the *interpretation* of those numbers
as subset counts; a non-integral value at any \(j\) would still refute the
design.

## 6. What a real closure needed, and what later supplied it

At this stage a real closure required either (a) a genuine 2-adic argument
bounding \(v_2\) of
\(\sum_wK_j(\varphi(w))K_w(d)+\Delta_jF(d,\varepsilon)(1+(-1)^{j+d})\) below
\(31\) never happening — with no appeal to self-consistency; or (b) a periodicity
/ finite-state reduction of that expression mod \(2^{31}\) in \(j\); or (c) a
certified counterexample at some \(j>20\,000\).  None is achieved by the
rejected Theorem-C argument.  The later Δ/tail/window proof supplies option
(a), and the formal differential identity supplies the reduction of (2),(3).

**#835 remains open; this particular proof remains rejected, while the
higher-XOR necessary-condition route is now closed by the later arguments.**

## 7. Reproducing

```bash
python3 -B evidence/verify_s141531_higher_xor_integrality_closure_draft.py
```

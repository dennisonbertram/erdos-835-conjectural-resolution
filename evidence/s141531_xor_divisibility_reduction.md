# Conditions (2) and (3) reduce to condition (1)

Date: 2026-07-26.  Verifier:
`verify_s141531_xor_divisibility_reduction.py`.
Status: **proved; exact verifier passed.**

> **What is proved.**  Working with the *forced constants only* — no design, no
> block set, no appeal to \(F=\widehat{\mathbf 1_A}\) — the all-\(j\)
> integrality of the layer/branch coefficients \(a_j(d,\varepsilon)\)
> **implies** both
> (2) integrality of \(A_j\) and (3) \(b\mid jA_j\), for every \(j\).
> The companion `s141531_higher_xor_2adic_closure.md` proves condition (1)
> for every \(j\), so together the two notes close all three arithmetic
> families.
>
> **What is not proved in this note.**  Condition (1) itself; that proof is
> external to this reduction.  **Erdős–Rosenfeld #835 remains open**, and
> closing this necessary-condition route does not establish or refute an
> \(S(14,15,31)\).

## 1. Formal setup (forced constants only)

All objects below are defined from explicit integers; no set of blocks is
assumed to exist.

\[
 \lambda_i=\frac{\binom{31-i}{14-i}}{15-i}\ (0\le i\le14),\qquad
 b=\lambda_0=17\,678\,835,
\]
\[
 \psi(w)=\sum_{i=0}^{\min(w,14)}\binom wi(-2)^i\lambda_i,\qquad
 \varphi(w)=\begin{cases}\psi(w),&w\le15\\[2pt]-\psi(31-w),&w\ge16,\end{cases}
\]
\[
 F_0=\varphi(15)=1549,\qquad F_1=F_0-2^{15}=-31219,
\]
\[
 K_w(d)=\sum_i(-1)^i\binom di\binom{31-d}{w-i}\quad(\text{Krawtchouk, }n=31).
\]

For \(F\equiv b\pmod2\) set
\(T_F(z)=(1+z)^{(b+F)/2}(1-z)^{(b-F)/2}\in\mathbb Z[[z]]\), and
\(D(z)=T_{F_1}(z)-T_{F_0}(z)\).  Note \(T_F(-z)=T_{-F}(z)\).

Branch values: \(F(d,\varepsilon)=\varphi(d)+(F_1-F_0)\varepsilon\) if
\(d=15\); \(\varphi(d)-(F_1-F_0)\varepsilon\) if \(d=16\); \(\varphi(d)\)
otherwise.  Define

\[
 a(z,d,\varepsilon)=\frac1{2^{31}}\Bigl[\sum_{w=0}^{31}K_w(d)\,T_{\varphi(w)}(z)
 +F(d,\varepsilon)\bigl(D(z)+(-1)^dD(-z)\bigr)\Bigr],
\]

whose coefficients are exactly the layer/branch quantities \(a_j(d,\varepsilon)\)
of the hierarchy note.  Put

\[
 A(z)=a(z,0,0)+a(z,31,0),\qquad C_B(z)=a(z,15,1)+a(z,16,1).
\]

**Hypothesis (I).**  \([z^j]a(z,d,\varepsilon)\in\mathbb Z\) for every \(j\),
every layer \(d\) and every branch \(\varepsilon\).  *(This is condition (1).)*

Two standard Krawtchouk facts are used: \(K_w(31-d)=(-1)^wK_w(d)\) and
\(K_{31-w}(d)=(-1)^dK_w(d)\).

## 2. Closed forms for \(A\) and \(C_B\)

**Lemma 1.**
\[
 A(z)=\frac1{2^{30}}\Bigl[\sum_{w\ \mathrm{even}}\tbinom{31}{w}T_{\varphi(w)}(z)
 +b\,D(-z)\Bigr],\qquad
 C_B(z)=\frac1{2^{30}}\Bigl[\sum_{w\ \mathrm{even}}K_w(15)T_{\varphi(w)}(z)
 -F_1D(-z)\Bigr].
\]

*Proof.*  \(K_w(0)=\binom{31}w\) and \(K_w(31)=(-1)^w\binom{31}w\), so
\(K_w(0)+K_w(31)=\binom{31}w(1+(-1)^w)\), which is \(2\binom{31}w\) for even
\(w\) and \(0\) otherwise.  The branch values are \(F(0,0)=b\),
\(F(31,0)=-b\), so the correction is
\(b(D(z)+D(-z))-b(D(z)-D(-z))=2bD(-z)\); divide by \(2^{31}\).

For \(C_B\): \(K_w(16)=(-1)^wK_w(15)\) gives
\(K_w(15)+K_w(16)=K_w(15)(1+(-1)^w)\).  The branch values are
\(F(15,1)=F_1\) and \(F(16,1)=\varphi(16)-(F_1-F_0)=-F_0-F_1+F_0=-F_1\), so
the correction is \(F_1(D(z)-D(-z))-F_1(D(z)+D(-z))=-2F_1D(-z)\). ∎

Since \(\varphi(16)=-F_0\) and \(D(-z)=T_{-F_1}-T_{-F_0}\), Lemma 1 shows
\(A(z)\) is exactly the generating function of
\(A_j=2^{-30}\sum_{|u|\ \mathrm{even}}K_j(F(u))\) with the forced
\(b\,/\,\binom{31}{16}-b\) split on the middle layer.

## 3. The two coefficient identities

**Lemma E1.**  \(\binom{31}{w}\varphi(w)=b\,K_w(15)\) for every
\(w\notin\{15,16\}\); in particular for every even \(w\ne16\).  Moreover
\(\binom{31}{15}F_0=b\bigl(K_{15}(15)+2^{15}\bigr)\).

*Proof.*  First, \(\binom{31}{i}\lambda_i=b\binom{15}{i}\) for \(i\le14\):
by \(\binom ni\binom{n-i}{k-i}=\binom nk\binom ki\) with \(n=31,k=14\),
\(\binom{31}i\binom{31-i}{14-i}=\binom{31}{14}\binom{14}i\), and
\((15-i)\binom{15}i=15\binom{14}i\), so
\(\binom{31}i\lambda_i=\binom{31}{14}\binom{14}i/(15-i)
=\binom{31}{14}\binom{15}i/15=b\binom{15}i\).

Next, \(\binom{31}{w}\binom wi=\binom{31}i\binom{31-i}{w-i}\), so

\[
 \tbinom{31}{w}\psi(w)=\sum_{i\le14}\tbinom{31}i\lambda_i(-2)^i\tbinom{31-i}{w-i}
 =b\sum_{i\le14}\tbinom{15}i(-2)^i\tbinom{31-i}{w-i}.
\]

Now the generating function
\(\sum_{i=0}^{15}\binom{15}i(-2)^i\binom{31-i}{w-i}
=[z^w](1+z)^{31}\bigl(1-\tfrac{2z}{1+z}\bigr)^{15}
=[z^w](1+z)^{16}(1-z)^{15}=K_w(15)\).
Subtracting the \(i=15\) term \(-2^{15}\binom{16}{w-15}\),

\[
 \tbinom{31}{w}\psi(w)=b\Bigl[K_w(15)+2^{15}\tbinom{16}{w-15}\Bigr].
\]

For \(w\le14\) the last binomial vanishes and \(\varphi=\psi\), giving the
claim; for \(w=15\) it gives \(\binom{31}{15}F_0=b(K_{15}(15)+2^{15})\).  For
\(w\ge17\), \(\varphi(w)=-\varphi(31-w)\) with \(31-w\le14\), and using
\(\binom{31}{w}=\binom{31}{31-w}\) together with \(K_{31-w}(15)=-K_w(15)\),
\(\binom{31}{w}\varphi(w)=-b\,K_{31-w}(15)=b\,K_w(15)\). ∎

**Lemma E2.**  \(-\bigl(\binom{31}{16}-b\bigr)F_0=b\,K_{16}(15)+b\,F_1\).

*Proof.*  Since \(F_1=F_0-2^{15}\), the claim is equivalent to
\(-\binom{31}{16}F_0=bK_{16}(15)-b\,2^{15}\).  Now \(\binom{31}{16}
=\binom{31}{15}\), so by the last part of Lemma E1,
\(-\binom{31}{16}F_0=-b(K_{15}(15)+2^{15})\); and \(K_{16}(15)=-K_{15}(15)\)
by \(K_{31-w}(d)=(-1)^dK_w(d)\) with \(d=15\) odd. ∎

## 4. Condition (2) follows from (1)

**Theorem E.**  Under (I), \(A_j\in\mathbb Z\) for every \(j\); equivalently
\(2^{30}\) divides the \(A_j\) numerator.

*Proof.*  \(A(z)=a(z,0,0)+a(z,31,0)\) by definition, and by Lemma 1 this is the
generating function of \(A_j\).  Both summands have integer coefficients by
(I). ∎

## 5. Condition (3) follows from (1)

**Lemma 2.**  \((1-z^2)\dot T_F=(F-bz)T_F\).

*Proof.*  \(\dot T_F/T_F=\frac{b+F}{2(1+z)}-\frac{b-F}{2(1-z)}\); multiplying by
\((1-z^2)=(1+z)(1-z)\) gives \(\frac{(b+F)(1-z)-(b-F)(1+z)}2=F-bz\). ∎

(At coefficient level this is exactly the Krawtchouk recurrence
\((j+1)K_{j+1}=FK_j-(b-j+1)K_{j-1}\).)

**Theorem F.**  Put \(\kappa(z)=\dfrac{zC_B(z)-z^2A(z)}{1-z^2}\).  Then

\[
 (1-z^2)\dot A=b\,(C_B-zA),\qquad\text{equivalently}\qquad
 b\,\kappa(z)=z\dot A(z),
\]

so \(b\,\kappa_j=jA_j\) for every \(j\).  Under (I), \(\kappa_j\in\mathbb Z\);
hence \(b\mid jA_j\) for every \(j\).

*Proof.*  Apply Lemma 2 termwise to the closed form of \(A\) in Lemma 1:

\[
 (1-z^2)\dot A=\frac1{2^{30}}\Bigl[\sum_{w\ \mathrm{even}}\tbinom{31}w
 (\varphi(w)-bz)T_{\varphi(w)}
 +b\bigl((-F_1-bz)T_{-F_1}-(-F_0-bz)T_{-F_0}\bigr)\Bigr],
\]

and the \(-bz\) parts reassemble to \(-bz\,A\).  Therefore

\[
 (1-z^2)\dot A+bzA=\frac1{2^{30}}\Bigl[\sum_{w\ \mathrm{even}}\tbinom{31}w
 \varphi(w)T_{\varphi(w)}-bF_1T_{-F_1}+bF_0T_{-F_0}\Bigr].
\]

By Lemma 1, \(b\,C_B=\frac1{2^{30}}\bigl[b\sum_{w\,\mathrm{even}}K_w(15)
T_{\varphi(w)}-bF_1T_{-F_1}+bF_1T_{-F_0}\bigr]\).  The \(T_{-F_1}\) terms are
identical, so the difference is

\[
 \frac1{2^{30}}\Bigl[\sum_{w\ \mathrm{even}}\bigl(\tbinom{31}w\varphi(w)
 -bK_w(15)\bigr)T_{\varphi(w)}+b(F_0-F_1)T_{-F_0}\Bigr].
\]

By Lemma E1 every summand with even \(w\ne16\) vanishes.  The \(w=16\) term is
\(\bigl(-\binom{31}{16}F_0-bK_{16}(15)\bigr)T_{-F_0}\) since
\(\varphi(16)=-F_0\) and \(T_{\varphi(16)}=T_{-F_0}\).  With
\(b(F_0-F_1)=b\,2^{15}\), the total coefficient of \(T_{-F_0}\) is

\[
 -\tbinom{31}{16}F_0-bK_{16}(15)+b\,2^{15},
\]

which is \(0\) by Lemma E2.  Hence \((1-z^2)\dot A=b(C_B-zA)\).  Multiplying by
\(z/(1-z^2)\) gives \(z\dot A=b\kappa\), i.e. \(jA_j=b\kappa_j\).

Finally \(\kappa_j\in\mathbb Z\): expanding \((1-z^2)^{-1}=\sum_{m\ge0}z^{2m}\),

\[
 \kappa_j=\sum_{m\ge0}\Bigl([z^{\,j-1-2m}]C_B-[z^{\,j-2-2m}]A\Bigr),
\]

a finite sum of coefficients of \(C_B\) and \(A\), each an integer by (I). ∎

## 6. What this does and does not do

* **Does:** removes conditions (2) and (3) from the open list.  Both are now
  algebraic consequences of (1), proved from the forced constants alone.  The
  proof never uses \(F=\widehat{\mathbf 1_A}\), never interprets \(a_j\) as a
  subset count, and never assumes a design exists — the only inputs are the
  definitions of §1, the two binomial identities of §3, and calculus (Lemma 2).
* **Does not:** prove condition (1) internally.  That separate task is completed
  by the Δ-lemma, finite-window certificates, and tail-collapse theorem in
  `s141531_higher_xor_2adic_closure.md`.

Note for the record: the *conceptual* reading of Lemma E1 —
"\(\sum_{|u|=w}F(u)=\sum_BK_w(|B|)\), all blocks having weight 15" — would use
self-consistency.  The proof in §3 deliberately does not take that route; it is
a binomial identity between explicit forced constants.

**#835 remains open.**

## 7. Reproducing

```bash
python3 -B evidence/verify_s141531_xor_divisibility_reduction.py
```

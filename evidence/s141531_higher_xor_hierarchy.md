# The higher block-XOR hierarchy of a hypothetical S(14,15,31)

Date: 2026-07-26.  Verifier: `verify_s141531_higher_xor_hierarchy.py`
(deterministic, exact integer arithmetic, standard library only).

> **Scope, stated up front.**  This note proves an explicit formula for the
> whole hierarchy (Theorem A), proves that its positivity conditions hold for
> **every** \(j\) (Theorem B), and verifies its remaining *integrality*
> conditions on an explicit finite range.  The integrality half is **not**
> closed, so the route is **not** closed, and this does **not** solve
> Erdős–Rosenfeld Problem #835.  Everything is conditional on the
> existence of an \(S(14,15,31)\).
>
> **Correction to an earlier draft of this note.**  A first version asserted
> that because the hierarchy is an inverse transform of the forced weight
> enumerator it "carries no information beyond it, so no level can yield a
> contradiction".  That is **wrong**, and the error is instructive: the
> MacWilliams/Delsarte necessary conditions are themselves transforms of forced
> spectral data, and they produce nonexistence proofs precisely by exposing a
> negative or non-integral coefficient.  Determined by the enumerator does not
> mean unable to contradict.  The earlier appeal to
> `collaboration/fable_parity_attack_2.md` Theorem 8.1 was also misplaced: that
> theorem is about *bilinear* invariants and does not cover degree-\(j\)
> coefficient-positivity tests.  The verdict in §6 is the corrected, weaker one.

## 0. Definitions

\(X=[31]\); \(\mathcal A\) a hypothetical \(S(14,15,31)\);
\(b=|\mathcal A|=\binom{31}{14}/15=17\,678\,835\).  Blocks are identified with
vectors of \(\mathbb F_2^{31}\) under symmetric difference; \(\mathbf 1\) is the
all-ones vector.  \(C\) is the binary point-incidence code (dimension 31),
\(C_0=\{x_S:|S|\text{ even}\}\) its even subcode (dimension 30), and
\(A_j:=A_j(C_0^\perp)\).

\(F(u)=\sum_{B\in\mathcal A}(-1)^{|u\cap B|}\);
\(a_j(D)=\#\{Y\subseteq\mathcal A:|Y|=j,\ \operatorname{XOR}(Y)=D\}\), so
\(m_D=a_2(D)\) and \(t_E=a_3(E)\); and
\(e_j=\sum_{|Y|=j}x^{\operatorname{XOR}(Y)}\).

Forced data: \(F(u)\) depends only on \(|u|\) except at \(|u|=15,16\), where it
is two-valued with \(F_0=1549\) (non-block), \(F_1=-31219\) (block),
\(F_1-F_0=-2^{15}\), and \(F(u^c)=-F(u)\).  \(\varphi(w)\) denotes the
non-block branch at weight \(w\).

## 1. Which \(j\)-subsets are dual words (PROVED)

**Proposition 1.**  \(Y\subseteq\mathcal A\) with \(|Y|=j\) is a dual word of
\(C_0\) iff \(d_p:=\#\{B\in Y:p\in B\}\) is constant mod 2; \(d\equiv0\) forces
\(j\) even and \(d\equiv1\) forces \(j\) odd.  Hence
\(A_j=a_j(0)\) for \(j\) even and \(A_j=a_j(\mathbf 1)\) for \(j\) odd.

*Proof.*  \(y\perp x_S\) reads \(\sum_{p\in S}d_p\equiv0\); requiring it for
every even \(|S|\) is constancy of \(d_p\).  Then \(\sum_pd_p=15j\): if
\(d\equiv0\) this is even so \(j\) is even; if \(d\equiv1\) it is
\(\equiv31\equiv1\) so \(j\) is odd.  Finally \(d\equiv0\iff
\operatorname{XOR}(Y)=0\) and \(d\equiv1\iff\operatorname{XOR}(Y)=\mathbf 1\). ∎

## 2. The transform (PROVED)

**Proposition 2.**  \(\prod_{B}(1+zx^B)=\sum_je_jz^j\) and
\(\chi_u(e_j)=K_j(F(u))\) where
\(K_j(F)=[z^j](1+z)^{(b+F)/2}(1-z)^{(b-F)/2}\).

*Proof.*  Expanding gives \(z^{|Y|}x^{\operatorname{XOR}(Y)}\) per subset.
Under \(\chi_u\) each factor becomes \(1+z(-1)^{u\cdot B}\); exactly
\(P(u)=(b+F(u))/2\) of them equal \(1+z\). ∎

**Proposition 3 (parity law).**  \(K_j(-F)=(-1)^jK_j(F)\).

*Proof.*  \(F\mapsto-F\) swaps \(P\) and \(Q=b-P\); substituting \(z\mapsto-z\)
in \((1+z)^P(1-z)^Q\) gives \((1-z)^P(1+z)^Q\), and
\([z^j]f(-z)=(-1)^j[z^j]f(z)\). ∎

**Theorem A (the general \(j\)-fold XOR law).**  With
\(\Delta_j=K_j(F_1)-K_j(F_0)\),

\[
 \boxed{\;a_j(D)=g_j(|D|)+\frac{\Delta_j\,F(D)}{2^{30}}\bigl[\,|D|\equiv j\ (2)\,\bigr],
 \qquad g_j(d)=\frac1{2^{31}}\sum_wK_j(\varphi(w))\,K_w(d).\;}
\]

So \(a_j(D)\) depends only on \(|D|\), except one split: at \(|D|=15\) for odd
\(j\) (by whether \(D\) is a block) and at \(|D|=16\) for even \(j\) (by whether
\(D^c\) is a block).

*Proof.*  \(a_j(D)=2^{-31}\sum_u(-1)^{u\cdot D}K_j(F(u))\).  Write
\(K_j(F(u))=K_j(\varphi(|u|))+\varepsilon_j(u)\); \(\varepsilon_j\) is supported
on \(|u|\in\{15,16\}\), equal to \(\Delta_j\mathbf 1_{\mathcal A}(u)\) at
\(|u|=15\) and, by Proposition 3, to \((-1)^j\Delta_j
\mathbf 1_{\mathcal A}(u+\mathbf 1)\) at \(|u|=16\).  Hence its transform is
\(\frac{\Delta_jF(D)}{2^{31}}[1+(-1)^{j+|D|}]\), using
\(\sum_{u\in\mathcal A}(-1)^{u\cdot D}=F(D)\).  The bracket is \(2\) exactly when
\(|D|\equiv j\pmod 2\), which is the only parity that occurs since
\(|D|\equiv15j\equiv j\). ∎

**Corollary A1 (what this does and does not give).**  Every \(a_j(D)\) and every
\(A_j\) is *computable in closed form* from the forced weight enumerator.  It
does **not** follow that these quantities are automatically admissible: they
must be non-negative integers, and that is a genuine arithmetic necessary
condition at every \(j\), of exactly the MacWilliams/Delsarte type.  Theorem A
converts the route into a *computable* infinite family of tests, not into a
closed one.

**Efficient evaluation.**  \(K_j\) obeys the three-term recurrence

\[
 (j+1)K_{j+1}(F)=F\,K_j(F)-(b-j+1)K_{j-1}(F),\qquad K_0=1,\ K_1=F,
\]

(the standard binary Krawtchouk recurrence with \(n=b\), \(x=(b-F)/2\), so
\(n-2x=F\)).  Only the 20 distinct arguments \(\{\varphi(w)\}\cup\{\pm F_1\}\)
are needed, all odd since \(F\equiv b\pmod 2\).  The verifier checks this
recurrence against the direct \([z^j]\) formula for \(j\le11\) at all 20
arguments.

**Symmetry.**  \(\lambda_1=8\,554\,275\) is odd, so every point lies in an odd
number of blocks and \(\operatorname{XOR}(\mathcal A)=\mathbf 1\).  Hence
\(Y\mapsto\mathcal A\setminus Y\) gives the exact symmetry

\[
 a_{b-j}(D)=a_j(\mathbf 1+D),
\]

so a sweep of \(0\le j\le J\) simultaneously covers \(b-J\le j\le b\).

## 3. The forced values

Validation: \(A_1=A_2=0\), \(A_3=927\,696\,866\,625\),
\(A_4=3\,793\,226\,637\,448\,341\,180\).  New:

\[
 A_5=13\,402\,303\,385\,620\,814\,734\,177\,080,\qquad
 A_6=39\,490\,202\,682\,224\,904\,419\,269\,612\,470\,360 .
\]

Triple differences \(t_E\) are non-negative integers, uniform on each odd layer,
symmetric under \(e\mapsto30-e\), with
\(\sum_Et_E=\binom b3=920\,893\,915\,145\,674\,553\,145\),
\(t_{\mathbf 1}=A_3\), and the \(|E|=15\) split \(858\,252\,625\,232\) (block)
versus \(858\,106\,686\,794\).

## 4. The exact identities (PROVED)

**(I5)** \(\displaystyle\sum_Dm_D\,t_{\mathbf 1+D}=10A_5+3(b-3)A_3
=134\,023\,083\,057\,999\,303\,311\,116\,800\).

*Proof.*  The left side counts pairs \((P,T)\), \(|P|=2\), \(|T|=3\), with
\(\operatorname{XOR}(P)+\operatorname{XOR}(T)=\mathbf 1\), no disjointness
imposed.  \(|P\cap T|=2\) would force the third block of \(T\) to be
\(\mathbf 1\), impossible for a weight-15 block.  \(|P\cap T|=0\) gives a
5-subset with XOR \(\mathbf 1\) — a weight-5 dual word — each arising from
\(\binom52=10\) splits.  \(|P\cap T|=1\), \(P=\{B,C\}\), \(T=\{B,D,E\}\),
forces \(C+D+E=\mathbf 1\): choose that weight-3 dual word (\(A_3\)), which of
its three elements is \(C\) (3), and \(B\notin\{C,D,E\}\) (\(b-3\)). ∎

**(I6)** \(\displaystyle\sum_Et_E^2=\binom b3+6(b-4)A_4+20A_6
=789\,804\,456\,004\,294\,991\,185\,507\,633\,323\,825\).

*Proof.*  Ordered pairs \((T_1,T_2)\) of 3-subsets with equal XOR.  \(T_1=T_2\)
gives \(\binom b3\).  \(|T_1\cap T_2|=2\) forces the two remaining blocks equal,
contributing 0.  \(|T_1\cap T_2|=1\) requires two distinct pairs with equal
difference — automatically disjoint — giving
\((b-4)\sum_Dm_D(m_D-1)=6(b-4)A_4\).  \(|T_1\cap T_2|=0\) gives a weight-6 dual
word, each with \(\binom63=20\) ordered splits. ∎

## 5. Positivity for every j (PROVED)

**Theorem B.**  For every \(j\) with \(40\le j\le b-40\) and every \(D\) with
\(|D|\equiv j\pmod 2\), \(a_j(D)>0\).

*Proof.*

*(i) Spectrum bound.*  \(F(0)=b\) and \(F(\mathbf 1)=-b\); for every other \(u\),
\(|F(u)|\le b/31=570\,285\), with equality exactly at weights \(1,2,29,30\).
(Finite exact check over the 32 forced weights and both branches at
\(|u|=15,16\); the largest nontrivial value is \(570\,285\) and
\(31\cdot570\,285=b\).)

*(ii) Normal form.*  Put \(f=|F|\) and \(Q=(b-f)/2\).  Since \((b+f)/2=Q+f\),

\[
 K_j(F)=\pm[z^j](1+z)^{Q+f}(1-z)^Q=\pm[z^j](1-z^2)^Q(1+z)^f,
\]

the sign being \((-1)^j\) when \(F<0\), by Proposition 3.

*(iii) Cauchy plus the maximal binomial term.*  For \(r>0\), Cauchy's estimate on
\(|z|=r\) with \(|1-z^2|\le1+r^2\) and \(|1+z|\le1+r\) gives
\(|K_j(F)|\le(1+r^2)^Q(1+r)^f/r^j\).  Take \(r=j/(b-j)\); then the ratio of
consecutive terms of \((1+r)^b=\sum_i\binom bi r^i\) is \(r(b-i)/(i+1)\), which
is \(\ge1\) at \(i=j-1\) and \(\le1\) at \(i=j\), so the largest term is the
\(j\)-th and \((1+r)^b\le(b+1)\binom bj r^j\).  Dividing, and using
\(b=2Q+f\),

\[
 \frac{|K_j(F)|}{\binom bj}\ \le\ (b+1)\Bigl[\tfrac{1+r^2}{(1+r)^2}\Bigr]^{Q}
 =(b+1)\,\rho^{\,b-f},\qquad \rho=\frac{\sqrt{1+r^2}}{1+r}.
\]

*(iv) Exponential form.*  \(\rho^2=1-\frac{2r}{(1+r)^2}\), and
\(\frac{2r}{(1+r)^2}\le\frac12<1\), so \(\ln\rho\le-\frac{r}{(1+r)^2}\).  With
\(r=j/(b-j)\) one has \(1+r=b/(b-j)\) and hence the exact identity
\(\frac{r}{(1+r)^2}=\frac{j(b-j)}{b^2}\).  By (i), \(b-f\ge30b/31\), and
\(\rho<1\), so

\[
 \rho^{\,b-f}\ \le\ \exp\Bigl(-\tfrac{30\,j(b-j)}{31\,b}\Bigr)=:e^{-E(j)}.
\]

*(v) Character split.*  \(a_j(D)=2^{-31}\sum_u(-1)^{u\cdot D}K_j(F(u))\).  The two
trivial characters give \(K_j(b)=\binom bj\) and \(K_j(-b)=(-1)^j\binom bj\),
contributing \(\bigl(1+(-1)^{j+|D|}\bigr)\binom bj\) — that is \(2\binom bj\) on
the forced parity, and \(0\) off it, consistently with Theorem A.  The remaining
\(2^{31}-2\) characters are nontrivial, so by (iii)–(iv) their total absolute
contribution is at most \((2^{31}-2)\binom bj(b+1)e^{-E(j)}\).

*(vi) Conclusion.*  \(a_j(D)>0\) as soon as
\(\tfrac12(2^{31}-2)(b+1)<e^{E(j)}\).  Now \(j(b-j)\), hence \(E\), is increasing
on \(j\le b/2\), and

\[
 E(40)=\tfrac{1200(b-40)}{31b}>\tfrac{77}{2}=38.5
 \quad\Longleftrightarrow\quad 60\cdot40\,(b-40)>2387\,b,
\]

which holds.  On the other side
\(\tfrac12(2^{31}-2)(b+1)=18\,982\,505\,595\,158\,028<2^{55}\) because
\(b+1<2^{25}\); and \(2^{55}<e^{38.5}\) because \(55\ln2<38.5\), i.e.
\(\ln2<0.7\), which follows from \(2.7<e\) and
\((27/10)^7=1046.0353\ldots>1024\).  Hence the error is strictly smaller than
the main term \(2\binom bj\) for \(40\le j\le b/2\), and the range
\(b/2\le j\le b-40\) follows from the symmetry \(a_{b-j}(D)=a_j(\mathbf 1+D)\). ∎

**Corollary B1 (non-negativity, all \(j\)).**  \(a_j(D)\ge0\) for **every**
\(0\le j\le b\) and every \(D\): strictly positive on the forced parity for
\(40\le j\le b-40\) by Theorem B, identically \(0\) off the forced parity by
Theorem A, and — for the residual \(0\le j\le39\) and its mirror
\(b-39\le j\le b\) — by the exact finite sweep of §7.

**Sharpness.**  The clean chain above (via \(38.5\) and \(2^{55}\)) certifies
\(j\ge40\).  With the exact constant
\(\ln\bigl(\tfrac12(2^{31}-2)(b+1)\bigr)=37.4823\ldots\) the argument already
works at \(j=39\); it genuinely fails at \(j=38\), where
\(E(38)=36.7741\ldots\).  Since the finite sweep covers \(j\le39\) either way,
nothing depends on which threshold is used.

## 6. The four mechanisms

- **Non-negativity.**  Now **settled for all \(j\)** by Corollary B1.  It was a
  genuine test — it is *tight* in places, e.g. \(a_2(0)=0\) and the whole
  \(|D|=30\) layer vanishes — and it is now closed.
- **Integrality.**  Still a genuine test at every \(j\), and **not** addressed
  by Theorem B: the analytic bound is archimedean and says nothing about the
  \(2\)-adic conditions \(2^{31}\mid\) numerator, \(2^{30}\mid\) the \(A_j\)
  numerator, or \(b\mid jA_j\).
- **Parity.**  No fixed-point-free involution is available on weight-\(j\) dual
  words, so no parity argument is in hand.
- **Convexity.**  Tight at \(j=4\) (\(\sum_D\binom{m_D}2=3A_4\)), which is what
  forces \(m_D\).  **Not** tight at \(j=6\): the slack of \(\sum_Et_E^2\) above
  its layer-balanced minimum is \(354\,375\,828\,032\,095\,615\,907\,520\), all
  of it from the \(|E|=15\) split.  So convexity forces nothing new at level 6.
- **Local conditioning.**  The punctured joint enumerator at a block is forced,
  so the count of weight-\(j\) dual words through a fixed block is the constant
  \(jA_j/b\), which must be a positive integer.  Verified for \(3\le j\le8\):
  \(157\,425\); \(858\,252\,625\,232\); \(3\,790\,493\,939\,680\,079\,240\); …
  In particular

  \[
   \frac{4A_4}{b}=858\,252\,625\,232=t_E\ (E\text{ a block}),
  \]

  forced structurally, since a weight-4 dual word through \(B_0\) is exactly a
  triple XOR-ing to \(B_0\).

## 7. Verdict

1. **Proved:** Propositions 1–3; Theorem A; the Krawtchouk recurrence; the
   symmetry \(a_{b-j}(D)=a_j(\mathbf 1+D)\); the identities (I5) and (I6); the
   \(j=6\) convexity slack; the per-block identity
   \(4A_4/b=858\,252\,625\,232\); and **Theorem B with Corollary B1, which
   settles non-negativity of \(a_j(D)\) for every \(0\le j\le b\)**.
2. **Verified, finite range:** exact **integrality** of \(a_j(D)\) on every
   layer \(|D|\in\{0,\dots,31\}\) and both branches, of \(A_j\), and the
   divisibility \(b\mid jA_j\), for

   \[
    \boxed{0\le j\le 20\,000}
   \]

   and hence, by the symmetry, also for \(b-20\,000\le j\le b\).  Recorded run:
   \(20\,001\) swept values of \(j\), \(364.9\) s, **zero violations**.  The two
   intervals are disjoint (since \(b-20\,000=17\,658\,835\)) and together contain
   \(20\,001+20\,001=40\,002\) of the \(17\,678\,836\) possible \(j\), about
   \(0.23\%\).  This sweep also supplies the residual \(j\le39\) needed by
   Corollary B1.
3. **Open:** the *arithmetic* half.  For \(20\,000<j<b-20\,000\) the integrality
   conditions — \(2^{31}\) dividing the \(a_j(D)\) numerator, \(2^{30}\) dividing
   the \(A_j\) numerator, and \(b\mid jA_j\) — are untested, and **no theorem
   closes them**.  Theorem B is archimedean and gives no information about these
   \(2\)-adic conditions.  Whether some larger \(j\) exposes a non-integral
   coefficient is unresolved.

So the route is now **half closed**: positivity is a theorem, integrality is
not.  **This does not solve Erdős–Rosenfeld Problem #835, and it does not close
this route.**

## 8. Reproducing

```bash
python3 -B evidence/verify_s141531_higher_xor_hierarchy.py                 # j <= 1000, ~2 s
python3 -B evidence/verify_s141531_higher_xor_hierarchy.py --max-j 20000   # the recorded range, ~6 min
```

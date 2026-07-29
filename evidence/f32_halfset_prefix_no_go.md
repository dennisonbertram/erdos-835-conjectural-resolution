# A 32-clique in the seven-coefficient transition graph over \(\mathbb F_{32}\)

This note closes a larger part of the half-set-polynomial route for a
putative tight colouring of \(J(32,16)\).  It does **not** prove that the
colouring does not exist.  It rules out every rule that uses only the first
seven coefficients of the selected half-set polynomial, even if its
postprocessing is arbitrary, nonlinear, and not complement-symmetric.

Label the 32 points by
\[
 F=\mathbb F_{32}=\mathbb F_2[\alpha]/(\alpha^5+\alpha^2+1).
\]
For a 16-set \(S\), write
\[
 P_S(Z)=\prod_{s\in S}(Z-s)
 =Z^{16}+a_1(S)Z^{15}+a_2(S)Z^{14}+\cdots+a_{16}(S).
\]
Thus \(a_i(S)=e_i(S)\), the \(i\)-th elementary symmetric sum (signs
disappear in characteristic two).

## Theorem

Let \(\Omega\) be any set and let
\[
 c(S)=f\bigl(a_1(S),a_2(S),\ldots,a_7(S)\bigr)
\tag{1}
\]
for an arbitrary function \(f:F^7\to\Omega\).  If \(c\) is a proper
colouring of \(J(32,16)\), then \(|\Omega|\ge32\).  In particular, no
17-colour rule of the form (1) can solve Erdős--Rosenfeld Problem #835 at
\(k=16\).

This is stronger than needed for complement-symmetric formulas: no
assumption that \(c(S)=c(F\setminus S)\) was used.

## A 32-clique of coefficient states

For every \(a\in F\), set
\[
 v(a)=(a,a^2,\ldots,a^7)\in F^7.
\]
We show that the 32 states \(v(a)\) form a clique in the transition graph
of the coefficient map
\[
 S\longmapsto(a_1(S),a_2(S),\ldots,a_7(S)).
\]
That is, for every distinct \(a,c\in F\), there are adjacent 16-sets
\(S_a,S_c\) whose coefficient prefixes are \(v(a),v(c)\), respectively.

The only finite certificate needed is the following lemma.

### Certificate lemma

For every \(r\in F\), there is a 15-set
\[
 U_r\subset F\setminus\{0,1\}
\]
such that
\[
 e_1(U_r)=e_2(U_r)=\cdots=e_7(U_r)=r. \tag{2}
\]

An explicit list of all 32 sets \(U_r\), in the five-bit field encoding,
is embedded in
[`verify_f32_halfset_prefix_no_go.py`](verify_f32_halfset_prefix_no_go.py).
The verifier directly checks (2), rather than relying on a probabilistic
search or a hash commitment.

### Constructing an edge

Fix distinct \(a,c\in F\), put \(d=a+c\), and let
\[
 r=\frac a d,
 \qquad T=c+dU_r.
\]
The exclusions in the certificate guarantee \(c,a\notin T\).  Hence
\[
 S_a=T\cup\{c\},\qquad S_c=T\cup\{a\}
\]
are adjacent 16-sets.

Let \(E_X(t)=\prod_{x\in X}(1+xt)\).  Equation (2) says, modulo
\(t^8\),
\[
 E_{U_r}(t)≡1+r(t+t^2+\cdots+t^7)
 \equiv\frac{1+(1+r)t}{1+t}.
\tag{3}
\]
The change of variables from \(U_r\) to \(T\) gives
\[
\begin{aligned}
 E_T(t)
 &= (1+ct)^{15}
 E_{U_r}\left(\frac{dt}{1+ct}\right)\\
 &\equiv \frac{(1+ct)^{15}}{1+at}
 \pmod {t^8}. \tag{4}
\end{aligned}
\]
Here the numerator introduced by (3) is
\[
 1+\bigl(c+(1+r)d\bigr)t
 =1+\bigl(c+d+a\bigr)t=1.
\]
Since every binomial coefficient \(\binom{15}{j}\) is odd,
\[
 (1+ct)^{15}=1+ct+c^2t^2+\cdots+c^{15}t^{15}.
\]
If \(q_j\) denotes the coefficient of \(t^j\) in (4), then for
\(0\le j\le7\),
\[
 q_j=\sum_{i=0}^j a^{j-i}c^i,
 \qquad q_j+cq_{j-1}=a^j,
 \qquad q_j+aq_{j-1}=c^j. \tag{5}
\]
Multiplying \(E_T\) by \(1+ct\), respectively \(1+at\), now proves
\[
 (a_1,a_2,\ldots,a_7)(S_a)=v(a),
 \qquad
 (a_1,a_2,\ldots,a_7)(S_c)=v(c). \tag{6}
\]

Properness forces \(f(v(a))\ne f(v(c))\) whenever \(a\ne c\).  Thus
the 32 values \(f(v(a))\) are distinct, proving the theorem.

## Consequence for the complement-symmetric polynomial

Put \(H_S=P_S+P_{F\setminus S}\).  The first relevant coefficients of
\(H_S\) are functions of the selected coefficients.  For example,
\[
\begin{aligned}
 h_2&=a_1^2,\\
 h_3&=a_1^3,\\
 h_4&=a_1^4+a_1^2a_2+a_2^2,\\
 h_5&=a_1^5+a_1a_2^2+a_1^2a_3,\\
 h_6&=a_1^6+a_1^4a_2+a_2^3+a_3^2+a_1^2a_4.
\end{aligned}
\tag{7}
\]
More generally, write \(A(t)=1+u(t)\), where
\(u(t)=a_1t+a_2t^2+\cdots\).  Reversing
\(P_S P_{F\setminus S}=Z^{32}+Z\) gives
\(A(t)A_{F\setminus S}(t)=1+t^{31}\), so below degree 31 the companion
series is \(A(t)^{-1}\).  In characteristic two,
\[
 A(t)+A(t)^{-1}=u(t)^2+u(t)^3+u(t)^4+\cdots.
\]
For \(j\ge4\), the coefficient of \(t^j\) on the right involves no
\(a_{j-1}\).  The square \(u(t)^2\) contains only square monomials, and
in \(u(t)^m\) for \(m\ge3\), a factor \(a_{j-1}t^{j-1}\) would leave at
least \(m-1\) further positive degrees, exceeding \(j\).  Hence \(h_j\)
depends only on \(a_1,\ldots,a_{j-2}\).  Every formula obtained by arbitrary
postprocessing of the prefix
\[
 (h_2,h_3,\ldots,h_9)
\]
therefore factors through (1), and cannot be a 17-colouring.  This includes
all normalized-coefficient, Artin--Schreier, trace, and Möbius formulas
that use no information from \(h_{10}\) or later.

The result does **not** apply to the full polynomial \(H_S\): as noted in
the preceding half-set audit, the full \(H_S\) recovers the complement
pair \(\{S,F\setminus S\}\).  Thus it is a rigorous no-go for a broad
low-coefficient family, not a resolution of Problem #835.

Run:

```bash
python3 evidence/verify_f32_halfset_prefix_no_go.py
```

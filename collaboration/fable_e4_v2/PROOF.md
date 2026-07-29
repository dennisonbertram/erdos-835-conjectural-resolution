# Independent proof: an actual-edge \(K_{18}\) in the five-statistic \(F_{32}\) quotient

Date: 2026-07-25.  Author: Claude Fable 5 (second, independent audit).

This file contains a complete, self-contained proof of the claimed
\(K_{18}\), with every finite-field computation displayed so that it can
be audited line by line without running any program.  The companion
checker `verify_k18_independent.py` replays the same claim by recomputing
every elementary symmetric coefficient of every exchanged \(16\)-set from
its roots; it was written from scratch for this audit and shares no code
with the discovering agent's verifier.  (Execution note: no code could be
run in the session that produced this file — every execution channel was
permission-denied — so the proof below was carried out and cross-checked
entirely by exact hand computation; the scripts are provided for machine
replay.)

## 0. Conventions

\(F=\mathbb F_2[\alpha]/(\alpha^5+\alpha^2+1)\), with the standard five-bit
encoding: the integer \(z=\sum_i z_i2^i\) encodes \(\sum_i z_i\alpha^i\).
Addition is XOR (written \(\oplus\) when integers are displayed).
A \(32\)-bit mask has bit \(z\) set iff the field element \(z\) belongs to
the set.

For a finite \(S\subset F\) write
\(\prod_{b\in S}(1+bt)=\sum_j e_j(S)\,t^j\), so \(e_j(S)\) is the \(j\)-th
elementary symmetric function of \(S\).  The five-statistic map on
\(16\)-sets is
\[
 \sigma(S)=\bigl(e_1,e_2,e_3,e_4,\;\lambda\bigr),\qquad
 \lambda(S)=e_8(S)+e_1(S)^8 .
\]
Two values of \(\sigma\) are joined ("actual edge") when they are realized
by \(16\)-sets meeting in \(15\) points.

**Discrete-log table.**  \(\alpha=2\) generates \(F^\times\).  Repeated
doubling with reduction \(\alpha^5=\alpha^2+1\) (XOR by \(37\) upon
overflow) gives
\[
\begin{array}{r|rrrrrrrrrrrrrrrr}
i&0&1&2&3&4&5&6&7&8&9&10&11&12&13&14&15\\
2^i&1&2&4&8&16&5&10&20&13&26&17&7&14&28&29&31\\\hline
i&16&17&18&19&20&21&22&23&24&25&26&27&28&29&30&31\\
2^i&27&19&3&6&12&24&21&15&30&25&23&11&22&9&18&1
\end{array}
\]
Step 31 returns to \(1\) and all 31 nonzero values occur, which
simultaneously proves that \(x^5+x^2+1\) is irreducible (the ring has 31
units) and self-checks the table.  Products below are computed as
\(ab=2^{(\log a+\log b)\bmod 31}\).

## 1. Two lemmas

**Lemma 1 (completion identity).**  For a finite \(T\subset F\) and
\(p\notin T\), writing \(\tau_j=e_j(T)\),
\[
 e_j(T\cup\{p\})=\tau_j+p\,\tau_{j-1}.
\]
*Proof.* Multiply \(\sum_j\tau_jt^j\) by \((1+pt)\). \(\square\)

**Lemma 2 (Frobenius).**  \((1+p)^8=1+p^8\) for all \(p\in F\), because
squaring is a field automorphism and \(x\mapsto x^8\) is its cube.
\(\square\)

## 2. The three base sets and their invariants

The claimed masks decode (bit \(z\) = element \(z\)) to
\[
\begin{aligned}
B_0=\texttt{0x7975CD00}&=\{8,10,11,14,15,16,18,20,21,22,24,27,28,29,30\},\\
B_1=\texttt{0x149693B9}&=\{0,3,4,5,7,8,9,12,15,17,18,20,23,26,28\},\\
B_2=\texttt{0xFA3041BA}&=\{1,3,4,5,7,8,14,20,21,25,27,28,29,30,31\},
\end{aligned}
\]
each of size \(15\) (hex digit popcounts: \(7975CD00\to3{+}2{+}3{+}2{+}2{+}3=15\);
\(149693B9\to1{+}1{+}2{+}2{+}2{+}2{+}3{+}2=15\);
\(FA3041BA\to4{+}2{+}2{+}0{+}1{+}1{+}3{+}2=15\)).

**Proposition.**  For each \(i\),
\[
 \prod_{b\in B_i}(1+bt)\equiv 1+t \pmod{t^5},\qquad
 e_7(B_i)=12,\qquad e_8(B_i)=5 .
\]

*Proof.*  Each product is computed in two halves; each half is a full
(untruncated) polynomial, checked by evaluation; the halves are then
convolved.  Every line below is one application of Lemma 1 inside a half.

**\(B_0\), half \(A=\{8,10,11,14,15,16,18\}\)** (rows = coefficients
\(e_0,e_1,\dots\) after inserting the row's element):

```
+8 : 1  8
+10: 1  2 26
+11: 1  9 12  5
+14: 1  7 29  7 19
+15: 1  8 21 13 27 26
+16: 1 24  1 26 21 22 28
+18: 1 10 13  8 24 14 23 14
```
Check: sum of coefficients \(=1\); directly
\(\prod(1\oplus b)=9\cdot11\cdot10\cdot15\cdot14\cdot17\cdot19\):
log-sum \(29{+}27{+}6{+}23{+}12{+}10{+}17=124\equiv0\), value \(2^0=1\). ✓

**\(B_0\), half \(C=\{20,21,22,24,27,28,29,30\}\):**

```
+20: 1 20
+21: 1  1  9
+22: 1 23 31 23
+24: 1 15  4 18 27
+27: 1 20  9 17  4  2
+28: 1  8  5 22 11 29 29
+29: 1 21 22 16 12 12 11 22
+30: 1 11  9  8 26 16 23 26 24
```
Check: coefficient sum \(=20\); directly
\(21\cdot20\cdot23\cdot25\cdot26\cdot29\cdot28\cdot31\):
log-sum \(22{+}7{+}26{+}25{+}9{+}14{+}13{+}15=131\equiv7\), \(2^7=20\). ✓

**Convolution** \(a=[1,10,13,8,24,14,23,14]\), \(c=[1,11,9,8,26,16,23,26,24]\),
\(\tau_k=\bigoplus_{i+j=k}a_ic_j\):

```
τ1 = 11 ⊕ 10                                            = 1
τ2 = 9 ⊕ (10·11=4) ⊕ 13                                 = 0
τ3 = 8 ⊕ (10·9=16) ⊕ (13·11=16) ⊕ 8                     = 0
τ4 = 26 ⊕ (10·8=26) ⊕ (13·9=10) ⊕ (8·11=18) ⊕ 24        = 0
τ7 = 26 ⊕ (10·23=2) ⊕ (13·16=14) ⊕ (8·26=14) ⊕ (24·8=30)
        ⊕ (14·9=17) ⊕ (23·11=21) ⊕ 14                   = 12
τ8 = 24 ⊕ (10·26=31) ⊕ (13·23=8) ⊕ (8·16=20) ⊕ (24·26=18)
        ⊕ (14·8=31) ⊕ (23·9=30) ⊕ (14·11=13)            = 5
```

**\(B_1\)**: the element \(0\) contributes the factor \(1\); halves
\(A=\{3,4,5,7,8,9,12\}\), \(C=\{15,17,18,20,23,26,28\}\):

```
+3 : 1  3                     +15: 1 15
+4 : 1  7 12                  +17: 1 30  4
+5 : 1  2 23 25               +18: 1 12 11  2
+7 : 1  5 25 19  5            +20: 1 24  0 10 13
+8 : 1 13 20  5  9 13         +23: 1 15 27 10 15  8
+9 : 1  4 30  0  1  6 10      +26: 1 21 25 19 16 10 14
+12: 1  8 11 28  1 10  7 23   +28: 1  9  9  7  2 25  8 25
```
Checks: \(A\): coefficient sum \(=5\); directly
\(2\cdot5\cdot4\cdot6\cdot9\cdot8\cdot13\): log-sum
\(1{+}5{+}2{+}19{+}29{+}3{+}8=67\equiv5\), \(2^5=5\). ✓
\(C\): coefficient sum \(=12\); directly
\(14\cdot16\cdot19\cdot21\cdot22\cdot27\cdot29\): log-sum
\(12{+}4{+}17{+}22{+}28{+}16{+}14=113\equiv20\), \(2^{20}=12\). ✓

Convolution \(a=[1,8,11,28,1,10,7,23]\), \(c=[1,9,9,7,2,25,8,25]\):

```
τ1 = 9 ⊕ 8                                              = 1
τ2 = 9 ⊕ (8·9=2) ⊕ 11                                   = 0
τ3 = 7 ⊕ (8·9=2) ⊕ (11·9=25) ⊕ 28                       = 0
τ4 = 2 ⊕ (8·7=29) ⊕ (11·9=25) ⊕ (28·9=7) ⊕ 1            = 0
τ7 = 25 ⊕ (8·8=10) ⊕ (11·25=24) ⊕ (28·2=29) ⊕ (1·7=7)
        ⊕ (10·9=16) ⊕ (7·9=26) ⊕ 23                     = 12
τ8 = (8·25=22) ⊕ (11·8=18) ⊕ (28·25=20) ⊕ (1·2=2)
        ⊕ (10·7=19) ⊕ (7·9=26) ⊕ (23·9=30)              = 5
```

**\(B_2\)**: halves \(A=\{1,3,4,5,7,8,14\}\),
\(C=\{20,21,25,27,28,29,30,31\}\):

```
+1 : 1  1                     +20: 1 20
+3 : 1  2  3                  +21: 1  1  9
+4 : 1  6 11 12               +25: 1 24 16 15
+5 : 1  3 21 14 25            +27: 1  3 26  3 13
+7 : 1  4 28 10 22  5         +28: 1 31 27 22 12 24
+8 : 1 12 25 17 12  4 13      +29: 1  2 18  4 11 16 16
+14: 1  2 27 27 25  6 16 12   +30: 1 28 11 11 28 28  6 22
                              +31: 1  3 29 12 27 10 16 30 14
```
Checks.  \(A\) contains \(1\), so \(P_A(1)=0\); coefficient sum is indeed
\(0\).  Stronger check at \(t=2\): from the coefficients,
\(\bigoplus_j a_j2^j=13\); directly
\(\prod_{b\in A}(1\oplus2b)=3\cdot7\cdot9\cdot11\cdot15\cdot17\cdot29\):
log-sum \(18{+}11{+}29{+}27{+}23{+}10{+}14=132\equiv8\), \(2^8=13\). ✓
\(C\): coefficient sum \(=2\); directly
\(21\cdot20\cdot24\cdot26\cdot29\cdot28\cdot31\cdot30\): log-sum
\(22{+}7{+}21{+}9{+}14{+}13{+}15{+}24=125\equiv1\), \(2^1=2\). ✓
At \(t=2\): from coefficients \(\bigoplus_j c_j2^j=4\); directly
\(\prod(1\oplus2b)=12\cdot14\cdot22\cdot18\cdot28\cdot30\cdot24\cdot26\):
log-sum \(20{+}12{+}28{+}30{+}13{+}24{+}21{+}9=157\equiv2\), \(2^2=4\). ✓

Convolution \(a=[1,2,27,27,25,6,16,12]\), \(c=[1,3,29,12,27,10,16,30,14]\):

```
τ1 = 3 ⊕ 2                                              = 1
τ2 = 29 ⊕ (2·3=6) ⊕ 27                                  = 0
τ3 = 12 ⊕ (2·29=31) ⊕ (27·3=8) ⊕ 27                     = 0
τ4 = 27 ⊕ (2·12=24) ⊕ (27·29=18) ⊕ (27·3=8) ⊕ 25        = 0
τ7 = 30 ⊕ (2·16=5) ⊕ (27·10=21) ⊕ (27·27=2) ⊕ (25·12=29)
        ⊕ (6·29=4) ⊕ (16·3=21) ⊕ 12                     = 12
τ8 = 14 ⊕ (2·30=25) ⊕ (27·16=12) ⊕ (27·10=21) ⊕ (25·27=17)
        ⊕ (6·12=13) ⊕ (16·29=3) ⊕ (12·3=20)             = 5
```

Independent cross-checks of \(\tau_1\): the direct XOR of all fifteen
elements of \(B_0\), of \(B_1\), and of \(B_2\) each equals \(1\). ✓
This proves the Proposition. \(\square\)

## 3. The eighteen states and the closed-form fifth coordinate

Let \(X=\{0,1,2,6,9,10,11,12,13,16,17,19,22,23,24,25,26,31\}\) be the 18
claimed parameters, with claimed states \(v_x=(1{+}x,\,x,\,0,\,0,\,
\lambda(x))\).

**Lemma 3.**  For every \(i\) and every \(p\notin B_i\),
\[
 \sigma(B_i\cup\{p\})=(1+p,\;p,\;0,\;0,\;4\oplus 12p\oplus p^8).
\]
*Proof.*  By the Proposition, \(\tau=(1,1,0,0,0,\ast,\ast,12,5)\) in
degrees \(0..8\) (degrees 5 and 6 are irrelevant).  Lemma 1 gives
\(e_1=1{+}p\), \(e_2=0{+}p\cdot1=p\), \(e_3=0{+}p\cdot0=0\),
\(e_4=0\), \(e_8=5+12p\), and by Lemma 2
\(\lambda=e_8+e_1^8=5+12p+(1{+}p)^8=5+12p+1+p^8=4\oplus12p\oplus p^8\).
\(\square\)

**Lemma 4.**  \(4\oplus12x\oplus x^8\) equals the claimed \(\lambda\) for
all eighteen \(x\in X\).

*Proof.*  \(12x=2^{(20+\log x)\bmod31}\) and \(x^8=2^{(8\log x)\bmod31}\):

```
 x   12x  x^8  4⊕12x⊕x^8   claimed
 0    0    0       4          4
 1   12    1       9          9
 2   24   13      17         17
 6   13   22      31         31
 9    3   31      24         24
10   23   19       0          0
11   27   18      13         13
12   26    5      27         27
13   22    4      22         22
16   30    2      24         24
17   18    3      21         21
19   10   14       0          0
22   19   20       3          3
23   31   21      14         14
24   17   28       9          9
25   29   29       4          4
26    9   17      28         28
31   16   11      31         31
```
All eighteen rows agree. \(\square\)

Note the strength of this check: the eighteen matches are eighteen
independent linear equations that would each fail under almost any
arithmetic slip in \(\tau_7\) or \(\tau_8\); moreover the three base sets
gave the same pair \((\tau_7,\tau_8)=(12,5)\) by three disjoint
computations.

## 4. Coverage and the theorem

**Lemma 5.**  The miss-sets \(M_i=X\cap B_i\) are
\[
 M_0=\{10,11,16,22,24\},\quad
 M_1=\{0,9,12,17,23,26\},\quad
 M_2=\{1,25,31\},
\]
and they are pairwise disjoint.

*Proof.*  Read off the three displayed base sets against \(X\); the three
listed sets share no element (direct inspection). \(\square\)

So \(B_i\) realizes \(18-|M_i|\) of the claimed states — \(13\), \(12\)
and \(15\) respectively.  (No single base realizes all eighteen, and none
needs to.)

**Theorem.**  The eighteen states \(v_x\), \(x\in X\), form an
actual-edge \(K_{18}\) in the five-statistic quotient.

*Proof.*  The states are pairwise distinct (their second coordinates
\(x\) are distinct).  Let \(\{x,y\}\subset X\).  A two-element set meets
at most two of the three pairwise-disjoint sets \(M_0,M_1,M_2\), so some
\(M_i\) satisfies \(\{x,y\}\cap M_i=\emptyset\), i.e. \(x,y\notin B_i\).
Then \(S_x=B_i\cup\{x\}\) and \(S_y=B_i\cup\{y\}\) are \(16\)-sets with
\(S_x\cap S_y=B_i\) of size \(15\) — an actual Johnson edge — and by
Lemmas 3–4, \(\sigma(S_x)=v_x\), \(\sigma(S_y)=v_y\).  Hence all
\(\binom{18}2=153\) pairs are actual edges. \(\square\)

**Corollary (death of the five-statistic family).**  If
\(c(S)=G\bigl(e_1,e_2,e_3,e_4,e_8+e_1^8\bigr)(S)\) is a proper colouring
of \(J(32,16)\), for **any** function \(G\colon F^5\to\) colours, then
\(c\) uses at least \(18\) colours.  In particular no tight
\(17\)-colouring factors through these five statistics.

*Proof.*  Properness forces different colours across each actual edge.
The eighteen states are pairwise joined by actual edges, so
\(G\) must take eighteen distinct values on them.  This argument uses
nothing about \(G\) — monotonicity, algebraicity, regularity are all
irrelevant, because \(G\) enters only through being constant on fibres of
\(\sigma\). \(\square\)

## 5. Precise scope: what this does and does not rule out

Ruled out: every colouring rule of \(J(32,16)\) whose colour depends on
\(S\) only through the five values
\(e_1(S),e_2(S),e_3(S),e_4(S),e_8(S)+e_1(S)^8\) — with completely
arbitrary postprocessing \(G\), for every choice of the \(2^{25}\)-point
codomain partition.  This strictly supersedes the four-statistic
\(K_{32}\) note (which allowed arbitrary \(G\) on
\((e_1,e_2,e_3,e_8+e_1^8)\)) in the direction of retaining \(e_4\), and
it settles the question left open by
`f32_five_statistic_moment_curve_clique_bound.md`: the moment-curve
subfamily has clique number \(17\), but the **full** five-statistic
quotient contains a \(K_{18}\) — the new clique lives on the line
\((e_1,e_2)=(1{+}x,x)\), which is disjoint from the moment curve since
\(e_2=e_1^2\) and \(e_2=1+e_1\) would force \(e_1^2+e_1+1=0\), impossible
in \(\mathbb F_{32}\) (no subfield \(\mathbb F_4\)).

Not ruled out, and why:

1. **Arbitrary colourings.**  A proper colouring of \(J(32,16)\) need not
   be constant on \(\sigma\)-fibres.  The 51 actual \(16\)-sets used above
   lie in three stars; within one star a proper colouring is merely
   rainbow, which any 17-colouring satisfies.  The contradiction lives
   entirely in the quotient, so nothing here constrains an unrestricted
   colouring.
2. **Richer statistics.**  Retaining any further separating information —
   \(e_5\), \(e_6\), \(e_7\), \(e_8\) itself, or non-symmetric invariants —
   refines the quotient and the present clique need not survive
   refinement (each of its states splits into many refined states, and
   the specific edges used here connect specific refined states only).
3. **Other \(k\).**  Everything is specific to \(k=16\),
   \(F=\mathbb F_{32}\).

Hence this is a family-kill theorem, not a resolution of
Erdős–Rosenfeld #835: it neither constructs a tight \(17\)-colouring nor
proves nonexistence.

## 6. Beyond the family: exact adjacency rigidity for prefix quotients

The following theorems are new, hold for every \(k\) with \(|F|=2k\)
(and in fact over any field, mutatis mutandis), and reduce the next
frontier — the six-statistic quotient retaining \(e_5\) — to a sharply
constrained finite search.  Proofs are complete; the \(k=2\) and \(k=4\)
controls are in §7.

**Lemma 6 (deletion identity).**  Let \(R\subset F\) be finite,
\(\rho_j=e_j(R)\), and \(x\in R\).  Then for all \(j\),
\[
 e_j(R\setminus\{x\})=\sum_{i=0}^{j}\rho_{j-i}\,x^{\,i}.
\]
*Proof.*  \(\prod_{b\in R\setminus\{x\}}(1+bt)=\rho(t)/(1+xt)\) and
\(1/(1+xt)=\sum_i x^it^i\) in \(F[[t]]\) (char 2). \(\square\)

**Setting.**  Let \(A\ne B\) be states of the \(m\)-prefix quotient
\((e_1,\dots,e_m,\lambda)\), \(m\ge2\), realized by \(16\)-sets \(S_A,S_B\)
with \(|S_A\cap S_B|=15\).  Write \(R=S_A\cup S_B\) (a \(17\)-set),
\(S_A=R\setminus\{u\}\), \(S_B=R\setminus\{v\}\), \(s=e_1(A)+e_1(B)\).

**Theorem R1 (determined witness).**  \(s\neq0\) — adjacent states have
distinct \(e_1\) — and the witness data are determined by the pair:
\[
 \rho_1=\frac{e_2(A)+e_2(B)}{s}+s,\qquad
 u=e_1(B)+\frac{e_2(A)+e_2(B)}{s},\qquad
 v=e_1(A)+\frac{e_2(A)+e_2(B)}{s},
\]
and then recursively
\(\rho_j=e_j(A)+\sum_{i=1}^{j}\rho_{j-i}u^i\) for \(j=2,\dots,m\).

*Proof.*  From Lemma 6 at \(j=1\): \(e_1(A)=\rho_1+u\),
\(e_1(B)=\rho_1+v\); subtracting, \(u+v=s\), and \(u\ne v\) forces
\(s\ne0\).  At \(j=2\): \(e_2(A)+e_2(B)=\rho_1(u+v)+(u^2+v^2)
=\rho_1s+s^2\), giving \(\rho_1\); then \(u=e_1(A)+\rho_1\),
\(v=e_1(B)+\rho_1\), which simplify as displayed.  The recursion is
Lemma 6 at \(j\le m\) solved for \(\rho_j\). \(\square\)

**Theorem R2 (pair conditions).**  With the determined values of
Theorem R1, adjacency of \(A\) and \(B\) requires, for every
\(3\le j\le m\), the closed-form condition
\[
 C_j:\qquad e_j(B)=\sum_{i=0}^{j}\rho_{j-i}\,v^{\,i}
 \qquad(\rho_0=1),
\]
i.e. \(m-2\) polynomial identities in the two states' coordinates.
Conversely, \(A\sim B\) **iff** \(C_3,\dots,C_m\) hold and there exists an
actual \(17\)-set \(R\supset\{u,v\}\) with prefix
\((\rho_1,\dots,\rho_m)\) whose tail satisfies the two linear equations
\[
 \lambda(A)+e_1(A)^8=\sum_{i=0}^{8}\rho_{8-i}u^{\,i},\qquad
 \lambda(B)+e_1(B)^8=\sum_{i=0}^{8}\rho_{8-i}v^{\,i}.
\]
*Proof.*  Necessity: Lemma 6 applied to \(B=R\setminus\{v\}\) for
\(j\le m\), and to \(e_8\) for the \(\lambda\) equations
(\(\lambda=e_8+e_1^8\) by definition).  Sufficiency: given such an \(R\),
the two deletions realize exactly the states \(A\) and \(B\) and meet in
15 points. \(\square\)

Consequences.

* For the five-statistic quotient (\(m=4\)) there are exactly two pair
  conditions \(C_3,C_4\); the residual freedom is the choice of
  \((\rho_5,\rho_6,\rho_7,\rho_8)\) of an actual \(17\)-set, constrained
  by two linear equations.  This freedom is why the \(K_{18}\) above
  could exist.
* For the six-statistic quotient \((e_1,\dots,e_5,e_8+e_1^8)\) a third
  condition \(C_5\) appears, and \(\rho_5\) becomes determined: the
  \(17\)-set must hit a codimension-\(2^{30}\) prefix class **and**
  satisfy two linear tail equations on \((\rho_6,\rho_7,\rho_8)\).
  Heuristically \(\binom{32}{17}\approx2^{29.07}\) while a full
  \((\rho_1,\dots,\rho_5)\)-class plus two tail equations costs
  \(2^{35}\): a *typical* determined witness class is empty, so six-stat
  quotient adjacency is sparse.  This is a search-design fact, not a
  theorem about cliques.

**Theorem R3 (star form; explains the certificate's shape).**  Every
witness of an edge between two "line states"
\(v_x=(1{+}x,x,0,0,\cdot)\), \(v_y\) is a \(15\)-set \(T=R\setminus\{x,y\}\)
with
\[
 e(T)\equiv 1+t\pmod{t^5},
\]
whose added points are exactly \(p=x\), \(q=y\), and whose seventh and
eighth coefficients satisfy, for both endpoints,
\[
 \lambda(z)=\bigl(e_8(T)+1\bigr)+e_7(T)\,z+z^8,\qquad z\in\{x,y\}.
\]
*Proof.*  By Lemma 1, \(e_1(T\cup\{p\})=\tau_1+p=1+x\) and
\(e_2=\tau_2+p\tau_1=x\); with the same two equations at \(q,y\),
subtracting gives \(p+q=x+y\) and \(\tau_1(p+q)=x+y\), so \(\tau_1=1\),
whence \(p=x\), \(q=y\), \(\tau_2=x+p=0\); then \(e_3=0\) forces
\(\tau_3=0\) and \(e_4=0\) forces \(\tau_4=0\).  The \(\lambda\) formula
is Lemma 3's computation with \(\tau_7,\tau_8\) generic. \(\square\)

So *any* clique in the line family is governed by the fibration of
prefix-\((1,1,0,0,0)\) \(15\)-sets over their \((\tau_7,\tau_8)\); the
certificate's three bases all sit in the single fibre
\((\tau_7,\tau_8)=(12,5)\), which is what makes one global function
\(\lambda(x)=4\oplus12x\oplus x^8\) work, and any two bases in one fibre
can share every state whose parameter avoids both.

## 7. Controls at \(k=2\) and \(k=4\)

The identities of §6 are proved in general, but per the audit protocol
they are controlled on the two decided cases.  (The companion script
`verify_rigidity_and_controls.py` performs the exhaustive versions; the
instances below were done by hand.)

**\(k=2\), \(F_4=\mathbb F_2[\omega]/(\omega^2+\omega+1)\).**
Lemma 6 on \(R=\{0,1,\omega\}\): \(\rho=(1,\;1{+}\omega,\;\omega,\;0)\)
in degrees \(0..2\) (\(\rho_1=1+\omega=\omega^2\), \(\rho_2=\omega\)),
and for \(x=1\): \(e_1(R\setminus\{1\})=\rho_1+1=\omega\) ✓ (direct:
\(0+\omega\)), \(e_2=\rho_2+\rho_1+1=\omega+\omega^2+1=0\) ✓ (direct:
\(0\cdot\omega\)).  At \(k=2\) the conditions \(C_j\), \(j\ge3\), are
vacuous (there is no \(e_3\)), consistent with the fact that a tight
\(3\)-colouring of \(J(4,2)\) **exists**: the machinery produces no false
obstruction at the true-positive control.

**\(k=4\), \(F_8=\mathbb F_2[\beta]/(\beta^3+\beta+1)\)** (encode
\(\beta=2\); \(\log\) table \(1,2,4,3,6,7,5\) for \(i=0..6\)).
Take \(R=\{1,2,3,4,6\}\).  Sequential expansion gives
\(e(R)=[1,2,2,3,1,3]\) in degrees \(0..5\).  Deleting \(x=4\):
direct expansion of \(\{1,2,3,6\}\) gives \([1,6,7,2,2]\); Lemma 6
predicts \(e_1=2{\oplus}4=6\), \(e_2=2\oplus(2\cdot4){\oplus}(4\cdot4)
=2\oplus3\oplus6=7\), \(e_3=3\oplus(2\cdot4)\oplus(2\cdot6)\oplus4^3
=3\oplus3\oplus7\oplus5=2\), \(e_4=1\oplus(3\cdot4)\oplus(2\cdot6)
\oplus(2\cdot5)\oplus4^4=1\oplus7\oplus7\oplus1\oplus2=2\).  All four
agree. ✓  At \(k=4\) the analogue quotient machinery has conditions
\(C_3,C_4\); the exhaustive control in the script checks them on all
\(560\) actual edges of \(J(8,4)\).  (At \(k=4\) the tight \(5\)-colouring
is known not to exist — `verify_k4.py` — so the control here is only that
the *identities* hold on every actual edge, i.e. no false negative.)

## 8. What was and was not machine-checked

Everything in §§0–5 above is a complete displayed computation: the log
table (self-checking), six half-product tables (each with one or two
evaluation identities checked against an independent product-of-values
computation), three term-by-term convolutions, the direct XOR
confirmation of \(\tau_1=1\) for all three bases, and the 18-row
\(\lambda\) table.  Additional end-to-end spot checks performed:
\(e_1(B_2\cup\{2\})=3\) and \(e_1(B_1\cup\{2\})=3\) by direct XOR of all
sixteen elements — two different realizations of the same state \(v_2\),
agreeing with Lemma 3.

The companion scripts (`verify_k18_independent.py`,
`verify_rigidity_and_controls.py`) recompute every claim from the roots
of every actual set with no reliance on the structure above; they could
not be executed in the authoring session (all execution channels were
permission-denied) and should be run on first opportunity.  The
hand-verified proof stands on its own.

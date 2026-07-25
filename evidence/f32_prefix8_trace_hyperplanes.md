# The trace-hyperplane classification at coefficient eight

This note replaces the enumerated 16-value spectrum in
[`f32_prefix8_affine_boundary.md`](f32_prefix8_affine_boundary.md) by an
algebraic classification.  It also determines exactly what that
classification does to the 32 lifted moment-curve states at coefficient
eight.

The result is sharp but is **not** a solution of Erdős--Rosenfeld Problem
#835.  At seven coefficients the same family gave a 32-clique.  At eight
coefficients each nonzero lift splits into one 17-clique and 15 isolated
vertices.  Thus this route reaches exactly the required number of colours,
not a contradiction.

Throughout,
\[
 F=\mathbb F_{32},\qquad
 \operatorname {Tr}(x)=x+x^2+x^4+x^8+x^{16}.
\]
For a finite set \(U\subset F\), let \(e_i(U)\) be its \(i\)-th elementary
symmetric sum.

## 1. Algebraic classification

### Theorem 1

Let \(U\subset F^\times\) have size 15 and suppose
\[
 e_1(U)=e_2(U)=\cdots=e_7(U)=0. \tag{1}
\]
Put \(u=e_8(U)\).  Then \(u\ne0\), and there is a unique \(b\in F^\times\)
such that
\[
 U=\{x\in F^\times:\operatorname {Tr}(bx)=0\},
 \qquad u=b^{-8}. \tag{2}
\]

Conversely, every \(b\in F^\times\) gives a set in (2) satisfying (1).

Consequently, if one also requires \(1\notin U\), then the candidates are
exactly those with \(\operatorname {Tr}(b)=1\).  There are 16 of them, and
their eighth coefficients are exactly
\[
 \{u\in F^\times:\operatorname {Tr}(u^{-1})=1\}. \tag{3}
\]

### Proof

Form the root polynomial after adjoining zero:
\[
 L(X)=X\prod_{x\in U}(X+x).
\]
Condition (1) gives
\[
 L(X)=X^{16}+uX^8+\sum_{i=1}^7 c_iX^i. \tag{4}
\]
All roots of \(L\) lie in \(F\), so \(L\) divides \(X^{32}+X\).  Therefore
\[
 L\mid (X^{32}+X)+L^2. \tag{5}
\]

If \(u=0\), the polynomial on the right of (5) has degree less than 16.
It would have to vanish identically, which is impossible because its
coefficient of \(X\) is 1.  Hence \(u\ne0\).  The right side of (5) now has
degree 16 and leading coefficient \(u^2\), so it must equal \(u^2L\).
Comparing coefficients gives
\[
 L(X)=X^{16}+uX^8+u^{-14}X^4+u^{-6}X^2+u^{-2}X. \tag{6}
\]
For completeness, the comparisons start with
\[
 c_1=u^{-2},\quad c_2=u^{-6},\quad c_3=0,\quad
 c_4=u^{-14},\quad c_5=c_6=c_7=0;
\]
the coefficient of \(X^8\) is then automatic because \(u^{31}=1\).

The map \(b\mapsto b^{-8}\) permutes \(F^\times\), since
\(\gcd(8,31)=1\).  Let \(b\) be the unique element with \(u=b^{-8}\).
Using \(b^{31}=1\), equation (6) becomes
\[
 \begin{aligned}
 L(X)
 &=X^{16}+b^{-8}X^8+b^{-12}X^4+b^{-14}X^2+b^{-15}X\\
 &=b^{-16}\operatorname {Tr}(bX). \tag{7}
 \end{aligned}
\]
Thus the roots of \(L\) are exactly the trace hyperplane
\(\ker(x\mapsto\operatorname {Tr}(bx))\), proving (2).  Equation (7) also
proves the converse.

Finally, \(1\notin U\) is equivalent to \(\operatorname {Tr}(b)=1\).
Since \(u^{-1}=b^8\) and trace is invariant under Frobenius,
\[
 \operatorname {Tr}(u^{-1})
 =\operatorname {Tr}(b^8)
 =\operatorname {Tr}(b),
\]
which proves (3).  \(\square\)

This proves algebraically, rather than by enumerating
\(\binom{30}{15}\) sets, the 16-value spectrum used in the earlier affine
boundary theorem.

## 2. The exact lifted moment-curve graph

Let \(\Gamma_8\) be the coefficient transition graph: two elements of
\(F^8\) are adjacent if they occur as the first eight coefficient vectors
of two adjacent 16-subsets of \(F\).

For \(\lambda\in F\), define
\[
 w_\lambda(a)
  =(a,a^2,\ldots,a^7,a^8+\lambda),\qquad a\in F. \tag{8}
\]

### Theorem 2

The graph induced in \(\Gamma_8\) by
\(\{w_\lambda(a):a\in F\}\) is:

* 32 isolated vertices if \(\lambda=0\);
* a \(K_{17}\) together with 15 isolated vertices if \(\lambda\ne0\).

For \(\lambda\ne0\), the parameters of the clique are exactly
\[
 R_\lambda
 =\{0\}\cup
 \{a\in F:\operatorname {Tr}(\lambda^{-4}a)=1\}. \tag{9}
\]
Equivalently, its 16 affine-hyperplane points satisfy
\(\operatorname {Tr}(a^8/\lambda)=1\).

### Proof

Suppose two distinct states \(w_\lambda(a)\) and \(w_\lambda(c)\) are
realized by adjacent 16-sets \(A\) and \(C\).  Write
\[
 A=T\cup\{x\},\qquad C=T\cup\{y\}.
\]
Thus \(y\) is the point missing from \(A\), and \(x\) is the point missing
from \(C\).

Let \(P_A(X)=\prod_{s\in A}(X+s)\), and similarly for \(P_C\).  The common
17-set \(R=A\cup C\) has root polynomial
\[
 P_R(X)=(X+y)P_A(X)=(X+x)P_C(X). \tag{10}
\]
Comparing the coefficients of \(X^{16}\) and \(X^{15}\) in (10) gives
\[
 a+y=c+x=:s,\qquad as=cs.
\]
Because \(a\ne c\), this forces \(s=0\), hence
\[
 y=a,\qquad x=c. \tag{11}
\]

Now use the first eight coefficients in (8).  Multiplication by \(X+a\)
cancels the geometric sequence \(a,a^2,\ldots,a^8\), leaving
\[
 P_R(X)=X^{17}+\lambda X^9+B(X),\qquad \deg B\le8. \tag{12}
\]
Let \(Q(X)\) be the root polynomial of the 15-point complement \(F\setminus
R\).  Since \(P_RQ=X^{32}+X\), comparison of the first eight elementary
coefficients gives
\[
 Q(X)=X^{15}+\lambda X^7+A(X),\qquad \deg A\le6. \tag{13}
\]

It remains important to know which factor contains zero.  Write
\[
 A(X)=\sum_{i=0}^6 A_iX^i,\qquad
 B(X)=\sum_{j=0}^8 B_jX^j.
\]
Comparing degrees 23 down to 17 in the product of (12) and (13) yields
\[
 B_{i+2}=A_i\quad(0\le i\le6).
\]
The coefficient of \(X^{16}\) gives \(B_1=\lambda^2\), and the coefficient
of \(X^{15}\) gives
\[
 B_0+\lambda B_8+\lambda A_6=B_0=0. \tag{14}
\]
Thus \(0\in R\), so all 15 roots of \(Q\) lie in \(F^\times\).

Theorem 1 applies to those roots, with eighth coefficient \(\lambda\).  If
\(\lambda=0\), no such complement exists, so there are no edges.  If
\(\lambda\ne0\), the complement is uniquely
\[
 \{x\in F^\times:\operatorname {Tr}(bx)=0\},
 \qquad b^{-8}=\lambda.
\]
Here \(b=\lambda^{-4}\), since
\((b^{-8})^{-4}=b^{32}=b\).  Therefore the only possible common 17-set is
exactly \(R_\lambda\) in (9).  In particular, every edge has both parameter
vertices in \(R_\lambda\).

Conversely, fix \(a\in R_\lambda\) and put \(S_a=R_\lambda\setminus\{a\}\).
The root polynomial of \(R_\lambda\) has its first seven elementary
coefficients zero and its eighth coefficient \(\lambda\).  From
\[
 P_{R_\lambda}(X)=(X+a)P_{S_a}(X)
\]
one obtains recursively
\[
 e_j(S_a)=a^j\quad(1\le j\le7),\qquad
 e_8(S_a)=a^8+\lambda. \tag{15}
\]
Hence \(S_a\) has state \(w_\lambda(a)\).  For distinct
\(a,c\in R_\lambda\), the sets \(S_a,S_c\) are adjacent.  Thus all 17
vertices indexed by \(R_\lambda\) form a clique, and the preceding
uniqueness shows that the other 15 vertices are isolated.  \(\square\)

## 3. What this does and does not prove

The trace identity does **not** upgrade the seven-coefficient 32-clique to
an 18-clique or larger at coefficient eight.  It proves the opposite sharp
statement for this entire lifted moment-curve family: its chromatic number
is exactly 17 when \(\lambda\ne0\).

The same \(K_{17}\) survives under the complement-symmetric prefix
\((h_2,\ldots,h_{10})\).  This prefix depends only on
\((a_1,\ldots,a_8)\), and \(h_2=a_1^2=a^2\) already distinguishes the 17
parameters in (9).  Therefore these states give an exact lower bound of 17
colours for that prefix, but not the \(18\)-colour lower bound that would
rule out a tight colouring.

Nothing here gives a clique obstruction for the full
\(H_S=P_S+P_{F\setminus S}\).  Its later coefficients contain information
not determined by \((a_1,\ldots,a_8)\), so Theorem 2 does not classify
their transitions.

Nor is (9) by itself a 17-colour construction.  It only identifies a
17-colouring of each explicit 32-state slice separately inside the full
transition graph.  A construction would still have to assign one common
palette of 17 colours to every
coefficient state and satisfy every transition between the slices.  No such
extension is supplied here.

There is a canonical way to identify every local clique with one fixed
17-element palette:
\[
 {\cal C}=\{0\}\cup\{z\in F:\operatorname {Tr}(z)=1\},\qquad
 a\longmapsto\lambda^{-4}a.
\]
The most direct attempt to extend it to an arbitrary coefficient state is
to put
\[
 \lambda=a_8+a_1^8,\qquad z=\lambda^{-4}a_1,
\]
return \(z\) when \(\lambda\ne0\) and \(\operatorname {Tr}(z)=1\), and
return \(0\) otherwise.  This attempt already fails on the adjacent sets
\[
 \begin{aligned}
 T&=\{0,5,6,7,8,10,11,14,16,20,24,25,26,29,31\},\\
 A&=T\cup\{2\},\qquad C=T\cup\{21\},
 \end{aligned}
\]
in the five-bit field encoding: both receive colour \(0\).  The verifier
checks this collision directly.  This only rejects the canonical naive
extension, not every possible 17-colour formula.

Run the independent finite-field audit:

```bash
python3 evidence/f32_prefix8_trace_classification_verifier.py
```

It constructs all 31 trace hyperplanes, exhaustively checks that they are
all the 15-subsets of \(F^\times\) satisfying (1), recovers the 16-set
restricted spectrum (3), and directly checks all 31 resulting
17-cliques.

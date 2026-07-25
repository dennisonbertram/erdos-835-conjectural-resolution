# The coefficient-eight boundary of the affine 32-clique template

This is an exact boundary result for the affine construction used in
[`f32_halfset_prefix_no_go.md`](f32_halfset_prefix_no_go.md).  That
construction gives a 32-clique after the first seven elementary symmetric
coefficients.  It cannot be continued through the eighth coefficient by the
same translation--dilation template, even if the eighth coordinate of the
32 proposed clique vertices is allowed to be an arbitrary function.

This is **not** a nonexistence proof for a tight 17-colouring of
\(J(32,16)\), nor even a proof that the eight-coefficient transition graph
has no 32-clique.  It rules out one precise way of extending the existing
seven-coefficient clique certificate.

## Setup

Let
\[
 F=\mathbb F_{32}=\mathbb F_2[\alpha]/(\alpha^5+\alpha^2+1).
\]
For a set \(X\subset F\), write \(e_i(X)\) for its elementary symmetric
sums.  The degree-seven certificate used a 15-set
\(U\subset F\setminus\{0,1\}\) with
\[
 e_1(U)=\cdots=e_7(U)=r, \tag{1}
\]
then, for distinct \(a,c\in F\), put
\[
 d=a+c,\qquad r=a/d,\qquad T=c+dU,
\]
and compare the two adjacent half-sets \(T\cup\{c\}\) and
\(T\cup\{a\}\).

The question here is whether this template can give a 32-clique in the
eight-coefficient transition graph with fixed vertices
\[
 (a,a^2,\ldots,a^7,\eta(a))\quad(a\in F), \tag{2}
\]
where \(\eta:F\to F\) is completely arbitrary.  A witness \(U\) in (1)
is allowed to depend on the ordered pair \((a,c)\), so the result does not
assume the 32 degree-seven witnesses are reused.

## Theorem

No such affine translation--dilation certificate exists.

Equivalently: there is no function \(\eta:F\to F\) such that for every
distinct \(a,c\in F\), some \(U\subset F\setminus\{0,1\}\) satisfying
(1) makes the two sets above have the eight coefficient states in (2).

### Exact finite input

Among all 15-subsets \(U\) of \(F\setminus\{0,1\}\) satisfying
\[
 e_1(U)=\cdots=e_7(U)=0, \tag{3}
\]
the possible eighth coefficients are exactly
\[
 \{1,3,5,6,7,12,17,20,21,22,23,24,25,26,28,29\}. \tag{4}
\]
In particular, zero is not possible, and only 16 of the 31 nonzero field
elements occur.  The accompanying verifier establishes (4) by an exhaustive
meet-in-the-middle enumeration of all \(\binom{30}{15}\) candidates.  It
enumerates all \(2^{15}\) subsets in each half, uses exact truncated
polynomial inversion to pair them, and directly recomputes every accepted
product.  There are exactly 16 accepted 15-sets.

### Proof

Set \(u=e_8(U)\).  With
\[
 E_X(t)=\prod_{x\in X}(1+xt),
\]
condition (1) says, modulo \(t^9\),
\[
 E_U(t)=\frac{1+(1+r)t}{1+t}+(u+r)t^8. \tag{5}
\]
The first term has coefficient \(r\) in every positive degree.  Applying
the affine change of variables gives
\[
 E_T(t)=(1+ct)^{15}E_U\!\left(\frac{dt}{1+ct}\right).
\]
The extra term in (5) contributes exactly \((u+r)d^8t^8\) modulo \(t^9\).
For the first term, the calculation from the degree-seven certificate gives
\[
 E_{T\cup\{c\}}(t)\equiv\frac1{1+at},\qquad
 E_{T\cup\{a\}}(t)\equiv(1+ct)^{15}\pmod {t^9}.
\]
All binomial coefficients \(\binom{15}{j}\), \(0\le j\le8\), are odd.
Therefore
\[
 \begin{aligned}
 e_8(T\cup\{c\})&=a^8+(u+r)d^8,\\
 e_8(T\cup\{a\})&=c^8+(u+r)d^8. \tag{6}
 \end{aligned}
\]

If these are the fixed states (2), equation (6) implies
\[
 \eta(a)+a^8=\eta(c)+c^8
\]
for every distinct pair.  Thus there is a constant \(\lambda\in F\) with
\[
 \eta(x)=x^8+\lambda\quad\text{for all }x\in F. \tag{7}
\]
Now take \(a=0\) and let \(c\) run through \(F^\times\).  Then
\(r=0\), \(d=c\), and (6)--(7) require
\[
 e_8(U)=\lambda/c^8. \tag{8}
\]
If \(\lambda=0\), this contradicts (4), which excludes zero.  If
\(\lambda\ne0\), the map \(c\mapsto\lambda/c^8\) permutes
\(F^\times\), because \(\gcd(8,31)=1\).  Equation (8) would require every
one of its 31 nonzero values to occur in (4), whereas only 16 occur.  This
is again a contradiction.  \(\square\)

## Interpretation

The seven-coefficient 32-clique has a genuine sharp obstruction at the
eighth coefficient in this affine scheme.  In particular, simply searching
for improved witnesses \(U_r\), allowing them to depend on each edge, cannot
turn that certificate into a no-go theorem for arbitrary postprocessing of
\((a_1,\ldots,a_8)\).  A successful coefficient-eight no-go would need a
different clique or a different chromatic lower-bound mechanism; a positive
formula would need to evade this particular affine template as well.

Run:

```bash
python3 evidence/f32_prefix8_affine_boundary_verifier.py
```

# The \(\mathbb F_{32}\) half-set polynomial and its 17-value no-go

Label the 32 ground points by \(\mathbb F_{32}\).  For a half-set
\(S\in\binom{\mathbb F_{32}}{16}\), put
\[
 P_S(Z)=\prod_{s\in S}(Z-s)
 =Z^{16}+a_1Z^{15}+a_2Z^{14}+\cdots .
\]
Let \(\bar S=\mathbb F_{32}\setminus S\) and define the
complement-symmetric polynomial
\[
 H_S(Z)=P_S(Z)+P_{\bar S}(Z).
\]
A tight colouring would have to be complement-symmetric, so it is natural
to seek 17 colours among the leading coefficients of \(H_S\).

## 1. The exact 17-value candidate

Write
\[
 H_S(Z)=h_1Z^{15}+h_2Z^{14}+h_3Z^{13}+h_4Z^{12}+\cdots .
\]
Since
\[
 P_S(Z)P_{\bar S}(Z)=Z^{32}-Z=Z^{32}+Z
\]
in characteristic two, comparison of the first four coefficients gives
\[
\begin{aligned}
 h_1&=0,\\
 h_2&=a_1^2,\\
 h_3&=a_1^3,\\
 h_4&=a_2^2+a_1^2a_2+a_1^4. \tag{1}
\end{aligned}
\]
Equivalently, put
\[
 A(t)=1+a_1t+a_2t^2+\cdots .
\]
Up to degree 30 the complementary series is \(A(t)^{-1}\), and
\[
 A+A^{-1}
 =\frac{(A+1)^2}{A}
 =(A+1)^2+(A+1)^3+\cdots ,
\]
which immediately yields (1).

When \(a_1\ne0\), normalize the first coefficient containing information
beyond \(a_1\):
\[
 \theta(S)=\frac{h_4}{h_2^2}
 =z^2+z+1,\qquad z=\frac{a_2}{a_1^2}. \tag{2}
\]
The absolute trace satisfies
\[
 \operatorname{Tr}_{32/2}(\theta(S))
 =\operatorname{Tr}(z^2+z)+\operatorname{Tr}(1)=1,
\]
because the extension degree is five.  There are exactly 16 trace-one
elements of \(\mathbb F_{32}\).  This produces the canonical-looking
17-value rule
\[
 \kappa(S)=
 \begin{cases}
 \infty,&a_1=0,\\
 \theta(S),&a_1\ne0.
 \end{cases} \tag{3}
\]
It is complement-symmetric.  Indeed the total sum of the field is zero,
so the complement has the same \(a_1\); coefficient comparison gives
\(\bar a_2=a_2+a_1^2\), which replaces \(z\) by \(z+1\) and leaves
\(z^2+z+1\) unchanged.

Thus (3) is not an arbitrary guess: it is the first genuinely new
normalized invariant in the complement-symmetric half-set polynomial,
and its range has exactly the target size 17.

## 2. A whole-star obstruction

The rule (3) is not a proper colouring.  Let \(T\) be a 15-set and write
\(\sigma(T)=\sum_{t\in T}t\).  For an extension \(S=T\cup\{x\}\),
\[
 a_1(S)=\sigma(T)+x. \tag{4}
\]
The exceptional colour \(\infty\) therefore occurs in the star over \(T\)
if and only if \(\sigma(T)\notin T\).  If
\(\sigma(T)\in T\), all 17 allowed extensions have nonzero \(a_1\), so
all 17 receive values in the 16-element trace-one set.  Two extensions
must have the same colour.

Such stars exist abundantly.  In the standard five-bit representation of
the additive group of \(\mathbb F_{32}\), take
\[
 T=\{0,1,2,3,4,5,6,7,8,9,10,11,12,16,23\}.
\]
Its xor sum is \(11\), which belongs to \(T\).  Hence (3) fails on this
single star, independently of the choice of irreducible polynomial used
to implement multiplication.

For the concrete presentation
\[
 \mathbb F_{32}=\mathbb F_2[\alpha]/(\alpha^5+\alpha^2+1),
\]
the verifier finds only 13 distinct values on the 17 extensions.  For
example, extensions by \(25\) and \(28\) both have colour \(8\), and
extensions by \(13\) and \(15\) both have colour \(14\).

More generally, any proposed 17-value rule whose exceptional value is
available only when the subset sum is zero, and whose nonzero-sum values
lie in a fixed 16-element set, fails by the same argument.

## 3. What remains

The full polynomial \(H_S\) itself loses no information except the
unavoidable complement ambiguity.  Indeed, if
\[
 P+Q=H,\qquad PQ=Z^{32}+Z,
\]
then any other polynomial factor \(R\) with the same sum and product
satisfies
\[
 (R+P)(R+Q)=0
\]
in the integral domain \(\mathbb F_{32}[Z]\), so \(R=P\) or \(R=Q\).
Also adjacent complement-pairs have distinct \(H\): if
\(S=T\cup\{x\}\) and \(S'=T\cup\{y\}\), equality would imply
\[
 P_T=\frac{(Z^{32}+Z)/P_T}{(Z-x)(Z-y)},
\]
which would make the squarefree polynomial \(Z^{32}+Z\) divisible by
\(P_T^2\).

Consequently, arbitrary postprocessing of the *entire* \(H_S\) is just a
re-encoding of the original complement-pair colouring problem.  The
rigorous no-go above concerns the natural 17-value invariant extracted
from its first new coefficient; higher coefficients retain genuinely new
information and are not excluded.

Run:

```bash
python3 evidence/verify_f32_halfset_polynomial.py
```


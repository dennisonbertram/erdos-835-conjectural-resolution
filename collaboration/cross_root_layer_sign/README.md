# Cross-root transformation of the individual layer signs

## Status

**PROVED.**  Let \((S_i)_{i\in A}\) be one fixed golf design
\(G(k+1)\), where \(k\) is even.  For a fixed colour \(x\), the
one-factorization sign
\[
 P(\Psi^{r,x})
\]
obtained after choosing the distinguished root colour \(r\) is independent of
\(r\).  The finite-layer signs at two roots have the exact transformation laws
in (13)--(16) below.  All transition products around root cycles are identically
\(+1\).

**CONSEQUENCE.**  Comparing the individual sign equations at the \(k+1\)
adjacent roots belonging to this *same* golf design gives no new scalar
compatibility condition.  The transformations are a coboundary, so there is
no sign holonomy to obstruct the Wallis \(k=16\) chart.

This conclusion concerns only the layer-sign equations proved in
[`../global_h_parity/README.md`](../global_h_parity/README.md).  It does not
construct compatible \(N\)-tables at different roots, a radius-five ball, or a
global colouring.  In particular, it does not settle Erdős--Rosenfeld problem
835.

## 1. One golf design and all its roots

Let
\[
 |C|=k+1,\qquad |A|=k-1,
\]
where \(C\) and \(A\) have fixed orders.  Suppose
\((S_i)_{i\in A}\) is a family of symmetric idempotent Latin squares on
\(C\) satisfying the golf identity
\[
 \{S_i(u,v):i\in A\}=C\setminus\{u,v\}
 \quad(u\ne v).                                                \tag{1}
\]
A hypothetical global \(O_k\to K_{k+1}\) covering (equivalently, the tight
middle-layer colouring in this repository), restricted to the \(k+1\)
centres through one lower star, supplies exactly such a family.  Thus
changing \(r\) below means
changing the distinguished root *inside the same family*, not comparing
unrelated radius-three charts.

The radius-three chart at root \(r\) is
\[
 L_i^r(u)=S_i(r,u),\qquad
 M_i^r(uv)=S_i(u,v)
 \quad(u,v\in C\setminus\{r\}).                                \tag{2a}
\]
These are precisely the \(L,M\) data to which the proved individual-layer
formulas apply.

For \(x\in C\), define the colour-\(x\) matching of \(S_i\) by
\[
 R_i^x=\{\{u,v\}\subset C\setminus\{x\}:S_i(u,v)=x\}.            \tag{2}
\]
It is a perfect matching of \(C\setminus\{x\}\).  Write
\(b_i^x(t)\) for the mate of \(t\) in \(R_i^x\).

Choose a root \(r\in C\), put \(V_r=C\setminus\{r\}\) with the induced
order, and define a perfect matching on \(V_r\) by
\[
 \Psi_i^{r,x}=
 \begin{cases}
 R_i^x,&x=r,\\[2mm]
 \bigl(R_i^x\setminus
       \{\{r,b_i^x(r)\}\}\bigr)
       \cup\{\{x,b_i^x(r)\}\},&x\ne r.
 \end{cases}                                                   \tag{3}
\]
Equation (1) says that
\(\Psi^{r,x}=(\Psi_i^{r,x})_{i\in A}\) is a one-factorization of
\(K_{V_r}\).

For \(x\ne r\), let \(B=A\cup\{*\}\), with \(*\) last, and set
\[
 \lambda_x^r(i)=b_i^x(r),\qquad \lambda_x^r(*)=x.               \tag{4}
\]
Again by (1), \(\lambda_x^r:B\to V_r\) is a permutation.

Let \(P\) have the definition and order convention of equation (4) in the
global \(H\)-parity note.  Namely, for a one-factorization
\(\mathcal F=(Q_i)_{i\in A}\) on an ordered \(k\)-set \(Y\),
\[
 P(\mathcal F)=
 \prod_{y\in Y}\operatorname{sgn}
   \bigl(i\longmapsto Q_i(y)\bigr).                             \tag{5}
\]

## 2. The one-factorization sign is root-independent

### Relabelling lemma

If \(\tau:Y\to Y'\) is a bijection of ordered sets of the same even size
\(k\), then
\[
 P(\tau\mathcal F)=P(\mathcal F).                              \tag{6}
\]
Indeed, at the row based at \(y\), relabelling multiplies the row sign by the
sign of
\(\tau_y:Y\setminus\{y\}\to Y'\setminus\{\tau(y)\}\).  If \(q,q'\) are
the two positions of \(y,\tau(y)\), the cofactor rule gives
\[
 \operatorname{sgn}(\tau_y)
   =(-1)^{q+q'}\operatorname{sgn}(\tau).
\]
Multiplication over all \(y\) gives
\[
 \operatorname{sgn}(\tau)^k
 (-1)^{2\binom{k}{2}}=+1,
\]
because \(k\) is even.

### Root-invariance theorem

For every fixed \(x\in C\), the value
\[
 \boxed{\quad p_x:=P(\Psi^{r,x})\quad}                          \tag{7}
\]
is independent of the root \(r\).

**Proof.**  Take distinct roots \(r,s\) and let \(\tau=(r\,s)\), restricted
from \(V_r\) to \(V_s\).

If \(x=r\), then
\[
 \tau R_i^r=\Psi_i^{s,r}
\]
for every \(i\): relabelling the unique endpoint \(s\) as \(r\) is exactly
the replacement in (3).  The case \(x=s\) is the reverse statement.  Hence
(6) proves (7) in these two cases.

Now suppose \(x\notin\{r,s\}\).  There is a unique \(h\in A\) with
\[
 S_h(r,s)=x.                                                   \tag{8}
\]
For \(i\ne h\), put
\[
 a_i=b_i^x(r),\qquad d_i=b_i^x(s).
\]
The transported matching and the new matching differ only by
\[
\begin{array}{c|c}
 \tau\Psi_i^{r,x}&\Psi_i^{s,x}\\ \hline
 \{x,a_i\},\{r,d_i\}&\{x,d_i\},\{r,a_i\}.
\end{array}                                                    \tag{9}
\]
For \(i=h\), they are equal.

Let \(D=C\setminus\{r,s,x\}\).  At a row \(y\in D\), exactly two factor
indices in (9) affect \(y\), and the two images \(x,r\) are transposed.
Thus each such row changes sign.  There are \(|D|=k-2\) such rows, an even
number.  At the \(x\)-row, the lists
\((a_i)_{i\ne h}\) and \((d_i)_{i\ne h}\) are two permutations of \(D\).
At the \(r\)-row the same two lists occur in the opposite order.  The two
rows have a fixed \(h\)-entry; after deleting it, one ratio is the sign of
the permutation carrying the \(a\)-list to the \(d\)-list and the other is
the sign of its inverse.  They are therefore equal and their product is
\(+1\).  Hence
\[
 P(\tau\Psi^{r,x})=P(\Psi^{s,x}).
\]
Apply (6) once more to obtain (7). \(\square\)

## 3. Exact \(\lambda\)- and \(H\)-transformation laws

Fix distinct \(r,s,x\).  Let
\[
 \varepsilon_{rs}
   =\operatorname{sgn}\bigl(\tau:V_r\to V_s\bigr),\qquad
 \theta_x^{r,s}
   =(\lambda_x^s)^{-1}\tau\lambda_x^r\in\operatorname{Sym}(B). \tag{10}
\]
The permutation \(\theta_x^{r,s}\) fixes both \(*\) and the unique index
\(h\) in (8).  Taking signs in
\(\tau\lambda_x^r=\lambda_x^s\theta_x^{r,s}\) gives the exact
\(\lambda\)-law
\[
 \boxed{\quad
 \operatorname{sgn}(\lambda_x^s)
  =\varepsilon_{rs}\,
    \operatorname{sgn}(\theta_x^{r,s})\,
    \operatorname{sgn}(\lambda_x^r).
 \quad}                                                       \tag{11}
\]
In terms of the fixed order on \(C\),
\[
 \varepsilon_{rs}
 =(-1)^{\operatorname{pos}_C(r)+\operatorname{pos}_C(s)+1}.
\]
Formula (10), rather than this positional abbreviation, is independent of
the names of the colours.

Let \(q_r(x)\) be the zero-based position of \(x\) in \(V_r\), and put
\[
 m=\frac{k-2}{2}.
\]
The proved finite-layer and root-layer formulas from the global
\(H\)-parity note are
\[
 H_x^r=
 \begin{cases}
 p_x,&x=r,\\[1mm]
 (-1)^{q_r(x)+1+m}
   \operatorname{sgn}(\lambda_x^r)p_x,&x\ne r.
 \end{cases}                                                   \tag{12}
\]
Here \(H_x^r\) means an observed layer sign when a compatible shared
\(N\)-table at root \(r\) exists.  Without such a table, the right side is
only the **conditional target** \(H_{\mathrm{required},x}^r\).

Combining (7), (11), and (12) gives, for \(x\notin\{r,s\}\),
\[
 \boxed{\quad
 H_x^sH_x^r
 =(-1)^{q_s(x)+q_r(x)}
   \varepsilon_{rs}\operatorname{sgn}(\theta_x^{r,s}).
 \quad}                                                       \tag{13}
\]
Products of two signs here are also their ratios.
The cases in which the layer colour becomes the root are just as explicit:
\[
 H_r^sH_r^r
   =(-1)^{q_s(r)+1+m}\operatorname{sgn}(\lambda_r^s),           \tag{14}
\]
and the analogous equation with \(r,s\) interchanged.
There is no omitted \(\lambda_x^x\): the root layer has no finite-layer
permutation \(\lambda\), which is why (14) compares it directly with \(p_x\).

There is a compact form which includes all cases.  Define
\[
 \kappa_x(r)=
 \begin{cases}
 1,&r=x,\\
 (-1)^{q_r(x)+1+m}\operatorname{sgn}(\lambda_x^r),&r\ne x.
 \end{cases}                                                   \tag{15}
\]
Then
\[
 \boxed{\quad H_x^r=\kappa_x(r)p_x,\qquad
 H_x^sH_x^r=\kappa_x(s)\kappa_x(r).\quad}                      \tag{16}
\]

## 4. Why adjacent-root comparison gives no new sign obstruction

For any closed sequence of roots
\[
 r_0,r_1,\ldots,r_t=r_0,
\]
equation (16) gives
\[
 \prod_{j=0}^{t-1}
   \bigl(H_x^{r_{j+1}}H_x^{r_j}\bigr)
 =\prod_{j=0}^{t-1}
   \kappa_x(r_{j+1})\kappa_x(r_j)
 =+1.                                                         \tag{17}
\]
Every \(\kappa_x(r)\) occurs twice.  Thus the transition is an exact
coboundary.  Triangle comparisons, longer cycles, and the complete graph of
the \(k+1\) roots produce no additional scalar equation.

This is stronger than merely observing that some small examples pass: it is
an algebraic theorem for every golf design of odd order \(k+1\).  It also
explains why comparing the signs of unrelated radius-three charts would be
invalid.  The common quantities \(p_x\), and hence the transition law, exist
only after all roots are derived from the same family \((S_i)\).

## 5. Exact Wallis \(k=16\) audit

The standard-library verifier constructs the published Wallis \(G(17)\)
starter and checks the following exact fingerprints of the theorem:

* all \(289=17\cdot17\) root/colour one-factorizations;
* all \(4{,}080=17\cdot16\cdot15\) ordered third-colour factor switches;
* all \(4{,}080\) instances of (11) and (13);
* all \(544=2\cdot17\cdot16\) root-crossing instances of (14);
* all \(83{,}521=17^4\) colour/root-triangle products in (17).

The last item is an implementation check of the coboundary formula, not
independent evidence for it; the proof is equation (17).

The exact Wallis fingerprints are
\[
 p_x=+1\quad\hbox{for every }x,
\]
and among the \(272\) finite pairs \((r,x)\), the signs
\(\operatorname{sgn}(\lambda_x^r)\) split \(136\) positive and \(136\)
negative.

For every root, the seventeen conditional layer targets in (12) contain
eight negative and nine positive signs; the root layer is positive.  For the
repository's usual root \(r=16\), in colour order \(0,\ldots,16\), they are
\[
 (+,-,-,-,-,-,+,+,-,-,-,+,+,+,+,+,+).                        \tag{18}
\]
Their product is \(+1\), agreeing with the already-proved global formula.
The individual conditional targets are therefore nonconstant but satisfy
the formal cross-root law (16) exactly.

Run:

```sh
python3 -B collaboration/cross_root_layer_sign/verify_cross_root_layer_sign.py
```

## 6. The remaining gap

Equations (7)--(17) retain only one bit from every large family of local
permutations.  They do **not** identify the entries of the root-\(r\)
\(N\)-table with those of the root-\(s\) table, nor do they prove that either
table exists.  A genuine global colouring would supply all those tables and
would therefore obey the sign laws above, but the converse is false: passing
every scalar transition says nothing about the unsolved cellwise matching,
shared-trace, and prescribed-link compatibility.

In particular, a future theorem derived from the *overlap of the actual
tables* could impose an additional scalar relation on their \(H\)-values.
No such overlap theorem is proved or disproved here.  What is ruled out is
obtaining a new condition merely by writing the already-proved individual
layer formulas at every root and multiplying them around root cycles.

Accordingly:

* the existing individual layer-sign formulas have been exhausted under
  formal root change;
* a new obstruction must retain finer correlations than their products, or
  use other global walks/subset geometry;
* no unrestricted \(k=16\) contradiction or construction follows.

Erdős--Rosenfeld problem 835 remains open.

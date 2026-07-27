# General even-\(k\) degree-one rigidity

## Status

Assume that \(k\ge4\) is even and that a tight colouring exists:

\[
O_k=KG(2k-1,k-1)\longrightarrow K_{k+1}.
\]

Fix one colour fibre \({\cal C}\).  It is a Steiner system

\[
{\cal C}=S(k-2,k-1,2k-1).
\]

This note proves a complete degree-one spectral theorem valid for every such
\(k\).  It also gives closed formulas for the action of every fibre
intersection relation and an exact arithmetic classification of when those
formulas are integral.

These are necessary conditions.  They give no new obstruction when
\(k+1\) is prime and therefore do **not** resolve Erdős--Rosenfeld problem
#835.

Put

\[
v=2k-1,\qquad r=k-1,\qquad
n=|{\cal C}|=\frac1{k+1}\binom vr.
\]

Let \({\cal A}\) be the adjacency matrix of \(O_k\), let
\(\iota:\mathbb R^{\cal C}\to\mathbb R^{\binom{[v]}r}\) extend a fibre
vector by zero, and let \(E_j\) be the global Johnson idempotent with

\[
{\cal A}E_j=\theta_jE_j,\qquad
\theta_j=(-1)^j(k-j),\qquad 0\le j\le k-1.
\]

Finally, let \({\cal H}_1\) be the fibre point module: the span of the
restrictions of \(f_p-f_q\), where \(f_p(B)=[p\in B]\).  It has dimension
\(2k-2\).

## 1. The support and weight theorem

> **Theorem 1.**  For every \(x\in{\cal H}_1\),
> \[
> E_j\iota x=0
> \quad\text{unless}\quad
> j\in\{1,k-2,k-1\}.
> \]
> Moreover, as full right-action identities,
> \[
> \boxed{
> \begin{aligned}
> \iota^*E_1\iota P_1&=\frac1{k+1}P_1,\\
> \iota^*E_{k-2}\iota P_1
>   &=\frac{2k-1}{3(k+1)}P_1,\\
> \iota^*E_{k-1}\iota P_1&=\frac13P_1,
> \end{aligned}}
> \tag{1}
> \]
> where \(P_1\) is the orthogonal projector onto \({\cal H}_1\).

### First proof of the support: design cross quadrature

Take a global degree-one harmonic \(g\) and a global degree-\(j\) harmonic
\(h\).  Their product has incidence degree at most \(j+1\).  Whenever
\(j+1\le k-2\), the \((k-2)\)-design equations give

\[
\sum_{B\in{\cal C}}g(B)h(B)
=\frac1{k+1}\sum_{B\in\binom{[v]}r}g(B)h(B).
\]

The right side is zero for \(j\ne1\), by orthogonality of distinct Johnson
modules.  Hence \(E_j\iota{\cal H}_1=0\) for
\(0\le j\le k-3,\ j\ne1\).  Degree-one vectors have sum zero, so the
principal component \(E_0\) also vanishes.  Only
\(E_1,E_{k-2},E_{k-1}\) remain.

The same quadrature with two degree-one harmonics says that restriction to
the fibre is a \(1/\sqrt{k+1}\)-scaled isometry.  Therefore

\[
\iota^*E_1\iota P_1=\frac1{k+1}P_1.
\tag{2}
\]

### Independent degree-two certificate

There is a shorter proof which uses only (2) and the first two restricted
walk identities.  Since a fibre is independent in \(O_k\),

\[
\iota^*{\cal A}\iota=0.
\tag{3}
\]

Two distinct fibre blocks meet in at most \(k-3\) points, so they have no
common Odd-graph neighbour.  A vertex has \(k\) neighbours.  Thus

\[
\iota^*{\cal A}^2\iota=kI.
\tag{4}
\]

Set

\[
q(t)=(t-2)(t+1).
\]

Apart from the principal eigenvalue, the Odd eigenvalues lie in
\((-\infty,-1]\cup[2,\infty)\), so \(q(\theta_j)\ge0\).  For a unit
\(x\in{\cal H}_1\), (3)--(4) give

\[
\langle\iota x,q({\cal A})\iota x\rangle=k-2.
\]

The fixed \(E_1\)-mass from (2) already contributes

\[
\frac1{k+1}q(-(k-1))
=\frac{(k+1)(k-2)}{k+1}
=k-2.
\]

Positivity forces every other component with \(q(\theta_j)>0\) to vanish.
The only remaining roots are

\[
\theta_{k-2}=2,\qquad \theta_{k-1}=-1.
\]

This independently proves the same three-point support.

### The other two weights and the full right actions

On the three support points, use the Lagrange polynomials

\[
\begin{aligned}
\ell_1(t)
 &=\frac{(t-2)(t+1)}{(k+1)(k-2)},\\
\ell_{k-2}(t)
 &=\frac{(t+k-1)(t+1)}{3(k+1)},\\
\ell_{k-1}(t)
 &=\frac{(t+k-1)(t-2)}{-3(k-2)}.
\end{aligned}
\]

Because the support theorem gives
\(E_j\iota P_1=\ell_j({\cal A})\iota P_1\), equations (3)--(4) yield the
full identities

\[
\iota^*E_j\iota P_1
=\iota^*\ell_j({\cal A})\iota P_1
=w_jP_1,
\]

with

\[
\boxed{
w_1=\frac1{k+1},\qquad
w_{k-2}=\frac{2k-1}{3(k+1)},\qquad
w_{k-1}=\frac13.}
\tag{5}
\]

This proves (1), including the absence of leakage.  The moment checks are

\[
\sum_jw_j=1,\qquad
\sum_jw_j\theta_j=0,\qquad
\sum_jw_j\theta_j^2=k.
\]

## 2. Every fibre intersection relation is scalar

Let \(D_d\) be the Johnson distance-\(d\) matrix on all \(r\)-subsets, and
let \(A_s\) be the matrix on \({\cal C}\) joining blocks with intersection
\(s\).  With

\[
d=r-s=k-1-s,
\]

one has \(A_s=\iota^*D_d\iota\).  Write \(P_d(j)\) for the eigenvalue of
\(D_d\) on \(E_j\).  Since

\[
D_d=\sum_{j=0}^{k-1}P_d(j)E_j,
\]

the full identities (1) give

\[
\boxed{
A_sP_1=\rho_sP_1,\qquad
\rho_s=
\frac{P_d(1)}{k+1}
+\frac{2k-1}{3(k+1)}P_d(k-2)
+\frac13P_d(k-1).}
\tag{6}
\]

Thus every fibre intersection relation preserves \({\cal H}_1\) and acts
there by a scalar.

For these three modules the Eberlein eigenvalues reduce to

\[
\begin{aligned}
P_d(1)
 &=\binom{k-2}{d}\binom{k}{d}
   -\binom{k-1}{d}\binom{k-1}{d-1},\\
P_d(k-2)
 &=(-1)^d\left[
   \binom{k-1}{d}-3\binom{k-2}{d-1}\right],\\
P_d(k-1)&=(-1)^d\binom{k-1}{d}.
\end{aligned}
\tag{7}
\]

Substitution and simplification give the closed formula

\[
\boxed{
\rho_s=
\frac{
\binom{k-1}{d}
\bigl(k(k-1)-(2k-1)d\bigr)
\bigl(\binom{k}{d}+(-1)^dk\bigr)
}{
k(k-1)(k+1)
},
\qquad d=k-1-s.}
\tag{8}
\]

The numerator in (8) is a product; the three displayed factors are
\(\binom{k-1}{d}\),
\(k(k-1)-(2k-1)d\), and
\(\binom{k}{d}+(-1)^dk\).

An expression which makes the possible denominator transparent is

\[
\boxed{\rho_s=\frac{N_d}{k+1},}
\tag{9}
\]

where the integer

\[
\begin{aligned}
N_d={}&
\binom{k-2}{d}\binom{k}{d}
-\binom{k-1}{d}\binom{k-1}{d-1}\\
&+(-1)^d\left[
k\binom{k-1}{d}
-(2k-1)\binom{k-2}{d-1}\right].
\end{aligned}
\tag{10}
\]

In particular, every denominator of a formal scalar divides \(k+1\).
The familiar point-module eigenvalue is recovered at \(s=1\):

\[
\rho_1=\frac{-k^2+4k-2}{2}.
\tag{11}
\]

For \(k=16\), (8) gives, among the useful controls,

\[
\rho_1=-97,\qquad
\rho_2=-2282,\qquad
\rho_{12}=8918,\qquad
\rho_{13}=623.
\]

## 3. Relation to the forced intersection profile

For a fixed \(B\in{\cal C}\), let \(n_s\) be the number of fibre blocks
\(C\) with \(|B\cap C|=s\), including \(n_{k-1}=1\).  The design equations

\[
\sum_s\binom{s}{i}n_s
=\binom{k-1}{i}\lambda_i
\qquad(0\le i\le k-2)
\]

together with \(n_{k-1}=1\), followed by binomial inversion, give

\[
\boxed{
n_s=
\frac{\binom{k-1}{s}
\left(\binom{k}{s+1}+(-1)^{s+1}k\right)}
{k+1}.}
\tag{12}
\]

The scalar has the transparent counting form

\[
\boxed{
\rho_s=n_s\,
\frac{(2k-1)s-(k-1)^2}{k(k-1)}.}
\tag{13}
\]

Indeed, for a point \(p\in B\), the average number of relation-\(s\)
blocks containing \(p\) is \(sn_s/(k-1)\); for \(p\notin B\), it is
\((k-1-s)n_s/k\).  Their difference is (13).  The spectral theorem above
upgrades these averages to the exact point-module action.

Formula (13) is also an independent check on (8).

## 4. Exact integrality criterion for the scalar formulas

It is tempting, from a finite scan, to claim that all \(\rho_s\) are
integral exactly when \(k+1\) is prime.  That conclusion is not justified.
The exact arithmetic statement is slightly subtler.

Put \(m=k+1\), an odd integer.  Then all the scalars in (8) are integral if
and only if:

1. \(m\) is squarefree; and
2. for every prime \(p\mid m\), every base-\(p\) digit of
   \[
   \frac mp-1
   \]
   is either \(0\) or \(p-1\).

This includes every prime \(m\).  A composite satisfying the condition
would necessarily be an odd Giuga number, because its units digit forces

\[
\frac mp\equiv1\pmod p
\qquad\text{for every }p\mid m.
\tag{14}
\]

The digit condition imposes every higher base-\(p\) digit in addition to
(14).  The verifier finds no composite survivor through \(m=1001\), but
that finite fact is not used as a proof that none exists.

### Proof of the criterion

Because \(\gcd(k(k-1),m)=1\), (8) and (9) show that integrality at distance
\(d\) is equivalent, prime-power by prime-power, to

\[
m\mid
\binom{m-2}{d}(3d+2)
\left(\binom{m-1}{d}-(-1)^d\right).
\tag{15}
\]

Suppose first that \(p^a\Vert m\) with \(a\ge2\), and take \(d=p\).
Modulo \(p\),

\[
\binom{m-2}{p}\equiv-1,\qquad 3p+2\equiv2.
\]

Moreover,

\[
\binom{m-1}{p}
=\left(\frac mp-1\right)
\prod_{i=1}^{p-1}\frac{m-i}{i}
\equiv\frac mp-1\pmod{p^a},
\]

where the displayed product is congruent to \(1\pmod{p^a}\).  Hence

\[
v_p\left(\binom{m-1}{p}+1-m\right)=a-1.
\]

The numerator in (15) has \(p\)-adic valuation \(a-1<a\), so the scalar is
not integral.  Thus \(m\) must be squarefree.

Now fix \(p\mid m\), put \(q=m/p\), and write

\[
d=pa+b,\qquad0\le b<p.
\]

Lucas' theorem gives

\[
\begin{aligned}
\binom{m-1}{d}
&\equiv(-1)^b\binom{q-1}{a}\pmod p,\\
\binom{m-2}{d}
&\equiv(-1)^b(b+1)\binom{q-1}{a}\pmod p.
\end{aligned}
\]

Since \(p\) is odd and \((-1)^d=(-1)^{a+b}\), condition (15) modulo \(p\)
is

\[
\binom{q-1}{a}(b+1)(3b+2)
\left(\binom{q-1}{a}-(-1)^a\right)\equiv0\pmod p.
\tag{16}
\]

Taking \(b=0\) proves that (16) for every \(d\) is equivalent to

\[
\binom{q-1}{a}\in\{0,(-1)^a\}\pmod p
\qquad(0\le a\le q-1).
\tag{17}
\]

For the converse, (17) makes the first or the last factor in (16) zero,
for every \(a,b\).

Finally, write the base-\(p\) expansion \(q-1=\sum_i c_ip^i\).  Taking
\(a=p^i\) in (17) and applying Lucas again gives

\[
c_i\in\{0,p-1\}.
\]

Conversely, if all digits are \(0\) or \(p-1\), Lucas' theorem says that
each \(\binom{q-1}{a}\) is either zero or
\[
\prod_i(-1)^{a_i}=(-1)^a.
\]

This proves the criterion.

## 5. What this does and does not add to Ma--Tang

The scalar theorem is a conceptual spectral rigidity result, but its
integrality does not eliminate any prime case.  If \(m=k+1=p\) is prime,

\[
\binom{k}{d}=\binom{p-1}{d}\equiv(-1)^d\pmod p,
\]

so (8) is integral for every \(d\).

The fibre design itself gives the full Ma--Tang composite obstruction more
directly.  Its \(i\)-th design index is

\[
\lambda_i
=\frac{\binom{2k-1-i}{k-2-i}}
       {\binom{k-1-i}{k-2-i}}.
\]

Writing \(a=k-2-i\), this becomes

\[
\lambda_i=\frac1{a+1}\binom{m+a}{a}.
\tag{18}
\]

If \(m\) is composite and \(p\) is its least prime divisor, take
\(a=p-1\).  Lucas' theorem gives

\[
\binom{m+p-1}{p-1}\equiv1\pmod p,
\]

so (18) is not an integer.  Conversely, if \(m=p\) is prime and
\(t=a+1<p\), then

\[
\frac1t\binom{p+t-1}{t-1}
=\frac1p\binom{p+t-1}{t},
\]

and the binomial coefficient on the right is divisible by \(p\).

Thus the ordinary fibre-design divisibilities hold exactly when \(k+1\)
is prime.  This recovers the Ma--Tang prime sieve.  The new \(H_1\)
calculation should be understood as:

* a full global-support theorem;
* a simultaneous scalar-action theorem for every fibre relation; and
* a spectral recoding of part of the already-known composite arithmetic,
  with no obstruction at the surviving prime parameters.

## 6. Verification

Run

```bash
python3 -B collaboration/general_h1_rigidity/verify_general_h1_rigidity.py
ruff check collaboration/general_h1_rigidity/verify_general_h1_rigidity.py
```

The verifier uses exact integer and `Fraction` arithmetic.  It audits:

* the three weights and their first moments;
* the general Eberlein specialisations and both closed scalar formulas;
* the complete forced intersection profile and every design moment;
* the exact digit criterion against direct scalar arithmetic through
  \(k=1000\); and
* the known controls \(k=6\) and \(k=16\).

The finite ranges are regression controls only.  The general arguments are
the proofs above.

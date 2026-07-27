# General pair-module rigidity for a hypothetical \(O_k\to K_{k+1}\) cover

## 0. Status and scope

Let \(k\ge 6\) be even and assume that there is a covering map

\[
O_k=KG(2k-1,k-1)\longrightarrow K_{k+1}.
\]

Fix one fibre \({\cal C}\).  The results below are conditional consequences
of this assumption.  They neither construct such a cover nor exclude one
when \(k+1\) is prime.  In particular, they do **not** settle
Erdős--Rosenfeld problem #835.

The main result is an all-parameter version of the \(k=16\) pair-module
theorem:

\[
\boxed{\;
\iota{\cal H}_2\subseteq
E_2\oplus E_{k-3}\oplus E_{k-2}\oplus E_{k-1},
\;}
\tag{0.1}
\]

with a fixed four-point spectral measure.  Moreover, every fibre
intersection matrix acts as an explicit integer scalar on \({\cal H}_2\).
The proof of (0.1) is direct design quadrature; the quartic positivity
argument used first at \(k=16\) becomes an independent equality audit.

## 1. Setup and the three local moments

Put

\[
v=2k-1,\qquad r=k-1,\qquad
V=\binom{2k-1}{k-1},\qquad n=|{\cal C}|=\frac{V}{k+1}.
\]

Local bijectivity makes \({\cal C}\) a Steiner system
\(S(k-2,k-1,2k-1)\).  Write \(\mathcal A\) for the adjacency matrix of
\(O_k\), let \(\iota:\mathbb R^{\cal C}\to\mathbb R^\Omega\) extend a
fibre vector by zero, and let \(E_j\) be the global Odd/Johnson idempotent
at

\[
\theta_j=(-1)^j(k-j),\qquad 0\le j\le k-1.
\]

Let \({\cal H}_2\) be the restricted degree-two harmonic space and \(P_2\)
its orthogonal projector.  Its dimension is

\[
d_2=\binom{2k-1}{2}-(2k-1)=(2k-1)(k-2).
\tag{1.1}
\]

The design has strength at least four, so restriction on the global
degree-two harmonic space is a \(1/\sqrt{k+1}\)-scaled isometry:

\[
\iota^*E_2\iota=\frac1{k+1}P_2.
\tag{1.2}
\]

Let \(R=A_1\) join two fibre blocks when their intersection has size one.
Here is the one-factorisation argument explicitly.  Fix \(B\in{\cal C}\)
and put \(Y=[2k-1]\setminus B\), so \(|Y|=k\).  For every edge
\(e\in\binom Y2\), the \((k-2)\)-set \(Y\setminus e\) has a unique
extension in the Steiner system:

\[
D_e=(Y\setminus e)\cup\{\phi_B(e)\}.
\]

The extension point lies in \(B\): if it lay in \(e\), then \(D_e\) would
be disjoint from \(B\).  Fibre independence forbids this, and Section 6
shows more strongly that \(n_0=0\) follows from the Steiner design
equations alone.  If two incident edges \(e,e'\) had
\(\phi_B(e)=\phi_B(e')\), then \(D_e,D_{e'}\) would share \(k-2\) points,
contrary to the Steiner property.  Thus each colour class
\(\phi_B^{-1}(p)\), \(p\in B\), is a matching in \(K_Y\).  The
\(\binom k2\) edges are partitioned among \(k-1\) such matchings, each of
size at most \(k/2\); equality of the total capacities forces every colour
class to be a perfect matching.  These \(D_e\) are exactly the
\(R\)-neighbours of \(B\).

Now fix a pair \(S=\{p,q\}\), write \(f_S(B)=[S\subseteq B]\), and let
\(i=|S\cap B|\).  The number of \(R\)-neighbours of \(B\) containing \(S\)
is

\[
F_0=\binom{k-2}{2},\qquad
F_1=\frac{k-2}{2},\qquad
F_2=0.
\tag{1.3}
\]

Indeed, for \(i=0\), the omitted edge must avoid the two points of \(S\).
For \(i=1\), it must have the colour of the point in \(B\) and avoid the
point in \(Y\); exactly one edge of that perfect matching contains the
latter point.  For \(i=2\), \(D_e\) contains only one point of \(B\), so
the count is zero.  Interpolating these three values in
\(1,f_p+f_q,f_{\{p,q\}}\) gives

\[
Rf_{\{p,q\}}
=F_0{\bf1}+(F_1-F_0)(f_p+f_q)
+\frac{(k-2)(k-5)}2f_{\{p,q\}}.
\tag{1.4}
\]

Consequently the pair-incidence span is \(R\)-invariant, and its quotient
by the point-incidence span has scalar action
\((k-2)(k-5)/2\).  Since \(R\) is symmetric, the orthogonal complement
\({\cal H}_2\) is invariant and has that same scalar action:

\[
RP_2=\mu_2P_2,\qquad
\mu_2=\frac{(k-2)(k-5)}2.
\tag{1.5}
\]

The first three restricted Odd-walk identities are

\[
\boxed{
\iota^*\mathcal A\iota=0,\qquad
\iota^*\mathcal A^2\iota=kI,\qquad
\iota^*\mathcal A^3\iota=2R.}
\tag{1.6}
\]

Thus a unit \(x\in{\cal H}_2\), extended as \(y=\iota x\), has moments

\[
m_0=1,\qquad m_1=0,\qquad m_2=k,\qquad
m_3=(k-2)(k-5).
\tag{1.7}
\]

## 2. Cross-degree quadrature forces the four-point support

Take a global degree-two harmonic \(f\) whose restriction represents
\(x\in{\cal H}_2\), and a global degree-\(j\) harmonic \(g\).  If
\(2+j\le k-2\), then \(fg\) has incidence degree at most the design
strength.  Design quadrature gives

\[
\sum_{B\in{\cal C}}f(B)g(B)
=\frac1{k+1}\sum_{B\in\Omega}f(B)g(B).
\tag{2.1}
\]

The right side is zero when \(j\ne2\), by orthogonality of the global
Johnson harmonic spaces.  Hence

\[
E_j\iota x=0
\quad\text{if}\quad
j\ne2\ \text{and}\ j\le k-4.
\tag{2.2}
\]

Only \(j=2,k-3,k-2,k-1\) remain, proving (0.1).  Notice that this argument
also covers the endpoint \(k=6\): it leaves precisely
\(E_2,E_3,E_4,E_5\).

Equivalently,

\[
\boxed{
(\mathcal A-(k-2)I)(\mathcal A+3I)
(\mathcal A-2I)(\mathcal A+I)\,\iota P_2=0.}
\tag{2.3}
\]

No averaged moment, sign polynomial, or finite computation is used in this
support theorem.

## 3. The spectral weights

For a unit \(x\in{\cal H}_2\), write
\(w_j=\|E_j\iota x\|^2\).  Equation (1.2) fixes
\(w_2=1/(k+1)\).  The remaining three weights are uniquely determined by
\(m_0,m_1,m_2\), because their spectral points are \(-3,2,-1\).  Solving
the three linear equations gives

\[
\boxed{
\begin{array}{c|c|c}
j&\theta_j&w_j\\ \hline
2&k-2&\displaystyle\frac1{k+1}\\[1mm]
k-3&-3&\displaystyle\frac{2k-3}{5(k+1)}\\[1mm]
k-2&2&\displaystyle\frac4{15}\\[1mm]
k-1&-1&\displaystyle\frac13
\end{array}}
\tag{3.1}
\]

All four weights are positive for \(k\ge6\).  They are independent of
\(x\).  Their third moment is

\[
\frac{(k-2)^3}{k+1}
-\frac{3^3(2k-3)}{5(k+1)}
+\frac4{15}2^3-\frac13
=(k-2)(k-5)=2\mu_2,
\tag{3.2}
\]

independently recovering the one-factorisation eigenvalue (1.5).

For \(k=6\), (3.1) is

\[
\frac17\delta_4+\frac9{35}\delta_{-3}
+\frac4{15}\delta_2+\frac13\delta_{-1};
\]

for \(k=16\), it is

\[
\frac1{17}\delta_{14}+\frac{29}{85}\delta_{-3}
+\frac4{15}\delta_2+\frac13\delta_{-1}.
\]

These agree with the explicit Witt control and the previous \(k=16\)
calculation.

## 4. The quartic equality, for every even \(k\ge6\)

The fourth restricted walk identity is

\[
\iota^*\mathcal A^4\iota
=k(2k-1)I+4A_{k-3}.
\tag{4.1}
\]

The measure (3.1) gives, pointwise on every unit vector in \({\cal H}_2\),

\[
\boxed{m_4=k^3-9k^2+33k-28.}
\tag{4.2}
\]

Here is an independent audit of the average-equality step.  In the full
Johnson scheme, the distance-two valency is

\[
\nu_2=\binom{k-1}{2}\binom{k}{2},
\]

and the distance-two eigenvalue on the degree-two module is

\[
\pi_2(2)
=\binom{k-1}{2}
-(k-1)(k-2)(k-3)
+\binom{k-3}{2}\binom{k}{2}
=\frac{k-1}{4}
 (k^3-11k^2+34k-28).
\tag{4.3}
\]

The fibre relation \(A_{k-3}\) has valency

\[
n_{k-3}=\frac{k(k-1)(k-2)}4.
\tag{4.4}
\]

Using \(P_2=(k+1)\iota^*E_2\iota\) and the Johnson kernel therefore gives

\[
\frac1{d_2}\operatorname{tr}(P_2A_{k-3})
=n_{k-3}\frac{\pi_2(2)}{\nu_2}
=\frac{k^3-11k^2+34k-28}{4}.
\tag{4.5}
\]

Substitution in (4.1) makes the average fourth moment exactly (4.2).

The original quartic certificate also generalises without change:

\[
h(t)=\frac15(5t-6)(t+3)(t-2)(t+1)
=t^4+\frac45t^3-\frac{37}{5}t^2+\frac{36}{5}.
\tag{4.6}
\]

On the even-\(k\) Odd spectrum, \(h\ge0\), with zeros exactly at
\(-3,2,-1\).  Subtracting the fixed \(1/(k+1)\) mass at \(k-2\) gives

\[
m_4\ge
\frac{h(k-2)}{k+1}
-\frac45(k-2)(k-5)+\frac{37}{5}k-\frac{36}{5}
=k^3-9k^2+33k-28.
\tag{4.7}
\]

Equation (4.5) says that equality is attained on average.  The compressed
positive operator

\[
\iota^*\bigl(h(\mathcal A)-h(k-2)E_2\bigr)\iota
\quad\text{on }{\cal H}_2
\]

has trace zero, hence is zero.  Thus the quartic route independently
recovers (0.1).  The direct quadrature proof in Section 2 is shorter and
does not need this averaging calculation.

At \(k=6\), (4.5) gives \(A_3|_{{\cal H}_2}=-I\) and \(m_4=62\).
At \(k=16\), it gives \(A_{13}|_{{\cal H}_2}=449I\) and \(m_4=2292\).

## 5. Every intersection relation acts scalarly

Let

\[
S=\{2,k-3,k-2,k-1\}.
\]

For \(j\in S\), let \(\ell_j\) be the degree-three Lagrange polynomial
which is one at \(\theta_j\) and zero at the other three supported spectral
points.  By (0.1),

\[
E_j\iota P_2=\ell_j(\mathcal A)\iota P_2.
\]

Applying \(\iota^*\) and using (1.6), together with the scalar action
(1.5), shows that the full image lies back in \({\cal H}_2\).  Its
quadratic form is the weight in (3.1), so

\[
\boxed{\iota^*E_j\iota P_2=w_jP_2\qquad(j\in S).}
\tag{5.1}
\]

This is a full right-action identity, not just
\(P_2\iota^*E_j\iota P_2=w_jP_2\).

Let \(A_s\) be the fibre matrix for block intersection \(s\).  For
convenience set \(A_{k-1}=I\); the cover also has
\(A_0=A_{k-2}=0\).  If \(P_i(j)\) denotes the Eberlein eigenvalue of the
Johnson distance-\(i\) relation on the degree-\(j\) module,

\[
P_i(j)=
\sum_{t=0}^{i}(-1)^{i-t}
\binom{k-1-t}{i-t}\binom{k-1-j}{t}\binom{k+t-j}{t},
\tag{5.2}
\]

then (5.1) gives, for every \(0\le s\le k-1\),

\[
\boxed{
A_sP_2=a_sP_2,\qquad
a_s=\sum_{j\in S}w_jP_{k-1-s}(j).}
\tag{5.3}
\]

Thus the pair module is invariant under every fibre intersection matrix.

## 6. Closed formula for every scalar

The complete fibre intersection distribution also has a simple
all-parameter form.  Including the fixed block itself at \(s=k-1\), put
\(n_s=|\{C\in{\cal C}:|B\cap C|=s\}|\).  Design quadrature through degree
\(k-2\), followed by binomial inversion, gives

\[
\boxed{
n_s=\frac{\binom{k-1}{s}}{k+1}
\left(\binom{k}{s+1}+(-1)^{s+1}k\right),
\qquad 0\le s\le k-1.}
\tag{6.1}
\]

This uses only the design equations and \(n_{k-1}=1\), not an additional
cover restriction.  To see it explicitly, let

\[
v_s^J=\binom{k-1}{s}\binom{k}{s+1}
\]

be the full Johnson intersection distribution.  For
\(0\le i\le k-2\), the \(i\)-design equation for a fixed block \(B\) is

\[
\sum_{s=i}^{k-1}\binom{s}{i}n_s
=\binom{k-1}{i}\lambda_i
=\frac1{k+1}\sum_{s=i}^{k-1}\binom{s}{i}v_s^J.
\tag{6.2}
\]

Here

\[
\lambda_i
=\frac{\binom{2k-1-i}{k-2-i}}{\binom{k-1-i}{k-2-i}}
=\frac1{k+1}\binom{2k-1-i}{k-1-i},
\]

which proves the second equality in (6.2).

Thus
\(d_s=n_s-v_s^J/(k+1)\) has zero binomial moments in all degrees
\(0,\ldots,k-2\).  The nullspace of this \(k-1\) by \(k\) binomial-transform
system is one-dimensional, spanned by

\[
(-1)^{k-1-s}\binom{k-1}{s}.
\]

Since \(n_{k-1}=1\) and \(v_{k-1}^J=1\), its coefficient is
\(1-1/(k+1)=k/(k+1)\).  Because \(k\) is even,
\((-1)^{k-1-s}=(-1)^{s+1}\), which yields (6.1).

In particular, substituting \(s=0\) gives

\[
\boxed{n_0=\frac{\binom{k}{1}-k}{k+1}=0.}
\tag{6.3}
\]

Therefore every \(S(k-2,k-1,2k-1)\) already has no disjoint pair of
blocks.  This is a consequence of the Steiner equations themselves; a
block-dependent disjointness count is not an unforced parameter.

The normalized degree-two Johnson kernel at intersection \(s\) is

\[
q_k(s)=
\frac{
2(2k-3)s(s-1)-4(k-2)^2s+(k-1)(k-2)^2
}{k(k-1)(k-2)}.
\tag{6.4}
\]

Evaluating the diagonal entry of \(A_sP_2=a_sP_2\), or directly simplifying
(5.3), gives the promised closed formula

\[
\boxed{
a_s=n_sq_k(s).}
\tag{6.5}
\]

Equations (6.1), (6.4), and (6.5) are an explicit answer for every
relation, without a recurrence or an implicit linear system.  They give

\[
a_0=0,\qquad
a_1=\frac{(k-2)(k-5)}2,\qquad
a_{k-2}=0,\qquad a_{k-1}=1,
\tag{6.6}
\]

and

\[
a_{k-3}=\frac{k^3-11k^2+34k-28}{4}.
\tag{6.7}
\]

For the two controls:

\[
\begin{array}{c|rrrrrr}
k=6,\ s&0&1&2&3&4&5\\ \hline
a_s&0&2&-2&-1&0&1
\end{array}
\]

and at \(k=16\),

\[
\begin{array}{c|rrrrrrr}
s&1&2&3&4&5&6&7\\ \hline
a_s&77&1488&13689&52000&75933&-24024&-162591\\
\end{array}
\]

\[
\begin{array}{c|rrrrrr}
s&8&9&10&11&12&13\\ \hline
a_s&-108108&42185&73216&30537&5148&449.
\end{array}
\]

## 7. Exact divisibility conditions, and why primes pass them

Because \(A_s\) is an integer matrix and \(a_s\) is rational, (5.3) forces
\(a_s\in\mathbb Z\).  Equations (6.1), (6.4), and (6.5) express the exact
necessary divisibilities.  Define

\[
B_s=\binom{k}{s+1}+(-1)^{s+1}k
\]

and

\[
F_s=2(2k-3)s(s-1)-4(k-2)^2s+(k-1)(k-2)^2.
\]

Then the two conditions are

\[
\boxed{
k+1\mid \binom{k-1}{s}B_s,}
\tag{7.1}
\]

and, once \(n_s\) is integral,

\[
\boxed{
k(k-1)(k-2)\mid n_sF_s.}
\tag{7.2}
\]

There is no new scalar-integrality obstruction when \(p=k+1\) is prime.
This is a general proof, not a finite scan.

First,
\(\binom{p-1}{s+1}\equiv(-1)^{s+1}\pmod p\), while
\(k\equiv-1\pmod p\).  Hence \(p\mid B_s\).  Put
\(b_s=B_s/p\in\mathbb Z\), so
\(n_s=\binom{k-1}{s}b_s\).

Next, direct expansion gives

\[
\begin{aligned}
F_s&\equiv-2s(s+1)&&\pmod{k-1},\\
F_s&\equiv 2s(s-1)&&\pmod{2(k-2)},\\
F_s&\equiv-2(s+1)(3s+2)&&\pmod{2k}.
\end{aligned}
\tag{7.3}
\]

The first congruence and
\[
s\binom{k-1}{s}=(k-1)\binom{k-2}{s-1}
\]
show \(k-1\mid n_sF_s\).  The second and
\[
s(s-1)\binom{k-1}{s}
=(k-1)(k-2)\binom{k-3}{s-2}
\]
show \(2(k-2)\mid n_sF_s\).
Here out-of-range lower binomial indices are read as zero, so the endpoint
cases are included.

Finally, reducing \(pb_s=B_s\) modulo \(k\) gives
\[
b_s\equiv\binom{k}{s+1}\pmod k.
\]
Therefore
\[
n_s(s+1)
\equiv \binom{k-1}{s}\binom{k}{s+1}(s+1)
=k\binom{k-1}{s}^2
\equiv0\pmod k,
\]
and the third congruence in (7.3) gives \(2k\mid n_sF_s\).
Since

\[
\operatorname{lcm}(2k,2(k-2))=k(k-2)
\]

for even \(k\), and \(k-1\) is coprime to \(k(k-2)\), (7.2) follows.
Thus every \(a_s\) is an integer for every prime \(k+1\).

The Perron inequalities also add no obstruction:
\(q_k(s)\) is the degree-two projector kernel divided by its diagonal, so
positive-semidefinite Cauchy--Schwarz gives
\(|q_k(s)|\le1\), and hence \(|a_s|\le n_s\).

## 8. What was and was not ruled out

The exact verifier checks:

* the support weights and moments for every even \(6\le k\le200\);
* agreement of the spectral formula (5.3) and closed formula (6.5);
* the \(k=6\) and \(k=16\) controls;
* all congruences in the general prime-integrality proof; and
* every prime \(7\le k+1\le2003\), relation by relation, for integrality,
  Perron bounds, scalar sums, and residual trace-square nonnegativity.

No prime case in that finite scan fails.  More importantly, Sections 2 and
7 prove for **all** even \(k\ge6\) that the support theorem holds
conditionally, and for **all** prime \(k+1\) that the new scalar
divisibilities are automatic.  The finite scan is only a regression and a
search for elementary arithmetic mistakes; it is not evidence that a cover
exists.

This closes the ordinary pair-module scalar route uniformly.  Any
obstruction at an admissible prime \(k+1\) must use information beyond the
single-module Johnson kernels and ordinary intersection matrices—for
example, state-refined entries, mixed higher-harmonic products, or global
compatibility between fibres.

## 9. Verification

Run:

```sh
python3 -B collaboration/general_h2_rigidity/verify_general_h2_rigidity.py
```

The verifier uses only the Python standard library and exact integer or
`Fraction` arithmetic.

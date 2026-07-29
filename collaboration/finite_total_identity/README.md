# Independent audit of the finite-layer and total sign identities

Date: 2026-07-26.

## Result and scope

The canonical finite-colour augmentation in
`collaboration/full_layer_augmentation/README.md` is mathematically sound:
its dual completion, no-hole theorem, cofactor formula, and layer equation
are correct under the stated induced-order conventions.

Carrying its cofactors to a closed form gives, for every finite colour
\(x\in V=\{0,\ldots ,k-1\}\),

\[
 \boxed{\displaystyle
 H_x=(-1)^{x+1+(k-2)/2}
       \operatorname{sgn}(\lambda_x)\,P(\Psi^x).}
\tag{1}
\]

Together with the infinity layer,

\[
 H_\infty=P(\Psi^\infty),
\tag{2}
\]

this gives the independent two-sided evaluation

\[
 \boxed{\displaystyle
 H=(-1)^{\binom{k}{2}}\Sigma(T)
       \prod_{x\in V\cup\{\infty\}}P(\Psi^x).}
\tag{3}
\]

However, the right side of (3) is identically the previously proved flag
formula:

\[
 \boxed{\displaystyle
 (-1)^{\binom{k}{2}}\Sigma(T)\prod_xP(\Psi^x)
 =(-1)^{\binom{k}{2}}\operatorname{AT}(T)
   \prod_{i\in A}\delta(S_i).}
\tag{4}
\]

Thus the **single-root total** product yields no new obstruction and does not
by itself supply a root-coupling invariant.  The separate equations
(1)--(2), or a comparison of them after changing the root, may still contain
information; that cross-root comparison is not analysed here, and no such
contradiction is proved.  In particular, this note neither constructs nor
excludes the required \(k=16\) object, and it does not solve
Erdős--Rosenfeld problem #835.

### Independence statement

This audit re-derived, rather than merely copied, all sign-sensitive steps:
the one-factorization constant (10), the no-hole theorem (11), every
finite-layer deletion and two-hole orientation in (13)--(18), the infinity
cofactor product, the dummy-vertex derivation of (20), and the global
Pfaffian replacement parity (21)--(23).  It reused only the already
established radius-3/radius-5 definitions and axioms for \(L,M,N,T,S_i\),
plus the standard Latin-square parity identity (24).  The accompanying
verifier was written independently of the earlier two verifiers; those
earlier verifiers were then rerun as additional cross-checks.

## 1. Orders and notation

Let \(k=2m\), let

\[
 V=\{0,\ldots ,k-1\},\qquad A=\{0,\ldots ,k-2\},
 \qquad B=A\sqcup\{*\},
\]

and put \(*\) last.  Every subset has its induced order.  If \(Q\) is a
perfect matching on an ordered even set, define

\[
 \operatorname{pf}(Q)
  =\operatorname{sgn}(a_1,b_1,\ldots ,a_m,b_m),
\tag{5}
\]

where each edge is written with its smaller endpoint first and the edges are
ordered by their smaller endpoints.

For an ordered one-factorization \(\mathcal F=(Q_c)_{c\in X}\) of a
complete graph on an ordered even set \(Y\), define

\[
 P(\mathcal F)=\prod_{u\in Y}
  \operatorname{sgn}\bigl(c\mapsto Q_c(u):
  X\longrightarrow Y\setminus\{u\}\bigr).
\tag{6}
\]

For finite \(x\), set

\[
 a_i=a_i(x)=L_i^{-1}(x),\qquad
 \Psi_i^x=M_i^{-1}(x)\cup\{\{x,a_i\}\}.
\tag{7}
\]

For \(x=\infty\), set
\(\Psi_i^\infty=M_i^{-1}(\infty)\).  The chart axioms imply that
\(\Psi^x=(\Psi_i^x)_{i\in A}\) is a one-factorization of \(K_V\) for every
\(x\in V\cup\{\infty\}\).  Finally,

\[
 \lambda_x:B\longrightarrow V,\qquad
 \lambda_x(i)=a_i(x),\quad\lambda_x(*)=x.
\tag{8}
\]

This is the \(x\)-symbol permutation of \(T\), so

\[
 \prod_{x\in V}\operatorname{sgn}(\lambda_x)=\Sigma(T).
\tag{9}
\]

## 2. A rigorous no-hole theorem

We first record the one-factorization sign identity

\[
 P(\mathcal F)
 =c_k\prod_{Q\in\mathcal F}\operatorname{pf}(Q),
 \qquad c_k=(-1)^{\binom m2}.
\tag{10}
\]

Here is a direct order audit.  Consider the incidences \((Q,u)\).  In
factor-major order, replacing the increasing vertex word inside each factor
by its paired endpoint word has sign
\(\prod_Q\operatorname{pf}(Q)\).  In vertex-major order, sorting the factors
at \(u\) by their mates has sign \(P(\mathcal F)\).  The transpose from the
\((k-1)\)-by-\(k\) factor-major rectangle to the vertex-major rectangle has
sign

\[
 (-1)^{\binom{k-1}{2}\binom{k}{2}}=+1.
\]

After identifying \((Q,u)\) with the directed edge \((u,Q(u))\), the paired
endpoint order lists \((p,q),(q,p)\) consecutively for every \(p<q\), while
the mate-sorted order is lexicographic directed-edge order.  Permuting the
two-element edge blocks is even.  The inversion count from the fixed paired
order to directed-edge order is

\[
 2\binom{k-1}{2}+5\binom{k-1}{3}+3\binom{k-1}{4}
 \equiv\binom{k}{4}\equiv\binom m2\pmod2.
\]

This proves (10), including its constant and all order conventions.

Now suppose ordered even sets \(X,Y\), both of size \(k\), carry perfect
matchings \(Q_{rs}\) of \(Y\), one for each \(rs\in E(K_X)\), and that for
every \(uv\in E(K_Y)\), the set
\(\{rs:uv\in Q_{rs}\}\) is a perfect matching of \(X\).  For fixed \(r\),
the matchings \((Q_{rs})_{s\ne r}\) form a one-factorization of \(K_Y\).
Consequently (10) gives

\[
\begin{aligned}
 \prod_{r\in X,u\in Y}
  \operatorname{sgn}\bigl(s\mapsto Q_{rs}(u)\bigr)
 &=c_k^k
   \prod_{r\in X}\prod_{s\ne r}\operatorname{pf}(Q_{rs})\\
 &=+1.
\end{aligned}
\tag{11}
\]

Indeed \(k\) is even, and every Pfaffian sign occurs twice.  This is the
no-hole theorem used in the augmentation.  It replaces the informal
corner-cell cancellation with an exact proof.

## 3. Exact finite-layer cofactor product

Fix finite \(x\).  The augmented matchings are

\[
 \widehat D_x^{ij}=D_x^{ij}\cup\{\{a_i,a_j\}\},\qquad
 \widehat D_x^{i*}=\Psi_i^x.
\tag{12}
\]

The dual completion in the earlier note is exact.  For
\(x\notin\{u,v\}\), it adds
\(\{i_u,i_v\}\) and \(\{i_M,*\}\); for \(x=u\) or \(x=v\), it adds the
single edge joining the remaining old hole to \(*\).  Hence (11) applies.

At the empty old flag \((i,a_i)\), the augmented link is \(\lambda_x\)
with \(i\mapsto a_i\) deleted.  Its sign is

\[
 \gamma_{i,x}=(-1)^{i+a_i}\operatorname{sgn}(\lambda_x).
\]

Because the \(a_i\) run through \(V\setminus\{x\}\),

\[
 \prod_i\gamma_{i,x}
 =(-1)^{\binom{k-1}{2}+\binom{k}{2}-x}
   \operatorname{sgn}(\lambda_x)
 =(-1)^{x+1}\operatorname{sgn}(\lambda_x).
\tag{13}
\]

We next multiply the cofactor signs at the nonempty flags.  Write
\(p_u(t)\) for the position of \(t\) in \(V\setminus\{u\}\), and
\(r_i(j)\) for the position of \(j\) in \(A\setminus\{i\}\).

At \(u=x\), the added map is \(*\mapsto a_i\), so its exact cofactor is

\[
 (-1)^{k-2+p_x(a_i)}.
\]

As \(i\) varies, the \(p_x(a_i)\) run through \(0,\ldots ,k-2\); their
product is therefore

\[
 (-1)^{\binom{k-1}{2}}.
\tag{14}
\]

For a generic \(u\in U_i:=V\setminus\{x,a_i\}\), let \(j_u\) be determined
by \(a_{j_u}=u\), and let \(\mu_i(u)\) be the mate of \(u\) in
\(M_i^{-1}(x)\).  The complement map is

\[
 j_u\mapsto a_i,\qquad *\mapsto\mu_i(u).
\]

The two-row/two-column cofactor lemma gives

\[
 \kappa_{i,u,x}
 =(-1)^{r_i(j_u)+(k-2)+p_u(a_i)+p_u(\mu_i(u))}
   \epsilon(a_i,\mu_i(u)),
\tag{15}
\]

where \(\epsilon(s,t)=+1\) for \(s<t\), and \(-1\) for \(s>t\).
The source-position product over all generic flags is

\[
 (-1)^{(k-1)\binom{k-2}{2}}
 =(-1)^{\binom{k-2}{2}}.
\tag{16}
\]

For fixed \(i\), the remaining target-and-orientation product is

\[
 \prod_{u\in U_i}
 (-1)^{p_u(a_i)+p_u(\mu_i(u))}
 \epsilon(a_i,\mu_i(u))
 =(-1)^{\binom{k}{2}-x-a_i+(k-2)/2}.
\tag{17}
\]

To check (17), use
\(p_u(t)=t-[u<t]\).  Since \(\mu_i\) permutes \(U_i\), the threshold
count \(\#\{u<a_i\}\) from the positions occurs a second time in the
orientation signs and cancels.  The sum of the \(\mu_i(u)\) is
\(\binom{k}{2}-x-a_i\), and exactly one endpoint of each of the
\((k-2)/2\) matching edges obeys \(u<\mu_i(u)\).

Multiplying (17) over \(i\) and using
\(\sum_i a_i=\binom{k}{2}-x\) gives
\((-1)^{(k-2)/2}\).  Also
\(\binom{k-2}{2}\equiv\binom{k-1}{2}\pmod2\), so (14) cancels (16).
Thus

\[
 \prod_{i,u\ne a_i}\kappa_{i,u,x}
 =(-1)^{(k-2)/2}.
\tag{18}
\]

The dummy-index links have product \(P(\Psi^x)\).  Equation (11), together
with (13) and (18), is exactly (1).

## 4. The infinity layer

Augment the infinity layer by putting \(\Psi_i^\infty\) on the edge \(i*\).
At an old link \((i,u)\), the added row maps to the mate \(p_i(u)\) in
\(\Psi_i^\infty\), and its cofactor is

\[
 (-1)^{k-2+p_u(p_i(u))}.
\]

Across the one-factorization \(\Psi^\infty\), every edge \(s<t\) occurs once,
and its two endpoints contribute

\[
 p_s(t)+p_t(s)=(t-1)+s.
\]

The total exponent is

\[
 \sum_{s<t}(s+t-1)
 =(k-2)\binom{k}{2},
\]

which is even.  The dummy-index links have product
\(P(\Psi^\infty)\), so (11) proves (2).

Multiplying (1) over finite \(x\), using (2) and (9), gives (3), because

\[
 \sum_{x=0}^{k-1}\left(x+1+\frac{k-2}{2}\right)
 \equiv\binom{k}{2}\pmod2.
\tag{19}
\]

## 5. Why the total product collapses

Fix \(i\).  In the symmetric idempotent Latin square \(S_i\) on
\(C=V\cup\{\infty\}\), let \(R_i^x\) be the near-perfect matching of
off-diagonal cells of colour \(x\), on \(C\setminus\{x\}\).
Add a last dummy vertex \(d\) and the edge \(\{x,d\}\) to \(R_i^x\).
These \(k+1\) matchings form a one-factorization of \(K_{k+2}\).

Applying (10), and explicitly deleting the dummy incidence, gives

\[
 \delta(S_i)=c_{k+2}\prod_{x\in C}\operatorname{pf}(R_i^x).
\tag{20}
\]

For clarity, the two fixed signs really cancel.  At a vertex \(u\in C\),
the dummy-augmented link has sign
\((-1)^{k-u}\) times the sign of row \(u\) of \(S_i\), so its product is
\((-1)^{\binom{k+1}{2}}\delta(S_i)\).  On the Pfaffian side,
deleting \(\{x,d\}\) contributes \((-1)^x\), whose product over \(x\)
is the same \((-1)^{\binom{k+1}{2}}\).  This proves (20).

For finite \(x\), \(\Psi_i^x\) replaces
\(\{\infty,a_i(x)\}\) in \(R_i^x\) by \(\{x,a_i(x)\}\).  The Pfaffian
edge-deletion rule gives

\[
 \frac{\operatorname{pf}(\Psi_i^x)}
      {\operatorname{pf}(R_i^x)}
 =(-1)^{k-1-x+[a_i(x)>x]}.
\tag{21}
\]

The product of (21) over all \(i,x\) is \(+1\).  Its fixed exponent is
\((k-1)\binom{k}{2}\), while, after substituting
\(x=L_i(u)\), the rainbow-column axiom gives

\[
 \sum_{i,x}[a_i(x)>x]
 =\sum_{i,u}[u>L_i(u)]
 =\sum_{u=0}^{k-1}u
 =\binom{k}{2}.
\tag{22}
\]

The combined exponent is \(k\binom{k}{2}\), hence even.

Apply (10) to every \(\Psi^x\), then use (20)--(22):

\[
\begin{aligned}
 \prod_{x\in C}P(\Psi^x)
 &=c_k^{k+1}\prod_{i,x}\operatorname{pf}(\Psi_i^x)\\
 &=c_kc_{k+2}^{k-1}\prod_i\delta(S_i)\\
 &=(-1)^{\binom{k}{2}}\prod_i\delta(S_i).
\end{aligned}
\tag{23}
\]

The last equality uses
\(c_kc_{k+2}=(-1)^{k/2}=(-1)^{\binom{k}{2}}\).
Finally, the universal Latin-square identity for \(T\) is

\[
 \operatorname{AT}(T)\Sigma(T)=(-1)^{\binom{k}{2}}.
\tag{24}
\]

Equations (3), (23), and (24) prove (4).

## 6. Audit of the earlier verifier and proof text

`collaboration/full_layer_augmentation/verify_full_layer_augmentation.py`
correctly checks its stated finite claims:

* the cofactor identity on 200 deterministic random instances;
* the two dual-hole patterns;
* all six \(k=4\) no-hole tensors;
* all 336 \(k=6\) tensors after fixing the first matching.

Fixing the first \(k=6\) matching is lossless for that sign test: all perfect
matchings are vertex-relabeling equivalent, and the product of all \(k^2\)
link signs is invariant under a vertex relabeling when \(k\) is even.
The enumeration is a finite check, not the proof of (11), and it does not
test the total identity (4).

During this audit, two local expressions in a draft of the global proof
needed correction, although its boxed conclusions were already correct:

1. In its equation (14)-type calculation, the exact sum is
   \[
   \sum_i i+\sum_i a_i
   =\binom{k-1}{2}+\binom{k}{2}-x,
   \]
   not \(2\binom{k-1}{2}-x\).
2. At \(u=x\), the individual cofactor is
   \((-1)^{k-2+p_x(a_i)}\), not in general
   \((-1)^{k-1+a_i}\).

Both expressions were corrected in
`collaboration/global_h_parity/README.md` before commit.  Equations
(13)--(18) above provide the independent check.

Run the independent standard-library audit:

```sh
/opt/homebrew/bin/python3 -B \
  collaboration/finite_total_identity/verify_finite_total_identity.py
```

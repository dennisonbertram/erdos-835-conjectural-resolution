# Global \(H\)-parity from the full shared \(N\)-table

## Status and scope

**PROVED.**  Suppose a compatible shared \(N\)-table exists for a radius-3
chart \((L,M)\), with the orders and sign conventions of
`evidence/odd_graph_local_ball`.  For every color \(x\), complete the partial
matchings in the \(x\)-layer to one-factorizations \(\Psi^x\) as defined below.
Then the observed product of all link signs is

\[
 \boxed{\quad
 H=(-1)^{\binom{k}{2}}\Sigma(T)
       \prod_{x\in V\cup\{\infty\}}P(\Psi^x).
 \quad}                                      \tag{1}
\]

Here \(P(\Psi^x)\) is a product of row-permutation signs of a
one-factorization, and \(\Sigma(T)\) is the symbol sign of the Latin square
obtained from \(L\).  Formula (1) is obtained from the two matching
descriptions of the same \(N\)-table: the matchings indexed by \(ij\) and
those indexed by \(uv\).

**PROVED.**  The apparently new right side of (1) simplifies, for every valid
radius-3 chart and without assuming that \(N\) exists, to the previous flag
formula:

\[
 (-1)^{\binom{k}{2}}\Sigma(T)\prod_xP(\Psi^x)
   =F(L,M).                                  \tag{2}
\]

Thus the full global product supplies an independent proof of the value of
\(H\), but it does **not** produce a new chart obstruction beyond
\(H=F(L,M)\).  The separate layer formulas below contain finer information
which is lost after multiplication over all colors.

This note proves only a structural sign theorem.  It does not assert the
existence or nonexistence of a compatible \(k=16\) shared \(N\)-table, and it
does not settle Erdős--Rosenfeld problem 835.

## 1. Notation

Let

\[
 V=\{0,\ldots ,k-1\},\qquad A=\{0,\ldots ,k-2\},
 \qquad C=V\cup\{\infty\},
\]

with the displayed orders.  Put \(K=\binom{k}{2}\).  For a perfect matching
\(Q\) on an ordered even set, write

\[
 \operatorname{pf}(Q)
   =\operatorname{sgn}(a_1,b_1,\ldots ,a_m,b_m),                 \tag{3}
\]

where every edge is written with its smaller endpoint first and the edges are
ordered by their smaller endpoints.

If \(\mathcal F=(Q_c)_{c\in X}\) is a one-factorization of the complete graph
on an ordered even set \(Y\), indexed by an ordered set \(X\) of size
\(|Y|-1\), define

\[
 P(\mathcal F)
   =\prod_{y\in Y}\operatorname{sgn}
      \bigl(c\longmapsto Q_c(y)\bigr).                           \tag{4}
\]

The domain is ordered by \(X\), and the codomain is \(Y\setminus\{y\}\) with
the induced order.

For finite \(x\in V\), set

\[
 a_i(x)=L_i^{-1}(x),\qquad
 \Psi_i^x=M_i^{-1}(x)\cup\{\{x,a_i(x)\}\}.                       \tag{5}
\]

For \(x=\infty\), set

\[
 \Psi_i^\infty=M_i^{-1}(\infty).                                \tag{6}
\]

Condition 1 on \(L\), together with the one-factorization condition on each
\(S_i\), says that

\[
 \Psi^x=(\Psi_i^x)_{i\in A}
\]

is a one-factorization of \(K_V\) for every \(x\in C\).

Finally let \(B=A\cup\{*\}\), ordered with \(*\) last, and define

\[
 \lambda_x:B\longrightarrow V,\qquad
 \lambda_x(i)=a_i(x),\quad \lambda_x(*)=x.                       \tag{7}
\]

This is a permutation.  Its sign is the \(x\)-symbol sign of the Latin square

\[
 T(i,u)=L_i(u),\qquad T(*,u)=u.
\]

Consequently

\[
 \prod_{x\in V}\operatorname{sgn}(\lambda_x)=\Sigma(T).          \tag{8}
\]

## 2. Two matching-sign lemmas

### Lemma 2.1: one-factorization sign

If \(\mathcal F\) is a one-factorization of \(K_n\), with \(n=2m\), then

\[
 P(\mathcal F)
   =c_n\prod_{Q\in\mathcal F}\operatorname{pf}(Q),
 \qquad
 c_n=(-1)^{\binom m2}.                                          \tag{9}
\]

**Proof.**  Let

\[
 \Omega=\{(y,Q):y\in Y,\ Q\in\mathcal F\},\qquad
 \vec E(Y)=\{(y,z):y\ne z\},
\]

and use the bijection

\[
 \Phi(y,Q)=(y,Q(y)).                                             \tag{9a}
\]

Order both sets vertex-major.  Then \(\Phi\) is block diagonal, with the
\(y\)-block equal to \(Q\mapsto Q(y)\), so its sign is \(P(\mathcal F)\).

Now order \(\Omega\) factor-major and, provisionally, order \(\vec E(Y)\)
factor-major and then by initial endpoint.  In these orders \(\Phi\) is the
identity.  The vertex-major/factor-major transpose on \(\Omega\) has

\[
 \binom n2\binom{n-1}{2}
\]

inversions.  For \(n=2m\) this is even, because its parity is
\(m(m-1)\).

Within one factor \(Q\), change from initial-endpoint order to consecutive
oriented edge blocks

\[
 (a_1,b_1),(b_1,a_1),\ldots,(a_m,b_m),(b_m,a_m),
\]

with the convention of (3).  The initial-endpoint word is
\((a_1,b_1,\ldots,a_m,b_m)\), so this change has sign
\(\operatorname{pf}(Q)\).  Next put all undirected edge blocks into global
lexicographic order.  Permuting blocks of size two has positive sign, so the
factorization-dependent part is exactly
\(\prod_Q\operatorname{pf}(Q)\).

It remains to change from global undirected-edge order

\[
 (a,b),(b,a)\quad (a<b,\ \text{lexicographically})
\]

to vertex-major directed-edge order.  An inverted pair of directed edges
has either three distinct endpoints (the underlying edges meet) or four
(they are disjoint).  Inspecting their two orientations gives two inversions
for each three-set and three for each four-set.  Hence

\[
 I_n=2\binom n3+3\binom n4
    =\frac{n(n-1)(n-2)(3n-1)}{24}.
\]

For \(n=2m\),

\[
 I_{2m}-\binom m2
   =\frac{m(m-1)(6m^2-4m-1)}3,
\]

which is even: division by the odd number \(3\) does not remove the factor
two in \(m(m-1)\).  Thus the fixed order change is
\((-1)^{I_n}=(-1)^{\binom m2}=c_n\).  Multiplying the three order changes
proves (9). \(\square\)

The identity was also exhaustively checked for every ordered
one-factorization of \(K_4,K_6,K_8\) by the verifier accompanying this note.

### Lemma 2.2: no-hole tensor

Let \(X,Y\) be ordered sets of the same even size \(k\).  Suppose that for
every unordered edge \(xx'\) of \(X\) there is a perfect matching
\(Q_{xx'}\) of \(Y\), and, dually, for every edge \(yy'\) of \(Y\) the set

\[
 \{\,xx': yy'\in Q_{xx'}\,\}
\]

is a perfect matching of \(X\).  At every cell \((x,y)\), the tensor induces
a bijection

\[
 X\setminus\{x\}\longrightarrow Y\setminus\{y\},
 \qquad x'\longmapsto Q_{xx'}(y).
\]

The product of the signs of all \(k^2\) such bijections is \(+1\).

**Proof.**  Fix \(x\).  The \(k-1\) matchings

\[
 \mathcal F_x=(Q_{xx'})_{x'\ne x}
\]

form a one-factorization of \(K_Y\), by the dual matching hypothesis.  The
product of the \(k\) cell signs with first coordinate \(x\) is
\(P(\mathcal F_x)\).  Applying (9) and multiplying over \(x\) gives

\[
 \prod_xP(\mathcal F_x)
   =c_k^k\prod_x\prod_{x'\ne x}\operatorname{pf}(Q_{xx'}).
\]

Since \(k\) is even, \(c_k^k=1\).  Every \(Q_{xx'}\) occurs exactly twice,
once from each endpoint of \(xx'\), so all Pfaffian signs square to \(1\).
The product is therefore \(+1\). \(\square\)

This is the point at which both families of matchings are used.  The
\(ij\)-indexed family supplies the rows \(Q_{xx'}\); the \(uv\)-indexed
family is exactly what makes each \(\mathcal F_x\) a one-factorization.

## 3. The \(\infty\)-layer

Augment the \(\infty\)-layer to a no-hole tensor on \(B\times V\):

* for \(i,j\in A\), use \(D_\infty^{ij}\);
* for \(i\in A\), use \(\Psi_i^\infty\) on the row edge \(i*\);
* if the edge \(uv\) belongs to the factor \(\Psi_h^\infty\), augment its
  original matching on \(A\setminus\{h\}\) by the edge \(\{h,*\}\).

At a cell \((i,u)\), deleting the added \(*\)-entry gives the old partial
link and a cofactor.  If \(p_u\) denotes position in \(V\setminus\{u\}\), the
cofactor exponent is

\[
 (k-2)+p_u\bigl(\Psi_i^\infty(u)\bigr).
\]

For one matching \(\Psi_i^\infty\), the sum of these exponents over \(u\) is,
modulo two,

\[
 \sum_{\{a,b\}\in\Psi_i^\infty}(a+b-1)
   =K-\frac{k}{2}
   =\frac{k(k-2)}2,
\]

which is even.  Hence the product of all old-cell cofactors is \(+1\).
The genuinely new cells \((*,u)\) have product \(P(\Psi^\infty)\), by
definition (4).  Lemma 2.2 therefore reads

\[
 1=H_\infty P(\Psi^\infty),
\]

and gives

\[
 \boxed{\quad H_\infty=P(\Psi^\infty).\quad}                    \tag{10}
\]

The companion note
[`../infinity_layer_theorem/README.md`](../infinity_layer_theorem/README.md)
denotes the same regrouping sign by \(\rho(\Psi^\infty)\).  Under the
shared-layer hypotheses, its corner-cell proof and the no-hole completion
above evaluate the same \(H_\infty\), hence

\[
 \rho(\Psi^\infty)=P(\Psi^\infty)=H_\infty.                     \tag{11}
\]

The exact \(k=16\) XOR and cyclic/Bose examples in that note give respectively
\(+1\) and \(-1\).  Therefore \(H_\infty\) is not a function of \(k\) alone.

## 4. A closed formula for every finite layer

Fix \(x\in V\).  Augment the \(x\)-layer to a no-hole tensor on \(B\times V\)
as follows:

\[
 \widehat D_x^{ij}
   =D_x^{ij}\cup\{\{a_i(x),a_j(x)\}\},                           \tag{12}
\]

\[
 \widehat D_x^{i*}
   =M_i^{-1}(x)\cup\{\{x,a_i(x)\}\}=\Psi_i^x.                    \tag{13}
\]

The dual completion at a column edge \(uv\) is forced:

* if \(u=x\), the unique old hole \(i_v\) is paired with \(*\);
* if \(v=x\), the unique old hole \(i_u\) is paired with \(*\);
* if \(x\notin\{u,v\}\), the old holes are
  \(i_u,i_v,i_M\), where
  \(a_{i_u}(x)=u\), \(a_{i_v}(x)=v\), and
  \(uv\in M_{i_M}^{-1}(x)\); add
  \(\{i_u,i_v\}\) and \(\{i_M,*\}\).

Thus (12)--(13) satisfy both hypotheses of Lemma 2.2.  We now compare the
augmented cell signs with the old signs.

At the empty old flag \((i,a_i(x))\), the augmented map is the permutation
\(\lambda_x\) with the entry \(i\mapsto a_i(x)\) deleted.  Multiplying these
cofactor signs over \(i\) gives

\[
 \prod_{i\in A}
   (-1)^{i+a_i(x)}\operatorname{sgn}(\lambda_x)
   =(-1)^{x+1}\operatorname{sgn}(\lambda_x).                    \tag{14}
\]

Indeed, \(\operatorname{sgn}(\lambda_x)\) occurs \(k-1\) times, and

\[
 \sum_i i+\sum_i a_i(x)
   =\binom{k-1}{2}+K-x
   =(k-1)^2-x\equiv x+1\pmod2.
\]

At \((i,x)\), deletion of the \(*\)-row and \(a_i(x)\)-column contributes
\[
 (-1)^{k-2+p_x(a_i(x))},
\]
where \(p_x\) is position in \(V\setminus\{x\}\).  Because the
\(a_i(x)\) run through that ordered set, their product is
\((-1)^{(k-2)(k-1)/2}\).  At every other flag \((i,u)\), delete the old
missing row \(j_u\) and the added target.  As \(u\) varies, \(j_u\) runs
through \(A\setminus\{i\}\), while the dummy row has position \(k-2\).
For fixed \(i\), the source-position exponent is therefore

\[
 \binom{k-2}{2}+(k-2)^2.
\]

After multiplication over the odd number \(k-1\) of indices, its parity is
\(\binom{k-2}{2}\), which differs from \(\binom{k-1}{2}\) by the even number
\(k-2\).  Thus the product of all omitted-row cofactors is the same

\[
 (-1)^{(k-2)(k-1)/2}
\]

as the product of the \(u=x\) cofactors, so those two products cancel.

It remains to multiply the target-position and edge-orientation corrections.
For fixed \(i\), put \(a=a_i(x)\),
\(U=V\setminus\{x,a\}\), and let \(\mu\) be the mate involution on \(U\) in
\(M_i^{-1}(x)\).  The correction at \(u\in U\) is

\[
 (-1)^{p_u(a)+p_u(\mu(u))}\epsilon(a,\mu(u)),                    \tag{15}
\]

where \(p_u(t)\) is the position of \(t\) in \(V\setminus\{u\}\) and
\(\epsilon(s,t)=+1\) when \(s<t\), \(-1\) otherwise.  Since \(\mu\)
permutes \(U\), the two threshold sums in (15) cancel.  Exactly one endpoint
of each of the \((k-2)/2\) matching edges satisfies \(u<\mu(u)\).  Hence the
product of (15) over \(u\in U\) is

\[
 (-1)^{K-x-a+(k-2)/2}.                                         \tag{16}
\]

Finally the \(a_i(x)\) range over \(V\setminus\{x\}\), so
\(\sum_i a_i(x)=K-x\).  Multiplying (16) over \(i\), and using that \(k-1\)
is odd, leaves just \((-1)^{(k-2)/2}\).

The cells based at the dummy index \(*\) have product \(P(\Psi^x)\).  The
other cells have product \(H_x\) times the correction just calculated.
Lemma 2.2 therefore says

\[
 1=P(\Psi^x)H_x
   (-1)^{x+1+(k-2)/2}\operatorname{sgn}(\lambda_x).
\]

Since every factor is a sign and hence its own inverse, this gives the closed
finite-layer identity

\[
 \boxed{\quad
 H_x=(-1)^{\,x+1+(k-2)/2}
       \operatorname{sgn}(\lambda_x)P(\Psi^x),
 \qquad x\in V.
 \quad}                                                        \tag{17}
\]

Formula (17) is the simplification left open after formula (9) of
[`../full_layer_augmentation/README.md`](../full_layer_augmentation/README.md).
The augmentations are identical; (14)--(16) evaluate all of its cofactor and
orientation terms.

Multiplying (17) over \(x\in V\), adjoining (10), and using (8), the fixed
exponent is

\[
 \sum_{x=0}^{k-1}\left(x+1+\frac{k-2}{2}\right)
 \equiv K\pmod2.
\]

This proves (1).

## 5. Why the global formula is identically the flag formula

For a symmetric idempotent Latin square \(S_i\) on \(C\), let \(R_i^x\) be
the near-perfect matching of color \(x\) on \(C\setminus\{x\}\).  Add a dummy
vertex \(d\), last in the order, and the edge \(\{x,d\}\) to every \(R_i^x\).
These \(k+1\) perfect matchings form a one-factorization of \(K_{k+2}\).
At an old vertex \(y\), moving the deleted symbol \(y\) to the dummy position
changes the augmented row sign from the \(S_i\)-row sign by
\((-1)^{k-\operatorname{pos}_C(y)}\).  Likewise,

\[
 \operatorname{pf}\bigl(R_i^x\cup\{\{x,d\}\}\bigr)
  =(-1)^{k-\operatorname{pos}_C(x)}
     \operatorname{pf}(R_i^x).
\]

Both products of deletion factors are
\((-1)^{\sum_{r=0}^k(k-r)}=(-1)^K\), and hence cancel in (9).  The dummy
vertex itself has the identity row.  Therefore (9) gives

\[
 \delta(S_i)
   =c_{k+2}\prod_{x\in C}\operatorname{pf}(R_i^x).               \tag{18}
\]

For \(x=\infty\), \(R_i^\infty=\Psi_i^\infty\).  For finite \(x\), the
matching \(\Psi_i^x\) replaces the edge
\(\{\infty,a_i(x)\}\) in \(R_i^x\) by \(\{x,a_i(x)\}\).  Direct deletion from
the ordered Pfaffian word gives

\[
 \frac{\operatorname{pf}(\Psi_i^x)}
      {\operatorname{pf}(R_i^x)}
  =(-1)^{\,k-1-x+[a_i(x)>x]}.                                  \tag{19}
\]

The product of (19) over all \(i,x\) is \(+1\).  The fixed part contributes
\((k-1)K\), while

\[
 \sum_{i,x}[a_i(x)>x]=K.
\]

For the last equality substitute \(x=L_i(u)\): for each \(u\), condition 1
says that \(L_i(u)\), as \(i\) varies, runs once through
\(V\setminus\{u\}\).  The total exponent is therefore \(kK\), which is even.

Apply (9) to every \(\Psi^x\), then use (18)--(19):

\[
\begin{aligned}
 \prod_{x\in C}P(\Psi^x)
  &=c_k^{k+1}\prod_{i,x}\operatorname{pf}(\Psi_i^x)\\
  &=c_kc_{k+2}^{\,k-1}\prod_i\delta(S_i)\\
  &=c_kc_{k+2}\prod_i\delta(S_i)\\
  &=(-1)^K\prod_i\delta(S_i).                                  \tag{20}
\end{aligned}
\]

The last step uses

\[
 c_kc_{k+2}=(-1)^{k/2}=(-1)^K.
\]

The universal Latin parity identity for \(T\) is

\[
 \operatorname{AT}(T)\Sigma(T)=(-1)^K.                          \tag{21}
\]

Combining (1), (20), and (21) gives

\[
\begin{aligned}
 H
  &=(-1)^K\Sigma(T)\prod_xP(\Psi^x)\\
  &=\Sigma(T)\prod_i\delta(S_i)\\
  &=(-1)^K\operatorname{AT}(T)\prod_i\delta(S_i)
   =F(L,M).
\end{aligned}
\]

This proves (2).

## 6. Exact computation and falsified weaker candidates

The standard-library verifier
[`verify_global_h_parity.py`](verify_global_h_parity.py) checks:

1. Lemma 2.1 for every ordered one-factorization of \(K_4,K_6,K_8\).
2. The two exact \(k=16\) infinity-layer tensors, including
   \(H_\infty=P(\Psi^\infty)=\rho(\Psi^\infty)\), with signs \(+1\) and
   \(-1\).
3. Formula (2) for all \(11{,}760\) chart/root controls at \(k=6\).
4. Formula (2), including the direct dummy-Pfaffian calculation (18), for all
   17 roots of the Wallis \(k=16\) chart.
5. Two abstract shared matching tables with all required per-\(ij\) and
   per-\(uv\) matching cardinalities but opposite values of \(H\).

Run:

```sh
python3 -B collaboration/global_h_parity/verify_global_h_parity.py
```

The final pair of tables proves a limited no-go statement:

**NO-GO.**  Matching sizes and the two families of matching cardinalities
alone do not determine \(H\); the two examples have \(H=+1\) and \(H=-1\).
Both fail the exact \(L/M\)-flag profile, at all 30 flags in the \(k=6\)
model.  They therefore do not contradict (1), and they are not claimed to be
radius-5 extensions.

## 7. What remains open

The global product has now been completely reduced and is exactly \(F(L,M)\).
Accordingly, no further obstruction can come from multiplying all link signs
without retaining more information.  Possible remaining sources of a genuine
obstruction include:

* the individual equations (10) and (17), before their product collapses;
* compatibility of those equations under a change of root;
* higher-order correlations among the completed one-factorizations
  \(\Psi^x\), rather than their total sign product.

No such cross-root or higher-order contradiction is proved here.

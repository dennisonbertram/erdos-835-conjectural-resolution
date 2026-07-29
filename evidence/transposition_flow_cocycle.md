# The transposition-flow cocycle forced by a tight \(17\)-colouring

## Status and scope

This is a **universal necessary condition** for a hypothetical tight
\(17\)-colouring of \(J(32,16)\).  It is not a construction of such a
colouring and not a nonexistence proof.  The exact small-\(k\) control in
the final section shows, in particular, that one nowhere-zero kernel vector
with all of the corresponding rowwise conditions is not by itself enough.

Identify the colour set with \(\mathbb F_{17}\).  Suppose
\[
 g:\binom X{16}\longrightarrow\mathbb F_{17},\qquad |X|=32,
 \tag{1}
\]
is rainbow on every \(15\)-star.  Thus, for every
\(D\in\binom X{15}\), the seventeen values
\[
 \{g(D\cup\{u\}):u\in X\setminus D\}
 \tag{2}
\]
are all the elements of \(\mathbb F_{17}\).

## Universal transposition-flow lemma

For distinct \(x,y\in X\), put \(Z=X\setminus\{x,y\}\).  Define
\[
 a_{xy}:\binom Z{15}\longrightarrow\mathbb F_{17},\qquad
 a_{xy}(B)=g(B\cup\{x\})-g(B\cup\{y\}).
 \tag{3}
\]
Let \(W=W_{14,15}(30)\) be the \(0,1\) inclusion matrix whose rows are
the \(14\)-subsets of \(Z\), whose columns are the \(15\)-subsets, and
whose \((C,B)\)-entry is \(1\) exactly when \(C\subset B\).

Then every hypothetical colouring (1) forces the following simultaneous
identities.

1. **Full support and reversal.**
   \[
   a_{xy}(B)\ne0,\qquad a_{yx}=-a_{xy}.
   \tag{4}
   \]

2. **Top-kernel equation.**
   \[
   Wa_{xy}=0;
   \quad\text{equivalently}\quad
   \sum_{z\in Z\setminus C}a_{xy}(C\cup\{z\})=0
   \tag{5}
   \]
   for every \(C\in\binom Z{14}\).

3. **Exact row-derangement form.**  For each such \(C\), set
   \[
   s_C=g(C\cup\{x,y\}),\quad
   \alpha_z=g(C\cup\{x,z\}),\quad
   \beta_z=g(C\cup\{y,z\})
   \tag{6}
   \]
   for \(z\in Z\setminus C\).  Both \(z\mapsto\alpha_z\) and
   \(z\mapsto\beta_z\) are bijections onto
   \(\mathbb F_{17}\setminus\{s_C\}\).  Consequently there is a
   fixed-point-free permutation
   \[
   \pi_C:\mathbb F_{17}\setminus\{s_C\}
          \longrightarrow\mathbb F_{17}\setminus\{s_C\},
   \qquad \pi_C(\alpha_z)=\beta_z,
   \tag{7}
   \]
   and, with \(t=\alpha_z\), the row entries have the signed form
   \[
   a_{xy}(C\cup\{z\})=t-\pi_C(t).
   \tag{8}
   \]

4. **Anti-complementarity.**  If \(B^c=Z\setminus B\), then
   \[
   a_{xy}(B^c)=-a_{xy}(B).
   \tag{9}
   \]

5. **Pointwise Frobenius identities.**
   \[
   a_{xy}^{16}=\mathbf1,\qquad a_{xy}^{17}=a_{xy}.
   \tag{10}
   \]
   These powers are pointwise.  No assertion is made that the intermediate
   powers \(a_{xy}^j\), \(2\le j\le15\), lie in \(\ker W\).

6. **Triangle cocycle.**  For distinct \(x,y,z\) and every
   \(B\in\binom{X\setminus\{x,y,z\}}{15}\),
   \[
   a_{xy}(B)+a_{yz}(B)+a_{zx}(B)=0.
   \tag{11}
   \]
   Here the three flows, originally defined on three different
   \(30\)-point deletion spaces, are restricted to their common domain.

### Proof

The two sets \(B\cup\{x\}\) and \(B\cup\{y\}\) lie in the same
\(15\)-star, so their colours differ.  This proves the first part of
(4); reversal is immediate from (3).

Fix \(C\in\binom Z{14}\).  The star based at \(C\cup\{x\}\) contains
the block \(C\cup\{x,y\}\) of colour \(s_C\), followed by the sixteen
blocks \(C\cup\{x,z\}\), \(z\in Z\setminus C\).  Its colours are all
of \(\mathbb F_{17}\), so the \(\alpha_z\)'s are exactly
\(\mathbb F_{17}\setminus\{s_C\}\).  The star based at
\(C\cup\{y\}\) proves the same assertion for the \(\beta_z\)'s.
Moreover, \(C\cup\{x,z\}\) and \(C\cup\{y,z\}\) share the \(15\)-set
\(C\cup\{z\}\), so \(\alpha_z\ne\beta_z\).  This constructs the
derangement (7) and proves the sign in (8):
\[
 a_{xy}(C\cup\{z\})=\alpha_z-\beta_z=t-\pi_C(t).
 \]
Because a permutation preserves the sum of its domain,
\[
 \sum_{z\in Z\setminus C}a_{xy}(C\cup\{z\})
 =\sum_{t\ne s_C}t-\sum_{t\ne s_C}\pi_C(t)=0.
 \]
This is exactly (5).

Complement closure is automatic for (1).  Indeed, if \(M\) is the
\(15\)-versus-\(16\) inclusion matrix on \(X\) and \(q_r\) is the
indicator of one colour class, then
\[
 Mq_r=\mathbf1,\qquad
 q_r-\frac1{17}\mathbf1\in\ker_{\mathbb Q}M.
 \]
The standard top polytabloids span this kernel.  Complementation acts
on each of them by \((-1)^{16}=1\), hence
\(q_r(A)=q_r(X\setminus A)\) for every colour \(r\).  Therefore
\[
 g(A)=g(X\setminus A).
 \tag{12}
 \]
Now
\[
 X\setminus\bigl((Z\setminus B)\cup\{x\}\bigr)=B\cup\{y\},\qquad
 X\setminus\bigl((Z\setminus B)\cup\{y\}\bigr)=B\cup\{x\}.
 \]
Using (12) in this order gives
\[
 a_{xy}(B^c)=g(B\cup\{y\})-g(B\cup\{x\})=-a_{xy}(B),
 \]
which audits the sign in (9).

Equation (10) follows from (4) and Fermat's theorem in
\(\mathbb F_{17}\).  Finally, (11) is the telescoping identity
\[
 [g(B+x)-g(B+y)]+[g(B+y)-g(B+z)]
 +[g(B+z)-g(B+x)]=0.
 \]
\(\square\)

## Why “top Specht” is exact here

Wilson's diagonal factors for \(W_{14,15}(30)\) are
\[
 \binom{15-j}{14-j}=15-j,\qquad 0\le j\le14.
 \tag{13}
 \]
They are \(15,14,\ldots,1\), all nonzero in \(\mathbb F_{17}\).
Thus \(W\) has full row rank and
\[
 \begin{aligned}
 \dim_{\mathbb F_{17}}\ker W
 &=\binom{30}{15}-\binom{30}{14}\\
 &=155\,117\,520-145\,422\,675\\
 &=9\,694\,845
 =\frac1{16}\binom{30}{15}.
 \end{aligned}
 \tag{14}
 \]

For a pairing
\((u_1,v_1),\ldots,(u_{15},v_{15})\) of \(Z\), the usual top
polytabloid is the function
\[
 h(B)=\prod_{i=1}^{15}
 \bigl(\mathbf1_{u_i\in B}-\mathbf1_{v_i\in B}\bigr).
 \tag{15}
 \]
These functions lie in \(\ker W\), span a module of the dimension in
(14), and therefore identify the kernel with the top Specht module
\(S^{(15,15)}\).  Complementation changes every factor in (15) by
\(-1\), so it acts as \((-1)^{15}=-1\) on this kernel.  Thus (9)
agrees with the entire ambient linear module.  The genuinely nonlinear
requirements are full support, the row derangements, the Frobenius
condition, and simultaneous cocycle compatibility.

## Exact false-\(k=4\) control: one flow is not sufficient

The analogous deletion space for \(k=4\) has six points and the linear
condition is
\[
 W_{2,3}(6)v=0\quad\text{over }\mathbb F_5.
 \tag{16}
 \]
Index the twenty triples of \(\{0,\ldots,5\}\) lexicographically.  The
vector
\[
 \begin{split}
 v={}&(3,4,4,4,\ 4,4,4,1,1,1,\\
      &4,4,4,1,1,1,\ 1,1,1,2)
 \end{split}
 \tag{17}
 \]
has all of the following properties:

- every coordinate is nonzero;
- all fifteen row sums in (16) vanish;
- \(v(B^c)=-v(B)\);
- the only sorted four-entry row multisets are
  \[
  (1,1,4,4),\qquad(3,4,4,4),\qquad(1,1,1,2);
  \tag{18}
  \]
- each multiset in (18) is \( \{t-\pi(t):t\in\mathbb F_5^\times\}\)
  for a derangement of \(\mathbb F_5^\times\).

For the last assertion one may use, respectively,
\[
 \begin{array}{c|rrrr}
 t&1&2&3&4\\ \hline
 \pi_1(t)&2&1&4&3\\
 \pi_2(t)&2&3&4&1\\
 \pi_3(t)&4&1&2&3
 \end{array}
 \tag{19}
 \]
and sort the four differences modulo \(5\).  Normalizing the omitted
row colour to \(0\) causes no loss, because translating both the domain
and image of a row permutation leaves all differences unchanged.

This control does **not** supply globally consistent \(\alpha\)- and
\(\beta\)-labels, a compatible family of pair flows, the triangle
cocycles, or a \(5\)-colouring of \(J(8,4)\) (which does not exist).
It only proves that the conditions visible in one pair flow, even with
every row multiset individually realizable, do not detect the false
case.  At \(k=16\), any contradiction must therefore use additional
simultaneous compatibility among the \(496=\binom{32}{2}\) unoriented
pair flows and their overlapping row derangements/cocycles.

## Reproducibility

Run

```text
python3 -B evidence/verify_transposition_flow_cocycle.py
```

The script uses only exact integer and finite-field arithmetic.  It does
not allocate the enormous \(W_{14,15}(30)\) matrix.
